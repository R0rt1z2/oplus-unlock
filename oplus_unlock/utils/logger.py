import datetime

LOGGING_LEVELS = {
    "0": "[*]", # Unknown (Default)
    "1": "[?]", # Info
    "2": "[!]", # Warning
    "3": "[-]", # Error
    "4": "[+]", # Success
}

class Logger:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def log(self, buf, prio = 0):
        if (prio := str(prio)) in LOGGING_LEVELS:
            line = f"{LOGGING_LEVELS[prio]}: " + buf
        else:
            line = LOGGING_LEVELS["0"] + buf

        print(line)

    def die(self, msg, ecl):
        self.log(f"{msg}", ecl)
        exit(ecl)