import os
import time
import shutil
import hashlib
import time
from datetime import datetime
import logging
import requests


# CONFIGURATION
UPDATE_TO_SNAPSHOT = False
BACKUP_DIR = 'world_backups'
LOG_FILENAME = 'auto_updater.log'
RAM_INITIAL = '512m'
RAM_MAX = '3g'

MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"

logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# retrieve version manifest
response = requests.get(MANIFEST_URL)
data = response.json()

if UPDATE_TO_SNAPSHOT:
    minecraft_ver = data['latest']['snapshot']
else:
    minecraft_ver = data['latest']['release']

# get checksum of running server
if os.path.exists('../minecraft_server.jar'):
    sha = hashlib.sha1()
    f = open("../minecraft_server.jar", 'rb')
    sha.update(f.read())
    cur_ver = sha.hexdigest()
else:
    cur_ver = ""

for version in data['versions']:
    if version['id'] == minecraft_ver:
        jsonlink = version['url']
        jar_data = requests.get(jsonlink).json()
        jar_sha = jar_data['downloads']['server']['sha1']

        logging.info('Your sha1 is ' + cur_ver + '. Latest version is ' + str(minecraft_ver) + " with sha1 of " + jar_sha)

        if cur_ver != jar_sha:
            logging.info('Updating server...')
            link = jar_data['downloads']['server']['url']
            logging.info('Downloading .jar from ' + link + '...')
            response = requests.get(link)
            with open('minecraft_server.jar', 'wb') as jar_file:
                jar_file.write(response.content)
            logging.info('Downloaded.')
            os.system('screen -S minecraft -X stuff \'say ATTENTION: Server will shutdown temporarily to update in 30 seconds.^M\'')
            logging.info('Shutting down server in 30 seconds.')

            for i in range(20, 9, -10):
                time.sleep(10)
                os.system('screen -S minecraft -X stuff \'say Shutdown in ' + str(i) + ' seconds^M\'')

            for i in range(9, 0, -1):
                time.sleep(1)
                os.system('screen -S minecraft -X stuff \'say Shutdown in ' + str(i) + ' seconds^M\'')
            time.sleep(1)

            logging.info('Stopping server.')
            os.system('screen -S minecraft -X stuff \'stop^M\'')
            time.sleep(5)
            logging.info('Backing up world...')

            if not os.path.exists(BACKUP_DIR):
                os.makedirs(BACKUP_DIR)

            backupPath = os.path.join(
                BACKUP_DIR,
                "world" + "_backup_" + datetime.now().isoformat().replace(':', '-') + "_sha=" + cur_ver)
            shutil.copytree("../world", backupPath)

            logging.info('Backed up world.')
            logging.info('Updating server .jar')

            if os.path.exists('../minecraft_server.jar'):
                os.remove('../minecraft_server.jar')

            os.rename('minecraft_server.jar', '../minecraft_server.jar')
            logging.info('Starting server...')
            os.chdir("..")
            os.system('screen -S minecraft -d -m java -Xms' + RAM_INITIAL + ' -Xmx' + RAM_MAX + ' -jar minecraft_server.jar')

        else:
            logging.info('Server is already up to date.')

        break

