from ipywidgets import widgets

class loopwidget(object):
    def __init__(self):
        self.fontsize = 20
        layout = widgets.Layout(height = '50px', width = '200px')
        collect_data = widgets.HTML(layout = layout)
        calculate_posterior = widgets.HTML(layout = layout)
        next_exp = widgets.HTML(layout = layout)
        # control could be any custom control
        self.view = widgets.VBox([collect_data, calculate_posterior,next_exp])

        self.string_map = {0: 'Collect Data', 1: 'Calculate Posterior', 2: 'Design Next'}
        
        for i in range(3):
            self.view.children[i].value = self.html(self.string_map[i])
        
    def html(self, text, background_color = 'white'):
        textcolor = 'black'
        return '<span style="font-size: {}px;font-weight: bold; background-color: {}; color: {}; width: 100%;">{}</span>'.format(self.fontsize, background_color,textcolor,text)

    def toggle(self,active = None):
        for i in range(3):
            self.view.children[i].value = self.html(self.string_map[i],'#2196F3' if active == i else 'white')
        
