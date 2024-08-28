from sys import argv

from core.walk_find import walk_find_config, walk_find_logo

CONFIG = walk_find_config()
LOGO = walk_find_logo()

args = argv[1:]
if args:
    if args[0] == "background":
        from core.background_process import background_process

        background_process(CONFIG)

else:
    from core.gui import load_gui

    load_gui(CONFIG, LOGO)
