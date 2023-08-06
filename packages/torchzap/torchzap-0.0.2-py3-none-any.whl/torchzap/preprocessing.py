#!/usr/bin/env python3

from typing import List

import codefast as cf


class LabelEncoder(object):

    def __init__(self, labels: List[str] = None):
        self.label2id = {}
        self.id2label = {}
        if labels:
            self.fit(labels)

    def fit(self, labels: List[str]):
        for i, label in enumerate(labels):
            self.label2id[label] = i
            self.id2label[i] = label

    def transform(self, labels: List[str]) -> List[int]:
        return [self.label2id[label] for label in labels]

    def inverse_transform(self, ids: List[int]) -> List[str]:
        return [self.id2label[id] for id in ids]
