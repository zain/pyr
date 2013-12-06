import argparse, os

from pyr.console import PyrConsole
from pyr.defaults import default_config


def main(config=None):
    if not config:
        config = {}
        config_path = os.path.expanduser("~/.pyr_profile")
        if os.path.exists(config_path):
            execfile(config_path, config)

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--init", dest="init_filename", required=False,
        help="input file with two matrices", metavar="FILE")
    args = parser.parse_args()

    initfile = None
    if args.init_filename:
        if not os.path.exists(args.init_filename):
            parser.error("Init file %s does not exist" % args.init_filename)
        else:
            initfile = open(args.init_filename, 'r')

    config = dict(default_config.items() + config.items())
    console = PyrConsole(pygments_style=config.get('pygments_style'), initfile=initfile, banner=config.get('banner'))
    console.interact()


if __name__ == '__main__':
    main()
