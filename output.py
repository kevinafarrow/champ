from colorama import Fore
from pprint import pformat
from jinja2 import Template

# Note this is a stripped down version of output.py which can be found in kftools.

def message_string(message, level, tabs=4, status='none'):
    color = {"success": Fore.GREEN, "error": Fore.RED, "attention": Fore.CYAN, "none": Fore.RESET, "yellow": Fore.YELLOW, "magenta": Fore.MAGENTA}
    tm = Template("{{ color }}    {{ ' ' * tabs * level }} {{ message }}{{ reset }}")
    x = locals()
    x['color'] = color[status]
    print(tm.render({**x, 'reset': Fore.RESET}))

def message_list(lst, level, tabs=4, status='none'):
    for l in lst:
        message_string(l, level=level, tabs=tabs, status=status)

def message_dict(dct, level, tabs=4, status='none'):
    for k, v in dct.items():
        message_string(f"{k}: {v}", level=level, tabs=tabs, status=status)

def message(thing, level=0, tabs=4, status='none', show_all=False):
    lookup = {
        "<class 'str'>": message_string,
        "<class 'list'>": message_list,
        "<class 'dict'>": message_dict,
        }
    func = lookup[str(type(thing))]
    if show_all:
        func(thing, level=level, tabs=tabs, status=status, show_all=show_all)
    else:
        func(thing, level=level, tabs=tabs, status=status)