
### @Author = Aashish
# This is a Code to test scrap methodology from guardian website to print out 100 best books into excel sheet
'''
1. Use of Beutiful Soup 4 to extract the html data and extract tags of following URLs
   "https://www.theguardian.com/books/series/100-best-nonfiction-books-of-all-time?page=2"
2. Use of xlwt module for excel functions
3. List of dictionaries is exported to Excel sheet. Excel file will be located in Current Directory
'''
###############################################


from bs4 import BeautifulSoup
from urllib.request import urlopen
import collections
import xlwt
import re
import string
import sys


html1 = urlopen("https://www.theguardian.com/books/series/100-best-nonfiction-books-of-all-time?page=1")
html2 = urlopen("https://www.theguardian.com/books/series/100-best-nonfiction-books-of-all-time?page=2")

bs4 = BeautifulSoup(html1, 'html.parser')


"""
re.match() vs re.search()
re.match() checks for a match only at the beginning of the string, while re.search() checks for a match anywhere in the string.
"""

"""
regex = r"([a-zA-Z]+) (\d+)"
if re.search(regex, "June 24"):
    match = re.search(regex, "June 24")

    # This will print [0, 7), since it matches at the beginning and end of the
    # string
    print("Match at index %s, %s" % (match.start(), match.end()))
    print("Full match: %s" % (match.group(0)))
    print("Month: %s" % (match.group(0)))
    print("Day: %s" % (match.group(0)))
"""

"""
# RESULT
Match at index 0, 7
Full match: June 24
Month: June 24
Day: June 24
"""

"""
# WORKS WRITING TO EXCEL
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")
#sheetn.write(row, column, "content")

sheet1.write(0, 0, "Display")
sheet1.write(1, 0, "Dominance")
sheet1.write(2, 0, "Test")
book.save("trials.xls")
"""

"""
# ORIGINAL CONTENT EXCERPT
<div class="fc-item__content">
  <div class="fc-item__header">
    <h1 class="fc-item__title"><a href="https://www.theguardian.com/books/2016/apr/25/female-eunuch-germaine-greer-100-best-nonfiction-books" class="fc-item__link" data-link-name="article"> <span class="u-faux-block-link__cta fc-item__headline"> <span class="js-headline-text">The 100 best nonfiction books: No 13 – The Female Eunuch by Germaine Greer (1970)</span></span> </a></h1>
    <!-- last part of h1 - <span class="js-headline-text">The 100 best nonfiction books: No 13 – The Female Eunuch by Germaine Greer (1970)</span></span> </a></h1> --!>
  </div>
  <div class="fc-item__standfirst">
  The Australian feminist’s famous polemic, if a little outdated, remains a masterpiece of passionate free expression
  <br>
  </div>
  <aside class="fc-item__meta js-item__meta">
</div>
"""

"""
#PRINT TAG WORKS
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, 'html.parser')
a_tag = soup.a
print(a_tag)
"""


"""
#DOESNT WORK
h1_tag = div_tag.find("h1", {'class': "fc-item__title"}) #works
a_tag = h1_tag.find('a')  #doesnt work

# COMMAND ERROR - h1 tag doesn't have 'a' attribute
"""

# Source: http://stackoverflow.com/questions/14630288/unicodeencodeerror-charmap-codec-cant-encode-character-maps-to-undefined
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

uprint('foo')
uprint('Antonín Dvořák')
uprint('foo', 'bar', u'Antonín Dvořák')




# Useful:

#didnt work
#book_tags = bs4.findAll('div', {'class': 'fc-item__content'})

index = 1
main_divs = bs4.find_all("div", {'class': 'fc-item__content'})

#book_dict keys are rank, title, link, desc

book_list = []
for tag in main_divs:
    # for book title
    div_tag = tag.find("div", {'class': 'fc-item__header'})
    h1_tag = div_tag.find("h1", {'class': "fc-item__title"})
    print("\n\n")
    title_tag = div_tag.find('span', {'class': "js-headline-text"})
    title = title_tag.get_text()
    regex = r"The 100 best nonfiction books: No (\d+)"
    print("\n\n Printing \n")
    print("Print title content ")
    uprint(title)
    print("\n Print regex" + str(regex))
    if re.search(regex, title):
        print("\n matched \n")
        match = re.search(regex, title)
        remove_str = match.group(0)
        print("\n Remove string is ")
        uprint(remove_str)
        book_rank = match.group(1)

    title_flt = title.replace(remove_str, "")
    #title_flt = title[39:len(title)]

    #print(title_flt)


    #for href links
    div_tag = tag.find("div", {'class': 'fc-item__header'})
    h1_tag = div_tag.find("h1", {'class': "fc-item__title"})
    print("\n")
    a_tag = div_tag.find('a', href=True)
    #print(a_tag['href'])

    # for book desc
    div_tag = tag.find("div", {'class': "fc-item__standfirst"})
    desc_text = div_tag.get_text()
    print("\n desc below \n")
    uprint(desc_text)


    book_dict = {'rank': book_rank, 'title': title_flt, 'link': a_tag['href'], 'desc': desc_text}
    book_list.append(book_dict)
    index += 1

print("\n\n Printing whole list of Book dictionaries \n\n")
#print(book_list)

#ordered_book_list = collections.OrderedDict(book_list)

book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")
for row_index, book_dict in enumerate(book_list):
    for column_index, book_content in enumerate(collections.OrderedDict(book_dict)):
        #For title Row
        if row_index == 0:
            sheet1.write(0, column_index, list(book_list[row_index].keys())[column_index])
        sheet1.write(row_index+1, column_index, book_list[row_index][book_content])
book.save("trials2.xls")

"""
ISSUE: while printing book contents, the order is hapazard
SOLUTION:
#Dictionaries are not required to keep order. Use OrderedDict.
import collections
cars_dict = [('Civic86', 12.5),
                   ('Camry98', 13.2),
                   ('Sentra98', 13.8)]
smallestCars = collections.OrderedDict(cars_dict)
for car in smallestCars:
    print(car)
"""



"""
for link in bsObj.findAll(""a""):
    if 'href' in link.attrs:
        print(link.attrs['href'])"
"""
