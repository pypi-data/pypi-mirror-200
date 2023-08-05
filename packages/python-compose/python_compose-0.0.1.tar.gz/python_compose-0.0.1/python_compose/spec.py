import pathlib
from typing import Annotated, List, Literal, Optional, Union

from pydantic import BaseModel, Field
from pydantic_yaml import YamlModelMixin


# TODO: Add classmethods to convert these to their a
# TODO: Move models to the associated unit class
class CondaUnitModel(BaseModel):
    unit_type: Literal["conda"]
    name: str
    requirements: Union[pathlib.Path, List[str]] = []
    script: List[str]
    working_dir: Optional[str] = None


class PyEnvUnitModel(BaseModel):
    unit_type: Literal["pyenv"]
    name: str
    py_version: str
    requirements: Union[pathlib.Path, List[str]] = []
    script_path: pathlib.Path
    binary_args: List[str]


class VenvUnitModel(BaseModel):
    unit_type: Literal["venv"]
    name: str
    env_dir: pathlib.Path
    requirements: Union[pathlib.Path, List[str]] = []
    script_path: pathlib.Path
    binary_args: List[str]


Unit = Annotated[
    Union[CondaUnitModel, PyEnvUnitModel, VenvUnitModel], Field(discriminator="unit_type")
]


# We have this class be separate from the yaml model so we can support
# toml, json, etc.
class Spec(BaseModel):
    units: List[Unit]


class YamlSpec(YamlModelMixin, Spec):
    pass
