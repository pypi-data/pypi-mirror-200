import torch

from torch import nn
from torch import Tensor
from typing import Optional
from cftool.types import tensor_dict_type

from .constants import LV1_ALPHA_KEY
from .constants import LV1_RAW_ALPHA_KEY
from ....register import register_module
from ....constants import INPUT_KEY
from ....modules.blocks import get_conv_blocks
from ....modules.blocks import ResidualBlock


# TODO : Try ResidualBlockV2


@register_module("alpha_refine")
class AlphaRefineNet(nn.Module):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        *,
        num_layers: int = 3,
        latent_channels: int = 64,
        dropout: float = 0.0,
        ca_reduction: Optional[int] = None,
        eca_kernel_size: Optional[int] = None,
        lite: bool = False,
    ):
        super().__init__()
        if lite:
            latent_channels //= 2
        blocks = get_conv_blocks(
            in_channels + 1,
            latent_channels,
            3,
            1,
            activation=nn.ReLU(inplace=True),
        )
        for _ in range(num_layers - 2):
            if lite:
                blocks.extend(
                    get_conv_blocks(
                        latent_channels,
                        latent_channels,
                        3,
                        1,
                        activation=nn.ReLU6(inplace=True),
                    )
                )
            else:
                blocks.append(
                    ResidualBlock(
                        latent_channels,
                        dropout,
                        ca_reduction=ca_reduction,
                        eca_kernel_size=eca_kernel_size,
                    )
                )
        blocks.extend(get_conv_blocks(latent_channels, out_channels, 3, 1))
        self.net = nn.Sequential(*blocks)

    def forward(self, batch: tensor_dict_type) -> Tensor:
        net = batch[INPUT_KEY]
        lv1_raw_alpha = batch[LV1_RAW_ALPHA_KEY]
        lv1_alpha = batch[LV1_ALPHA_KEY]
        net = self.net(torch.cat([net, lv1_alpha], dim=1))
        net = net + lv1_raw_alpha
        return net

    def refine_from(self, net: Tensor, lv1_raw_alpha: Tensor) -> Tensor:
        alpha = torch.sigmoid(lv1_raw_alpha)
        inp = {INPUT_KEY: net, LV1_RAW_ALPHA_KEY: lv1_raw_alpha, LV1_ALPHA_KEY: alpha}
        return self.forward(inp)


__all__ = [
    "AlphaRefineNet",
]
