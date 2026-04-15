import streamlit as st
import requests

st.set_page_config(page_title="Cloud Screenshot Analyzer", layout="wide")

st.title("📸 Cloud-Based Screenshot Analyzer")
st.write("Upload a screenshot to extract text and get ML-based insights.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Uploaded Screenshot', use_column_width=True)
    
    if st.button("Analyze Screenshot"):
        with st.spinner('Processing...'):
            files = {"file": uploaded_file.getvalue()}
            # Replace localhost with your AWS EC2 Public IP after deployment
            response = requests.post("http://54.226.75.102:8000/analyze", files=files)
            
            if response.status_code == 200:
                data = response.json()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Extracted Text")
                    st.text_area("", data['text'], height=300)
                
                with col2:
                    st.subheader("ML Analysis")
                    st.success(f"**Category:** {data['category']}")
                    st.info(f"**Confidence:** {data['confidence']}")
                    st.warning(f"**Actionable Insight:** {data['insight']}")
            else:
                st.error("Failed to process image.")