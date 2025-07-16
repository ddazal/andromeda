import streamlit as st
from dotenv import load_dotenv
import os
from andromeda import Andromeda

load_dotenv()

st.set_page_config(page_title="Andromeda: Go Test Generator", layout="wide")

st.title("🌌 Andromeda: Go Test Generator")
st.markdown("Paste your Go function code below, and Andromeda will generate an analysis, test cases, and Go test code using AI.")

if 'andromeda_instance' not in st.session_state:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            st.session_state.andromeda_instance = Andromeda(api_key)
        except ValueError as e:
            st.error(f"Configuration Error: {e}. Please ensure your OPENAI_API_KEY is set in a `.env` file or environment variables.")
            st.stop() # Stop the app if API key is missing
    else:
        st.error("Error: OPENAI_API_KEY not found. Please set the OPENAI_API_KEY environment variable in a `.env` file or directly.")
        st.stop() # Stop the app if API key is missing

andromeda = st.session_state.andromeda_instance

# Input Text Area for Go Function
go_code_input = st.text_area(
    "Paste your Go Function Code here:",
    height=300,
    placeholder="""
type rectangle struct {
    width  float64
    height float64
}

func (r *rectangle) area() float64 {
    if r.width < 0 || r.height < 0 {
        panic("width and height must be non-negative")
    }
    // Calculate the area of the rectangle
    return r.width * r.height
}
    """
)

# Button to trigger generation
if st.button("Generate Tests"):
    if go_code_input.strip():
        # Clear previous results and errors
        st.session_state.results = None
        st.session_state.errors = []

        # Run the generation process
        st.info("Generating tests... This may take a moment.")
        results = andromeda.generate_go_tests(go_code_input)
        st.session_state.results = results

        if results["errors"]:
            for err in results["errors"]:
                st.error(err)
            st.warning("Test generation completed with errors. Please check the console/logs.")
        else:
            st.success("Test generation completed successfully!")
            st.balloons() # Fun little celebration

# Display Results
if 'results' in st.session_state and st.session_state.results:
    results = st.session_state.results

    st.markdown("---")

    st.subheader("📊 Function Analysis")
    if results["analysis"]:
        st.write(results["analysis"])
    else:
        st.info("Analysis not generated.")

    st.subheader("🧪 Generated Test Cases")
    if results["test_cases"]:
        st.markdown(results["test_cases"])
    else:
        st.info("Test cases not generated.")

    st.subheader("📝 Go Test Code (`_test.go`)")
    if results["go_test_code"]:
        st.code(results["go_test_code"], language="go")
    else:
        st.info("Go test code not generated.")

    if results["errors"]:
        st.subheader("❗ Errors Encountered")
        for error in results["errors"]:
            st.error(error)

st.markdown("---")
st.caption("Powered by OpenAI (gpt-4o-mini) and Streamlit.")