# This script initializes the LaTeX author resources provided for
# Springer journals based on the bmcart.cls document class.
# https://advancesincontinuousanddiscretemodels.springeropen.com/submission-guidelines/preparing-your-manuscript
# https://bmcbioinformatics.biomedcentral.com/submission-guidelines/preparing-your-manuscript

import sys
from ste.utilities import utilities

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher.
        utilities.get_archive('https://resource-cms.springernature.com/springer-cms/rest/v1/content/18361120/data/v2', junk = 1)

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
