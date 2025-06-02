import openai
import json
import os
from dotenv import load_dotenv
from src.genai_schema import classify_fn
from src.genai_fewshot import SYSTEM, FEW_SHOT
from src.taxonomy_service import unspsc_map

load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAPIKEY')

# (No need to set openai.api_base for official OpenAI API)

def classify_with_ai(desc: str, supp: str, candidates) -> dict:
    import time
    import json

    options = "\n".join(f"{i+1}. {r['code']} – {r['title']}" for i, r in candidates.iterrows())
    user_msg = (
        f"Invoice: '{desc}'\nSupplier: '{supp}'\nOptions:\n{options}\n"
        "Respond ONLY with a JSON object: {\"code\": \"<8-digit-code>\", \"confidence\": <score between 0 and 1>}."
        " Do not add any extra text or explanation."
    )

    for attempt in range(5):
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[{'role': 'system', 'content': SYSTEM}] + FEW_SHOT + [{'role': 'user', 'content': user_msg}],
                temperature=0,
                max_tokens=512
            )
            break  # Success, exit the retry loop
        except openai.error.RateLimitError:
            print("Rate limit hit, sleeping before retry...")
            time.sleep(5)  # Wait 5 seconds before retrying
        except Exception as e:
            print(f"[ERROR] OpenAI API call failed: {e}")
            return {
                "commodity_code": "",
                "commodity_title": "",
                "confidence": 0.0,
                "matched_rule": "",
            }
    else:
        # All retries failed
        print("[ERROR] All retries failed for OpenAI API call.")
        return {
            "commodity_code": "",
            "commodity_title": "",
            "confidence": 0.0,
            "matched_rule": "",
        }

    # Get the model's plain text response
    content = response['choices'][0]['message']['content']
    try:
        # Extract JSON from the response
        start = content.find('{')
        end = content.rfind('}') + 1
        json_str = content[start:end]
        args = json.loads(json_str)
    except Exception as e:
        print(f"[WARN] Could not parse JSON from model response: {content}")
        return {
            "commodity_code": "",
            "commodity_title": "",
            "confidence": 0.0,
            "matched_rule": "",
        }

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
        print(f"[WARN] UNSPSC code '{code}' not found in taxonomy map")
        return {
            "commodity_code": code,
            "commodity_title": "",
            "confidence": 0.0,
            "matched_rule": "",
        }

    info = unspsc_map[code].copy()
    info['confidence'] = args.get('confidence', 1.0)
    return info