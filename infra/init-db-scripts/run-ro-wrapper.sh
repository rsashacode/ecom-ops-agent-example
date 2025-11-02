#!/usr/bin/env bash
set -euo pipefail

: "${POSTGRES_DB:=postgres}"
: "${POSTGRES_USER:=postgres}"
: "${PGUSER_RO:?PGUSER_RO must be set}"
: "${PGUSER_RO_PASSWORD:?PGUSER_RO_PASSWORD must be set}"

psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<SQL
\\set ON_ERROR_STOP on

DO \$do\$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = ${PGUSER_RO@Q}) THEN
    -- %I for identifiers (role), %L for string literal (password)
    EXECUTE format('CREATE ROLE %I LOGIN PASSWORD %L',
                   ${PGUSER_RO@Q}, ${PGUSER_RO_PASSWORD@Q});
  END IF;

  -- Grants that require identifiers: use EXECUTE/format with %I
  EXECUTE format('GRANT CONNECT ON DATABASE %I TO %I',
                 ${POSTGRES_DB@Q}, ${PGUSER_RO@Q});
  EXECUTE format('GRANT USAGE ON SCHEMA %I TO %I',
                 'public', ${PGUSER_RO@Q});
  EXECUTE format('GRANT SELECT ON ALL TABLES IN SCHEMA %I TO %I',
                 'public', ${PGUSER_RO@Q});
  EXECUTE format('ALTER DEFAULT PRIVILEGES IN SCHEMA %I GRANT SELECT ON TABLES TO %I',
                 'public', ${PGUSER_RO@Q});
END
\$do\$ LANGUAGE plpgsql;
SQL
