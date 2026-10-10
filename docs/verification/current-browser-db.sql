-- Read-only checks on synthetic records, guarded ppm_test browser database.
WITH imported AS (SELECT id, organization_id FROM ppm_projects WHERE name='Sprint 08 import project' ORDER BY created_at DESC LIMIT 1), created AS (SELECT id,organization_id,archived FROM ppm_projects WHERE name='Browser project' ORDER BY created_at DESC LIMIT 1)
SELECT 'import_project='||(SELECT count(*)=1 FROM imported)::text,
'imported_work='||(SELECT count(*)=1 FROM ppm_work_items w JOIN imported p ON p.id=w.project_id WHERE w.name='Imported release work' AND w.status='backlog')::text,
'provenance='||(SELECT count(*)=1 FROM ingestion_sources s JOIN imported p ON p.id=s.project_id JOIN ppm_work_items w ON w.id=s.work_item_id WHERE w.name='Imported release work' AND s.external_id='1' AND s.source_updated_at='2026-10-09T00:00:00Z')::text,
'partial_jobs='||(SELECT count(*)=2 FROM durable_jobs j JOIN job_integrations i ON i.id=j.integration_id JOIN imported p ON p.id=i.project_id WHERE j.status='partially_succeeded' AND j.accepted=1 AND jsonb_array_length(j.errors)=1)::text,
'rejected_connection_absent='||(SELECT count(*)=0 FROM job_integrations i JOIN imported p ON p.id=i.project_id WHERE i.config->>'name'='Invalid overlapping mapping')::text,
'ui_project_archived='||(SELECT count(*)=1 AND bool_and(archived) FROM created)::text,
'ui_work_persisted='||(SELECT count(*)=1 FROM ppm_work_items w JOIN created p ON p.id=w.project_id WHERE w.name='Browser work')::text;
