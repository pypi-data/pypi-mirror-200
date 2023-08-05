import pathlib
import shutil
import subprocess
from typing import List, Union
from venv import EnvBuilder

from python_compose.unit.compose_unit import ComposeUnit


class VenvUnit(ComposeUnit):
    def __init__(
        self,
        name: str,
        env_dir: pathlib.Path,
        requirements: Union[pathlib.Path, List[str]],
        script_path: pathlib.Path,
        binary_args: List[str],
    ):
        self.name = name
        self.env_dir = env_dir
        self.env_path = self.env_dir / self.name
        self.python_path = self.env_path / "bin/python"
        self.requirements = requirements
        self.script_path = script_path
        self.binary_args = binary_args

    def create(self) -> None:
        self.env = EnvBuilder(
            system_site_packages=True, clear=False, with_pip=True, upgrade_deps=True
        )
        self.env.create(self.env_path)

    def install_requirements(self) -> None:
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
