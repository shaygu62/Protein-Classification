# Based on pdb_query

# Import all of the files
# Observe the dictionary
# Choose 40 families and num select points.
# Choose num_select points


# Imports
from Bio import PDB
import os
import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import random
import pickle



#plots 3D scatter of XYZ data
def scatter_plot(x_vals,y_vals,z_vals):
    fig = pyplot.figure()
    ax = Axes3D(fig)
    ax.scatter(x_vals,y_vals,z_vals)
    pyplot.show()
    return


def randomly_choose_points(points_array , num_select):
#''' Gets points_array which is x,y,z representation of single pdb
#    and num_select which is the amount of atoms we chosen
#    
#    Returns Randomly sampled points, in indices 0:len(points_array)
#'''
    pdb_points = np.zeros((num_select,3))
    len_points = len(points_array)
    np_points_array = np.array(points_array)
    index = np.random.choice(range(len_points), np.min([len_points,num_select]), replace=False)
    np_points_chosen = np_points_array[index]
    pdb_points[0:len(np_points_chosen)] = np_points_chosen
    #return np.expand_dims(pdb_points,axis=0)
    return pdb_points

#select how many samples from each family
train_example_num = 400
#select how many families are represented
family_num = 57



# name of folder where all the families are located
families_folder = '/cs/labs/dina/shaygu/chosen_families_aligned/Chosen_families_within_chosen_families_aligned'
# Get all dirs in the folder
entries = os.listdir(families_folder)
#Initiate dict
dict_families = {}
# For all of the families - files in the folder
for family_name in entries:
    print(family_name)
    #create dicts for all C-Alphas, C-Betas, and C-gammas
    dict_pdbsA = {}
    dict_pdbsB = {}
    dict_pdbsG = {}
    # Get all PDBS from the folder and select randomly train_example_num of them
    pdbs = os.listdir(families_folder +'/' + family_name)
    pdb_index = 0
    pdbs_available = len(pdbs)
    indices = np.random.choice(range(pdbs_available), train_example_num, replace=False)
# Run over the PDBS
    for ind in indices:
        pdb = pdbs[ind]
#        print(pdb)
        # Get x,y,z coordinates of chosen atoms, and store them in dictionaries
        parser = PDB.PDBParser()
        io = PDB.PDBIO()
        struct = parser.get_structure(pdb,families_folder +'/' + family_name + '/' + pdb)
        dict_pdbsA[pdb+ '_Alpha'] = []
        dict_pdbsB[pdb+ '_Beta'] = []
        dict_pdbsG[pdb + '_Gamma'] = []

        for model in struct:
            for chain in model:
                for i,residue in enumerate(chain):
                    #select the desired atoms from each residue(amino-acid)
                     try: #read CAlpha if exists:
                         xA,yA,zA = residue['CA'].get_coord()
                         dict_pdbsA[pdb + '_Alpha'].append([xA,yA,zA])
                     except:
                         continue
                     
                     try: #read Cbeta if exists
                         xB,yB,zB = residue['CB'].get_coord()
                         dict_pdbsB[pdb + '_Beta'].append([xB,yB,zB])
                     except:
                         continue
                     
                     try:#read Cgamma if exists
                         xG,yG,zG = residue['CG'].get_coord()
                         dict_pdbsG[pdb + '_Gamma'].append([xG,yG,zG])
                     except:
                         try:
                             xG,yG,zG = residue['CG2'].get_coord()
                             dict_pdbsG[pdb+ '_Gamma'].append([xG,yG,zG])
                         except:
                             continue  
                                  
    #store all the XYZ data of each family in a dict using the family name as key                 
    dict_families[family_name] = [dict_pdbsA, dict_pdbsB, dict_pdbsG]



# Having the dict, select amount of points and get coordinates
num_select = 256
#initiate the X_train set and labels
X_train = np.zeros([train_example_num*family_num,num_select,3])
X_labels = np.zeros(train_example_num*family_num)
#for QA reasons - keep the origin of each XYZ array - which family, PDB and chain it came from
# and how many atoms were stored in it
X_families = []
X_origin = []

# Set label initial value
label = 0
for family_key in sorted(dict_families.keys()):
    #iterate over each family
    non_zero_count = 0
    non_zero_mean = 0 
    pdb_xyz_concat = np.zeros([1,num_select,3])
    family_dict = dict_families[family_key]
    Alpha_dict = family_dict[0]
    Beta_dict = family_dict[1]
    Gamma_dict = family_dict[2]
    
    
    for key_A in sorted(Alpha_dict.keys()):
        #iterate over each PDB within the family, and select only num_select coordinates
        # CA is priority, then CB, then CG
        key_B = key_A[0:-5] + 'Beta'
        key_G = key_A[0:-5] + 'Gamma'
        len_A, len_B, len_G = len(Alpha_dict[key_A]),len(Beta_dict[key_B]),len(Gamma_dict[key_G])
        pdb_xyz = np.zeros((num_select, 3))
        if  len_A > num_select:
            pdb_xyz = randomly_choose_points(Alpha_dict[key_A], num_select)
        else:
            pdb_xyz[0:len(Alpha_dict[key_A]), :] = np.array(Alpha_dict[key_A])
            if len_B > num_select - len_A:
                pdb_xyz[len_A:, :] = randomly_choose_points(Beta_dict[key_B], num_select - len_A)              
            else:
                pdb_xyz[len_A:len_B+len_A, :] = np.array(Beta_dict[key_B])
                if len_G > num_select - len_A-len_B:
                    pdb_xyz[len_A+len_B:, :] = randomly_choose_points(Gamma_dict[key_G], num_select - len_A-len_B)                    
                else:
                    pdb_xyz[len_A+len_B:len_B+len_A+len_G, :] = np.array(Gamma_dict[key_G])
                    
            #non_zero_count += 1
            #non_zero_mean += len_pdb
#            print(key , len_pdb)
        #pdb_xyz = randomly_choose_points(family_dict[key], num_select)
        pdb_xyz_expanded = np.expand_dims(pdb_xyz,axis=0)
        pdb_xyz_concat = np.concatenate((pdb_xyz_concat, pdb_xyz_expanded), axis=0)
        X_origin.append([family_key, key_A,len_A,len_B,len_G, len_A+len_B + len_G])
        # scatter_plot(pdb_xyz[0][:,0],pdb_xyz[0][:,1],pdb_xyz[0][:,2])
    family_data  = pdb_xyz_concat[1:,:,:]
    family_label = np.ones([family_data.shape[0]]) * label
    #not sure if next 15 lines are critical...
    print(family_key)
    print(['None zero count',non_zero_count])
    if non_zero_count == 0:
        Mean_length = 512
    if non_zero_count > 0:
        Mean_length = (non_zero_mean*non_zero_count/train_example_num) + 512*(train_example_num-non_zero_count)/train_example_num
        
    print(['Mean length',Mean_length ])
    print()
#    print(families_folder +'/' + family_key + '/' + family_key + '.npy')

    X_train[label*train_example_num:(label+1)*train_example_num,:,:] = family_data
    X_labels[label*train_example_num:(label+1)*train_example_num] = family_label
    X_families.append(family_key)
    
    label = label + 1


#save X_train and X_labels as np arrays for pointnet
np.save('X_train'  + '.npy', X_train) # save
np.save('X_label'  + '.npy', X_labels) # save



#save the origins of the XYZ data in pickle file
with open('X_Origin.data', 'wb') as filehandle:
    # store the data as binary data stream
    pickle.dump(X_origin, filehandle)
with open('X_families.data', 'wb') as filehandle:
    # store the data as binary data stream
    pickle.dump(X_families, filehandle)
    
