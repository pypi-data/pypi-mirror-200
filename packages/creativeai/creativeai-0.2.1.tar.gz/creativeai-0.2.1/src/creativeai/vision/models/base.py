# Copyright (c) 2020, Novelty Factory KG.  See LICENSE for details.

import itertools
import functools
import collections

import torch
import torch.utils.checkpoint as tcp

from . import io
from . import convert


class ModuleConfig:
    def __init__(self, f, b):
        self.filters = f
        self.blocks = b


class Encoder(torch.nn.Module):
    def __init__(
        self, block_type, pool_type, input_type, in_channels=3, pretrained=True
    ):
        super(Encoder, self).__init__()

        blocks = self.make_blocks(self.CONFIG, block_type, pool_type, in_channels)
        if input_type == "RGB":
            blocks = [("0_1", convert.NormalizeRGB())] + list(blocks)

        self.features = torch.nn.Sequential(collections.OrderedDict(blocks))

        if pretrained is True:
            self.load_pretrained(self.FILENAME, self.HEXDIGEST)

    def load_pretrained(self, model: str, hexdigest: str, verbose=False):
        fullpath = io.download_model(model, hexdigest, quiet=not verbose)
        missing, unexpected = self.load_state_dict(torch.load(fullpath), strict=False)
        if missing and verbose: print("  - MISSING", missing)
        if unexpected and verbose: print("  - UNEXPECTED", unexpected)

    def make_blocks(self, config, block_type, pool_type, in_channels):
        previous = in_channels
        for octave, module in enumerate(config):
            for block in range(module.blocks):
                yield f"{octave+1}_{block+1}", block_type(previous, module.filters)
                if block == module.blocks - 1:
                    yield f"{octave+2}_0", pool_type(kernel_size=(2, 2))
                previous = module.filters

    def calculate_receptive_field(self, size, start_layer):
        names = list(self.features._modules.keys())
        for i in range(names.index(start_layer), -1, -1):
            block = self.features[i]
            if 'Normalize' in block.__class__.__name__:
                continue
            if 'Pool' in block.__class__.__name__:
                size *= block.kernel_size[0]
            elif 'Block' in block.__class__.__name__:
                size += 2 * (block.layers[1].kernel_size // 2)
            else:
                size += 2 * (block[1].kernel_size[0] // 2)
        return size

    def extract_one(self, current, _, start, layer, raw=False):
        names = ["0_0"] + list(self.features._modules.keys())
        index = names.index(layer)

        for i in range(names.index(start) + 1, index + 1):
            current = self.features[i - 1].forward(current)
        return current

    def _get_extractors(self, layers, start):
        layers = [start] + layers
        layers = layers[layers.index(start) :]

        for prev, cur in zip(layers[:-1], layers[1:]):
            yield cur, functools.partial(self.extract_one, start=prev, layer=cur)

    def extract_all(self, img, layers, start="0_0", as_checkpoints=False, as_raw=set()):
        def convert(l):
            return (l,) if isinstance(l, str) else l
        layers = list(set(itertools.chain.from_iterable(convert(l) for l in layers)))

        cur = img
        for layer, func in self._get_extractors(sorted(layers), start):
            if as_checkpoints is True:
                try:
                    cur = tcp.checkpoint(func, cur, img, raw=bool(layer in as_raw))
                except ValueError:
                    assert len(as_raw) == 0
                    cur = tcp.checkpoint(func, cur, img)
            else:
                try:
                    cur = func(cur, img, raw=bool(layer in as_raw))
                except TypeError:
                    assert len(as_raw) == 0
                    cur = func(cur, img)
            yield layer, cur


class Decoder(torch.nn.Module):
    def __init__(self, block_type, output_type, out_channels=3, pretrained=True):
        super(Decoder, self).__init__()

        blocks = self.make_blocks(self.CONFIG, block_type, out_channels)
        blocks = [("0_0", None)] + list(blocks)

        blocks = reversed(list(blocks))
        self.features = torch.nn.Sequential(collections.OrderedDict(blocks))

        if pretrained is True:
            self.load_pretrained(self.FILENAME, self.HEXDIGEST)

    def load_pretrained(self, model: str, hexdigest: str):
        fullpath = io.download_model(model, hexdigest, quiet=True)
        self.load_state_dict(torch.load(fullpath), strict=True)

    def make_blocks(self, config, block_type, out_channels):
        def pool_type(a, b):
            return torch.nn.Upsample(scale_factor=(2, 2), mode="nearest")

        previous = out_channels
        for octave, module in enumerate(config):
            for block in range(module.blocks + 1):
                yield f"{octave}_{block+1}", block_type(module.filters, previous)
                previous = module.filters

                if block == module.blocks and octave != 0:
                    yield f"{octave}_u", pool_type(module.filters, previous)

        yield f"{octave+1}_0", None

    def rebuild_one(self, data, layer, start):
        names = list(self.features._modules.keys()) + ["0_0"]
        index = names.index(layer)

        for i in range(names.index(start) + 1, index + 1):
            block = self.features[i]
            if block is not None:
                data = block.forward(data)
        return data

    def rebuild_all(self, data, layers: set, start: str):
        """Convert features extracted from the encoder and turn them into an image.
        """
        if len(layers) == 0:
            return

        names = list(self.features._modules.keys()) + ["0_0"]
        indices = [names.index(l) for l in layers]

        for i in range(names.index(start) + 1, max(indices) + 1):
            block = self.features[i]

            if block is not None:
                data = block.forward(data)

            if i in indices:
                yield names[i], data
