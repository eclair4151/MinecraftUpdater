from urllib import urlopen, urlretrieve
import json
import os
import time
import shutil


def log(string, logfile):
    print(string)
    logfile.write(string + "\n")


updateToSnapShot = True

url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
response = urlopen(url)
res = response.read()
data = json.loads(res.decode('UTF-8'))

if updateToSnapShot:
    minecraft_ver = data['latest']['snapshot']
else:
    minecraft_ver = data['latest']['release']


if not os.path.isfile('version.txt'): #create version file if it does not exist
    open('version.txt', 'w')

versionFile = open('version.txt', 'r+')
logFile = open("update.log", "a+")
cur_ver = versionFile.read()
if cur_ver == "":
    cur_ver = "init"
log('Your version is ' + cur_ver + '. Latest version is ' + str(minecraft_ver), logFile)

if cur_ver != minecraft_ver:
    log('Updating Server', logFile)
    for version in data['versions']:
        if version['id'] == minecraft_ver:
            jsonlink = version['url']
            jarres = urlopen(jsonlink).read()
            jardata = json.loads(jarres.decode('UTF-8'))
            link = jardata['downloads']['server']['url']
            log('Downloading jar from ' + link, logFile)
            urlretrieve(link, 'minecraft_server.jar')
            log('Downloaded', logFile)
            os.system('screen -S minecraft -X stuff \'say ATTENTION: Server will shutdown for 1 minutes to update in 30 seconds.^M\'')
            log('Shutdown in 30 seconds', logFile)

            for i in range(20, 9, -10):
                time.sleep(10)
                os.system('screen -S minecraft -X stuff \'say Shutdown in ' + str(i) + ' seconds^M\'')

            for i in range(9, 0, -1):
                time.sleep(1)
                os.system('screen -S minecraft -X stuff \'say Shutdown in ' + str(i) + ' seconds^M\'')
            time.sleep(1)

            log('Stopping server', logFile)
            os.system('screen -S minecraft -X stuff \'stop^M\'')
            time.sleep(5) #sleep for 5 seconds to allow for server to shutdown. Adjust if your server is modded and needs more time

            log('Backing up world', logFile)
            if not os.path.exists("world_backups"):
                os.makedirs("world_backups")

            if os.path.exists("world_backups/world" +"_backup_" + cur_ver):
                shutil.rmtree("world_backups/world" +"_backup_" + cur_ver)

            shutil.copytree("../world", "world_backups/world" +"_backup_" + cur_ver)

            log('Backed up world\nUpdating server jar', logFile)
            if os.path.exists('../minecraft_server.jar'):
                os.remove('../minecraft_server.jar')

            os.rename('minecraft_server.jar', '../minecraft_server.jar')
            log('Updating version file', logFile)
            logFile.write('Updating version file\n')
            versionFile.seek(0)
            versionFile.write(minecraft_ver)
            versionFile.truncate()
            log('Starting server', logFile)
            logFile.close()
            versionFile.close()
            os.chdir("..")
            os.system('screen -S minecraft -d -m java -Xmx5120M -Xms5120M -jar minecraft_server.jar')
            break

else:
    log('You are to date', logFile)
    logFile.close()
    versionFile.close()


