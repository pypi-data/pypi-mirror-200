# This script initializes the LaTeX author resources provided for
# Mathematics of Computation (MCOM).
# https://www.ams.org/publications/journals/journalsframework/mcomauthorpac

import sys
from ste.utilities import utilities
from subprocess import run, STDOUT

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher.
        utilities.get_archive('https://www.ams.org/arc/journals/packages/mcom/mcom_amslatex.zip', junk = 1)

        # Compile the template file.
        run(['latexmk', '-pdf', '-norc', '-interaction=nonstopmode',  'mcom-l-template.tex'], stderr = STDOUT)
        run(['latexmk', '-c'  , '-norc', '-interaction=nonstopmode',  'mcom-l-template.tex'], stderr = STDOUT)

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
