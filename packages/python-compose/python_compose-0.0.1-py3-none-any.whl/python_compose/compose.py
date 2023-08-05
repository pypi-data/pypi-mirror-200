import argparse
import multiprocessing
import pathlib
from typing import List, cast

from python_compose.spec import Unit, YamlSpec
from python_compose.unit.compose_unit import ComposeUnit
from python_compose.unit.conda import CondaUnit
from python_compose.unit.pyenv import PyEnvUnit
from python_compose.unit.venv import VenvUnit


def runUnit(unit: ComposeUnit, clean: bool = False) -> None:
    if clean:
        unit.clean()
    unit.create()
    unit.install_requirements()
    unit.start()


def compose(units: List[ComposeUnit], clean: bool = False) -> None:
    with multiprocessing.Pool(len(units)) as p:
        p.starmap(runUnit, ((unit, clean) for unit in units))


def from_yaml(yaml_path: pathlib.Path) -> List[Unit]:
    return cast(YamlSpec, YamlSpec.parse_file(yaml_path)).units


def pydantic_to_units(units: List[Unit]) -> List[ComposeUnit]:
    ret: List[ComposeUnit] = []
    for unit in units:
        kwargs = {k: v for k, v in unit.dict().items() if k != "unit_type"}
        if unit.unit_type == "conda":
            ret.append(CondaUnit(**kwargs))
        elif unit.unit_type == "pyenv":
            ret.append(PyEnvUnit(**kwargs))
        elif unit.unit_type == "venv":
            ret.append(VenvUnit(**kwargs))
        else:
            raise ValueError(f"Invalid unit type {unit.unit_type} passed!")
    return ret


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config_path", type=pathlib.Path)
    args = parser.parse_args()

    if cast(pathlib.Path, args.config_path).suffix in [".yml", ".yaml"]:
        parsed_units = from_yaml(args.config_path)
        units = pydantic_to_units(parsed_units)
        compose(units=units)
    else:
        raise ValueError("Invalid config type passed. Currently, only yaml is supported.")
