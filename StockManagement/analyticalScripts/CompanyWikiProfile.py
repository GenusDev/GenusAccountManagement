import wikipedia
from bs4 import BeautifulSoup


class CompanyWikiProfile:

    def __init__(self,companyName):
        self.name = companyName
        self.wikiProfileInfo = self.searchAndFind(companyName).infoBoxData

    def searchAndFind(self,name):
        searchResults = wikipedia.search(name)

        for eachResult in searchResults:
            eachResultsWikiData = self.wikiData(eachResult)
            eachResultsWikiData.pullPageData()
            if eachResultsWikiData.hasCompanyData():
                return eachResultsWikiData
                break
            else:
                pass

    class wikiData(object):
        def __init__(self, search):
            print(search)
            searchPage = wikipedia.page(search)
            print(searchPage.title)
            html = searchPage.html()
            self.soup = BeautifulSoup(html)

        def pullPageData(self):
            InfoTable = self.soup.find(class_='infobox')
            allRows = InfoTable.find_all('tr')
            infoBoxData = {}
            self.test = "Testing"
            for eachRow in allRows:
                try:
                    label = str(eachRow.th.text).replace('\n', '')
                    info = str(eachRow.td.text).replace('\n', '')
                    infoBoxData[label] = info
                except:
                    pass
            print(infoBoxData)
            self.infoBoxData = infoBoxData


        def hasCompanyData(self):
            textToSearchFor = ['Founded','Industry',"Traded as"]
            for each in textToSearchFor:
                if each in self.infoBoxData.keys():
                    return True
                    break
            else:
                return False


        def grabRelevantData():
            test = self.soup


# Merge Dataframes
# Convert data early on into useful data
