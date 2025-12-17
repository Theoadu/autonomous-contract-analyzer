from langchain.messages import SystemMessage, HumanMessage
from langchain.chat_models import init_chat_model
from langfuse import observe

system_prompt = """
You are a legal document analyst. Your task is to read an original contract and its amendment, then produce a structured context that maps corresponding sections, clauses, and exhibits. Focus on:
- Section numbering (e.g., Section 3.1, Exhibit B)
- Paragraph alignment
- Major structural elements

Your output will be used by another agent to detect precise changes.
"""


@observe()
def contextualize_documents(original: str, amendment: str) -> dict:
    """Agent 1: Understand and align document structures."""
    llm = init_chat_model("gpt-4o-mini", model_provider="openai", temperature=0.0)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(
            content=f"Original Contract:\n{original}\n\nAmended Contract:\n{amendment}"
        ),
    ]

    response = llm.invoke(messages)
    return {"context": response.content}
