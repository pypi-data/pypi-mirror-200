# This script initializes the LaTeX author resources provided for
# GAMM Mitteilungen.
# https://onlinelibrary.wiley.com/page/journal/15222608/homepage/2250_authorguidelines.html

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
        utilities.get_archive('https://onlinelibrary.wiley.com/pb-assets/assets/15222608/AMS-stix_New-1661331773537.zip', method = "wget")

        # Move the content of the ams/ directory one up.
        for f in glob.glob(f'ams/*'):
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
        utilities.link_or_copy('WileyNJD-v2.cls', 'WileyNJD-v2-gamm.cls')

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
