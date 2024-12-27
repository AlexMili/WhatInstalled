import subprocess
from abc import ABC, abstractmethod


def execute_command(
    cmd: str, stderr: int = subprocess.DEVNULL, return_stderr: bool = False
) -> str | None:
    try:
        output = subprocess.check_output(
            cmd,
            shell=True,
            stderr=stderr,
        )
    except subprocess.CalledProcessError as e:
        if return_stderr is True:
            decoded_out = e.output.decode("utf-8")
            return str(decoded_out)
        else:
            return None

    decoded_out = output.decode("utf-8")

    return str(decoded_out)


class BaseInstaller(ABC):
    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def list_cmd(self) -> str:
        raise NotImplementedError

    @property
    def outdated_cmd(self) -> str:
        raise NotImplementedError

    @property
    def available_cmd(self) -> str:
        raise NotImplementedError

    def __init__(self) -> None:
        self.packages: list[dict[str, str | None]] = []
        self.outdated: list[dict[str, str | None]] = []

    @abstractmethod
    def list_packages(self, include_latest: bool) -> list[dict[str, str | None]]:
        pass

    @abstractmethod
    def list_outdated(self) -> list[dict[str, str | None]]:
        pass

    def is_available(self) -> bool:
        return execute_command(self.available_cmd) is not None
