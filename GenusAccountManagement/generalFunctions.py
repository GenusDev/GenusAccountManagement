import os
import subprocess
import datetime

def makeRelativePath(Path):
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    abs_file_path = os.path.join(script_dir, Path)
    return abs_file_path


def copy(data):
    print(data + " copied")
    os.system("echo '%s' | pbcopy" % data)


def gitPush():
    date = datetime.date.today().strftime('%Y%m%d')
    script_dir = os.path.dirname(__file__)
    script_dir = "'"+script_dir+"'"
    script_dir = script_dir.replace("/Users/matthewsteele 1/","")
    print(script_dir)
    orient = "pwd"
    test = "echo 'testing'"
    add = "git "
    #script_dir = "'Desktop/ProjectFolder/GenusAccountManagement/GenusAccountManagement'"

    commitDescrip = "'update of accounts {}'".format(date)
    push = 'git push origin master"'
    # os.system("echo '%s' | pbcopy" % data)
    # subprocess.check_call(["ls", "-l"])
    # os.system("cd  '%s' " % script_dir)
    # subprocess.check_call(["echo",script_dir])
    subprocess.call(["git","add","."])
    subprocess.call(["git","commit","-m",commitDescrip])
    subprocess.call(["git","push","origin","master"])
    #subprocess.call(["cd",script_dir])
    # subprocess.check_call([orient])
# cd /Users/matthewsteele\ 1/Desktop/ProjectFolder/GenusAccountManagement/GenusAccountManagement

gitPush()
