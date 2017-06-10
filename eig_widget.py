from ipywidgets import widgets
def widget():
    single_progress  = widgets.IntProgress(min = 0, max = 10, description = 'Calculating EIG: ')
    overall_progress = widgets.IntProgress(min = 0, max = 10, description = 'EIG Progress   : ')
    return widgets.VBox([single_progress, overall_progress])
