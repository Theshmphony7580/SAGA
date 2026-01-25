from huggingface_hub import InferenceClient
from backend.config import HF_API_TOKEN

MODEL_NAME = "Ellbendls/Qwen-2.5-3b-Text_to_SQL"

client = InferenceClient(
    model=MODEL_NAME,
    token=HF_API_TOKEN
)


def generate_sql(schema: str, question: str):

    prompt = f"""
You are an expert SQL generator.

Rules:
- Use ONLY SELECT queries
- Do NOT modify data
- Add LIMIT 100 if not specified
- Return SQL only

Schema:
{schema}

Question:
{question}

SQL:
"""

    result = client.text_generation(
        prompt,
        max_new_tokens=200,
        temperature=0.1
    )
    if isinstance(result, list):
        sql = result[0]["generated_text"]
    else:
        sql = result

    return sql.strip()