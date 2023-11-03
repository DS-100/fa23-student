# import psycopg2
import sql

import dill as pickle

from pathlib import Path
from subprocess import run, PIPE

RESULTS_DIR = "results"
N_TUPLES = 10

def save_results(pkl_fname, *args):
    pkl_fname = f"{RESULTS_DIR}/{pkl_fname}.pkl"
    with open(pkl_fname, 'wb') as f:
        for arg in args:
            if type(arg) == sql.run.ResultSet:
                arg = arg.DataFrame() # convert jupysql to dataframe
            pickle.dump(arg, f)
    with open(pkl_fname, 'rb') as f:
        ret_vals = [pickle.load(f) for _ in args]
    return ret_vals
    
# https://stackoverflow.com/questions/18675863/load-data-from-python-pickle-file-in-a-loop
def load_results(pkl_fname):
    def pickleLoader(pklFile):
        try:
            while True:
                yield pickle.load(pklFile)
        except EOFError:
            pass
        
    pkl_fname = f"{RESULTS_DIR}/{pkl_fname}.pkl"
    with open(pkl_fname, 'rb') as f:
        return [event for event in pickleLoader(f)]