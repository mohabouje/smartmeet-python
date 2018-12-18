from beeprint import pp


def pprint(o, output=True, max_depth=5, indent=2, width=80, sort_keys=True, config=None, **kwargs):
    pp(o, output=output, max_depth=max_depth, indent=indent, width=width, sort_keys=sort_keys, config=config, **kwargs)
