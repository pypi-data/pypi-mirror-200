from uuid import uuid4

from ..examination import Examination


def test_examination_supports_service_creator_type():
    Examination(
        id=str(uuid4()),
        case_id=str(uuid4()),
        creator_id=str(uuid4()),
        creator_type="SERVICE",
        state="OPEN",
        created_at=0,
        updated_at=0,
        app_id=str(uuid4()),
        jobs=[],
    )
