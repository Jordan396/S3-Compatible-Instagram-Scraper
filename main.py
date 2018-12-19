from instagram_scraper.scraper import InstagramScraper
import config
import boto3
import json
import shutil
import requests

TARGET_INSTAGRAM_USER = config.TARGET_INSTAGRAM_USER
S3_BUCKET_NAME = config.S3_BUCKET_NAME
AWS_REGION_NAME = config.AWS_REGION_NAME


TARGET_INSTAGRAM_USERS = [TARGET_INSTAGRAM_USER]
local_metadata_filename = 'metadata/{}.json'.format(TARGET_INSTAGRAM_USER)
destination_directory = 'instagram/{}'.format(TARGET_INSTAGRAM_USER)
destination_metadata_filename = '{}/full-metadata.json'.format(destination_directory)

s3_client = boto3.client(
		's3',
		region_name=AWS_REGION_NAME,
		aws_access_key_id=config.AWS_ACCESS_KEY_ID,
		aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
	)

def uploadFileToS3(s3_client, local_filename, destination_filename):
	s3_client.put_object(Body=open(local_filename, 'rb'), Bucket=S3_BUCKET_NAME, Key=destination_filename)

def uploadStreamToS3(s3_client, sourcestream, destination_filename):
	s3_client.put_object(Body=sourcestream, Bucket=S3_BUCKET_NAME, Key=destination_filename)

def extractKeyInformation(s3_client, local_metadata_filename, destination_directory):
	with open(local_metadata_filename) as json_data:
		json_data = json.load(json_data)
		for entry in json_data:
			keyInformation = {}
			entryID = entry['id']
			displayURL = entry['display_url']
			keyInformation['entryID'] = entryID
			keyInformation['displayURL'] = displayURL
			keyInformation['dimensions'] = entry['dimensions']
			keyInformation['edge_media_preview_like'] = entry['edge_media_preview_like']
			keyInformation['edge_media_to_caption'] = entry['edge_media_to_caption']
			keyInformation['edge_media_to_comment'] = entry['edge_media_to_comment']
			keyInformation['tags'] = entry['tags']
			keyInformation['comments'] = entry['comments']
			keyInformation['location'] = entry['location']

			s3_destination_directory = '{}/{}'.format(destination_directory, entryID)
			response = requests.get(displayURL)
			# TODO: Add support for more image formats
			destination_filename = '{}/{}.jpg'.format(s3_destination_directory, entryID)
			uploadStreamToS3(s3_client, response.content, destination_filename)
			destination_filename = '{}/summary.json'.format(s3_destination_directory)
			print(destination_filename)
			uploadStreamToS3(s3_client, json.dumps(keyInformation), destination_filename)


def main():
	scraper = InstagramScraper(media_types=['none'], login_user=config.INSTAGRAM_USER_ID, login_pass=config.INSTAGRAM_USER_PASSWORD, 
		usernames=TARGET_INSTAGRAM_USERS, comments=True, include_location=True)
	scraper.login()
	scraper.scrape()
	uploadFileToS3(s3_client, local_metadata_filename, destination_metadata_filename)
	extractKeyInformation(s3_client, local_metadata_filename, destination_directory)

if __name__ == '__main__':
	main()