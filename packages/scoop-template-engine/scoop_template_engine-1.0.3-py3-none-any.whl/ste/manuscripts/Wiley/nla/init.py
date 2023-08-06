# This script initializes the LaTeX author resources provided for
# Numerical Linear Algebra with Applications (NLA).
# https://onlinelibrary.wiley.com/page/journal/10991506/homepage/forauthors.html
# https://onlinelibrary.wiley.com/page/journal/10991506/homepage/la_tex_class_file.htm

import glob
import os
import re
import shutil
import sys
from ste.utilities import utilities

if __name__ == '__main__':
    try:
        # Remove the initialization time and version stamp.
        utilities.remove_time_version_stamp()

        # Get and unpack the LaTeX author resources from the publisher, using wget.
        utilities.get_archive('https://onlinelibrary.wiley.com/pb-assets/assets/10991506/VANCOUVER-stix_New-1658936365330.zip', junk = 1, method = "wget")

        # Move the content of the VANCOUVER/ directory one up.
        for f in glob.glob(f'VANCOUVER/*'):
            # Proceed only if the object is a file (not a directory).
            if os.path.isfile(f):
                destination = f
                destination = re.sub(r'.*?/', '', destination, count = 1)

                # Construct the full path of the destination.
                # This may be necessary in order to allow files to be overwritten.
                destination = os.path.join(os.getcwd(), destination)
                shutil.move(f, destination)

        # The WileyNJD-v2.cls file requires WileyNJD-VANCOUVER.bst but the author resources contain wileyNJD-VANCOUVER.bst.
        # We rename the file since symbolic links to files differing only w.r.t. the case cause issues on macOS.
        source = 'wileyNJD-VANCOUVER.bst'
        destination = os.path.join(os.getcwd(), 'WileyNJD-VANCOUVER.bst')
        shutil.move(source, destination)

        # Wiley journals use different versions of WileyNJD-v2.cls under the same name.
        # We rename the file in a journal specific way for the purpose of disambiguation.
        utilities.link_or_copy('WileyNJD-v2.cls', 'WileyNJD-v2-nla.cls')

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
