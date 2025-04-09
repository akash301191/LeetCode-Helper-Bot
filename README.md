# LeetCode Helper Bot

LeetCode Helper Bot is an intelligent Streamlit application that takes in LeetCode problems and their solutions, refactors the code for clarity and efficiency, and provides detailed explanations to enhance your problem-solving skills. Powered by [Agno](https://github.com/agno-agi/agno) and OpenAI's GPT-4o model, this tool simplifies technical solutions and adds helpful context to accelerate your coding journey.

## Folder Structure

```
leetcode-helper-bot/
├── leetcode-helper-bot.py
├── README.md
└── requirements.txt
```

- **leetcode-helper-bot.py**: The main Streamlit application.
- **requirements.txt**: A list of all required Python packages.
- **README.md**: This documentation file.

## Features

- **LeetCode Input Interface:**  
  Paste any LeetCode problem statement and your Python solution side by side in a dual-column layout.

- **Refactored Code Generation:**  
  Customize refactoring preferences such as level of refactor, whether to preserve variable names, and whether to prioritize readability.

- **Commented Code Output:**  
  Choose between concise, descriptive, or step-by-step commenting styles, and optionally include a structured docstring with algorithm overview and complexity.

- **Code Explanation:**  
  Generate a human-readable explanation of your solution with a choice of basic, intermediate, or detailed depth, and optionally include time and space complexity analysis.

- **Download Output:**  
  Save both the refactored solution and explanation as a single downloadable `.txt` file for future study or sharing.

- **Streamlined UI:**  
  A clean, organized Streamlit interface that guides users through code input, customization, result generation, and download.

## Prerequisites

- Python 3.11 or higher  
- An OpenAI API key (get yours [here](https://platform.openai.com/account/api-keys))

## Installation

1. **Clone the repository** (or download it):
   ```bash
   git clone https://github.com/akash301191/LeetCode-Helper-Bot.git
   cd LeetCode-Helper-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Streamlit app**:
   ```bash
   streamlit run leetcode-helper-bot.py
   ```

2. **Open your browser** to the local URL shown in the terminal (usually `http://localhost:8501`).

3. **Interact with the app**:
   - Enter your OpenAI API key when prompted.
   - Paste your LeetCode problem and solution into the side-by-side text areas.
   - Adjust the refactoring, commenting, and explanation settings in the sidebar.
   - Click the **Refactor & Comment Code** button.
   - Review the refactored solution and detailed explanation.
   - Download the full result as a `.txt` file if desired.

## Code Overview

- **`main`**: Orchestrates the application flow—from input collection to model invocation, output rendering, and file download.
- **`customization_sidebar`**: Provides user controls for customizing refactoring level, commenting style, and explanation depth.
- **`leetcode_input_section`**: Allows users to input the LeetCode problem and solution in a dual-column layout.
- **`initialize_openai_model`**: Initializes the GPT-4o model using the user-provided OpenAI API key.
- **`refactor_and_comment_code`**: Invokes an agent to refactor the original code and then adds comments according to the selected style.
- **`generate_code_explanation`**: Uses a dedicated agent to generate a step-by-step explanation of the code with optional complexity analysis.
- **`sanitize_text`**: Cleans and formats problem and solution inputs to ensure model-safe prompts.

## Contributions

Contributions are welcome! Feel free to fork the repository, improve the code, and open a pull request. Please ensure your changes follow the existing style and include any necessary documentation or tests.