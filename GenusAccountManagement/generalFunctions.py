import os

def makeRelativePath(Path):
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    abs_file_path = os.path.join(script_dir, Path)
    return abs_file_path

def loadOldAccountData(date):
    fileRead = open(makeRelativePath('AccountDataPickles/{}accountData.pickle'.format(date)), 'rb')
    accountData = pickle.load(fileRead)
    return accountData
