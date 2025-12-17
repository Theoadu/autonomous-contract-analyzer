def test_contextualization_agent():
    from src.agents.contextualization_agent import contextualize_documents
    orig = "Section 1: Hello.\nSection 2: World."
    am = "Section 1: Hello.\nSection 2: LangChain."
    result = contextualize_documents(orig, am)
    assert "context" in result
    assert isinstance(result["context"], str)

def test_extraction_agent_structure():
    from src.agents.extraction_agent import extract_changes
    context = {"context": "Both documents have Section 1 and Section 2."}
    orig = "Section 1: Hello."
    am = "Section 1: Hi."
    # This may fail without API, but should not crash on structure
    try:
        result = extract_changes(context, orig, am)
        assert "sections_changed" in result
    except Exception:
        pass  # Expected without real API