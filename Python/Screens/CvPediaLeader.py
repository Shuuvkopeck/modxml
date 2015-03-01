## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## Alex Mantzaris / Jesse Smith 09-2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
##--------	BUGFfH: Added by Denev 2009/09/27
import CvPediaScreen		# base class
##--------	BUGFfH: End Add
import CvScreenEnums
import random

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

##--------	BUGFfH: Modified by Denev 2009/09/27
#class CvPediaLeader:
class CvPediaLeader( CvPediaScreen.CvPediaScreen ):
	"Civilopedia Screen for Leaders"

	def __init__(self, main):
		self.iLeader = -1
		self.top = main

##--------	BUGFfH: Modified by Denev 2009/09/23
		"""
		self.X_LEADERHEAD_PANE = 20
		self.Y_LEADERHEAD_PANE = 65
		self.W_LEADERHEAD_PANE = 370
		self.H_LEADERHEAD_PANE = 390

		self.W_LEADERHEAD = 320
		self.H_LEADERHEAD = 384
		self.X_LEADERHEAD = self.X_LEADERHEAD_PANE + ((self.W_LEADERHEAD_PANE - self.W_LEADERHEAD) / 2)
		self.Y_LEADERHEAD = self.Y_LEADERHEAD_PANE + ((self.H_LEADERHEAD_PANE - self.H_LEADERHEAD) / 2) + 3 # Fudge factor

		self.X_HISTORY = self.X_LEADERHEAD_PANE + self.W_LEADERHEAD_PANE + 20
		self.Y_HISTORY = self.Y_LEADERHEAD_PANE + 85
		self.W_HISTORY = 370
		self.H_HISTORY = 550

		self.X_TRAITS = 20
		self.Y_TRAITS = self.Y_LEADERHEAD_PANE + self.H_LEADERHEAD_PANE + 5
		self.W_TRAITS = self.W_LEADERHEAD_PANE
		self.H_TRAITS = 240

		self.X_CIV = self.X_LEADERHEAD_PANE + self.W_LEADERHEAD_PANE + 20
		self.Y_CIV = self.Y_LEADERHEAD_PANE + 15
		self.W_CIV = 64
		self.H_CIV = 64

		self.X_CIVIC = self.X_HISTORY + self.W_CIV + 10
		self.Y_CIVIC = self.Y_LEADERHEAD_PANE - 5
		self.W_CIVIC = self.W_HISTORY - self.W_CIV - 10
		self.H_CIVIC = 80
		"""
		X_MERGIN = self.top.X_MERGIN
		Y_MERGIN = self.top.Y_MERGIN

		self.X_LEADERHEAD_PANE = self.top.X_PEDIA_PAGE
		self.Y_LEADERHEAD_PANE = self.top.Y_PEDIA_PAGE
		self.W_LEADERHEAD_PANE = 370
		self.H_LEADERHEAD_PANE = 390

		self.W_LEADERHEAD = 320
		self.H_LEADERHEAD = 384
		self.X_LEADERHEAD = self.X_LEADERHEAD_PANE + ((self.W_LEADERHEAD_PANE - self.W_LEADERHEAD) / 2)
		self.Y_LEADERHEAD = self.Y_LEADERHEAD_PANE + ((self.H_LEADERHEAD_PANE - self.H_LEADERHEAD) / 2) + 3 # Fudge factor

		self.H_HISTORY = 550
		self.X_HISTORY = self.X_LEADERHEAD_PANE + self.W_LEADERHEAD_PANE + X_MERGIN
		self.Y_HISTORY = self.top.B_PEDIA_PAGE - self.H_HISTORY
		self.W_HISTORY = self.top.R_PEDIA_PAGE - self.X_HISTORY

		self.X_TRAITS = self.X_LEADERHEAD_PANE
		self.Y_TRAITS = self.Y_LEADERHEAD_PANE + self.H_LEADERHEAD_PANE + Y_MERGIN
		self.W_TRAITS = self.W_LEADERHEAD_PANE
		self.H_TRAITS = self.top.B_PEDIA_PAGE - self.Y_TRAITS

		self.W_CIV = 64
		self.H_CIV = 64
		self.X_CIV = self.X_HISTORY
		self.Y_CIV = self.Y_HISTORY - self.H_CIV - Y_MERGIN

		self.H_CIVIC = 80
		self.X_CIVIC = self.X_CIV + self.W_CIV + X_MERGIN
		self.Y_CIVIC = self.Y_HISTORY - self.H_CIVIC - Y_MERGIN
		self.W_CIVIC = self.top.R_PEDIA_PAGE - self.X_CIVIC
##--------	BUGFfH: End Modify

	# Screen construction function
	def interfaceScreen(self, iLeader):

		self.iLeader = iLeader

		self.top.deleteAllWidgets()

		screen = self.top.getScreen()

		bNotActive = (not screen.isActive())
		if bNotActive:
			self.top.setPediaCommonWidgets()

		# Header...
		szHeader = u"<font=4b>" + gc.getLeaderHeadInfo(self.iLeader).getDescription().upper() + u"</font>"
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Top
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_LEADER, -1)

		if self.top.iLastScreen	!= CvScreenEnums.PEDIA_LEADER or bNotActive:
			self.placeLinks(true)
			self.top.iLastScreen = CvScreenEnums.PEDIA_LEADER
		else:
			self.placeLinks(false)

		# Leaderhead
		leaderPanelWidget = self.top.getNextWidgetName()
		screen.addPanel( leaderPanelWidget, "", "", true, true,
						 self.X_LEADERHEAD_PANE, self.Y_LEADERHEAD_PANE, self.W_LEADERHEAD_PANE, self.H_LEADERHEAD_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		self.leaderWidget = self.top.getNextWidgetName()
		screen.addLeaderheadGFC(self.leaderWidget, self.iLeader, AttitudeTypes.ATTITUDE_PLEASED,
						 self.X_LEADERHEAD, self.Y_LEADERHEAD, self.W_LEADERHEAD, self.H_LEADERHEAD, WidgetTypes.WIDGET_GENERAL, -1, -1)

		self.placeHistory()
		self.placeCivic()
		self.placeCiv()
		self.placeTraits()

	def placeCiv(self):
		screen = self.top.getScreen()

##--------	BUGFfH: Added by Denev 2009/09/27
		liLeaderCiv = []
##--------	BUGFfH: End Add
		for iCiv in range(gc.getNumCivilizationInfos()):
			civ = gc.getCivilizationInfo(iCiv)
			if civ.isLeaders(self.iLeader):
##--------	BUGFfH: Modified by Denev 2009/09/27
#				screen.setImageButton(self.top.getNextWidgetName(), civ.getButton(), self.X_CIV, self.Y_CIV, self.W_CIV, self.H_CIV, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, iCiv, 1)
				liLeaderCiv.append(iCiv)
		if len(liLeaderCiv) > 0:
			iCiv = random.choice(liLeaderCiv)
			szButton = gc.getCivilizationInfo(iCiv).getButton()
			screen.setImageButton(self.top.getNextWidgetName(), szButton, self.X_CIV, self.Y_CIV, self.W_CIV, self.H_CIV, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, iCiv, 1)
##--------	BUGFfH: End Modify

	def placeTraits(self):
		screen = self.top.getScreen()

		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_TRAITS", ()), "", true, false,
						 self.X_TRAITS, self.Y_TRAITS, self.W_TRAITS, self.H_TRAITS, PanelStyles.PANEL_STYLE_BLUE50 )

		listName = self.top.getNextWidgetName()

		iNumCivs = 0
		iLeaderCiv = -1
		for iCiv in range(gc.getNumCivilizationInfos()):
			civ = gc.getCivilizationInfo(iCiv)
			if civ.isLeaders(self.iLeader):
				iNumCivs += 1
				iLeaderCiv = iCiv

		if iNumCivs == 1:
			szSpecialText = CyGameTextMgr().parseLeaderTraits(self.iLeader, iLeaderCiv, False, True)
		else:
			szSpecialText = CyGameTextMgr().parseLeaderTraits(self.iLeader, -1, False, True)
		szSpecialText = szSpecialText[1:]
##--------	BUGFfH: Modified by Denev 2009/09/27
#		screen.addMultilineText(listName, szSpecialText, self.X_TRAITS+5, self.Y_TRAITS+30, self.W_TRAITS-10, self.H_TRAITS-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.addMultilineText(listName, szSpecialText, self.X_TRAITS+5, self.Y_TRAITS+30, self.W_TRAITS-5, self.H_TRAITS-32, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
##--------	BUGFfH: End Modify

	def placeCivic(self):
		screen = self.top.getScreen()

		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_FAV_CIVIC", ()), "", true, true,
						 self.X_CIVIC, self.Y_CIVIC, self.W_CIVIC, self.H_CIVIC, PanelStyles.PANEL_STYLE_BLUE50 )

		iCivic = gc.getLeaderHeadInfo(self.iLeader).getFavoriteCivic()
		if (-1 != iCivic):

#FfH: Modified by Kael 10/12/2007
#			szCivicText = u"<link=literal>" + gc.getCivicInfo(iCivic).getDescription() + u"</link>"
			szCivicText = u"" + localText.getText("TXT_KEY_MISC_FAVORITE_CIVIC", ())  + " <link=literal>" + gc.getCivicInfo(iCivic).getDescription() + u"</link>"
#FfH: End Modify

			listName = self.top.getNextWidgetName()
			screen.addMultilineText(listName, szCivicText, self.X_CIVIC+5, self.Y_CIVIC+30, self.W_CIVIC-10, self.H_CIVIC-10, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

#FfH: Added by Kael 12/31/2006
		iWonder = gc.getLeaderHeadInfo(self.iLeader).getFavoriteWonder()
		if (-1 != iWonder):
			szWonderText = u"" + localText.getText("TXT_KEY_MISC_FAVORITE_WONDER", ())  + " <link=literal>" + gc.getBuildingInfo(iWonder).getDescription() + u"</link>"
			listName = self.top.getNextWidgetName()
			screen.addMultilineText(listName, szWonderText, self.X_CIVIC+5, self.Y_CIVIC+50, self.W_CIVIC-10, self.H_CIVIC-10, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
#FfH: End Add

	def placeHistory(self):
		screen = self.top.getScreen()

		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, "", "", true, true,
			self.X_HISTORY, self.Y_HISTORY, self.W_HISTORY, self.H_HISTORY, PanelStyles.PANEL_STYLE_BLUE50 )

		historyTextName = self.top.getNextWidgetName()
		CivilopediaText = gc.getLeaderHeadInfo(self.iLeader).getCivilopedia()
		CivilopediaText = u"<font=2>" + CivilopediaText + u"</font>"
		screen.attachMultilineText( panelName, historyTextName, CivilopediaText,
			WidgetTypes.WIDGET_GENERAL,-1,-1, CvUtil.FONT_LEFT_JUSTIFY )


	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()

		if bRedraw:
			screen.clearListBoxGFC(self.top.LIST_ID)

		# sort leaders alphabetically
##--------	BUGFfH: Modified by Denev 2009/09/27
		"""
		rowListName=[(0,0)]*gc.getNumLeaderHeadInfos()
		for j in range(gc.getNumLeaderHeadInfos()):
			rowListName[j] = (gc.getLeaderHeadInfo(j).getDescription(), j)
		rowListName.sort()

		i = 0
		iSelected = 0
		for iI in range(gc.getNumLeaderHeadInfos()):
			if (rowListName[iI][1] != gc.getDefineINT("BARBARIAN_LEADER") and not gc.getLeaderHeadInfo(rowListName[iI][1]).isGraphicalOnly()

#FfH: Added by Kael 04/28/2008
			 and not gc.getLeaderHeadInfo(rowListName[iI][1]).isGraphicalOnly()
#FfH: End Add

			):
				if (not gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY") or not gc.getGame().isFinalInitialized() or gc.getGame().isLeaderEverActive(rowListName[iI][1])):
					if bRedraw:
						screen.appendListBoxStringNoUpdate(self.top.LIST_ID, rowListName[iI][0], WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, rowListName[iI][1], -1, CvUtil.FONT_LEFT_JUSTIFY)
					if rowListName[iI][1] == self.iLeader:
						iSelected = i
					i += 1

		if bRedraw:
			screen.updateListBox(self.top.LIST_ID)
		"""
		listSorted = self.getSortedList( gc.getNumLeaderHeadInfos(), gc.getLeaderHeadInfo )

		iSelected = 0
		for iIndex, (szDescription, iLeaderHead) in enumerate(listSorted):
			if (not gc.getLeaderHeadInfo(iLeaderHead).isGraphicalOnly()):
				if bRedraw:
					screen.appendListBoxString(self.top.LIST_ID, szDescription, WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, iLeaderHead, -1, CvUtil.FONT_LEFT_JUSTIFY)
				if iLeaderHead == self.iLeader:
					iSelected = iIndex
##--------	BUGFfH: End Modify

		screen.setSelectedListBoxStringGFC(self.top.LIST_ID, iSelected)


	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CHARACTER):
			if (inputClass.getData() == int(InputTypes.KB_0)):
				self.top.getScreen().performLeaderheadAction(self.leaderWidget, LeaderheadAction.LEADERANIM_GREETING)
			elif (inputClass.getData() == int(InputTypes.KB_6)):
				self.top.getScreen().performLeaderheadAction(self.leaderWidget, LeaderheadAction.LEADERANIM_DISAGREE)
			elif (inputClass.getData() == int(InputTypes.KB_7)):
				self.top.getScreen().performLeaderheadAction(self.leaderWidget, LeaderheadAction.LEADERANIM_AGREE)
			elif (inputClass.getData() == int(InputTypes.KB_1)):
				self.top.getScreen().setLeaderheadMood(self.leaderWidget, AttitudeTypes.ATTITUDE_FRIENDLY)
				self.top.getScreen().performLeaderheadAction(self.leaderWidget, LeaderheadAction.NO_LEADERANIM)
			elif (inputClass.getData() == int(InputTypes.KB_2)):
				self.top.getScreen().setLeaderheadMood(self.leaderWidget, AttitudeTypes.ATTITUDE_PLEASED)
				self.top.getScreen().performLeaderheadAction(self.leaderWidget, LeaderheadAction.NO_LEADERANIM)
			elif (inputClass.getData() == int(InputTypes.KB_3)):
				self.top.getScreen().setLeaderheadMood(self.leaderWidget, AttitudeTypes.ATTITUDE_CAUTIOUS)
				self.top.getScreen().performLeaderheadAction(self.leaderWidget, LeaderheadAction.NO_LEADERANIM)
			elif (inputClass.getData() == int(InputTypes.KB_4)):
				self.top.getScreen().setLeaderheadMood(self.leaderWidget, AttitudeTypes.ATTITUDE_ANNOYED)
				self.top.getScreen().performLeaderheadAction(self.leaderWidget, LeaderheadAction.NO_LEADERANIM)
			elif (inputClass.getData() == int(InputTypes.KB_5)):
				self.top.getScreen().setLeaderheadMood(self.leaderWidget, AttitudeTypes.ATTITUDE_FURIOUS)
				self.top.getScreen().performLeaderheadAction(self.leaderWidget, LeaderheadAction.NO_LEADERANIM)
			else:
				self.top.getScreen().leaderheadKeyInput(self.leaderWidget, inputClass.getData())
		return 0
