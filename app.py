import streamlit as st
import os
import gc 
import time
from streamlit_option_menu import option_menu
from embedding import embedd_pdfs 
from generate_response import generate_response

st.set_page_config(page_title="Study Assistant", layout="wide")

# Ensure subjects directory exists
if not os.path.exists("./subjects"):
    os.makedirs("./subjects")

def get_subjects():
    return [d for d in os.listdir("./subjects") if os.path.isdir(os.path.join("./subjects", d))]
#Get list of available subjects from the subjects directory
subjects = get_subjects()

def chat(subject_name):
    st.title(f"Chat: {subject_name}")
    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    # Accept user input
    if prompt := st.chat_input("Ask a question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    stream_generator = generate_response(subject_name, prompt)
                    response = st.write_stream(stream_generator)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error generating response: {e}")

def upload():
    st.title("Upload Documents")
    # File uploader for new subject
    new_subject = st.text_input("New Subject Name").title().strip()
    files = st.file_uploader("Upload files (PDF, TXT)", type=["txt", "pdf"], accept_multiple_files=True)

    if st.button("Process Files"):
        if not new_subject or not files:
            st.error("Please provide a subject name and upload at least one file.")
            return

        subject_dir = f'./subjects/{new_subject}'
        
        if not os.path.exists(subject_dir):
            os.makedirs(subject_dir)

        file_paths = []
        # Process uploaded files
        with st.spinner("Processing files... This may take a moment."):
            try:
                for file in files:
                    file_path = os.path.join(subject_dir, file.name)
                    with open(file_path, "wb") as f:
                        f.write(file.getbuffer())
                    file_paths.append(file_path)
                
                embedd_pdfs(file_paths, new_subject)
                
                st.success(f"Successfully processed {len(files)} files for '{new_subject}'!")
                
                gc.collect()
                
                time.sleep(1)
                st.rerun()
                
            except Exception as e:
                st.error(f"An error occurred during processing: {e}")

# --- Sidebar Layout ---
with st.sidebar:
    selected = option_menu(
        "Main Menu", 
        ["Home", 'Upload'], 
        icons=['house', 'cloud-upload'], 
        menu_icon="cast", 
        default_index=0
    )
    
    # Initialize a variable to track the current subject in session state
    if "current_subject" not in st.session_state:
        st.session_state.current_subject = None

    if selected == "Home":
        if subjects:
            # 1. Get the selection from the menu
            selected_subject = option_menu(
                'Select Subject', 
                subjects, 
                icons=['book'] * len(subjects),
                default_index=0
            )

            # 2. CHECK FOR CHANGE: Has the subject changed since the last run?
            if st.session_state.current_subject != selected_subject:
                st.session_state.messages = []
                st.session_state.current_subject = selected_subject
                st.rerun() 
        else:
            selected_subject = None
            st.info("No subjects found. Go to 'Upload' to create one.")
# --- Main Page Logic ---
if selected == "Home":
    if subjects and selected_subject:
        chat(selected_subject)
    else:
        st.write("### Welcome! Please upload a document to get started.")
elif selected == "Upload":
    upload()