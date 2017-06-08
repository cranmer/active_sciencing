import weinberg
import numpy as np
import sys
import time

def main():
    theta     = float(sys.argv[1])
    phi       = float(sys.argv[2])
    n_samples = int(sys.argv[3])


    try:
        mean = float(sys.argv[5])
        if mean:
            random_delay = np.random.normal(mean)
            print 'random',random_delay
            time.sleep(random_delay)
    except IndexError:
        pass 

    outfile = sys.argv[4]
    data = weinberg.simulator(theta = theta, phi = phi, n_samples = n_samples)
    np.save(open(outfile,'w'), data)

if __name__ == '__main__':
    main()
