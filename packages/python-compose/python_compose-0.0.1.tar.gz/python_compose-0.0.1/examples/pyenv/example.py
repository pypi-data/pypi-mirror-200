import pathlib

from python_compose import compose
from python_compose.unit.pyenv import PyEnvUnit

compose.compose(
    [
        PyEnvUnit(
            name=f"httpd_{i}",
            py_version=f"3.{9+i}",
            requirements=[],
            script_path=pathlib.Path("./httpd.py"),
            binary_args=[str(8080 + i)],
        )
        for i in range(3)
    ]
)
