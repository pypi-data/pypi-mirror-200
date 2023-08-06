# This script initializes the LaTeX author resources provided for
# BIT Numerical Mathematics (BIT).
# https://projects.mai.liu.se/BIT/Contributions.html

import os
import sys
from ste.utilities import utilities
from subprocess import run, STDOUT

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get the LaTeX author resources from the publisher.
        utilities.get_file('https://projects.mai.liu.se/BIT/BITtemplate.tex')
        utilities.get_file('https://projects.mai.liu.se/BIT/svjour3.cls')
        utilities.get_file('https://projects.mai.liu.se/BIT/svglov3.clo')
        utilities.get_file('https://projects.mai.liu.se/BIT/usrguid3.pdf')

        # Link to spmpsci.bst which is recommended but not available from the author resources page.
        utilities.link_or_copy('../svjour3.cls/spmpsci.bst', 'spmpsci.bst')

        # Compile the template file.
        run(['latexmk', '-pdf', '-norc', '-interaction=nonstopmode',  'BITtemplate.tex'], stderr = STDOUT)
        run(['latexmk', '-c'  , '-norc', '-interaction=nonstopmode',  'BITtemplate.tex'], stderr = STDOUT)

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
