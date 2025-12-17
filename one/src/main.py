import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI
from langfuse import Langfuse, observe
from rich import print
from image_parser import parse_contract_image
from agents.contextualization_agent import contextualize_documents
from agents.extraction_agent import extract_changes
from models import ContractChange

load_dotenv()

langfuse = Langfuse()

@observe()
def validate_output( data) -> ContractChange:
    return ContractChange.model_validate(data)

@observe()
def main():
    parser = argparse.ArgumentParser(description="Compare original and amended contract images.")
    parser.add_argument("--original", required=True, help="Path to original contract image (JPEG/PNG)")
    parser.add_argument("--amendment", required=True, help="Path to amendment contract image (JPEG/PNG)")
    parser.add_argument("--contract-id", default="default-session", help="Unique ID for tracing in Langfuse")
    args = parser.parse_args()

    # Set Langfuse session
    os.environ["LANGFUSE_SESSION_ID"] = args.contract_id
    # langfuse.context().session_id = args.contract_id
    

    # load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Step 1: Parse images
    original_text = parse_contract_image(args.original, client)
    amendment_text = parse_contract_image(args.amendment, client)

    # Step 2: Agent 1
    context = contextualize_documents(original_text, amendment_text)

    # Step 3: Agent 2
    change_data = extract_changes(context, original_text, amendment_text)

    # Step 4: Validate
    validated = validate_output(change_data)

    # Output
    print(validated.model_dump_json(indent=2))

    # Ensure trace is sent
    langfuse.flush()

if __name__ == "__main__":
    main()