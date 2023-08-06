import io
import os
import sys
from sys import platform
import subprocess
from setuptools.command.build_py import build_py
import shutil
import tarfile
from urllib.request import urlopen

CUSTOM_COMMANDS = [['echo', f'DO NOT SUBMIT: {os.path.dirname(__file__)}']]


def get_virtualenv_path():
    """Used to work out path to install compiled binaries to."""
    if hasattr(sys, 'real_prefix'):
        return sys.prefix

    if hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix:
        return sys.prefix

    if 'conda' in sys.prefix:
        return sys.prefix

    return None


class InstallCustomDeps(build_py):

    def _install_prometheus(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        tar_base_path = 'launch/prometheus'
        if platform == "linux" or platform == "linux2":
            download_url = 'https://github.com/prometheus/prometheus/releases/download/v2.43.0/prometheus-2.43.0.linux-amd64.tar.gz'  # noqa: E501
            extracted_dir = 'prometheus-2.43.0.linux-amd64'
        elif platform == "darwin":
            download_url = 'https://github.com/prometheus/prometheus/releases/download/v2.43.0/prometheus-2.43.0.darwin-amd64.tar.gz'  # noqa: E501
            extracted_dir = 'prometheus-2.43.0.darwin-amd64'
        else:
            raise ValueError(
                f'launch CLI is not supported for platform: {platform}')
        final_binary_path = os.path.join(dir_path, tar_base_path, 'prometheus')
        final_yaml_path = os.path.join(dir_path, tar_base_path,
                                       'prometheus.yml')
        if (os.path.exists(final_binary_path)
                and os.path.exists(final_yaml_path)):
            # Already exist we can just return. This really only happens with
            # local development.
            return

        response = urlopen(download_url)
        tar_bytes = io.BytesIO(response.read())

        with tarfile.open(fileobj=tar_bytes) as f:
            f.extractall(os.path.join(dir_path, tar_base_path))

        if not os.path.exists(final_binary_path):
            shutil.move(
                os.path.join(dir_path, tar_base_path, extracted_dir,
                             'prometheus'),
                os.path.join(dir_path, tar_base_path))
        if not os.path.exists(final_yaml_path):
            shutil.move(
                os.path.join(dir_path, tar_base_path, extracted_dir,
                             'prometheus.yml'),
                os.path.join(dir_path, tar_base_path))

        shutil.rmtree(os.path.join(dir_path, tar_base_path, extracted_dir))

    def _run_custom_commands(self, command_list):
        print('Running command: %s' % command_list)
        p = subprocess.Popen(command_list,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        # Can use communicate(input='y\n'.encode()) if the command run requires
        # some confirmation.
        stdout_data, _ = p.communicate()
        print('Command output: %s' % stdout_data)
        if p.returncode != 0:
            raise RuntimeError('Command %s failed: exit code: %s' %
                               (command_list, p.returncode))

    def run(self) -> None:
        self._install_prometheus()
        build_py.run(self)
