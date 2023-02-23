import abc

from common.type import BiosVersion, CpuCpldVersion, BmcVersion, Sku, Platform


class X86Action:
    @abc.abstractmethod
    def lspci(self) -> str:
        pass

    @abc.abstractmethod
    def get_bios_version(self) -> BiosVersion:
        pass

    @abc.abstractmethod
    def get_cpu_cpld_version(self) -> CpuCpldVersion:
        pass

    @abc.abstractmethod
    def get_bmc_version(self) -> BmcVersion:
        pass

    @abc.abstractmethod
    def get_os_version(self) -> str:
        pass

    @abc.abstractmethod
    def get_sys_sku(self) -> Sku:
        pass

    @abc.abstractmethod
    def get_platform(self) -> Platform:
        pass

    @abc.abstractmethod
    def get_cpu_code_name(self) -> str:
        pass


class IcelakeAction(X86Action):
    pass


class OnieAction:
    pass


class BmcAction:
    pass
