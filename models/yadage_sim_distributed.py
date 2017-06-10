import shutil
import logging
import os
import uuid
import json
import random
import numpy as np
import sys
import yadage.steering_object
from yadage.clihelpers import setupbackend_fromstring,prepare_workdir_from_archive
import os
import tempfile

logging.getLogger('adage').setLevel(logging.ERROR)
logging.getLogger('yadage').setLevel(logging.ERROR)

def pars_to_initdata(theta,phi,n_samples):
    theta, phi, n_samples = float(theta), float(phi), int(n_samples)
    nthreads = 2
    return {
            'nevents': int(n_samples / nthreads),
            'seeds': [random.randint(1000,9999) for x in range(nthreads)],
            'sqrtshalf':phi,
            'polbeam1': 0,
            'polbeam2': 0,
            'Gf': theta * 1e-05,
            'runcardtempl':'run_card.templ',
            'proccardtempl':'sm_proc_card.templ',
            'paramcardtempl':'param_card.templ',
    }

def workflow_config(initdata):
    return ['rootflow.yml','github:lukasheinrich/weinberg-exp:example_yadage',initdata]

def load_data(adageobj):
    with open(adageobj.view().getSteps('merge')[0].result['jsonlinesfile']) as f:
        parsed = map(json.loads,f.readlines())

    costhetas = []
    for e in parsed:
        els = [p for p in e['particles'] if p['id'] == 11]
        mus = [p for p in e['particles'] if p['id'] == 13]
        assert len(mus) == 1
        assert len(els) == 1
        mu = mus[0]
        el = els[0]
        el_px, el_py, el_pz = [el[x] for x in ['px','py','pz']]
        mu_px, mu_py, mu_pz = [mu[x] for x in ['px','py','pz']]
        costheta = mu_pz/el_pz
        costhetas.append(costheta)
    return np.array(costhetas)

def simulator(theta,phi,n_samples, widget = None, delay = False):
    theta, phi, n_samples = float(theta), float(phi), int(n_samples)

    uniqdir = 'work_'+''.join(str(uuid.uuid4()).split('-')[:2])
    workdir = os.path.join(os.environ.get('YCOMB_WOKRKDIR_BASE',os.path.abspath(os.curdir)),uniqdir)


    repolocation = 'https://raw.githubusercontent.com/lukasheinrich/weinberg-exp/master/example_yadage'
    prepare_workdir_from_archive(
            workdir,
            '{}/input.zip'.format(repolocation)
    )

    ys = yadage.steering_object.YadageSteering()
    ys.prepare_workdir(workdir, accept_existing_workdir = True)

    initdata = pars_to_initdata(theta,phi,n_samples)
    ys.init_workflow(
        *workflow_config(initdata),
        initdir = '{}/init'.format(workdir)
    )

    backend = setupbackend_fromstring(os.environ.get('YCOMB_BACKEND','multiproc:4'))
    ys.adage_argument(default_trackers = False)
    if widget:
        widget.wflow = ys.controller.adageobj
        ys.adage_argument(additional_trackers = [widget.adagetracker])

    ys.run_adage(backend)


    data = load_data(ys.controller.adageobj)
    shutil.rmtree(workdir)
    return data