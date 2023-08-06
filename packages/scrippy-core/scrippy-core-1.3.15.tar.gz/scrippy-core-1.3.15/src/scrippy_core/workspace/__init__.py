"""Le sous-module scrippy_core.workspace apporte les objets nécessaires à la gestion de l'espace de travail."""
import os
import shutil
import pathlib
import logging
import scrippy_core
from scrippy_core.error_handler import ScrippyCoreError


class Workspace():
  """La classe Workspace offre un espace de travail dont le répertoire est basé sur le le nom passé en argument du constructeur.

  L'espace de travail sera alors créé dans le répoetoire scrippy_core.SCRIPPY_TMPDIR.
  """

  def __init__(self, name):
    """Initialise l'espace de travail."""
    self.path = pathlib.Path(os.path.join(scrippy_core.SCRIPPY_TMPDIR, name))

  def __enter__(self):
    """Point d'entrée."""
    logging.info(f"[+] Creation de l'espace de travail: {self.path}")
    try:
      self.path.mkdir(mode=0o750, parents=True, exist_ok=False)
    except Exception as err:
      err_msg = f"Erreur lors de la creation de l'espace de travail temporaire: [{err.__class__.__name__}] {err}"
      logging.critical(err_msg)
      raise ScrippyCoreError(err_msg) from err
    return str(self.path)

  def __exit__(self, kind, value, traceback):
    """Point de sortie."""
    logging.info(f"[+] Suppression de l'espace de travail: {self.path}")
    try:
      shutil.rmtree(self.path)
    except Exception as err:
      err_msg = f"Erreur lors de la suppression de l'espace de travail temporaire: [{err.__class__.__name__}] {err}"
      logging.critical(err_msg)
      raise ScrippyCoreError(err_msg) from err

  def __eq__(self, other):
    """Surcharge l'implémentation par défaut."""
    if isinstance(other, Workspace):
      return self.path == other.path
    return False

  def __str__(self):
    """Renvoie une représentation sous forme de chaîne de caractères."""
    return str(self.path)
