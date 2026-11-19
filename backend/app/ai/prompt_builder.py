import os
import logging
from typing import List, Dict

logger = logging.getLogger("aethera.prompt_builder")
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts")

def get_template(filename: str) -> str:
    """
    Read a prompt text template safely.
    """
    path = os.path.join(TEMPLATE_DIR, filename)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read prompt template {filename}: {e}")
    return ""

def build_aera_prompt(
    mode: str,
    level: str,
    question: str,
    context: str,
    history: List[Dict[str, str]],
    compound_name: str,
    compound_formula: str,
    compare_name: str = "",
    compare_formula: str = ""
) -> str:
    """
    Stitch database contexts, level instructions, mode tasks, and chat history
    into a unified prompt payload.
    """
    # 1. Resolve core task/mode template
    task_tpl = get_template(f"{mode}.txt")
    if not task_tpl:
        task_tpl = "Answer the user question about this compound based on context.\nQuestion: {question}"

    # 2. Resolve level instructions template
    level_map = {
        "school": "beginner.txt",
        "high_school": "beginner.txt",
        "university": "intermediate.txt",
        "research": "advanced.txt",
        "professional": "advanced.txt"
    }
    level_file = level_map.get(level.lower(), "intermediate.txt")
    level_tpl = get_template(level_file)

    # 3. Assemble Prompt body
    prompt_str = f"{context}\n\n"

    if level_tpl:
        prompt_str += f"### CRITICAL EXPLANATION LEVEL INSTRUCTION:\n{level_tpl}\n\n"

    prompt_str += "### TASK INSTRUCTION:\n"
    try:
        if mode == "compare":
            prompt_str += task_tpl.format(
                name_a=compound_name,
                formula_a=compound_formula,
                name_b=compare_name,
                formula_b=compare_formula,
                level=level,
                question=question
            )
        elif mode == "summarize":
            prompt_str += task_tpl.format(
                name=compound_name,
                formula=compound_formula,
                level=level,
                question=question
            )
        else: # explain, teach, research, etc.
            prompt_str += task_tpl.format(
                name=compound_name,
                formula=compound_formula,
                category="", 
                subcategory="",
                smiles="",
                inchi="",
                description="",
                biological_role="",
                applications="",
                industrial_uses="",
                physical_properties="",
                chemical_properties="",
                hazards="",
                references="",
                level=level,
                question=question
            )
    except KeyError as e:
        logger.error(f"Formatting placeholder key error in {mode}.txt: {e}")
        # fallback string without complex formatting to prevent crashes
        prompt_str += f"Explain {compound_name} ({compound_formula}) regarding: {question}"

    # 4. Append chat history to preserve conversation context
    if history:
        prompt_str += "\n\n### ACTIVE SESSION CONVERSATION HISTORY (Do NOT persist):\n"
        for msg in history:
            role = "User" if msg.get("role") == "user" else "Assistant"
            prompt_str += f"{role}: {msg.get('content')}\n"

    # 5. Add current user question
    prompt_str += f"\n\nUser's Current Question: {question}\n\n"
    prompt_str += "Aera scientific output:"

    return prompt_str
