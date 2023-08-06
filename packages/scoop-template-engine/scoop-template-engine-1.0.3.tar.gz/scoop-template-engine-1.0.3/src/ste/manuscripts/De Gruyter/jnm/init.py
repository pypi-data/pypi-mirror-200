# This script initializes the LaTeX author resources provided for
# Journal of Numerical Mathematics (JNM).
# https://www.degruyter.com/journal/key/jnma/html

import sys
from ste.utilities import utilities

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher.
        utilities.get_archive('https://www.degruyter.com/publication/journal_key/JNMA/downloadAsset/JNMA_LaTeX_Template_for_Authors.zip')

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
