from logging import Logger as _Logger
from SimpleWorkspace.SettingsProviders import SettingsManager_JSON as _SettingsManager_JSON

class App:
    appName = None
    appCompany = None
    appTitle = None #example: "appname - appcompany"
    appHash = 0 #appname + appcompany hashed together, numeric hash
    path_currentAppData = ""            #windows example: 'C:\\Users\\username\\AppData\\Roaming\\AppCompany\\AppName'
    path_currentAppData_storage = None  #windows example: 'C:\\Users\\username\\AppData\\Roaming\\AppCompany\\AppName\\Storage'

    _loggerFilepath = None
    logger = None #type: _Logger
    settingsManager = None #type: _SettingsManager_JSON

    @staticmethod
    def Setup(appName, appCompany=None, extraIdentifier=None):
        '''
        @param extraIdentifier: used for creating a more unique apphash to identify this program, will be bundled with appName and appCompany
        '''
        import os
        import SimpleWorkspace.IO
        from SimpleWorkspace.LogProviders import RotatingFileLogger

        App.appName = appName
        App.appCompany = appCompany
        App.appTitle = appName
        if appCompany is not None:
            App.appTitle += " - " + appCompany
        
        App.appHash = hash((appName, appCompany, extraIdentifier))

        App.path_currentAppData = SimpleWorkspace.IO.Path.GetAppdataPath(appName, appCompany)
        App.path_currentAppData_storage = os.path.join(App.path_currentAppData, "storage")
        SimpleWorkspace.IO.Directory.Create(App.path_currentAppData_storage)
        
        App._loggerFilepath = os.path.join(App.path_currentAppData, "info.log")
        App.logger = RotatingFileLogger.GetLogger( App._loggerFilepath)

        App.settingsManager = _SettingsManager_JSON(os.path.join(App.path_currentAppData, "config.json"))
        App.settingsManager.LoadSettings()
        return