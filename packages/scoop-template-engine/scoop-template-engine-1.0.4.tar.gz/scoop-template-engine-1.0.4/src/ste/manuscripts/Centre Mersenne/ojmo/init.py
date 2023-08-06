# This script initializes the LaTeX author resources provided for
# Open Journal of Mathematical Optimization (OJMO).
# https://ojmo.centre-mersenne.org/page/latex/

import sys
from ste.utilities import utilities

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher.
        utilities.get_archive('https://www.centre-mersenne.org/media/texmf/pack_author-ojmo.zip', junk = 1)

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
