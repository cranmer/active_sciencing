from ipywidgets import widgets

class loopwidget(object):
    def __init__(self):
        collect_data = widgets.HTML()
        calculate_posterior = widgets.HTML() 
        next_exp = widgets.HTML()
        # control could be any custom control
        self.view = widgets.VBox([collect_data, calculate_posterior,next_exp])

        self.string_map = {0: 'Collect Data', 1: 'Calculate Posterior', 2: 'Design Next'}
        
        for i in range(3):
            self.view.children[i].value = self.html(self.string_map[i])
        
    def html(self, text, background_color = 'white'):
        textcolor = 'black' if background_color=='white' else 'white'
        return '<span style="font-weight: bold; background-color: {}; color: {}; margin:0 px; width: 100px;">{}</span>'.format(background_color,textcolor,text)

    def toggle(self,active = None):
        for i in range(3):
            self.view.children[i].value = self.html(self.string_map[i],'green' if active == i else 'white')
        
