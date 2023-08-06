# This script initializes the LaTeX author resources provided for
# American Chemical Society journals.
# https://pubs.acs.org/page/4authors/submission/tex.html

import shutil
import sys
from ste.utilities import utilities
from subprocess import run, STDOUT

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from CTAN.
        utilities.get_archive('https://mirrors.ctan.org/macros/latex/contrib/achemso.zip', junk = 1)

        # Run the installer, which is going to create the .cls, .bst, .cfg, .sty files.
        run(['latex', 'achemso.ins'], stderr = STDOUT)

        # Correct misnamed files.
        shutil.move('achemso-inoraj.cfg', 'achemso-inocaj.cfg')
        shutil.move('achemso-appccd.cfg', 'achemso-apaccd.cfg')

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
