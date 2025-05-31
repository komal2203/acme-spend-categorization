import openai
import json
import os
from dotenv import load_dotenv
from src.genai_schema import classify_fn
from src.genai_fewshot import SYSTEM, FEW_SHOT
from src.taxonomy_service import unspsc_map

load_dotenv()

# Set your OpenRouter API key
openai.api_key = os.getenv('OPENROUTER_API_KEY')

# Set OpenRouter API base URL explicitly
openai.api_base = "https://openrouter.ai/api/v1"

def classify_with_ai(desc: str, supp: str, candidates) -> dict:
    options = "\n".join(f"{i+1}. {r['code']} – {r['title']}" for i, r in candidates.iterrows())

    user_msg = (
    f"Invoice: '{desc}'\nSupplier: '{supp}'\nOptions:\n{options}\n"
    "Respond ONLY by calling the classify_invoice_line function. "
    "Select and return exactly one valid 8-digit UNSPSC code from the options list above. "
    "Do NOT return codes that are not listed. Your response must be a valid 8-digit code."
)

    response = openai.ChatCompletion.create(
        model='gpt-4o-mini',
        messages=[{'role': 'system', 'content': SYSTEM}] + FEW_SHOT + [{'role': 'user', 'content': user_msg}],
        tools=[{"type": "function", "function": classify_fn}],
        tool_choice='auto',
        temperature=0,
        max_tokens=1000
    )

    tool_calls = response['choices'][0]['message'].get('tool_calls', [])
    if not tool_calls:
        raise ValueError("No tool call returned by the model.")
    args_str = tool_calls[0].get('function', {}).get('arguments', '{}')
    args = json.loads(args_str)

    code = args.get('code')
    if not (code and len(code) == 8 and code.isdigit()):
        # Return a low-confidence result for manual review
        return {
        "commodity_code": code or "",
        "commodity_title": "",
        "confidence": 0.0,
        "matched_rule": "",
        }

    if code not in unspsc_map:
        raise KeyError(f"UNSPSC code '{code}' not found in taxonomy map")

    info = unspsc_map[code].copy()
    info['confidence'] = args.get('confidence', 1.0)
    return info
