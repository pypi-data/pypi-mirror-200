import os
import pathlib
import shutil
import subprocess
import warnings
from typing import List, Union

from python_compose.unit.compose_unit import ComposeUnit


class PyEnvUnit(ComposeUnit):
    def __init__(
        self,
        name: str,
        py_version: str,
        requirements: Union[pathlib.Path, List[str]],
        script_path: pathlib.Path,
        binary_args: List[str],
    ):
        self.name = name
        self.py_version = py_version
        self.requirements = requirements
        self.script_path = script_path
        self.binary_args = binary_args
        self.pyenv_root = pathlib.Path(subprocess.check_output(["pyenv", "root"]).decode().strip())
        self.env_path = self.pyenv_root / "versions" / self.name
        self.python_path = self.pyenv_root / "versions" / self.name / "bin" / "python"

    def create(self) -> None:
        subprocess.check_call(["pyenv", "install", self.py_version, "--skip-existing"])
        if os.path.exists(self.env_path):
            warnings.warn(f"Skipping pyenv venv creation for {self.name}. Venv already exists.")
        else:
            subprocess.check_call(["pyenv", "virtualenv", "-p", self.py_version, self.name])

    def install_requirements(self) -> None:
        subprocess.check_call([str(self.python_path), "-m", "pip", "install", "-U", "pip"])
        if isinstance(self.requirements, list) and self.requirements:
            subprocess.check_call(
                [str(self.python_path), "-m", "pip", "install"] + self.requirements
            )
        elif isinstance(self.requirements, pathlib.Path):
            subprocess.check_call(
                [str(self.python_path), "-m", "pip", "install", "-r", str(self.requirements)]
            )

    def start(self) -> None:
        p = subprocess.Popen([str(self.python_path), str(self.script_path)] + self.binary_args)
        p.communicate()

    def clean(self) -> None:
        shutil.rmtree(self.env_path)
