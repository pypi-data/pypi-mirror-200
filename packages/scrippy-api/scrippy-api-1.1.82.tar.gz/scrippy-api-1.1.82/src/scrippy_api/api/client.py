"""Module facilitant l'utilisation d'API ReST."""


import os
import logging
import requests
from scrippy_api import ScrippyApiError


class Client:
  """
  Classe permettant l'utilisation d'API REST.

  https://fr.wikipedia.org/wiki/Representational_state_transfer.
  """

  def __init__(self, verify=True, exit_on_error=True):
    """
    Initialise la classe Client.

    :param method
    :param: verify: Vérifie le certificat SSL, defaults to True
    :exit_on_error: Lève immédiatement une erreur ScrippyApiError en cas d'erreur lors de la requête, defaults to True
    """
    self.exit_on_error = exit_on_error
    self.verify = verify
    self.session = requests.Session()
    if not self.verify:
      requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

  def download(self, url, local_path, filename=''):
    """
    Permet le téléchargement d'un fichier.

    :param url: L'UrL à partir de laquelle télécharger le fichier
    :param local_path: Le répertoire dans lequel sauvegarder le fichier
    :param filename: Le nom du fichier local
    """
    if len(filename) == 0:
      filename = url.split('/')[-1]
    filename = os.path.join(local_path, filename)
    logging.debug("[+] Downloading file")
    logging.debug(f" '-> From: {url}")
    logging.debug(f" '-> To: {filename}")
    try:
      with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(filename, 'wb') as dl_file:
          for chunk in response.iter_content(chunk_size=8192):
            dl_file.write(chunk)
      return True
    except Exception as err:
      if self.exit_on_error:
        err_msg = f"Request error: [{err.__class__.__name__}] {err}"
        raise ScrippyApiError(err_msg) from err
      else:
        logging.warning(f"Request error: [{err.__class__.__name__}] {err}")
        return response

  def request(self, method, url, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=None, proxies=None, json=None):
    """
    Permet d'exécuter une requête HTTP.

    :param  method
    :param: url: L'URL à atteindre
    :param: params: Les paramètres (GET) de la requête, defaults to None
    :param: data: Les paramètres (POST) de la requête, defaults to None
    :param: headers: Les entêtes de la requête, defaults to None
    :param: cookies: Les cookies de la requête, defaults to None
    :param: file: Le fichier envoyé (POST), defaults to None
    :param: auth: Les informations d'authentification (BASIC AUTH) sous forme d'un tuple (user, password), defaults to None
    :param: timeout: Le délai maximum à attendre, defaults to None
    :param: proxies: La liste des serveurs mandataires utilisés, defaults to None
    :param: json: JSON à envoyer dans le corps de la requête (POST), defaults to None
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    logging.debug("[+] Sending request to server")
    default_get_kwargs = {"params": params,
                          "timeout": timeout,
                          "headers": headers,
                          "cookies": cookies,
                          "proxies": proxies,
                          "auth": auth,
                          "verify": self.verify}
    default_post_kwargs = {"data": data, "json": json, "files": files}
    # TO BE IMPLEMENTED:
    #  "CONNECT": self._connect,
    #  "OPTIONS": self._options,
    #  "TRACE": self._trace,
    #  "HEAD": self._trace,
    methods = {"GET": {"method": self._get,
                       "kwargs": default_get_kwargs},
               "POST": {"method": self._post,
                        "kwargs": {**default_get_kwargs, **default_post_kwargs}},
               "PUT": {"method": self._put,
                       "kwargs": {**default_get_kwargs, **default_post_kwargs}},
               "DELETE": {"method": self._delete,
                          "kwargs": {**default_get_kwargs, **default_post_kwargs}},
               "PATCH": {"method": self._patch,
                         "kwargs": {**default_get_kwargs, **default_post_kwargs}}}
    try:
      response = None
      response = methods[method]["method"](url, **methods[method]["kwargs"])
      response.raise_for_status()
      return response
    except Exception as err:
      if self.exit_on_error:
        err_msg = f"Request error: [{err.__class__.__name__}] {err}"
        raise ScrippyApiError(err_msg) from err
      else:
        logging.warning(f"Request error: [{err.__class__.__name__}] {err}")
        return response

  def _get(self, url, **kwargs):
    return self.session.get(url, **kwargs)

  def _post(self, url, **kwargs):
    return self.session.post(url, **kwargs)

  def _head(self, url, **kwargs):
    return self.session.head(url, **kwargs)

  def _put(self, url, **kwargs):
    return self.session.put(url, **kwargs)

  def _delete(self, url, **kwargs):
    return self.session.delete(url, **kwargs)

  def _patch(self, url, **kwargs):
    return self.session.patch(url, **kwargs)
