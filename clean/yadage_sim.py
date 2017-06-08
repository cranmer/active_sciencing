import shutil
import logging
import os
import numpy as np
import sys
import yadage.steering_object
from yadage.clihelpers import setupbackend_fromstring
import os
import tempfile

logging.getLogger('adage').setLevel(logging.ERROR)
logging.getLogger('yadage').setLevel(logging.ERROR)

def pars_to_initdata(theta,phi,n_samples):
    theta, phi, n_samples = float(theta), float(phi), int(n_samples)
    return {'n_samples':n_samples,'phi': phi,'theta':theta}

def workflow_config(initdata):
    return ['workflow.yml','../workflows/codes',initdata]

def load_data(adageobj):
    return np.load(adageobj.view().getSteps('generate')[0].result['outfile'])

def simulator(theta,phi,n_samples, trackers = []):
    theta, phi, n_samples = float(theta), float(phi), int(n_samples)
    sys.stdout.write('.')
    workdir = tempfile.mkdtemp(dir = os.environ.get('YCOMB_WOKRKDIR_BASE',os.path.abspath(os.curdir)))
    ys = yadage.steering_object.YadageSteering()
    ys.prepare_workdir(workdir)
    initdata = pars_to_initdata(theta,phi,n_samples)
    ys.init_workflow(
        *workflow_config(initdata)
    )

    backend = setupbackend_fromstring(os.environ.get('YCOMB_BACKEND','multiproc:4'))
    ys.adage_argument(additional_trackers = trackers, default_trackers = False)
    ys.run_adage(backend)

    data = load_data(ys.controller.adageobj)
    shutil.rmtree(workdir)
    return data
