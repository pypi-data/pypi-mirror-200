from __future__ import print_function
from __future__ import unicode_literals
from netmiko.cisco_base_connection import CiscoSSHConnection
import time
import re
from netmiko import log

class LancomRouterSSH(CiscoSSHConnection):
    def __init__(self, *args, **kwargs):
        default_enter = kwargs.get('default_enter')
        kwargs['default_enter'] = '\r\n' if default_enter is None else default_enter
        super(LancomRouterSSH, self).__init__(*args, **kwargs)

    def session_preparation(self):
        self._test_channel_read()
        self.set_base_prompt()
        # Clear the read buffer
        time.sleep(0.3 * self.global_delay_factor)
        self.clear_buffer()
