from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import json
from AccountStructurePrograms import loadAccountDataFiles
from pprint import pprint
from generalFunctions import makeRelativePath

chunkSize = 64*1024


def getKey(password):
    encodedKey = password.encode('utf-8')
    hash = SHA256.new(encodedKey)
    return hash.digest()


def pad(s):  # AES only takes blocks of 16 bits
    return s + ((16-len(s) % 16)*'{')


def encryptFile(key, inFileName):
    localKey = getKey(key)
    cipher = AES.new(localKey, 1)

    outputFile = inFileName.replace("decrypted", "encrypted")

    outputFileFullPath = makeRelativePath('AccountDataEncryption/{fileName}'.format(fileName=outputFile))
    inFileFullPath = makeRelativePath("AccountDataEncryption/"+inFileName)

    # fileSize = str(os.path.getsize(inFileFullPath)).zfill(16) # make sure there are 16 digits - as this will be printed

    with open(inFileFullPath,"rb") as inFile:
        with open(outputFileFullPath, "wb") as outFile:
            # outFile.write(fileSize.encode('utf-8'))

            while True:
                print("this is working!")
                chunk = inFile.read(chunkSize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16-(len(chunk) % 16))  # padding
                print(chunk)
                outFile.write(cipher.encrypt(chunk))


def encryptJson(key, AccountDataDict, OutFileName):  # needs fixing
    localKey = getKey(key)
    cipher = AES.new(localKey, 1)
    jsonString = json.dumps(AccountDataDict)

    outputFileName = makeRelativePath("AccountDataEncryption/"+OutFileName)
    jsonBites = str(jsonString).encode()

    with open(outputFileName, "wb") as outFile:
        print(outputFileName)
        if len(jsonBites) % 16 != 0:
            jsonBites += b' ' * (16-(len(jsonBites) % 16))  # padding
        outFile.write(cipher.encrypt(jsonBites))


def encryptText(plaintext):
    global cipher  # pulls in global variable
    return cipher.encrypt(pad(plaintext))


def decryptText(ciphertext):
    global cipher
    dec = cipher.decrypt(ciphertext).decode('utf-8')
    l = dec.count('{')
    return dec[:len(dec)-l]


def decryptFileasJson(key, fileName):

    localKey = getKey(key)
    cipher = AES.new(localKey,1)

    InFilePath = makeRelativePath('AccountDataEncryption/{fileName}'.format(fileName=fileName))

    with open(InFilePath, 'rb') as inFile:
        chunk = inFile.read(chunkSize)    #won't work for data larger than chunksize - check with
        outData = cipher.decrypt(chunk)
        #json_data = ast.literal_eval(outData)
        json_data = json.loads(outData)
        return json_data


def decryptFile(key, fileName):
    localKey = getKey(key)
    cipher = AES.new(localKey, 1)

    outputFile = fileName.replace("encrypted", "decrypted")

    outputFile = makeRelativePath('AccountDataEncryption/{fileName}'.format(fileName=outputFile))
    print(outputFile)
    fileName = makeRelativePath('AccountDataEncryption/{fileName}'.format(fileName=fileName))
    print(fileName)
    with open(fileName, 'rb') as inFile:
        # fileSize = int(inFile.read(16))

        with open(outputFile, 'wb') as outFile:
            while True:
                chunk = inFile.read(chunkSize)
                if len(chunk) == 0:
                    break

                outFile.write(cipher.decrypt(chunk))

            # outFile.truncate(fileSize)


def Main():
    choice = input("Would you like to (E)ncrypt? or (D)ecrypt : ")

    if choice == 'E':
        options = loadAccountDataFiles.loadAccountDataFiles()
        for eachOption in options:
            options[eachOption] = options[eachOption].replace("encrypted", "decrypted")
        pprint(options)
        fileName = input("File to decrypt? :")
        if len(fileName) < 2:
            fileName = options[fileName]

        code = input("code? :")
        encryptFile(code, fileName)
        print("done")

    if choice == 'D':
        options = loadAccountDataFiles.loadAccountDataFiles()
        pprint(options)
        fileName = input("File to Encrypt? :")
        if len(fileName) < 2:
            fileName = options[fileName]

        code = input("code? :")

        decryptFile(code, fileName)
        print("done")
    else:
        print("No option selected, closing")

if __name__  ==  '__main__':
    Main()

# set it up so it decrypts a file
# allow it to pass through as an decryption process only as bits, with no writing.
# set it up so you can to batches of text as needed
# Manage permissions based on code inputted - business vs personal
