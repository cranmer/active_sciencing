import random
import shutil
import os
import json
import numpy as np
import yadage_widget
import yadage.steering_object
from yadage.clihelpers import setupbackend_fromstring, prepare_workdir_from_archive


def run_weinberg_yadage(workdir, sqrtshalf = 45, polbeam1 = 0, polbeam2 = 0,Gf = 1.166390e-05, nevents_per_thread = 10000, threads = 4, backend = 'multiproc:4'):
    repolocation = 'https://raw.githubusercontent.com/lukasheinrich/weinberg-exp/master/example_yadage'
    try:
        shutil.rmtree(workdir)
    except OSError:
        pass
    finally:
        prepare_workdir_from_archive(
            workdir,
            '{}/input.zip'.format(repolocation)
        )

    ys = yadage.steering_object.YadageSteering()
    ys.prepare_workdir(workdir, accept_existing_workdir = True)

    #initialize workflow with parameters
    initdata ={
            'nevents': nevents_per_thread,
            'seeds': [random.randint(1000,9999) for x in range(threads)],
            'sqrtshalf':sqrtshalf,
            'polbeam1': polbeam1,
            'polbeam2': polbeam2,
            'Gf': Gf,
            'runcardtempl':'run_card.templ'.format(os.path.realpath(workdir)),
            'proccardtempl':'sm_proc_card.templ'.format(os.path.realpath(workdir)),
            'paramcardtempl':'param_card.templ'.format(os.path.realpath(workdir)),
    }

    ys.init_workflow(
        'rootflow.yml',
        'github:lukasheinrich/weinberg-exp:example_yadage',
        initdata, initdir = '{}/init'.format(workdir)
    )
    ys.adage_argument(default_trackers = False)
    backend = setupbackend_fromstring(backend)
    ys.run_adage(backend)

    with open(ys.controller.adageobj.view().getSteps('merge')[0].result['jsonlinesfile']) as f:
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
