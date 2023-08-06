"""Scrippy Core module."""


import os
import grp
import pwd
import time
import yaml
import logging
from scrippy_core.conf import Config
from scrippy_core import error_handler
from scrippy_core.history import History
from scrippy_core.arguments import Parser
from scrippy_core.workspace import Workspace
from scrippy_core.context import Context, PIDStack
from scrippy_core.log.debuglogger import DebugLogger
from scrippy_core.log import LogConfig, setLoggerClass
from scrippy_core.error_handler import ScrippyCoreError


def check_users(context):
  """
  Vérifie que l'utilisateur courant est autorisé à exécuter le script en comparant les déclarations "@user" dans le cartouche du script.

  Lève une ScrippyCoreError si l'utilisateur n'est pas autorisé.
  """
  user_id = os.geteuid()
  try:
    users = [line.split(':')[1].strip() for line in context.doc.splitlines() if line.strip().startswith("@user")]
    users = [pwd.getpwnam(user).pw_uid for user in users]
    if len(users) > 0 and user_id not in users:
      raise ScrippyCoreError('[BadUserError] Utilisateur non autorisé')
  except KeyError as erro:
    raise ScrippyCoreError(f"[UnknownUserError] Utilisateur inconnu: {str(erro)}") from erro
  except Exception as erro:
    err_msg = f"[{erro.__class__.__name__}] {erro}"
    logging.critical(err_msg)
    raise ScrippyCoreError(err_msg) from erro


def check_groups(context):
  """
  Vérifie que l'utilisateur courant est autorisé à exécuter le script en comparant les déclarations "@group" dans le cartouche du script.

  Lève une ScrippyCoreError si l'utilisateur ne fait pas partie des groupes autorisés.
  """
  user_groups = os.getgroups()
  try:
    groups = [line.split(':')[1].strip() for line in context.doc.splitlines() if line.strip().startswith("@group")]
    groups = [grp.getgrnam(group)[2] for group in groups]
    if len(groups) > 0:
      if not len([groups for g in user_groups if g in groups]) > 0:
        raise ScrippyCoreError("[BadGroupError] L'utilisateur ne fait pas partie des groupes autorisés")
  except KeyError as erro:
    raise ScrippyCoreError(f"[UnknownGroupError] Groupe inconnu: {str(erro)}") from erro
  except Exception as erro:
    err_msg = f"[{erro.__class__.__name__}] {erro}"
    logging.critical(err_msg)
    raise ScrippyCoreError(err_msg) from erro


def check_instances(context):
  """
  Vérifie que le nombre d'instances autorisées à être simultanément exécutées n'est pas atteint en comparant la déclaration @max_instance dans le cartouche du script et le nombr de PID retourné par la pidstack.

  Si le nombre d'instance est atteint, le script fera une pause jusqu'à ce que le nombre d'instance en cours d'exécution soit inférieur au nombre d'instances autorisées.
  Lorsque le nombre maximum d'instance autorisées n'est pas atetint, le script s'enregistre dans la pidstack et s'exécute.
  """
  sleep_step = 3
  bools = ["true", "1", "on"]
  try:
    max_instance = [line.split(':')[1].strip() for line in context.doc.splitlines() if line.strip().startswith("@max_instance")][0]
  except IndexError:
    max_instance = 0
  try:
    timeout = [line.split(':')[1].strip() for line in context.doc.splitlines() if line.strip().startswith("@timeout")][0]
  except IndexError:
    timeout = 0
  try:
    exit_on_wait = [line.split(':')[1].strip() for line in context.doc.splitlines() if line.strip().startswith("@exit_on_wait")][0]
  except IndexError:
    exit_on_wait = "False"
  try:
    exit_on_timeout = [line.split(':')[1].strip() for line in context.doc.splitlines() if line.strip().startswith("@exit_on_timeout")][0]
  except IndexError:
    exit_on_timeout = "False"
  pids = context.pidstack.get_pids()
  try:
    timeout = int(timeout)
    max_instance = int(max_instance)
    exit_on_timeout = exit_on_timeout.lower() in bools
    exit_on_wait = exit_on_wait.lower() in bools
    if max_instance > 0 and len(pids) > max_instance:
      logging.info(f"[+] En attente d'un creneau d'execution: {len(pids)}/{max_instance} [{timeout}s]")
      while len(pids) > max_instance and pids[0] != os.getpid():
        timeout -= sleep_step
        if timeout <= 0 and exit_on_timeout:
          raise Exception("TimeoutError: Delai d'attente depasse")
        if exit_on_wait:
          raise Exception(f"EagernessError: `exit_on_wait` positionne a {exit_on_wait}")
        pids = context.pidstack.get_pids()
        time.sleep(sleep_step)
  except Exception as erro:
    err_msg = f"[{erro.__class__.__name__}] {erro}"
    logging.critical(err_msg)
    raise ScrippyCoreError(err_msg) from erro


# ------------------------------------------------------------------------------
# INITIALISATION
# ------------------------------------------------------------------------------
conf_files = ["/etc/scrippy/scrippy.yml",
              os.path.expanduser("~/.config/scrippy/scrippy.yml"),
              "/usr/local/etc/scrippy/scrippy.yml"]

for conf_file in conf_files:
  if os.path.isfile(conf_file):
    with open(conf_file, mode="r", encoding="utf-8") as conf_file:
      scrippy_conf = yaml.load(conf_file, Loader=yaml.FullLoader)
      SCRIPPY_LOGDIR = scrippy_conf.get("env").get("logdir")
      SCRIPPY_HISTDIR = scrippy_conf.get("env").get("histdir")
      SCRIPPY_REPORTDIR = scrippy_conf.get("env").get("reportdir")
      SCRIPPY_TMPDIR = scrippy_conf.get("env").get("tmpdir")
      SCRIPPY_DATADIR = scrippy_conf.get("env").get("datadir")
      SCRIPPY_TEMPLATEDIR = scrippy_conf.get("env").get("templatedir")
      SCRIPPY_CONFDIR = scrippy_conf.get("env").get("confdir")

conf_keys = [SCRIPPY_LOGDIR,
             SCRIPPY_HISTDIR,
             SCRIPPY_REPORTDIR,
             SCRIPPY_TMPDIR,
             SCRIPPY_DATADIR,
             SCRIPPY_TEMPLATEDIR,
             SCRIPPY_CONFDIR]

for conf_key in conf_keys:
  if conf_key is None:
    raise ScrippyCoreError(f"Clef de configuration manquante: {conf_key}")

LogConfig.default_configuration()
arg_parser = Parser()
args = arg_parser.args
_log_file_enabled = True

if args.nolog:
  logging.getLogger().setLevel(logging.ERROR)

if args.debug:
  logging.warning("[+] Option --debug activee -> le niveau de log ne peut plus etre modifie")
  logging.getLogger().setLevel(logging.DEBUG)
  setLoggerClass(DebugLogger)

logging.debug(f"[+] Arguments : {vars(args)}")

if args.no_log_file:
  _log_file_enabled = False
  logging.warning("[+] Option --no-log-file activee -> pas de fichier de log, ni d'historique pour cette execution")

# Chargement et contrôle du fichier de configuration root
root_config = Config()

if root_config.has('log', 'level'):
  logging.info(f"[!] Configuration de la journalisation: {root_config.get('log', 'level').upper()}")
  logging.getLogger().setLevel(root_config.get('log', 'level').upper())

if root_config.has('log', 'file') and \
   not root_config.get('log', 'file', 'bool'):
  logging.warning("[+] Config log.file = False -> pas de fichier de log, ni d'historique pour cette execution")
  _log_file_enabled = False

if _log_file_enabled:
  LogConfig.add_file_handler()


class ScriptContext:
  """Contexte d'exécution du script."""

  def __init__(self, name, retention=50, workspace=False):
    """Initalisation du contexte."""
    self.name = name
    self.hist_enabled = True
    self.worskspace_enabled = workspace
    # La variable _context est nécessaire à getCurrentContext()
    # Touche pas à ça p'tit con©
    _context = Context.create(self.name)
    self.context = _context

    if self.context.root:
      self.context.config = root_config
    else:
      self.context.config = Config()
    self.context.config.register_secrets(self.context)
    arg_parser.register_secrets(self.context)

    if self.worskspace_enabled:
      self.workspace = Workspace(self.context.log_session_name)

    if _log_file_enabled:
      self.context.hist = History(retention=retention)
    else:
      self.hist_enabled = False

    check_users(self.context)
    check_groups(self.context)
    try:
      self.context.pidstack = PIDStack(self.name, SCRIPPY_TMPDIR)
      self.context.pidstack.register()
    except PermissionError as erro:
      err_msg = f"Erreur lors de la création de la pile des instances: [{erro.__class__.__name__}] {erro}"
      logging.critical(err_msg)
      raise ScrippyCoreError(err_msg) from erro
    check_instances(self.context)

  def __enter__(self):
    """Point d'entrée."""
    # La variable _context est nécessaire à getCurrentContext()
    # Touche pas à ça p'tit con©
    _context = self.context
    if self.hist_enabled:
      self.context.hist.__enter__()
    if self.worskspace_enabled:
      self.context.workspace_path = self.workspace.__enter__()
    return self.context

  def __exit__(self, kind, value, tb):
    """Point de sortie."""
    # La variable _context est nécessaire à getCurrentContext()
    # Touche pas à ça p'tit con©
    _context = self.context
    if self.worskspace_enabled:
      self.workspace.__exit__(kind, value, tb)
    if self.hist_enabled:
      self.context.hist.__exit__(kind, value, tb)
    self.context.pidstack.checkout()
    error_handler.handle_error(kind, value, tb)
