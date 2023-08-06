# This script initializes the LaTeX author resources provided for
# AIMS journals.
# https://www.aimsciences.org/common_news/column/TexPreparation

import sys
from ste.utilities import utilities

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher.
        utilities.get_archive('https://www.aimsciences.org/others/AIMSTemplateFiles.zip', verify = False)

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
