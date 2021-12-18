# MinecraftUpdater
This is a python package to automate the updating of your Minecraft server.<br>
It's very annoying to have to download the jar,
ftp it over, stop the server, back up your world, etc. This automates alll that. just git clone this in the root of
your server so there is an extra folder. Then run python3 update.py in the new folder. It will check if you have the
latest version of Minecraft using the Mojang provided manfest URL. If your server is out of date, it will download the latest minecraft server jar from the official Mojang S3 bucket. Then using screen it will announce to the server that it is going to restart for an update, and give a 30 seconds countdown before stopping the server. Next it will then backup your world into a new folder, incase something goes wrong. It then updates the server jar and starts the server back up in a screen session so it's in the background.
           
## Configuration

### Latest vs. Snapshot
UPDATE_TO_SNAPSHOT = \<True,False\> whether to update to the latest snapshot, or main release

### Backup Directory
BACKUP_DIR = \<name of directory to save files\>

### Log File
LOG_FILENAME = \<name of file to save log messages\>

### Ram Settings                
RAM_INITIAL = \<amount of ram to start the server with\><br>
RAM_MAX = \<maximum amount of ram to allocate torwards the server\>           
           
## Scheduling Updates
This script is intended to be run as a cron job.
