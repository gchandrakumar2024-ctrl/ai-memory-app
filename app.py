[12:26 PM, 2/27/2026] Adrian College Fri: import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="AI Memory Reconstruction", layout="centered")

if "history" not in st.session_state:
    st.session_state.history = []

if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = None


st.title("🧠 AI Memory Reconstruction")

prompt = st.text_area("Enter your memory prompt")

col1, col2 = st.columns(2)
generate_btn = col1.button("Generate New Memory")
modify_btn = col2.button("Reconstruct Last Memory")


def generate_image(final_prompt):
    try:
        url = f"https://image.pollinations.ai/prompt/{final_prompt}"
        response = requests.get(url, timeout=60)

        if response.status_code != 200:
            return None, "Image generation failed."

        return response.content, None

    except Exception:
        return None, "Connection error."


if generate_btn:
    if not prompt:
        st.warning("Please enter a prompt.")
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
        combined_prompt = st.session_state.last_prompt + ", " + prompt
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


st.markdown("---")
st.subheader("🖼 Reconstructed Memories")

for item in reversed(st.session_state.history):
    with st.container():
        st.markdown("---")
        st.markdown(f"*Prompt:* {item['prompt']}")
        st.image(item["image"], use_container_width=True)
[12:28 PM, 2/27/2026] Adrian College Fri: import streamlit as st
import requests
from datetime import datetime
import urllib.parse

st.set_page_config(page_title="AI Memory Reconstruction", layout="centered")

# -----------------------------
# Session State
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = None


# -----------------------------
# UI
# -----------------------------
st.title("🧠 AI Memory Reconstruction")

prompt = st.text_area("Enter your memory prompt")

col1, col2 = st.columns(2)
generate_btn = col1.button("Generate New Memory")
modify_btn = col2.button("Reconstruct Last Memory")


# -----------------------------
# Image Generation Function
# -----------------------------
def generate_image(final_prompt):
    try:
        encoded_prompt = urllib.parse.quote(final_prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

        response = requests.get(url, timeout=60)

        if response.status_code != 200:
            return None, f"Error {response.status_code}"

        return response.content, None

    except Exception as e:
        return None, str(e)


# -----------------------------
# Button Logic
# -----------------------------
if generate_btn:
    if not prompt:
        st.warning("Please enter a prompt.")
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
        combined_prompt = st.session_state.last_prompt + ", " + prompt
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
# Display History
# -----------------------------
st.markdown("---")
st.subheader("🖼 Reconstructed Memories")

for item in reversed(st.session_state.history):
    with st.container():
        st.markdown("---")
        st.markdown(f"*Prompt:* {item['prompt']}")
        st.image(item["image"], use_container_width=True)
