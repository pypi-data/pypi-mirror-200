# Multi Scale Expansion
Repository to create framework for image classification computer vision models in tensorflow. <br>
![image](https://img.shields.io/pypi/l/tensorflow)
![image](https://img.shields.io/github/issues/ColumbiaMancera/multi-scale-expansion)
![Build Status](https://github.com/ColumbiaMancera/multi-scale-expansion/actions/workflows/build.yml/badge.svg)
[![codecov](https://codecov.io/gh/ColumbiaMancera/multi-scale-expansion/branch/main/graph/badge.svg)](https://codecov.io/gh/ColumbiaMancera/multi-scale-expansion)

## Overview
`multi-scale-expansion` is a library for automating the set up of an image classification model. The user provides their data, and the library creates and trains a ready-to-use model to complete the image classification task and apply it to any image further. The objective is that this framework can be automated and applied for recognizing whether a plant is healthy or not, through the use of the models we train. 

## Contributions
For instructions on how to contribute, go to the [Contribution Guidelines Page](https://github.com/ColumbiaMancera/multi-scale-expansion/blob/main/CONTRIBUTING.md). 

## Installation
Prerequisites: 
- Python >= 3.7
- Torch & Torchvision
- Numpy 
- Matplotlib
- PIL (Pillow) 

To install Python packages: 
```bash
$ pip install torch
$ pip install torchvision
$ pip install numpy
$ pip install matplotlib
$ pip install Pillow
```

To install library: 
```bash
$ pip install multi-scale-expansion
```

## Quick-Start Example
```python 
import torch
from torchvision import models
import numpy as np
import matplotlib
from PIL import Image
import importlib

ms_model = importlib.import_module("multi-scale-expansion.model")
ms_datasets = importlib.import_module("multi-scale-expansion.dataset")
ms = importlib.import_module("multi-scale-expansion.classification")

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
mock_model = models.resnet18(weights='DEFAULT')
mock_model = ms_model.get_plant_model(mock_model, list(range(6))

mock_lr = 0.001
mock_momentum = 0.9
mock_step_size = 7
mock_gamma = 0.1
mock_criterion, mock_optimizer, mock_lr_scheduler = get_train_loss_needs(
    mock_model, mock_lr, mock_momentum, mock_step_size, mock_gamma
)

mock_datasets = {
    "train": FakeData(num_classes=6, transform=mock_transforms["train"]),
    "test": FakeData(num_classes=6, transform=mock_transforms["test"]),
}

mock_dataset_sizes = {x: len(mock_datasets[x]) for x in ['train', 'test']}
mock_dataloaders = ms_datasets.get_dataloaders(mock_datasets)

model, train_losses, train_accuracies, val_losses, val_accuracies = ms.train_model(
    device,
    mock_dataset_sizes,
    mock_dataloaders,
    mock_model,
    mock_criterion,
    mock_optimizer,
    mock_lr_scheduler,
    num_epochs=1,
    testing=True,
)
```

And now your model is ready-to-use! 
