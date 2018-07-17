import os
import subprocess
import datetime
import git

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
    script_dir = script_dir.replace("/programFiles","")
    print(script_dir)
    commitDescrip = "update of accounts {}".format(date)
    # subprocess.call(["pwd"])
    # subprocess.call(["cd",script_dir])
    # subprocess.call(["pwd"])
    # subprocess.call(["git","add","."])
    # subprocess.call(["git","commit","-m",commitDescrip])
    # subprocess.call(["git","push","origin","master"])
    #

    repo = git.Repo(script_dir)
    print (repo.git.status())
    # checkout and track a remote branch
    repo.git.add(u=True)
    # commit
    repo.git.commit( m=commitDescrip )
    # now we are one commit ahead
    repo.git.status()
    repo.git.push()

gitPush()


    #subprocess.call(["cd",script_dir])
    # subprocess.check_call([orient])
# cd /Users/matthewsteele\ 1/Desktop/ProjectFolder/GenusAccountManagement/GenusAccountManagement
# gitPush()
