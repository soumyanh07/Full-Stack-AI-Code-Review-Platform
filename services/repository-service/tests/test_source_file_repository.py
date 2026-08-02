from app.repositories.source_file_repository import SourceFileRepository


class DummyDB:
    def __init__(self):
        self.added = []

    def add(self, obj):
        self.added.append(obj)

    def commit(self):
        return None

    def refresh(self, obj):
        return None


def test_create_file_alias_works_for_legacy_calls():
    db = DummyDB()
    repository = SourceFileRepository(db)

    source_file = repository.create_file(
        repository_id=1,
        file_path="app/main.py",
        language="py",
        content="print('hi')",
        metadata={"parsed": True},
    )

    assert source_file.repository_id == 1
    assert source_file.path == "app/main.py"
    assert source_file.language == "py"
    assert source_file.content == "print('hi')"
    assert source_file.metadata == {"parsed": True}
