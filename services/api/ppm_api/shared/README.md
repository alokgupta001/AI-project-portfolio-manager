# Shared record foundation

| File | Responsibility |
| --- | --- |
| [record_schemas.py](record_schemas.py) | Common record fields, primitive money/fraction/currency types and the record-kind contract |
| [table_base.py](table_base.py) | Shared SQLAlchemy metadata, typed-record registry and reusable record/tenant table constructors |
| [table_registry.py](table_registry.py) | Explicitly import every feature table once and expose complete metadata/TABLES to API, scripts, workers and migrations |
| [__init__.py](__init__.py) | Package description; no eager exports |

Feature tables depend on table_base. Consumers load table_registry when they need
the composed record catalogue. This keeps record registration complete without
making one feature the owner of another feature's tables. No database table,
constraint, migration or RLS policy is introduced by this Python composition.

The generic delivery record API intentionally composes input/view contracts across
delivery, capacity and command. Definitions remain at their feature owners; the
existing polymorphic API and its transaction/audit behavior remain.
