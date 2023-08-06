# This script initializes the LaTeX author resources provided for
# Journal of Applied Mathematics and Mechanics (ZAMM).
# https://onlinelibrary.wiley.com/page/journal/15214001/homepage/2233_authorguidelines.html

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
        utilities.get_archive('https://onlinelibrary.wiley.com/pb-assets/assets/15214001/ACS-stix_New-1659350218477.zip', junk = 1, method = "wget")

        # Move the content of the acs/ directory one up.
        for f in glob.glob(f'acs/*'):
            # Proceed only if the object is a file (not a directory).
            if os.path.isfile(f):
                destination = f
                destination = re.sub(r'.*?/', '', destination, count = 1)

                # Construct the full path of the destination.
                # This may be necessary in order to allow files to be overwritten.
                destination = os.path.join(os.getcwd(), destination)
                shutil.move(f, destination)

        # Wiley journals use different versions of WileyNJD-v2.cls under the same name.
        # We rename the file in a journal specific way for the purpose of disambiguation.
        utilities.link_or_copy('WileyNJD-v2.cls', 'WileyNJD-v2-zamm.cls')

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
