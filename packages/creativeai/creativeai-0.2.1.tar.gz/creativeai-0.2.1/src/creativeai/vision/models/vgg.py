# Copyright (c) 2020, Novelty Factory KG.  See LICENSE for details.

from torch import nn

from .base import Encoder, Decoder, ModuleConfig as M

__all__ = [
    "VGG19Encoder", "VGG19Decoder",
    "VGG16Encoder", "VGG16Decoder",
    "VGG13Encoder", "VGG13Decoder",
    "VGG11Encoder", "VGG11Decoder",
    "ThinetSmall", "ThinetTiny"
]


def ConvBlock(in_channels, out_channels, activation="ReLU"):
    layers = [
        nn.ReflectionPad2d(1),
        nn.Conv2d(in_channels, out_channels, kernel_size=(3, 3)),
        getattr(nn, activation)(inplace=True),
    ]
    return nn.Sequential(*layers)


class VGG19Encoder(Encoder):
    CONFIG = [M(f=64, b=2), M(f=128, b=2), M(f=256, b=4), M(f=512, b=4), M(f=512, b=4)]
    FILENAME = "v0.1/vgg19"
    HEXDIGEST = "29e01ad88d45dcc69672b816e400760a"

    def __init__(self, block_type=ConvBlock, pool_type=nn.MaxPool2d, input_type="RGB", **kwargs):
        super(VGG19Encoder, self).__init__(block_type, pool_type, input_type=input_type, **kwargs)


class VGG19Decoder(Decoder):
    CONFIG = [M(f=64, b=2), M(f=128, b=2), M(f=256, b=4), M(f=512, b=4), M(f=512, b=4)]

    def __init__(self, block_type=ConvBlock, **kwargs):
        """Loads the pre-trained VGG19 convolution layers from the PyTorch vision module.
        """
        super(VGG19Decoder, self).__init__(block_type, output_type="RGB")


class VGG16Encoder(Encoder):
    CONFIG = [M(f=64, b=2), M(f=128, b=2), M(f=256, b=3), M(f=512, b=3), M(f=512, b=3)]
    FILENAME = "v0.1/vgg16"
    HEXDIGEST = "a11733085f299b8c7933e9140d7ea3c4"

    def __init__(self, block_type=ConvBlock, pool_type=nn.MaxPool2d, input_type="RGB", **kwargs):
        super(VGG16Encoder, self).__init__(block_type, pool_type=pool_type, input_type=input_type, **kwargs)



def PConvBlock(in_channels, out_channels, activation="PReLU"):
    return nn.Sequential([
        nn.Identity(),         # Placeholder for pre-processing, e.g. padding.
        nn.Conv2d(in_channels, out_channels, kernel_size=(3, 3)),
        getattr(nn, activation)(),
        nn.Identity(),         # Placeholder for post-processing.
    ])


class VGG16Decoder(Decoder):
    CONFIG = [M(f=64, b=2), M(f=128, b=2), M(f=256, b=3), M(f=512, b=3), M(f=512, b=3), M(f=512, b=3)]

    def __init__(self, block_type=PConvBlock, **kwargs):
        """Loads the pre-trained VGG19 convolution layers from the PyTorch vision module.
        """
        super(VGG16Decoder, self).__init__(block_type, output_type="RGB")


class VGG13Encoder(Encoder):
    CONFIG = [M(f=64, b=2), M(f=128, b=2), M(f=256, b=2), M(f=512, b=2), M(f=512, b=2)]
    FILENAME = "v0.1/vgg13"
    HEXDIGEST = "22e6a1292435b04ba3273300c9e867aa"

    def __init__(self, block_type=ConvBlock, pool_type=nn.MaxPool2d, input_type="RGB", **kwargs):
        super(VGG13Encoder, self).__init__(block_type, pool_type=pool_type, input_type=input_type, **kwargs)


class VGG13Decoder(Decoder):
    CONFIG = [M(f=64, b=2), M(f=128, b=2), M(f=256, b=2), M(f=512, b=2), M(f=512, b=2), M(f=512, b=2)]

    def __init__(self, block_type=PConvBlock, **kwargs):
        super(VGG13Decoder, self).__init__(block_type, output_type="RGB", **kwargs)


class VGG11Encoder(Encoder):
    CONFIG = [M(f=64, b=1), M(f=128, b=1), M(f=256, b=2), M(f=512, b=2), M(f=512, b=2)]
    FILENAME = "v0.1/vgg11"
    HEXDIGEST = "2898532ef3f0910dfb1634482a1ca4ef"

    def __init__(self, block_type=ConvBlock, pool_type=nn.MaxPool2d, input_type="RGB", **kwargs):
        super(VGG11Encoder, self).__init__(block_type, pool_type, input_type=input_type, **kwargs)


class VGG11Decoder(Decoder):
    CONFIG = [M(f=64, b=1), M(f=128, b=1), M(f=256, b=2), M(f=512, b=2), M(f=512, b=2), M(f=512, b=2)]

    def __init__(self, block_type=ConvBlock, **kwargs):
        super(VGG11Decoder, self).__init__(block_type, output_type="RGB", **kwargs)



class ThinetSmall(Encoder):
    CONFIG = [M(f=32, b=2), M(f=64, b=2), M(f=128, b=3), M(f=256, b=3), M(f=512, b=3)]
    FILENAME = "v0.1/thinet_small"
    HEXDIGEST = "f15444e14276f8f36d162ee9d97ec54b"

    def __init__(self, block_type=ConvBlock, pool_type=nn.MaxPool2d, **kwargs):
        super(ThinetSmall, self).__init__(
            block_type, pool_type, input_type="RGB", **kwargs
        )


class ThinetTiny(Encoder):
    CONFIG = [M(f=16, b=2), M(f=32, b=2), M(f=64, b=3), M(f=128, b=3), M(f=128, b=2)]
    FILENAME = "v0.1/thinet_tiny"
    HEXDIGEST = "1e33d824b47a850485a2e85c29d5ddf0"

    def __init__(self, block_type=ConvBlock, pool_type=nn.MaxPool2d, **kwargs):
        super(ThinetTiny, self).__init__(
            block_type, pool_type, input_type="RGB", **kwargs
        )

ALL_LAYERS = ["1_1", "2_1", "3_1", "4_1", "5_1"]
