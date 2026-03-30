from fastapi import FastAPI, File, UploadFile, Form
import numpy as np
import cv2
from PIL import Image
import io

# ✅ FIXED IMPORTS (VERY IMPORTANT)
from backend.inference import predict, extract_embedding
from backend.similarity import search

app = FastAPI()


# ---------------- FEATURE EXTRACTION ----------------
def extract_features(img):
    height, width, _ = img.shape
    shoulder_ratio = width / height

    return {
        "shoulder_ratio": shoulder_ratio
    }


# ---------------- SMART PLAN ENGINE ----------------
def generate_plan(body_type, goal, weight, age, features):

    insights = []
    plan = []

    # ---------------- BODY TYPE ----------------
    if body_type == "slim":
        insights.append("Lean physique with lower muscle mass")
        insights.append("May have faster metabolism")

    elif body_type == "average":
        insights.append("Balanced body composition")
        insights.append("Good potential for recomposition")

    elif body_type == "athletic":
        insights.append("Strong muscular foundation")
        insights.append("Body responds well to training")

    # ---------------- FEATURE BASED ----------------
    if features["shoulder_ratio"] < 0.6:
        insights.append("Narrow shoulder frame detected")
        plan.append("Focus on lateral raises & shoulder hypertrophy")

    elif features["shoulder_ratio"] > 0.85:
        insights.append("Broad shoulder structure")
        plan.append("Maintain upper body strength balance")

    # ---------------- GOAL BASED ----------------
    if goal == "Muscle Gain":
        plan += [
            "Calorie surplus (+300–500 kcal)",
            "Compound lifts (bench, squat, deadlift)",
            "Train 4–5 times per week",
            "Progressive overload strategy"
        ]

        if body_type == "slim":
            plan.append("Limit cardio to conserve calories")

    elif goal == "Fat Loss":
        plan += [
            "Calorie deficit (~400 kcal)",
            "Strength training + cardio",
            "High protein intake",
            "Track daily calorie intake"
        ]

    else:
        plan += [
            "Maintain calorie balance",
            "Combine strength + cardio",
            "Stay consistent with routine"
        ]

    # ---------------- PERSONALIZATION ----------------
    if weight < 55:
        insights.append("Lower body weight detected")
        plan.append("Increase calorie-dense foods (nuts, milk, rice)")

    elif weight > 90:
        insights.append("Higher body weight detected")
        plan.append("Focus on fat loss while preserving muscle")

    if age < 18:
        insights.append("Body still developing")
        plan.append("Avoid heavy lifting; focus on form")

    elif age > 40:
        insights.append("Recovery may be slower")
        plan.append("Include mobility & rest days")

    return insights, plan


# ---------------- DIET GENERATOR ----------------
def generate_diet(goal):

    if goal == "Muscle Gain":
        return {
            "Breakfast": "Oats + Milk + Banana + Peanut Butter",
            "Lunch": "Rice + Chicken + Vegetables",
            "Dinner": "Chapati + Paneer/Eggs",
            "Snacks": "Nuts + Protein Shake"
        }

    elif goal == "Fat Loss":
        return {
            "Breakfast": "Boiled eggs + Green tea",
            "Lunch": "Grilled chicken + Salad",
            "Dinner": "Vegetable soup",
            "Snacks": "Fruits + Black coffee"
        }

    else:
        return {
            "Breakfast": "Balanced meal",
            "Lunch": "Home food",
            "Dinner": "Light meal",
            "Snacks": "Fruits"
        }


# ---------------- API ----------------
@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...)
):
    try:
        file_bytes = await file.read()

        # OpenCV
        img = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)

        if img is None or len(img.shape) < 3:
            return {"error": "Invalid or unsupported image"}

        # PIL
        pil_image = Image.open(io.BytesIO(file_bytes)).convert("RGB")

        # ---------------- ML ----------------
        pred = predict(pil_image)
        body_type = pred["label"]
        confidence = pred["confidence"]

        # ✅ Confidence filter
        if confidence < 0.6:
            body_type = "average"

        # ---------------- FEATURES ----------------
        features = extract_features(img)

        # ---------------- PLAN ----------------
        insights, plan = generate_plan(body_type, goal, weight, age, features)

        # ---------------- DIET ----------------
        diet = generate_diet(goal)

        # ---------------- SIMILARITY ----------------
        try:
            embedding = extract_embedding(pil_image)
            similar = search(embedding)
        except:
            similar = []

        return {
            "body_type": body_type,
            "confidence": confidence,
            "insights": insights,
            "recommendations": plan,
            "diet": diet,
            "similar": similar
        }

    except Exception as e:
        return {"error": str(e)}