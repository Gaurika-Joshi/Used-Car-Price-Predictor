import streamlit as st
import pandas as pd
import pickle
import datetime

# 1. Wide Page Setup
st.set_page_config(
    page_title="AutoValuate | Used Car Price Predictor",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load Model & Columns
model = pickle.load(open("car_price_model.pkl", "rb"))
model_columns = pickle.load(open("model_columns.pkl", "rb"))

# 2. Custom Warm Beige, Brown & Sage Green Editorial CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,600&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap');

/* Main Warm Beige Background */
.stApp {
    background: linear-gradient(145deg, #F3ECE1 0%, #E6DAC8 55%, #D9C8B2 100%);
    color: #3A2E28;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Subtle Editorial Watermark in Background (like the poster) */
.stApp::before {
    content: "VALUATION";
    position: fixed;
    top: 12%;
    left: 50%;
    transform: translateX(-50%);
    font-family: 'Playfair Display', serif;
    font-size: 14vw;
    font-weight: 700;
    color: rgba(92, 68, 51, 0.045);
    letter-spacing: 12px;
    pointer-events: none;
    z-index: 0;
}

/* Hide default Streamlit header/footer clutter */
header[data-testid="stHeader"] {
    background: transparent;
}

/* Hero Section */
.eyebrow-tag {
    text-align: center;
    font-size: 0.8rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #4A5D4E; /* Muted Sage Green */
    font-weight: 600;
    margin-bottom: 0.2rem;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.4rem;
    font-weight: 700;
    text-align: center;
    color: #2E221D; /* Deep Espresso Brown */
    line-height: 1.1;
    margin-bottom: 0.2rem;
}

.hero-cursive {
    font-family: 'Dancing Script', cursive;
    font-size: 2rem;
    text-align: center;
    color: #7D5A44; /* Warm Chestnut Brown */
    margin-bottom: 2rem;
}

/* Layered Aesthetic Cards */
.editorial-card {
    background: rgba(250, 246, 240, 0.82);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(125, 90, 68, 0.2);
    border-radius: 20px;
    padding: 2.2rem;
    box-shadow: 0 12px 32px rgba(58, 46, 40, 0.08);
    position: relative;
    z-index: 1;
}

.mini-pill {
    display: inline-block;
    background: rgba(74, 93, 78, 0.12);
    color: #3E5242;
    padding: 0.35rem 0.9rem;
    border-radius: 50px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.price-display {
    font-family: 'Playfair Display', serif;
    font-size: 3.1rem;
    font-weight: 700;
    color: #2E221D;
    margin: 0.4rem 0;
}

.range-badge {
    display: inline-block;
    background: #4A5D4E; /* Sage Green Accent */
    color: #FAF6F0;
    padding: 0.45rem 1.1rem;
    border-radius: 10px;
    font-size: 0.88rem;
    font-weight: 500;
    margin: 0.8rem 0 1.4rem 0;
}

.spec-row {
    display: flex;
    justify-content: space-between;
    padding: 0.6rem 0;
    border-bottom: 1px solid rgba(125, 90, 68, 0.15);
    font-size: 0.9rem;
    color: #5C493E;
}

/* Style Streamlit Labels & Inputs to match Beige/Brown */
label, .stSelectbox label, .stNumberInput label {
    color: #4A382E !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background-color: #FAF6F0 !important;
    border: 1px solid #CBB9A4 !important;
    border-radius: 10px !important;
    color: #2E221D !important;
}

/* Primary Button - Deep Espresso Brown with Sage Hover */
div.stButton > button {
    width: 100%;
    background-color: #3A2E28;
    color: #FAF6F0;
    border: none;
    border-radius: 12px;
    padding: 0.8rem 1.5rem;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    transition: all 0.25s ease;
    margin-top: 0.5rem;
}

div.stButton > button:hover {
    background-color: #4A5D4E;
    color: #FAF6F0;
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(74, 93, 78, 0.25);
}

/* Bottom Feature Cards */
.feature-card {
    background: rgba(250, 246, 240, 0.65);
    border: 1px solid rgba(125, 90, 68, 0.15);
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    text-align: center;
    margin-top: 1.5rem;
}

.feature-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #3A2E28;
}

.feature-desc {
    font-size: 0.8rem;
    color: #6E5A4F;
    margin-top: 0.2rem;
}
</style>
""", unsafe_allow_html=True)

# 3. Header
st.markdown('<div class="eyebrow-tag">AI-Powered Automotive Valuation</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Used Car Price Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-cursive">Crafted for accurate, effortless market estimates</div>', unsafe_allow_html=True)

# 4. Main Two-Column Editorial Layout
col1, col2 = st.columns([1.15, 1], gap="large")

with col1:
    st.markdown("#### Vehicle Specifications")
    
    # IMPORTANT: Keep your exact brand-to-number mapping from your original app.py!
    brand_options = [
        ("Maruti Suzuki", 0), ("Hyundai", 1), ("Honda", 2), ("Tata", 3),
        ("Mahindra", 4), ("Toyota", 5), ("Ford", 6), ("Volkswagen", 7)
    ]

    c1, c2 = st.columns(2)
    with c1:
        brand = st.selectbox("Car Brand", options=brand_options, format_func=lambda x: x[0])
        year = st.selectbox("Manufacturing Year", options=list(range(2026, 1999, -1)))
        fuel = st.selectbox(
            "Fuel Type",
            options=[("Petrol", 4), ("Diesel", 3), ("CNG", 0), ("LPG", 2), ("Electric", 1)],
            format_func=lambda x: x[0]
        )
    with c2:
        km = st.number_input("Kilometers Driven", min_value=0, value=20000, step=5000)
        transmission = st.selectbox(
            "Transmission",
            options=[("Manual", 0), ("Automatic", 1)],
            format_func=lambda x: x[0]
        )
        owner = st.selectbox(
            "Ownership",
            options=[("1st Owner", 1), ("2nd Owner", 2), ("3rd Owner", 3), ("4th & Above", 4)],
            format_func=lambda x: x[0]
        )

    predict_btn = st.button("Calculate Fair Market Value")

with col2:
    if predict_btn:
        current_year = datetime.datetime.now().year
        calculated_age = current_year - year

        input_data = pd.DataFrame(
            [[brand[1], km, fuel[1], transmission[1], owner[1], calculated_age]],
            columns=model_columns
        )
        prediction = model.predict(input_data)[0]
        low_est = prediction * 0.94
        high_est = prediction * 1.06

        st.markdown(f"""
        <div class="editorial-card" style="text-align: center;">
            <div class="mini-pill">Verified Estimate</div>
            <div style="font-size: 0.9rem; color: #6E5A4F;">Estimated Resale Value</div>
            <div class="price-display">₹ {prediction:,.0f}</div>
            <div class="range-badge">Fair Range: ₹ {low_est:,.0f} – ₹ {high_est:,.0f}</div>
            <div class="spec-row"><span>Vehicle</span><b>{year} {brand[0]}</b></div>
            <div class="spec-row"><span>Usage</span><b>{km:,} km • {owner[0]}</b></div>
            <div class="spec-row" style="border-bottom: none;"><span>Drivetrain</span><b>{fuel[0]} • {transmission[0]}</b></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="editorial-card" style="text-align: center; padding: 3.5rem 2rem;">
            <div class="mini-pill">Ready to Evaluate</div>
            <div style="font-family: 'Playfair Display', serif; font-size: 1.6rem; color: #2E221D; margin-bottom: 0.6rem;">
                Your Valuation Card
            </div>
            <p style="color: #6E5A4F; font-size: 0.92rem; line-height: 1.6;">
                Enter your car's specifications on the left and click <b>Calculate Fair Market Value</b> to reveal its estimated resale price and fair market range.
            </p>
        </div>
        """, unsafe_allow_html=True)

# 5. Subtle Bottom Editorial Info Cards (matches the bottom spec bar in your poster)
f1, f2, f3 = st.columns(3)
with f1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">Random Forest Engine</div>
        <div class="feature-desc">Trained on real-world used car market data</div>
    </div>
    """, unsafe_allow_html=True)
with f2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">Fair Range Analysis</div>
        <div class="feature-desc">Instant ±6% negotiation window included</div>
    </div>
    """, unsafe_allow_html=True)
with f3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">Live Cloud Prediction</div>
        <div class="feature-desc">Real-time depreciation & mileage scoring</div>
    </div>
    """, unsafe_allow_html=True)
