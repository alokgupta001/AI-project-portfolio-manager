# ruff: noqa: E501
"""Durable hybrid tasks and shared zero-spend admission. Normal recovery is forward-only."""

from alembic import op

revision = "0015_agent_task_runtime"
down_revision = "0014_specialist_reviewer"
branch_labels = None
depends_on = None

DDL = [
    "\nCREATE TABLE agent_tasks (\n\tid UUID NOT NULL, \n\torganization_id UUID NOT NULL, \n\trun_id UUID NOT NULL, \n\ttask_key VARCHAR(64) NOT NULL, \n\tagent VARCHAR(20) NOT NULL, \n\tkind VARCHAR(16) NOT NULL, \n\tlogical_section_id VARCHAR(64) NOT NULL, \n\tsection_id VARCHAR(64) NOT NULL, \n\tparent_task_id UUID, \n\tdependencies JSONB NOT NULL, \n\tinput_manifest JSONB NOT NULL, \n\tinput_hash VARCHAR(64) NOT NULL, \n\tschema_hash VARCHAR(64) NOT NULL, \n\tprompt_hash VARCHAR(64) NOT NULL, \n\tpolicy_hash VARCHAR(64) NOT NULL, \n\tstate VARCHAR(16) NOT NULL, \n\toutcome VARCHAR(24), \n\trequired BOOLEAN NOT NULL, \n\trevision INTEGER NOT NULL, \n\tattempt_count INTEGER NOT NULL, \n\tnext_attempt_at TIMESTAMP WITH TIME ZONE, \n\tlease_token UUID, \n\tcreated_at TIMESTAMP WITH TIME ZONE NOT NULL, \n\tupdated_at TIMESTAMP WITH TIME ZONE NOT NULL, \n\tdiagnostic VARCHAR(48), \n\tcandidate_payload JSONB, \n\tcandidate_hash VARCHAR(64), \n\tcandidate_attempt_id UUID, \n\tresolved_context_manifest JSONB, \n\tresolved_input_hash VARCHAR(64), \n\tbound_at TIMESTAMP WITH TIME ZONE, \n\tPRIMARY KEY (id), \n\tFOREIGN KEY(organization_id, run_id) REFERENCES ai_runs (organization_id, id), \n\tUNIQUE (organization_id, run_id, id), \n\tUNIQUE (run_id, task_key), \n\tFOREIGN KEY(organization_id, run_id, parent_task_id) REFERENCES agent_tasks (organization_id, run_id, id), \n\tCHECK (revision>0 AND attempt_count BETWEEN 0 AND 2), \n\tCHECK (kind IN ('deterministic','semantic','evaluator','reconcile')), \n\tCHECK (state IN ('WAITING','READY','RUNNING','VALIDATING','RETRY_WAIT','SUCCEEDED','FAILED','BLOCKED','SKIPPED','CANCELLED')), \n\tCHECK (jsonb_array_length(dependencies)<=24 AND octet_length(input_manifest::text)<=90000), \n\tFOREIGN KEY(organization_id) REFERENCES organizations (id), \n\tUNIQUE (organization_id, id)\n)\n\n",
    "CREATE INDEX ix_agent_tasks_due ON agent_tasks (run_id, state, next_attempt_at)",
    "\nCREATE TABLE agent_sections (\n\tid UUID NOT NULL, \n\torganization_id UUID NOT NULL, \n\trun_id UUID NOT NULL, \n\ttask_id UUID NOT NULL, \n\tsection_id VARCHAR(64) NOT NULL, \n\tlogical_section_id VARCHAR(64) NOT NULL, \n\tresult JSONB NOT NULL, \n\tvalidation JSONB NOT NULL, \n\tcontent_sha256 VARCHAR(64) NOT NULL, \n\tschema_version VARCHAR(48) NOT NULL, \n\tcreated_at TIMESTAMP WITH TIME ZONE NOT NULL, \n\tPRIMARY KEY (id), \n\tFOREIGN KEY(organization_id, run_id, task_id) REFERENCES agent_tasks (organization_id, run_id, id), \n\tUNIQUE (task_id, section_id), \n\tCHECK (octet_length(result::text)<=64000 AND octet_length(validation::text)<=64000), \n\tFOREIGN KEY(organization_id) REFERENCES organizations (id), \n\tUNIQUE (organization_id, id)\n)\n\n",
    "CREATE INDEX ix_agent_sections_run ON agent_sections (organization_id, run_id)",
    "\nCREATE TABLE ai_provider_scopes (\n\tid VARCHAR(160) NOT NULL, \n\tprovider_id VARCHAR(32) NOT NULL, \n\tpolicy_hash VARCHAR(64) NOT NULL, \n\tbilling_class VARCHAR(24) NOT NULL, \n\tenabled BOOLEAN NOT NULL, \n\tallowed_tenants JSONB NOT NULL, \n\tallowed_models JSONB NOT NULL, \n\tconcurrency_slots INTEGER NOT NULL, \n\trequests_per_minute INTEGER NOT NULL, \n\trequests_per_day INTEGER NOT NULL, \n\ttenant_requests_per_day INTEGER NOT NULL, \n\ttokens_per_minute INTEGER NOT NULL, \n\tcircuit_until TIMESTAMP WITH TIME ZONE, \n\tfailure_count INTEGER NOT NULL, \n\tdisabled_reason VARCHAR(48), \n\tquarantined_attempt_id UUID, \n\tquarantine_reason VARCHAR(48), \n\trevision INTEGER NOT NULL, \n\tPRIMARY KEY (id), \n\tCHECK (concurrency_slots BETWEEN 1 AND 4 AND requests_per_minute>0 AND requests_per_day>0 AND tokens_per_minute>0 AND revision>0)\n)\n\n",
    "\nCREATE TABLE ai_quota_reservations (\n\tattempt_id UUID NOT NULL, \n\torganization_id UUID NOT NULL, \n\trun_id UUID NOT NULL, \n\ttask_id UUID NOT NULL, \n\tquota_scope_id VARCHAR(160) NOT NULL, \n\tadmitted_at TIMESTAMP WITH TIME ZONE NOT NULL, \n\twindow_expires_at TIMESTAMP WITH TIME ZONE NOT NULL, \n\tslot_expires_at TIMESTAMP WITH TIME ZONE NOT NULL, \n\trequest_count INTEGER NOT NULL, \n\treserved_input INTEGER NOT NULL, \n\treserved_output INTEGER NOT NULL, \n\treported_input INTEGER, \n\treported_output INTEGER, \n\toutcome VARCHAR(16) NOT NULL, \n\tPRIMARY KEY (attempt_id), \n\tFOREIGN KEY(organization_id, run_id, task_id) REFERENCES agent_tasks (organization_id, run_id, id), \n\tFOREIGN KEY(quota_scope_id) REFERENCES ai_provider_scopes (id)\n)\n\n",
    "CREATE INDEX ix_model_quota_slots ON ai_quota_reservations (quota_scope_id, slot_expires_at)",
    "CREATE INDEX ix_model_quota_time ON ai_quota_reservations (quota_scope_id, admitted_at)",
    "ALTER TABLE ai_calls ADD COLUMN task_id UUID",
    "ALTER TABLE ai_calls ADD COLUMN attempt_id UUID",
    "ALTER TABLE ai_calls ADD COLUMN run_attempt_no INTEGER",
    "ALTER TABLE ai_calls ADD COLUMN provider_id VARCHAR(32)",
    "ALTER TABLE ai_calls ADD COLUMN model_id VARCHAR(160)",
    "ALTER TABLE ai_calls ADD COLUMN quota_scope_hash VARCHAR(64)",
    "ALTER TABLE ai_calls ADD COLUMN policy_hash VARCHAR(64)",
    "ALTER TABLE ai_calls ADD COLUMN request_hash VARCHAR(64)",
    "ALTER TABLE ai_calls ADD COLUMN started_at TIMESTAMP WITH TIME ZONE",
    "ALTER TABLE ai_calls ADD COLUMN completed_at TIMESTAMP WITH TIME ZONE",
    "ALTER TABLE ai_calls ADD COLUMN finish_category VARCHAR(32)",
    "ALTER TABLE ai_calls ADD COLUMN native_reason VARCHAR(48)",
    "ALTER TABLE ai_calls ADD COLUMN usage_source VARCHAR(16)",
    "ALTER TABLE ai_calls ADD COLUMN reserved_input_tokens INTEGER",
    "ALTER TABLE ai_calls ADD COLUMN reserved_output_tokens INTEGER",
    "ALTER TABLE ai_calls ADD COLUMN reasoning_tokens INTEGER",
    "ALTER TABLE ai_calls ADD COLUMN provider_request_id VARCHAR(160)",
    "ALTER TABLE ai_calls ADD COLUMN send_state VARCHAR(16)",
    "ALTER TABLE ai_calls ADD COLUMN response_hash VARCHAR(64)",
    "ALTER TABLE ai_calls ADD CONSTRAINT uq_ai_run_attempt_no UNIQUE (run_id, run_attempt_no)",
    "ALTER TABLE ai_calls ADD CONSTRAINT ck_ai_attempt CHECK (run_attempt_no IS NULL OR run_attempt_no BETWEEN 1 AND 4)",
    "ALTER TABLE ai_calls ADD CONSTRAINT fk_ai_call_task FOREIGN KEY(organization_id, run_id, task_id) REFERENCES agent_tasks (organization_id, run_id, id)",
    "ALTER TABLE ai_calls ADD CONSTRAINT uq_ai_call_attempt_id UNIQUE (attempt_id)",
]

OID = "NULLIF(current_setting('ppm.organization_id',true),'')::uuid"
UID = "NULLIF(current_setting('ppm.user_id',true),'')::uuid"


def upgrade():
    for statement in DDL:
        op.execute(statement)
    for name in ("agent_tasks", "agent_sections"):
        op.execute(f"ALTER TABLE {name} ENABLE ROW LEVEL SECURITY")
        read = f"organization_id={OID} AND EXISTS (SELECT 1 FROM agent_analyses a WHERE a.run_id={name}.run_id)"
        write = f"organization_id={OID} AND current_setting('ppm.role',true)='Admin' AND EXISTS (SELECT 1 FROM ai_runs r WHERE r.id={name}.run_id AND r.organization_id={name}.organization_id AND r.actor_id={UID} AND NOT r.settled AND r.versions->>'runtime_version'='v2')"
        op.execute(f"CREATE POLICY task_read ON {name} FOR SELECT TO ppm_app USING ({read})")
        op.execute(
            f"CREATE POLICY task_insert ON {name} FOR INSERT TO ppm_app WITH CHECK ({write})"
        )
        op.execute(f"GRANT SELECT,INSERT ON {name} TO ppm_app")
        if name == "agent_tasks":
            op.execute(
                f"CREATE POLICY task_update ON {name} FOR UPDATE TO ppm_app USING ({write}) WITH CHECK ({write})"
            )
            op.execute(f"GRANT UPDATE ON {name} TO ppm_app")
    op.execute("REVOKE ALL ON ai_provider_scopes,ai_quota_reservations FROM PUBLIC,ppm_app")
    op.execute("""CREATE FUNCTION public.ppm_task_guard() RETURNS trigger
      LANGUAGE plpgsql SET search_path=pg_catalog,public AS $$ BEGIN
      IF TG_OP='DELETE' OR (TG_TABLE_NAME='agent_sections' AND TG_OP='UPDATE') THEN
        RAISE check_violation USING MESSAGE='Hybrid history is immutable'; END IF;
      IF TG_TABLE_NAME='agent_sections' THEN
        IF NOT EXISTS(SELECT 1 FROM public.agent_tasks t WHERE t.id=NEW.task_id
          AND t.organization_id=NEW.organization_id AND t.run_id=NEW.run_id
          AND t.section_id=NEW.section_id AND t.state='VALIDATING') THEN
          RAISE check_violation USING MESSAGE='Section parent mismatch'; END IF;
        RETURN NEW;
      END IF;
      IF NEW.agent NOT IN ('financial','schedule','sentiment','risk','resource','governance','agile_coach','pmo','executive')
        OR octet_length(NEW.candidate_payload::text)>16000 OR octet_length(NEW.resolved_context_manifest::text)>90000 THEN
        RAISE check_violation USING MESSAGE='Hybrid task bounds'; END IF;
      IF TG_OP='INSERT' THEN
        IF (SELECT count(*) FROM public.agent_tasks WHERE run_id=NEW.run_id)>=24
          OR EXISTS(SELECT 1 FROM jsonb_array_elements_text(NEW.dependencies) dep
            WHERE NOT EXISTS(SELECT 1 FROM public.agent_tasks t WHERE t.id::text=dep
              AND t.run_id=NEW.run_id AND t.organization_id=NEW.organization_id)) THEN
          RAISE check_violation USING MESSAGE='Invalid task dependencies'; END IF;
      ELSE
        IF (NEW.id,NEW.organization_id,NEW.run_id,NEW.task_key,NEW.agent,NEW.kind,NEW.logical_section_id,
            NEW.section_id,NEW.parent_task_id,NEW.dependencies,NEW.input_manifest,NEW.input_hash,
            NEW.schema_hash,NEW.prompt_hash,NEW.policy_hash,NEW.required,NEW.created_at)
           IS DISTINCT FROM
           (OLD.id,OLD.organization_id,OLD.run_id,OLD.task_key,OLD.agent,OLD.kind,OLD.logical_section_id,
            OLD.section_id,OLD.parent_task_id,OLD.dependencies,OLD.input_manifest,OLD.input_hash,
            OLD.schema_hash,OLD.prompt_hash,OLD.policy_hash,OLD.required,OLD.created_at)
          OR NEW.attempt_count<OLD.attempt_count OR NEW.revision<=OLD.revision
          OR OLD.state IN ('SUCCEEDED','FAILED','BLOCKED','SKIPPED','CANCELLED')
          OR (OLD.bound_at IS NOT NULL AND (NEW.resolved_context_manifest,NEW.resolved_input_hash,NEW.bound_at)
              IS DISTINCT FROM (OLD.resolved_context_manifest,OLD.resolved_input_hash,OLD.bound_at)) THEN
          RAISE check_violation USING MESSAGE='Hybrid provenance/state is immutable'; END IF;
        IF NEW.state<>OLD.state AND NEW.state NOT IN ('FAILED','BLOCKED','CANCELLED') AND NOT (
          (OLD.state='WAITING' AND NEW.state IN ('READY','SKIPPED')) OR
          (OLD.state='READY' AND NEW.state='RUNNING') OR
          (OLD.state='RUNNING' AND NEW.state IN ('VALIDATING','RETRY_WAIT','READY')) OR
          (OLD.state='VALIDATING' AND NEW.state IN ('SUCCEEDED','RETRY_WAIT')) OR
          (OLD.state='RETRY_WAIT' AND NEW.state='READY')) THEN
          RAISE check_violation USING MESSAGE='Invalid hybrid transition'; END IF;
      END IF; RETURN NEW; END $$""")
    for name in ("agent_tasks", "agent_sections"):
        op.execute(
            f"CREATE TRIGGER hybrid_guard BEFORE INSERT OR UPDATE OR DELETE ON {name} FOR EACH ROW EXECUTE FUNCTION public.ppm_task_guard()"
        )
    op.execute("""CREATE FUNCTION public.ppm_model_admit(rid uuid,tid uuid,sid text,mid text,
      phash text,lease uuid,aid uuid,input_count integer,output_count integer,timeout_s integer)
      RETURNS jsonb LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,public AS $$
      DECLARE r public.ai_runs; t public.agent_tasks; s public.ai_provider_scopes;
        attempt_no integer; recent integer; daily integer; tenant_daily integer; tokens bigint; active integer;
      BEGIN
        SELECT * INTO r FROM public.ai_runs WHERE id=rid FOR UPDATE;
        IF NOT FOUND OR r.organization_id::text IS DISTINCT FROM current_setting('ppm.organization_id',true)
          OR r.actor_id::text IS DISTINCT FROM current_setting('ppm.user_id',true) OR r.settled
          OR r.versions->>'runtime_version' IS DISTINCT FROM 'v2'
          OR r.deadline<now()+make_interval(secs=>timeout_s+5)
          OR timeout_s NOT BETWEEN 1 AND 22 OR input_count NOT BETWEEN 0 AND 100000
          OR output_count NOT BETWEEN 1 AND 512
          OR NOT EXISTS(SELECT 1 FROM public.identity_sessions i JOIN public.memberships m
            ON m.organization_id=r.organization_id AND m.user_id=r.actor_id
            JOIN public.identity_users u ON u.id=r.actor_id
            WHERE i.id=r.session_id AND NOT i.revoked AND i.expires_at>now()
              AND m.active AND m.role='Admin' AND u.active AND u.verified)
          OR NOT EXISTS(SELECT 1 FROM public.durable_jobs j WHERE j.ai_run_id=rid
            AND j.status='running' AND j.lease_token=lease AND j.lease_until>now() AND NOT j.cancel_requested)
        THEN RETURN jsonb_build_object('code','AUTHORITY_REVOKED'); END IF;
        PERFORM 1 FROM public.ai_budgets WHERE organization_id=r.organization_id FOR UPDATE;
        SELECT * INTO t FROM public.agent_tasks WHERE id=tid AND run_id=rid FOR UPDATE;
        IF NOT FOUND OR t.state NOT IN ('READY','RUNNING') OR t.policy_hash<>phash
          OR t.resolved_input_hash IS NULL THEN RETURN jsonb_build_object('code','CONFIGURATION'); END IF;
        SELECT count(*)+1 INTO attempt_no FROM public.ai_calls WHERE run_id=rid AND operation='agent_v2';
        IF attempt_no>4 OR (SELECT coalesce(sum(attempt_count),0) FROM public.agent_tasks
          WHERE run_id=rid AND logical_section_id=t.logical_section_id)>=2 THEN
          RETURN jsonb_build_object('code','QUOTA_EXHAUSTED'); END IF;
        SELECT * INTO s FROM public.ai_provider_scopes WHERE id=sid FOR UPDATE;
        IF NOT FOUND OR NOT s.enabled OR s.policy_hash<>phash
          OR NOT s.allowed_tenants @> jsonb_build_array(r.organization_id::text)
          OR NOT s.allowed_models @> jsonb_build_array(mid)
          OR s.billing_class NOT IN ('local','verified_free')
          OR s.disabled_reason IS NOT NULL OR s.circuit_until>now() OR s.quarantined_attempt_id IS NOT NULL
          OR (s.provider_id<>'ollama' AND r.versions->>'execution_mode'<>'hybrid') THEN
          RETURN jsonb_build_object('code','SPENDING_NOT_AUTHORIZED'); END IF;
        IF s.provider_id='ollama' THEN
          PERFORM pg_advisory_xact_lock(hashtextextended('ppm:ollama-host',0));
          IF EXISTS(SELECT 1 FROM public.ai_provider_scopes WHERE provider_id='ollama'
              AND quarantined_attempt_id IS NOT NULL)
            OR EXISTS(SELECT 1 FROM public.ai_quota_reservations q
              JOIN public.ai_provider_scopes ps ON ps.id=q.quota_scope_id
              WHERE ps.provider_id='ollama' AND q.outcome IN ('admitted','unknown')) THEN
            RETURN jsonb_build_object('code','LOCAL_RESOURCE'); END IF;
        END IF;
        SELECT count(*) FILTER(WHERE admitted_at>now()-interval '1 minute'),count(*),
          coalesce(sum(greatest(reserved_input,coalesce(reported_input,0))+greatest(reserved_output,coalesce(reported_output,0))) FILTER(WHERE admitted_at>now()-interval '1 minute'),0),
          count(*) FILTER(WHERE slot_expires_at>now() AND outcome IN ('admitted','unknown')),
          count(*) FILTER(WHERE organization_id=r.organization_id)
          INTO recent,daily,tokens,active,tenant_daily FROM public.ai_quota_reservations
          WHERE quota_scope_id=sid AND admitted_at>now()-interval '24 hours';
        IF recent>=s.requests_per_minute OR daily>=s.requests_per_day
          OR tenant_daily>=s.tenant_requests_per_day OR tokens+input_count+output_count>s.tokens_per_minute
          OR active>=s.concurrency_slots THEN RETURN jsonb_build_object('code','QUOTA_EXHAUSTED'); END IF;
        INSERT INTO public.ai_quota_reservations VALUES(aid,r.organization_id,rid,tid,sid,now(),
          now()+interval '24 hours',now()+make_interval(secs=>timeout_s+5),1,input_count,output_count,NULL,NULL,'admitted');
        INSERT INTO public.ai_calls(id,organization_id,run_id,operation,attempt,status,code,charged_usd,
          latency_ms,task_id,attempt_id,run_attempt_no,provider_id,model_id,quota_scope_hash,policy_hash,
          request_hash,started_at,usage_source,reserved_input_tokens,reserved_output_tokens,send_state)
          VALUES(aid,r.organization_id,rid,'agent_v2',attempt_no,'unknown','CALL_OUTCOME_UNKNOWN',0,
          0,tid,aid,attempt_no,s.provider_id,mid,encode(sha256(convert_to(sid,'UTF8')),'hex'),phash,t.resolved_input_hash,now(),'unknown',input_count,output_count,'admitted');
        UPDATE public.agent_tasks SET state='RUNNING',attempt_count=attempt_count+1,revision=revision+1,
          lease_token=lease,updated_at=now() WHERE id=tid;
        RETURN jsonb_build_object('attempt',attempt_no);
      END $$""")
    op.execute(
        "REVOKE ALL ON FUNCTION public.ppm_model_admit(uuid,uuid,text,text,text,uuid,uuid,integer,integer,integer) FROM PUBLIC"
    )
    op.execute(
        "GRANT EXECUTE ON FUNCTION public.ppm_model_admit(uuid,uuid,text,text,text,uuid,uuid,integer,integer,integer) TO ppm_app"
    )
    op.execute("""CREATE FUNCTION public.ppm_model_settle(aid uuid,category text,code text,
      in_tokens integer,out_tokens integer,cooldown integer DEFAULT NULL) RETURNS void LANGUAGE plpgsql SECURITY DEFINER
      SET search_path=pg_catalog,public AS $$ DECLARE q public.ai_quota_reservations; BEGIN
      SELECT * INTO q FROM public.ai_quota_reservations WHERE attempt_id=aid FOR UPDATE;
      IF NOT FOUND OR q.organization_id::text IS DISTINCT FROM current_setting('ppm.organization_id',true)
        OR category NOT IN ('complete','failed','unknown') OR in_tokens<0 OR out_tokens<0
        OR cooldown NOT BETWEEN 1 AND 86400
        OR NOT EXISTS(SELECT 1 FROM public.ai_runs r WHERE r.id=q.run_id AND r.actor_id::text=current_setting('ppm.user_id',true))
        THEN RAISE insufficient_privilege USING MESSAGE='Attempt unavailable'; END IF;
      IF q.outcome<>'admitted' THEN RETURN; END IF;
      UPDATE public.ai_quota_reservations SET outcome=category,reported_input=in_tokens,
        reported_output=out_tokens,slot_expires_at=CASE WHEN category='unknown' THEN slot_expires_at ELSE now() END
        WHERE attempt_id=aid;
      UPDATE public.ai_provider_scopes SET
        quarantined_attempt_id=CASE WHEN category='unknown' AND provider_id='ollama' THEN aid ELSE quarantined_attempt_id END,
        quarantine_reason=CASE WHEN category='unknown' AND provider_id='ollama' THEN 'OUTCOME_UNKNOWN' ELSE quarantine_reason END,
        failure_count=CASE WHEN category='complete' THEN 0 ELSE failure_count+1 END,
        circuit_until=CASE WHEN code IN ('QUOTA_EXHAUSTED','RATE_LIMIT') THEN now()+make_interval(secs=>coalesce(cooldown,60))
          WHEN category<>'complete' AND failure_count>=2 THEN now()+interval '30 seconds' ELSE circuit_until END,
        disabled_reason=CASE WHEN code='AUTHENTICATION' THEN code ELSE disabled_reason END
        WHERE id=q.quota_scope_id;
      END $$""")
    op.execute(
        "REVOKE ALL ON FUNCTION public.ppm_model_settle(uuid,text,text,integer,integer,integer) FROM PUBLIC"
    )
    op.execute(
        "GRANT EXECUTE ON FUNCTION public.ppm_model_settle(uuid,text,text,integer,integer,integer) TO ppm_app"
    )


def downgrade():
    op.execute(
        "DROP FUNCTION IF EXISTS public.ppm_model_settle(uuid,text,text,integer,integer,integer)"
    )
    # Clean the development-only predecessor signature in disposable test DBs.
    # 0015 has never been applied to the normal database.
    op.execute("DROP FUNCTION IF EXISTS public.ppm_model_settle(uuid,text,text,integer,integer)")
    op.execute(
        "DROP FUNCTION public.ppm_model_admit(uuid,uuid,text,text,text,uuid,uuid,integer,integer,integer)"
    )
    op.drop_constraint("fk_ai_call_task", "ai_calls")
    op.drop_constraint("uq_ai_call_attempt_id", "ai_calls")
    op.drop_constraint("uq_ai_run_attempt_no", "ai_calls")
    op.drop_constraint("ck_ai_attempt", "ai_calls")
    for name in (
        "task_id",
        "attempt_id",
        "run_attempt_no",
        "provider_id",
        "model_id",
        "quota_scope_hash",
        "policy_hash",
        "request_hash",
        "started_at",
        "completed_at",
        "finish_category",
        "native_reason",
        "usage_source",
        "reserved_input_tokens",
        "reserved_output_tokens",
        "reasoning_tokens",
        "provider_request_id",
        "send_state",
        "response_hash",
    ):
        op.drop_column("ai_calls", name)
    for name in ("ai_quota_reservations", "ai_provider_scopes", "agent_sections", "agent_tasks"):
        op.drop_table(name)
    op.execute("DROP FUNCTION public.ppm_task_guard()")
