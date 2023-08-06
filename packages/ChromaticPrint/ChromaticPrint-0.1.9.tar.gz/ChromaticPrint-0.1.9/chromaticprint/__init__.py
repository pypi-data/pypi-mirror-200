from .colors import Colors

colors = Colors(escape_codes)


def puts(the_color_chosen, text):
    print(f"{getattr(colors, the_color_chosen)}{text}{colors.reset}")
    