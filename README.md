## FAO Food Aid Shipments and Food Security Data Collector

Collector for [FAO Data](http://faostat3.fao.org).

## Setup

*local*

(You are using a [virtualenv](http://www.virtualenv.org/en/latest/index.html), right?)

    sudo pip install -r requirements.txt
    manage setup

*ScraperWiki Box*

    make setup

## Usage

*local*

    manage run

*ScraperWiki Box*

    source venv/bin/activate
    manage -m Scraper run

The results will be stored in a SQLite database `scraperwiki.sqlite`.
