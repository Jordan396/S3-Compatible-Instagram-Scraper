# -*- coding: utf-8 -*-
"""S3 compatible instagram scraper script.

This file has been adapted from racega's scraper.
<https://github.com/rarcega/instagram-scraper>

It is a simple extension to organize the data neatly in S3.

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

TODO
    * Add support for more image formats
"""

# Library imports
import boto3
import json
import shutil
import requests

# Local imports
import config
from instagram_scraper.scraper import InstagramScraper

__author__ = "Jordan396"
__status__ = "Development"

# Assign config variables
AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
AWS_REGION_NAME = config.AWS_REGION_NAME
S3_BUCKET_NAME = config.S3_BUCKET_NAME
TARGET_INSTAGRAM_USER = config.TARGET_INSTAGRAM_USER
INSTAGRAM_USER_ID = config.INSTAGRAM_USER_ID
INSTAGRAM_USER_PASSWORD = config.INSTAGRAM_USER_PASSWORD

# Set file paths
local_metadata_filename = 'metadata/{}.json'.format(TARGET_INSTAGRAM_USER)
destination_directory = 'instagram/{}'.format(TARGET_INSTAGRAM_USER)
destination_metadata_filename = '{}/full-metadata.json'.format(
    destination_directory)

# Initialize S3 client
s3_client = boto3.client(
    's3',
    region_name=AWS_REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


def upload_file_to_S3(s3_client, local_filename, destination_filename):
	"""Uploads a file to S3.
	"""
	s3_client.put_object(Body=open(local_filename, 'rb'),
                         Bucket=S3_BUCKET_NAME, Key=destination_filename)


def upload_stream_to_s3(s3_client, sourcestream, destination_filename):
	"""Uploads a binary stream to S3.
	"""
	s3_client.put_object(
        Body=sourcestream, Bucket=S3_BUCKET_NAME, Key=destination_filename)


def extract_key_info(s3_client, local_metadata_filename, destination_directory):
	"""Extract key information from metadata.
	"""
	with open(local_metadata_filename) as json_data:
		json_data = json.load(json_data)
		for entry in json_data:
			keyInfo = {}
			entryID = entry['id']
			displayURL = entry['display_url']
			keyInfo['entryID'] = entryID
			keyInfo['displayURL'] = displayURL
			keyInfo['dimensions'] = entry['dimensions']
			keyInfo['edge_media_preview_like'] = entry['edge_media_preview_like']
			keyInfo['edge_media_to_caption'] = entry['edge_media_to_caption']
			keyInfo['edge_media_to_comment'] = entry['edge_media_to_comment']
			keyInfo['tags'] = entry['tags']
			keyInfo['comments'] = entry['comments']
			keyInfo['location'] = entry['location']

			s3_destination_directory = '{}/{}'.format(
				destination_directory, entryID)
			response = requests.get(displayURL)
			destination_filename = '{}/{}.jpg'.format(
				s3_destination_directory, entryID)
			upload_stream_to_s3(s3_client, response.content, destination_filename)
			destination_filename = '{}/summary.json'.format(
				s3_destination_directory)
			upload_stream_to_s3(s3_client, json.dumps(
				keyInfo), destination_filename)


def scrape():
	"""main scraping function.
	"""
	scraper = InstagramScraper(media_types=['none'], login_user=INSTAGRAM_USER_ID, login_pass=INSTAGRAM_USER_PASSWORD,
                               usernames=[TARGET_INSTAGRAM_USER], comments=True, include_location=True)
	scraper.login()
	scraper.scrape()
	upload_file_to_S3(s3_client, local_metadata_filename,
					destination_metadata_filename)
	extract_key_info(
		s3_client, local_metadata_filename, destination_directory)


if __name__ == '__main__':
    scrape()
