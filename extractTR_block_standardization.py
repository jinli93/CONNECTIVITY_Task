# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import os
import time
import nibabel as nib
import numpy as np

base_dir = r'/nfs/h2/fmricenter/volume/'
task = 'obj'
rlf = 'obj.rlf'
runfile = 'Face.ev'
output_dir = r'/nfs/h1/workingshop/lijin/CONNECTIVITY/Task/raw_ts/'

sessid_file = r'/nfs/h1/workingshop/lijin/CONNECTIVITY/subjID_190'
sessid = open(sessid_file).readlines()
sessid = [line.strip() for line in sessid]

for subj in sessid:
    outputpath = os.path.join(output_dir, subj)
    frlf = open(os.path.join(base_dir, subj, task, rlf))
    run_list = [line.strip() for line in frlf]
    i = 0
    face = np.zeros((60, 72, 60, 54))
    for r in run_list:
        func = nib.load(os.path.join(base_dir, subj, task, r, 'func.feat', 'standard_filtered_func_data.nii.gz'))
        func_data = func.get_data()

        affine = func.get_affine()

        runf = open(os.path.join(base_dir, subj, task, r, runfile))
        runf_data = [line.strip() for line in runf]
        temp_1 = ''.join(runf_data[0])
        TR_1 = float(temp_1[0:3])
        temp_2 = ''.join(runf_data[1])
        TR_2 = float(temp_2[0:3])
        avg_1 = np.mean(func_data[:, :, :, (TR_1 / 2):(TR_1 / 2 + 9)], axis=3)
        std_1 = np.std(func_data[:, :, :, (TR_1 / 2):(TR_1 / 2 + 9)], axis=3)
        avg_2 = np.mean(func_data[:, :, :, (TR_2 / 2):(TR_2 / 2 + 9)], axis=3)
        std_2 = np.std(func_data[:, :, :, (TR_2 / 2):(TR_2 / 2 + 9)], axis=3)
        n = 0;
        m = 0;
        for j in range(i,i+18):
            if (j < 9) or (j >= 18 and j < 27) or (j >=36 and j<45):
                face[:, :, :, j] = (func_data[:, :, :, (TR_1 / 2 + n)] - avg_1) / std_1
                n = n+1;
            else:
                face[:, :, :, j] = (func_data[:, :, :, (TR_2 / 2 + m)] - avg_2) / std_2
                m = m+1;
        i = j + 1
    face[np.isnan(face)] = 0
    face_vol = nib.Nifti1Image(face, affine)
    nib.save(face_vol, outputpath + '/fa/007/' + 'func_fa_stand.nii.gz') 
	
    print subj + 'is ok!'
