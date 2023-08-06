import os as _os
import string

def FindEmptySpot(filepath: str):
    from SimpleWorkspace.IO.File import FileInfo

    fileContainer = FileInfo(filepath)
    TmpPath = filepath
    i = 1
    while _os.path.exists(TmpPath) == True:
        TmpPath = f"{fileContainer.tail}{fileContainer.filename}_{i}{fileContainer.fileExtension}"
        i += 1
    return TmpPath

def GetAppdataPath(appName=None, companyName=None):
    """
    Retrieves roaming Appdata folder.\n
    no arguments        -> %appdata%/\n
    appName only        -> %appdata%/appname\n
    appname and company -> %appdata%/appname/companyName\n
    """
    from SimpleWorkspace.ExtLibs import appdirs

    return appdirs.user_data_dir(appName, companyName, roaming=True)


