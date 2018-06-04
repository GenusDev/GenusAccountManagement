
PersonalAccounts = [
    {
        "Account": "BECU",
        "Debit": atof(accountData['BECU']["cash"].strip("$")) + atof(accountData['BECU']["savings"].strip("$"))

    },
    {
        "Account": "BFSFCU",
        "Credit": accountData['BFSFCU']["credit"],
        "Debit": accountData['BFSFCU']["cash"],
    },
    {
        "Account": "Venmo",
        "Debit": accountData['Venmo']["cash"]
    },
    {
        "Account": "Paypal",
        "Debit": accountData['PayPal']["cash"]
    },
    {
        "Account": "Citi",
        "Credit": accountData['Citi']["credit"]
    },
    {
        "Account": "Jacob",
        "Debit": accountData['Jacob']["cash"],
    },
    {
        "Account": "Rick",
        "Credit": accountData['Rick']["credit"],
    },
    {
        "Account": "House",
        "Debit": accountData['House']["cash"]
    },
    {
        "Account": "Consolidatedloan",
        "Credit": accountData['Consolidatedloan']["credit"]
    },
    {
        "Account": "NewGradPlusLoan",
        "Credit": accountData['NewGradPlusLoan']["credit"]
    },

]
