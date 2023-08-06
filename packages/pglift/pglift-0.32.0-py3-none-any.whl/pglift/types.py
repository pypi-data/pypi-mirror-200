import abc
import enum
import json
import re
import socket
import subprocess
from functools import cached_property
from pathlib import Path
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Dict,
    Iterator,
    List,
    Literal,
    Optional,
    Protocol,
    Tuple,
    Type,
    TypedDict,
    Union,
)

import psycopg.errors
import yaml
from pgtoolkit import conf as pgconf
from pydantic import BaseModel, ConstrainedStr, SecretStr, create_model
from typing_extensions import TypeAlias

from ._compat import Self

if TYPE_CHECKING:
    CompletedProcess = subprocess.CompletedProcess[str]
    Popen = subprocess.Popen[str]
    from .pm import PluginManager
else:
    CompletedProcess = subprocess.CompletedProcess
    Popen = subprocess.Popen


class StrEnum(str, enum.Enum):
    def __str__(self) -> str:
        assert isinstance(self.value, str)
        return self.value


@enum.unique
class AutoStrEnum(StrEnum):
    """Enum base class with automatic values set to member name.

    >>> class State(AutoStrEnum):
    ...     running = enum.auto()
    ...     stopped = enum.auto()
    >>> State.running
    <State.running: 'running'>
    >>> State.stopped
    <State.stopped: 'stopped'>
    """

    def _generate_next_value_(name, *args: Any) -> str:  # type: ignore[override]
        return name


ConfigChanges: TypeAlias = Dict[
    str, Tuple[Optional[pgconf.Value], Optional[pgconf.Value]]
]


class BackupType(AutoStrEnum):
    """Backup type."""

    full = enum.auto()
    """full backup"""
    incr = enum.auto()
    """incremental backup"""
    diff = enum.auto()
    """differential backup"""

    @classmethod
    def default(cls) -> "BackupType":
        return cls.incr


PostgreSQLStopMode = Literal["smart", "fast", "immediate"]


class Role(Protocol):
    @property
    def name(self) -> str:
        ...

    @property
    def password(self) -> Optional[SecretStr]:
        ...

    @property
    def encrypted_password(self) -> Optional[SecretStr]:
        ...


class NoticeHandler(Protocol):
    def __call__(self, diag: psycopg.errors.Diagnostic) -> Any:
        ...


class AnsibleArgSpec(TypedDict, total=False):
    required: bool
    type: str
    default: Any
    choices: List[str]
    description: List[str]
    no_log: bool
    elements: str
    options: Dict[str, Any]


class CLIConfig(TypedDict, total=False):
    """Configuration for CLI generation of a manifest field."""

    name: str
    hide: bool
    choices: List[str]


class AnsibleConfig(TypedDict, total=False):
    hide: bool
    choices: List[str]
    spec: AnsibleArgSpec


class Port(int):
    """Port field type."""

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[..., Self]]:
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> Self:
        return cls(value)

    def available(self) -> bool:
        """Return True if this port is free to use."""
        port = int(self)
        for family, socktype, proto, canonname, sockaddr in socket.getaddrinfo(
            None, port, 0, socket.SOCK_STREAM, 0, socket.AI_PASSIVE
        ):
            with socket.socket(family, socktype, proto) as s:
                if s.connect_ex(sockaddr) == 0:
                    return False
        return True


class Manifest(BaseModel):
    """Base class for manifest data classes."""

    _cli_config: ClassVar[Dict[str, CLIConfig]] = {}
    _ansible_config: ClassVar[Dict[str, AnsibleConfig]] = {}

    class Config:
        allow_mutation = False
        extra = "forbid"
        validate_always = True
        validate_assignment = True

    @classmethod
    def parse_yaml(cls, value: Union[str, IO[str]]) -> Self:
        """Parse from a YAML stream."""
        data = yaml.safe_load(value)
        return cls.parse_obj(data)

    def yaml(self, **kwargs: Any) -> str:
        """Return a YAML serialization of this manifest."""
        data = json.loads(self.json(by_alias=True, **kwargs))
        return yaml.dump(data, sort_keys=False, explicit_start=True)  # type: ignore[no-any-return]

    def _copy_validate(self, update: Dict[str, Any]) -> Self:
        """Like .copy(), but with validation (and default value setting).

        (Internal method, mostly useful for test purpose.)
        """
        return self.__class__.validate(dict(self.dict(by_alias=True), **update))


class CompositeManifest(Manifest, abc.ABC):
    """A manifest type with extra fields from plugins."""

    class Config(Manifest.Config):
        # Allow extra fields to permit plugins to populate an object with
        # their specific data, following (hopefully) what's defined by
        # the "composite" model (see composite()).
        extra = "allow"

    @classmethod
    def composite(cls, pm: "PluginManager") -> Type[Self]:
        fields = {}
        for name, m, f in cls.component_models(pm):
            if name in fields:
                raise ValueError(f"duplicated '{name}' service")
            fields[name] = m, f
        # XXX Spurious 'type: ignore' below.
        m = create_model(cls.__name__, __base__=cls, __module__=__name__, **fields)  # type: ignore[call-overload]
        # pydantic.create_model() uses type(), so this will confuse mypy which
        # cannot handle dynamic base class; hence the 'type: ignore'.
        return m  # type: ignore[no-any-return]

    @classmethod
    @abc.abstractmethod
    def component_models(cls, pm: "PluginManager") -> List[Tuple[str, Any, Any]]:
        ...


class ServiceManifest(Manifest):
    __service__: ClassVar[str]

    def __init_subclass__(cls, *, service_name: str, **kwargs: Any) -> None:
        """Set a __name__ to subclasses.

        >>> class MyS(ServiceManifest, service_name="my"):
        ...     x: str
        >>> s = MyS(x=1)
        >>> s.__class__.__service__
        'my'
        """
        super().__init_subclass__(**kwargs)
        cls.__service__ = service_name


class Runnable(Protocol):
    __service_name__: ClassVar[str]

    @property
    def name(self) -> Optional[str]:
        ...

    def args(self) -> List[str]:
        ...

    def pidfile(self) -> Path:
        ...

    def env(self) -> Optional[Dict[str, str]]:
        ...


class Address(ConstrainedStr):
    r"""Network address type <host or ip>:<port>.

    >>> class Cfg(BaseModel):
    ...     addr: Address
    >>> cfg = Cfg(addr="server:123")
    >>> cfg.addr
    'server:123'
    >>> cfg.addr.host, cfg.addr.port
    ('server', 123)

    >>> a = Address("server:123")
    >>> a.host, a.port
    ('server', 123)

    >>> Address("server")  # no validation
    'server'
    >>> Address.validate("server")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    pydantic.errors.StrRegexError: string does not match regex "(?P<host>[^\s:?#]+):(?P<port>\d+)"

    >>> Cfg(addr="server")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    pydantic.error_wrappers.ValidationError: 1 validation error for Cfg
    addr
      string does not match regex "(?P<host>[^\s:?#]+):(?P<port>\d+)" (type=value_error.str.regex; pattern=...)
    >>> Cfg(addr="server:ab")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    pydantic.error_wrappers.ValidationError: 1 validation error for Cfg
    addr
      string does not match regex "(?P<host>[^\s:?#]+):(?P<port>\d+)" (type=value_error.str.regex; pattern=...)
    """

    regex = re.compile(r"(?P<host>[^\s:?#]+):(?P<port>\d+)")

    @classmethod
    def validate(cls, value: str) -> Self:
        value = super().validate(value)
        return cls(value)

    @classmethod
    def get(cls, port: int) -> Self:
        host = socket.gethostbyname(socket.gethostname())
        if host.startswith("127."):  # loopback addresses
            host = socket.getfqdn()
        return cls.validate(f"{host}:{port}")

    @cached_property
    def host(self) -> str:
        m = self.regex.match(self)
        assert m
        return m.group("host")

    @cached_property
    def port(self) -> int:
        m = self.regex.match(self)
        assert m
        return int(m.group("port"))

    @classmethod
    def unspecified(cls) -> Self:
        return cls()
