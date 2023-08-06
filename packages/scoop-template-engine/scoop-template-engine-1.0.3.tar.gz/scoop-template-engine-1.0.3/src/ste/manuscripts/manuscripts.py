# This class introduces a parser object intended for templates of type manuscript.

# Resolve the dependencies.
import collections
import glob
import itertools
import numpy as np
import os
import re
import subprocess
import stat
import sys
import tempfile
from scipy import optimize

class parserObject(object):

    def __init__(self, parserInfo):
        # Initialize the data structure.
        self.authors = parserInfo.dataFileData.get("authors", []) or []
        self.institutions = parserInfo.dataFileData.get("institutions", {}) or {}
        self.latex = parserInfo.dataFileData.get("latex", {}) or {}
        self.manuscript = parserInfo.dataFileData.get("manuscript", {}) or {}
        self.outDirectory = parserInfo.outDirectory
        self.outFileBaseName = parserInfo.outFileBaseName
        self.templateBaseName = parserInfo.templateBaseName
        self.templateDescription = parserInfo.templateDescription
        self.scoopTemplateEngineVersion = parserInfo.scoopTemplateEngineVersion
        self.thisScriptAbsolutePathCallSummary = parserInfo.thisScriptAbsolutePathCallSummary
        self.customBibliographySwitches = parserInfo.customBibliographySwitches
        self.customBib = parserInfo.customBib
        self.noBib = parserInfo.noBib
        self.footnoteSeparator = "\,\\textsuperscript{\\,\\,\\,,}"
        self.fallbackColors = ["red!80!black", "blue!80!black", "orange!80!black", "green!70!black", "teal"]
        self.fallbackColorIndex = 0

        # Perform some checks on the data.
        # Do we have unique data for all authors whose tags appear in manuscript["authors"]?
        if not self.VerifyAllAuthorsPresentAndUnique():
            raise Exception('No output was produced.')

        # Do we have data for all institutions any of the authors are affiliated with?
        if not self.VerifyAllInstitutionsPresent():
            raise Exception('No output was produced.')

    # Notice that in Python3, list comprehensions possess their own scope and therefore constructions such as
    #   [self.AuthorFullName(author) for author in self.ManuscriptAuthors()]
    # throw
    #   NameError: name 'self' is not defined.
    # See also https://stackoverflow.com/questions/13905741/.
    # A possible solution is to use
    #   [self.AuthorFullName(author) for (author, self) in zip(self.ManuscriptAuthors(), itertools.repeat(self))]
    # but we prefer here the shorter generator expression
    #   (lambda self: [self.AuthorFullName(author) for author in self.ManuscriptAuthors()])(self)
    # . Similar constructions appear throughout this module.

    # VerifyAllAuthorsPresent()
    # returns True or False, depending on whether or not all author tags are present exactly once.
    def VerifyAllAuthorsPresentAndUnique(self):
        authorTagsRequired = self.manuscript.get("authors", []) or []
        authorTagsPresent = [author.get("tag") for author in self.ManuscriptAuthors()]
        for authorTag in authorTagsRequired:
            if authorTagsPresent.count(authorTag) == 0:
                print(file = sys.stderr)
                print('ERROR: Author data with tag {author:s} not found.'.format(author = authorTag), file = sys.stderr)
                return False
            if authorTagsPresent.count(authorTag) > 1:
                print(file = sys.stderr)
                print('ERROR: Multiple authors with tag {author:s} were found.'.format(author = authorTag), file = sys.stderr)
                return False
        return True

    # VerifyAllInstitutionsPresent()
    # returns True or False, depending on whether or not we have data for all institutions any of the authors are affiliated with.
    def VerifyAllInstitutionsPresent(self):
        institutionTagsRequired = self.UniqueInstitutionTags()
        institutionTagsPresent = list(self.institutions.keys())
        for institutionTag in institutionTagsRequired:
            if institutionTagsPresent.count(institutionTag) == 0:
                print(file = sys.stderr)
                print('ERROR: institution data with tag {institution:s} not found.'.format(institution = institutionTag), file = sys.stderr)
                return False
        return True

    # TemplateBaseName()
    # returns the template base name as is.
    def TemplateBaseName(self):
        return self.templateBaseName

    # ShortJournalName()
    # returns the template acronym as given by the templateBaseName.
    def ShortJournalName(self):
        return self.TemplateBaseName()

    # ShortJournalNameCAPS()
    # returns the template acronym as given by the templateBaseName, capitalized.
    def ShortJournalNameCAPS(self):
        return self.ShortJournalName().upper()

    # JournalName()
    # returns the template description as defined inside the template file.
    def JournalName(self):
        return self.templateDescription

    # ScoopTemplateEngineSignature()
    # returns a signature containing the scoopTemplateEngineVersion.
    def ScoopTemplateEngineSignature(self):
        return "Created using the Scoop Template Engine version " + self.scoopTemplateEngineVersion + "."

    # LaTeXCompatibility()
    # returns latex["compatibility"] as a list of strings
    # with "None"s eliminated.
    # Instead of an empty list, return ["minimal"].
    def LaTeXCompatibility(self):
        content = self.EnsureList(self.latex.get("compatibility", "") or [])
        return [item for item in content if item] or ["minimal"]

    # LaTeXChangesAuthorColor(author)
    # returns the author's color for the use of the LaTeX 'changes.sty' package.
    # If that is undefined, the current fallbackColor is being used.
    # In this case, the fallbackColorIndex is advanced by one.
    def LaTeXChangesAuthorColor(self, author):
        color = self.AuthorColor(author)
        if not color:
            color = self.fallbackColors[self.fallbackColorIndex]
            self.fallbackColorIndex = (self.fallbackColorIndex + 1) % len(self.fallbackColors)
        colorString = self.CommandWrapper(color, "color = ")
        return colorString

    # LaTeXChangesAuthor(author)
    # returns code such as
    #   \definechangesauthor[name = {givenname familyname}, color = {red}]{tag}
    # which is used for configuration of the 'changes.sty' package.
    def LaTeXChangesAuthor(self, author):
        authorNameString = self.CommandWrapper(self.AuthorFullName(author), "name = ")
        authorColorString = self.LaTeXChangesAuthorColor(author)
        authorTagString = self.CommandWrapper(author.get("tag"), "")
        return "\\definechangesauthor[" + ", ".join([authorNameString, authorColorString]) + "]" + authorTagString

    # LaTeXChanges()
    # returns code such as
    #   % Configure the changes.sty package.
    #   \makeatletter
    #   \@ifpackageloaded{changes}{
    #     \definechangesauthor[name = {givenname familyname}, color = {red}]{tag}
    #     \definechangesauthor[name = {givenname familyname}, color = {red}]{tag}
    #   }{}
    #   \makeatother
    # to facilitate the use of the LaTeX 'changes.sty' package, provided that the
    # 'changes' compatibility option has been specified.
    def LaTeXChanges(self):
        changesString = ""
        if 'changes' in self.latex.get("compatibility", ""):
            changesString = """\
% Configure the changes.sty package.
\makeatletter
\@ifpackageloaded{{changes}}{{
{LaTeXChangesDefinitions:s}
}}{{}}
\makeatother\
        """.format(LaTeXChangesDefinitions = "\n".join((lambda self: [self.LaTeXChangesAuthor(author) for author in self.ManuscriptAuthors()])(self)))
        return changesString

    # CustomPrePreambleFileNameWithoutExtension()
    # returns a string such as
    #   prepreamble-template
    # derived from the templateBaseName name.
    def CustomPrePreambleFileNameWithoutExtension(self):
        return "prepreamble-" + self.templateBaseName

    # CustomPreambleFileNameWithoutExtension()
    # returns a string such as
    #   prepreamble-template
    # derived from the templateBaseName name.
    def CustomPreambleFileNameWithoutExtension(self):
        return "preamble-" + self.templateBaseName

    # CustomPostPreambleFileNameWithoutExtension()
    # returns a string such as
    #   postpreamble-template
    # derived from the templateBaseName name.
    def CustomPostPreambleFileNameWithoutExtension(self):
        return "postpreamble-" + self.templateBaseName

    # LaTeXPrePreamble()
    # returns a string such as
    #   % Insert the template-specific compatibility prepreamble.
    #   \IfFileExists{./prepreamble-template.sty}{\RequirePackage[latex["compatiblity"]]{./prepreamble-template}}{}
    # followed by
    #   % Insert the user-defined prepreamble.
    #   \latex["prepreamble"] as is with "" as default.
    # It is intended to be included before \documentclass.
    def LaTeXPrePreamble(self):
        prePreambleString = """\
% Insert the template-specific compatibility prepreamble.
\\IfFileExists{{./{customPrePreambleFileNameWithoutExtension:s}.sty}}{{\\RequirePackage[{LaTeXCompatibilityLevels:s}]{{./{customPrePreambleFileNameWithoutExtension:s}}}}}{{}}

% Insert the user-defined prepreamble.
{prePreamble:s}\
    """.format(customPrePreambleFileNameWithoutExtension = self.CustomPrePreambleFileNameWithoutExtension(),
            LaTeXCompatibilityLevels = ",".join(self.LaTeXCompatibility()),
            prePreamble = self.latex.get("prepreamble", "") or ""
            )
        return prePreambleString

    # LaTeXPreamble()
    # returns a string such as
    #   % Insert the template-specific compatibility preamble.
    #   \IfFileExists{./preamble-template.sty}{\RequirePackage[latex["compatiblity"]]{./preamble-template}}{}
    # followed by
    #   % Insert the user-defined preamble.
    #   \latex["preamble"] as is with "" as default
    # followed by
    #   % Insert the template-specific compatibility postpreamble.
    #   \IfFileExists{./postpreamble-template.sty}{\RequirePackage[latex["compatiblity"]]{./postpreamble-template}}{}
    # followed by code related to the 'changes' compatibility option (if active).
    # It is intended to be included after \documentclass.
    def LaTeXPreamble(self):
        preambleString = """\
% Insert the template-specific compatibility preamble.
\\IfFileExists{{./{customPreambleFileNameWithoutExtension:s}.sty}}{{\\RequirePackage[{LaTeXCompatibilityLevels:s}]{{./{customPreambleFileNameWithoutExtension:s}}}}}{{}}

% Insert the user-defined preamble.
{preamble:s}

% Insert the template-specific compatibility postpreamble.
\\IfFileExists{{./{customPostPreambleFileNameWithoutExtension:s}.sty}}{{\\RequirePackage[{LaTeXCompatibilityLevels:s}]{{./{customPostPreambleFileNameWithoutExtension:s}}}}}{{}}

{LaTeXChanges:s}\
""".format(customPreambleFileNameWithoutExtension = self.CustomPreambleFileNameWithoutExtension(),
            customPostPreambleFileNameWithoutExtension = self.CustomPostPreambleFileNameWithoutExtension(),
            LaTeXCompatibilityLevels = ",".join(self.LaTeXCompatibility()),
            preamble = self.latex.get("preamble", "") or "",
            LaTeXChanges = self.LaTeXChanges()
            )
        return preambleString

    # LaTeXBibFiles()
    # returns latex["bibfiles"] as a list of strings
    # with "None"s eliminated.
    def LaTeXBibFiles(self):
        content = self.EnsureList(self.latex.get("bibfiles", "") or [])
        return [item for item in content if item]

    # LaTeXBibFileNamesWithoutExtension()
    # returns latex["bibfiles"] (with file extensions removed) as a list of strings
    # with "None"s eliminated.
    def LaTeXBibFileNamesWithoutExtension(self):
        content = self.EnsureList(self.latex.get("bibfiles", "") or [])
        return [re.sub('\.bib$', '', item) for item in content if item]

    # LaTeXBody()
    # returns latex["body"] as a list of strings
    # with "None"s eliminated.
    def LaTeXBody(self):
        content = self.EnsureList(self.latex.get("body", "") or [])
        return [item for item in content if item]

    # LaTeXAbstract()
    # returns latex["abstract"] as a list of strings
    # with "None"s eliminated.
    def LaTeXAbstract(self):
        content = self.EnsureList(self.latex.get("abstract", "") or [])
        return [item for item in content if item]

    # LaTeXAppendix()
    # returns latex["appendix"] as a list of strings
    # with "None"s eliminated.
    def LaTeXAppendix(self):
        content = self.EnsureList(self.latex.get("appendix", "") or [])
        return [item for item in content if item]

    # ManuscriptMSC()
    # returns manuscript["msc"] as a list of strings
    # with "None"s eliminated.
    def ManuscriptMSC(self):
        content = self.EnsureList(self.manuscript.get("msc", "") or [])
        return [item.rstrip() for item in content if item]

    # ManuscriptKeywords()
    # returns manuscript["keywords"] as a list of strings
    # with "None"s eliminated.
    def ManuscriptKeywords(self):
        content = self.EnsureList(self.manuscript.get("keywords", "") or [])
        return [item for item in content if item]

    # def ToString(content):
    # where content is a string/number or a list of these data types
    # returns a string or a list of strings
    # with "None"s eliminated.
    def ToString(self, content):
        if isinstance(content, list):
            return [str(item) for item in content if item]
        else:
            if content:
                return str(content)
            else:
                return ""

    # DocumentClassOptions()
    # returns a comma separated string.
    # It is intended to be used as document class options in \documentclass.
    def DocumentClassOptions(self):
        content = self.EnsureList(self.latex.get("documentclassoptions", "") or [])
        return ",".join([item for item in content if item])

    # CreateCustomBibTeXFile()
    # creates a customized BibTeX file such as manuscript-template.bib by
    # * running scoop-template-engine.py again on the specialized
    #   template-bibgenerator.tex with a random --prefix
    # * to create the temporary file random-bibgenerator.bcf, from which
    # * spbf then derives manuscript-template.bib.
    def CreateCustomBibTeXFile(self):
        # Create a temporary file (actually just to obtain its file name).
        fp = tempfile.NamedTemporaryFile(dir = self.outDirectory)
        outname = os.path.basename(fp.name)

        # Invoke scoop-template-engine.py recursively with the same command line arguments plus 
        #   --prefix random 
        #   --template bibgenerator 
        #   --quiet
        # .
        args = sys.argv.copy()
        args.extend(['--prefix', outname])
        args.extend(['--template', 'bibgenerator'])
        args.append('--quiet')
        returnValue = subprocess.run(args)

        # Run pdflatex once on the generated file, suppressing the output.
        texFileNameStub = os.path.join(self.outDirectory, outname + '-bibgenerator')
        texFileName = texFileNameStub + ".tex"
        commandString = "pdflatex -interaction nonstopmode -output-directory " + self.outDirectory + " " + texFileName
        returnValue = subprocess.run(commandString, shell = True, stdout = subprocess.DEVNULL)
        try:
            returnValue.check_returncode()
        except subprocess.CalledProcessError:
            print('WARNING: {commandString:s} failed.\n'.format(commandString = commandString), file = sys.stderr)

        # Report on the generation of the .bib file.
        bcfFileName = texFileNameStub + ".bcf"
        bibFileName = os.path.join(self.outDirectory, re.sub('.tex$', '.bib', self.outFileBaseName))
        print('Creating              {bibFileName:s}'.format(bibFileName = bibFileName))

        # Make the .bib file writable (in case it exists).
        try:
            os.chmod(bibFileName, stat.S_IWRITE)
        except:
            pass

        # Invoke spbf on the generated .bcf file, provided it is non-empty.
        commandString = "spbf convert " + bcfFileName + " " + self.customBibliographySwitches
        with open(bibFileName, "w") as bibFileStream:
            returnValue = subprocess.run(commandString, shell = True, stdout = bibFileStream)
        try:
            returnValue.check_returncode()
        except subprocess.CalledProcessError:
            print('WARNING: {commandString:s} failed.\n'.format(commandString = commandString), file = sys.stderr)

        # Make the .bib file protected.
        try:
            os.chmod(bibFileName, stat.S_IREAD)
        except:
            pass

        # Remove temporary files.
        fp.close()
        fileList = glob.glob(texFileNameStub + ".*")
        for filePath in fileList:
            os.remove(filePath)
        return ""

    # CustomBibTeXFileName()
    # returns a string such as
    #   manuscript-template.bib
    # derived from the outFileBaseName name.
    def CustomBibTeXFileName(self):
        return self.CustomBibTeXFileNameWithoutExtension() + ".bib"

    # CustomBibTeXFileNameWithoutExtension()
    # returns a string such as
    #   manuscript-template
    # derived from the outFileBaseName name.
    def CustomBibTeXFileNameWithoutExtension(self):
        return self.outFileBaseName.rsplit(".",1)[0]

    # CustomBibliography()
    # returns a string such as
    #   \IfFileExists{./manuscript-template.bib}{\bibliography{./manuscript-template.bib}}{\bibliography{file.bib,file.bib}}
    # with the BibTeX file name as returned by customBibTeXFile(self)
    # or (in case --nocustombib was given)
    #   \bibliography{file.bib,file.bib}
    # . In case --nobib was given, an empty string is returned.
    def CustomBibliography(self):
        fallbackBibliography = self.CommandWrapper(",".join(self.LaTeXBibFiles()), "\\bibliography")
        if self.noBib:
            return ""
        if self.customBib:
            # Create the custom .bib file.
            self.CreateCustomBibTeXFile()
        return "\\IfFileExists{./" + self.CustomBibTeXFileName() + "}{\\bibliography{./" + self.CustomBibTeXFileName() + "}}{" + fallbackBibliography + "}"

    # CustomBibliographyWithoutExtension()
    # returns a string such as
    #   \IfFileExists{./manuscript-template.bib}{\bibliography{./manuscript-template}}{\bibliography{file,file}}
    # with the BibTeX file name as returned by customBibTeXFileWithoutExtension(self)
    # or (in case --nocustombib was given)
    #   \bibliography{file,file}
    # . In case --nobib was given, an empty string is returned.
    def CustomBibliographyWithoutExtension(self):
        fallbackBibliography = self.CommandWrapper(",".join(self.LaTeXBibFileNamesWithoutExtension()), "\\bibliography")
        if self.noBib:
            return ""
        if self.customBib:
            # Create the custom .bib file.
            self.CreateCustomBibTeXFile()
        return "\\IfFileExists{./" + self.CustomBibTeXFileName() + "}{\\bibliography{./" + self.CustomBibTeXFileNameWithoutExtension() + "}}{" + fallbackBibliography + "}"

    # BibLaTeXResources()
    # returns a string such as
    #   \addbibresources{bibfile.bib}{}
    #   \addbibresources{bibfile.bib}{}
    # .
    def BibLaTeXResources(self):
        bibFiles = self.LaTeXBibFiles()
        return "\n".join([self.CommandWrapper(bibFile, "\\addbibresource") for bibFile in bibFiles])

    # BibLaTeXPrintBibliography()
    # returns a string such as
    #   \printbibliography
    # unless --nobib was given.
    def BibLaTeXPrintBibliography(self):
        if self.noBib:
            return ""
        else:
            return "\\printbibliography"

    # InputBody()
    # returns a string such as
    #   \input{file.tex}
    #   \input{file.tex}
    # .
    def InputBody(self):
        body = self.LaTeXBody()
        return "\n".join(["\\input{" + bodyFile + "}" for bodyFile in body])

    # InputAbstract()
    # returns a string such as
    #   \input{file.tex}
    #   \input{file.tex}
    # .
    def InputAbstract(self):
        abstract = self.LaTeXAbstract()
        return "\n".join(["\\input{" + abstractFile + "}" for abstractFile in abstract])

    # InputAppendix()
    # returns a string such as
    #   \input{file.tex}
    #   \input{file.tex}
    # .
    def InputAppendix(self):
        appendix = self.LaTeXAppendix()
        return "\n".join(["\\input{" + appendixFile + "}" for appendixFile in appendix])

    # MSCLink(msc)
    # returns a string such as
    #   \href{https://mathscinet.ams.org/msc/msc2020.html?t=49J20}{49J20}
    # .
    def MSCLink(self, msc):
        return "\\href{https://mathscinet.ams.org/msc/msc2020.html?t=" + msc + "}{" + msc + "}"

    # MSC()
    # returns a comma separated string with unformatted entries.
    def MSC(self):
        msc = self.ManuscriptMSC()
        return ", ".join([singleMSC for singleMSC in msc])

    # MSCBackslashAndSeparated()
    # returns an \and separated string with unformatted entries.
    def MSCBackslashAndSeparated(self):
        msc = self.ManuscriptMSC()
        return " \\and ".join([singleMSC for singleMSC in msc])

    # MSCWithLinks()
    # returns a comma separated string with entries formatted by mscLink().
    def MSCWithLinks(self):
        msc = self.ManuscriptMSC()
        return ", ".join([self.MSCLink(singleMSC) for singleMSC in msc])

    # MSCInBackslashKWD()
    # returns a string such as
    #   \kwd{MSC}
    #   \kwd{MSC}
    # .
    def MSCInBackslashKWD(self):
        return self.CommandWrapper(self.ManuscriptMSC(), "\\kwd")

    # KeywordsCommaSeparated()
    # returns a comma separated string with unformatted entries.
    def KeywordsCommaSeparated(self):
        return ", ".join(self.ManuscriptKeywords())

    # KeywordsSemicolonSeparated()
    # returns a semicolon separated string with unformatted entries.
    def KeywordsSemicolonSeparated(self):
        return "; ".join(self.ManuscriptKeywords())

    # KeywordsBackslashAndSeparated()
    # returns an \and separated string with unformatted entries.
    def KeywordsBackslashAndSeparated(self):
        return "\\and ".join(self.ManuscriptKeywords())

    # KeywordsInBackslashKWD()
    # returns a string such as
    #   \kwd{keyword}
    #   \kwd{keyword}
    # .
    def KeywordsInBackslashKWD(self):
        return self.CommandWrapper(self.ManuscriptKeywords(), "\\kwd")

    # Title()
    # returns manuscript["title"] as is with "" as default.
    def Title(self):
        return self.manuscript.get("title", "") or ""

    # ShortTitle()
    # returns manuscript["shortTitle"] as is, with Title() as a fallback.
    def ShortTitle(self):
        shortTitle = self.manuscript.get("shorttitle", "") or ""
        if shortTitle:
            return shortTitle
        else:
            return self.Title()

    # ShortTitleWithCAPS()
    # returns shortTitle() but with CAPS.
    def ShortTitleWithCAPS(self):
        return self.ShortTitle().upper()

    # SubTitle()
    # returns manuscript["subtitle"] as is with "" as default.
    def SubTitle(self):
        return self.manuscript.get("subtitle", "") or ""

    # TitleNewlineSubTitle()
    # returns a string composed of Title() and Subtitle(), separated by a newline.
    def TitleNewlineSubTitle(self):
        return " \\\\ ".join(filter(None, [self.Title(), self.SubTitle()]))

    # Date()
    # returns manuscript["date"] as is.
    def Date(self):
        return self.manuscript.get("date", "") or ""

    # Dedication()
    # returns manuscript["dedication"] as is.
    def Dedication(self):
        return self.manuscript.get("dedication", "") or ""

    # DedicationCommand()
    # returns a string such as
    #   \dedication{dedication}
    # unless manuscript["dedication"] is empty.
    def DedicationCommand(self):
        dedication = self.manuscript.get("dedication", "") or ""
        if dedication:
            return self.CommandWrapper(dedication, "\\dedication")
        else:
            return ""

    # DedicationFootnote()
    # returns a string such as
    #   \footnote{dedication}
    # unless manuscript["dedication"] is empty.
    def DedicationFootnote(self):
        if self.Dedication():
            return self.CommandWrapper(self.Dedication(), "\\footnote")
        else:
            return ""

    # DedicationFootnoteText()
    # returns a string such as
    #   \footnotetext{dedication}
    # unless manuscript["dedication"] is empty.
    def DedicationFootnoteText(self):
        if self.Dedication():
            return "\\footnotetext{" + self.Dedication() + "}"
        else:
            return ""

    # DedicationVerse()
    # returns a string such as
    #   \begin{verse}
    #   dedication
    #   \end{verse}
    # unless manuscript["dedication"] is empty.
    def DedicationVerse(self):
        if self.Dedication():
            return "\\begin{verse}\n" + self.Dedication() + "\n\\end{verse}\n"
        else:
            return ""

    # DedicationThanks()
    # returns a string such as
    #   \thanks{dedication}
    # unless manuscript["dedication"] is empty.
    def DedicationThanks(self):
        if self.Dedication():
            return "\\thanks{" + self.Dedication() + "}"
        else:
            return ""

    # DedicationTnoteRef()
    # returns a string such as
    #   \tnoteref{Elsevier-t2}
    # unless manuscript["dedication"] is empty.
    def DedicationTnoteRef(self):
        if self.Dedication():
            return "\\tnoteref{Elsevier-t2}"
        else:
            return ""

    # DedicationTnoteText()
    # returns a string such as
    #   \tnotetext[Elsevier-t2]{dedication}
    # unless manuscript["dedication"] is empty.
    def DedicationTnoteText(self):
        if self.Dedication():
            return "\\tnotetext[Elsevier-t2]{" + self.Dedication() + "}"
        else:
            return ""

    # DedicationThanksRef()
    # returns a string such as
    #   \thanksref{footnotededication}
    # unless manuscript["dedication"] is empty.
    def DedicationThanksRef(self):
        if self.Dedication():
            return "\\thanksref{footnotededication}"
        else:
            return ""

    # DedicationThanksText()
    # returns a string such as
    #   \thanks[footnotefunding]{dedication}
    # unless manuscript["dedication"] is empty.
    def DedicationThanksText(self):
        if self.Dedication():
            return "\\thanks[footnotededication]{" + self.Dedication() + "}"
        else:
            return ""

    # Funding()
    # returns manuscript["funding"] as is.
    def Funding(self):
        return self.manuscript.get("funding", "") or ""

    # FundingEnvironment()
    # returns a string such as
    #   \begin{funding}
    #   funding
    #   \end{funding}
    # unless manuscript["funding"] is empty.
    def FundingEnvironment(self):
        if self.Funding():
            return "\\begin{funding}\n" + self.Funding() + "\n\\end{funding}"
        else:
            return ""

    # FundingFootnote()
    # returns a string such as
    #   \footnote{funding}
    # unless manuscript["funding"] is empty.
    def FundingFootnote(self):
        if self.Funding():
            return self.CommandWrapper(self.Funding(), "\\footnote")
        else:
            return ""

    # FundingAcknowledgementEnvironment()
    # returns a string such as
    #   \begin{acknowledgement}
    #   funding
    #   \end{acknowledgement}
    # unless manuscript["funding"] is empty.
    def FundingAcknowledgementEnvironment(self):
        if self.Funding():
            return "\\begin{acknowledgement}\n" + self.Funding() + "\n\\end{acknowledgement}\n"
        else:
            return ""

    # FundingAcknowledgments()
    # returns a string such as
    #   \acknowledgments{funding}
    # unless manuscript["funding"] is empty.
    def FundingAcknowledgments(self):
        if self.Funding():
            return "\\acknowledgments{" + self.Funding() + "}"
        else:
            return ""

    # FundingTnoteRef()
    # returns a string such as
    #   \tnoteref{Elsevier-t1}
    # unless manuscript["funding"] is empty.
    def FundingTnoteRef(self):
        if self.Funding():
            return "\\tnoteref{Elsevier-t1}"
        else:
            return ""

    # FundingTnoteText()
    # returns a string such as
    #   \tnotetext[Elsevier-t1]{funding}
    # unless manuscript["funding"] is empty.
    def FundingTnoteText(self):
        if self.Funding():
            return "\\tnotetext[Elsevier-t1]{" + self.Funding() + "}"
        else:
            return ""

    # FundingThanksRef()
    # returns a string such as
    #   \thanksref{footnotefunding}
    # unless manuscript["funding"] is empty.
    def FundingThanksRef(self):
        if self.Funding():
            return "\\thanksref{footnotefunding}"
        else:
            return ""

    # FundingThanksText()
    # returns a string such as
    #   \thanks[footnotefunding]{funding}
    # unless manuscript["funding"] is empty.
    def FundingThanksText(self):
        if self.Funding():
            return "\\thanks[footnotefunding]{" + self.Funding() + "}"
        else:
            return ""

    # FundingThanks()
    # returns a string such as
    #   \thanks{funding}
    # unless manuscript["funding"] is empty.
    def FundingThanks(self):
        if self.Funding():
            return "\\thanks{" + self.Funding() + "}"
        else:
            return ""

    # FundingSectionStarred()
    # returns a string such as
    #   \section*{Funding}
    #   funding
    # unless manuscript["funding"] is empty.
    def FundingSectionStarred(self):
        if self.Funding():
            return "\\section*{Funding}\n\n" + self.Funding() + "\n"
        else:
            return ""

    # AuthorNumberFromAuthor(author)
    # returns the author number (an index into ManuscriptAuthors) from the author.
    def AuthorNumberFromAuthor(self, author):
        return self.ManuscriptAuthors().index(author)

    # AuthorFromAuthorNumber(authorNumber)
    # returns the author from the author number (an index into ManuscriptAuthors).
    def AuthorFromAuthorNumber(self, authorNumber):
        return self.ManuscriptAuthors()[authorNumber]

    # AuthorsFromInstitutionTag(institutionTag)
    # returns the list of authors affiliated with an institution.
    def AuthorsFromInstitutionTag(self, institutionTag):
        return [author for author in self.ManuscriptAuthors() if institutionTag in self.InstitutionTagsFromAuthor(author)]

    # AuthorFromAuthorTag(authorTag)
    # returns the author from their tag.
    def AuthorFromAuthorTag(self, authorTag):
        return next(author for author in self.authors if author.get("tag") == authorTag)

    # AuthorGivenName(author, separator)
    # returns a string such as
    #   givenname
    # .
    def AuthorGivenName(self, author, separator = " "):
        return (author.get("givenname", "") or "").replace(" ", separator)

    # AuthorFamilyName(author, separator)
    # returns a string such as
    #   familyname
    # .
    def AuthorFamilyName(self, author, separator = " "):
        return (author.get("familyname", "") or "").replace(" ", separator)

    # AuthorFullName(author, separator)
    # returns a string such as
    #   givenname familyname
    # or
    #   givenname~familyname
    # .
    def AuthorFullName(self, author, separator = " "):
        return separator.join([self.AuthorGivenName(author, separator = separator), self.AuthorFamilyName(author, separator = separator)])

    # AuthorShortName(author, separator)
    # returns a string such as
    #   G.-N. familyname
    # or
    #   G.-N.~familyname
    # .
    def AuthorShortName(self, author, separator = " "):
        s = ""
        for index, givennames in enumerate(re.split('([- ])', self.AuthorGivenName(author))):
            s = s + givennames[0]
            if not (index % 2):
                s = s + "."
        return (s + " " + self.AuthorFamilyName(author)).replace(" ", separator)

    # AuthorShortNameNoPeriod(author, separator)
    # returns a string such as
    #   G-N familyname
    # or
    #   G-N~familyname
    # .
    def AuthorShortNameNoPeriod(self, author, separator = " "):
        s = ""
        for index, givennames in enumerate(re.split('([- ])', self.AuthorGivenName(author))):
            s = s + givennames[0]
        return (s + " " + self.AuthorFamilyName(author)).replace(" ", separator)

    # AuthorsFullNamesCommaSeparated(separator)
    # returns a string such as
    #   givenname familyname, givenname familyname
    # or
    #   givenname~familyname, givenname~familyname
    # .
    def AuthorsFullNamesCommaSeparated(self, separator = " "):
        return ", ".join([self.AuthorFullName(author, separator = separator) for author in self.ManuscriptAuthors()])

    # Join(content, allButLast, last)
    # returns a string similar to
    #   allButLast.join(content)
    # except that the last occurrence of the separator allButLast is replaced by Last.
    def Join(self, content, allButLast, last):
        return last.join([allButLast.join(content[:-1]), content[-1]] if len(content) > 2 else content)

    # AuthorsFamilyNamesCommaSeparatedLastAnd()
    # returns a string such as
    #   familyname, familyname and familyname
    # .
    def AuthorsFamilyNamesCommaSeparatedLastAnd(self):
        return self.Join((lambda self: [self.AuthorFamilyName(author) for author in self.ManuscriptAuthors()])(self), ", ", " and ")

    # AuthorsFullNamesCommaSeparatedLastAnd()
    # returns a string such as
    #   givenname familyname, givenname familyname and givenname familyname
    # .
    def AuthorsFullNamesCommaSeparatedLastAnd(self):
        return self.Join((lambda self: [self.AuthorFullName(author) for author in self.ManuscriptAuthors()])(self), ", ", " and ")

    # AuthorsShortNamesCommaSeparated()
    # returns a string such as
    #   G.-N. familyname, G.-N. familyname, G.-N. familyname
    # .
    def AuthorsShortNamesCommaSeparated(self):
        return ", ".join([self.AuthorShortName(author) for author in self.ManuscriptAuthors()])

    # AuthorsShortNamesCommaSeparatedLastAnd()
    # returns a string such as
    #   G.-N. familyname, G.-N. familyname and G.-N. familyname
    # .
    def AuthorsShortNamesCommaSeparatedLastAnd(self):
        return self.Join((lambda self: [self.AuthorShortName(author) for author in self.ManuscriptAuthors()])(self), ", ", " and ")

    # AuthorsShortNamesCommaSeparatedLastCommaAnd()
    # returns a string such as
    #   G.-N. familyname, G.-N. familyname, and G.-N. familyname
    # .
    def AuthorsShortNamesCommaSeparatedLastCommaAnd(self):
        return self.Join((lambda self: [self.AuthorShortName(author) for author in self.ManuscriptAuthors()])(self), ", ", ", and ")

    # AuthorsShortNamesCommaSeparatedLastAmpersand()
    # returns a string such as
    #   G.-N. familyname, G.-N. familyname and G.-N. familyname
    # .
    def AuthorsShortNamesCommaSeparatedLastAmpersand(self):
        return self.Join((lambda self: [self.AuthorShortName(author) for author in self.ManuscriptAuthors()])(self), ", ", " \& ")

    # AuthorColor(author):
    # returns a string such as
    #   red
    # representing uhe author's color.
    def AuthorColor(self, author):
        return author.get("color", "") or ""

    # EnsureList(content)
    # returns content as is, if it already is a list, or [content] if not.
    def EnsureList(self, content):
        if isinstance(content, list):
            return content
        else:
            return [content]

    # CommandWrapper(content, command, separator)
    # where content is a string or a list of strings
    # and command is a string or a list of strings
    # returns a string such as
    #   \command{content}
    # .
    # When content == ["item1", "item2", "item3"] and
    # command == ["command1", "command2"],
    # then it returns
    #   \command1{item1}
    #   \command2{item2}
    #   \command2{item3}
    # .
    # The default separator, which is used to join the list items, is "\n".
    # When the separator is 'None', then no concatenation will be performed.
    def CommandWrapper(self, content, command, separator = "\n"):
        content = self.EnsureList(content)
        commands = self.EnsureList(command)
        commands = commands[:len(content)]  # truncate the commands list if necessary
        commands.extend(commands[-1:] * (len(content) - len(commands)))  # amend the commands list by repeating the last element if necessary
        commands = [command + "{" + item + "}" for (command, item) in zip(commands, content)]
        if separator is not None:
            return separator.join(commands)
        else:
            return commands

    # IsCorrespondingAuthor(author)
    # returns True if author is among the manuscript authors,
    # i.e., if author's tag is in manuscript["authors"].
    def IsCorrespondingAuthor(self, author):
        return author.get("tag") in self.EnsureList(self.manuscript.get("corresponding"))

    # ManuscriptAuthors()
    # returns a list of authors from author tags in manuscript["authors"].
    def ManuscriptAuthors(self):
        return [self.AuthorFromAuthorTag(authorTag) for authorTag in self.EnsureList(self.manuscript.get("authors"))]

    # CorrespondingAuthors()
    # returns a list of authors from author tags in manuscript["authors"], limited to those who are corresponding authors.
    def CorrespondingAuthors(self):
        return [self.AuthorFromAuthorTag(authorTag) for authorTag in self.EnsureList(self.manuscript.get("corresponding"))]

    # AddressFromInstitutionTag(institutionTag)
    # returns the institution as is.
    def AddressFromInstitutionTag(self, institutionTag):
        return self.institutions.get(institutionTag, "") or ""

    # AddressesFromAuthor(author)
    # returns a list of addresses for an author.
    def AddressesFromAuthor(self, author):
        return [self.AddressFromInstitutionTag(institutionTag) for institutionTag in self.InstitutionTagsFromAuthor(author)]

    # AddressesFromInstitutionNumbers(institutionNumbers)
    # returns a list of addresses for institutionsNumbers, which can be an integer or a list.
    def AddressesFromInstitutionNumbers(self, institutionNumbers):
        return [self.AddressFromInstitutionTag(self.UniqueInstitutionTags()[institutionNumber]) for institutionNumber in self.EnsureList(institutionNumbers)]

    # AuthorEMails(author)
    # returns a list of email addresses for an author.
    def AuthorEMails(self, author):
        return self.EnsureList(author.get("emails", []) or [])

    # AuthorURLs(author)
    # returns a list of email addresses for an author.
    def AuthorURLs(self, author):
        return [self.EscapedURL(url) for url in self.EnsureList(author.get("urls", []) or []) if url]

    # EscapedURL(url)
    # returns a URL with some characters escaped.
    def EscapedURL(self, url):
        return url.replace('~', '\\string~')

    # InstitutionTagsFromAuthor(author)
    # returns a list of institution tags for an author
    # with "None"s eliminated.
    def InstitutionTagsFromAuthor(self, author):
        return self.EnsureList(author.get("institutions", []) or [])

    # InstitutionNumberFromInstitutionTag(institutionTag)
    # returns the index into UniqueInstitutionTags() corresponding to institutionTag.
    def InstitutionNumberFromInstitutionTag(self, institutionTag):
        return self.UniqueInstitutionTags().index(institutionTag)

    # AuthorAMS(author)
    # returns a string such as
    #   \author{givenname familyname}
    #   \address[tag]{Institute, City, Country}
    #   \address[tag]{Institute, City, Country}
    #   \email{email}
    #   \email{email}
    #   \urladdr{URL}
    # .
    def AuthorAMS(self, author):
        return self.CommandWrapper(self.AuthorFullName(author), "\\author") + "\n" + \
            self.CommandWrapper(self.AddressesFromAuthor(author), "\\address[" + self.AuthorShortName(author) + "]") + "\n" + \
            self.CommandWrapper(self.AuthorEMails(author), "\\email") + "\n" + \
            self.CommandWrapper(self.AuthorURLs(author), "\\urladdr") + "\n"

    # AuthorsInstitutionsAMS()
    # returns a string according to AuthorAMS(author), one for each author, followed by funding information,
    # attributed to the last author.
    def AuthorsInstitutionsAMS(self):
        return "\n".join([self.AuthorAMS(author) for author in self.ManuscriptAuthors()] + [self.FundingThanks()])

    # AuthorEMS(author)
    # returns a string such as
    #   \emsauthor{1}{givenname familyname}{G.-N.~familyname}
    #   \emsaffil{1}{Institute, City, Country\email{email}\secondemail{email}\secondemail{email}}
    # or
    #   \emsauthor*{1}{givenname familyname}{G.-N.~familyname}
    #   \emsaffil{1}{Institute, City, Country\email{email}\secondemail{email}\secondemail{email}}
    # .
    def AuthorEMS(self, author):
        authorNumber = self.AuthorNumberFromAuthor(author)
        if self.IsCorrespondingAuthor(author):
            authorString = self.CommandWrapper(str(authorNumber), "\\emsauthor*") + self.CommandWrapper(self.AuthorFullName(author), "") + self.CommandWrapper(self.AuthorShortName(author, separator = "~"), "")
        else:
            authorString = self.CommandWrapper(str(authorNumber), "\\emsauthor") + self.CommandWrapper(self.AuthorFullName(author), "") + self.CommandWrapper(self.AuthorShortName(author, separator = "~"), "")
        addressString = "; ".join(self.AddressesFromAuthor(self.AuthorFromAuthorNumber(authorNumber)))
        emailString = self.CommandWrapper(self.AuthorEMails(author), ["\\email", "\\secondemail"], "")
        affiliationString = self.CommandWrapper(str(authorNumber), "\\emsaffil") + self.CommandWrapper(addressString + emailString, "")
        return "\n".join([authorString, affiliationString])

    # AuthorsInstitutionsEMS()
    # returns a string according to AuthorEMS(author), one for each author.
    def AuthorsInstitutionsEMS(self):
        return "\n".join([self.AuthorEMS(author) for author in self.ManuscriptAuthors()])

    # AuthorEMSSimple(author)
    # returns a string such as
    #   givenname familyname (Institute, City, Country)
    # .
    def AuthorEMSSimple(self, author):
        addressString = "; ".join(self.AddressesFromAuthor(author))
        return self.AuthorFullName(author) + " (" + addressString + ")"

    # AuthorsInstitutionsEMSSimple()
    # returns a string according to AuthorEMSSimple(author), one for each author.
    def AuthorsInstitutionsEMSSimple(self):
        return " \\\\\n".join([self.AuthorEMSSimple(author) for author in self.ManuscriptAuthors()])

    # AuthorACS(author)
    # returns a string such as
    #   \author{givenname familyname}
    #   \affiliation{Institute, City, Country} for the author's 1st affiliation
    #   \alsoaffiliation{Institute, City, Country} for the author's 2nd affiliation
    #   \altaffiliation{Institute, City, Country} for the author's 3rd and further affiliations
    #   \email{email address,email address}
    # .
    def AuthorACS(self, author):
        return self.CommandWrapper(self.AuthorFullName(author), "\\author") + "\n" + \
            self.CommandWrapper(self.AddressesFromAuthor(author), ["\\affiliation", "\\alsoaffiliation", "\\altaffiliation"]) + "\n" + \
            self.CommandWrapper(", ".join(self.AuthorEMails(author)), "\\email") + "\n"

    # AuthorsInstitutionsACS()
    # returns a string according to AuthorACS(author), one for each author.
    def AuthorsInstitutionsACS(self):
        return "\n".join([self.AuthorACS(author) for author in self.ManuscriptAuthors()])

    # FlattenList(content)
    #   returns a list of lists content flattened to a list.
    def FlattenList(self, content):
        return [item for sublist in content for item in sublist]

    # UniqueInstitutionTags()
    #   returns a list of institutions at least one author is affiliated with, ordered by the manuscript authors.
    def UniqueInstitutionTags(self):
        return list(dict.fromkeys(self.FlattenList([self.InstitutionTagsFromAuthor(author) for author in self.ManuscriptAuthors()])))

    # InstitutionNumbersFromAuthor(author)
    # returns a list of indices into the UniqueInstitutionTags an authors belongs to.
    def InstitutionNumbersFromAuthor(self, author):
        return [self.UniqueInstitutionTags().index(institution) for (institution) in self.InstitutionTagsFromAuthor(author)]

    # InstitutionNumbersByAuthor()
    # returns a list of lists of indices into the UniqueInstitutionTags the authors belong to.
    def InstitutionNumbersByAuthor(self):
        return [self.InstitutionNumbersFromAuthor(author) for author in self.ManuscriptAuthors()]

    # AuthorCMAM(author)
    # returns a string such as
    #   \author[0,1]{givenname familyname} or
    #   \author*[0,1]{givenname familyname}
    # where [0,1] are indices into the UniqueInstitutionTags the author belongs to.
    def AuthorCMAM(self, author):
        if self.IsCorrespondingAuthor(author):
            return self.CommandWrapper(self.AuthorFullName(author), "\\author*[" + ",".join([str(index) for index in self.InstitutionNumbersFromAuthor(author)]) + "]")
        else:
            return self.CommandWrapper(self.AuthorFullName(author), "\\author[" + ",".join([str(index) for index in self.InstitutionNumbersFromAuthor(author)]) + "]")

    # InstitutionCMAM(institutionTag)
    # returns a string such as
    #   \affil[0]{Institute, City, Country, e-mail: email, email}
    # .
    def InstitutionCMAM(self, institutionTag):
        email = ", ".join(self.AuthorEMailsIfFirstFromInstitutionTag(institutionTag))
        if email:
            email = ",\ne-mail: " + email + "\n"
        else:
            email = ""
        return self.CommandWrapper(self.AddressFromInstitutionTag(institutionTag) + email, "\\affil[" + str(self.UniqueInstitutionTags().index(institutionTag)) + "]")

    # AuthorEMailsIfFirstFromInstitutionTag(institutionTag)
    # returns a list of email addresses for those authors whose first institution agrees with institutionTag.
    def AuthorEMailsIfFirstFromInstitutionTag(self, institutionTag):
        return self.FlattenList([self.AuthorEMails(author) for author in self.ManuscriptAuthors() if self.InstitutionTagsFromAuthor(author)[0] == institutionTag])

    # AuthorEMailsFromInstitutionTag(institutionTag)
    # returns a list of email addresses for those authors any of whose institution agrees with institutionTag.
    def AuthorEMailsFromInstitutionTag(self, institutionTag):
        return self.FlattenList([self.AuthorEMails(author) for author in self.ManuscriptAuthors() if institutionTag in self.InstitutionTagsFromAuthor(author)])

    # AuthorsInstitutionsCMAM()
    # returns a string such as
    #   \author[0,1]{givenname familyname}
    #   \author[1]{givenname familyname}
    #   \affil[0]{Institute, City, Country}
    #   \affil[1]{Institute, City, Country}
    # .
    def AuthorsInstitutionsCMAM(self):
        return "\n".join([self.AuthorCMAM(author) for author in self.ManuscriptAuthors()]) + "\n" + \
            "\n".join([self.InstitutionCMAM(institutionTag) for institutionTag in self.UniqueInstitutionTags()])

    # AssignedInstitutionNumbersByAuthor(A, b, c)
    # determines an assignment of institutions to authors, i.e., which author gets to 'present' which of
    # the institutions they are affiliated with. The function returns three lists.
    # The first list, termed
    #   assignedInstitutionNumbersByAuthor,
    # determines for each author which
    # institution(s) (if any) they present, by index into UniqueInstitutionTags.
    # This is determined through the solution of an assignment problem of the type
    #   Minimize c'x
    #   s.t. A x <= b
    #   and  x >= 0
    # where
    #   A is the unsigned indicence matrix of the bipartite author-institutions graph,
    #   b is the vector of assignment capacities of authors and institutions,
    #   c is the cost vector determining a preference of assignments.
    # The first block of rows of A pertain to authors.
    # The second block of rows of A pertain to institutions.
    # The second list,
    #   extraInstitutionNumbersByAuthors,
    # contains, for each author, indices into UniqueInstitutionTags to indicate institutions they
    # are affiliated with but which are presented by another author.
    # The third list,
    #   assignedFellowAuthorsByAuthor,
    # contains information about which author gets to present whose
    # email addresses. Email addresses of an author are presented the first time one of the institutions
    # they are affiliated with is presented.
    def AssignedInstitutionNumbersByAuthor(self, A, b, c):
        # Solve the assignment problem described by the data (A, b, c).
        result = optimize.linprog(c, A_ub = A, b_ub = b, method = "simplex")
        if not result.success:
            print()
            raise Exception('ERROR: Assigning authors to institutions failed.')

        # Make sure that a perfect assignment has been achieved.
        if result.x.sum() < len(self.UniqueInstitutionTags()):
            print()
            raise Exception('ERROR: There appear to be too many different institutions for them to be assigned to the authors.')

        # Postprocess the result to find the assignedInstitutionNumbersByAuthor.
        assignedInstitutionNumbersByAuthor = [[] for _ in range(len(self.ManuscriptAuthors()))]
        for column in result.x.nonzero()[0]:
            assignedInstitutionNumbersByAuthor[A[:len(self.ManuscriptAuthors()),column].nonzero()[0][0]].append(A[len(self.ManuscriptAuthors()):,column].nonzero()[0][0])

        # Perform a pass over the authors to collect any remaining institutions of an author not assigned to them.
        # Initialize the assignments of institution numbers to authors.
        extraInstitutionNumbersByAuthors = [[] for _ in range(len(self.InstitutionNumbersByAuthor()))]
        for authorNumber in range(len(self.ManuscriptAuthors())):
            extraInstitutionNumbersByAuthors[authorNumber] = list(set(self.InstitutionNumbersByAuthor()[authorNumber]) - set(assignedInstitutionNumbersByAuthor[authorNumber]))

        # Finally, go through the authors and the institutions assigned to them, and record which authors affiliated with that institution
        # will use the opportunity to have their email addresses presented.
        assignedFellowAuthorsByAuthor = [[] for _ in range(len(self.InstitutionNumbersByAuthor()))]
        authorEMailsCovered = [False for _ in range(len(self.ManuscriptAuthors()))]
        for authorNumber in range(len(self.ManuscriptAuthors())):
            # Find all authors at the current author's assigned institution, which have not had their email addresses presented.
            for localAuthorNumber in range(len(self.ManuscriptAuthors())) :
                if not set(assignedInstitutionNumbersByAuthor[authorNumber]).isdisjoint(self.InstitutionNumbersByAuthor()[localAuthorNumber]) and not authorEMailsCovered[localAuthorNumber]:
                    assignedFellowAuthorsByAuthor[authorNumber].append(localAuthorNumber)
                    authorEMailsCovered[localAuthorNumber] = True
        return (assignedInstitutionNumbersByAuthor, extraInstitutionNumbersByAuthors, assignedFellowAuthorsByAuthor)

    # AssignmentIncidenceMatrix()
    # returns an undirected incidence matrix A with initial rows indicating
    # authors and later rows indicating institutions, describing which author is
    # affiliated with which institutions.
    def AssignmentIncidenceMatrix(self):
        A = np.zeros([len(self.ManuscriptAuthors()) + len(self.UniqueInstitutionTags()), 0])
        for authorNumber in range(len(self.ManuscriptAuthors())):
            for institutionNumber in self.InstitutionNumbersByAuthor()[authorNumber]:
                column = np.zeros([len(self.ManuscriptAuthors()) + len(self.UniqueInstitutionTags()), 1])
                column[authorNumber,0] = 1
                column[len(self.ManuscriptAuthors()) + institutionNumber,0] = 1
                A = np.hstack((A, column))
        return A

    # AssignedInstitutionNumbersByAuthorESAIM()
    # calls AssignedInstitutionNumbersByAuthor(A, b, c) to solve an assignment problem
    # in order to determine which author 'presents' which institution(s).
    # In ESAIM templates, each author 'presents' up to two institutions they are affiliated with.
    # In case an author presents two institutions, they cannot be affiliated with more than those two.
    # In case an author presents zero or one institutions, they can be affiliated with an arbitrary number of further institutions,
    # which are presented by other authors.
    # As an example, a manuscript has 4 authors and
    #   InstitutionNumbersByAuthor == [[0,1,2,3], [1,3], [1,2], [2]].
    # Then AssignedInstitutionNumbersByAuthorESAIM() should return the lists
    #   [[0], [1,3], [2], []]       (author 0 presents institution 0; author 1 presents institutions 1 and 3 and so on)
    #   [[1,2,3], [], [1], [2]]     (author 0 has additional institutions 1,2,3 and so on)
    #   [[0], [1,2], [3], []]       (author 0 presents email addresses for author 0 only and so on)
    def AssignedInstitutionNumbersByAuthorESAIM(self):
        # Set up the incidence matrix.
        A = self.AssignmentIncidenceMatrix()

        # Create the authors' part of the capacity vector b reflecting how many institutions can be assigned to each author.
        # This is normally two unless an author has more than two institutions they are affiliated with, then they can present
        # only one of these institutions themselves.
        b = 2 * np.ones(len(self.ManuscriptAuthors()))
        for authorNumber in range(len(self.ManuscriptAuthors())):
            if len(self.InstitutionNumbersByAuthor()[authorNumber]) > 2:
                b[authorNumber] = 1

        # Create the institutions' part of the right hand side vector b reflecting that each institution should not be assigned to more than one author.
        b = np.hstack((b, np.ones(len(self.UniqueInstitutionTags()))))

        # Define the cost vector, indicating that we prefer assignments of
        # institutions to authors coming early in the list.
        c = np.arange(-A.shape[1], 0)

        # Return the result.
        return self.AssignedInstitutionNumbersByAuthor(A, b, c)

    # AuthorInstitutionsESAIM(authorNumber)
    # returns a string such as
    #   \author{givenname familyname}
    #   \address{Institute, City, Country, e-mail:
    #   \email{}
    #   \email{}
    #   }
    # or
    #   \author{givenname familyname}
    #   \sameaddress{1}
    #   \secondaddress{Institute, City, Country, e-mail:
    #   \email{}
    #   \email{}
    #   }
    # .
    # The information which institution the author has been assigned to present is taken from
    # AssignedInstitutionNumbersByAuthorESAIM().
    # The \email addresses included in the \address or \secondaddress command are those of all authors assigned to the particular institute whose email addresses have not been output previously.
    def AuthorInstitutionsESAIM(self, authorNumber):

        # Get all authors' assignments of institutions to them, as well as all authors' further institutions and fellow authors (whose email addresses they present).
        (assignedInstitutionNumbersByAuthor, extraInstitutionNumbersByAuthors, assignedFellowAuthorsByAuthor) = self.AssignedInstitutionNumbersByAuthorESAIM()
        institutionNumbersInOrderOfAppearance = self.FlattenList(assignedInstitutionNumbersByAuthor)

        # Typeset the author name.
        authorInstitutionsESAIM = self.CommandWrapper(self.AuthorFullName(self.AuthorFromAuthorNumber(authorNumber)), "\\author")

        # First typeset any extra institutions of the author (via \sameaddress).
        if extraInstitutionNumbersByAuthors[authorNumber]:
            authorInstitutionsESAIM = authorInstitutionsESAIM + "\n" + self.CommandWrapper(",\\,".join(sorted([str(institutionNumbersInOrderOfAppearance.index(institutionNumber) + 1) for (institutionNumber, institutionNumbersInOrderOfAppearance) in zip(extraInstitutionNumbersByAuthors[authorNumber], itertools.repeat(institutionNumbersInOrderOfAppearance))])), "\\sameaddress")

        # Then typeset the institution(s) (if any) assigned to the author (via
        # \address or \secondaddress), together with the email addresses of all
        # assigned fellow authors.
        authorEMailsCovered = [False for _ in range(len(self.ManuscriptAuthors()))]
        for (index, institutionNumber) in enumerate(assignedInstitutionNumbersByAuthor[authorNumber]):
            institutionTag = self.UniqueInstitutionTags()[institutionNumber]
            address = self.AddressFromInstitutionTag(institutionTag)
            emails = []
            for localAuthorNumber in assignedFellowAuthorsByAuthor[authorNumber]:
                # If the author identified by localAuthorNumber is at the institution identified by institutionTag,
                # add their email addresses unless they have been presented before.
                if institutionTag in self.InstitutionTagsFromAuthor(self.AuthorFromAuthorNumber(localAuthorNumber)) and not authorEMailsCovered[localAuthorNumber]:
                    emails = emails + self.AuthorEMails(self.AuthorFromAuthorNumber(localAuthorNumber))
                    authorEMailsCovered[localAuthorNumber] = True
            emails = self.CommandWrapper("\ \&\ ".join(emails), "\\email")
            if emails:
                addressEMails = address + " \\\\\n" + emails + "\n"
            else:
                addressEMails = address + "\n"
            if (index == 1) or extraInstitutionNumbersByAuthors[authorNumber]:
                authorInstitutionsESAIM = authorInstitutionsESAIM + "\n" + self.CommandWrapper(addressEMails, "\\secondaddress")
            elif (index == 0):
                authorInstitutionsESAIM = authorInstitutionsESAIM + "\n" + self.CommandWrapper(addressEMails, "\\address")
            else:
                print()
                raise Exception('ERROR: An author apparently has been assigned more than two institutions. This should not have happened.')

        return authorInstitutionsESAIM

    # AuthorsInstitutionsESAIM()
    # returns a string composed of the output of AuthorInstitutionsESAIM()
    # for each author.
    def AuthorsInstitutionsESAIM(self):
        authorsInstitutionsESAIM = []
        for authorNumber in range(len(self.ManuscriptAuthors())):
            authorsInstitutionsESAIM.append(self.AuthorInstitutionsESAIM(authorNumber))
        return "\n\n".join(authorsInstitutionsESAIM)

    # AuthorElsevier(author)
    # returns a string such as
    #   \author[0,1]{givenname familyname} or
    #   \author[0,1]{givenname familyname\corref{cor1}}
    #   \cortext[cor1]{Corresponding author}
    #   \ead{email}
    #   \ead{email}
    #   \ead[url]{URL}
    # where [0,1] are indices into the UniqueInstitutionTags the author belongs to.
    def AuthorElsevier(self, author):
        if self.IsCorrespondingAuthor(author):
            authorElsevier = self.CommandWrapper(self.AuthorFullName(author) + "\\corref{cor1}", "\\author[" + ",".join([str(index) for index in self.InstitutionNumbersFromAuthor(author)]) + "]")
            authorElsevier = authorElsevier + "\n" + "\\cortext[cor1]{Corresponding author}"
        else:
            authorElsevier = self.CommandWrapper(self.AuthorFullName(author), "\\author[" + ",".join([str(index) for index in self.InstitutionNumbersFromAuthor(author)]) + "]")
        authorElsevier = authorElsevier + "\n" + self.CommandWrapper(self.AuthorEMails(author), "\\ead")
        authorElsevier = authorElsevier + "\n" + self.CommandWrapper(self.AuthorURLs(author), "\\ead[url]")
        return authorElsevier

    # AuthorsInstitutionsElsevier()
    # returns a string according to AuthorElsevier(author), one for each author, plus institution information:
    #   \address[0]{Institute, City, Country}
    #   \address[1]{Institute, City, Country}
    # .
    def AuthorsInstitutionsElsevier(self):
        return "\n".join((lambda self: [self.AuthorElsevier(author) for author in self.ManuscriptAuthors()])(self)) + "\n" + \
            "\n".join((lambda self: [self.CommandWrapper(self.AddressFromInstitutionTag(institutionTag), "\\address[" + str(self.UniqueInstitutionTags().index(institutionTag)) + "]") for institutionTag in self.UniqueInstitutionTags()])(self))

    # ShortAuthorsETNA()
    # returns a string such as
    #   G.-N. familyname, G.-N. familyname and G.-N. familyname
    # .
    def ShortAuthorsETNA(self):
        return self.AuthorsShortNamesCommaSeparatedLastAnd()

    # InstitutionETNA(institutionTag)
    # returns a string such as
    #   \footnotetext[2]{Institute, City, Country (\texttt{email}, \texttt{email})}
    # .
    def InstitutionETNA(self, institutionTag):
        email = ", ".join(self.EnsureList(self.CommandWrapper(self.AuthorEMailsIfFirstFromInstitutionTag(institutionTag), "\\texttt", ", ")))
        if email:
            email = " (" + email + ")"
        return self.CommandWrapper(self.AddressFromInstitutionTag(institutionTag) + email, "\\footnotetext[" + str(self.UniqueInstitutionTags().index(institutionTag) + 2) + "]")

    # InstitutionsETNA()
    # returns a string according to InstitutionETNA(institutionTag), one for each institutionTag.
    def InstitutionsETNA(self):
        return "\n".join([self.InstitutionETNA(institutionTag) for institutionTag in self.UniqueInstitutionTags()])

    # AuthorETNA(author)
    # returns a string such as
    #   \author{givenname familyname\footnotemark[1]\,\textsuperscript{\,\,\,,}\footnotemark[2]
    # .
    def AuthorETNA(self, author):
        return self.AuthorFullName(author) + \
            self.footnoteSeparator.join(["\\footnotemark[" + str(institutionNumber + 2) + "]" for institutionNumber in self.InstitutionNumbersFromAuthor(author)])

    # AuthorsInstitutionsETNA()
    # returns a string such as
    #   \author{givenname familyname\footnotemark[2] \and
    #   \author{givenname familyname\footnotemark[2,3]
    # .
    def AuthorsETNA(self):
        return "\n\\and\n".join((lambda self: [self.AuthorETNA(author) for author in self.ManuscriptAuthors()])(self))

    # AuthorNamesFrontiers()
    # returns a string such as
    #   familyname et al.
    # .
    def AuthorNamesFrontiers(self):
        if (len(self.ManuscriptAuthors()) > 1):
            return self.AuthorFamilyName(self.ManuscriptAuthors()[0]) + " el al."
        else:
            return self.AuthorFamilyName(self.ManuscriptAuthors()[0])

    # AuthorFrontiers()
    # returns a string such as
    #   givenname familyname$^{1,*}$  or
    #   givenname familyname$^{2}$    or
    #   givenname familyname$^{1,2}$
    # .
    def AuthorFrontiers(self, author):
        authorString = self.AuthorFullName(author) + "$^{"
        authorString = authorString + ",".join([str(index + 1) for index in self.InstitutionNumbersFromAuthor(author)])
        if self.IsCorrespondingAuthor(author):
            authorString = authorString + ",*"
        authorString = authorString + "}$"
        return authorString

    # AuthorsFrontiers()
    # returns a string such as
    #   givenname familyname$^{1,*}$;
    #   givenname familyname$^{2}$ and
    #   givenname familyname$^{1,2}$
    # .
    def AuthorsFrontiers(self):
        return self.Join((lambda self: [self.AuthorFrontiers(author) for author in self.ManuscriptAuthors()])(self), ";\n", " and ")

    # InstitutionsFrontiers()
    # returns a string such as
    #   $^{1}$Institute, City, Country \\
    #   $^{2}$Institute, City, Country
    # .
    def InstitutionsFrontiers(self):
        return " \\\\\n".join((lambda self: ["$^{" + str(self.UniqueInstitutionTags().index(institutionTag) + 1) +"}$" + self.AddressFromInstitutionTag(institutionTag) for institutionTag in self.UniqueInstitutionTags()])(self))

    # CorrespondingAuthorsFrontiers()
    # returns a string with the corresponding authors' names
    def CorrespondingAuthorsFrontiers(self):
        return ", ".join([self.AuthorFullName(author) for author in self.CorrespondingAuthors()])

    # CorrespondingAuthorsEMailsFrontiers()
    # returns a string with the email addresses of all corresponding authors separated by commas.
    def CorrespondingAuthorsEMailsFrontiers(self):
        return ", ".join(self.FlattenList((lambda self: [self.AuthorEMails(author) for author in self.CorrespondingAuthors()])(self)))

    # AuthorWiley()
    # returns a string such as
    #   \author[1]{givenname familyname} or
    #   \author[1,2]{givenname familyname}
    # .
    def AuthorWiley(self, author):
        return self.CommandWrapper(self.AuthorFullName(author), "\\author[" + ",".join([str(index) for index in self.InstitutionNumbersFromAuthor(author)]) + "]")

    # ShortAuthorsWiley()
    # returns a string such as
    #   \author{G.-N. familyname}, \author{G.-N. familyname}, and \author{G.-N. familyname}
    # .
    def ShortAuthorsWiley(self):
        return self.Join(self.CommandWrapper((lambda self: [self.AuthorShortName(author) for author in self.ManuscriptAuthors()])(self), "\\author", separator = None), ", ", ", and ")

    # AuthorsWiley()
    # returns a string such as
    #   \author[1]{givenname familyname}
    #   \author[1,2]{givenname familyname}
    #   \corres{givenname familyname. \email{email}. givenname familyname. \email{email}.}
    # .
    def AuthorsWiley(self):
        return "\n".join((lambda self: [self.AuthorWiley(author) for author in self.ManuscriptAuthors()])(self)) + "\n" + \
            self.CommandWrapper(". ".join((lambda self: [self.AuthorFullName(author) + ". " + self.CommandWrapper(", ".join(self.AuthorEMails(author)), "\\email") for author in self.CorrespondingAuthors()])(self)), "\\corres")

    # AuthorsInstitutionsWiley()
    # returns a string according to AuthorsWiley(author), plus institution information:
    #   \address[1]{Institute, City, Country}
    #   \address[2]{Institute, City, Country}
    # .
    def AuthorsInstitutionsWiley(self):
        return self.AuthorsWiley() + "\n" + \
            "\n".join((lambda self: [self.CommandWrapper(self.AddressFromInstitutionTag(institutionTag), "\\address[" + str(self.UniqueInstitutionTags().index(institutionTag)) + "]") for institutionTag in self.UniqueInstitutionTags()])(self))

    # AuthorGroupIEEETransactions()
    # returns a string such as
    #   G.-N. familyname, G.-N. familyname and G.-N. familyname are with the {Institute, City, Country}.
    #   E-mail: \email{email}, \email{email}
    # describing the authors' affiliations with an institution, together with their email addresses, provided the institution is
    # an author's first institution.
    def AuthorGroupIEEETransactions(self, institutionTag):
        institutionNumber = self.InstitutionNumberFromInstitutionTag(institutionTag)
        authors = self.Join((lambda self: [self.AuthorShortName(author) for author in self.AuthorsFromInstitutionTag(institutionTag)])(self), ", ", " and ")
        address = self.AddressFromInstitutionTag(institutionTag)
        if len(self.AuthorsFromInstitutionTag(institutionTag)) > 1:
            address = " are with the " + address + "."
        else:
            address = " is with the " + address + "."
        emails = ", ".join(self.AuthorEMailsIfFirstFromInstitutionTag(institutionTag))
        if emails:
            emails = "\nE-mail: " + emails
        return "\\IEEEcompsocthanksitem " + authors + address + emails

    # AuthorsInstitutionsIEEETransactions()
    def AuthorsInstitutionsIEEETransactions(self):
        return "\\IEEEcompsocitemizethanks{%\n" + "\n".join((lambda self: [self.AuthorGroupIEEETransactions(institutionTag) for institutionTag in self.UniqueInstitutionTags()])(self)) + "\n}"

    # AuthorNamesIEEE()
    # returns a string such as
    #   familyname et al.
    # .
    def AuthorNamesIEEE(self):
        if (len(self.ManuscriptAuthors()) > 1):
            return self.AuthorFamilyName(self.ManuscriptAuthors()[0]) + " \\textit{el al.}"
        else:
            return self.AuthorFamilyName(self.ManuscriptAuthors()[0])

    # AuthorIFAC()
    # returns a string such as
    #   \author[1]{givenname familyname} or
    #   \author[1,2]{givenname familyname}
    # .
    def AuthorIFAC(self, author):
        return self.AuthorWiley(author)

    # AuthorsIFAC()
    # returns a string such as
    #   \author[1]{givenname familyname}
    #   \author[1,2]{givenname familyname}
    # .
    def AuthorsIFAC(self):
        return "\n".join((lambda self: [self.AuthorIFAC(author) for author in self.ManuscriptAuthors()])(self))

    # AuthorsInstitutionsIFAC()
    # returns a string according to AuthorsIFAC(author), plus institution information:
    #   \address[1]{Institute, City, Country}
    #   \address[2]{Institute, City, Country}
    # .
    def AuthorsInstitutionsIFAC(self):
        return self.AuthorsIFAC() + "\n" + \
            "\n".join((lambda self: [self.CommandWrapper(self.AddressFromInstitutionTag(institutionTag), "\\address[" + str(self.UniqueInstitutionTags().index(institutionTag)) + "]") for institutionTag in self.UniqueInstitutionTags()])(self))

    # ShortAuthorsBegell()
    # returns a string such as
    #   G.-N. familyname, G.-N. familyname \& G.-N. familyname
    # .
    def ShortAuthorsBegell(self):
        return self.AuthorsShortNamesCommaSeparatedLastAmpersand()

    # AuthorBegell()
    # returns a string such as
    #   \author[1]{givenname familyname} or
    #   \author[1,2]{givenname familyname}
    # .
    def AuthorBegell(self, author):
        return self.CommandWrapper(self.AuthorFullName(author), "\\author[" + ",".join([str(index + 1) for index in self.InstitutionNumbersFromAuthor(author)]) + "]")

    # AuthorsBegell()
    # returns a string such as
    #   \author[1]{givenname familyname}
    #   \author[1,2]{givenname familyname}
    # .
    def AuthorsBegell(self):
        return "\n".join((lambda self: [self.AuthorBegell(author) for author in self.ManuscriptAuthors()])(self))

    # AuthorsInstitutionsBegell()
    # returns a string according to AuthorsBegell(author), plus institution information:
    #   \address[1]{Institute, City, Country}
    #   \address[2]{Institute, City, Country}
    # .
    def AuthorsInstitutionsBegell(self):
        return self.AuthorsBegell() + "\n" + \
            "\n".join((lambda self: [self.CommandWrapper(self.AddressFromInstitutionTag(institutionTag), "\\address[" + str(self.UniqueInstitutionTags().index(institutionTag) + 1) + "]") for institutionTag in self.UniqueInstitutionTags()])(self))


    # AuthorIMA(author)
    # returns a string such as
    #   givenname familyname
    # or
    #   givenname familyname*
    # .
    def AuthorIMA(self, author):
        if self.IsCorrespondingAuthor(author):
            return self.AuthorFullName(author) + "*"
        else:
            return self.AuthorFullName(author)

    # AuthorGroupIMA(authors)
    # returns a string such as
    #   AuthorIMA(authors[0]), AuthorIMA(authors[1]) and AuthorIMA(authors[2])
    #   \address{Institute, City, Country}
    #   \address{Institute, City, Country}
    # describing the authors' affiliations with identical institutions.
    def AuthorGroupIMA(self, authors):
        return self.CommandWrapper(self.Join((lambda self, authors: [self.AuthorIMA(author) for author in authors])(self, authors), ", ", " and ") + "\n" + \
            self.CommandWrapper(self.AddressesFromAuthor(authors[0]), "\\address"), "\\author")

    # AuthorsInstitutionsIMA()
    # returns a string according to AuthorGroupIMA(), one for each group of authors appearing consecutively
    # with identical affiliations (up to order).
    def AuthorsInstitutionsIMA(self):
        authorsInstitutionsIMA = []
        for (institutions, authors) in itertools.groupby(self.authors, lambda author: sorted(author.get("institutions", []) or [])):
            authorsInstitutionsIMA.append(self.AuthorGroupIMA(list(authors)))
        return "\n".join(authorsInstitutionsIMA)

    # CorrespondingAuthorsEMailsFrontiers()
    # returns a string such as
    #   Corresponding author: \email{email}, \email{email}
    # or
    #   Corresponding authors: \email{email}, \email{email}
    def CorrespondingAuthorsIMA(self):
        authors = self.CorrespondingAuthors()
        if len(authors) == 0:
            return ""
        emails = ", ".join((lambda self, authors: [self.CommandWrapper(self.AuthorEMails(author), "\\email", separator = ", ") for author in authors])(self, authors))
        if len(authors) == 1:
            return "Corresponding author: " + emails
        else:
            return "Corresponding authors: " + emails

    # AuthorIOP(author)
    # returns a string such as
    #   givenname familyname$^{1,2}$
    # .
    def AuthorIOP(self, author):
        return self.AuthorShortNameNoPeriod(author) + "$^{" + ",".join([str(index + 1) for index in self.InstitutionNumbersFromAuthor(author)]) + "}$"

    # AuthorsIOP()
    # returns a string such as
    #   \author{givenname familyname$^{1}$, givenname familyname$^{1,2}$ and givenname familyname$^{2}$}
    # .
    def AuthorsIOP(self):
        return self.CommandWrapper(self.Join((lambda self: [self.AuthorIOP(author) for author in self.ManuscriptAuthors()])(self), ", ", " and "), "\\author")

    # InstitutionsIOP()
    # returns a string such as
    #   \address{$^{1}$Institute, City, Country} \\
    #   \address{$^{2}$Institute, City, Country}
    # .
    def InstitutionsIOP(self):
        return "\n".join((lambda self: ["\\address{$^{" + str(self.UniqueInstitutionTags().index(institutionTag) + 1) +"}$" + self.AddressFromInstitutionTag(institutionTag) + "}" for institutionTag in self.UniqueInstitutionTags()])(self))

    # AuthorsInstitutionsIOP()
    # returns a string according to AuthorsIOP(author), plus InstitutionsIOP(), plus
    #   \ead{email, email, email}
    # .
    def AuthorsInstitutionsIOP(self):
        return self.AuthorsIOP() + "\n" + \
            self.InstitutionsIOP() + "\n" + \
            self.CommandWrapper(", ".join(self.FlattenList((lambda self: [self.AuthorEMails(author) for author in self.ManuscriptAuthors()])(self))), "\\ead")

    # ShortAuthorsJNSAO()
    # returns a string such as
    #   G.-N. familyname, G.-N. familyname and G.-N. familyname
    # .
    def ShortAuthorsJNSAO(self):
        return self.AuthorsShortNamesCommaSeparatedLastAnd()

    # InstitutionsFirstOccurrencesByAuthor()
    # returns a list, where each entry represents an author and the institutionNumbers they are affiliated with and which have
    # not appeared in the list previously.
    def InstitutionsFirstOccurrencesByAuthor(self):
        institutionsFirstOccurrencesByAuthor = [[] for _ in range(len(self.ManuscriptAuthors()))]
        for institutionNumber in range(len(self.UniqueInstitutionTags())):
            authorNumber = next((authorNumber for ((authorNumber, institutions), institutionNumber) in zip(enumerate(self.InstitutionNumbersByAuthor()), itertools.repeat(institutionNumber)) if institutionNumber in institutions), [])
            institutionsFirstOccurrencesByAuthor[authorNumber].append(institutionNumber)
        return institutionsFirstOccurrencesByAuthor

    # AssignedInstitutionNumbersByAuthorJNSAO()
    # calls AssignedInstitutionNumbersByAuthor(A, b, c) to solve an assignment problem
    # in order to determine which author 'presents' which institution(s).
    # In the JNSAO template, each author 'presents' an arbitrary number of institutions they are affiliated with, which have not been presented by previous authors.
    # As an example, a manuscript has 4 authors and
    #   InstitutionNumbersByAuthor == [[0,2], [1,3], [1,2], [2]].
    # Then AssignedInstitutionNumbersByAuthorESAIM() should return the lists
    #   [[0,2], [1,3], [], []]      (author 0 presents institutions 0 and 2; author 1 presents institutions 1 and 3 and so on)
    #   [[], [], [], []]            (no author has additional institutions)
    #   [[0,2], [1,2], [3], []]     (author 0 presents email addresses for authors 0 and 2, only and so on)
    def AssignedInstitutionNumbersByAuthorJNSAO(self):
        assignedInstitutionNumbersByAuthor = self.InstitutionsFirstOccurrencesByAuthor()

        # Set up the incidence matrix
        A = self.AssignmentIncidenceMatrix()

        # Create the authors' part of the capacity vector b reflecting how many institutions can be assigned to each author.
        # This is unlimited but optimize.linprog does not accept np.Inf.
        b = 1000 * np.ones(len(self.ManuscriptAuthors()))

        # Create the institutions' part of the right hand side vector b reflecting that each institution should not be assigned to more than one author.
        b = np.hstack((b, np.ones(len(self.UniqueInstitutionTags()))))

        # Define the cost vector, indicating that we prefer assignments of
        # institutions to authors coming early in the list.
        c = np.arange(-A.shape[1], 0)

        # Return the result.
        return self.AssignedInstitutionNumbersByAuthor(A, b, c)

    # AuthorInstitutionsJNSAO(authorNumber)
    # returns a string such as
    #   givenname familyname\thanks{Institute, City, Country (\email{email}, \email{email})}
    # or
    #   givenname familyname\footnotemark[1]\footnoteseparator\footnotemark[2]
    # or
    #   givenname familyname\thanks{Institute, City, Country (\email{email}, \email{email})}\footnoteseparator\footnotemark[1]
    # .
    # The information which institutions the author has been assigned to present is taken from
    # AssignedInstitutionNumbersByAuthorJNSAO().
    # The \email addresses included in the \thanks command are those of all authors assigned to the particular institute whose email addresses have not been output previously.
    def AuthorInstitutionsJNSAO(self, authorNumber):

        # Get all authors' assignments of institutions to them, as well as all authors' further institutions and fellow authors (whose email addresses they present).
        (assignedInstitutionNumbersByAuthor, extraInstitutionNumbersByAuthors, assignedFellowAuthorsByAuthor) = self.AssignedInstitutionNumbersByAuthorJNSAO()
        institutionNumbersInOrderOfAppearance = self.FlattenList(assignedInstitutionNumbersByAuthor)

        # Typeset the author name.
        authorInstitutionsJNSAO = self.AuthorFullName(self.AuthorFromAuthorNumber(authorNumber))

        # First typeset the institution(s) (if any) assigned to the author (via \thanks), together with the email addresses of all assigned fellow authors.
        emailAddressesHaveBeenPresented = False
        assignedInstitutionsMarkup = []
        for (index, institutionNumber) in enumerate(assignedInstitutionNumbersByAuthor[authorNumber]):
            institutionTag = self.UniqueInstitutionTags()[institutionNumber]
            address = self.AddressFromInstitutionTag(institutionTag)
            emailsURLs = []
            if not emailAddressesHaveBeenPresented:
                for localAuthorNumber in assignedFellowAuthorsByAuthor[authorNumber]:
                    emailsURLs = emailsURLs + self.CommandWrapper(self.EnsureList(self.AuthorEMails(self.AuthorFromAuthorNumber(localAuthorNumber))), "\\email", separator = None)
                    emailsURLs = emailsURLs + self.CommandWrapper(self.EnsureList(self.AuthorURLs(self.AuthorFromAuthorNumber(localAuthorNumber))), "\\url", separator = None)
                emailsURLs = ", ".join(emailsURLs)
                if emailsURLs:
                   assignedInstitutionsMarkup.append(self.CommandWrapper(address + " (" + emailsURLs + ")", "\\thanks"))
                else:
                   assignedInstitutionsMarkup.append(self.CommandWrapper(address, "\\thanks"))
                emailAddressesHaveBeenPresented = True
            else:
                assignedInstitutionsMarkup.append(self.CommandWrapper(address, "\\thanks"))

        # Then typeset any extra institutions of the author (via \footnotemark).
        extraInstitutionsMarkup = []
        if extraInstitutionNumbersByAuthors[authorNumber]:
            extraInstitutionsMarkup.extend(["\\footnotemark[" + str(institutionNumbersInOrderOfAppearance.index(institutionNumber) + 1) + "]" for (institutionNumber, institutionNumbersInOrderOfAppearance) in zip(extraInstitutionNumbersByAuthors[authorNumber], itertools.repeat(institutionNumbersInOrderOfAppearance))])
        authorInstitutionsJNSAO = authorInstitutionsJNSAO + "%\n" + ("%\n" + self.footnoteSeparator + "%\n").join(assignedInstitutionsMarkup + extraInstitutionsMarkup)

        return authorInstitutionsJNSAO

    # AuthorsInstitutionsJNSAO()
    # returns a string composed of the output of AuthorInstitutionsJNSAO()
    # for each author.
    def AuthorsInstitutionsJNSAO(self):
        return "\n\\and\n".join((lambda self: [self.AuthorInstitutionsJNSAO(authorNumber) for authorNumber in range(len(self.ManuscriptAuthors()))])(self))

    # AuthorsSpringer()
    # returns a string such as
    #   familyname \and familyname \and familyname
    # .
    def AuthorsSpringer(self):
        return " \\and ".join([self.AuthorFullName(author) for author in self.ManuscriptAuthors()])

    # InstitutionSpringer(institutionNumber)
    # returns a string such as
    #   familyname \and familyname \at Institute, City, Country \\
    #   \email{email} \\
    #   \email{email}
    # .
    def InstitutionSpringer(self, institutionNumber, authorEMailsCovered):
        institutionTag = self.UniqueInstitutionTags()[institutionNumber]
        authors = self.AuthorsFromInstitutionTag(institutionTag)
        emails = []
        for author in authors:
            if not authorEMailsCovered[self.AuthorNumberFromAuthor(author)]:
                emails.extend(self.EnsureList(self.AuthorEMails(author)))
                authorEMailsCovered[self.AuthorNumberFromAuthor(author)] = True
        authors = " \\and ".join((lambda self: [self.AuthorFullName(author) for author in authors])(self))
        address = self.AddressFromInstitutionTag(institutionTag)
        institutionSpringer = "\n".join(filter(None, [authors + " \\at " + address + " \\\\", self.CommandWrapper(emails, "\\email", " \\\\\n")]))
        return (institutionSpringer, authorEMailsCovered)

    # InstitutionsSpringer()
    # returns a string such as
    #   familyname \and familyname \at Institute, City, Country \\
    #   \email{email} \\
    #   \email{email}
    #   \and
    #   familyname \and familyname \at Institute, City, Country \\
    #   \email{email} \\
    #   \email{email}
    # .
    def InstitutionsSpringer(self):
        authorEMailsCovered = [False for _ in range(len(self.ManuscriptAuthors()))]
        authorsInstitutions = []
        for institutionNumber in range(len(self.UniqueInstitutionTags())):
            (institutionSpringer, authorEMailsCovered) = self.InstitutionSpringer(institutionNumber, authorEMailsCovered)
            authorsInstitutions.append(institutionSpringer)
        return "\n\\and\n".join(authorsInstitutions)

    # AuthorInstitutionsM3AS()
    # returns a string such as
    #   \author{givenname familyname}
    #   \address{%
    #   Institute, City, Country \\
    #   Institute, City, Country \\
    #   \email{email}, \email{email}
    #   }
    # .
    def AuthorInstitutionsM3AS(self, authorNumber):
        authorString = self.CommandWrapper(self.AuthorFullName(self.AuthorFromAuthorNumber(authorNumber)), "\\author")
        address = " \\\\\n".join(self.AddressesFromAuthor(self.AuthorFromAuthorNumber(authorNumber)))
        emails = self.CommandWrapper(self.AuthorEMails(self.AuthorFromAuthorNumber(authorNumber)), "\\email")
        return authorString + "\n" + self.CommandWrapper(address + " \\\\\n" + emails, "\\address")

    # AuthorsInstitutionsM3AS()
    # returns a string composed of the output of AuthorInstitutionsM3AS()
    # for each author.
    def AuthorsInstitutionsM3AS(self):
        return "\n".join((lambda self: [self.AuthorInstitutionsM3AS(authorNumber) for authorNumber in range(len(self.ManuscriptAuthors()))])(self))

    # AuthorInstitutionsOJMO(authorNumber)
    # returns a string such as
    #   \author[G.-N. familyname]{\firstname{givenname} \lastname{familyname}}
    #   \address{Institute, City, Country \\
    #   Institute, City, Country}
    #   \email{email}
    #   \email{email}
    # .
    def AuthorInstitutionsOJMO(self, authorNumber):
        author = self.AuthorFromAuthorNumber(authorNumber)
        authorString = "\\author[" + self.AuthorShortName(author) + "]{\\firstname{" + self.AuthorGivenName(author) + "} " + "\\lastname{" + self.AuthorFamilyName(author) + "}}"
        address = " \\\\\n".join(self.AddressesFromAuthor(self.AuthorFromAuthorNumber(authorNumber)))
        emails = self.CommandWrapper(self.AuthorEMails(self.AuthorFromAuthorNumber(authorNumber)), "\\email")
        return authorString + "\n" + self.CommandWrapper(address, "\\address") + "\n" + emails

    # AuthorsInstitutionsOJMO()
    # returns a string composed of the output of AuthorInstitutionsOJMO()
    # for each author.
    def AuthorsInstitutionsOJMO(self):
        return "\n".join((lambda self: [self.AuthorInstitutionsOJMO(authorNumber) for authorNumber in range(len(self.ManuscriptAuthors()))])(self))

    # AuthorPAMM(authorNumber)
    # returns a string such as
    #   \author{\firstname{givenname} \lastname{familyname}\inst{1,2,}\footnote{\ElectronicMail{email}, \ElectronicMail{email}}}
    # .
    def AuthorPAMM(self, authorNumber):
        author = self.AuthorFromAuthorNumber(authorNumber)
        authorString = "\\firstname{" + self.AuthorGivenName(author) + "} " + "\\lastname{" + self.AuthorFamilyName(author) + "}"
        authorString = authorString + "\\inst{" + ",".join([str(index + 1) for index in self.InstitutionNumbersFromAuthor(author)]) + ",}"
        authorString = authorString + self.CommandWrapper(self.CommandWrapper(self.AuthorEMails(author), "\\ElectronicMail", ", "), "\\footnote")
        return self.CommandWrapper(authorString, "\\author")

    # InstitutionsPAMM()
    # returns a string such as
    #   \address[\inst{1}]{Institute, City, Country}
    #   \address[\inst{2}]{Institute, City, Country}
    # .
    def InstitutionsPAMM(self):
        return "\n".join((lambda self: ["\\address[\\inst{" + str(self.UniqueInstitutionTags().index(institutionTag) + 1) + "}]{" + self.AddressFromInstitutionTag(institutionTag) + "}" for institutionTag in self.UniqueInstitutionTags()])(self))

    # AuthorsInstitutionsPAMM()
    # returns a string composed of the output of AuthorInstitutionsPAMM() for each author, plus
    # the output of InstitutionsPAMM().
    def AuthorsInstitutionsPAMM(self):
        return "\n".join((lambda self: [self.AuthorPAMM(authorNumber) for authorNumber in range(len(self.ManuscriptAuthors()))])(self)) + "\n" + \
            self.InstitutionsPAMM()

    # AssignedInstitutionNumbersByAuthorSIAM()
    # calls AssignedInstitutionNumbersByAuthor(A, b, c) to solve an assignment problem
    # in order to determine which author 'presents' which institution(s).
    # In SIAM templates, each author can present at most one institution they are affiliated with.
    # They can be affiliated with an arbitrary number of further institutions,
    # which are presented by other authors.
    # As an example, a manuscript has 4 authors and
    #   InstitutionNumbersByAuthor == [[0,1,2,3], [1,3], [1,2], [2]].
    # Then AssignedInstitutionNumbersByAuthorSIAM() should return the lists
    #   [[0], [3], [1], [2]]        (author 0 presents institution 0; author 1 presents institution 3 and so on)
    #   [[1,2,3], [1], [1, 2], []]  (author 0 has additional institutions 1,2,3 and so on)
    #   [[0], [1], [2], [3]]        (author 0 presents email addresses for author 0 only and so on)
    def AssignedInstitutionNumbersByAuthorSIAM(self):
        # Set up the incidence matrix.
        A = self.AssignmentIncidenceMatrix()

        # Create the authors' part of the right hand side vector b reflecting how many institutions can be assigned to each author.
        # This is always one.
        b = np.ones(len(self.ManuscriptAuthors()))

        # Create the institutions' part of the right hand side vector b reflecting that each institution should not be assigned to more than one author.
        b = np.hstack((b, np.ones(len(self.UniqueInstitutionTags()))))

        # Define the cost vector, indicating that we want as many edges selected as possible, and in fact, we prefer assignments which use authors
        # coming early in the list.
        c = np.arange(-A.shape[1], 0)

        # Return the result.
        return self.AssignedInstitutionNumbersByAuthor(A, b, c)

    # AuthorInstitutionsSAIM(authorNumber)
    # returns a string such as
    #   givenname familyname
    #   \thanks{Institute, City, Country
    #   (\email{email}, \email{email}).
    #   }
    # or
    #   givenname familyname
    #   \footnotemark[2]\footnoteseparator
    #   \thanks{Institute, City, Country
    #   (\email{email}, \email{email}).
    #   }
    # .
    # The information which institution the author has been assigned to present is taken from
    # AssignedInstitutionNumbersByAuthorSIAM().
    # The \email addresses included in the \address or \secondaddress command are those of all authors assigned to the particular institute whose email addresses have not been output previously.
    def AuthorInstitutionsSIAM(self, authorNumber):

        # Get all authors' assignments of institutions to them, as well as all authors' further institutions and fellow authors (whose email addresses they present).
        (assignedInstitutionNumbersByAuthor, extraInstitutionNumbersByAuthors, assignedFellowAuthorsByAuthor) = self.AssignedInstitutionNumbersByAuthorSIAM()
        institutionNumbersInOrderOfAppearance = self.FlattenList(assignedInstitutionNumbersByAuthor)

        # Typeset the author name.
        authorInstitutionsSIAM = self.AuthorFullName(self.AuthorFromAuthorNumber(authorNumber))

        # First typeset the institution(s) (if any) assigned to the author (via \thanks), together with the email addresses of all assigned fellow authors.
        emailAddressesHaveBeenPresented = False
        assignedInstitutionsMarkup = []
        for (index, institutionNumber) in enumerate(assignedInstitutionNumbersByAuthor[authorNumber]):
            institutionTag = self.UniqueInstitutionTags()[institutionNumber]
            address = self.AddressFromInstitutionTag(institutionTag)
            emailsURLs = []
            if not emailAddressesHaveBeenPresented:
                for localAuthorNumber in assignedFellowAuthorsByAuthor[authorNumber]:
                    emailsURLs = emailsURLs + self.CommandWrapper(self.EnsureList(self.AuthorEMails(self.AuthorFromAuthorNumber(localAuthorNumber))), "\\email", separator = None)
                    emailsURLs = emailsURLs + self.CommandWrapper(self.EnsureList(self.AuthorURLs(self.AuthorFromAuthorNumber(localAuthorNumber))), "\\url", separator = None)
                emailsURLs = ", ".join(emailsURLs)
                if emailsURLs:
                   assignedInstitutionsMarkup.append(self.CommandWrapper(address + " (" + emailsURLs + ")", "\\thanks"))
                else:
                   assignedInstitutionsMarkup.append(self.CommandWrapper(address, "\\thanks"))
                emailAddressesHaveBeenPresented = True
            else:
                assignedInstitutionsMarkup.append(self.CommandWrapper(address, "\\thanks"))

        # Then typeset any extra institutions of the author (via \footnotemark).
        extraInstitutionsMarkup = []
        if extraInstitutionNumbersByAuthors[authorNumber]:
            extraInstitutionsMarkup.extend(["\\footnotemark[" + str(institutionNumbersInOrderOfAppearance.index(institutionNumber) + 2) + "]" for (institutionNumber, institutionNumbersInOrderOfAppearance) in zip(extraInstitutionNumbersByAuthors[authorNumber], itertools.repeat(institutionNumbersInOrderOfAppearance))])
        authorInstitutionsSIAM = authorInstitutionsSIAM + "%\n" + ("%\n" + self.footnoteSeparator + "%\n").join(extraInstitutionsMarkup + assignedInstitutionsMarkup)

        return authorInstitutionsSIAM

    # AuthorsInstitutionsSIAM()
    # returns a string composed of the output of AuthorInstitutionsSIAM()
    # for each author.
    def AuthorsInstitutionsSIAM(self):
        return "\n\\and\n".join((lambda self: [self.AuthorInstitutionsSIAM(authorNumber) for authorNumber in range(len(self.ManuscriptAuthors()))])(self))

    # AuthorTaylorAndFrancis()
    # returns a string such as
    #   G.-N. familyname\textsuperscript{a}\thanks{G.-N. familyname. Email: email, email}
    # .
    def AuthorTaylorAndFrancis(self, author):
        authorString = self.AuthorShortName(author)
        authorString = authorString + self.CommandWrapper(",".join([chr(index + 97) for index in self.InstitutionNumbersFromAuthor(author)]), "\\textsuperscript", "")
        if self.IsCorrespondingAuthor(author):
            authorString = authorString + self.CommandWrapper(self.AuthorShortName(author) + ". Email: " + ", ".join(self.AuthorEMails(author)), "\\thanks")
        return authorString

    # AuthorsTaylorAndFrancis()
    # returns a string such as
    #   G.-N. familyname\textsuperscript{a}\thanks{G.-N. familyname. Email: email, email},
    #   G.-N. familyname\textsuperscript{b} and
    #   G.-N. familyname\textsuperscript{a,b}
    # .
    def AuthorsTaylorAndFrancis(self):
        return self.Join([self.AuthorTaylorAndFrancis(author) for author in self.ManuscriptAuthors()], ", \n", " and \n")

    # InstitutionTaylorAndFrancis(institutionTag)
    # returns a string such as
    #   \textsuperscript{a}Institute, City, Country
    # .
    def InstitutionTaylorAndFrancis(self, institutionNumber):
        return self.CommandWrapper(chr(institutionNumber + 97), "\\textsuperscript") + \
            self.AddressFromInstitutionTag(self.UniqueInstitutionTags()[institutionNumber])

    # InstitutionsTaylorAndFrancis()
    # returns a string composed of the output of InstitutionTaylorAndFrancis()
    # for each institution.
    def InstitutionsTaylorAndFrancis(self):
        return ";\n".join((lambda self: [self.InstitutionTaylorAndFrancis(institutionNumber) for institutionNumber in range(len(self.UniqueInstitutionTags()))])(self))

    # AuthorSpringerNature(author)
    # returns a string such as
    #   \author[1,2]{givenname familyname} or
    #   \email{email}
    #   \email{email}
    #   \author*[1,2]{givenname familyname}
    #   \email{email}
    #   \email{email}
    # where [1,2] are indices into the UniqueInstitutionTags the author belongs to.
    def AuthorSpringerNature(self, author):
        if self.IsCorrespondingAuthor(author):
            return self.CommandWrapper(self.AuthorFullName(author), "\\author*[" + ",".join([str(index + 1) for index in self.InstitutionNumbersFromAuthor(author)]) + "]") + "\n" + \
                self.CommandWrapper(self.AuthorEMails(author), "\\email")
        else:
            return self.CommandWrapper(self.AuthorFullName(author), "\\author[" + ",".join([str(index + 1) for index in self.InstitutionNumbersFromAuthor(author)]) + "]") + "\n" + \
                self.CommandWrapper(self.AuthorEMails(author), "\\email")

    # InstitutionSpringerNature(institutionTag)
    # returns a string such as
    #   \affil[1]{Institute, City, Country, e-mail: email, email}
    # .
    def InstitutionSpringerNature(self, institutionTag):
        return self.CommandWrapper(self.AddressFromInstitutionTag(institutionTag), "\\affil[" + str(self.UniqueInstitutionTags().index(institutionTag) + 1) + "]")

    # AuthorsInstitutionsSpringerNature()
    # returns a string such as
    #   \author[1,2]{givenname familyname}
    #   \author[2]{givenname familyname}
    #   \affil[1]{Institute, City, Country}
    #   \affil[2]{Institute, City, Country}
    # .
    def AuthorsInstitutionsSpringerNature(self):
        return "\n".join([self.AuthorSpringerNature(author) for author in self.ManuscriptAuthors()]) + "\n" + \
            "\n".join([self.InstitutionSpringerNature(institutionTag) for institutionTag in self.UniqueInstitutionTags()])

    # AuthorInstitutionsCrelle()
    # returns a string such as
    #   \author{givenname}{familyname}{}{City}
    #   \contact{Institute, City, Country}{email, email}
    # .
    def AuthorInstitutionsCrelle(self, author):
        authorString = self.CommandWrapper(self.AuthorGivenName(author), "\\author")
        authorString = authorString + "{" + self.AuthorFamilyName(author)+ "}{}{}"
        institutionsString = " and \\\\\n".join(self.AddressesFromAuthor(author))
        institutionsString = self.CommandWrapper(institutionsString, "\\contact") + "{" + ", ".join(self.AuthorEMails(author)) + "}"
        return authorString + "\n" + institutionsString

    # AuthorsInstitutionsCrelle()
    # returns a string such as
    #   \author{givenname}{familyname}{}{City}
    #   \contact{Institute, City, Country}{email, email}
    #
    #   \author{givenname}{familyname}{}{City}
    #   \contact{Institute, City, Country}{email, email}
    # .
    def AuthorsInstitutionsCrelle(self):
        return "\n".join((lambda self: [self.AuthorInstitutionsCrelle(author) for author in self.ManuscriptAuthors()])(self))

    # AuthorBiomedCentral(author)
    # returns a string such as
    #   \author[%
    #   addressref = {0,1},
    #   corref = {0,1},
    #   email = {email, email}
    #   ]{\inits{authorTag}\fnm{givenname} \snm{familyname}}
    def AuthorBiomedCentral(self, author):
        authorString = "\\author[%\n"
        authorString = authorString + self.CommandWrapper(",".join((lambda self: [str(self.InstitutionNumberFromInstitutionTag(institutionTag)) for institutionTag in self.InstitutionTagsFromAuthor(author)])(self)), "addressref = ")
        if self.IsCorrespondingAuthor(author):
            authorString = authorString + ",\n" + self.CommandWrapper(",".join((lambda self: [str(self.InstitutionNumberFromInstitutionTag(institutionTag)) for institutionTag in self.InstitutionTagsFromAuthor(author)])(self)), "corref = ")
        authorString = authorString + ",\n" + self.CommandWrapper(", ".join(self.AuthorEMails(author)), "email = ")
        authorString = authorString + "\n]"
        authorString = authorString + "{" + self.CommandWrapper(author.get("tag"), "\\inits") + self.CommandWrapper(self.AuthorGivenName(author), "\\fnm") + " " + self.CommandWrapper(self.AuthorFamilyName(author), "\\snm") + "}"
        return authorString

    # InstitutionBiomedCentral(institutionTag)
    # returns a string such as
    #   \address[id=0]{%
    #   Institute, City, Country
    #   }
    # .
    def InstitutionBiomedCentral(self, institutionTag):
        institutionNumber = self.InstitutionNumberFromInstitutionTag(institutionTag)
        addressString = "\\address[id=" + str(institutionNumber) + "]{%\n"
        addressString = addressString + self.AddressFromInstitutionTag(institutionTag)
        addressString = addressString + "\n}"
        return addressString

    def AuthorsInstitutionsBiomedCentral(self):
        return "\n".join((lambda self: [self.AuthorBiomedCentral(author) for author in self.ManuscriptAuthors()])(self)) + "\n" + \
            "\n".join([self.InstitutionBiomedCentral(institutionTag) for institutionTag in self.UniqueInstitutionTags()])

    # AuthorEMailsAIMS()
    # returns a string such as
    #   \email{email}
    #   \email{email}
    # .
    def AuthorEMailsAIMS(self):
        return self.CommandWrapper(self.FlattenList((lambda self: [self.AuthorEMails(author) for author in self.ManuscriptAuthors()])(self)), "\\email")

    # AuthorAIMS(author)
    # returns a string such as
    #   givenname familyname
    # or
    #   givenname familyname$^*$
    # .
    def AuthorAIMS(self, author):
        authorString = self.AuthorFullName(author)
        if self.IsCorrespondingAuthor(author):
            authorString = authorString + "$^*$"
        return authorString

    # AuthorGroupAIMS(authors)
    # returns a string such as
    #   \centerline{\scshape givenname familyname$^*$ and givenname familyname}
    #   \medskip
    #   {\footnotesize
    #   \begin{center}
    #   Institute, City, Country
    #   \end{center}
    #   }
    # describing the authors' affiliations with identical institutions.
    def AuthorGroupAIMS(self, authors):
        return "\\centerline{\\scshape " + self.Join([self.AuthorAIMS(author) for author in authors], ", ", " and ") + "}\n\\medskip\n" + \
            "{\\footnotesize\n\\begin{center}\n" + " and\\\\\n".join(self.AddressesFromAuthor(authors[0])) + "\n\\end{center}\n}"

    # AuthorsInstitutionsAIMS()
    # returns a string according to AuthorGroupAIMS(), one for each group of authors appearing consecutively
    # with identical affiliations (up to order).
    def AuthorsInstitutionsAIMS(self):
        authorsInstitutionsAIMS = []
        for (institutions, authors) in itertools.groupby(self.authors, lambda author: sorted(author.get("institutions", []) or [])):
            authorsInstitutionsAIMS.append(self.AuthorGroupAIMS(list(authors)))
        return "\n\n\\medskip\n".join(authorsInstitutionsAIMS)

    # CorrespondingAuthorsAIMS()
    # returns a string such as
    #   \thanks{$^*$Corresponding author: givenname familyname, givenname familyname and givenname familyname}
    # .
    def CorrespondingAuthorsAIMS(self):
        authorString = self.Join([self.AuthorFullName(author) for author in self.CorrespondingAuthors()], ", ", " and ")
        if authorString:
            return self.CommandWrapper("$^*$Corresponding author: " + authorString, "\\thanks")
        else:
            return ""
