# This script initializes the LaTeX author resources provided for
# International Journal of Computational Methods (IJCM).
# https://www.worldscientific.com/page/authors/journal-stylefiles

import sys
from ste.utilities import utilities

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher.
        utilities.get_archive('https://www.worldscientific.com/sda/1037/ijcm-2e.zip')

        # Get the separate style manual as well.
        utilities.get_file('https://www.worldscientific.com/sda/1037/ws-ijcm.pdf')

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
