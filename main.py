#!/usr/bin/env python
import common.base as Base
import controller.session as s
import common.type as Type
import controller.system_undertest as Sut

import pexpect
import paramiko


if __name__ == "__main__":
    cip: Type.ConsoleIp = Type.ConsoleIp(ip="192.168.162.2", port=5102)
    dut = Sut.SystemUnderTest(cip)
    dut.connect_console()
    dut.update()
    dut.connect_x86()
    print(dut.x86.lspci())
    print(dir(dut))
