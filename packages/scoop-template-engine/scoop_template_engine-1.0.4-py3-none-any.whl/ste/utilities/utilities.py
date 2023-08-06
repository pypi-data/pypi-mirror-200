import cloudscraper
import datetime
import glob
import importlib.metadata
import os
import patch
import re
import requests
import shutil
import sys
import tempfile
import setuptools_git_versioning
from subprocess import run, STDOUT


# Define a neutral user agent.
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

def get_file(url, verify = True, method = "requests"):
    """
    Retrieves a file from a given url, writes it to the current directory and
    returns the file name.
    """

    if method == "wget":
        # The 'wget' option uses the system-level 'wget' which is capable of
        # overcoming some protections against automated downloads.
        print('Retrieving {0:s} using wget'.format(url))
        filename = url.split("/")[-1]
        filename = filename.split("?")[0]
        print('File name from URL: {0:s}'.format(filename))
        try:
            # We need 'shell = True' likely since some download protection mechanisms
            # check the environment. '--timestamping' is used in order to make wget
            # overwrite possibly existing copies of the file.
            command = 'wget --user-agent="' + userAgent + '" --timestamping --trust-server-names ' + url
            print('Running {0:s}'.format(command))
            run(command, shell = True, stderr = STDOUT)
        except FileNotFoundError:
            print('wget does not seem to be available on your system. Unable to retrieve {0:s}. The template will not be available.'.format(url))

    elif method == "requests":
        # Retrieve the URL using 'requests'.
        print('Retrieving {0:s} using requests'.format(url))
        r = requests.get(url, verify = verify)

        # If the request was rejected, try again using a neutral user agent.
        if not r.ok:
            headers = {"User-Agent": userAgent}
            r = requests.get(url, verify = verify, headers = headers)

        # Retrieve the file name.
        filename = get_filename(r)

        # Write out the raw content.
        with open(filename, 'wb') as f:
            f.write(r.content)

    elif method == "cloudscraper":
        # Retrieve the URL using 'cloudscraper'.
        print('Retrieving {0:s} using cloudscraper'.format(url))
        scraper = cloudscraper.create_scraper()
        r = scraper.get(url, verify = verify)

        # Retrieve the file name.
        filename = get_filename(r)

        # Write out the raw content.
        with open(filename, 'wb') as f:
            f.write(r.content)

    else:
        # Unknown download method.
        print(f'Unknown download method {method}.')
        sys.exit(1)

    # Return the file name.
    return filename


def get_filename(r):
    """
    Retrieves the file name from the request r.
    """
    # Construct the file name either as specified by the server, or else from
    # the URL. The header field 'Content-Disposition', if it exists, typically
    # reads
    #   Content-Disposition: attachment
    #   Content-Disposition: attachment; filename="file.zip"
    #   Content-Disposition: inline; filename="file.zip"

    # Try the 'Content-Disposition' header field.
    filename = r.headers.get("Content-Disposition")
    if filename and re.search('^(attachment|inline)', filename):
        filename = re.findall(r'^(?:attachment|inline); filename=(.*)$', filename)[0]
        # Strip enclosing single or double quotes from the file name.
        filename = filename.strip('\'')
        filename = filename.strip('\"')

    # If this is not successful, extract the file name from the URL.
    if not filename:
        filename = r.url.split("/")[-1]
        filename = filename.split("?")[0]
        print('File name from URL: {0:s}'.format(filename))
    else:
        print('File name from header: {0:s}'.format(filename))

    return filename


def get_archive(url, verify = True, junk = 0, method = "requests"):
    """
    Retrieves an archive file from a given url, extracts it and writes the
    content to the current directory with the required number of leading
    directories junked from the path.
    """

    # Retrieve the archive file.
    filename = get_file(url, verify = verify, method = method)

    # Unpack the archive into a temporary directory (plus whatever relative paths
    # there may be associated with the archive's content).
    tmpdir = 'tmp'
    print('Unpacking {0:s} into {1:s}'.format(filename, tmpdir))
    shutil.unpack_archive(filename, tmpdir)

    # Move the archive's content into the current directory, i.e., junk the
    # tmpdir and whichever number of additional path components as indicated
    # through the junk parameter.
    for f in glob.glob(f'{tmpdir}/**/*', recursive = True) + glob.glob(f'{tmpdir}/**/.*', recursive = True):

        # Proceed only if the object is a file (not a directory).
        if os.path.isfile(f):
            # Construct the relative path of the destination.
            # Remove the tmpdir/ component from the left.
            regex = r'^' + tmpdir + r'/'
            destination = f
            destination = re.sub(regex, '', destination, count = 1)

            # Remove up to 'junk' many additional path components from the left.
            if junk > 0:
                destination = re.sub(r'.*?/', '', destination, count = junk)

            # Construct the full path of the destination.
            # This may be necessary in order to allow files to be overwritten.
            destination = os.path.join(os.getcwd(), destination)

            # Make sure the destination directory exists.
            if not os.path.exists(os.path.dirname(destination)):
                os.mkdir(os.path.dirname(destination))

            # Move the file.
            print('Moving {0:s} to {1:s}'.format(f, destination))
            shutil.move(f, destination)

    # Remove the archive folder
    shutil.rmtree(tmpdir)


def apply_patch(patchFile):
    """
    Applies the patches described in the patch file.
    """
    # Since https://pypi.org/project/patch/ modifies the source file in place and
    # does not honor the target file, we create a work around. For each patch
    # item, we copy its source file into a temporary file, then apply the patch
    # file, move the patched source files to their destination and move the
    # temporary copies back to the source files.

    # Read the patch data.
    patchData = patch.fromfile(patchFile)

    # Create lists of source, target, and temporary file names.
    sourceFiles = []
    tempFiles = []
    targetFiles = []

    # Iterate over the files to be patched.
    for patchItem in patchData.items:

        # Get and store the files affected by the current patch item.
        sourceFile = patchItem.source
        targetFile = patchItem.target
        tempFile = tempfile.mkstemp()[1]

        # Copy the source file to the temporary file.
        shutil.copy(sourceFile, tempFile)

        # Store the file names.
        sourceFiles.append(sourceFile)
        targetFiles.append(targetFile)
        tempFiles.append(tempFile)

    # Apply the patch set to all files.
    patchData.apply()

    # Iterate over the files again.
    for sourceFile, targetFile, tempFile in zip(sourceFiles, targetFiles, tempFiles):
        # Move the patched source file to its target.
        shutil.move(sourceFile, targetFile)

        # Retrieve the original source file from the temporary file.
        shutil.move(tempFile, sourceFile)


def link_or_copy(source, destination):
    """
    Tries to make destination a symbolic link pointing to source.
    If this fails, copies destination to source instead.
    """
    # Remove the destination if it exists.
    if os.path.isfile(destination):
        os.remove(destination)

    # Try to create a symbolic link.
    # If this fails, copy the source to the destination instead.
    try:
        os.symlink(source, destination)
    except:
        shutil.copy(source, destination)


def protect(source):
    """
    Renames the source file to a reproducible but unlikely name to protect it from being
    overwritten by content of the same name in the publisher's archive.
    """
    destination = 'scoop-tmp-' + source
    os.replace(source, destination)


def restore(source):
    """
    Renames the source file to a reproducible alternative name with prefix
    'scoop-disambiguation-' and restores the original file.
    """
    original = 'scoop-tmp-' + source
    alternative = 'scoop-disambiguation-' + source
    os.replace(source, alternative)
    os.replace(original, source)


def remove_time_version_stamp():
    """
    Remove an existing time and version stamp.
    """
    filename = 'SCOOP-STAMP'
    if os.path.isfile(filename):
        os.remove(filename)


def write_time_version_stamp():
    """
    Write a time and version stamp to indicate successful completion.
    """
    filename = 'SCOOP-STAMP'
    try:
        # Get the version number from the package data.
        version = importlib.metadata.version("scoop-template-engine")
    except:
        # Get the version number from the most recent git tag,
        # defaulting to "0.0.0".
        version = str(setuptools_git_versioning.get_tag() or "0.0.0").lstrip("v")

    # Generate the date string.
    dateTime = datetime.datetime.utcnow().strftime("%Y%m%d-%H:%M:%S UTC")

    # Write the time and version stamp.
    stampString = "{version:s}\n{dateTime:s}\n".format(version = version, dateTime = dateTime)
    with open(filename, 'w') as f:
        f.write(stampString)
