-- =====================================================================================
-- DATABRICKS METADATA EXTRACTION — READ-ONLY (Databricks SQL / Unity Catalog)
-- For the BRD Reconstruction Playbook (memory step M2: technical map).
--
-- HOW TO RUN (see README.md for detail)
-- - Run in a Databricks SQL editor or notebook, on a SQL warehouse, as a read-only user.
-- - Replace <catalog> with the catalog(s) in scope (repeat or use IN ('a','b')).
-- - Download each result as CSV, named as shown in each query header,
--   e.g. databricks_D1_tables.csv. The editor's download quotes text correctly.
-- - Queries D6–D10 use system tables (system.access, system.lakeflow). An admin must have
--   enabled those schemas and granted SELECT. If one fails with "not found / no access",
--   skip it and note that in the README checklist.
-- - Every statement here is SELECT only. Nothing is created, changed or deleted.
-- =====================================================================================


-- ---------- D1  Tables and views  →  databricks_D1_tables.csv ----------
SELECT  table_catalog, table_schema, table_name, table_type, data_source_format,
        table_owner, comment, created, created_by, last_altered, last_altered_by
FROM    system.information_schema.tables
WHERE   table_catalog IN ('<catalog>')
  AND   table_schema <> 'information_schema'
ORDER BY table_catalog, table_schema, table_name;


-- ---------- D2  Columns  →  databricks_D2_columns.csv ----------
SELECT  table_catalog, table_schema, table_name, ordinal_position, column_name,
        full_data_type, is_nullable, comment
FROM    system.information_schema.columns
WHERE   table_catalog IN ('<catalog>')
  AND   table_schema <> 'information_schema'
ORDER BY table_catalog, table_schema, table_name, ordinal_position;


-- ---------- D3  View definitions  →  databricks_D3_views.csv ----------
SELECT  table_catalog, table_schema, table_name, view_definition
FROM    system.information_schema.views
WHERE   table_catalog IN ('<catalog>')
  AND   table_schema <> 'information_schema'
ORDER BY table_catalog, table_schema, table_name;


-- ---------- D4  Functions and procedures (if used)  →  databricks_D4_routines.csv ----------
SELECT  specific_catalog, specific_schema, routine_name, routine_type, data_type,
        routine_body, external_language, routine_definition, created, last_altered
FROM    system.information_schema.routines
WHERE   specific_catalog IN ('<catalog>')
  AND   specific_schema <> 'information_schema'
ORDER BY specific_catalog, specific_schema, routine_name;


-- ---------- D5  Declared keys (primary / foreign, informational in Unity Catalog)  →  databricks_D5_keys.csv ----------
SELECT  tc.table_catalog, tc.table_schema, tc.table_name, tc.constraint_name, tc.constraint_type,
        kcu.column_name, kcu.ordinal_position
FROM    system.information_schema.table_constraints tc
JOIN    system.information_schema.key_column_usage kcu
          ON  kcu.constraint_catalog = tc.constraint_catalog
          AND kcu.constraint_schema  = tc.constraint_schema
          AND kcu.constraint_name    = tc.constraint_name
WHERE   tc.table_catalog IN ('<catalog>')
ORDER BY tc.table_catalog, tc.table_schema, tc.table_name, tc.constraint_name, kcu.ordinal_position;


-- ---------- D6  Table lineage, last 90 days  →  databricks_D6_table_lineage.csv ----------
-- Which job, notebook or pipeline read which table and wrote which table, and when last seen.
-- This is the strongest evidence of what is actually running (active / inactive).
SELECT  source_table_full_name,
        target_table_full_name,
        entity_type,
        entity_id,
        COUNT(*)          AS events_last_90_days,
        MIN(event_time)   AS first_seen,
        MAX(event_time)   AS last_seen
FROM    system.access.table_lineage
WHERE   event_time >= current_date() - INTERVAL 90 DAYS
  AND  (source_table_full_name LIKE '<catalog>.%' OR target_table_full_name LIKE '<catalog>.%')
GROUP BY source_table_full_name, target_table_full_name, entity_type, entity_id
ORDER BY last_seen DESC;


-- ---------- D7  Column lineage, last 90 days (optional; can be large)  →  databricks_D7_column_lineage.csv ----------
SELECT  source_table_full_name, source_column_name,
        target_table_full_name, target_column_name,
        MAX(event_time) AS last_seen
FROM    system.access.column_lineage
WHERE   event_time >= current_date() - INTERVAL 90 DAYS
  AND   target_table_full_name LIKE '<catalog>.%'
GROUP BY source_table_full_name, source_column_name, target_table_full_name, target_column_name
ORDER BY target_table_full_name, target_column_name;


-- ---------- D8  Jobs (current definition)  →  databricks_D8_jobs.csv ----------
SELECT  workspace_id, job_id, name, description, creator_id, run_as, change_time
FROM    system.lakeflow.jobs
QUALIFY ROW_NUMBER() OVER (PARTITION BY workspace_id, job_id ORDER BY change_time DESC) = 1
    AND delete_time IS NULL
ORDER BY name;


-- ---------- D9  Job tasks and their order  →  databricks_D9_job_tasks.csv ----------
SELECT  workspace_id, job_id, task_key, depends_on_keys, change_time
FROM    system.lakeflow.job_tasks
QUALIFY ROW_NUMBER() OVER (PARTITION BY workspace_id, job_id, task_key ORDER BY change_time DESC) = 1
    AND delete_time IS NULL
ORDER BY job_id, task_key;


-- ---------- D10  Job runs, last 90 days  →  databricks_D10_job_runs.csv ----------
SELECT  workspace_id, job_id,
        COUNT(DISTINCT run_id)                                         AS runs_last_90_days,
        COUNT(DISTINCT CASE WHEN result_state = 'FAILED' THEN run_id END) AS failed_runs,
        MAX(period_end_time)                                           AS last_run
FROM    system.lakeflow.job_run_timeline
WHERE   period_start_time >= current_date() - INTERVAL 90 DAYS
GROUP BY workspace_id, job_id
ORDER BY last_run DESC;


-- ---------- D11  Your own metadata tables (if procedure text etc. is stored in custom tables) ----------
-- If the team keeps stored-procedure text, mappings or descriptions in their own tables,
-- export those too, for example:
--   SELECT * FROM <catalog>.<schema>.<metadata_table>;
-- → databricks_D11_<metadata_table>.csv
-- Do NOT export business data rows; metadata only.
