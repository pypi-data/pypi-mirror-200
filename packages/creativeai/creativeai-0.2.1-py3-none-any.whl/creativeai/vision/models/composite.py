# Copyright (c) 2020, Novelty Factory KG.  See LICENSE for details.

import torch
import torch.nn.functional as F


class MultiScaleEncoder(torch.nn.Module):

    def __init__(self, encoder, stagger=3):
        super().__init__()
        self.stagger = stagger
        self.encoder = encoder

    def extract(self, image, layers : set, base_layers : set = None):
        if len(layers) == 0:
            raise ValueError("No layers specified.")
        if base_layers is None:
            base_layers = layers

        generators = []
        for l in layers:
            generators.append(self.encoder.extract(image, base_layers))
            if len(generators) > self.stagger:
                del generators[0]

            sz = image.shape[2:]
            image = F.interpolate(image, size=(sz[0] // 2, sz[1] // 2), mode="area")
            try:
                outputs = [next(g) for g in generators]
            except StopIteration:
                pass

            yield l, torch.cat([o for _, o in outputs], dim=1)
