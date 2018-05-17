#Patrick Du
#This program uses Edgar's Search page as base page for all the below code.
#It take's a CIK/ ticker, navigates to the most relevant 13F form,
#navigates to the relevant XML file, parses said file and returns another file
#with the content of the XML file tab delimited
import requests
from bs4 import BeautifulSoup

userCIK=input('Enter CIK/ ticker :')
url='https://www.sec.gov/cgi-bin/browse-edgar?CIK=%s&Find=Search&owner=exclude&action=getcompany'
userReqURL='https://www.sec.gov/cgi-bin/browse-edgar?CIK=%s&Find=Search&owner=exclude&action=getcompany' % userCIK
page=requests.get(userReqURL)
edgarPage=page.content
soup=BeautifulSoup(edgarPage,'lxml')
result_table=soup.find('table', summary='Results')
urlExtension=[i.find('a')['href'] for i in soup.find_all('tr') for j in i.find_all('td') for k in j if '13F' in k]
#looking for all extensions to the next webpage via finding 13F form 
fullURL=['https://www.sec.gov%s' % u for u in urlExtension]
indexPage=requests.get(fullURL[0])#get the most up to date one
edgarDocumentPage=indexPage.content
soup1=BeautifulSoup(edgarDocumentPage,'lxml')
docFileExtensions=[i.find_next('a')['href'] for i in soup1.find_all('tr')]
urlLinks=['https://www.sec.gov%s' % extension for extension in docFileExtensions]
urlLink=urlLinks[-2]
#Looking through the Edgar page I found that the info table xml file
#is consistently the second to last 
xmlFile=urlLink[urlLink.rfind('/')+1:]

response=requests.get(urlLink)
with open(xmlFile,'wb') as file:
    file.write(response.content)
soup2=BeautifulSoup(open(xmlFile),'lxml')

outfile=open('infoTableFile','w')
for info in soup2.find_all('infotable'):
    if info.name is not None:
        for data in info.stripped_strings:
             outfile.write(data +'\t')
        outfile.write('\n')
outfile.close()
infile=open('infoTableFile','r')
print(infile.read())
infile.close()
