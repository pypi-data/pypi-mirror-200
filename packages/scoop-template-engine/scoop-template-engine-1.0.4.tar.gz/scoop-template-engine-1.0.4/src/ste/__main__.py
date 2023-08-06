"""
The scoop template engine (ste) is meant to facilitate the preparation of LaTeX
documents to abide to the formatting standards for various scientific
journals. Please visit
https://gitlab.com/scoopgroup-public/scoop-template-engine
for a full description of the features.
"""

# Resolve the dependencies.
import argparse
import datetime
import glob
import importlib.metadata
import importlib.resources
import importlib.util
import inspect
import itertools
import operator
import os
import packaging.version
import pathlib
import platform
import re
import shutil
import stat
import sys
import yaml
from subprocess import run, STDOUT, DEVNULL
from multiprocessing import Pool, cpu_count


def removePrefix(text, prefix):
    """
    removes a prefix from a string when present.
    """
    if text.startswith(prefix):
        return text[len(prefix):]
    else:
        return text

def extractTemplateDescription(text, templateName):
    """
    extracts the template description present in the form
      <<TemplateDescription templateName: description>> or else
      <<TemplateDescription: description>>
    from the text.
    """
    # Try and find a template specific description first.
    templateDescription = re.findall('<<TemplateDescription ' + templateName + ':\s*(.*?)>>|$', text)[0]
    # If that did not turn up anything, try and find a generic template description.
    if not templateDescription:
        templateDescription = re.findall('<<TemplateDescription:\s*(.*?)>>|$', text)[0]
    return templateDescription

def extractDependencies(text, templateName):
    """
    extracts the dependencies present in the form
      <<Dependency templateName: file>> and
      <<Dependency: file>>
    from the text.
    """
    # Try and find template specific depencies first.
    dependencies = list(filter(None, re.findall('<<Dependency ' + templateName + ':\s*(.*?)>>|$', text)))
    # In addition, try and find generic depencies.
    dependencies = dependencies + list(filter(None, re.findall('<<Dependency:\s*(.*?)>>|$', text)))
    return dependencies

def extractVersionRequirement(text):
    """
    verifies whether the template's resources are compatible with the template.
    The template's minimum required version (if any) is specified in the form
    <<MinimumVersion: 1.2.3>>
    """
    # Try to find a minimum version requirement, if any.
    minimumVersion = re.search('<<MinimumVersion:\s*([0-9.]*)>>|$', text).group(1)
    return minimumVersion

def init(data, baseDirectory):
    """
    runs a script (typically init.py) and catches its stdout and stderr in a .log file.
    """
    # Construct the absolute path of the init.py file under consideration.
    folder = data[0]
    scriptname = data[1]
    scriptnameAbsolutePath = os.path.abspath(os.path.join(f'{folder}', f'{scriptname}'))
    scriptnameRelativePath = os.path.relpath(scriptnameAbsolutePath, start = baseDirectory)

    # Create the .log file with file name derived from the scriptname file name.
    logfilename = os.path.splitext(scriptnameAbsolutePath)[0] + '.log'
    print('Running {0:s}'.format(scriptnameRelativePath))
    with open(logfilename, 'w') as logfile:
        # Run the scriptname, capture its stdout and stderr and return value.
        returnValue = run([sys.executable, scriptnameAbsolutePath], cwd = folder, stdout = logfile, stderr = STDOUT)

    # Remember the script in case of failure.
    if returnValue.returncode != 0:
        return (False, folder, scriptname, logfilename)
    return (True, )

def main():
    """
    implements the user interface to the Scoop Template Engine.
    """

    # Remember who we are and how we were called.
    thisScriptName = os.path.basename(sys.argv[0])
    thisScriptAbsolutePath = os.path.abspath(sys.argv[0])
    thisScriptCallSummary = " ".join([thisScriptName] + sys.argv[1:])
    thisScriptAbsolutePathCallSummary = " ".join(sys.argv)
    baseDirectory = str(importlib.resources.files("ste"))

    # Get the version number.
    try:
        scoopTemplateEngineVersion = importlib.metadata.version("scoop-template-engine")
    except:
        scoopTemplateEngineVersion = "VERSION ERROR"

    # Specify some default values.
    dataFile = None
    outFileSuffix = True

    # Define some constants.
    templatePrefix = "template-"

    # Define a description field for the command line argument parser.
    description = """
The scoop template engine facilitates the preparation of LaTeX documents by allowing the separation of layout from content.

    {prog:s} help                show this help message and exit
    {prog:s} doc                 show the documentation
    {prog:s} version             show the version information and exit
    {prog:s} list [filter]       list available templates
    {prog:s} init [filter]       download and initialize template resources
    {prog:s} start               create files to start a new document
    {prog:s} prepare [options]   prepare a document for LaTeX compilation

    [filter] is a Python regular expression.

'Prepare a document' means that
* the required .cls files etc. will be copied to the output directory
* a customized .tex file will be generated from the selected template
* a customized .bib file will be generated containing the required references

Examples:

    {prog:s} list Springer          list available templates matching 'Springer'
    {prog:s} init SIAM              download and initialize template resources matching 'SIAM'
    {prog:s} prepare -t acdm        prepare a document for 'Advances in Continuous and Discrete Models'

Example workflow:
    {prog:s} start                         create default files 'manuscript.yaml', 'content.tex', 'abstract.tex' 
    <edit manuscript.yaml>            adjust title, authors etc.
    {prog:s} prepare                       create 'manuscript-amspreprint.tex'
    ⎢ <edit content.tex>              enter the usual edit - compile loop
    ⎣ pdflatex manuscript-amspreprint.tex
""".format(prog = thisScriptName)

    # Define the command line argument parser.
    parser = argparse.ArgumentParser(
            description = description, 
            formatter_class = lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position = 40),
            usage = '%(prog)s <command> [filter] [options]',
            add_help = False,
            )
    # Add command as the first positional argument.
    commandList = ['help', 'doc', 'version', 'list', 'init', 'start', 'prepare']
    parser.add_argument('command', 
            choices = commandList, 
            help = argparse.SUPPRESS, 
            default = 'help', 
            metavar = 'command',
            nargs = '?')
    # Add filter as an optional second positional argument.
    parser.add_argument('filter',
            #  help = 'regular expression\nvalid for commands init and list',
            help = argparse.SUPPRESS, 
            default = '',
            metavar = 'filter',
            nargs = '?')
    # Add --datafile as an optional argument.
    parser.add_argument('-d', '--datafile', 
            metavar = 'file.yaml', 
            help = 'YAML file containing document data\n(default: the unique .yaml or .yml file in the current directory)', 
            action = 'store')
    # Add --template as an optional argument.
    parser.add_argument('-t', '--template', 
            metavar = 'template', 
            help = 'name of template to be used', 
            default = None)
    # Add --outdir as an optional argument.
    parser.add_argument('-o', '--outdir', 
            metavar = 'directory', 
            help = 'generated files will be written to this directory\n(default: current directory)', 
            default = None)
    # Add --prefix as an optional argument.
    parser.add_argument('-p', '--prefix', 
            metavar = 'prefix', 
            help = '<prefix>-<template>.tex file will be generated\n(default: derived from YAML file)', 
            default = None)
    # Add --nosuffix as an optional argument.
    parser.add_argument('-ns', '--nosuffix', 
            help = 'generate <prefix>.tex rather than <prefix>-<template>.tex', 
            action = 'store_true')
    # Add --nocustombib as an optional argument.
    parser.add_argument('-nc', '--nocustombib', 
            help = 'do not generate a custom .bib file', 
            action = 'store_true')
    # Add --nobib as an optional argument.
    parser.add_argument('-nb', '--nobib', 
            help = 'do not use any .bib files', 
            action = 'store_true')
    # Add --quiet as an optional argument.
    parser.add_argument('-q', '--quiet', 
            help = 'report only errors', 
            action = 'store_true')

    # Parse the command line arguments.
    args = parser.parse_args()

    # Define a print function which honors the --quiet option.
    quietprint = print if not args.quiet else lambda *args, **kwargs: None

    # If the command is 'help', print the help and exit.
    if args.command == 'help':
        parser.print_help()
        sys.exit(0)

    # If the command is 'doc', launch the system's default viewer on the doc file and exit.
    if args.command == 'doc':
        # Specify the relevant doc file.
        docfile = importlib.resources.files("doc").joinpath("scoop-template-engine.pdf")
        # Launch the system's default viewer.
        if platform.system() == 'Darwin':
            run(['open', docfile], stderr = STDOUT, stdout = DEVNULL)
        elif platform.system() == 'Windows':
            os.startfile(docfile)
        elif platform.system() == 'Linux':
            run(['xdg-open', docfile], stderr = STDOUT, stdout = DEVNULL)
        else:
            print('Unknown platform. Don\'t know how to launch a pdf viewer.')
        sys.exit(0)

    # If the command is 'version', print the version number and exit.
    if args.command == 'version':
        print(scoopTemplateEngineVersion)
        sys.exit(0)

    # If the command is 'init', run all manuscripts/**/init.py scripts and exit.
    if args.command == 'init':
        print('Initializing the template resources in {filter:s}...'.format(filter = args.filter))
        # Collect the init.py files to be executed, and the absolute names of
        # the folders they are in.
        fileList = []

        # Find all init.py files relative to the base directory.
        # If the the filter expression is found as a substring of the
        # relative path, add the init.py file to the list of files to be processed.
        initFiles = glob.glob(baseDirectory + '/**/init.py', recursive = True)
        for initFile in initFiles:
            relativePath = str(pathlib.Path(initFile).relative_to(baseDirectory))
            if re.search(args.filter, relativePath):
                scriptname = os.path.basename(initFile)
                folder = os.path.dirname(initFile)
                fileList.append((folder, scriptname))

        # Get the number of CPUs for parallel processing.
        nCPU = cpu_count()

        # Execute all scripts in parallel (by calling the init function) and catch
        # their return values.
        with Pool(nCPU) as p:
            returnValues = p.starmap(init, zip(fileList, itertools.cycle([baseDirectory])))

            # Filter the return values for failed scripts.
            failedList = [(x[1], x[2], x[3]) for x in returnValues if not x[0]]

            # Try again on the scripts which failed.
            returnValues = p.starmap(init, zip(failedList, itertools.cycle([baseDirectory])))

            # Filter the return values for failed scripts.
            failedList = [(x[1], x[2], x[3]) for x in returnValues if not x[0]]

            # Show the scripts which failed twice.
            if len(failedList) > 0:
                print()
                print('The following scripts failed twice:')
                for item in failedList:
                    print('{0:s}/{1:s}'.format(item[0], item[1]))
                    print('See {0:s} for details.'.format(item[2]))
                print('Associated templates will not be available.')
        sys.exit(0)


    # If the command is 'list', list all templates and their descriptions and exit.
    if args.command == 'list':
        # Find all template files in any of the template directories specified (default: '.').
        templateFiles = glob.glob(baseDirectory + '/**/' + templatePrefix + '*.tex', recursive = True)

        # Create a list of templates with relevant information.
        templateList = []
        for templateFile in templateFiles:
            # Determine whether the template file is a regular file or a link.
            templateFileIsLink = os.path.islink(templateFile)

            # Open the template file.
            try:
                with open(templateFile) as templateFileStream:
                    templateFileData = templateFileStream.read()
            except IOError:
                print()
                print('ERROR: Template file {file:s} is not readable.'.format(file = templateFile))
                sys.exit(1)

            # Extract the template decription from the template.
            templateBaseName = re.findall('.*' + templatePrefix + '(.*?)\.tex', templateFile)[0]
            templateDescription = extractTemplateDescription(templateFileData, templateBaseName)

            # Verify whether the template uses BibLaTeX.
            templateUsesBibLaTeX = '<<BibLaTeXResources>>' in templateFileData

            # Get the relative path of the template file to the base directory.
            relativePath = str(pathlib.Path(templateFile).relative_to(baseDirectory))

            # If the the filter expression is found as a substring of the
            # relative path, add the template to the template list.
            # Also filter out the 'bibgenerator' template at this time.
            if re.search(args.filter, relativePath) and not re.search('template-bibgenerator.tex', relativePath):
                templateList.append([templateBaseName,
                  templateUsesBibLaTeX,
                  templateDescription,
                  relativePath,
                  templateFileIsLink])

        # Find the maximal lengths of the entries in each column of the
        # template list, and create a customized format string from it.
        if not templateList:
            sys.exit(0)
        formatString = ""
        formatString = formatString + "{template:" + str(max([len(item[0]) for item in templateList])) + "s}"
        formatString = formatString + "  {BibLaTeX:" + "1s}"
        formatString = formatString + "  {isLink:" + "1s}"
        formatString = formatString + "  {description:" + str(max([len(item[2]) for item in templateList])) + "s}"
        formatString = formatString + "  {file:" + str(max([len(item[3]) for item in templateList])) + "s}"

        # Print the list of template information, sorted by template description.
        templateList.sort(key = operator.itemgetter(2))
        for template in templateList:
            print(formatString.format(
                template = template[0], 
                BibLaTeX = '*' if template[1] else '-', 
                isLink = 'L' if template[4]  else 'F', 
                description = template[2], 
                file = template[3]))
        sys.exit(0)

    # If the command is 'start', copy the content of schemes/manuscript to the
    # current directory (but do not overwrite) and exit.
    if args.command == 'start':
        # Find the directory of the scheme and the target (current) directory.
        sourceDirectory = os.path.join(baseDirectory, 'schemes/manuscript')
        targetDirectory = os.getcwd()

        # Get a list of the files to be copied.
        fileList = glob.glob(sourceDirectory + '/*', recursive = True)

        # Verify that none of the files exists (as a file or directory) in the target directory.
        filesExisting = []
        for file in fileList:
            relativePath = pathlib.Path(file).relative_to(sourceDirectory)
            if os.path.exists(relativePath):
                filesExisting.append(relativePath)
        if filesExisting:
            print("The following files already exist in the current directory:")
            print([str(file) for file in filesExisting])
            print("Aborting. No files were created.")
            sys.exit(1)

        # Copy the files pertaining to the scheme to the target directory.
        for file in fileList:
            relativePath = pathlib.Path(file).relative_to(sourceDirectory)
            print('Copying {file:s} to ./'.format(file = str(relativePath)))
            shutil.copy(file, targetDirectory)
        sys.exit(0)


    # From here on, the command is 'prepare'.
    # Print a greeting.
    quietprint()
    quietprint('The scoop template engine (version {version:s}).'.format(version = scoopTemplateEngineVersion))
    quietprint()

    # Get and process the --datafile argument from the parser.
    dataFile = args.datafile
    if not dataFile:
        # Try to locate the unique .yaml or .yml file in the current directory.
        dataFile = glob.glob('*.yaml') + glob.glob('*.yml')
        if len(dataFile) == 0:
            print("No .yaml or .yml file found was found in the current directory.")
            print("Please specify the YAML document data file to use via --datafile.")
            print("Aborting. No output was produced.")
            sys.exit(1)
        if len(dataFile) != 1:
            print("More than one .yaml or .yml file was found in the current directory.")
            print("Please specify the YAML document data file to use via --datafile.")
            quietprint("The following .yaml or .yml files were found:")
            quietprint('\n'.join(dataFile))
            print("Aborting. No output was produced.")
            sys.exit(1)
        dataFile = dataFile[0]

    # Get and process the --template argument from the parser.
    templateBaseName = args.template

    # Get and process the --prefix argument from the parser.
    outFileBaseName = args.prefix

    # Get and process the --outdir argument from the parser.
    outDirectory = args.outdir

    # Get and process the --nocustombib argument from the parser.
    customBib = not args.nocustombib

    # Get and process the --nobib argument from the parser.
    noBib = args.nobib

    # Report the data file to the user.
    quietprint("Using data file:      {file:s}".format(file = dataFile))

    # Read the .yaml data file.
    try:
        with open(dataFile) as dataFileStream:
            dataFileData = yaml.safe_load(dataFileStream)
            if not dataFileData:
                dataFileData = {}
    except IOError:
        print()
        print("ERROR: dataFile {file:s} is not readable.".format(file = dataFile))
        print("Aborting. No output was produced.")
        sys.exit(1)

    # Process and remove the "outdir" key from the data file, unless we already have it from the command line.
    if not outDirectory:
        outDirectory = dataFileData.get("control", {}).get("outdir")
    dataFileData.pop("outdir", None)
    if not outDirectory:
        outDirectory = "./"

    # Process and remove the "prefix" key from the data file, unless we alredy have it from the command line.
    if not outFileBaseName:
        outFileBaseName = dataFileData.get("control", {}).get("prefix")
    if not outFileBaseName:
        outFileBaseName = os.path.splitext(dataFile)[0]
    dataFileData.pop("prefix", None)

    # Process and remove the "nocustombib" key from the data file, unless we alredy have it from the command line.
    if customBib:
        if dataFileData.get("control", {}).get("nocustombib"):
            customBib = False
    dataFileData.pop("nocustombib", None)

    # Process and remove the "nobib" key from the data file, unless we alredy have it from the command line.
    if not noBib:
        if dataFileData.get("control", {}).get("nobib"):
            noBib = True
    dataFileData.pop("nobib", None)

    # Process and remove the "template" key from the data file, unless we already have it from the command line.
    if not templateBaseName:
        templateBaseName = dataFileData.get("control", {}).get("template")
    dataFileData.pop("template", None)

    # Report the template name in use to the user.
    quietprint("Using template:       {template:s}".format(template = templateBaseName))

    # Make sure we have a template file.
    if not templateBaseName:
        print("You need to specify a template file via '--template' or via the 'template' key in the datafile.")
        print("Aborting. No output was produced.")
        sys.exit(1)

    # Assemble the full name of the template file.
    templateFile = templatePrefix + templateBaseName

    # Try to locate the unique .tex template file to be used.
    templateFile = glob.glob(baseDirectory + '/**/' + templateFile + '.tex', recursive = True)
    if len(templateFile) == 0:
        print("No template file matching '{templateBaseName:s}' was found.".format(templateBaseName = templateBaseName))
        print("Please specify the template via --template.")
        print("Aborting. No output was produced.")
        sys.exit(1)
    if len(templateFile) != 1:
        print("More than one .tex file is matching the pattern.")
        print("Please specify the template via --template unambiguously.")
        print("Aborting. No output was produced.")
        quietprint("The following .yaml or .yml files were found:")
        quietprint('\n'.join(templateFile))
        sys.exit(1)
    templateFile = templateFile[0]
    templateFileExtension = os.path.splitext(templateFile)[1]
    templateDirectory = os.path.dirname(templateFile)

    # Infer the top-level component (such as 'manuscripts') of the directory the template resides in.
    templateTopLevelDirectory = pathlib.Path(templateFile).relative_to(baseDirectory).parts[0]

    # Report the template file to the user.
    quietprint("Using template file:  {file:s}".format(file = os.path.relpath(templateFile, start = baseDirectory)))

    # Infer the rules file from the template file.
    rulesFile = os.path.join(baseDirectory, templateTopLevelDirectory, templateTopLevelDirectory + '.py')

    # Report the rules file to the user.
    quietprint("Using rules file:     {file:s}".format(file = os.path.relpath(rulesFile, start = baseDirectory)))

    # Process the --nosuffix argument from the parser.
    if args.nosuffix:
        outFileSuffix = False

    # Process and remove the "nosuffix" key from the data file.
    if dataFileData.get("control", {}).get("nosuffix"):
        outFileSuffix = False
    dataFileData.pop("nosuffix", None)

    # Assemble the output file name.
    if outFileSuffix:
        outFileBaseName = outFileBaseName + '-' + templateBaseName + templateFileExtension
    else:
        outFileBaseName = outFileBaseName + templateFileExtension
    outFile = os.path.join(outDirectory, outFileBaseName)

    # Read the template file.
    try:
        with open(templateFile) as templateFileStream:
            templateFileData = templateFileStream.read()
    except IOError:
        print()
        print('ERROR: Template file {file:s} is not readable.'.format(file = templateFile))
        print("Aborting. No output was produced.")
        sys.exit(1)

    # Verify that the template's resources were initialized with a compatible
    # version of the template engine.
    # Extract the template's minimum version requirement (if any).
    minimumVersion = extractVersionRequirement(templateFileData)
    if minimumVersion:
        minimumVersion = packaging.version.Version(minimumVersion)
        # Get the version used to initialize the template's resources.
        stampFile = templateDirectory + '/SCOOP-STAMP'
        try:
            with open(stampFile) as stampFileStream:
                stampFileData = stampFileStream.read()
        except:
            print()
            print('ERROR: The resources for template {template:s} have not been initialized.'.format(template = templateBaseName))
            print('Please run')
            print('  {scriptName:s} init'.format(scriptName = thisScriptName))
            sys.exit(1)
        versionInitialized = packaging.version.Version(stampFileData.split('\n')[0])
        # Verify whether the version requirement is met.
        if versionInitialized < minimumVersion:
            print()
            print('ERROR: The resources for template {template:s} are outdated.'.format(template = templateBaseName))
            print('Please run')
            print('  {scriptName:s} init'.format(scriptName = thisScriptName))
            sys.exit(1)

    # Remove all version tags from the template.
    templateFileData = re.sub(r'<<MinimumVersion.*>>.*\n', '', templateFileData)

    # Find the dependencies in the template.
    dependencies = extractDependencies(templateFileData, templateBaseName)

    # Copy all dependencies of the template to the outDirectory and make them
    # write protected.
    for dependency in dependencies:
        sourceFile = templateDirectory + "/" + dependency
        sourceFileRelativePath = os.path.relpath(sourceFile, start = baseDirectory)
        destinationFile = outDirectory + "/" + dependency
        quietprint("Copying dependency    {sourceFile:s} to {outDirectory:s}".format(sourceFile = sourceFileRelativePath, outDirectory = outDirectory))
        os.makedirs(os.path.dirname(destinationFile), exist_ok = True)
        # Make the destination writable (in case it exists).
        try:
            os.chmod(destinationFile, stat.S_IWRITE)
        except:
            pass
        shutil.copy(sourceFile, destinationFile, follow_symlinks = True)
        try:
            os.chmod(destinationFile, stat.S_IREAD)
        except:
            pass

    # Remove all dependency tags from the template.
    templateFileData = re.sub(r'<<Dependency.*>>.*\n', '', templateFileData)

    # Find the switches for the creation of a custom bibliography in the template.
    customBibliographySwitches = " ".join(re.findall('<<CreateCustomBibliography:\s*(.*?)>>', templateFileData))

    # Remove all switches for the creation of a custom bibliography from the template.
    templateFileData = re.sub(r'<<CreateCustomBibliography.*>>.*\n', '', templateFileData)

    # Find the template description in the template.
    templateDescription = extractTemplateDescription(templateFileData, templateBaseName)

    # Remove all template description tags from the template.
    templateFileData = re.sub(r'<<TemplateDescription.*>>.*\n', '', templateFileData)

    # Remove all comment tags from the template.
    templateFileData = re.sub(r'<<%.*>>.*\n', '', templateFileData)

    # Report the template description to the user.
    quietprint("Template description: {description:s}".format(description = templateDescription))

    # Import the rules file, which is supposed to provide functions to fill in the placeholders present in the template.
    spec = importlib.util.spec_from_file_location("scoop template engine rules", rulesFile)
    rules = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rules)

    # Create an instance of a parserObject.
    from collections import namedtuple
    parserInfoStructure = namedtuple('parserInfo', ['dataFileData', 'outDirectory', 'outFileBaseName', 'templateBaseName', 'templateDescription', 'scoopTemplateEngineVersion', 'thisScriptAbsolutePathCallSummary', 'customBibliographySwitches', 'customBib', 'noBib'])
    parserInfo = parserInfoStructure(
        dataFileData = dataFileData,
        outDirectory = outDirectory,
        outFileBaseName = outFileBaseName,
        templateBaseName = templateBaseName,
        templateDescription = templateDescription,
        scoopTemplateEngineVersion = scoopTemplateEngineVersion,
        thisScriptAbsolutePathCallSummary = thisScriptAbsolutePathCallSummary,
        customBibliographySwitches = customBibliographySwitches,
        customBib = customBib,
        noBib = noBib)
    parserFunctions = rules.parserObject(parserInfo)

    # Create a dictionary of substitutions to be performed on the template, recognized by the pattern '<<...>>'.
    substitutions = re.findall('<<(.*?)>>', templateFileData)
    substitutions = dict(zip(substitutions, [getattr(parserFunctions, substitution)() for substitution in substitutions]))

    # Apply the substitutions to the template.
    templateSpecialized = templateFileData
    for (replaceSource, replaceTarget) in substitutions.items():
        if replaceTarget is not None:
            templateSpecialized = templateSpecialized.replace("<<" + replaceSource + ">>", replaceTarget)

    # Prepend generation info including a time stamp.
    stampString = """% Generated by {scriptName:s} (version {version:s})
% on {dateTime:s} using
% {callSummary:s}

  """.format(scriptName = thisScriptName,
      version = scoopTemplateEngineVersion,
      dateTime = datetime.datetime.utcnow().strftime("%Y%m%d-%H:%M:%S UTC"),
      callSummary = thisScriptCallSummary)
    templateSpecialized = stampString + templateSpecialized

    # Report the output file to the user.
    quietprint("Writing output file:  {file:s}".format(file = outFile))

    # Make the output file writable (in case it exists).
    try:
        os.chmod(outFile, stat.S_IWRITE)
    except:
        pass

    # Write the output file.
    try:
        with open(outFile, "w") as outFileStream:
            outFileData = outFileStream.write(templateSpecialized)
    except IOError:
        print()
        print('ERROR: outFile file {file:s} is not writable.'.format(file = outFile))
        sys.exit(1)

    # Make the output file write protected.
    try:
        os.chmod(outFile, stat.S_IREAD)
    except:
        pass


if __name__ == "__main__":
    sys.exit(main())
