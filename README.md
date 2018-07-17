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
locOfScript=''"$DirVar"'/programFiles/accountDataRequest.py'
echo 'alias GAI="python3 '"'"''"$locOfScript"''"'"'"'  >>~/.bash_profile
```
Script to edit bash profile to assign the python scripts

The alias through terminal won't be available until after you have restarted terminal.

## putting a chrome selenium webdriver in your bin folder

The most complicated aspect to executing the account scraping module is finding and placing the Selenium Chrome Webdriver in your computer's bin folder.

You can download the file from this site:

[Chrome Webdriver](http://chromedriver.chromium.org/getting-started)

Most users will find their bin folder in the following location.

cd into it and open in finder.

```console
cd /usr/local/bin
open .
```

Then place the downloaded Chrome Webdriver into the bin folder.

## Usage

You can look up p*ssw*rds by calling the command with with keycode and the account of interest.
```console
AI code accountName
```
doing so will copy the password directly



### TODO:
- automate account updates on a daily basis
- integrate coinbase lookups directly
- create functionality in main interface for adding new accounts
  - setting up account structure and initializing the creation of a encrypted store
  - automating permissions or the step by step process of associating a gdoc with the right email.
