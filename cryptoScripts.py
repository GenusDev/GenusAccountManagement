import os, random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import json
import ast

chunkSize = 64*1024

def getKey(password):
    encodedKey = password.encode('utf-8')
    hash = SHA256.new(encodedKey)
    return hash.digest()

def pad(s): #AES only takes blocks of 16 bits
    return s + ((16-len(s)%16)*'{')

def encryptFile(key, fileName):
    localKey = getKey(key)
    cipher = AES.new(localKey)
    outputFile = "(encrypted)" + fileName
    fileSize = str(os.path.getsize(fileName)).zfill(16) # make sure there are 16 digits - as this will be printed
    
    with open(fileName,"rb") as inFile:
        with open(outputFile, "wb") as outFile:
            outFile.write(fileSize.encode('utf-8'))

            while True:
                chunk = inFile.read(chunkSize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16-(len(chunk)%16)) #padding

                outFile.write(cipher.encrypt(chunk))

#encryptFile("go5Ity", "AccountData.json")                
                
def encryptJson(key, json, fileName):
    localKey = getKey(key)
    cipher = AES.new(localKey)
    outputFile = "(encrypted)" + fileName
    fileSize = str(os.path.getsize(fileName)).zfill(16) # make sure there are 16 digits - as this will be printed
    jsonBites = str(json).encode('utf-8')
  
    with open(outputFile, "wb") as outFile:
        outFile.write(fileSize.encode('utf-8'))

        if len(jsonBites) % 16 != 0:
            jsonBites += b' ' * (16-(len(jsonBites)%16)) #padding

        outFile.write(cipher.encrypt(jsonBites))

#encryptJson("go5Ity",AI,"AccountData.json")
    
def encryptText(plaintext):
    global cipher #pulls in global variable
    return cipher.encrypt(pad(plaintext))

def decryptText(ciphertext):
    global cipher
    dec = cipher.decrypt(ciphertext).decode('utf-8')
    l = dec.count('{')
    return dec[:len(dec)-l]

def decryptFileasJson(key, fileName):
    localKey = getKey(key)
    cipher = AES.new(localKey)
    
    with open(fileName, 'rb') as inFile:
        fileSize = int(inFile.read(16))
        outData = {}
        while True:
            chunk = inFile.read(chunkSize)
            if len(chunk) == 0:
                break
            outData = cipher.decrypt(chunk).decode('utf-8')
        #print(outData)
        try:
            json_data = ast.literal_eval(outData)
        except:
            json_data = json.loads(outData)
        return json_data 

def decryptFile(key, fileName):
    localKey = getKey(key)
    cipher = AES.new(localKey)
    
    outputFile = fileName[11:] + "(Decrypted)"
    
    with open(fileName, 'rb') as inFile:
        fileSize = int(inFile.read(16))
       
        with open(outputFile,'wb') as outFile:
            while True:
                chunk = inFile.read(chunkSize)
                if len(chunk) == 0:
                    break
                
                outFile.write(cipher.decrypt(chunk))
            
            outFile.truncate(fileSize)  

#decryptFile("go5Ity","(encrypted)AccountData.json")

def Main():
    choice = input("Would you like to (E)ncrypt? or (D)ecrypt : ")
    
    if choice == 'E':        
        fileName = input("File to encrypt? :")
        code = input("code? :")
        encryptFile(code,fileName)
        print("done")
    if choice == 'D':
        fileName = input("File to decrypt? :")
        code = input("code? :")
        decryptFile(code,fileName)
        print("done")
    else:
        print("No option selected, closing")

if __name__ == '__main__':
    Main()

#set it up so it decrypts a file
#allow it to pass through as an decryption process only as bits, with no writing. 
# set it up so you can to batches of text as needed
# only works with json files #go5Ity
#Manage permissions based on code inputted - business vs personal
# go5Ity