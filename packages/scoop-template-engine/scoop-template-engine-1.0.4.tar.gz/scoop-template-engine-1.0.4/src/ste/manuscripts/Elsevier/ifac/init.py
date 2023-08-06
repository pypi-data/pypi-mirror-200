# This script initializes the LaTeX author resources provided for
# IFAC-PapersOnLine (IFAC).
# https://www.ifac-control.org/conferences/authors-guide

import os
import sys
from ste.utilities import utilities
from subprocess import run, STDOUT

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher.
        utilities.get_archive('https://www.ifac-control.org/conferences/resolveuid/b0e4734736878819db179d76290a8f78', junk = 1)

        # Remove some files.
        os.remove('.gitignore')

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
