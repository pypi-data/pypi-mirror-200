"""Python library bindings for the Spectre password manager"""
import enum
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from typing import Union


__title__ = "spectrepy"
__summary__ = "Python bindings for the Spectre Password Manager"
__version__ = "0.1.0"
__url__ = "https://github.com/enpaul/spectrepy/"
__license__ = "MIT"
__authors__ = ["Ethan Paul <24588726+enpaul@users.noreply.github.com>"]

__all__ = [
    "__title__",
    "__summary__",
    "__version__",
    "__url__",
    "__license__",
    "__authors__",
    "SpectrePasswordType",
    "SpectreAlgorithmVersion",
    "SpectrePassword",
    "Spectre",
    "generate",
    "get_version",
]


class SpectrePasswordType(enum.Enum):
    X = "maximum"
    L = "long"
    M = "medium"
    B = "basic"
    S = "short"
    I = "pin"
    N = "name"
    P = "phrase"
    K = "key"


class SpectreAlgorithmVersion(enum.Enum):
    V0 = 0
    V1 = 1
    V2 = 2
    V3 = 3


@dataclass(frozen=True)
class SpectrePassword:
    site: str
    identicon: str
    password_type: SpectrePasswordType
    username: str
    algorithm_version: SpectreAlgorithmVersion
    context: str


def generate(*args, **kwargs) -> SpectrePassword:
    return Spectre(*args, **kwargs).generate()


def get_version(*args, **kwargs) -> str:
    return Spectre(*args, **kwargs).version


def get_path(*args, **kwargs) -> Path:
    return Spectre(*args, **kwargs).path


class Spectre:
    def __init__(self, binary: Optional[Union[str, Path]] = None):
        self._path: Path
        self._version: str

        self._path = (
            Path(binary).resolve() if binary is not None else self._find_binary()
        )
        self._version = self._fetch_version()

    @property
    def version(self) -> str:
        return self._version

    @property
    def program(self) -> str:
        return self._program

    @property
    def path(self) -> Path:
        return self._path

    @staticmethod
    def _find_binary() -> Path:
        binary = shutil.which("spectre") or shutil.which("mpw")

        if not binary:
            raise RuntimeError
        return Path(binary)

    def generate(self) -> SpectrePassword:
        pass

    def _call(self, *args, raise_errors: bool = True) -> subprocess.CompletedProcess:
        result = subprocess.run([str(self._path)] + [*args], capture_output=True)

        if result.returncode != 0 and raise_errors:
            raise RuntimeError
        return result

    def _fetch_version(self) -> str:
        out = self._call("-h")
        raw = out.stderr.decode().split("\n")[0].strip().split(" ")
        version = raw[-1]
        return version
