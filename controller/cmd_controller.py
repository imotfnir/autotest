from common.type import BiosVersion, CpuCpldVersion, Sku, Platform
from controller.session import Session


class CommandSet:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.exec_command = self.session.exec_command

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


class TestPatternController:
    pass
