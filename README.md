# 🌌 Andromeda: Go Test Generator

Andromeda is a Streamlit-based web application running on Ollama to analyze Go functions, generate comprehensive test cases, and produce idiomatic Go test code. 


## ✨ Features

* **Go Function Analysis:** Understands the purpose, inputs, outputs, and edge cases of your Go code.
* **Intelligent Test Case Generation:** Creates a list of distinct test scenarios, including positive, zero, and error/panic cases.
* **Automatic Go Test Code Generation:** Writes ready-to-use `_test.go` code using standard Go `testing` package conventions.
* **Local LLM Integration:** Powered by Ollama, allowing you to run powerful LLMs locally without relying on external API keys (except for your local Ollama setup).
* **Interactive Web UI:** A user-friendly interface built with Streamlit for easy interaction.
* **Step-by-Step Progress:** Provides clear feedback on the current stage of test generation.

## 🚀 Getting Started

Follow these steps to set up and run Andromeda on your local machine.

### Prerequisites

* **Python 3.10+:** Download and install Python from [python.org](https://www.python.org/downloads/).
* **Ollama:** You need Ollama installed and running on your system.
    * Download and install Ollama from [ollama.com](https://ollama.com/download).
    * Ensure the Ollama server is running (it usually runs in the background after installation).
* **Ollama Model:** You need to pull the specific LLM model that Andromeda uses. This project is configured for `qwen2.5-coder:7b`.
    * Open your terminal and run:
        ```bash
        ollama pull qwen2.5-coder:7b
        ```
    * If you wish to use a different model, you'll need to update the `self.model` variable in `andromeda.py`.

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/ddazal/andromeda.git](https://github.com/ddazal/andromeda.git)
    cd andromeda
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    * **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    * **On Windows (Command Prompt):**
        ```bash
        venv\Scripts\activate.bat
        ```
    * **On Windows (PowerShell):**
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```

4.  **Install Dependencies:**
    With your virtual environment active, install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  **Ensure Ollama is Running and Model is Pulled:** Double-check the "Prerequisites" section above.

2.  **Navigate to the Project Directory:** Make sure your terminal is in the directory where `app.py` and `andromeda.py` are located.

3.  **Run the Streamlit App:**

    ```bash
    streamlit run app.py
    ```

4.  **Access the UI:**
    Your default web browser should automatically open a new tab with the Andromeda app, typically at `http://localhost:8501`. If it doesn't, copy and paste the URL from your terminal into your browser.

## 👩‍💻 Usage

1.  **Paste Go Function:** In the Streamlit web interface, paste your Go function code into the provided text area.
2.  **Generate Tests:** Click the "Generate Tests" button.
3.  **Observe Progress:** A single status bar will appear, showing the current step (e.g., "Analyzing Go function...", "Generating test cases..."). You can expand it to see more detailed logs.
4.  **View Results:** Once the generation is complete, the analysis, generated test cases, and the final Go test code will be displayed below the input area.

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, feel free to open an issue or submit a pull request.