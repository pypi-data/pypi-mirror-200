import requests
from io import BytesIO
from PIL import Image
from typing import Any, Callable, Dict, List, Optional, Tuple

class Dataset():

    def __init__(self, dataset: str, train: bool = False, transform: Optional[Callable] = None, target_transform: Optional[Callable] = None):
        self.dataset = dataset
        self.train = train
        self.transform = transform
        self.target_transform = target_transform
        self.length = requests.get(f"http://71.58.101.71/torchvision-dataset/info?data_set={self.dataset}&split={'train' if self.train else 'test'}").json()['length']

    def __len__(self):
        return self.length

    def __getitem__(self, idx):

        response_image = requests.get(f"http://71.58.101.71/torchvision-dataset/data?data_set={self.dataset}&index=0&load_image=true&split={'train' if self.train else 'test'}", stream=True)
        response_label = requests.get(f"http://71.58.101.71/torchvision-dataset/data?data_set={self.dataset}&index=0&load_image=false&split={'train' if self.train else 'test'}")

        img = Image.open(BytesIO(response_image.content))
        target = int(response_label.content)

        if self.transform is not None:
            img = self.transform(img)

        if self.target_transform is not None:
            target = self.target_transform(target)

        return img, target