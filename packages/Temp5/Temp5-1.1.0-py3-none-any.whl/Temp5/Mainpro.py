# In the name of God
# Main Program Start
#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Allimp import *
import locale

from Config.Init import *
import GUI.window2 as window2
import GUI.Start as Strt


class mainApp(wx.App):

    def OnInit(self):
        self.locale = None
        wx.Locale.AddCatalogLookupPathPrefix(LOCALE_PATH)
        self.config = self.GetConfig()
        lang = self.config.Read("Language")
        langu_dic = LANGUAGE_LIST

        self.UpdateLanguage(langu_dic[int(lang)])
        self.SetAppName('Temp5')
        if self.config.Read('Splash') != '':
            splash = Strt.MySplashScreen(window2)
            splash.Show(True)
        else:
            frame = window2.MainWin()
            if self.config.Read('WinSize') != '(-1, -1)':
                SIZE = wx.Size(eval(self.config.Read(u'WinSize')))
            else:
                SIZE = (wx.GetDisplaySize()[0],wx.GetDisplaySize()[1]-30)
            frame.SetSize(SIZE)
            frame.SetPosition((0,0))
            #frame.EnableFullScreenView(True)
            frame.Show()
        return True

    def GetConfig(self):
        config = wx.FileConfig(appName='Temp5',localFilename=CONFIG_PATH+'option.ini',globalFilename=CONFIG_PATH+'system1.ini')
        return config

    def UpdateLanguage(self, lang):
        supportedLangs = {"English": wx.LANGUAGE_ENGLISH,
                          "Farsi": wx.LANGUAGE_FARSI,
                          "French": wx.LANGUAGE_FRENCH,
                          "German": wx.LANGUAGE_GERMAN,
                          "Spanish": wx.LANGUAGE_SPANISH,
                          "Turkish": wx.LANGUAGE_TURKISH,
                          }
        if self.locale:
            assert sys.getrefcount(self.locale) <= 2
            del self.locale
        if supportedLangs[lang]:
            self.locale = wx.Locale(supportedLangs[lang])
            if self.locale.IsOk():
                self.locale.AddCatalog("Temp5fa")
                # self.locale.AddCatalog("Temp5fr")
                self.locale.AddCatalog("Temp5de")
                # self.locale.AddCatalog("Temp5sp")
                self.locale.AddCatalog("Temp5tr")
            else:
                self.locale = None
        else:
            wx.MessageBox("Language support not found please sending an email to us for update new language!")


def main(argv):
    #print(argv)
    if len(argv) > 0:
        if argv[0] == '-c':
            app = mainApp()
    else:
        app = mainApp(redirect=True)
        locale.setlocale(locale.LC_ALL, '')
    app.MainLoop()


if __name__ == '__main__':
    main(sys.argv[1:])
