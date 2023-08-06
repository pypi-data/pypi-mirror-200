from multi_scale_expansion import *
import unittest
from unittest.mock import patch
import torch
import torch.nn as nn
from torchvision import transforms, models
from torchvision.datasets import FakeData


## Tests related to our Dataset
class TestDataset(unittest.TestCase):
    def test_collate_fn(self):
        first_tensor = torch.randn((576, 576, 3))
        second_tensor = torch.randn((576, 576, 3))
        batch = [[first_tensor, 0], [second_tensor, 1]]
        output = collate_fn(batch)

        # Expected
        images = torch.stack([batch[0][0], batch[1][0]])
        labels = torch.LongTensor([batch[0][1], batch[1][1]])

        assert torch.equal(output[0], images)
        assert torch.equal(output[1], labels)

    def test_get_datasets_fn(self):  # mock_dir, mock_transforms
        mock_dir = "/Users/angelmancera/Columbia/Classes/Spring_2023/Open_Src_Dev/Taiwan_Tomato_Leaves"
        mock_transforms = {
            'train': transforms.Compose(
                [
                    transforms.RandomResizedCrop(224),
                    transforms.RandomHorizontalFlip(),
                    transforms.ToTensor(),
                    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
                ]
            ),
            'test': transforms.Compose(
                [
                    transforms.Resize(256),
                    transforms.CenterCrop(224),
                    transforms.ToTensor(),
                    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
                ]
            ),
        }
        datasets = get_datasets(mock_dir, mock_transforms)

        for ds in datasets.items():
            assert ds[0] in ["train", "test"]
            assert isinstance(ds[1], torch.utils.data.Dataset)

    def test_get_dataloaders_fn(self):  # mock_datasets
        data_transforms = {
            'train': transforms.Compose(
                [
                    transforms.RandomResizedCrop(224),
                    transforms.RandomHorizontalFlip(),
                    transforms.ToTensor(),
                    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
                ]
            ),
            'test': transforms.Compose(
                [
                    transforms.Resize(256),
                    transforms.CenterCrop(224),
                    transforms.ToTensor(),
                    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
                ]
            ),
        }
        mock_datasets = {
            "train": FakeData(num_classes=6, transform=data_transforms["train"]),
            "test": FakeData(num_classes=6, transform=data_transforms["test"]),
        }
        dataloaders = get_dataloaders(mock_datasets)
        for dl in dataloaders.values():
            assert isinstance(dl, torch.utils.data.DataLoader)


## Tests related to our model
def test_get_plant_model():  # mock_model
    mock_model = models.resnet18(weights='DEFAULT')
    class_names = list(range(6))
    model = get_plant_model(mock_model, class_names)
    assert isinstance(model, nn.Module)


def test_get_train_loss_needs():  # mock_model, mock_lr, mock_momentum, mock_step_size, mock_gamma
    mock_model = models.resnet18(weights='DEFAULT')
    mock_lr = 0.001
    mock_momentum = 0.9
    mock_step_size = 7
    mock_gamma = 0.1
    needs = get_train_loss_needs(mock_model, mock_lr, mock_momentum, mock_step_size, mock_gamma)
    criterion = needs[0]
    assert isinstance(criterion, nn.CrossEntropyLoss)
    optimizer = needs[1]
    assert isinstance(optimizer, torch.optim.SGD)
    lr_scheduler = needs[2]
    assert isinstance(lr_scheduler, torch.optim.lr_scheduler.StepLR)


## Tests related to our classification training and visualization
# Integration test
def test_train_model():  # mock_dir, mock_transforms
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    mock_model = models.resnet18(weights='DEFAULT')
    class_names = list(range(6))
    mock_model = get_plant_model(mock_model, class_names)

    mock_model = models.resnet18(weights='DEFAULT')
    mock_lr = 0.001
    mock_momentum = 0.9
    mock_step_size = 7
    mock_gamma = 0.1
    mock_criterion, mock_optimizer, mock_lr_scheduler = get_train_loss_needs(
        mock_model, mock_lr, mock_momentum, mock_step_size, mock_gamma
    )

    mock_transforms = {
        'train': transforms.Compose(
            [
                transforms.RandomResizedCrop(224),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        ),
        'test': transforms.Compose(
            [
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        ),
    }
    mock_datasets = {
        "train": FakeData(num_classes=6, transform=mock_transforms["train"]),
        "test": FakeData(num_classes=6, transform=mock_transforms["test"]),
    }
    mock_dataset_sizes = {x: len(mock_datasets[x]) for x in ['train', 'test']}
    mock_dataloaders = get_dataloaders(mock_datasets)

    model, train_losses, train_accuracies, val_losses, val_accuracies = train_model(
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
    assert isinstance(model, nn.Module)
    assert isinstance(train_losses, list)
    assert isinstance(train_accuracies, list)
    assert isinstance(val_losses, list)
    assert isinstance(val_accuracies, list)
