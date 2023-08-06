# This script initializes the LaTeX author resources provided for
# Mathematical Methods in the Applied Sciences (MMA).
# https://onlinelibrary.wiley.com/page/journal/10991476/homepage/latex_class_files.htm

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
        utilities.get_archive('https://onlinelibrary.wiley.com/pb-assets/assets/10991476/AMA-stix_New-1658766862393.zip', junk = 1, method = "wget")

        # Move the content of the ama/ directory one up.
        for f in glob.glob(f'ama/*'):
            # Proceed only if the object is a file (not a directory).
            if os.path.isfile(f):
                destination = f
                destination = re.sub(r'.*?/', '', destination, count = 1)

                # Construct the full path of the destination.
                # This may be necessary in order to allow files to be overwritten.
                destination = os.path.join(os.getcwd(), destination)
                shutil.move(f, destination)

        # The template wileyNJD-AMA.tex uses the 'AMA' documentclass option, which results in
        # the bibliography style WileyNJD-AMA.bst being used. This, however, requires a number of
        # non-standard fields to be set for various entry types.
        # Therefore, we resort to the WileyNJD-VANCOUVER.bst style, which is also used, e.g., by
        # the Numerical Linear Algebra and Applications (NLA) template.
        # We provide a link to this .bst file.
        utilities.link_or_copy('../nla/WileyNJD-VANCOUVER.bst', 'WileyNJD-VANCOUVER.bst')

        # Wiley journals use different versions of WileyNJD-v2.cls under the same name.
        # We rename the file in a journal specific way for the purpose of disambiguation.
        utilities.link_or_copy('WileyNJD-v2.cls', 'WileyNJD-v2-mma.cls')

        # Write the initialization time and version stamp.
        utilities.write_time_version_stamp()

    except:
        sys.exit(1)
