# Import to main file with:
#                           from skullstripping import *
# connection example: main_wf.connect(datasource, 'subject_id', skull_stripping, 'conv_mgz.in_file')

from nipype.pipeline.engine import Workflow, Node, MapNode
import nipype.interfaces.fsl as fsl
import nipype.interfaces.freesurfer as fs


#mri_convert --in_type nii --out_type mgz --input_volume $tmpdir/${subj_str}_roi.nii.gz --output_volume $tmpdir/${subj_str}_cut.mgz"
conv_mgz = Node(interface=fs.MRIConvert(in_type = 'nii',
                                       out_type = 'mgz'),
                name = 'conv_mgz')

#mri_watershed -atlas $tmpdir/${subj_str}_cut.mgz $tmpdir/${subj_str}_skullstrip.mgz
watershed = Node(interface=fs.WatershedSkullStrip(),
                name = 'watershed')
#mri_convert -i $tmpdir/${subj_str}_skullstrip.mgz -o $tmpdir/${subj_str}_fertig.nii.gz
conv_nii = Node(interface=fs.MRIConvert(in_type = 'mgz',
                                       out_type = 'nii'),
                name = 'conv_nii')
#bet $tmpdir/${subj_str}_fertig.nii.gz $brainsdir/${subj_str}_brain.nii.gz -m -R -c $cog -f 0.5
bet = Node(interface=fsl.BET(robust = True,
                            mask = True,
                            frac=0.35),
          name='bet')


skull_stripping = Workflow(name='skull_stripping',
                          base_dir='./')
skull_stripping.connect(conv_mgz, 'out_file', watershed, 'in_file')
skull_stripping.connect(watershed, 'out_file', conv_nii, 'in_file')
skull_stripping.connect(conv_nii, 'out_file', bet, 'in_file')
