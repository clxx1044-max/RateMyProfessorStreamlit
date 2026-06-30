# Rate My Professor Streamlit Website

This is a Streamlit web version of Tkinter Rate My Professor programme.

## Files

- `app.py` - main website code
- `requirements.txt` - Python packages
- `.gitignore` - prevents private Firebase key from being uploaded
- `.streamlit/secrets.example.toml` - example format for Streamlit Cloud secrets

## Setup

1. Put `serviceAccountKey.json` in this folder.
2. Optional: put `background.jpg` in this folder.
3. Install packages:

```bash
pip3 install -r requirements.txt
```

4. Run:

```bash
streamlit run app.py
```

## Deploy to Streamlit Cloud

Do NOT upload `serviceAccountKey.json` to GitHub.

Instead, paste your Firebase service account JSON into Streamlit Cloud secrets using the format shown in:

`.streamlit/secrets.example.toml`

## Firestore

The app uses the `reviews` collection with these fields:

- professor
- review
- rating
- automatic_rating
- rating_type
- created_at
