from langchain.messages import SystemMessage, HumanMessage
from langchain.chat_models import init_chat_model
from models import ContractChange
from langfuse import observe


system_prompt = """
You are a legal change detection specialist. Using the provided context, 
compare the original and amended contracts to extract EXACT changes.

Rules:
- Only report real, observable changes
- Use precise section identifiers (e.g., "Section 4.2")
- Categorize topics (e.g., "Termination", "Confidentiality")
- Summarize clearly: what was added, deleted, or modified
"""


@observe()
def extract_changes(context_dict: dict, original: str, amendment: str) -> dict:
    """Agent 2: Extract validated changes using Pydantic."""
    llm = init_chat_model("gpt-4o-mini", model_provider="openai", temperature=0.0)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(
            content=f"Context:\n{context_dict["context"]}\n\nOriginal:\n{original}\n\nAmendment:\n{amendment}"
        ),
    ]

    llm = llm.with_structured_output(ContractChange)
    result = llm.invoke(messages)

    return result.model_dump() 
