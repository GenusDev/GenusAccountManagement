#from AccountData import AllAccountInfo as AI
import os
from selenium import webdriver
from cryptoScripts import decryptFileasJson, encryptJson
import ast

def copy(data):
    print(data + " copied")
    os.system("echo '%s' | pbcopy" % data)

def runLookup(AI):
    lowerKeysAI =  {k.lower(): v for k, v in AI.items()}
    inputedText = input("Account? -c to list commands : ").lower().replace(" ","")
    commands = {
        "-a" : "list all accounts",
        "-c" : "list all commands",
        "nameOfAccount,-command" : ["account specific commands", 
                                    {
                                        "-a": "list all account specific info",
                                        "-u": "list username",
                                        "-h" : "get home URL",
                                        "-c" : "challenge questions",
                                        "-e" : "escape",
                                        "add" : "add or modify a new account"
                                    }]

    }
    
    def shortLookUp(inputedText,accountFactor):
        if inputedText in lowerKeysAI:
            if accountFactor != "all":
                copy(lowerKeysAI[inputedText][accountFactor])
                return lowerKeysAI[inputedText][accountFactor]
            elif accountFactor == "all":
                copy(lowerKeysAI[inputedText])
        else:
            for each in lowerKeysAI.keys():
                if inputedText in each:
                    correctAccountQuestion = input(each+" ? y/n")
                    if correctAccountQuestion == "y":
                        correctAccount = each
                        if accountFactor != "all":
                            copy(lowerKeysAI[correctAccount][accountFactor])
                            return lowerKeysAI[correctAccount][accountFactor]
                        elif accountFactor == "all":
                            copy(lowerKeysAI[correctAccount])
                            break              
                    elif correctAccountQuestion == "n":
                        pass     

    if "-a" in inputedText:
        for each in AI:
            print (each)
        runLookup(AI)

    if "-c" in inputedText:
        print (commands)
        runLookup(AI)

        
    elif inputedText in lowerKeysAI:
        copy(lowerKeysAI[inputedText]["Pass"])

    elif inputedText not in lowerKeysAI.keys():
        shortLookUp(inputedText,"Pass")


    if "," in inputedText:
        x,y = inputedText.split(",")
        if "-a" in y:
            shortLookUp(x,"all")
        elif "-u" in y:
            shortLookUp(x,"Usr")
        elif "-c" in y:
            shortLookUp(x,"challengInput")
        elif "-h" in y:
            url = shortLookUp(x,"LogInURL")
            driver = webdriver.Chrome()
            driver.get(url)
    if "-e" in inputedText:
        print("bye Felicia")
    
    if "add" in inputedText:
        newAccountName = input("account name?: ")
        keyInputed = input("key?: ")
        valueInputed = input("value?: ")
    # print(type(newInfo))
        try:
            currentData = ast.literal_eval(AI[newAccountName])
            currentData.update({keyInputed:valueInputed})
            AI[newAccountName] = currentData
        except:
            AI[newAccountName] = {keyInputed:valueInputed}
        encryptJson("go5Ity",AI,"AccountData.json")
        runLookup(AI)
        
def Main():
    input("Account Key?").replace(" ","") 
    try:
        AI = decryptFileasJson(key,"(encrypted)AccountData.json")        
    except:
        tryAgain = input("nope - you are likely less wrong than you are sloppy - Try the code again? (y/n)")
        if 'y' in tryAgain:
            Main()
        if 'n' in tryAgain:
            print("okay, bye Felicia")
    else:
        runLookup(AI)

if __name__ == '__main__':
    Main()


# try to run script on one line in terminal 
# get accountinfo look up working with encrypted file
# Take out all critical files and put them in a sub folder and shift to a github repot with encrypted file, and remove all sensitive material, and save main copy on desktop and out of the cloud, as well as key.  
# figure out how to shift everything to a github account such that when downloaded everything works, after installing the dependencies
