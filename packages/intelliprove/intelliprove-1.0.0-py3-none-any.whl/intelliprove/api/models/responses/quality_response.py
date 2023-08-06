from typing import Optional
from dataclasses import dataclass
from intelliprove.api.models.enums import QualityErrorType
from intelliprove.api.models.dataclasses import Quality


@dataclass
class QualityResponse:
    score: int
    error_type: QualityErrorType
    message: str
    signature: Optional[str] = None

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            score=data['quality_score'],
            error_type=QualityErrorType(data['quality_error_code']),
            message=data['prompt'],
            signature=data['signature']
        )

    def to_dataclass(self):
        return Quality(**self.__dict__)