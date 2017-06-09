from ipywidgets import widgets
def widget():
    return widgets.IntProgress(min = 0, max = 10, description = 'Calculating EIG: ')
