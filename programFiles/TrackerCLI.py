import sys
from GSheetsAuth import GenTrackrGSheets
from TimeTracked import TimeTracked
from dotenv import load_dotenv
import os
import shlex
from pprint import pprint
from TrackerCommandOptions import TrackerCommands
import pickle

load_dotenv()



class TrackerSession:

    def __init__(self, initials, args):
        self.sheetsInstance = GenTrackrGSheets(initials)
        self.loggedTasks = []
        self.initials = initials
        self.allPreviouslyLoggedTasks = {}
        #self.loadAllTasksAsTaskInstances()
        self.createAndLogaTask(args)

    def createAndLogaTask(self, args):
        TimeTrackedInstance = TimeTracked(self.sheetsInstance, args)
        self.loggedTasks.append(TimeTrackedInstance)
        TimeTrackedInstance.logTask()

        taskState = input("end? (y?) {}".format(TimeTrackedInstance.taskDesciption) )

        if taskState == "y":
            TimeTrackedInstance.endTask()
            self.dealWithCommandInputs()
        else:
            self.dealWithCommandInputs()

    def logAllTasks(self):
        for eachTask in self.loggedTasks:
            eachTask.logTask()

    def loadAllTasksAsTaskInstances(self):
        allTasks = self.sheetsInstance.allTasks
        i = 0

        loadPicklebyMonth()

        for eachRow in allTasks:
            print(len(eachRow[3]))
            if len(eachRow[3]) > 1 and i > 13:
                exists = checkIflogged(eachRow)
                if not exists:
                    print(eachRow)
                    args =[]
                    args.append(eachRow[5])
                    args.append(eachRow[7])
                    args.append(eachRow[8])
                    args.append(eachRow[9])
                    args.append(eachRow[10])
                    taskInstance = TimeTracked(self.sheetsInstance, args)
                    taskInstance.stars = eachRow[11]
                    taskInstance.start = eachRow[12]
                    taskInstance.end = eachRow[13]
                    taskInstance.date = eachRow[4]
                    taskInstance.row = i
                    self.allPreviouslyLoggedTasks.append(taskInstance)
                    saveToPickle(taskInstance)

            i += 1
        writeAndClosePickle()


        for eachTask in self.allPreviouslyLoggedTasks:
            print(eachTask.taskDesciption)

        def checkIflogged(eachRow):
            dateTimeMerge = eachRow[3] + eachRow[11]

            try:
                TrackedTimeInstance[dateTimeMerge]
                return True
            except:
                return False

        def loadPicklebyMonth():
            month = datetime.date.today().strftime('%m')
            filename = month+"_loggedTasks_"+self.initials
            path = makeRelativePath('AccountDataPickles/{}.pickle'.format(fileName))

            tasksByMonth = open(path, 'wb') #might be a pickle file not a dict
            tasksByMonth = pickle.load(fileRead)
            self.allPreviouslyLoggedTasks = tasksByMonth

        def writeAndClosePickle():
            pickle.dump(self.allPreviouslyLoggedTasks, path)
            fileWrite.close(self.allPreviouslyLoggedTasks)

        def saveToPickle(taskInstance):
            dateTimeMerge = taskInstance.date + taskInstance.start
            self.allPreviouslyLoggedTasks[dateTimeMerge].update(taskInstance)




    def dealWithCommandInputs(self):

        command = input("What would you like to do? (write c for list of commands)")

        def options():
            if len(command) == 0:
                pass
            else:
                if command == "c":
                    printCommands()
                if command == "e":
                    exitAndLog()
                if command[0] == "l":
                    passCommandsToTaskLogger()
                if command[0] == "t":
                    listTasks()


            self.dealWithCommandInputs()

        def passCommandsToTaskLogger(): #doesn't take quotes as commands
            commandSplit = shlex.split(command)

            self.createAndLogaTask(commandSplit[1:])

        def exitAndLog():
            self.logAllTasks()
            raise Exception("exiting to Python!")

        def printCommands():
            pprint(TrackerCommands)

        def listTasks():
            i = 0
            for eachTask in self.loggedTasks:
                print(i,"  ", eachTask.taskDesciption)
                i += 1

            editCommand = input("edit a task? \n select and choose how [example: 3 t1 Personal] \n(t1 = context, t2 = project... | \n s = start time [match start with task number end or start [3 s s2]], e = end time | d = date [3 d d2])")

            if len(editCommand) == 0:
                self.dealWithCommandInputs()

            else:

                editCommandsplit = editCommand.split()
                taskChoice = int(editCommandsplit[0])
                taskChosen = self.loggedTasks[taskChoice]

                if editCommandsplit[2]:
                    qualityText = editCommandsplit[2]


                if "t" in editCommandsplit[1]:
                    taskQualityToEdit = int(editCommandsplit[1][1])-1


                    optionsList = ['context', 'project', 'output', 'feature', 'task']

                    chosenQuality = optionsList[taskQualityToEdit]

                    if taskQualityToEdit == taskQualityToEdit:
                        taskChosen.setQuality(chosenQuality, qualityText)

                if "s" in editCommandsplit[1]:

                    if 's' in editCommandsplit[2]:
                        taskToCopy = int(editCommandsplit[2][1])
                        taskChosen.start = self.loggedTasks[taskToCopy].start

                    if 'e' in editCommandsplit[2]:
                        taskToCopy = int(editCommandsplit[2][1])
                        taskChosen.start = self.loggedTasks[taskToCopy].end

                    else:
                        taskChosen.start = editCommandsplit[2]


                if 'e' in editCommandsplit[1]:

                    if 's' in editCommandsplit[2]:
                        taskToCopy = int(editCommandsplit[2][1])
                        taskChosen.end = self.loggedTasks[taskToCopy].start

                    if 'e' in editCommandsplit[2]:
                        taskToCopy = int(editCommandsplit[2][1])
                        taskChosen.end = self.loggedTasks[taskToCopy].end

                    else:
                        taskChosen.end = editCommandsplit[2]


                if 'd' in editCommandsplit[1]:

                    if editCommandsplit[2].contains["d"]:
                        taskToCopy = int(editCommandsplit[2][1])
                        taskChosen.date = self.loggedTasks[taskToCopy].date

                    else:
                        taskChosen.end = editCommandsplit[2]

                else:
                    self.dealWithCommandInputs()


                #make date, start or end time match specific task date, start or end time by number


        options()


def Main(args="", session=""):
    if len(args) == 0:
        initials = sys.argv[1]
        args = sys.argv[2:]

    else:
        args =shlex.split(args)
        initials = args[0]
        args = args[1:]

    if len(session) == 0:
        TrackerSessionInstance = TrackerSession(initials, args)

    elif len(session) > 0:
        TrackerSessionInstance = session

    return TrackerSessionInstance



if __name__ == '__main__':
    Main()
