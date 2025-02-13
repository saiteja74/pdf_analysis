import streamlit as st
import fitz  # PyMuPDF
from groq import Groq
import os
from typing import List

# Initialize Groq client
client = Groq(
    api_key="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"
)

def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from uploaded PDF file."""
    try:
        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = ""
        for page in pdf_document:
            text += page.get_text()
        return text
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return ""

def get_llm_response(context: str, query: str) -> str:
    """Get response from Groq API."""
    try:
        prompt = f"""Context: {context}\n\nQuestion: {query}\n\nPlease provide an answer based on the context above."""
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0.1,
            max_tokens=1024,
        )
        
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error getting response from Groq: {str(e)}")
        return ""

def main():
    # Set up the centered container
    container = st.container()
    with container:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            
            st.title("PDF Q&A System")
            
            # File uploader with reduced size
            pdf_files = st.file_uploader(
                "Upload PDF file(s)",
                type="pdf",
                accept_multiple_files=True,
                label_visibility="collapsed"
            )
            
            if pdf_files:
                # Extract text from all PDFs
                all_text = ""
                for pdf_file in pdf_files:
                    st.write(f"Processing: {pdf_file.name}")
                    text = extract_text_from_pdf(pdf_file)
                    all_text += f"\n\nContent from {pdf_file.name}:\n{text}"
                
                # Query input with custom styling
                query = st.text_input(
                    "Your question:",
                    key="query",
                    label_visibility="collapsed",
                    placeholder="Enter your question about the PDF(s)"
                )
                
                # Submit button with custom styling
                if st.button("Get Answer", use_container_width=True):
                    if query:
                        with st.spinner("Getting answer..."):
                            response = get_llm_response(all_text, query)
                            st.write("### Answer")
                            st.write(response)
                    else:
                        st.warning("Please enter a question.")

if __name__ == "__main__":
    # Set page configuration
    st.set_page_config(
        page_title="PDF Q&A System",
        page_icon="📚",
        layout="centered",  # Changed to centered layout
        initial_sidebar_state="collapsed"  # Hide sidebar by default
    )
    
    # Add custom CSS to make the interface more compact
    st.markdown("""
        <style>
        .block-container {
            padding-top: 4rem;
            padding-bottom: 4rem;
            max-width: 10000px;
        }
        .stFileUploader > div > div {
            padding: 1rem;
        }
        .stTextInput > div > div > input {
            padding: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    main()
