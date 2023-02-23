from abc import ABC, abstractmethod

from common.type import BiosVersion, CpuCpldVersion, BmcVersion, Sku, Platform


class CommandController(ABC):
    @property
    @abstractmethod
    def command(self) -> str:
        pass

    @property
    @abstractmethod
    def stdin(self) -> str:
        pass

    @property
    @abstractmethod
    def stdout(self) -> str:
        pass

    @property
    @abstractmethod
    def stderr(self) -> str:
        pass

    @property
    @abstractmethod
    def timeout(self) -> float:
        pass

    @abstractmethod
    def exec_command(self, command: str) -> bool:
        pass


class AdvanceCommandController(CommandController):
    @property
    @abstractmethod
    def exec_time(self) -> float:
        pass

    @property
    @abstractmethod
    def exit_code(self) -> int:
        pass


# ToDo


class TerminalCommandController(AdvanceCommandController):
    def __init__(self) -> None:
        pass

# ToDo


class ConsoleCommandController(CommandController):
    def __init__(self) -> None:
        pass


class Action:
    def __init__(self) -> None:
        self.controller = TerminalCommandController()

    @property
    def controller(self) -> TerminalCommandController:
        return self._controller

    @controller.setter
    def controller(self, controller: TerminalCommandController) -> None:
        if self.controller is not None:
            return
        self._controller = controller


class OnieAction(Action):
    pass


class LinuxAction(Action):
    def lspci(self) -> str:
        pass

    def get_bios_version(self) -> BiosVersion:
        pass

    def get_cpu_cpld_version(self) -> CpuCpldVersion:
        pass

    def get_sys_sku(self) -> Sku:
        pass

    def get_platform(self) -> Platform:
        pass

    def get_cpu_code_name(self) -> str:
        pass

    def get_os_version(self) -> str:
        pass


class BmcAction:
    @abstractmethod
    def get_bmc_version(self) -> BmcVersion:
        pass
