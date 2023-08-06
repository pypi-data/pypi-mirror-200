import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler


def get_plant_model(model, class_names):
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, len(class_names))
    return model


def get_train_loss_needs(model_ft, lr, momentum, step_size, gamma):
    criterion = nn.CrossEntropyLoss()
    optimizer_ft = optim.SGD(model_ft.parameters(), lr=lr, momentum=momentum)
    exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=step_size, gamma=gamma)
    return criterion, optimizer_ft, exp_lr_scheduler
