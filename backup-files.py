# Sync of files - DONE
# Sync should be one way - DONE
# Sync should be done periodically - DONE
# File manipulation should be logged to file and console - CONSOLE
# Folder paths, interval and log path should be configurable via args - DONE
# Folder sync should not use 3th party library - DONE
# Other things can be via libraries - DONE

import sys
import os
import shutil
import time

class main:
    def __init__(self):
        # Args: Path to sync, Synced path, Interval, Log
        try:
            self.args = sys.argv
            self.src = sys.argv[1]
            self.dst = sys.argv[2]
            self.interval = int(sys.argv[3])
            self.log = sys.argv[4]
        except IndexError:
            # Error with missing parameters
            print('No parameters given! Parameters should be: Sync folder path, Syndec folder, Interval, Log file.')

    def run(self):
        while True:
            print('1')
            try:
                src_d = os.listdir(self.src)
                src_d.sort()
                dst_d = os.listdir(self.dst)
                dst_d.sort()

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
                                shutil.copy2(self.src + src_d[i],self.dst + src_d[i])
                                print('File copied because file difference '+ self.src + src_d[i] + ' to ' + self.dst + '!')
                        else:
                            # If there s missing file, then copy new one
                            shutil.copy2(self.src + src_d[i],self.dst + src_d[i])
                            print('File copied because they are missing '+ self.src + src_d[i] + ' to ' + self.dst + '!')
                    except IndexError:
                        pass
                    try:
                        if dst_d[i] not in src_d:
                            # if there s file which doesnt belong there then delete it
                            print('File deleted ' + self.dst + dst_d[i])
                            os.remove(self.dst + dst_d[i])
                    except IndexError:
                        pass
            except AttributeError:
                # Pass because duplicate error
                pass
            time.sleep(self.interval)

if __name__ == '__main__':
    main = main()
    main.run()