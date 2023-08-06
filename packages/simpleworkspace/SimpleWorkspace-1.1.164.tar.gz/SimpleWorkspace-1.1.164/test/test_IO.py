import hashlib
import os
import SimpleWorkspace as sw
from SimpleWorkspace.IO.File import FileInfo
from BaseTestCase import BaseTestCase 



class IO_FileTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.testPath_samples = cls.testPath + "/FileSamples"
        cls.testPath_samples_byteTestFile = cls.testPath_samples + "/byteTestFile.bin"
        cls.testPath_samples_byteTestFile_content = b""
        cls.testPath_samples_textTestFile = cls.testPath_samples + "/textTestFile.txt"
        cls.testPath_samples_textTestFile_content = "1234567890"
        cls.testPath_samples_nestedFolder = cls.testPath_samples + "/nestedTest"
        cls.testPath_samples_nestedFolder_folderCount = 15
        cls.testPath_samples_nestedFolder_textFileCount = 6
        cls.testPath_samples_nestedFolder_binaryFileCount = 5
        cls.testPath_samples_nestedFolder_allFileCount = cls.testPath_samples_nestedFolder_textFileCount + cls.testPath_samples_nestedFolder_binaryFileCount
        cls.testPath_samples_nestedFolder_entryCount = cls.testPath_samples_nestedFolder_folderCount + cls.testPath_samples_nestedFolder_allFileCount
        cls.testPath_samples_nestedFolder_fileContentText = "1234567890"
        cls.testPath_samples_nestedFolder_fileContentBin = b"12\x004567890"
        cls.testPath_samples_nestedFolder_totalFileSize = cls.testPath_samples_nestedFolder_allFileCount * len(cls.testPath_samples_nestedFolder_fileContentText)


    def GenerateSampleFiles(self):
        sw.IO.Directory.Create(self.testPath_samples)
        sw.IO.Directory.Create(self.testPath_samples_nestedFolder + "/tree1/sub1/sub2/sub3")
        sw.IO.Directory.Create(self.testPath_samples_nestedFolder + "/tree1/sub1/splitsub2/sub3")
        sw.IO.Directory.Create(self.testPath_samples_nestedFolder + "/tree2/sub1/sub2/sub3")
        sw.IO.Directory.Create(self.testPath_samples_nestedFolder + "/tree3/sub1/sub2/sub3")
        sw.IO.Directory.Create(self.testPath_samples_nestedFolder + "/tree3/sub1/sub2/splitsub3")
        sw.IO.File.Create(self.testPath_samples_nestedFolder + "/tree1/sub1/splitsub2/sub3/sample1.txt", self.testPath_samples_nestedFolder_fileContentText)
        sw.IO.File.Create(self.testPath_samples_nestedFolder + "/tree1/sub1/sub2/sub3/sample1.txt", self.testPath_samples_nestedFolder_fileContentText)
        sw.IO.File.Create(self.testPath_samples_nestedFolder + "/tree1/sub1/sub2/sample1.txt", self.testPath_samples_nestedFolder_fileContentText)
        sw.IO.File.Create(self.testPath_samples_nestedFolder + "/tree1/sub1/sample1.txt", self.testPath_samples_nestedFolder_fileContentText)
        sw.IO.File.Create(self.testPath_samples_nestedFolder + "/tree1/sample1.txt", self.testPath_samples_nestedFolder_fileContentText)
        sw.IO.File.Create(self.testPath_samples_nestedFolder + "/tree2/sub1/sub2/sub3/sample1.txt", self.testPath_samples_nestedFolder_fileContentText)
        sw.IO.File.Create(self.testPath_samples_nestedFolder + "/tree3/sub1/sub2/splitsub3/sample1.bin", self.testPath_samples_nestedFolder_fileContentBin)
        sw.IO.File.Create(self.testPath_samples_nestedFolder + "/tree3/sub1/sub2/sub3/sample1.bin", self.testPath_samples_nestedFolder_fileContentBin)
        sw.IO.File.Create(self.testPath_samples_nestedFolder + "/tree3/sub1/sub2/sample1.bin", self.testPath_samples_nestedFolder_fileContentBin)
        sw.IO.File.Create(self.testPath_samples_nestedFolder + "/tree3/sub1/sample1.bin", self.testPath_samples_nestedFolder_fileContentBin)
        sw.IO.File.Create(self.testPath_samples_nestedFolder + "/tree3/sample1.bin", self.testPath_samples_nestedFolder_fileContentBin)

        sw.IO.File.Create(self.testPath_samples_textTestFile, self.testPath_samples_textTestFile_content)
        for i in range(255):
            self.testPath_samples_byteTestFile_content += bytes(chr(i), "utf-8")
        for i in range(255):
            self.testPath_samples_byteTestFile_content += bytes(chr(i), "utf-8")
        sw.IO.File.Create(self.testPath_samples_byteTestFile, self.testPath_samples_byteTestFile_content)


    def setUp(self) -> None:
        super().setUp()
        self.GenerateSampleFiles()

    def test_FileContainer_GetsValidPaths(self):
        t0 = FileInfo("a/b/c.exe")
        t1 = FileInfo("a/b/c")
        t2 = FileInfo("a/b/.exe")
        t3 = FileInfo(".exe")
        t4 = FileInfo("c")
        t5 = FileInfo("c.exe")
        t6 = FileInfo(".")
        t7 = FileInfo("a.,-.asd/\\/b.,ca.asd/c.,..exe")

        self.assertTrue(t0.fileExtension == ".exe" and t0.filename == "c"    and t0.tail == "a/b/"                   and t0.head == "c.exe"     )
        self.assertTrue(t1.fileExtension == ""     and t1.filename == "c"    and t1.tail == "a/b/"                   and t1.head == "c"         )
        self.assertTrue(t2.fileExtension == ".exe" and t2.filename == ""     and t2.tail == "a/b/"                   and t2.head == ".exe"      )
        self.assertTrue(t3.fileExtension == ".exe" and t3.filename == ""     and t3.tail == ""                       and t3.head == ".exe"      )
        self.assertTrue(t4.fileExtension == ""     and t4.filename == "c"    and t4.tail == ""                       and t4.head == "c"         )
        self.assertTrue(t5.fileExtension == ".exe" and t5.filename == "c"    and t5.tail == ""                       and t5.head == "c.exe"     )
        self.assertTrue(t6.fileExtension == "."    and t6.filename == ""     and t6.tail == ""                       and t6.head == "."         )
        self.assertTrue(t7.fileExtension == ".exe" and t7.filename == "c.,." and t7.tail == "a.,-.asd/\\/b.,ca.asd/" and t7.head == "c.,..exe"  )

    def test_File_ReadsCorrectTypes(self):
        data = sw.IO.File.Read(self.testPath_samples_byteTestFile)
        self.assertIs(type(data), str)
        data = sw.IO.File.Read(self.testPath_samples_byteTestFile, callback=lambda x: self.assertEqual(type(x), str))
        self.assertIs(data, None)

        ##bytes##
        data = sw.IO.File.Read(self.testPath_samples_byteTestFile, getBytes=True)
        self.assertIs(type(data), bytes)
        data = sw.IO.File.Read(self.testPath_samples_byteTestFile, callback=lambda x: self.assertEqual(type(x), bytes), getBytes=True)
        self.assertIs(data, None)

    def test_Hash_GetsCorrectHash(self):
        originalHash = sw.IO.File.Hash(self.testPath_samples_byteTestFile, hashFunc=hashlib.sha256())

        #
        sha256 = hashlib.sha256()
        sha256.update(self.testPath_samples_byteTestFile_content)
        resultHash = sha256.hexdigest()
        self.assertEqual(originalHash,  resultHash)
        #
        sha256 = hashlib.sha256()
        sw.IO.File.Read(self.testPath_samples_byteTestFile, callback=sha256.update, getBytes=True)
        resultHash = sha256.hexdigest()
        self.assertEqual(originalHash,  resultHash)
        #
        sha256 = hashlib.sha256()
        sw.IO.File.Read(self.testPath_samples_byteTestFile, callback=sha256.update, readSize=100, getBytes=True)
        resultHash = sha256.hexdigest()
        self.assertEqual(originalHash,  resultHash)
        #
        sha256 = hashlib.sha256()
        sw.IO.File.Read(self.testPath_samples_byteTestFile, callback=sha256.update, readLimit=len(self.testPath_samples_byteTestFile_content), getBytes=True)
        resultHash = sha256.hexdigest()
        self.assertEqual(originalHash,  resultHash)

    def test_File_Reading_ReadsCorrect(self):
        data = sw.IO.File.Read(self.testPath_samples_textTestFile, readLimit=10, getBytes=False)
        self.assertEqual(data,  self.testPath_samples_textTestFile_content)

        #
        tmpList = []
        sw.IO.File.Read(self.testPath_samples_byteTestFile, callback=tmpList.append, readSize=50, readLimit=200, getBytes=True)
        self.assertEqual(len(tmpList), 4)
        self.assertEqual(len(tmpList[0]), 50)

        #
        tmpList = []
        sw.IO.File.Read(self.testPath_samples_byteTestFile, callback=lambda x: tmpList.append(x), readSize=50, getBytes=True)
        self.assertEqual(len(tmpList[0]),  50)

        #
        tmpList = []
        sw.IO.File.Read(self.testPath_samples_byteTestFile, callback=tmpList.append, readSize=50, readLimit=4, getBytes=True)
        self.assertEqual(len(tmpList), 1)
        self.assertEqual(len(tmpList[0]), 4)

        #
        tmpList = []
        sw.IO.File.Read(self.testPath_samples_byteTestFile, callback=tmpList.append, readSize=-1, readLimit=4, getBytes=True)
        self.assertEqual(len(tmpList[0]),  4)

    def test_Directories_ListsAll(self):
        fileSizes = []
        sw.IO.Directory.List(self.testPath_samples_nestedFolder, lambda x: fileSizes.append(os.path.getsize(x)), includeDirs=True)
        fileSize = 0
        for i in fileSizes:
            fileSize += i
        self.assertEqual(fileSize,  self.testPath_samples_nestedFolder_totalFileSize)

        #
        tmpList = []
        sw.IO.Directory.List(self.testPath_samples_nestedFolder, tmpList.append, includeDirs=False)
        self.assertEqual(len(tmpList),  self.testPath_samples_nestedFolder_allFileCount)

        #
        tmpList = []
        sw.IO.Directory.List(self.testPath_samples_nestedFolder, tmpList.append, includeDirs=True)
        self.assertEqual(len(tmpList),  self.testPath_samples_nestedFolder_entryCount)

    def test_Directories_ListsOnlyDirectories(self):
        #
        tmpList = sw.IO.Directory.List(self.testPath_samples_nestedFolder, includeDirs=False, includeFiles=False)
        self.assertEqual(len(tmpList),  0)

        #
        tmpList = sw.IO.Directory.List(self.testPath_samples_nestedFolder, includeDirs=True, includeFiles=False)
        self.assertEqual(len(tmpList),  self.testPath_samples_nestedFolder_folderCount)

    def test_Directories_ListsAll_maxDepth(self):

        #
        tmpList = []
        sw.IO.Directory.List(self.testPath_samples_nestedFolder, tmpList.append, includeDirs=False, maxRecursionDepth=9999)
        self.assertEqual(len(tmpList),  self.testPath_samples_nestedFolder_allFileCount)

        totalFilesInLevel1 = len(os.listdir(self.testPath_samples_nestedFolder))
        #
        tmpList = []
        sw.IO.Directory.List(self.testPath_samples_nestedFolder, tmpList.append, includeDirs=True, maxRecursionDepth=1)
        self.assertEqual(len(tmpList),  totalFilesInLevel1)

        totalFilesInLevel2 = totalFilesInLevel1
        for filename in os.listdir(self.testPath_samples_nestedFolder):
            totalFilesInLevel2 += len(os.listdir(os.path.join(self.testPath_samples_nestedFolder, filename)))

        sw.IO.Directory.List(self.testPath_samples_nestedFolder, tmpList.append, includeDirs=True, maxRecursionDepth=2)
        self.assertEqual(len(tmpList),  totalFilesInLevel2)

    def test_Directories_callbackFiltering_1(self):
        tmpList = []
        sw.IO.Directory.List(self.testPath_samples_nestedFolder, tmpList.append, includeFilter = lambda x: x.endswith(".txt") or x.endswith(".exe"))
        totalTxt = 0
        totalExe = 0
        for i in tmpList:
            fcon = FileInfo(i)
            if fcon.fileExtension == ".exe":
                totalExe += 1
            if fcon.fileExtension == ".txt":
                totalTxt += 1
        self.assertEqual(totalTxt,  self.testPath_samples_nestedFolder_textFileCount)
        self.assertEqual(totalExe,  0)

    def test_Directories_regexFiltering_1(self):
        tmpList = []
        sw.IO.Directory.List(self.testPath_samples_nestedFolder, tmpList.append, includeFilter=r"/\.(exe|txt)/i")
        totalTxt = 0
        totalExe = 0
        for i in tmpList:
            fcon = FileInfo(i)
            if fcon.fileExtension == ".exe":
                totalExe += 1
            if fcon.fileExtension == ".txt":
                totalTxt += 1
        self.assertEqual(totalTxt,  self.testPath_samples_nestedFolder_textFileCount)
        self.assertEqual(totalExe,  0)

    def test_Directories_regexFiltering_2(self):
        tmpList = []
        sw.IO.Directory.List(self.testPath_samples_nestedFolder, tmpList.append, includeFilter=r"/\.(bin)$/i")
        for path in tmpList:
            self.assertEqual(
                sw.IO.File.Read(path, getBytes=True),
                self.testPath_samples_nestedFolder_fileContentBin
            )
        self.assertEqual(len(tmpList),  self.testPath_samples_nestedFolder_binaryFileCount)

    def test_Directories_regexFiltering_3(self):
        tmpList = []
        sw.IO.Directory.List(self.testPath_samples_nestedFolder, tmpList.append, includeFilter=r"\.(nonexisting)$")
        self.assertEqual(len(tmpList),  0)

    def test_Directories_regexFiltering_AllFiles_1(self):
        tmpList = []
        sw.IO.Directory.List(self.testPath_samples_nestedFolder, tmpList.append, includeFilter=r"\.(bin|txt)$")
        self.assertEqual(len(tmpList),  self.testPath_samples_nestedFolder_allFileCount)

    def test_Directories_regexFiltering_AllFiles_1(self):
        tmpList = []
        sw.IO.Directory.List(self.testPath_samples_nestedFolder, tmpList.append, includeFilter=r"/.*/i")
        self.assertEqual(len(tmpList),  self.testPath_samples_nestedFolder_entryCount)

