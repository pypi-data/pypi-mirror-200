"""Module de chargement de définition d'API."""

import yaml
import logging
from scrippy_api import ScrippyApiError


class ApiLoader:
  """L'objet ApiLoader permet le chargement d'une API définie à l'aide d'un fichier YAML."""

  def __init__(self):
    """Initialise la classe ApiLoader."""
    self.api = {}

  def _walk_api(self, dic, path):
    """Parcours la représentation de l'API passée en argument sous forme de dictionnaire."""
    for key, value in dic.items():
      if isinstance(value, list):
        for action_list in value:
          for action in action_list:
            ppath = ".".join(path)
            ppath = f"{ppath}.{action}"
            path.append(ppath)
            self.api[ppath] = action_list[action]
            path.pop()
      elif isinstance(value, dict):
        path.append(key)
        self._walk_api(value, path)
        path.pop()

  def load_api(self, api_definition):
    """Charge l'API à partir du fichier YAML passé en argument."""
    logging.debug("[+] Loading API")
    logging.debug(f" '-> {api_definition}")
    try:
      with open(api_definition, mode="r") as yaml_file:
        api_yaml = yaml.load(yaml_file, Loader=yaml.FullLoader)
      self._walk_api(dic=api_yaml, path=[])
    except Exception as err:
      err_msg = f"Unknown error: [{err.__class__.__name__}] {err}"
      raise ScrippyApiError(err_msg) from err

  def get_endpoint_info(self, endpoint):
    """
    Renvoi les informations du endpoint passé en argument.

    Les informations renvoyées sont un dictionnaire tel que:
    {"method": <HTTP METHOD>, "url": <URL>}
    """
    logging.debug(f"[+] Getting data for: {endpoint}")
    try:
      return self.api[endpoint]
    except KeyError as err:
      err_msg = f"Unknown endpoint: {endpoint}"
      raise ScrippyApiError(err_msg) from err
