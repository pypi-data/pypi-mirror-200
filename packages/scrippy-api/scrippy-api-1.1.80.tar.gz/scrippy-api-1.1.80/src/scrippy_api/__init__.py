"""Module d'utilisation des API REST."""


class ScrippyApiError(Exception):
  """Classe d'erreur spécifique."""

  def __init__(self, message):
    """Initialise l'instance."""
    self.message = message
    super().__init__(self.message)
