import hashlib as _hashlib
import os as _os
import string
from typing import Callable as _Callable


class FileInfo:
    """
    example case: a/b/test.exe\n
    - filename      = test\n
    - fileExtension = .exe\n
    - tail          = a/b/\n
    - head          = test.exe\n
    - rawPath       = a/b/test.exe\n

    - If no match can be found for any property, they will default to empty string
    """

    tail = ""
    '''example case: a/b/test.exe -> a/b/'''
    head = ""
    '''example case: a/b/test.exe -> test.exe'''
    filename = ""
    '''example case: a/b/test.exe -> test'''
    fileExtension = ""
    '''example case: a/b/test.exe -> .exe'''
    rawPath = ""
    '''example case: a/b/test.exe -> a/b/test.exe'''

    def __init__(self, filepath) -> None:
        self.rawPath = filepath
        headTail = _os.path.split(filepath)
        self.tail = headTail[0]
        if self.tail != "":
            self.tail += "/"
        self.head = headTail[1]
        baseName = headTail[1]

        fullFilename = baseName.rsplit(".", 1)
        self.filename = fullFilename[0]
        if len(fullFilename) == 2:
            self.fileExtension = "." + fullFilename[1]


def Hash(filePath: str, hashFunc=_hashlib.sha256()) -> str:
    import SimpleWorkspace.Enums.ByteEnum
    Read(filePath, lambda x: hashFunc.update(x), readSize=SimpleWorkspace.Enums.ByteEnum.MB.value * 1, getBytes=True)
    return hashFunc.hexdigest()

def Read(filePath: str, callback: _Callable[[str | bytes], None] = None, readSize=-1, readLimit=-1, getBytes=False, normalizeLineEndings=True) -> (str | bytes | None):
    """
    :callback:
        the callback is triggered each time a file is read with the readSize, \n
        callback recieves one parameter as bytes or str depending on getBytes param
    :readSize: amount of bytes to read at each callback, default of -1 reads all at once\n
    :ReadLimit: Max amount of bytes to read, default -1 reads until end of file\n
    :getBytes: specifies if the data returned is in string or bytes format\n
    :NormalizeLineEndings: default True, if getBytes is false aka reading as string, then change \\r\\n to \\n \n

    :Returns
        if no callback is used, the filecontent will be returned\n
        otherwise None
    """
    from io import BytesIO, StringIO

    content = BytesIO()
    if not getBytes:
        content = StringIO()

    if (readSize == -1 and readLimit >= 0) or (readLimit < readSize and readLimit >= 0):
        readSize = readLimit

    openMode = "rb"
    totalRead = 0
    with open(filePath, openMode) as fp:
        while True:
            if readLimit != -1 and totalRead >= readLimit:
                break
            data = fp.read(readSize)
            totalRead += readSize
            if data:
                if not getBytes:
                    data = data.decode('utf-8', 'replace')
                    if normalizeLineEndings:
                        data = data.replace("\r\n", "\n")
                if callback is None:
                    content.write(data)
                else:
                    callback(data)
            else:
                break

    if callback is None:
        return content.getvalue()
    return None


    
def Create(filepath: str, data: bytes | str = None):
    if type(data) is str:
        data = data.encode()
    with open(filepath, "wb") as file:
        if data is not None:
            file.write(data)

def Append(filepath: str, data: bytes | str):
    if type(data) is bytes:
        pass  # all good
    elif type(data) is str:
        data = data.encode()
    else:
        raise Exception("Only bytes or string can be used to append to file")
    with open(filepath, "ab") as file:
        file.write(data)


def CleanInvalidNameChars(filename:str, allowedCharset = string.ascii_letters + string.digits + " .-_"):
    return ''.join(c for c in filename if c in allowedCharset)

def IsPossiblyBinary(filepath):
    textchars = bytearray([7,8,9,10,12,13,27]) + bytearray(range(0x20, 0x7f)) + bytearray(range(0x80, 0x100))
    is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))

    text = Read(filepath, readLimit=1024, getBytes=True)
    return is_binary_string(text)