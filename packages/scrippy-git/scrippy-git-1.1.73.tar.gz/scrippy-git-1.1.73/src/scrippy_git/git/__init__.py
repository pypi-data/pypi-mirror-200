"""Module client Git."""
import git
import logging
from scrippy_git import ScrippyGitError


class Repo():
  """Cette classe permet la manipulation d'un dépôt Git, notamment son clonage, l'enregistrement (commit), la récuparation (pull) et l'envoi (push) des modifications apportées.

  Cette classe permet uniquement la manipulation d'un dépôt via SSH.

  :param username: Le nom d'utilisateur utilisé pour se connecter via SSH sur le serveur Git
  :type username: str, obligatoire
  :param host: Le nom de l'hôte distant hébergeant le serveur Git
  :type host: str, obligatoire
  :param port: Le numéro du port sur lequel se connecter, valeur par défaut: 22
  :type port: int, optionnel
  :param reponame: Le nom du dépôt distant
  :type reponame: str, obligatoire
  """

  def __init__(self, username=None, host=None, port=22, reponame=None):
    self.url = f"ssh://{username}@{host}:{port}/{reponame}"
    self.name = reponame
    self.cloned = None
    self.path = None
    self.origin = None
    self.branch = None

  def clone(self, branch, path, origin="origin", options=None, env=None):
    if options is None:
      options = []
    if env is None:
      env = {}
    logging.debug(f"[+] Clonage du depot: {self.url}")
    logging.debug(f" '-> {path}")
    self.path = path
    self.branch = branch
    try:
      self.cloned = git.Repo.clone_from(self.url, path, branch=branch, multi_options=options, env=env)
      self.origin = self.cloned.remote(name=origin)
    except Exception as err:
      err_msg = f"Erreur lors du clonage du depot: [{err.__class__.__name__}]: {err}"
      raise ScrippyGitError(err_msg) from err

  def commit(self, message, error_on_clean_repo=True):
    logging.debug(f"[+] Commit: [{self.name}]: {message}")
    if not self.cloned.is_dirty(untracked_files=True):
      if error_on_clean_repo:
        err_msg = "Impossible de commiter sans modification"
        raise ScrippyGitError(err_msg)
      logging.warning(" '-> Aucune modification a commiter")
      return
    self.cloned.git.add(".")
    self.cloned.git.commit(m=message)

  def pull(self):
    logging.debug(f"[+] Pull: [{self.name}]: {self.origin}")
    self.cloned.git.pull()

  def push(self):
    logging.debug(f"[+] Push: [{self.name}]: {self.origin}")
    self.origin.push()

  def commit_push(self, message, error_on_clean_repo=True):
    try:
      self.commit(message=message, error_on_clean_repo=error_on_clean_repo)
      self.pull()
      self.push()
    except Exception as err:
      err_msg = f"Erreur lors du commit: [{err.__class__.__name__}]: {err}"
      raise ScrippyGitError(err_msg) from err
