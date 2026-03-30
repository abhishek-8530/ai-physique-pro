import os
from PIL import Image
from torch.utils.data import Dataset
import torchvision.transforms as transforms

class PhysiqueDataset(Dataset):
    def __init__(self, root):
        self.images = []
        self.labels = []
        self.classes = sorted(os.listdir(root))

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor()
        ])

        for idx, cls in enumerate(self.classes):
            folder = os.path.join(root, cls)

            if not os.path.isdir(folder):
                continue

            for file in os.listdir(folder):
                path = os.path.join(folder, file)

                if file.lower().endswith((".jpg", ".png", ".jpeg")):
                    self.images.append(path)
                    self.labels.append(idx)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        try:
            img = Image.open(self.images[idx]).convert("RGB")
        except:
            # fallback image
            img = Image.new("RGB", (224, 224))

        return self.transform(img), self.labels[idx]