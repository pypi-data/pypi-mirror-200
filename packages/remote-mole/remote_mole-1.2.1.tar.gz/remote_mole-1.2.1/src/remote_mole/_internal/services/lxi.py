import os
import re
import subprocess

from PIL import Image


class LXIDevice:
    @staticmethod
    def _system_command(cmd):
        return subprocess.check_output(cmd, shell=True, text=True)

    @staticmethod
    def _get_address(name):
        cmd = 'lxi discover'
        stdout = LXIDevice._system_command(cmd)
        found_str = re.search(f'Found.*{name}.*', stdout).group(0)
        return re.search('address.*', found_str).group(0)[len('address '):]

    @staticmethod
    def _get_name(address):
        cmd = 'lxi discover'
        stdout = LXIDevice._system_command(cmd)
        found_str = re.search(f'Found.*{address}.*', stdout).group(0)
        return re.search('\".*\"', found_str).group(0)[1:-1]

    def __init__(self, name=None, address=None):
        if address is not None:
            self.address = address
            try:
                self.name = self._get_name(address)
            except AttributeError:
                raise RuntimeError('Device not connected')
        elif name is not None:
            try:
                self.address = self._get_address(name)
                self.name = self._get_name(self.address)
            except AttributeError:
                raise RuntimeError('Device not connected')
        else:
            raise ValueError('Need either address or name of the device')

    def _is_connected(self):
        return self.address == self._get_address(self.address)

    def capture_screenshot(self, path='~/remote_screenshot.png'):
        path = os.path.expanduser(path)
        path_no_ext = os.path.splitext(path)[0]
        path_bmp = path_no_ext + '.bmp'

        cmd = f'lxi screenshot -a {self.address} {path_bmp}'
        self._system_command(cmd)

        Image.open(path_bmp).save(path)

        return path

    def send_command(self, command):
        cmd = f'lxi scpi -a {self.address} "{command}"'
        return self._system_command(cmd)
