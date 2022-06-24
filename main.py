import sys
import load
import middleware
debug_ = 2
debug_2 = 2
if __name__ == '__main__':
    load.load_domain(sys.argv[1])
    load.load_prob(sys.argv[2])
    middleware.assign()