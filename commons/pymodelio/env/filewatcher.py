import time
import threading

class FileWatcher(object):
    def __init__(self, sleepInterval = 1):
        self.filesWatched = {}
        self.doWatch = False
        self.sleepInterval = sleepInterval
        self.watchThread = None

    def watchFile(self, fileName, handler):
        if fileName not in self.filesWatched:
            self.filesWatched[fileName] = []
        if handler not in self.filesWatched[fileName]:
            self.filesWatched[fileName].append(handler)
        if self.watchThread is None:
            self.start()

    def start(self):
        self.doWatch = True
        self.watchThread = \
            threading.Thread(target=lambda: self.__watchLoop()).start()
        self.watchThread = None

    def stop(self):
        self.doWatch = False

    #--------------------------------------------------------------------------
    #  Implementation
    #--------------------------------------------------------------------------

    def __watchLoop(self):
        loop = 0
        while self.doWatch:
            loop += 1
            for (fileName,handlers) in self.filesWatched.items():
                modifications = self.__checkFileModifications(fileName)
                if modifications is not None:
                    for handler in handlers:
                        handler(modifications)
            time.sleep(self.sleepInterval)

    def __checkFileModifications(self, fileName):
        try:
            with open(fileName, "r+") as f:
                data = f.read()
                f.seek(0)
                f.truncate()
            if len(data) > 0:
                return data
            else:
                return None
        except Exception as e:
            print 'ERROR: %s' % e
            return None

