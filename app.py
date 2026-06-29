import os
import base64
from datetime import datetime

import streamlit as st
from textblob import TextBlob

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


st.set_page_config(page_title="Rate My Professor", page_icon="⭐", layout="wide")

folder = os.path.dirname(os.path.abspath(__file__))
key_file = os.path.join(folder, "serviceAccountKey.json")
background_file = os.path.join(folder, "background.jpg")


def start_firebase():
    if firebase_admin._apps:
        return firestore.client()

    if os.path.exists(key_file):
        cred = credentials.Certificate(key_file)
        firebase_admin.initialize_app(cred)
        return firestore.client()

    if "firebase" in st.secrets:
        firebase_info = dict(st.secrets["firebase"])

        if "private_key" in firebase_info:
            firebase_info["private_key"] = firebase_info["private_key"].replace("\\n", "\n")

        cred = credentials.Certificate(firebase_info)
        firebase_admin.initialize_app(cred)
        return firestore.client()

    st.error("Firebase key not found.")
    st.stop()


db = start_firebase()


list1 = [
    "IST:",
    "Aileen Aizenshtat",
    "AJ LaConte",
    "Alex Korablev",
    "Anne Eta",
    "Antara Bajaj",
    "Anushka Chandran",
    "Brandon Yang",
    "Charnice Hoegnifioh",
    "Ezra Laufenberg",
    "Frank Petty",
    "Gabriela Rodrigues de Morais",
    "Galiya Askarova",
    "Hillary Babalola",
    "Joseph Elsayyid",
    "Kayla Hightower",
    "Kevin Patterson",
    "Micah Okwah",
    "Nathan Beyene",
    "Nhan Nguyen",
    "Pedro Goncalves de Paiva",
    "Rapunzel Chen",

    "PLE:",
    "Diego Martinez Rios",
    "Josie Morrison",
    "Liam Heraty",
    "Liza Sadaterashvili",
    "Andrey Sokolov",
    "Angela Hummingbird",
    "Christian Thomas",
    "David Johnson",
    "Jada Wilson",
    "Karolina Kedzia",
    "Lauren Johnson",
    "Paula Garcia",
    "Polina Protozanova",
    "Sherry Huang",
    "Taisei Ishikawa",
    "Taylor Craig",
    "Zeeshan Ali",

    "SGC:",
    "Bamlak Aklilu",
    "Divin Dushimimana",
    "Esha Akhtar",
    "James Obasiolu",
    "Breanna Ellison",
    "Camila Pantoja",
    "Christina Oh",
    "Henry Vo",
    "Kadiatou Keita",
    "Melanie Trotochaud",
    "Olivia Birney",
    "Phoebe Yeh",
    "Raquel Mandojana",
    "Rebecca McMillin-Hastings",
    "Salaar Ali",
    "Vitoria Souza Reyes"
]

professors = []

for item in list1:
    if not item.endswith(":"):
        professors.append(item)


def g_rat(review):
    blob = TextBlob(review)
    polarity = blob.sentiment.polarity

    rating = (polarity + 1) * 2.5
    words = review.lower()

    if "would not recommend" in words:
        rating -= 1
    if "avoid" in words:
        rating -= 1
    if "unfair" in words:
        rating -= 0.5
    if "confusing" in words:
        rating -= 0.5
    if "disorganised" in words or "disorganized" in words:
        rating -= 0.5

    rating = round(rating * 2) / 2
    rating = max(0, min(5, rating))

    return rating


def g_str(rating):
    try:
        rating = float(rating)
    except Exception:
        return "No stars"

    full_stars = int(rating)
    half_star = rating - full_stars

    stars = "★" * full_stars

    if half_star == 0.5:
        stars += "½"

    if stars == "":
        stars = "No stars"

    return stars


def add_background():
    if not os.path.exists(background_file):
        return

    with open(background_file, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image:
            linear-gradient(rgba(245,248,252,0.35), rgba(220,228,238,0.45)),
            url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .block-container {{
        padding-top: 30px;
    }}


    .review-card {{
        background: #f7f9fc;
        color: black;
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #d7dde6;
        margin-bottom: 20px;
    }}

    .average-box {{
        background: #2e8b57;
        color: white;
        padding: 24px;
        border-radius: 14px;
        font-size: 26px;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
    }}

    h1, h2, h3, h4, p, label, span {{
        color: black !important;
    }}

    .stMarkdown,
    .stText,
    .stWrite {{
        color: black !important;
    }}

    .stSelectbox div[data-baseweb="select"] > div {{
        background: white !important;
        color: black !important;
    }}

    .stTextArea textarea {{
        background: white !important;
        color: black !important;
    }}

    .stNumberInput input {{
        background: white !important;
        color: black !important;
    }}

    .stRadio label {{
        color: black !important;
    }}

    .stButton > button {{
        background: #1f77b4;
        color: white;
        border-radius: 10px;
        border: none;
        font-weight: bold;
    }}

    .stButton > button:hover {{
        background: #1565a8;
    }}

    section[data-testid="stSidebar"] {{
        background: #eef3f8;
    }}

    section[data-testid="stSidebar"] * {{
        color: black !important;
    }}

    /* This changes the >> sidebar button */
    button:has(span[data-testid="stIconMaterial"]) {{
        background: cyan !important;
        color: black !important;
        border-radius: 14px !important;
        border: none !important;
    }}

    button:has(span[data-testid="stIconMaterial"]):hover {{
        background: #00e5ff !important;
    }}

    button:has(span[data-testid="stIconMaterial"]) span {{
        color: black !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


@st.cache_data(ttl=5, show_spinner=False)
def load_reviews(professor_name):
    results = []

    docs = (
        db.collection("reviews")
        .where("professor", "==", professor_name)
        .limit(100)
        .stream(timeout=10)
    )

    for doc in docs:
        data = doc.to_dict()
        results.append(data)

    return results


def save_review(professor_name, review, final_rating, auto_rating, rating_type):
    db.collection("reviews").add(
        {
            "professor": professor_name,
            "review": review,
            "rating": float(final_rating),
            "automatic_rating": float(auto_rating),
            "rating_type": rating_type,
            "created_at": firestore.SERVER_TIMESTAMP,
            "created_local": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        timeout=10
    )

    load_reviews.clear()


add_background()

st.markdown(
    """
    <div style='text-align:center; background-color:rgba(220,230,239,0.95); padding:15px; border-radius:12px;'>
        <h1 style='color:#071b3a !important; font-size:58px;'>Rate My Professor</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

page = st.sidebar.radio("Choose one", ["See Reviews", "Write Reviews"])


if page == "See Reviews":
    st.markdown("<div class='main-box'>", unsafe_allow_html=True)

    st.header("See Reviews")

    chosen_professor = st.selectbox("Choose a professor", professors)

    if st.button("Load Reviews"):
        st.session_state["show_professor"] = chosen_professor

    if "show_professor" in st.session_state:
        name = st.session_state["show_professor"]
        st.subheader(name + " Reviews")

        try:
            with st.spinner("Loading reviews..."):
                reviews = load_reviews(name)

            if len(reviews) == 0:
                st.info("No reviews yet.")
            else:
                total_rating = 0
                rating_count = 0

                for number, data in enumerate(reviews, start=1):
                    review_words = data.get("review", "")

                    try:
                        rating = float(data.get("rating", g_rat(review_words)))
                    except Exception:
                        rating = g_rat(review_words)

                    rating_type = data.get("rating_type", "Automatic")

                    total_rating += rating
                    rating_count += 1

                    st.markdown("<div class='review-card'>", unsafe_allow_html=True)

                    st.markdown("### Review " + str(number))

                    st.write(
                        "**Rating:** "
                        + str(rating)
                        + "/5 "
                        + g_str(rating)
                        + " ("
                        + rating_type
                        + ")"
                    )

                    if rating_type == "Manual":
                        old_auto_rating = data.get("automatic_rating", "Unknown")
                        st.write("Automatic rating was: " + str(old_auto_rating) + "/5")

                    st.write(review_words)

                    st.markdown("</div>", unsafe_allow_html=True)

                average = total_rating / rating_count
                average = round(average * 2) / 2

                st.markdown(
                    "<div class='average-box'>"
                    + "Average Rating: "
                    + str(average)
                    + "/5 "
                    + g_str(average)
                    + "<br>Total Reviews: "
                    + str(rating_count)
                    + "</div>",
                    unsafe_allow_html=True
                )

        except Exception as error:
            st.error("Could not load reviews.")
            st.code(str(error))

    st.markdown("</div>", unsafe_allow_html=True)


if page == "Write Reviews":
    st.markdown("<div class='main-box'>", unsafe_allow_html=True)

    st.header("Write a Review")

    chosen_professor = st.selectbox("Choose a professor", professors)
    review_text = st.text_area("Write your review", height=180)

    if review_text.strip() != "":
        auto_rating = g_rat(review_text)
        st.write("Automatic rating: **" + str(auto_rating) + "/5 " + g_str(auto_rating) + "**")
    else:
        auto_rating = 0

    rating_choice = st.radio(
        "Which rating do you want to use?",
        ["Use automatic rating", "Use my own rating"]
    )

    if rating_choice == "Use automatic rating":
        final_rating = auto_rating
        rating_type = "Automatic"
    else:
        final_rating = st.number_input(
            "Your rating",
            min_value=0.0,
            max_value=5.0,
            value=float(auto_rating),
            step=0.5
        )
        rating_type = "Manual"

    if st.button("Submit Review"):
        if review_text.strip() == "":
            st.warning("Please write a review first.")
        else:
            try:
                final_rating = round(float(final_rating) * 2) / 2

                with st.spinner("Saving review..."):
                    save_review(
                        chosen_professor,
                        review_text.strip(),
                        final_rating,
                        auto_rating,
                        rating_type
                    )

                st.success("Your review was submitted. Final rating: " + str(final_rating) + "/5")

            except Exception as error:
                st.error("The review could not be saved.")
                st.code(str(error))

    st.markdown("</div>", unsafe_allow_html=True)
