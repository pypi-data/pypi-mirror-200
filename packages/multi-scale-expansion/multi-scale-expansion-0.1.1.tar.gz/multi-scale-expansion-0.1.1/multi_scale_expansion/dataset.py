import os
import glob
import torch
import itertools
import numpy as np
from PIL import Image


class PlantDataset(torch.utils.data.Dataset):
    def __init__(self, images_dir, image_transform):
        self.image_transform = image_transform

        # Get a list of all class names inside the images directory
        self.classes = self.get_class_names(images_dir)

        # Assign a unique label index to each class name
        self.class_labels = {name: idx for idx, name in enumerate(self.classes)}

        image_files, labels = self.get_image_filenames_with_labels(
            images_dir,
            self.classes,
            self.class_labels,
        )

        # This is a trick to avoid memory leaks over very large datasets.
        self.image_files = np.array(image_files)
        self.labels = np.array(labels).astype("int")

        # How many total images do we need to iterate in this entire dataset?
        self.num_images = len(self.image_files)

    def __len__(self):
        return self.num_images

    def get_class_names(self, images_dir):
        """
        Given a directory of images, underneath which we have directories of class
        names, collect all these class names and return as a list of strings.
        """
        class_name_dirs = glob.glob(images_dir + "/*")
        class_names = [name.replace(images_dir + "/", "") for name in class_name_dirs]
        return sorted(class_names)  # sort just to keep consistency

    def get_image_filenames_with_labels(self, images_dir, class_names, class_labels):
        image_files = []
        labels = []

        supported_file_types = ["/*.jpg", "/*.jpeg", "/*.gif"]

        for name in class_names:
            # Glob all (supported) image file names in this directory
            image_class_dir = os.path.join(images_dir, name)

            # Iterate through the supported file types.  For each, glob a list of
            # all file names with that file extension.  Then combine the entire list
            # into one list using itertools.
            image_class_files = list(
                itertools.chain.from_iterable(
                    [glob.glob(image_class_dir + file_type) for file_type in supported_file_types]
                )
            )

            # Concatenate the image file names to the overall list and create a label for each
            image_files += image_class_files
            labels += [class_labels[name]] * len(image_class_files)

        return image_files, labels

    def __getitem__(self, idx):
        try:
            image = Image.open(self.image_files[idx]).convert('RGB')
            label = self.labels[idx]

            # Apply the image transform
            image = self.image_transform(image)

            return image, label
        except Exception as exc:
            return exc


def collate_fn(batch):
    # Filter failed images first
    batch = list(filter(lambda x: x is not None, batch))

    # Now collate into mini-batches
    images = torch.stack([b[0] for b in batch])
    labels = torch.LongTensor([b[1] for b in batch])

    return images, labels


def get_datasets(data_dir, data_transforms):
    return {x: PlantDataset(os.path.join(data_dir, x), data_transforms[x]) for x in ['train', 'test']}


def get_dataloaders(image_datasets):
    return {
        x: torch.utils.data.DataLoader(
            image_datasets[x], batch_size=4, shuffle=True, num_workers=0, collate_fn=collate_fn
        )
        for x in ['train', 'test']
    }
