"""Le sous-module scrippy_core.log.debuglogger permet la journalisation en mode normal."""
import logging
from scrippy_core.context import Context


class InfraLogger(logging.Logger):
  """Gestionnaire de journaux."""

  def __init__(self, name, level=logging.NOTSET):
    """Initialise le gestionnaire de journaux en mode normal."""
    super(InfraLogger, self).__init__(name, level)

  def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
    """Surcharge logging.Logger.makeRecord."""
    script_name = name
    context = Context.get_current()
    if context is None:
      context = Context.get_root_context()
    script_name = context.log_session_name
    msg = context.vault.protect(msg)
    return super(InfraLogger, self).makeRecord(script_name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)
