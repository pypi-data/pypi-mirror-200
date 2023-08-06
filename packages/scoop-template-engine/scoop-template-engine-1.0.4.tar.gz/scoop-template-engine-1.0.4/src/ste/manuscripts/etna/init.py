# This script initializes the LaTeX author resources provided for
# Electronic Transactions on Numerical Analysis (ETNA).
# https://etna.ricam.oeaw.ac.at/submissions/latex/
# https://etna.ricam.oeaw.ac.at/submissions/

import sys
from ste.utilities import utilities
from subprocess import run, STDOUT

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get the LaTeX author resources from the publisher.
        utilities.get_file('https://etna.ricam.oeaw.ac.at/submissions/latex/example.tex')
        utilities.get_file('https://etna.ricam.oeaw.ac.at/submissions/latex/etna.cls')
        utilities.get_file('https://etna.ricam.oeaw.ac.at/submissions/ETNA_guidelines.pdf')

        # Compile the template file.
        run(['latexmk', '-pdf', '-norc', '-interaction=nonstopmode',  'example.tex'], stderr = STDOUT)
        run(['latexmk', '-c'  , '-norc', '-interaction=nonstopmode',  'example.tex'], stderr = STDOUT)

        # The file etna.cls has some issues.
        # One issue is that it redefines \@begintheorem in a way incompatible with amsthm.sty.
        # However we would like to use amsthm.sty, which offers cleveref.sty support with a combined counter for all
        # theorem-like environments.
        # Also, it defines remark and example environments which cause some trouble.
        # We apply a patch created via
        #   diff -u etna.cls etna-scoop.cls > etna.cls.patch
        utilities.apply_patch('etna.cls.patch')

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
