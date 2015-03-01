## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import string
import CvUtil
import ScreenInput
import CvScreenEnums
import CvPediaScreen		# base class
import CvPediaTech
import CvPediaUnit
import CvPediaBuilding
import CvPediaPromotion
import CvPediaUnitChart
import CvPediaBonus
import CvPediaTerrain
import CvPediaFeature
import CvPediaImprovement
import CvPediaCivic
import CvPediaCivilization
import CvPediaLeader
import CvPediaSpecialist
import CvPediaHistory
import CvPediaProject
import CvPediaReligion
import CvPediaSpell
import CvPediaCorporation
##--------	BUGFfH: Added by Denev 2009/09/19
import CvPediaTrait
##--------	BUGFfH: End Add

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvPediaMain( CvPediaScreen.CvPediaScreen ):
	"Civilopedia Main Screen"

	def __init__(self):

		self.PEDIA_MAIN_SCREEN_NAME = "PediaMainScreen"
		self.INTERFACE_ART_INFO = "SCREEN_BG_OPAQUE"

		self.WIDGET_ID = "PediaMainWidget"
		self.EXIT_ID = "PediaMainExitWidget"
		self.BACKGROUND_ID = "PediaMainBackground"
		self.TOP_PANEL_ID = "PediaMainTopPanel"
		self.BOTTOM_PANEL_ID = "PediaMainBottomPanel"
		self.BACK_ID = "PediaMainBack"
		self.NEXT_ID = "PediaMainForward"
		self.TOP_ID = "PediaMainTop"
		self.LIST_ID = "PediaMainList"

		self.X_SCREEN = 500
		self.Y_SCREEN = 396
		self.W_SCREEN = 1024
		self.H_SCREEN = 768
##--------	BUGFfH: Modified by Denev 2009/09/23
		"""
		self.Y_TITLE = 8
		self.DY_TEXT = 45

		self.X_EXIT = 994
		self.Y_EXIT = 730

		self.X_BACK = 50
		self.Y_BACK = 730

		self.X_FORWARD = 200
		self.Y_FORWARD = 730

		self.X_MENU = 450
		self.Y_MENU = 730

		self.BUTTON_SIZE = 64
		self.BUTTON_COLUMNS = 9

		self.X_ITEMS_PANE = 30
		self.Y_ITEMS_PANE = 80
		self.H_ITEMS_PANE = 610
		self.W_ITEMS_PANE = 740
		self.ITEMS_MARGIN = 18
		self.ITEMS_SEPARATION = 2

		self.X_LINKS = 797
		self.Y_LINKS = 51
		self.H_LINKS = 665
		self.W_LINKS = 225
		"""
		self.H_PANEL = 50
		self.TITLE_FONT_SIZE = 22

		LINKS_MERGIN = 2
		self.W_LINKS = 225
		self.H_LINKS = self.H_SCREEN - (self.H_PANEL + LINKS_MERGIN) * 2
		self.X_LINKS = self.W_SCREEN - self.W_LINKS - LINKS_MERGIN
		self.Y_LINKS = self.H_PANEL + LINKS_MERGIN

		ITEMS_MERGIN = 18
		self.X_ITEMS_PANE = ITEMS_MERGIN
		self.Y_ITEMS_PANE = ITEMS_MERGIN + self.H_PANEL
		self.H_ITEMS_PANE = self.H_SCREEN - (ITEMS_MERGIN + self.H_PANEL) * 2
		self.W_ITEMS_PANE = self.X_LINKS - self.X_ITEMS_PANE - ITEMS_MERGIN

		self.Y_TITLE = (self.H_PANEL - self.TITLE_FONT_SIZE) // 2

		self.X_EXIT = 994
		self.Y_EXIT = self.H_SCREEN - self.H_PANEL + self.TITLE_FONT_SIZE // 2

		self.X_BACK = 50
		self.Y_BACK = self.Y_EXIT

		self.X_FORWARD = 200
		self.Y_FORWARD = self.Y_EXIT

		self.X_MENU = 450
		self.Y_MENU = self.Y_EXIT
##--------	BUGFfH: End Add

##--------	BUGFfH: Added by Denev 2009/09/18
		self.X_PEDIA_PAGE = 20
		self.Y_PEDIA_PAGE = self.H_PANEL + 16
		self.R_PEDIA_PAGE = self.X_LINKS - 16
		self.B_PEDIA_PAGE = self.Y_LINKS + self.H_LINKS - 16
		self.W_PEDIA_PAGE = self.R_PEDIA_PAGE - self.X_PEDIA_PAGE
		self.H_PEDIA_PAGE = self.B_PEDIA_PAGE - self.Y_PEDIA_PAGE

		self.X_MERGIN = 16
		self.Y_MERGIN = 5
##--------	BUGFfH: End Add

		self.nWidgetCount = 0

		# screen instances
		self.pediaTechScreen = CvPediaTech.CvPediaTech(self)
		self.pediaUnitScreen = CvPediaUnit.CvPediaUnit(self)
		self.pediaBuildingScreen = CvPediaBuilding.CvPediaBuilding(self)
		self.pediaPromotionScreen = CvPediaPromotion.CvPediaPromotion(self)
		self.pediaSpellScreen = CvPediaSpell.CvPediaSpell(self)
		self.pediaUnitChartScreen = CvPediaUnitChart.CvPediaUnitChart(self)
		self.pediaBonusScreen = CvPediaBonus.CvPediaBonus(self)
		self.pediaTerrainScreen = CvPediaTerrain.CvPediaTerrain(self)
		self.pediaFeatureScreen = CvPediaFeature.CvPediaFeature(self)
		self.pediaImprovementScreen = CvPediaImprovement.CvPediaImprovement(self)
		self.pediaCivicScreen = CvPediaCivic.CvPediaCivic(self)
		self.pediaCivilizationScreen = CvPediaCivilization.CvPediaCivilization(self)
		self.pediaLeaderScreen = CvPediaLeader.CvPediaLeader(self)
##--------	BUGFfH: Added by Denev 2009/09/18
		self.pediaTraitScreen = CvPediaTrait.CvPediaTrait(self)
##--------	BUGFfH: End Add
		self.pediaSpecialistScreen = CvPediaSpecialist.CvPediaSpecialist(self)
		self.pediaProjectScreen = CvPediaProject.CvPediaProject(self)
		self.pediaReligionScreen = CvPediaReligion.CvPediaReligion(self)
		self.pediaCorporationScreen = CvPediaCorporation.CvPediaCorporation(self)
		self.pediaHistoricalScreen = CvPediaHistory.CvPediaHistory(self)

		# used for navigating "forward" and "back" in civilopedia
		self.pediaHistory = []
		self.pediaFuture = []

		self.listCategories = []

		self.iCategory = -1
		self.iLastScreen = -1
		self.iActivePlayer = -1
##--------	BUGFfH: Added by Denev 2009/09/25
		self.iActiveCiv = -1
##--------	BUGFfH: End Add

		self.mapCategories = { 
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_TECH			: self.placeTechs, 
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT			: self.placeUnits, 
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_HERO			: self.placeHeros, 
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_BUILDING		: self.placeBuildings, 
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_WONDER		: self.placeWonders, 
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_TERRAIN		: self.placeTerrains,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_FEATURE		: self.placeFeatures,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIQUE_FEATURE	: self.placeUniqueFeatures,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_BONUS			: self.placeBoni, 
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_IMPROVEMENT	: self.placeImprovements,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPECIALIST	: self.placeSpecialists,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_EFFECT		: self.placeEffects,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_EQUIPMENT		: self.placeEquipments,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_RACE			: self.placeRaces,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROMOTION		: self.placePromotions,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPELL			: self.placeSpells,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT_GROUP	: self.placeUnitGroups,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIV			: self.placeCivs,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_LEADER		: self.placeLeaders,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_RELIGION		: self.placeReligions,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_CORPORATION	: self.placeCorporations,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIVIC			: self.placeCivics,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROJECT		: self.placeProjects,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT		: self.placeConcepts,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT_NEW	: self.placeNewConcepts,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_HINTS			: self.placeHints,
##--------	BUGFfH: Added by Denev 2009/09/19
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_ABILITY		: self.placeAbilities,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_TRAIT			: self.placeTraits,
##--------	BUGFfH: End Add
			}

	def getScreen(self):
		return CyGInterfaceScreen(self.PEDIA_MAIN_SCREEN_NAME, CvScreenEnums.PEDIA_MAIN)

	def setPediaCommonWidgets(self):
		self.EXIT_TEXT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>"
		self.BACK_TEXT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_BACK", ()).upper() + "</font>"
		self.FORWARD_TEXT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_FORWARD", ()).upper() + "</font>"
		self.MENU_TEXT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_TOP", ()).upper() + "</font>"

		self.szCategoryTech = localText.getText("TXT_KEY_PEDIA_CATEGORY_TECH", ())
		self.szCategoryUnit = localText.getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ())
#FfH: Added by Chalid Heros 06/03/2006##
		self.szCategoryHero = localText.getText("TXT_KEY_PEDIA_CATEGORY_HERO", ())
#FfH: End Add##
		self.szCategoryBuilding = localText.getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ())
		self.szCategoryWonder = localText.getText("TXT_KEY_CONCEPT_WONDERS", ())
		self.szCategoryBonus = localText.getText("TXT_KEY_PEDIA_CATEGORY_BONUS", ())
		self.szCategoryTerrain = localText.getText("TXT_KEY_PEDIA_CATEGORY_TERRAIN", ())
		self.szCategoryFeature = localText.getText("TXT_KEY_PEDIA_CATEGORY_FEATURE", ())
		self.szCategoryUniqueFeature = localText.getText("TXT_KEY_PEDIA_CATEGORY_UNIQUE_FEATURE", ())
		self.szCategoryImprovement = localText.getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ())
		self.szCategorySpecialist = localText.getText("TXT_KEY_PEDIA_CATEGORY_SPECIALIST", ())
		self.szCategoryEffect = localText.getText("TXT_KEY_PEDIA_CATEGORY_EFFECTS", ())
##--------	BUGFfH: Modified by Denev 2009/09/20
#		self.szCategoryEquipment = localText.getText("TXT_KEY_PEDIA_CATEGORY_ITEMS", ())
		self.szCategoryEquipment = localText.getText("TXT_KEY_PEDIA_CATEGORY_EQUIPMENTS", ())
##--------	BUGFfH: End Modify
		self.szCategoryRace = localText.getText("TXT_KEY_PEDIA_CATEGORY_RACES", ())
		self.szCategoryPromotion = localText.getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION", ())
##--------	BUGFfH: Modified by Denev 2009/09/20
#		self.szCategorySpell = localText.getText("TXT_KEY_PEDIA_CATEGORY_SPELL", ())
		self.szCategorySpell = localText.getText("TXT_KEY_PEDIA_CATEGORY_SPELLS", ())
##--------	BUGFfH: End Modify
		self.szCategoryUnitCombat = localText.getText("TXT_KEY_PEDIA_CATEGORY_UNIT_COMBAT", ())
		self.szCategoryCiv = localText.getText("TXT_KEY_PEDIA_CATEGORY_CIV", ())
		self.szCategoryLeader = localText.getText("TXT_KEY_PEDIA_CATEGORY_LEADER", ())
		self.szCategoryReligion = localText.getText("TXT_KEY_PEDIA_CATEGORY_RELIGION", ())
		self.szCategoryCorporation = localText.getText("TXT_KEY_CONCEPT_CORPORATIONS", ())
		self.szCategoryCivic = localText.getText("TXT_KEY_PEDIA_CATEGORY_CIVIC", ())
		self.szCategoryProject = localText.getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ())
		self.szCategoryConcept = localText.getText("TXT_KEY_PEDIA_CATEGORY_CONCEPT", ())
		self.szCategoryConceptNew = localText.getText("TXT_KEY_PEDIA_CATEGORY_CONCEPT_NEW", ())
		self.szCategoryHints = localText.getText("TXT_KEY_PEDIA_CATEGORY_HINTS", ())
##--------	BUGFfH: Added by Denev 2009/09/19
		self.szCategoryAbility = localText.getText("TXT_KEY_PEDIA_CATEGORY_ABILITY", ())
		self.szCategoryTrait = localText.getText("TXT_KEY_PEDIA_TRAITS", ())
##--------	BUGFfH: End Add

		self.listCategories = [ self.szCategoryTech, 
								self.szCategoryUnit, 
#FfH: Added by Chalid Heros 06/03/2006##
								self.szCategoryHero, 
#FfH: End Add##
								self.szCategoryBuilding,
								self.szCategoryWonder,
								self.szCategoryTerrain, 
								self.szCategoryFeature, 
								self.szCategoryUniqueFeature, 
								self.szCategoryBonus, 
								self.szCategoryImprovement, 
								self.szCategorySpecialist, 
								self.szCategoryEffect, 
								self.szCategoryEquipment, 
								self.szCategoryRace, 
								self.szCategoryPromotion, 
								self.szCategorySpell,
##--------	BUGFfH: Added by Denev 2009/09/19
								self.szCategoryAbility,
##--------	BUGFfH: End Add
								self.szCategoryUnitCombat, 
								self.szCategoryCiv, 
								self.szCategoryLeader,
##--------	BUGFfH: Added by Denev 2009/09/19
								self.szCategoryTrait,
##--------	BUGFfH: End Add
								self.szCategoryReligion, 
##--------	BUGFfH: Deleted by Denev 2009/09/19
#								self.szCategoryCorporation, 
##--------	BUGFfH: End Delete
								self.szCategoryCivic, 
								self.szCategoryProject,  
								self.szCategoryConcept,
##--------	BUGFfH: Deleted by Denev 2009/09/19
#								self.szCategoryConceptNew,
##--------	BUGFfH: End Delete
								self.szCategoryHints]

		# Create a new screen
		screen = self.getScreen()
		screen.setRenderInterfaceOnly(True);
		screen.setScreenGroup(1)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		# Set background
		screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel(self.TOP_PANEL_ID, u"", u"", True, False, 0, 0, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel(self.BOTTOM_PANEL_ID, u"", u"", True, False, 0, 713, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)

		# Exit button
		screen.setText(self.EXIT_ID, "Background", self.EXIT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)

		# Back
		screen.setText(self.BACK_ID, "Background", self.BACK_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.X_BACK, self.Y_BACK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_BACK, 1, -1)

		# Forward
		screen.setText(self.NEXT_ID, "Background", self.FORWARD_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.X_FORWARD, self.Y_FORWARD, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_FORWARD, 1, -1)

		# List of items on the right
		screen.addListBoxGFC(self.LIST_ID, "", self.X_LINKS, self.Y_LINKS, self.W_LINKS, self.H_LINKS, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(self.LIST_ID, True)
		screen.setStyle(self.LIST_ID, "Table_StandardCiv_Style")

	# Screen construction function
	def showScreen(self, iCategory):
		self.iCategory = iCategory

		self.deleteAllWidgets()

		screen = self.getScreen()

		bNotActive = (not screen.isActive())
		if bNotActive:
			self.setPediaCommonWidgets()

		# Header...
		szHeader = u"<font=4b>" +localText.getText("TXT_KEY_WIDGET_HELP", ()).upper() + u"</font>"
		szHeaderId = self.getNextWidgetName()
		screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_DESCRIPTION, -1, -1)

		self.panelName = self.getNextWidgetName()
		screen.addPanel(self.panelName, "", "", false, false,
			self.X_ITEMS_PANE, self.Y_ITEMS_PANE, self.W_ITEMS_PANE, self.H_ITEMS_PANE, PanelStyles.PANEL_STYLE_BLUE50)

		if self.iLastScreen	!= CvScreenEnums.PEDIA_MAIN or bNotActive:
			self.placeLinks(true)
			self.iLastScreen = CvScreenEnums.PEDIA_MAIN
		else:
			self.placeLinks(false)

		if (self.mapCategories.has_key(iCategory)):
			self.mapCategories.get(iCategory)()

	def placeTechs(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()

		# Create and place a tech pane
		list = self.getSortedList( gc.getNumTechInfos(), gc.getTechInfo )

		nColumns = 4
		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iRow = iCounter % nRows
			iColumn = iCounter // nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getTechInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		"""
		nColumns = 4
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH
		lTech = self.getSortedList( gc.getNumTechInfos(), gc.getTechInfo )

		self.placeItems(lTech, gc.getTechInfo, iWidget, nColumns)
##--------	BUGFfH: End Modify

	def placeUnits(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()

		# Create and place a tech pane
#FfH: Modified by Chalid Heros 06/03/2006##
#		list = self.getSortedList( gc.getNumUnitInfos(), gc.getUnitInfo )
#		nColumns = 4
		list = self.pediaUnitScreen.getUnitSortedList(false)
		nColumns = 3
#FfH: End Modify##
#		if gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY") and gc.getGame().isFinalInitialized():
#			listCopy = list[:]
#			for item in listCopy:
#				if not gc.getGame().isUnitEverActive(item[1]):
#					list.remove(item)

		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iRow = iCounter % nRows
			iColumn = iCounter // nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			szButton = gc.getUnitInfo(item[1]).getButton()
			if self.iActivePlayer != -1:
				szButton = gc.getPlayer(self.iActivePlayer).getUnitButton(item[1])
			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", szButton, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		"""
		nColumns = 4
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT

		bHero = false
		lUnit = self.getSortedList( gc.getNumUnitInfos(), gc.getUnitInfo, bHero, self.pediaUnitScreen.getUnitType )

		self.placeItems(lUnit, gc.getUnitInfo, iWidget, nColumns)
##--------	BUGFfH: End Modify

#FfH: Added by Chalid Heros 06/03/2006##
	def placeHeros(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()

		# Create and place a tech pane
		list = self.pediaUnitScreen.getUnitSortedList(true)
		nColumns = 3
		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 25, 25, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iRow = iCounter % nRows
			iColumn = iCounter // nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getUnitInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		"""
		nColumns = 3
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT

		bHero = true
		lUnit = self.getSortedList( gc.getNumUnitInfos(), gc.getUnitInfo, bHero, self.pediaUnitScreen.getUnitType )

		self.placeItems(lUnit, gc.getUnitInfo, iWidget, nColumns)
##--------	BUGFfH: End Modify
#FfH: End Add ##

	def placeBuildings(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()

		# Create and place a tech pane
		list = self.pediaBuildingScreen.getBuildingSortedList(false)

		if gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY") and gc.getGame().isFinalInitialized():
			listCopy = list[:]
			for item in listCopy:
				if not gc.getGame().isBuildingEverActive(item[1]):
					list.remove(item)

#FfH: Modified by Kael 11/06/2007
#		nColumns = 4
		nColumns = 3
#FfH: End Modify

		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iRow = iCounter % nRows
			iColumn = iCounter // nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getBuildingInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		"""
		nColumns = 3
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING

		bWonder = false
		lBuilding = self.getSortedList( gc.getNumBuildingInfos(), gc.getBuildingInfo, bWonder, self.pediaBuildingScreen.getBuildingType )

		self.placeItems(lBuilding, gc.getBuildingInfo, iWidget, nColumns)
##--------	BUGFfH: End Modify

	def placeWonders(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()

		# Create and place a tech pane
		list = self.pediaBuildingScreen.getBuildingSortedList(true)

		nColumns = 3
		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iRow = iCounter % nRows
			iColumn = iCounter // nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getBuildingInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		"""
		nColumns = 3
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING

		bWonder = true
		lBuilding = self.getSortedList( gc.getNumBuildingInfos(), gc.getBuildingInfo, bWonder, self.pediaBuildingScreen.getBuildingType )

		self.placeItems(lBuilding, gc.getBuildingInfo, iWidget, nColumns)
##--------	BUGFfH: End Modify

	def placeBoni(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()

		# Create and place a tech pane
		list = self.getSortedList( gc.getNumBonusInfos(), gc.getBonusInfo )

		nColumns = 3
		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iRow = iCounter % nRows
			iColumn = iCounter // nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getBonusInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		"""
		nColumns = 3
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS
		lBonus = self.getSortedList( gc.getNumBonusInfos(), gc.getBonusInfo )

		self.placeItems(lBonus, gc.getBonusInfo, iWidget, nColumns)

	def placeImprovements(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()

		# Create and place a tech pane

#FfH: Modified by Kael 09/27/2007
#		list = self.getSortedList( gc.getNumImprovementInfos(), gc.getImprovementInfo )
#		nColumns = 1
		list = self.pediaImprovement.getImprovementSortedList(False)
		nColumns = 3
#FfH: End Modify

		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iRow = iCounter % nRows
			iColumn = iCounter // nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getImprovementInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		"""
		nColumns = 3
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT

		bGlobal = false
		lImprovement = self.getSortedList( gc.getNumImprovementInfos(), gc.getImprovementInfo, bGlobal, self.pediaImprovementScreen.getImprovementType )

		self.placeItems(lImprovement, gc.getImprovementInfo, iWidget, nColumns)
##--------	BUGFfH: End Modify

	def placeUniqueFeatures(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()
		list = self.pediaImprovement.getImprovementSortedList(True)
		nColumns = 3
		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iRow = iCounter % nRows
			iColumn = iCounter // nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getImprovementInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		"""
		nColumns = 3
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT

		bGlobal = true
		lImprovement = self.getSortedList( gc.getNumImprovementInfos(), gc.getImprovementInfo, bGlobal, self.pediaImprovementScreen.getImprovementType )

		self.placeItems(lImprovement, gc.getImprovementInfo, iWidget, nColumns)
##--------	BUGFfH: End Modify

	def placeEffects(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()

		# Create and place a tech pane
		list = self.pediaPromotionScreen.getPromotionSortedList(3)

		nColumns = 3
		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iRow = iCounter % nRows
			iColumn = iCounter // nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getPromotionInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		"""
		nColumns = 3
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION

		iPromotionType = CvPediaPromotion.CvPediaPromotion(self).TYPE_EFFECT
		lPromotion = self.getSortedList( gc.getNumPromotionInfos(), gc.getPromotionInfo, iPromotionType, self.pediaPromotionScreen.getPromotionType )

		self.placeItems(lPromotion, gc.getPromotionInfo, iWidget, nColumns)
##--------	BUGFfH: End Modify

	def placeEquipments(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()

		# Create and place a tech pane
		list = self.pediaPromotionScreen.getPromotionSortedList(2)

		nColumns = 3
		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iRow = iCounter % nRows
			iColumn = iCounter // nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getPromotionInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		"""
		nColumns = 3
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION

		iPromotionType = CvPediaPromotion.CvPediaPromotion(self).TYPE_EQUIPMENT
		lPromotion = self.getSortedList( gc.getNumPromotionInfos(), gc.getPromotionInfo, iPromotionType, self.pediaPromotionScreen.getPromotionType )

		self.placeItems(lPromotion, gc.getPromotionInfo, iWidget, nColumns)
##--------	BUGFfH: End Modify

	def placeRaces(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()

		# Create and place a tech pane
		list = self.pediaPromotionScreen.getPromotionSortedList(1)

		nColumns = 2
		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iRow = iCounter % nRows
			iColumn = iCounter // nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getPromotionInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		"""
		nColumns = 3
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION

		iPromotionType = CvPediaPromotion.CvPediaPromotion(self).TYPE_RACE
		lPromotion = self.getSortedList( gc.getNumPromotionInfos(), gc.getPromotionInfo, iPromotionType, self.pediaPromotionScreen.getPromotionType )

		self.placeItems(lPromotion, gc.getPromotionInfo, iWidget, nColumns)
##--------	BUGFfH: End Modify

	def placePromotions(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()

		# Create and place a tech pane
		list = self.pediaPromotionScreen.getPromotionSortedList(4)

		nColumns = 3
		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iRow = iCounter % nRows
			iColumn = iCounter // nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getPromotionInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		"""
		nColumns = 3
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION

		iPromotionType = CvPediaPromotion.CvPediaPromotion(self).TYPE_REGULAR
		lPromotion = self.getSortedList( gc.getNumPromotionInfos(), gc.getPromotionInfo, iPromotionType, self.pediaPromotionScreen.getPromotionType )

		self.placeItems(lPromotion, gc.getPromotionInfo, iWidget, nColumns)
##--------	BUGFfH: End Modify

	def placeSpells(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()

		# Create and place a tech pane
		list = self.getSortedList( gc.getNumSpellInfos(), gc.getSpellInfo )

		nColumns = 3
		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 25, 25, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iRow = iCounter % nRows
			iColumn = iCounter // nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getSpellInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPELL, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		"""
		nColumns = 3
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPELL

		bAbility = false
		lAbility = self.getSortedList( gc.getNumSpellInfos(), gc.getSpellInfo, bAbility, self.pediaSpellScreen.getSpellType )

		self.placeItems(lAbility, gc.getSpellInfo, iWidget, nColumns)
##--------	BUGFfH: End Modify

##--------	BUGFfH: Added by Denev 2009/09/19
	def placeAbilities(self):
		nColumns = 3
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPELL

		bSpellType = true
		lAbility = self.getSortedList( gc.getNumSpellInfos(), gc.getSpellInfo, bSpellType, self.pediaSpellScreen.getSpellType )

		self.placeItems(lAbility, gc.getSpellInfo, iWidget, nColumns)
##--------	BUGFfH: End Add

	def placeUnitGroups(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()

		# Create and place a tech pane
		list = self.getSortedList( gc.getNumUnitCombatInfos(), gc.getUnitCombatInfo )

		nColumns = 1
		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iRow = iCounter % nRows
			iColumn = iCounter // nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getUnitCombatInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		"""
		nColumns = 1
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT
		lUnitCombat = self.getSortedList( gc.getNumUnitCombatInfos(), gc.getUnitCombatInfo )

		self.placeItems(lUnitCombat, gc.getUnitCombatInfo, iWidget, nColumns)
##--------	BUGFfH: End Modify

	def placeCivs(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()

		# Create and place a tech pane
		list = self.getSortedList( gc.getNumCivilizationInfos(), gc.getCivilizationInfo )

		if gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY") and gc.getGame().isFinalInitialized():
			listCopy = list[:]
			for item in listCopy:
				if not gc.getGame().isCivEverActive(item[1]):
					list.remove(item)

#FfH: Added by Kael 05/28/2008
				if gc.getCivilizationInfo(item[1]).isGraphicalOnly():
					list.remove(item)
#FfH: End Add

		nColumns = 2
		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iRow = iCounter % nRows
			iColumn = iCounter // nRows
#			if (gc.getCivilizationInfo(item[1]).isPlayable()):
			if item[1] != gc.getInfoTypeForString('CIVILIZATION_BARBARIAN'):
				if iRow >= iNumRows:
					iNumRows += 1
					screen.appendTableRow(tableName)
				screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getCivilizationInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
				iCounter += 1
		"""
		nColumns = 2
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV
		lCivilization = self.getSortedList( gc.getNumCivilizationInfos(), gc.getCivilizationInfo )

		self.placeItems(lCivilization, gc.getCivilizationInfo, iWidget, nColumns)
##--------	BUGFfH: End Modify

	def placeLeaders(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()

		# Create and place a tech pane
		list = self.getSortedList( gc.getNumLeaderHeadInfos(), gc.getLeaderHeadInfo )
		listCopy = list[:]
		for item in listCopy:
			if item[1] == gc.getDefineINT("BARBARIAN_LEADER"):
				list.remove(item)

#FfH: Added by Kael 04/28/2008
			if gc.getLeaderHeadInfo(item[1]).isGraphicalOnly():
				list.remove(item)
#FfH: End Add

			elif gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY") and gc.getGame().isFinalInitialized():
				if not gc.getGame().isLeaderEverActive(item[1]):
					list.remove(item)

		nColumns = 3
		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iRow = iCounter % nRows
			iColumn = iCounter // nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)

			iNumCivs = 0
			iLeaderCiv = -1
			for iCiv in range(gc.getNumCivilizationInfos()):
				civ = gc.getCivilizationInfo(iCiv)
				if civ.isLeaders(item[1]):
					iNumCivs += 1
					iLeaderCiv = iCiv

			if iNumCivs != 1:
				iLeaderCiv = -1

			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getLeaderHeadInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, item[1], iLeaderCiv, CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		"""
		nColumns = 3
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER
		lLeaderHead = self.getSortedList( gc.getNumLeaderHeadInfos(), gc.getLeaderHeadInfo )

		self.placeItems(lLeaderHead, gc.getLeaderHeadInfo, iWidget, nColumns)
##--------	BUGFfH: End Modify

##--------	BUGFfH: Added by Denev 2009/09/19
	def placeTraits(self):
		nColumns = 2
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_TRAIT
		lTrait = self.getSortedList( gc.getNumTraitInfos(), gc.getTraitInfo )

		self.placeItems(lTrait, gc.getTraitInfo, iWidget, nColumns)
##--------	BUGFfH: End Add

	def placeReligions(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()

		# Create and place a tech pane
		list = self.getSortedList( gc.getNumReligionInfos(), gc.getReligionInfo )

		nColumns = 1
		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iRow = iCounter % nRows
			iColumn = iCounter // nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getReligionInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		"""
		nColumns = 1
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION
		lReligion = self.getSortedList( gc.getNumReligionInfos(), gc.getReligionInfo )

		self.placeItems(lReligion, gc.getReligionInfo, iWidget, nColumns)
##--------	BUGFfH: End Modify

	def placeCorporations(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()

		# Create and place a tech pane
		list = self.getSortedList( gc.getNumCorporationInfos(), gc.getCorporationInfo )

		nColumns = 1
		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iRow = iCounter % nRows
			iColumn = iCounter // nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getCorporationInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_CORPORATION, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		"""
		nColumns = 1
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_CORPORATION
		lCorporation = self.getSortedList( gc.getNumCorporationInfos(), gc.getCorporationInfo )

		self.placeItems(lCorporation, gc.getCorporationInfo, iWidget, nColumns)
##--------	BUGFfH: End Modify

	def placeCivics(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()

		# Create and place a tech pane
		list = self.getSortedList( gc.getNumCivicInfos(), gc.getCivicInfo )

#FfH: Modified by Kael 09/27/2007
#		nColumns = 1
		nColumns = 2
#FfH: End Modify

		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iRow = iCounter % nRows
			iColumn = iCounter // nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getCivicInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		"""
		nColumns = 2
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC
		lCivic = self.getSortedList( gc.getNumCivicInfos(), gc.getCivicInfo )

		self.placeItems(lCivic, gc.getCivicInfo, iWidget, nColumns)
##--------	BUGFfH: End Modify

	def placeProjects(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()

		# Create and place a tech pane
		list = self.pediaProjectScreen.getProjectSortedList()

		nColumns = 1
		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iRow = iCounter % nRows
			iColumn = iCounter // nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getProjectInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		"""
		nColumns = 1
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT
		lProject = self.getSortedList( gc.getNumProjectInfos(), gc.getProjectInfo )

		self.placeItems(lProject, gc.getProjectInfo, iWidget, nColumns)
##--------	BUGFfH: End Modify

	def placeTerrains(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()

		# Create and place a tech pane
		list = self.getSortedList( gc.getNumTerrainInfos(), gc.getTerrainInfo )

		nColumns = 1
		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iColumn = iCounter // nRows
			iRow = iCounter % nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getTerrainInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_TERRAIN, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		"""
		nColumns = 1
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_TERRAIN
		lTerrain = self.getSortedList( gc.getNumTerrainInfos(), gc.getTerrainInfo )

		self.placeItems(lTerrain, gc.getTerrainInfo, iWidget, nColumns)
##--------	BUGFfH: End Modify


	def placeFeatures(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()

		# Create and place a tech pane
		list = self.getSortedList( gc.getNumFeatureInfos(), gc.getFeatureInfo )

		nColumns = 1
		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iColumn = iCounter // nRows
			iRow = iCounter % nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getFeatureInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_FEATURE, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		"""
		nColumns = 1
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_FEATURE
		lFeature = self.getSortedList( gc.getNumFeatureInfos(), gc.getFeatureInfo )

		self.placeItems(lFeature, gc.getFeatureInfo, iWidget, nColumns)
##--------	BUGFfH: End Modify

	def placeConcepts(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()

		# Create and place a tech pane
		list = self.getSortedList( gc.getNumConceptInfos(), gc.getConceptInfo )

		nColumns = 3
		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iColumn = iCounter // nRows
			iRow = iCounter % nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getConceptInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_DESCRIPTION, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, item[1], CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		"""
		nColumns = 3
		iWidget = WidgetTypes.WIDGET_PEDIA_DESCRIPTION
		lConcept = self.getSortedList( gc.getNumConceptInfos(), gc.getConceptInfo )

		self.placeItems(lConcept, gc.getConceptInfo, iWidget, nColumns)
##--------	BUGFfH: End Modify


	def placeNewConcepts(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()

		# Create and place a tech pane
		list = self.getSortedList( gc.getNumNewConceptInfos(), gc.getNewConceptInfo )

		nColumns = 3
		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iColumn = iCounter // nRows
			iRow = iCounter % nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getNewConceptInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_DESCRIPTION, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT_NEW, item[1], CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		"""
		nColumns = 3
		iWidget = WidgetTypes.WIDGET_PEDIA_DESCRIPTION
		lNewConcept = self.getSortedList( gc.getNumNewConceptInfos(), gc.getNewConceptInfo )

		self.placeItems(lNewConcept, gc.getNewConceptInfo, iWidget, nColumns)
##--------	BUGFfH: End Modify


	def placeSpecialists(self):
##--------	BUGFfH: Modified by Denev 2009/09/19
		"""
		screen = self.getScreen()

		# Create and place a tech pane
		list = self.getSortedList( gc.getNumSpecialistInfos(), gc.getSpecialistInfo )

		nColumns = 1
		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iColumn = iCounter // nRows
			iRow = iCounter % nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getSpecialistInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPECIALIST, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		"""
		nColumns = 1
		iWidget = WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPECIALIST
		lSpecialist = self.getSortedList( gc.getNumSpecialistInfos(), gc.getSpecialistInfo )

		self.placeItems(lSpecialist, gc.getSpecialistInfo, iWidget, nColumns)
##--------	BUGFfH: End Modify

	def placeHints(self):
		screen = self.getScreen()

		self.szAreaId = self.getNextWidgetName()
		screen.addListBoxGFC( self.szAreaId, "",
							  self.X_ITEMS_PANE, self.Y_ITEMS_PANE, self.W_ITEMS_PANE, self.H_ITEMS_PANE, TableStyles.TABLE_STYLE_STANDARD )

		szHintsText = CyGameTextMgr().buildHintsList()
		hintText = string.split( szHintsText, "\n" )
		for hint in hintText:
			if len( hint ) != 0:
				screen.appendListBoxStringNoUpdate( self.szAreaId, hint, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		screen.updateListBox(self.szAreaId)

	def placeLinks(self, bRedraw):

		screen = self.getScreen()

		if bRedraw:
			screen.clearListBoxGFC(self.LIST_ID)

		i = 0
		for szCategory in self.listCategories:
			if bRedraw:
				screen.appendListBoxStringNoUpdate(self.LIST_ID, szCategory, WidgetTypes.WIDGET_PEDIA_MAIN, i, 0, CvUtil.FONT_LEFT_JUSTIFY )
			i += 1

		if bRedraw:
			screen.updateListBox(self.LIST_ID)

		screen.setSelectedListBoxStringGFC(self.LIST_ID, self.iCategory)

	# returns a unique ID for a widget in this screen
	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName

	def pediaJump(self, iScreen, iEntry, bRemoveFwdList):

		if (iEntry < 0):
			return

		self.iActivePlayer = gc.getGame().getActivePlayer()
##--------	BUGFfH: Added by Denev 2009/09/25
		self.iActiveCiv = gc.getGame().getActiveCivilizationType()
##--------	BUGFfH: End Add

		self.pediaHistory.append((iScreen, iEntry))
		if (bRemoveFwdList):
			self.pediaFuture = []

		if (iScreen == CvScreenEnums.PEDIA_MAIN):
			self.showScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_TECH):
			self.pediaTechScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_UNIT):
			self.pediaUnitScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_BUILDING):
			self.pediaBuildingScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_PROMOTION):
			self.pediaPromotionScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_SPELL):
			self.pediaSpellScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_UNIT_CHART):
			self.pediaUnitChartScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_BONUS):
			self.pediaBonusScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_TERRAIN):
			self.pediaTerrainScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_FEATURE):
			self.pediaFeatureScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_IMPROVEMENT):
			self.pediaImprovementScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_CIVIC):
			self.pediaCivicScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_CIVILIZATION):
			self.pediaCivilizationScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_LEADER):
			self.pediaLeaderScreen.interfaceScreen(iEntry)
##--------	BUGFfH: Added by Denev 2009/09/19
		elif (iScreen == CvScreenEnums.PEDIA_TRAIT):
			self.pediaTraitScreen.interfaceScreen(iEntry)
##--------	BUGFfH: End Add
		elif (iScreen == CvScreenEnums.PEDIA_SPECIALIST):
			self.pediaSpecialistScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_PROJECT):
			self.pediaProjectScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_RELIGION):
			self.pediaReligionScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_CORPORATION):
			self.pediaCorporationScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_HISTORY):
			self.pediaHistoricalScreen.interfaceScreen(iEntry)

	def back(self):
		if (len(self.pediaHistory) > 1):
			self.pediaFuture.append(self.pediaHistory.pop())
			current = self.pediaHistory.pop()
			self.pediaJump(current[0], current[1], False)
		return 1

	def forward(self):
		if (self.pediaFuture):
			current = self.pediaFuture.pop()
			self.pediaJump(current[0], current[1], False)
		return 1

	def pediaShow(self):
		if (not self.pediaHistory):
			self.pediaHistory.append((CvScreenEnums.PEDIA_MAIN, 0))

		current = self.pediaHistory.pop()

		# erase history so it doesn't grow too large during the game
		self.pediaFuture = []
		self.pediaHistory = []

		# jump to the last screen that was up
		self.pediaJump(current[0], current[1], False)

	def link(self, szLink):
		if (szLink == "PEDIA_MAIN_TECH"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_TECH), True)
		if (szLink == "PEDIA_MAIN_UNIT"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT), True)
		if (szLink == "PEDIA_MAIN_BUILDING"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_BUILDING), True)
		if (szLink == "PEDIA_MAIN_TERRAIN"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_TERRAIN), True)
		if (szLink == "PEDIA_MAIN_FEATURE"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_FEATURE), True)
		if (szLink == "PEDIA_MAIN_BONUS"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_BONUS), True)
		if (szLink == "PEDIA_MAIN_IMPROVEMENT"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_IMPROVEMENT), True)
		if (szLink == "PEDIA_MAIN_SPECIALIST"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPECIALIST), True)
		if (szLink == "PEDIA_MAIN_PROMOTION"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROMOTION), True)
		if (szLink == "PEDIA_MAIN_SPELL"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPELL), True)
		if (szLink == "PEDIA_MAIN_UNIT_GROUP"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT_GROUP), True)
		if (szLink == "PEDIA_MAIN_CIV"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIV), True)
		if (szLink == "PEDIA_MAIN_LEADER"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_LEADER), True)
##--------	BUGFfH: Added by Denev 2009/09/19
		if (szLink == "PEDIA_MAIN_TRAIT"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_TRAIT), True)
##--------	BUGFfH: End Add
		if (szLink == "PEDIA_MAIN_RELIGION"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_RELIGION), True)
		if (szLink == "PEDIA_MAIN_CORPORATION"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CORPORATION), True)
		if (szLink == "PEDIA_MAIN_CIVIC"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIVIC), True)
		if (szLink == "PEDIA_MAIN_PROJECT"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROJECT), True)
		if (szLink == "PEDIA_MAIN_CONCEPT"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT), True)
		if (szLink == "PEDIA_MAIN_CONCEPT_NEW"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT_NEW), True)
		if (szLink == "PEDIA_MAIN_HINTS"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_HINTS), True)

		for i in range(gc.getNumConceptInfos()):
			if (gc.getConceptInfo(i).isMatchForLink(szLink, False)):
				iEntryId = self.pediaHistoricalScreen.getIdFromEntryInfo(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, i)
				return self.pediaJump(CvScreenEnums.PEDIA_HISTORY, iEntryId, True)
		for i in range(gc.getNumNewConceptInfos()):
			if (gc.getNewConceptInfo(i).isMatchForLink(szLink, False)):
				iEntryId = self.pediaHistoricalScreen.getIdFromEntryInfo(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT_NEW, i)
				return self.pediaJump(CvScreenEnums.PEDIA_HISTORY, iEntryId, True)
		for i in range(gc.getNumTechInfos()):
			if (gc.getTechInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_TECH, i, True)
		for i in range(gc.getNumUnitInfos()):
			if (gc.getUnitInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_UNIT, i, True)
		for i in range(gc.getNumCorporationInfos()):
			if (gc.getCorporationInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_CORPORATION, i, True)
		for i in range(gc.getNumBuildingInfos()):
			if (gc.getBuildingInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_BUILDING, i, True)
		for i in range(gc.getNumPromotionInfos()):
			if (gc.getPromotionInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_PROMOTION, i, True)
		for i in range(gc.getNumSpellInfos()):
			if (gc.getSpellInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_SPELL, i, True)
		for i in range(gc.getNumUnitCombatInfos()):
			if (gc.getUnitCombatInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_UNIT_CHART, i, True)
		for i in range(gc.getNumBonusInfos()):
			if (gc.getBonusInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_BONUS, i, True)
		for i in range(gc.getNumTerrainInfos()):
			if (gc.getTerrainInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_TERRAIN, i, True)
		for i in range(gc.getNumFeatureInfos()):
			if (gc.getFeatureInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_FEATURE, i, True)
		for i in range(gc.getNumImprovementInfos()):
			if (gc.getImprovementInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_IMPROVEMENT, i, True)
		for i in range(gc.getNumCivicInfos()):
			if (gc.getCivicInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_CIVIC, i, True)
		for i in range(gc.getNumCivilizationInfos()):
			if (gc.getCivilizationInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_CIVILIZATION, i, True)
		for i in range(gc.getNumLeaderHeadInfos()):
			if (gc.getLeaderHeadInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_LEADER, i, True)
##--------	BUGFfH: Added by Denev 2009/09/19
		for i in range(gc.getNumTraitInfos()):
			if (gc.getTraitInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_TRAIT, i, True)
##--------	BUGFfH: End Add
		for i in range(gc.getNumSpecialistInfos()):
			if (gc.getSpecialistInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_SPECIALIST, i, True)
		for i in range(gc.getNumProjectInfos()):
			if (gc.getProjectInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_PROJECT, i, True)
		for i in range(gc.getNumReligionInfos()):
			if (gc.getReligionInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_RELIGION, i, True)

	def deleteAllWidgets(self):
		screen = self.getScreen()
		iNumWidgets = self.nWidgetCount
		self.nWidgetCount = 0
		for i in range(iNumWidgets):
			screen.deleteWidget(self.getNextWidgetName())
		self.nWidgetCount = 0



	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		# redirect to proper screen if necessary
		if (self.iLastScreen == CvScreenEnums.PEDIA_UNIT):
			return self.pediaUnitScreen.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_TECH):
			return self.pediaTechScreen.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_BUILDING):
			return self.pediaBuildingScreen.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_PROMOTION):
			return self.pediaPromotionScreen.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_SPELL):
			return self.pediaSpellScreen.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_UNIT_CHART):
			return self.pediaUnitChartScreen.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_BONUS):
			return self.pediaBonusScreen.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_TERRAIN):
			return self.pediaTerrainScreen.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_FEATURE):
			return self.pediaFeatureScreen.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_IMPROVEMENT):
			return self.pediaImprovementScreen.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_CIVIC):
			return self.pediaCivicScreen.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_CIVILIZATION):
			return self.pediaCivilizationScreen.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_LEADER):
			return self.pediaLeaderScreen.handleInput(inputClass)
##--------	BUGFfH: Added by Denev 2009/09/19
		if (self.iLastScreen == CvScreenEnums.PEDIA_TRAIT):
			return self.pediaTraitScreen.handleInput(inputClass)
##--------	BUGFfH: End Add
		if (self.iLastScreen == CvScreenEnums.PEDIA_SPECIALIST):
			return self.pediaSpecialistScreen.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_PROJECT):
			return self.pediaProjectScreen.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_RELIGION):
			return self.pediaReligionScreen.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_CORPORATION):
			return self.pediaCorporationScreen.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_HISTORY):
			return self.pediaHistoricalScreen.handleInput(inputClass)

		return 0

##--------	BUGFfH: Added by Denev 2009/09/19
	def placeItems(self, liItem, pItemInfo, iWidget, nColumns):
		screen = self.getScreen()

		nEntries = len(liItem)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = self.getNextWidgetName()
		screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 25, 25, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iNumRows = 0
		for iIndex, (szDescription, iItem) in enumerate(liItem):
			iRow = iIndex % nRows
			iColumn = iIndex // nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)

			if (pItemInfo == gc.getConceptInfo):
				data1 = CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT
				data2 = iItem
			elif (pItemInfo == gc.getNewConceptInfo):
				data1 = CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT_NEW
				data2 = iItem
			elif (pItemInfo == gc.getLeaderHeadInfo):
				data1 = iItem						#LeaderHeadID
				data2 = self.pickLeaderCiv(iItem)	#CivilizationID which includes Leader
			else:
				data1 = iItem
				data2 = 1		#dummy data

			if pItemInfo == gc.getUnitInfo:
				szButton = gc.getUnitInfo(iItem).getUnitButtonWithCivArtStyle(self.iActiveCiv)
				screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + szDescription + u"</font>", szButton, iWidget, data1, data2, CvUtil.FONT_LEFT_JUSTIFY)
			else:
				screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + szDescription + u"</font>", pItemInfo(iItem).getButton(), iWidget, data1, data2, CvUtil.FONT_LEFT_JUSTIFY)

	def pickLeaderCiv(self, iLeader):
		liLeaderCiv = []
		iLeaderCiv = CivilizationTypes.NO_CIVILIZATION
		for iCiv in range(gc.getNumCivilizationInfos()):
			pCiv = gc.getCivilizationInfo(iCiv)
			if pCiv.isLeaders(iLeader):
				liLeaderCiv.append(iCiv)
		if len(liLeaderCiv) > 0:
			iLeaderCiv = liLeaderCiv[CyGame().getSorenRandNum(len(liLeaderCiv), "PickLeaderCiv")]

		return iLeaderCiv
##--------	BUGFfH: End Add
