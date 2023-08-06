# This script initializes the LaTeX author resources provided for
# International Journal for Uncertainty Quantification (IJUQ).
# https://www.submission.begellhouse.com/help/hub.html

import os
import sys
from ste.utilities import utilities

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher.
        utilities.get_archive('https://www.submission.begellhouse.com/download/latex_template/52034eb04b657aea/IJUQ_Latex_Template.zip')

        # Get the non-standard uarial.sty as well as a substitute for arial.sty.
        utilities.get_file('https://mirrors.ctan.org/fonts/urw/arial/latex/uarial.sty')
        utilities.link_or_copy('uarial.sty', 'arial.sty')

        # The file IJ4UQ_Bibliography_Style.bst has an issue causing 'r is an illegal
        # case-conversion string' error messages.
        # We apply a patch created via
        #   diff -u IJ4UQ_Bibliography_Style.bst IJ4UQ_Bibliography_Style-scoop.bst > IJ4UQ_Bibliography_Style.bst.patch
        utilities.apply_patch('IJ4UQ_Bibliography_Style.bst.patch')

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
