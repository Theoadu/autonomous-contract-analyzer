import base64
from pathlib import Path
from openai import OpenAI
from langfuse import observe


@observe()
def encode_image(image_path: str) -> str:
    """Encode image to base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


@observe()
def parse_contract_image(image_path: str, client: OpenAI) -> str:
    """Extract full text from contract image using GPT-4o."""
    if not Path(image_path).exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    base64_image = encode_image(image_path)

    response = client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Extract ALL text from this legal contract image. Preserve section numbers, headings, paragraphs, and formatting as faithfully as possible. Do not summarize or omit anything.",
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ],
        temperature=0.0,
    )
    return response.output_text.strip()
