import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter

# -----------------------------
# PAGE SETUP
# -----------------------------
st.set_page_config(
    page_title="Rate My Professor",
    layout="wide"
)

# -----------------------------
# FIREBASE SETUP
# -----------------------------
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# -----------------------------
# PROFESSOR LIST
# -----------------------------
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
    "Pedro Goncalves de Morais",
    "Ryan Pocius",
    "Saman Iqbal",
    "Shannon McCauley",
    "Yining Chen"
]

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-image: url("background.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.title-box {
    background-color: rgba(235, 242, 250, 0.95);
    width: fit-content;
    margin: 20px auto 35px auto;
    padding: 20px 35px;
}

.title-box h1 {
    color: #071b3a;
    font-family: Georgia, serif;
    font-size: 52px;
    font-weight: bold;
    margin: 0;
}

.big-box {
    width: 94%;
    height: 570px;
    background-color: rgba(255, 255, 255, 0.96);
    border: 3px solid #444;
    margin: 0 auto 25px auto;
    overflow-y: auto;
    padding: 25px;
}

.department {
    text-align: center;
    font-size: 34px;
    color: purple;
    font-weight: bold;
    font-family: Georgia, serif;
    margin-bottom: 12px;
}

div.stButton > button {
    width: 72%;
    height: 55px;
    display: block;
    margin: 10px auto;
    background-color: white;
    color: #071b3a;
    border: 2px solid #555;
    border-radius: 0px;
    font-size: 18px;
}

div.stButton > button:hover {
    border: 2px solid #071b3a;
    color: #071b3a;
    background-color: #eef3fa;
}

.review-card {
    background-color: #f7f7f7;
    border: 1px solid #999;
    padding: 15px;
    margin-bottom: 15px;
    color: black;
}

.review-title {
    font-size: 24px;
    color: #071b3a;
    font-weight: bold;
    text-align: center;
    margin-bottom: 15px;
}

.average {
    font-size: 22px;
    text-align: center;
    font-weight: bold;
    color: purple;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION STATE
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_professor" not in st.session_state:
    st.session_state.selected_professor = ""

# -----------------------------
# FUNCTIONS
# -----------------------------
def get_reviews(professor_name):
    try:
        reviews_ref = db.collection("reviews")
        query = reviews_ref.where(
            filter=FieldFilter("professor", "==", professor_name)
        ).stream(timeout=10)

        reviews = []
        for doc in query:
            reviews.append(doc.to_dict())

        return reviews

    except Exception as e:
        st.error("Could not load reviews from Firebase.")
        st.write(e)
        return []


def add_review(professor_name, rating, review_text):
    try:
        db.collection("reviews").add({
            "professor": professor_name,
            "rating": rating,
            "review": review_text
        })
        return True

    except Exception as e:
        st.error("Could not submit review to Firebase.")
        st.write(e)
        return False


def show_home():
    st.markdown("""
    <div class="title-box">
        <h1>Choose a Professor to View Reviews</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="big-box"></div>', unsafe_allow_html=True)

    st.markdown('<div class="department">IST:</div>', unsafe_allow_html=True)

    for professor in professors:
        if professor != "IST:":
            if st.button(professor, key="view_" + professor):
                st.session_state.selected_professor = professor
                st.session_state.page = "reviews"
                st.rerun()


def show_reviews():
    professor = st.session_state.selected_professor

    st.markdown(f"""
    <div class="title-box">
        <h1>{professor}</h1>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Back"):
        st.session_state.page = "home"
        st.rerun()

    reviews = get_reviews(professor)

    st.markdown('<div class="big-box">', unsafe_allow_html=True)

    st.markdown(
        f'<div class="review-title">Reviews for {professor}</div>',
        unsafe_allow_html=True
    )

    if len(reviews) == 0:
        st.write("No reviews yet.")
    else:
        ratings = []

        for review in reviews:
            rating = review.get("rating", 0)
            text = review.get("review", "")

            try:
                ratings.append(float(rating))
            except:
                pass

            st.markdown(f"""
            <div class="review-card">
                <b>Rating:</b> {rating}/5<br><br>
                {text}
            </div>
            """, unsafe_allow_html=True)

        if len(ratings) > 0:
            average = sum(ratings) / len(ratings)
            st.markdown(
                f'<div class="average">Average Rating: {average:.2f}/5</div>',
                unsafe_allow_html=True
            )

    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("Leave a Review")

    rating = st.slider("Rating", 1, 5, 3)
    review_text = st.text_area("Write your review")

    if st.button("Submit Review"):
        if review_text.strip() == "":
            st.warning("Please write a review first.")
        else:
            worked = add_review(professor, rating, review_text)

            if worked:
                st.success("Review submitted.")
                st.rerun()


# -----------------------------
# RUN APP
# -----------------------------
if st.session_state.page == "home":
    show_home()
else:
    show_reviews()
