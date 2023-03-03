import socket
import re
from unittest.mock import MagicMock, patch


import pytest

from common.type import ConsoleIp, Account, SshIp
import controller.session as ss


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


is_intranet: bool = bool(re.search(r"10.58.\d{1,3}.\d{1,3}", get_ip_address()))


stub_console_ip = ConsoleIp("192.168.162.2", 5102)
stub_ssh_ip = SshIp("192.168.165.115")
stub_ssh_account = Account(stub_ssh_ip, "root", "ufispace")
stub_console_account = Account(stub_console_ip, "administrator", "ufispace")
stub_account_fail = Account(stub_console_ip, "xxx", "xxx")


@pytest.mark.skip
@pytest.mark.skipif(not is_intranet,
                    reason="skip the test if ip address is not intranet")
def test_console_connect() -> None:
    sut = ss.Console(stub_console_account)
    assert sut.is_connect is False
    sut.connect()
    assert sut.is_connect is True

    sut_fail = ss.Console(stub_account_fail)
    assert sut_fail.is_connect is False
    sut_fail.timeout = 2
    sut_fail.connect()
    assert sut_fail.is_connect is False


def test_console_flush_buffer() -> None:
    pass


def test_console_send() -> None:
    pass


def test_console_exec_command() -> None:
    def dummy_flush() -> None:
        pass
    mock_spawn = MagicMock()
    mock_spawn.expect.return_value = 1
    mock_spawn.before = b"Linux ubuntu 5.4.0-96-generic #109 SMP Mon Feb 7 01:17:35 PST 2022 x86_64 x86_64 x86_64 GNU/Linux\nroot@ubuntu:~#"

    sut = ss.Console(stub_console_account)
    sut.process = mock_spawn
    sut._flush_buffer = dummy_flush

    result = sut.exec_command("uname -a")
    print(result)


@pytest.mark.skip
@pytest.mark.skipif(not is_intranet,
                    reason="skip the test if ip address is not intranet")
def test_terminal_connect() -> None:
    sut = ss.Terminal(stub_ssh_account)
    assert sut.is_connect is False
    sut.connect()
    assert sut.is_connect is True


# ToDo: Session.Terminal test
if __name__ == "__main__":
    test_console_exec_command()
