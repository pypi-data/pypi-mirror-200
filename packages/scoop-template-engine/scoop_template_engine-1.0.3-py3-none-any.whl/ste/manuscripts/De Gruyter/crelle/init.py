# This script initializes the LaTeX author resources provided for
# Journal für die reine und angewandte Mathematik (Crelle).
# https://www.degruyter.com/journal/key/crll/html

import re
import sys
from ste.utilities import utilities
from subprocess import run, STDOUT

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher.
        utilities.get_archive('https://www.degruyter.com/publication/journal_key/CRLL/downloadAsset/CRLL_LaTeX_template.zip')

        # Activate the template file by uncommenting one of the \documentclass lines.
        data = open('article.tex', 'r').read()
        data = re.sub(r'%% (\\documentclass\[SecEq)', r'\1', data)
        open('article.tex', 'w').write(data)

        # Compile the template file.
        run(['latexmk', '-pdf', '-norc', '-interaction=nonstopmode',  'article.tex'], stderr = STDOUT)
        run(['latexmk', '-c'  , '-norc', '-interaction=nonstopmode',  'article.tex'], stderr = STDOUT)

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
