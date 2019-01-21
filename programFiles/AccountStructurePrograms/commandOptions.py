commands = {
    "-a" : "list all accounts",
    "-c" : "list all commands",
    "-e" : "escape",
    "-updateAcc": "will update all accounts - be sure to put in account info as needed",
    "add" : "add a new account and/or data point",
    "del" : "remove a new account and/or data point",
    "loadAccountData": "Loads old account data based on date",
    "+": "commands are chained with +",
    "nameOfAccount +command" : ["account specific commands",
                                {
                                    "+i": "list all account specific info",
                                    "+Key": "look for specific data by key",
                                    "+u": "list us*rn*me",
                                    "+p": "list p*ssw*rd (password is default output if no command provided)",
                                }]

}
