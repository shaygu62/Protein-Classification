###############################################################################################################
# In this code we will import chosen family, 60 CATHCODES that are well represented.
# We will work with small chunks taken from the 500MB txt file. Each small chunk is seperated by "//"
# From each chunk we will save DOMAIN and SRANGE in to a dictionary dict{#CATHCODE} = [DOMAIN,SRANGE]
# In the end we will get a dictionary with all of the CATHCODES as key and # amount of domains and srange as the
# cath-superfamily-list dictates.
###############################################################################################################
import pandas as pd
# import xlrd

# Import chosen families (CATHCODES)
file_str_3 = 'cath-superfamily-list.xlsx' # Family representation txt
xl = pd.read_excel(file_str_3,sheet_name ='ordered by CATH ID' )
family_choosen = xl['# CATH_ID'].values
print(list(family_choosen))
family_list = family_choosen
# print(family_list[0])


file_str_1 = 'cath-domain-description-file.txt' # Data base txt
file_str_2 = 'cath-domain-description-file-small.txt' # Data base txt
file_str_3 = 'cath-superfamily-list.txt' # Family representation txt




# Read until // without importing all of the file
def each_chunk(stream, separator):
  buffer = ''
  while True:  # until EOF
    chunk = stream.read(1000)  # I propose 4096 or so
    if not chunk:  # EOF?
      yield buffer
      break
    buffer += chunk
    while True:  # until no separator is found
      try:
        part, buffer = buffer.split(separator, 1)
      except ValueError:
        break
      else:
        yield part

# Family dict
family_domain_dict = {}
with open(file_str_1) as myFile:
  for chunk in each_chunk(myFile, separator='//'):
    # For every relevant chunk
    chunk_split = chunk.split('\n')
    # Split chunk in to lines in list and extract the chunks family
    for line in chunk_split:
        if 'CATHCODE' in line:
            line_split = line.split(' ')
            family_chunk = line_split[2]
    # Go over all of the families chosen
    for family in family_list:
    # If the family of the chunk is equal to one of the relevant families
        if family == family_chunk:
            # Save DOMAIN
            for line in chunk_split:
                 if 'DOMAIN' in line:
                    domain_split = line.split(' ')
                    domain_chunk = domain_split[4]
            # Save SRANGE
                 if 'SRANGE' in line:
                    line_split = line.split(' ')
                    srange_chunk = line_split[4:8]

            # Put DOMAIN and SRANGE in to dictionary with family (CATHCODE) as a key.
            if family_chunk in family_domain_dict:
                # print(family_domain_dict)
                family_domain_dict[family_chunk][0].append(domain_chunk)
                family_domain_dict[family_chunk][1].append(srange_chunk)
            else:
                family_domain_dict[family_chunk] = ([domain_chunk],[srange_chunk])
    #
# print('Dict: ', family_domain_dict)
print(family_domain_dict['1.10.8.10'][0][0:10])
print(family_domain_dict['1.10.8.10'][1][0:10])

import csv

# Save dictionary as pickle file
# import pickle
# pickle_out = open("family_domain_dict.pickle","wb+")
# pickle.dump(family_domain_dict, pickle_out)
# pickle_out.close()

# Load dictionary
import pickle
pickle_in = open("family_domain_dict.pickle","rb")
family_domain_dict = pickle.load(pickle_in)
one_family_srange = family_domain_dict['1.10.8.10'][1]

# Correct for SRANGE format 
for i in range (1, len(one_family_srange)):
    print (one_family_srange[i][0])
    start_initial = one_family_srange[i][0].find('=')
    print(one_family_srange[i][0][start_initial+1:])

    print (one_family_srange[i][2])
    stop_initial = one_family_srange[i][2].find('=')
    print(one_family_srange[i][2][stop_initial+1:])