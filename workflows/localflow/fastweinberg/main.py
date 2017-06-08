import weinberg
import numpy as np
import sys


def main():
     theta     = float(sys.argv[1])
     phi       = float(sys.argv[2])
     n_samples = int(sys.argv[3])
     outfile   = sys.argv[4]

     print theta,phi,n_samples, outfile

     data = weinberg.simulator(theta = theta, phi = phi, n_samples = n_samples)
     np.save(open(outfile,'w'), data)

if __name__ == '__main__':
    main()
