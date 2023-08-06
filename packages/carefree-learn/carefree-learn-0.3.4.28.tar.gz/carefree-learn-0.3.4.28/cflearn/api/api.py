import os
import sys
import json
import shutil

from typing import Any
from typing import Dict
from typing import List
from typing import Type
from typing import Union
from typing import Callable
from typing import Optional
from typing import NamedTuple
from cftool.misc import print_info
from cftool.misc import random_hash
from cftool.misc import update_dict
from cftool.misc import parse_config
from cftool.misc import print_warning
from cftool.misc import get_latest_workplace
from cftool.types import np_dict_type
from cftool.types import tensor_dict_type

from ..models import *
from .cv.pipeline import CVPipeline
from .ml.api import repeat_with
from .ml.api import RepeatResult
from .ml.pipeline import MLConfig
from .ml.pipeline import MLPipeline
from .ml.pipeline import MLCarefreePipeline
from .cv.models.diffusion import ldm as _ldm
from .cv.models.diffusion import ldm_vq as _ldm_vq
from .cv.models.diffusion import ldm_sd as _ldm_sd
from .cv.models.diffusion import ldm_sd_v2 as _ldm_sd_v2
from .cv.models.diffusion import ldm_sd_v2_base as _ldm_sd_v2_base
from .cv.models.diffusion import ldm_sr as _ldm_sr
from .cv.models.diffusion import ldm_sd_anime as _ldm_sd_anime
from .cv.models.diffusion import ldm_semantic as _ldm_semantic
from .cv.models.diffusion import ldm_celeba_hq as _ldm_celeba_hq
from .cv.models.diffusion import ldm_inpainting as _ldm_inpainting
from .cv.models.diffusion import ldm_sd_version as _ldm_sd_version
from .cv.models.diffusion import ldm_sd_inpainting as _ldm_sd_inpainting
from .cv.models.translator import esr as _esr
from .cv.models.translator import esr_anime as _esr_anime
from ..data import MLData
from ..data import IMLData
from ..data import CVDataModule
from ..data import MLCarefreeData
from ..types import data_type
from ..types import configs_type
from ..types import general_config_type
from ..types import sample_weights_type
from ..types import states_callback_type
from ..schema import loss_dict
from ..schema import metric_dict
from ..schema import ILoss
from ..schema import IDLModel
from ..schema import _IMetric
from ..schema import IDataLoader
from ..schema import DLConfig
from ..trainer import get_sorted_checkpoints
from ..pipeline import DLPipeline
from ..pipeline import ModelSoupConfigs
from ..constants import SCORES_FILE
from ..constants import DEFAULT_ZOO_TAG
from ..constants import CHECKPOINTS_FOLDER
from ..zoo.core import _parse_config
from ..zoo.core import configs_root
from ..zoo.core import DLZoo
from ..dist.ml import Experiment
from ..misc.toolkit import download_model
from ..models.schemas.ml import ml_core_dict


# dl


def make(name: str, config: general_config_type = None) -> DLPipeline:
    m_base: Type[DLPipeline] = DLPipeline.get(name)
    return m_base(m_base.config_base(**parse_config(config)))  # type: ignore


def run_ddp(path: str, cuda_list: List[Union[int, str]], **kwargs: Any) -> None:
    def _convert_config() -> str:
        return " ".join([f"--{k}={v}" for k, v in kwargs.items()])

    os.environ["CUDA_VISIBLE_DEVICES"] = ",".join(map(str, cuda_list))
    kwargs["nproc_per_node"] = len(cuda_list)
    prefix = f"{sys.executable} -m torch.distributed.run "
    os.system(f"{prefix}{_convert_config()} {path}")


def run_multiple(
    path: str,
    model_name: str,
    cuda_list: Optional[List[Union[int, str]]],
    *,
    num_jobs: int = 2,
    num_multiple: int = 5,
    workplace: str = "_multiple",
    resource_config: Optional[Dict[str, Any]] = None,
    is_fix: bool = False,
    task_meta_fn: Optional[Callable[[int], Any]] = None,
    temp_folder: Optional[str] = None,
) -> None:
    def is_buggy(i_: int) -> bool:
        i_workplace = os.path.join(workplace, model_name, str(i_))
        i_latest_workplace = get_latest_workplace(i_workplace)
        if i_latest_workplace is None:
            return True
        checkpoint_folder = os.path.join(i_latest_workplace, CHECKPOINTS_FOLDER)
        if not os.path.isfile(os.path.join(checkpoint_folder, SCORES_FILE)):
            return True
        if not get_sorted_checkpoints(checkpoint_folder):
            return True
        return False

    if num_jobs <= 1:
        raise ValueError("`num_jobs` should greater than 1")
    # remove workplace if exists
    if os.path.isdir(workplace) and not is_fix:
        print_warning(f"'{workplace}' already exists, it will be erased")
        shutil.rmtree(workplace)
    # generate temporary runtime script
    with open(path, "r") as rf:
        original_scripts = rf.read()
    if temp_folder is None:
        temp_folder = os.path.split(os.path.abspath(path))[0]
    tmp_path = os.path.join(temp_folder, f"{random_hash()}.py")
    with open(tmp_path, "w") as wf:
        wf.write(
            f"""
import os
from cflearn.misc.toolkit import _set_environ_workplace
from cflearn.dist.ml.runs._utils import get_info
from cflearn.parameters import OPT

info = get_info(requires_data=False)
os.environ["CUDA_VISIBLE_DEVICES"] = str(info.meta["cuda"])
_set_environ_workplace(info.meta["workplace"])
OPT.meta_settings = info.meta

{original_scripts}
"""
        )
    print_info(f"`{tmp_path}` will be executed")
    # construct & execute an Experiment
    cudas = None if cuda_list is None else list(map(int, cuda_list))
    experiment = Experiment(
        num_jobs=num_jobs,
        available_cuda_list=cudas,
        resource_config=resource_config,
    )
    for i in range(num_multiple):
        if is_fix and not is_buggy(i):
            continue
        if task_meta_fn is None:
            i_meta_kw = {}
        else:
            i_meta_kw = task_meta_fn(i)
        if not is_fix:
            workplace_key = None
        else:
            workplace_key = model_name, str(i)
        experiment.add_task(
            model=model_name,
            root_workplace=workplace,
            workplace_key=workplace_key,
            run_command=f"{sys.executable} {tmp_path}",
            task_meta_kwargs=i_meta_kw,
        )
    experiment.run_tasks(use_tqdm=False)
    os.remove(tmp_path)


def pack(
    workplace: str,
    *,
    step: Optional[str] = None,
    config_bundle_callback: Optional[Callable[[Dict[str, Any]], Any]] = None,
    pack_folder: Optional[str] = None,
    cuda: Optional[Union[int, str]] = None,
    compress: bool = True,
    # model soup
    model_soup_loader: Optional[IDataLoader] = None,
    model_soup_metric_names: Optional[Union[str, List[str]]] = None,
    model_soup_metric_configs: configs_type = None,
    model_soup_metric_weights: Optional[Dict[str, float]] = None,
    model_soup_valid_portion: float = 1.0,
    model_soup_strategy: str = "greedy",
    model_soup_states_callback: states_callback_type = None,
    model_soup_verbose: bool = True,
) -> str:
    cls = DLPipeline.get_base(workplace)
    if model_soup_loader is None or model_soup_metric_names is None:
        model_soup_configs = None
    else:
        model_soup_configs = ModelSoupConfigs(
            model_soup_loader,
            model_soup_metric_names,
            model_soup_metric_configs,
            model_soup_metric_weights,
            model_soup_valid_portion,
            model_soup_strategy,
            model_soup_states_callback,
            model_soup_verbose,
        )
    return cls.pack(
        workplace,
        step=step,
        config_bundle_callback=config_bundle_callback,
        pack_folder=pack_folder,
        cuda=cuda,
        compress=compress,
        model_soup_configs=model_soup_configs,
    )


def load(
    export_folder: str,
    *,
    cuda: Optional[Union[int, str]] = None,
    compress: bool = True,
    states_callback: states_callback_type = None,
    pre_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    post_callback: Optional[Callable[[DLPipeline, Dict[str, Any]], None]] = None,
    strict: bool = True,
) -> DLPipeline:
    return DLPipeline.load(
        export_folder,
        cuda=cuda,
        compress=compress,
        states_callback=states_callback,
        pre_callback=pre_callback,
        post_callback=post_callback,
        strict=strict,
    )


def load_data_info(export_folder: str, *, compress: bool = True) -> Dict[str, Any]:
    return DLPipeline.load_data_info(export_folder, compress=compress)


def pack_onnx(
    workplace: str,
    export_folder: str,
    dynamic_axes: Optional[Union[List[int], Dict[int, str]]] = None,
    *,
    input_sample: tensor_dict_type,
    step: Optional[str] = None,
    config_bundle_callback: Optional[Callable[[Dict[str, Any]], Any]] = None,
    pack_folder: Optional[str] = None,
    states_callback: states_callback_type = None,
    pre_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    post_callback: Optional[Callable[[DLPipeline, Dict[str, Any]], None]] = None,
    onnx_file: str = "model.onnx",
    opset: int = 11,
    simplify: bool = True,
    num_samples: Optional[int] = None,
    verbose: bool = True,
    **kwargs: Any,
) -> DLPipeline:
    cls = DLPipeline.get_base(workplace)
    return cls.pack_onnx(
        workplace,
        export_folder,
        dynamic_axes,
        step=step,
        config_bundle_callback=config_bundle_callback,
        pack_folder=pack_folder,
        states_callback=states_callback,
        pre_callback=pre_callback,
        post_callback=post_callback,
        onnx_file=onnx_file,
        opset=opset,
        simplify=simplify,
        input_sample=input_sample,
        num_samples=num_samples,
        verbose=verbose,
        **kwargs,
    )


def from_json(d: Union[str, Dict[str, Any]]) -> DLPipeline:
    return DLPipeline.from_json(d)


def make_model(name: str, **kwargs: Any) -> IDLModel:
    return IDLModel.make(name, kwargs)


def make_loss(name: str, **kwargs: Any) -> ILoss:
    return ILoss.make(name, kwargs)


def make_metric(name: str, **kwargs: Any) -> _IMetric:
    return _IMetric.make(name, kwargs)


class ModelItem(NamedTuple):
    name: str
    requirements: Dict[str, Any]


def model_zoo(*, verbose: bool = False) -> List[ModelItem]:
    def _squeeze_requirements(req: Dict[str, Any], d: Dict[str, Any]) -> None:
        for k, v in req.items():
            kd = d.get(k)
            if kd is None:
                continue
            if isinstance(v, dict):
                _squeeze_requirements(v, kd)
                continue
            assert isinstance(v, list)
            pop_indices = []
            for i, vv in enumerate(v):
                if vv in kd:
                    pop_indices.append(i)
            for i in pop_indices[::-1]:
                v.pop(i)

    models = []
    for task in sorted(os.listdir(configs_root)):
        if task == "common_":
            continue
        task_folder = os.path.join(configs_root, task)
        for model in sorted(os.listdir(task_folder)):
            model_folder = os.path.join(task_folder, model)
            for config_file in sorted(os.listdir(model_folder)):
                config_path = os.path.join(model_folder, config_file)
                d = _parse_config(config_path)
                requirements = d.pop("__requires__", {})
                _squeeze_requirements(requirements, d)
                tag = os.path.splitext(config_file)[0]
                name = f"{task}/{model}"
                if tag != DEFAULT_ZOO_TAG:
                    name = f"{name}.{tag}"
                models.append(ModelItem(name, requirements))
    if verbose:

        def _stringify_item(item: ModelItem) -> str:
            return f"{item.name:>{span}s}   |   {json.dumps(item.requirements)}"

        span = 42
        print(
            "\n".join(
                [
                    "=" * 120,
                    f"{'Names':>{span}s}   |   Requirements",
                    "-" * 120,
                    "\n".join(map(_stringify_item, models)),
                    "-" * 120,
                ]
            )
        )
    return models


def from_zoo(
    model: str,
    *,
    build: bool = True,
    return_model: bool = False,
    **kwargs: Any,
) -> Union[IDLModel, DLPipeline]:
    if return_model and not build:
        raise ValueError("`build` should be True when `return_model` is True")
    kwargs["build"] = build
    fn = DLZoo.load_model if return_model else DLZoo.load_pipeline
    return fn(model, **kwargs)  # type: ignore


def supported_losses() -> List[str]:
    return sorted(loss_dict)


def supported_metrics() -> List[str]:
    return sorted(metric_dict)


# ml


def _make_ml_data(
    x_train: Union[data_type, IMLData],
    y_train: data_type = None,
    x_valid: data_type = None,
    y_valid: data_type = None,
    train_others: Optional[np_dict_type] = None,
    valid_others: Optional[np_dict_type] = None,
    carefree: bool = False,
    is_classification: Optional[bool] = None,
    data_config: Optional[Dict[str, Any]] = None,
    cf_data_config: Optional[Dict[str, Any]] = None,
) -> IMLData:
    if isinstance(x_train, IMLData):
        x_train.is_classification = is_classification
        return x_train
    data_kwargs: Dict[str, Any] = {
        "is_classification": is_classification,
        "train_others": train_others,
        "valid_others": valid_others,
    }
    if carefree:
        data_kwargs["cf_data_config"] = cf_data_config
    update_dict(data_config or {}, data_kwargs)
    args = x_train, y_train, x_valid, y_valid
    fn = MLCarefreeData.make_with if carefree else MLData
    return fn(*args, **data_kwargs)  # type: ignore


def fit_ml(
    x_train: Union[data_type, IMLData],
    y_train: data_type = None,
    x_valid: data_type = None,
    y_valid: data_type = None,
    *,
    # pipeline
    config: Optional[MLConfig] = None,
    debug: bool = False,
    # data
    train_others: Optional[np_dict_type] = None,
    valid_others: Optional[np_dict_type] = None,
    carefree: bool = False,
    is_classification: Optional[bool] = None,
    data_config: Optional[Dict[str, Any]] = None,
    cf_data_config: Optional[Dict[str, Any]] = None,
    # fit
    sample_weights: sample_weights_type = None,
    cuda: Optional[Union[int, str]] = None,
) -> MLPipeline:
    config = config or MLConfig()
    if debug:
        config.to_debug()
    fit_kwargs = dict(sample_weights=sample_weights, cuda=cuda)
    m_base = MLCarefreePipeline if carefree else MLPipeline
    data = _make_ml_data(
        x_train,
        y_train,
        x_valid,
        y_valid,
        train_others,
        valid_others,
        carefree,
        is_classification,
        data_config,
        cf_data_config,
    )
    return m_base(config).fit(data, **fit_kwargs)  # type: ignore


def repeat_ml(
    x_train: Union[data_type, IMLData],
    y_train: data_type = None,
    x_valid: data_type = None,
    y_valid: data_type = None,
    *,
    num_jobs: int = 1,
    num_repeat: int = 5,
    train_others: Optional[np_dict_type] = None,
    valid_others: Optional[np_dict_type] = None,
    # repeat
    workplace: str = "_repeat",
    models: Union[str, List[str]] = "fcnn",
    model_configs: Optional[Dict[str, Dict[str, Any]]] = None,
    predict_config: Optional[Dict[str, Any]] = None,
    sequential: Optional[bool] = None,
    return_patterns: bool = True,
    compress: bool = True,
    use_tqdm: bool = True,
    cuda: Optional[Union[int, str]] = None,
    available_cuda_list: Optional[List[int]] = None,
    resource_config: Optional[Dict[str, Any]] = None,
    task_meta_kwargs: Optional[Dict[str, Any]] = None,
    to_original_device: bool = False,
    is_fix: bool = False,
    # data
    carefree: bool = False,
    is_classification: Optional[bool] = None,
    data_config: Optional[Dict[str, Any]] = None,
    cf_data_config: Optional[Dict[str, Any]] = None,
    # pipeline
    config: Optional[MLConfig] = None,
    debug: bool = False,
    # fit
    sample_weights: sample_weights_type = None,
) -> RepeatResult:
    config = config or MLConfig()
    if debug:
        config.to_debug()
    return repeat_with(
        _make_ml_data(
            x_train,
            y_train,
            x_valid,
            y_valid,
            train_others,
            valid_others,
            carefree,
            is_classification,
            data_config,
            cf_data_config,
        ),
        config,
        carefree=carefree,
        workplace=workplace,
        models=models,
        model_configs=model_configs,
        predict_config=predict_config,
        sample_weights=sample_weights,
        sequential=sequential,
        num_jobs=num_jobs,
        num_repeat=num_repeat,
        return_patterns=return_patterns,
        compress=compress,
        use_tqdm=use_tqdm,
        cuda=cuda,
        available_cuda_list=available_cuda_list,
        resource_config=resource_config,
        task_meta_kwargs=task_meta_kwargs,
        to_original_device=to_original_device,
        is_fix=is_fix,
    )


def supported_ml_models() -> List[str]:
    return sorted(ml_core_dict)


# cv


def fit_cv(
    data: CVDataModule,
    config: DLConfig,
    *,
    debug: bool = False,
    sample_weights: sample_weights_type = None,
    cuda: Optional[Union[int, str]] = None,
) -> "CVPipeline":
    if debug:
        config.to_debug()
    fit_kwargs = dict(sample_weights=sample_weights, cuda=cuda)
    return CVPipeline(config).fit(data, **fit_kwargs)  # type: ignore


# clf


def _clf(
    model: str,
    num_classes: int,
    aux_num_classes: Optional[Dict[str, int]],
    pretrained_name: Optional[str],
    img_size: Optional[int],
    return_model: bool = False,
    **kwargs: Any,
) -> Any:
    if img_size is not None:
        kwargs["img_size"] = img_size
    kwargs["num_classes"] = num_classes
    if pretrained_name is not None:
        model_config = kwargs.setdefault("model_config", {})
        model_config["encoder1d_pretrained_name"] = pretrained_name
    model = f"clf/{model}"
    fn = DLZoo.load_model if return_model else DLZoo.load_pipeline
    if aux_num_classes is None:
        return fn(model, **kwargs)  # type: ignore
    config = DLZoo(model, **kwargs).config
    aux_labels = sorted(aux_num_classes)
    loss_name = config["loss_name"]
    config["loss_name"] = f"{loss_name}:aux:{','.join(aux_labels)}"
    metric_names = config.setdefault("metric_names", [])
    metric_configs = config.setdefault("metric_configs", {})
    if isinstance(metric_configs, dict):
        metric_configs = [metric_configs.get(name, {}) for name in metric_names]
    for label in aux_labels:
        metric_names.append("aux")
        metric_configs.append({"key": label, "base": "acc"})
    config["metric_configs"] = metric_configs
    model_config = config.setdefault("model_config", {})
    model_config["aux_num_classes"] = aux_num_classes
    return fn(model, **config)  # type: ignore


def cct(
    img_size: int,
    num_classes: int,
    aux_num_classes: Optional[Dict[str, int]] = None,
    **kwargs: Any,
) -> DLPipeline:
    return _clf("cct", num_classes, aux_num_classes, None, img_size, **kwargs)


def cct_model(
    img_size: int,
    num_classes: int,
    aux_num_classes: Optional[Dict[str, int]] = None,
    **kwargs: Any,
) -> VanillaClassifier:
    return _clf("cct", num_classes, aux_num_classes, None, img_size, True, **kwargs)


def cct_lite(
    img_size: int,
    num_classes: int,
    aux_num_classes: Optional[Dict[str, int]] = None,
    **kwargs: Any,
) -> DLPipeline:
    return _clf("cct.lite", num_classes, aux_num_classes, None, img_size, **kwargs)


def cct_lite_model(
    img_size: int,
    num_classes: int,
    aux_num_classes: Optional[Dict[str, int]] = None,
    **kwargs: Any,
) -> VanillaClassifier:
    return _clf(
        "cct.lite",
        num_classes,
        aux_num_classes,
        None,
        img_size,
        True,
        **kwargs,
    )


def cct_large(
    img_size: int,
    num_classes: int,
    aux_num_classes: Optional[Dict[str, int]] = None,
    **kwargs: Any,
) -> DLPipeline:
    return _clf("cct.large", num_classes, aux_num_classes, None, img_size, **kwargs)


def cct_large_model(
    img_size: int,
    num_classes: int,
    aux_num_classes: Optional[Dict[str, int]] = None,
    **kwargs: Any,
) -> VanillaClassifier:
    return _clf(
        "cct.large",
        num_classes,
        aux_num_classes,
        None,
        img_size,
        True,
        **kwargs,
    )


def cct_large_224(
    num_classes: int,
    aux_num_classes: Optional[Dict[str, int]] = None,
    *,
    pretrained: bool = True,
    **kwargs: Any,
) -> DLPipeline:
    pretrained_name = "cct_large_224" if pretrained else None
    return _clf(
        "cct.large_224",
        num_classes,
        aux_num_classes,
        pretrained_name,
        None,
        **kwargs,
    )


def cct_large_224_model(
    num_classes: int,
    aux_num_classes: Optional[Dict[str, int]] = None,
    *,
    pretrained: bool = True,
    **kwargs: Any,
) -> VanillaClassifier:
    pretrained_name = "cct_large_224" if pretrained else None
    return _clf(
        "cct.large_224",
        num_classes,
        aux_num_classes,
        pretrained_name,
        None,
        True,
        **kwargs,
    )


def cct_large_384(
    num_classes: int,
    aux_num_classes: Optional[Dict[str, int]] = None,
    *,
    pretrained: bool = True,
    **kwargs: Any,
) -> DLPipeline:
    pretrained_name = "cct_large_384" if pretrained else None
    return _clf(
        "cct.large_384",
        num_classes,
        aux_num_classes,
        pretrained_name,
        None,
        **kwargs,
    )


def cct_large_384_model(
    num_classes: int,
    aux_num_classes: Optional[Dict[str, int]] = None,
    *,
    pretrained: bool = True,
    **kwargs: Any,
) -> VanillaClassifier:
    pretrained_name = "cct_large_384" if pretrained else None
    return _clf(
        "cct.large_384",
        num_classes,
        aux_num_classes,
        pretrained_name,
        None,
        True,
        **kwargs,
    )


def resnet18(num_classes: int, pretrained: bool = True, **kwargs: Any) -> DLPipeline:
    kwargs["num_classes"] = num_classes
    model_config = kwargs.setdefault("model_config", {})
    encoder1d_config = model_config.setdefault("encoder1d_config", {})
    encoder1d_config["pretrained"] = pretrained
    return DLZoo.load_pipeline("clf/resnet18", **kwargs)


def resnet18_model(
    num_classes: int,
    *,
    pretrained: bool = False,
    **kwargs: Any,
) -> VanillaClassifier:
    kwargs["num_classes"] = num_classes
    model_config = kwargs.setdefault("model_config", {})
    encoder1d_config = model_config.setdefault("encoder1d_config", {})
    encoder1d_config["pretrained"] = pretrained
    return DLZoo.load_model("clf/resnet18", **kwargs)


def resnet18_gray(num_classes: int, **kwargs: Any) -> DLPipeline:
    kwargs["num_classes"] = num_classes
    return DLZoo.load_pipeline("clf/resnet18.gray", **kwargs)


def resnet50(num_classes: int, pretrained: bool = True, **kwargs: Any) -> DLPipeline:
    kwargs["num_classes"] = num_classes
    model_config = kwargs.setdefault("model_config", {})
    encoder1d_config = model_config.setdefault("encoder1d_config", {})
    encoder1d_config["pretrained"] = pretrained
    return DLZoo.load_pipeline("clf/resnet50", **kwargs)


def resnet50_model(
    num_classes: int,
    *,
    pretrained: bool = False,
    **kwargs: Any,
) -> VanillaClassifier:
    kwargs["num_classes"] = num_classes
    model_config = kwargs.setdefault("model_config", {})
    encoder1d_config = model_config.setdefault("encoder1d_config", {})
    encoder1d_config["pretrained"] = pretrained
    return DLZoo.load_model("clf/resnet50", **kwargs)


def resnet50_gray(num_classes: int, **kwargs: Any) -> DLPipeline:
    kwargs["num_classes"] = num_classes
    return DLZoo.load_pipeline("clf/resnet50.gray", **kwargs)


def resnet101(num_classes: int, pretrained: bool = True, **kwargs: Any) -> DLPipeline:
    kwargs["num_classes"] = num_classes
    model_config = kwargs.setdefault("model_config", {})
    encoder1d_config = model_config.setdefault("encoder1d_config", {})
    encoder1d_config["pretrained"] = pretrained
    return DLZoo.load_pipeline("clf/resnet101", **kwargs)


def resnet101_model(
    num_classes: int,
    *,
    pretrained: bool = False,
    **kwargs: Any,
) -> VanillaClassifier:
    kwargs["num_classes"] = num_classes
    model_config = kwargs.setdefault("model_config", {})
    encoder1d_config = model_config.setdefault("encoder1d_config", {})
    encoder1d_config["pretrained"] = pretrained
    return DLZoo.load_model("clf/resnet101", **kwargs)


# gan


def vanilla_gan(img_size: int, **kwargs: Any) -> DLPipeline:
    kwargs["img_size"] = img_size
    return DLZoo.load_pipeline("gan/vanilla", **kwargs)


def vanilla_gan_gray(img_size: int, **kwargs: Any) -> DLPipeline:
    kwargs["img_size"] = img_size
    return DLZoo.load_pipeline("gan/vanilla.gray", **kwargs)


def siren_gan(img_size: int, **kwargs: Any) -> DLPipeline:
    kwargs["img_size"] = img_size
    return DLZoo.load_pipeline("gan/siren", **kwargs)


def siren_gan_gray(img_size: int, **kwargs: Any) -> DLPipeline:
    kwargs["img_size"] = img_size
    return DLZoo.load_pipeline("gan/siren.gray", **kwargs)


# generator


def pixel_cnn(num_classes: int, **kwargs: Any) -> DLPipeline:
    kwargs["num_classes"] = num_classes
    return DLZoo.load_pipeline("generator/pixel_cnn", **kwargs)


# multimodal


def clip(pretrained: bool = True, **kwargs: Any) -> DLPipeline:
    return DLZoo.load_pipeline("multimodal/clip", pretrained=pretrained, **kwargs)


def clip_model(pretrained: bool = True, **kwargs: Any) -> CLIP:
    return DLZoo.load_model("multimodal/clip", pretrained=pretrained, **kwargs)


def clip_large(pretrained: bool = True, **kwargs: Any) -> DLPipeline:
    return DLZoo.load_pipeline("multimodal/clip.large", pretrained=pretrained, **kwargs)


def clip_large_model(pretrained: bool = True, **kwargs: Any) -> CLIP:
    return DLZoo.load_model("multimodal/clip.large", pretrained=pretrained, **kwargs)


def chinese_clip(pretrained: bool = True, **kwargs: Any) -> DLPipeline:
    model = "multimodal/clip.chinese"
    return DLZoo.load_pipeline(model, pretrained=pretrained, **kwargs)


def chinese_clip_model(pretrained: bool = True, **kwargs: Any) -> CLIP:
    model = "multimodal/clip.chinese"
    return DLZoo.load_model(model, pretrained=pretrained, **kwargs)


def open_clip_ViT_H_14(pretrained: bool = True, **kwargs: Any) -> DLPipeline:
    model = "multimodal/clip.open_clip_ViT_H_14"
    return DLZoo.load_pipeline(model, pretrained=pretrained, **kwargs)


def open_clip_ViT_H_14_model(pretrained: bool = True, **kwargs: Any) -> CLIP:
    model = "multimodal/clip.open_clip_ViT_H_14"
    return DLZoo.load_model(model, pretrained=pretrained, **kwargs)


def clip_vqgan_aligner(**kwargs: Any) -> DLPipeline:
    return DLZoo.load_pipeline("multimodal/clip_vqgan_aligner", **kwargs)


# segmentor


def aim() -> DLPipeline:
    return DLZoo.load_pipeline("segmentor/aim")


def aim_model() -> IDLModel:
    return DLZoo.load_model("segmentor/aim")


def u2net(pretrained: bool = False, **kwargs: Any) -> DLPipeline:
    return DLZoo.load_pipeline("segmentor/u2net", pretrained=pretrained, **kwargs)


def u2net_model(pretrained: bool = False, **kwargs: Any) -> IDLModel:
    return DLZoo.load_model("segmentor/u2net", pretrained=pretrained, **kwargs)


def u2net_lite(pretrained: bool = False, **kwargs: Any) -> DLPipeline:
    return DLZoo.load_pipeline("segmentor/u2net.lite", pretrained=pretrained, **kwargs)


def u2net_lite_model(pretrained: bool = False, **kwargs: Any) -> IDLModel:
    return DLZoo.load_model("segmentor/u2net.lite", pretrained=pretrained, **kwargs)


def u2net_finetune(ckpt: Optional[str] = None, **kwargs: Any) -> DLPipeline:
    if ckpt is None:
        ckpt = download_model("u2net")
    kwargs["pretrained_ckpt"] = ckpt
    return DLZoo.load_pipeline("segmentor/u2net.finetune", **kwargs)


def u2net_lite_finetune(ckpt: Optional[str] = None, **kwargs: Any) -> DLPipeline:
    if ckpt is None:
        ckpt = download_model("u2net.lite")
    kwargs["pretrained_ckpt"] = ckpt
    return DLZoo.load_pipeline("segmentor/u2net.finetune_lite", **kwargs)


def u2net_refine(lv1_model_ckpt_path: str, **kwargs: Any) -> DLPipeline:
    kwargs["lv1_model_ckpt_path"] = lv1_model_ckpt_path
    return DLZoo.load_pipeline("segmentor/u2net.refine", **kwargs)


def u2net_lite_refine(lv1_model_ckpt_path: str, **kwargs: Any) -> DLPipeline:
    kwargs["lv1_model_ckpt_path"] = lv1_model_ckpt_path
    return DLZoo.load_pipeline("segmentor/u2net.refine_lite", **kwargs)


# ssl


def dino(img_size: int, **kwargs: Any) -> DLPipeline:
    kwargs["img_size"] = img_size
    return DLZoo.load_pipeline("ssl/dino", **kwargs)


def dino_gray(img_size: int, **kwargs: Any) -> DLPipeline:
    model_config = kwargs.setdefault("model_config", {})
    encoder1d_config = model_config.setdefault("encoder1d_config", {})
    encoder1d_config["in_channels"] = 1
    return dino(img_size, **kwargs)


# style transfer


def adain(pretrained: bool = False, **kwargs: Any) -> DLPipeline:
    kwargs["pretrained"] = pretrained
    return DLZoo.load_pipeline("style_transfer/adain", **kwargs)


# ae


def ae_kl_f4(size: int = 256, pretrained: bool = True, **kwargs: Any) -> DLPipeline:
    if pretrained and size != 256:
        raise ValueError("pretrained `ae_kl_f4` should have `size`=256")
    kwargs["img_size"] = size
    kwargs["pretrained"] = pretrained
    return DLZoo.load_pipeline("ae/kl.f4", **kwargs)


def ae_kl_f8(size: int = 256, pretrained: bool = True, **kwargs: Any) -> DLPipeline:
    if pretrained and size != 256:
        raise ValueError("pretrained `ae_kl_f8` should have `size`=256")
    kwargs["img_size"] = size
    kwargs["pretrained"] = pretrained
    return DLZoo.load_pipeline("ae/kl.f8", **kwargs)


def ae_kl_f16(size: int = 256, pretrained: bool = True, **kwargs: Any) -> DLPipeline:
    if pretrained and size != 256:
        raise ValueError("pretrained `ae_kl_f16` should have `size`=256")
    kwargs["img_size"] = size
    kwargs["pretrained"] = pretrained
    return DLZoo.load_pipeline("ae/kl.f16", **kwargs)


def ae_vq_f4(size: int = 256, pretrained: bool = True, **kwargs: Any) -> DLPipeline:
    if pretrained and size != 256:
        raise ValueError("pretrained `ae_vq_f4` should have `size`=256")
    kwargs["img_size"] = size
    kwargs["pretrained"] = pretrained
    return DLZoo.load_pipeline("ae/vq.f4", **kwargs)


def ae_vq_f4_no_attn(
    size: int = 256,
    pretrained: bool = True,
    **kwargs: Any,
) -> DLPipeline:
    if pretrained and size != 256:
        raise ValueError("pretrained `ae_vq_f4_no_attn` should have `size`=256")
    kwargs["img_size"] = size
    kwargs["pretrained"] = pretrained
    return DLZoo.load_pipeline("ae/vq.f4_no_attn", **kwargs)


def ae_vq_f8(size: int = 256, pretrained: bool = True, **kwargs: Any) -> DLPipeline:
    if pretrained and size != 256:
        raise ValueError("pretrained `ae_vq_f8` should have `size`=256")
    kwargs["img_size"] = size
    kwargs["pretrained"] = pretrained
    return DLZoo.load_pipeline("ae/vq.f8", **kwargs)


# vae


def vanilla_vae(img_size: int, **kwargs: Any) -> DLPipeline:
    kwargs["img_size"] = img_size
    return DLZoo.load_pipeline("vae/vanilla", **kwargs)


def vanilla_vae_gray(img_size: int, **kwargs: Any) -> DLPipeline:
    kwargs["img_size"] = img_size
    return DLZoo.load_pipeline("vae/vanilla.gray", **kwargs)


def vanilla_vae2d(img_size: int, **kwargs: Any) -> DLPipeline:
    kwargs["img_size"] = img_size
    return DLZoo.load_pipeline("vae/vanilla.2d", **kwargs)


def vanilla_vae2d_gray(img_size: int, **kwargs: Any) -> DLPipeline:
    kwargs["img_size"] = img_size
    return DLZoo.load_pipeline("vae/vanilla.2d_gray", **kwargs)


def style_vae(img_size: int, **kwargs: Any) -> DLPipeline:
    kwargs["img_size"] = img_size
    return DLZoo.load_pipeline("vae/style", **kwargs)


def style_vae_gray(img_size: int, **kwargs: Any) -> DLPipeline:
    kwargs["img_size"] = img_size
    return DLZoo.load_pipeline("vae/style.gray", **kwargs)


def siren_vae(img_size: int, **kwargs: Any) -> DLPipeline:
    kwargs["img_size"] = img_size
    return DLZoo.load_pipeline("vae/siren", **kwargs)


def siren_vae_gray(img_size: int, **kwargs: Any) -> DLPipeline:
    kwargs["img_size"] = img_size
    return DLZoo.load_pipeline("vae/siren.gray", **kwargs)


def _vq_vae(
    model: str,
    img_size: int,
    num_classes: Optional[int] = None,
    **kwargs: Any,
) -> DLPipeline:
    kwargs["img_size"] = img_size
    if num_classes is not None:
        model_config = kwargs.setdefault("model_config", {})
        num_classes = model_config.setdefault("num_classes", num_classes)
        callback_names = kwargs.get("callback_names")
        if callback_names is None or "vq_vae" in callback_names:
            callback_configs = kwargs.setdefault("callback_configs", {})
            vq_vae_callback_configs = callback_configs.setdefault("vq_vae", {})
            vq_vae_callback_configs.setdefault("num_classes", num_classes)
    return DLZoo.load_pipeline(f"vae/{model}", **kwargs)


def vq_vae(
    img_size: int,
    *,
    num_classes: Optional[int] = None,
    **kwargs: Any,
) -> DLPipeline:
    return _vq_vae("vq", img_size, num_classes, **kwargs)


def vq_vae_gray(
    img_size: int,
    *,
    num_classes: Optional[int] = None,
    **kwargs: Any,
) -> DLPipeline:
    return _vq_vae("vq.gray", img_size, num_classes, **kwargs)


def vq_vae_lite(
    img_size: int,
    *,
    num_classes: Optional[int] = None,
    **kwargs: Any,
) -> DLPipeline:
    return _vq_vae("vq.lite", img_size, num_classes, **kwargs)


def vq_vae_gray_lite(
    img_size: int,
    *,
    num_classes: Optional[int] = None,
    **kwargs: Any,
) -> DLPipeline:
    return _vq_vae("vq.gray_lite", img_size, num_classes, **kwargs)


# diffusion


def ddpm(img_size: int = 256, **kwargs: Any) -> DLPipeline:
    kwargs["img_size"] = img_size
    return DLZoo.load_pipeline("diffusion/ddpm", **kwargs)


def ldm(
    latent_size: int = 32,
    latent_in_channels: int = 4,
    latent_out_channels: int = 4,
    **kwargs: Any,
) -> DLPipeline:
    return _ldm(latent_size, latent_in_channels, latent_out_channels, **kwargs)


def ldm_vq(
    latent_size: int = 64,
    latent_in_channels: int = 3,
    latent_out_channels: int = 3,
    **kwargs: Any,
) -> DLPipeline:
    return _ldm_vq(latent_size, latent_in_channels, latent_out_channels, **kwargs)


def ldm_sd(pretrained: bool = True) -> DLPipeline:
    return _ldm_sd(pretrained)


def ldm_sd_version(version: str, pretrained: bool = True) -> DLPipeline:
    return _ldm_sd_version(version, pretrained)


def ldm_sd_anime(pretrained: bool = True) -> DLPipeline:
    return _ldm_sd_anime(pretrained)


def ldm_sd_inpainting(pretrained: bool = True) -> DLPipeline:
    return _ldm_sd_inpainting(pretrained)


def ldm_sd_v2(pretrained: bool = True) -> DLPipeline:
    return _ldm_sd_v2(pretrained)


def ldm_sd_v2_base(pretrained: bool = True) -> DLPipeline:
    return _ldm_sd_v2_base(pretrained)


def ldm_celeba_hq(pretrained: bool = True) -> DLPipeline:
    return _ldm_celeba_hq(pretrained)


def ldm_inpainting(pretrained: bool = True) -> DLPipeline:
    return _ldm_inpainting(pretrained)


def ldm_sr(pretrained: bool = True) -> DLPipeline:
    return _ldm_sr(pretrained)


def ldm_semantic(pretrained: bool = True) -> DLPipeline:
    return _ldm_semantic(pretrained)


# sr


def esr(pretrained: bool = True) -> DLPipeline:
    return _esr(pretrained)


def esr_anime(pretrained: bool = True) -> DLPipeline:
    return _esr_anime(pretrained)


# nlp


def hugging_face(model: str) -> DLPipeline:
    return DLZoo.load_pipeline("hugging_face/general", model_config={"model": model})


def hugging_face_model(model: str) -> HuggingFaceModel:
    return DLZoo.load_model("hugging_face/general", model_config={"model": model})


def simbert_model() -> SimBERT:
    return DLZoo.load_model("hugging_face/simbert")


def opus_model(src: str, tgt: str) -> OPUSBase:
    return DLZoo.load_model("hugging_face/opus", model_config={"src": src, "tgt": tgt})


def opus_zh_en_model() -> OPUS_ZH_EN:
    return opus_model("zh", "en")
