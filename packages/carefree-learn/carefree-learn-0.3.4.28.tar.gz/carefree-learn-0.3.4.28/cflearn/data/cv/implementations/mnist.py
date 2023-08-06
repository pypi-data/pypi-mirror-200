from torch import Tensor
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union
from typing import Callable
from typing import Optional
from functools import partial
from cftool.types import tensor_dict_type
from torchvision.datasets import MNIST

from ..basic import Transforms
from ..basic import CVDataset
from ..basic import CVLoader
from ..basic import DataLoader
from ..basic import CVDataModule
from ..basic import DLDataModule
from ...core import TDataModule
from ....types import sample_weights_type
from ....constants import INPUT_KEY
from ....constants import LABEL_KEY
from ....constants import ORIGINAL_LABEL_KEY
from ....parameters import OPT


def batch_callback(
    label_callback: Optional[Callable[[Tuple[Tensor, Tensor]], Tensor]],
    batch: Tuple[Tensor, Tensor],
) -> tensor_dict_type:
    img, labels = batch
    if label_callback is None:
        actual_labels = labels.view(-1, 1)
    else:
        actual_labels = label_callback(batch)
    return {
        INPUT_KEY: img,
        LABEL_KEY: actual_labels,
        ORIGINAL_LABEL_KEY: labels,
    }


@DLDataModule.register("mnist")
class MNISTData(CVDataModule):
    def __init__(
        self,
        *,
        root: str = OPT.data_cache_dir,
        shuffle: bool = True,
        batch_size: int = 64,
        num_workers: int = 0,
        drop_train_last: bool = True,
        transform: Optional[Union[str, List[str], Transforms, Callable]],
        transform_config: Optional[Dict[str, Any]] = None,
        test_shuffle: Optional[bool] = None,
        test_transform: Optional[Union[str, List[str], Transforms, Callable]] = None,
        test_transform_config: Optional[Dict[str, Any]] = None,
        label_callback: Optional[Callable[[Tuple[Tensor, Tensor]], Tensor]] = None,
    ):
        self.root = root
        self.shuffle = shuffle
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.drop_train_last = drop_train_last
        self.transform = Transforms.convert(transform, transform_config)
        if test_shuffle is None:
            test_shuffle = shuffle
        self.test_shuffle = test_shuffle
        if test_transform is None:
            self.test_transform = self.transform
        else:
            cfg = test_transform_config or transform_config
            self.test_transform = Transforms.convert(test_transform, cfg)
        self.label_callback = label_callback

    @property
    def info(self) -> Dict[str, Any]:
        return dict(root=self.root, shuffle=self.shuffle, batch_size=self.batch_size)

    # TODO : support sample weights
    def prepare(self: TDataModule, sample_weights: sample_weights_type) -> TDataModule:
        self.train_data = CVDataset(
            MNIST(
                self.root,
                transform=self.transform,
                download=True,
            )
        )
        self.valid_data = CVDataset(
            MNIST(
                self.root,
                train=False,
                transform=self.test_transform,
                download=True,
            )
        )
        return self

    def initialize(self) -> Tuple[CVLoader, Optional[CVLoader]]:
        train_loader = CVLoader(
            DataLoader(
                self.train_data,
                batch_size=self.batch_size,
                shuffle=self.shuffle,
                num_workers=self.num_workers,
                drop_last=self.drop_train_last,
            ),
            partial(batch_callback, self.label_callback),
        )
        valid_loader = CVLoader(
            DataLoader(
                self.valid_data,
                batch_size=self.batch_size,
                shuffle=self.test_shuffle,
                num_workers=self.num_workers,
            ),
            partial(batch_callback, self.label_callback),
        )
        return train_loader, valid_loader


__all__ = [
    "MNISTData",
]
