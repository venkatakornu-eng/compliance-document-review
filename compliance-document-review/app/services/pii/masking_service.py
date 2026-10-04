import uuid
from typing import Optional

from app.core.logging_config import logger
from app.models.pii import MaskingResult
from app.services.pii.detector import PIIDetector
from app.services.pii.mapper import build_token_mapping
from app.storage.mapping_store import mapping_store


class PIIMaskingService:

    def __init__(
        self,
        detector: Optional[PIIDetector] = None,
    ):

        self.detector = (
            detector
            if detector is not None
            else PIIDetector()
        )

    def mask(
        self,
        text: str,
        document_id: Optional[str] = None,
    ) -> MaskingResult:

        if document_id is None:
            document_id = str(
                uuid.uuid4()
            )

        entities = self.detector.detect(
            text
        )

        value_to_token, token_to_value = (
            build_token_mapping(
                entities
            )
        )

        masked_text = text

        # Replace from right to left so offsets
        # do not become invalid.
        entities_desc = sorted(
            entities,
            key=lambda entity: entity.start,
            reverse=True,
        )

        for entity in entities_desc:

            mapping_key = (
                f"{entity.entity_type}:"
                f"{entity.original_text.strip().lower()}"
            )

            token = value_to_token[
                mapping_key
            ]

            masked_text = (
                masked_text[:entity.start]
                + token
                + masked_text[entity.end:]
            )

        mapping_store.save(
            document_id=document_id,
            mapping=token_to_value,
        )

        logger.info(
            "PII masking completed | "
            "document_id=%s | entities=%s",
            document_id,
            len(entities),
        )

        return MaskingResult(
            document_id=document_id,
            masked_text=masked_text,
            entity_count=len(entities),
            tokens=list(
                token_to_value.keys()
            ),
        )


pii_masking_service = PIIMaskingService()