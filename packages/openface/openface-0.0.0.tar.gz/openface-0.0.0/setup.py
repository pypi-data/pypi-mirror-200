from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

import subprocess
import shlex


def compile():
    args = (
        'bash -c "'
        "git clone https://github.com/GuillaumeRochette/openface-backend.git"
        " && "
        "cd openface-backend"
        " && "
        "bash install.sh"
        " && "
        "mv build/bin .."
        " && "
        "cd .."
        " && "
        "rm -rf openface-backend"
        '"'
    )
    try:
        process = subprocess.run(
            args=shlex.split(args),
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        print(process.stdout)
    except subprocess.CalledProcessError as e:
        print(e.stdout)


class CustomDevelop(develop):
    def run(self):
        develop.run(self)
        compile()


class CustomInstall(install):
    def run(self):
        install.run(self)
        compile()


if __name__ == "__main__":
    setup(
        cmdclass={
            "develop": CustomDevelop,
            "install": CustomInstall,
        },
    )
