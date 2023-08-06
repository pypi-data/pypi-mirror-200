# Copyright (c) 2020, Novelty Factory KG.  See LICENSE for details.

import torch
from torch import nn

class NormalizeRGB(nn.Module):
    """Convert RGB colors from [0.0, 1.0] range to a uniform distribution of the
    ImageNet dataset used to train the models.
    """

    def __init__(self):
        super(NormalizeRGB, self).__init__()

        means = torch.tensor([0.485, 0.456, 0.406], dtype=torch.float32)
        self.means = nn.Parameter(means.view(1, 3, 1, 1))

        stdvs = torch.tensor([0.229, 0.224, 0.225], dtype=torch.float32)
        self.stdvs = nn.Parameter(stdvs.view(1, 3, 1, 1))

    def forward(self, data):
        return (data - self.means) / self.stdvs
