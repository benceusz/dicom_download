
# DIPR - Inselspital
"""
Selection of DICOM images based on DICOM metaheader filtering.
Iteration through folder
filtering out the necessary sequences from whole DICOM list_studies
store it in output_dir in a similar folder formas as project_dir
"""
import pydicom as dicom
import os
import shutil
import numpy as np

### VARIABLES TO SET ###
project_dir = "set manually"
output_dir = "set manually"

### FUNCTIONS ###
def copy_dcm_file(source, destination):
    """
    Source path
    Destination path: destination
    """
    try:
        shutil.copyfile(source, destination)
        #print("File copied successfully.")

    # If source and destination are same
    except shutil.SameFileError:
        print("Source and destination represents the same file.")

    # If destination is a directory.
    except IsADirectoryError:
        print("Destination is a directory: %s" %destination)

    # If there is any permission issue
    except PermissionError:
        print("Permission denied.")

    # For other errors
    except:
        print("Error occurred while copying file.")
    return

### MAIN ###
list_studies = [ name for name in os.listdir(project_dir) if os.path.isdir(os.path.join(project_dir, name))  ]

if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

for i_dir in list_studies:
    path_out_patient = os.path.join(output_dir, i_dir)
    path_in_patient = os.path.join(project_dir, i_dir)

    if not os.path.isdir(path_out_patient): os.mkdir(path_out_patient)
    
    print("processing study: %s" % i_dir)
    if not os.path.isdir(os.path.join(path_out_patient,"33")):
        os.mkdir(os.path.join(path_out_patient,"33"))
    else:
        if os.listdir(os.path.join(path_out_patient,"33")):
            continue
        
    if not os.path.isdir(os.path.join(path_out_patient,"66")):
        os.mkdir(os.path.join(path_out_patient,"66"))
    else:
        if os.listdir(os.path.join(path_out_patient,"66")):
            continue

        

    print(path_in_patient)
    counter = 0
    c_failure = 0

    max_slice_33 = 0
    max_series33 = []
    max_slice_66 = 0
    max_series66 = []


    for root, dir, files in os.walk(path_in_patient):
        for i_file in files:
            path_i_file = os.path.join(path_in_patient, i_file)
            ds = dicom.read_file(path_i_file)
            try:
                if ds.ImageType[6] == "DET_A" and ds.ImageType[0] == "ORIGINAL":
                    path_det_a = os.path.join(output_dir, i_dir, "66", str(ds.SeriesNumber), i_file)
                    if ds.InstanceNumber >= max_slice_66: max_slice_66 = ds.InstanceNumber

                elif ds.ImageType[6] == "DET_B" and ds.ImageType[0] == "ORIGINAL":
                    path_det_b = os.path.join(output_dir, i_dir, "33", str(ds.SeriesNumber), i_file)
                    if ds.InstanceNumber >= max_slice_33: max_slice_33 = ds.InstanceNumber 

            except:
                pass
    
    print(max_slice_33)
    print(max_slice_66)

    
    if len({max_slice_33, max_slice_66}) != 1:
        min_slice_threshold = min(max_slice_33, max_slice_66)
        if max_slice_33 != min_slice_threshold:       
            max_slice_33 = min_slice_threshold
            print("WARNING! The filter of the sequence at patient %s, in dose 33 has been lowered"%i_dir)
        if max_slice_66 != min_slice_threshold:       
            max_slice_66 = min_slice_threshold
            print("WARNING! The filter of the sequence at patient %s, in dose 66 has been lowered"%i_dir)

                
    print("Sequences before")
    print(max_series33)
    print(max_series66)
            
    # find the sequences in each subfolder that has the biggest number of slices
    for root, dir, files in os.walk(path_in_patient):
        for i_file in files:
            path_i_file = os.path.join(path_in_patient, i_file)
            ds = dicom.read_file(path_i_file)
            
            if len({max_slice_33, max_slice_66}) == 1:
                try:
                    if ds.ImageType[6] == "DET_A" and ds.ImageType[0] == "ORIGINAL":
                        path_det_a = os.path.join(output_dir, i_dir, "66", str(ds.SeriesNumber), i_file)
                        if ds.InstanceNumber == max_slice_66: 
                            if ds.SeriesNumber not in max_series66: max_series66+= [ds.SeriesNumber ] 
                        if ds.InstanceNumber > min_slice_threshold: 
                            if ds.SeriesNumber in max_series66: max_series66.remove(ds.SeriesNumber)  

                    elif ds.ImageType[6] == "DET_B" and ds.ImageType[0] == "ORIGINAL":
                        path_det_b = os.path.join(output_dir, i_dir, "33", str(ds.SeriesNumber), i_file)
                        if ds.InstanceNumber == max_slice_33: 
                            if ds.SeriesNumber not in max_series33: max_series33+= [ds.SeriesNumber ] 
                        if ds.InstanceNumber > min_slice_threshold: 
                            if ds.SeriesNumber in max_series33: max_series33.remove(ds.SeriesNumber)    

                except:
                        pass
            else:
                print("WARNING! Sequence with max slice are not present in all the subfolder at patient %s!" % i_dir)


    print("Sequences after")
    print(max_series33)
    print(max_series66)

    if len({max_slice_33, max_slice_66}) == 1:

        for root, dir, files in os.walk(path_in_patient):
            for i_file in files:
                path_i_file = os.path.join(path_in_patient, i_file)
                ds = dicom.read_file(path_i_file)

                try:
                    if ds.ImageType[6] == "DET_A" and ds.ImageType[0] == "ORIGINAL" and ds.SeriesNumber in max_series66 :
                        path_det_a = os.path.join(output_dir, i_dir, "66", str(ds.SeriesNumber), i_file)
                        seq_dir = os.path.join(output_dir, i_dir, "66", str(ds.SeriesNumber))
                        if not os.path.isdir(seq_dir): os.mkdir(seq_dir)
                        if not os.path.isfile(path_det_a): copy_dcm_file(source = path_i_file, destination = path_det_a)

                    elif ds.ImageType[6] == "DET_B" and ds.ImageType[0] == "ORIGINAL" and ds.SeriesNumber in max_series33:
                        path_det_b = os.path.join(output_dir, i_dir, "33", str(ds.SeriesNumber), i_file)
                        seq_dir = os.path.join(output_dir, i_dir, "33", str(ds.SeriesNumber))
                        if not os.path.isdir(seq_dir): os.mkdir(seq_dir)
                        if not os.path.isfile(path_det_b): copy_dcm_file(source = path_i_file, destination = path_det_b)

                except:
                    c_failure += 1
                    print("Failure B")
                    #print("'FileDataset' %s could not be processed.  has it no attribute 'ImageType'? " % i_file)
    else:
        for root, dir, files in os.walk(path_in_patient):
            for i_file in files:
                path_i_file = os.path.join(path_in_patient, i_file)
                ds = dicom.read_file(path_i_file)
                #print(os.path.join(path_in_patient, i_file))
                try:
                    if ds.ImageType[6] == "DET_A" and ds.ImageType[0] == "ORIGINAL":
                        path_det_a = os.path.join(output_dir, i_dir, "66", str(ds.SeriesNumber), i_file)
                        seq_dir = os.path.join(output_dir, i_dir, "66", str(ds.SeriesNumber))
                        if not os.path.isdir(seq_dir): os.mkdir(seq_dir)
                        if not os.path.isfile(path_det_a): copy_dcm_file(source = path_i_file, destination = path_det_a)

                    elif ds.ImageType[6] == "DET_B" and ds.ImageType[0] == "ORIGINAL":
                        path_det_b = os.path.join(output_dir, i_dir, "33", str(ds.SeriesNumber), i_file)
                        seq_dir = os.path.join(output_dir, i_dir, "33", str(ds.SeriesNumber))
                        if not os.path.isdir(seq_dir): os.mkdir(seq_dir)                    
                        if not os.path.isfile(path_det_b): copy_dcm_file(source = path_i_file, destination = path_det_b)

                except:
                    c_failure += 1
                    #print("'FileDataset' %s could not be processed.  has it no attribute 'ImageType'? " % i_file)


    print("number of files that has not bee copied: %i" % counter)
    print("number of failures occured during processing.E.g. file does not have metaheader: %i" % c_failure)

