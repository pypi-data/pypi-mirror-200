import datetime
import logging
import shlex
import subprocess
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

import psycopg.rows
from pgtoolkit import conf as pgconf
from psycopg import sql

from . import cmd, db, exceptions, hookimpl, types
from .ctx import Context
from .models import interface, system
from .postgresql.ctl import libpq_environ
from .settings import PostgreSQLVersion
from .task import task

logger = logging.getLogger(__name__)


def apply(
    ctx: Context,
    instance: "system.PostgreSQLInstance",
    database: interface.Database,
) -> interface.ApplyResult:
    """Apply state described by specified interface model as a PostgreSQL database.

    The instance should be running.
    """
    name = database.name
    if database.state == interface.PresenceState.absent:
        dropped = False
        if exists(ctx, instance, name):
            drop(ctx, instance, database)
            dropped = True
        return interface.ApplyResult(
            change_state=interface.ApplyChangeState.dropped if dropped else None
        )

    if not exists(ctx, instance, name):
        create(ctx, instance, database)

        if database.clone_from:
            clone(ctx, instance, name, str(database.clone_from))

        return interface.ApplyResult(change_state=interface.ApplyChangeState.created)

    actual = get(ctx, instance, name)
    alter(ctx, instance, database)
    return interface.ApplyResult(
        change_state=(
            interface.ApplyChangeState.changed
            if (get(ctx, instance, name) != actual)
            else None
        )
    )


@task("cloning '{name}' database in instance {instance} from {clone_from}")
def clone(
    ctx: Context, instance: "system.PostgreSQLInstance", name: str, clone_from: str
) -> None:
    def log_cmd(cmd_args: List[str]) -> None:
        base, conninfo = cmd_args[:-1], cmd_args[-1]
        logger.debug(shlex.join(base + [db.obfuscate_conninfo(conninfo)]))

    postgresql_settings = ctx.settings.postgresql
    pg_dump = instance.bindir / "pg_dump"
    dump_cmd = [str(pg_dump), clone_from]
    user = postgresql_settings.surole.name
    psql_cmd = [
        str(instance.bindir / "psql"),
        db.dsn(instance, postgresql_settings, dbname=name, user=user),
    ]
    env = libpq_environ(instance, postgresql_settings.auth, user)
    with subprocess.Popen(  # nosec
        dump_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    ) as dump:
        log_cmd(dump_cmd)
        psql = subprocess.Popen(  # nosec B603
            psql_cmd,
            stdin=dump.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )
        log_cmd(psql_cmd)
        pg_dump_stderr = []
        assert dump.stderr
        for errline in dump.stderr:
            logger.debug("%s: %s", pg_dump, errline.rstrip())
            pg_dump_stderr.append(errline)
        psql_stdout, psql_stderr = psql.communicate()

    if dump.returncode:
        raise exceptions.CommandError(
            dump.returncode, dump_cmd, stderr="".join(pg_dump_stderr)
        )
    if psql.returncode:
        raise exceptions.CommandError(
            psql.returncode, psql_cmd, psql_stdout, psql_stderr
        )


@clone.revert(None)
def revert_clone(
    ctx: Context, instance: "system.PostgreSQLInstance", name: str, clone_from: str
) -> None:
    drop(ctx, instance, interface.DatabaseDropped(name=name))


def get(
    ctx: Context, instance: "system.PostgreSQLInstance", name: str
) -> interface.Database:
    """Return the database object with specified name.

    :raises ~pglift.exceptions.DatabaseNotFound: if no role with specified 'name' exists.
    """
    if not exists(ctx, instance, name):
        raise exceptions.DatabaseNotFound(name)
    with db.connect(ctx, instance, dbname=name) as cnx:
        row = cnx.execute(db.query("database_inspect")).fetchone()
        assert row is not None
        settings = row.pop("settings")
        if settings is None:
            row["settings"] = None
        else:
            row["settings"] = {}
            for s in settings:
                k, v = s.split("=", 1)
                row["settings"][k.strip()] = pgconf.parse_value(v.strip())
        row["schemas"] = schemas(cnx)
        row["extensions"] = extensions(cnx)
    return interface.Database.parse_obj({"name": name, **row})


def list(
    ctx: Context, instance: "system.PostgreSQLInstance", dbnames: Sequence[str] = ()
) -> List[interface.DetailedDatabase]:
    """List databases in instance.

    :param dbnames: restrict operation on databases with a name in this list.
    """
    where_clause: sql.Composable
    where_clause = sql.SQL("")
    if dbnames:
        where_clause = sql.SQL("AND d.datname IN ({})").format(
            sql.SQL(", ").join((map(sql.Literal, dbnames)))
        )
    with db.connect(ctx, instance) as cnx:
        with cnx.cursor(
            row_factory=psycopg.rows.class_row(interface.DetailedDatabase)
        ) as cur:
            cur.execute(db.query("database_list", where_clause=where_clause))
            return cur.fetchall()


def drop(
    ctx: Context,
    instance: "system.PostgreSQLInstance",
    database: interface.DatabaseDropped,
) -> None:
    """Drop a database from a primary instance.

    :raises ~pglift.exceptions.DatabaseNotFound: if no role with specified 'name' exists.
    """
    logger.info("dropping '%s' database from instance %s", database.name, instance)
    if instance.standby:
        raise exceptions.InstanceReadOnlyError(instance)
    if not exists(ctx, instance, database.name):
        raise exceptions.DatabaseNotFound(database.name)

    options = ""
    if database.force_drop:
        if instance.version < PostgreSQLVersion.v13:
            raise exceptions.UnsupportedError(
                "Force drop option can't be used with PostgreSQL < 13"
            )
        options = "WITH (FORCE)"

    with db.connect(ctx, instance) as cnx:
        cnx.execute(
            db.query(
                "database_drop",
                database=sql.Identifier(database.name),
                options=sql.SQL(options),
            )
        )


def exists(ctx: Context, instance: "system.PostgreSQLInstance", name: str) -> bool:
    """Return True if named database exists in 'instance'.

    The instance should be running.
    """
    with db.connect(ctx, instance) as cnx:
        cur = cnx.execute(db.query("database_exists"), {"database": name})
        return cur.rowcount == 1


def options_and_args(
    database: interface.Database,
) -> Tuple[sql.Composable, Dict[str, Any]]:
    """Return the "options" part of CREATE DATABASE or ALTER DATABASE SQL
    commands based on 'database' model along with query arguments.
    """
    opts = []
    args: Dict[str, Any] = {}
    if database.owner is not None:
        opts.append(sql.SQL("OWNER {}").format(sql.Identifier(database.owner)))
    return sql.SQL(" ").join(opts), args


def create(
    ctx: Context,
    instance: "system.PostgreSQLInstance",
    database: interface.Database,
) -> None:
    """Create 'database' in 'instance'.

    The instance should be a running primary and the database should not exist already.
    """
    logger.info("creating '%s' database on instance %s", database.name, instance)
    if instance.standby:
        raise exceptions.InstanceReadOnlyError(instance)
    options, args = options_and_args(database)
    with db.connect(ctx, instance) as cnx:
        cnx.execute(
            db.query(
                "database_create",
                database=sql.Identifier(database.name),
                options=options,
            ),
            args,
        )
        if database.settings is not None:
            alter(ctx, instance, database)

    if database.schemas is not None:
        with db.connect(ctx, instance, dbname=database.name) as cnx:
            create_or_drop_schemas(cnx, database.schemas)

    if database.extensions is not None:
        with db.connect(ctx, instance, dbname=database.name) as cnx:
            create_or_drop_extensions(cnx, database.extensions)


def alter(
    ctx: Context,
    instance: "system.PostgreSQLInstance",
    database: interface.Database,
) -> None:
    """Alter 'database' in 'instance'.

    The instance should be a running primary and the database should exist already.
    """
    logger.info("altering '%s' database on instance %s", database.name, instance)
    if instance.standby:
        raise exceptions.InstanceReadOnlyError(instance)

    if not exists(ctx, instance, database.name):
        raise exceptions.DatabaseNotFound(database.name)

    owner: sql.Composable
    if database.owner is None:
        owner = sql.SQL("CURRENT_USER")
    else:
        owner = sql.Identifier(database.owner)
    options = sql.SQL("OWNER TO {}").format(owner)
    with db.connect(ctx, instance) as cnx:
        cnx.execute(
            db.query(
                "database_alter",
                database=sql.Identifier(database.name),
                options=options,
            ),
        )

    if database.settings is not None:
        with db.connect(ctx, instance) as cnx, cnx.transaction():
            if not database.settings:
                # Empty input means reset all.
                cnx.execute(
                    db.query(
                        "database_alter",
                        database=sql.Identifier(database.name),
                        options=sql.SQL("RESET ALL"),
                    )
                )
            else:
                for k, v in database.settings.items():
                    if v is None:
                        options = sql.SQL("RESET {}").format(sql.Identifier(k))
                    else:
                        options = sql.SQL("SET {} TO {}").format(
                            sql.Identifier(k), sql.Literal(v)
                        )
                    cnx.execute(
                        db.query(
                            "database_alter",
                            database=sql.Identifier(database.name),
                            options=options,
                        )
                    )

    if database.schemas is not None:
        with db.connect(ctx, instance, dbname=database.name) as cnx:
            create_or_drop_schemas(cnx, database.schemas)

    if database.extensions is not None:
        with db.connect(ctx, instance, dbname=database.name) as cnx:
            create_or_drop_extensions(cnx, database.extensions)


def encoding(cnx: db.Connection) -> str:
    """Return the encoding of connected database."""
    row = cnx.execute(db.query("database_encoding")).fetchone()
    assert row is not None
    value = row["encoding"]
    return str(value)


def run(
    ctx: Context,
    instance: "system.PostgreSQLInstance",
    sql_command: str,
    *,
    dbnames: Sequence[str] = (),
    exclude_dbnames: Sequence[str] = (),
    notice_handler: types.NoticeHandler = db.default_notice_handler,
) -> Dict[str, List[Dict[str, Any]]]:
    """Execute a SQL command on databases of `instance`.

    :param dbnames: restrict operation on databases with a name in this list.
    :param exclude_dbnames: exclude databases with a name in this list from
        the operation.
    :param notice_handler: a function to handle notice.

    :returns: a dict mapping database names to query results, if any.

    :raises psycopg.ProgrammingError: in case of unprocessable query.
    """
    result = {}
    for database in list(ctx, instance):
        if (
            dbnames and database.name not in dbnames
        ) or database.name in exclude_dbnames:
            continue
        with db.connect(ctx, instance, dbname=database.name) as cnx:
            cnx.add_notice_handler(notice_handler)
            logger.info(
                'running "%s" on %s database of %s',
                sql_command,
                database.name,
                instance,
            )
            cur = cnx.execute(sql_command)
            if cur.statusmessage:
                logger.info(cur.statusmessage)
            if cur.description is not None:
                result[database.name] = cur.fetchall()
    return result


def dump(ctx: Context, instance: "system.PostgreSQLInstance", dbname: str) -> None:
    """dump a database of `instance` (logical backup)."""
    logger.info("backing up database '%s' on instance %s", dbname, instance)
    if not exists(ctx, instance, dbname):
        raise exceptions.DatabaseNotFound(dbname)
    postgresql_settings = ctx.settings.postgresql

    conninfo = db.dsn(
        instance,
        postgresql_settings,
        dbname=dbname,
        user=ctx.settings.postgresql.surole.name,
    )

    date = (
        datetime.datetime.now(datetime.timezone.utc)
        .astimezone()
        .isoformat(timespec="seconds")
    )
    dumps_directory = instance.dumps_directory
    cmds = [
        [
            c.format(
                bindir=instance.bindir,
                path=dumps_directory,
                conninfo=conninfo,
                dbname=dbname,
                date=date,
            )
            for c in cmd_args
        ]
        for cmd_args in postgresql_settings.dump_commands
    ]
    env = libpq_environ(
        instance, postgresql_settings.auth, postgresql_settings.surole.name
    )
    for cmd_args in cmds:
        cmd.run(cmd_args, check=True, env=env)

    manifest = dumps_directory / f"{dbname}_{date}.manifest"
    manifest.touch()
    manifest.write_text(
        "\n".join(
            [
                "# File created by pglift to keep track of database dumps",
                f"# database: {dbname}",
                f"# date: {date}",
            ]
        )
    )


def list_dumps(
    ctx: Context, instance: "system.PostgreSQLInstance", dbnames: Sequence[str] = ()
) -> List[interface.DatabaseDump]:
    dumps = (
        x.stem.rsplit("_", 1)
        for x in sorted(instance.dumps_directory.glob("*.manifest"))
        if x.is_file()
    )
    return [
        interface.DatabaseDump.build(dbname=dbname, date=date)
        for dbname, date in dumps
        if not dbnames or dbname in dbnames
    ]


def restore(
    ctx: Context,
    instance: "system.PostgreSQLInstance",
    dump_id: str,
    targetdbname: Optional[str] = None,
) -> None:
    """Restore a database dump in `instance`."""
    postgresql_settings = ctx.settings.postgresql

    conninfo = db.dsn(
        instance,
        postgresql_settings,
        dbname=targetdbname or "postgres",
        user=ctx.settings.postgresql.surole.name,
    )

    for dump in list_dumps(ctx, instance):
        if dump.id == dump_id:
            break
    else:
        raise exceptions.DatabaseDumpNotFound(name=f"{dump_id}")

    msg = "restoring dump for '%s' on instance %s"
    msg_variables = [dump.dbname, instance]
    if targetdbname:
        msg += " into '%s'"
        msg_variables.append(targetdbname)
    logger.info(msg, *msg_variables)

    def format_cmd(value: str) -> str:
        assert dump is not None
        return value.format(
            bindir=instance.bindir,
            path=instance.dumps_directory,
            conninfo=conninfo,
            dbname=dump.dbname,
            date=dump.date.isoformat(),
            createoption="-C" if targetdbname is None else "",
        )

    env = libpq_environ(
        instance, postgresql_settings.auth, postgresql_settings.surole.name
    )
    for cmd_args in postgresql_settings.restore_commands:
        parts = [format_cmd(part) for part in cmd_args if format_cmd(part)]
        cmd.run(parts, check=True, env=env)


@hookimpl
def instance_configure(
    ctx: "Context", manifest: "interface.Instance", creating: bool
) -> None:
    if creating:
        instance = system.BaseInstance.get(manifest.name, manifest.version, ctx)
        instance.dumps_directory.mkdir(parents=True, exist_ok=True)


@hookimpl
def instance_drop(ctx: "Context", instance: "system.Instance") -> None:
    dumps_directory = instance.dumps_directory
    if not dumps_directory.exists():
        return
    has_dumps = next(dumps_directory.iterdir(), None) is not None
    if not has_dumps or ctx.confirm(
        f"Confirm deletion of database dump(s) for instance {instance}?",
        True,
    ):
        ctx.rmtree(dumps_directory)


def schemas(cnx: db.Connection) -> List[interface.Schema]:
    """Return list of schemas of database."""
    with cnx.cursor(row_factory=psycopg.rows.class_row(interface.Schema)) as cur:
        cur.execute(db.query("list_schemas"))
        return cur.fetchall()


def create_or_drop_schemas(
    cnx: db.Connection, schemas_: Sequence[interface.Schema]
) -> None:
    """Create or drop schemas in/from database."""
    existing = {s.name for s in schemas(cnx)}
    absent = interface.PresenceState.absent
    for schema in schemas_:
        if schema.state is absent and schema.name in existing:
            logger.info("dropping schema '%s'", schema.name)
            cnx.execute(
                db.query("drop_schema", schema=psycopg.sql.Identifier(schema.name))
            )
        elif schema.state is not absent and schema.name not in existing:
            logger.info("creating schema '%s'", schema.name)
            cnx.execute(
                db.query("create_schema", schema=psycopg.sql.Identifier(schema.name))
            )


def extensions(cnx: db.Connection) -> List[interface.Extension]:
    """Return list of extensions created in connected database using CREATE EXTENSION"""

    with cnx.cursor(row_factory=psycopg.rows.class_row(interface.Extension)) as cur:
        cur.execute(db.query("list_extensions"))
        return cur.fetchall()


def extensions_state(
    current: Sequence[interface.Extension], target: Sequence[interface.Extension]
) -> Tuple[
    Set[interface.Extension], Set[interface.Extension], Set[interface.Extension]
]:
    """Return a set of extensions to add, update and remove.
    >>> from .models.interface import PresenceState
    >>> installed = [
    ...     interface.Extension(name="foo", schema="public"),
    ...     interface.Extension(name="bar", schema="public"),
    ...     interface.Extension(name="dude", schema="public"),
    ... ]
    >>> extensions_ = [
    ...     interface.Extension(name="bar", schema="schema1"),
    ...     interface.Extension(name="dude", state=PresenceState.absent, schema="public"),
    ...     interface.Extension(name="truc", schema="public"),
    ... ]
    >>> to_add, to_update, to_remove = extensions_state(installed, extensions_)
    >>> [e.name for e in to_add]
    ['truc']
    >>> [e.name for e in to_update]
    ['bar']
    >>> [e.name for e in to_remove]
    ['dude']
    """
    current_names = {c.name for c in current}
    absent = interface.PresenceState.absent
    to_drop = {e for e in target if e.state is absent and e.name in current_names}
    to_alter = {
        e
        for e in target
        if e.state is not absent and e.name in current_names and e not in current
    }
    to_add = {
        e for e in target if e.state is not absent and e.name not in current_names
    }
    assert not to_drop & to_alter & to_add  # sets are not supposed to overlap
    return to_add, to_alter, to_drop


def create_or_drop_extensions(
    cnx: db.Connection, extensions_: Sequence[interface.Extension]
) -> None:
    """Create or drop extensions from database."""

    def s(extensions: Set[interface.Extension]) -> List[interface.Extension]:
        return sorted(extensions, key=lambda e: e.name)

    with cnx.transaction():
        installed = extensions(cnx)
        to_add, to_update, to_remove = extensions_state(installed, extensions_)

        r = cnx.execute("SELECT current_schema()").fetchone()
        assert r is not None
        current_schema = r["current_schema"]
        opts: sql.Composable
        for extension in s(to_add):
            if extension.schema_:
                opts = sql.SQL("WITH SCHEMA {}").format(
                    sql.Identifier(extension.schema_)
                )
                logger.info(
                    "creating extension '%s' in schema '%s'",
                    extension.name,
                    extension.schema_,
                )
            else:
                opts = sql.SQL("")
                logger.info("creating extension '%s'", extension.name)
            cnx.execute(
                db.query(
                    "create_extension",
                    extension=psycopg.sql.Identifier(extension.name),
                    opts=opts,
                )
            )

        for extension in s(to_update):
            schema = extension.schema_ or current_schema
            opts = sql.SQL("SET SCHEMA {}").format(sql.Identifier(schema))
            logger.info("setting '%s' extension schema to '%s'", extension.name, schema)
            cnx.execute(
                db.query(
                    "alter_extension",
                    extension=psycopg.sql.Identifier(extension.name),
                    opts=opts,
                )
            )

        for extension in s(to_remove):
            logger.info("dropping extension '%s'", extension.name)
            cnx.execute(
                db.query(
                    "drop_extension",
                    extension=psycopg.sql.Identifier(extension.name),
                )
            )
