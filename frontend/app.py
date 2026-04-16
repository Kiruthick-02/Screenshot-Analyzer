import streamlit as st
import requests

st.set_page_config(page_title="Cloud Screenshot Analyzer", layout="wide")

# Sidebar Navigation
st.sidebar.title("📸 Screenshot Analyzer")
page = st.sidebar.radio("Navigate", [
    "🏠 Home",
    "🔍 Analyze Screenshot",
    "🧾 OCR Viewer",
    "🧠 Insight History",
    "📚 Use Cases"
])

# ------------------ HOME ------------------
if page == "🏠 Home":
    st.title("📸 Cloud-Based Screenshot Analyzer")

    st.markdown("""
    ### 🔍 What this system does
    - Extracts text from screenshots using OCR  
    - Classifies content using Machine Learning  
    - Generates meaningful insights  

    ### ⚡ Supported Inputs
    - Error Screenshots  
    - Chat Conversations  
    - Code Snippets  
    - Bills / Receipts  

    ### 🚀 Workflow
    Upload → Extract → Analyze → Insights
    """)

    st.success("Navigate to 'Analyze Screenshot' to get started.")

# ------------------ ANALYZE ------------------
elif page == "🔍 Analyze Screenshot":
    st.title("🔍 Screenshot Analysis")

    uploaded_file = st.file_uploader("Upload Screenshot", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.image(uploaded_file, caption="Uploaded Screenshot", use_column_width=True)

        with col2:
            st.markdown("### 📋 Ready to Analyze")
            
            if st.button("🚀 Analyze Now"):
                with st.spinner("Processing..."):
                    try:
                        files = {"file": uploaded_file.getvalue()}
                        response = requests.post(
                            "http://54.226.75.102:8000/analyze",
                            files=files
                        )

                        if response.status_code == 200:
                            data = response.json()

                            st.success("✅ Analysis Complete")

                            st.markdown("---")

                            colA, colB = st.columns(2)

                            with colA:
                                st.subheader("📝 Extracted Text")
                                st.text_area("", data['text'], height=300)

                            with colB:
                                st.subheader("🤖 ML Insights")
                                st.metric("Category", data['category'])
                                st.metric("Confidence", data['confidence'])
                                st.info(f"💡 {data['insight']}")

                            # Save history
                            if "history" not in st.session_state:
                                st.session_state.history = []

                            st.session_state.history.append(data)

                        else:
                            st.error("❌ Unable to process image.")

                    except:
                        st.error("⚠️ Unable to connect to server.")

# ------------------ OCR VIEWER ------------------
elif page == "🧾 OCR Viewer":
    st.title("🧾 OCR Text Explorer")

    st.markdown("View previously extracted text results.")

    if "history" in st.session_state and len(st.session_state.history) > 0:
        for i, item in enumerate(st.session_state.history[::-1]):
            with st.expander(f"📄 Screenshot Result #{len(st.session_state.history)-i}"):
                st.text_area("Extracted Text", item['text'], height=200)
    else:
        st.info("No OCR data available. Analyze a screenshot first.")

# ------------------ INSIGHT HISTORY ------------------
elif page == "🧠 Insight History":
    st.title("🧠 Analysis History")

    if "history" in st.session_state and len(st.session_state.history) > 0:
        for i, item in enumerate(st.session_state.history[::-1]):
            col1, col2, col3 = st.columns(3)

            col1.write(f"**Category:** {item['category']}")
            col2.write(f"**Confidence:** {item['confidence']}")
            col3.write(f"**Insight:** {item['insight']}")

            st.markdown("---")
    else:
        st.info("No analysis history available.")

# ------------------ USE CASES ------------------
elif page == "📚 Use Cases":
    st.title("📚 Real-World Use Cases")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💻 Error Detection")
        st.write("Analyze error screenshots and get debugging insights.")

        st.subheader("💬 Chat Analysis")
        st.write("Understand sentiment and context from chat screenshots.")

    with col2:
        st.subheader("🧾 Invoice Processing")
        st.write("Extract important fields like amount and date.")

        st.subheader("🧑‍💻 Code Understanding")
        st.write("Identify programming errors from screenshots.")
