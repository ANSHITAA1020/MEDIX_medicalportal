import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
from datetime import datetime
import speech_recognition as sr
from gtts import gTTS
import uuid
import firebase_admin
from firebase_admin import credentials, firestore, storage
from io import BytesIO  # Import BytesIO for in-memory file handling
import tempfile

# Load environment variables
load_dotenv()

if not firebase_admin._apps:
    # Get Firebase credentials from environment variables
    cred_path = os.getenv("service_acc_cred")  # Environment variable for Firebase service account key path
    bucket_name = os.getenv("storage_bucket_cred")  # Environment variable for Firebase Storage bucket name
    
    cred = credentials.Certificate(cred_path)  # Load the service account key
    firebase_admin.initialize_app(cred, {
        'storageBucket': bucket_name  # Use the storage bucket from the environment variable
    })

# Access Firestore database
db = firestore.client()
bucket = storage.bucket()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Medix",
    page_icon="👩‍⚕️",
    layout="centered",
)

# Configure the Google Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
gen_ai.configure(api_key=GOOGLE_API_KEY)

# Define generation and safety settings
generation_config = {
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Initialize the model
model = gen_ai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction=(
        "You are a knowledgeable and empathetic AI specialized in developing a secure and effective medical chatbot. "
        "Your primary goal is to assist users with their health-related inquiries while ensuring their safety and privacy. "
        "You should provide accurate information on medical conditions, treatment options, and healthy lifestyle choices. "
        "When users ask about medications, consider their medical history and potential interactions with other conditions. "
        "Encourage users to consult with healthcare professionals for personalized medical advice. "
        "Respond with empathy and clarity, ensuring that complex medical terms are explained in simple language. "
        "If a user expresses distress or urgency, provide them with relevant medical helplines and direct them to seek immediate medical attention. "
        "Always prioritize user safety and adhere to ethical guidelines in providing health information. "
        "Be aware of common health issues prevalent in India, such as diabetes, heart disease, and hypertension, "
        "and provide culturally relevant advice and resources. "
        "Only respond to queries related to medical issues; do not engage with non-medical inquiries. "
        "You are a knowledgeable and empathetic AI specialized in developing a secure and effective medical chatbot. "
        "Your primary goal is to assist users with their health-related inquiries while ensuring their safety and privacy. "
        "Respond in a culturally relevant way, adhering to ethical guidelines in medical assistance. "
        "Talk in the user preferred language. "
        "Introduce yourself as Medimitra at the start of the conversation and welcome the user to Medix medical portal"
    )
)

# Initialize chat session
st.image("logo.png", width=350)
st.header("_Medix_ is your :blue[smart] health companion :robot_face: for a healthier tomorrow! :sparkles:", divider=True)

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    welcome_message = "Welcome to Medix! How can I assist you with your health today?"
    st.chat_message("assistant").markdown(welcome_message)

# Initialize the speech recognizer
r = sr.Recognizer()

# Function to convert text to speech and return the audio URL
def get_speech_file_and_upload(text):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(temp_audio_file.name)  # Save TTS output to the temporary file
        temp_audio_file.close()  # Close the file to release the handle
        
        blob = bucket.blob(f'audio/{uuid.uuid4().hex}.mp3')  # Create a new blob with a unique name
        blob.upload_from_filename(temp_audio_file.name)  # Use upload_from_filename since the file is closed
        blob.make_public()  # Make the file publicly accessible
        return blob.public_url

# Function to store message in Firestore
def store_message(user_id, message_text, audio_url, message_type, session_id):
    doc_ref = db.collection('chat_messages').document()  # Automatically generates a unique ID
    doc_ref.set({
        'user_id': user_id,
        'Type': message_type,
        'Value': message_text,
        'audio_file_url': audio_url,
        'timestamp': datetime.now(),
        'session_id': session_id,
        'message_id': doc_ref.id,
        'language': 'en'  # Or other language based on your input
    })

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(message.role):
        st.markdown(message.parts[0].text)

# Handle user text input
user_prompt = st.chat_input("How can Medix assist you today?")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)

    # Check if the user mentioned "appointment"
    if "appointment" in user_prompt.lower():
        st.markdown("Redirecting you to the appointment booking page...")
        st.markdown("[Click here to book an appointment](http://your-django-app-url/appointment/)")  # Replace with your actual URL
        st.stop()  # Stop further processing

    # Send user's message and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display response and upload audio to Firebase
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
        audio_url = get_speech_file_and_upload(gemini_response.text)  # Get audio URL
        store_message(user_id="user_123", message_text=user_prompt, audio_url=None, message_type='text', session_id="session_456")
        store_message(user_id="assistant", message_text=gemini_response.text, audio_url=audio_url, message_type='audio', session_id="session_456")
        st.audio(audio_url, format="audio/mp3", autoplay=True)

# Handle voice input
if st.button("Speak🎤", type="primary"):
    with sr.Microphone() as source:
        try:
            audio = r.listen(source)
            user_prompt = r.recognize_google(audio)
            st.chat_message("user").markdown(user_prompt)

            # Check if the user mentioned "appointment"
            if "appointment" in user_prompt.lower():
                st.markdown("Redirecting you to the appointment booking page...")
                st.markdown("[Click here to book an appointment](http://127.0.0.1:8000/book-appointment/)")  # Replace with your actual URL
                st.stop()  # Stop further processing

            # Send the recognized voice input to the chatbot
            gemini_response = st.session_state.chat_session.send_message(user_prompt)

            # Display response and upload audio to Firebase
            with st.chat_message("assistant"):
                st.markdown(gemini_response.text)
                audio_url = get_speech_file_and_upload(gemini_response.text)  # Get audio URL
                store_message(user_id="user_123", message_text=user_prompt, audio_url=None, message_type='text', session_id="session_456")
                store_message(user_id="assistant", message_text=gemini_response.text, audio_url=audio_url, message_type='audio', session_id="session_456")
                st.audio(audio_url, format="audio/mp3", autoplay=True)

        except sr.UnknownValueError:
            st.error("Could not understand, try speaking again.")
        except sr.RequestError as e:
            st.error(f"Could not request results; {e}")

# Get the current date and time
current_datetime = datetime.now().strftime("%B %d, %Y | %I:%M %p")

# Hide Streamlit's default footer
st.markdown(
    """
    <style>
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# Add custom styling for the footer and audio player
footer = f"""
<style>
.footer {{
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f1f1f1;
    text-align: center;
    font-size: 12px;
}}
</style>
<div class="footer">
    <p>🧑‍⚕️ Medix | Your Health Assistant | {current_datetime}</p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
