import os
import torch
import torchvision.transforms as transforms
from torch.utils.data import Dataset
from PIL import Image

#skapar ett dataset som "inherits från torch"
class ParkingSignDataset(Dataset):
    def init_(self, root_dir, annotations, transform=None): #lagrar datan
        self.root_dir = root_dir 
        self.annotations = annotations
        self.transform = transform

#längden av setet
    def len_(self):
        return len(self.annotations)
#indexet för bilden och ettiketten(labeln)
    def getitem_(self, idx):
        img_path = os.path.join(self.root_dir, self.annotations.iloc[idx, 0])
        image = Image.open(img_path)
        label = self.annotations.iloc[idx, 1]

        if self.transform:
            image = self.transform(image)

        return image, label
#försöker retunera en förtränad model (ResNet-18)
    def get_pretrained_model(num_classes):
        model = models.resnet18(pretrained=True)
        num_features = model.fc.in_features
        model.fc = torch.nn.Linear(num_features, num_classes)
        return model

