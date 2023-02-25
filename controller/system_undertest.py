from common.type import ConsoleIp, SshIp, Account, SystemInfo
from common.base import Decoding
from controller.session import Console, Terminal, BmcTerminal


class SystemUnderTest():
    def __init__(self, console_ip: ConsoleIp) -> None:
        self.console_ip: ConsoleIp = console_ip
        self.x86_ip: SshIp = None
        self.bmc_ip: SshIp = None
        self.console: Console = None
        self.x86: Terminal = None
        self.bmc: Terminal = None
        self.config: dict = None
        self.system_info: SystemInfo = None
        self.update_config()

    @property
    def console_ip(self) -> ConsoleIp:
        return self._console_ip

    @console_ip.setter
    def console_ip(self, ip: ConsoleIp) -> None:
        self._console_ip = ip

    @property
    def x86_ip(self) -> SshIp:
        return self._x86_ip

    @x86_ip.setter
    def x86_ip(self, ip: SshIp) -> None:
        self._x86_ip = ip

    @property
    def bmc_ip(self) -> SshIp:
        return self._bmc_ip

    @bmc_ip.setter
    def bmc_ip(self, ip: SshIp) -> None:
        self._bmc_ip = ip

    def __str__(self) -> str:
        var = f"Console: {self.console_ip}\n"
        var += f"x86: {self.x86_ip}\n"
        var += f"bmc: {self.bmc_ip}"
        return var

    def connect_console(self) -> None:
        account = Account(
            ConsoleIp(
                self._console_ip.ip,
                self._console_ip.port),
            "administrator",
            "ufispace")
        self.console = Console(account)
        self.console.connect()

    def connect_x86(self) -> None:
        account = Account(
            SshIp(self.x86_ip.ip),
            "root",
            "ufispace")
        self.x86 = Terminal(account)
        self.x86.connect()

    def connext_bmc(self) -> BmcTerminal:
        account = Account(
            SshIp(self.bmc_ip.ip),
            "sysadmin",
            "superuser")
        self.bmc = BmcTerminal(account)
        self.bmc.connect()

    def update_x86_ip(self) -> None:
        self.x86_ip = self.console.get_ssh_ip()

    def update_bmc_ip(self) -> None:
        self.bmc_ip = self.console.get_bmc_ip()

    def update(self) -> None:
        self.update_x86_ip()
        self.update_bmc_ip()

    def connect_all(self) -> None:
        self.connect_console()
        self.connect_x86()
        self.connext_bmc()

    def update_config(self) -> None:
        self.config = Decoding.decode_config("common/config.json")
        self.platform = self.config["platform"]
        self.sku = self.config["sku"]
        self.console_ip = ConsoleIp(
            self.config["console_ip"]["ip"],
            self.config["console_ip"]["port"])


if __name__ == '__main__':
    pass
