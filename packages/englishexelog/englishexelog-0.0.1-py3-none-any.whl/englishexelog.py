def log(status, text):
    f = open("Log.log", "a")
    f.write("\n")
    f.write(f"[ {status} ] {text}")
    f.close()


def logfile(status, text, file):
    f = open(file, "a")
    f.write("\n")
    f.write(f"[ {status} ] {text}")
    f.close()


def logadd(add, status, text):
    f = open("Log.log", "a")
    f.write("\n")
    f.write(f"[ {add} ][ {status} ] {text}")
    f.close()


def logaddfile(add, status, text, file):
    f = open(file, "a")
    f.write("\n")
    f.write(f"[ {add} ][ {status} ] {text}")
    f.close()


def wipe(file):
    f = open(file, "w")
    f.write("")
    f.close()