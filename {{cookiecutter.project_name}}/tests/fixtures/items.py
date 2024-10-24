import uuid
from datetime import datetime
from collections.abc import AsyncGenerator

import pytest
from tests.data import mock_data
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.documents.dto_models import DocumentDTO, DocumentTypeDTO
from src.service.postgres.models.documents import Document, DocumentType


@pytest.fixture
async def seed_doc_type(db_session: AsyncSession) -> AsyncGenerator[DocumentTypeDTO, None]:
    _id = 1
    name = "Test document type"
    doc_type_data = DocumentTypeDTO(id=_id, name=name)
    db_session.add(DocumentType(**doc_type_data.model_dump()))
    yield doc_type_data


@pytest.fixture
async def seed_doc(seed_doc_type: DocumentTypeDTO, db_session: AsyncSession) -> AsyncGenerator[DocumentDTO, None]:
    doc_id = uuid.uuid4()
    document_data = DocumentDTO(
        id=doc_id,
        s3key=str(doc_id),
        employee_id=uuid.UUID(mock_data.employees[0]["id"]),
        uploader_id=uuid.UUID(mock_data.employees[0]["id"]),
        document_type_id=seed_doc_type.id,
        name="Test document",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db_session.add(Document(**document_data.model_dump()))

    yield document_data
