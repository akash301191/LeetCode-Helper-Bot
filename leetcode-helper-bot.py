import re
import streamlit as st
from agno.agent import Agent
from agno.models.openai import OpenAIChat

def initialize_openai_model():
    try:
        api_key = st.session_state.openai_api_key
        return OpenAIChat(id='gpt-4o', api_key=api_key)
    except Exception as e:
        st.error(f"❌ Error initializing OpenAI Model: {e}")
        return None
    
def sanitize_text(text: str) -> str:
    """
    Sanitize input text (problem or solution) to avoid issues with quotes, formatting,
    and hidden characters in prompt construction or markdown rendering.
    """

    if not isinstance(text, str):
        return ""

    # Normalize smart quotes to standard quotes
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("‘", "'").replace("’", "'")

    # Escape triple backticks to prevent breaking markdown
    text = text.replace("```", "'''")

    # Remove invisible/control characters (except newlines)
    text = re.sub(r"[^\x20-\x7E\n]", "", text)

    # Replace tabs with spaces
    text = text.replace("\t", "    ")

    # Strip leading/trailing whitespace
    return text.strip()

def leetcode_input_section(): 
    st.markdown("## 📝 Paste Your LeetCode Problem and Solution")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        problem_input = st.text_area(
            "LeetCode Problem Statement",
            placeholder="Paste the problem description here...",
            height=300
        )

    with col2:
        solution_input = st.text_area(
            "LeetCode Solution (Python Code)",
            placeholder="Paste your existing solution here...",
            height=300
        )

    return problem_input, solution_input

def customization_sidebar():
        
    with st.sidebar:
        # ----------------- Refactoring Options ----------------- #
        st.markdown("## ⚙️ Output Settings")
        st.markdown("---")

        st.markdown("### 🛠 Refactoring")
        refactor_level = st.selectbox("Level", ["Basic", "Moderate", "Aggressive"], key="refactor_level")
        preserve_names = st.checkbox("Preserve Names", value=True, key="preserve_names")
        prioritize_readability = st.checkbox("Prioritize Readability", value=True, key="readability")
        st.markdown("---")

        # ----------------- Commenting Options ------------------ #
        st.markdown("#### 💬 Commenting")
        comment_style = st.selectbox(
            "Style", ["Concise", "Descriptive", "Step-by-step"], key="comment_style"
        )
        include_docstring = st.checkbox("Include Docstring", value=True, key="docstring")
        st.markdown("---")

        # ----------------- Explanation Options ----------------- #
        st.markdown("### 📘 Explanation")
        explanation_depth = st.selectbox(
            "Depth", ["Basic", "Intermediate", "Detailed"], key="explanation_depth"
        )
        include_complexity = st.checkbox("Time & Space Complexity", value=True, key="complexity")
        st.markdown("---")

    return {
        "refactor_level": refactor_level,
        "preserve_names": preserve_names,
        "prioritize_readability": prioritize_readability,
        "comment_style": comment_style,
        "include_docstring": include_docstring,
        "explanation_depth": explanation_depth,
        "include_complexity": include_complexity,
    }

def refactor_and_comment_code(openai_model, problem_text: str, solution_text: str, customization: dict) -> str:
    """
    Calls the LeetCode Refactor Agent to refactor a solution based on the problem and customization options.
    For now, this only performs refactoring. Commenting will be handled by a second agent later.
    """

    problem_text = sanitize_text(problem_text)
    solution_text = sanitize_text(solution_text)

    refactor_agent = Agent(
        name="LeetCode Refactor Agent",
        role="Refactors LeetCode Python solutions based on user instructions.",
        model=openai_model,
        instructions=[
            "You will be given a LeetCode problem description and its solution code.",
            "Your task is to refactor the solution to simplify and improve its logic while ensuring it remains correct and efficient.",
            f"Apply the following user preferences during refactoring:",
            f"- **Refactor Level:** {customization['refactor_level']}",
            f"- **Preserve Variable Names:** {'Yes' if customization['preserve_names'] else 'No'}",
            f"- **Prioritize Readability:** {'Yes' if customization['prioritize_readability'] else 'No'}",
            "Do not add any comments or explanations in the code.",
            "Return only the final refactored code as a single markdown-formatted code block.",
            "Do not include any headings, notes, or content outside the code block."
        ]
    )

    response = refactor_agent.run(f"""
        problem: {problem_text},
        solution: {solution_text}
    """)

    refactored_code = response.content 

    comment_style_desc = {
        "Concise": "Add short inline comments that explain key lines or blocks of logic.",
        "Descriptive": (
            "Add clear, full-line comments that describe each important step in detail, "
            "especially clarifying reasoning, conditions, or loops wherever the logic may be non-obvious. "
            "Use helpful multi-line comments if needed. Follow the example of LeetCode editorial-level explanation."
        ),
        "Step-by-step": "Explain each individual line or small group of lines, making the logic approachable for beginners with no assumptions."
    }

    commenter_agent = Agent(
        name="LeetCode Commenter Agent",
        role="Adds helpful comments to refactored LeetCode code solutions based on user preferences.",
        model=openai_model,
        instructions=[
            "You will be given a LeetCode problem description and a refactored code solution.",
            "Your task is to enhance the code by adding meaningful comments that explain how it solves the problem.",
            f"{comment_style_desc[customization['comment_style']]}",
            f"{'Include a well-structured, detailed docstring at the top of each function that summarizes the problem, the algorithmic insight, the step-by-step approach, and time/space complexity.' if customization['include_docstring'] else 'Do not include a docstring.'}",
            "Do not change the code logic in any way. Only add comments or docstrings.",
            "The final output must be a single markdown-formatted code block containing the commented version of the refactored code.",
            "Do not include any text, explanation, or headings outside the code block."
        ]
    )

    response = commenter_agent.run(f"""
        problem: {problem_text},
        solution: {refactored_code}
    """)

    commented_code = response.content

    return commented_code

def generate_code_explanation(openai_model, problem_text: str, solution_text: str, customization: dict) -> str:
    """
    Calls the LeetCode Explanation Agent to generate a detailed explanation of the final code
    using the problem description and customization preferences.
    """

    # Sanitize inputs
    problem_text = sanitize_text(problem_text)
    solution_text = sanitize_text(solution_text)

    # Extract customization settings
    explanation_depth = customization.get("explanation_depth", "Intermediate")
    include_complexity = customization.get("include_complexity", True)

    # Base explanation instructions by depth
    depth_instructions = {
        "Basic": "Explain the core logic of the solution in 3–4 sentences, focusing on what the code does overall.",
        "Intermediate": "Break down the key steps in the logic, including major loops, conditions, and how the problem is solved step by step.",
        "Detailed": (
            "Provide a comprehensive, structured explanation covering each logical component of the code, "
            "including control flow, data structure choices, and the problem-solving strategy."
        )
    }

    # Optional complexity detail
    complexity_instruction = (
        "Also include a brief analysis of time and space complexity at the end of the explanation."
        if include_complexity else
        "You do not need to include time or space complexity analysis."
    )

    # Create the agent
    explanation_agent = Agent(
        name="LeetCode Explanation Agent",
        role="Generates human-readable explanations of LeetCode solutions based on problem context and final code.",
        model=openai_model,
        instructions=[
            "You will be given a LeetCode problem description and a refactored, commented solution.",
            "Your task is to generate a clear explanation that helps the user understand how the code solves the problem.",
            depth_instructions[explanation_depth],
            complexity_instruction,
            "Do not repeat or restate the code. Focus only on explaining the logic.",
            "Format the explanation using markdown if needed (bullet points, sections) to make it easier to read.",
            "Return your explanation as a markdown-formatted string, without any surrounding notes or greetings."
        ]
    )

    # Run the agent
    response = explanation_agent.run(f"""
        problem: {problem_text},
        solution: {solution_text}
    """)

    return response.content

def main() -> None:
    st.set_page_config(page_title="LeetCode Helper Bot", page_icon="🧠", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>🧠 LeetCode Helper Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to LeetCode Helper Bot — an intelligent Streamlit tool that takes in LeetCode problems and solutions, refactors code for simplicity, and delivers step-by-step explanations to enhance your problem-solving skills.",
        unsafe_allow_html=True
    )

    # Get OpenAI API Key
    openai_api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )

    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.success("✅ API key updated!")

    st.markdown("---")

    customization_options = customization_sidebar()
    problem_text, solution_text = leetcode_input_section()
    st.markdown("---")

    # Refactor & Comment Button Workflow
    if st.button("🔧 Refactor & Comment Code"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key.")
        elif not problem_text.strip() or not solution_text.strip():
            st.warning("⚠️ Please paste both the problem and the solution to proceed.")
        else:
            openai_model = initialize_openai_model()

            with st.spinner("Refactoring and Commenting your Solution..."):
                final_code = refactor_and_comment_code(
                    openai_model=openai_model,
                    problem_text=problem_text,
                    solution_text=solution_text,
                    customization=customization_options
                )
                st.session_state.final_code = final_code

            with st.spinner("🧠 Generating explanation for your solution..."):
                explanation = generate_code_explanation(
                    openai_model=openai_model,
                    problem_text=problem_text,
                    solution_text=st.session_state.final_code,
                    customization=customization_options
                )
                st.session_state.code_explanation = explanation

    # Always render output if it exists in session state
    if "code_explanation" in st.session_state:
        st.markdown("## 🧠 Code Explanation")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(st.session_state.code_explanation)
        st.markdown("---")

    if "final_code" in st.session_state:
        st.markdown("## 📄 Final Solution")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(st.session_state.final_code)
        st.markdown("---")

    # Download button (persistent and independent of previous button click)
    if "final_code" in st.session_state and "code_explanation" in st.session_state:
        download_content = f"""#🧠 Code Explanation\n\n{st.session_state.code_explanation}\n\n# 📄 Refactored Solution\n\n{st.session_state.final_code}"""

        st.download_button(
            label="📥 Download Final Solution & Explanation",
            data=download_content,
            file_name="leetcode_helper_output.txt",
            mime="text/plain"
        )
         

if __name__ == "__main__": 
    main()
