import os

from pyr.console import PyrConsole
from pyr.defaults import default_config


def main(config=None):
    if not config:
        config = {}
        config_path = os.path.expanduser("~/.pyr_profile")
        if os.path.exists(config_path):
            execfile(config_path, config)

    config = dict(default_config.items() + config.items())
    console = PyrConsole(pygments_style=config.get('pygments_style'))
    console.interact(banner=config.get('banner'))


if __name__ == '__main__':
    main()
