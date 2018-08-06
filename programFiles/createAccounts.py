

print("Will initialize account creation")

firstLetter = input("What is the first letter of your first name? ")

lastName = input("What is your last name? ")


accountName = firstLetter + lastName
print("your account name will be " + accountName)

accountData = {
    "$Endogen": {
        "Usr": accountName
    }
}
print(accountData)
# input to ask
