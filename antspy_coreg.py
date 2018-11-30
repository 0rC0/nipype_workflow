from nipype.interfaces.base import BaseInterface, \
    BaseInterfaceInputSpec, traits, File, TraitedSpec
from nipype.utils.filemanip import split_filename

import ants
import os

class AntsPyCoregInputSpec(BaseInterfaceInputSpec):
    t1_path = File(exists = True, desc = 't1 as coregister reference', mandatory = True)
    flair_path = File(exists = True, desc = 'FLAIR as moving image', mandatory = True)
    roi_path = File(exists = True, desc = 'ROI, to apply the same transormation as the FLAIR',
                    mandatory = False)

class AntsPyCoregOutputSpec(TraitedSpec):
    coreg_flair = File(exists=True, desc="coregistered FLAIR")
    coreg_roi = File(exists=True, desc="coregistered ROI")


class AntsPyCoreg(BaseInterface):
    input_spec = AntsPyCoregInputSpec
    output_spec = AntsPyCoregOutputSpec

    def _run_interface(self, runtime):
        t1 = ants.image(self.inputs.t1_path)
        flair = ants.image(self.inputs.flair_path)
        roi = ants.image(self.inputs.roi_path)
        reg = ants.registration( t1, flair, 'SyN', reg_iterations = [100,100,20] )
        coreg_flair = ants.apply_transforms( fixed = t1, 
                                       moving = flair, 
                                       transformlist = reg[ 'invtransforms'], 
                                       interpolator  = 'nearestNeighbor', 
                                       whichtoinvert = [False,False])
        coreg_les = ants.apply_transforms( fixed = t1, 
                                       moving = les, 
                                       transformlist = reg[ 'invtransforms'], 
                                       interpolator  = 'nearestNeighbor', 
                                       whichtoinvert = [False,False])
        _, base, _ = split_filename(self.inputs.flair_path)
        coreg_flair.to_file(base + '_flair_coreg.nii.gz')
        coreg_roi.to_file(base + '_roi_coreg.nii.gz') 
        return runtime

    def _list_outputs(self):
        outputs = self._outputs().get()
        _, base, _ = split_filename(self.inputs.flair_path)
        outputs["coreg_flair"] = os.path.abspath(base + '_flair_coreg.nii.gz')
        outputs["coreg_roi"] = os.path.abspath(base + '_roi_coreg.nii.gz')
        return outputs
