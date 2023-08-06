import os
import json
import torch

from abc import ABC
from typing import Any
from typing import Dict
from typing import List
from typing import Type
from typing import Union
from typing import Optional
from typing import NamedTuple
from cftool.misc import update_dict
from cftool.misc import print_warning
from cftool.misc import shallow_copy_dict
from cftool.types import tensor_dict_type

from .models import dl_zoo_model_loaders
from ..schema import IDLModel
from ..pipeline import DLPipeline
from ..pipeline import IPipeline
from ..constants import DEFAULT_ZOO_TAG
from ..misc.toolkit import download_model


root = os.path.dirname(__file__)
configs_root = os.path.join(root, "configs")


class ParsedModel(NamedTuple):
    json_path: str
    download_name: str


def _parse_model(model: str) -> ParsedModel:
    tag = DEFAULT_ZOO_TAG
    model_type, model_name = model.split("/")
    download_name = model_name
    if "." in model_name:
        model_name, tag = model_name.split(".")
    json_folder = os.path.join(configs_root, model_type, model_name)
    json_path = os.path.join(json_folder, f"{tag}.json")
    if not os.path.isfile(json_path):
        json_path = os.path.join(json_folder, f"{DEFAULT_ZOO_TAG}.json")
    return ParsedModel(json_path, download_name)


def _parse_config(json_path: str) -> Dict[str, Any]:
    with open(json_path, "r") as f:
        config = json.load(f)
    bases = config.pop("__bases__", [])
    for base in bases[::-1]:
        parsed = _parse_model(base)
        config = update_dict(config, _parse_config(parsed.json_path))
    return config


class ZooBase(ABC):
    def __init__(
        self,
        model: Optional[str] = None,
        *,
        build: bool = True,
        report: Optional[bool] = None,
        report_folder: Optional[str] = None,
        data_info: Optional[Dict[str, Any]] = None,
        download_name: Optional[str] = None,
        json_path: Optional[str] = None,
        debug: bool = False,
        **kwargs: Any,
    ):
        self.download_name = download_name
        # load json
        if json_path is None:
            if model is None:
                raise ValueError("either `model` or `json_path` should be provided")
            parsed = _parse_model(model)
            json_path = parsed.json_path
            if self.download_name is None:
                self.download_name = parsed.download_name
        self.json_path = json_path
        parsed_config = _parse_config(json_path)
        if self.download_name is None:
            self.download_name = parsed_config.pop("tag", None)
        self.err_msg_fmt = f"`{'{}'}` should be provided in '{json_path}'"
        # get pipeline
        self.pipeline_name = parsed_config.pop("pipeline", None)
        if self.pipeline_name is None:
            raise ValueError(self.err_msg_fmt.format("pipeline"))

        def _example(l: str, r: str, h: List[str]) -> str:
            key = h.pop(0)
            if not h:
                return f"{l}{key}=...{r}"
            return _example(f"{l}{key}=dict(", f"){r}", h)

        # handle requires
        def _inject_requires(
            inc: Dict[str, Any],
            reference: Dict[str, Any],
            local_requires: Dict[str, Any],
            hierarchy: Optional[str],
        ) -> None:
            for k, v in local_requires.items():
                k_hierarchy = k if hierarchy is None else f"{hierarchy} -> {k}"
                ki = inc.setdefault(k, {})
                kr = reference.setdefault(k, {})
                if isinstance(v, dict):
                    _inject_requires(ki, kr, v, k_hierarchy)
                    continue
                assert isinstance(v, list), "requirements should be a list"
                for vv in v:
                    shortcut = kwargs.pop(vv, no_shortcut_token)
                    if shortcut != no_shortcut_token:
                        ki[vv] = shortcut
                        continue
                    if vv not in kr:
                        example = _example("", "", k_hierarchy.split(" -> ") + [vv])
                        raise ValueError(
                            f"Failed to build '{model}': "
                            f"'{vv}' should be provided in `{k_hierarchy}`, for example:\n"
                            f'* cflearn.api.from_zoo("{model}", {example})\n'
                            f'* cflearn.ZooBase.load_pipeline("{model}", {example})\n'
                            f"\nOr you can use shortcut for simplicity:\n"
                            f'* cflearn.api.from_zoo("{model}", {vv}=...)\n'
                            f'* cflearn.ZooBase.load_pipeline("{model}", {vv}=...)\n'
                        )

        no_shortcut_token = "@#$no_shortcut$#@"
        requires = parsed_config.pop("__requires__", {})
        merged_config = shallow_copy_dict(parsed_config)
        update_dict(shallow_copy_dict(kwargs), merged_config)
        increment: Dict[str, Any] = {}
        _inject_requires(increment, merged_config, requires, None)
        self.config = shallow_copy_dict(parsed_config)
        update_dict(kwargs, self.config)
        update_dict(increment, self.config)
        # build
        m_base: Type[DLPipeline] = DLPipeline.get(self.pipeline_name)
        config = m_base.config_base(**shallow_copy_dict(self.config))
        if debug:
            config.to_debug()
        self.m = DLPipeline.make(self.pipeline_name, config)
        if build:
            try:
                self.m.build(
                    data_info or {},
                    build_trainer=False,
                    report=report,
                    report_folder=report_folder,
                )
            except Exception as err:
                raise ValueError(f"Failed to build '{model}': {err}")

    @classmethod
    def load_pipeline(
        cls,
        model: Optional[str] = None,
        *,
        build: bool = True,
        report: Optional[bool] = None,
        data_info: Optional[Dict[str, Any]] = None,
        json_path: Optional[str] = None,
        debug: bool = False,
        **kwargs: Any,
    ) -> IPipeline:
        zoo = cls(
            model,
            build=build,
            report=report,
            data_info=data_info,
            json_path=json_path,
            debug=debug,
            **kwargs,
        )
        assert zoo.m is not None
        return zoo.m


class DLZoo(ZooBase):
    m: DLPipeline

    def __init__(
        self,
        model: Optional[str] = None,
        *,
        build: bool = True,
        report: Optional[bool] = None,
        data_info: Optional[Dict[str, Any]] = None,
        json_path: Optional[str] = None,
        debug: bool = False,
        **kwargs: Any,
    ):
        if model is not None:
            loader_base = dl_zoo_model_loaders.get(model)
            if loader_base is not None:
                loader = loader_base()
                loader.permute_kwargs(kwargs)
        self.pretrained_state_callback = kwargs.pop("pretrained_state_callback", None)
        super().__init__(
            model,
            build=build,
            report=report,
            data_info=data_info,
            json_path=json_path,
            debug=debug,
            **kwargs,
        )

    def load_pretrained(self) -> IDLModel:
        if self.download_name is None:
            err_msg = self.err_msg_fmt.format("tag")
            raise ValueError(f"{err_msg} when `pretrained` is True")
        m = self.m.model
        states = torch.load(download_model(self.download_name), map_location="cpu")
        if self.pretrained_state_callback is not None:
            states = self.pretrained_state_callback(states)
        m.load_state_dict(states)
        return m

    @classmethod
    def load_pipeline(
        cls,
        model: Optional[str] = None,
        *,
        build: bool = True,
        report: Optional[bool] = None,
        data_info: Optional[Dict[str, Any]] = None,
        json_path: Optional[str] = None,
        pretrained: bool = False,
        debug: bool = False,
        **kwargs: Any,
    ) -> DLPipeline:
        zoo = cls(
            model,
            build=build,
            report=report,
            data_info=data_info,
            json_path=json_path,
            debug=debug,
            **kwargs,
        )
        if pretrained:
            zoo.load_pretrained()
        return zoo.m

    @classmethod
    def load_model(
        cls,
        model: Optional[str] = None,
        *,
        report: bool = True,
        data_info: Optional[Dict[str, Any]] = None,
        json_path: Optional[str] = None,
        pretrained: bool = False,
        **kwargs: Any,
    ) -> IDLModel:
        kwargs.setdefault("in_loading", True)
        zoo = cls(
            model,
            build=True,
            report=report,
            data_info=data_info,
            json_path=json_path,
            **kwargs,
        )
        if pretrained:
            zoo.load_pretrained()
        return zoo.m.model

    @classmethod
    def dump_onnx(
        cls,
        model: str,
        export_folder: str,
        dynamic_axes: Optional[Union[List[int], Dict[int, str]]] = None,
        *,
        data_info: Optional[Dict[str, Any]] = None,
        json_path: Optional[str] = None,
        onnx_file: str = "model.onnx",
        opset: int = 11,
        simplify: bool = True,
        input_sample: Optional[tensor_dict_type] = None,
        num_samples: Optional[int] = None,
        verbose: bool = True,
        **kwargs: Any,
    ) -> DLPipeline:
        kwargs["in_loading"] = True
        zoo = cls(
            model,
            build=True,
            data_info=data_info,
            json_path=json_path,
            **kwargs,
        )
        try:
            zoo.load_pretrained()
        except ValueError:
            print_warning(
                f"no pretrained models are available for '{model}', "
                "so onnx will not be dumped"
            )
            return zoo.m
        zoo.m.to_onnx(
            export_folder,
            dynamic_axes,
            onnx_file=onnx_file,
            opset=opset,
            simplify=simplify,
            input_sample=input_sample,
            num_samples=num_samples,
            verbose=verbose,
        )
        return zoo.m


__all__ = [
    "ZooBase",
    "DLZoo",
]
