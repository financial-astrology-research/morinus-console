import os
import pickle
import copy
import chart
import primdirs
import mtexts


class Options:
    NONE = 0
    FIXSTARS = 1
    ANTIS = 2
    CANTIS = 3
# ###################################
# Elias change v 7.2.0
    DODECATEMORIA = 4
# ###################################

    MOON = 0
    ABOVEHOR = 1
    ABOVEHORNATAL = 2

    def __init__(self):
        #Appearance
        self.def_aspects = self.aspects = True
        self.aspect = [True, False, False, True, False, True, True, False, False, False, True]
        self.def_aspect = self.aspect[:]
        self.def_symbols = self.symbols = True
        self.def_traditionalaspects = self.traditionalaspects = False
        self.def_houses = self.houses = True
        self.def_positions = self.positions = False
        self.def_intables = self.intables = False
        self.def_bw = self.bw = False
        self.def_theme = self.theme = 0
        self.def_ascmcsize = self.ascmcsize = 5
        self.def_tablesize = self.tablesize = 0.75
        self.def_planetarydayhour = self.planetarydayhour = True
        self.def_housesystem = self.housesystem = True
        self.transcendental = [True, True, True]
        self.def_transcendental = self.transcendental[:]
        self.def_shownodes = self.shownodes = True
        self.def_aspectstonodes = self.aspectstonodes = False
        self.def_showlof = self.showlof = True
        self.def_showaspectstolof = self.showaspectstolof = False
        self.def_showterms = self.showterms = False
        self.def_showdecans = self.showdecans = False
        self.def_showfixstars = self.showfixstars = 0
        self.def_showfixstarsnodes = self.showfixstarsnodes = False
        self.def_showfixstarshcs = self.showfixstarshcs = False
        self.def_showfixstarslof = self.showfixstarslof = False
        self.def_topocentric = self.topocentric = False
        self.def_usetradfixstarnamespdlist = self.usetradfixstarnamespdlist = False
        self.def_netbook = self.netbook = False

        #AppearanceII
        self.speculums = [[True, True, True, True, False, False, False, False, False, False, False, False, False, False], [True, True, True, True, False, False, False, False, False, False, False, False, True, True]]
        self.def_speculums = copy.deepcopy(self.speculums)
# ########################################
# Roberto change - V 7.1.0
# ########################################

        self.intime = False
        self.def_intime = self.intime

        #Symbols
        self.def_uranus = self.uranus = True
        self.def_pluto = self.pluto = 0
        self.def_signs = self.signs = True

        #Dignities(planets, domicile, exaltatio)
                            #Sun
        self.dignities = [[[False, False, False, False, True, False, False, False, False, False, False, False], [True, False, False, False, False, False, False, False, False, False, False, False]],
                            #Moon
                            [[False, False, False, True, False, False, False, False, False, False, False, False], [False, True, False, False, False, False, False, False, False, False, False, False]],
                            #Mercury
                            [[False, False, True, False, False, True, False, False, False, False, False, False], [False, False, False, False, False, True, False, False, False, False, False, False]],
                            #Venus
                            [[False, True, False, False, False, False, True, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False, False, True]],
                            #Mars
                            [[True, False, False, False, False, False, False, True, False, False, False, False], [False, False, False, False, False, False, False, False, False, True, False, False]],
                            #Jupiter
                            [[False, False, False, False, False, False, False, False, True, False, False, True], [False, False, False, True, False, False, False, False, False, False, False, False]],
                            #Saturnus
                            [[False, False, False, False, False, False, False, False, False, True, True, False], [False, False, False, False, False, False, True, False, False, False, False, False]],
                            #Uranus
                            [[False, False, False, False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False, False, False]],
                            #Neptune
                            [[False, False, False, False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False, False, False]],
                            #Pluto
                            [[False, False, False, False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False, False, False]]]

        self.def_dignities = copy.deepcopy(self.dignities)

        #Minor dignities
        #Triplicities
        self.seltrip = 0
        self.def_seltrip = self.seltrip

        self.trips = [[[0, 5, 6],
                        [6, 2, 5],
                        [3, 4, 1],
                        [3, 1, 4]],
                        [[0, 5, 7],
                        [6, 2, 7],
                        [4, 4, 7],
                        [3, 1, 7]],
                        [[0, 4, 5],
                        [6, 3, 2],
                        [5, 1, 4],
                        [2, 6, 3]]]

        self.def_trips = copy.deepcopy(self.trips)

        #Terms
        self.selterm = 0
        self.def_selterm = self.selterm

        self.terms = [[[[5, 6], [3, 6], [2, 8], [4, 5], [6, 5]],
                    [[3, 8], [2, 6], [5, 8], [6, 5], [4, 3]],
                    [[2, 6], [5, 6], [3, 5], [4, 7], [6, 6]],
                    [[4, 7], [3, 6], [2, 6], [5, 7], [6, 4]],
                    [[5, 6], [3, 5], [6, 7], [2, 6], [4, 6]],
                    [[2, 7], [3, 10], [5, 4], [4, 7], [6, 2]],
                    [[6, 6], [2, 8], [5, 7], [3, 7], [4, 2]],
                    [[4, 7], [3, 4], [2, 8], [5, 5], [6, 6]],
                    [[5, 12], [3, 5], [2, 4], [6, 5], [4, 4]],
                    [[2, 7], [5, 7], [3, 8], [6, 4], [4, 4]],
                    [[2, 7], [3, 6], [5, 7], [4, 5], [6, 5]],
                    [[3, 12], [5, 4], [2, 3], [4, 9], [6, 2]]],
                    [[[5, 6], [3, 8], [2, 7], [4, 5], [6, 4]],
                    [[3, 8], [2, 7], [5, 7], [6, 2], [4, 6]],
                    [[2, 7], [5, 6], [3, 7], [4, 6], [6, 4]],
                    [[4, 6], [5, 7], [2, 7], [3, 7], [6, 3]],
                    [[5, 6], [2, 7], [6, 6], [3, 6], [4, 5]],
                    [[2, 7], [3, 6], [5, 5], [6, 6], [4, 6]],
                    [[6, 6], [3, 5], [2, 5], [5, 8], [4, 6]],
                    [[4, 6], [3, 7], [5, 8], [2, 6], [6, 3]],
                    [[5, 8], [3, 6], [2, 5], [6, 6], [4, 5]],
                    [[3, 6], [2, 6], [5, 7], [6, 6], [4, 5]],
                    [[6, 6], [2, 6], [3, 8], [5, 5], [4, 5]],
                    [[3, 8], [5, 6], [2, 6], [4, 5], [6, 5]]]]

        self.def_terms = copy.deepcopy(self.terms)

        #Decans
        self.seldecan = 0
        self.def_seldecan = self.seldecan

        self.decans = [[[4, 0, 3],
                        [2, 1, 6],
                        [5, 4, 0],
                        [3, 2, 1],
                        [6, 5, 4],
                        [0, 3, 2],
                        [1, 6, 5],
                        [4, 0, 3],
                        [2, 1, 6],
                        [5, 4, 0],
                        [3, 2, 1],
                        [6, 5, 4]],
                        [[4, 0, 5],
                        [3, 2, 6],
                        [2, 3, 6],
                        [1, 4, 5],
                        [0, 5, 4],
                        [2, 6, 3],
                        [3, 6, 2],
                        [4, 5, 1],
                        [5, 4, 0],
                        [6, 3, 2],
                        [6, 2, 3],
                        [5, 1, 4]]]

        self.def_decans = copy.deepcopy(self.decans)

        #ChartAlmuten
        self.def_oneruler = self.oneruler = True
        self.def_usedaynightorb = self.usedaynightorb = False
        self.def_dignityscores = self.dignityscores = [5, 4, 3, 2, 1]
        self.def_useaccidental = self.useaccidental = True
        self.def_housescores = self.housescores = [12, 6, 3, 9, 7, 1, 10, 5, 4, 11, 8, 2]
        self.def_sunphases = self.sunphases = [3, 2, 1]
        self.def_dayhourscores = self.dayhourscores = [7, 6]
        self.def_useexaltationmercury = self.useexaltationmercury = False

        #TopicalAlmuten and Parts
        self.def_topicals = self.topicals = None
            #Arabic Parts
        self.def_arabicpartsref = self.arabicpartsref = 0
        self.def_daynightorbdeg = self.daynightorbdeg = 0
        self.def_daynightorbmin = self.daynightorbmin = 0
        self.def_arabicparts = self.arabicparts = None

        #Ayanamsha
        self.def_ayanamsha = self.ayanamsha = 0

        #Colors
        self.def_clrframe = self.clrframe = (0,0,255)
        self.def_clrsigns = self.clrsigns = (0,0,255)
        self.def_clrAscMC = self.clrAscMC = (0,0,0)
        self.def_clrhouses = self.clrhouses = (0,0,255)
        self.def_clrhousenumbers = self.clrhousenumbers = (0,0,255)
        self.def_clrpositions = self.clrpositions = (0,0,128)

        self.def_clrperegrin = self.clrperegrin = (0,0,128)
        self.def_clrdomicil = self.clrdomicil = (2, 191, 2)
        self.def_clrexil = self.clrexil = (255,0,0)
        self.def_clrexal = self.clrexal = (255,215,0)
        self.def_clrcasus = self.clrcasus = (205,92,92)

        self.clraspect = [(0,0,128), (0,128,0), (128,0,0), (0,128,0), (0,128,0), (128,0,0), (0,128,0), (128,0,0), (0,128,0), (128,0,0), (128,0,0)]
        self.def_clraspect = self.clraspect[:]

        self.clrindividual = [(255,215,0), (0,191,255), (138,43,226), (0,128,0), (178,34,34), (0,0,255), (0,0,0), (0,0,128), (0,0,128), (0,0,128), (139,54,38), (205,96,144)]
        self.def_clrindividual = self.clrindividual[:]

        self.def_useplanetcolors = self.useplanetcolors = False

#       self.def_clrbackground = self.clrbackground = (wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWFRAME)).Get(False)
        self.def_clrbackground = self.clrbackground = (192,192,192)
        self.def_clrtable = self.clrtable = (0,0,0)
        self.def_clrtexts = self.clrtexts = (0,0,0)

        #Housesystem
        self.def_hsys = self.hsys = 'P'

        #Nodes
        self.def_meannode = self.meannode = True

        #Orbis
        self.orbis = [[5.0, 1.75, 1.75, 3.0, 1.75, 4.0, 4.0, 1.75, 1.75, 1.75, 5.0], [5.0, 1.75, 1.75, 3.0, 1.75, 4.0, 4.0, 1.75, 1.75, 1.75, 5.0], [3.5, 1.5, 1.5, 2.5, 1.5, 3.0, 3.0, 1.5, 1.5, 1.5, 3.5], [3.5, 1.5, 1.5, 2.5, 1.5, 3.0, 3.0, 1.5, 1.5, 1.5, 3.5], [3.5, 1.5, 1.5, 2.5, 1.5, 3.0, 3.0, 1.5, 1.5, 1.5, 3.5], [4.0, 1.5, 1.5, 3.0, 1.5, 3.5, 3.5, 1.5, 1.5, 1.5, 4.0], [4.0, 1.5, 1.5, 3.0, 1.5, 3.5, 3.5, 1.5, 1.5, 1.5, 4.0], [3.0, 1.0, 1.0, 2.0, 1.0, 2.5, 2.5, 1.0, 1.0, 1.0, 3.0], [3.0, 1.0, 1.0, 2.0, 1.0, 2.5, 2.5, 1.0, 1.0, 1.0, 3.0], [3.0, 1.0, 1.0, 2.0, 1.0, 2.5, 2.5, 1.0, 1.0, 1.0, 3.0], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]]
        self.def_orbis = copy.deepcopy(self.orbis)

        self.orbisplanetspar = [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0], [1.0, 1.0], [1.0, 1.0], [1.0, 1.0], [1.0, 1.0], [1.0, 1.0], [1.0, 1.0], [1.0, 1.0], [1.0, 1.0]]
        self.def_orbisplanetspar = copy.deepcopy(self.orbisplanetspar)

            # Houses
        self.orbisH = [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]
        self.def_orbisH = self.orbisH[:]

        self.orbisparH = [0.25, 0.25] #parallel/contraparallel
        self.def_orbisparH = self.orbisparH[:]

        self.def_orbiscuspH = self.orbiscuspH = 3.0

            # Asc,MC
        self.orbisAscMC = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
        self.def_orbisAscMC = self.orbisAscMC[:]

        self.orbisparAscMC = [0.5, 0.5]
        self.def_orbisparAscMC = self.orbisparAscMC[:]

        self.def_orbiscuspAscMC = self.orbiscuspAscMC = 5.0

        self.def_exact = self.exact = 1.0

        #Primary Dirs
        self.def_primarydir = self.primarydir = primdirs.PrimDirs.PLACIDIANSEMIARC
        self.def_subprimarydir = self.subprimarydir = primdirs.PrimDirs.MUNDANE
        self.def_subzodiacal = self.subzodiacal = primdirs.PrimDirs.SZNEITHER
        self.def_bianchini = self.bianchini = False

        self.sigascmc = [True, True]
        self.def_sigascmc = self.sigascmc[:]

        self.sighouses = False
        self.def_sighouses = self.sighouses

        self.sigplanets = [True, True, True, True, True, True, True, True, True, True, True, True]
        self.def_sigplanets = self.sigplanets[:]
        self.promplanets = [True, True, True, True, True, True, True, True, True, True, True, True]
        self.def_promplanets = self.promplanets[:]

        self.pdaspects = [True, False, False, True, False, True, True, False, False, False, True]
        self.def_pdaspects = self.pdaspects[:]

        self.pdmidpoints = False
        self.def_pdmidpoints = self.pdmidpoints

        self.pdparallels = [False, False]
        self.def_pdparallels = self.pdparallels[:]

        self.pdsecmotion = self.def_pdsecmotion = False
        self.pdsecmotioniter = self.def_pdsecmotioniter = 2 #3rd iter is the default

        self.zodpromsigasps = [True, False]
        self.def_zodpromsigasps = self.zodpromsigasps[:]
        self.ascmchcsasproms = False
        self.def_ascmchcsasproms = self.ascmchcsasproms

        self.pdfixstars = False
        self.def_pdfixstars = self.pdfixstars

        self.pdfixstarssel = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        self.def_pdfixstarssel = self.pdfixstarssel[:]

        self.pdlof = [False, False]
        self.def_pdlof = self.pdlof[:]

        self.pdsyzygy = self.def_pdsyzygy = False

        self.pdterms = False
        self.def_pdterms = self.pdterms

        self.pdantiscia = False
        self.def_pdantiscia = self.pdantiscia

        self.def_pdcustomer = self.pdcustomer = False
        self.pdcustomerlon = [0,0,0]
        self.def_pdcustomerlon = self.pdcustomerlon[:]
        self.pdcustomerlat = [0,0,0]
        self.def_pdcustomerlat = self.pdcustomerlat[:]
        self.def_pdcustomersouthern = self.pdcustomersouthern = False

        self.def_pdcustomer2 = self.pdcustomer2 = False
        self.pdcustomer2lon = [0,0,0]
        self.def_pdcustomer2lon = self.pdcustomer2lon[:]
        self.pdcustomer2lat = [0,0,0]
        self.def_pdcustomer2lat = self.pdcustomer2lat[:]
        self.def_pdcustomer2southern = self.pdcustomer2southern = False

        #PD-keys
        self.pdkeydyn = False
        self.def_pdkeydyn = self.pdkeydyn
        self.pdkeyd = primdirs.PrimDirs.TRUESOLAREQUATORIALARC
        self.def_pdkeyd = self.pdkeyd
        self.pdkeys = primdirs.PrimDirs.NAIBOD
        self.def_pdkeys = self.pdkeys
        self.pdkeydeg = 0
        self.def_pdkeydeg = self.pdkeydeg
        self.pdkeymin = 0
        self.def_pdkeymin = self.pdkeymin
        self.pdkeysec = 0
        self.def_pdkeysec = self.pdkeysec

        self.useregressive = False
        self.def_useregressive = self.useregressive

        #Lot of Fortune
        self.lotoffortune = chart.Chart.LFMOONSUN
        self.def_lotoffortune = self.lotoffortune

        #Syzygy
        self.def_syzmoon = self.syzmoon = Options.MOON

        #Fixstars
        self.fixstars = {'etTau':1.5, 'alTau':1.5, 'bePer':1.5, 'ga-1And':1.5, 'alSco':1.5, 'alBoo':1.5, 'deCnc':1.5, 'gaCnc':1.5, 'etUMa':1.5, 'alOri':1.5, 'alCen':1.5, 'alCar':1.5, 'alGem':1.5, 'beLeo':1.5, 'alPsA':1.5, 'alCrB':1.5, 'alPeg':1.5, 'beAnd':1.5, 'alUMi':1.5, 'beGem':1.5, 'M44':1.5, 'alCMi':1.5, 'alLeo':1.5, 'beOri':1.5, 'alCMa':1.5, 'alVir':1.5, 'alSer':1.5, 'alLyr':1.5, 'al-2Lib':1.5, 'beLib':1.5}

        self.def_fixstars = self.fixstars.copy()

        #Profections
        self.def_zodprof = self.zodprof = True
        self.def_usezodprojsprof = self.usezodprojsprof = False

# ########################################
# Roberto change - V 7.3.0
        #Firdaria
        self.def_isfirbonatti = self.isfirbonatti = True
# ########################################

# ########################################
# Roberto change - V 7.2.0
        #Default Location
        self.def_deflocname = self.deflocname = ''
        self.def_deflocplus = self.deflocplus = True
        self.def_defloczhour = self.defloczhour = 0
        self.def_defloczminute = self.defloczminute = 0
        self.def_deflocdst = self.deflocdst = False
        self.def_defloclondeg = self.defloclondeg = 0
        self.def_defloclonmin = self.defloclonmin = 0
        self.def_defloclatdeg = self.defloclatdeg = 0
        self.def_defloclatmin = self.defloclatmin = 0
        self.def_defloceast = self.defloceast = True
        self.def_deflocnorth = self.deflocnorth = True
        self.def_deflocalt = self.deflocalt = 0
# ########################################

        #PDsInChart
        self.def_pdincharttyp = self.pdincharttyp = 0
        self.def_pdinchartsecmotion = self.pdinchartsecmotion = False

        self.def_pdinchartterrsecmotion = self.pdinchartterrsecmotion = True

        #Languages
        self.def_langid = self.langid = 0

        self.autosave = False
        self.def_autosave = self.autosave

# ########################################
# Roberto change - V 7.2.0 / V 7.3.0
        self.optionsfilestxt = ('appearance1.opt', 'appearance2.opt', 'symbols.opt', 'dignities.opt', 'triplicities.opt', 'terms.opt', 'decans.opt', 'almutenchart.opt', 'almutentopicalandparts.opt', 'ayanamsa.opt', 'colors.opt', 'housesystem.opt', 'nodes.opt', 'orbs.opt', 'primarydirs.opt', 'primarykeys.opt', 'fortune.opt', 'syzygy.opt', 'fixedstars.opt', 'profections.opt', 'firdaria.opt', 'deflocation.opt', 'pdsinchart.opt', 'languages.opt', 'autosave.opt')
# ########################################
        self.optsdirtxt = 'Opts'

        self.appearance1opt = os.path.join(self.optsdirtxt, self.optionsfilestxt[0])
        self.appearance2opt = os.path.join(self.optsdirtxt, self.optionsfilestxt[1])
        self.symbolsopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[2])
        self.dignitiesopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[3])
        self.triplicitiesopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[4])
        self.termsopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[5])
        self.decansopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[6])
        self.chartalmutenopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[7])
        self.topicalandpartsopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[8])
        self.ayanamsaopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[9])
        self.colorsopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[10])
        self.housesystemopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[11])
        self.nodesopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[12])
        self.orbsopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[13])
        self.primarydirsopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[14])
        self.primarykeysopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[15])
        self.fortuneopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[16])
        self.syzygyopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[17])
        self.fixstarsopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[18])
        self.profectionsopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[19])
# ########################################
# Roberto change - V 7.3.0
        self.firdariaopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[20])
# ########################################
# ########################################
# Roberto change - V 7.2.0 / V 7.3.0
        self.deflocationopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[21])
        self.pdsinchartopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[22])
        self.languagesopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[23])
        self.autosaveopt = os.path.join(self.optsdirtxt, self.optionsfilestxt[24])
        self.load()
# ########################################

    def reload(self):
        #Appearance
        self.aspects = self.def_aspects
        self.aspect = self.def_aspect[:]
        self.symbols = self.def_symbols
        self.traditionalaspects = self.def_traditionalaspects
        self.houses = self.def_houses
        self.positions = self.def_positions
        self.intables = self.def_intables
        self.bw = self.def_bw
        self.theme = self.def_theme
        self.ascmcsize = self.def_ascmcsize
        self.tablesize = self.def_tablesize
        self.planetarydayhour = self.def_planetarydayhour
        self.housesystem = self.def_housesystem
        self.transcendental = self.def_transcendental[:]
        self.shownodes = self.def_shownodes
        self.aspectstonodes = self.def_aspectstonodes
        self.showlof = self.def_showlof
        self.showaspectstolof = self.def_showaspectstolof
        self.showterms = self.def_showterms
        self.showdecans = self.def_showdecans
        self.showfixstars = self.def_showfixstars
        self.showfixstarsnodes = self.def_showfixstarsnodes
        self.showfixstarshcs = self.def_showfixstarshcs
        self.showfixstarslof = self.def_showfixstarslof
        self.topocentric = self.def_topocentric
        self.usetradfixstarnamespdlist = self.def_usetradfixstarnamespdlist
        self.netbook = self.def_netbook

        #AppearanceII
        self.speculums = copy.deepcopy(self.def_speculums)
        self.intime = self.def_intime

        #Symbols
        self.uranus = self.def_uranus
        self.pluto = self.def_pluto
        self.signs = self.def_signs

        #Dignities
        self.dignities = copy.deepcopy(self.def_dignities)

        #Minor dignities
        self.seltrip = self.def_seltrip
        self.trips = copy.deepcopy(self.def_trips)
        self.selterm = self.def_selterm
        self.terms = copy.deepcopy(self.def_terms)
        self.seldecan = self.def_seldecan
        self.decans = copy.deepcopy(self.def_decans)

        #Chart Almutens
        self.oneruler = self.def_oneruler
        self.usedaynightorb = self.def_usedaynightorb
        self.dignityscores = self.def_dignityscores[:]
        self.useaccidental = self.def_useaccidental
        self.housescores = self.def_housescores[:]
        self.sunphases = self.def_sunphases[:]
        self.dayhourscores = self.def_dayhourscores[:]
        self.useexaltationmercury = self.def_useexaltationmercury

        #Topical almutens and Parts
        if self.topicals != None:
            del self.topicals
        self.topicals = self.def_topicals
        self.arabicpartsref = self.def_arabicpartsref
        self.daynightorbdeg = self.def_daynightorbdeg
        self.daynightorbmin = self.def_daynightorbmin
        if self.arabicparts != None:
            del self.arabicparts
        self.arabicparts = self.def_arabicparts

        #Ayanamsha
        self.ayanamsha = self.def_ayanamsha

        #Colors
        self.clrframe = self.def_clrframe
        self.clrsigns = self.def_clrsigns
        self.clrAscMC = self.def_clrAscMC
        self.clrhouses = self.def_clrhouses
        self.clrhousenumbers = self.def_clrhousenumbers
        self.clrpositions = self.def_clrpositions

        self.clrperegrin = self.def_clrperegrin
        self.clrdomicil = self.def_clrdomicil
        self.clrexil = self.def_clrexil
        self.clrexal = self.def_clrexal
        self.clrcasus = self.def_clrcasus

        self.clraspect = self.def_clraspect[:]

        self.clrindividual = self.def_clrindividual[:]

        self.useplanetcolors = self.def_useplanetcolors

        self.clrbackground = self.def_clrbackground
        self.clrtable = self.def_clrtable
        self.clrtexts = self.def_clrtexts

        #Housesystem
        self.hsys = self.def_hsys

        #Nodes
        self.meannode = self.def_meannode

        #Orbis
        self.orbis = copy.deepcopy(self.def_orbis)
        self.orbisplanetspar = copy.deepcopy(self.def_orbisplanetspar)

        # Houses
        self.orbisH = self.def_orbisH[:]
        self.orbisparH = self.def_orbisparH[:]

        self.orbiscuspH = self.def_orbiscuspH

        # Asc,MC
        self.orbisAscMC = self.def_orbisAscMC[:]
        self.orbisparAscMC = self.def_orbisparAscMC[:]

        self.orbiscuspAscMC = self.def_orbiscuspAscMC

        self.exact = self.def_exact

        #Primary Dir
        self.primarydir = self.def_primarydir
        self.subprimarydir = self.def_subprimarydir
        self.subzodiacal = self.def_subzodiacal
        self.bianchini = self.def_bianchini

        self.sigascmc = self.def_sigascmc[:]

        self.sighouses = self.def_sighouses

        self.sigplanets = self.def_sigplanets[:]
        self.promplanets = self.def_promplanets[:]

        self.pdaspects = self.def_pdaspects[:]

        self.pdmidpoints = self.def_pdmidpoints

        self.pdparallels = self.def_pdparallels[:]

        self.pdsecmotion = self.def_pdsecmotion
        self.pdsecmotioniter = self.def_pdsecmotioniter

        self.zodpromsigasps = self.def_zodpromsigasps[:]
        self.ascmchcsasproms = self.def_ascmchcsasproms

        self.pdfixstars = self.def_pdfixstars

        del self.pdfixstarssel[:]
        self.pdfixstarssel = self.def_pdfixstarssel[:]

        self.pdlof = self.def_pdlof[:]

        self.pdsyzygy = self.def_pdsyzygy

        self.pdterms = self.def_pdterms

        self.pdantiscia = self.def_pdantiscia

        self.pdcustomer = self.def_pdcustomer
        self.pdcustomerlon = self.def_pdcustomerlon
        self.pdcustomerlat = self.def_pdcustomerlat
        self.pdcustomersouthern = self.def_pdcustomersouthern

        self.pdcustomer2 = self.def_pdcustomer2
        self.pdcustomer2lon = self.def_pdcustomer2lon
        self.pdcustomer2lat = self.def_pdcustomer2lat
        self.pdcustomer2southern = self.def_pdcustomer2southern

        #PD-Keys
        self.pdkeydyn = self.def_pdkeydyn
        self.pdkeyd = self.def_pdkeyd
        self.pdkeys = self.def_pdkeys
        self.pdkeydeg = self.def_pdkeydeg
        self.pdkeymin = self.def_pdkeymin
        self.pdkeysec = self.def_pdkeysec

        self.useregressive = self.def_useregressive

        #Fortune
        self.lotoffortune = self.def_lotoffortune

        #Syzygy
        self.syzmoon = self.def_syzmoon

        #Fixstars
        self.fixstars.clear()
        self.fixstars = self.def_fixstars.copy()

        #Profections
        self.zodprof = self.def_zodprof
        self.usezodprojsprof = self.def_usezodprojsprof

# ########################################
# Roberto change - V 7.3.0
        #Firdaria
        self.isfirbonatti = self.def_isfirbonatti
# ########################################

# ########################################
# Roberto change - V 7.2.0
        #Default Location
        self.deflocname = self.def_deflocname
        self.deflocplus = self.def_deflocplus
        self.defloczhour = self.def_defloczhour
        self.defloczminute = self.def_defloczminute
        self.deflocdst = self.def_deflocdst
        self.defloclondeg = self.def_defloclondeg
        self.defloclonmin = self.def_defloclonmin
        self.defloclatdeg = self.def_defloclatdeg
        self.defloclatmin = self.def_defloclatmin
        self.defloceast = self.def_defloceast
        self.deflocnorth = self.def_deflocnorth
        self.deflocalt = self.def_deflocalt
# ########################################

        #PDsInChart
        self.pdincharttyp = self.def_pdincharttyp
        self.pdinchartsecmotion = self.def_pdinchartsecmotion

        self.pdinchartterrsecmotion = self.def_pdinchartterrsecmotion

        #Languages
        self.langid = self.def_langid

        #Autosave
        self.autosave = self.def_autosave


    def load(self):
        res = True

        try:
            optfile = self.appearance1opt
            f = open(optfile, 'rb')
            self.aspects = pickle.load(f)
            self.aspect = pickle.load(f)
            self.symbols = pickle.load(f)
            self.traditionalaspects = pickle.load(f)
            self.houses = pickle.load(f)
            self.positions = pickle.load(f)
            self.intables = pickle.load(f)
            self.bw = pickle.load(f)
            self.theme = pickle.load(f)
            self.ascmcsize = pickle.load(f)
            self.tablesize = pickle.load(f)
            self.planetarydayhour = pickle.load(f)
            self.housesystem = pickle.load(f)
            self.transcendental = pickle.load(f)
            self.shownodes = pickle.load(f)
            self.aspectstonodes = pickle.load(f)
            self.showlof = pickle.load(f)
            self.showaspectstolof = pickle.load(f)
            self.showterms = pickle.load(f)
            self.showdecans = pickle.load(f)
            self.showfixstars = pickle.load(f)
            self.showfixstarsnodes = pickle.load(f)
            self.showfixstarshcs = pickle.load(f)
            self.showfixstarslof = pickle.load(f)
            self.topocentric = pickle.load(f)
            self.usetradfixstarnamespdlist = pickle.load(f)
            self.netbook = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.appearance2opt
            f = open(optfile, 'rb')
            self.speculums = pickle.load(f)
            self.intime = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.symbolsopt
            f = open(optfile, 'rb')
            self.uranus = pickle.load(f)
            self.pluto = pickle.load(f)
            self.signs = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.dignitiesopt
            f = open(optfile, 'rb')
            self.dignities = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.triplicitiesopt
            f = open(optfile, 'rb')
            self.seltrip = pickle.load(f)
            self.trips = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.termsopt
            f = open(optfile, 'rb')
            self.selterm = pickle.load(f)
            self.terms = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.decansopt
            f = open(optfile, 'rb')
            self.seldecan = pickle.load(f)
            self.decans = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.chartalmutenopt
            f = open(optfile, 'rb')
            self.oneruler = pickle.load(f)
            self.usedaynightorb = pickle.load(f)
            self.dignityscores = pickle.load(f)
            self.useaccidental = pickle.load(f)
            self.housescores = pickle.load(f)
            self.sunphases = pickle.load(f)
            self.dayhourscores = pickle.load(f)
            self.useexaltationmercury = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.topicalandpartsopt
            f = open(optfile, 'rb')
            self.topicals = pickle.load(f)
            self.arabicparts = pickle.load(f)
            self.arabicpartsref = pickle.load(f)
            self.daynightorbdeg = pickle.load(f)
            self.daynightorbmin = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.ayanamsaopt
            f = open(optfile, 'rb')
            self.ayanamsha = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.colorsopt
            f = open(optfile, 'rb')
            self.clrframe = pickle.load(f)
            self.clrsigns = pickle.load(f)
            self.clrAscMC = pickle.load(f)
            self.clrhouses = pickle.load(f)
            self.clrhousenumbers = pickle.load(f)
            self.clrpositions = pickle.load(f)
            self.clrperegrin = pickle.load(f)
            self.clrdomicil = pickle.load(f)
            self.clrexil = pickle.load(f)
            self.clrexal = pickle.load(f)
            self.clrcasus = pickle.load(f)
            self.clraspect = pickle.load(f)
            self.clrindividual = pickle.load(f)
            self.useplanetcolors = pickle.load(f)
            self.clrbackground = pickle.load(f)
            self.clrtable = pickle.load(f)
            self.clrtexts = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.housesystemopt
            f = open(optfile, 'rb')
            self.hsys = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.nodesopt
            f = open(optfile, 'rb')
            self.meannode = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.orbsopt
            f = open(optfile, 'rb')
            self.orbis = pickle.load(f)
            self.orbisplanetspar = pickle.load(f)
            self.orbisH = pickle.load(f)
            self.orbiscuspH = pickle.load(f)
            self.orbisparH = pickle.load(f)
            self.orbisAscMC = pickle.load(f)
            self.orbisparAscMC = pickle.load(f)
            self.orbiscuspAscMC = pickle.load(f)
            self.exact = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.primarydirsopt
            f = open(optfile, 'rb')
            self.primarydir = pickle.load(f)
            self.subprimarydir = pickle.load(f)
            self.subzodiacal = pickle.load(f)
            self.bianchini = pickle.load(f)
            self.zodpromsigasps = pickle.load(f)
            self.ascmchcsasproms = pickle.load(f)
            self.pdfixstars = pickle.load(f)
            self.pdfixstarssel = pickle.load(f)
            self.pdlof = pickle.load(f)
            self.pdsyzygy = pickle.load(f)
            self.pdterms = pickle.load(f)
            self.pdantiscia = pickle.load(f)
            self.pdcustomer = pickle.load(f)
            self.pdcustomerlon = pickle.load(f)
            self.pdcustomerlat = pickle.load(f)
            self.pdcustomersouthern = pickle.load(f)
            self.pdcustomer2 = pickle.load(f)
            self.pdcustomer2lon = pickle.load(f)
            self.pdcustomer2lat = pickle.load(f)
            self.pdcustomer2southern = pickle.load(f)
            self.sigascmc = pickle.load(f)
            self.sighouses = pickle.load(f)
            self.sigplanets = pickle.load(f)
            self.promplanets = pickle.load(f)
            self.pdaspects = pickle.load(f)
            self.pdmidpoints = pickle.load(f)
            self.pdparallels = pickle.load(f)
            self.pdsecmotion = pickle.load(f)
            self.pdsecmotioniter = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.primarykeysopt
            f = open(optfile, 'rb')
            self.pdkeydyn = pickle.load(f)
            self.pdkeyd = pickle.load(f)
            self.pdkeys = pickle.load(f)
            self.pdkeydeg = pickle.load(f)
            self.pdkeymin = pickle.load(f)
            self.pdkeysec = pickle.load(f)
            self.useregressive = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.fortuneopt
            f = open(optfile, 'rb')
            self.lotoffortune = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.syzygyopt
            f = open(optfile, 'rb')
            self.syzmoon = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.fixstarsopt
            f = open(optfile, 'rb')
            self.fixstars = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.profectionsopt
            f = open(optfile, 'rb')
            self.zodprof = pickle.load(f)
            self.usezodprojsprof = pickle.load(f)
            f.close()
        except IOError:
            res = False

# ########################################
# Roberto change - V 7.3.0
        try:
            optfile = self.firdariaopt
            f = open(optfile, 'rb')
            self.isfirbonatti = pickle.load(f)
            f.close()
        except IOError:
            res = False
# ########################################

# ########################################
# Roberto change - V 7.2.0
        try:
            optfile = self.deflocationopt
            f = open(optfile, 'rb')
            self.deflocname = pickle.load(f)
            self.deflocplus = pickle.load(f)
            self.defloczhour = pickle.load(f)
            self.defloczminute = pickle.load(f)
            self.deflocdst = pickle.load(f)
            self.defloclondeg = pickle.load(f)
            self.defloclonmin = pickle.load(f)
            self.defloclatdeg = pickle.load(f)
            self.defloclatmin = pickle.load(f)
            self.defloceast = pickle.load(f)
            self.deflocnorth = pickle.load(f)
            self.deflocalt = pickle.load(f)
            f.close()
        except IOError:
            res = False
# ########################################

        try:
            optfile = self.pdsinchartopt
            f = open(optfile, 'rb')
            self.pdincharttyp = pickle.load(f)
            self.pdinchartsecmotion = pickle.load(f)
            self.pdinchartterrsecmotion = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.languagesopt
            f = open(optfile, 'rb')
            self.langid = pickle.load(f)
            f.close()
        except IOError:
            res = False

        try:
            optfile = self.autosaveopt
            f = open(optfile, 'rb')
            self.autosave = pickle.load(f)
            f.close()
        except IOError:
            res = False

        return res


    def saveAppearance1(self):
        try:
            optfile = self.appearance1opt
            f = open(optfile, 'wb')
            pickle.dump(self.aspects, f)
            pickle.dump(self.aspect, f)
            pickle.dump(self.symbols, f)
            pickle.dump(self.traditionalaspects, f)
            pickle.dump(self.houses, f)
            pickle.dump(self.positions, f)
            pickle.dump(self.intables, f)
            pickle.dump(self.bw, f)
            pickle.dump(self.theme, f)
            pickle.dump(self.ascmcsize, f)
            pickle.dump(self.tablesize, f)
            pickle.dump(self.planetarydayhour, f)
            pickle.dump(self.housesystem, f)
            pickle.dump(self.transcendental, f)
            pickle.dump(self.shownodes, f)
            pickle.dump(self.aspectstonodes, f)
            pickle.dump(self.showlof, f)
            pickle.dump(self.showaspectstolof, f)
            pickle.dump(self.showterms, f)
            pickle.dump(self.showdecans, f)
            pickle.dump(self.showfixstars, f)
            pickle.dump(self.showfixstarsnodes, f)
            pickle.dump(self.showfixstarshcs, f)
            pickle.dump(self.showfixstarslof, f)
            pickle.dump(self.topocentric, f)
            pickle.dump(self.usetradfixstarnamespdlist, f)
            pickle.dump(self.netbook, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txts['OptFileError'] + ' ('+optfile+')', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False


    def saveAppearance2(self):
        try:
            optfile = self.appearance2opt
            f = open(optfile, 'wb')
            pickle.dump(self.speculums, f)
            pickle.dump(self.intime, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txts['OptFileError']+' ('+optfile+')', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False


    def saveSymbols(self):
        try:
            optfile = self.symbolsopt
            f = open(optfile, 'wb')
            pickle.dump(self.uranus, f)
            pickle.dump(self.pluto, f)
            pickle.dump(self.signs, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txts['OptFileError']+' ('+optfile+')', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False


    def saveDignities(self):
        try:
            optfile = self.dignitiesopt
            f = open(optfile, 'wb')
            pickle.dump(self.dignities, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txts['OptFileError']+' ('+optfile+')', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False


    def saveTriplicities(self):
        try:
            optfile = self.triplicitiesopt
            f = open(optfile, 'wb')
            pickle.dump(self.seltrip, f)
            pickle.dump(self.trips, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txts['OptFileError']+' ('+optfile+')', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False


    def saveTerms(self):
        try:
            optfile = self.termsopt
            f = open(optfile, 'wb')
            pickle.dump(self.selterm, f)
            pickle.dump(self.terms, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txts['OptFileError']+' ('+optfile+')', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False


    def saveDecans(self):
        try:
            optfile = self.decansopt
            f = open(optfile, 'wb')
            pickle.dump(self.seldecan, f)
            pickle.dump(self.decans, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txts['OptFileError']+' ('+optfile+')', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False


    def saveChartAlmuten(self):
        try:
            optfile = self.chartalmutenopt
            f = open(optfile, 'wb')
            pickle.dump(self.oneruler, f)
            pickle.dump(self.usedaynightorb, f)
            pickle.dump(self.dignityscores, f)
            pickle.dump(self.useaccidental, f)
            pickle.dump(self.housescores, f)
            pickle.dump(self.sunphases, f)
            pickle.dump(self.dayhourscores, f)
            pickle.dump(self.useexaltationmercury, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txts['OptFileError']+' ('+optfile+')', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False


    def saveTopicalandParts(self):
        try:
            optfile = self.topicalandpartsopt
            f = open(optfile, 'wb')
            pickle.dump(self.topicals, f)
            pickle.dump(self.arabicparts, f)
            pickle.dump(self.arabicpartsref, f)
            pickle.dump(self.daynightorbdeg, f)
            pickle.dump(self.daynightorbmin, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txts['OptFileError']+' ('+optfile+')', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False


    def saveAyanamsa(self):
        try:
            optfile = self.ayanamsaopt
            f = open(optfile, 'wb')
            pickle.dump(self.ayanamsha, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txts['OptFileError']+' ('+optfile+')', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False


    def saveColors(self):
        try:
            optfile = self.colorsopt
            f = open(optfile, 'wb')
            pickle.dump(self.clrframe, f)
            pickle.dump(self.clrsigns, f)
            pickle.dump(self.clrAscMC, f)
            pickle.dump(self.clrhouses, f)
            pickle.dump(self.clrhousenumbers, f)
            pickle.dump(self.clrpositions, f)
            pickle.dump(self.clrperegrin, f)
            pickle.dump(self.clrdomicil, f)
            pickle.dump(self.clrexil, f)
            pickle.dump(self.clrexal, f)
            pickle.dump(self.clrcasus, f)
            pickle.dump(self.clraspect, f)
            pickle.dump(self.clrindividual, f)
            pickle.dump(self.useplanetcolors, f)
            pickle.dump(self.clrbackground, f)
            pickle.dump(self.clrtable, f)
            pickle.dump(self.clrtexts, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txts['OptFileError']+' ('+optfile+')', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False


    def saveHouseSystem(self):
        try:
            optfile = self.housesystemopt
            f = open(optfile, 'wb')
            pickle.dump(self.hsys, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txts['OptFileError']+' ('+optfile+')', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False


    def saveNodes(self):
        try:
            optfile = self.nodesopt
            f = open(optfile, 'wb')
            pickle.dump(self.meannode, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txts['OptFileError']+' ('+optfile+')', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False


    def saveOrbs(self):
        try:
            optfile = self.orbsopt
            f = open(optfile, 'wb')
            pickle.dump(self.orbis, f)
            pickle.dump(self.orbisplanetspar, f)
            pickle.dump(self.orbisH, f)
            pickle.dump(self.orbiscuspH, f)
            pickle.dump(self.orbisparH, f)
            pickle.dump(self.orbisAscMC, f)
            pickle.dump(self.orbisparAscMC, f)
            pickle.dump(self.orbiscuspAscMC, f)
            pickle.dump(self.exact, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txts['OptFileError']+' ('+optfile+')', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False


    def savePrimaryDirs(self):
        try:
            optfile = self.primarydirsopt
            f = open(optfile, 'wb')
            pickle.dump(self.primarydir, f)
            pickle.dump(self.subprimarydir, f)
            pickle.dump(self.subzodiacal, f)
            pickle.dump(self.bianchini, f)
            pickle.dump(self.zodpromsigasps, f)
            pickle.dump(self.ascmchcsasproms, f)
            pickle.dump(self.pdfixstars, f)
            pickle.dump(self.pdfixstarssel, f)
            pickle.dump(self.pdlof, f)
            pickle.dump(self.pdsyzygy, f)
            pickle.dump(self.pdterms, f)
            pickle.dump(self.pdantiscia, f)
            pickle.dump(self.pdcustomer, f)
            pickle.dump(self.pdcustomerlon, f)
            pickle.dump(self.pdcustomerlat, f)
            pickle.dump(self.pdcustomersouthern, f)
            pickle.dump(self.pdcustomer2, f)
            pickle.dump(self.pdcustomer2lon, f)
            pickle.dump(self.pdcustomer2lat, f)
            pickle.dump(self.pdcustomer2southern, f)
            pickle.dump(self.sigascmc, f)
            pickle.dump(self.sighouses, f)
            pickle.dump(self.sigplanets, f)
            pickle.dump(self.promplanets, f)
            pickle.dump(self.pdaspects, f)
            pickle.dump(self.pdmidpoints, f)
            pickle.dump(self.pdparallels, f)
            pickle.dump(self.pdsecmotion, f)
            pickle.dump(self.pdsecmotioniter, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txts['OptFileError']+' ('+optfile+')', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False


    def savePrimaryKeys(self):
        try:
            optfile = self.primarykeysopt
            f = open(optfile, 'wb')
            pickle.dump(self.pdkeydyn, f)
            pickle.dump(self.pdkeyd, f)
            pickle.dump(self.pdkeys, f)
            pickle.dump(self.pdkeydeg, f)
            pickle.dump(self.pdkeymin, f)
            pickle.dump(self.pdkeysec, f)
            pickle.dump(self.useregressive, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txts['OptFileError']+' ('+optfile+')', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False


    def saveFortune(self):
        try:
            optfile = self.fortuneopt
            f = open(optfile, 'wb')
            pickle.dump(self.lotoffortune, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txts['OptFileError']+' ('+optfile+')', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False


    def saveSyzygy(self):
        try:
            optfile = self.syzygyopt
            f = open(optfile, 'wb')
            pickle.dump(self.syzmoon, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txts['OptFileError']+' ('+optfile+')', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

# ###########################################
# Elias -  V 8.0.0 fixstarsorbdlg change fs=[]
# ###########################################
    def saveFixstars(self,fs=[]):
        try:
            optfile = self.fixstarsopt
            f = open(optfile, 'wb')
            if fs != []:
                self.fixstars = fs
# ###########################################
            pickle.dump(self.fixstars, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txts['OptFileError']+' ('+optfile+')', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False


    def saveProfections(self):
        try:
            optfile = self.profectionsopt
            f = open(optfile, 'wb')
            pickle.dump(self.zodprof, f)
            pickle.dump(self.usezodprojsprof, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txts['OptFileError']+' ('+optfile+')', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

# ########################################
# Roberto change - V 7.3.0
    def saveFirdaria(self):
        try:
            optfile = self.firdariaopt
            f = open(optfile, 'wb')
            pickle.dump(self.isfirbonatti, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txtsfiles['OptFileError']+' ('+optfile+')', mtexts.txtsfiles['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False
# ########################################

# ########################################
# Roberto change - V 7.2.0
    def saveDefLocation(self):
        try:
            optfile = self.deflocationopt
            f = open(optfile, 'wb')
            pickle.dump(self.deflocname, f)
            pickle.dump(self.deflocplus, f)
            pickle.dump(self.defloczhour, f)
            pickle.dump(self.defloczminute, f)
            pickle.dump(self.deflocdst, f)
            pickle.dump(self.defloclondeg, f)
            pickle.dump(self.defloclonmin, f)
            pickle.dump(self.defloclatdeg, f)
            pickle.dump(self.defloclatmin, f)
            pickle.dump(self.defloceast, f)
            pickle.dump(self.deflocnorth, f)
            pickle.dump(self.deflocalt, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txts['OptFileError']+' ('+optfile+')', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False
# ########################################


    def savePDsInChart(self):
        try:
            optfile = self.pdsinchartopt
            f = open(optfile, 'wb')
            pickle.dump(self.pdincharttyp, f)
            pickle.dump(self.pdinchartsecmotion, f)
            pickle.dump(self.pdinchartterrsecmotion, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txts['OptFileError']+' ('+optfile+')', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False


    def saveLanguages(self):
        try:
            optfile = self.languagesopt
            f = open(optfile, 'wb')
            pickle.dump(self.langid, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txts['OptFileError']+' ('+optfile+')', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False


    def saveAutoSave(self):
        try:
            optfile = self.autosaveopt
            f = open(optfile, 'wb')
            pickle.dump(self.autosave, f)
            f.close()
            return True
        except IOError:
            dlg = wx.MessageDialog(None, mtexts.txts['OptFileError']+' ('+optfile+')', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            return False

        return res


    def save(self):
        self.saveAppearance1()
        self.saveAppearance2()
        self.saveSymbols()
        self.saveDignities()
        self.saveTriplicities()
        self.saveTerms()
        self.saveDecans()
        self.saveChartAlmuten()
        self.saveTopicalandParts()
        self.saveAyanamsa()
        self.saveColors()
        self.saveHouseSystem()
        self.saveNodes()
        self.saveOrbs()
        self.savePrimaryDirs()
        self.savePrimaryKeys()
        self.saveFortune()
        self.saveSyzygy()
        self.saveFixstars()
        self.saveProfections()
# ########################################
# Roberto change - V 7.2.0
        self.saveDefLocation()
# ########################################
        self.savePDsInChart()
        self.saveLanguages()
        self.saveAutoSave()
        return True


    def clearPDFSSel(self):
        del self.pdfixstarssel[:]
        for i in range(len(self.fixstars)):
            self.pdfixstarssel.append(False)


    def checkOptsFiles(self):
        numfiles = len(self.optionsfilestxt)
        for i in range(numfiles):
            if os.path.exists(os.path.join(self.optsdirtxt, self.optionsfilestxt[i])):
                return True

        return False


    def removeOptsFiles(self):
        numfiles = len(self.optionsfilestxt)
        for i in range(numfiles):
            f = os.path.join(self.optsdirtxt, self.optionsfilestxt[i])
            if os.path.exists(f):
                os.remove(f)
