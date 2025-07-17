import streamlit as st
from ollama import Client, ResponseError
from typing import Any

class Andromeda:
    """
    Andromeda class encapsulates the logic for interacting with the Ollama API
    to analyze Go functions, generate test cases, and produce Go test code.
    It manages the prompt chaining and output presentation.
    """
    def __init__(self, model: str = "qwen2.5-coder:7b"):
        """
        Initializes the Andromeda client for Ollama.
        """
        self.client = Client()
        self.model = model

    def _call_ollama_api(self, system_prompt: str, user_prompt: str, temperature: float) -> str | None:
        """
        Helper method to call the Ollama API with common parameters and handle errors.
        """
        try:
            ollama_response = self.client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                options={"temperature": temperature}
            )
            return ollama_response.message.content
        except ResponseError as e: # Catch Ollama-specific API errors
            st.error(f"Error communicating with Ollama API: {e.status_code} - {e.response}")
            return None
        except Exception as e: # Catch any other unexpected errors
            st.error(f"An unexpected error occurred: {e}")
            return None

    def generate_go_tests(self, function_code: str, status_reporter: Any = None) -> dict:
        """
        Executes the prompt chaining for code analysis, test case generation,
        and Go test code generation. Returns a dictionary of results.
        """
        results = {
            "analysis": None,
            "test_cases": None,
            "go_test_code": None,
            "errors": []
        }

        try:

            # --- Prompt 1: Analyze the Function ---
            if status_reporter:
                status_reporter.update(label="Analyzing Go function...", state="running", expanded=True)
                status_reporter.write("Starting static analysis of the Go function...")
            
            system_prompt_analysis = "You are an expert software engineer specialized in Go. Your task is to meticulously analyze Go code and identify its purpose, inputs, outputs, and all potential edge cases or error conditions."
            prompt_analysis = f"""
            Analyze the provided Go function delimited by <go_code></go_code> tags. Describe its purpose, inputs, outputs, and any potential edge cases or error conditions based on its docstring and code.

            <go_code>
            {function_code}
            </go_code>
            """
            analysis = self._call_ollama_api(system_prompt_analysis, prompt_analysis, 0.3)
            if analysis is None:
                results["errors"].append("Failed to perform code analysis.")
                return results
            results["analysis"] = analysis

            # --- Prompt 2: Generate Test Cases ---
            if status_reporter:
                status_reporter.update(label="Generating test cases...", state="running", expanded=True)
                status_reporter.write("Based on analysis, formulating diverse test scenarios...")
            
            system_prompt_test_cases = "You are a quality assurance expert. Your goal is to generate comprehensive and distinct test cases (inputs, expected outputs/behaviors) for a given function, covering all identified scenarios including positive, zero, and error cases."
            prompt_test_cases = f"""
            Based on the analysis delimited by <analysis></analysis> tags, generate a list of distinct test cases (inputs and expected outputs/behaviors) to thoroughly test the Go function delimited by <go_code></go_code> tags. Include positive cases, zero cases, and cases that should trigger some kind of error or panic.

            <analysis>
            {analysis}
            </analysis>

            <go_code>
            {function_code}
            </go_code>
            """
            tests = self._call_ollama_api(system_prompt_test_cases, prompt_test_cases, 0.4)
            if tests is None:
                results["errors"].append("Failed to generate test cases.")
                return results
            results["test_cases"] = tests

            # --- Prompt 3: Generate Go Test Code ---
            if status_reporter:
                status_reporter.update(label="Generating Go test code...", state="running", expanded=True)
                status_reporter.write("Translating test cases into executable Go test code...")
            
            system_prompt_go_tests = "You are an experienced Go developer. Your task is to write idiomatic Go test code using the standard 'testing' package, based on provided test cases and the function under test. Ensure correct error/panic handling assertions. Assume the function is part of a `main` package for simplicity, but use standard Go testing conventions."
            prompt_go_tests = f"""
            Using the generated test cases delimited by <test_cases></test_cases> tags, write Go test code for the function delimited by <go_code></go_code> tags.

            <test_cases>
            {tests}
            </test_cases>

            <go_code>
            {function_code}
            </go_code>
            """
            go_test_code = self._call_ollama_api(system_prompt_go_tests, prompt_go_tests, 0.2)
            if go_test_code is None:
                results["errors"].append("Failed to generate Go test code.")
                return results
            results["go_test_code"] = go_test_code
        except Exception as e:
            results["errors"].append(str(e))

        return results