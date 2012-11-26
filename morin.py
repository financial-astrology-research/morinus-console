
# -*- coding: utf-8 -*-

import wx
import os
import pickle
import Image
import astrology
import houses
import planets
import chart
import common
import graphchart
import graphchart2
import revolutions
import suntransits
import secdir
import transits
import personaldatadlg
import findtimedlg
import graphephemdlg
import appearance1dlg
import appearance2dlg
import dignitiesdlg
import colorsdlg
import primarydirsdlg
import primarydirsdlgsmall
import fortunedlg
import arabicpartsdlg
import fixstarsdlg
import triplicitiesdlg
import termsdlg
import decansdlg
import ayanamshadlg
import profdlg
import profections
import profectionsframe
import munprofections
import profectionstepperdlg
import proftabledlg
import profstableframe
import profectiontablestepperdlg
import almutenchartdlg
import almutentopicalsdlg
import almutentopicalsframe
import orbisdlg
import langsdlg
import symbolsdlg
import timespacedlg
import transitmdlg
import revolutionsdlg
import syzygydlg
import suntransitsdlg
import secdirdlg
import stepperdlg
import graphephemframe
import positionsframe
import squarechartframe
import almutenchartframe
import almutenzodsframe
import miscframe
import customerframe
import risesetframe
import speedsframe
import munposframe
import arabicpartsframe
import antisciaframe
import zodparsframe
import stripframe
import fixstarsframe
import fixstarsaspectsframe
import hoursframe
import midpointsframe
import aspectsframe
import transitmframe
import transitframe
import secdirframe
import electionsframe
import mundaneframe
import profdlgopts
import pdsinchartdlgopts
import pdsinchartterrdlgopts
import electionstepperdlg
import primdirslistframe
import primdirs
import primarykeysdlg
import primdirsrangedlg
import placidiansapd
import placidianutppd
import regiomontanpd
import campanianpd
import thread
import options
import util
import mtexts
import htmlhelpframe
import customerpd
import ephemcalc
import wx.lib.newevent
import math #solar precession

(PDReadyEvent, EVT_PDREADY) = wx.lib.newevent.NewEvent()
pdlock = thread.allocate_lock()


class MFrame(wx.Frame):

  def __init__(self, parent, id, title, opts):
    wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(640, 400))

    self.fpath = ''
    self.fpathhors = u'Hors'
    self.fpathimgs = u'Images'
    self.title = title
    self.origtitle = title
    self.hortitle = title
    
    self.options = opts

    common.common = common.Common()
    common.common.update(self.options)

    self.CenterOnScreen()
    self.SetMinSize((200,200))
    self.SetBackgroundColour(self.options.clrbackground)

    self.dirty = False

    menubar = wx.MenuBar()
    self.mhoros = wx.Menu()
    self.mtable = wx.Menu()
    self.moptions = wx.Menu()
    self.mcharts = wx.Menu()
    self.mhelp = wx.Menu()

    #Horoscope-menu
    self.ID_New, self.ID_Data, self.ID_Load, self.ID_Save, self.ID_SaveAsBitmap, self.ID_Synastry, self.ID_FindTime, self.ID_Ephemeris, self.ID_Close, self.ID_Exit = range(100, 110)

    #Table-menu
    (self.ID_Positions, self.ID_TAlmutens, self.ID_AlmutenZodiacal, self.ID_AlmutenChart, self.ID_AlmutenTopical, self.ID_Misc, self.ID_MunPos, 
    self.ID_Antiscia, self.ID_Aspects, self.ID_Midpoints, self.ID_RiseSet, self.ID_Speeds, self.ID_ZodPars, self.ID_FixStars, self.ID_FixStarsAsps, 
    self.ID_Arabians, self.ID_Strip, self.ID_PlanetaryHours, self.ID_ExactTransits, self.ID_Profections, self.ID_CustomerSpeculum, self.ID_PrimaryDirs) = range(110,132)

    #Charts-menu
    self.ID_Transits, self.ID_Revolutions, self.ID_SunTransits, self.ID_SecondaryDirs, self.ID_Elections, self.ID_SquareChart, self.ID_ProfectionsChart, self.ID_MundaneChart = range(140, 148)

    #Options-menu
    (self.ID_Appearance1, self.ID_Appearance2, self.ID_Symbols, self.ID_Dignities, self.ID_MinorDignities, self.ID_Triplicities, self.ID_Terms, 
    self.ID_Decans, self.ID_Almutens, self.ID_ChartAlmuten, self.ID_Topical, self.ID_Colors, self.ID_Ayanamsha, self.ID_HouseSystem, 
    self.ID_Nodes, self.ID_Orbs, self.ID_PrimaryDirsOpt, self.ID_PrimaryKeys, self.ID_PDsInChartOpt, self.ID_PDsInChartOptZod, self.ID_PDsInChartOptMun, self.ID_LotOfFortune, self.ID_ArabicParts, self.ID_Syzygy, self.ID_FixStarsOpt, self.ID_ProfectionsOpt, self.ID_Languages, self.ID_AutoSaveOpts, self.ID_SaveOpts, self.ID_Reload) = range(150, 180)

    self.ID_Housesystem1, self.ID_Housesystem2, self.ID_Housesystem3, self.ID_Housesystem4, self.ID_Housesystem5, self.ID_Housesystem6, self.ID_Housesystem7, self.ID_Housesystem8, self.ID_Housesystem9, self.ID_Housesystem10, self.ID_Housesystem11, self.ID_Housesystem12 = range(1050, 1062)

    self.ID_NodeMean = 1070
    self.ID_NodeTrue = 1071

    self.hsbase = 1050
    self.nodebase = 1070

    #Help-menu
    self.ID_Help = 180
    self.ID_About = 181

    #Horoscope-menu
    self.mhoros.Append(self.ID_New, mtexts.menutxts['HMNew'], mtexts.menutxts['HMNewDoc'])
    self.mhoros.Append(self.ID_Data, mtexts.menutxts['HMData'], mtexts.menutxts['HMDataDoc'])
    self.mhoros.Append(self.ID_Load, mtexts.menutxts['HMLoad'], mtexts.menutxts['HMLoadDoc'])
    self.mhoros.Append(self.ID_Save, mtexts.menutxts['HMSave'], mtexts.menutxts['HMSaveDoc'])
    self.mhoros.Append(self.ID_SaveAsBitmap, mtexts.menutxts['HMSaveAsBmp'], mtexts.menutxts['HMSaveAsBmpDoc'])
    self.mhoros.Append(self.ID_Synastry, mtexts.menutxts['HMSynastry'], mtexts.menutxts['HMSynastryDoc'])
    self.mhoros.Append(self.ID_FindTime, mtexts.menutxts['HMFindTime'], mtexts.menutxts['HMFindTimeDoc'])
    self.mhoros.Append(self.ID_Ephemeris, mtexts.menutxts['HMEphemeris'], mtexts.menutxts['HMEphemerisDoc'])
    self.mhoros.AppendSeparator()
    self.mhoros.Append(self.ID_Close, mtexts.menutxts['HMClose'], mtexts.menutxts['HMCloseDoc'])
    self.mhoros.AppendSeparator()
    self.mhoros.Append(self.ID_Exit, mtexts.menutxts['HMExit'], mtexts.menutxts['HMExitDoc'])

    self.filehistory = wx.FileHistory()
    self.filehistory.UseMenu(self.mhoros)
    self.Bind(wx.EVT_MENU_RANGE, self.OnFileHistory, id=wx.ID_FILE1, id2=wx.ID_FILE9)

    #Table-menu
    self.mtable.Append(self.ID_Positions, mtexts.menutxts['TMPositions'], mtexts.menutxts['TMPositionsDoc'])

    self.talmutens = wx.Menu()
    self.talmutens.Append(self.ID_AlmutenZodiacal, mtexts.menutxts['TMAlmutenZodiacal'], mtexts.menutxts['TMAlmutenZodiacalDoc'])
    self.talmutens.Append(self.ID_AlmutenChart, mtexts.menutxts['TMAlmutenChart'], mtexts.menutxts['TMAlmutenChartDoc'])
    self.talmutens.Append(self.ID_AlmutenTopical, mtexts.menutxts['TMAlmutenTopical'], mtexts.menutxts['TMAlmutenTopicalDoc'])
    self.mtable.AppendMenu(self.ID_TAlmutens, mtexts.menutxts['TMAlmutens'], self.talmutens)

    self.mtable.Append(self.ID_Misc, mtexts.menutxts['TMMisc'], mtexts.menutxts['TMMiscDoc'])
    self.mtable.Append(self.ID_MunPos, mtexts.menutxts['TMMunPos'], mtexts.menutxts['TMMunPosDoc'])
    self.mtable.Append(self.ID_Antiscia, mtexts.menutxts['TMAntiscia'], mtexts.menutxts['TMAntisciaDoc'])
    self.mtable.Append(self.ID_Aspects, mtexts.menutxts['TMAspects'], mtexts.menutxts['TMAspectsDoc'])
    self.mtable.Append(self.ID_Midpoints, mtexts.menutxts['TMMidpoints'], mtexts.menutxts['TMMidpointsDoc'])
    self.mtable.Append(self.ID_RiseSet, mtexts.menutxts['TMRiseSet'], mtexts.menutxts['TMRiseSetDoc'])
    self.mtable.Append(self.ID_Speeds, mtexts.menutxts['TMSpeeds'], mtexts.menutxts['TMSpeedsDoc'])
    self.mtable.Append(self.ID_ZodPars, mtexts.menutxts['TMZodPars'], mtexts.menutxts['TMZodParsDoc'])
    self.mtable.Append(self.ID_FixStars, mtexts.menutxts['TMFixStars'], mtexts.menutxts['TMFixStarsDoc'])
    self.mtable.Append(self.ID_FixStarsAsps, mtexts.menutxts['TMFixStarsAsps'], mtexts.menutxts['TMFixStarsAspsDoc'])
    self.mtable.Append(self.ID_Arabians, mtexts.menutxts['TMArabianParts'], mtexts.menutxts['TMArabianPartsDoc'])
    self.mtable.Append(self.ID_Strip, mtexts.menutxts['TMStrip'], mtexts.menutxts['TMStripDoc'])
    self.mtable.Append(self.ID_PlanetaryHours, mtexts.menutxts['TMPlanetaryHours'], mtexts.menutxts['TMPlanetaryHoursDoc'])
    self.mtable.Append(self.ID_ExactTransits, mtexts.menutxts['TMExactTransits'], mtexts.menutxts['TMExactTransitsDoc'])
    self.mtable.Append(self.ID_Profections, mtexts.menutxts['TMProfections'], mtexts.menutxts['TMProfectionsDoc'])
    self.mtable.Append(self.ID_CustomerSpeculum, mtexts.menutxts['TMCustomerSpeculum'], mtexts.menutxts['TMCustomerSpeculumDoc'])
    self.mtable.Append(self.ID_PrimaryDirs, mtexts.menutxts['TMPrimaryDirs'], mtexts.menutxts['TMPrimaryDirsDoc'])

    #Charts-menu
    self.mcharts.Append(self.ID_Transits, mtexts.menutxts['PMTransits'], mtexts.menutxts['PMTransitsDoc'])
    self.mcharts.Append(self.ID_Revolutions, mtexts.menutxts['PMRevolutions'], mtexts.menutxts['PMRevolutionsDoc'])
    self.mcharts.Append(self.ID_SunTransits, mtexts.menutxts['PMSunTransits'], mtexts.menutxts['PMSunTransitsDoc'])
    self.mcharts.Append(self.ID_SecondaryDirs, mtexts.menutxts['PMSecondaryDirs'], mtexts.menutxts['PMSecondaryDirsDoc'])
    self.mcharts.Append(self.ID_Elections, mtexts.menutxts['PMElections'], mtexts.menutxts['PMElectionsDoc'])
    self.mcharts.Append(self.ID_SquareChart, mtexts.menutxts['PMSquareChart'], mtexts.menutxts['PMSquareChartDoc'])
    self.mcharts.Append(self.ID_ProfectionsChart, mtexts.menutxts['PMProfections'], mtexts.menutxts['PMProfectionsDoc'])
    self.mcharts.Append(self.ID_MundaneChart, mtexts.menutxts['PMMundane'], mtexts.menutxts['PMMundaneDoc'])

    #Options-menu
    self.mhousesystem = wx.Menu()
    self.itplac = self.mhousesystem.Append(self.ID_Housesystem1, mtexts.menutxts['OMHSPlacidus'], '', wx.ITEM_RADIO)
    self.itkoch = self.mhousesystem.Append(self.ID_Housesystem2, mtexts.menutxts['OMHSKoch'], '', wx.ITEM_RADIO)
    self.itregio = self.mhousesystem.Append(self.ID_Housesystem3, mtexts.menutxts['OMHSRegiomontanus'], '', wx.ITEM_RADIO)
    self.itcampa = self.mhousesystem.Append(self.ID_Housesystem4, mtexts.menutxts['OMHSCampanus'], '', wx.ITEM_RADIO)
    self.itequal = self.mhousesystem.Append(self.ID_Housesystem5, mtexts.menutxts['OMHSEqual'], '', wx.ITEM_RADIO)
    self.itwholesign = self.mhousesystem.Append(self.ID_Housesystem6, mtexts.menutxts['OMHSWholeSign'], '', wx.ITEM_RADIO)
    self.itaxial = self.mhousesystem.Append(self.ID_Housesystem7, mtexts.menutxts['OMHSAxial'], '', wx.ITEM_RADIO)
    self.itmorin = self.mhousesystem.Append(self.ID_Housesystem8, mtexts.menutxts['OMHSMorinus'], '', wx.ITEM_RADIO)
    self.ithoriz = self.mhousesystem.Append(self.ID_Housesystem9, mtexts.menutxts['OMHSHorizontal'], '', wx.ITEM_RADIO)
    self.itpage = self.mhousesystem.Append(self.ID_Housesystem10, mtexts.menutxts['OMHSPagePolich'], '', wx.ITEM_RADIO)
    self.italcab = self.mhousesystem.Append(self.ID_Housesystem11, mtexts.menutxts['OMHSAlcabitus'], '', wx.ITEM_RADIO)
    self.itporph = self.mhousesystem.Append(self.ID_Housesystem12, mtexts.menutxts['OMHSPorphyrius'], '', wx.ITEM_RADIO)

    self.moptions.Append(self.ID_Appearance1, mtexts.menutxts['OMAppearance1'], mtexts.menutxts['OMAppearance1Doc'])
    self.moptions.Append(self.ID_Appearance2, mtexts.menutxts['OMAppearance2'], mtexts.menutxts['OMAppearance2Doc'])
    self.moptions.Append(self.ID_Symbols, mtexts.menutxts['OMSymbols'], mtexts.menutxts['OMSymbolsDoc'])
    self.moptions.Append(self.ID_Dignities, mtexts.menutxts['OMDignities'], mtexts.menutxts['OMDignitiesDoc'])

    self.mdignities = wx.Menu()
    self.mdignities.Append(self.ID_Triplicities, mtexts.menutxts['OMTriplicities'], mtexts.menutxts['OMTriplicitiesDoc'])
    self.mdignities.Append(self.ID_Terms, mtexts.menutxts['OMTerms'], mtexts.menutxts['OMTermsDoc'])
    self.mdignities.Append(self.ID_Decans, mtexts.menutxts['OMDecans'], mtexts.menutxts['OMDecansDoc'])

    self.moptions.AppendMenu(self.ID_MinorDignities, mtexts.menutxts['OMMinorDignities'], self.mdignities)

    self.malmutens = wx.Menu()
    self.malmutens.Append(self.ID_ChartAlmuten, mtexts.menutxts['OMChartAlmuten'], mtexts.menutxts['OMChartAlmutenDoc'])
    self.malmutens.Append(self.ID_Topical, mtexts.menutxts['OMTopical'], mtexts.menutxts['OMTopicalDoc'])

    self.moptions.AppendMenu(self.ID_Almutens, mtexts.menutxts['OMAlmutens'], self.malmutens)
    self.moptions.Append(self.ID_Ayanamsha, mtexts.menutxts['OMAyanamsha'], mtexts.menutxts['OMAyanamshaDoc'])
    self.moptions.Append(self.ID_Colors, mtexts.menutxts['OMColors'], mtexts.menutxts['OMColorsDoc'])

    self.moptions.AppendMenu(self.ID_HouseSystem, mtexts.menutxts['OMHouseSystem'], self.mhousesystem)

    self.setHouse()

    self.mnodes = wx.Menu()
    self.meanitem = self.mnodes.Append(self.ID_NodeMean, mtexts.menutxts['OMNMean'], '', wx.ITEM_RADIO)
    self.trueitem = self.mnodes.Append(self.ID_NodeTrue, mtexts.menutxts['OMNTrue'], '', wx.ITEM_RADIO)

    self.moptions.AppendMenu(self.ID_Nodes, mtexts.menutxts['OMNodes'], self.mnodes)

    self.setNode()

    self.moptions.Append(self.ID_Orbs, mtexts.menutxts['OMOrbs'], mtexts.menutxts['OMOrbsDoc'])
    self.moptions.Append(self.ID_PrimaryDirsOpt, mtexts.menutxts['OMPrimaryDirs'], mtexts.menutxts['OMPrimaryDirsDoc'])
    self.moptions.Append(self.ID_PrimaryKeys, mtexts.menutxts['OMPrimaryKeys'], mtexts.menutxts['OMPrimaryKeysDoc'])

    self.mpdsinchartopts = wx.Menu()
    self.mpdsinchartopts.Append(self.ID_PDsInChartOptZod, mtexts.menutxts['OMPDsInChartOptZod'], mtexts.menutxts['OMPDsInChartOptZodDoc'])
    self.mpdsinchartopts.Append(self.ID_PDsInChartOptMun, mtexts.menutxts['OMPDsInChartOptMun'], mtexts.menutxts['OMPDsInChartOptMunDoc'])

    self.moptions.AppendMenu(self.ID_PDsInChartOpt, mtexts.menutxts['OMPDsInChartOpt'], self.mpdsinchartopts)
    self.moptions.Append(self.ID_LotOfFortune, mtexts.menutxts['OMLotFortune'], mtexts.menutxts['OMLotFortuneDoc'])
    self.moptions.Append(self.ID_ArabicParts, mtexts.menutxts['OMArabicParts'], mtexts.menutxts['OMArabicPartsDoc'])
    self.moptions.Append(self.ID_Syzygy, mtexts.menutxts['OMSyzygy'], mtexts.menutxts['OMSyzygyDoc'])
    self.moptions.Append(self.ID_FixStarsOpt, mtexts.menutxts['OMFixStarsOpt'], mtexts.menutxts['OMFixStarsOptDoc'])
    self.moptions.Append(self.ID_ProfectionsOpt, mtexts.menutxts['OMProfectionsOpt'], mtexts.menutxts['OMProfectionsOptDoc'])
    self.moptions.Append(self.ID_Languages, mtexts.menutxts['OMLanguages'], mtexts.menutxts['OMLanguagesDoc'])
    self.moptions.AppendSeparator()
    self.autosave = self.moptions.Append(self.ID_AutoSaveOpts, mtexts.menutxts['OMAutoSave'], mtexts.menutxts['OMAutoSaveDoc'], wx.ITEM_CHECK)
    self.moptions.Append(self.ID_SaveOpts, mtexts.menutxts['OMSave'], mtexts.menutxts['OMSaveDoc'])
    self.moptions.Append(self.ID_Reload, mtexts.menutxts['OMReload'], mtexts.menutxts['OMReloadDoc'])

    self.setAutoSave()

    #Help-menu
    self.mhelp.Append(self.ID_Help, mtexts.menutxts['HEMHelp'], mtexts.menutxts['HEMHelpDoc'])
    self.mhelp.Append(self.ID_About, mtexts.menutxts['HEMAbout'], mtexts.menutxts['HEMAboutDoc'])


    menubar.Append(self.mhoros, mtexts.menutxts['MHoroscope'])
    menubar.Append(self.mtable, mtexts.menutxts['MTable'])
    menubar.Append(self.mcharts, mtexts.menutxts['MCharts'])
    menubar.Append(self.moptions, mtexts.menutxts['MOptions'])
    menubar.Append(self.mhelp, mtexts.menutxts['MHelp'])
    self.SetMenuBar(menubar)

    self.CreateStatusBar()

    self.Bind(wx.EVT_MENU, self.onNew, id=self.ID_New)
    self.Bind(wx.EVT_MENU, self.onData, id=self.ID_Data)
    self.Bind(wx.EVT_MENU, self.onLoad, id=self.ID_Load)
    self.Bind(wx.EVT_MENU, self.onSave, id=self.ID_Save)
    self.Bind(wx.EVT_MENU, self.onSaveAsBitmap, id=self.ID_SaveAsBitmap)
    self.Bind(wx.EVT_MENU, self.onSynastry, id=self.ID_Synastry)
    self.Bind(wx.EVT_MENU, self.onFindTime, id=self.ID_FindTime)
    self.Bind(wx.EVT_MENU, self.onEphemeris, id=self.ID_Ephemeris)
    self.Bind(wx.EVT_MENU, self.onClose, id=self.ID_Close)
    self.Bind(wx.EVT_MENU, self.onExit, id=self.ID_Exit)

    if os.name == 'mac' or os.name == 'posix':
      self.Bind(wx.EVT_PAINT, self.onPaint)
    else:
      self.Bind(wx.EVT_ERASE_BACKGROUND, self.onEraseBackground)

    self.Bind(wx.EVT_SIZE, self.onSize)
    self.Bind(wx.EVT_MENU_OPEN, self.onMenuOpen)
    #The events EVT_MENU_OPEN and CLOSE are not called on windows in case of accelarator-keys
    self.Bind(wx.EVT_MENU_CLOSE, self.onMenuClose)

    self.Bind(wx.EVT_MENU, self.onPositions, id=self.ID_Positions)
    self.Bind(wx.EVT_MENU, self.onAlmutenZodiacal, id=self.ID_AlmutenZodiacal)
    self.Bind(wx.EVT_MENU, self.onAlmutenChart, id=self.ID_AlmutenChart)
    self.Bind(wx.EVT_MENU, self.onAlmutenTopical, id=self.ID_AlmutenTopical)
    self.Bind(wx.EVT_MENU, self.onMisc, id=self.ID_Misc)
    self.Bind(wx.EVT_MENU, self.onMunPos, id=self.ID_MunPos)
    self.Bind(wx.EVT_MENU, self.onAntiscia, id=self.ID_Antiscia)
    self.Bind(wx.EVT_MENU, self.onAspects, id=self.ID_Aspects)
    self.Bind(wx.EVT_MENU, self.onFixStars, id=self.ID_FixStars)
    self.Bind(wx.EVT_MENU, self.onFixStarsAsps, id=self.ID_FixStarsAsps)
    self.Bind(wx.EVT_MENU, self.onMidpoints, id=self.ID_Midpoints)
    self.Bind(wx.EVT_MENU, self.onRiseSet, id=self.ID_RiseSet)
    self.Bind(wx.EVT_MENU, self.onSpeeds, id=self.ID_Speeds)
    self.Bind(wx.EVT_MENU, self.onZodPars, id=self.ID_ZodPars)
    self.Bind(wx.EVT_MENU, self.onArabians, id=self.ID_Arabians)
    self.Bind(wx.EVT_MENU, self.onStrip, id=self.ID_Strip)
    self.Bind(wx.EVT_MENU, self.onPlanetaryHours, id=self.ID_PlanetaryHours)
    self.Bind(wx.EVT_MENU, self.onExactTransits, id=self.ID_ExactTransits)
    self.Bind(wx.EVT_MENU, self.onProfections, id=self.ID_Profections)
    self.Bind(wx.EVT_MENU, self.onCustomerSpeculum, id=self.ID_CustomerSpeculum)
    self.Bind(wx.EVT_MENU, self.onPrimaryDirs, id=self.ID_PrimaryDirs)

    self.Bind(wx.EVT_MENU, self.onTransits, id=self.ID_Transits)
    self.Bind(wx.EVT_MENU, self.onRevolutions, id=self.ID_Revolutions)
    self.Bind(wx.EVT_MENU, self.onSunTransits, id=self.ID_SunTransits)
    self.Bind(wx.EVT_MENU, self.onSecondaryDirs, id=self.ID_SecondaryDirs)
    self.Bind(wx.EVT_MENU, self.onElections, id=self.ID_Elections)
    self.Bind(wx.EVT_MENU, self.onSquareChart, id=self.ID_SquareChart)
    self.Bind(wx.EVT_MENU, self.onProfectionsChart, id=self.ID_ProfectionsChart)
    self.Bind(wx.EVT_MENU, self.onMundaneChart, id=self.ID_MundaneChart)

    self.Bind(wx.EVT_MENU, self.onAppearance1, id=self.ID_Appearance1)
    self.Bind(wx.EVT_MENU, self.onAppearance2, id=self.ID_Appearance2)
    self.Bind(wx.EVT_MENU, self.onSymbols, id=self.ID_Symbols)
    self.Bind(wx.EVT_MENU, self.onDignities, id=self.ID_Dignities)
    self.Bind(wx.EVT_MENU, self.onAyanamsha, id=self.ID_Ayanamsha)
    self.Bind(wx.EVT_MENU, self.onColors, id=self.ID_Colors)
    self.Bind(wx.EVT_MENU_RANGE, self.onHouseSystem, id=self.ID_Housesystem1, id2=self.ID_Housesystem12)
    self.Bind(wx.EVT_MENU_RANGE, self.onNodes, id=self.ID_NodeMean, id2=self.ID_NodeTrue)
    self.Bind(wx.EVT_MENU, self.onOrbs, id=self.ID_Orbs)
    self.Bind(wx.EVT_MENU, self.onPrimaryDirsOpt, id=self.ID_PrimaryDirsOpt)
    self.Bind(wx.EVT_MENU, self.onPrimaryKeys, id=self.ID_PrimaryKeys)
    self.Bind(wx.EVT_MENU, self.onPDsInChartOptZod, id=self.ID_PDsInChartOptZod)
    self.Bind(wx.EVT_MENU, self.onPDsInChartOptMun, id=self.ID_PDsInChartOptMun)
    self.Bind(wx.EVT_MENU, self.onFortune, id=self.ID_LotOfFortune)
    self.Bind(wx.EVT_MENU, self.onArabicParts, id=self.ID_ArabicParts)
    self.Bind(wx.EVT_MENU, self.onSyzygy, id=self.ID_Syzygy)
    self.Bind(wx.EVT_MENU, self.onFixStarsOpt, id=self.ID_FixStarsOpt)
    self.Bind(wx.EVT_MENU, self.onProfectionsOpt, id=self.ID_ProfectionsOpt)
    self.Bind(wx.EVT_MENU, self.onLanguages, id=self.ID_Languages)
    self.Bind(wx.EVT_MENU, self.onTriplicities, id=self.ID_Triplicities)
    self.Bind(wx.EVT_MENU, self.onTerms, id=self.ID_Terms)
    self.Bind(wx.EVT_MENU, self.onDecans, id=self.ID_Decans)
    self.Bind(wx.EVT_MENU, self.onChartAlmuten, id=self.ID_ChartAlmuten)
    self.Bind(wx.EVT_MENU, self.onTopicals, id=self.ID_Topical)
    self.Bind(wx.EVT_MENU, self.onAutoSaveOpts, id=self.ID_AutoSaveOpts)
    self.Bind(wx.EVT_MENU, self.onSaveOpts, id=self.ID_SaveOpts)
    self.Bind(wx.EVT_MENU, self.onReload, id=self.ID_Reload)

    self.Bind(wx.EVT_MENU, self.onHelp, id=self.ID_Help)
    self.Bind(wx.EVT_MENU, self.onAbout, id=self.ID_About)

    self.Bind(wx.EVT_CLOSE, self.onExit)

    self.splash = True

    self.enableMenus(False)

    self.moptions.Enable(self.ID_SaveOpts, False)
    if self.options.checkOptsFiles():
      self.moptions.Enable(self.ID_Reload, True)
    else:
      self.moptions.Enable(self.ID_Reload, False)

    self.trdatedlg = None
    self.trmondlg = None
    self.suntrdlg = None
    self.revdlg = None
    self.secdirdlg = None
    self.pdrangedlg = None

    os.environ['SE_EPHE_PATH'] = ''
    astrology.swe_set_ephe_path(common.common.ephepath)
    
    self.drawSplash()

    self.Bind(EVT_PDREADY, self.OnPDReady)


  #Horoscope-menu 
  def onNew(self, event):
    dlg = personaldatadlg.PersonalDataDlg(self, self.options.langid)
    dlg.CenterOnParent()
    dlg.initialize()  

    # this does not return until the dialog is closed.
    val = dlg.ShowModal()
    if val == wx.ID_OK: 
      self.dirty = True

      direc = dlg.placerbE.GetValue()
      hemis = dlg.placerbN.GetValue()

      place = chart.Place(dlg.birthplace.GetValue(), int(dlg.londeg.GetValue()), int(dlg.lonmin.GetValue()), 0, direc, int(dlg.latdeg.GetValue()), int(dlg.latmin.GetValue()), 0, hemis, int(dlg.alt.GetValue()))

      plus = True
      if dlg.pluscb.GetCurrentSelection() == 1:
        plus = False
      time = chart.Time(int(dlg.year.GetValue()), int(dlg.month.GetValue()), int(dlg.day.GetValue()), int(dlg.hour.GetValue()), int(dlg.minute.GetValue()), int(dlg.sec.GetValue()), dlg.timeckb.GetValue(), dlg.calcb.GetCurrentSelection(), dlg.zonecb.GetCurrentSelection(), plus, int(dlg.zhour.GetValue()), int(dlg.zminute.GetValue()), dlg.daylightckb.GetValue(), place)

      male = dlg.genderrbM.GetValue()
      self.horoscope = chart.Chart(dlg.name.GetValue(), male, time, place, dlg.typecb.GetCurrentSelection(), dlg.notes.GetValue(), self.options)
      self.splash = False 
      self.enableMenus(True)
      self.drawBkg()
      self.Refresh()
      self.handleStatusBar(True)
      self.handleCaption(True)
#     self.calc()##

    dlg.Destroy()


  def onData(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    dlg = personaldatadlg.PersonalDataDlg(self, self.options.langid)
    dlg.CenterOnParent()
    dlg.fill(self.horoscope)

    val = dlg.ShowModal()
    if val == wx.ID_OK: 
      changed = dlg.check(self.horoscope)

      if self.dirty and changed:
        dlgm = wx.MessageDialog(self, mtexts.txts['DiscardCurrHor'], '', wx.YES_NO|wx.ICON_QUESTION)
        if dlgm.ShowModal() == wx.ID_NO:
          self.save()
        dlgm.Destroy()#

      if changed:
        self.dirty = True

      direc = dlg.placerbE.GetValue()
      hemis = dlg.placerbN.GetValue()
      place = chart.Place(dlg.birthplace.GetValue(), int(dlg.londeg.GetValue()), int(dlg.lonmin.GetValue()), 0, direc, int(dlg.latdeg.GetValue()), int(dlg.latmin.GetValue()), 0, hemis, int(dlg.alt.GetValue()))

      plus = True
      if dlg.pluscb.GetCurrentSelection() == 1:
        plus = False
      time = chart.Time(int(dlg.year.GetValue()), int(dlg.month.GetValue()), int(dlg.day.GetValue()), int(dlg.hour.GetValue()), int(dlg.minute.GetValue()), int(dlg.sec.GetValue()), dlg.timeckb.GetValue(), dlg.calcb.GetCurrentSelection(), dlg.zonecb.GetCurrentSelection(), plus, int(dlg.zhour.GetValue()), int(dlg.zminute.GetValue()), dlg.daylightckb.GetValue(), place)

      male = dlg.genderrbM.GetValue()
      self.horoscope = chart.Chart(dlg.name.GetValue(), male, time, place, dlg.typecb.GetCurrentSelection(), dlg.notes.GetValue(), self.options)
      self.splash = False 
      self.enableMenus(True)
      self.drawBkg()
      self.Refresh()
      self.handleStatusBar(True)
      self.handleCaption(True)
#     self.calc()##

      if changed:
        self.closeChildWnds()

    dlg.Destroy()


  def showFindTime(self, bc, fnd, arplac):
    place = chart.Place('London, GBR', 0, 6, 0, False, 51, 31, 0, True, 10)

    h, m, s = util.decToDeg(fnd[3])
    time = chart.Time(fnd[0], fnd[1], fnd[2], h, m, s, bc, chart.Time.GREGORIAN, chart.Time.GREENWICH, True, 0, 0, False, place)
    #Calc obliquity
    d = astrology.swe_deltat(time.jd)
    rflag, obl, serr = astrology.swe_calc(time.jd+d, astrology.SE_ECL_NUT, 0)

    if arplac[2]:
      #calc GMTMidnight:
      timeMidnight = chart.Time(time.year, time.month, time.day, 0, 0, 0, bc, chart.Time.GREGORIAN, chart.Time.GREENWICH, True, 0, 0, False, place)
      place = self.calcPlace(time.time, timeMidnight.sidTime, arplac[0], arplac[1], obl[0])

    self.horoscope = chart.Chart('Search', True, time, place, chart.Chart.RADIX, '', self.options)

    if (not self.splash):
      self.destroyDlgs()
      self.closeChildWnds()

    self.dirty = True
    self.splash = False 
    self.fpath = ''
    self.enableMenus(True)
    self.clickedPlId = None
    self.drawBkg()
    self.Refresh()
    self.handleStatusBar(True)
    self.handleCaption(True)


  def calcPlace(self, gmt, gmst0, mclon, asclon, obl):
    robl = math.radians(obl)
    deltaGMST = gmt*1.00273790927949
    gmstNat = util.normalizeTime(gmst0+deltaGMST)

    ramc = 0.0
    if mclon == 90.0:
      ramc = 90.0
    elif mclon == 270.0:
      ramc = 270.0
    else:
      rmclon = math.radians(mclon)
      X = math.degrees(math.atan(math.tan(rmclon)*math.cos(robl)))
      if mclon >= 0.0 and mclon < 90.0:
        ramc = X
      elif mclon > 90.0 and mclon < 270.0:
        ramc = X+180.0
      elif mclon > 270.0 and mclon < 360.0:
        ramc = X+360.0

    lmstNat = ramc/15.0

    lonInTime = gmstNat-lmstNat

    if not (-12.0 <= lonInTime and lonInTime <= 12.0):
      if lonInTime < -12.0:
        lonInTime += 24.0
      elif lonInTime > 12.0:
        lonInTime -= 24.0

    lon = 0.0
    east = False
    if lonInTime == 0.0:
      lon = 0.0
    elif 0.0 < lonInTime and lonInTime <= 12.0: #West
      lon = lonInTime*15.0
    elif -12.0 <= lonInTime and lonInTime < 0.0: #East
      lon = lonInTime*15.0
      east = True

    #Lat
    rasclon = math.radians(asclon)
    rramc = math.radians(ramc)

    lat = 30.0#
    north = True
    if math.sin(robl) != 0.0:
      lat = math.degrees(math.atan(-(math.cos(rramc)*(1/math.tan(rasclon))+math.sin(rramc)*math.cos(robl))/math.sin(robl)))
      if lat < 0.0:
        north = False

    lon = math.fabs(lon)
    lat = math.fabs(lat)
    
    ld, lm, ls = util.decToDeg(lon)
    lad, lam, las = util.decToDeg(lat)

    return chart.Place('Place', ld, lm, ls, east, lad, lam, las, north, 10)


  def onLoad(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if self.dirty:
      dlgm = wx.MessageDialog(self, mtexts.txts['DiscardCurrHor'], '', wx.YES_NO|wx.ICON_QUESTION)
      if dlgm.ShowModal() == wx.ID_NO:
        dlgm.Destroy()#
        return

      dlgm.Destroy()#

    dlg = wx.FileDialog(self, mtexts.txts['OpenHor'], '', '', mtexts.txts['HORFiles'], wx.FD_OPEN)
    if os.path.isdir(self.fpathhors):
      dlg.SetDirectory(self.fpathhors)
    else:
      dlg.SetDirectory(u'.')

    if dlg.ShowModal() == wx.ID_OK:
      dpath = dlg.GetDirectory()
      fpath = dlg.GetPath()

      if not fpath.endswith(u'.hor'):
        fpath+=u'.hor'

      chrt = self.subLoad(fpath, dpath)

      if chrt != None:
        self.horoscope = chrt
        self.splash = False 
        self.drawBkg()
        self.Refresh()
        self.fpathhors = dpath
        self.fpath = fpath
        self.enableMenus(True)
        self.handleStatusBar(True)
        self.handleCaption(True)
        self.dirty = False
#       self.calc()##

        self.filehistory.AddFileToHistory(fpath)

    dlg.Destroy()#


  def subLoad(self, fpath, dpath, dontclose = False):
    chrt = None

    try:
      f = open(fpath, 'rb')   
      name = pickle.load(f)
      male = pickle.load(f)
      htype = pickle.load(f)
      bc = pickle.load(f)
      year = pickle.load(f)
      month = pickle.load(f)
      day = pickle.load(f)
      hour = pickle.load(f)
      minute = pickle.load(f)
      second = pickle.load(f)
      cal = pickle.load(f)
      zt = pickle.load(f)
      plus = pickle.load(f)
      zh = pickle.load(f)
      zm = pickle.load(f)
      daylightsaving = pickle.load(f)
      place = pickle.load(f)
      deglon = pickle.load(f)
      minlon = pickle.load(f)
      seclon = pickle.load(f)
      east = pickle.load(f)
      deglat = pickle.load(f)
      minlat = pickle.load(f)
      seclat = pickle.load(f)
      north = pickle.load(f)
      altitude = pickle.load(f)
      notes = pickle.load(f)
      f.close()

      if (not self.splash) and (not dontclose):
        self.closeChildWnds()
      
      place = chart.Place(place, deglon, minlon, 0, east, deglat, minlat, seclat, north, altitude)
      time = chart.Time(year, month, day, hour, minute, second, bc, cal, zt, plus, zh, zm, daylightsaving, place)
      chrt = chart.Chart(name, male, time, place, htype, notes, self.options)
    except IOError:
      dlgm = wx.MessageDialog(self, mtexts.txts['FileError'], mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
      dlgm.ShowModal()
      dlgm.Destroy()#

    return chrt 


  def onSave(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    self.save()


  def save(self):
    dlg = wx.FileDialog(self, mtexts.txts['SaveHor'], '', self.horoscope.name, mtexts.txts['HORFiles'], wx.FD_SAVE)
    if os.path.isdir(self.fpathhors):
      dlg.SetDirectory(self.fpathhors)
    else:
      dlg.SetDirectory(u'.')

    if dlg.ShowModal() == wx.ID_OK:
      dpath = dlg.GetDirectory()
      fpath = dlg.GetPath()

      if not fpath.endswith(u'.hor'):
        fpath+=u'.hor'
      #Check if fpath already exists!?
      if os.path.isfile(fpath):
        dlgm = wx.MessageDialog(self, mtexts.txts['FileExists'], mtexts.txts['Message'], wx.YES_NO|wx.YES_DEFAULT|wx.ICON_QUESTION)
        if dlgm.ShowModal() == wx.ID_NO:
          dlgm.Destroy()#
          return
        dlgm.Destroy()#
      
      try:
        f = open(fpath, 'wb')   
        pickle.dump(self.horoscope.name, f)
        pickle.dump(self.horoscope.male, f)
        pickle.dump(self.horoscope.htype, f)
        pickle.dump(self.horoscope.time.bc, f)
        pickle.dump(self.horoscope.time.origyear, f)
        pickle.dump(self.horoscope.time.origmonth, f)
        pickle.dump(self.horoscope.time.origday, f)
        pickle.dump(self.horoscope.time.hour, f)
        pickle.dump(self.horoscope.time.minute, f)
        pickle.dump(self.horoscope.time.second, f)
        pickle.dump(self.horoscope.time.cal, f)
        pickle.dump(self.horoscope.time.zt, f)
        pickle.dump(self.horoscope.time.plus, f)
        pickle.dump(self.horoscope.time.zh, f)
        pickle.dump(self.horoscope.time.zm, f)
        pickle.dump(self.horoscope.time.daylightsaving, f)
        pickle.dump(self.horoscope.place.place, f)
        pickle.dump(self.horoscope.place.deglon, f)
        pickle.dump(self.horoscope.place.minlon, f)
        pickle.dump(self.horoscope.place.seclon, f)
        pickle.dump(self.horoscope.place.east, f)
        pickle.dump(self.horoscope.place.deglat, f)
        pickle.dump(self.horoscope.place.minlat, f)
        pickle.dump(self.horoscope.place.seclat, f)
        pickle.dump(self.horoscope.place.north, f)
        pickle.dump(self.horoscope.place.altitude, f)
        pickle.dump(self.horoscope.notes, f)
        self.fpathhors = dpath
        self.fpath = fpath
        self.handleCaption(True)
        f.close()
        self.dirty = False
      except IOError:
        dlgm = wx.MessageDialog(self, mtexts.txts['FileError'], mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
        dlgm.ShowModal()
        dlgm.Destroy()#

    dlg.Destroy()#


  def onSaveAsBitmap(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    name = self.horoscope.name
    if name == '':
      name = mtexts.txts['Horoscope']
    dlg = wx.FileDialog(self, mtexts.txts['SaveAsBmp'], '', name, mtexts.txts['BMPFiles'], wx.FD_SAVE)
    if os.path.isdir(self.fpathimgs):
      dlg.SetDirectory(self.fpathimgs)
    else:
      dlg.SetDirectory(u'.')

    if dlg.ShowModal() == wx.ID_OK:
      dpath = dlg.GetDirectory()
      fpath = dlg.GetPath()
      if not fpath.endswith(u'.bmp'):
        fpath+=u'.bmp'
      #Check if fpath already exists!?
      if os.path.isfile(fpath):
        dlgm = wx.MessageDialog(self, mtexts.txts['FileExists'], mtexts.txts['Message'], wx.YES_NO|wx.YES_DEFAULT|wx.ICON_QUESTION)
        if dlgm.ShowModal() == wx.ID_NO:
          dlgm.Destroy()#
          return
        dlgm.Destroy()#

      self.buffer.SaveFile(fpath, wx.BITMAP_TYPE_BMP)   
      self.fpathimgs = dpath

    dlg.Destroy()#


  def onSynastry(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    dlg = wx.FileDialog(self, mtexts.txts['OpenHor'], '', '', mtexts.txts['HORFiles'], wx.FD_OPEN)
    if os.path.isdir(self.fpathhors):
      dlg.SetDirectory(self.fpathhors)
    else:
      dlg.SetDirectory(u'.')

    chrt = None
    if dlg.ShowModal() == wx.ID_OK:
      dpath = dlg.GetDirectory()
      fpath = dlg.GetPath()

      if not fpath.endswith(u'.hor'):
        fpath+=u'.hor'

      chrt = self.subLoad(fpath, dpath, True)

    dlg.Destroy()#

    if chrt != None:
      txt = self.horoscope.name+u' - '+chrt.name+' '+mtexts.txts['Synastry']+' ('+str(chrt.time.origyear)+'.'+common.common.months[chrt.time.origmonth-1]+'.'+str(chrt.time.origday)+' '+str(chrt.time.hour)+':'+str(chrt.time.minute).zfill(2)+':'+str(chrt.time.second).zfill(2)+')'
      tw = transitframe.TransitFrame(self, txt, chrt, self.horoscope, self.options, transitframe.TransitFrame.COMPOUND)
      tw.Show(True)


  def onFindTime(self, event):
    findtimdlg = findtimedlg.FindTimeDlg(self)
    findtimdlg.fill()
    findtimdlg.CenterOnParent()

#   findtimdlg.ShowModal() # because the "Calculating"-dialog will also be modal and it enables the Menues of the MainFrame!!
    findtimdlg.Show()


  def onEphemeris(self, event):
    ephemdlg = graphephemdlg.GraphEphemDlg(self)
    ephemdlg.CenterOnParent()
    val = ephemdlg.ShowModal()

    if val == wx.ID_OK:
      year = int(ephemdlg.year.GetValue())
      wait = wx.BusyCursor()
      eph = ephemcalc.EphemCalc(year, self.options)
      ephemfr = graphephemframe.GraphEphemFrame(self, mtexts.txts['Ephemeris'], year, eph.posArr, self.options)
      ephemfr.Show(True)


  def onClose(self, event):
    if self.dirty:
      dlgm = wx.MessageDialog(self, mtexts.txts['DiscardCurrHor'], '', wx.YES_NO|wx.ICON_QUESTION)
      if dlgm.ShowModal() == wx.ID_NO:
        dlgm.Destroy()#
        return
      dlgm.Destroy()#

    self.destroyDlgs()

    self.fpath = ''
    self.dirty = False
    self.splash = True
    self.enableMenus(False)
    self.closeChildWnds()
    self.drawSplash()
    self.handleStatusBar(False)
    self.handleCaption(False)
    self.Refresh()  


  def onExit(self, event):
    if self.dirty:
      dlgm = wx.MessageDialog(self, mtexts.txts['DiscardCurrHor'], '', wx.YES_NO|wx.ICON_QUESTION)
      if dlgm.ShowModal() == wx.ID_NO:
        dlgm.Destroy()#
        return
      dlgm.Destroy()#

    self.destroyDlgs()

    del self.filehistory

    self.Destroy()


  def OnFileHistory(self, evt):
    if self.dirty:
      dlgm = wx.MessageDialog(self, mtexts.txts['DiscardCurrHor'], '', wx.YES_NO|wx.ICON_QUESTION)
      if dlgm.ShowModal() == wx.ID_NO:
        dlgm.Destroy()#
        return

      dlgm.Destroy()#

    # get the file based on the menu ID
    fileNum = evt.GetId()-wx.ID_FILE1
    path = self.filehistory.GetHistoryFile(fileNum)

    #check file
    if os.path.exists(path):
      dname = os.path.dirname(path)
      chrt = self.subLoad(path, dname)

      if chrt != None:
        self.horoscope = chrt
        self.splash = False 
        self.drawBkg()
        self.Refresh()
        self.fpathhors = dname
        self.fpath = path
        self.enableMenus(True)
        self.handleStatusBar(True)
        self.handleCaption(True)
        self.dirty = False
#       self.calc()##

        self.filehistory.AddFileToHistory(path)

      # add it back to the history so it will be moved up the list
#     self.filehistory.AddFileToHistory(path)

      self.destroyDlgs()
    else:
      dlgm = wx.MessageDialog(self, mtexts.txts['FileError'], mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
      dlgm.ShowModal()
      dlgm.Destroy()#
      self.filehistory.RemoveFileFromHistory(fileNum)


  def destroyDlgs(self):
    if self.trdatedlg != None:
      self.trdatedlg.Destroy()
      self.trdatedlg = None
    if self.trmondlg != None:
      self.trmondlg.Destroy()
      self.trmondlg = None
    if self.suntrdlg != None:
      self.suntrdlg.Destroy()
      self.suntrdlg = None
    if self.revdlg != None:
      self.revdlg.Destroy()
      self.revdlg = None
    if self.secdirdlg != None:
      self.secdirdlg.Destroy()
      self.secdirdlg = None
    if self.pdrangedlg != None:
      self.pdrangedlg.Destroy()
      self.pdrangedlg = None


  #Table-menu
  def onPositions(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if not self.splash:
      speculum = 0
      if self.options.primarydir == primdirs.PrimDirs.REGIOMONTAN:
        speculum = 1
      if True in self.options.speculums[speculum]:
        wait = wx.BusyCursor()
        posframe = positionsframe.PositionsFrame(self, self.title, self.horoscope, self.options)
        posframe.Show(True)
      else:
        dlgm = wx.MessageDialog(self, mtexts.txts['SelectColumn'], '', wx.OK|wx.ICON_INFORMATION)
        dlgm.ShowModal()
        dlgm.Destroy()#


  def onAlmutenZodiacal(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if not self.splash:
      wait = wx.BusyCursor()
      almutenfr = almutenzodsframe.AlmutenZodsFrame(self, self.title, self.horoscope, self.options)
      almutenfr.Show(True)


  def onAlmutenChart(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if not self.splash:
      wait = wx.BusyCursor()
      almutenfr = almutenchartframe.AlmutenChartFrame(self, self.title, self.horoscope, self.options)
      almutenfr.Show(True)


  def onAlmutenTopical(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if not self.splash:
      if self.horoscope.options.topicals != None and len(self.horoscope.almutens.topicals.names) != 0:
        wait = wx.BusyCursor()
        topicalframe = almutentopicalsframe.AlmutenTopicalsFrame(self, self.horoscope, self.title)
        topicalframe.Show(True)
      else:
        dlgm = wx.MessageDialog(self, mtexts.txts['NoTopicalsCreated'], '', wx.OK|wx.ICON_INFORMATION)
        dlgm.ShowModal()
        dlgm.Destroy()#


  def onMisc(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if not self.splash:
      wait = wx.BusyCursor()
      tblframe = miscframe.MiscFrame(self, self.title, self.horoscope, self.options)
      tblframe.Show(True)


  def onAspects(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if not self.splash:
      wait = wx.BusyCursor()
      aspsframe = aspectsframe.AspectsFrame(self, self.title, self.horoscope, self.options)
      aspsframe.Show(True)


  def onMidpoints(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if not self.splash:
      wait = wx.BusyCursor()
      midsframe = midpointsframe.MidPointsFrame(self, self.title, self.horoscope, self.options)
      midsframe.Show(True)


  def onRiseSet(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if not self.splash:
      wait = wx.BusyCursor()
      risesetfr = risesetframe.RiseSetFrame(self, self.title, self.horoscope, self.options)
      risesetfr.Show(True)


  def onSpeeds(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if not self.splash:
      wait = wx.BusyCursor()
      speedsfr = speedsframe.SpeedsFrame(self, self.title, self.horoscope, self.options)
      speedsfr.Show(True)


  def onMunPos(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if not self.splash:
      wait = wx.BusyCursor()
      munposfr = munposframe.MunPosFrame(self, self.title, self.horoscope, self.options)
      munposfr.Show(True)


  def onAntiscia(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if not self.splash:
      wait = wx.BusyCursor()
      antisciafr = antisciaframe.AntisciaFrame(self, self.title, self.horoscope, self.options)
      antisciafr.Show(True)


  def onZodPars(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if not self.splash:
      wait = wx.BusyCursor()
      zodparsfr = zodparsframe.ZodParsFrame(self, self.title, self.horoscope, self.options)
      zodparsfr.Show(True)


  def onStrip(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if not self.splash:
      wait = wx.BusyCursor()
      stripfr = stripframe.StripFrame(self, self.title, self.horoscope, self.options)
      stripfr.Show(True)


  def onFixStars(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if not self.splash:
      if not self.checkFixStars():
        return

      if len(self.options.fixstars) == 0:
        dlgm = wx.MessageDialog(self, mtexts.txts['NoSelFixStars'], '', wx.OK|wx.ICON_INFORMATION)
        dlgm.ShowModal()
        dlgm.Destroy()
        return  

      wait = wx.BusyCursor()
      fixstarsfr = fixstarsframe.FixStarsFrame(self, self.title, self.horoscope, self.options)
      fixstarsfr.Show(True)


  def onFixStarsAsps(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if not self.splash:
      if not self.checkFixStars():
        return

      if len(self.options.fixstars) == 0:
        dlgm = wx.MessageDialog(self, mtexts.txts['NoSelFixStars'], '', wx.OK|wx.ICON_INFORMATION)
        dlgm.ShowModal()
        dlgm.Destroy()
        return  

      wait = wx.BusyCursor()
      fixstarsaspsfr = fixstarsaspectsframe.FixStarsAspectsFrame(self, self.title, self.horoscope, self.options)
      fixstarsaspsfr.Show(True)


  def onPlanetaryHours(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if not self.splash:
      wait = wx.BusyCursor()
      planetaryfr = hoursframe.HoursFrame(self, self.title, self.horoscope, self.options)
      planetaryfr.Show(True)


  def onArabians(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if not self.splash:
      wait = wx.BusyCursor()
      partsfr = arabicpartsframe.ArabicPartsFrame(self, self.title, self.horoscope, self.options)
      partsfr.Show(True)


  def onExactTransits(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if self.horoscope.time.bc:
      dlgm = wx.MessageDialog(self, mtexts.txts['NotAvailable'], '', wx.OK|wx.ICON_INFORMATION)
      dlgm.ShowModal()
      dlgm.Destroy()
      return

    if self.trmondlg == None:
      self.trmondlg = transitmdlg.TransitMonthDlg(None, self.horoscope.time)
    self.trmondlg.CenterOnParent()
    val = self.trmondlg.ShowModal()

    if val == wx.ID_OK: 
      year = int(self.trmondlg.year.GetValue())
      month = int(self.trmondlg.month.GetValue())

      wait = wx.BusyCursor()

      trans = transits.Transits()
      trans.month(year, month, self.horoscope)
      tw = transitmframe.TransitMonthFrame(self, self.title.replace(mtexts.typeList[self.horoscope.htype], mtexts.txts['Transit']+' ('+str(year)+'.'+common.common.months[month-1]+')'), trans.transits, year, month, self.horoscope, self.options)
      tw.Show(True)


  def onProfections(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if self.horoscope.time.bc:
      dlgm = wx.MessageDialog(self, mtexts.txts['NotAvailable'], '', wx.OK|wx.ICON_INFORMATION)
      dlgm.ShowModal()
      dlgm.Destroy()
      return

    pdlg = proftabledlg.ProfTableDlg(self)
    pdlg.initialize()

    pdlg.CenterOnParent()

    val = pdlg.ShowModal()
    if val == wx.ID_OK:
      proftype = chart.Chart.YEAR
      mainsigs = pdlg.mainrb.GetValue()

      pchart = self.horoscope

      wait = wx.BusyCursor()

      #Cycle
      y = self.horoscope.time.year
      m = self.horoscope.time.month
      d = self.horoscope.time.day
      t = self.horoscope.time.time

      #Feb29?
      if self.horoscope.time.month == 2 and self.horoscope.time.day == 29:
        d -= 1

      pcharts = []

      cyc = 0
      while(cyc < 12):
        if self.options.zodprof:
          prof = profections.Profections(self.horoscope, y, m, d, t, cyc)
          pchart = chart.Chart(self.horoscope.name, self.horoscope.male, self.horoscope.time, self.horoscope.place, chart.Chart.PROFECTION, '', self.options, False, proftype)
          pchart.calcProfPos(prof)
        else:
          if not self.options.usezodprojsprof and (y+cyc == self.horoscope.time.year or (y+cyc-self.horoscope.time.year) % 12 == 0) and m == self.horoscope.time.month and d == self.horoscope.time.day:
            pchart = self.horoscope
          else:
            prof = munprofections.MunProfections(self.horoscope, y, m, d, t, cyc)
            proflondeg, proflonmin, proflonsec = util.decToDeg(prof.lonZ)
            profplace = chart.Place(mtexts.txts['Profections'], proflondeg, proflonmin, proflonsec, prof.east, self.horoscope.place.deglat, self.horoscope.place.minlat, self.horoscope.place.seclat, self.horoscope.place.north, self.horoscope.place.altitude)
            pchart = chart.Chart(self.horoscope.name, self.horoscope.male, self.horoscope.time, profplace, chart.Chart.PROFECTION, '', self.options, False, proftype, self.options.usezodprojsprof)
            pchartpls = chart.Chart(self.horoscope.name, self.horoscope.male, self.horoscope.time, self.horoscope.place, chart.Chart.PROFECTION, '', self.options, False, proftype, self.options.usezodprojsprof)
            #modify planets, ...
            pchart.planets.calcMundaneProfPos(pchart.houses.ascmc2, pchartpls.planets.planets, self.horoscope.place.lat, self.horoscope.obl[0])
  
            #modify lof
            pchart.fortune.calcMundaneProfPos(pchart.houses.ascmc2, pchartpls.fortune, self.horoscope.place.lat, self.horoscope.obl[0])
  
        pcharts.append((pchart, y+cyc, m, d, t))
        cyc += 1

      profsfr = profstableframe.ProfsTableFrame(self, self.title, pcharts, self.options, mainsigs)
      profsfr.Show(True)

      pstepdlg = profectiontablestepperdlg.ProfectionTableStepperDlg(profsfr, self.horoscope, self.options, proftype)
      pstepdlg.CenterOnParent()
      pstepdlg.Show(True)

    pdlg.Destroy()


  def onCustomerSpeculum(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if not self.splash:
      speculum = 0
      if self.options.primarydir == primdirs.PrimDirs.REGIOMONTAN:
        speculum = 1
      if True in self.options.speculums[speculum]:
          if self.horoscope.cpd != None:
            wait = wx.BusyCursor()
            custframe = customerframe.CustomerFrame(self, self.title, self.horoscope, self.options, self.horoscope.cpd)
            custframe.Show(True)
          elif self.horoscope.cpd2 != None:
            wait = wx.BusyCursor()
            custframe = customerframe.CustomerFrame(self, self.title, self.horoscope, self.options, self.horoscope.cpd2)
            custframe.Show(True)
          else:
            dlgm = wx.MessageDialog(self, mtexts.txts['CheckUser'], '', wx.OK|wx.ICON_INFORMATION)
            dlgm.ShowModal()
            dlgm.Destroy()#
      else:
        dlgm = wx.MessageDialog(self, mtexts.txts['SelectColumn'], '', wx.OK|wx.ICON_INFORMATION)
        dlgm.ShowModal()
        dlgm.Destroy()#


  def onPrimaryDirs(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if self.horoscope.time.bc:
      dlgm = wx.MessageDialog(self, mtexts.txts['NotAvailable'], '', wx.OK|wx.ICON_INFORMATION)
      dlgm.ShowModal()
      dlgm.Destroy()
      return

    if self.pdrangedlg == None:
      self.pdrangedlg = primdirsrangedlg.PrimDirsRangeDlg(None)

    self.pdrangedlg.CenterOnParent()

    val = self.pdrangedlg.ShowModal()
    if val == wx.ID_OK:
      pdrange = primdirs.PrimDirs.RANGEALL
      if self.pdrangedlg.range25rb.GetValue():
        pdrange = primdirs.PrimDirs.RANGE25
      elif self.pdrangedlg.range50rb.GetValue():
        pdrange = primdirs.PrimDirs.RANGE50
      elif self.pdrangedlg.range75rb.GetValue():
        pdrange = primdirs.PrimDirs.RANGE75
      elif self.pdrangedlg.range100rb.GetValue():
        pdrange = primdirs.PrimDirs.RANGE100

      direction = primdirs.PrimDirs.BOTHDC
      if self.pdrangedlg.directrb.GetValue():
        direction = primdirs.PrimDirs.DIRECT
      elif self.pdrangedlg.converserb.GetValue():
        direction = primdirs.PrimDirs.CONVERSE

      keytxt = ''
      if self.options.pdkeydyn:
        keytxt = mtexts.typeListDyn[self.options.pdkeyd]
      else:
        keytxt = mtexts.typeListStat[self.options.pdkeys]

      txt = mtexts.typeListDirs[self.options.primarydir]+'; '+keytxt+'\n'+mtexts.txts['BusyInfo']

      self.progbar = wx.ProgressDialog(mtexts.txts['Calculating'], txt, parent=self, style = wx.PD_CAN_ABORT|wx.PD_APP_MODAL)
      self.progbar.Fit()

      self.pds = None
      self.pdready = False
      self.abort = primdirs.AbortPD()
      thId = thread.start_new_thread(self.calcPDs, (pdrange, direction, self))

      self.timer = wx.Timer(self)
      self.Bind(wx.EVT_TIMER, self.OnTimer)
      self.timer.Start(500)


  def calcPDs(self, pdrange, direction, win):
    if self.options.primarydir == primdirs.PrimDirs.PLACIDIANSEMIARC:
      self.pds = placidiansapd.PlacidianSAPD(self.horoscope, self.options, pdrange, direction, self.abort)
    elif self.options.primarydir == primdirs.PrimDirs.PLACIDIANUNDERTHEPOLE:
      self.pds = placidianutppd.PlacidianUTPPD(self.horoscope, self.options, pdrange, direction, self.abort)
    elif self.options.primarydir == primdirs.PrimDirs.REGIOMONTAN:
      self.pds = regiomontanpd.RegiomontanPD(self.horoscope, self.options, pdrange, direction, self.abort)
    else:
      self.pds = campanianpd.CampanianPD(self.horoscope, self.options, pdrange, direction, self.abort)

    pdlock.acquire()
    self.pdready = True
    pdlock.release()
    evt = PDReadyEvent()
    wx.PostEvent(win, evt)


  def OnTimer(self, event):
    pdlock.acquire()
    if not self.pdready:
      (keepGoing, skip) = self.progbar.Pulse()

      if not keepGoing:
        self.abort.aborting()
    pdlock.release()


  def OnPDReady(self, event):
    self.timer.Stop()
    del self.timer
    self.progbar.Destroy()
    del self.progbar

    if self.abort.abort:
      self.Refresh()
    else:
      if self.pds != None and len(self.pds.pds) > 0:
        pdw = primdirslistframe.PrimDirsListFrame(self, self.horoscope, self.options, self.pds, self.title.replace(mtexts.typeList[self.horoscope.htype], mtexts.txts['PrimaryDirs']))

        pdw.Show(True)
      else:
        dlgm = wx.MessageDialog(self, mtexts.txts['NoPDsWithSettings'], mtexts.txts['Information'], wx.OK|wx.ICON_INFORMATION)
        dlgm.ShowModal()
        dlgm.Destroy()#

    if self.pds != None:
      del self.pds

    del self.abort


  #Charts-menu
  def onTransits(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if self.horoscope.time.bc:
      dlgm = wx.MessageDialog(self, mtexts.txts['NotAvailable'], '', wx.OK|wx.ICON_INFORMATION)
      dlgm.ShowModal()
      dlgm.Destroy()
      return

    if self.trdatedlg == None:
      self.trdatedlg = timespacedlg.TimeSpaceDlg(None, mtexts.txts['Transits'], self.options.langid)
      self.trdatedlg.initialize(self.horoscope)
    self.trdatedlg.CenterOnParent()

    val = self.trdatedlg.ShowModal()
    if val == wx.ID_OK: 
      wait = wx.BusyCursor()

      direc = self.trdatedlg.placerbE.GetValue()
      hemis = self.trdatedlg.placerbN.GetValue()
      place = chart.Place(self.trdatedlg.birthplace.GetValue(), int(self.trdatedlg.londeg.GetValue()), int(self.trdatedlg.lonmin.GetValue()), 0, direc, int(self.trdatedlg.latdeg.GetValue()), int(self.trdatedlg.latmin.GetValue()), 0, hemis, 0) #Transit doesn't calculate planetary hours => altitude is zero

      plus = True
      if self.trdatedlg.pluscb.GetCurrentSelection() == 1:
        plus = False
      time = chart.Time(int(self.trdatedlg.year.GetValue()), int(self.trdatedlg.month.GetValue()), int(self.trdatedlg.day.GetValue()), int(self.trdatedlg.hour.GetValue()), int(self.trdatedlg.minute.GetValue()), int(self.trdatedlg.sec.GetValue()), self.trdatedlg.timeckb.GetValue(), self.trdatedlg.calcb.GetCurrentSelection(), self.trdatedlg.zonecb.GetCurrentSelection(), plus, int(self.trdatedlg.zhour.GetValue()), int(self.trdatedlg.zminute.GetValue()), self.trdatedlg.daylightckb.GetValue(), place, False)

      trans = chart.Chart(self.horoscope.name, self.horoscope.male, time, place, chart.Chart.TRANSIT, '', self.options, False)

      tw = transitframe.TransitFrame(self, self.title.replace(mtexts.typeList[self.horoscope.htype], mtexts.typeList[chart.Chart.TRANSIT]+' ('+str(time.year)+'.'+common.common.months[time.month-1]+'.'+str(time.day)+' '+str(time.hour)+':'+str(time.minute).zfill(2)+':'+str(time.second).zfill(2)+')'), trans, self.horoscope, self.options)
      tw.Show(True)


  def onRevolutions(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if self.horoscope.time.bc:
      dlgm = wx.MessageDialog(self, mtexts.txts['NotAvailable'], '', wx.OK|wx.ICON_INFORMATION)
      dlgm.ShowModal()
      dlgm.Destroy()
      return

    if self.revdlg == None:
      self.revdlg = revolutionsdlg.RevolutionsDlg(None)
      self.revdlg.initialize(self.horoscope)  
    self.revdlg.CenterOnParent()

    val = self.revdlg.ShowModal()
    if val == wx.ID_OK: 
      wx.BeginBusyCursor()

      revs = revolutions.Revolutions()
      result = revs.compute(self.revdlg.typecb.GetCurrentSelection(), int(self.revdlg.year.GetValue()), int(self.revdlg.month.GetValue()), int(self.revdlg.day.GetValue()), self.horoscope)

      wx.EndBusyCursor()

      t1, t2, t3, t4, t5, t6 = revs.t[0], revs.t[1], revs.t[2], revs.t[3], revs.t[4], revs.t[5] 
      if result:
        if self.options.ayanamsha != 0 and self.revdlg.typecb.GetCurrentSelection() == 0:
          t1, t2, t3, t4, t5, t6 = self.calcPrecNutCorrectedSolar(revs) #y, m, d, hour, min, sec

        dlg = timespacedlg.TimeSpaceDlg(self, mtexts.txts['Revolutions'], self.options.langid)
        ti = (t1, t2, t3, t4, t5, t6, chart.Time.GREGORIAN, chart.Time.GREENWICH, 0, 0)
        dlg.initialize(self.horoscope, ti)  
        dlg.CenterOnParent()

        val = dlg.ShowModal()

        if val == wx.ID_OK:
          wait = wx.BusyCursor()
          direc = dlg.placerbE.GetValue()
          hemis = dlg.placerbN.GetValue()
          place = chart.Place(dlg.birthplace.GetValue(), int(dlg.londeg.GetValue()), int(dlg.lonmin.GetValue()), 0, direc, int(dlg.latdeg.GetValue()), int(dlg.latmin.GetValue()), 0, hemis, 0)#the same as for the transits

          plus = True
          if dlg.pluscb.GetCurrentSelection() == 1:
            plus = False
          time = chart.Time(t1, t2, t3, t4, t5, t6, False, self.horoscope.time.cal, chart.Time.GREENWICH, plus, 0, 0, False, place, False)

          revtype = chart.Chart.REVOLUTION
          if self.revdlg.typecb.GetCurrentSelection() == 0:
            revtype = chart.Chart.SOLAR
          elif self.revdlg.typecb.GetCurrentSelection() == 1:
            revtype = chart.Chart.LUNAR

          revolution = chart.Chart(self.horoscope.name, self.horoscope.male, time, place, revtype, '', self.options, False)

          rw = transitframe.TransitFrame(self, self.title.replace(mtexts.typeList[self.horoscope.htype], mtexts.typeList[revtype]+' ('+str(time.year)+'.'+common.common.months[time.month-1]+'.'+str(time.day)+' '+str(time.hour)+':'+str(time.minute).zfill(2)+':'+str(time.second).zfill(2)+'('+mtexts.txts['GMT']+'))'), revolution, self.horoscope, self.options)
          rw.Show(True)
    
        dlg.Destroy()
      else:
        dlgm = wx.MessageDialog(self, mtexts.txts['CouldnotComputeRevolution'], mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
        dlgm.ShowModal()
        dlgm.Destroy()#


  def calcPrecNutCorrectedSolar(self, revs):
    time = chart.Time(revs.t[0], revs.t[1], revs.t[2], revs.t[3], revs.t[4], revs.t[5], False, self.horoscope.time.cal, chart.Time.GREENWICH, False, 0, 0, False, self.horoscope.place, False)
    #The algorithm of the Janus astrological program
    jdSol = time.jd
    JD1900 = 2415020.5
    FBAyanamsa1900 = astrology.swe_get_ayanamsa_ut(JD1900)

    rflag, dat, serr = astrology.swe_calc_ut(JD1900, astrology.SE_ECL_NUT, 0)
    NutLon1900 = dat[2]
    SVP1900 = 360.0-FBAyanamsa1900-NutLon1900

    #calc natalprecfrom1900
    rflag, dat, serr = astrology.swe_calc_ut(self.horoscope.time.jd, astrology.SE_ECL_NUT, 0)
    NutLonNatal = dat[2]
    SVPNatal = 360.0-self.horoscope.ayanamsha-NutLonNatal
    NatalChartPrecessionFrom1900 = SVPNatal-SVP1900

    #Calc SVP for return date
    NatalSunLon = self.horoscope.planets.planets[astrology.SE_SUN].data[planets.Planet.LONG]
    DiffAngle = 50.0 # this is my idea
    pflag = astrology.SEFLG_SWIEPH+astrology.SEFLG_SPEED

    #Keep recalculating transiting Sun position using new jdSol until
    #DiffAngle is small enough.
    while (DiffAngle > 0.00001):
      rflag, dat, serr = astrology.swe_calc_ut(jdSol, astrology.SE_SUN, pflag)
      TranSunLon = dat[0]
      TranSunVel = dat[3]

      rflag, dat, serr = astrology.swe_calc_ut(jdSol, astrology.SE_ECL_NUT, 0)
      FBAyanamsaReturn = astrology.swe_get_ayanamsa_ut(jdSol)
      NutLonReturn = dat[2]
      SVPReturn = 360.0-FBAyanamsaReturn-NutLonReturn

      SolPrecessionFrom1900 = SVPReturn-SVP1900
      Precession = SolPrecessionFrom1900-NatalChartPrecessionFrom1900 #

      TranSunLon = TranSunLon+Precession

      DiffAngle = NatalSunLon-TranSunLon

      if math.fabs(DiffAngle) > 180.0:
        DiffAngle = DiffAngle-util.sgn(DiffAngle)*360.0

      CorrectionJD = DiffAngle/TranSunVel

      jdSol = jdSol+CorrectionJD

      fromjdtime = astrology.swe_revjul(jdSol, astrology.SE_GREG_CAL)

    h, mi, s = util.decToDeg(fromjdtime[3])
    return fromjdtime[0], fromjdtime[1], fromjdtime[2], h, mi, s


  def onSunTransits(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if self.horoscope.time.bc:
      dlgm = wx.MessageDialog(self, mtexts.txts['NotAvailable'], '', wx.OK|wx.ICON_INFORMATION)
      dlgm.ShowModal()
      dlgm.Destroy()
      return

    if self.suntrdlg == None:
      self.suntrdlg = suntransitsdlg.SunTransitsDlg(None)
      self.suntrdlg.initialize(self.horoscope)

    self.suntrdlg.CenterOnParent()

    val = self.suntrdlg.ShowModal()
    if val == wx.ID_OK: 
      wx.BeginBusyCursor()

      lons = (self.horoscope.houses.ascmc[houses.Houses.ASC], self.horoscope.houses.ascmc[houses.Houses.MC], self.horoscope.planets.planets[astrology.SE_SUN].data[planets.Planet.LONG], self.horoscope.planets.planets[astrology.SE_MOON].data[planets.Planet.LONG], self.horoscope.planets.planets[astrology.SE_MERCURY].data[planets.Planet.LONG], self.horoscope.planets.planets[astrology.SE_VENUS].data[planets.Planet.LONG], self.horoscope.planets.planets[astrology.SE_MARS].data[planets.Planet.LONG], self.horoscope.planets.planets[astrology.SE_JUPITER].data[planets.Planet.LONG], self.horoscope.planets.planets[astrology.SE_SATURN].data[planets.Planet.LONG], self.horoscope.planets.planets[astrology.SE_URANUS].data[planets.Planet.LONG], self.horoscope.planets.planets[astrology.SE_NEPTUNE].data[planets.Planet.LONG], self.horoscope.planets.planets[astrology.SE_PLUTO].data[planets.Planet.LONG])
      btns = (self.suntrdlg.ascrb.GetValue(), self.suntrdlg.mcrb.GetValue(), self.suntrdlg.sunrb.GetValue(), self.suntrdlg.moonrb.GetValue(), self.suntrdlg.mercuryrb.GetValue(), self.suntrdlg.venusrb.GetValue(), self.suntrdlg.marsrb.GetValue(), self.suntrdlg.jupiterrb.GetValue(), self.suntrdlg.saturnrb.GetValue(), self.suntrdlg.uranusrb.GetValue(), self.suntrdlg.neptunerb.GetValue(), self.suntrdlg.plutorb.GetValue())

      trlon = lons[0]
      for i in range(len(btns)):
        if btns[i]:
          trlon = lons[i]
      
      suntrs = suntransits.SunTransits()
      result = suntrs.compute(int(self.suntrdlg.year.GetValue()), int(self.suntrdlg.month.GetValue()), int(self.suntrdlg.day.GetValue()), self.horoscope, trlon)

      wx.EndBusyCursor()

      if result:
        dlg = timespacedlg.TimeSpaceDlg(self, mtexts.txts['SunTransits'], self.options.langid)
        ti = (suntrs.t[0], suntrs.t[1], suntrs.t[2], suntrs.t[3], suntrs.t[4], suntrs.t[5], chart.Time.GREGORIAN, chart.Time.GREENWICH, 0, 0)
        dlg.initialize(self.horoscope, ti)  
        dlg.CenterOnParent()

        val = dlg.ShowModal()

        if val == wx.ID_OK:
          wait = wx.BusyCursor()
          direc = dlg.placerbE.GetValue()
          hemis = dlg.placerbN.GetValue()
          place = chart.Place(dlg.birthplace.GetValue(), int(dlg.londeg.GetValue()), int(dlg.lonmin.GetValue()), 0, direc, int(dlg.latdeg.GetValue()), int(dlg.latmin.GetValue()), 0, hemis, 0)#Same as for the transits

          plus = True
          if dlg.pluscb.GetCurrentSelection() == 1:
            plus = False
          time = chart.Time(suntrs.t[0], suntrs.t[1], suntrs.t[2], suntrs.t[3], suntrs.t[4], suntrs.t[5], False, chart.Time.GREGORIAN, chart.Time.GREENWICH, plus, 0, 0, False, place, False)

          suntrschart = chart.Chart(self.horoscope.name, self.horoscope.male, time, place, chart.Chart.TRANSIT, '', self.options, False)

          rw = transitframe.TransitFrame(self, self.title.replace(mtexts.typeList[self.horoscope.htype], mtexts.typeList[chart.Chart.TRANSIT]+' ('+str(time.year)+'.'+common.common.months[time.month-1]+'.'+str(time.day)+' '+str(time.hour)+':'+str(time.minute).zfill(2)+':'+str(time.second).zfill(2)+'('+mtexts.txts['GMT']+'))'), suntrschart, self.horoscope, self.options)
          rw.Show(True)

        dlg.Destroy()

      else:
        dlgm = wx.MessageDialog(self, mtexts.txts['CouldnotComputeTransit'], mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
        dlgm.ShowModal()
        dlgm.Destroy()#


  def onSecondaryDirs(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if self.horoscope.time.bc:
      dlgm = wx.MessageDialog(self, mtexts.txts['NotAvailable'], '', wx.OK|wx.ICON_INFORMATION)
      dlgm.ShowModal()
      dlgm.Destroy()
      return

    if self.secdirdlg == None:
      self.secdirdlg = secdirdlg.SecondaryDirsDlg(None)
      self.secdirdlg.initialize()

    self.secdirdlg.CenterOnParent()

    val = self.secdirdlg.ShowModal()
    if val == wx.ID_OK:
      age = int(self.secdirdlg.age.GetValue())
      direct = self.secdirdlg.directrb.GetValue()
      soltime = self.secdirdlg.solartimerb.GetValue()

      zt = chart.Time.LOCALMEAN
      if soltime:
        zt = chart.Time.LOCALAPPARENT
      zh = 0
      zm = 0

      sdir = secdir.SecDir(self.horoscope, age, direct, soltime)
      y, m, d, hour, minute, second = sdir.compute()

      dlg = timespacedlg.TimeSpaceDlg(self, mtexts.txts['SecondaryDirs'], self.options.langid)
      ti = (y, m, d, hour, minute, second, self.horoscope.time.cal, zt, zh, zm)
      dlg.initialize(self.horoscope, ti)  
      dlg.CenterOnParent()

      val = dlg.ShowModal()

      if val == wx.ID_OK:
        wait = wx.BusyCursor()

        direc = dlg.placerbE.GetValue()
        hemis = dlg.placerbN.GetValue()
        place = chart.Place(dlg.birthplace.GetValue(), int(dlg.londeg.GetValue()), int(dlg.lonmin.GetValue()), 0, direc, int(dlg.latdeg.GetValue()), int(dlg.latmin.GetValue()), 0, hemis, 0)#Also, no altitude neccesary here

        plus = True
        if dlg.pluscb.GetCurrentSelection() == 1:
          plus = False
        time = chart.Time(y, m, d, hour, minute, second, False, self.horoscope.time.cal, zt, plus, zh, zm, False, place, False)

        secdirchart = chart.Chart(self.horoscope.name, self.horoscope.male, time, place, chart.Chart.TRANSIT, '', self.options, False)

        sf = secdirframe.SecDirFrame(self, self.title.replace(mtexts.typeList[self.horoscope.htype], mtexts.txts['SecondaryDir']+' ('+str(time.year)+'.'+common.common.months[time.month-1]+'.'+str(time.day)+' '+str(time.hour)+':'+str(time.minute).zfill(2)+':'+str(time.second).zfill(2)+')'), secdirchart, self.horoscope, self.options)
        sf.Show(True)

        stepdlg = stepperdlg.StepperDlg(sf, self.horoscope, age, direct, soltime, self.options, self.title)
        stepdlg.CenterOnParent()
        stepdlg.Show(True)

      dlg.Destroy()


  def onElections(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if self.horoscope.time.bc:
      dlgm = wx.MessageDialog(self, mtexts.txts['NotAvailable'], '', wx.OK|wx.ICON_INFORMATION)
      dlgm.ShowModal()
      dlgm.Destroy()
      return

    time = chart.Time(self.horoscope.time.origyear, self.horoscope.time.origmonth, self.horoscope.time.origday, self.horoscope.time.hour, self.horoscope.time.minute, self.horoscope.time.second, self.horoscope.time.bc, self.horoscope.time.cal, self.horoscope.time.zt, self.horoscope.time.plus, self.horoscope.time.zh, self.horoscope.time.zm, self.horoscope.time.daylightsaving, self.horoscope.place, False)

    electionchart = chart.Chart(self.horoscope.name, self.horoscope.male, time, self.horoscope.place, chart.Chart.TRANSIT, '', self.options, False)

    ef = electionsframe.ElectionsFrame(self, self.title.replace(mtexts.typeList[self.horoscope.htype], mtexts.txts['Elections']+' ('+str(time.origyear)+'.'+common.common.months[time.origmonth-1]+'.'+str(time.origday)+' '+str(time.hour)+':'+str(time.minute).zfill(2)+':'+str(time.second).zfill(2)+')'), electionchart, self.horoscope, self.options)
    ef.Show(True)

    estepdlg = electionstepperdlg.ElectionStepperDlg(ef, self.horoscope, self.options, self.title)
    estepdlg.CenterOnParent()
    estepdlg.Show(True)


  def onSquareChart(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    sc = squarechartframe.SquareChartFrame(self, self.title, self.horoscope, self.options)
    sc.Show(True)


  def onProfectionsChart(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if self.horoscope.time.bc:
      dlgm = wx.MessageDialog(self, mtexts.txts['NotAvailable'], '', wx.OK|wx.ICON_INFORMATION)
      dlgm.ShowModal()
      dlgm.Destroy()
      return

    pdlg = profdlg.ProfDlg(self, self.horoscope.time.jd, self.horoscope.place)
#   h, m, s = util.decToDeg(self.horoscope.time.time)
    pdlg.initialize(self.horoscope.time.year, self.horoscope.time.month, self.horoscope.time.day, 12, 0, 0)

    pdlg.CenterOnParent()

    val = pdlg.ShowModal()
    if val == wx.ID_OK:
      y = int(pdlg.year.GetValue())
      m = int(pdlg.month.GetValue())
      d = int(pdlg.day.GetValue())
      h = int(pdlg.hour.GetValue())
      mi = int(pdlg.minute.GetValue())
      s = int(pdlg.second.GetValue())
      proftype = chart.Chart.YEAR

      t = h+mi/60.0+s/3600.0

      if self.options.zodprof:
        prof = profections.Profections(self.horoscope, y, m, d, t)
        pchart = chart.Chart(self.horoscope.name, self.horoscope.male, self.horoscope.time, self.horoscope.place, chart.Chart.PROFECTION, '', self.options, False, proftype)
        pchart.calcProfPos(prof)
      else:
        if not self.options.usezodprojsprof and (y == self.horoscope.time.year or (y-self.horoscope.time.year) % 12 == 0) and m == self.horoscope.time.month and d == self.horoscope.time.day:
          pchart = self.horoscope
        else:
          prof = munprofections.MunProfections(self.horoscope, y, m, d, t)
          proflondeg, proflonmin, proflonsec = util.decToDeg(prof.lonZ)
          profplace = chart.Place(mtexts.txts['Profections'], proflondeg, proflonmin, proflonsec, prof.east, self.horoscope.place.deglat, self.horoscope.place.minlat, self.horoscope.place.seclat, self.horoscope.place.north, self.horoscope.place.altitude)
          pchart = chart.Chart(self.horoscope.name, self.horoscope.male, self.horoscope.time, profplace, chart.Chart.PROFECTION, '', self.options, False, proftype, self.options.usezodprojsprof)
          pchartpls = chart.Chart(self.horoscope.name, self.horoscope.male, self.horoscope.time, self.horoscope.place, chart.Chart.PROFECTION, '', self.options, False, proftype, self.options.usezodprojsprof)
          #modify planets ...
          pchart.planets.calcMundaneProfPos(pchart.houses.ascmc2, pchartpls.planets.planets, self.horoscope.place.lat, self.horoscope.obl[0])

          #modify lof
          pchart.fortune.calcMundaneProfPos(pchart.houses.ascmc2, pchartpls.fortune, self.horoscope.place.lat, self.horoscope.obl[0])
  
          #recalc AspMatrix
          pchart.calcAspMatrix()

      pf = profectionsframe.ProfectionsFrame(self, self.title.replace(mtexts.typeList[self.horoscope.htype], mtexts.txts['Profections']+' ('+str(y)+'.'+str(m)+'.'+str(d)+' '+str(h).zfill(2)+':'+str(mi).zfill(2)+':'+str(s).zfill(2)+')'), pchart, self.horoscope, self.options)
      pf.Show(True)

      pstepdlg = profectionstepperdlg.ProfectionStepperDlg(pf, self.horoscope, y, m, d, t, self.options, self.title)
      pstepdlg.CenterOnParent()
      pstepdlg.Show(True)

    pdlg.Destroy()


  def onMundaneChart(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

#   if self.horoscope.time.bc:
#     dlgm = wx.MessageDialog(self, mtexts.txts['NotAvailable'], '', wx.OK|wx.ICON_INFORMATION)
#     dlgm.ShowModal()
#     dlgm.Destroy()
#     return

    mf = mundaneframe.MundaneFrame(self, self.title, self.options, self.horoscope, None)
    mf.Show(True)


  #Options-menu
  def onAppearance1(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    wx.BeginBusyCursor()
    dlg = appearance1dlg.Appearance1Dlg(self)
    dlg.CenterOnParent()
    wx.EndBusyCursor()
    dlg.fill(self.options)

    topocentric = self.options.topocentric
#   traditionalaspects = self.options.traditionalaspects
    netb = self.options.netbook
    val = dlg.ShowModal()
    if val == wx.ID_OK: 
      if(dlg.check(self.options)):
        self.enableOptMenus(True)

        if self.options.autosave:
          if self.options.saveAppearance1():
            self.moptions.Enable(self.ID_SaveOpts, False)

        if netb != self.options.netbook:
          if self.options.subprimarydir == primdirs.PrimDirs.BOTH:
            self.options.subprimarydir = primdirs.PrimDirs.MUNDANE

        if not self.splash:
          self.closeChildWnds()


          if topocentric != self.options.topocentric:
            self.horoscope.recalc()
#         elif traditionalaspects != self.options.traditionalaspects:
#           self.horoscope.recalcAlmutens()

          self.drawBkg()
          self.Refresh()

    dlg.Destroy()


  def onAppearance2(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    wx.BeginBusyCursor()
    dlg = appearance2dlg.Appearance2Dlg(self)
    dlg.CenterOnParent()
    wx.EndBusyCursor()
    dlg.fill(self.options)

    val = dlg.ShowModal()
    if val == wx.ID_OK: 
      if dlg.check(self.options):
        self.enableOptMenus(True)

        if self.options.autosave:
          if self.options.saveAppearance2():
            self.moptions.Enable(self.ID_SaveOpts, False)

        if not self.splash:
          self.closeChildWnds()
          self.drawBkg()
          self.Refresh()

    dlg.Destroy()


  def onSymbols(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    dlg = symbolsdlg.SymbolsDlg(self)
    dlg.CenterOnParent()
    dlg.fill(self.options)

    val = dlg.ShowModal()
    if val == wx.ID_OK: 
      if dlg.check(self.options):
        self.enableOptMenus(True)

        common.common.update(self.options)

        if self.options.autosave:
          if self.options.saveSymbols():
            self.moptions.Enable(self.ID_SaveOpts, False)

        if not self.splash:
          self.closeChildWnds()
          self.drawBkg()
          self.Refresh()

    dlg.Destroy()


  def onDignities(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    dlg = dignitiesdlg.DignitiesDlg(self, self.options)
    dlg.CenterOnParent()

    val = dlg.ShowModal()
    if val == wx.ID_OK: 
      if dlg.check(self.options):
        self.enableOptMenus(True)

        if self.options.autosave:
          if self.options.saveDignities():
            self.moptions.Enable(self.ID_SaveOpts, False)

        if not self.splash:
          self.closeChildWnds()
          self.drawBkg()
          self.Refresh()

    dlg.Destroy()


  def onAyanamsha(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    dlg = ayanamshadlg.AyanamshaDlg(self)
    dlg.CenterOnParent()
    dlg.fill(self.options)

    ayan = self.options.ayanamsha
    val = dlg.ShowModal()
    if val == wx.ID_OK: 
      if dlg.check(self.options):
        self.enableOptMenus(True)

        if self.options.autosave:
          if self.options.saveAyanamsa():
            self.moptions.Enable(self.ID_SaveOpts, False)

        if not self.splash:
          self.closeChildWnds()

          if ayan != self.options.ayanamsha:
            self.horoscope.recalc()

          self.drawBkg()
          self.Refresh()

    dlg.Destroy()


  def onColors(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    dlg = colorsdlg.ColorsDlg(self)
    dlg.CenterOnParent()
    dlg.fill(self.options)

    val = dlg.ShowModal()
    if val == wx.ID_OK: 
      if dlg.check(self.options):
        self.enableOptMenus(True)

        if self.options.autosave:
          if self.options.saveColors():
            self.moptions.Enable(self.ID_SaveOpts, False)

        if not self.splash:
          self.closeChildWnds()
          self.drawBkg()
          self.Refresh()

    dlg.Destroy()


  def onHouseSystem(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    typ = event.GetId()-self.hsbase
    hs = ('P', 'K', 'R', 'C', 'E', 'W', 'X', 'M', 'H', 'T', 'B', 'O')

    if self.options.hsys != hs[typ]:
      self.options.hsys = hs[typ]
      self.enableOptMenus(True)

      if self.options.autosave:
        if self.options.saveHouseSystem():
          self.moptions.Enable(self.ID_SaveOpts, False)

      if not self.splash:
        self.closeChildWnds()
        self.horoscope.setHouseSystem()
        self.horoscope.calcAspMatrix()
        self.horoscope.calcFixStarAspMatrix()
        self.horoscope.calcArabicParts()
        self.horoscope.recalcAlmutens()
        self.drawBkg()
        self.Refresh()


  def onNodes(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    typ = event.GetId()-self.nodebase
    nodes = (True, False)

    if self.options.meannode != nodes[typ]:
      self.options.meannode = nodes[typ]
      self.enableOptMenus(True)

      if self.options.autosave:
        if self.options.saveNodes():
          self.moptions.Enable(self.ID_SaveOpts, False)

      if not self.splash:
        self.closeChildWnds()
        self.horoscope.setNodes()
        self.horoscope.calcAspMatrix()
        self.horoscope.calcFixStarAspMatrix()
        self.drawBkg()
        self.Refresh()


  def onOrbs(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    dlg = orbisdlg.OrbisDlg(self, self.options)
    dlg.CenterOnParent()

    val = dlg.ShowModal()
    if val == wx.ID_OK: 
      dlg.save(dlg.currid)

      if dlg.check(self.options):
        self.enableOptMenus(True)

        if self.options.autosave:
          if self.options.saveOrbs():
            self.moptions.Enable(self.ID_SaveOpts, False)

        if not self.splash:
          self.closeChildWnds()
          self.horoscope.calcAspMatrix()
          self.horoscope.calcFixStarAspMatrix()
          self.horoscope.recalcAlmutens()
          self.drawBkg()
          self.Refresh()

    dlg.Destroy()


  def onFortune(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    dlg = fortunedlg.FortuneDlg(self)
    dlg.CenterOnParent()
    dlg.fill(self.options)

    val = dlg.ShowModal()
    if val == wx.ID_OK: 
      if dlg.check(self.options):
        self.enableOptMenus(True)

        if self.options.autosave:
          if self.options.saveFortune():
            self.moptions.Enable(self.ID_SaveOpts, False)

        if not self.splash:
          self.closeChildWnds()
          self.horoscope.calcFortune()
          self.horoscope.calcArabicParts()
          self.horoscope.calcAntiscia()
          self.horoscope.recalcAlmutens()
          self.drawBkg()
          self.Refresh()

    dlg.Destroy()


  def onArabicParts(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    wx.BeginBusyCursor()
    dlg = arabicpartsdlg.ArabicPartsDlg(self, self.options)
    dlg.CenterOnParent()
    dlg.fill(self.options)
    wx.EndBusyCursor()

    val = dlg.ShowModal()
    if val == wx.ID_OK: 
      ch, rem = dlg.check(self.options)
      if ch:
        self.enableOptMenus(True)

        if rem:
          if self.options.topicals != None:
            del self.options.topicals 
            self.options.topicals = None

        if self.options.autosave:
          if self.options.saveTopicalandParts():
            self.moptions.Enable(self.ID_SaveOpts, False)

        if not self.splash:
          self.closeChildWnds()
          self.horoscope.calcFortune()
          self.horoscope.calcAntiscia()
          self.horoscope.calcArabicParts()
          self.horoscope.recalcAlmutens()
          self.drawBkg()
          self.Refresh()

    dlg.Destroy()


  def onSyzygy(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    dlg = syzygydlg.SyzygyDlg(self)
    dlg.CenterOnParent()
    dlg.fill(self.options)

    val = dlg.ShowModal()
    if val == wx.ID_OK: 
      if dlg.check(self.options):
        self.enableOptMenus(True)

        if self.options.autosave:
          if self.options.saveSyzygy():
            self.moptions.Enable(self.ID_SaveOpts, False)

        if not self.splash:
          self.closeChildWnds()
          self.horoscope.calcSyzygy()
          self.horoscope.calcArabicParts()
          self.horoscope.recalcAlmutens()
          self.drawBkg()
          self.Refresh()

    dlg.Destroy()


  def onFixStarsOpt(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if not self.checkFixStars():
      return

    dlg = fixstarsdlg.FixStarsDlg(self, self.options.fixstars, common.common.ephepath)
    dlg.CenterOnParent()

    val = dlg.ShowModal()
    if val == wx.ID_OK: 
      if dlg.check(self.options.fixstars):
        self.enableOptMenus(True)

        self.options.clearPDFSSel()

        if self.options.autosave:
          if self.options.saveFixstars():
            self.moptions.Enable(self.ID_SaveOpts, False)

        if not self.splash:
          self.closeChildWnds()
          self.horoscope.rebuildFixStars()
          self.horoscope.calcFixStarAspMatrix()
          self.drawBkg()
          self.Refresh()

    dlg.Destroy()


  def onProfectionsOpt(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    dlg = profdlgopts.ProfDlgOpts(self)
    dlg.fill(self.options)
    dlg.CenterOnParent()

    val = dlg.ShowModal()
    if val == wx.ID_OK: 
      if dlg.check(self.options):
        self.enableOptMenus(True)

        if self.options.autosave:
          if self.options.saveProfections():
            self.moptions.Enable(self.ID_SaveOpts, False)

        if not self.splash:
          self.closeChildWnds()
          self.drawBkg()
          self.Refresh()

    dlg.Destroy()


  def onLanguages(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    dlg = langsdlg.LanguagesDlg(self, self.options.langid)
    dlg.CenterOnParent()

    val = dlg.ShowModal()
    if val == wx.ID_OK: 
      if dlg.check(self.options):
        self.enableOptMenus(True)

        if self.options.autosave:
          if self.options.saveLanguages():
            self.moptions.Enable(self.ID_SaveOpts, False)

    dlg.Destroy()


  def onTriplicities(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    wx.BeginBusyCursor()
    dlg = triplicitiesdlg.TriplicitiesDlg(self, self.options)
    dlg.CenterOnParent()
    wx.EndBusyCursor()
    val = dlg.ShowModal()
    if val == wx.ID_OK: 
      if dlg.check(self.options):
        self.enableOptMenus(True)

        if self.options.autosave:
          if self.options.saveTriplicities():
            self.moptions.Enable(self.ID_SaveOpts, False)

        if not self.splash:
          self.closeChildWnds()
          self.horoscope.recalcAlmutens()
#         self.drawBkg()
#         self.Refresh()

    dlg.Destroy()


  def onTerms(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    wx.BeginBusyCursor()
    dlg = termsdlg.TermsDlg(self, self.options)
    dlg.CenterOnParent()
    wx.EndBusyCursor()
    val = dlg.ShowModal()
    if val == wx.ID_OK: 
      if dlg.check(self.options):
        self.enableOptMenus(True)

        if self.options.autosave:
          if self.options.saveTerms():
            self.moptions.Enable(self.ID_SaveOpts, False)

        if not self.splash:
          self.closeChildWnds()
          self.horoscope.recalcAlmutens()
          self.drawBkg()
          self.Refresh()

    dlg.Destroy()


  def onDecans(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    wx.BeginBusyCursor()
    dlg = decansdlg.DecansDlg(self, self.options)
    dlg.CenterOnParent()
    wx.EndBusyCursor()
    val = dlg.ShowModal()
    if val == wx.ID_OK: 
      if dlg.check(self.options):
        self.enableOptMenus(True)

        if self.options.autosave:
          if self.options.saveDecans():
            self.moptions.Enable(self.ID_SaveOpts, False)

        if not self.splash:
          self.closeChildWnds()
          self.horoscope.recalcAlmutens()
          self.drawBkg()
          self.Refresh()

    dlg.Destroy()


  def onChartAlmuten(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    wx.BeginBusyCursor()
    dlg = almutenchartdlg.AlmutenChartDlg(self)
    dlg.fill(self.options)
    dlg.CenterOnParent()
    wx.EndBusyCursor()
    val = dlg.ShowModal()
    if val == wx.ID_OK: 
      if dlg.check(self.options):
        self.enableOptMenus(True)

        if self.options.autosave:
          if self.options.saveChartAlmuten():
            self.moptions.Enable(self.ID_SaveOpts, False)

        if not self.splash:
          self.closeChildWnds()
          self.horoscope.recalcAlmutens()
          self.drawBkg()
          self.Refresh()

    dlg.Destroy()


  def onTopicals(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    wx.BeginBusyCursor()
    dlg = almutentopicalsdlg.AlmutenTopicalsDlg(self, self.options)
    dlg.fill(self.options)
    dlg.CenterOnParent()
    wx.EndBusyCursor()
    val = dlg.ShowModal()
    if val == wx.ID_OK:
      if dlg.check(self.options):
        self.enableOptMenus(True)

        if self.options.autosave:
          if self.options.saveTopicalandParts():
            self.moptions.Enable(self.ID_SaveOpts, False)

        if not self.splash:
          self.closeChildWnds()
          self.horoscope.recalcAlmutens()
          self.drawBkg()
          self.Refresh()

    dlg.Destroy()


  def onPrimaryDirsOpt(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    wx.BeginBusyCursor()

    dlg = None
    if self.options.netbook:
      dlg = primarydirsdlgsmall.PrimDirsDlgSmall(self, self.options, common.common.ephepath)
    else:
      dlg = primarydirsdlg.PrimDirsDlg(self, self.options, common.common.ephepath)

    dlg.CenterOnParent()
    wx.EndBusyCursor()
    dlg.fill(self.options)

    val = dlg.ShowModal()
    if val == wx.ID_OK: 
      changed, changedU1, changedU2 = dlg.check(self.options)
      if changed or changedU1 or changedU2:
        if changedU1 and not self.splash:
          cpd = None
          if self.options.pdcustomer:
            cpd = customerpd.CustomerPD(self.options.pdcustomerlon[0], self.options.pdcustomerlon[1], self.options.pdcustomerlon[2], self.options.pdcustomerlat[0], self.options.pdcustomerlat[1], self.options.pdcustomerlat[2], self.options.pdcustomersouthern, self.horoscope.place.lat, self.horoscope.houses.ascmc2, self.horoscope.obl[0], self.horoscope.raequasc)
          self.horoscope.setCustomer(cpd)

        if changedU2 and not self.splash:
          cpd2 = None
          if self.options.pdcustomer2:
            cpd2 = customerpd.CustomerPD(self.options.pdcustomer2lon[0], self.options.pdcustomer2lon[1], self.options.pdcustomer2lon[2], self.options.pdcustomer2lat[0], self.options.pdcustomer2lat[1], self.options.pdcustomer2lat[2], self.options.pdcustomer2southern, self.horoscope.place.lat, self.horoscope.houses.ascmc2, self.horoscope.obl[0], self.horoscope.raequasc)
          self.horoscope.setCustomer2(cpd2)

        self.enableOptMenus(True)

        if self.options.autosave:
          if self.options.savePrimaryDirs():
            self.moptions.Enable(self.ID_SaveOpts, False)

        if not self.splash:
          self.closeChildWnds()
          self.drawBkg()
          self.Refresh()

    dlg.Destroy()


  def onPrimaryKeys(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    dlg = primarykeysdlg.PrimaryKeysDlg(self, self.options)
    dlg.CenterOnParent()
    dlg.fill(self.options)

    val = dlg.ShowModal()
    if val == wx.ID_OK: 
      
      if dlg.check(self.options):
        self.enableOptMenus(True)

        if self.options.autosave:
          if self.options.savePrimaryKeys():
            self.moptions.Enable(self.ID_SaveOpts, False)

        if not self.splash:
          self.closeChildWnds()
          self.drawBkg()
          self.Refresh()

    dlg.Destroy()


  def onPDsInChartOptZod(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    dlg = pdsinchartdlgopts.PDsInChartsDlgOpts(self)
    dlg.fill(self.options)
    dlg.CenterOnParent()

    val = dlg.ShowModal()
    if val == wx.ID_OK: 
      if dlg.check(self.options):
        self.enableOptMenus(True)

        if self.options.autosave:
          if self.options.savePDsInChart():
            self.moptions.Enable(self.ID_SaveOpts, False)

        if not self.splash:
          self.closeChildWnds()
          self.drawBkg()
          self.Refresh()

    dlg.Destroy()


  def onPDsInChartOptMun(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    dlg = pdsinchartterrdlgopts.PDsInChartsTerrDlgOpts(self)
    dlg.fill(self.options)
    dlg.CenterOnParent()

    val = dlg.ShowModal()
    if val == wx.ID_OK: 
      if dlg.check(self.options):
        self.enableOptMenus(True)

        if self.options.autosave:
          if self.options.savePDsInChart():
            self.moptions.Enable(self.ID_SaveOpts, False)

        if not self.splash:
          self.closeChildWnds()
          self.drawBkg()
          self.Refresh()

    dlg.Destroy()


  def onAutoSaveOpts(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    self.options.autosave = self.autosave.IsChecked()
    if self.options.autosave:
      if self.options.save():
        self.moptions.Enable(self.ID_SaveOpts, False)


  def onSaveOpts(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    if self.options.save():
      self.moptions.Enable(self.ID_SaveOpts, False)


  def onReload(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    dlg = wx.MessageDialog(self, mtexts.txts['AreYouSure'], mtexts.txts['Confirm'], wx.YES_NO|wx.ICON_QUESTION)
    val = dlg.ShowModal()
    if val == wx.ID_YES:
      if self.options.checkOptsFiles():
        self.options.removeOptsFiles()
      self.options.reload()
      common.common.update(self.options)
      self.enableOptMenus(False)
      self.setHouse()
      self.setNode()
      self.setAutoSave()
      if not self.splash:
        self.closeChildWnds()
        self.horoscope.recalc()
        self.drawBkg()
        self.Refresh()


  def onHelp(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    fname = os.path.join('Res', mtexts.helptxt)

    if not os.path.exists(fname):
      txt = fname+' '+mtexts.txts['NotFound']
      dlgm = wx.MessageDialog(self, txt, mtexts.txts['Error'], wx.OK|wx.ICON_INFORMATION)
      dlgm.ShowModal()
      dlgm.Destroy()
    else:
      hframe = htmlhelpframe.HtmlHelpFrame(self, -1, mtexts.txts['Morinus'], fname)
      hframe.Show(True)


  def onAbout(self, event):
    #Because on Windows the EVT_MENU_CLOSE event is not sent in case of accelerator-keys
    if wx.Platform == '__WXMSW__' and not self.splash:
      self.handleStatusBar(True)

    info = wx.AboutDialogInfo()
    info.Name = mtexts.txts['Morinus']
    info.Version = '6.2'
    info.Copyright = mtexts.txts['FreeSoft']
    info.Description = mtexts.txts['Description']+str(astrology.swe_version())
    info.WebSite = 'http://sites.google.com/site/pymorinus/', 'http://sites.google.com/site/pymorinus/'
    info.Developers = ['Robert Nagy (Hungary); robert.pluto@gmail.com (programming and astrology)\nPhilippe Epaud(France); philipeau@free.fr (french translation)\nMargherita Fiorello (Italy); margherita.fiorello@gmail.com (astrology, italian translation)\nMartin Gansten (Sweden); http://www.martingansten.com/ (astrology)\nJaime Chica Londoño(Colombia); aulavirtual@astrochart.org (spanish translation)\nRoberto Luporini (Italy); roberto.luporini@tiscali.it (Astrological astronomy)\nPetr Radek (Czech Rep.); petr_radek@raz-dva.cz (astrology)\nEndre Csaba Simon (Finland); secsaba@gmail.com (programming and astrology)\nDenis Steinhoff (Israel); denis@steindan.com (astrology, russian translation)\nVáclav Jan Špirhanzl (Czech Rep.); vjs.morinus@gmail.com (MacOS version)']
    info.License = mtexts.licensetxt
    
    wx.AboutBox(info)


  #Misc
  def setHouse(self):
    sysh = (self.itplac, self.itkoch, self.itregio, self.itcampa, self.itequal, self.itwholesign, self.itaxial, self.itmorin, self.ithoriz, self.itpage, self.italcab, self.itporph)
    for i in range(len(sysh)):
      if houses.Houses.hsystems[i] == self.options.hsys:
        sysh[i].Check(True)


  def setNode(self):
    if self.options.meannode:
      self.meanitem.Check(True)
    else:
      self.trueitem.Check(True)


  def setAutoSave(self):
    self.autosave.Check(self.options.autosave)


  def closeChildWnds(self):
    li = self.GetChildren()
    for ch in li:
      x,y = ch.GetClientSize()
      if ch.GetName() != 'status_line' and y > 50:
        ch.Destroy()


  def onMenuOpen(self, event):
    if not self.splash:
      self.handleStatusBar(False)


  def onMenuClose(self, event):
    if not self.splash:
      self.handleStatusBar(True)


  def enableMenus(self, bEnable):
    self.mhoros.Enable(self.ID_New, not bEnable)
    self.mhoros.Enable(self.ID_Data, bEnable)
    self.mhoros.Enable(self.ID_Save, bEnable)
    self.mhoros.Enable(self.ID_SaveAsBitmap, bEnable)
    self.mhoros.Enable(self.ID_Synastry, bEnable)
    self.mhoros.Enable(self.ID_Close, bEnable)
    self.mtable.Enable(self.ID_Positions, bEnable)
    self.mtable.Enable(self.ID_TAlmutens, bEnable)
    self.mtable.Enable(self.ID_AlmutenZodiacal, bEnable)
    self.mtable.Enable(self.ID_AlmutenChart, bEnable)
    self.mtable.Enable(self.ID_AlmutenTopical, bEnable)
    self.mtable.Enable(self.ID_Misc, bEnable)
    self.mtable.Enable(self.ID_MunPos, bEnable)
    self.mtable.Enable(self.ID_Antiscia, bEnable)
    self.mtable.Enable(self.ID_Aspects, bEnable)
    self.mtable.Enable(self.ID_FixStars, bEnable)
    self.mtable.Enable(self.ID_FixStarsAsps, bEnable)
    self.mtable.Enable(self.ID_Midpoints, bEnable)
    self.mtable.Enable(self.ID_RiseSet, bEnable)
    self.mtable.Enable(self.ID_Speeds, bEnable)
    self.mtable.Enable(self.ID_ZodPars, bEnable)
    self.mtable.Enable(self.ID_Arabians, bEnable)
    self.mtable.Enable(self.ID_Strip, bEnable)
    self.mtable.Enable(self.ID_PlanetaryHours, bEnable)
    self.mtable.Enable(self.ID_ExactTransits, bEnable)
    self.mtable.Enable(self.ID_Profections, bEnable)
    self.mtable.Enable(self.ID_CustomerSpeculum, bEnable)
    self.mtable.Enable(self.ID_PrimaryDirs, bEnable)
    self.mcharts.Enable(self.ID_Transits, bEnable)
    self.mcharts.Enable(self.ID_Revolutions, bEnable)
    self.mcharts.Enable(self.ID_SunTransits, bEnable)
    self.mcharts.Enable(self.ID_SecondaryDirs, bEnable)
    self.mcharts.Enable(self.ID_Elections, bEnable)
    self.mcharts.Enable(self.ID_SquareChart, bEnable)
    self.mcharts.Enable(self.ID_ProfectionsChart, bEnable)
    self.mcharts.Enable(self.ID_MundaneChart, bEnable)


  def enableOptMenus(self, bEnable):
    self.moptions.Enable(self.ID_SaveOpts, bEnable)
    self.moptions.Enable(self.ID_Reload, bEnable)


  def handleStatusBar(self, bHor):
    sb = self.GetStatusBar()
    if bHor:
      sb.SetFieldsCount(4)
      sb.SetStatusWidths([160, 80, 220, 220])
      txt = self.horoscope.name
      if self.horoscope.name == '':
        txt = mtexts.txts['Untitled']
      self.SetStatusText(txt, 0)
      self.SetStatusText(mtexts.typeList[self.horoscope.htype], 1)
      signtxt = ''
      if self.horoscope.time.bc:
        signtxt = '-'
      ztxt = mtexts.txts['UT']
      if self.horoscope.time.zt == chart.Time.ZONE:
        ztxt = mtexts.txts['ZN']
      if self.horoscope.time.zt == chart.Time.LOCALMEAN or self.horoscope.time.zt == chart.Time.LOCALAPPARENT:
        ztxt = mtexts.txts['LC']
      txt = signtxt+str(self.horoscope.time.origyear)+'.'+common.common.months[self.horoscope.time.origmonth-1]+'.'+(str(self.horoscope.time.origday)).zfill(2)+'. '+(str(self.horoscope.time.hour)).zfill(2)+':'+(str(self.horoscope.time.minute)).zfill(2)+':'+(str(self.horoscope.time.second)).zfill(2)+ztxt
      self.SetStatusText(txt, 2)
      deg_symbol = u'\u00b0'
      t1 = mtexts.txts['Long']+'.: '
      t2 = ' '+mtexts.txts['Lat']+'.: '
      dirlontxt = mtexts.txts['E']
      if not self.horoscope.place.east:
        dirlontxt = mtexts.txts['W']
      dirlattxt = mtexts.txts['N']
      if not self.horoscope.place.north:
        dirlattxt = mtexts.txts['S']

      txt = t1+(str(self.horoscope.place.deglon)).zfill(2)+deg_symbol+(str(self.horoscope.place.minlon)).zfill(2)+"'"+dirlontxt+t2+(str(self.horoscope.place.deglat)).zfill(2)+deg_symbol+(str(self.horoscope.place.minlat)).zfill(2)+"'"+dirlattxt
      self.SetStatusText(txt, 3)
    else:
      sb.SetFieldsCount(1)
      self.SetStatusText('')


  def handleCaption(self, bHor):
    if bHor:
      name = self.horoscope.name
      if name == '':
        name = mtexts.txts['Untitled']
      path = self.fpath
      if self.fpath == '':
        path = '-----'

      txt = self.origtitle+' - '+'['+name+', '+mtexts.typeList[self.horoscope.htype]+'; '+path+']'
      self.title = txt
    else:
      self.title = self.origtitle

    self.SetTitle(self.title)


  def checkFixStars(self):
    res = True
    fname = os.path.join(common.common.ephepath, 'fixstars.cat')

    if not os.path.exists(fname):
      txt = fname+' '+mtexts.txts['NotFound']
      dlgm = wx.MessageDialog(self, txt, mtexts.txts['Error'], wx.OK|wx.ICON_INFORMATION)
      dlgm.ShowModal()
      dlgm.Destroy()
      res = False

    return res


  def drawSplash(self):
    splashpath = os.path.join('Res', 'Morinus.jpg')
    self.buffer = wx.Image(splashpath).ConvertToBitmap()


  def drawBkg(self):
    gchart = None
    if self.options.theme == 0:
      gchart = graphchart.GraphChart(self.horoscope, self.GetClientSize(), self.options, self.options.bw)
    else:
      gchart = graphchart2.GraphChart2(self.horoscope, self.GetClientSize(), self.options, self.options.bw)

    if gchart != None:
      self.buffer = gchart.drawChart()


  def onEraseBackground(self, event):
    dc = wx.ClientDC(self)
#   dc = event.GetDC()
    x = y = 0

    if self.splash:
      wx.size = self.GetClientSize()
      x = wx.size.x/2-self.buffer.GetWidth()/2
      y = wx.size.y/2-self.buffer.GetHeight()/2

      bkgclr = self.options.clrbackground
      if self.options.bw:
        bkgclr = (255,255,255)
      self.SetBackgroundColour(bkgclr)
      self.ClearBackground()

    dc.DrawBitmap(self.buffer, x, y)


  def onPaint(self, event):
    dc = wx.ClientDC(self)
#   dc = event.GetDC()
    x = y = 0

    if self.splash:
      wx.size = self.GetClientSize()
      x = wx.size.x/2-self.buffer.GetWidth()/2
      y = wx.size.y/2-self.buffer.GetHeight()/2

      bkgclr = self.options.clrbackground
      if self.options.bw:
        bkgclr = (255,255,255)
      self.SetBackgroundColour(bkgclr)

    dc.DrawBitmap(self.buffer, x, y)


  def onSize(self, event):
    if self.splash:
      self.Refresh()
    else:
      self.drawBkg()
      self.Refresh()


  def calc(self):
    for planet in self.horoscope.planets.planets:
      print ''
      print '%s:' % planet.name

      (d, m, s) = decToDeg(planet.data[0])
      print 'lon: %02d %02d\' %02d"' % (d, m, s)
      (d, m, s) = decToDeg(planet.data[1])
      print 'lat: %02d %02d\' %02d"' % (d, m, s)
      (d, m, s) = decToDeg(planet.data[3])
      if planet.data[3] > 0:
        print 'speed: %02d %02d\' %02d"' % (d, m, s)
      else:
        print 'speed: %02d %02d\' %02d"  R' % (d, m, s)


    print ''
    print 'Houses'
    for i in range(1, Houses.HOUSE_NUM+1):
      (d, m, s) = decToDeg(self.horoscope.houses.cusps[i])
      print 'house[%d]: %02d %02d\' %02d"' % (i, d, m, s)

    print ''
    print 'Vars'
    xvars = ('Asc', 'MC', 'ARMC', 'Vertex', 'Equatorial Ascendant', 'Co-Asc', 'Co-Asc2', 'Polar Asc')
    for i in range(0, 8):
      (d, m, s) = decToDeg(self.horoscope.houses.ascmc[i])
      print '%s = %02d %02d\' %02d"' % (xvars[i], d, m, s)




