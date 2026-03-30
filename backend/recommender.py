import random

# ---------------- SMART RECOMMENDER ----------------
def recommend(similar_indices, body_type):
    """
    similar_indices → output from similarity search
    body_type → output from CNN (athletic/slim/average)
    """

    # ✅ FIX: use "average" instead of "normal"
    base_plans = {
        "slim": [
            "Heavy Weight Training",
            "Calorie Surplus Diet",
            "Progressive Overload Training",
            "Low Cardio Focus"
        ],
        "average": [
            "Balanced Strength Training",
            "Moderate Cardio Routine",
            "Core Strength Exercises",
            "Consistency & Routine Building"
        ],
        "athletic": [
            "Advanced Hypertrophy Training",
            "Isolation Exercises",
            "HIIT + Strength Combo",
            "Cutting & Bulking Cycles"
        ]
    }

    # 🔥 Expanded bonus pool (more variety)
    similarity_bonus_pool = [
        "Chest Focus Workout",
        "Leg Day Optimization",
        "Back & Shoulder Sculpting",
        "Abs & Core Strength Training",
        "Upper Body Strength Routine",
        "Lower Body Power Training",
        "Mobility & Flexibility Work",
        "Endurance Training Session"
    ]

    # ✅ Pick RANDOM bonuses → makes output dynamic
    bonus = random.sample(similarity_bonus_pool, k=3)

    # ✅ Safe handling of similar indices
    if hasattr(similar_indices, "tolist"):
        similar_indices = similar_indices.tolist()

    # ✅ Merge plans
    final_plan = base_plans.get(body_type, []) + bonus

    return {
        "body_type": body_type,
        "recommendations": final_plan,
        "similar_images_index": similar_indices
    }