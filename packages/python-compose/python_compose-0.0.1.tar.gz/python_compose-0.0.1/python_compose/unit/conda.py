import pathlib
import subprocess
import warnings
from typing import List, Optional, Union

from python_compose.unit.compose_unit import ComposeUnit


class CondaUnit(ComposeUnit):
    def __init__(
        self,
        name: str,
        requirements: Union[pathlib.Path, List[str]],
        script: List[str],
        working_dir: Optional[pathlib.Path] = None,
    ):
        self.name = name
        self.requirements = requirements
        self.script = script
        self.working_dir = working_dir

    def create(self) -> None:
        envs = [
            row.split()[0]
            for row in subprocess.check_output(["conda", "env", "list"]).decode().split("\n")[2:]
            if row
        ]
        if self.name in envs:
            warnings.warn(f"Skipping pyenv venv creation for {self.name}. Venv already exists.")
        else:
            subprocess.check_call(["conda", "create", "-n", self.name, "-y"])

    def install_requirements(self) -> None:
        if isinstance(self.requirements, list) and self.requirements:
            subprocess.check_call(["conda", "install", "-n", self.name] + self.requirements)
        elif isinstance(self.requirements, pathlib.Path):
            subprocess.check_call(
                ["conda", "install", "-n", self.name, "-f", str(self.requirements)]
            )

    def start(self) -> None:
        p = subprocess.Popen(
            ["conda", "run", "-n", self.name, "--no-capture-output"]
            + (["--cwd", str(self.working_dir)] if self.working_dir else [])
            + self.script
        )
        p.communicate()

    def clean(self) -> None:
        subprocess.check_call(["conda", "remove", "-n", self.name, "--all"])
