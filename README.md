## FAO Food Aid Shipments and Food Security Data Collector

[HDX](https://data.hdx.rwlabs.org/) collector for [FAO Data](http://faostat3.fao.org).

## Introduction

hdxscraper-fao operates in the following way:

- Downloads `faostat-bulkdownloads` zip files
- Extracts and normalizes the csv file
- Places the resulting data for each file into a separate database table

With hdxscraper-fao, you can

- Save FAO Data to an external database
- Create CKAN datasets/packages for each database table
- Upload ScraperWiki generated CSV files into a CKAN instance
- Update resources previously uploaded to CKAN with new metadata

[View the live data](https://data.hdx.rwlabs.org/organization/fao)

## Requirements

hdxscraper-fao has been tested on the following configuration:

- MacOS X 10.9.5
- Python 2.7.10

hdxscraper-fao requires the following in order to run properly:

- [Python >= 2.7](http://www.python.org/download) (MacOS X comes with python pre-installed)

## Setup

*local*

(You are using a [virtualenv](http://www.virtualenv.org/en/latest/index.html), right?)

    git clone https://github.com/reubano/hdxscraper-fao.git
    pip install -r requirements.txt
    manage setup

*ScraperWiki Box*

    make setup

## Usage

*local*

    manage run

*ScraperWiki Box*

    cd tool
    source venv/bin/activate
    screen manage -m Scraper run
    # Now press `Ctrl-a d`

The results will be stored in a SQLite database `scraperwiki.sqlite`.

*view all available commands*

    manage

## Upload tables to [HDX](http://data.hdx.rwlabs.org/)/[CKAN](http://ckan.org/)

*upload to production site*

    manage upload

*upload to staging site*

    manage upload -s

## Update tables on [HDX](http://data.hdx.rwlabs.org/)/[CKAN](http://ckan.org/) with new metadata

*update dataset on production site*

    manage update

*update dataset on staging site*

    manage update -s

*ScraperWiki box*

    make update
    cd tool
    source venv/bin/activate
    screen manage -m Scraper run
    # Now press `Ctrl-a d`
    manage update

## Configuration

hdxscraper-fao will use the following [Environment Variables](http://www.cyberciti.biz/faq/set-environment-variable-linux/) if set:

Environment Variable|Description
--------------------|-----------
CKAN_API_KEY|Your CKAN API Key
CKAN_PROD_URL|Your CKAN instance remote production url
CKAN_REMOTE_URL|Your CKAN instance remote staging url
CKAN_USER_AGENT|Your user agent

## Creating a new collector

If you would like to create collector or scraper from scratch, check out [cookiecutter-collector](https://github.com/reubano/cookiecutter-collector).

    pip install cookiecutter
    cookiecutter https://github.com/reubano/cookiecutter-collector.git

## Contributing

### Code

1. fork
2. commit
3. submit PR
4. ???
5. PROFIT!!!

### Document

- improve this readme
- add comments to confusing parts of the code
- write a "Getting Started" guide
- write additional deployment instructions ([Heroku](http://heroku.com/), [AWS](http://aws.amazon.com/), [Digital Ocean](http://digitalocean.com/, [GAE](https://appengine.google.com/))

### QA

1. follow this guide and see if everything works as expected
2. if something doesn't work, please submit an issue

## License

hdxscraper-fao is distributed under the [MIT License](http://opensource.org/licenses/MIT).
