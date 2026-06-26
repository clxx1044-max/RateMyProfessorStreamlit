import base64
import os

import streamlit as st
from textblob import TextBlob

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


st.set_page_config(
    page_title="Rate My Professor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

folder = os.path.dirname(os.path.abspath(__file__))
key_file = os.path.join(folder, "serviceAccountKey.json")
background_file = os.path.join(folder, "background.jpg")


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


@st.cache_resource
def get_db():
    if not os.path.exists(key_file):
        return None

    if not firebase_admin._apps:
        cred = credentials.Certificate(key_file)
        firebase_admin.initialize_app(cred)

    return firestore.client()


db = get_db()


def get_background_image():
    if not os.path.exists(background_file):
        return ""

    with open(background_file, "rb") as f:
        data = f.read()

    encoded = base64.b64encode(data).decode()
    return "data:image/jpg;base64," + encoded


bg = get_background_image()


st.markdown(
    f"""
    <style>
    [data-testid="stSidebar"] {{
        display: none;
    }}

    [data-testid="collapsedControl"] {{
        display: none;
    }}

    header {{
        display: none;
    }}

    .stApp {{
        background-image: url('{bg}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .block-container {{
        max-width: 1280px;
        padding-top: 55px;
        padding-left: 45px;
        padding-right: 45px;
    }}

    .main-title {{
        background-color: #dce6ef;
        color: #071b3a;
        font-family: "Times New Roman", serif;
        font-size: 76px;
        font-weight: bold;
        text-align: center;
        padding: 35px 10px;
        border-radius: 4px;
        margin: 70px auto 25px auto;
        width: 760px;
        box-sizing: border-box;
    }}

    .home-box {{
        background-color: #f2f2f2;
        border: 3px ridge #999999;
        width: 560px;
        height: 300px;
        margin: 45px auto 0 auto;
        padding-top: 32px;
        box-sizing: border-box;
    }}

    .page-title {{
        background-color: #dce6ef;
        color: #071b3a;
        font-family: "Times New Roman", serif;
        font-size: 44px;
        font-weight: bold;
        text-align: center;
        margin: 10px auto 25px auto;
        width: fit-content;
        padding: 5px 18px;
    }}

    .big-box {{
        background-color: #f2f2f2;
        border: 3px ridge #999999;
        width: 980px;
        height: 575px;
        margin: 0 auto;
        padding: 20px;
        overflow-y: auto;
        box-sizing: border-box;
    }}

    .review-box {{
        background-color: #dce6ef;
        width: 800px;
        min-height: 560px;
        margin: 20px auto;
        padding: 20px;
        box-sizing: border-box;
    }}

    .reviews-box {{
        background-color: #dce6ef;
        width: 850px;
        min-height: 620px;
        margin: 20px auto;
        padding: 20px;
        box-sizing: border-box;
    }}

    .section-title {{
        color: #5c258d;
        font-family: "Times New Roman", serif;
        font-size: 30px;
        font-weight: bold;
        text-align: center;
        margin-top: 14px;
        margin-bottom: 10px;
    }}

    .review-card {{
        background-color: white;
        color: #071b3a;
        border: 1px solid #bbbbbb;
        padding: 14px;
        margin-bottom: 14px;
        font-family: Arial, sans-serif;
        font-size: 18px;
    }}

    .average {{
        background-color: #f2f2f2;
        color: #071b3a;
        border: 2px solid #999999;
        padding: 14px;
        margin-top: 20px;
        text-align: center;
        font-family: "Times New Roman", serif;
        font-size: 26px;
        font-weight: bold;
    }}

    div.stButton > button {{
        font-family: "Times New Roman", serif;
        font-weight: bold;
        color: #071b3a;
        background-color: white;
        border: 2px solid #999999;
        border-radius: 2px;
        min-height: 46px;
    }}

    .home-box div.stButton > button {{
        font-size: 32px;
        width: 100%;
        min-height: 75px;
    }}

    .big-box div.stButton > button {{
        font-size: 20px;
        width: 430px;
        margin: auto;
        display: block;
    }}

    .back-button div.stButton > button {{
        background-color: #071b3a;
        color: white;
        width: 110px;
        min-height: 45px;
        font-size: 18px;
    }}

    textarea {{
        font-size: 18px !important;
        font-family: Arial, sans-serif !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


if "page" not in st.session_state:
    st.session_state.page = "home"

if "person" not in st.session_state:
    st.session_state.person = ""

if "review_text" not in st.session_state:
    st.session_state.review_text = ""

if "auto_rating" not in st.session_state:
    st.session_state.auto_rating = 0


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
        stars = stars + "½"

    if stars == "":
        stars = "No stars"

    return stars


def change_page(page):
    st.session_state.page = page


def choose_person(name, page):
    st.session_state.person = name
    st.session_state.page = page


def back_home():
    st.session_state.page = "home"
    st.session_state.person = ""
    st.session_state.review_text = ""
    st.session_state.auto_rating = 0


def professor_buttons(mode):
    st.markdown('<div class="big-box">', unsafe_allow_html=True)

    for item in list1:
        if item.endswith(":"):
            st.markdown('<div class="section-title">' + item + '</div>', unsafe_allow_html=True)
        else:
            left, mid, right = st.columns([1, 2, 1])
            with mid:
                if mode == "write":
                    if st.button(item, key="write_" + item):
                        choose_person(item, "write_review")
                        st.rerun()
                else:
                    if st.button(item, key="see_" + item):
                        choose_person(item, "show_reviews")
                        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


def save_review(name, review, final_rating, auto_rating, rating_type):
    if db is None:
        st.error("Firebase is not connected. Put serviceAccountKey.json in the same folder as app.py.")
        return False

    try:
        db.collection("reviews").add({
            "professor": name,
            "review": review,
            "rating": float(final_rating),
            "automatic_rating": float(auto_rating),
            "rating_type": rating_type,
            "created_at": firestore.SERVER_TIMESTAMP
        })
        return True
    except Exception as error:
        st.error("The review could not be saved. " + str(error))
        return False


def load_reviews(name):
    if db is None:
        st.error("Firebase is not connected. Put serviceAccountKey.json in the same folder as app.py.")
        return []

    try:
        docs = db.collection("reviews").where("professor", "==", name).stream()
        results = []
        for doc in docs:
            results.append(doc.to_dict())
        return results
    except Exception as error:
        st.error("Could not load reviews. " + str(error))
        return []


def home_page():
    st.markdown('<div class="main-title">Rate My Professor</div>', unsafe_allow_html=True)
    st.markdown('<div class="home-box">', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 4, 1])
    with c2:
        if st.button("💬  See Reviews", key="home_see"):
            change_page("see_list")
            st.rerun()

        if st.button("✎  Write Reviews", key="home_write"):
            change_page("write_list")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


def list_page(title, mode):
    st.markdown('<div class="back-button">', unsafe_allow_html=True)
    if st.button("Back", key="back_" + mode):
        back_home()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="page-title">' + title + '</div>', unsafe_allow_html=True)
    professor_buttons(mode)


def write_review_page():
    st.markdown('<div class="back-button">', unsafe_allow_html=True)
    if st.button("Back", key="back_write_review"):
        change_page("write_list")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    name = st.session_state.person
    st.markdown('<div class="review-box">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Leave a review for ' + name + '</div>', unsafe_allow_html=True)

    review = st.text_area("", height=260, key="typed_review")

    if st.button("Submit Review", key="submit_review"):
        if review.strip() == "":
            st.warning("Please write a review first.")
        else:
            st.session_state.review_text = review.strip()
            st.session_state.auto_rating = g_rat(review.strip())
            change_page("check_rating")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


def check_rating_page():
    st.markdown('<div class="back-button">', unsafe_allow_html=True)
    if st.button("Back", key="back_check"):
        change_page("write_review")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    name = st.session_state.person
    review = st.session_state.review_text
    auto_rating = st.session_state.auto_rating

    st.markdown('<div class="review-box">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Check the Automatic Rating</div>', unsafe_allow_html=True)
    st.markdown(
        '<h3 style="text-align:center;color:#071b3a;font-family:Times New Roman;">The programme gave this review:</h3>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<h1 style="text-align:center;color:#5c258d;font-family:Times New Roman;">'
        + str(auto_rating) + '/5  ' + g_str(auto_rating) + '</h1>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<h3 style="text-align:center;color:#071b3a;font-family:Times New Roman;">Do you agree with this rating?</h3>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns([1, 3, 1])
    with c2:
        if st.button("Yes, use this automatic rating", key="use_auto"):
            ok = save_review(name, review, auto_rating, auto_rating, "Automatic")
            if ok:
                st.success("Your review was submitted. Final rating: " + str(auto_rating) + "/5")
                st.session_state.typed_review = ""

        st.markdown(
            '<h3 style="text-align:center;color:#071b3a;font-family:Times New Roman;">Or give your own rating:</h3>',
            unsafe_allow_html=True
        )
        manual = st.number_input("", min_value=0.0, max_value=5.0, value=float(auto_rating), step=0.5)

        if st.button("Submit My Rating", key="submit_manual"):
            manual = round(float(manual) * 2) / 2
            ok = save_review(name, review, manual, auto_rating, "Manual")
            if ok:
                st.success("Your review was submitted. Final rating: " + str(manual) + "/5")
                st.session_state.typed_review = ""

    st.markdown('</div>', unsafe_allow_html=True)


def show_reviews_page():
    st.markdown('<div class="back-button">', unsafe_allow_html=True)
    if st.button("Back", key="back_show_reviews"):
        change_page("see_list")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    name = st.session_state.person
    st.markdown('<div class="reviews-box">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">' + name + ' Reviews</div>', unsafe_allow_html=True)

    reviews = load_reviews(name)

    if len(reviews) == 0:
        st.markdown('<div class="review-card">No reviews yet.</div>', unsafe_allow_html=True)
    else:
        total_rating = 0
        count = 0
        number = 1

        for data in reviews:
            review_words = data.get("review", "")

            try:
                rating = float(data.get("rating", g_rat(review_words)))
            except Exception:
                rating = g_rat(review_words)

            rating_type = data.get("rating_type", "Automatic")
            total_rating += rating
            count += 1

            extra = ""
            if rating_type == "Manual":
                old_auto_rating = data.get("automatic_rating", "Unknown")
                extra = "<br>Automatic rating was: " + str(old_auto_rating) + "/5"

            st.markdown(
                '<div class="review-card"><b>Review ' + str(number) + ':</b><br>'
                + 'Rating: ' + str(rating) + '/5 ' + g_str(rating) + ' (' + rating_type + ')'
                + extra
                + '<br><br>' + review_words.replace("\n", "<br>")
                + '</div>',
                unsafe_allow_html=True
            )
            number += 1

        average = total_rating / count
        average = round(average * 2) / 2
        st.markdown(
            '<div class="average">Average Rating: ' + str(average) + '/5 ' + g_str(average) + '</div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)


if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "see_list":
    list_page("Choose a Professor to View Reviews", "see")
elif st.session_state.page == "write_list":
    list_page("Choose a Professor to Review", "write")
elif st.session_state.page == "write_review":
    write_review_page()
elif st.session_state.page == "check_rating":
    check_rating_page()
elif st.session_state.page == "show_reviews":
    show_reviews_page()
