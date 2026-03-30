import streamlit as st
import requests

st.set_page_config(page_title="AI Physique", layout="centered")

st.title("💪 AI Physique Analyzer")

# ---------------- USER PROFILE ----------------
st.sidebar.header("👤 User Profile")

age = st.sidebar.number_input("Age", 10, 80, 22)
weight = st.sidebar.number_input("Weight (kg)", 30, 150, 65)
goal = st.sidebar.selectbox("Goal", ["Muscle Gain", "Fat Loss", "Maintain"])

st.sidebar.markdown("---")
st.sidebar.info("Your inputs help generate personalized plans")

# ---------------- IMAGE ----------------
file = st.file_uploader("📸 Upload Body Image", type=["jpg", "png", "jpeg"])

if file:
    st.image(file, caption="Uploaded Image", use_column_width=True)

    if st.button("🚀 Analyze"):
        with st.spinner("Analyzing your physique..."):

            try:
                res = requests.post(
                    "http://127.0.0.1:8000/analyze",
                    files={"file": file.getvalue()},
                    data={
                        "age": age,
                        "weight": weight,
                        "goal": goal
                    }
                )

                data = res.json()

                if "error" in data:
                    st.error(data["error"])
                else:
                    st.success("✅ Analysis Complete!")

                    # ---------------- BODY TYPE ----------------
                    body_type = data.get("body_type")

                    st.markdown("## 🧍 Body Type")
                    if body_type:
                        st.info(f"Your body type is **{body_type.capitalize()}**")
                    else:
                        st.warning("Could not determine body type")

                    # ---------------- INSIGHTS ----------------
                    st.markdown("## 🧠 Insights")

                    insights = data.get("insights", [])
                    if insights:
                        for i in insights:
                            st.write(f"✔️ {i}")
                    else:
                        st.write("No insights available")

                    # ---------------- WORKOUT PLAN ----------------
                    st.markdown("## 💪 Personalized Workout Plan")

                    recs = data.get("recommendations", [])
                    if recs:
                        for rec in recs:
                            st.write(f"🔥 {rec}")
                    else:
                        st.write("No recommendations available")

                    # ---------------- DIET PLAN ----------------
                    st.markdown("## 🍽 Diet Plan")

                    diet = data.get("diet", {})
                    if diet:
                        for meal, food in diet.items():
                            st.write(f"**{meal}:** {food}")
                    else:
                        st.write("No diet plan available")

                    # ---------------- SMART SUMMARY ----------------
                    st.markdown("## 🤖 AI Coach Summary")

                    if body_type and recs:
                        st.success(
                            f"You are a {body_type} individual aiming for {goal.lower()}. "
                            f"Follow the above plan consistently for best results."
                        )

            except Exception as e:
                st.error(f"Error connecting to backend: {e}")