import streamlit as st
import json
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
from streamlit_lottie import st_lottie
from few_shot import FewShotPosts
from post_generator import generate_post

# 🔥 Firebase Configuration
firebase_Config = {
    "apiKey": "AIzaSyBTFZyZr_BLJcbs6uKc1DfThONhg5HgH-I",
    "authDomain": "pythonlinkedingenerator.firebaseapp.com",
    "projectId": "pythonlinkedingenerator",
    "storageBucket": "pythonlinkedingenerator.appspot.com",
    "messagingSenderId": "487899444946",
    "appId": "1:487899444946:web:bfe89193f534039a579f0b",
    "measurementId": "G-K7NBRT3763",
    "databaseURL": "https://pythonlinkedingenerator.firebaseio.com"
}

# 🔥 Initialize Firebase
firebase = pyrebase.initialize_app(firebase_Config)
auth = firebase.auth()

# 📌 Firebase Admin SDK Initialization
cred = credentials.Certificate("pythonlinkedingenerator-2faa464b19bb.json")  # Ensure this file exists
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

# 🌟 Default Page State
if "page" not in st.session_state:
    st.session_state["page"] = "login"  # Start on login page

# 🚀 Navigation Function
def navigate(page):
    st.session_state["page"] = page
    st.rerun()

# 🔑 Login Page
if st.session_state["page"] == "login":
    st.subheader("🔓 Login to Your Account")
    email = st.text_input("📧 Email", placeholder="Enter your email...")
    password = st.text_input("🔒 Password", placeholder="Enter your password...", type="password")

    if st.button("✅ Login"):
        with st.spinner("Authenticating..."):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                db.collection("users").document(email).update({"last_login": firestore.SERVER_TIMESTAMP})
                st.success(f"🎉 Welcome back, {user}! Login successful.")

                # ✅ Navigate to LinkedIn Post Generator after login
                user_name = st.session_state.get("username","User")
 # Store email for session
                navigate("generator")

            except Exception as e:
                st.error(f"❌ Login failed: {e}")

# 🚀 LinkedIn Post Generator UI
if st.session_state["page"] == "generator":
    # 🎨 Function to load Lottie animation from a local file
    def load_lottie_local(filepath):
        with open(filepath, "r") as f:
            return json.load(f)

    lottie_animation = load_lottie_local("HelloANimation/AnimationHelloWB - 1747456505830.json")

    # Set Page Config
    st.set_page_config(page_title="LinkedIn Post Generator", page_icon="🚀", layout="centered")

    # Sidebar for customization
    st.sidebar.title("🎨 Post Customization")
    fs = FewShotPosts()
    tags = fs.get_tags()
    selected_tag = st.sidebar.selectbox("📌 Topic", options=tags)
    selected_length = st.sidebar.radio("📏 Length", options=["Short", "Medium", "Long"])
    selected_language = st.sidebar.radio("🗣 Language", options=["English", "Hinglish"])

    # 👤 Capture User Name
    user_name = st.session_state.get("username","email")

    # 🌗 Theme Toggle
    if "theme" not in st.session_state:
        st.session_state["theme"] = "Light"

    theme = st.sidebar.radio("🌗 Choose Theme", options=["Light", "Dark"])
    st.session_state["theme"] = theme

    # Custom Styling with Button Hover Effects
    light_theme = """
    <style>
        body { background-color: #ffffff; color: #333; }
        .header-card { 
            background-color: #007ACC; 
            color: white; 
            font-size: 32px; 
            font-family: Arial, sans-serif; 
            font-weight: bold;
            text-align: center; 
            padding: 25px; 
            border-radius: 12px; 
            margin-bottom: 30px;
        }
        .user-header { 
            background-color: #f4f4f4; 
            color: #333; 
            font-size: 24px; 
            font-family: Arial, sans-serif; 
            font-weight: bold; 
            text-align: center; 
            padding: 20px; 
            border-radius: 12px; 
            margin-bottom: 30px;
        }
        .tips-box { 
            background-color: #E3F2FD; 
            color: #333; 
            font-size: 18px; 
            padding: 20px; 
            border-radius: 12px; 
            text-align: left; 
            margin-bottom: 30px; 
            line-height: 1.8;
        }
        .preview-box { 
            background-color: #f4f4f4; 
            color: #333; 
            font-size: 18px; 
            padding: 20px; 
            border-radius: 12px; 
            text-align: left; 
            margin-bottom: 30px; 
        }
        .generate-button {
            background-color: #007ACC;
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 15px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease-in-out;
        }
        .generate-button:hover {
            background-color: #005F99;
            transform: scale(1.05);
        }
    </style>
    """

    dark_theme = """
    <style>
        body { background-color: #1e1e1e; color: white; }
        .header-card { 
            background-color: #333333; 
            color: white; 
            font-size: 32px; 
            font-family: Arial, sans-serif; 
            font-weight: bold;
            text-align: center; 
            padding: 25px; 
            border-radius: 12px; 
            margin-bottom: 30px;
        }
        .user-header { 
            background-color: #444444; 
            color: white; 
            font-size: 24px; 
            font-family: Arial, sans-serif; 
            font-weight: bold; 
            text-align: center; 
            padding: 20px; 
            border-radius: 12px; 
            margin-bottom: 30px;
        }
        .tips-box { 
            background-color: #2C3E50; 
            color: white; 
            font-size: 18px; 
            padding: 20px; 
            border-radius: 12px; 
            text-align: left; 
            margin-bottom: 30px; 
            line-height: 1.8;
        }
        .preview-box { 
            background-color: #555555; 
            color: white; 
            font-size: 18px; 
            padding: 20px; 
            border-radius: 12px; 
            text-align: left; 
            margin-bottom: 30px; 
        }
        .generate-button {
            background-color: #005F99;
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 15px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease-in-out;
        }
        .generate-button:hover {
            background-color: #007ACC;
            transform: scale(1.05);
        }
    </style>
    """

    # Apply theme
    st.markdown(light_theme if st.session_state["theme"] == "Light" else dark_theme, unsafe_allow_html=True)

    # Display animation
    if lottie_animation:
        st_lottie(lottie_animation, speed=1, height=250, key="animation1")
    else:
        st.error("⚠️ Failed to load animation. Check the JSON file path.")

    # **Separate Header Card - LinkedIn Post Generator**
    st.markdown('<div class="header-card">🚀 LinkedIn Post Generator</div>', unsafe_allow_html=True)

    # **Welcome Message**
    st.markdown(f'<div class="user-header">👤 Welcome, {user_name}!</div>', unsafe_allow_html=True)

    # 📝 **LinkedIn Post Tips & Insights**
    tips = """
    ✅ **Start with a Hook**: Grab attention in the first sentence  
    ✅ **Use Engaging Visuals**: Images & GIFs boost visibility  
    ✅ **Tell a Story**: Share personal experiences for impact  
    ✅ **Keep it Concise**: Shorter posts tend to perform better  
    ✅ **Ask Questions**: Encourage engagement through discussions  
    ✅ **Use Relevant Hashtags**: Improve discoverability  
    ✅ **Engage with Comments**: Responding increases visibility  
    """

    st.markdown(f'<div class="tips-box"><strong>💡 LinkedIn Post Tips</strong><br>{tips}</div>', unsafe_allow_html=True)

    # Live Preview Section
    preview_post = f"💡 Here's a {selected_length.lower()} LinkedIn post in {selected_language} about {selected_tag}. Stay tuned for your generated content!"
    st.markdown(f'<div class="preview-box">{preview_post}</div>', unsafe_allow_html=True)

    # ✨ Generate Button
    if st.button("✨ Generate Post"):
        with st.spinner("🚀 Generating your LinkedIn post..."):
            post = generate_post(selected_length, selected_language, selected_tag)

        # Display Final Post
        st.markdown(f'<div class="preview-box">{post}</div>', unsafe_allow_html=True)

    # 🔙 Logout Option
    if st.button("🔙 Logout"):
        st.session_state["page"] = "login"
        st.session_state.pop("user_email", None)  # Clear session
        st.rerun()
