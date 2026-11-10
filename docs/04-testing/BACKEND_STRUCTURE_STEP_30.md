# Backend structure cleanup — step 30: table and record ownership

37 existing declarations/helpers move to their owners with identical statement
ASTs. Capacity owns workforce tables; integrations owns connector authority and
conflicts; identity owns mail deliveries. Command owns writable metric/risk input
models. Common record primitives and explicit table registration live in shared/.
Typed-record consumers load the composed registry; feature tables depend on base
constructors. API JSON and all 83 table/index DDL definitions match exactly.

Import/static/type checks pass. No applied migration or database schema change.
Full regression results are recorded in [step 32](BACKEND_STRUCTURE_STEP_32.md).
