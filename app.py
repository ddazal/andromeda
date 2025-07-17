import streamlit as st

from andromeda import Andromeda

st.set_page_config(page_title="Andromeda: Go Test Generator", layout="wide")

st.title("🌌 Andromeda: Go Test Generator")
st.markdown(
    "Paste your Go function code below, and Andromeda will generate an analysis, test cases, and Go test code using AI."
)

if "andromeda_instance" not in st.session_state:
    try:
        st.session_state.andromeda_instance = Andromeda()
    except Exception as e:
        st.error(
            f"Initialization Error: {e}. Please ensure Ollama is running and the specified model is available."
        )
        st.stop()  # Stop the app if initialization fails


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
    """,
)

# Button to trigger generation
if st.button("Generate Tests"):
    if go_code_input.strip():
        # Clear previous results and errors
        st.session_state.results = None
        st.session_state.errors = []

        # Run the generation process
        with st.status("Starting test generation...", expanded=True) as status:
            results = andromeda.generate_go_tests(go_code_input, status_reporter=status)
            st.session_state.results = results

            if results["errors"]:
                for err in results["errors"]:
                    st.error(err)
                status.update(
                    label="Test generation completed with errors.",
                    state="error",
                    expanded=False,
                )
                st.warning(
                    "Please check the console/logs for more details if needed."
                )  # Additional warning below status
            else:
                status.update(
                    label="Test generation completed successfully!",
                    state="complete",
                    expanded=False,
                )
                st.balloons()  # Fun little celebration
    else:
        st.warning("Please paste your Go function code to generate tests.")

# Display Results
if "results" in st.session_state and st.session_state.results:
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
st.caption(
    f"Powered by Ollama ({st.session_state.andromeda_instance.model}) and Streamlit."
)
