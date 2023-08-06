# This script initializes the LaTeX author resources provided for
# Control, Optimisation and Calculus of Variations (ESAIM: COCV).
# https://www.esaim-cocv.org/author-information/latex2e-macro-package

import sys
from ste.utilities import utilities
from subprocess import run, STDOUT

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher.
        utilities.get_archive('http://ftp.edpsciences.org/pub/cocv/cocv.tar.gz')

        # Get the separate style manual as well.
        utilities.get_file('https://www.esaim-cocv.org/images/stories/instructions/cocv_instructions.pdf')

        # Compile the template file.
        run(['latexmk', '-pdf', '-norc', '-interaction=nonstopmode',  'template.tex'], stderr = STDOUT)
        run(['latexmk', '-c'  , '-norc', '-interaction=nonstopmode',  'template.tex'], stderr = STDOUT)

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
