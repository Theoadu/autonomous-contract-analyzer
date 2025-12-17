import pytest
from src.models import ContractChange

def test_valid_contract_change():
    data = {
        "sections_changed": ["Section 5.1"],
        "topics_touched": ["Payment Terms"],
        "summary_of_the_change": "Extended payment deadline from 15 to 30 days."
    }
    obj = ContractChange.model_validate(data)
    assert obj.sections_changed == ["Section 5.1"]
    assert len(obj.summary_of_the_change) >= 20

def test_invalid_empty_sections():
    with pytest.raises(ValueError):
        ContractChange.model_validate({
            "sections_changed": [],
            "topics_touched": ["A"],
            "summary_of_the_change": "x" * 30
        })

def test_invalid_short_summary():
    with pytest.raises(ValueError):
        ContractChange.model_validate({
            "sections_changed": ["A"],
            "topics_touched": ["B"],
            "summary_of_the_change": "too short"
        })