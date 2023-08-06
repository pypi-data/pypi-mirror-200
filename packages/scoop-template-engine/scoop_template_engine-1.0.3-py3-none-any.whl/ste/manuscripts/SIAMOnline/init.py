# This script initializes the LaTeX author resources provided for
# SIAM online journals.
# https://epubs.siam.org/journal-authors

import sys
from ste.utilities import utilities

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher.
        utilities.get_archive('https://epubs.siam.org/pb-assets/macros/online/siamonline_220329.zip', method = "wget")

        # Get the separate style manual as well.
        utilities.get_file('https://epubs.siam.org/pb-assets/files/SIAM_STYLE_GUIDE_2019.pdf', method = "wget")

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
