import streamlit as st
import google.generativeai as genai
import re

# Set up Gemini API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-flash")

# App config
st.set_page_config(page_title="Flight Mood ✈️", page_icon="🛫")
st.title("🛫 Flight Mode")
st.subheader("Ever feel like a hydraulic system under pressure? Or maybe just a backup generator keeping everyone going?
Step into Flight Mode—where your mood meets machinery.
Discover which aircraft system you are today, and why.
It's not just personality. It's ATA-approved.")

# Inputs
mood = st.selectbox("How are you feeling today?", [
    "Focused and Efficient", "Adventurous", "Mysterious", "Overloaded",
    "Calm and Balanced", "Bold and Decisive", "Creative and Dreamy", "Anxious but Hopeful"
])

traits = st.multiselect("Choose your personality traits:", [
    "Analytical", "Empathetic", "Curious", "Disciplined",
    "Playful", "Reserved", "Intense", "Supportive"
])

weather = st.selectbox("What’s your mental weather today?", [
    "Clear skies", "Foggy brain", "Turbulent day", "Scattered thoughts", "Breezy and light"
])

# Emoji mappings for ATA chapters
emoji_map = {
    "21": "❄️",   # Air Conditioning
    "27": "🕹️",   # Flight Controls
    "33": "💡",   # Lights
    "35": "🫁",   # Oxygen
    "73": "⚙️",   # Engine Fuel & Control
    "23": "📡",   # Communications
    "24": "🔋",   # Electrical Power
    "25": "🪑",   # Equipment/Furnishings
    "26": "🔥",   # Fire Protection
    "29": "💧",   # Hydraulic Power
}

def insert_emoji(text):
    match = re.search(r"ATA Chapter: (\d+)", text)
    if match:
        chapter = match.group(1)
        emoji = emoji_map.get(chapter)
        if emoji:
            # Inject emoji after the ATA chapter line
            text = re.sub(rf"(ATA Chapter: {chapter} – )", rf"\1{emoji} ", text)
    return text

# Generate result
if st.button("Match Me ✈️"):
    with st.spinner("Matching your personality to aircraft systems..."):
        prompt = f"""
        Based on this person's mood, personality, and mental state, match them to the most fitting ATA (Air Transport Association) chapter number and aircraft system.

        Respond in a playful, smart tone and explain the match with a metaphor and insight.

        Mood: {mood}
        Traits: {', '.join(traits)}
        Mental Weather: {weather}

        Format:
        - ATA Chapter: [Number] – [System Name]
        - Call Sign: A fun nickname for the user
        - Description: A human-readable metaphor and explanation
        """

        response = model.generate_content(prompt)
        output = insert_emoji(response.text)

        st.success("Match complete!")
        st.markdown(output)
