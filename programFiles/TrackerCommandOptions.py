TrackerCommands = {
    "t" : "list tasks being logged",
    "c" : "list all commands",
    "e" : "escape and log",
    "l": "log new task",
    "_": "log args are chained with spaces",
    "l args..." : ["log options",
                                {
                                    "tasks": "list all current tasks and choose to log from them",
                                    "?": "will do a look up for projects, outputs, and features",
                                    "input directly": "input direcly projects by inputting in the following order - context, project, output, feature, task ",
                                    "appreviation": "you can abbreviate context types by their first two letters",
                                    "task detail" : "the last argument is always the task note",
                                    "quotes" : "use ' ' quotes for arguments with more than one word"
                                }]

}
