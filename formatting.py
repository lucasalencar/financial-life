PERC_FORMAT = "{:.2%}"
BR_CURRENCY_FORMAT = "R$ {:.2f}"

def amount_color(value):
    color = 'red' if value <= 0 else 'green'
    return "color: %s" % color


def red_to_green_background(mid_range):
    """When value is below 0, color is red.
    When value is below mid_range, color is yellow.
    When value is above mid_range, color is green."""
    def background_color(value):
        if value <= 0:
            color = 'red'
        elif value <= mid_range:
            color = 'yellow'
        else:
            color = 'green'
        return 'background-color: %s' % color
    return background_color
