#
def loadPersonalAccounts():

    sheetInfo = {
        "account": "MSteele",
        "spreadsheetId": "10o-H7l5u0BvazIs4g3Fy4NpJcb8d4X6n7vFBVs0pKCc",
        "worksheets" : [
            "Statements",
            "Valuation"
        ],
        "structure": {
            "credit": "Credit",
            "invested" : "Debit",
            "debit" : "Debit",
            "cash" : "Debit",
            "savings": "Debit"
        }
    }

    return sheetInfo

    #
    # Accounts = [
    #     {
    #         "Account": "BECU",
    #         "Debit": accountData['BECU']["cash"].strip("$")
    #
    #     },
    #     {
    #         "Account": "BFSFCU",
    #         "Credit": accountData['BFSFCU']["credit"],
    #         "Debit": accountData['BFSFCU']["cash"],
    #     },
    #     {
    #         "Account": "Venmo",
    #         "Debit": accountData['Venmo']["cash"]
    #     },
    #     {
    #         "Account": "Paypal",
    #         "Debit": accountData['PayPal']["cash"]
    #     },
    #     {
    #         "Account": "Citi",
    #         "Credit": accountData['Citi']["credit"]
    #     },
    #     {
    #         "Account": "Jacob",
    #         "Debit": accountData['Jacob']["cash"],
    #     },
    #     {
    #         "Account": "Rick",
    #         "Credit": accountData['Rick']["credit"],
    #     },
    #     {
    #         "Account": "House",
    #         "Debit": accountData['House']["cash"]
    #     },
    #     {
    #         "Account": "Consolidatedloan",
    #         "Credit": accountData['Consolidatedloan']["credit"]
    #     },
    #     {
    #         "Account": "NewGradPlusLoan",
    #         "Credit": accountData['NewGradPlusLoan']["credit"]
    #     },
    # ]
