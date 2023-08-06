"""Gestionnaire d'erreurs."""
import sys
import traceback
import logging


class ScrippyCoreError(Exception):
  """Classe d'erreur spécifique."""

  def __init__(self, message):
    """Initialise l'instance."""
    self.message = message
    super().__init__(self.message)


def handle_error(kind, value, tb):
  """Récupère toutes les erreurs et sort proprement après avoir logguer les erreurs rencontrées."""
  if kind is not None:
    logging.critical(f"[{kind.__name__}]: {str(value)}")
    if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
      traceback.print_tb(tb)
    if kind != SystemExit:
      sys.exit(1)
