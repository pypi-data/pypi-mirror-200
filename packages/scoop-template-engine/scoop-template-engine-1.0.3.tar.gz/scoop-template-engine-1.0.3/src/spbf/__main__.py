"""
The Scoop Prepare Bibtex File (spbf) tool prepares a legacy BibTeX file from a
BibTeX or BibLaTeX source. In particular, it
* converts UTF8 characters into their BibTeX transcriptions and
* converts entry types such as @THESIS into BibTeX compatible types,
 depending on command line parameters.
This tool can operate
* in a document oriented mode, where the bibliography is drawn from a
 document's .bcf file (using the data source(s) declared there), or
* in a database oriented mode, where an entire .bib file is
 processed.
"""

# Resolve the dependencies.
import argparse
import bibtexparser
import datetime
import importlib.metadata
import importlib.resources
import os
import platform
import re
import subprocess
import sys
import tempfile


def main():
    """
    implements the user interface to the Scoop Prepare Bibtex File tool.
    """

    # Remember who we are and how we were called.
    thisScriptName = os.path.basename(sys.argv[0])
    thisScriptAbsolutePath = os.path.abspath(sys.argv[0])
    thisScriptCallSummary = " ".join([thisScriptName] + sys.argv[1:])

    # Get the version number.
    try:
        scoopTemplateEngineVersion = importlib.metadata.version("scoop-template-engine")
    except:
        scoopTemplateEngineVersion = "VERSION ERROR"

    # Define a description field for the command line argument parser.
    description = """
The scoop prepare bibtex file tool prepares a legacy BibTeX file from a BibTeX or BibLaTeX source.

    {prog:s} help                                show this help message and exit
    {prog:s} doc                                 show the documentation
    {prog:s} version                             show the version information and exit
    {prog:s} convert [options] infile [outfile]  convert 'infile' to a legacy bibtex file 'outfile'

The 'infile' can be
* a BibTeX or BibLaTeX (.bib) file - database mode
* a BibLaTeX control (.bcf) file   - document mode
In document mode, your 'biber' command must be version 2.10 or newer.

Examples:

    {prog:s} convert my.bib             convert 'my.bib' into a legacy bibtex file and write it to stdout
    {prog:s} convert my.bib legacy.bib  same but write to 'legacy.bib'
    {prog:s} convert my.bcf legacy.bib  convert the references used in my.bcf into a legacy bibtex file 
                                    and write it to 'legacy.bib'
""".format(prog = thisScriptName)

    # Define the command line argument parser.
    parser = argparse.ArgumentParser(
            description = description, 
            formatter_class = lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position = 41),
            usage = '%(prog)s <command> [options] infile [outfile]',
            add_help = False,
            )

    # Add command as the first positional argument.
    commandList = ['help', 'doc', 'version', 'convert']
    parser.add_argument('command', 
            choices = commandList, 
            help = argparse.SUPPRESS, 
            default = 'help', 
            metavar = 'command',
            nargs = '?')

    # Add infile as the second, optional positional argument.
    parser.add_argument('infile', 
            help = argparse.SUPPRESS, 
            default = None, 
            metavar = 'infile',
            nargs = '?')

    # Add outfile as the third, optional positional argument.
    parser.add_argument('outfile', 
            help = argparse.SUPPRESS, 
            default = None, 
            metavar = 'outfile',
            nargs = '?')

    # Add --giveninits as an optional argument.
    parser.add_argument('-gi', '--giveninits', 
            help = 'abbreviate authors\' and editors\' given names', 
            action = 'store_true')

    # Add --onlinetotechreport as an optional argument.
    parser.add_argument('-o2t', '--onlinetotechreport', 
            help = 'transcribe @ONLINE entries into @TECHREPORT', 
            action = 'store_true')

    # Add --proceedingstocollection as an optional argument.
    parser.add_argument('-p2c', '--proceedingstocollection', 
            help = 'transcribe @PROCEEDINGS entries into @COLLECTION', 
            action = 'store_true')

    # Add --doitonote as an optional argument.
    parser.add_argument('-d2n', '--doitonote',
            help = 'transcribe DOI into NOTE fields, with a link to https://doi.org/doi',
            action = 'store_true')

    # Add --doitourl as an optional argument.
    parser.add_argument('-d2u', '--doitourl',
            help = 'transcribe DOI into URL fields, pointing to https://doi.org/doi',
            action = 'store_true')

    # Add --urltonote as an optional argument.
    parser.add_argument('-u2n', '--urltonote',
            help = 'transcribe URL into NOTE fields, with a link to the url',
            action = 'store_true')

    # Add --arxivtotypeornote as an optional argument.
    parser.add_argument('-arxiv2tn', '--arxivtotypeornote',
            help = 'transcribe EPRINTTYPE = {arxiv} into a TYPE (for @TECHREPORTs) or NOTE field',
            action = 'store_true')

    # Add --haltotypeornote as an optional argument.
    parser.add_argument('-hal2tn', '--haltotypeornote',
            help = 'transcribe EPRINTTYPE = {HAL} into a TYPE (for @TECHREPORTs) or NOTE field',
            action = 'store_true')

    # Add --urntonote as an optional argument.
    parser.add_argument('-urn2n', '--urntonote',
            help = 'transcribe EPRINTTYPE = {urn} into a NOTE field',
            action = 'store_true')

    # Add --proceedingstitletobooktitle as an optional argument.
    parser.add_argument('-pt2bt', '--proceedingstitletobooktitle',
            help = 'transcribe TITLE into a BOOKTITLE field for @PROCEEDINGS',
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
        docfile = importlib.resources.files("doc").joinpath("scoop-prepare-bibtex-file.pdf")
        # Launch the system's default viewer.
        if platform.system() == 'Darwin':
            subprocess.run(['open', docfile], stderr = subprocess.STDOUT, stdout = subprocess.DEVNULL)
        elif platform.system() == 'Windows':
            os.startfile(docfile)
        elif platform.system() == 'Linux':
            subprocess.run(['xdg-open', docfile], stderr = subprocess.STDOUT, stdout = subprocess.DEVNULL)
        else:
            print('Unknown platform. Don\'t know how to launch a pdf viewer.')
        sys.exit(0)

    # If the command is 'version', print the version number and exit.
    if args.command == 'version':
        print(scoopTemplateEngineVersion)
        sys.exit(0)

    # From here on, the command is 'convert'.
    # Make sure the input file exists and is readable.
    if args.infile is None:
        print()
        print('\'{prog:s} convert\' requires an input file to be specified.'.format(prog = thisScriptName))
        print('See \'{prog:s} help\' for details.'.format(prog = thisScriptName))
        sys.exit(1)
    try:
        with open(args.infile) as infileStream:
            infileData = infileStream.read()
    except IOError:
        print()
        print('ERROR: Input file {file:s} is not readable.'.format(file = args.infile))
        sys.exit(1)

    # Determine whether we are in document or database oriented mode.
    infileExtension = os.path.splitext(args.infile)[1]
    if infileExtension == '.bcf':
        mode = 'document'
    elif infileExtension == '.bib':
        mode = 'database'
    else:
        print()
        print('ERROR: Input file {file:s} must have .bcf or .bib extension.'.format(file = args.infile))
        sys.exit(1)

    # Prepare a temporary output .bib file in the /tmp directory.
    temporaryOutfile = tempfile.NamedTemporaryFile(suffix = '.bib')

    # Invoke biber to prepare an initial output .bib file, with UTF8 characters
    # replaced by their LaTeX equivalents. Notice that biber also pretty-prints
    # the output, making sure all fields are on one line and white spaces are
    # trimmed.
    # Assemble the biber command line string.
    commandString = 'biber --quiet'
    if mode == 'database':
        commandString += ' --tool'
    commandString += (' --output-safechars --output-format=bibtex --output-file={outfilename:s} {infilename:s}').format(outfilename = temporaryOutfile.name, infilename = args.infile)

    # Invoke biber and make sure its run was successful.
    returnValue = subprocess.run(commandString, shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    try:
        returnValue.check_returncode()
    except subprocess.CalledProcessError:
        print('WARNING: {commandString:s} failed.\n'.format(commandString = commandString))

    # Customize the BibTeX parser.
    parser = bibtexparser.bparser.BibTexParser()
    parser.ignore_nonstandard_types = False

    # Read the .bib file into a dictionary.
    if os.path.getsize(temporaryOutfile.name) == 0:
        print('NOTICE: The input file is empty, either because your document contains no citations, or due to an error.', file = sys.stderr)
        sys.exit(0)
    with open(temporaryOutfile.name) as bibfile:
        bibData = bibtexparser.load(bibfile, parser)

    # Iterate over the bibData entries and modify them as required.
    for entry in bibData.entries:
        # entry.ID represents the cite key as a string.
        # entry.ENTRYTYPE represents the record's type (such as 'ARTICLE').

        # Convert all DATE to YEAR fields, preserving the first four digits of the
        # actual date.
        if entry.get('date') is not None:
            entry['year'] = entry.pop('date')[:4]

        # Replace all LOCATION (BibLaTeX) by ADDRESS (BibTeX) fields.
        if entry.get('location') is not None:
            entry['address'] = entry.pop('location')

        # Replace all JOURNALTITLE (BibLaTeX) by JOURNAL (BibTeX) fields.
        if entry.get('journaltitle') is not None:
            entry['journal'] = entry.pop('journaltitle')

        # Replace all ORGANIZATION (BibLaTeX) by PUBLISHER (BibTeX) fields.
        if entry.get('organization') is not None:
            entry['publisher'] = entry.pop('organization')

        # Append the content of SUBTITLE (BibLaTeX) field to the TITLE (BibTeX) field.
        # Leave SUBTITLE in since it does no harm.
        if entry.get('subtitle') is not None:
            entry['title'] = '. '.join(filter(None, [entry.get('title'), entry.get('subtitle')]))

        # Replace all @REPORT (BibLaTeX) by @TECHREPORT (BibTeX) entries.
        if entry.get('ENTRYTYPE') == 'report':
            entry['ENTRYTYPE'] = 'techreport'

        # Replace all @COLLECTION (BibLaTeX) by @BOOK (BibTeX) entries.
        if entry.get('ENTRYTYPE') == 'collection':
            entry['ENTRYTYPE'] = 'book'

        # Convert @THESIS with TYPE = "Bachelor thesis" (and similar) to @MASTERSTHESIS, and modify the
        # TYPE to say 'Bachelor thesis' explicitly. Replace INSTITUTION by SCHOOL.
        if entry.get('ENTRYTYPE') == 'thesis' and re.search('(Bachelor|B.Sc.|BSc)\s*Thesis', entry.get('type'), flags = re.IGNORECASE) is not None:
            entry['ENTRYTYPE'] = 'mastersthesis'
            entry['type'] = '{B}achelor thesis'
            if entry.get('institution') is not None:
                entry['school'] = entry.pop('institution')

        # Convert @THESIS with TYPE = "mathesis" (and similar) to @MASTERSTHESIS, and modify the
        # TYPE to say 'Master thesis' explicitly. Replace INSTITUTION by SCHOOL.
        if entry.get('ENTRYTYPE') == 'thesis' and re.search('(Master|M.Sc.|MSc|M.A.|MA)\s*Thesis', entry.get('type'), flags = re.IGNORECASE) is not None:
            entry['ENTRYTYPE'] = 'mastersthesis'
            entry['type'] = '{M}aster thesis'
            if entry.get('institution') is not None:
                entry['school'] = entry.pop('institution')

        # Convert @THESIS with TYPE = "phdthesis" (and similar) to @PHDTHESIS, and modify the
        # TYPE to say 'Ph.D. thesis' explicitly. Replace INSTITUTION by SCHOOL.
        if entry.get('ENTRYTYPE') == 'thesis' and re.search('(Doctoral|Ph.D.|PHD)\s*Thesis', entry.get('type'), flags = re.IGNORECASE) is not None:
            entry['ENTRYTYPE'] = 'phdthesis'
            entry['type'] = '{Ph.D.} thesis'
            if entry.get('institution') is not None:
                entry['school'] = entry.pop('institution')

        # Convert @THESIS with TYPE = "Habilitation thesis" (and similar) to @PHDTHESIS, and modify the
        # TYPE to say 'Ph.D. thesis' explicitly. Replace INSTITUTION by SCHOOL.
        if entry.get('ENTRYTYPE') == 'thesis' and re.search('(Habilitation)\s*Thesis', entry.get('type'), flags = re.IGNORECASE) is not None:
            entry['ENTRYTYPE'] = 'phdthesis'
            entry['type'] = '{H}abilitation thesis'
            if entry.get('institution') is not None:
                entry['school'] = entry.pop('institution')


        # Additional conversions triggered by command line switches follow.

        # If required, transcribe @ONLINE into @TECHREPORT entries.
        if args.onlinetotechreport:
            if entry.get('ENTRYTYPE') == 'online':
                entry['ENTRYTYPE'] = 'techreport'

        # If required, transcribe @PROCEEDINGS into @COLLECTION entries.
        if args.proceedingstocollection:
            if entry.get('ENTRYTYPE') == 'proceedings':
                entry['ENTRYTYPE'] = 'collection'

        # If required, transcribe EPRINTTTYPE = {arXiv} fields.
        # In @TECHREPORT, generate a TYPE field from EPRINT field.
        # In all other entry types (for example, @ARTICLE), generate a NOTE field from EPRINT field.
        # Leave EPRINTTYPE in since it does no harm but remove EPRINT since some .bst files
        # interpret every EPRINT as an arxiv preprint.
        if args.arxivtotypeornote:
            if entry.get('eprinttype') == 'arXiv':
                arxivIdentifier = entry.pop('eprint')
                if arxivIdentifier is not None:
                    arxivString = '{{arXiv}}: \href{{https://arxiv.org/abs/{arxivIdentifier:s}}}{{\detokenize{{{arxivIdentifier:s}}}}}'.format(arxivIdentifier = arxivIdentifier)
                    if entry.get('ENTRYTYPE') == 'techreport':
                        entry['type'] = '. '.join(filter(None, [entry.get('type'), arxivString]))
                    else:
                        entry['note'] = '. '.join(filter(None, [entry.get('note'), arxivString]))

        # If required, transcribe EPRINTTTYPE = {HAL} fields.
        # In @TECHREPORT, generate a TYPE field from the EPRINT field.
        # In all other entry types (for example, @ARTICLE), generate a NOTE field from EPRINT field.
        # Leave EPRINTTYPE in since it does no harm but remove EPRINT since some .bst files
        # interpret every EPRINT as an arxiv preprint.
        if args.haltotypeornote:
            if entry.get('eprinttype') == 'HAL':
                halIdentifier = entry.pop('eprint')
                if halIdentifier is not None:
                    halString = '{{HAL}}: \href{{https://hal.archives-ouvertes.fr/{halIdentifier:s}}}{{\detokenize{{{halIdentifier:s}}}}}'.format(halIdentifier = halIdentifier)
                    if entry.get('ENTRYTYPE') == 'techreport':
                        entry['type'] = '. '.join(filter(None, [entry.get('type'), halString]))
                    else:
                        entry['note'] = '. '.join(filter(None, [entry.get('note'), halString]))

        # If required, transcribe EPRINTTTYPE = {urn} fields.
        # In @TECHREPORT, generate a TYPE field from the EPRINT field.
        # In all entry types (for example, @ARTICLE), generate a NOTE field from EPRINT field.
        # Leave EPRINTTYPE in since it does no harm but remove EPRINT since some .bst files
        # interpret every EPRINT as an arxiv preprint.
        if args.urntonote:
            if entry.get('eprinttype') == 'urn':
                urnIdentifier = entry.pop('eprint')
                if urnIdentifier is not None:
                    urnString = '{{URN}}: \href{{https://www.nbn-resolving.de/{urnIdentifier:s}}}{{\detokenize{{{urnIdentifier:s}}}}}'.format(urnIdentifier = urnIdentifier)
                    entry['note'] = '. '.join(filter(None, [entry.get('note'), urnString]))

        # If required, transcribe DOI into URL fields.
        # Leave DOI in since it does no harm.
        if args.doitourl:
            doi = entry.get('doi')
            if doi is not None:
                urlString = 'https://doi.org/{doi:s}'.format(doi = doi)
                entry['url'] = '. '.join(filter(None, [entry.get('url'), urlString]))

        # If required, transcribe DOI into NOTE fields.
        # Leave DOI in since it does no harm.
        if args.doitonote:
            doi = entry.get('doi')
            if doi is not None:
                noteString = '{{DOI}} \href{{https://doi.org/{doi:s}}}{{\detokenize{{{doi:s}}}}}'.format(doi = doi)
                entry['note'] = '. '.join(filter(None, [entry.get('note'), noteString]))

        # If required, transcribe URL into NOTE fields.
        # Leave DOI in since it does no harm.
        if args.urltonote:
            url = entry.get('url')
            if url is not None:
                noteString = '\\url{{{url:s}}}'.format(url = url)
                entry['note'] = '. '.join(filter(None, [entry.get('note'), noteString]))

        # If required, transcribe TITLE into BOOKTITLE fields for @PROCEEDINGS.
        if args.proceedingstitletobooktitle:
            if entry.get('ENTRYTYPE') == 'proceedings':
                title = entry.pop('title')
                if title is not None:
                    entry['booktitle'] = title

        # If required, abbreviate authors' and editors' given names.
        if args.giveninits:
            def abbreviateFullName(fullName):
                # Split names (which always come in comma-separated form) such as
                #   'Smith, John'
                #   'Smith, Jr, John'
                # into their components, using the comma as a separator. Then process
                # the last component (the given names) through the abbreviate function, and
                # paste the results back together.
                nameParts = fullName.split(',')
                return ', '.join(nameParts[:-1] + [abbreviateGivenNames(nameParts[-1].strip())])
            def abbreviateGivenNames(givenNames):
                # Replace (repeated) whitespaces in givenNames by a single ' '.
                # Then split the givenNames at ' ' and '-', apply abbreviateSingleGivenName to
                # each part, and paste the results back together, using the captured separators.
                givenNames = ' '.join(givenNames.split())
                givenNames = re.split('([ -])', givenNames)
                for iter in range(0,len(givenNames),2):
                    givenNames[iter] = abbreviateSingleGivenName(givenNames[iter])
                return ''.join(givenNames)

            def abbreviateSingleGivenName(givenName):
                # Abbreviate a single given name, taking into account (partly fictitious) cases such as
                #   'Donald'
                #   'Jean-Paul'
                #   '\.{I}lker'
                #   '\v{R}\'{\i{}}'
                #   '\AE{}'
                # We use the following logic. If the single given name starts with '\', then copy it
                # until we have found at least one '{' and then until the matching '}'. If the single
                # name does not start with '\', the copy only the first character.
                if givenName[0] == '\\':
                    numberOfOpeningBrackets = 0;
                    numberOfClosingBrackets = 0;
                    for iter in range(len(givenName)):
                        if givenName[iter] == '{':
                            numberOfOpeningBrackets += 1
                        if givenName[iter] == '}':
                            numberOfClosingBrackets += 1
                        if (numberOfOpeningBrackets > 0) and (numberOfOpeningBrackets == numberOfClosingBrackets):
                            break
                    return givenName[:iter+1] + '.'
                else:
                    return givenName[0] + '.'

            # Perform the abbreviations of author and editor names.
            if entry.get('author') is not None:
                entry['author'] = ' and '.join([abbreviateFullName(authorName) for authorName in entry.get('author').split(' and ')])
            if entry.get('editor') is not None:
                entry['editor'] = ' and '.join([abbreviateFullName(editorName) for editorName in entry.get('editor').split(' and ')])

        # Protect upper-case characters.
        # In all TITLE, SUBTITLE, BOOKTITLE fields, protect all consecutive chains of
        # uppercase letters by braces.
        def protect(string):
            return re.sub(r"([A-Z]+)", r"{\1}", string)
        if entry.get('title') is not None:
            entry['title'] = protect(entry.get('title'))
        if entry.get('subtitle') is not None:
            entry['subtitle'] = protect(entry.get('subtitle'))
        if entry.get('booktitle') is not None:
            entry['booktitle'] = protect(entry.get('booktitle'))

    # Prepare a custom writer.
    writer = bibtexparser.bwriter.BibTexWriter()
    writer.indent = '  '
    writer.add_trailing_comma = True

    # Write the pybtex dictionary into a string initially.
    bibDataString = writer.write(bibData)

    # Create a time and invokation stamp.
    stampString = """@COMMENT{{
Generated by {scriptName:s} (version {version:s})
on {dateTime:s} using
{callSummary:s}
}}

""".format(
      scriptName = thisScriptName,
      version = scoopTemplateEngineVersion,
      dateTime = datetime.datetime.utcnow().strftime("%Y%m%d-%H:%M:%S UTC"),
      callSummary = thisScriptCallSummary)

    # Finally, write the result to the desired outfile.
    if args.outfile is not None:
        with open(args.outfile, 'w') as outfile:
            outfile.write(stampString + bibDataString)
    else:
        print(stampString + bibDataString)


if __name__ == "__main__":
    sys.exit(main())
