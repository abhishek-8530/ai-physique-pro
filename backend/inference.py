import torch
import torchvision.transforms as transforms
from PIL import Image
import torchvision.models as models
import numpy as np
import os
import json

# ---------------- PATH ----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "cnn_model.pth")
CLASS_PATH = os.path.join(BASE_DIR, "models", "classes.json")

print("MODEL PATH:", MODEL_PATH)
print("MODEL EXISTS:", os.path.exists(MODEL_PATH))

print("CLASS PATH:", CLASS_PATH)
print("CLASS EXISTS:", os.path.exists(CLASS_PATH))

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ---------------- LOAD CLASSES ----------------
try:
    with open(CLASS_PATH, "r") as f:
        classes = json.load(f)

    if not classes:
        raise ValueError("Empty classes.json")

    print("✅ Classes loaded:", classes)

except Exception as e:
    print("⚠️ classes.json invalid, using default classes")
    classes = ["athletic", "average", "slim"]

# ---------------- LOAD MODEL ----------------
model = models.resnet18(weights=None)
model.fc = torch.nn.Linear(model.fc.in_features, len(classes))

try:
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    print("✅ Model loaded successfully")
except Exception as e:
    print("❌ Model loading failed:", e)

model = model.to(device)
model.eval()

# ---------------- FEATURE EXTRACTOR ----------------
feature_extractor = torch.nn.Sequential(*list(model.children())[:-1])

# ---------------- TRANSFORM ----------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# ---------------- PREDICT ----------------
def predict(image):
    img = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(img)
        probs = torch.nn.functional.softmax(output, dim=1)

        confidence, pred = torch.max(probs, 1)

    return {
        "label": classes[pred.item()],
        "confidence": float(confidence.item())
    }

# ---------------- EMBEDDING ----------------
def extract_embedding(image):
    img = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        emb = feature_extractor(img)

    emb = emb.cpu().numpy().flatten()
    emb = emb / (np.linalg.norm(emb) + 1e-10)

    return emb