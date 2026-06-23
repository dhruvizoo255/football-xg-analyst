import streamlit as st
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch

from predict import predict_xg
from retrieval import get_similar_shots
from explainations import explain_xg

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Football xG Analyst",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# CSS
# ======================================================

st.markdown("""
<style>

.stApp {
    background-color: #0B0F19;
    color: #E6EDF3;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #111827 0%,
        #0B1220 100%
    );
}

/* Make ALL sidebar text white */
[data-testid="stSidebar"] * {
    color: #E6EDF3 !important;
}

/* Sidebar heading */
[data-testid="stSidebar"] h1 {
    color: #00FF88 !important;
    font-weight: 800 !important;
}

/* Title */
.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: 800;
    color: #00FF88;
}

.subtitle {
    text-align: center;
    color: #B8C5D6;
    font-size: 18px;
}

/* Metric Cards */
.metric-card {
    background: #161B22;
    padding: 30px;
    border-radius: 22px;
    text-align: center;
    border: 1px solid rgba(0,255,136,0.25);
    box-shadow: 0px 0px 25px rgba(0,255,136,0.15);
}

/* Similar Shot Cards */
.shot-card {
    background: #161B22;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 18px;
    border-left: 6px solid #00FF88;
    box-shadow: 0px 0px 15px rgba(0,255,136,0.10);
}

/* Buttons */
.stButton > button {
    width: 100%;
    height: 55px;
    border-radius: 15px;
    font-size: 18px;
    font-weight: bold;
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


</style>
""", unsafe_allow_html=True)

# ======================================================
# HEADER
# ======================================================

st.markdown(
    '<p class="main-title">⚽ Football xG Analyst</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Predict • Explore • Explain</p>',
    unsafe_allow_html=True
)

st.divider()

# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.title("⚽ Shot Context")

location_mode = st.sidebar.radio(
    "Location Input",
    [
        "Pitch Zones",
        "Advanced Coordinates"
    ]
)

if location_mode == "Pitch Zones":

    zone = st.sidebar.selectbox(
        "Shot Location",
        [
            "Penalty Spot",
            "Center Box",
            "Left Side of Box",
            "Right Side of Box",
            "Outside Box",
            "Long Range"
        ]
    )

    zone_map = {
        "Penalty Spot": (108, 40),
        "Center Box": (104, 40),
        "Left Side of Box": (104, 30),
        "Right Side of Box": (104, 50),
        "Outside Box": (96, 40),
        "Long Range": (85, 40)
    }

    x, y = zone_map[zone]

else:

    x = st.sidebar.slider(
        "X Coordinate",
        min_value=80,
        max_value=120,
        value=108
    )

    y = st.sidebar.slider(
        "Y Coordinate",
        min_value=0,
        max_value=80,
        value=40
    )

body_part = st.sidebar.selectbox(
    "Body Part",
    [
        "Left Foot",
        "Right Foot",
        "Head"
    ]
)

technique = st.sidebar.selectbox(
    "Technique",
    [
        "Normal",
        "Half Volley",
        "Volley"
    ]
)

shot_type = st.sidebar.selectbox(
    "Shot Type",
    [
        "Open Play",
        "Free Kick",
        "Corner"
    ]
)

play_pattern = st.sidebar.selectbox(
    "Play Pattern",
    [
        "Regular Play",
        "From Counter",
        "From Corner",
        "From Throw In"
    ]
)

under_pressure = st.sidebar.checkbox(
    "Under Pressure"
)

first_time = st.sidebar.checkbox(
    "First Time Shot"
)

predict_button = st.sidebar.button(
    "⚽ Analyze Shot"
)

# ======================================================
# PREDICTION
# ======================================================

if predict_button:

    xg = predict_xg(
        x,
        y,
        body_part,
        technique,
        shot_type,
        play_pattern,
        under_pressure,
        first_time
    )

    explanation = explain_xg(xg)

    similar = get_similar_shots(
        x,
        y,
        n_neighbors=100
    )

    display_shots = similar.head(5)

    left, right = st.columns([1.3, 1])

    # ==================================================
    # LEFT
    # ==================================================

    with left:

        st.subheader("🔥 Historical Shot Density")

        pitch = VerticalPitch(
            pitch_type="statsbomb",
            pitch_color="#0B0F19",
            line_color="#E6EDF3"
        )

        fig, ax = pitch.draw(
            figsize=(6, 8)
        )

        pitch.kdeplot(
            similar["x"],
            similar["y"],
            ax=ax,
            fill=True,
            levels=30,
            alpha=0.7
        )

        pitch.scatter(
            x,
            y,
            ax=ax,
            s=300,
            c="#00FF88",
            edgecolors="white",
            linewidth=2
        )

        st.pyplot(fig)

    # ==================================================
    # RIGHT
    # ==================================================

    with right:

        st.markdown(
            f"""
            <div class='metric-card'>
                <h3>Expected Goals</h3>
                <h1 style='font-size:60px;color:#00FF88;'>
                    {xg*100:.1f}%
                </h1>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        if xg < 0.10:
            quality = "Low Quality Chance"
        elif xg < 0.30:
            quality = "Decent Opportunity"
        elif xg < 0.60:
            quality = "High Quality Chance"
        else:
            quality = "Clear Cut Opportunity"

        st.markdown(
            f"""
            <div class='metric-card'>
                <h3>Chance Quality</h3>
                <h2 style='color:#00FF88;'>
                    {quality}
                </h2>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("### Goal Probability")
        st.progress(float(xg))

    st.divider()

    # ==================================================
    # EXPLANATION
    # ==================================================

    st.subheader("🧠 AI Analyst")
    st.info(explanation)

    st.divider()

    # ==================================================
    # SIMILAR SHOTS
    # ==================================================

    st.subheader("⚽ Similar Historical Shots")

    for _, row in display_shots.iterrows():

        st.markdown(
            f"""
            <div class='shot-card'>
                <h3>{row['player']}</h3>
                <p><b>Team:</b> {row['team']}</p>
                <p><b>Outcome:</b> {row['outcome']}</p>
                <p><b>Historical xG:</b> {row['statsbomb_xg']:.3f}</p>
            </div>
            """,
            unsafe_allow_html=True
        )