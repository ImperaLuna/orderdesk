from app.core.ids import new_principal_id, new_record_id


def test_principal_ids_are_v4() -> None:
    assert new_principal_id().version == 4


def test_record_ids_are_v7() -> None:
    assert new_record_id().version == 7
