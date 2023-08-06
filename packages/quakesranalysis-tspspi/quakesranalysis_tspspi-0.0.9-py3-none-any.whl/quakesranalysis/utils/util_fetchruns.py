import paramiko
import sys
import os
import json
import textwrap

import datetime

from pathlib import Path

def printUsage():
    print(textwrap.dedent("""
        Usage: {} [OPTIONS] FROMDATE [TODATE]

        Fetches all NPZ and run files from QUAK/ESR runs from the configured
        measurement directory that are taken since the specified dates and times.
        If no end date is specified all runs starting from the given timestamp will
        be fetched.

        The date and timestamps can be supplied either as

        \tYYYYMMDD
        \t\tWhen addressing a whole day
        \tYYYYMMDDHHMMSS
        \t\tWhen adressing a given date and time

        Options:
        \t--outdir DIRECTORY
        \t\tWrite all fetched NPZs into the specified output directory
        \t--list
        \t\tAlso write a list of fetched NPZs onto standard output to be passed
        \t\tto an analysis tool
        \t--sshkey KEYFILE
        \t\tSpecified the SSH keyfile to use. It's assumed to be a passwordless (!)
        \t\tkeyfile ...
    """.format(sys.argv[0])))

def transferStatusDisplay(bytesTransferred, bytesTotal):
    print(f"{bytesTransferred} out of {bytesTotal} bytes transferred", end = "\r")

def loadConfig():
    try:
        with open(os.path.join(Path.home(), ".config/quakesranalysis/datarepo.conf")) as cfgFile:
            return json.load(cfgFile)
    except FileNotFoundError:
        return { }

def configurationDefault():
    return {
        "writeList" : False,
        "outDir" : None,
        "strFromDate" : None,
        "strToDate" : None,

        "sshkeyfile" : None,

        "sshhost" : None,
        "sshuser" : None,
        "sshmeasurementsdatadir" : None,
        "sshmeasurementsdir" : None,
    }

def dtstringToDatetime(dstr):
    if dstr is None:
        return None

    dstr = dstr.strip()

    try:
        if len(dstr) == 8:
            year = int(dstr[0:4])
            month = int(dstr[4:6])
            day = int(dstr[6:])
            return datetime.datetime(year, month, day, 0, 0, 0)
        elif len(dstr) == 14:
            year = int(dstr[0:4])
            month = int(dstr[4:6])
            day = int(dstr[6:8])
            hour = int(dstr[8:10])
            minute = int(dstr[10:12])
            second = int(dstr[12:])
            return datetime.datetime(year, month, day, hour, minute, second)
    except ValueError:
        print(f"Invalid timestamp format {dstr}")
        sys.exit(1)

    return None
    

def main():
    # Create default configuration
    cfg = configurationDefault()

    # Load configuration and merge into cfg
    cfg = { **cfg, ** loadConfig() }

    if len(sys.argv) < 2:
        printUsage()
        sys.exit(0)

    i = 1
    while i < len(sys.argv):
        if sys.argv[i].strip() == "--outdir":
            if i == (len(sys.argv) - 1):
                print("Error: Missing output directory after --outdir")
                print("\n")
                printUsage()
                sys.exit(1)
            cfg["outDir"] = sys.argv[i+1]

            # Check output directory exists
            if not os.path.isdir(cfg["outDir"]):
                print(f"Output directory {cfg['outDir']} not found")
                print("\n")
                printUsage()
                sys.exit(1)

            i = i + 2
            continue

        if sys.argv[i].strip() == "--keyfile":
            if i == (len(sys.argv) - 1):
                print("Error: Missing keyfile name after --keyfile")
                print("\n")
                printUsage()
                sys.exit(1)
            cfg["sshkeyfile"] = sys.argv[i+1]

            if not os.path.isfile(cfg["sshkeyfile"]):
                print(f"Keyfile {cfg['sshkeyfile']} not found")
                print("\n")
                printUsage()
                sys.exit(1)
            i = i + 2
            continue

        if sys.argv[i].strip() == "--list":
            cfg["writeList"] = True
            i = i + 1
            continue

        # This is either the FROM or the TO date.
        if cfg["strFromDate"] is None:
            cfg["strFromDate"] = sys.argv[i].strip()
            i = i + 1
            continue
        elif cfg["strToDate"] is None:
            cfg["strToDate"] = sys.argv[i].strip()
            i = i + 1
            continue
        else:
            print("Can only supply one FROM and TO date, not three or more")

        print(f"Unknown option {sys.argv[i]}")
        print("\n")
        printUsage()
        sys.exit(1)

    dtfrom = dtstringToDatetime(cfg["strFromDate"])
    dtto = dtstringToDatetime(cfg["strToDate"])

    # Fetch file list and determine which files to fetch ...
    # Load SSH Key

    if cfg["sshkeyfile"] is None:
        print("Missing SSH keyfile for authentication")
        printUsage()
        sys.exit(1)

    sshkey = paramiko.RSAKey.from_private_key_file(cfg["sshkeyfile"])

    # We automatically add host keys when they are unknown (only error on conflicting key)
    sshClient = paramiko.SSHClient()
    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to storage repository
    sshClient.connect(
        cfg["sshhost"],
        username = cfg["sshuser"],
        pkey = sshkey
    )
    sftpClient = sshClient.open_sftp()

    transfersrc = []
    transferdest = []

    for f in sftpClient.listdir_iter(path = cfg["sshmeasurementsdatadir"], read_aheads = 250):
        if str(f.filename).endswith(".npz") or str(f.filename).endswith("_run.txt"):
            if "autosave" in str(f.filename):
                # Ignore autosave files
                continue

            # Now check if the filename embedded YYYY MM DD matches our from / to pattern ...
            sfn = str(f.filename)
            if len(sfn) < 20:
                continue

            try:
                year = int(sfn[0:4])
                month = int(sfn[5:7])
                day = int(sfn[8:10])
                hour = int(sfn[11:13])
                minute = int(sfn[14:16])
                second = int(sfn[17:19])
            except ValueError as e:
                pass

            dtFile = datetime.datetime(year, month, day, hour, minute, second)

            # Check if we are in range ...
            if (dtFile >= dtfrom) and ((dtto is None) or (dtFile <= dtto)):
                # We want to copy that file
                if cfg["outDir"] is not None:
                    dstname = os.path.join(cfg["outDir"], str(f.filename))
                else:
                    dstname = str(f.filename)

                sourceName = os.path.join(cfg['sshmeasurementsdatadir'], f.filename)

                transfersrc.append(sourceName)
                transferdest.append(dstname)

    for isrc, srcfile in enumerate(transfersrc):
        sourceName = srcfile
        dstname = transferdest[isrc]

        if cfg["writeList"]:
            print(dstname)
            callback = None 
        else:
            print(dstname)
            callback = transferStatusDisplay

            sftpClient.get(sourceName, dstname, callback = callback)
            print("")



    sftpClient.close()
    sshClient.close()


if __name__ == "__main__":
    main()
