# PyTubeLib

## Installation

`pip install pytubelib`
## Usage

	from pytubelib import YTAPI

	# Load credentials from a JSON file
	creds_file = '/path/to/credentials.json'

	# Create an instance of the YTAPI class
	yt = YTAPI(creds_file)

	# Search for channels by keyword
	channels = yt.search_channels('xXBlackDev9010Xx')

	# Get details for the first channel in the list
	channel_id = channels[0]
	channel_details = yt.get_channel_details(channel_id)

	# Search for videos in the channel by keyword
	videos = yt.search_new_videos(channel_id, 'tutorial')

	# Get details for the first video in the list
	video_id = videos[0]['id']['videoId']
	video_details = yt.get_video_details(video_id)