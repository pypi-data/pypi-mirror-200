"""Le sous-module scrippy_core.log fournit les objets nécessaires à la gestion des fichiers de journalisation."""
import os
import sys
import logging
import coloredlogs
import scrippy_core
from scrippy_core.context import Context
from scrippy_core.log.infralogger import InfraLogger


def setLoggerClass(klass):
  """https://stackoverflow.com/questions/51938027/python-3-7-logging-setloggerclass-isnt ."""
  logging.getLogger().__class__ = klass
  logging.setLoggerClass(klass)


class LogConfig:
  """Configurateur du logger."""

  console_fmt = '[%(asctime)s] [%(levelname)-8s] %(message)s'
  file_fmt = '[%(asctime)s] [%(levelname)-8s] [%(name)s] %(message)s'
  datefmt = '%Y%m%d %H:%M:%S'
  field_styles = {'asctime': {'color': 'magenta'},
                  'hostname': {'color': 'magenta'},
                  'levelname': {'color': 'white', 'bold': True},
                  'programname': {'color': 'cyan'},
                  'name': {'color': 'cyan'}}
  level_styles = {'debug': {'color': 'white'},
                  'info': {'color': 'green'},
                  'warning': {'color': 'yellow'},
                  'error': {'color': 'red'},
                  'critical': {'color': 'red', 'bold': True}}

  @staticmethod
  def default_configuration():
    """Met en place la configuration par défaut du logger."""
    console_handler = logging.StreamHandler(sys.stdout)
    # TERM vaut "dumb" dans JobScheduler
    if "TERM" in os.environ and os.environ["TERM"] != "dumb":
      console_handler.setFormatter(coloredlogs.ColoredFormatter(fmt=LogConfig.console_fmt,
                                                                datefmt=LogConfig.datefmt,
                                                                level_styles=LogConfig.level_styles,
                                                                field_styles=LogConfig.field_styles))
    else:
      console_handler.setFormatter(logging.Formatter(fmt=LogConfig.console_fmt,
                                                     datefmt=LogConfig.datefmt))
    logging.basicConfig(level=logging.INFO,
                        handlers=[console_handler])

  @staticmethod
  def add_file_handler():
    """Ajoute un fichier journal."""
    context = Context.get_root_context()
    log_filename = LogConfig.get_filename_for_session(context.session)
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(coloredlogs.ColoredFormatter(fmt=LogConfig.file_fmt,
                                                           datefmt=LogConfig.datefmt,
                                                           level_styles=LogConfig.level_styles,
                                                           field_styles=LogConfig.field_styles))

    logging.getLogger().addHandler(file_handler)

  @staticmethod
  def get_filename_for_session(session):
    """Renvoie le nom du fichier de journalisation du script courant."""
    context = Context.get_root_context()
    log_filename = f"{context.name}_{session}.log"
    return os.path.join(scrippy_core.SCRIPPY_LOGDIR, log_filename)

  @staticmethod
  def render_logfile(session):
    """Affiche le journal de la session demandée."""
    if session is not None:
      logfile = LogConfig.get_filename_for_session(session)
      with open(logfile, 'r') as log:
        print(log.read())


setLoggerClass(InfraLogger)
