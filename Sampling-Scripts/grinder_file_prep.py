# script that generate 
import sys 
import os
import re
import random
import pandas as pd
from io import StringIO
from collections import defaultdict

# from nested_dict_script import Nested 
# importing the nested dictionary with the 100 species, 2 barcodes + seq_ids + sequences

# reading in the raw data from locally saved files 'trnl.tax' and 'its2.tax'
trnL_raw_dataframe = pd.read_csv("trnL.tax", sep = "\t", header = None). drop(columns=8)
its2_raw_dataframe = pd.read_csv("its2.tax", sep = "\t", header = None). drop(columns=8)
trnL_raw_dataframe.columns = ['sequence_id', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
its2_raw_dataframe.columns = ['sequence_id', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
trnL_raw_dataframe['species'] = trnL_raw_dataframe['species'].str[3:]
its2_raw_dataframe['species'] = its2_raw_dataframe['species'].str[3:]

# reading in the curated species list from locally svaed file 'curated_specie_list.xlsx'
curated_species_df = pd.read_excel (r'C:\dissertation\software\Grinder\preparing_files\curated_species_list.xlsx') 

# combining its2 and trnl dataframes
its2_trnL_df = its2_raw_dataframe[its2_raw_dataframe.species.isin(trnL_raw_dataframe.species)]

# list of unique species in ITS2 and trnL
its2_trnL_df = its2_trnL_df.drop_duplicates('species') # 18,000 species shared between each 
its2_and_trnl_species = its2_trnL_df['species'].tolist()

# concataning with curated species
concat_its2_trnL = pd.merge(its2_trnL_df, curated_species_df , on='species') # merging the two species dataframes.
concat_its2_trnL = concat_its2_trnL.drop(columns= ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'common name']) 
concat_its2_trnL = concat_its2_trnL.drop_duplicates() # there are 100 different species available 
concat_its2_trnL['species'] = concat_its2_trnL['species'].replace(' ','_', regex=True) # adding an underscore between the species names in the species list

# dropping NAs and creating a list
species_list = concat_its2_trnL['species'].tolist() 
len(species_list) # the list of species is 100 long - this is the 'curated species list' (final)

# removing the duplicates from the species list
def remove_duplicates(l):
    return list(set(l))
new_list = remove_duplicates(species_list)
species_list = sorted(new_list)
len(species_list)

# creating nested dictionary for file generation
species = species_list
nested_dict = {}

input1 = open("its2.txt")

for line in input1:
    its2D = {}
    line_list = line.strip("\n").split("\t")
    if line_list[1] in species:
        its2D.update({"seq_id": line_list[0], "sequence": line_list[2]})
        nested_dict.update({line_list[1]: {"its2": its2D}})
input1.close()


input2 = open("trnL.txt")
for line in input2:
    trnlD = {}
    line_list = line.strip("\n").split("\t")
    if line_list[1] in species:
        trnlD.update({"seq_id": line_list[0], "sequence": line_list[2]})
        if nested_dict.get(line_list[1]) is None:
            nested_dict.update({line_list[1]: {"trnL": trnlD}})
        else:
            nested_dict.get(line_list[1]).update({"trnL": trnlD})
input2.close()

def getSizeOfNestedList(nested_dict):
    count = 0
    # Iterate over the list
    for elem in nested_dict:
        # Check if type of element is list
        if type(elem) == list:  
            # Again call this function to get the size of this element
            count += getSizeOfNestedList(elem)
        else:
            count += 1    
    return count

count = getSizeOfNestedList(nested_dict)
print(f"The number of species in the nested dictionary is {count}") # prints the number of species in the nested dictionary

# Sampling
# generating sample sizes (ranging from 1 to 4)
potential_sample_size = range(1, 5) # how many pollen species CAN be in each sample
sample_sizes = random.choices(potential_sample_size, k=40) ##### CHANGE NUMBER OF SAMPLES HERE ### 

# sampling abundancies
possible_abundancies_dict = {}
possible_abundancies_dict[1] = [[100]]
possible_abundancies_dict[2] = [[10,90], [25,75], [50, 50]]
possible_abundancies_dict[3] = [[10, 50, 40], [10, 10, 80], [25, 25, 50], [30, 40, 30], [20, 50, 30], [10, 20, 70], [90, 5, 5]]
possible_abundancies_dict[4] = [[10, 10, 10, 70], [5, 5, 45, 45], [10, 20, 20, 30], [30, 30, 30, 10], [25, 25, 25, 25]]

abundancy_values = []
for i in sample_sizes:
    if i in possible_abundancies_dict:
        abundancy_values.append(random.choice(possible_abundancies_dict[i])) # this uses the dic key to exctract a random 
    
abundancy_values_dict = {}
x = 1
for i in abundancy_values:  
    abundancy_values_dict[x] = i
    x += 1

# sampling species
species_in_samples = []
for i in sample_sizes:  #
    species_samples = random.sample(species_list, i)
    species_in_samples.append(species_samples)

species_in_samples_dict = {}
x = 1
for i in species_in_samples:  #
    species_in_samples_dict[x] = i
    x += 1

# generating Grinder input files
grinder_input_files = 'grinder_input_files' 
os.system('mkdir ' + grinder_input_files) # creates a directory called grinder_input_files

# making the species_in_samples a tuple so it is hashable
species_tuples = []
for x in species_in_samples:
    species_tuples.append(tuple(x))

# grinder input file generation
counter = 0
for sample in species_tuples:
    counter += 1
    output_its2_fas = open(grinder_input_files + '\input' + str(counter) + 'its2.fas' , 'w')
    output_trnl_fas = open(grinder_input_files + '\input' + str(counter) + 'trnl.fas' , 'w')
    output_abundancy = open(grinder_input_files + '\input' + str(counter) + 'abundancy.txt', 'w')

    abundance_info = abundancy_values_dict.get(counter)
    counter2 = -1
    for species in sample:
        counter2 += 1

        output_abundancy.write(species + '\t' + str(abundance_info[counter2]) + '\n')
        
        if species in nested_dict:
                info = nested_dict.get(species)
                        
        for barcode in info:
            barcode_info = info.get(barcode)
            sequence = barcode_info.get('sequence')
                    
            if barcode == 'its2':
                output_its2_fas.write('>' + species +  '\n' + sequence + '\n')                
            else:
                output_trnl_fas.write('>' + species +  '\n' + sequence + '\n')
print('Grinder input files have been generated succesfully')