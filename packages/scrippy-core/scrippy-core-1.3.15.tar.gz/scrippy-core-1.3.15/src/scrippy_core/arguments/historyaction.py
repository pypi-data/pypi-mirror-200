"""Gestion de l'utilisation de l'historisation."""
import sys
from argparse import Action, SUPPRESS
from scrippy_core.history import History
from scrippy_core.context import Context


class HistoryAction(Action):
  """Classe de gestion de l'utilisation de l'historisation."""

  def __init__(self, option_strings,
               dest=SUPPRESS, default=SUPPRESS,
               help="Show execution history"):
    """Initialise la classe."""
    super(HistoryAction, self).__init__(option_strings=option_strings,
                                        dest=dest,
                                        default=default,
                                        nargs='?',
                                        type=int,
                                        # nombre d'excution affiché par défaut
                                        const=10,
                                        metavar=('NB_EXECUTION (default:10)'),
                                        help=help)

  def __call__(self, parser, namespace, nb_execution, option_string=None):
    _context = Context.get_root_context()
    print(f"{nb_execution} dernières executions de {_context.filename}")
    formatter = parser._get_formatter()
    formatter.add_text(History().read_history(nb_execution))
    parser._print_message(formatter.format_help(), sys.stdout)
    parser.exit()
