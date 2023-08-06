# This script initializes the LaTeX author resources provided for
# Journal of Nonsmooth Analysis and Optimization (JNSAO).
# https://jnsao.episciences.org/page/for-authors

import sys
from ste.utilities import utilities

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher.
        utilities.get_archive('https://jnsao.episciences.org/public/jnsao_latex.zip')

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
