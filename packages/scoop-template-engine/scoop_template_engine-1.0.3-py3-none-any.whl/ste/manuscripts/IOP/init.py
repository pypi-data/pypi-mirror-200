# This script initializes the LaTeX author resources provided for
# IOP journals.
# https://publishingsupport.iopscience.iop.org/publishing-support/authors/authoring-for-journals/writing-journal-article/
# https://publishingsupport.iopscience.iop.org/questions/latex-template/

# In fact, since IOP allows us to
# "[...] format your paper in the way that you choose!"
# and their template is incompatible with amsmath.sty [IOPLaTeXGuidelines.tex],
# which we wish to support, we use a neutral preprint style as template but
# still download their author resources.

import sys
from ste.utilities import utilities

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher.
        utilities.get_archive('https://ioppservices.wpenginepowered.com/wp-content/uploads/2017/10/ioplatexguidelines-1.zip')

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
