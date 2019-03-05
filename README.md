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


  