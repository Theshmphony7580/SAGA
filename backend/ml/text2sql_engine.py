from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

# Use a model that supports HF serverless Inference API
MODEL_NAME = "Qwen/Qwen2.5-Coder-32B-Instruct"


def _get_client():
    """Create a fresh client with the current token from .env."""
    load_dotenv(override=True)
    token = os.getenv("HF_API_TOKEN")
    if not token:
        raise RuntimeError("HF_API_TOKEN not set in .env")
    return InferenceClient(token=token)


def generate_sql(schema: str, question: str) -> str:
    """
    Uses HuggingFace Inference API (chat completion) to convert
    a natural language question into a SQL query.
    """

    system_prompt = """You are an expert SQL generator. You ONLY output raw SQL queries.

Rules:
- Use ONLY SELECT queries
- Do NOT modify data (no INSERT, UPDATE, DELETE, DROP, etc.)
- Use the EXACT table name from the schema provided
- Add LIMIT 100 if the user does not specify a row limit
- Return ONLY the raw SQL query — no explanations, no markdown fences, no commentary"""

    user_prompt = f"""Schema:
{schema}

Question:
{question}

SQL:"""

    try:
        response = _get_client().chat_completion(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=256,
            temperature=0.1,
        )
        sql = response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Text2SQL model call failed: {e}") from e

    if not sql or not sql.strip():
        raise ValueError("Text2SQL model returned empty output")

    return sql.strip()
