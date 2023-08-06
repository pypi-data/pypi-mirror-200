# This script initializes the LaTeX author resources provided for
# Springer Nature journals based on the sn-jnl.cls document class.
# https://www.springer.com/journal/10851/submission-guidelines
# https://www.springernature.com/gp/authors/campaigns/latex-author-support

import sys
from ste.utilities import utilities

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher.
        utilities.get_archive('https://media.springernature.com/full/springer-cms/rest/v1/content/18782940/data/Download+the+journal+article+template+package.zip', junk = 2)

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
