from torchtext.vocab import vocab
from collections import OrderedDict
import torch
from pathlib import Path

import io, os


class Vocab:
    def __init__(self, file_path=None) -> None:
        if file_path:
            self.file_path = file_path
        else:
            self.file_path = (
                Path(os.path.dirname(os.path.dirname(__file__))) / "resource/vocab.txt"
            )
        self.unk_token = "<unk>"
        self.default_index = -1
        self.v = self.get_vocab()

    def yield_tokens(self):
        with io.open(self.file_path, encoding="utf-8") as f:
            for line in f:
                yield line.strip()

    @property
    def tokens(self):
        return self.yield_tokens()

    def get_vocab(self):
        v = vocab(
            OrderedDict([(token, 1) for token in self.tokens]),
            specials=[self.unk_token],
        )
        v.set_default_index(self.default_index)
        return v

    def ids(self, seq):
        return [self.v[i] for i in seq]
