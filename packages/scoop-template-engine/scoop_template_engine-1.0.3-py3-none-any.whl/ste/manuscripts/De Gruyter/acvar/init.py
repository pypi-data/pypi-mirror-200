# This script initializes the LaTeX author resources provided for
# Advances in Calculus of Variations (ACVAR).
# https://www.degruyter.com/journal/key/acv/html

import sys
from ste.utilities import utilities

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher.
        utilities.get_archive('https://www.degruyter.com/publication/journal_key/ACV/downloadAsset/ACV_LaTeX-Template-for-Authors.zip')

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
