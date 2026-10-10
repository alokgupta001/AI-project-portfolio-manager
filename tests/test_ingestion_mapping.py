"""Mapping validation must prevent projection crashes and preserve nested fields."""

from uuid import uuid4

import pytest
from ppm_api.ingestion import ConnectorConfig, project_rows


@pytest.mark.parametrize("paths", [("id", "id.title"), ("id.title", "id")])
def test_mapping_rejects_scalar_parent_of_another_field(paths):
    with pytest.raises(ValueError, match="overlap"):
        ConnectorConfig(
            name="Invalid mapping",
            provider="csv",
            project_id=uuid4(),
            mapping={
                "external_id": paths[0],
                "name": paths[1],
                "source_updated_at": "updated_at",
            },
        )


def test_mapping_preserves_nested_siblings_and_discards_private_fields():
    config = ConnectorConfig(
        name="Jira mapping",
        provider="jira",
        resource="example.atlassian.net",
        project_id=uuid4(),
        mapping={
            "external_id": "id",
            "name": "fields.summary",
            "source_updated_at": "fields.updated",
        },
    )
    assert project_rows(
        config,
        [{"id": "1", "fields": {"summary": "Work", "updated": "stamp", "private": "notes"}}],
    ) == [{"id": "1", "fields": {"summary": "Work", "updated": "stamp"}}]
