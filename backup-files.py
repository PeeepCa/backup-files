# Backup-files

# Application just checking source folder if there s any new file or if there s any file which has changes
# in comparison to second folder
# App checking the creation time and date to compare files
# if there s any change in destination folder it ll automaticly revert changes to actual one
# Interval is implemented just by adding sleep
# App can be improved by multithreading in future, but it depends on future testing
# Multithreading, can improve logging performance
# Theres possibility to add UI as well

import sys
import os
from time import sleep
from shutil import copy2
from datetime import datetime

class main:
    def __init__(self):
        # Args: Path to sync, Synced path, Interval, Log
        try:
            self.src = sys.argv[1]
            self.dst = sys.argv[2]
            self.interval = int(sys.argv[3])
            self.log = sys.argv[4]
            print('Parameters are:\nSource path: ' + self.src + '\nDestination path: ' + self.dst + '\nInterval: ' + str(self.interval) + 's\nLog path: ' + sys.argv[4] + '\nApp started at: ' + self.timeStmp())
            self.logHandler(self.timeStmp() + ' Application started with parameters:\nSource path: ' + self.src + '\nDestination path: ' + self.dst + '\nInterval: ' + str(self.interval) + 's\nLog path: ' + sys.argv[4])
        except IndexError:
            # Error with missing parameters
            print('No parameters given! Parameters should be: Sync folder path, Syndec folder, Interval, Log file.')

    def logHandler(self, content):
        # Log handler
        self.config = open(self.log, 'a')
        self.config.write(content + '\n')
        self.config.close()

    def timeStmp(self):
        # Timestamp for logging
        actualTime = datetime.now()
        actualTime = actualTime.strftime('%d/%m/%Y, %H:%M:%S')
        return actualTime

    def run(self):
        # Main loop for backup service
        while True:
            print('Alive')
            try:
                src_d = os.listdir(self.src)
                src_d.sort()
                dst_d = os.listdir(self.dst)
                dst_d.sort()

                # Added because one or second folder can have different number of files in
                if len(src_d) < len(dst_d):
                    size = len(dst_d)
                else:
                    size = len(src_d)
                for i in range(size):
                    try:
                        if src_d[i] in dst_d:
                            if os.stat(self.src + src_d[i]).st_mtime == os.stat(self.dst + src_d[i]).st_mtime:
                                # If files are synced, do nothing
                                continue
                            else:
                                # If source file was different then copy new one
                                copy2(self.src + src_d[i],self.dst + src_d[i])
                                print('File copied because file difference '+ self.src + src_d[i] + ' to ' + self.dst + '!')
                                self.logHandler(self.timeStmp() + ' File copied because file difference '+ self.src + src_d[i] + ' to ' + self.dst)
                        else:
                            # If there s missing file, then copy new one
                            copy2(self.src + src_d[i],self.dst + src_d[i])
                            print('File copied because they are missing '+ self.src + src_d[i] + ' to ' + self.dst + '!')
                            self.logHandler(self.timeStmp() + ' File copied because they are missing '+ self.src + src_d[i] + ' to ' + self.dst)
                    except IndexError:
                        pass
                    except PermissionError:
                        print('File ' + src_d[i] + ' cannot be copied')
                        self.logHandler(self.timeStmp() + ' File ' + src_d[i] + ' cannot be copied')
                        continue
                    
                    try:
                        if dst_d[i] not in src_d:
                            # if there s file which doesnt belong there then delete it
                            os.remove(self.dst + dst_d[i])
                            print('File deleted ' + self.dst + dst_d[i])
                            self.logHandler(self.timeStmp() + ' File deleted ' + self.dst + dst_d[i])
                    except IndexError:
                        pass
            except AttributeError:
                # Pass because duplicate error
                pass
            sleep(self.interval)

if __name__ == '__main__':
    main = main()
    main.run()