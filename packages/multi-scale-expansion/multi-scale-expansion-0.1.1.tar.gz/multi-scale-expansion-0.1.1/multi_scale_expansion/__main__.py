import torch
from torchvision import transforms, models
from model import get_train_loss_needs, get_plant_model
from dataset import get_dataloaders, get_datasets
from classification import train_model, save_learning_curve

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

if __name__ == "__main__":
    data_dir = '/Users/angelmancera/Columbia/Classes/Spring_2023/Open_Src_Dev/Taiwan_Tomato_Leaves'
    image_datasets = get_datasets(data_dir, data_transforms)
    dataloaders = get_dataloaders(image_datasets)

    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'test']}
    class_names = image_datasets['train'].classes

    # Sanity Checks
    # print(dataset_sizes)
    # print(class_names)

    # Configure to train with GPU
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # Load pre-trained model and set add classification layer
    model = models.resnet18(pretrained=True)
    model_ft = get_plant_model(model, class_names)
    model_ft = model_ft.to(device)

    # Set up loss, optimizer, and scheduler
    criterion, optimizer_ft, exp_lr_scheduler = get_train_loss_needs(
        model_ft, lr=0.001, momentum=0.9, step_size=7, gamma=0.1
    )

    # Train and evaluate model
    model_ft, train_losses, train_accuracies, val_losses, val_accuracies = train_model(
        device, dataset_sizes, dataloaders, model_ft, criterion, optimizer_ft, exp_lr_scheduler, num_epochs=16
    )

    # Let's save our learning curve as well
    save_learning_curve(train_losses, train_accuracies, val_losses, val_accuracies)
