"""
Ce module propose une interface à la configuration des scripts basés sur le cadriciel Scrippy.

Cette interface permet:
- Le chargement et la prise en compte automatique d'un fichier de configuration
- Le controle de la validité de la configuration
"""

import os
import logging
import configparser
import scrippy_core
from scrippy_core.context import Context
from scrippy_core.scriptinfo import ScriptInfo
from scrippy_core.error_handler import ScrippyCoreError


class Config:
  """
  Config est la classe principale du module scrippy_core.conf.

  Elle permet le chargement automatique de la configuration et, si la *docstring* du script comporte un ensemble de
  ligne commençant par `@conf`, permet le contrôle de validité de la configuration du fichier de configuration.

  Les lignes des déclarations du format de configuration doivent respecter le formalisme suivant:

  @conf:<section>|<clé>|<type_valeur>

  <type_valeur> doit être l'un des types reconnus suivants:
  - str (chîne de caractères)
  - int (entier)
  - float (nombre à virgule flotante)
  - bool (booléen)

  Exemple:
  --------
  À partir de la déclaration suivante:

  @conf:log/level/str
  @conf:database/port/int
  @conf:sql/verbose/bool

  Le fichier de configuration suivant sera vérifié:
  [log]
    level = ERROR
  [database]
    port = 5432
  [sql]
    verbose = True
  """

  def __init__(self):
    """Initialise l'instance.

    Aucun contrôle des valeurs des paramètres n'est effectué.
    Seule la structure de la configuration (présence des sections et clés décrites par l'ensemble `@conf`) est vérifiée. Un contrôle du type des clés déclarées est également effectué.
    """
    self.conf = configparser.ConfigParser()
    context = Context.get_current()
    if context is not None:
      script_name = context.name
      self.doc = context.doc
    else:
      script_name = ScriptInfo.get_script_name()
      self.doc = ScriptInfo.get_doc()
    self.config_filename = os.path.join(scrippy_core.SCRIPPY_CONFDIR,
                                        f"{script_name}.conf")
    if os.path.isfile(self.config_filename):
      logging.info(f"[+] Chargement du fichier de configuration {self.config_filename}")
      self.conf.read(self.config_filename)
    else:
      logging.info(f"[+] Pas de fichier de configuration {self.config_filename}")
    self._check()

  def _check(self):
    """
    Contrôle de la configuration.

    Cette méthode est appelée automatiquement par le constructeur si l'argument optionnel 'params' est fourni.
    Cette méthode n'a pas à être appelée autrement que par le constructeur de la classe Config
    """
    context = Context.get_current()
    if context is None:
      context = Context.get_root_context()
    logging.info("[+] Controle de la configuration")
    conf_lines = []
    conf_lines = [line.split(':')[1].strip() for line in self.doc.splitlines() if line.strip().startswith("@conf")]
    for line in conf_lines:
      try:
        section, key, param_type, secret = line.split("|")
        value = self.get(section, key, param_type)
        if secret.lower() == "true":
          context.vault.add(value)
      except ValueError:
        section, key, param_type = line.split("|")
        value = self.get(section, key, param_type)
      logging.debug(f"[{section}][{key}] = {value} [OK]")
    return True

  def register_secrets(self, context):
    logging.info("[+] Enregistrement des secrets (conf)")
    conf_lines = []
    conf_lines = [line.split(':')[1].strip() for line in self.doc.splitlines() if line.strip().startswith("@conf")]
    for line in conf_lines:
      try:
        section, key, param_type, secret = line.split("|")
        value = self.get(section, key, param_type)
        if secret.lower() == "true":
          context.vault.add(value)
      except ValueError:
        pass

  def get_section(self, section):
    """
    Renvoie l'ensemble des paires clef/valeur de la section passée en argument.

    Lève une  si la section demandée n'existe pas.
    """
    sec = {}
    try:
      for key in self.conf[section]:
        sec[key] = self.conf[section][key]
      return sec
    except configparser.NoSectionError as err:
      err_msg = f"Section inconnue: [{section}]"
      logging.critical(err_msg)
      raise ScrippyCoreError(err_msg) from err

  def get(self, section, key, param_type='str'):
    """
    Renvoie la valeur d'une clef dont le nom et la section sont passées en argument.

    À moins que le paramètre 'param_type' soit positionné à l'une des valeurs autorisées (str (défaut), int, float ou bool), le type renvoyé est systématiquement une chaine de caractère.
    """
    try:
      return {'int': self.conf.getint,
              'float': self.conf.getfloat,
              'bool': self.conf.getboolean,
              'str': self.conf.get}[param_type](section, key)
    except configparser.NoOptionError as err:
      err_msg = f"Parametre inconnu: [{section}][{key}]"
      logging.critical(err_msg)
      raise ScrippyCoreError(err_msg) from err
    except configparser.NoSectionError as err:
      err_msg = f"Section inconnue: [{section}]"
      logging.critical(err_msg)
      raise ScrippyCoreError(err_msg) from err
    except ValueError as err:
      err_msg = f"Erreur de type: [{section}][{key}] n'est pas de type '{param_type}'"
      logging.critical(err_msg)
      raise ScrippyCoreError(err_msg) from err
    except KeyError as err:
      err_msg = f"Erreur d'usage: Type de parametre inexistant: '{param_type}'"
      logging.critical(err_msg)
      raise ScrippyCoreError(err_msg) from err

  def has(self, section, key):
    """Renvoie True si la clé section.key existe dans la config."""
    return self.conf.has_option(section, key)
