import re
import time
from abc import ABC, abstractmethod

import paramiko
import pexpect

from common.type import Account, SshIp, CommandResult
from common.base import print_err


class Session(ABC):
    def __init__(self, account: Account, timeout: float = 15) -> None:
        self.account = account
        self.timeout = timeout
        self.process = None
        self.is_connect: bool = False

    @property
    def account(self) -> Account:
        return self._account

    @account.setter
    def account(self, account: Account) -> None:
        self._account = account

    @property
    def timeout(self) -> float:
        return self._timeout

    @timeout.setter
    def timeout(self, timeout: float) -> None:
        if timeout < 0:
            print_err("Timeout must >= 0")
            raise ValueError("Timeout must >= 0")
        self._timeout = timeout

    @property
    def is_connect(self) -> bool:
        if self.process is None:
            self._is_connect = False
        return self._is_connect

    @is_connect.setter
    def is_connect(self, status: bool) -> None:
        self._is_connect = status

    @property
    def process(self) -> bool:
        return self._process

    @process.setter
    def process(self, status: bool) -> None:
        self._process = status

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def exec_command(self, command: str, *args, **kwargs) -> CommandResult:
        pass


class Terminal(Session):
    def connect(self) -> None:
        try:
            self.process = paramiko.SSHClient()
            self.process.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.process.connect(
                self.account.ipv4.ip,
                self.account.ipv4.port,
                self.account.username,
                self.account.password,
                timeout=self.timeout)
            self.is_connect = True
        except Exception:
            self.is_connect = False
            print_err("X86 ssh connect fail")
            raise

    def disconnect(self) -> None:
        self.process.close()

    def exec_command(self, command: str, *args, **kwargs) -> CommandResult:
        result = CommandResult()
        result.command = command
        start = time.time()
        try:
            result.stdin, result.stdout, result.stderr = self.process.exec_command(
                command, args, kwargs)
        except Exception:
            print_err(f"fail exec_command: {command}")
            raise
        end = time.time()
        result.stdout = str(result.stdout.read(), encoding='UTF-8')
        result.stdin = str(result.stdin.read(), encoding='UTF-8')
        result.stderr = str(result.stderr.read(), encoding='UTF-8')
        result.exec_time = end - start
        return result


class Console(Session):
    def __init__(self, account: Account, timeout: float = 15) -> None:
        super().__init__(account, timeout)
        self._prompt = "root@ubuntu:~#"

    def connect(self) -> None:
        try:
            self.process = pexpect.spawn('ssh',
                                         ['-o',
                                          'StrictHostKeyChecking=no',
                                          '-o',
                                          'UserKnownHostsFile=/dev/null',
                                          '-l',
                                          self.account.username,
                                          self.account.ipv4.ip,
                                          '-p',
                                          str(self.account.ipv4.port)],
                                         timeout=self.timeout)
        except Exception:
            self.is_connect = False
            print_err("Terminal server login fail")
            raise

        match self.process.expect(["(?i)password:", pexpect.EOF, pexpect.TIMEOUT]):
            case 0:
                self.process.sendline(self.account.password)
                print('Terminal server Enter password')
                self.is_connect = self._is_connect_success()
            case _:
                self.is_connect = False
                print_err("Terminal server login timeout")
        return

    def _is_connect_success(self) -> bool:
        match self.process.expect(["Suspend Menu", pexpect.EOF, pexpect.TIMEOUT]):
            case 0:
                print("Terminal server login success")
                return True
            case _:
                print_err("Terminal server login timeout")
                return False

    def disconnect(self) -> None:
        self.process.expect(pexpect.EOF)
        self.process.close()

    def _flush_buffer(self) -> None:
        if self.process.before:
            self.process.expect(r'.+')
        return

    def login(self) -> None:
        self._flush_buffer()
        self.process.send("\r")

        while True:
            self._flush_buffer()
            self.process.send("\r")
            match self.process.expect(["ubuntu login", pexpect.EOF, pexpect.TIMEOUT], timeout=5):
                case 0:
                    break
                case _:
                    pass

        self.process.send("root\r")

        match self.process.expect(["(?i)password", pexpect.EOF, pexpect.TIMEOUT]):
            case 0:
                self.process.send("ufispace\r")
            case _:
                print('Login failed')
                return

        match self.process.expect([self._prompt, pexpect.EOF, pexpect.TIMEOUT]):
            case 0:
                return
            case _:
                print('Login failed')
                return

    def send(self, data: str) -> None:
        self._flush_buffer()
        self.process.send(data)
        return

    def exec_command(self, command: str, *args, **kwargs) -> CommandResult:
        self._flush_buffer()
        self.process.send(command + "\r")
        match self.process.expect([self._prompt, pexpect.EOF, pexpect.TIMEOUT], timeout=self.timeout):
            case 0:
                return str(self.process.after, encoding='UTF-8')
            case 1:
                raise ConnectionError
            case 2:
                raise TimeoutError

    def is_hardware_error(self) -> bool:
        self._flush_buffer()
        self.process.send("dmesg | grep -i \"hardware error\"\r")
        match self.process.expect(["(?i)hardware error", pexpect.EOF, pexpect.TIMEOUT], timeout=5):
            case 0:
                return True
            case _:
                return False

    def get_ssh_ip(self) -> SshIp:
        self._flush_buffer()
        self.process.send("ip r\r")
        self.process.expect(
            ["(?<=link src )(\\d{1,3}\\.){3}\\d{1,3}", pexpect.EOF, pexpect.TIMEOUT], timeout=5)
        return SshIp(str(self.process.after, encoding='UTF-8'))

    def get_bmc_ip(self) -> SshIp:
        self._flush_buffer()
        self.process.send("ipmitool lan print\r")
        self.process.expect(
            ["(IP Address\\s*\\:\\s)(\\d{1,3}\\.){3}\\d{1,3}", pexpect.EOF, pexpect.TIMEOUT], timeout=5)
        ip = re.search(
            "(\\d{1,3}\\.){3}\\d{1,3}", str(
                self.process.after, encoding='UTF-8')).group(0)
        return SshIp(ip)


if __name__ == "__main__":
    pass
