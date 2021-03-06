import CvUtil
from CvPythonExtensions import *
import PyHelpers
PyPlayer = PyHelpers.PyPlayer

gc = CyGlobalContext()

import CustomFunctions
cf = CustomFunctions.CustomFunctions()

def	spellCallToArms(pCaster):
	pPlayer = gc.getPlayer(pCaster.getOwner())
	pPlot = pCaster.plot()
	pCity = pPlot.getPlotCity()
	eConscript = pCity.getConscriptUnit()
	if (eConscript != -1):
		pPlayer.initUnit(eConscript, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

	return

def reqLightOfLugus(pCaster):
	pPlayer = gc.getPlayer(pCaster.getOwner())
	pPlot = pCaster.plot()
	pOtherPlayer = gc.getPlayer(pPlot.getOwner())
	pCity = pPlot.getPlotCity()

	if pPlot.getTeam() == pCaster.getTeam():
		return false

	if not pCity.isCapital():
		return false

	if pOtherPlayer.getAlignment() != gc.getInfoTypeForString('ALIGNMENT_GOOD'):
		return false

	return true

def spellLightOfLugus(pCaster):
	pPlayer = gc.getPlayer(pCaster.getOwner())
	pPlot = pCaster.plot()
	pOtherPlayer = gc.getPlayer(pPlot.getOwner())
	pCity = pPlot.getPlotCity()

	pOtherPlayer.AI_changeMemoryCount(pPlayer.getID(), MemoryTypes.MEMORY_EVENT_GOOD_TO_US, 1)

def reqVisionary(pCaster):
	ePlayer = pCaster.getOwner()
	pPlayer = gc.getPlayer(ePlayer)
	pPlot = pCaster.plot()

	if pPlot.getOwner() != ePlayer:
		return false

	if pPlot.getImprovementType() == -1:
		return false

	if pPlot.getUpgradeTimeLeft(pPlot.getImprovementType(), ePlayer) <= 0:
		return false

	return true

def spellVisionary(pCaster):
	ePlayer = pCaster.getOwner()
	pPlayer = gc.getPlayer(ePlayer)
	pPlot = pCaster.plot()

	pPlot.changeUpgradeProgress(20)
	return

def	spellLugusGuidance(pCaster):
	pPlayer = gc.getPlayer(pCaster.getOwner())
	pPlot = pCaster.plot()
	eGreatperson = -1
	iRand = CyGame().getSorenRandNum(4, "Lugus Guidance")
	if iRand == 0:
		eGreatperson = gc.getInfoTypeForString('UNIT_ARTIST')
	if iRand == 1:
		eGreatperson = gc.getInfoTypeForString('UNIT_MERCHANT')
	if iRand == 2:
		eGreatperson = gc.getInfoTypeForString('UNIT_SCIENTIST')
	if iRand == 3:
		eGreatperson = gc.getInfoTypeForString('UNIT_ENGINEER')

	if (eGreatperson != -1):
		pPlayer.initUnit(eGreatperson, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

	return

def	spellMiracleKilmorphProduction(pCaster):
	pCity = pCaster.plot().getPlotCity()

	pCity.changeProduction(60)

def spellBountyOfKilmorph(caster):
	pPlayer = gc.getPlayer(caster.getOwner())

	iMapPlots=CyMap().numPlots()

	listPlots = []

	for i in range(iMapPlots):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.isHills():
			if pPlot.getOwner()==caster.getOwner():
				if pPlot.getBonusType(-1)==-1:
					listPlots.append(i)

	if len(listPlots)>0:
		iRnd=CyGame().getSorenRandNum(len(listPlots), "Arrrgh")
		pPlot = CyMap().plotByIndex(listPlots[iRnd])
		lBonusList = []
		lBonusList = lBonusList + ['BONUS_IRON']
		lBonusList = lBonusList + ['BONUS_COPPER']
		lBonusList = lBonusList + ['BONUS_MITHRIL']
		lBonusList = lBonusList + ['BONUS_GEMS']
		lBonusList = lBonusList + ['BONUS_SILVER']
		lBonusList = lBonusList + ['BONUS_AMBER']

		sBonus = lBonusList[CyGame().getSorenRandNum(len(lBonusList), "Pick Bonus")]
		pPlot.setBonusType(gc.getInfoTypeForString(sBonus))
		return
