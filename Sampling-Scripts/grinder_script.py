import os

grinder_input_files = 'grinder_input_files'

for n in range(1,41):
    its2_seq = grinder_input_files + '\input' + str(n) + 'its2.fas'
    trnl_seq = grinder_input_files + '\input' + str(n) + 'trnl.fas'
    abundance_file = grinder_input_files + '\input' + str(n) + 'abundancy.txt'
    prefix = 'sample' + str(n) 
    call_its2 = 'grinder -rf ' + its2_seq + ' -tr 20000 -di 0 -af ' + abundance_file + \
    ' -id 300 -rd 300 -fq 1 -ql 36 26 -mo FR -un 0 -md poly4 3e-3 3.3e-8 -mr 98 2 -bn ' + prefix + ' -od grinder_output\grinder_output_files_its2'
    os.system(call_its2)
    call_trnl = 'grinder -rf ' + trnl_seq + ' -tr 20000 -di 0 -af ' + abundance_file + \
    ' -id 300 -rd 300 -fq 1 -ql 36 26 -mo FR -un 0 -md poly4 3e-3 3.3e-8 -mr 98 2 -bn ' + prefix + ' -od grinder_output\grinder_output_files_trnl'
    os.system(call_trnl)
    
print("the simulation has run succesfully")