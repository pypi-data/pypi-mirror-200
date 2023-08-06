from pathlib import Path

import srsly
from confection import Config

PROJECT_FILE = "kewr_config.yaml"


def check_dependencies(stage_data):
    return all([Path(d).exists() for d in stage_data["deps"]])


def check_outputs(stage_data):
    return all([Path(d).exists() for d in stage_data["outs"]])


def is_config_valid(data):
    NECESSARY_FORMAT = {
        "name": "str",
        "help": "str",
        "cmd": "str",
        "deps": [],
        "outs": [],
    }
    stages = data["stages"]
    try:
        for s in stages:
            if not all([i in s.keys() for i in NECESSARY_FORMAT.keys()]):
                return False
            for k, v in s.items():
                if not isinstance(v, type(NECESSARY_FORMAT[k])):
                    return False
        return True
    except Exception as e:
        print(f"config not valid, key error {e}")
        return False


def load_config():
    file_path = Path().cwd() / PROJECT_FILE
    try:
        config = srsly.read_yaml(file_path)
        assert is_config_valid(config), "config format validation error"
        config = substitute_project_variables(config)
        return config
    except FileNotFoundError as e:
        print(e)
    except AssertionError as e:
        print(e)


def substitute_project_variables(config, key="vars"):
    """Interpolate variables in the project file using the config system.
    config (Dict[str, Any]): The project config.
    key (str): Key containing variables in project config.
    RETURNS (Dict[str, Any]): The interpolated project config.
    """
    config.setdefault(key, {})
    cfg = Config({"project": config, key: config[key]})
    cfg = Config().from_str(cfg.to_str())
    interpolated = cfg.interpolate()
    return dict(interpolated["project"])


EXAMPLE = """variables:
  var1: x

stages:
  - name: stage1
    help: "description of what the stage does"
    cmd: python ex.py
    deps: 
      - dla
    outs:
      - fjk
  - name: stage2
    help: "description of what the stage does"
    cmd: python ex.py
    deps: 
      - dla
    outs:
      - fjk
    """
