class Logger:
    LOGGING_LEVELS = {
        0: "[*]", # Unknown (Default)
        1: "[?]", # Info
        2: "[!]", # Warning
        3: "[-]", # Error
        4: "[+]", # Success
        5: "[~]", # Debug
    }

    def __init__(self, debug = False):
        self.debug = debug

    def log(self, buf, prio = 0):
        if prio == 5 and not self.debug:
            return

        line = f"{self.LOGGING_LEVELS.get(prio, self.LOGGING_LEVELS[0])}: {buf}"
        print(line)

    def die(self, msg, ecl):
        self.log(f"{msg}", ecl)
        exit(ecl)