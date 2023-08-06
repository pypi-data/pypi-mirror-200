import shlex
import sys

from neuropredict.classify import cli


out_dir = '/Users/Reddy/dev/rotman-dev/freesurfer_QC/site_predict/ONDRI_FSv6/CAM_ROB_SBH_G_SMH_TOH_TWH'

sys.argv = shlex.split('np_classify -z {}'.format(out_dir))

cli()

