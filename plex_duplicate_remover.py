#!/usr/bin/env python3
from plexapi.myplex import MyPlexAccount
import plexapi
import os
import sys
import logging
from send2trash import send2trash  # Import the send2trash module

# Setup output of debug statements
log = logging.getLogger("PlexSmartDuplicateRemover")
log.setLevel(logging.INFO)  # INFO level to reduce verbosity

# Log to a file
file_handler = logging.FileHandler('plex_duplicate_remover.log')
file_handler.setLevel(logging.INFO)
console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.INFO)
log.addHandler(file_handler)
log.addHandler(console_handler)

# Authenticate with Plex
username = os.getenv('PLEX_USERNAME')
pw = os.getenv('PLEX_PASSWORD')
account = MyPlexAccount(username, pw)

# List all resources (servers) available
print("Available Plex Servers:")
for resource in account.resources():
    print(f"Name: {resource.name}, ID: {resource.clientIdentifier}")

# Replace this with the correct server identifier after verifying
server_identifier = "YOUR_SERVER_IDENTIFIER"

# Enhanced Connection Logic
plex = None
for resource in account.resources():
    if resource.clientIdentifier == server_identifier:
        plex = resource.connect()
        break

if plex is None:
    raise Exception(f"Unable to connect to server with ID: {server_identifier}")

# Get the music library
library_name = "Music"  # Adjust this to your library name
library = plex.library.section(library_name)

# Fetch all tracks explicitly
tracks = library.search(libtype='track')
total_tracks = len(tracks)
log.info(f"Total number of tracks: {total_tracks}")

uniqueTracks = {}  # Dictionary to store unique tracks
duplicateTracks = []  # List to store duplicates to remove

# Function to determine the better quality track
def compare_quality(track1, track2):
    try:
        quality1 = int(track1.media[0].bitrate or 0)
    except AttributeError:
        quality1 = 0
    try:
        quality2 = int(track2.media[0].bitrate or 0)
    except AttributeError:
        quality2 = 0

    return track1 if quality1 > quality2 else track2

# Process tracks
for track in tracks:
    try:
        title = track.title
        artist = track.grandparentTitle if hasattr(track, 'grandparentTitle') else "Unknown Artist"
        album = track.parentTitle if hasattr(track, 'parentTitle') else "Unknown Album"
        file_path = track.media[0].parts[0].file if hasattr(track.media[0], 'parts') else "No file path available"

        key = (title, artist)

        if key in uniqueTracks:
            betterTrack = compare_quality(uniqueTracks[key], track)
            if betterTrack == uniqueTracks[key]:
                duplicateTracks.append(track)
                log.info(f"Duplicate found: {title} by {artist} - Keeping better quality track.")
            else:
                duplicateTracks.append(uniqueTracks[key])
                uniqueTracks[key] = track
                log.info(f"Duplicate found: {title} by {artist} - Replacing with better quality track.")
        else:
            uniqueTracks[key] = track

    except Exception as e:
        log.error(f"Error processing track: {e}")

# Move lower quality duplicates to trash with logging
for track in duplicateTracks:
    artist = track.grandparentTitle if hasattr(track, 'grandparentTitle') else "Unknown Artist"
    log.info(f'Removing {track.title} by {artist} and moving to trash.')

    for media in track.media:
        for part in media.parts:
            file_path = part.file
            if os.path.exists(file_path):
                send2trash(file_path)
                log.info(f'Moved to trash: {file_path}')
            else:
                log.error(f'File does not exist: {file_path}')
    track.delete()

print("Duplicate processing completed.")
