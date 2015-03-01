from CvPythonExtensions import *
import CvUtil
import Popup as PyPopup
import CvScreensInterface
import sys
import PyHelpers
import CustomFunctions

cf = CustomFunctions.CustomFunctions()

PyInfo = PyHelpers.PyInfo
PyPlayer = PyHelpers.PyPlayer
gc = CyGlobalContext()

def globalenchantment(argsList):
	iPlayer, eProject = argsList
	GE = gc.getProjectInfo(eProject)
	eval(GE.getPyResult())
	
def addWhiteHandUnit(iUnit):
	pBestPlot = -1
	iBestPlot = -1
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		iPlot = -1
		if pPlot.isWater() == False:
			if pPlot.getNumUnits() == 0:
				if pPlot.isCity() == False:
					if pPlot.isImpassable() == False:
						iPlot = CyGame().getSorenRandNum(500, "Add Unit")
						iPlot = iPlot + (pPlot.area().getNumTiles() * 10)
						if pPlot.isOwned():
							iPlot = iPlot / 2
						if iPlot > iBestPlot:
							iBestPlot = iPlot
							pBestPlot = pPlot
	if iBestPlot != -1:
		bPlayer = gc.getPlayer(gc.getWHITEHAND_PLAYER())
		newUnit = bPlayer.initUnit(iUnit, pBestPlot.getX(), pBestPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)	
		
def samhain(iPlayer):
	for pyCity in PyPlayer(iPlayer).getCityList():
		pCity = pyCity.GetCy()
		pCity.changeHappinessTimer(20)
	iCount = CyGame().countCivPlayersAlive() + int(CyGame().getHandicapType()) - 5
	for i in range(iCount):
	
		addWhiteHandUnit(gc.getInfoTypeForString('UNIT_FROSTLING'))
		addWhiteHandUnit(gc.getInfoTypeForString('UNIT_FROSTLING'))
		addWhiteHandUnit(gc.getInfoTypeForString('UNIT_FROSTLING_ARCHER'))
		addWhiteHandUnit(gc.getInfoTypeForString('UNIT_FROSTLING_WOLF_RIDER'))
	addWhiteHandUnit(gc.getInfoTypeForString('UNIT_MOKKA'))

def whitehand(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCapitalCity()
	iPriest = gc.getInfoTypeForString('UNIT_PRIEST_OF_WINTER')
	
	bDum=true
	bRiu=true
	bAna=true
	py = PyPlayer(iPlayer)
	for pUnit in py.getUnitList():
		if pUnit.getUnitType()==iPriest:
			if pUnit.getNameKey()=="Dumannios":
				bDum=false
			if pUnit.getNameKey()=="Riuros":
				bRiu=false
			if pUnit.getNameKey()=="Anagantios":
				bAna=false

	if bDum:
		newUnit1 = pPlayer.initUnit(iPriest, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit1.setName("Dumannios")
		
	if bRiu:		
		newUnit2 = pPlayer.initUnit(iPriest, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit2.setName("Riuros")
	
	if bAna:	
		newUnit3 = pPlayer.initUnit(iPriest, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit3.setName("Anagantios")
		
def deepening(iPlayer):	
	iDesert = gc.getInfoTypeForString('TERRAIN_DESERT')
	iGrass = gc.getInfoTypeForString('TERRAIN_GRASS')
	iMarsh = gc.getInfoTypeForString('TERRAIN_MARSH')
	iPlains = gc.getInfoTypeForString('TERRAIN_PLAINS')
	iSnow = gc.getInfoTypeForString('TERRAIN_SNOW')
	iTundra = gc.getInfoTypeForString('TERRAIN_TUNDRA')
	iBlizzard = gc.getInfoTypeForString('FEATURE_BLIZZARD')
	iTimer = 40 + (CyGame().getGameSpeedType() * 20)
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		bValid = False
		if pPlot.isWater() == False:
			if CyGame().getSorenRandNum(100, "The Deepening") < 75:
				iTerrain = pPlot.getTerrainType()
				chance = CyGame().getSorenRandNum(100, "Bob")
				if iTerrain == iSnow:
					bValid = True
				if iTerrain == iTundra:
					pPlot.setTempTerrainType(iSnow, CyGame().getSorenRandNum(iTimer, "Bob") + 10)
					bValid = True
				if iTerrain == iGrass or iTerrain == iMarsh:
					if chance < 40:
						pPlot.setTempTerrainType(iSnow, CyGame().getSorenRandNum(iTimer, "Bob") + 10)
					else:
						pPlot.setTempTerrainType(iTundra, CyGame().getSorenRandNum(iTimer, "Bob") + 10)
					bValid = True
				if iTerrain == iPlains:
					if chance < 60:
						pPlot.setTempTerrainType(iSnow, CyGame().getSorenRandNum(iTimer, "Bob") + 10)
					else:
						pPlot.setTempTerrainType(iTundra, CyGame().getSorenRandNum(iTimer, "Bob") + 10)
					bValid = True
				if iTerrain == iDesert:
					if chance < 10:
						pPlot.setTempTerrainType(iSnow, CyGame().getSorenRandNum(iTimer, "Bob") + 10)
					elif chance < 30:
						pPlot.setTempTerrainType(iTundra, CyGame().getSorenRandNum(iTimer, "Bob") + 10)
					else:
						pPlot.setTempTerrainType(iPlains, CyGame().getSorenRandNum(iTimer, "Bob") + 10)
				if bValid:
					if CyGame().getSorenRandNum(750, "The Deepening") < 10:
						pPlot.setFeatureType(iBlizzard,-1)
						
def GrigoriAdventure(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	
	iMapPlots=CyMap().numPlots()
	listPlots = []
	
	for i in range(iMapPlots):
		bvalid=false
		pPlot = CyMap().plotByIndex(i)			
		if not pPlot.isWater():
			if not pPlot.isPeak():
				if pPlot.getOwner()==iPlayer:
					if pPlot.getImprovementType()==-1:
						bValid=true
						for iiX in range(pPlot.getX()-2, pPlot.getY()+3, 1):
							for iiY in range(pPlot.getY()-2, pPlot.getY()+3, 1):
								pPlot2 = CyMap().plot(iiX,iiY)
								if pPlot2.getImprovementType()==gc.getInfoTypeForString('IMPROVEMENT_DUNGEON'):
									bValid=false
								
						if bValid:
							listPlots.append(i)

	if(len(listPlots)>0):	
		iRnd=CyGame().getSorenRandNum(len(listPlots), "New Dungeon")
		pPlot = CyMap().plotByIndex(listPlots[iRnd])			
		pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_DUNGEON'))
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DUNGEON_DISCOVERED",()),'AS2D_DISCOVERBONUS',3,', ,Art/Interface/Buttons/Spells/Spells_Atlas1.dds,3,4',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)


def GiftofKilmorph(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	pPlayer.changeGlobalYield(YieldTypes.YIELD_METAL,300)

def DemonPortal(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	pPlot = pPlayer.getCapitalCity().plot()
	
	iUnitType = gc.getInfoTypeForString('UNIT_CHAOS_MARAUDER')
	
	if CyGame().getGlobalCounter()>50:
		iUnitType = gc.getInfoTypeForString('UNIT_SUCCUBUS')	
	if CyGame().getGlobalCounter()>75:
		iUnitType = gc.getInfoTypeForString('UNIT_MANTICORE')	
		
	if iUnitType!=-1:
		newUnit = pPlayer.initUnit(iUnitType, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)	