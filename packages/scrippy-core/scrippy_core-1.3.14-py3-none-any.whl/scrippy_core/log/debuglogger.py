"""Le sous-module scrippy_core.log.debuglogger permet la journalisation en mode déverminage."""
import logging
from scrippy_core.log.infralogger import InfraLogger


class DebugLogger(InfraLogger):
  """Gestionnaire de journaux spécifique au mode déverminage."""

  def __init__(self, name, level=logging.NOTSET):
    """Initialise le gestionnaire de journaux en mode déverminage."""
    super(DebugLogger, self).__init__(name, level)

  def setLevel(self, level):
    """Surcharge logging.Logger.setLevel."""
    # On ne fait rien le niveau de log est forcé à DEBUG
    pass
