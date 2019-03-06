# Auto Stock Trade

Auto trade stocks in Degiro using Selenium + Chrome headless mode.

## Pre-requisites

1. [Chromedriver](http://chromedriver.chromium.org/)
2. [Google Chrome web browser](https://www.google.com/chrome/).
3. [Selenium](https://www.seleniumhq.org/).

pyenv and pipenv are not required but highly recommended.
 
With pyenv, one can very easily manage multiple versions of Python on a single operating system.
 
And with the help of `pipenv`, the dependencies of the project is auto updated (and locked) in a file called `Pipfile.lock`, so setting up an identical environment on a different machine
is as easy as cloning the repo, and running `pipenv install` the same directory as the `Pipfile`. pipenv also automatically creates a virtual environment for the project.

## How it works
This project starts Chrome in headless mode, imitate user action in the GUI browser to log in to www.degiro.ie using username/password.

After rendering the web page using Selenium + Chrome, it then uses XPATH(in Selenium) to retrieve `Day Diff` and Nasdaq 100 index change on the website.

Meanwhile, it retrieves the open price + instant price for interested shares, calculate and compare the `Chg %` of the price to pre-defined threshold.

The pre-defined threshold for each share is analysed using histogram utilizing the historical daily `Chg %`since year 2000 (if exists).

If the monitored `Chg %` passed the threshold, this program will sell/buy the specified shares as instructed.

It worth mentioning that there is an additional step called `confirmOrder` following the `checkOrder` is needed for the order to be placed successfully in Degiro.

## Get it up and running!

1. Follow instructions in pre-requisites to set up the environment.
1. Clone the repo.
1. Go to root directory of the repo, run `pipenv install` to install all the project dependencies.
1. Set up a crontab task to start the program at the time specified. It also keeps monitoring the execution of this program, restart it if stopped.

>crontab job
```
* 14-21 * * 1-5 restart_stockstrading_job.sh >> ~/Documents/crontab.log
```

>restart_stockstrading_job.sh
```
#!/bin/bash

# crontab only sets PATH=/bin;/usr/bin by default
PATH=/usr/bin:/usr/local/bin:/home/dwrm/.local/bin
SHELL=/bin/bash
working_dir="/home/dwrm/Dropbox/WorkSpace/PyCharmProjects/stocks"

trading_process=$(pgrep -f '/home/dwrm/.local/share/virtualenvs/stocks-imp7Hn9_/bin/python -u -m autostockstrading')

# using the actual returned pid from pgrep is much more reliable than $?
if [ -z "$trading_process" ]; then
    cd $working_dir
    # -u must be used here to unbuffer the output from print in the program
    pipenv run python -u -m autostockstrading >> /home/dwrm/Documents/restart_stockstrading_job.log 2>&1
fi
```

