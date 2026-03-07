import os
import json
from pathlib import Path
from typing import Any, Dict, List
from dotenv import load_dotenv
import base64

import httpx
from fastapi import FastAPI, HTTPException, APIRouter
load_dotenv()

router = APIRouter()

BASE_DIR = Path(__file__).parent
OBSERVED_IMAGE_PATH = BASE_DIR / "drawings" / "1.png"

with open(OBSERVED_IMAGE_PATH, "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")

# -------- LLM Config --------
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openai/gpt-5-nano"
)
OPENROUTER_SITE_URL = os.getenv("OPENROUTER_SITE_URL", "http://localhost:8000")
OPENROUTER_APP_NAME = os.getenv("OPENROUTER_APP_NAME", "image-analysis")

def file_to_data_url(image_path: Path) -> str:
    if not image_path.exists():
        raise HTTPException(status_code=500, detail=f"Missing observed image file: {image_path}")
    b64 = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    return f"data:image/png;base64,{b64}"


def load_json(p: Path):
    if not p.exists():
        raise HTTPException(status_code=500, detail=f"Missing file: {p.name}")
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Invalid JSON in {p.name}: {e}")


def extract_first_json_object(text: str) -> str:
    """Defensive extraction in case the model adds extra text."""
    first = text.find("{")
    last = text.rfind("}")
    if first == -1 or last == -1 or last <= first:
        return text
    return text[first : last + 1]


def validate_analysis_shape(obj: Any) -> Dict[str, Any]:
    """
    Minimal validation so your API doesn't crash later.
    You can tighten this over time.
    """
    if not isinstance(obj, dict):
        raise ValueError("Analysis is not a JSON object")

    # Fill defaults if missing
    obj.setdefault("confidence", 0.5)
    obj.setdefault("affirmations", [])
    obj.setdefault("issues", [])
    obj.setdefault("next_steps", [])
    obj.setdefault("questions", [])

    if not isinstance(obj["issues"], list):
        raise ValueError("'issues' must be a list")
    if not isinstance(obj["next_steps"], list):
        raise ValueError("'next_steps' must be a list")
    if not isinstance(obj["affirmations"], list):
        raise ValueError("'affirmations' must be a list")
    if not isinstance(obj["questions"], list):
        raise ValueError("'questions' must be a list")

    return obj

# CHANGE
SYSTEM_PROMPT = """
You are a geometric scene interpreter that describes the 3D images in a drawing.

Your task is to analyze an input image and identify the basic 3D geometric shapes that compose the structure. Focus only on simple primitives commonly used in AutoCAD modeling.

Allowed primitive shapes include:

* cube
* rectangular_prism
* cylinder
* sphere
* cone
* triangular_prism
* square_pyramid
* wedge

Instructions:

1. Identify the minimal set of 3D primitives that best represent the objects in the image.
2. Use approximate relative measurements rather than exact values. Dimensions should reflect proportions visible in the image.
3. Coordinates should represent the center or base of each primitive.
4. Do not overfit details — simplify complex forms into basic primitives.
5. Ignore textures, colors, shading, and small decorative elements.

Output Format:
Give a general description of the 3D shapes in the drawing and the relative coordinates.

Guidelines for dimensions:

* Cubes/prisms: width, depth, height
* Sphere: radius
* Cylinder/cone: radius, height
* Pyramid: base_width, base_depth, height
* Wedge: width, depth, height

All measurements should be proportional and relative rather than exact real-world measurements.

Your goal is to produce a simplified geometric description that could easily be used as a starting point for AutoCAD modeling.

""".strip()


async def llm_analyze(data_url) -> Dict[str, Any]:
    """
    Send an image URL to the LLM and receive structured JSON describing 3D primitives.
    """
    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=500, detail="Missing OPENROUTER_API_KEY environment variable")

    payload = {
        "model": OPENROUTER_MODEL,
        "temperature": 0,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": data_url},  # base64 PNG
                    {"type": "text", "text": """Give a concise general description of the 3D shapes in this drawing in the following format:"
                    - Each shape has:
                    - "shape": type of shape (cube, pyramid, cylinder, prism, etc.)
                    - "size": size or dimensions
                    - "position": [x, y, z] coordinates in 3D space
                    - "relationship": optional, e.g., "on_top_of" another object
                 """}
                ]
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": OPENROUTER_SITE_URL,
        "X-Title": OPENROUTER_APP_NAME,
    }

    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
        if r.status_code >= 400:
            raise HTTPException(status_code=502, detail=f"OpenRouter error {r.status_code}: {r.text}")

        data = r.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")

        return content


# @router.get("/health")
# def health():
#     return {"ok": True}


@router.get("/analyze")
async def analyze():
    data_url = file_to_data_url(OBSERVED_IMAGE_PATH)
    analysis = await llm_analyze(data_url)

    # Return analysis only (clean). If you want to include inputs too, uncomment below.
    return {
        "analysis": analysis,
    }
