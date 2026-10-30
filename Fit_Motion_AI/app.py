
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from ai_helper import ask_gemma, get_api_key

load_dotenv()
APP_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="FitMotion AI",
    page_icon="💪",
    layout="wide"
)

# Configure the AI client
api_key = get_api_key()
model_name = os.getenv("GEMMA_MODEL", "gemma4:e2b")

client = (
    genai.Client(api_key=api_key)
    if api_key else None
)

# Exercise library
EXERCISES = {
    "Chest": {
        "Pushups": {
            "muscles": "Chest, shoulders, triceps",
            "sets": "3 sets",
            "reps": "8–12 reps",
            "gif": "assets/pushups.gif",
            "video": "assets/pushups.mp4",
            "steps": [
                "Place your hands slightly wider than your shoulders.",
                "Keep your body straight.",
                "Lower your chest under control.",
                "Push back up without locking your elbows."
            ]
        }
    },
    "Legs": {
        "Squats": {
            "muscles": "Quadriceps, glutes",
            "sets": "3 sets",
            "reps": "10–12 reps",
            "gif": "assets/squats.gif",
            "video": "assets/squats.mp4",
            "steps": [
                "Stand with feet around shoulder-width apart.",
                "Bend your knees and hips.",
                "Keep your heels on the floor.",
                "Stand up in a controlled movement."
            ]
        }
    },
    "Arms": {
        "Bicep Curls": {
            "muscles": "Biceps",
            "sets": "3 sets",
            "reps": "10–12 reps",
            "gif": "assets/bicep_curl.gif",
            "steps": [
                "Hold the weights by your sides.",
                "Keep your elbows close to your body.",
                "Curl the weights upward.",
                "Lower them slowly."
            ]
        }
    },
    "Shoulders": {
        "Shoulder Press": {
            "muscles": "Shoulders, triceps",
            "sets": "3 sets",
            "reps": "8–12 reps",
            "gif": "assets/shoulder_press.gif",
            "steps": [
                "Hold weights around shoulder height.",
                "Keep your torso stable.",
                "Press upward with control.",
                "Lower the weights slowly."
            ]
        }
    },
    "Back": {
        "Lat Pulldown": {
            "muscles": "Latissimus dorsi, upper back",
            "sets": "3 sets",
            "reps": "10–12 reps",
            "gif": "assets/lat_pulldown.gif",
            "steps": [
                "Sit securely at the pulldown machine.",
                "Grip the bar comfortably.",
                "Pull it toward your upper chest.",
                "Return the bar slowly."
            ]
        }
    },
    "Core": {
        "Plank": {
            "muscles": "Abdominals, core",
            "sets": "3 sets",
            "reps": "Hold 20–40 seconds",
            "gif": "assets/plank.gif",
            "steps": [
                "Place your forearms on the floor.",
                "Keep your body in a straight line.",
                "Brace your abdominal muscles.",
                "Breathe normally and stop if your form fails."
            ]
        }
    }
}

def ask_ai(prompt):
    if not client or not model_name:
        return (
            "AI is not configured yet. Add your API key "
            "and approved model ID to the .env file."
        )

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        return response.text or "No response received."
    except Exception as error:
        return (
            "The AI request failed. Check your internet, "
            "API access, model ID, and API quota. "
            f"Details: {error}"
        )

st.title("💪 FitMotion AI")
st.caption("Your smart exercise guide and AI fitness coach")

tab1, tab2, tab3 = st.tabs([
    "🏋️ Exercise Library",
    "✨ Workout Planner",
    "💬 AI Coach"
])

# TAB 1: Exercise library
with tab1:
    st.subheader("Explore Exercises")

    category = st.selectbox(
        "Choose a muscle group",
        list(EXERCISES.keys())
    )

    exercise_name = st.selectbox(
        "Choose an exercise",
        list(EXERCISES[category].keys())
    )

    exercise = EXERCISES[category][exercise_name]

    left, right = st.columns(2)

    with left:
        mp4_path = exercise.get("video")
        video_file = os.path.join(APP_DIR, mp4_path) if mp4_path else None
        gif_file = os.path.join(APP_DIR, exercise["gif"])

        if video_file and os.path.isfile(video_file):
            st.video(video_file)
        elif os.path.isfile(gif_file):
            st.image(gif_file)
        else:
            st.info(
                f"Add the animation file: {mp4_path or exercise['gif']}"
            )

    with right:
        st.subheader(exercise_name)
        st.write("**Target muscles:**", exercise["muscles"])
        st.write("**Sets:**", exercise["sets"])
        st.write("**Repetitions:**", exercise["reps"])

        st.markdown("### How to perform it")
        for step in exercise["steps"]:
            st.write("•", step)

        st.caption(
            "Use a comfortable range of motion and stop "
            "if you feel pain."
        )

# TAB 2: Personalized workout
with tab2:
    st.subheader("Create Your Workout")

    goal = st.selectbox(
        "Your goal",
        ["Muscle gain", "Weight loss", "General fitness",
         "Strength"]
    )

    level = st.selectbox(
        "Experience",
        ["Beginner", "Intermediate", "Advanced"]
    )

    equipment = st.selectbox(
        "Available equipment",
        ["No equipment", "Dumbbells", "Full gym"]
    )

    duration = st.slider(
        "Workout duration (minutes)", 10, 90, 30, step=5
    )

    if st.button("Create my workout"):
        prompt = f"""
        You are FitMotion AI, a cautious fitness assistant
        for gym beginners.

        Create a beginner-friendly workout plan.

        Fitness goal: {goal}
        Experience: {level}
        Equipment: {equipment}
        Available time: {duration} minutes

        Include:
        1. A short warm-up
        2. Suitable exercises
        3. Sets and repetitions for each exercise
        4. Rest periods
        5. Approximate time allocation
        6. A short cool-down

        Use only exercises suitable for the available equipment.
        Keep instructions clear and beginner-friendly.
        Do not promise medical outcomes or encourage training
        through pain. Tell the user to stop if they feel pain
        or dizziness and seek appropriate professional advice.
        """

        with st.spinner("Gemma is creating your workout..."):
            answer = ask_gemma(prompt)

        st.markdown("### Your AI-generated workout")
        st.markdown(answer)

# TAB 3: AI fitness coach
with tab3:
    question = st.text_area("What would you like to ask your fitness coach?")

    if st.button("Ask coach"):
        if question.strip():
            prompt = f"""
            You are FitMotion AI, a friendly fitness coach
            for beginners.

            Answer in simple language. Be practical and concise.
            Suggest safe alternatives when appropriate.
            Do not diagnose injuries or medical conditions.
            If the question concerns an injury or medical issue,
            recommend qualified professional advice.

            User question: {question}
            """

            with st.spinner("Gemma is preparing an answer..."):
                answer = ask_gemma(prompt)

            st.markdown("### Coach's answer")
            st.markdown(answer)
        else:
            st.warning("Please enter a question first.")