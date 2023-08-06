from __future__ import print_function
from __future__ import unicode_literals
from netmiko.cisco_base_connection import CiscoSSHConnection
import time
import re
from netmiko import log

class LancomRouterSSH(CiscoSSHConnection):

    log.info("hier")
    def session_preparation(self):
        log.info("da")
        #self._test_channel_read()
        self.set_base_prompt()
        log.info("nochmal")
        # Clear the read buffer
        time.sleep(3 * self.global_delay_factor)
        self.clear_buffer()

    def check_enable_mode(self, *args, **kwargs):
        raise AttributeError("Accedian devices do not support enable mode!")

    def enable(self, *args, **kwargs):
        raise AttributeError("Accedian devices do not support enable mode!")

    def exit_enable_mode(self, *args, **kwargs):
        raise AttributeError("Accedian devices do not support enable mode!")

    def check_config_mode(self):
        """Accedian devices do not have a config mode."""
        return False

    def config_mode(self):
        """Accedian devices do not have a config mode."""
        return ''

    def exit_config_mode(self):
        """Accedian devices do not have a config mode."""
        return ''

    def set_base_prompt(self, pri_prompt_terminator='>', alt_prompt_terminator=r'#',
                        delay_factor=2):
        #self.write_channel("\r")
        self.read_channel()
        print(pri_prompt_terminator + " Test")
        #pri_prompt_terminator = '>'
        print(pri_prompt_terminator + " Test")
        """Sets self.base_prompt: used as delimiter for stripping of trailing prompt in output."""
        #super(LancomRouterSSH, self).set_base_prompt(pri_prompt_terminator=pri_prompt_terminator,
        #                                         alt_prompt_terminator=alt_prompt_terminator,
        #                                         delay_factor=delay_factor)
        return self.base_prompt

    def set_base_prompt2(self, pri_prompt_terminator='>\t', alt_prompt_terminator=')\t',
                        delay_factor=0):
        log.info("in set_base_prompt")
        """Check if at shell prompt root@ and go into CLI."""
        delay_factor = self.select_delay_factor(delay_factor=0)
        count = 0
        cur_prompt = ''
        while count < 50:
            self.write_channel(self.RETURN)
            time.sleep(.1 * delay_factor)
            cur_prompt = self.read_channel()
            if re.search(r'>\s', cur_prompt):
                #self.write_channel("cli" + self.RETURN)
                log.info(cur_prompt)
                pri_prompt_terminator='> '
                log.info("aha")
                time.sleep(.3 * delay_factor)
                self.clear_buffer()
                break
            #elif '>' in cur_prompt or '#' in cur_prompt:
            #    break
        count += 1
        """Sets self.base_prompt: used as delimiter for stripping of trailing prompt in output."""
        super(LancomRouterSSH, self).set_base_prompt(pri_prompt_terminator=pri_prompt_terminator,
                                                 alt_prompt_terminator=alt_prompt_terminator,
                                                 delay_factor=delay_factor)
        return self.base_prompt

    def save_config(self, cmd='', confirm=True, confirm_response=''):
        """Not Implemented"""
        raise NotImplementedError
