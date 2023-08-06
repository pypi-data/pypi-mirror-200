![Build Status](https://drone.mcos.nc/api/badges/scrippy/scrippy-api/status.svg) ![License](https://img.shields.io/static/v1?label=license&color=orange&message=MIT) ![Language](https://img.shields.io/static/v1?label=language&color=informational&message=Python)

![Scrippy, mon ami le scrangourou](./scrippy-api.png "Scrippy, mon ami le scrangourou")

# `scrippy_api`

Client d'_API ReST_ pour le cadriciel [`Scrippy`](https://codeberg.org/scrippy).

## Prérequis

### Modules Python

#### Liste des modules nécessaires

Les modules listés ci-dessous seront automatiquement installés.

- requests
- PyYAML
- jsonschema

## Installation

### Manuelle

```bash
git clone https://codeberg.org/scrippy/scrippy-api.git
cd scrippy-api.git
sudo python3 -m pip install -r requirements.txt
make install
```

### Avec `pip`

```bash
sudo pip3 install scrippy-api
```

### Utilisation

Le module `scrippy_api.api` fournit l'objet `Client` permettant d'interroger n'importe quelle [_API REST_ ](https://fr.wikipedia.org/wiki/Representational_state_transfer) de manière uniforme à l'aide de l'unique méthode `Client.request()`.

L'objet `Client` dispose d'une unique méthode `Client.request()` qui accepte de nombreux paramètres dont la plupart sont optionnels. Cependant certains paramètres optionnels peuvent devenir obligatoires en fonction de la méthode _HTTP_ utilisée pour la requête et du cas d'utilisation. _YMMV_.

La méthode `Client.request()` renvoie systématiquement un objet `requests.Response` (voir [la documentation](https://2.python-requests.org/en/master/user/advanced/#request-and-response-objects)) qui devra être traité par le script.

Les clefs comme les valeurs des paramètres seront automatiquement _encodés_ lorsque nécessaire.

En cas d'erreur (code _HTTP_ != 200), le client sort avec un code retour `1` et l'erreur est enregistrée dans le journal comme `critical`.
Ce comportement peut être inhibé lors de l'instanciation du client en positionnant le paramètre `exit_on_error` à `False`:

```python
from scrippy_api.api import Client
client = Client(exit_on_error=False)
```

Dans ce cas les éventuelles erreurs rencontrées apparaîtront dans le fichier de journalisation comme `warning`.

#### Paramètres

| Paramètre | Type | Utilité | Valeur par défaut |
| --------- | ---- | ------- | ----------------- |
| `params`  | Dictionnaire | Applicable à toutes les méthodes _HTTP_. Chacune des paires clef/valeur sera concaténée à l'URL. | `None` |
| `cookies` | Dictionnaire | Les _cookies_ à envoyer avec la requête | `None` |
| `timeout` | Entier | Délai d'attente avant d'interrompre la connexion | `None` |
| `headers` | Dictionnaire | Entêtes à envoyer avec la requête | `None` |
| `proxies` | Liste | Liste des serveurs mandataires à utiliser pour la connexion | `None` |
| `auth`    | Tuple | Nom d'utilisateur et mot de passe pour l'authentification _BASIC AUTH_ |
| `data`    | Dictionnaire | Données à envoyer avec la requête. Non applicable avec la méthode `GET` | `None` |
| `json`    | Dictionnaire | Données au format _JSON_ à envoyer avec la requête. Non applicable a la méthode `GET`. Utilisable lorsque `data` et `file` ne sont pas spécifiés | `None` |
| `files`   | Dictionnaire | Les fichiers à téléverser en _multipart_. Le dictionnaire prend la forme `{<nom fichier>: <fichier>}`  | `None` |
| `verify`   | Booléen/String | Vérifie permet la vérification du certificat SSL. Si `vérify` est positionnée à `False` aucune vérification n'est effectuée. `verify` accepte également une chaîne de caractères qui doit être soit le nom d'un fichier certificat soit le nom d'un répertoire qui contient les certificats. | `True` |

Méthodes _HTTP_ implémentées:

| Méthode HTTP | Utilité |
| ------------ | ------- |
| `GET`        | Récupérer une ressource ou une liste d'URI de ressources |
| `POST`       | Créer une ressource |
| `PUT`        | Remplacer ou créer une ressource  |
| `PATCH`      | Met à jour une ressource ou la créer si inexistante |
| `DELETE`     | Supprimer une ressource |



#### Exemples

##### URL avec paramètres

```python
from scrippy_api.api import Client
params = {"name": "Luiggi Vercotti", "password": "dead/parrot"}
client = Client()
response = client.request(method="GET", url="https://montypython.org/user", params=params)
```

L'URL appelée sera
```
https://montypython.org/user?name=Luiggi+Vercotti&password=dead%2Fparrot
```

##### Authentification de base (BASIC AUTH)

Authentification de base à l'aide des identifiants suivants:
- Utilisateur: `Luiggi Vercotti`
- Mot de passe: `dead/parrot`

```python
from scrippy_api.api import Client
auth = ("Luiggi Vercotti", "dead/parrot")
client = Client()
response = client.request(method="POST", url="https://montypython.org", auth=auth)
```

##### Envoi de données

Création de l'utilisateur `Luiggi Vercotti` dont le mot de passe est `dead/parrot`:

```python
from scrippy_api.api import Client
data = {"name": "Luiggi Vercotti", "password": "dead/parrot"}
client = Client()
response = client.request(method="POST", url="https://montypython.org/user", data=data)
```

##### Téléversement de fichiers

Téléversement des deux fichiers `./images/dead_parrot.png` et `./images/flying_circus.mp4`:

```python
from scrippy_api.api import Client
files = {"dead_parrot.png": open("./images/dead_parrot.png", "rb"), "flying_circus.mp4": open("./images/flying_circus.mp4", "rb")}
client = Client()
response = client.request(method="POST", url="https://montypython.org/upload", data=data)
```

##### Modification de ressource

Remplacement du mot de passe de l'utilisateur `Luiggi Vercotti`

```python
from scrippy_api.api import Client
auth = ("Luiggi Vercotti", "dead/parrot")
data = {"password": "live/parrot"}
params = {"name": "Luiggi Vercotti"}
client = Client()
response = client.request(method="PATCH",
                          url="https://montypython.org/user",
                          params=params,
                          data=data)
```

##### Téléchargement de fichiers

```python
from scrippy_api.api import Client
url = "https://monthy.python/inquisition.zip"
local_dir = "/home/luiggi.vercotti"
local_filename = "spanish_inquisition.zip"
client = Client()
if client.download(url, local_dir, local_filename):
  print("No one expects the Spanish inquisition")
```
