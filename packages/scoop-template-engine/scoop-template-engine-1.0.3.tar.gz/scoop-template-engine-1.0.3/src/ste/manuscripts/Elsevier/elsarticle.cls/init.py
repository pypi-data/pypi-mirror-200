# This script initializes the LaTeX author resources provided for
# Elsevier journals.
# https://www.elsevier.com/authors/author-schemas/latex-instructions

import sys
from ste.utilities import utilities
from subprocess import run, STDOUT

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher.
        utilities.get_archive('https://mirrors.ctan.org/macros/latex/contrib/elsarticle.zip', junk = 1)

        # Run the installer, which is going to create the elsarticle.cls file.
        run(['latex', 'elsarticle.ins'], stderr = STDOUT)

        # Compile the template files.
        run(['latexmk', '-pdf', '-norc', '-interaction=nonstopmode',  'elsarticle-template-harv.tex'], stderr = STDOUT)
        run(['latexmk', '-c'  , '-norc', '-interaction=nonstopmode',  'elsarticle-template-harv.tex'], stderr = STDOUT)

        run(['latexmk', '-pdf', '-norc', '-interaction=nonstopmode',  'elsarticle-template-num.tex'], stderr = STDOUT)
        run(['latexmk', '-c'  , '-norc', '-interaction=nonstopmode',  'elsarticle-template-num.tex'], stderr = STDOUT)

        run(['latexmk', '-pdf', '-norc', '-interaction=nonstopmode',  'elsarticle-template-num-names.tex'], stderr = STDOUT)
        run(['latexmk', '-c'  , '-norc', '-interaction=nonstopmode',  'elsarticle-template-num-names.tex'], stderr = STDOUT)

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
