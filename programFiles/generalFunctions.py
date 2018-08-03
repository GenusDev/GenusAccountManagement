import os
import datetime
import git

def makeRelativePath(Path):
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    abs_file_path = os.path.join(script_dir, Path)
    return abs_file_path


def copy(data):
    print(data + " copied")
    os.system("echo '%s' | pbcopy" % data)


def gitPull():
    script_dir = os.path.dirname(__file__)
    script_dir = script_dir.replace("/programFiles","")

    repo = git.Repo(script_dir)
    repo.git.pull()

def gitPush():
    date = datetime.date.today().strftime('%Y%m%d')
    script_dir = os.path.dirname(__file__)
    script_dir = script_dir.replace("/programFiles","")
    print(script_dir)
    commitDescrip = "update of accounts {}".format(date)

    repo = git.Repo(script_dir)
    repo.git.add(u=True)
    repo.git.commit( m=commitDescrip )
    repo.git.push()

# gitPush()


    #subprocess.call(["cd",script_dir])
    # subprocess.check_call([orient])
# cd /Users/matthewsteele\ 1/Desktop/ProjectFolder/GenusAccountManagement/GenusAccountManagement
# gitPush()
