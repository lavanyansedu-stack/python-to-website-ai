# Python-to-Website AI Agent

A beginner-friendly Streamlit app that accepts Python source, asks Groq to convert it into a Gradio or Streamlit app, and optionally uploads the generated files to Hugging Face Spaces.

## Run locally (Windows / VS Code)

1. Install Python 3.10+ and Git.
2. Open this folder in VS Code.
3. In the terminal, run:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, use Command Prompt and run `.venv\Scripts\activate.bat`, or run `python -m pip install -r requirements.txt` without activating the environment.

## Credentials

- Groq API key: https://console.groq.com/keys
- Hugging Face token: https://huggingface.co/settings/tokens

The Hugging Face token needs write access to create and upload a Space. Enter credentials in the app UI; do not hard-code or commit them.

## Publish

Enter a unique Space name and tick the publish option. The app uploads the generated `app.py`, `requirements.txt`, and deployment metadata. The resulting Space URL is `https://huggingface.co/spaces/USERNAME/SPACE-NAME`.

## Important limitations and safety

- Generated code is shown for review; this generator does not run untrusted code on its own server.
- Publishing uploads code to a public repository. Do not include passwords, API keys, private data, or proprietary source you are not allowed to publish.
- Review generated source and dependencies before publishing. AI output may need debugging.
- Hugging Face Space compute availability, pricing, account requirements, and build times can change. If publishing fails with a billing or hardware error, use an eligible Space configuration or another host.
- A public URL does not guarantee the app is successfully running; check the Space build/runtime status.
