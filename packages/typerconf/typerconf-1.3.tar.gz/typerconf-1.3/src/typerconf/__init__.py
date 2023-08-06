"""The typerconf module and config subcommand"""

import appdirs
import json
import logging
import os
import sys
import typer
import typing

normalized_path = os.path.normpath(sys.argv[0])
basename = os.path.basename(normalized_path)
dirs = appdirs.AppDirs(basename)

class Config:
  """Navigates nested JSON structures by dot-separated addressing."""

  def __init__(self, json_data={}):
    """
    Constructs a config object to navigate from JSON data `json_data`.
    """
    self.__data = json_data

  def get(self, path: str = "") -> typing.Any:
    """
    Returns object at `path`.
    Example:
    - `path = "courses.datintro22.url"` and
    - Config contains `{"courses": {"datintro22": {"url": "https://..."}}}` 
      will return "https://...".

    Any part of the path that can be converted to an integer, will be converted 
    to an integer. This way we can access elements of lists too.
    """
    structure = self.__data

    if not path:
      return structure

    for part in path.split("."):
      try:
        part = int(part)
      except ValueError:
        pass

      try:
        structure = structure[part]
      except KeyError:
        raise KeyError(f"{part} along {path} doesn't exist")

    return structure

  def set(self, path: str, value: typing.Any):
    """
    Sets `value` at `path`. Any parts along the path that don't exist will be 
    created.

    Example:
    - `value = "https://..."`,
    - `path = "courses.datintro22.url"`
    will create `{"courses": {"datintro22": {"url": "https://..."}}}`.

    Any part of the path that can be converted to an integer, will be converted 
    to an integer. This way we can access elements of lists too. However, we 
    cannot create index 3 in a list if it doesn't exist.
    """
    structure = self.__data

    parts = path.split(".")
    for part in parts[:-1]:
      try:
        part = int(part)
      except ValueError:
        pass

      try:
        structure = structure[part]
      except KeyError:
        structure[part] = {}
        structure = structure[part]

    part = parts[-1]
    try:
      part = int(part)
    except ValueError:
      pass
    structure[part] = value

  def paths(self, from_root=""):
    """
    Returns all existing paths.

    The optional argument `from_root` is a path and the method return all 
    subpaths rooted at that point.
    """
    paths = []
    root = self.get(from_root)

    if isinstance(root, dict):
      for part in root:
        if from_root:
          path = f"{from_root}.{part}"
        else:
          path = part

        paths.append(path)
        paths += self.paths(from_root=path)
    elif isinstance(root, list):
      paths += [f"{from_root}.{x}" for x in range(len(root))]

    return paths
def add_config_cmd(cli: typer.Typer):
  """
  Add config command to Typer cli
  """
  path_arg = typer.Argument(...,
                            help="Path in config, e.g. 'courses.datintro22'. "
                                 "Empty string is root of config.",
                            autocompletion=complete_path_callback)
  value_arg = typer.Option([], "-s", "--set",
                           help="Values to store. "
                                "More than one value makes a list. "
                                "Values are treated as JSON if possible.")

  @cli.command(name="config")
  def config_cmd(path: str = path_arg,
                 values: typing.List[str] = value_arg):
    """
    Reads values from or writes values to the config.
    """
    if values:
      set(path, values)
    else:
      print_config(get(path), path)
def get(path: str = "") -> typing.Any:
  """
  Returns the value stored at `path` in the config.

  By default, `path = ""`, which returns the entire configuration as a Config 
  object.
  """
  conf = read_config()
  return conf.get(path)

def set(path: str, values: typing.List[typing.Any]):
  """
  Sets `value` at `path` in the config. `value` will be interpreted as JSON, if 
  conversion to JSON fails, it will be used as is.
  """
  conf = read_config()
  for i in range(len(values)):
    try:
      values[i] = json.loads(values[i])
    except json.decoder.JSONDecodeError:
      pass

  if len(values) == 1:
    values = values[0]

  conf.set(path, values)
  write_config(conf)
def read_config(conf_path=f"{dirs.user_config_dir}/config.json"):
  """
  Returns the config data structure (JSON).
  `conf_path` is an optional argument providing the path to the config file.
  """
  try:
    with open(conf_path) as conf_file:
      return Config(json.load(conf_file))
  except FileNotFoundError as err:
    logging.warning(f"Config file {conf_path} could not be found: {err}")
  except NotADirectoryError as err:
    logging.error(f"A part of the path is a file, but used as directory: {err}")
    raise err
  except json.decoder.JSONDecodeError as err:
    logging.warning(f"Config file {conf_path} could not be decoded: {err}")

  return Config()
def write_config(conf,
                 conf_path=f"{dirs.user_config_dir}/config.json"):
  """
  Stores the config data `conf` (extracts JSON) in the config file.
  `conf_path` is an optional argument providing the path to the config file.
  """
  conf_dir = os.path.dirname(conf_path)
  if not os.path.isdir(conf_dir):
    os.makedirs(conf_dir)

  with open(conf_path, "w") as conf_file:
    json.dump(conf.get(), conf_file)
def complete_path(initial_path: str, conf: Config = None):
  """
  Returns all valid paths in the config starting with `initial_path`.
  If `conf` is not None, use that instead of the actual config.
  """
  if not conf:
    conf = Config(get())

  return list(filter(lambda x: x.startswith(initial_path),
                     conf.paths()))
def complete_path_callback(initial_path: str):
  return complete_path(initial_path)
def print_config(conf, path=""):
  """
  Prints the config tree contained in `conf` to stdout.
  Optional `path` is prepended.
  """
  try:
    for key in conf.keys():
      if path:
        print_config(conf[key], f"{path}.{key}")
      else:
        print_config(conf[key], key)
  except AttributeError:
    print(f"{path} = {conf}")

def main():
  cli = typer.Typer()
  add_config_cmd(cli)
  cli()

if __name__ == "__main__":
  main()
