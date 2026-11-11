# Backend structure cleanup — step 31: complete HTTP/operation separation

90 remaining handlers become thin adapters with unchanged HTTP signatures,
decorators, response metadata and descriptions. Operations retain their complete
body statements/comments, use Principal and ordinary parameter defaults, and do
not register HTTP routes. Existing 39 assessment/document handlers remain thin,
giving 129 handlers across 13 routing modules. Domain/worker callers use operation
owners directly. Inline job/connector, workspace and selection models move to
their schemas modules with unchanged definitions. Complete API JSON (113 paths)
and all 83 table/index DDL definitions match exactly; no contract regeneration.

AST checks preserve operations, models, wrappers and unrelated source. Typing and
583-case collection pass. See [step 32](BACKEND_STRUCTURE_STEP_32.md) for executed
full-suite results and environmental limits. Existing authority, transaction,
CSRF, quota, source prompts, providers and stopped pilots remain unchanged.
