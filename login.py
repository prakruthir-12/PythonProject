import streamlit as st
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
from streamlit_extras.add_vertical_space import add_vertical_space

# 🔥 Firebase Configuration
firebase_Config = {
    "apiKey": "AIzaSyBTFZyZr_BLJcbs6uKc1DfThONhg5HgH-I",
    "authDomain": "pythonlinkedingenerator.firebaseapp.com",
    "projectId": "pythonlinkedingenerator",
    "storageBucket": "pythonlinkedingenerator.firebasestorage.app",
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
    st.session_state["page"] = "Home"

# 🌐 Navigation Map
page_map = {
    "🏠 Home": "Home",
    "🔑 Login": "Login",
    "📝 Register": "Register",
    "🚀 Dashboard": "Dashboard"
}
reverse_page_map = {v: k for k, v in page_map.items()}

# 📌 Sidebar Navigation
st.sidebar.radio(
    "🌐 Navigate",
    list(page_map.keys()),
    index=list(page_map.values()).index(st.session_state["page"]),
    key="nav",
    on_change=lambda: st.session_state.update({"page": page_map[st.session_state["nav"]]})
)

# 🎨 UI Styling
st.markdown("""
    <style>
    body { background-color: #1E1E1E; color: white; }
    div.stButton > button { width: 100%; height: 48px; font-size: 16px; font-weight: 600;
        border-radius: 12px; background: linear-gradient(to right, #00c6ff, #007bff); color: white; 
        border: none; transition: transform 0.2s ease-in-out; }
    div.stButton > button:hover { transform: scale(1.05); }
    .success-box { background-color: #2ECC71; color: white; padding: 15px; border-radius: 8px; text-align: center; }
    .error-box { background-color: #E74C3C; color: white; padding: 15px; border-radius: 8px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# 🏠 Home Page
if st.session_state["page"] == "Home":
    st.title("🚀 Welcome to Firebase Authentication")
    st.write("Secure login system powered by Streamlit & Firebase")
    add_vertical_space(2)

    st.subheader("🔑 Get Started with Secure Login")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🚀 Register Now"):
            st.session_state["page"] = "Register"
            st.rerun()

    with col_btn2:
        if st.button("✅ Login"):
            st.session_state["page"] = "Login"
            st.rerun()

# 📝 Register Page
elif st.session_state["page"] == "Register":
    st.subheader("👤 Create an Account")
    email = st.text_input("📧 Email", placeholder="Enter your email...")
    password = st.text_input("🔒 Password", type="password", placeholder="Enter a secure password...")
    username = st.text_input("🆔 Username", placeholder="Choose a unique username...")

    if st.button("🚀 Register"):
        with st.spinner("Creating Account..."):
            try:
                user = auth.create_user_with_email_and_password(email, password)
                db.collection("users").document(email).set({"email": email, "name": username})
                st.success("✅ Account Created Successfully! You can now log in.")
            except Exception as e:
                st.error(f"⚠️ Error: {e}")

# 🔑 Login Page
elif st.session_state["page"] == "Login":
    st.subheader("🔓 Login to Your Account")
    email = st.text_input("📧 Email", placeholder="Enter your email...")
    password = st.text_input("🔒 Password", type="password", placeholder="Enter your password...")

    if st.button("✅ Login"):
        with st.spinner("Authenticating..."):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                db.collection("users").document(email).update({"last_login": firestore.SERVER_TIMESTAMP})
                st.success(f"🎉 Welcome back, {email}! Login successful.")

                # ✅ Navigate to Dashboard
                st.session_state["user_email"] = email  # Store email for session
                st.session_state["page"] = "Dashboard"
                st.rerun()

            except Exception as e:
                st.error("❌ Invalid Credentials or Account Does Not Exist")

# 🚀 Dashboard Page (Post-login)
elif st.session_state["page"] == "Dashboard":
    st.subheader(f"🚀 Welcome to Your Dashboard, {st.session_state.get('user_email', 'User')}!")

    st.write("📌 Access your LinkedIn Post Generator & Firebase settings below:")
    add_vertical_space(2)

    if st.button("🔙 Logout"):
        st.session_state["page"] = "Login"
        st.session_state.pop("user_email", None)  # Clear session
        st.rerun()
