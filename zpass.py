import argparse
import zpass.configuration as config

parser = argparse.ArgumentParser()
parser.add_argument('--file', help="The database file to use", default=config.config_file)
commands = parser.add_subparsers(help='commands', dest='command')


def _add(args):
    print(args)
def _list(args):
    print(args)
def _lookup(args):
    print(args)
def _remove(args):
    print(args)
def _generate(args):
    print(args)


#ADD
add_parser = commands.add_parser(
    'add',
    help='Add a set of credentials.')
add_parser.set_defaults(func=_add)

#LIST
list_parser = commands.add_parser(
    'list',
    help='List available credentials.')
list_parser.add_argument('search', type=str, nargs='?', default=None)
list_parser.set_defaults(func=_list)

#LOOKUP
search_parser = commands.add_parser(
    'lookup',
    aliases=['search'],
    help='Retrieve a particular credential.')
search_parser.add_argument('-s','--show', action='store_true', help="Display password.", default=config.default_show_password)
search_parser.add_argument('-c','--copy', action='store_true', help="Copy password to clipboard.", default=config.default_copy_password)
search_parser.add_argument('search', type=str, nargs='?', default=None)
search_parser.set_defaults(func=_lookup)

#REMOVE
remove_parser = commands.add_parser(
    'remove',
    help='Remove a set of credentials.')
remove_parser.add_argument('search', type=str)
remove_parser.set_defaults(func=_remove)

#GENERATE
generate_parser = commands.add_parser(
    'generate',
    aliases=['gen'],
    help='Generate new passwords.'
)
generate_parser.set_defaults(func=_generate)


if __name__ == "__main__":
    args = parser.parse_args(['lookup', '--show', 'careview'])
    args.func(args)