#!/usr/bin/env python
from torch.utils.data import DataLoader
from abc import ABC, abstractmethod
from typing import Any, Dict, List
import os

import codefast as cf
import pandas as pd
import torch
from torch import nn
from torch.utils.data import Dataset
from tqdm import tqdm
from transformers import BertForSequenceClassification, BertTokenizer

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class TextDataset(Dataset):

    def __init__(self, df: pd.DataFrame, tokenizer: BertTokenizer):
        self.df = df
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.df)

    def __getitem__(self, index):
        text = str(self.df.iloc[index]['text'])
        label = self.df.iloc[index]['label']

        encoding = self.tokenizer.encode_plus(text,
                                              add_special_tokens=True,
                                              padding='max_length',
                                              truncation=True,
                                              max_length=256,
                                              return_tensors='pt')
        input_ids = encoding['input_ids'].squeeze()
        attention_mask = encoding['attention_mask'].squeeze()
        return input_ids, attention_mask, label


class BaseTrainer(ABC):

    @abstractmethod
    def train(self):
        pass


class History(object):
    """ History for training process
    """

    def __init__(self):
        self.history = {
            'train_loss': [],
            'val_loss': [],
            'train_acc': [],
            'val_acc': []
        }

    def add(self, **kwds):
        for key, value in kwds.items():
            self.history[key].append(value)

    def get(self):
        return self.history

    def __str__(self):
        return str(self.history)

    def display_last(self):
        print({k: round(v[-1], 4) for k, v in self.history.items()})


class TransformerTrainer(BaseTrainer):
    """ Trainer for transformers models
    """

    def __init__(self, model, train_loader, val_loader, **kwds: Any):
        self.model = model
        self.model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.epochs = kwds.get('epochs', 1)
        self.optimizer = kwds.get(
            'optimizer', torch.optim.Adam(self.model.parameters(), lr=1e-3))
        self.criterion = kwds.get('criterion', nn.CrossEntropyLoss())
        self.history = History()
        self.log_path = kwds.get('log_path', '/tmp/zap_logs')

        for key, value in kwds.items():
            setattr(self, key, value)

    def validate(self):
        val_loss, val_correct = 0.0, 0.0
        self.model.eval()
        with torch.no_grad():
            for input_ids, attention_mask, labels in tqdm(self.val_loader,
                                                          desc='Validation'):
                input_ids = input_ids.to(device)
                attention_mask = attention_mask.to(device)
                labels = labels.to(device)
                outputs = self.model(input_ids=input_ids,
                                     attention_mask=attention_mask,
                                     labels=labels)
                val_loss += outputs.loss.item()
                val_correct += (outputs.logits.argmax(1) == labels).sum().item()
        val_loss = val_loss / len(self.val_loader)
        val_acc = val_correct / len(self.val_loader.dataset)
        return val_loss, val_acc

    def train(self):
        best_val_acc = 0.0
        for _epoch in range(self.epochs):
            self.model.train()
            train_loss = 0.0
            train_acc = 0.0
            for input_ids, attention_mask, labels in tqdm(self.train_loader,
                                                          desc='Training'):
                input_ids = input_ids.to(device)
                attention_mask = attention_mask.to(device)
                labels = labels.to(device)

                self.optimizer.zero_grad()
                outputs = self.model(input_ids=input_ids,
                                     attention_mask=attention_mask,
                                     labels=labels)
                loss = outputs.loss
                loss.backward()
                self.optimizer.step()

                train_loss += loss.item()
                train_acc += (outputs.logits.argmax(1) == labels).sum().item()

            val_loss, val_acc = self.validate()
            train_loss = train_loss / len(self.train_loader)
            train_acc = train_acc / len(self.train_loader.dataset)
            self.history.add(train_loss=train_loss,
                             val_loss=val_loss,
                             train_acc=train_acc,
                             val_acc=val_acc)
            self.history.display_last()

            if val_acc > best_val_acc:
                best_val_acc = val_acc
                best_model_path = '{}/best_model'.format(self.log_path)
                if not os.path.exists(self.log_path):
                    os.makedirs(self.log_path)
                self.model.save_pretrained(best_model_path)
                cf.info('Save pretrained model to {}'.format(best_model_path))
        return self


class TransformerPredictor(object):

    def __init__(self, model, tokenizer: BertTokenizer):
        self.model = model
        self.tokenizer = tokenizer
        self.model.to(device)

    def predict(self, text_list: List[str]) -> List[int]:
        self.model.eval()
        labels = []
        with torch.no_grad():
            for text in text_list:
                inputs = self.tokenizer.encode_plus(text,
                                                      add_special_tokens=True,
                                                      padding='max_length',
                                                      truncation=True,
                                                      max_length=256,
                                                      return_tensors='pt')
                inputs.to(device)
                outputs = self.model(**inputs)
                labels.append(outputs.logits.argmax(1).item())
        return labels