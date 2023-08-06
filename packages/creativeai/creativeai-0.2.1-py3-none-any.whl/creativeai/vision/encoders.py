# Copyright (c) 2020, Novelty Factory KG.  See LICENSE for details.

from .models.vgg import *

ALL_MODELS = [VGG19Encoder, VGG16Encoder, VGG13Encoder, VGG11Encoder, ThinetSmall, ThinetTiny]
ALL_LAYERS = ["1_1", "2_1", "3_1", "4_1", "5_1"]
