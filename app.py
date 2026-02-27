import streamlit as st
import requests
import base64
from datetime import datetime

st.set_page_config(page_title="AI Memory Reconstruction", layout="centered")

# -----------------------------
# Session State Initialization
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = None


# -----------------------------
# UI
# -----------------------------
st.title("🧠 AI Memory Reconstruction")

endpoint = st.text_input(
    "API Endpoint URL",
    placeholder="https://api.example.com/generate"
)

api_key = st.text_input("API Key", type="password")

prompt = st.text_area("Enter your memory prompt")

col1, col2 = st.columns(2)
generate_btn = col1.button("Generate New Memory")
modify_btn = col2.button("Reconstruct Last Memory")


# -----------------------------
# Image Generation Function
# -----------------------------
def generate_image(final_prompt):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": final_prompt,
        "size": "1024x1024"
    }

    try:
        response = requests.post(
            endpoint,
            json=payload,
            headers=headers,
            timeout=60
        )

        if response.status_code != 200:
            return None, "API error. Check endpoint or API key."

        data = response.json()

        if "image" in data:
            image_b64 = data["image"]
        elif "data" in data and len(data["data"]) > 0:
            image_b64 = data["data"][0].get("b64_json")
        else:
            return None, "Unexpected API response format."

        image_bytes = base64.b64decode(image_b64)
        return image_bytes, None

    except requests.exceptions.RequestException:
        return None, "Could not connect to API."


# -----------------------------
# Button Logic
# -----------------------------
if generate_btn:
    if not endpoint or not api_key or not prompt:
        st.warning("Please fill all fields.")
    else:
        image, error = generate_image(prompt)
        if error:
            st.error(error)
        else:
            st.session_state.history.append({
                "prompt": prompt,
                "image": image,
                "time": datetime.now()
            })
            st.session_state.last_prompt = prompt


if modify_btn:
    if not st.session_state.last_prompt:
        st.warning("No previous memory to reconstruct.")
    elif not prompt:
        st.warning("Enter additional details.")
    else:
        combined_prompt = (
            st.session_state.last_prompt + ", " + prompt
        )

        image, error = generate_image(combined_prompt)
        if error:
            st.error(error)
        else:
            st.session_state.history.append({
                "prompt": combined_prompt,
                "image": image,
                "time": datetime.now()
            })
            st.session_state.last_prompt = combined_prompt


# -----------------------------
# Display History (Newest First)
# -----------------------------
st.markdown("---")
st.subheader("🖼 Reconstructed Memories")

for item in reversed(st.session_state.history):
    with st.container():
        st.markdown("---")
        st.markdown(f"*Prompt:* {item['prompt']}")
        st.image(item["image"], use_container_width=True)
