from datetime import datetime, timedelta


class Timer:
    def __init__(self, tick):
        self.tick, self.last = tick, datetime.now() - timedelta(seconds=tick)

    def tk(self):
        if (datetime.now() - self.last) > timedelta(seconds=self.tick):
            self.last = datetime.now()
            return True
        return False