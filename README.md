# MinecraftUpdater
This is a python package to automate the updating of your server. Its so annoying to try and download the jar,
ftp it over, stop the server, back up your world, etc. This automates alll that. just git clone this in the root of
your server so there is an extra folder. Then run python update.py in the new folder. it will check if you have the
latest version. if not if will download the latest jar, then using screen it will announce to the server that it will
shutdown and give a 30 seconds countdown before stopping the server. it will then backup your world into a new folder
when it updates incase somethign goes wrong. then update the jar and start the server back up in screen so its in
the background.
           
The first line of the file is         
updateToSnapShot = True          
which means it will update to snapshots. change it to false if you only want to update to the main releases
         
All the logs can be found in the update.log file.          
        
I run this in a crop job twice a day so it will be fully automatic but feel free to only run it manually
