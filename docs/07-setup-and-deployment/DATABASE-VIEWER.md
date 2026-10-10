# View the project database on this PC

The Enterprise PPM application uses PostgreSQL, running in Docker Desktop's Linux
engine. Its main database is `ppm_local`, with 63 public tables at migration
`0008_pilot_completion` (verified 10 October 2026). Test/demo databases are separate.

## Open the viewer

Open <http://localhost:5050> while Docker Desktop is running. The local pgAdmin
viewer has the existing server connection configured and opens without a login.
Expand:

`Servers > Enterprise PPM - Local database > Databases > ppm_local > Schemas > public > Tables`

Right-click `ppm_projects`, then select **View/Edit Data > All Rows** to see
project records. Other useful tables include `organizations`, `ppm_portfolios`,
`ppm_programs`, and `ppm_work_items`. Use **Query Tool** for SQL, for example:

```sql
SELECT id, name FROM public.ppm_projects LIMIT 50;
```

This is an administrator connection to the actual application database. Edits
and deletes here affect the application directly. The viewer listens only on
this PC's loopback interface; its login-free configuration is for local use.
Database credentials stay in ignored local configuration, outside source control.

## Where the data lives

- Windows clients connect to `localhost`, port `15432`, database `ppm_local`.
- PostgreSQL container: `enterprise-ppm-postgres-1`.
- Persistent Docker volume: `enterprise-ppm_postgres_data`.
- Linux volume location: `/var/lib/docker/volumes/enterprise-ppm_postgres_data/_data`.
- This location is inside Docker Desktop's Linux storage, rather than an ordinary
  database file under the project's Windows folder.
- Schema definitions: `services/api/ppm_api/*tables.py`; migrations:
  `services/api/migrations/versions/`.
- Redis is a separate job broker/cache; uploaded objects use the `objects` volume.

The project credentials are in the existing ignored `.env`. Do not rerun bootstrap
to replace passwords on established data, delete the PostgreSQL volume, or use
`docker compose down -v` to stop the viewer.

Verification on 10 October 2026: the viewer returned HTTP 200, its own database
connection successfully read `ppm_local` and all 63 public tables, and the browser
displayed the configured server and database list. The existing web/API remained
healthy. `ppm_local` contained three organizations and zero project rows at setup.

## Start and stop

Run PowerShell in `C:\Users\alokg\OneDrive\Documents\Codex\enterprise-ppm`.

```powershell
# Start the database and viewer, preserving existing data.
docker compose -f compose.yaml -f compose.database-viewer.yaml up -d postgres pgadmin

# Stop just the viewer.
docker compose -f compose.yaml -f compose.database-viewer.yaml stop pgadmin
```

The viewer restarts when Docker starts, unless you explicitly stop it. Its own
preferences are stored separately in `enterprise-ppm_pgadmin_data`.
The bootstrap secret is `artifacts/local/pgadmin-password.txt` (ignored); it is
required by the container even though local desktop mode skips the login screen.

Setup follows the [official Docker pgAdmin guide](https://docs.docker.com/guides/pgadmin/)
and [pgAdmin container documentation](https://www.pgadmin.org/docs/pgadmin4/9.18/container_deployment.html).
