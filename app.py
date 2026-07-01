import os
import base64
import html
from datetime import datetime
import hashlib
import streamlit as st
from textblob import TextBlob

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def generate_sha256(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


st.set_page_config(
    page_title="Rate My Professor",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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

departments: dict = {}
_dept = None
for _item in list1:
    if _item.endswith(":"): _dept = _item[:-1]
    else: departments[_item] = _dept


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

DESIGN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,400&family=Source+Sans+3:wght@400;500;600;700&display=swap');

:root {
  --paper:    #F7F3EC;
  --surf:     #FFFFFF;
  --surf2:    #F4F0E8;
  --ink:      #20262F;
  --ink2:     #6B655C;
  --line:     #E3DACE;
  --accent:   #2F5233;
  --adk:      #1E3721;
  --alt:      #E7EDE4;
  --gold:     #B8832C;
  --goldlt:   #F5E8D0;
  --brick:    #8C3A34;
  --bricklt:  #F3E3DF;
  --r:        14px;
  --sh:       0 1px 3px rgba(32,38,47,.05),0 6px 20px rgba(32,38,47,.07);
  --shsm:     0 1px 2px rgba(32,38,47,.06);
}

html,body,[class*="css"],p,span,div,label,input,textarea {
  font-family:'Source Sans 3',-apple-system,system-ui,sans-serif;
  color: var(--ink);
  box-sizing: border-box;
}

.stApp { background:var(--paper) !important; }

[data-testid="stHeader"] {
  visibility:hidden !important;
  height:0 !important;
}

[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu,
footer { visibility:hidden !important; height:0 !important; }

.block-container {
  max-width:900px !important;
  padding:3rem 2rem 5rem !important;
  margin:0 auto !important;
}

/* ── Masthead ── */
.mast { text-align:center; padding:.25rem 0 1.4rem; }
.mast-eye {
  font-size:.7rem; letter-spacing:.24em; font-weight:700;
  color:var(--accent); text-transform:uppercase; margin:0 0 .65rem;
}
.mast-h1 {
  font-family:'Fraunces',Georgia,serif;
  font-weight:600; font-size:2.85rem; color:var(--ink);
  margin:0; letter-spacing:-.02em; line-height:1.1;
}
.mast-sub { color:var(--ink2); font-size:.97rem; margin:.45rem 0 0; }
.mast-rule {
  width:48px; height:3px; background:var(--accent);
  margin:1rem auto 0; border-radius:2px;
}

/* ── Hero banner ── */
.hero {
  position:relative; width:100%; height:196px;
  border-radius:var(--r); background-size:cover;
  background-position:center 38%; overflow:hidden;
  margin:1.4rem 0 1.9rem; box-shadow:var(--sh);
}
.hero::after {
  content:""; position:absolute; inset:0;
  background:linear-gradient(180deg,transparent 50%,rgba(18,22,16,.5) 100%);
}
.hero-cap {
  position:absolute; bottom:13px; left:18px;
  color:rgba(247,243,236,.88); font-size:.7rem;
  letter-spacing:.12em; font-weight:700; text-transform:uppercase; z-index:2;
}

/* ── Tabs ── */
[data-testid="stTabs"] button[role="tab"] {
  font-family:'Source Sans 3',sans-serif !important;
  font-weight:600 !important; font-size:.88rem !important;
  color:var(--ink2) !important; padding:.52rem 1rem !important;
  letter-spacing:.01em;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
  color:var(--accent) !important;
}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
  background:var(--accent) !important; height:2.5px !important;
}
[data-testid="stTabs"] [data-baseweb="tab-border"] {
  background:var(--line) !important;
}

/* ── Section header ── */
.tab-h {
  font-family:'Fraunces',serif; font-size:1.4rem;
  font-weight:600; color:var(--ink); margin:1.4rem 0 .2rem;
}
.tab-p { color:var(--ink2); font-size:.88rem; margin:0 0 1.2rem; }

/* ── Form controls ── */
.stTextInput input, .stTextArea textarea, .stNumberInput input {
  background:var(--surf) !important;
  border:1.5px solid var(--line) !important;
  border-radius:10px !important;
  color:var(--ink) !important;
  font-family:'Source Sans 3',sans-serif !important;
  font-size:.92rem !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
  border-color:var(--accent) !important;
  box-shadow:0 0 0 3px var(--alt) !important;
}
.stSelectbox [data-baseweb="select"] > div {
  background:var(--surf) !important;
  border:1.5px solid var(--line) !important;
  border-radius:10px !important;
  color:var(--ink) !important;
  font-size:.92rem !important;
}
label p, .stMarkdown p, .stRadio label,
.stTextInput label p, .stTextArea label p,
.stSelectbox label p, .stNumberInput label p {
  color:var(--ink) !important;
}
.stTextInput label p, .stTextArea label p,
.stSelectbox label p, .stNumberInput label p,
.stRadio > label > div > p {
  font-weight:600 !important; font-size:.84rem !important;
}

/* ── Button ── */
.stButton > button {
  background:var(--accent) !important; color:#F7F3EC !important;
  border:none !important; border-radius:10px !important;
  font-weight:700 !important; font-size:.88rem !important;
  padding:.52rem 1.45rem !important; letter-spacing:.01em !important;
  transition:background .15s !important;
}
.stButton > button:hover, .stButton > button:focus {
  background:var(--adk) !important; color:#F7F3EC !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
  border-radius:10px !important; font-size:.88rem !important;
}

/* ── Stat grid ── */
.sg { display:flex; gap:.9rem; flex-wrap:wrap; margin-bottom:1.05rem; }
.sb {
  flex:1; min-width:135px;
  background:var(--surf); border:1px solid var(--line);
  border-radius:12px; padding:.95rem 1rem .8rem;
  text-align:center; box-shadow:var(--shsm);
}
.sv {
  font-family:'Fraunces',serif; font-size:2rem;
  font-weight:600; color:var(--ink); line-height:1;
}
.sl {
  font-size:.68rem; font-weight:700; letter-spacing:.1em;
  text-transform:uppercase; color:var(--ink2); margin-top:.28rem;
}
.ss { margin-top:.38rem; }

/* ── Distribution bars ── */
.dr { display:flex; align-items:center; gap:.5rem; margin-bottom:.26rem; }
.dl { width:27px; font-size:.78rem; color:var(--ink2); text-align:right; }
.dt { flex:1; height:6px; border-radius:999px; background:var(--surf2); overflow:hidden; }
.df { display:block; height:100%; background:var(--gold); border-radius:999px; }
.dn { width:20px; font-size:.76rem; color:var(--ink2); }

/* ── Stars ── */
.sr { position:relative; display:inline-block; line-height:1; letter-spacing:3px; font-size:.98rem; }
.srb { color:#DDD3BD; }
.srf { position:absolute; top:0; left:0; overflow:hidden; white-space:nowrap; color:var(--gold); }

/* ── Review card ── */
.rc {
  background:var(--surf);
  border:1px solid var(--line);
  border-left:4px solid var(--tc, var(--accent));
  border-radius:12px; padding:.95rem 1.15rem;
  margin-bottom:.8rem; box-shadow:var(--shsm);
}
.rch {
  display:flex; justify-content:space-between;
  align-items:center; flex-wrap:wrap; gap:.35rem; margin-bottom:.46rem;
}
.rcn { font-family:'Fraunces',serif; font-weight:600; font-size:.96rem; color:var(--ink); }
.rcts { display:flex; gap:.32rem; }
.rct {
  font-size:.64rem; font-weight:700; letter-spacing:.05em;
  text-transform:uppercase; padding:.16rem .48rem;
  border-radius:999px; background:var(--surf2);
  color:var(--ink2); border:1px solid var(--line);
}
.rcb { color:var(--ink); font-size:.92rem; line-height:1.6; }
.rcm { color:var(--ink2); font-size:.74rem; margin-top:.42rem; }

/* ── Department badge ── */
.dp {
  display:inline-block; font-size:.69rem; font-weight:700;
  letter-spacing:.04em; padding:.18rem .6rem;
  border-radius:999px; margin-left:.32rem; vertical-align:middle;
}
.dIST { background:#F4E2D6; color:#8A3F22; }
.dPLE { background:#DCE9E9; color:#275557; }
.dSGC { background:#EADEED; color:#5A3563; }

/* ── Session badge ── */
.sbd {
  display:flex; align-items:center; gap:.6rem;
  background:var(--alt); border:1px solid #BDD1BA;
  border-radius:10px; padding:.65rem .95rem; margin:1rem 0;
}
.sav {
  width:34px; height:34px; border-radius:50%;
  background:var(--accent); color:#F7F3EC;
  display:flex; align-items:center; justify-content:center;
  font-family:'Fraunces',serif; font-weight:600; font-size:1rem; flex-shrink:0;
}
.snm { font-weight:700; font-size:.9rem; color:var(--ink); }
.sem { font-size:.78rem; color:var(--ink2); }

/* ── Live rating chip ── */
.lrc {
  display:inline-flex; align-items:center; gap:.5rem;
  background:var(--goldlt); border:1px solid #E4CC99;
  border-radius:10px; padding:.4rem .85rem; margin:.4rem 0 .95rem;
}
.lrn { font-family:'Fraunces',serif; font-weight:600; font-size:1.05rem; color:var(--ink); }
.lrl { font-size:.76rem; color:var(--ink2); }

/* ── Empty state ── */
.empty {
  text-align:center; padding:2.75rem 1.5rem;
  background:var(--surf); border:1.5px dashed var(--line);
  border-radius:var(--r); color:var(--ink2);
}
.empty strong {
  color:var(--ink); font-family:'Fraunces',serif;
  font-size:1.05rem; display:block; margin-bottom:.45rem;
}

/* ── Footer ── */
.ft {
  text-align:center; color:var(--ink2); font-size:.76rem;
  margin-top:3.5rem; padding-top:1.2rem;
  border-top:1px solid var(--line); letter-spacing:.04em;
}
</style>
"""


def inject_styles():
    st.markdown(DESIGN_CSS, unsafe_allow_html=True)

    if not os.path.exists(background_file):
        return

    with open(background_file, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f'<div class="hero" style="background-image:url(\'data:image/jpeg;base64,{encoded}\')">'
        '<span class="hero-cap">Campus &nbsp;·&nbsp; Fall Semester</span>'
        '</div>',
        unsafe_allow_html=True,
    )


def render_stars(rating: float) -> str:
    try:
        pct = max(0.0, min(100.0, float(rating) / 5.0 * 100.0))
    except Exception:
        pct = 0.0
    return (
        f'<span class="sr"><span class="srb">★★★★★</span>'
        f'<span class="srf" style="width:{pct:.1f}%">★★★★★</span></span>'
    )


def dept_badge(d: str) -> str:
    cls = {"IST": "dIST", "PLE": "dPLE", "SGC": "dSGC"}.get(d, "")
    return f'<span class="dp {cls}">{html.escape(d)}</span>' if d else ""


def tier_color(r: float) -> str:
    return "#2F5233" if r >= 4.0 else ("#B8832C" if r >= 3.0 else "#8C3A34")


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


inject_styles()

st.markdown(
    '<div class="mast">'
    '<p class="mast-eye">Student Voices &nbsp;·&nbsp; IST &nbsp;·&nbsp; PLE &nbsp;·&nbsp; SGC</p>'
    '<h1 class="mast-h1">Rate My Professor</h1>'
    '<p class="mast-sub">Please show respect to your instructor and provide constructive criticism!</p>'
    '<div class="mast-rule"></div>'
    '</div>',
    unsafe_allow_html=True,
)

t_see, t_write = st.tabs(["  See Reviews  ", "  Write a Review  "])

with t_see:
    st.markdown('<h2 class="tab-h">Browse reviews</h2>', unsafe_allow_html=True)

    chosen = st.selectbox("Select a professor", professors, key="see_prof")
    dept = departments.get(chosen, "")
    if dept:
        st.markdown(
            f'<p style="margin-top:-.3rem;margin-bottom:.75rem;color:var(--ink2);font-size:.83rem;">'
            f'Department{dept_badge(dept)}</p>',
            unsafe_allow_html=True,
        )

    try:
        with st.spinner("Loading reviews…"):
            reviews = load_reviews(chosen)

        if not reviews:
        st.markdown(
                f'<div class="empty"><strong>No reviews yet for {html.escape(chosen)}</strong>'
                f'Be the first — head to the Write a Review tab.</div>',
                unsafe_allow_html=True,
            )
        else:
            ratings = []
            for d in reviews:
                try:
                    ratings.append(float(d.get("rating", g_rat(d.get("review", "")))))
                except Exception:
                    ratings.append(g_rat(d.get("review", "")))

            total = len(ratings)
            avg = round(sum(ratings) / total * 2) / 2

            bkts: dict = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
            for _r in ratings:
                bkts[min(5, max(1, round(_r)))] += 1

            dist = "".join(
                f'<div class="dr"><span class="dl">{s}★</span>'
                f'<span class="dt"><span class="df" style="width:{bkts[s]/total*100:.0f}%"></span></span>'
                f'<span class="dn">{bkts[s]}</span></div>'
                for s in [5, 4, 3, 2, 1]
            )

        st.markdown(
                f'<div class="sg">'
                f'<div class="sb"><div class="sv">{avg:.1f}'
                f'<span style="font-size:.95rem;color:var(--ink2)">/5</span></div>'
                f'<div class="ss">{render_stars(avg)}</div>'
                f'<div class="sl">Average Rating</div></div>'
                f'<div class="sb"><div class="sv">{total}</div>'
                f'<div class="sl">{"Review" if total == 1 else "Reviews"}</div></div>'
                f'<div class="sb" style="text-align:left;padding:.8rem .95rem;">'
                f'<div style="font-size:.67rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;'
                f'color:var(--ink2);margin-bottom:.42rem;">Distribution</div>'
                f'{dist}</div></div>',
                unsafe_allow_html=True,
            )

            for d, r in zip(reviews, ratings):
                review_words = d.get("review", "")
            rating_type = d.get("rating_type", "Automatic")
                old_auto = d.get("automatic_rating")
                date_str = d.get("created_local", "")
                tc = tier_color(r)

                escaped_text = html.escape(review_words).replace("\n", "<br>")
                auto_badge = (
                    f'<span class="rct" style="background:var(--goldlt);color:var(--gold);border-color:#E4CC99">'
                    f'Auto: {old_auto}/5</span>'
                    if rating_type == "Manual" and old_auto is not None else ""
                )

        st.markdown(
                    f'<div class="rc" style="--tc:{tc}">'
                    f'<div class="rch">'
                    f'<span class="rcn">{r:.1f}/5&nbsp;&nbsp;{render_stars(r)}</span>'
                    f'<span class="rcts"><span class="rct">{html.escape(rating_type)}</span>{auto_badge}</span>'
                    f'</div>'
                    f'<div class="rcb">{escaped_text}</div>'
                    + (f'<div class="rcm">{html.escape(date_str)}</div>' if date_str else "")
                    + '</div>',
                    unsafe_allow_html=True,
                )

    except Exception as error:
        st.error("Could not load reviews.")
        st.code(str(error))

with t_write:
    st.markdown('<h2 class="tab-h">Write a review</h2>', unsafe_allow_html=True)        _i = st.session_state["user_name"][0].upper() if st.session_state["user_name"] else "?"
        st.markdown(
            f'<div class="sbd" style="margin-bottom:1.2rem">'
            f'<div class="sav">{html.escape(_i)}</div><div>'
            f'<div class="snm">Posting as {html.escape(st.session_state["user_name"])}</div>'
            f'<div class="sem">{html.escape(st.session_state["user_email"])}</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

    chosen_professor = st.selectbox("Choose a professor", professors)
    dw = departments.get(chosen_professor, "")
    if dw:
        st.markdown(
                f'<p style="margin-top:-.3rem;margin-bottom:.7rem;color:var(--ink2);font-size:.83rem;">'
                f'Department{dept_badge(dw)}</p>',
                unsafe_allow_html=True,
            )

    review_text = st.text_area(
            "Your review",
            height=170,
            placeholder="Share your honest experience — what worked, what didn't, and what would help other students…",
        )

    auto_rating = 0.0
    if review_text.strip():
        auto_rating = g_rat(review_text)
        st.markdown(
                f'<div class="lrc">'
                f'<span class="lrn">{auto_rating}/5</span>'
                f'{render_stars(auto_rating)}'
                f'<span class="lrl">Auto-detected rating</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    rating_choice = st.radio(
            "Rating method",
            ["Use auto-detected rating", "Set my own rating"],
        )

    final_rating = auto_rating
    rating_type = "Automatic"
    if rating_choice == "Set my own rating":
        final_rating = st.number_input(
                "Your rating (0 – 5, steps of 0.5)",
                min_value=0.0, max_value=5.0,
                value=float(auto_rating), step=0.5,
            )
        rating_type = "Manual"

    if st.button("Submit Review"):
            if not review_text.strip():
                st.warning("Please write your review before submitting.")
            else:
                try:
                final_rating = round(float(final_rating) * 2) / 2

                    with st.spinner("Saving review…"):
                        save_review(
                            chosen_professor,
                            review_text.strip(),
                            final_rating,
                        auto_rating,
                            rating_type,
                        )

                    st.success(f"Review submitted! Rating: {final_rating}/5")

                except Exception as error:
                    st.error("The review could not be saved.")
                    st.code(str(error))

st.markdown(
    '<div class="ft">Rate My Professor &nbsp;·&nbsp; IST · PLE · SGC</div>',
    unsafe_allow_html=True,
)
