from urllib import urlopen, urlretrieve
import json
import os
import time
import shutil
import hashlib
import time

def log(string, logfile):
    print(string)
    logfile.write(string + "\n")


updateToSnapShot = False

os.chdir(os.path.dirname(os.path.abspath(__file__)))
url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
response = urlopen(url)
res = response.read()
data = json.loads(res.decode('UTF-8'))

if updateToSnapShot:
    minecraft_ver = data['latest']['snapshot']
else:
    minecraft_ver = data['latest']['release']

logFile = open("update.log", "a+")

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
        jarres = urlopen(jsonlink).read()
        jardata = json.loads(jarres.decode('UTF-8'))
        jarsha = jardata['downloads']['server']['sha1']

        log('Your sha1 is ' + cur_ver + '. Latest version is ' + str(minecraft_ver) + " with sha1 of " + jarsha, logFile)

        if cur_ver != jarsha:
            log('Updating Server', logFile)
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
            time.sleep(5)
            log('Backing up world', logFile)
            if not os.path.exists("world_backups"):
                os.makedirs("world_backups")

            backupPath = "world_backups/world" +"_backup_" + str(int(time.time()/1000)) + "_sha=" + cur_ver
            shutil.copytree("../world", backupPath)

            log('Backed up world\nUpdating server jar', logFile)
            if os.path.exists('../minecraft_server.jar'):
                os.remove('../minecraft_server.jar')

            os.rename('minecraft_server.jar', '../minecraft_server.jar')
            log('Starting server', logFile)
            logFile.close()
            os.chdir("..")
            os.system('screen -S minecraft -d -m java -Xmx5120M -Xms5120M -jar minecraft_server.jar')

        else:
            log('You are up to date', logFile)
            logFile.close()

        break

