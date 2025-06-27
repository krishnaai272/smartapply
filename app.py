import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import queue

from src.parser import parse_resume
from src.llm import load_model, generate_all
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.pdf_generator import create_downloadable_pdf
# from src.audio import transcribe_audio # Whisper can be heavy, enable if you have the resources

class GenerationRequest(BaseModel):
    resume_text: str
    job_description: str
    user_notes: str = ""

app = FastAPI(title="SmartApply AI Backend")
llm = None

@app.on_event("startup")
def startup_event():
    global llm
    print("--> Loading the AI model...")
    llm = load_model()
    print("--> AI Model Loaded Successfully!")

@app.post("/generate")
def generate_application_endpoint(request: GenerationRequest):
    if llm is None:
        raise HTTPException(status_code=503, detail="Model is not ready.")
    
    try:
        result = generate_all(
            llm=llm,
            resume_text=request.resume_text,
            job_description=request.job_description,
            user_notes=request.user_notes
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SmartApply AI",
    page_icon="✨",
    layout="wide",
)

# --- LOAD CSS FOR STYLING ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("assets/style.css")

# --- STATE MANAGEMENT ---
if "llm" not in st.session_state:
    st.session_state.llm = None
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "generated_content" not in st.session_state:
    st.session_state.generated_content = None

# --- SIDEBAR (optional for settings or info) ---
# with st.sidebar:
#     st.header("Settings")
#     # Add any settings if needed

# --- MAIN APPLICATION UI ---
st.title("Land Your Dream Job with AI-Powered Applications")
st.markdown("Transform your resume and craft perfect cover letters tailored to any job description. Get ATS-friendly documents that pass initial screenings and impress recruiters.")

# --- STEP 1: UPLOAD RESUME ---
st.header("1. Start with Your Resume")
upload_container = st.container()
with upload_container:
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF, DOCX, TXT) or paste content below.",
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        with st.spinner("Parsing your resume..."):
            st.session_state.resume_text = parse_resume(uploaded_file)
            if "Error:" in st.session_state.resume_text:
                st.error(st.session_state.resume_text)
                st.session_state.resume_text = ""
            else:
                st.success("Resume parsed successfully!")
    
    st.session_state.resume_text = st.text_area(
        "Or paste your resume/LinkedIn profile content here",
        value=st.session_state.resume_text,
        height=250,
        key="resume_input"
    )

# --- STEP 2: JOB INFORMATION ---
if st.session_state.resume_text:
    st.header("2. Tell Us About the Job")
    job_info_container = st.container()
    with job_info_container:
        job_description = st.text_area("Paste the full job description here", height=250)
        
        # Optional Voice Notes (Uncomment if you want to use Whisper)
        # st.markdown("##### Add Personal Notes (Optional)")
        # st.write("Add any specific points you want in the cover letter (e.g., explain a career gap, mention a referral, express passion for the company's mission).")
        # user_notes = st.text_input("Type your notes here...")
        
        # --- GENERATION BUTTON ---
        if st.button("✨ Optimize My Application"):
            if not job_description:
                st.warning("Please paste the job description to proceed.")
            else:
                # Load model on first use
                if st.session_state.llm is None:
                    with st.spinner("Warming up the AI... This might take a moment."):
                        st.session_state.llm = load_model()
                
                with st.spinner("AI is crafting your tailored application... This can take 1-2 minutes."):
                    st.session_state.generated_content = generate_all(
                        st.session_state.llm,
                        st.session_state.resume_text,
                        job_description,
                        "" # user_notes
                    )

# --- STEP 3: DISPLAY RESULTS ---
if st.session_state.generated_content:
    st.header("🎉 Your Application is Ready!")
    
    score = st.session_state.generated_content["score"]
    analysis = st.session_state.generated_content["analysis"]
    
    # Display Score and Analysis
    score_color = "green" if score >= 80 else ("orange" if score >= 60 else "red")
    st.markdown(f"### Compatibility Score: <span style='color:{score_color}; font-size: 1.5em;'>{score}/100</span>", unsafe_allow_html=True)
    st.info(f"**AI Analysis:** {analysis}")

    results_container = st.container()
    with results_container:
        tab1, tab2, tab3 = st.tabs(["📄 Tailored Resume", "✉️ Cover Letter", "📥 Download"])

        with tab1:
            st.subheader("Optimized Resume")
            st.markdown(f"```{st.session_state.generated_content['tailored_resume']}```")

        with tab2:
            st.subheader("Customized Cover Letter")
            st.markdown(st.session_state.generated_content['cover_letter'])

        with tab3:
            st.subheader("Export Your Documents")
            st.markdown("Download your generated documents as ATS-friendly PDF files.")
            
            # Create PDFs in memory
            resume_pdf = create_downloadable_pdf(st.session_state.generated_content['tailored_resume'])
            cover_letter_pdf = create_downloadable_pdf(st.session_state.generated_content['cover_letter'])

            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📥 Download Resume",
                    data=resume_pdf,
                    file_name="Optimized_Resume.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            with col2:
                st.download_button(
                    label="📥 Download Cover Letter",
                    data=cover_letter_pdf,
                    file_name="Cover_Letter.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )