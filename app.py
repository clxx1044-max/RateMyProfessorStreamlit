import base64
import os

import streamlit as st
from textblob import TextBlob

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# ============================================================
# Page setup
# ============================================================

st.set_page_config(
    page_title="Rate My Professor",
    page_icon="⭐",
    layout="centered"
)


# ============================================================
# Background and styling
# ============================================================

def load_background():
    folder = os.path.dirname(os.path.abspath(__file__))
    background_file = os.path.join(folder, "background.jpg")

    if os.path.exists(background_file):
        with open(background_file, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()

        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image:
                    linear-gradient(rgba(0, 0, 0, 0.25), rgba(0, 0, 0, 0.25)),
                    url("data:image/jpg;base64,{encoded_image}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            .stApp {
                background: linear-gradient(135deg, #dce6ef, #ffffff);
            }
            </style>
            """,
            unsafe_allow_html=True
        )


def load_css():
    st.markdown(
        """
        <style>
        html, body, [class*="css"] {
            font-family: "Times New Roman", serif;
        }

        .block-container {
            padding-top: 3rem;
            padding-bottom: 3rem;
        }

        .main-title {
            background-color: #dce6ef;
            color: #071b3a;
            text-align: center;
            font-size: 76px;
            font-weight: bold;
            padding: 18px 30px;
            border-radius: 10px;
            margin-top: 40px;
            margin-bottom: 50px;
            border: 3px solid rgba(7, 27, 58, 0.2);
            box-shadow: 0 6px 18px rgba(0,0,0,0.18);
        }

        .page-title {
            background-color: #dce6ef;
            color: #071b3a;
            text-align: center;
            font-size: 44px;
            font-weight: bold;
            padding: 12px 24px;
            border-radius: 10px;
            margin-top: 20px;
            margin-bottom: 30px;
            border: 3px solid rgba(7, 27, 58, 0.2);
            box-shadow: 0 6px 18px rgba(0,0,0,0.18);
        }

        .section-title {
            color: #5c258d;
            background-color: #f2f2f2;
            border-radius: 8px;
            font-size: 32px;
            font-weight: bold;
            text-align: center;
            margin-top: 26px;
            margin-bottom: 12px;
            padding: 8px;
        }

        .rating-big {
            color: #5c258d;
            background-color: #f2f2f2;
            border: 3px ridge #999;
            border-radius: 10px;
            font-size: 42px;
            font-weight: bold;
            text-align: center;
            margin: 20px 0;
            padding: 20px;
        }

        .review-card {
            background-color: white;
            border: 2px solid #cccccc;
            border-radius: 8px;
            padding: 18px;
            margin: 16px 0;
            color: #071b3a;
            font-family: Arial, sans-serif;
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        }

        .review-card h2 {
            margin-top: 0;
            color: #071b3a;
            font-family: "Times New Roman", serif;
        }

        .average-box {
            background-color: #dce6ef;
            border: 2px solid #071b3a;
            border-radius: 8px;
            padding: 18px;
            margin-top: 25px;
            color: #071b3a;
            font-size: 28px;
            font-weight: bold;
            text-align: center;
        }

        .info-box {
            background-color: #f2f2f2;
            border: 3px ridge #999;
            border-radius: 10px;
            padding: 22px;
            margin-top: 20px;
            margin-bottom: 20px;
            color: #071b3a;
            text-align: center;
            box-shadow: 0 6px 18px rgba(0,0,0,0.18);
        }

        .small-note {
            color: #333333;
            font-size: 15px;
            text-align: center;
        }

        div.stButton > button {
            background-color: white;
            color: #071b3a;
            border: 2px solid #071b3a;
            border-radius: 8px;
            font-family: "Times New Roman", serif;
            font-size: 22px;
            font-weight: bold;
            padding: 10px 18px;
            margin-top: 8px;
            margin-bottom: 8px;
        }

        div.stButton > button:hover {
            background-color: #dce6ef;
            color: #071b3a;
            border: 2px solid #071b3a;
        }

        textarea {
            font-family: Arial, sans-serif !important;
            font-size: 18px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


load_background()
load_css()


# ============================================================
# Firebase connection
# ============================================================

@st.cache_resource
def get_database():
    """
    Local:
    Use serviceAccountKey.json in the same folder as app.py.

    Streamlit Cloud:
    Use [firebase_service_account] in Streamlit secrets.
    """

    if not firebase_admin._apps:
        folder = os.path.dirname(os.path.abspath(__file__))
        key_file = os.path.join(folder, "serviceAccountKey.json")

        secret_data = None

        try:
            if "firebase_service_account" in st.secrets:
                secret_data = dict(st.secrets["firebase_service_account"])
        except Exception:
            secret_data = None

        if secret_data is not None:
            cred = credentials.Certificate(secret_data)
            firebase_admin.initialize_app(cred)

        elif os.path.exists(key_file):
            cred = credentials.Certificate(key_file)
            firebase_admin.initialize_app(cred)

        else:
            st.error(
                "Firebase is not connected. Locally, add serviceAccountKey.json. "
                "On Streamlit Cloud, add Firebase credentials in Secrets."
            )
            return None

    return firestore.client()

db = get_database()


# ============================================================
# Professor list
# ============================================================

professors = [
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


# ============================================================
# Rating functions
# ============================================================

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
    full_stars = int(rating)
    half_star = rating - full_stars

    stars = "★" * full_stars

    if half_star == 0.5:
        stars = stars + "½"

    if stars == "":
        stars = "No stars"

    return stars


# ============================================================
# Session state / navigation
# ============================================================

def setup_state():
    if "page" not in st.session_state:
        st.session_state.page = "home"

    if "chosen_professor" not in st.session_state:
        st.session_state.chosen_professor = ""

    if "current_review" not in st.session_state:
        st.session_state.current_review = ""

    if "auto_rating" not in st.session_state:
        st.session_state.auto_rating = 0.0

    if "success_message" not in st.session_state:
        st.session_state.success_message = ""


def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()


def choose_professor(page_name, professor_name):
    st.session_state.chosen_professor = professor_name
    st.session_state.page = page_name
    st.rerun()


def show_success_message():
    if st.session_state.success_message != "":
        st.success(st.session_state.success_message)
        st.session_state.success_message = ""


def back_button(target_page):
    if st.button("Back"):
        go_to(target_page)


setup_state()


# ============================================================
# Firestore helper functions
# ============================================================

def save_review_to_db(name, review, final_rating, auto_rating, rating_type):
    if db is None:
        st.error("Firebase is not connected.")
        return False

    try:
        db.collection("reviews").add({
            "professor": name,
            "review": review,
            "rating": final_rating,
            "automatic_rating": auto_rating,
            "rating_type": rating_type,
            "created_at": firestore.SERVER_TIMESTAMP
        })

        return True

    except Exception as error:
        st.error("The review could not be saved.")
        st.code(str(error))
        return False


def get_reviews_for_professor(name):
    if db is None:
        st.error("Firebase is not connected.")
        return []

    try:
        reviews = db.collection("reviews").where(
            "professor",
            "==",
            name
        ).stream()

        results = []

        for review in reviews:
            results.append(review.to_dict())

        return results

    except Exception as error:
        st.error("Could not load reviews.")
        st.exception(error)
        return []

    except Exception as error:
        st.error("Could not load reviews.")
        st.code(str(error))
        return []


# ============================================================
# Pages
# ============================================================

def home_page():
    st.markdown(
        '<div class="main-title">Rate My Professor</div>',
        unsafe_allow_html=True
    )

    show_success_message()

    left, middle, right = st.columns([1, 2, 1])

    with middle:
        if st.button("💬  See Reviews"):
            go_to("see_list")

        if st.button("✎  Write Reviews"):
            go_to("write_list")


def professor_list_page(mode):
    if mode == "write":
        st.markdown(
            '<div class="page-title">Choose a Professor to Review</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="page-title">Choose a Professor to View Reviews</div>',
            unsafe_allow_html=True
        )

    back_button("home")

    for item in professors:
        if item.endswith(":"):
            st.markdown(
                f'<div class="section-title">{item}</div>',
                unsafe_allow_html=True
            )
        else:
            if mode == "write":
                if st.button(item, key="write_" + item):
                    choose_professor("write_review", item)
            else:
                if st.button(item, key="see_" + item):
                    choose_professor("show_reviews", item)


def write_review_page():
    name = st.session_state.chosen_professor

    st.markdown(
        f'<div class="page-title">Leave a review for {name}</div>',
        unsafe_allow_html=True
    )

    back_button("write_list")

    review = st.text_area(
        "Write your review here:",
        height=260,
        key="review_text_area"
    )

    if st.button("Submit Review"):
        review = review.strip()

        if review == "":
            st.warning("Please write a review first.")
        else:
            auto_rating = g_rat(review)

            st.session_state.current_review = review
            st.session_state.auto_rating = auto_rating
            st.session_state.page = "check_rating"

            st.rerun()


def check_rating_page():
    name = st.session_state.chosen_professor
    review = st.session_state.current_review
    auto_rating = st.session_state.auto_rating

    st.markdown(
        '<div class="page-title">Check the Automatic Rating</div>',
        unsafe_allow_html=True
    )

    back_button("write_review")

    st.markdown(
        """
        <div class="info-box">
            <h3>The programme gave this review:</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="rating-big">{auto_rating}/5 {g_str(auto_rating)}</div>',
        unsafe_allow_html=True
    )

    st.write("Do you agree with this rating?")

    if st.button("Yes, use this automatic rating"):
        saved = save_review_to_db(
            name,
            review,
            auto_rating,
            auto_rating,
            "Automatic"
        )

        if saved:
            st.session_state.success_message = (
                "Your review was submitted. Final rating: "
                + str(auto_rating)
                + "/5"
            )
            go_to("home")

    st.subheader("Or give your own rating:")

    manual_rating = st.number_input(
        "Manual rating",
        min_value=0.0,
        max_value=5.0,
        step=0.5,
        value=float(auto_rating)
    )

    if st.button("Submit My Rating"):
        manual_rating = round(manual_rating * 2) / 2

        saved = save_review_to_db(
            name,
            review,
            manual_rating,
            auto_rating,
            "Manual"
        )

        if saved:
            st.session_state.success_message = (
                "Your review was submitted. Final rating: "
                + str(manual_rating)
                + "/5"
            )
            go_to("home")

    st.markdown(
        '<p class="small-note">Use a number from 0 to 5, like 1, 2.5, 4, or 5.</p>',
        unsafe_allow_html=True
    )


def show_reviews_page():
    name = st.session_state.chosen_professor

    st.markdown(
        f'<div class="page-title">{name} Reviews</div>',
        unsafe_allow_html=True
    )

    back_button("see_list")

    with st.spinner("Loading reviews..."):
        reviews = get_reviews_for_professor(name)

    if len(reviews) == 0:
        st.info("No reviews yet.")
        return

    number = 1
    total_rating = 0

    for data in reviews:
        review_text = data.get("review", "")

        rating = data.get("rating")

        if rating is None:
            rating = g_rat(review_text)

        rating_type = data.get("rating_type", "Automatic")

        total_rating = total_rating + rating

        review_html = f"""
        <div class="review-card">
            <h2>Review {number}</h2>
            <p><strong>Rating:</strong> {rating}/5 {g_str(rating)} ({rating_type})</p>
        """

        if rating_type == "Manual":
            old_auto_rating = data.get("automatic_rating", "Unknown")

            review_html += f"""
            <p><strong>Automatic rating was:</strong> {old_auto_rating}/5</p>
            """

        review_html += f"""
            <p>{review_text}</p>
        </div>
        """

        st.markdown(review_html, unsafe_allow_html=True)

        number = number + 1

    average = total_rating / (number - 1)
    average = round(average * 2) / 2

    st.markdown(
        f'<div class="average-box">Average Rating: {average}/5 {g_str(average)}</div>',
        unsafe_allow_html=True
    )


# ============================================================
# Run the selected page
# ============================================================

if st.session_state.page == "home":
    home_page()

elif st.session_state.page == "write_list":
    professor_list_page("write")

elif st.session_state.page == "see_list":
    professor_list_page("see")

elif st.session_state.page == "write_review":
    write_review_page()

elif st.session_state.page == "check_rating":
    check_rating_page()

elif st.session_state.page == "show_reviews":
    show_reviews_page()

else:
    st.session_state.page = "home"
    st.rerun()
