# This script initializes the LaTeX author resources provided for
# IMA Journal of Numerical Analysis.
# https://academic.oup.com/imajna/pages/General_Instructions

import sys
from ste.utilities import utilities

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher.
        utilities.get_archive('https://static.primary.prod.gcms.the-infra.com/static/site/imamat/document/ima-authoring-template.zip?node=ad2e6afe141e2df8c873')

        # Get the separate style manual as well.
        utilities.get_file('https://static.primary.prod.gcms.the-infra.com/static/site/imajna/document/styleguide.pdf?node=5b8886f8fcd3ab63fda8')

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
