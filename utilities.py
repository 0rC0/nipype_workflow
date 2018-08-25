def spm_tissues(in_list):
    '''
    from a SPM NewSegment Tissues list, return GM, WM and CSf

    Example Node:
    spm_tissues_split = Node(
    Function(['in_list'], ['gm', 'wm', 'csf'], spm_tissues), name='spm_tissues_split')

    '''
    return in_list[0][0], in_list[1][0], in_list[2][0]

def count_voxels(in_file):
    '''
    count voxels for the a given nifti
    from the benchmarks seems faster then fslstats -V
    :param in_file:
    :return: number of voxel, volume in mm^3 (voxel * pixdim)
    '''
    import nibabel as nib
    import numpy as np
    img = nib.load(in_file)
    voxels = (img.get_fdata() != 0).sum()
    volume = img.header['pixdim'][[1,2,3]].prod() * voxels
    return voxels, volume

# From https://github.com/spinoza-centre/spynoza/blob/master/spynoza/utils.py - MIT License
def split_4D_to_3D(in_file):
    """split_4D_to_3D splits a single 4D file into a list of nifti files.
    Because it splits the file at once, it's faster than fsl.ExtractROI
    Parameters
    ----------
    in_file : str
        Absolute path to nifti-file.
    Returns
    -------
    out_files : list
        List of absolute paths to nifti-files.    """

    import nibabel as nib
    import os
    import tempfile

    original_file = nib.load(in_file)
    affine = original_file.affine
    header = original_file.header
    dyns = original_file.shape[-1]

    data = original_file.get_data()
    tempdir = tempfile.gettempdir()
    fn_base = os.path.split(in_file)[-1][:-7]  # take off .nii.gz

    out_files = []
    for i in range(dyns):
        img = nib.Nifti1Image(data[..., i], affine=affine, header=header)
        opfn = os.path.join(tempdir, fn_base + '_%s.nii.gz' % str(i).zfill(4))
        nib.save(img, opfn)
        out_files.append(opfn)

    return out_files


Split_4D_to_3D = Function(function=split_4D_to_3D, input_names=['in_file'],
output_names=['out_files'])
