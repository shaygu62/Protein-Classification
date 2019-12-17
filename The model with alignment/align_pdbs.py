import numpy as np
import os
# import logger
from subprocess import PIPE, Popen, call

# LOCATION OF ALIGNpdb FUNCTION
pdbalign = '/cs/staff/dina/scripts/align.pl'

#LOCATION WHERE ALL THE FAMILIES OF PROTEINS ARE. MAKE SURE THERE ARE NO SPACES
# IN FILE LOCATION NAME        
dir_path = '/cs/labs/dina/shaygu/chosen_families_aligned'
    
#GET ALL THE FAMILIES WITHIN THE ABOVE FOLDER
entries = os.listdir(dir_path)

# LOOP THROUGH ALL THE FAMILIES
for family_name in entries:
    print(family_name)
    # Get all PDBS from the folder 
    pdbs = os.listdir(dir_path +'/' + family_name)
# Run over the PDBS
    for current_pdb in pdbs[1:]:
# Run alignment with pdbs [0]
        pdb_ref = dir_path + '/' + family_name + '/' + pdbs[0]
        pdb_to_align = dir_path + '/' + family_name + '/' + current_pdb
        aligned_pdb = dir_path + '/' + family_name + '/transformed_' + current_pdb
        #CALL COMMAND LINE FROM PYTHON
        os.system("cd " + dir_path +'/' + family_name)
        os.system(pdbalign+" " + pdb_ref +" "+ pdb_to_align +" " +aligned_pdb)
        
        

        
