// Generated from backend OpenAPI. Do not edit.
export interface paths {
    "/api/v1/agents/definitions": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Definitions
         * @description List the available typed specialist definitions for the current runtime.
         */
        get: operations["definitions_api_v1_agents_definitions_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/agents/runs": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Listing
         * @description List visible specialist analyses for the requested project and page.
         */
        get: operations["listing_api_v1_agents_runs_get"];
        put?: never;
        /**
         * Create
         * @description Queue an authorized specialist analysis using the existing budget and job controls.
         */
        post: operations["create_api_v1_agents_runs_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/agents/runs/{id_}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Detail
         * @description Return an analysis with evidence filtered through current access checks.
         */
        get: operations["detail_api_v1_agents_runs__id___get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/agents/runs/{id_}/reviews/{item_key}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Review
         * @description Record an authorized suggestion decision with revision and idempotency checks.
         */
        post: operations["review_api_v1_agents_runs__id___reviews__item_key__post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/ai/budget": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /**
         * Configure
         * @description Update the tenant budget within the operator limit using optimistic concurrency.
         */
        patch: operations["configure_api_v1_ai_budget_patch"];
        trace?: never;
    };
    "/api/v1/ai/evaluation": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Evaluation
         * @description Run the deterministic offline evaluation suite for an administrator.
         */
        get: operations["evaluation_api_v1_ai_evaluation_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/ai/operations": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Operations
         * @description Return tenant budget, circuit and provider operations data for an administrator.
         */
        get: operations["operations_api_v1_ai_operations_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/ai/runs": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Listing
         * @description List visible AI runs in a bounded page, optionally scoped to a project.
         */
        get: operations["listing_api_v1_ai_runs_get"];
        put?: never;
        /**
         * Create
         * @description Queue an idempotent authorized run after reserving its budget and frozen inputs.
         */
        post: operations["create_api_v1_ai_runs_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/ai/runs/{id_}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Detail
         * @description Return a run after current tenant, project and private evidence checks.
         */
        get: operations["detail_api_v1_ai_runs__id___get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/ai/runs/{id_}/cancel": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Cancel
         * @description Cancel a visible run with revision checks and settle its remaining reservation.
         */
        post: operations["cancel_api_v1_ai_runs__id___cancel_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/ai/runs/{id_}/diagnostics": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Diagnostics
         * @description Expose sanitized run diagnostics to an authorized administrator.
         */
        get: operations["diagnostics_api_v1_ai_runs__id___diagnostics_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/ai/runs/{id_}/events": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Progress
         * @description Stream bounded run progress while repeatedly checking the caller's authority.
         */
        get: operations["progress_api_v1_ai_runs__id___events_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/ai/runs/{id_}/stages": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Stages
         * @description Return the visible run's ordered durable stage history.
         */
        get: operations["stages_api_v1_ai_runs__id___stages_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/ai/status": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Status
         * @description Return the configured AI provider status without exposing credentials.
         */
        get: operations["status_api_v1_ai_status_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/assessment/access": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Access List */
        get: operations["access_list_api_v1_assessment_access_get"];
        put?: never;
        /** Set Access */
        post: operations["set_access_api_v1_assessment_access_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/assessment/assessments": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List Assessments */
        get: operations["list_assessments_api_v1_assessment_assessments_get"];
        put?: never;
        /** Assign */
        post: operations["assign_api_v1_assessment_assessments_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/assessment/assessments/{assessment_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Detail */
        get: operations["detail_api_v1_assessment_assessments__assessment_id__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/assessment/assessments/{assessment_id}/answers": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        /** Save Answers */
        put: operations["save_answers_api_v1_assessment_assessments__assessment_id__answers_put"];
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/assessment/assessments/{assessment_id}/events": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** History */
        get: operations["history_api_v1_assessment_assessments__assessment_id__events_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/assessment/assessments/{assessment_id}/evidence": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Evidence List */
        get: operations["evidence_list_api_v1_assessment_assessments__assessment_id__evidence_get"];
        put?: never;
        /** Upload */
        post: operations["upload_api_v1_assessment_assessments__assessment_id__evidence_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/assessment/assessments/{assessment_id}/evidence/{evidence_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Download */
        get: operations["download_api_v1_assessment_assessments__assessment_id__evidence__evidence_id__get"];
        put?: never;
        post?: never;
        /** Delete Evidence */
        delete: operations["delete_evidence_api_v1_assessment_assessments__assessment_id__evidence__evidence_id__delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/assessment/assessments/{assessment_id}/evidence/{evidence_id}/preview": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Preview Evidence */
        get: operations["preview_evidence_api_v1_assessment_assessments__assessment_id__evidence__evidence_id__preview_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/assessment/assessments/{assessment_id}/evidence/{evidence_id}/release": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Release Evidence */
        post: operations["release_evidence_api_v1_assessment_assessments__assessment_id__evidence__evidence_id__release_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/assessment/assessments/{assessment_id}/review": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Review */
        post: operations["review_api_v1_assessment_assessments__assessment_id__review_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/assessment/assessments/{assessment_id}/submit": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Submit */
        post: operations["submit_api_v1_assessment_assessments__assessment_id__submit_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/assessment/frameworks": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List Frameworks */
        get: operations["list_frameworks_api_v1_assessment_frameworks_get"];
        put?: never;
        /** Create Framework */
        post: operations["create_framework_api_v1_assessment_frameworks_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/assessment/frameworks/{framework_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        /** Edit Framework */
        put: operations["edit_framework_api_v1_assessment_frameworks__framework_id__put"];
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/assessment/frameworks/{framework_id}/publish": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Publish Framework */
        post: operations["publish_framework_api_v1_assessment_frameworks__framework_id__publish_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/assessment/frameworks/{framework_id}/versions": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Versions */
        get: operations["versions_api_v1_assessment_frameworks__framework_id__versions_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/assessment/seed-examples": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Seed Examples */
        post: operations["seed_examples_api_v1_assessment_seed_examples_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/auth/complete": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Complete */
        post: operations["complete_api_v1_auth_complete_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/auth/csrf": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Csrf */
        get: operations["csrf_api_v1_auth_csrf_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/auth/login": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Login */
        post: operations["login_api_v1_auth_login_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/auth/logout": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Logout */
        post: operations["logout_api_v1_auth_logout_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/auth/me": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Me */
        get: operations["me_api_v1_auth_me_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/auth/profile": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /** Profile */
        patch: operations["profile_api_v1_auth_profile_patch"];
        trace?: never;
    };
    "/api/v1/auth/refresh": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Refresh */
        post: operations["refresh_api_v1_auth_refresh_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/auth/register": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Register */
        post: operations["register_api_v1_auth_register_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/auth/reset-request": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Reset Request */
        post: operations["reset_request_api_v1_auth_reset_request_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/auth/sessions": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List Sessions */
        get: operations["list_sessions_api_v1_auth_sessions_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/auth/sessions/{session_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        /** Revoke */
        delete: operations["revoke_api_v1_auth_sessions__session_id__delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/auth/switch": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Switch */
        post: operations["switch_api_v1_auth_switch_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/capacity/resources/{rid}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Resource Summary */
        get: operations["resource_summary_api_v1_capacity_resources__rid__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/capacity/snapshots/{id_}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Saved Snapshot */
        get: operations["saved_snapshot_api_v1_capacity_snapshots__id___get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/capacity/teams/{tid}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Team Summary */
        get: operations["team_summary_api_v1_capacity_teams__tid__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/command/snapshot": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Snapshot */
        get: operations["snapshot_api_v1_command_snapshot_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/delivery/history/{kind}/{id_}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** History */
        get: operations["history_api_v1_delivery_history__kind___id___get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/delivery/people": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** People */
        get: operations["people_api_v1_delivery_people_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/delivery/portfolio-summary/{id_}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Portfolio Summary */
        get: operations["portfolio_summary_api_v1_delivery_portfolio_summary__id___get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/delivery/project-summary/{id_}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Summary */
        get: operations["summary_api_v1_delivery_project_summary__id___get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/delivery/{kind}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Listing */
        get: operations["listing_api_v1_delivery__kind__get"];
        put?: never;
        /** Create */
        post: operations["create_api_v1_delivery__kind__post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/delivery/{kind}/{id_}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Detail */
        get: operations["detail_api_v1_delivery__kind___id___get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /** Update */
        patch: operations["update_api_v1_delivery__kind___id___patch"];
        trace?: never;
    };
    "/api/v1/documents": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Library */
        get: operations["library_api_v1_documents_get"];
        put?: never;
        /** Upload */
        post: operations["upload_api_v1_documents_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/documents/citations/{id_}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Citation */
        get: operations["citation_api_v1_documents_citations__id___get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/documents/retention/orphans": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Orphan Preview */
        get: operations["orphan_preview_api_v1_documents_retention_orphans_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/documents/retention/orphans/purge": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Orphan Purge */
        post: operations["orphan_purge_api_v1_documents_retention_orphans_purge_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/documents/search": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Search */
        get: operations["search_api_v1_documents_search_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/documents/versions/{id_}/assessment-link": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Link */
        post: operations["link_api_v1_documents_versions__id___assessment_link_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/documents/versions/{id_}/assessment-links": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Evidence References */
        get: operations["evidence_references_api_v1_documents_versions__id___assessment_links_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/documents/versions/{id_}/cancel": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Cancel */
        post: operations["cancel_api_v1_documents_versions__id___cancel_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/documents/versions/{id_}/download": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Download */
        get: operations["download_api_v1_documents_versions__id___download_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/documents/versions/{id_}/download-ticket": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Ticket */
        post: operations["ticket_api_v1_documents_versions__id___download_ticket_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/documents/versions/{id_}/job": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Job Status */
        get: operations["job_status_api_v1_documents_versions__id___job_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/documents/versions/{id_}/preview": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Preview */
        get: operations["preview_api_v1_documents_versions__id___preview_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/documents/versions/{id_}/reprocess": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Reprocess */
        post: operations["reprocess_api_v1_documents_versions__id___reprocess_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/documents/{id_}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Detail */
        get: operations["detail_api_v1_documents__id___get"];
        put?: never;
        post?: never;
        /** Delete */
        delete: operations["delete_api_v1_documents__id___delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/documents/{id_}/governance": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /** Governance */
        patch: operations["governance_api_v1_documents__id___governance_patch"];
        trace?: never;
    };
    "/api/v1/documents/{id_}/purge": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Purge */
        post: operations["purge_api_v1_documents__id___purge_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/foundation": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Foundation
         * @description Return the persisted foundation identity for the current installation.
         */
        get: operations["getFoundation"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/health/live": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Live
         * @description Report that the API process can handle a liveness request.
         */
        get: operations["getLiveness"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/health/ready": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Ready
         * @description Probe database, Redis and storage readiness under bounded dependency timeouts.
         */
        get: operations["getReadiness"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/integrations": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List Integrations */
        get: operations["list_integrations_api_v1_integrations_get"];
        put?: never;
        /** Create Integration */
        post: operations["create_integration_api_v1_integrations_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/integrations/activity/jobs": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Activity */
        get: operations["activity_api_v1_integrations_activity_jobs_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/integrations/activity/jobs/{id_}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Job Detail */
        get: operations["job_detail_api_v1_integrations_activity_jobs__id___get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/integrations/activity/jobs/{id_}/cancel": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Cancel */
        post: operations["cancel_api_v1_integrations_activity_jobs__id___cancel_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/integrations/activity/jobs/{id_}/events": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Stream */
        get: operations["stream_api_v1_integrations_activity_jobs__id___events_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/integrations/activity/jobs/{id_}/stages": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Stage History */
        get: operations["stage_history_api_v1_integrations_activity_jobs__id___stages_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/integrations/hooks/github/{id_}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Github Hook */
        post: operations["github_hook_api_v1_integrations_hooks_github__id___post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/integrations/{id_}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /** Enable Integration */
        patch: operations["enable_integration_api_v1_integrations__id___patch"];
        trace?: never;
    };
    "/api/v1/integrations/{id_}/authority": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Authority */
        get: operations["authority_api_v1_integrations__id___authority_get"];
        /**
         * Approve
         * @description Each rotation fences queued work; secrets themselves never travel through this API.
         */
        put: operations["approve_api_v1_integrations__id___authority_put"];
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/integrations/{id_}/conflicts": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Review */
        get: operations["review_api_v1_integrations__id___conflicts_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/integrations/{id_}/conflicts/{conflict_id}/resolve": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Resolve */
        post: operations["resolve_api_v1_integrations__id___conflicts__conflict_id__resolve_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/integrations/{id_}/preview": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Preview */
        post: operations["preview_api_v1_integrations__id___preview_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/integrations/{id_}/sources": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Source Evidence */
        get: operations["source_evidence_api_v1_integrations__id___sources_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/integrations/{id_}/sync": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Sync */
        post: operations["sync_api_v1_integrations__id___sync_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/integrations/{id_}/webhook": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Webhook
         * @description Authenticated signed gateway intake; never an unauthenticated provider endpoint.
         */
        post: operations["webhook_api_v1_integrations__id___webhook_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/ml/datasets": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Dataset List */
        get: operations["dataset_list_api_v1_ml_datasets_get"];
        put?: never;
        /** Create Dataset */
        post: operations["create_dataset_api_v1_ml_datasets_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/ml/datasets/{id_}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Dataset Detail */
        get: operations["dataset_detail_api_v1_ml_datasets__id___get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/ml/histories": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** History List */
        get: operations["history_list_api_v1_ml_histories_get"];
        put?: never;
        /** Import History */
        post: operations["import_history_api_v1_ml_histories_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/ml/histories/{id_}/withdraw": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Withdraw */
        post: operations["withdraw_api_v1_ml_histories__id___withdraw_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/ml/runs": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Run List */
        get: operations["run_list_api_v1_ml_runs_get"];
        put?: never;
        /** Train */
        post: operations["train_api_v1_ml_runs_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/ml/runs/{id_}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Run Detail */
        get: operations["run_detail_api_v1_ml_runs__id___get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/ml/runs/{id_}/artifacts": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Artifacts */
        get: operations["artifacts_api_v1_ml_runs__id___artifacts_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/ml/template": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Template */
        get: operations["template_api_v1_ml_template_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/organization/audit": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Audit List */
        get: operations["audit_list_api_v1_organization_audit_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/organization/invitations": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Invitation List */
        get: operations["invitation_list_api_v1_organization_invitations_get"];
        put?: never;
        /** Invite */
        post: operations["invite_api_v1_organization_invitations_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/organization/invitations/{invitation_id}/{operation}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Invitation Action */
        post: operations["invitation_action_api_v1_organization_invitations__invitation_id___operation__post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/organization/members": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Member List */
        get: operations["member_list_api_v1_organization_members_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/organization/members/{user_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /** Change Member */
        patch: operations["change_member_api_v1_organization_members__user_id__patch"];
        trace?: never;
    };
    "/api/v1/organization/profile": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Organization Profile */
        get: operations["organization_profile_api_v1_organization_profile_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /** Edit Organization */
        patch: operations["edit_organization_api_v1_organization_profile_patch"];
        trace?: never;
    };
    "/api/v1/workspace/comparison": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Comparison */
        get: operations["comparison_api_v1_workspace_comparison_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/workspace/events": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Stream */
        get: operations["stream_api_v1_workspace_events_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/workspace/my-work": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** My Work */
        get: operations["my_work_api_v1_workspace_my_work_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/workspace/notification-preference": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        /** Preference */
        put: operations["preference_api_v1_workspace_notification_preference_put"];
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/workspace/notifications": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Feed */
        get: operations["feed_api_v1_workspace_notifications_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/workspace/notifications/{id_}/read": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Mark Read */
        post: operations["mark_read_api_v1_workspace_notifications__id___read_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/workspace/search": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Search */
        get: operations["search_api_v1_workspace_search_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/workspace/setup": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Setup */
        get: operations["setup_api_v1_workspace_setup_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
}
export type webhooks = Record<string, never>;
export interface components {
    schemas: {
        /** AIBudgetInput */
        AIBudgetInput: {
            /** Concurrency */
            concurrency: number;
            /** Limit Usd */
            limit_usd: number | string;
        };
        /** AICallView */
        AICallView: {
            /** Attempt */
            attempt: number;
            /** Charged Usd */
            charged_usd: string;
            /** Code */
            code: string | null;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Input Tokens */
            input_tokens: number | null;
            /** Latency Ms */
            latency_ms: number;
            /** Operation */
            operation: string;
            /** Output Tokens */
            output_tokens: number | null;
            /** Status */
            status: string;
        };
        /** AIDiagnostics */
        AIDiagnostics: {
            /** Calls */
            calls: components["schemas"]["AICallView"][];
            /** Evidence Snapshot */
            evidence_snapshot: {
                [key: string]: string;
            }[];
            /** Graph Version */
            graph_version: string;
            /** Input Sha256 */
            input_sha256: string;
            /** Prompt Version */
            prompt_version: string;
            run: components["schemas"]["AIRunView"];
            /** Schema Version */
            schema_version: string;
            /** Tool Version */
            tool_version: string;
        };
        /** AIEvaluation */
        AIEvaluation: {
            /** Count */
            count: number;
            /** Eligible */
            eligible: boolean;
            /** Environment */
            environment: string;
            /** Failures */
            failures: string[];
            /** Limitation */
            limitation: string;
            /** Passed */
            passed: number;
            /** Real Provider Acceptance */
            real_provider_acceptance: string;
            /** Thresholds */
            thresholds: {
                [key: string]: number;
            };
            /** Version */
            version: string;
        };
        /** AIEvidence */
        AIEvidence: {
            /**
             * Chunk Id
             * Format: uuid
             */
            chunk_id: string;
            /** Location */
            location: string;
            /** Quote */
            quote: string;
            /** Sha256 */
            sha256: string;
            /** Text Sha256 */
            text_sha256: string;
            /**
             * Version Id
             * Format: uuid
             */
            version_id: string;
        };
        /** AIOperations */
        AIOperations: {
            /** Circuit Until */
            circuit_until: string | null;
            /** Concurrency */
            concurrency: number;
            /** Deployment Limit Usd */
            deployment_limit_usd: string;
            /** Failures */
            failures: number;
            /** Limit Usd */
            limit_usd: string;
            provider: components["schemas"]["AIProviderStatus"];
            /** Reserved Usd */
            reserved_usd: string;
            /** Revision */
            revision: number;
            /** Runs */
            runs: components["schemas"]["AIRunView"][];
            /** Spent Usd */
            spent_usd: string;
        };
        /** AIProviderStatus */
        AIProviderStatus: {
            /** Completion Model */
            completion_model: string | null;
            /** Embedding Model */
            embedding_model: string | null;
            /** Enabled */
            enabled: boolean;
            /** Provider */
            provider: string;
            /**
             * Real Provider Acceptance
             * @default not_verified
             * @constant
             */
            real_provider_acceptance: "not_verified";
            /** Reason */
            reason: string;
        };
        /** AIRunInput */
        AIRunInput: {
            /** Analysis Mode */
            analysis_mode?: ("auto" | "metrics" | "domain" | "assessment" | "portfolio" | "executive" | "all_specialists" | "guided") | null;
            /** Assessment Id */
            assessment_id?: string | null;
            /**
             * Operation
             * @default query
             * @enum {string}
             */
            operation: "query" | "index" | "agents";
            /** Prior Run Id */
            prior_run_id?: string | null;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
            /**
             * Query
             * @default
             */
            query: string;
            /** Question Ids */
            question_ids?: string[] | null;
            /** Requested Agents */
            requested_agents?: ("financial" | "schedule" | "sentiment" | "risk" | "resource" | "governance" | "agile_coach" | "pmo" | "executive")[] | null;
            /** Runtime Version */
            runtime_version?: "v2" | null;
            /** Version Id */
            version_id?: string | null;
            /** Version Ids */
            version_ids?: string[];
        };
        /** AIRunView */
        AIRunView: {
            /**
             * Answer Status
             * @enum {string}
             */
            answer_status: "supported" | "unavailable" | "source_fallback" | "indexed" | "not_requested";
            /** Charged Usd */
            charged_usd: string;
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
            /** Diagnostic */
            diagnostic: string | null;
            /** Evidence */
            evidence: components["schemas"]["AIEvidence"][];
            /** Generated At */
            generated_at: string | null;
            /** Graph Version */
            graph_version: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /**
             * Input Snapshot Id
             * Format: uuid
             */
            input_snapshot_id: string;
            /** Input Tokens */
            input_tokens: number | null;
            /** Latency Ms */
            latency_ms: number;
            /** Limitations */
            limitations: string[];
            /** Model */
            model: string | null;
            /** Operation */
            operation: string;
            /**
             * Organization Id
             * Format: uuid
             */
            organization_id: string;
            /** Output Tokens */
            output_tokens: number | null;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
            /** Prompt Version */
            prompt_version: string;
            /** Provider */
            provider: string;
            /** Reserved Usd */
            reserved_usd: string;
            /**
             * Retrieval
             * @enum {string}
             */
            retrieval: "keyword" | "hybrid" | "none";
            /** Revision */
            revision: number;
            /** Schema Version */
            schema_version: string;
            /** Sequence */
            sequence: number;
            /** Status */
            status: string;
            /** Tool Version */
            tool_version: string;
        };
        /** Accepted */
        Accepted: {
            document: components["schemas"]["DocumentView"];
            /**
             * Duplicate
             * @default false
             */
            duplicate: boolean;
            /** Job Id */
            job_id: string | null;
            /**
             * Version Id
             * Format: uuid
             */
            version_id: string;
        };
        /** AccessInput */
        AccessInput: {
            /**
             * Active
             * @default true
             */
            active: boolean;
            /** Assessment Id */
            assessment_id?: string | null;
            /** Framework Id */
            framework_id?: string | null;
            /**
             * User Id
             * Format: uuid
             */
            user_id: string;
        };
        /** AccountView */
        AccountView: {
            /** Email */
            email: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Name */
            name: string;
            /** Organization Id */
            organization_id: string | null;
            /** Organizations */
            organizations: components["schemas"]["OrganizationView"][];
            /** Role */
            role: ("Admin" | "Project Manager" | "Viewer") | null;
        };
        /** ActionInput */
        ActionInput: {
            /**
             * Note
             * @default
             */
            note: string;
        };
        /** Adjustment */
        Adjustment: {
            /**
             * Answer Id
             * Format: uuid
             */
            answer_id: string;
            /** Reviewer Note */
            reviewer_note: string;
            /** Reviewer Score */
            reviewer_score: number | string;
        };
        /** AgentDefinition */
        AgentDefinition: {
            /**
             * Agent
             * @enum {string}
             */
            agent: "financial" | "schedule" | "sentiment" | "risk" | "resource" | "governance" | "agile_coach" | "pmo" | "executive";
            /**
             * Evaluation Cases
             * @default [
             *       "supported",
             *       "missing",
             *       "contradictory",
             *       "malicious"
             *     ]
             */
            evaluation_cases: string[];
            /** Execution Policy */
            execution_policy?: string | null;
            /** Fallback */
            fallback: string;
            /**
             * Guided Enabled
             * @default false
             */
            guided_enabled: boolean;
            /** Guided Project Ids */
            guided_project_ids?: string[];
            /** Inputs */
            inputs: string[];
            /** Modes */
            modes?: string[];
            /**
             * Output Schema
             * @default SpecialistOutput
             */
            output_schema: string;
            /** Task Class */
            task_class?: string | null;
            /** Timeout Seconds */
            timeout_seconds: number;
            /** Tools */
            tools: string[];
        };
        /** AgentState */
        AgentState: {
            /**
             * Agent
             * @enum {string}
             */
            agent: "financial" | "schedule" | "sentiment" | "risk" | "resource" | "governance" | "agile_coach" | "pmo" | "executive";
            /** Code */
            code?: string | null;
            /**
             * Status
             * @enum {string}
             */
            status: "supported" | "fallback" | "unavailable" | "failed";
        };
        /** AlignmentInput */
        "AlignmentInput-Input": {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /** Contribution */
            contribution: number | string;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * Goal Id
             * Format: uuid
             */
            goal_id: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "alignments";
            /** Name */
            name: string;
            /** Portfolio Id */
            portfolio_id?: string | null;
            /** Project Id */
            project_id?: string | null;
            /** Weight */
            weight: number | string;
        };
        /** AlignmentInput */
        "AlignmentInput-Output": {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /** Contribution */
            contribution: string;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * Goal Id
             * Format: uuid
             */
            goal_id: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "alignments";
            /** Name */
            name: string;
            /** Portfolio Id */
            portfolio_id?: string | null;
            /** Project Id */
            project_id?: string | null;
            /** Weight */
            weight: string;
        };
        /** AllocationInput */
        "AllocationInput-Input": {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * End Date
             * Format: date
             */
            end_date: string;
            /** Hours Per Day */
            hours_per_day: number | string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "allocations";
            /** Name */
            name: string;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
            /**
             * Resource Id
             * Format: uuid
             */
            resource_id: string;
            /**
             * Start Date
             * Format: date
             */
            start_date: string;
        };
        /** AllocationInput */
        "AllocationInput-Output": {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * End Date
             * Format: date
             */
            end_date: string;
            /** Hours Per Day */
            hours_per_day: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "allocations";
            /** Name */
            name: string;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
            /**
             * Resource Id
             * Format: uuid
             */
            resource_id: string;
            /**
             * Start Date
             * Format: date
             */
            start_date: string;
        };
        /** AnalysisInput */
        AnalysisInput: {
            /** Analysis Mode */
            analysis_mode?: ("auto" | "metrics" | "domain" | "assessment" | "portfolio" | "executive" | "all_specialists" | "guided") | null;
            /** Assessment Id */
            assessment_id?: string | null;
            /** Prior Run Id */
            prior_run_id?: string | null;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
            /** Question Ids */
            question_ids?: string[] | null;
            /** Requested Agents */
            requested_agents?: ("financial" | "schedule" | "sentiment" | "risk" | "resource" | "governance" | "agile_coach" | "pmo" | "executive")[] | null;
            /** Runtime Version */
            runtime_version?: "v2" | null;
            /** Version Ids */
            version_ids?: string[];
        };
        /** AnalysisRunSummary */
        AnalysisRunSummary: {
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Status */
            status: string;
        };
        /** AnalysisSummary */
        AnalysisSummary: {
            run: components["schemas"]["AnalysisRunSummary"];
            /** Semantic Status */
            semantic_status: string;
        };
        /** AnalysisView */
        AnalysisView: {
            /** Agents */
            agents: components["schemas"]["AgentState"][];
            /** Analysis Mode */
            analysis_mode?: ("auto" | "metrics" | "domain" | "assessment" | "portfolio" | "executive" | "all_specialists" | "guided") | null;
            /** Assessment Id */
            assessment_id: string | null;
            /** Assessment Revision */
            assessment_revision: number | null;
            /** Blocked Reason */
            blocked_reason?: string | null;
            /** Briefing */
            briefing?: components["schemas"]["FindingView"][];
            /**
             * Can Cancel
             * @default false
             */
            can_cancel: boolean;
            /** Can Review */
            can_review: boolean;
            /** Capability Details */
            capability_details?: components["schemas"]["CapabilityDetail"][];
            /** Evidence */
            evidence: components["schemas"]["EvidenceView"][];
            /** Findings */
            findings: components["schemas"]["FindingView"][];
            /** Framework Version Id */
            framework_version_id: string | null;
            guided_review?: components["schemas"]["GuidedReview"] | null;
            /** Limitations */
            limitations: string[];
            /** Missing Agents */
            missing_agents: ("financial" | "schedule" | "sentiment" | "risk" | "resource" | "governance" | "agile_coach" | "pmo" | "executive")[];
            /**
             * Model Quality
             * @default UNVERIFIED/BLOCKED
             * @constant
             */
            model_quality: "UNVERIFIED/BLOCKED";
            /**
             * Prompt Version
             * @default specialists-rubric-v1
             */
            prompt_version: string;
            /** Route Summary */
            route_summary?: {
                [key: string]: unknown;
            }[];
            /**
             * Rule Version
             * @default specialist-support-v1
             */
            rule_version: string;
            run: components["schemas"]["AIRunView"];
            /** Runtime Version */
            runtime_version?: string | null;
            /** Semantic Status */
            semantic_status: string;
            /** Source Snapshot Sha256 */
            source_snapshot_sha256: string;
            /** Stages */
            stages: components["schemas"]["StageView"][];
            /** Suggestions */
            suggestions: components["schemas"]["SuggestionView"][];
            /** Task Summary */
            task_summary?: {
                [key: string]: unknown;
            }[];
            /** Validation Summary */
            validation_summary?: {
                [key: string]: unknown;
            };
        };
        /** AnswerBatchInput */
        AnswerBatchInput: {
            /** Items */
            items: components["schemas"]["AnswerInput"][];
        };
        /** AnswerInput */
        AnswerInput: {
            /**
             * Evidence Text
             * @default
             */
            evidence_text: string;
            /**
             * Question Id
             * Format: uuid
             */
            question_id: string;
            /** Value */
            value?: string | null;
        };
        /** AnswerRecord */
        AnswerRecord: {
            /**
             * Evidence Text
             * @default
             */
            evidence_text: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /**
             * Question Id
             * Format: uuid
             */
            question_id: string;
            /** Reviewer Note */
            reviewer_note: string | null;
            /** Reviewer Score */
            reviewer_score: string | null;
            /** Value */
            value?: string | null;
        };
        /** AssessmentDetail */
        AssessmentDetail: {
            /** Answers */
            answers: components["schemas"]["AnswerRecord"][];
            assessment: components["schemas"]["AssessmentRecord"];
            /** Notes */
            notes: string[];
            snapshot: components["schemas"]["FrameworkInput-Output"];
        };
        /** AssessmentRecord */
        AssessmentRecord: {
            /**
             * Assigned To
             * Format: uuid
             */
            assigned_to: string;
            /** Can Answer */
            can_answer: boolean;
            /** Can Read Evidence */
            can_read_evidence: boolean;
            /** Can Review */
            can_review: boolean;
            /** Department Id */
            department_id?: string | null;
            /** Dimension Scores */
            dimension_scores: components["schemas"]["DimensionScoreDetail"][];
            /** Framework Name */
            framework_name: string;
            /** Framework Version */
            framework_version: number;
            /**
             * Framework Version Id
             * Format: uuid
             */
            framework_version_id: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Name */
            name: string;
            /** Overall Score */
            overall_score: string | null;
            /** Provisional */
            provisional: boolean;
            /**
             * Reviewer Id
             * Format: uuid
             */
            reviewer_id: string;
            /** Revision */
            revision: number;
            /**
             * Status
             * @enum {string}
             */
            status: "draft" | "submitted" | "in_review" | "returned" | "completed";
            /** Team Id */
            team_id?: string | null;
        };
        /** AssignmentInput */
        AssignmentInput: {
            /**
             * Assigned To
             * Format: uuid
             */
            assigned_to: string;
            /** Department Id */
            department_id?: string | null;
            /**
             * Framework Version Id
             * Format: uuid
             */
            framework_version_id: string;
            /** Name */
            name: string;
            /**
             * Reviewer Id
             * Format: uuid
             */
            reviewer_id: string;
            /** Team Id */
            team_id?: string | null;
        };
        /** AuditView */
        AuditView: {
            /** Action */
            action: string;
            /**
             * Actor Id
             * Format: uuid
             */
            actor_id: string;
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /**
             * Request Id
             * Format: uuid
             */
            request_id: string;
            /** Target Id */
            target_id: string | null;
        };
        /** AuditsView */
        AuditsView: {
            /**
             * As Of
             * Format: date-time
             */
            as_of: string;
            /** Items */
            items: components["schemas"]["AuditView"][];
            /** Next Cursor */
            next_cursor?: string | null;
        };
        /** AuthorityInput */
        AuthorityInput: {
            /**
             * Active
             * @default true
             */
            active: boolean;
            /**
             * Interval Minutes
             * @default 0
             */
            interval_minutes: number;
            /**
             * Secret Ref
             * @default
             */
            secret_ref: string;
            /**
             * Webhook Secret Ref
             * @default
             */
            webhook_secret_ref: string;
        };
        /** AuthorityView */
        AuthorityView: {
            /** Active */
            active: boolean;
            /** Generation */
            generation: number;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /**
             * Integration Id
             * Format: uuid
             */
            integration_id: string;
            /** Interval Minutes */
            interval_minutes: number;
            /**
             * Next Due
             * Format: date-time
             */
            next_due: string;
            /** Revision */
            revision: number;
            /**
             * Updated At
             * Format: date-time
             */
            updated_at: string;
        };
        /** AvailabilityInput */
        AvailabilityInput: {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Calendar Id
             * Format: uuid
             */
            calendar_id: string;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * End Date
             * Format: date
             */
            end_date: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "availability";
            /** Name */
            name: string;
            /**
             * Resource Id
             * Format: uuid
             */
            resource_id: string;
            /**
             * Start Date
             * Format: date
             */
            start_date: string;
        };
        /** BaselineInput */
        BaselineInput: {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "baselines";
            /** Name */
            name: string;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
        };
        /** BaselineView */
        BaselineView: {
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Reason */
            reason: string;
            /** Snapshot */
            snapshot: {
                [key: string]: unknown;
            };
            /** Version */
            version: number;
        };
        /** BenefitInput */
        "BenefitInput-Input": {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "benefits";
            /** Name */
            name: string;
            /**
             * Period End
             * Format: date
             */
            period_end: string;
            /**
             * Period Start
             * Format: date
             */
            period_start: string;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
            /** Realized */
            realized?: number | string | null;
            /** Target */
            target: number | string;
            /** Unit */
            unit: string;
        };
        /** BenefitInput */
        "BenefitInput-Output": {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "benefits";
            /** Name */
            name: string;
            /**
             * Period End
             * Format: date
             */
            period_end: string;
            /**
             * Period Start
             * Format: date
             */
            period_start: string;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
            /** Realized */
            realized?: string | null;
            /** Target */
            target: string;
            /** Unit */
            unit: string;
        };
        /** BlockerInput */
        BlockerInput: {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "blockers";
            /** Name */
            name: string;
            /** Owner Id */
            owner_id?: string | null;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
            /**
             * Status
             * @default open
             * @enum {string}
             */
            status: "open" | "resolved";
            /** Work Item Id */
            work_item_id?: string | null;
        };
        /** BudgetInput */
        "BudgetInput-Input": {
            /** Amount */
            amount: number | string;
            /**
             * Approved
             * @default true
             */
            approved: boolean;
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /** Currency */
            currency: string;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "budget_lines";
            /** Name */
            name: string;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
        };
        /** BudgetInput */
        "BudgetInput-Output": {
            /** Amount */
            amount: string;
            /**
             * Approved
             * @default true
             */
            approved: boolean;
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /** Currency */
            currency: string;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "budget_lines";
            /** Name */
            name: string;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
        };
        /** CalendarInput */
        "CalendarInput-Input": {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /** Friday */
            friday: number | string;
            /**
             * Holidays
             * @default
             */
            holidays: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "calendars";
            /** Monday */
            monday: number | string;
            /** Name */
            name: string;
            /** Saturday */
            saturday: number | string;
            /** Sunday */
            sunday: number | string;
            /** Thursday */
            thursday: number | string;
            /** Timezone */
            timezone: string;
            /** Tuesday */
            tuesday: number | string;
            /** Wednesday */
            wednesday: number | string;
        };
        /** CalendarInput */
        "CalendarInput-Output": {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /** Friday */
            friday: string;
            /**
             * Holidays
             * @default
             */
            holidays: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "calendars";
            /** Monday */
            monday: string;
            /** Name */
            name: string;
            /** Saturday */
            saturday: string;
            /** Sunday */
            sunday: string;
            /** Thursday */
            thursday: string;
            /** Timezone */
            timezone: string;
            /** Tuesday */
            tuesday: string;
            /** Wednesday */
            wednesday: string;
        };
        /** CapabilityDetail */
        CapabilityDetail: {
            /**
             * Agent
             * @enum {string}
             */
            agent: "financial" | "schedule" | "sentiment" | "risk" | "resource" | "governance" | "agile_coach" | "pmo" | "executive";
            /** Base Covered Ids */
            base_covered_ids?: string[];
            /**
             * Base Outcome
             * @default insufficient_evidence
             * @enum {string}
             */
            base_outcome: "supported" | "no_findings" | "insufficient_evidence";
            /** Base Required Ids */
            base_required_ids?: string[];
            /** Code */
            code?: string | null;
            /**
             * Execution Method
             * @default deterministic
             * @enum {string}
             */
            execution_method: "deterministic" | "semantic" | "hybrid";
            /**
             * Interpretation Reason
             * @default none
             * @enum {string}
             */
            interpretation_reason: "explicit_request" | "explanatory_text" | "conflicting_evidence" | "cross_domain_synthesis" | "none";
            /** Semantic Covered Ids */
            semantic_covered_ids?: string[];
            /** Semantic Deferred Ids */
            semantic_deferred_ids?: string[];
            /**
             * Semantic Outcome
             * @default not_requested
             * @enum {string}
             */
            semantic_outcome: "not_requested" | "not_needed" | "completed" | "deferred" | "unavailable" | "failed";
            /** Semantic Required Ids */
            semantic_required_ids?: string[];
        };
        /** CapacityDay */
        CapacityDay: {
            /** Actual Hours */
            actual_hours: string | null;
            /** Actual Percent */
            actual_percent: string | null;
            /** Allocated Hours */
            allocated_hours: string;
            /** Available Hours */
            available_hours: string | null;
            /** Calendar Id */
            calendar_id: string | null;
            /**
             * Day
             * Format: date
             */
            day: string;
            /** Effort Complete */
            effort_complete: boolean;
            /** Excess Hours */
            excess_hours: string | null;
            /** Overtime Hours */
            overtime_hours: string | null;
            /** Planned Percent */
            planned_percent: string | null;
            /** Timezone */
            timezone: string | null;
        };
        /** CapacitySnapshotInput */
        CapacitySnapshotInput: {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * End Date
             * Format: date
             */
            end_date: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "capacity_snapshots";
            /** Name */
            name: string;
            /**
             * Resource Id
             * Format: uuid
             */
            resource_id: string;
            /**
             * Start Date
             * Format: date
             */
            start_date: string;
        };
        /** CapacityView */
        CapacityView: {
            /** Actual Hours */
            actual_hours: string | null;
            /** Actual Percent */
            actual_percent: string | null;
            /** Allocated Hours */
            allocated_hours: string;
            /**
             * As Of
             * Format: date-time
             */
            as_of: string;
            /** Available Hours */
            available_hours: string | null;
            /** Can Effort */
            can_effort: boolean;
            /** Can Manage */
            can_manage: boolean;
            /** Days */
            days: components["schemas"]["CapacityDay"][];
            /** Effort Complete */
            effort_complete: boolean;
            /**
             * End Date
             * Format: date
             */
            end_date: string;
            /** Excess Hours */
            excess_hours: string | null;
            /**
             * Metric Version
             * @default capacity-v1
             * @constant
             */
            metric_version: "capacity-v1";
            /** Planned Percent */
            planned_percent: string | null;
            /**
             * Resource Id
             * Format: uuid
             */
            resource_id: string;
            /** Resource Name */
            resource_name: string;
            /**
             * Scope
             * @enum {string}
             */
            scope: "full_resource" | "visible_projects_only";
            /**
             * Start Date
             * Format: date
             */
            start_date: string;
            /** Weeks */
            weeks: components["schemas"]["CapacityWeek"][];
        };
        /** CapacityWeek */
        CapacityWeek: {
            /** Allocated Hours */
            allocated_hours: string;
            /** Available Hours */
            available_hours: string | null;
            /**
             * End Date
             * Format: date
             */
            end_date: string;
            /** Excess Hours */
            excess_hours: string | null;
            /** Planned Percent */
            planned_percent: string | null;
            /**
             * Start Date
             * Format: date
             */
            start_date: string;
        };
        /** Card */
        Card: {
            /** Action */
            action: string;
            /** Fact */
            fact: string;
            /** Location */
            location: string;
            /** Source */
            source: string;
        };
        /** Checklist */
        Checklist: {
            /** Action */
            action: string;
            /**
             * Agent
             * @enum {string}
             */
            agent: "financial" | "schedule" | "sentiment" | "risk" | "resource" | "governance" | "agile_coach" | "pmo" | "executive";
            /** Provider */
            provider: string;
        };
        /** ChunkView */
        ChunkView: {
            /** Confidence */
            confidence: number | null;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Location */
            location: string;
            /** Method */
            method: string;
            /** Ordinal */
            ordinal: number;
            /** Text */
            text: string;
            /**
             * Version Id
             * Format: uuid
             */
            version_id: string;
        };
        /** CommandSnapshot */
        CommandSnapshot: {
            /** Amber */
            amber: string;
            /** Compute Ms */
            compute_ms: number;
            /**
             * Computed At
             * Format: date-time
             */
            computed_at: string;
            /**
             * End
             * Format: date
             */
            end: string;
            /** Limitations */
            limitations: string[];
            /**
             * Metric Version
             * @default command-v1
             * @constant
             */
            metric_version: "command-v1";
            /** Policy Revision */
            policy_revision: number;
            /** Portfolio Id */
            portfolio_id: string | null;
            /** Projects */
            projects: components["schemas"]["ProjectMetrics"][];
            /** Records */
            records: components["schemas"]["RecordView"][];
            /** Red */
            red: string;
            /** Resources */
            resources: components["schemas"]["ResourceMetric"][];
            /**
             * Risk Rule
             * @default risk-rule-v1
             * @constant
             */
            risk_rule: "risk-rule-v1";
            /**
             * Scope
             * @default Current authorized projects only; hidden projects are not counted
             */
            scope: string;
            /** Stale Days */
            stale_days: number;
            /**
             * Start
             * Format: date
             */
            start: string;
            /** Teams */
            teams: components["schemas"]["TeamMetric"][];
            /** Timezone */
            timezone: string;
            /** Totals */
            totals: components["schemas"]["Metric"][];
            /** Velocity */
            velocity: components["schemas"]["Velocity"][];
        };
        /** CompleteChallenge */
        CompleteChallenge: {
            /** Name */
            name: string;
            /** Password */
            password: string;
            /** Token */
            token: string;
        };
        /** ConflictView */
        ConflictView: {
            /** Candidate */
            candidate: {
                [key: string]: unknown;
            };
            /** Fingerprint */
            fingerprint: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Local */
            local: {
                [key: string]: unknown;
            };
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
            /** Revision */
            revision: number;
            /**
             * Source Id
             * Format: uuid
             */
            source_id: string;
            /**
             * Source Observed At
             * Format: date-time
             */
            source_observed_at: string;
            /** Source Updated At */
            source_updated_at: string | null;
            /** Status */
            status: string;
        };
        /** ConnectorConfig */
        ConnectorConfig: {
            /** Board Id */
            board_id?: number | null;
            /**
             * Entity
             * @default issues
             * @enum {string}
             */
            entity: "issues" | "pulls" | "sprints";
            /**
             * Jira Project
             * @default
             */
            jira_project: string;
            /** Mapping */
            mapping?: {
                [key: string]: string;
            };
            /**
             * Mode
             * @default fixture
             * @enum {string}
             */
            mode: "fixture" | "live";
            /** Name */
            name: string;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
            /**
             * Provider
             * @enum {string}
             */
            provider: "csv" | "github" | "jira";
            /**
             * Resource
             * @default
             */
            resource: string;
            /**
             * Secret Ref
             * @default
             */
            secret_ref: string;
            /**
             * Source Namespace
             * @default manual
             */
            source_namespace: string;
            /** Status Map */
            status_map?: {
                [key: string]: string;
            };
            /** Team Id */
            team_id?: string | null;
            /**
             * Webhook Secret Ref
             * @default
             */
            webhook_secret_ref: string;
        };
        /** Credentials */
        Credentials: {
            /**
             * Email
             * Format: email
             */
            email: string;
            /** Password */
            password: string;
        };
        /** CsrfResponse */
        CsrfResponse: {
            /** Csrf Token */
            csrf_token: string;
        };
        /** DatasetInput */
        DatasetInput: {
            /**
             * Cutoff
             * Format: date-time
             */
            cutoff: string;
            /**
             * History Id
             * Format: uuid
             */
            history_id: string;
            /**
             * Horizon Days
             * @default 30
             */
            horizon_days: number;
            /**
             * Target
             * @enum {string}
             */
            target: "delay" | "overrun" | "risk" | "failure" | "sentiment";
            /**
             * Train End
             * Format: date-time
             */
            train_end: string;
            /**
             * Validation End
             * Format: date-time
             */
            validation_end: string;
        };
        /** DatasetView */
        DatasetView: {
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
            /** Digest */
            digest: string;
            /**
             * History Id
             * Format: uuid
             */
            history_id: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Manifest */
            manifest: {
                [key: string]: unknown;
            };
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
        };
        /** DepartmentInput */
        DepartmentInput: {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "departments";
            /** Name */
            name: string;
            /** Owner Id */
            owner_id?: string | null;
        };
        /** DependencyInput */
        DependencyInput: {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "dependencies";
            /** Name */
            name: string;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
            /** Source Milestone Id */
            source_milestone_id?: string | null;
            /** Source Work Item Id */
            source_work_item_id?: string | null;
            /** Target Milestone Id */
            target_milestone_id?: string | null;
            /**
             * Target Project Id
             * Format: uuid
             */
            target_project_id: string;
            /** Target Work Item Id */
            target_work_item_id?: string | null;
        };
        /** DependencyStatus */
        DependencyStatus: {
            /**
             * Name
             * @enum {string}
             */
            name: "database" | "redis" | "storage";
            /**
             * Status
             * @enum {string}
             */
            status: "ready" | "unavailable";
        };
        /** Dimension */
        "Dimension-Input": {
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * Id
             * Format: uuid
             */
            id?: string;
            /** Name */
            name: string;
            /** Questions */
            questions?: components["schemas"]["Question-Input"][];
            /** Weight */
            weight: number | string;
        };
        /** Dimension */
        "Dimension-Output": {
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * Id
             * Format: uuid
             */
            id?: string;
            /** Name */
            name: string;
            /** Questions */
            questions?: components["schemas"]["Question-Output"][];
            /** Weight */
            weight: string;
        };
        /** DimensionScoreDetail */
        DimensionScoreDetail: {
            /** Answered Count */
            answered_count: number;
            /** Coverage Percent */
            coverage_percent: string;
            /**
             * Dimension Id
             * Format: uuid
             */
            dimension_id: string;
            /** Dimension Name */
            dimension_name: string;
            /** Evidence Coverage Percent */
            evidence_coverage_percent: string;
            /** Score */
            score: string | null;
            /** Total Required */
            total_required: number;
            /** Weight */
            weight: string;
        };
        /** DocumentPage */
        DocumentPage: {
            /**
             * As Of
             * Format: date-time
             */
            as_of: string;
            /** Items */
            items: components["schemas"]["DocumentView"][];
            /** Total */
            total: number;
        };
        /** DocumentView */
        DocumentView: {
            /** Can Manage */
            can_manage: boolean;
            /**
             * Category
             * @enum {string}
             */
            category: "SRS" | "BRD" | "PRD" | "MOM" | "sprint_report" | "risk_log" | "charter" | "policy";
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Legal Hold */
            legal_hold: boolean;
            policy: components["schemas"]["Policy"] | null;
            /** Policy Label */
            policy_label?: string | null;
            /** Project Id */
            project_id: string | null;
            /**
             * Retain Until
             * Format: date-time
             */
            retain_until: string;
            /** Revision */
            revision: number;
            /** Title */
            title: string;
            /** Versions */
            versions: components["schemas"]["VersionView"][];
        };
        /** DownloadTicket */
        DownloadTicket: {
            /**
             * Expires At
             * Format: date-time
             */
            expires_at: string;
            /** Token */
            token: string;
        };
        /** EffortCoverageInput */
        EffortCoverageInput: {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Complete
             * @default false
             */
            complete: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "effort_coverage";
            /** Name */
            name: string;
            /**
             * Resource Id
             * Format: uuid
             */
            resource_id: string;
            /**
             * Worked On
             * Format: date
             */
            worked_on: string;
        };
        /** EffortInput */
        "EffortInput-Input": {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /** Hours */
            hours: number | string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "effort";
            /** Name */
            name: string;
            /**
             * Overtime Hours
             * @default 0
             */
            overtime_hours: number | string;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
            /**
             * Resource Id
             * Format: uuid
             */
            resource_id: string;
            /**
             * Worked On
             * Format: date
             */
            worked_on: string;
        };
        /** EffortInput */
        "EffortInput-Output": {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /** Hours */
            hours: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "effort";
            /** Name */
            name: string;
            /**
             * Overtime Hours
             * @default 0
             */
            overtime_hours: string;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
            /**
             * Resource Id
             * Format: uuid
             */
            resource_id: string;
            /**
             * Worked On
             * Format: date
             */
            worked_on: string;
        };
        /** EmailInput */
        EmailInput: {
            /**
             * Email
             * Format: email
             */
            email: string;
        };
        /** EnabledInput */
        EnabledInput: {
            /** Enabled */
            enabled: boolean;
        };
        /** ErrorBody */
        ErrorBody: {
            /** Code */
            code: string;
            /** Details */
            details?: components["schemas"]["ErrorDetail"][];
            /** Message */
            message: string;
            /** Request Id */
            request_id: string;
        };
        /** ErrorDetail */
        ErrorDetail: {
            /** Field */
            field: string;
            /** Reason */
            reason: string;
        };
        /** ErrorResponse */
        ErrorResponse: {
            error: components["schemas"]["ErrorBody"];
        };
        /** EventRecord */
        EventRecord: {
            /**
             * Actor Id
             * Format: uuid
             */
            actor_id: string;
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
            /** Details */
            details: {
                [key: string]: unknown;
            };
            /** Event */
            event: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Note */
            note: string;
        };
        /** EvidenceInput */
        EvidenceInput: {
            /** Content Base64 */
            content_base64: string;
            /** File Name */
            file_name: string;
            /**
             * Question Id
             * Format: uuid
             */
            question_id: string;
        };
        /** EvidenceLink */
        EvidenceLink: {
            /**
             * Attachment Id
             * Format: uuid
             */
            attachment_id: string;
        };
        /** EvidenceRecord */
        EvidenceRecord: {
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
            /** File Name */
            file_name: string;
            /** File Size */
            file_size: number;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /**
             * Question Id
             * Format: uuid
             */
            question_id: string;
            /** Released */
            released: boolean;
            /** Sha256 */
            sha256: string;
        };
        /** EvidenceReference */
        EvidenceReference: {
            /**
             * Assessment Id
             * Format: uuid
             */
            assessment_id: string;
            /** Assessment Name */
            assessment_name: string;
            /**
             * Attachment Id
             * Format: uuid
             */
            attachment_id: string;
        };
        /** EvidenceView */
        EvidenceView: {
            /** Location */
            location: string;
            /** Sha256 */
            sha256: string;
            /** Source */
            source: string;
            /** Text */
            text: string;
            /** Version */
            version: string;
        };
        /** ExpenditureInput */
        "ExpenditureInput-Input": {
            /** Amount */
            amount: number | string;
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /** Currency */
            currency: string;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "expenditures";
            /** Name */
            name: string;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
            /** Reversal Of */
            reversal_of?: string | null;
            /**
             * Spent On
             * Format: date
             */
            spent_on: string;
        };
        /** ExpenditureInput */
        "ExpenditureInput-Output": {
            /** Amount */
            amount: string;
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /** Currency */
            currency: string;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "expenditures";
            /** Name */
            name: string;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
            /** Reversal Of */
            reversal_of?: string | null;
            /**
             * Spent On
             * Format: date
             */
            spent_on: string;
        };
        /** Fact */
        Fact: {
            /** Detail */
            detail: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Kind */
            kind: string;
            /** Name */
            name: string;
            /**
             * Updated At
             * Format: date-time
             */
            updated_at: string;
        };
        /** Features */
        Features: {
            /** Allocation Percent */
            allocation_percent?: number | null;
            /** Bugs */
            bugs?: number | null;
            /** Dependencies */
            dependencies?: number | null;
            /** Scope Change */
            scope_change?: number | null;
            /** Spend Ratio */
            spend_ratio?: number | null;
            /** Velocity */
            velocity?: number | null;
        };
        /** FindingView */
        FindingView: {
            /** Agents */
            agents: ("financial" | "schedule" | "sentiment" | "risk" | "resource" | "governance" | "agile_coach" | "pmo" | "executive")[];
            /** Available */
            available: boolean;
            /** Basis */
            basis?: string[];
            /** Confidence */
            confidence: string | null;
            /** Conflicts */
            conflicts: string[];
            /** Discrepancy */
            discrepancy: boolean;
            /**
             * Epistemic
             * @default deterministic
             * @enum {string}
             */
            epistemic: "deterministic" | "interpretation" | "hypothesis";
            /** Improvement */
            improvement: string;
            /** Key */
            key: string;
            /**
             * Kind
             * @enum {string}
             */
            kind: "risk" | "blocker" | "dependency" | "compliance_gap" | "maturity_evidence";
            /** Predicate */
            predicate?: string | null;
            /** Review Revision */
            review_revision: number;
            /** Reviews */
            reviews: components["schemas"]["ReviewView"][];
            /**
             * Semantic Status
             * @default not_assessed
             */
            semantic_status: string;
            /**
             * Severity
             * @enum {string}
             */
            severity: "low" | "medium" | "high";
            /**
             * Signal
             * @enum {string}
             */
            signal: "adverse" | "clear" | "uncertain";
            /** Spans */
            spans: components["schemas"]["Span"][];
            /** Title */
            title: string;
        };
        /** FoundationResponse */
        FoundationResponse: {
            /**
             * Environment
             * @enum {string}
             */
            environment: "local" | "test" | "demo";
            /**
             * Initialized At
             * Format: date-time
             */
            initialized_at: string;
            /**
             * Instance Id
             * Format: uuid
             */
            instance_id: string;
            /**
             * Schema Revision
             * @default 0017_local_ml_foundations
             * @constant
             */
            schema_revision: "0017_local_ml_foundations";
        };
        /** FrameworkInput */
        "FrameworkInput-Input": {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Category
             * @default custom
             * @enum {string}
             */
            category: "pmo" | "agile" | "governance" | "delivery" | "custom";
            /**
             * Description
             * @default
             */
            description: string;
            /** Dimensions */
            dimensions?: components["schemas"]["Dimension-Input"][];
            /** Name */
            name: string;
        };
        /** FrameworkInput */
        "FrameworkInput-Output": {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Category
             * @default custom
             * @enum {string}
             */
            category: "pmo" | "agile" | "governance" | "delivery" | "custom";
            /**
             * Description
             * @default
             */
            description: string;
            /** Dimensions */
            dimensions?: components["schemas"]["Dimension-Output"][];
            /** Name */
            name: string;
        };
        /** FrameworkRecord */
        FrameworkRecord: {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /** Can Edit */
            can_edit: boolean;
            /**
             * Category
             * @default custom
             * @enum {string}
             */
            category: "pmo" | "agile" | "governance" | "delivery" | "custom";
            /**
             * Description
             * @default
             */
            description: string;
            /** Dimensions */
            dimensions?: components["schemas"]["Dimension-Output"][];
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Name */
            name: string;
            /** Published Version */
            published_version: number | null;
            /** Revision */
            revision: number;
        };
        /** GoalInput */
        GoalInput: {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "goals";
            /** Name */
            name: string;
            /** Owner Id */
            owner_id?: string | null;
        };
        /** Governance */
        Governance: {
            /** Legal Hold */
            legal_hold: boolean;
            policy?: components["schemas"]["Policy"] | null;
            /**
             * Retain Until
             * Format: date-time
             */
            retain_until: string;
        };
        /** GrantInput */
        GrantInput: {
            /**
             * Access
             * @default read
             * @enum {string}
             */
            access: "read" | "edit" | "manage";
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "grants";
            /** Name */
            name: string;
            /** Portfolio Id */
            portfolio_id?: string | null;
            /** Project Id */
            project_id?: string | null;
            /**
             * User Id
             * Format: uuid
             */
            user_id: string;
        };
        /** GuidedReview */
        GuidedReview: {
            /**
             * Agent
             * @enum {string}
             */
            agent: "financial" | "schedule" | "sentiment" | "risk" | "resource" | "governance" | "agile_coach" | "pmo" | "executive";
            /** Cards */
            cards?: components["schemas"]["Card"][];
            /** Checklists */
            checklists?: components["schemas"]["Checklist"][];
            /** Code */
            code?: string | null;
            /** Provider */
            provider: string;
            /**
             * Quality
             * @default LIMITED_SELECTION_NOT_SEMANTIC_QUALIFICATION
             * @constant
             */
            quality: "LIMITED_SELECTION_NOT_SEMANTIC_QUALIFICATION";
            /**
             * Status
             * @enum {string}
             */
            status: "api_selected" | "rules_only" | "pending";
        };
        /** HTTPValidationError */
        HTTPValidationError: {
            /** Detail */
            detail?: components["schemas"]["ValidationError"][];
        };
        /** HealthResponse */
        HealthResponse: {
            /**
             * Service
             * @default enterprise-ppm-api
             * @constant
             */
            service: "enterprise-ppm-api";
            /**
             * Status
             * @default alive
             * @constant
             */
            status: "alive";
        };
        /** HistoryInput */
        HistoryInput: {
            /** Authorized */
            authorized: boolean;
            /**
             * Label Declaration
             * @enum {string}
             */
            label_declaration: "observed-outcomes" | "synthetic-fixture" | "unlabeled";
            /**
             * License
             * @enum {string}
             */
            license: "organization-authorized" | "CC0-1.0";
            /**
             * Lineage
             * @enum {string}
             */
            lineage: "synthetic" | "real";
            /** Name */
            name: string;
            /** Origin */
            origin: string;
            /**
             * Permitted Use
             * @default local-research
             * @constant
             */
            permitted_use: "local-research";
            /**
             * Privacy
             * @default aggregate-numeric-no-personal-data
             * @constant
             */
            privacy: "aggregate-numeric-no-personal-data";
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
            /** Records */
            records: components["schemas"]["Observation"][];
        };
        /** HistoryView */
        HistoryView: {
            /**
             * Actor Id
             * Format: uuid
             */
            actor_id: string;
            /** After */
            after: {
                [key: string]: unknown;
            };
            /** Before */
            before: {
                [key: string]: unknown;
            } | null;
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
        };
        /** ImportInput */
        ImportInput: {
            /** Csv Text */
            csv_text?: string | null;
            /** Records */
            records?: {
                [key: string]: unknown;
            }[] | null;
        };
        /** IntegrationView */
        IntegrationView: {
            config: components["schemas"]["ConnectorConfig"];
            /** Cursor */
            cursor: string | null;
            /** Enabled */
            enabled: boolean;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Revision */
            revision: number;
            /**
             * Updated At
             * Format: date-time
             */
            updated_at: string;
        };
        /** InviteInput */
        InviteInput: {
            /**
             * Email
             * Format: email
             */
            email: string;
            /**
             * Role
             * @enum {string}
             */
            role: "Admin" | "Project Manager" | "Viewer";
        };
        /** JobStatus */
        JobStatus: {
            /** Attempt */
            attempt: number;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Stages */
            stages: string[];
            /** Status */
            status: string;
        };
        /** JobView */
        JobView: {
            /** Accepted */
            accepted: number;
            /** Attempt */
            attempt: number;
            /** Cancel Requested */
            cancel_requested: boolean;
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
            /** Errors */
            errors: {
                [key: string]: unknown;
            }[];
            /** Heartbeat At */
            heartbeat_at: string | null;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Integration Id */
            integration_id: string | null;
            /** Ml Run Id */
            ml_run_id?: string | null;
            /** Position */
            position: number;
            /** Sequence */
            sequence: number;
            /** Status */
            status: string;
            /**
             * Updated At
             * Format: date-time
             */
            updated_at: string;
        };
        /** Level */
        Level: {
            /**
             * Description
             * @default
             */
            description: string;
            /** Label */
            label: string;
            /** Level */
            level: number;
        };
        /** MLHistoryView */
        MLHistoryView: {
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
            /** Digest */
            digest: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Manifest */
            manifest: {
                [key: string]: unknown;
            };
            /** Name */
            name: string;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
            /** Version */
            version: number;
            /** Withdrawn */
            withdrawn: boolean;
        };
        /** MemberInput */
        MemberInput: {
            /** Active */
            active: boolean;
            /**
             * Role
             * @enum {string}
             */
            role: "Admin" | "Project Manager" | "Viewer";
        };
        /** MemberView */
        MemberView: {
            /** Active */
            active: boolean;
            /** Email */
            email: string;
            /** Name */
            name: string;
            /** Revision */
            revision: number;
            /**
             * Role
             * @enum {string}
             */
            role: "Admin" | "Project Manager" | "Viewer";
            /**
             * User Id
             * Format: uuid
             */
            user_id: string;
        };
        /** MembersView */
        MembersView: {
            /**
             * As Of
             * Format: date-time
             */
            as_of: string;
            /** Items */
            items: components["schemas"]["MemberView"][];
            /** Next Cursor */
            next_cursor?: string | null;
        };
        /** Message */
        Message: {
            /** Message */
            message: string;
        };
        /** Metric */
        Metric: {
            /** Coverage Percent */
            coverage_percent: string;
            /** Explanation */
            explanation: string;
            /** Facts */
            facts: components["schemas"]["Fact"][];
            /**
             * Freshness
             * @enum {string}
             */
            freshness: "fresh" | "stale" | "missing";
            /** Key */
            key: string;
            /** Label */
            label: string;
            /** Period */
            period: string;
            /** Source */
            source: string;
            /** Source Updated At */
            source_updated_at: string | null;
            /**
             * Status
             * @enum {string}
             */
            status: "available" | "partial" | "unknown";
            /** Unit */
            unit: string;
            /** Value */
            value: string | null;
        };
        /** MetricPlanInput */
        "MetricPlanInput-Input": {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Baseline Id
             * Format: uuid
             */
            baseline_id: string;
            /**
             * Calendar Id
             * Format: uuid
             */
            calendar_id: string;
            /**
             * Description
             * @default
             */
            description: string;
            /** Forecast Cost */
            forecast_cost?: number | string | null;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "metric_plans";
            /** Name */
            name: string;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
        };
        /** MetricPlanInput */
        "MetricPlanInput-Output": {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Baseline Id
             * Format: uuid
             */
            baseline_id: string;
            /**
             * Calendar Id
             * Format: uuid
             */
            calendar_id: string;
            /**
             * Description
             * @default
             */
            description: string;
            /** Forecast Cost */
            forecast_cost?: string | null;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "metric_plans";
            /** Name */
            name: string;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
        };
        /** MetricPolicyInput */
        "MetricPolicyInput-Input": {
            /**
             * Amber
             * @default 30
             */
            amber: number | string;
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "metric_policies";
            /** Name */
            name: string;
            /**
             * Red
             * @default 60
             */
            red: number | string;
            /**
             * Stale Days
             * @default 7
             */
            stale_days: number;
        };
        /** MetricPolicyInput */
        "MetricPolicyInput-Output": {
            /**
             * Amber
             * @default 30
             */
            amber: string;
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "metric_policies";
            /** Name */
            name: string;
            /**
             * Red
             * @default 60
             */
            red: string;
            /**
             * Stale Days
             * @default 7
             */
            stale_days: number;
        };
        /** MilestoneInput */
        MilestoneInput: {
            /** Actual Date */
            actual_date?: string | null;
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Critical
             * @default false
             */
            critical: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * Due Date
             * Format: date
             */
            due_date: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "milestones";
            /** Name */
            name: string;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
        };
        /** MoneyTotal */
        MoneyTotal: {
            /** Approved Budget */
            approved_budget: string;
            /** Currency */
            currency: string;
            /** Ledger Complete */
            ledger_complete: boolean;
            /** Recorded Spend */
            recorded_spend: string;
            /** Usage Percent */
            usage_percent: string | null;
        };
        /** Observation */
        Observation: {
            /** Entity Id */
            entity_id: string;
            /**
             * Entity Kind
             * @enum {string}
             */
            entity_kind: "project" | "milestone" | "sprint" | "team";
            /**
             * Feature Asof
             * Format: date-time
             */
            feature_asof: string;
            features: components["schemas"]["Features"];
            /**
             * Observed At
             * Format: date-time
             */
            observed_at: string;
            outcome?: components["schemas"]["Outcome"] | null;
        };
        /** OrganizationProfileInput */
        OrganizationProfileInput: {
            /** Description */
            description?: string | null;
            /** Industry */
            industry?: string | null;
            /** Name */
            name?: string | null;
            /** Website */
            website?: string | null;
        };
        /** OrganizationView */
        OrganizationView: {
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Name */
            name: string;
            /**
             * Role
             * @enum {string}
             */
            role: "Admin" | "Project Manager" | "Viewer";
        };
        /** OrphanPage */
        OrphanPage: {
            /** Keys */
            keys: string[];
            /**
             * Minimum Age Days
             * @default 30
             */
            minimum_age_days: number;
            /**
             * Scan Limit
             * @default 10000
             */
            scan_limit: number;
        };
        /** OrphanPurge */
        OrphanPurge: {
            /** Keys */
            keys: string[];
        };
        /** Outcome */
        Outcome: {
            /** Actual Finish */
            actual_finish?: string | null;
            /** Actual Spend */
            actual_spend?: number | null;
            /** Adjudication */
            adjudication?: "independent_outcome_review" | null;
            /** Adverse Category */
            adverse_category?: (0 | 1) | null;
            /**
             * Available At
             * Format: date-time
             */
            available_at: string;
            /**
             * Baseline Known At
             * Format: date-time
             */
            baseline_known_at: string;
            /** Budget */
            budget?: number | null;
            /**
             * Consent
             * @default false
             */
            consent: boolean;
            /** Disposition */
            disposition?: ("cancelled" | "abandoned" | "missed_commitment" | "accepted") | null;
            /** Evidence Ref */
            evidence_ref: string;
            /**
             * Kind
             * @enum {string}
             */
            kind: "observed" | "synthetic";
            /**
             * Occurred At
             * Format: date-time
             */
            occurred_at: string;
            /** Planned Finish */
            planned_finish?: string | null;
            /** Respondents */
            respondents?: number | null;
            /** Survey Mean */
            survey_mean?: number | null;
            /**
             * Target
             * @enum {string}
             */
            target: "delay" | "overrun" | "risk" | "failure" | "sentiment";
        };
        /** PageView */
        PageView: {
            /**
             * As Of
             * Format: date-time
             */
            as_of: string;
            /** Items */
            items: components["schemas"]["RecordView"][];
            /** Limit */
            limit: number;
            /** Offset */
            offset: number;
            /** Total */
            total: number;
        };
        /** PersonView */
        PersonView: {
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Name */
            name: string;
        };
        /** Policy */
        Policy: {
            /** Applicability */
            applicability: string;
            /**
             * Effective Date
             * Format: date
             */
            effective_date: string;
            /**
             * Owner Id
             * Format: uuid
             */
            owner_id: string;
            /**
             * Review Date
             * Format: date
             */
            review_date: string;
            /**
             * State
             * @enum {string}
             */
            state: "draft" | "current" | "superseded";
            /**
             * Version Id
             * Format: uuid
             */
            version_id: string;
        };
        /** PortfolioInput */
        PortfolioInput: {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "portfolios";
            /** Name */
            name: string;
            /** Owner Id */
            owner_id?: string | null;
        };
        /** PortfolioSummary */
        PortfolioSummary: {
            /**
             * As Of
             * Format: date-time
             */
            as_of: string;
            /** Money */
            money: components["schemas"]["MoneyTotal"][];
            portfolio: components["schemas"]["RecordView"];
            /**
             * Scope
             * @default authorized_projects
             * @constant
             */
            scope: "authorized_projects";
            /** Visible Projects */
            visible_projects: number;
        };
        /** PreferenceInput */
        PreferenceInput: {
            /** Enabled */
            enabled: boolean;
        };
        /** Preview */
        Preview: {
            /** Errors */
            errors: {
                [key: string]: unknown;
            }[];
            /** Examples */
            examples: {
                [key: string]: unknown;
            }[];
            /** Valid */
            valid: number;
        };
        /** ProfileInput */
        ProfileInput: {
            /** Name */
            name: string;
        };
        /** ProgramInput */
        ProgramInput: {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "programs";
            /** Name */
            name: string;
            /** Owner Id */
            owner_id?: string | null;
            /**
             * Portfolio Id
             * Format: uuid
             */
            portfolio_id: string;
        };
        /** ProjectInput */
        ProjectInput: {
            /** Actual End Date */
            actual_end_date?: string | null;
            /** Actual Start Date */
            actual_start_date?: string | null;
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /** Category */
            category?: ("delivery" | "transformation" | "compliance" | "research" | "other") | null;
            /** Currency */
            currency: string;
            /** Department Id */
            department_id?: string | null;
            /**
             * Description
             * @default
             */
            description: string;
            /** Forecast End Date */
            forecast_end_date?: string | null;
            /** Industry */
            industry?: ("fintech" | "technology" | "healthcare" | "public_sector" | "other") | null;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "projects";
            /**
             * Ledger Complete
             * @default false
             */
            ledger_complete: boolean;
            /** Methodology */
            methodology?: ("agile" | "waterfall" | "hybrid" | "other") | null;
            /** Name */
            name: string;
            /** Owner Id */
            owner_id?: string | null;
            /**
             * Portfolio Id
             * Format: uuid
             */
            portfolio_id: string;
            /** Priority */
            priority?: ("low" | "normal" | "high" | "urgent") | null;
            /** Program Id */
            program_id?: string | null;
            /**
             * Reported Health
             * @default Unknown
             * @enum {string}
             */
            reported_health: "Green" | "Amber" | "Red" | "Unknown";
            /** Size Band */
            size_band?: ("small" | "medium" | "large") | null;
            /** Start Date */
            start_date?: string | null;
            /**
             * Status
             * @default draft
             * @enum {string}
             */
            status: "draft" | "active" | "on_hold" | "completed" | "cancelled";
            /** Target End Date */
            target_end_date?: string | null;
            /** Team Id */
            team_id?: string | null;
        };
        /** ProjectMetrics */
        ProjectMetrics: {
            /** Can Edit */
            can_edit: boolean;
            /** Computed Health */
            computed_health: string;
            /** Discrepancy */
            discrepancy: boolean;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Metrics */
            metrics: components["schemas"]["Metric"][];
            /** Name */
            name: string;
            /**
             * Portfolio Id
             * Format: uuid
             */
            portfolio_id: string;
            /** Reported Health */
            reported_health: string;
        };
        /** Question */
        "Question-Input": {
            /**
             * Answer Type
             * @default rubric
             * @enum {string}
             */
            answer_type: "boolean" | "rubric" | "text";
            /**
             * Id
             * Format: uuid
             */
            id?: string;
            /** Name */
            name: string;
            /**
             * Required
             * @default true
             */
            required: boolean;
            /** Rubric Levels */
            rubric_levels?: components["schemas"]["Level"][];
            /** Text */
            text: string;
            /**
             * Weight
             * @default 1
             */
            weight: number | string;
        };
        /** Question */
        "Question-Output": {
            /**
             * Answer Type
             * @default rubric
             * @enum {string}
             */
            answer_type: "boolean" | "rubric" | "text";
            /**
             * Id
             * Format: uuid
             */
            id?: string;
            /** Name */
            name: string;
            /**
             * Required
             * @default true
             */
            required: boolean;
            /** Rubric Levels */
            rubric_levels?: components["schemas"]["Level"][];
            /** Text */
            text: string;
            /**
             * Weight
             * @default 1
             */
            weight: string;
        };
        /** ReadyResponse */
        ReadyResponse: {
            /** Dependencies */
            dependencies: components["schemas"]["DependencyStatus"][];
            /**
             * Status
             * @enum {string}
             */
            status: "ready" | "not_ready";
        };
        /** RecordView */
        RecordView: {
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
            /** Data */
            data: components["schemas"]["RiskInput"] | components["schemas"]["BenefitInput-Output"] | components["schemas"]["MetricPlanInput-Output"] | components["schemas"]["MetricPolicyInput-Output"] | components["schemas"]["SavedViewInput"] | components["schemas"]["SettingsInput"] | components["schemas"]["DepartmentInput"] | components["schemas"]["GoalInput"] | components["schemas"]["PortfolioInput"] | components["schemas"]["TeamInput"] | components["schemas"]["ProgramInput"] | components["schemas"]["ProjectInput"] | components["schemas"]["GrantInput"] | components["schemas"]["TeamMemberInput"] | components["schemas"]["SprintInput"] | components["schemas"]["WorkInput-Output"] | components["schemas"]["MilestoneInput"] | components["schemas"]["BlockerInput"] | components["schemas"]["DependencyInput"] | components["schemas"]["BudgetInput-Output"] | components["schemas"]["ExpenditureInput-Output"] | components["schemas"]["StatusInput"] | components["schemas"]["BaselineInput"] | components["schemas"]["AlignmentInput-Output"] | components["schemas"]["ResourceInput"] | components["schemas"]["CalendarInput-Output"] | components["schemas"]["AvailabilityInput"] | components["schemas"]["ResourceTeamInput"] | components["schemas"]["ResourceSkillInput"] | components["schemas"]["TimeOffInput-Output"] | components["schemas"]["AllocationInput-Output"] | components["schemas"]["ResourceAccessInput"] | components["schemas"]["EffortInput-Output"] | components["schemas"]["EffortCoverageInput"] | components["schemas"]["CapacitySnapshotInput"];
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /**
             * Organization Id
             * Format: uuid
             */
            organization_id: string;
            /** Revision */
            revision: number;
            /**
             * Updated At
             * Format: date-time
             */
            updated_at: string;
        };
        /** RegistrationInput */
        RegistrationInput: {
            /**
             * Email
             * Format: email
             */
            email: string;
            /** Organization Name */
            organization_name: string;
        };
        /** Resolution */
        Resolution: {
            /**
             * Decision
             * @enum {string}
             */
            decision: "keep_local" | "accept_source";
            /** Local Revision */
            local_revision: number;
            /** Source Fingerprint */
            source_fingerprint: string;
        };
        /** ResourceAccessInput */
        ResourceAccessInput: {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * Effort
             * @default false
             */
            effort: boolean;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "resource_access";
            /**
             * Manage
             * @default false
             */
            manage: boolean;
            /** Name */
            name: string;
            /**
             * Resource Id
             * Format: uuid
             */
            resource_id: string;
            /**
             * User Id
             * Format: uuid
             */
            user_id: string;
        };
        /** ResourceInput */
        ResourceInput: {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "resources";
            /** Name */
            name: string;
            /** User Id */
            user_id?: string | null;
        };
        /** ResourceMetric */
        ResourceMetric: {
            /** Freshness */
            freshness: string;
            /** Source Updated At */
            source_updated_at: string | null;
            summary: components["schemas"]["CapacityView"];
        };
        /** ResourceSkillInput */
        ResourceSkillInput: {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "resource_skills";
            /** Name */
            name: string;
            /**
             * Resource Id
             * Format: uuid
             */
            resource_id: string;
            /** Skill */
            skill: string;
        };
        /** ResourceTeamInput */
        ResourceTeamInput: {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * End Date
             * Format: date
             */
            end_date: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "resource_teams";
            /** Name */
            name: string;
            /**
             * Resource Id
             * Format: uuid
             */
            resource_id: string;
            /**
             * Start Date
             * Format: date
             */
            start_date: string;
            /**
             * Team Id
             * Format: uuid
             */
            team_id: string;
        };
        /** Result */
        Result: {
            /** Status */
            status: string;
        };
        /** Retrieval */
        Retrieval: {
            /**
             * Chunk Version
             * @default locations-1200-v1
             */
            chunk_version: string;
            /**
             * Embedding Status
             * @default budgeted_ai_runtime
             * @constant
             */
            embedding_status: "budgeted_ai_runtime";
            /** Items */
            items: components["schemas"]["SearchHit"][];
            /**
             * Mode
             * @default keyword
             * @constant
             */
            mode: "keyword";
        };
        /** ReviewView */
        ReviewView: {
            /**
             * Actor Id
             * Format: uuid
             */
            actor_id: string;
            /** Approved Score */
            approved_score?: string | null;
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
            /**
             * Decision
             * @enum {string}
             */
            decision: "accepted" | "rejected";
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Item Key */
            item_key: string;
            /** Reason */
            reason: string;
            /** Revision */
            revision: number;
        };
        /** RiskInput */
        RiskInput: {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "risks";
            /** Likelihood */
            likelihood: number;
            /**
             * Mitigation
             * @default
             */
            mitigation: string;
            /** Name */
            name: string;
            /** Owner Id */
            owner_id?: string | null;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
            /**
             * Resolution
             * @default
             */
            resolution: string;
            /**
             * Review On
             * Format: date
             */
            review_on: string;
            /** Severity */
            severity: number;
            /**
             * Status
             * @default open
             * @enum {string}
             */
            status: "open" | "mitigating" | "accepted" | "closed";
        };
        /** RunInput */
        RunInput: {
            /**
             * Dataset Id
             * Format: uuid
             */
            dataset_id: string;
        };
        /** RunView */
        RunView: {
            /** Card */
            card: {
                [key: string]: unknown;
            };
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
            /**
             * Dataset Id
             * Format: uuid
             */
            dataset_id: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
            /** Status */
            status: string;
        };
        /** SavedViewInput */
        SavedViewInput: {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Dashboard
             * @default Executive
             * @enum {string}
             */
            dashboard: "Executive" | "Delivery" | "Risk" | "Resource";
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * End Date
             * Format: date
             */
            end_date: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "saved_views";
            /** Name */
            name: string;
            /** Portfolio Id */
            portfolio_id?: string | null;
            /**
             * Start Date
             * Format: date
             */
            start_date: string;
            /**
             * User Id
             * Format: uuid
             */
            user_id: string;
        };
        /** SearchHit */
        SearchHit: {
            /** Confidence */
            confidence: number | null;
            /**
             * Document Id
             * Format: uuid
             */
            document_id: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Location */
            location: string;
            /** Method */
            method: string;
            /** Ordinal */
            ordinal: number;
            /** Score */
            score: number;
            /** Sha256 */
            sha256: string;
            /** Text */
            text: string;
            /** Title */
            title: string;
            /**
             * Version Id
             * Format: uuid
             */
            version_id: string;
            /** Version Number */
            version_number: number;
        };
        /** SearchItem */
        SearchItem: {
            /** Due Date */
            due_date?: string | null;
            /** Href */
            href: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /**
             * Kind
             * @enum {string}
             */
            kind: "projects" | "work_items" | "risks" | "assessments";
            /** Name */
            name: string;
            /**
             * Organization Id
             * Format: uuid
             */
            organization_id: string;
            /** Project Id */
            project_id?: string | null;
        };
        /** SearchPage */
        SearchPage: {
            /** Items */
            items: components["schemas"]["SearchItem"][];
            /** Limit */
            limit: number;
            /** Offset */
            offset: number;
            /** Total */
            total: number;
        };
        /** SessionView */
        SessionView: {
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
            /** Current */
            current: boolean;
            /**
             * Expires At
             * Format: date-time
             */
            expires_at: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
        };
        /** SessionsView */
        SessionsView: {
            /** Items */
            items: components["schemas"]["SessionView"][];
        };
        /** SettingsInput */
        SettingsInput: {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /** Currency */
            currency: string;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "settings";
            /** Name */
            name: string;
            /** Timezone */
            timezone: string;
        };
        /** SnapshotView */
        SnapshotView: {
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Snapshot */
            snapshot: {
                [key: string]: unknown;
            };
        };
        /** SourceView */
        SourceView: {
            /** External Id */
            external_id: string;
            /**
             * Job Id
             * Format: uuid
             */
            job_id: string;
            /**
             * Source Observed At
             * Format: date-time
             */
            source_observed_at: string;
            /** Source Updated At */
            source_updated_at: string | null;
            /**
             * Target Id
             * Format: uuid
             */
            target_id: string;
            /** Target Kind */
            target_kind: string;
            /** Target Revision */
            target_revision: number;
        };
        /** Span */
        Span: {
            /** End */
            end: number;
            /** Source */
            source: string;
            /** Start */
            start: number;
        };
        /** SprintInput */
        SprintInput: {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * End Date
             * Format: date
             */
            end_date: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "sprints";
            /** Name */
            name: string;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
            /**
             * Start Date
             * Format: date
             */
            start_date: string;
            /**
             * Status
             * @default planned
             * @enum {string}
             */
            status: "planned" | "active" | "closed";
            /**
             * Team Id
             * Format: uuid
             */
            team_id: string;
        };
        /** StageView */
        StageView: {
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /**
             * Occurred At
             * Format: date-time
             */
            occurred_at: string;
            /** Sequence */
            sequence: number;
            /** Stage */
            stage: string;
        };
        /** StatusInput */
        StatusInput: {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "status_updates";
            /** Name */
            name: string;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
            /**
             * Reported Health
             * @enum {string}
             */
            reported_health: "Green" | "Amber" | "Red" | "Unknown";
        };
        /** SuggestionView */
        SuggestionView: {
            /** Approved Score */
            approved_score: string | null;
            /** Available */
            available: boolean;
            /** Confidence */
            confidence: string | null;
            /**
             * Dimension Id
             * Format: uuid
             */
            dimension_id: string;
            /** Dimension Name */
            dimension_name: string;
            /** Gaps */
            gaps: string[];
            /** Improvement */
            improvement: string;
            /** Key */
            key: string;
            /** Original Score */
            original_score: string | null;
            /** Review Revision */
            review_revision: number;
            /** Reviews */
            reviews: components["schemas"]["ReviewView"][];
            /** Spans */
            spans: components["schemas"]["Span"][];
            /** Suggested Score */
            suggested_score: string | null;
        };
        /** SummaryView */
        SummaryView: {
            /** Alignment Complete */
            alignment_complete: boolean;
            /** Alignment Percent */
            alignment_percent: string | null;
            /**
             * As Of
             * Format: date-time
             */
            as_of: string;
            /** Baselines */
            baselines: components["schemas"]["BaselineView"][];
            /** Can Edit */
            can_edit: boolean;
            /** Can Manage */
            can_manage: boolean;
            /** Computed Health */
            computed_health?: null;
            /**
             * Metric Version
             * @default delivery-v1
             * @constant
             */
            metric_version: "delivery-v1";
            /** Money */
            money: components["schemas"]["MoneyTotal"][];
            project: components["schemas"]["RecordView"];
            /** Work Counts */
            work_counts: {
                [key: string]: number;
            };
        };
        /** SwitchInput */
        SwitchInput: {
            /**
             * Organization Id
             * Format: uuid
             */
            organization_id: string;
        };
        /** TeamCapacityView */
        TeamCapacityView: {
            /** Actual Percent */
            actual_percent?: string | null;
            /** Allocated Hours */
            allocated_hours?: string | null;
            /**
             * As Of
             * Format: date-time
             */
            as_of: string;
            /** Available Hours */
            available_hours?: string | null;
            /** Excess Hours */
            excess_hours?: string | null;
            /**
             * Label
             * @default Team workload support signal; not a diagnosis or individual ranking
             */
            label: string;
            /** Overtime Warning */
            overtime_warning?: boolean | null;
            /** Planned Percent */
            planned_percent?: string | null;
            /** Resource Count */
            resource_count: number;
            /**
             * Status
             * @enum {string}
             */
            status: "available" | "suppressed" | "insufficient_scope" | "incomplete_capacity";
            /** Sustained Overload */
            sustained_overload?: boolean | null;
            /**
             * Team Id
             * Format: uuid
             */
            team_id: string;
        };
        /** TeamInput */
        TeamInput: {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /** Department Id */
            department_id?: string | null;
            /**
             * Description
             * @default
             */
            description: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "teams";
            /** Name */
            name: string;
            /** Owner Id */
            owner_id?: string | null;
        };
        /** TeamMemberInput */
        TeamMemberInput: {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /** End Date */
            end_date?: string | null;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "team_members";
            /** Name */
            name: string;
            /**
             * Start Date
             * Format: date
             */
            start_date: string;
            /**
             * Team Id
             * Format: uuid
             */
            team_id: string;
            /**
             * User Id
             * Format: uuid
             */
            user_id: string;
        };
        /** TeamMetric */
        TeamMetric: {
            /** Name */
            name: string;
            summary: components["schemas"]["TeamCapacityView"];
        };
        /** TimeOffInput */
        "TimeOffInput-Input": {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             * @constant
             */
            description: "";
            /**
             * End Date
             * Format: date
             */
            end_date: string;
            /** Hours Per Day */
            hours_per_day: number | string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "time_off";
            /** Name */
            name: string;
            /**
             * Resource Id
             * Format: uuid
             */
            resource_id: string;
            /**
             * Start Date
             * Format: date
             */
            start_date: string;
        };
        /** TimeOffInput */
        "TimeOffInput-Output": {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Description
             * @default
             * @constant
             */
            description: "";
            /**
             * End Date
             * Format: date
             */
            end_date: string;
            /** Hours Per Day */
            hours_per_day: string;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "time_off";
            /** Name */
            name: string;
            /**
             * Resource Id
             * Format: uuid
             */
            resource_id: string;
            /**
             * Start Date
             * Format: date
             */
            start_date: string;
        };
        /** Upload */
        Upload: {
            /**
             * Category
             * @enum {string}
             */
            category: "SRS" | "BRD" | "PRD" | "MOM" | "sprint_report" | "risk_log" | "charter" | "policy";
            /** Content Base64 */
            content_base64: string;
            /** Document Id */
            document_id?: string | null;
            /** Filename */
            filename: string;
            /** Project Id */
            project_id?: string | null;
            /** Title */
            title: string;
        };
        /** ValidationError */
        ValidationError: {
            /** Context */
            ctx?: Record<string, never>;
            /** Input */
            input?: unknown;
            /** Location */
            loc: (string | number)[];
            /** Message */
            msg: string;
            /** Error Type */
            type: string;
        };
        /** Velocity */
        Velocity: {
            /**
             * End Date
             * Format: date
             */
            end_date: string;
            /** Freshness */
            freshness: string;
            /** Name */
            name: string;
            /** Points */
            points: string | null;
            /**
             * Policy
             * @default team-points-v1: completed work at closure; no cross-team ranking
             */
            policy: string;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
            /** Recorded Points */
            recorded_points: string;
            /** Source Updated At */
            source_updated_at: string | null;
            /**
             * Sprint Id
             * Format: uuid
             */
            sprint_id: string;
            /**
             * Team Id
             * Format: uuid
             */
            team_id: string;
        };
        /** VersionRecord */
        VersionRecord: {
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
            /**
             * Framework Id
             * Format: uuid
             */
            framework_id: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            snapshot: components["schemas"]["FrameworkInput-Output"];
            /** Version */
            version: number;
        };
        /** VersionView */
        VersionView: {
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
            /** Diagnostic */
            diagnostic: string | null;
            /**
             * Document Id
             * Format: uuid
             */
            document_id: string;
            /** Filename */
            filename: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Number */
            number: number;
            /** Parser Version */
            parser_version: string;
            /** Scanner */
            scanner: string | null;
            /** Sha256 */
            sha256: string;
            /** Size */
            size: number;
            /** Status */
            status: string;
            /**
             * Uploaded By
             * Format: uuid
             */
            uploaded_by: string;
        };
        /** WorkInput */
        "WorkInput-Input": {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Blocked
             * @default false
             */
            blocked: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /** Due Date */
            due_date?: string | null;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "work_items";
            /** Name */
            name: string;
            /** Owner Id */
            owner_id?: string | null;
            /** Points */
            points?: number | string | null;
            /** Priority */
            priority?: ("low" | "normal" | "high" | "urgent") | null;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
            /** Sprint Id */
            sprint_id?: string | null;
            /** Start Date */
            start_date?: string | null;
            /**
             * Status
             * @default backlog
             * @enum {string}
             */
            status: "backlog" | "ready" | "in_progress" | "done";
            /** Work Type */
            work_type?: ("task" | "bug" | "story" | "feature" | "other") | null;
        };
        /** WorkInput */
        "WorkInput-Output": {
            /**
             * Archived
             * @default false
             */
            archived: boolean;
            /**
             * Blocked
             * @default false
             */
            blocked: boolean;
            /**
             * Description
             * @default
             */
            description: string;
            /** Due Date */
            due_date?: string | null;
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "work_items";
            /** Name */
            name: string;
            /** Owner Id */
            owner_id?: string | null;
            /** Points */
            points?: string | null;
            /** Priority */
            priority?: ("low" | "normal" | "high" | "urgent") | null;
            /**
             * Project Id
             * Format: uuid
             */
            project_id: string;
            /** Sprint Id */
            sprint_id?: string | null;
            /** Start Date */
            start_date?: string | null;
            /**
             * Status
             * @default backlog
             * @enum {string}
             */
            status: "backlog" | "ready" | "in_progress" | "done";
            /** Work Type */
            work_type?: ("task" | "bug" | "story" | "feature" | "other") | null;
        };
        /** ReviewInput */
        ppm_api__agent_schemas__ReviewInput: {
            /** Approved Score */
            approved_score?: number | string | null;
            /**
             * Decision
             * @enum {string}
             */
            decision: "accepted" | "rejected";
            /** Reason */
            reason: string;
        };
        /** ReviewInput */
        ppm_api__assessment_schemas__ReviewInput: {
            /**
             * Action
             * @enum {string}
             */
            action: "start" | "return" | "complete";
            /** Adjustments */
            adjustments?: components["schemas"]["Adjustment"][];
            /** Note */
            note: string;
        };
    };
    responses: never;
    parameters: never;
    requestBodies: never;
    headers: never;
    pathItems: never;
}
export type $defs = Record<string, never>;
export interface operations {
    definitions_api_v1_agents_definitions_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AgentDefinition"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    listing_api_v1_agents_runs_get: {
        parameters: {
            query?: {
                offset?: number;
            };
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AnalysisSummary"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    create_api_v1_agents_runs_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["AnalysisInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            202: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AnalysisView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    detail_api_v1_agents_runs__id___get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AnalysisView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    review_api_v1_agents_runs__id___reviews__item_key__post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
                item_key: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ppm_api__agent_schemas__ReviewInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AnalysisView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    configure_api_v1_ai_budget_patch: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["AIBudgetInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AIOperations"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    evaluation_api_v1_ai_evaluation_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AIEvaluation"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    operations_api_v1_ai_operations_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AIOperations"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    listing_api_v1_ai_runs_get: {
        parameters: {
            query?: {
                project_id?: string | null;
                offset?: number;
            };
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AIRunView"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    create_api_v1_ai_runs_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["AIRunInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            202: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AIRunView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    detail_api_v1_ai_runs__id___get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AIRunView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    cancel_api_v1_ai_runs__id___cancel_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AIRunView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    diagnostics_api_v1_ai_runs__id___diagnostics_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AIDiagnostics"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    progress_api_v1_ai_runs__id___events_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    stages_api_v1_ai_runs__id___stages_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["StageView"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    status_api_v1_ai_status_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AIProviderStatus"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    access_list_api_v1_assessment_access_get: {
        parameters: {
            query?: {
                framework_id?: string | null;
                assessment_id?: string | null;
            };
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": {
                        [key: string]: unknown;
                    }[];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    set_access_api_v1_assessment_access_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["AccessInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AccessInput"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_assessments_api_v1_assessment_assessments_get: {
        parameters: {
            query?: {
                offset?: number;
                limit?: number;
                framework_version_id?: string | null;
                q?: string;
            };
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AssessmentRecord"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    assign_api_v1_assessment_assessments_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["AssignmentInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AssessmentRecord"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    detail_api_v1_assessment_assessments__assessment_id__get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                assessment_id: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AssessmentDetail"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    save_answers_api_v1_assessment_assessments__assessment_id__answers_put: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                assessment_id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["AnswerBatchInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AssessmentDetail"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    history_api_v1_assessment_assessments__assessment_id__events_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                assessment_id: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["EventRecord"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    evidence_list_api_v1_assessment_assessments__assessment_id__evidence_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                assessment_id: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["EvidenceRecord"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    upload_api_v1_assessment_assessments__assessment_id__evidence_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                assessment_id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["EvidenceInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["EvidenceRecord"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    download_api_v1_assessment_assessments__assessment_id__evidence__evidence_id__get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                assessment_id: string;
                evidence_id: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    delete_evidence_api_v1_assessment_assessments__assessment_id__evidence__evidence_id__delete: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                assessment_id: string;
                evidence_id: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ActionInput"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    preview_evidence_api_v1_assessment_assessments__assessment_id__evidence__evidence_id__preview_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                assessment_id: string;
                evidence_id: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": {
                        [key: string]: string;
                    };
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    release_evidence_api_v1_assessment_assessments__assessment_id__evidence__evidence_id__release_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                assessment_id: string;
                evidence_id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ActionInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["EvidenceRecord"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    review_api_v1_assessment_assessments__assessment_id__review_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                assessment_id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ppm_api__assessment_schemas__ReviewInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AssessmentRecord"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    submit_api_v1_assessment_assessments__assessment_id__submit_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                assessment_id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ActionInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AssessmentRecord"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_frameworks_api_v1_assessment_frameworks_get: {
        parameters: {
            query?: {
                offset?: number;
                limit?: number;
            };
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["FrameworkRecord"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    create_framework_api_v1_assessment_frameworks_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["FrameworkInput-Input"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["FrameworkRecord"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    edit_framework_api_v1_assessment_frameworks__framework_id__put: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                framework_id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["FrameworkInput-Input"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["FrameworkRecord"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    publish_framework_api_v1_assessment_frameworks__framework_id__publish_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                framework_id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ActionInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["VersionRecord"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    versions_api_v1_assessment_frameworks__framework_id__versions_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                framework_id: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["VersionRecord"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    seed_examples_api_v1_assessment_seed_examples_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["FrameworkRecord"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    complete_api_v1_auth_complete_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["CompleteChallenge"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Message"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    csrf_api_v1_auth_csrf_get: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["CsrfResponse"];
                };
            };
        };
    };
    login_api_v1_auth_login_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Credentials"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AccountView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    logout_api_v1_auth_logout_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Message"];
                };
            };
        };
    };
    me_api_v1_auth_me_get: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AccountView"];
                };
            };
        };
    };
    profile_api_v1_auth_profile_patch: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ProfileInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Message"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    refresh_api_v1_auth_refresh_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Message"];
                };
            };
        };
    };
    register_api_v1_auth_register_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["RegistrationInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Message"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    reset_request_api_v1_auth_reset_request_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["EmailInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Message"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_sessions_api_v1_auth_sessions_get: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["SessionsView"];
                };
            };
        };
    };
    revoke_api_v1_auth_sessions__session_id__delete: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                session_id: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Message"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    switch_api_v1_auth_switch_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["SwitchInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AccountView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    resource_summary_api_v1_capacity_resources__rid__get: {
        parameters: {
            query: {
                start: string;
                end: string;
                project_id?: string | null;
            };
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                rid: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["CapacityView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    saved_snapshot_api_v1_capacity_snapshots__id___get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["SnapshotView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    team_summary_api_v1_capacity_teams__tid__get: {
        parameters: {
            query: {
                start: string;
                end: string;
            };
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                tid: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["TeamCapacityView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    snapshot_api_v1_command_snapshot_get: {
        parameters: {
            query: {
                start: string;
                end: string;
                portfolio_id?: string | null;
            };
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["CommandSnapshot"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    history_api_v1_delivery_history__kind___id___get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                kind: "risks" | "benefits" | "metric_plans" | "metric_policies" | "saved_views" | "resources" | "calendars" | "availability" | "resource_teams" | "resource_skills" | "time_off" | "allocations" | "resource_access" | "effort" | "effort_coverage" | "capacity_snapshots" | "settings" | "departments" | "teams" | "goals" | "portfolios" | "programs" | "projects" | "grants" | "team_members" | "sprints" | "work_items" | "milestones" | "blockers" | "dependencies" | "budget_lines" | "expenditures" | "status_updates" | "baselines" | "alignments";
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HistoryView"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    people_api_v1_delivery_people_get: {
        parameters: {
            query?: {
                q?: string;
                offset?: number;
                limit?: number;
            };
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["PersonView"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    portfolio_summary_api_v1_delivery_portfolio_summary__id___get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["PortfolioSummary"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    summary_api_v1_delivery_project_summary__id___get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["SummaryView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    listing_api_v1_delivery__kind__get: {
        parameters: {
            query?: {
                q?: string;
                project_id?: string | null;
                portfolio_id?: string | null;
                resource_id?: string | null;
                skill?: string;
                archived?: boolean;
                status?: string | null;
                industry?: string | null;
                sort?: "name" | "updated";
                offset?: number;
                limit?: number;
            };
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                kind: "risks" | "benefits" | "metric_plans" | "metric_policies" | "saved_views" | "resources" | "calendars" | "availability" | "resource_teams" | "resource_skills" | "time_off" | "allocations" | "resource_access" | "effort" | "effort_coverage" | "capacity_snapshots" | "settings" | "departments" | "teams" | "goals" | "portfolios" | "programs" | "projects" | "grants" | "team_members" | "sprints" | "work_items" | "milestones" | "blockers" | "dependencies" | "budget_lines" | "expenditures" | "status_updates" | "baselines" | "alignments";
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["PageView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    create_api_v1_delivery__kind__post: {
        parameters: {
            query?: never;
            header: {
                "idempotency-key": string;
                "x-organization-id"?: string | null;
            };
            path: {
                kind: "risks" | "benefits" | "metric_plans" | "metric_policies" | "saved_views" | "resources" | "calendars" | "availability" | "resource_teams" | "resource_skills" | "time_off" | "allocations" | "resource_access" | "effort" | "effort_coverage" | "capacity_snapshots" | "settings" | "departments" | "teams" | "goals" | "portfolios" | "programs" | "projects" | "grants" | "team_members" | "sprints" | "work_items" | "milestones" | "blockers" | "dependencies" | "budget_lines" | "expenditures" | "status_updates" | "baselines" | "alignments";
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["RiskInput"] | components["schemas"]["BenefitInput-Input"] | components["schemas"]["MetricPlanInput-Input"] | components["schemas"]["MetricPolicyInput-Input"] | components["schemas"]["SavedViewInput"] | components["schemas"]["SettingsInput"] | components["schemas"]["DepartmentInput"] | components["schemas"]["GoalInput"] | components["schemas"]["PortfolioInput"] | components["schemas"]["TeamInput"] | components["schemas"]["ProgramInput"] | components["schemas"]["ProjectInput"] | components["schemas"]["GrantInput"] | components["schemas"]["TeamMemberInput"] | components["schemas"]["SprintInput"] | components["schemas"]["WorkInput-Input"] | components["schemas"]["MilestoneInput"] | components["schemas"]["BlockerInput"] | components["schemas"]["DependencyInput"] | components["schemas"]["BudgetInput-Input"] | components["schemas"]["ExpenditureInput-Input"] | components["schemas"]["StatusInput"] | components["schemas"]["BaselineInput"] | components["schemas"]["AlignmentInput-Input"] | components["schemas"]["ResourceInput"] | components["schemas"]["CalendarInput-Input"] | components["schemas"]["AvailabilityInput"] | components["schemas"]["ResourceTeamInput"] | components["schemas"]["ResourceSkillInput"] | components["schemas"]["TimeOffInput-Input"] | components["schemas"]["AllocationInput-Input"] | components["schemas"]["ResourceAccessInput"] | components["schemas"]["EffortInput-Input"] | components["schemas"]["EffortCoverageInput"] | components["schemas"]["CapacitySnapshotInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["RecordView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    detail_api_v1_delivery__kind___id___get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                kind: "risks" | "benefits" | "metric_plans" | "metric_policies" | "saved_views" | "resources" | "calendars" | "availability" | "resource_teams" | "resource_skills" | "time_off" | "allocations" | "resource_access" | "effort" | "effort_coverage" | "capacity_snapshots" | "settings" | "departments" | "teams" | "goals" | "portfolios" | "programs" | "projects" | "grants" | "team_members" | "sprints" | "work_items" | "milestones" | "blockers" | "dependencies" | "budget_lines" | "expenditures" | "status_updates" | "baselines" | "alignments";
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["RecordView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    update_api_v1_delivery__kind___id___patch: {
        parameters: {
            query?: never;
            header?: {
                "if-match"?: number | null;
                "x-change-reason"?: string;
                "x-organization-id"?: string | null;
            };
            path: {
                kind: "risks" | "benefits" | "metric_plans" | "metric_policies" | "saved_views" | "resources" | "calendars" | "availability" | "resource_teams" | "resource_skills" | "time_off" | "allocations" | "resource_access" | "effort" | "effort_coverage" | "capacity_snapshots" | "settings" | "departments" | "teams" | "goals" | "portfolios" | "programs" | "projects" | "grants" | "team_members" | "sprints" | "work_items" | "milestones" | "blockers" | "dependencies" | "budget_lines" | "expenditures" | "status_updates" | "baselines" | "alignments";
                id_: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["RiskInput"] | components["schemas"]["BenefitInput-Input"] | components["schemas"]["MetricPlanInput-Input"] | components["schemas"]["MetricPolicyInput-Input"] | components["schemas"]["SavedViewInput"] | components["schemas"]["SettingsInput"] | components["schemas"]["DepartmentInput"] | components["schemas"]["GoalInput"] | components["schemas"]["PortfolioInput"] | components["schemas"]["TeamInput"] | components["schemas"]["ProgramInput"] | components["schemas"]["ProjectInput"] | components["schemas"]["GrantInput"] | components["schemas"]["TeamMemberInput"] | components["schemas"]["SprintInput"] | components["schemas"]["WorkInput-Input"] | components["schemas"]["MilestoneInput"] | components["schemas"]["BlockerInput"] | components["schemas"]["DependencyInput"] | components["schemas"]["BudgetInput-Input"] | components["schemas"]["ExpenditureInput-Input"] | components["schemas"]["StatusInput"] | components["schemas"]["BaselineInput"] | components["schemas"]["AlignmentInput-Input"] | components["schemas"]["ResourceInput"] | components["schemas"]["CalendarInput-Input"] | components["schemas"]["AvailabilityInput"] | components["schemas"]["ResourceTeamInput"] | components["schemas"]["ResourceSkillInput"] | components["schemas"]["TimeOffInput-Input"] | components["schemas"]["AllocationInput-Input"] | components["schemas"]["ResourceAccessInput"] | components["schemas"]["EffortInput-Input"] | components["schemas"]["EffortCoverageInput"] | components["schemas"]["CapacitySnapshotInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["RecordView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    library_api_v1_documents_get: {
        parameters: {
            query?: {
                q?: string;
                project_id?: string | null;
                limit?: number;
                offset?: number;
                deleted?: boolean;
            };
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["DocumentPage"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    upload_api_v1_documents_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Upload"];
            };
        };
        responses: {
            /** @description Successful Response */
            202: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Accepted"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    citation_api_v1_documents_citations__id___get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ChunkView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    orphan_preview_api_v1_documents_retention_orphans_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["OrphanPage"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    orphan_purge_api_v1_documents_retention_orphans_purge_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["OrphanPurge"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Result"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    search_api_v1_documents_search_get: {
        parameters: {
            query: {
                q: string;
                project_id?: string | null;
                limit?: number;
            };
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Retrieval"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    link_api_v1_documents_versions__id___assessment_link_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["EvidenceLink"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Result"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    evidence_references_api_v1_documents_versions__id___assessment_links_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["EvidenceReference"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    cancel_api_v1_documents_versions__id___cancel_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Result"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    download_api_v1_documents_versions__id___download_get: {
        parameters: {
            query: {
                token: string;
            };
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    ticket_api_v1_documents_versions__id___download_ticket_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["DownloadTicket"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    job_status_api_v1_documents_versions__id___job_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["JobStatus"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    preview_api_v1_documents_versions__id___preview_get: {
        parameters: {
            query?: {
                offset?: number;
                limit?: number;
            };
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ChunkView"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    reprocess_api_v1_documents_versions__id___reprocess_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            202: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Accepted"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    detail_api_v1_documents__id___get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["DocumentView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    delete_api_v1_documents__id___delete: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Result"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    governance_api_v1_documents__id___governance_patch: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Governance"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["DocumentView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    purge_api_v1_documents__id___purge_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Result"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    getFoundation: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["FoundationResponse"];
                };
            };
            /** @description Service Unavailable */
            503: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorResponse"];
                };
            };
        };
    };
    getLiveness: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HealthResponse"];
                };
            };
        };
    };
    getReadiness: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ReadyResponse"];
                };
            };
            /** @description Service Unavailable */
            503: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ReadyResponse"];
                };
            };
        };
    };
    list_integrations_api_v1_integrations_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["IntegrationView"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    create_integration_api_v1_integrations_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ConnectorConfig"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["IntegrationView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    activity_api_v1_integrations_activity_jobs_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["JobView"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    job_detail_api_v1_integrations_activity_jobs__id___get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["JobView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    cancel_api_v1_integrations_activity_jobs__id___cancel_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["JobView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    stream_api_v1_integrations_activity_jobs__id___events_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    stage_history_api_v1_integrations_activity_jobs__id___stages_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["StageView"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    github_hook_api_v1_integrations_hooks_github__id___post: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            202: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["JobView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    enable_integration_api_v1_integrations__id___patch: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["EnabledInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["IntegrationView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    authority_api_v1_integrations__id___authority_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AuthorityView"] | null;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    approve_api_v1_integrations__id___authority_put: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["AuthorityInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AuthorityView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    review_api_v1_integrations__id___conflicts_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ConflictView"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    resolve_api_v1_integrations__id___conflicts__conflict_id__resolve_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
                conflict_id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Resolution"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ConflictView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    preview_api_v1_integrations__id___preview_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ImportInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Preview"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    source_evidence_api_v1_integrations__id___sources_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["SourceView"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    sync_api_v1_integrations__id___sync_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ImportInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            202: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["JobView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    webhook_api_v1_integrations__id___webhook_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ImportInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            202: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["JobView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    dataset_list_api_v1_ml_datasets_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["DatasetView"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    create_dataset_api_v1_ml_datasets_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["DatasetInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["DatasetView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    dataset_detail_api_v1_ml_datasets__id___get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["DatasetView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    history_list_api_v1_ml_histories_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["MLHistoryView"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    import_history_api_v1_ml_histories_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["HistoryInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["MLHistoryView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    withdraw_api_v1_ml_histories__id___withdraw_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["MLHistoryView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    run_list_api_v1_ml_runs_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["RunView"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    train_api_v1_ml_runs_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["RunInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            202: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["RunView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    run_detail_api_v1_ml_runs__id___get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["RunView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    artifacts_api_v1_ml_runs__id___artifacts_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": {
                        [key: string]: unknown;
                    };
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    template_api_v1_ml_template_get: {
        parameters: {
            query: {
                project_id: string;
                target?: "delay" | "overrun" | "risk" | "failure" | "sentiment";
            };
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": {
                        [key: string]: unknown;
                    };
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    audit_list_api_v1_organization_audit_get: {
        parameters: {
            query?: {
                after?: string | null;
            };
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AuditsView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    invitation_list_api_v1_organization_invitations_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": {
                        [key: string]: unknown;
                    }[];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    invite_api_v1_organization_invitations_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["InviteInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Message"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    invitation_action_api_v1_organization_invitations__invitation_id___operation__post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                invitation_id: string;
                operation: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Message"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    member_list_api_v1_organization_members_get: {
        parameters: {
            query?: {
                after?: string | null;
            };
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["MembersView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    change_member_api_v1_organization_members__user_id__patch: {
        parameters: {
            query?: never;
            header?: {
                "if-match"?: string | null;
                "x-organization-id"?: string | null;
            };
            path: {
                user_id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["MemberInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["MemberView"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    organization_profile_api_v1_organization_profile_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": {
                        [key: string]: unknown;
                    };
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    edit_organization_api_v1_organization_profile_patch: {
        parameters: {
            query?: never;
            header?: {
                "if-match"?: number | null;
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["OrganizationProfileInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Message"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    comparison_api_v1_workspace_comparison_get: {
        parameters: {
            query: {
                framework_version_id: string;
                start: string;
                end: string;
            };
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": {
                        [key: string]: unknown;
                    };
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    stream_api_v1_workspace_events_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    my_work_api_v1_workspace_my_work_get: {
        parameters: {
            query?: {
                offset?: number;
                limit?: number;
            };
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["SearchPage"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    preference_api_v1_workspace_notification_preference_put: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["PreferenceInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["PreferenceInput"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    feed_api_v1_workspace_notifications_get: {
        parameters: {
            query?: {
                offset?: number;
                limit?: number;
            };
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": {
                        [key: string]: unknown;
                    };
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    mark_read_api_v1_workspace_notifications__id___read_post: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path: {
                id_: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": {
                        [key: string]: unknown;
                    };
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    search_api_v1_workspace_search_get: {
        parameters: {
            query?: {
                q?: string;
                kind?: ("projects" | "work_items" | "risks" | "assessments") | null;
                offset?: number;
                limit?: number;
            };
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["SearchPage"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    setup_api_v1_workspace_setup_get: {
        parameters: {
            query?: never;
            header?: {
                "x-organization-id"?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": {
                        [key: string]: unknown;
                    };
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
}
