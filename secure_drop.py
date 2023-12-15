# PYTHONPATH=./src to run include

import sys
sys.path.append('./src')
sys.path.append('./bin')

from run import run

if __name__ == "__main__":
    run()
