import CvUtil
from CvPythonExtensions import *
import PyHelpers
PyPlayer = PyHelpers.PyPlayer

gc = CyGlobalContext()

import CustomFunctions
cf = CustomFunctions.CustomFunctions()

#ELOHIM

def doTurnElohim(argsList):
	'Run once a Turn'
	iGameTurn  = argsList[0]
	iPlayer = argsList[1]
	pPlayer = gc.getPlayer(iPlayer)

	pPlayer = gc.getPlayer(iPlayer)
	if not (pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_ELOHIM')):
		return

	iPurity=ElohimFunctions.doElohimPurity(ElohimFunctions(),iPlayer)
	pPlayer.setPurityCounter(iPurity)
#	CyInterface().addMessage(0,true,25,"This is Player is (%i)" %(iPurity),'',0,'',ColorTypes(11), 0, 0, True,True)
	if iPurity>50:
		if CyGame().getSorenRandNum(iPurity, "Purity") > CyGame().getGlobalCounter():
			CyGame().changeGlobalCounter(-1)

	py = PyPlayer(iPlayer)

	for pUnit in py.getUnitList():
		if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_MONK'):
			if iPurity<25:
				pUnit.setBaseCombatStr(16)
				pUnit.setBaseCombatStrDefense(16)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MONK_3'),false)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MONK_4'),false)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MONK_5'),false)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MONK_6'),false)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MONK_7'),false)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MONK_9'),false)
			elif iPurity<50:
				pUnit.setBaseCombatStr(18)
				pUnit.setBaseCombatStrDefense(18)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MONK_3'),true)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MONK_4'),true)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MONK_5'),false)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MONK_6'),false)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MONK_7'),false)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MONK_9'),false)
			elif iPurity<75:
				pUnit.setBaseCombatStr(20)
				pUnit.setBaseCombatStrDefense(20)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MONK_3'),true)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MONK_4'),true)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MONK_5'),true)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MONK_6'),true)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MONK_7'),false)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MONK_9'),false)
			else:
				pUnit.setBaseCombatStr(22)
				pUnit.setBaseCombatStrDefense(22)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MONK_3'),true)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MONK_4'),true)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MONK_5'),true)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MONK_6'),true)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MONK_7'),true)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MONK_9'),true)



class ElohimFunctions:

	def doElohimPurity(self,iPlayer):
		if iPlayer == -1:
			pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
		else:
			pPlayer = gc.getPlayer(iPlayer)

		if pPlayer.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_ELOHIM'):
			return

		#Purity From Buildings
		iPurity = pPlayer.CalculateCivCounter(0,0)

		#Bonus From Mana
		iManaMod=100+pPlayer.CalculateCivCounter(1,0)

#Pacifism Civic Bonus
		iUFmod =100+pPlayer.CalculateCivCounter(2,0)

#Unique features Modifier
		iUFmod+=pPlayer.CalculateCivCounter(3,0)

#State Religion Modifier
		iRelMod=pPlayer.CalculateCivCounter(4,0)

#UF sealed
		iUFBonus=pPlayer.CalculateCivCounter(5,0)
	# Difficulty level modifier
		iHumanmod = 100
		iAImod = 100
		if pPlayer.isHuman():
			iDifficulty = gc.getNumHandicapInfos() + 1 - int(gc.getGame().getHandicapType())
			iHumanmod = 50 + (iDifficulty * 10)
			iAImod = 100
		else:
			iDifficulty = gc.getNumHandicapInfos() + 1 - int(gc.getGame().getHandicapType())
			iAImod = 70 + (iDifficulty * 10)
			iHumanmod = 100

		iPurity *=iManaMod
		iPurity /=100

		iPurity*=iHumanmod
		iPurity/=iAImod

		iPurity/=99+pPlayer.getNumCities()*pPlayer.getNumCities()

		if iPurity>50:
			iPurity=50

		iPurity*=iUFmod
		iPurity/=100

		iPurity*=iRelMod
		iPurity/=100

		iPurity+=iUFBonus

		if iPurity>100:
			return 100
		elif iPurity<0:
			return 0

		return iPurity
