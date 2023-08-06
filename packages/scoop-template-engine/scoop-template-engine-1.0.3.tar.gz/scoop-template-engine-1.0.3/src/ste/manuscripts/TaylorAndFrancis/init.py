# This script initializes the LaTeX author resources provided for
# Taylor and Francis journals.
# https://www.tandfonline.com/action/authorSubmission?show=instructions\&journalCode=gopt20

import sys
from ste.utilities import utilities

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher.
        utilities.get_archive('https://files.taylorandfrancis.com/InteractNLMLaTeX.zip')

        # Get the separate style manual as well.
        utilities.get_file('https://files.taylorandfrancis.com/tf_NLM.pdf')

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
