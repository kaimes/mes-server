from alembic import context
from sqlalchemy import create_engine, engine_from_config, pool, inspect
from sqlalchemy import  text

from dispatch.log import logging
from dispatch.config import SQLALCHEMY_DATABASE_ARCHIVE_URI
from dispatch.database import Base


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.

from dispatch.log import getLogger
log = getLogger(__name__)

config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_ARCHIVE_URI)

target_metadata = Base.metadata


def get_tenant_schemas(connection):
    tenant_schemas = []
    for s in inspect(connection).get_schema_names():
        if s.startswith("dispatch_organization_"):
            tenant_schemas.append(s)
    return tenant_schemas


# produce an include object function that filters on the given schemas
def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table":
        if object.schema:
            return False
    return True


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    def process_revision_directives(context, revision, directives):
        script = directives[0]
        if script.upgrade_ops.is_empty():
            directives[:] = []
            log.info("No changes found skipping revision creation.")

    connectable = engine_from_config(
        config.get_section(config.config_ini_section), prefix="sqlalchemy.", poolclass=pool.NullPool
    )
    all_tentant_schemas = []
    with connectable.connect() as connection:
        all_tentant_schemas = get_tenant_schemas(connectable)


    #  op.execute("SET search_path TO dispatch_organization_mes_root")
    
    for schema in all_tentant_schemas:
        with connectable.connect() as connection:
            log.info(f"Migrating {schema}...")
            connection = connection.execution_options(schema_translate_map={None: schema})
            connection.execute(text(f'SET search_path TO {schema}'))
            connection.dialect.default_schema_name = schema


            # get the schema names
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                include_schemas=True,
                include_object=include_object,
                process_revision_directives=process_revision_directives,
            )
            try:
                with context.begin_transaction():
                    context.run_migrations()
            except Exception as e:
                log.error(f"run_migrations_online, {e}...")
            

if context.is_offline_mode():
    log.info("Can't run migrations offline")
else:
    run_migrations_online()
