import shutil
import logging
import os
import numpy as np
import sys
import yadage.steering_object
from yadage.clihelpers import setupbackend_fromstring
import os
import tempfile

def simulator(theta,phi,n_samples, widget = None, delay = False):
    theta, phi, n_samples = float(theta), float(phi), int(n_samples)

    workdir = tempfile.mkdtemp(dir = os.environ.get('YCOMB_WOKRKDIR_BASE',os.path.abspath(os.curdir)))

    ys = yadage.steering_object.YadageSteering()
    ys.prepare_workdir(workdir, accept_existing_workdir = True)

    #initialize workflow with parameters

    initdata ={
        'n_samples': n_samples,
        'phi': phi,
        'theta': theta,
    }

    ys.init_workflow(
        'workflow_delay.yml' if delay else 'workflow.yml',
        '../workflows/localflow/workflow',
        initdata
    )

    backend = setupbackend_fromstring('fourgroundasync')
    ys.adage_argument(default_trackers = False)
    if widget:
        widget.wflow = ys.controller.adageobj
        ys.adage_argument(additional_trackers = [widget.adagetracker])
    ys.run_adage(backend)

    data = np.load(open(ys.controller.adageobj.view().getSteps('feature_extraction')[0].result['outfile']))
    shutil.rmtree(workdir)
    return data