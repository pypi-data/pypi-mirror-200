"""Le sous-module scrippy_core.scriptinfo."""
import os
import __main__


class ScriptInfo:
  """L'objet ScriptInfo."""

  @staticmethod
  def get_script_full_filename():
    """Retourne le chemin complet du script courant."""
    return __main__.__file__

  @staticmethod
  def get_script_filename():
    """Retourne le nom de fichier du script courant."""
    return os.path.basename(__main__.__file__)

  @staticmethod
  def get_script_name():
    """Retourne le nom du script courant."""
    return os.path.splitext(ScriptInfo.get_script_filename())[0]

  @staticmethod
  def get_doc():
    """Retourne la documentation du script courant."""
    return __main__.__doc__
