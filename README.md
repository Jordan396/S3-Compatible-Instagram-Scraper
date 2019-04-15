# S3-Compatible-Instagram-Scraper
[![Project Status: Inactive – The project has reached a stable, usable state but is no longer being actively developed; support/maintenance will be provided as time allows.](https://www.repostatus.org/badges/latest/inactive.svg)](https://www.repostatus.org/#inactive)
[![Latest Commit](https://img.shields.io/github/last-commit/jordan396/S3-Compatible-Instagram-Scraper/master.svg)](https://img.shields.io/github/last-commit/jordan396/S3-Compatible-Instagram-Scraper/master.svg)
[![Repo Size](https://img.shields.io/github/repo-size/jordan396/S3-Compatible-Instagram-Scraper.svg)](https://img.shields.io/github/repo-size/jordan396/S3-Compatible-Instagram-Scraper.svg)
[![GitHub Followers](https://img.shields.io/github/followers/jordan396.svg?label=Follow)](https://img.shields.io/github/followers/jordan396.svg?label=Follow)

## Overview
This project is an extension of the Instagram scraper built by [*rarcega*](https://github.com/rarcega/instagram-scraper).

It is designed to organize the scraped instagram data neatly in AWS S3, according to this structure:
```
S3_BUCKET_NAME/
|
|-- instagram/
   |-- TARGET_USER
      |-- full-metadata.json: Contains metadata for entire operation
      |-- [POST_ID_X]
         |-- [POST_ID_X].jpg: Image of the post
         |-- summary.json: Key information associated with post
      |-- [POST_ID_Y]
         |-- [POST_ID_Y].jpg
         |-- summary.json
      | ...
```
- Each _post_ by the target instagram user is stored in its own folder. 
- Each folder contains the image as well as the post's associated metadata.

## Getting Started

### Prerequisites

These instructions were designed for *Ubuntu 18.04*.

You will need to create a `config.py` file with the following contents:
```
AWS_ACCESS_KEY_ID = [YOUR AWS_ACCESS_KEY_ID]
AWS_SECRET_ACCESS_KEY = [YOUR AWS_SECRET_ACCESS_KEY]
AWS_REGION_NAME = [YOUR AWS_REGION_NAME]
S3_BUCKET_NAME = [YOUR AWS_S3_BUCKET_NAME]
INSTAGRAM_USER_ID = [YOUR INSTAGRAM_USER_ID]
INSTAGRAM_USER_PASSWORD = [YOUR INSTAGRAM_USER_PASSWORD]
TARGET_INSTAGRAM_USER = [YOUR TARGET_INSTAGRAM_USER TO SCRAPE DATA FROM]
```
A `config_template.py` file has been provided for your convenience.

Now, follow these instructions to get the variables above.
- Lines 1-3 relating to [AWS](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html).
- Line 4 relating to AWS [S3](https://docs.aws.amazon.com/quickstarts/latest/s3backup/step-1-create-bucket.html).
- Lines 5-7 are self-explanatory. The TARGET_INSTAGRAM_USER refers to the name of the user you intend to scrape data from.

**NOTE**: Your userId and password are required to scrape data from *private* users followed by you.

## Installation
1. Clone this repository.
   ```
   git clone https://github.com/Jordan396/S3-Compatible-Instagram-Scraper.git
   cd S3-Compatible-Instagram-Scraper/
   ```
2. Create a venv and activate it.
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies.
   ```
   pip install -r requirements.txt
   ```
4. Add your `config.py` above to the base directory.
5. Start scraping!
   ```
   python scrape.py
   ```
6. Navigate to your S3 bucket to view the scraped data.
