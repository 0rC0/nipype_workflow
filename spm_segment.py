from nipype.pipeline.engine import Workflow, Node, MapNode
import nipype.interfaces.fsl as fsl
import nipype.interfaces.spm as spm

#Matlab and SPM configuration
# Set the way matlab should be called
# mlab.MatlabCommand.set_default_matlab_cmd("matlab -nodesktop -nosplash -nojvm -noFigureWindows")
spm_path='/opt/spm12'
mlab.MatlabCommand.set_default_matlab_cmd("matlab -nodesktop -nosplash")
mlab.MatlabCommand.set_default_paths(spm_path)

# Nodes

ro = Node(interface=fsl.Reorient2Std(output_type = 'NIFTI'), name='ro')
seg = Node(interface=spm.Segment(csf_output_type=[False,False,True],
                                gm_output_type=[False,False,True],
                                wm_output_type=[False,False,True],
                                save_bias_corrected = True),
           name="segment")

# Connections:
segment = Workflow(name='Segment', base_dir='./')
segment.connect(ro, 'out_file', seg, 'data')

# Example connection to the main Workflow:
# main = Workflow(name='main', base_dir=w_dir)
# main.connect(infosource, 'subject_id', datasource, 'subject_id')
# main.connect(datasource, 'nii', segment, 'ro.in_file')
# main.connect(segment, 'seg.bias_corrected_image', sink, '@bias_corr')
# main.connect(segment, 'seg.native_csf_image', sink, '@csf')
# main.connect(segment, 'seg. native_gm_image', sink, '@gm')
# main.connect(segment, 'seg. native_wm_image', sink, '@wm')
