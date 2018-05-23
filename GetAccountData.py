import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import datetime
import pickle


def RDataPull(BankInfo):
    from Robinhood import Robinhood

    Account = BankInfo["Usr"]
    PWord = BankInfo["Pass"]
    trader = Robinhood()
    trader.login(username=Account, password=PWord)
    cash = trader.get_account()['cash']
    equity = trader.equity()
    invested = float(equity) - float(cash)

    dsecowned = trader.securities_owned()['results']
    RData = {
        "cash": cash,
        "invested": invested
    }
    positions = {}

    for position in dsecowned:
        id = position['instrument'].split('/')[4]
        if float(position['quantity']) > 0 :
            positions[trader.instrument(id)['symbol']] = position['quantity']

    RData["positions"] = positions
    
    return RData
        
def CitiAccountGrab(BankInfo):   

    acctData = {}

    def logIn(driver):
        login_url = BankInfo["LogInURL"]
        driver.get(login_url)
        info_url = BankInfo["dataGrabURL"]
        x = 12
        while x < 20:
            time.sleep(x)
            if "login" in driver.current_url:
                x = 3 
            elif "ain" in driver.current_url:
                x = 20
#                 driver.get(info_url)
                grabData(driver)
            else:
                x + 2

    def grabData(driver):
        cashData = driver.find_element_by_xpath(BankInfo["XPathBalance"])
        acctData['credit'] = cashData.text
        driver.quit()
        return acctData
    
    def execute():
        options = webdriver.ChromeOptions()
        #options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)   
        logIn(driver)

    execute()
    
    return acctData

def AccountGrab(BankInfo):   

    AccountSpecificData = {}

    def logIn(driver,BankInfo):
        driver.get(BankInfo["LogInURL"])
        
        try:
            UserNm = driver.find_element_by_name(BankInfo["UsrInputByName"])
            Pass = driver.find_element_by_name(BankInfo["PassInputByName"])
        except:
            UserNm = driver.find_element_by_id(BankInfo["UsrInputById"])
            Pass = driver.find_element_by_id(BankInfo["PassInputById"])
        
        
        try:
            UserNm.send_keys(BankInfo["Usr"])
            Pass.send_keys(BankInfo["Pass"])
            Pass.send_keys(Keys.RETURN)
        except:
            UserNm.send_keys(Keys.RETURN)
            time.sleep(2)
            Pass.send_keys(BankInfo["Pass"])
            Pass.send_keys(Keys.RETURN)
            
        
        time.sleep(1)    

        if BankInfo["ChallengeHomeKeyWord"] not in driver.current_url:
            try:
                #Text grab
                if "ChallengeTextByClass" in BankInfo.keys():
                    ChallengeText = driver.find_element_by_class_name(BankInfo["ChallengeTextByClass"])
                elif "ChallengeTextByName" in BankInfo.keys():
                    ChallengeText = driver.find_element_by_name(BankInfo["ChallengeTextByClass"])
                #Answer grab
                if "ChallengeAnwsByClass" in BankInfo.keys() :
                    ChallengeAnsw = driver.find_element_by_class_name(BankInfo["ChallengeAnwsByClass"])
                elif "ChallengeAnwsByName" in BankInfo.keys():
                    ChallengeAnsw = driver.find_element_by_name(BankInfo["ChallengeAnwsByName"])

                for key, value in BankInfo["challengInput"].items():
                    if key in ChallengeText.text:
                        ChallengeAnsw.send_keys(value)
                ChallengeAnsw.send_keys(Keys.RETURN)
            except Exception as e:
                print("Challenge link not Found : {}".format(e))
                
                #venmo specific bank verify 
                try:
                    time.sleep(3)
                    print("working")
                    bankShift = driver.find_element_by_class_name("link")
                    bankShift.click()
                    time.sleep(3)

                    accountInfo = driver.find_element_by_name("bankAccountNumber")
                    accountInfo.send_keys(BankInfo["AccountVerify"])
                    accountInfo.send_keys(Keys.RETURN)

                    time.sleep(3)

                    if driver.current_url == "https://venmo.com/account/mfa/remember-device":         
                        DontRemember = driver.find_element_by_class_name("ladda-button")
                        DontRemember.click()  
                except:
                    pass

    def getData(driver,BankInfo):
        if "dataGrabURL" in BankInfo.keys():
            driver.get(BankInfo["dataGrabURL"]) 
        time.sleep(3)
        if "XPathManyBalances" in BankInfo.keys():
            siteData = driver.find_elements_by_xpath(BankInfo["XPathManyBalances"])
            try:
                AccountSpecificData['invested'] = siteData[BankInfo["BalanceElementNum"]['invested']].text
            except:
                pass
            try:
                AccountSpecificData['cash'] = siteData[BankInfo["BalanceElementNum"]['cash']].text
            except:
                pass
            try:
                AccountSpecificData['bonds'] = siteData[BankInfo["BalanceElementNum"]['bonds']].text
            except:
                pass
            try:
                AccountSpecificData['savings'] = siteData[BankInfo["BalanceElementNum"]['savings']].text
            except:
                pass
            try:
                AccountSpecificData['credit'] = siteData[BankInfo["BalanceElementNum"]['credit']].text
            except:
                pass
            
        if "BalanceByClass" in BankInfo.keys():
            balance = driver.find_element_by_class_name(BankInfo["BalanceByClass"])           
            AccountSpecificData['cash'] = balance.text

        if "BalanceById" in BankInfo.keys():
            balance = driver.find_element_by_id(BankInfo["BalanceById"])
            AccountSpecificData['cash'] = balance.text 
        
        if "XPathManyPositions" in BankInfo.keys():
            positions = {}
            SymboldData = driver.find_elements_by_xpath(BankInfo['XPathManyPositions'])

            for each in SymboldData:
                dataJson = json.loads(each.get_attribute("data-trade-action"))
                positions[dataJson['symbol']] = dataJson['quantity']
        
            AccountSpecificData['positions'] = positions
            
        driver.quit()
        return AccountSpecificData


    def execute(BankInfo):
        options = webdriver.ChromeOptions()
#       options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
    
        logIn(driver,BankInfo)
        time.sleep(1)
        return getData(driver,BankInfo)
    
    execute(BankInfo)
    return AccountSpecificData

def removeText(accountData):
    #print(accountData)
    for each in accountData:
        #print(accountData[each])
        try:
            if len(accountData[each]['cash'].split(" "))>3:
                accountData[each]['cash'] = 0
        except:
            pass
        try:
            if len(accountData[each]['credit'].split(" "))>3:
                accountData[each]['credit'] = 0
        except:
            pass
        
    return accountData

def compileAllData(AllAccountInfo):
    accountData = {}
    accountData['Citi'] = CitiAccountGrab(AllAccountInfo["Citi"])
    accountData['PayPal'] = AccountGrab(AllAccountInfo["PayPal"])
    accountData['TDClub'] = AccountGrab(AllAccountInfo["TDClub"])
    accountData['TDMattIRA'] = AccountGrab(AllAccountInfo["TDMattIRA"])
    accountData['TDJohnIRA'] = AllAccountInfo["TDJohnIRA"]
    accountData['Venmo'] = AccountGrab(AllAccountInfo["Venmo"])
    accountData['BECU'] = AccountGrab(AllAccountInfo["BECU"])
    accountData['BFSFCU'] = AccountGrab(AllAccountInfo["BFSFCU"])
    accountData['Robinhood'] = RDataPull(AllAccountInfo["Robinhood"])
    accountData['Rick'] = AllAccountInfo["Rick"]
    accountData['Jacob'] = AllAccountInfo["Jacob"]
    accountData['Consolidatedloan'] = AllAccountInfo["Consolidatedloan"]
    accountData['NewGradPlusLoan'] = AllAccountInfo["NewGradPlusLoan"]
    accountData['House'] = AllAccountInfo["House"]

    date = datetime.date.today().strftime('%Y%m%d')
    fileWrite = open('/Users/matthewsteele 1/Google Drive/Projects - /HoldingCompany/StockAnalysis/AccountManagementScript/AccountDataPickles/{}accountData.pickle'.format(date), 'wb')
    pickle.dump(accountData, fileWrite)
    fileWrite.close()
    
    accountData = removeText(accountData)
    
    return accountData
