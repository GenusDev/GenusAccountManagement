 from GSheetsAuth import GenTrackrGSheets
import datetime

#probably better to pass this object the client rather than have to recreate the instance with every creation

class TimeTracked:

    def __init__(self, sheetsInstance, args):
        self.sheetsInstance = sheetsInstance
        self.row = self.setRow()
        self.person = sheetsInstance.initials
        self.date = datetime.date.today().strftime('%m/%d/%Y')
        self.start =  datetime.datetime.now().strftime('%H:%M:%S')
        self.end = ""
        self.context = "" #potentially default to projects unless otherwise set
        self.project = ""
        self.output = ""
        self.feature = ""
        self.task = ""
        self.stars = ""
        self.refKey = ""
        self.args = args ##shift
        self.taskDesciption = "{} {} {} {} {} {} ({})".format(self.context, self.project, self.output, self.feature, self.task, self.start, self.end)

        self.manageInputs(args)


    def setRow(self):
        row = self.sheetsInstance.createNewLine()
        return row

    def setQuality(self, quality, newDescription):

        setattr(self, quality, newDescription)

        self.taskDesciption = "{} {} {} {} {} {} ({})".format(self.context, self.project, self.output, self.feature, self.task, self.start, self.end)

        print(self.taskDesciption)

    def setRefKey(self):

        self.refKey = self.date + self.start
        

    def manageInputs(self, args):

        def plausableInputs():

            if args[0] == "tasks":
                selectTask()

            else:
                if args[0] == "??":
                    args[0] = "Projects"
                    for i in range(4):
                        args.append("?")

                self.task = args[-1]

                if len(args) > 1:
                    self.context = handleContextAbbreviations(args[0])

                if len(args) > 2:
                    self.project = pickFromProjects(args[1])

                if len(args) > 3 :
                    self.output = pickFromOutputs(args[2])

                if len(args) > 4 :
                    self.feature = pickFromFeatures(args[3])

                if len(args) == 5 :
                    self.task = pickFromTasks(args[4])

            self.taskDesciption = "{} {} {} {} {} {} ({})".format(self.context, self.project, self.output, self.feature, self.task, self.start, self.end)
            self.setRefKey()

        def selectTask():
            taskRows = self.sheetsInstance.listCurrentTasks()

            whichTaskNum = int(input("select task by #"))
            taskSelected = taskRows[whichTaskNum]

            self.context = "Projects"
            self.project = taskSelected[0]
            self.output = taskSelected[1]
            self.feature = taskSelected[2]
            self.task = taskSelected[3]

        def handleContextAbbreviations(arg):
            contextOptions = self.sheetsInstance.grabContextOptions()

            if len(arg) < 3:
                for eachOption in contextOptions:
                    if arg.lower() == eachOption.value[:2].lower():
                        self.args[0] = eachOption.value
                        return eachOption.value
            else:
                return arg

        def pickFromProjects(arg):
            if arg == "?":
                projectSheet = self.sheetsInstance.client.open_by_key(self.sheetsInstance.spreadsheetId).worksheet('ProjectRanges')
                values = projectSheet.get_all_values()
                columnToChooseFrom = []

                for eachRow in values:
                    if self.args[0] == eachRow[0]:
                        columnToChooseFrom = eachRow

                return chooseFromList("project",columnToChooseFrom[1:])


                #         for eachCell in eachRow:
                #             if i > 0 and len(eachCell)>1:
                #                 print(i, "  ",eachCell)
                #             i += 1
                #
                # return projectSelection

            else:
                return arg

        def pickFromOutputs(arg):

            if arg == "?":
                projectTaskSheet = self.sheetsInstance.client.open_by_key(self.sheetsInstance.spreadsheetId).worksheet(self.project)
                unique_output_list = list(set(projectTaskSheet.col_values(2)))[1:]
                return chooseFromList("output", unique_output_list)

            else:
                return arg



        def pickFromFeatures(arg):

            if arg == "?":
                projectTaskSheet = self.sheetsInstance.client.open_by_key(self.sheetsInstance.spreadsheetId).worksheet(self.project)
                outPutCells = projectTaskSheet.findall(self.output)
                i = 0
                featuresByOutput = []
                for eachCell in outPutCells:
                    cellRow = eachCell.row
                    cellColumn = eachCell.col
                    val = projectTaskSheet.cell(cellRow, cellColumn+1).value
                    if len(val)>0:
                        featuresByOutput.append(val)

                return chooseFromList("feature", list(set(featuresByOutput)))

            else:
                return arg


        def pickFromTasks(arg):

            if arg == "?":
                projectTaskSheet = self.sheetsInstance.client.open_by_key(self.sheetsInstance.spreadsheetId).worksheet(self.project)
                taskCells = projectTaskSheet.findall(self.feature)
                i = 0
                tasksByOutput = []
                for eachCell in taskCells:
                    cellRow = eachCell.row
                    cellColumn = eachCell.col
                    val = projectTaskSheet.cell(cellRow, cellColumn+1).value
                    if len(val)>0:
                        tasksByOutput.append(val)

                return chooseFromList("task", list(set(tasksByOutput)))

            else:
                return arg

        def chooseFromList(choice,listOfItems):
            if len(listOfItems) == 0:
                return ""

            else:
                i = 0
                for eachItem in listOfItems:
                    if len(eachItem) > 0:
                        print(i, "  ",eachItem)
                        i += 1


                SelectionNumb = int(input("Which {} ? (by#)".format(choice)))

                return listOfItems[SelectionNumb]



        plausableInputs()



    def logTask(self, Row="nonSpecified"):
        cell_list = self.sheetsInstance.individualTrackerSheet.range(self.row,4,self.row,13)

        cell_list[0].value = self.date
        cell_list[1].value = self.context
        cell_list[2].value = ''
        cell_list[3].value = self.project
        cell_list[4].value = self.output
        cell_list[5].value = self.feature
        cell_list[6].value = self.task
        cell_list[7].value = ''
        cell_list[8].value = self.start
        cell_list[9].value = self.end


        self.sheetsInstance.individualTrackerSheet.update_cells(cell_list, value_input_option='USER_ENTERED')


    def endTask(self):
        cell_list = self.sheetsInstance.individualTrackerSheet.range(self.row,13,self.row,13)
        self.end = datetime.datetime.now().strftime('%H:%M:%S')
        cell_list[0].value = self.end

        self.sheetsInstance.individualTrackerSheet.update_cells(cell_list, value_input_option='USER_ENTERED')
