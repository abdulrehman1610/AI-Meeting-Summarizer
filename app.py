import streamlit as st
import os
import sys
import tempfile

# Add modules to path (Windows safe)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules import ingest, transcriber, llm_processor, exporter, email_dispatcher

st.set_page_config(page_title="AI Meeting Summarizer", layout="wide")

st.sidebar.title("⚙️ Settings")
model_size = st.sidebar.selectbox("Whisper Model", ["tiny", "base", "small", "medium"], index=1)
llm_backend = st.sidebar.selectbox("LLM Backend", ["ollama", "openrouter"])

st.title("📹 Meeting Recording Summarizer")
st.markdown("Upload a meeting recording to generate summaries and action items.")

uploaded_file = st.file_uploader("Upload Audio/Video", type=["mp4", "mov", "m4a", "mp3", "wav", "webm"])

if uploaded_file:
    st.success(f"File uploaded: {uploaded_file.name}")

    # Initialize session state for results
    if "current_file" not in st.session_state:
        st.session_state.current_file = None
        
    # Reset results if a new file is uploaded
    if st.session_state.current_file != uploaded_file.name:
        st.session_state.summary_data = None
        st.session_state.transcript = None
        st.session_state.md_content = None
        st.session_state.current_file = uploaded_file.name
        
    if "summary_data" not in st.session_state:
        st.session_state.summary_data = None
    if "transcript" not in st.session_state:
        st.session_state.transcript = None
    if "md_content" not in st.session_state:
        st.session_state.md_content = None

    if st.button("🚀 Process Meeting"):
        # Create a temp file on Windows
        temp_dir = tempfile.gettempdir()
        temp_input_path = os.path.join(temp_dir, uploaded_file.name)
        
        with open(temp_input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        try:
            # 1. Ingest
            with st.spinner("Step 1: Preprocessing audio (converting to WAV)..."):
                wav_path = ingest.convert_to_wav(temp_input_path)
                chunks = ingest.chunk_audio(wav_path)
            
            # 2. Transcribe
            with st.spinner(f"Step 2: Transcribing ({len(chunks)} chunks)... This may take time."):
                model = transcriber.load_model(model_size)
                transcript = transcriber.transcribe_audio(model, chunks)
            
            # 3. LLM Processing
            with st.spinner(f"Step 3: Generating Summary & Action Items via {llm_backend.title()}..."):
                os.environ["LLM_BACKEND"] = llm_backend
                summary_data = llm_processor.get_llm_response(transcript)
            
            # 4. Export
            md_content = exporter.generate_markdown(transcript, summary_data, {"filename": uploaded_file.name})
            md_path = exporter.save_markdown(md_content, uploaded_file.name)
            
            # Save to session state
            st.session_state.summary_data = summary_data
            st.session_state.transcript = transcript
            st.session_state.md_content = md_content
            
            st.success("Processing Complete!")

        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            # Cleanup temp file
            if os.path.exists(temp_input_path):
                os.remove(temp_input_path)

    # Display Results if available
    if st.session_state.summary_data is not None:
        summary_data = st.session_state.summary_data
        transcript = st.session_state.transcript
        md_content = st.session_state.md_content

        # Display Results
        tab1, tab2, tab3 = st.tabs(["📄 Summary", "✅ Action Items", "📝 Transcript"])
        
        with tab1:
            st.markdown(summary_data.get("summary", "No summary generated."))
        
        with tab2:
            items = summary_data.get("action_items", [])
            if items:
                st.dataframe(items, use_container_width=True)
            else:
                st.write("No action items detected.")
        
        with tab3:
            with st.expander("View Full Transcript"):
                st.text_area("Transcript", transcript, height=300)
        
        st.download_button(
            label="📥 Download Markdown Report",
            data=md_content,
            file_name=f"{uploaded_file.name}_summary.md",
            mime="text/markdown"
        )
        
        st.markdown("---")
        st.subheader("📧 Email Action Items")
        recipient_email = st.text_input("Enter Recipient Email")
        if st.button("Send Email"):
            if recipient_email:
                with st.spinner("Sending email..."):
                    success, message = email_dispatcher.send_email(
                        recipient_email,
                        f"Meeting Summary: {uploaded_file.name}",
                        summary_data.get("summary", ""),
                        summary_data.get("action_items", [])
                    )
                if success:
                    st.success(message)
                else:
                    st.error(message)
            else:
                st.warning("Please enter a recipient email address.")