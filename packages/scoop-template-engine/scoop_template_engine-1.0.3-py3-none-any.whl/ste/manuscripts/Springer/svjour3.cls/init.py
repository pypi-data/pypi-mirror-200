# This script initializes the LaTeX author resources provided for
# Springer journals based on the svjour3.cls document class.
# https://www.springer.com/journal/245/submission-guidelines

import sys
from ste.utilities import utilities

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher.
        utilities.get_archive('https://media.springer.com/full/springer-instructions-for-authors-assets/zip/468198_LaTeX_DL_468198_240419.zip', junk = 1)

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
