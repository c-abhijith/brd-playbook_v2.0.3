/* =====================================================================================
   SQL SERVER METADATA EXTRACTION — READ-ONLY
   For the BRD Reconstruction Playbook (memory step M2: technical map).

   HOW TO RUN (see README.md for detail)
   - Run against PRODUCTION (or a current production copy). Use a read-only login.
   - Run queries Q1–Q8 once per user database:  USE [YourDatabase];  then run them.
   - Run Q9–Q11 once per server (they read msdb / server-level views).
   - Results to Grid → right-click the grid → "Save Results As…" → CSV,
     named as shown in each query header, e.g. sqlserver_<database>_Q1_objects.csv.
   - Every statement here is SELECT only. Nothing is created, changed or deleted.

   Line breaks inside code are replaced with the marker  \n  so each row stays on one
   line in the CSV; the agent restores them when reading.
   ===================================================================================== */


/* ---------- Q1  Objects inventory  →  sqlserver_<database>_Q1_objects.csv ----------
   Every table, view, procedure, function, trigger and synonym, with created/modified dates. */
SELECT  DB_NAME()            AS database_name,
        s.name               AS schema_name,
        o.name               AS object_name,
        o.type               AS object_type_code,
        o.type_desc          AS object_type,
        o.create_date,
        o.modify_date
FROM    sys.objects o
JOIN    sys.schemas s ON s.schema_id = o.schema_id
WHERE   o.is_ms_shipped = 0
  AND   o.type IN ('U','V','P','PC','FN','IF','TF','FS','FT','TR','SN')
ORDER BY s.name, o.type_desc, o.name;


/* ---------- Q2  Columns  →  sqlserver_<database>_Q2_columns.csv ----------
   Every column of every table and view, with type, nullability, identity and computed flags. */
SELECT  DB_NAME()            AS database_name,
        s.name               AS schema_name,
        o.name               AS object_name,
        o.type_desc          AS object_type,
        c.column_id,
        c.name               AS column_name,
        ty.name              AS data_type,
        c.max_length,
        c.precision,
        c.scale,
        c.is_nullable,
        c.is_identity,
        c.is_computed
FROM    sys.columns c
JOIN    sys.objects o  ON o.object_id = c.object_id
JOIN    sys.schemas s  ON s.schema_id = o.schema_id
JOIN    sys.types  ty  ON ty.user_type_id = c.user_type_id
WHERE   o.is_ms_shipped = 0
  AND   o.type IN ('U','V')
ORDER BY s.name, o.name, c.column_id;


/* ---------- Q3a  Primary keys and unique keys  →  sqlserver_<database>_Q3a_keys.csv ---------- */
SELECT  DB_NAME()            AS database_name,
        s.name               AS schema_name,
        t.name               AS table_name,
        i.name               AS key_name,
        CASE WHEN i.is_primary_key = 1 THEN 'PRIMARY KEY'
             WHEN i.is_unique_constraint = 1 THEN 'UNIQUE CONSTRAINT'
             ELSE 'UNIQUE INDEX' END AS key_type,
        ic.key_ordinal,
        c.name               AS column_name
FROM    sys.indexes i
JOIN    sys.tables  t  ON t.object_id = i.object_id
JOIN    sys.schemas s  ON s.schema_id = t.schema_id
JOIN    sys.index_columns ic ON ic.object_id = i.object_id AND ic.index_id = i.index_id
JOIN    sys.columns c  ON c.object_id = ic.object_id AND c.column_id = ic.column_id
WHERE   (i.is_primary_key = 1 OR i.is_unique = 1)
  AND   ic.is_included_column = 0
  AND   t.is_ms_shipped = 0
ORDER BY s.name, t.name, i.name, ic.key_ordinal;


/* ---------- Q3b  Foreign keys  →  sqlserver_<database>_Q3b_foreign_keys.csv ---------- */
SELECT  DB_NAME()                        AS database_name,
        fk.name                          AS foreign_key_name,
        SCHEMA_NAME(pt.schema_id)        AS parent_schema,
        pt.name                          AS parent_table,
        pc.name                          AS parent_column,
        SCHEMA_NAME(rt.schema_id)        AS referenced_schema,
        rt.name                          AS referenced_table,
        rc.name                          AS referenced_column,
        fk.is_disabled
FROM    sys.foreign_keys fk
JOIN    sys.foreign_key_columns fkc ON fkc.constraint_object_id = fk.object_id
JOIN    sys.tables  pt ON pt.object_id = fkc.parent_object_id
JOIN    sys.columns pc ON pc.object_id = fkc.parent_object_id AND pc.column_id = fkc.parent_column_id
JOIN    sys.tables  rt ON rt.object_id = fkc.referenced_object_id
JOIN    sys.columns rc ON rc.object_id = fkc.referenced_object_id AND rc.column_id = fkc.referenced_column_id
ORDER BY parent_schema, parent_table, fk.name;


/* ---------- Q4  Code of procedures, views, functions, triggers  →  sqlserver_<database>_Q4_definitions.csv ----------
   Long code is split into numbered 4000-character pieces so nothing is cut off by SSMS.
   The agent joins the pieces back together by object and chunk_no. */
WITH defs AS (
    SELECT  s.name AS schema_name, o.name AS object_name, o.type_desc AS object_type,
            m.definition, DATALENGTH(m.definition) / 2 AS def_len
    FROM    sys.sql_modules m
    JOIN    sys.objects o ON o.object_id = m.object_id
    JOIN    sys.schemas s ON s.schema_id = o.schema_id
    WHERE   o.is_ms_shipped = 0
),
nums AS (   -- 0..9999 → supports code up to 40 million characters per object
    SELECT TOP (10000) ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) - 1 AS k
    FROM sys.all_objects a CROSS JOIN sys.all_objects b
)
SELECT  DB_NAME()                               AS database_name,
        d.schema_name,
        d.object_name,
        d.object_type,
        n.k + 1                                 AS chunk_no,
        CEILING(d.def_len / 4000.0)             AS chunks_total,
        REPLACE(REPLACE(REPLACE(
            SUBSTRING(d.definition, n.k * 4000 + 1, 4000),
            CHAR(13), ''), CHAR(10), ' \n '), CHAR(9), '    ') AS definition_chunk
FROM    defs d
JOIN    nums n ON n.k * 4000 < d.def_len
ORDER BY d.schema_name, d.object_name, chunk_no;
/* Encrypted objects (WITH ENCRYPTION) return no code; Q1 still lists them. */


/* ---------- Q5  Static dependencies  →  sqlserver_<database>_Q5_dependencies.csv ----------
   Which object refers to which (procedure → table, view → table, procedure → procedure).
   Limits: does not say read vs write, and misses dynamic SQL (EXEC of a built string).
   The agent fills those gaps by reading the code from Q4. */
SELECT  DB_NAME()                                  AS database_name,
        OBJECT_SCHEMA_NAME(d.referencing_id)       AS referencing_schema,
        OBJECT_NAME(d.referencing_id)              AS referencing_object,
        o.type_desc                                AS referencing_type,
        d.referenced_server_name,
        d.referenced_database_name,
        d.referenced_schema_name,
        d.referenced_entity_name,
        d.is_caller_dependent,
        d.is_ambiguous
FROM    sys.sql_expression_dependencies d
JOIN    sys.objects o ON o.object_id = d.referencing_id
WHERE   o.is_ms_shipped = 0
ORDER BY referencing_schema, referencing_object, d.referenced_entity_name;


/* ---------- Q6  Procedure usage since the last restart  →  sqlserver_<database>_Q6_proc_usage.csv ----------
   Needs VIEW SERVER STATE (SQL Server 2022: VIEW SERVER PERFORMANCE STATE).
   Based on the plan cache: a procedure missing here is not proof it is unused. */
SELECT  DB_NAME()                                           AS database_name,
        OBJECT_SCHEMA_NAME(ps.object_id, ps.database_id)    AS schema_name,
        OBJECT_NAME(ps.object_id, ps.database_id)           AS procedure_name,
        ps.execution_count,
        ps.last_execution_time,
        ps.cached_time,
        (SELECT sqlserver_start_time FROM sys.dm_os_sys_info) AS server_start_time
FROM    sys.dm_exec_procedure_stats ps
WHERE   ps.database_id = DB_ID()
ORDER BY ps.last_execution_time DESC;


/* ---------- Q7  Table read/write activity since the last restart  →  sqlserver_<database>_Q7_table_usage.csv ----------
   Needs VIEW SERVER STATE. Resets on restart; absence is not proof a table is unused. */
SELECT  DB_NAME()                                  AS database_name,
        OBJECT_SCHEMA_NAME(u.object_id)            AS schema_name,
        OBJECT_NAME(u.object_id)                   AS table_name,
        SUM(u.user_seeks + u.user_scans + u.user_lookups) AS reads,
        SUM(u.user_updates)                        AS writes,
        MAX(u.last_user_seek)                      AS last_seek,
        MAX(u.last_user_scan)                      AS last_scan,
        MAX(u.last_user_lookup)                    AS last_lookup,
        MAX(u.last_user_update)                    AS last_write,
        (SELECT sqlserver_start_time FROM sys.dm_os_sys_info) AS server_start_time
FROM    sys.dm_db_index_usage_stats u
WHERE   u.database_id = DB_ID()
  AND   OBJECTPROPERTY(u.object_id, 'IsUserTable') = 1
GROUP BY u.object_id
ORDER BY schema_name, table_name;


/* ---------- Q8  Row counts and size  →  sqlserver_<database>_Q8_row_counts.csv ---------- */
SELECT  DB_NAME()                                  AS database_name,
        s.name                                     AS schema_name,
        t.name                                     AS table_name,
        SUM(CASE WHEN p.index_id IN (0,1) THEN p.row_count ELSE 0 END) AS row_count,
        CAST(SUM(p.reserved_page_count) * 8 / 1024.0 AS DECIMAL(18,1)) AS reserved_mb
FROM    sys.dm_db_partition_stats p
JOIN    sys.tables  t ON t.object_id = p.object_id
JOIN    sys.schemas s ON s.schema_id = t.schema_id
WHERE   t.is_ms_shipped = 0
GROUP BY s.name, t.name
ORDER BY s.name, t.name;


/* =====================================================================================
   SERVER-LEVEL QUERIES — run once per server
   ===================================================================================== */

/* ---------- Q9  SQL Agent jobs, steps and schedules  →  sqlserver_<server>_Q9_agent_jobs.csv ----------
   Needs read access to msdb (e.g. SQLAgentReaderRole). Shows what runs, in what order, how often.
   Long step commands are cut at 4000 characters; the agent asks for the full text if needed. */
SELECT  j.name                    AS job_name,
        j.enabled                 AS job_enabled,
        REPLACE(REPLACE(ISNULL(j.description,''), CHAR(13), ''), CHAR(10), ' \n ') AS job_description,
        c.name                    AS category,
        js.step_id,
        js.step_name,
        js.subsystem,
        js.database_name,
        js.on_success_action,
        js.on_fail_action,
        REPLACE(REPLACE(REPLACE(LEFT(js.command, 4000), CHAR(13), ''), CHAR(10), ' \n '), CHAR(9), '    ') AS step_command,
        sch.name                  AS schedule_name,
        sch.enabled               AS schedule_enabled,
        sch.freq_type,
        sch.freq_interval,
        sch.freq_subday_type,
        sch.freq_subday_interval,
        sch.active_start_time
FROM    msdb.dbo.sysjobs j
JOIN    msdb.dbo.syscategories c      ON c.category_id = j.category_id
LEFT JOIN msdb.dbo.sysjobsteps js     ON js.job_id = j.job_id
LEFT JOIN msdb.dbo.sysjobschedules jsch ON jsch.job_id = j.job_id
LEFT JOIN msdb.dbo.sysschedules sch   ON sch.schedule_id = jsch.schedule_id
ORDER BY j.name, js.step_id;


/* ---------- Q10  Job run history, last 90 days  →  sqlserver_<server>_Q10_job_runs.csv ----------
   Evidence of what actually runs (active / inactive). History may be trimmed by the server's retention setting. */
SELECT  j.name                                                   AS job_name,
        COUNT(*)                                                 AS runs_last_90_days,
        SUM(CASE WHEN h.run_status = 1 THEN 1 ELSE 0 END)        AS succeeded,
        SUM(CASE WHEN h.run_status = 0 THEN 1 ELSE 0 END)        AS failed,
        MIN(msdb.dbo.agent_datetime(h.run_date, h.run_time))     AS first_run_in_window,
        MAX(msdb.dbo.agent_datetime(h.run_date, h.run_time))     AS last_run
FROM    msdb.dbo.sysjobhistory h
JOIN    msdb.dbo.sysjobs j ON j.job_id = h.job_id
WHERE   h.step_id = 0
  AND   h.run_date >= CONVERT(INT, CONVERT(CHAR(8), DATEADD(DAY, -90, GETDATE()), 112))
GROUP BY j.name
ORDER BY last_run DESC;


/* ---------- Q11  Linked servers and synonyms (upstream / downstream hints)  →  sqlserver_<server>_Q11_links.csv ----------
   Names only; no credentials are returned. Run the synonym part per database if synonyms are used. */
SELECT  'LINKED SERVER'     AS item_type,
        s.name              AS item_name,
        s.product,
        s.provider,
        s.data_source       AS points_to
FROM    sys.servers s
WHERE   s.is_linked = 1
UNION ALL
SELECT  'SYNONYM in ' + DB_NAME(),
        SCHEMA_NAME(sn.schema_id) + '.' + sn.name,
        NULL, NULL,
        sn.base_object_name
FROM    sys.synonyms sn;
