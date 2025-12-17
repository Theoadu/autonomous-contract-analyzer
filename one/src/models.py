from pydantic import BaseModel, Field, field_validator
from typing import List

class ContractChange(BaseModel):
    sections_changed: List[str] = Field(
        ...,
        min_length=1,
        description="Specific section identifiers (e.g., 'Section 4.2', 'Exhibit A')"
    )
    topics_touched: List[str] = Field(
        ...,
        min_length=1,
        description="Legal or business topics affected (e.g., 'Liability', 'Payment Terms')"
    )
    summary_of_the_change: str = Field(
        ...,
        min_length=20,
        description="Precise summary of additions, deletions, or modifications"
    )

    @field_validator("sections_changed", "topics_touched")
    @classmethod
    def validate_non_empty_strings(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("List must not be empty")
        cleaned = [s.strip() for s in v]
        if any(s == "" for s in cleaned):
            raise ValueError("Items must be non-empty strings")
        return cleaned