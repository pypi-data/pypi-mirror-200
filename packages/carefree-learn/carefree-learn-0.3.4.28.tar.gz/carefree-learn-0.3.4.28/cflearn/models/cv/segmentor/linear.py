import torch

from torch import nn
from torch import Tensor
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from ....register import register_module
from ....constants import LATENT_KEY
from ..encoder.backbone import BackboneEncoder
from ...schemas.cv import ImageTranslatorMixin
from ....misc.toolkit import interpolate
from ....modules.blocks import get_conv_blocks
from ....modules.blocks import Conv2d
from ....modules.blocks import Lambda
from ....modules.blocks import Linear


@register_module("linear_seg")
class LinearSegmentation(nn.Module, ImageTranslatorMixin):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        latent_dim: int = 768,
        *,
        dropout: float = 0.1,
        backbone: str = "mix_vit",
        backbone_config: Optional[Dict[str, Any]] = None,
    ):
        super().__init__()
        self.backbone = BackboneEncoder(
            backbone,
            in_channels,
            backbone_config=backbone_config,
        )
        linear_blocks: List[nn.Module] = []
        backbone_channels = self.backbone.net.out_channels
        for num_channel in backbone_channels:
            linear_blocks.append(
                nn.Sequential(
                    Lambda(lambda t: t.flatten(2).transpose(1, 2), "BCHW -> BNC"),
                    Linear(num_channel, latent_dim),
                )
            )
        self.linear_blocks = nn.ModuleList(linear_blocks)
        self.linear_fuse = nn.Sequential(
            *get_conv_blocks(
                latent_dim * 4,
                latent_dim,
                kernel_size=1,
                stride=1,
                norm_type="batch",
            )
        )
        self.dropout = nn.Dropout2d(dropout) if dropout > 0.0 else None
        self.linear_head = Conv2d(latent_dim, out_channels, kernel_size=1)

    def forward(self, inp: Tensor) -> Tensor:
        features = self.backbone(inp)
        features.pop(LATENT_KEY)
        outputs = []
        for i, linear in enumerate(self.linear_blocks):
            net = features[f"stage{i + 1}"]
            b, _, h, w = net.shape
            net = linear(net).transpose(1, 2)
            net = net.contiguous().view(b, -1, h, w)
            net = interpolate(net, anchor=inp, mode="bilinear")
            outputs.append(net)
        net = torch.cat(outputs, dim=1)
        net = self.linear_fuse(net)
        if self.dropout is not None:
            net = self.dropout(net)
        net = self.linear_head(net)
        return net


__all__ = ["LinearSegmentation"]
