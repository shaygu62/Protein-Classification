import numpy as np
import os
# import logger
from subprocess import PIPE, Popen, call

# Get PDB functions
getpdb='~dina/scripts/getPDB.pl'
getchain='~dina/utils/get_frag_chain.Linux'

# Random value for the function, doesnt do anything
path_to_save = 'not_important.pdb'

# Load Domains and read keys
family_domain_dict = np.load('dict.npy').item()
keys = family_domain_dict.keys()

# For every Family (key)
for key in keys:
    # Defining dirs to read data into
    dir_name = key
    dir_path = '/cs/labs/dina/shaygu/'
    dir_total =  dir_path + dir_name
    os.mkdir(dir_total)
    os.chdir(dir_total)
    # Go over all the proteins that belong to the family
    for ind in range(len(family_domain_dict[key][0])):

        # Read Domain and Srange from dict
        Domain = family_domain_dict[key][0][ind]
        Srange = family_domain_dict[key][1][ind]
        # Find relevant values for every protein
        id = Domain[0:4]
        frag = Domain[4]
        start_initial = Srange[0].find('=')
        start = Srange[0][start_initial+1:]
        stop_initial = Srange[2].find('=')
        stop = Srange[2][stop_initial+1:]

        # Define paths and functions to read PDB and get chain
        path_to_save_chain = id +'_'+ frag +'_'+ str(start) +'_'+ str(stop) + '_chain.pdb'
        # getPDB returns the id of the protein and ignores the path_to_save
        cmdpdb = '{} {} > {}'.format(getpdb, id, path_to_save)
        #get_frag_chain reads the id.PDB and returns a frag and renames it
        cmdchain = '{} {} {} {} {} > {}'.format(getchain, id+'.pdb', frag, start, stop, path_to_save_chain)

        # Call functions, might need to add wait function.
        call(cmdpdb, shell=True, stdout=PIPE)
        call(cmdchain, shell=True)