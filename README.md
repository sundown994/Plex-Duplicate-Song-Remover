# Plex Duplicate Remover Script

This Python script automatically identifies and removes duplicate tracks in your Plex music library, prioritizing higher-quality versions based on bitrate. It leverages the `plexapi` library to connect to your Plex server and `send2trash` to safely move files to the trash.

## Requirements:
- Python 3
- `plexapi` library (`pip install plexapi`)
- `send2trash` library (`pip install send2trash`)

## How It Works:
- **Quality Comparison**: The script compares duplicates by checking the bitrate of the tracks. It retains the version with the higher bitrate and moves the lower-quality version to the trash.
- **File Hierarchy**: The script processes tracks based on their metadata in Plex. However, if the metadata is inconsistent or missing, the script relies on the directory structure to determine artist and album information.

## Steps to Use:

1. **Set Up Environment Variables**:
   - Create environment variables `PLEX_USERNAME` and `PLEX_PASSWORD` on your system to securely store your Plex account credentials.
   - Alternatively, replace `os.getenv('PLEX_USERNAME')` and `os.getenv('PLEX_PASSWORD')` with your username and password directly in the script, though using environment variables is recommended for security.

2. **Identify Your Server**:
   - Run the script to list your available Plex servers. Locate your server's identifier and replace `"YOUR_SERVER_IDENTIFIER"` in the script with your specific server identifier.

3. **Customize Your Library**:
   - Update the `library_name` variable to match the name of your music library in Plex if it is not named "Music."

4. **Directory Structure**:
   - Ensure that your music files follow a consistent directory structure. The script expects files to be organized as follows:
     ```
     /path/to/music/Artist Name/Album Name/Track.flac
     ```
   - For example:
     ```
     /Volumes/Music/Alabama/Greatest Hits/01 - Mountain Music.flac
     ```

   - If the script can't retrieve artist and album information from Plex metadata, it will extract this information from the file path. Ensure the directory structure is consistent to avoid misidentification.

5. **Run the Script**:
   - Execute the script from your terminal. It will process your tracks, identify duplicates based on title and artist, and move the lower-quality versions to the trash.

6. **Check the Log**:
   - The script generates a log file named `plex_duplicate_remover.log`. This log provides details on the tracks processed, duplicates identified, and files moved to the trash.

## Additional Notes:
- **Quality Check**: The script compares tracks based on their bitrate. If you prefer a different method of determining quality (e.g., file size, sample rate), you can modify the `compare_quality` function in the script to reflect your criteria.
- **Customizing File Paths**: If your music files are stored in a different location or follow a different hierarchy, you might need to adjust how the script extracts artist and album information from the file paths.

## Sharing the Script:
- Replace `"YOUR_SERVER_IDENTIFIER"` with the specific server identifier for others who want to use this script.
- Guide them on how to set up their Plex credentials and configure the library name and file paths.
