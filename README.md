# S3-Compatible-Instagram-Scraper
**DISCLAIMER**

Please view and respect the license file attached. Credits to [*rarcega*](https://github.com/rarcega/instagram-scraper) for which this repository was built upon.

---

## Project Overview
Building upon the fantastic work by [*rarcega*](https://github.com/rarcega/instagram-scraper), this repository allows users to start scraping instagram data *immediately*, with the scraped data being organized neatly in Amazon S3 ready to be analyzed. Each _post_ by the target instagram user is stored conveniently in its own folder. Each folder contains the image as well as the post's associated metadata.

The directory structure on Amazon S3 is as such:
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

## Installation
#### 1) Clone this Repository
`git clone https://github.com/Jordan396/S3-Compatible-Instagram-Scraper.git`

`cd S3-Compatible-Instagram-Scraper/`

#### 2) Activate your Virtual Environment
`source venv/bin/activate`

#### 3) Set up Configuration
Create a file called _config.py_ and add the following lines:
```
AWS_ACCESS_KEY_ID = [YOUR AWS_ACCESS_KEY_ID]
AWS_SECRET_ACCESS_KEY = [YOUR AWS_SECRET_ACCESS_KEY]
AWS_REGION_NAME = [YOUR AWS_REGION_NAME]
INSTAGRAM_USER_ID = [YOUR INSTAGRAM_USER_ID]
INSTAGRAM_USER_PASSWORD = [YOUR INSTAGRAM_USER_PASSWORD]
S3_BUCKET_NAME = [YOUR AWS_S3_BUCKET_NAME]
TARGET_INSTAGRAM_USER = [YOUR TARGET_INSTAGRAM_USER TO SCRAPE DATA FROM]
```
Detailed instructions for lines 1-3 can be found [here](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html). Your instagram userID and password are required to scrape posts from private users followed by your account. To create an S3 bucket, refer to this [link](https://docs.aws.amazon.com/quickstarts/latest/s3backup/step-1-create-bucket.html). Lastly, input the name of the instagram user you want to scrape data from.

#### 4) Begin scraping!
`python main.py`

Once operation completes, you can navigate to your S3 bucket to view your scraped data.
