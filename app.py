import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="AI Memory Reconstruction", layout="centered")

if "history" not in st.session_state:
    st.session_state.history = []

if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = None

st.title("🧠 AI Memory Reconstruction")

hf_token = st.text_input("HuggingFace API Key", type="password")
prompt = st.text_area("Enter your memory prompt")

col1, col2 = st.columns(2)
generate_btn = col1.button("Generate New Memory")
modify_btn = col2.button("Reconstruct Last Memory")


def generate_image(final_prompt):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
    headers = {"Authorization": f"Bearer {hf_token}"}

    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": final_prompt}, timeout=60)

        if response.status_code != 200:
            return None, response.text

        return response.content, None

    except Exception as e:
        return None, str(e)


if generate_btn:
    if not hf_token or not prompt:
        st.warning("Enter HuggingFace API key and prompt.")
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
        st.warning("No previous memory.")
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
