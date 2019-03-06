from nipype.interfaces.base import TraitedSpec, \
    File, \
    Str, \
    traits, \
    InputMultiPath, \
    isdefined
from nipype.interfaces.ants.base import ANTSCommand, \
    ANTSCommandInputSpec, \
    LOCAL_DEFAULT_NUMBER_OF_THREADS
import os

"""
based on AntsRegistrationSynQuick.sh wrapper:
https://github.com/djarecka/nipype/blob/5cd952fae1c3f913fa9ee37ff0ee38187c3032fe/nipype/interfaces/ants/registration.py
"""

class RegistrationSynInputSpec(ANTSCommandInputSpec):
    dimension = traits.Enum(3, 2, argstr='-d %d',
                            usedefault=True, desc='image dimension (2 or 3)')
    fixed_image = InputMultiPath(File(exists=True), mandatory=True, argstr='-f %s...',
                                 desc='Fixed image or source image or reference image')
    moving_image = InputMultiPath(File(exists=True), mandatory=True, argstr='-m %s...',
                                  desc='Moving image or target image')
    output_prefix = Str("transform", usedefault=True, argstr='-o %s',
                        desc="A prefix that is prepended to all output files")
    num_threads = traits.Int(default_value=LOCAL_DEFAULT_NUMBER_OF_THREADS, usedefault=True,
                             desc='Number of threads (default = 1)', argstr='-n %d')

    transform_type = traits.Enum('s', 't', 'r', 'a', 'sr', 'b', 'br', argstr='-t %s',
                                 desc="""
                                 transform type
                                 t:  translation
                                 r:  rigid
                                 a:  rigid + affine
                                 s:  rigid + affine + deformable syn (default)
                                 sr: rigid + deformable syn
                                 b:  rigid + affine + deformable b-spline syn
                                 br: rigid + deformable b-spline syn""",
                                 usedefault=True)

    use_histogram_matching = traits.Bool(False, argstr='-j %d',
                                         desc='use histogram matching')
    histogram_bins = traits.Int(default_value=32, argstr='-r %d',
                                desc='histogram bins for mutual information in SyN stage \
                                 (default = 32)')
    spline_distance = traits.Int(default_value=26, argstr='-s %d',
                                 desc='spline distance for deformable B-spline SyN transform \
                                 (default = 26)')
    precision_type = traits.Enum('double', 'float', argstr='-p %s',
                                 desc='precision type (default = double)', usedefault=True)


class RegistrationSynOutputSpec(TraitedSpec):
    warped_image = File(exists=True, desc="Warped image")
    inverse_warped_image = File(exists=True, desc="Inverse warped image")
    out_matrix = File(exists=True, desc='Affine matrix')
    forward_warp_field = File(exists=True, desc='Forward warp field')
    inverse_warp_field = File(exists=True, desc='Inverse warp field')

class RegistrationSyn(ANTSCommand):
    """
    Registration using a symmetric image normalization method (SyN).
    You can read more in Avants et al.; Med Image Anal., 2008
    (https://www.ncbi.nlm.nih.gov/pubmed/17659998).
    Examples
    --------
    [....]
    """


    _cmd = 'antsRegistrationSyn.sh'
    input_spec = RegistrationSynInputSpec
    output_spec = RegistrationSynOutputSpec

    def _num_threads_update(self):
        """
        antsRegistrationSyn.sh ignores environment variables,
        so override environment update frm ANTSCommand class
        """
        pass

    def _format_arg(self, name, spec, value):
        if name == 'precision_type':
            return spec.argstr % value[0]
        return super(RegistrationSyn, self)._format_arg(name, spec, value)

    def _list_outputs(self):
        outputs = self.output_spec().get()
        out_base = os.path.abspath(self.inputs.output_prefix)
        outputs['warped_image'] = out_base + 'Warped.nii.gz'
        outputs['inverse_warped_image'] = out_base + 'InverseWarped.nii.gz'
        outputs['out_matrix'] = out_base + '0GenericAffine.mat'

        if self.inputs.transform_type not in ('t', 'r', 'a'):
            outputs['forward_warp_field'] = out_base + '1Warp.nii.gz'
            outputs['inverse_warp_field'] = out_base + '1InverseWarp.nii.gz'
return outputs
