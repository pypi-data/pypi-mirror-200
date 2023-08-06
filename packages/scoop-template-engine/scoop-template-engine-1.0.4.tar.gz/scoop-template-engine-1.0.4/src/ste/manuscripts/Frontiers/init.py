# This script initializes the LaTeX author resources provided for
# Frontiers journals.
# https://www.frontiersin.org/journals/applied-mathematics-and-statistics/sections/optimization#author-guidelines

import sys
from ste.utilities import utilities

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher.
        utilities.get_archive('https://www.frontiersin.org/design/zip/Frontiers_LaTeX_Templates.zip')

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
