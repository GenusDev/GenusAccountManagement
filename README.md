# GenusAccountManagement
Scripts for automating account management for Genus Development Partners

Optimized for a Mac OS

## Dependencies

These scripts use Python3 - so first make sure you have a current version of Python3 before installing

### command for installing dependencies

```console
pip install -r requirements.txt
```
You may need to install the Robinhood library directly from this link: [github](https://github.com/Jamonek/Robinhood)

## Copy the following into your bash profile:
From terminal in project folder run:

Copy PWD as DirVar

```console
pwd | tr -d '\n' | pbcopy
DirVar=`pwd`
locOfScript=''"$DirVar"'/GenusAccountManagement/accountDataRequest.py'
echo 'alias GAI="python3 '"'"''"$locOfScript"''"'"'"'  >>~/.bash_profile
```
Script to edit bash profile to assign the python scripts

Replace the curly braces by pasting in the copied the PWD.


## putting a chrome selenium webdriver in your bin folder

The most complicated aspect to executing the account scraping module is finding and placing the Selenium Chrome Webdriver in your computer's bin folder.

You can download the file from this site:

[Chrome Webdriver](http://chromedriver.chromium.org/getting-started)

Most users will find their bin folder in the following location.

cd into it and open in finder.

```console
cd ***
open .
```

Then place the downloaded Chrome Webdriver into the bin folder.

## Usage

You can look up p*ssw*rds by calling the command with with keycode and the account of interest.
```console
GAI code accountName
```
doing so will copy the password directly
