HoldingCoAccounts = [
    {
        "Account": "Robinhood",
        "Invested": accountData['Robinhood']["invested"],
        "Cash": accountData['Robinhood']["cash"]
    },
    {
        "Account": "TD Club",
        "Invested": atof(accountData['TDClub']["invested"].strip("$")) + atof(accountData['TDClub']["bonds"].strip("$")),
        "Cash": float(atof(accountData['TDClub']["cash"].strip("$")))
    },
    {
        "Account": "TD Matt's IRA",
        "Invested": atof(accountData['TDMattIRA']["invested"].strip("$")) + atof(accountData['TDClub']["bonds"].strip("$")),
        "Cash": float(atof(accountData['TDMattIRA']["cash"].strip("$"))) #MIRA
    },
    {
        "Account": "CoinBase",
        "Invested": accountData['Robinhood']["invested"],
        "Cash": accountData['Robinhood']["cash"]
    },
    {
        "Account": "TD John's IRA",
        "Invested": 0,
        "Cash": 5500
    },
]
