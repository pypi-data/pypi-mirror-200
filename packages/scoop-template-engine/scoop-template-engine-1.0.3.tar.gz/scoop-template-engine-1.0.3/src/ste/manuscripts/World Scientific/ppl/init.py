# This script initializes the LaTeX author resources provided for
# Parallel Processing Letters (PPL).
# https://www.worldscientific.com/page/authors/journal-stylefiles

import sys
from ste.utilities import utilities

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher.
        utilities.get_archive('https://www.worldscientific.com/sda/1037/ppl-2e.zip')

        # Get the separate style manual as well.
        utilities.get_file('https://www.worldscientific.com/sda/1037/ws-ppl.pdf')

        # The file ws-ppl.bst has some issues.
        # One issue is that a @BOOK entry requires the VOLUME field to be nonempty whenever the SERIES field is nonempty.
        # Another issue is that @PHDTHESIS without an ADDRESS field but with a YEAR field yields an error.
        # We apply a patch created via
        #   diff -u ws-ppl.bst ws-ppl-scoop.bst > ws-ppl.bst.patch
        utilities.apply_patch('ws-ppl.bst.patch')

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
