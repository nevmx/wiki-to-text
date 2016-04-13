import mechanicalsoup
import sys 

class WikiPage:
    def __init__(self, title):
        self.title = title
        self.sections = []

    def getText(self):
        '''Print out the wiki page, formatted for console output.'''

        # First, the page title is printed
        wikiPageText = "          ---= "
        wikiPageText += self.title + ' =---\n'

        # Then, the description (sections[0]) is printed
        wikiPageText += '\n\n'
        wikiPageText += self.sections[0].getText()
        return wikiPageText

    def addSection(self, title, text):
        self.sections.append(Section(title, text))
        return

class Section:
    def __init__(self, title, text):
        self.title = title
        self.text = text

    def getText(self):
        '''Generate the text for this section'''

        # First, insert the title and then the text
        sectionText = "+ " + self.title + " +\n"
        sectionText += self.text
        return sectionText

# Instantiate the browser
browser = mechanicalsoup.Browser()

# Get the wiki page
page = browser.get('http://en.wikipedia.org/wiki/' + sys.argv[1]);

# Get the tile and instantiate WikiPage
page_title = page.soup.select('.firstHeading')[0].get_text()
wikipage = WikiPage(page_title)

# Get the first section (description that's not in any particular
# section).
page_description = page.soup.select('p')[0]

# Remove superscript tags and their contents
[s.extract() for s in page_description('sup')]
page_description = page_description.get_text()

wikipage.addSection('Description', page_description)

# Get the table of contents
toc = page.soup.select('div #toc')[0].get_text()

print wikipage.getText()
