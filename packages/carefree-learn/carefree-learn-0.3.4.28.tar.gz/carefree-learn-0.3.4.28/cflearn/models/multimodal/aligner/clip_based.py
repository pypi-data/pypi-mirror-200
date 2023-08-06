from torch import Tensor
from typing import Any
from typing import Dict
from typing import Tuple
from typing import Optional

from .core import Text2ImageAligner
from ..clip import CLIP
from ...register import register_custom_loss_module
from ...cv.generator import VQGANGenerator


@register_custom_loss_module("clip_vqgan_aligner", is_ml=False)
class CLIPWithVQGANAligner(Text2ImageAligner):
    perceptor: CLIP
    generator: VQGANGenerator

    def __init__(
        self,
        perceptor: str = "clip",
        generator: str = "vqgan_generator",
        tokenizer: str = "clip",
        resolution: Tuple[int, int] = (400, 224),
        *,
        text: str,
        noise: str = "fractal",
        condition_path: Optional[str] = None,
        vision_encoder: Optional[str] = None,
        vision_encoder_config: Optional[Dict[str, Any]] = None,
        vision_encoder_pretrained_name: Optional[str] = None,
        vision_encoder_pretrained_path: Optional[str] = None,
        vision_weight: float = 0.1,
        vision_monitor_step: int = 5,
        tokenizer_config: Optional[Dict[str, Any]] = None,
        num_cuts: int = 36,
        perceptor_config: Optional[Dict[str, Any]] = None,
        generator_config: Optional[Dict[str, Any]] = None,
        perceptor_pretrained_name: Optional[str] = "clip",
        generator_pretrained_name: Optional[str] = "vqgan_generator",
        perceptor_pretrained_path: Optional[str] = None,
        generator_pretrained_path: Optional[str] = None,
    ):
        if generator_config is None:
            generator_config = {}
        generator_config.setdefault("img_size", 256)
        if condition_path is not None:
            if vision_encoder is None:
                vision_encoder = "backbone"
            if vision_encoder_config is None:
                vision_encoder_config = {"name": "vgg_style", "pretrained": True}
        super().__init__(
            perceptor,
            generator,
            tokenizer,
            resolution,
            text=text,
            noise=noise,
            condition_path=condition_path,
            vision_encoder=vision_encoder,
            vision_encoder_config=vision_encoder_config,
            vision_encoder_pretrained_name=vision_encoder_pretrained_name,
            vision_encoder_pretrained_path=vision_encoder_pretrained_path,
            vision_weight=vision_weight,
            vision_monitor_step=vision_monitor_step,
            tokenizer_config=tokenizer_config,
            num_cuts=num_cuts,
            perceptor_config=perceptor_config,
            generator_config=generator_config,
            perceptor_pretrained_name=perceptor_pretrained_name,
            generator_pretrained_name=generator_pretrained_name,
            perceptor_pretrained_path=perceptor_pretrained_path,
            generator_pretrained_path=generator_pretrained_path,
        )
        self.normalize = self.perceptor.get_transform().transforms[-1]

    def generate_raw(self) -> Tensor:
        z_q = self.generator.codebook(self.z)[0]
        return self.generator.decode(z_q, resize=False)

    def perceptor_normalize(self, image: Tensor) -> Tensor:
        return self.normalize(image)


__all__ = [
    "CLIPWithVQGANAligner",
]
