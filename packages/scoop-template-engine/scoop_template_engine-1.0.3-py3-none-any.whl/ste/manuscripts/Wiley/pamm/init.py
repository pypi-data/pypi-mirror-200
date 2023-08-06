# This script initializes the LaTeX author resources provided for
# Proceedings in Applied Mathematics and Mechanics (PAMM).
# https://onlinelibrary.wiley.com/page/journal/16177061/homepage/2130_authorguidelines.html

import sys
from ste.utilities import utilities

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher.
        utilities.get_archive('https://www.wiley-vch.de/vch/journals/2130/public/pamm_latex_unix.tgz', junk = 1)

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
