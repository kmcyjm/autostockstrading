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
This project uses Selenium to start Chrome in headless mode, then log in to https://www.degiro.ie by simulating users
typing the username/password in a website.

After a successful login, the user home page will be rendered into plain HTML, it is then parsed using `XPATH` by 
Selenium to retrieve `DayDiff` and `% Chg` (Percent Change) of Nasdaq100 index on the web page.

Next, the open price and instant price for each share is retrieved in the current portofolio, and the Percent Change 
`(instant price - open price) * 100% / open price` is calculated for each of them. This value is then 
compared with the buy&sell thresholds pre-defined for each share, along with the NASDAQ100 index Percent Change to 
decide whether to buy or sell a specific share.

It worth mentioning that there is an additional step called `confirmOrder` following the `checkOrder` is needed for the order to be placed successfully in Degiro.

> The pre-defined thresholds for each share is a statistical result from the histogram based on the historical 
data of daily Percent Change since year 2000.

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

