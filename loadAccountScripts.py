import UpdateHoldingCo
import GetAccountData
from AccountData import AllAccountInfo # potentially have inputted at a later stage

def loadAccountScripts():
    accountData = GetAccountData.compileAllData(AllAccountInfo)
    
    updateClass = UpdateHoldingCo.updateAccounts(accountData)
    updateClass.execute()
    
    return accountData


loadAccountScripts()


# create python function in terminal that takes two inputs as account info and interested info, and outputs the password or info, and copies it to the pasteboard. It should be able to do partial searchs, it will copy the first match for both. 
# download bank statements into a folder where available 
# write to personal google sheet
# open and update time tracker with date/time and the text inputed in the notes section. 
    # start small with a starter script and build on it later
# then jump into building trading algorythms