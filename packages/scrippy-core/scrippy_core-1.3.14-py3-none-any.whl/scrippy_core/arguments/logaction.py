from argparse import Action, SUPPRESS
from scrippy_core.log import LogConfig
from scrippy_core.context import Context
from scrippy_core.history import History


class LogAction(Action):
  def __init__(self,
               option_strings,
               dest=SUPPRESS,
               default=SUPPRESS,
               help="Show execution history"):
    super(LogAction, self).__init__(option_strings=option_strings,
                                    dest=dest,
                                    default=default,
                                    nargs='?',
                                    type=str,
                                    metavar=('SESSION (default: last)'),
                                    help=help)

  def __call__(self, parser, namespace, session, option_string=None):
    _context = Context.get_root_context()
    session = session or History().get_last_session()
    LogConfig.render_logfile(session)
    parser.exit()
