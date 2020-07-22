# -*- coding: utf-8 -*-
# Python 3.8.2
# Author: ZER0-Nu1L

import pexpect
import sys
import os
# pip3 install pexpect


def scp_getfile(remoteIP, targetFile, StorageCata, port=50022, remoteUser="root", password="***********"):
    # os.system('scp -P "%d" "%s"@"%s:%s" "%s"' % (port, remoteUser, remoteIP, targetFile, StorageCata))

    transport_sh = pexpect.spawn('scp -P "%d" "%s"@"%s:%s" "%s"' %
                                 (port, remoteUser, remoteIP, targetFile, StorageCata))
    try:
        i = transport_sh.expect(
            ['password:', 'password: ', 'continue connecting (yes/no)?'])
        if (i == 0 or i == 1):
            transport_sh.sendline(password)
        elif i == 1:
            transport_sh.sendline('yes')
            transport_sh.expect('password:')
            transport_sh.sendline(password)
    except pexpect.EOF:
        transport_sh.close()
        print("pexpect.EOF")
    else:
        with open('transport.log', 'ab') as fout:
            # pexpect Info -> transport.log || sys.stdout
            res = transport_sh.read()
            fout.write(res)
            transport_sh.expect(pexpect.EOF)
            transport_sh.close()
    return res


if __name__ == '__main__':
    remoteIP = "xxx.xxx.xxx.xxx"
    targetFile = "~/test"
    StorageCata = "."
    scp_getfile(remoteIP, targetFile, StorageCata)
