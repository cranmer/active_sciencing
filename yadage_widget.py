import ipywidgets as widgets
from traitlets import Unicode, validate
import adage.visualize
import time
from contextlib import contextmanager
from functools import wraps

def update_widget(widget,wflow):
    widget.dotstring = adage.visualize.colorize_graph_at_time(wflow.dag,time.time()).to_string()

class WorkflowWidget(widgets.DOMWidget):
    _view_name = Unicode('WorkflowWidgetView').tag(sync=True)
    _view_module = Unicode('yadage').tag(sync=True)
    dotstring = Unicode('strict digraph {}').tag(sync = True)

    def update(self):
        update_widget(self,self.wflow)

    def __init__(self,wflow):
        self.wflow = wflow
        super(WorkflowWidget,self).__init__()
        self.update()

    def reset(self,name,offset = ''):
        yadage.reset.reset_state(self.wflow,offset,name)
        self.update()

    @property
    def adagetracker(self):
        return ViewTracker(self)

class ViewTracker(object):
    def __init__(self,widget):
        self.widget = widget
    def initialize(self,adageobj):
        pass
    def track(self,adageobj):
        self.widget.dotstring = adage.visualize.colorize_graph_at_time(adageobj.dag,time.time()).to_string()
    def finalize(self,adageobj):
        self.widget.dotstring = adage.visualize.colorize_graph_at_time(adageobj.dag,time.time()).to_string()
