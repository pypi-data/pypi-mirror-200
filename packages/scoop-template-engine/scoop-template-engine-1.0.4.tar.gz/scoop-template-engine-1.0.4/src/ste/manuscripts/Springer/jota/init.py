# This script initializes the LaTeX author resources provided for
# Journal of Optimization Theory and Applications (JOTA).
# https://www.springer.com/journal/10957/submission-guidelines

import re
import sys
from ste.utilities import utilities

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher.
        utilities.get_archive('https://media.springer.com/full/springer-instructions-for-authors-assets/zip/1705114_LaTeX%20JOTA.zip')

        # Fix the missing comment in the spmpsci.bst file.
        data = open('spmpsci.bst', 'r', newline = '\r\n').read()
        data = re.sub(r'`vonx', r'%% `vonx', data)
        open('spmpsci.bst', 'w').write(data)

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
