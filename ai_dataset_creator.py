import streamlit as st

# --- Page config ---
st.set_page_config(page_title="AI Dataset Creator", page_icon="🤖", layout="centered")

# --- Custom CSS for Chat-like UI ---
st.markdown("""
    <style>
    body {
        background-color: #ffffff;
    }
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 15px;
        margin: 8px 0;
        max-width: 80%;
        font-family: 'Open Sans', sans-serif;
        font-size: 15px;
        line-height: 1.4;
    }
    .bot {
        background-color: #f1f1f1;
        color: #000;
        text-align: left;
    }
    .user {
        background-color: #007BFF;
        color: #fff;
        text-align: right;
        margin-left: auto;
    }
    .option-button {
        display: block;
        width: 100%;
        padding: 12px;
        margin: 6px 0;
        background-color: #007BFF;
        color: white;
        border: none;
        border-radius: 10px;
        font-size: 15px;
        text-align: left;
        cursor: pointer;
    }
    .option-button:hover {
        background-color: #0056b3;
    }
    </style>
""", unsafe_allow_html=True)

# --- Session state for chat ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Greeting ---
if not st.session_state.messages:
    st.session_state.messages.append(("bot", "👋 Hello! Welcome to **AI Dataset Creator**."))
    st.session_state.messages.append(("bot", "📂 What would you like to do? Choose an option below."))

# --- Display chat bubbles ---
for sender, msg in st.session_state.messages:
    css_class = "bot" if sender == "bot" else "user"
    st.markdown(f"<div class='chat-bubble {css_class}'>{msg}</div>", unsafe_allow_html=True)

# --- Options as buttons ---
st.markdown("### 🔽 Options")
options = [
    "1️⃣ Clean Messy Data",
    "2️⃣ Create JSON File",
    "3️⃣ Create CSV File",
    "4️⃣ Create Excel File",
    "5️⃣ Create PDF File",
    "6️⃣ Edit Data",
    "7️⃣ Style Data (fonts, colors, expand rows/columns)",
    "8️⃣ Upload Existing File"
]

for option in options:
    if st.button(option, key=option):
        st.session_state.messages.append(("user", option))
        st.session_state.messages.append(("bot", f"✅ You chose: **{option}**. (Feature coming soon!)"))
        st.rerun()

# --- Input box ---
user_input = st.text_input("💬 Type or paste your data here:", "")
if st.button("Send ➡️"):
    if user_input:
        st.session_state.messages.append(("user", user_input))
        st.session_state.messages.append(("bot", "✅ Got your data! I will process it shortly."))
        st.rerun()

