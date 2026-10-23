
import streamlit as st
import requests
import re
import os
import sys
import time
import socket
import subprocess
import tempfile

st.set_page_config(
    page_title="Python to Website AI",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Python to Website AI Agent")
st.write("Convert Python code into a live Streamlit website.")

api_key = st.text_input("Groq API Key", type="password")

uploaded = st.file_uploader(
    "Upload Python file (.py)",
    type=["py"]
)

code = st.text_area(
    "Or paste your Python code",
    height=220
)

model = st.text_input(
    "Groq model ID",
    value="openai/gpt-oss-120b"
)

if st.button("✨ Generate Website", type="primary"):

    source = (
        uploaded.getvalue().decode("utf-8", errors="replace")
        if uploaded else code
    )

    if not api_key.strip():
        st.error("Enter your Groq API key.")

    elif not source.strip():
        st.error("Upload a Python file or paste your code.")

    elif not model.strip():
        st.error("Enter a supported Groq model ID.")

    else:
        prompt = f"""
Convert the Python program below into a complete,
working Streamlit web application.

Requirements:
- Preserve its main functionality.
- Replace terminal inputs with Streamlit controls.
- Display results on the webpage.
- Include required imports and error handling.
- Do not invent API keys.
- Do not execute the original source code.
- Return only complete Python code inside a python code block.

Original Python code:
{source}
"""

        with st.spinner("Generating your website..."):
            try:
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key.strip()}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model.strip(),
                        "messages": [
                            {
                                "role": "system",
                                "content": (
                                    "Generate complete Streamlit applications."
                                )
                            },
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.1
                    },
                    timeout=180
                )

                response.raise_for_status()

                result = response.json()["choices"][0]["message"]["content"]

                match = re.search(
                    r"```(?:python)?\s*(.*?)```",
                    result,
                    re.S
                )

                app_code = (
                    match.group(1).strip()
                    if match else result.strip()
                )

                if not app_code:
                    st.error("No code was generated.")
                else:
                    st.session_state["app_code"] = app_code
                    st.session_state["preview_ready"] = True
                    st.success("Website code generated!")

            except requests.RequestException as e:
                st.error(f"Groq API error: {e}")

            except (KeyError, ValueError) as e:
                st.error(f"Could not process AI response: {e}")


if st.session_state.get("preview_ready"):

    st.subheader("🧑‍💻 Generated Python Code")

    st.code(
        st.session_state["app_code"],
        language="python"
    )

    st.info(
        "Review the code before running it. "
        "Only preview code you trust."
    )

    if st.button("🌐 Preview Website", type="primary"):

        try:
            # Find an available port for the preview app.
            with socket.socket() as sock:
                sock.bind(("127.0.0.1", 0))
                port = sock.getsockname()[1]

            # Save the generated application.
            preview_dir = tempfile.mkdtemp(
                prefix="python_website_"
            )

            app_path = os.path.join(preview_dir, "app.py")

            with open(app_path, "w", encoding="utf-8") as file:
                file.write(st.session_state["app_code"])

            # Launch a separate Streamlit application.
            log_path = os.path.join(preview_dir, "app.log")
            log_file = open(log_path, "w", encoding="utf-8")

            process = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "streamlit",
                    "run",
                    app_path,
                    "--server.port",
                    str(port),
                    "--server.address",
                    "127.0.0.1",
                    "--server.headless",
                    "true"
                ],
                stdout=log_file,
                stderr=subprocess.STDOUT,
                cwd=preview_dir
            )

            st.session_state["preview_process"] = process
            st.session_state["preview_port"] = port
            st.session_state["preview_log"] = log_path
            st.session_state["preview_dir"] = preview_dir

            time.sleep(3)

            if process.poll() is not None:
                with open(log_path, encoding="utf-8") as file:
                    error_log = file.read()

                st.error("The preview app stopped during startup.")
                st.code(error_log[-4000:] or "No error log available.")

            else:
                st.session_state["preview_started"] = True
                st.rerun()

        except Exception as e:
            st.error(f"Could not start preview: {e}")


if st.session_state.get("preview_started"):

    process = st.session_state.get("preview_process")
    port = st.session_state.get("preview_port")

    if process and process.poll() is None and port:
        st.subheader("🌐 Live Website Preview")

        st.markdown(
            f"[Open website in a new browser tab](http://localhost:{port})"
        )

        st.components.v1.iframe(
            f"http://localhost:{port}",
            height=700,
            scrolling=True
        )

        if st.button("⏹ Stop Preview"):
            process.terminate()
            st.session_state["preview_started"] = False
            st.session_state["preview_ready"] = False
            st.success("Preview stopped.")
            st.rerun()

    else:
        st.error("The preview process is no longer running.")
