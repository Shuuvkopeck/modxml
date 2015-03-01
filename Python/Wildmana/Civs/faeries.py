import CvUtil
from CvPythonExtensions import *

import PyHelpers
PyPlayer = PyHelpers.PyPlayer

gc = CyGlobalContext()

def reqBrilliance(caster):
	iVampire = gc.getInfoTypeForString('PROMOTION_VAMPIRE')
	iWerewolf = gc.getInfoTypeForString('PROMOTION_WEREWOLF')
	iX = caster.getX()
	iY = caster.getY()
	pPlayer = gc.getPlayer(caster.getOwner())
	eTeam = pPlayer.getTeam()
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			pPlot = CyMap().plot(iiX,iiY)
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if (pUnit.getRace() == iVampire or pUnit.getRace() == iWerewolf):
					if pPlayer.isHuman():
						return True
					p2Player = gc.getPlayer(pUnit.getOwner())
					e2Team = gc.getTeam(p2Player.getTeam())
					if e2Team.isAtWar(eTeam):
						return True
	return False

def spellBrilliance(pCaster):
	iVampire = gc.getInfoTypeForString('PROMOTION_VAMPIRE')
	iWerewolf = gc.getInfoTypeForString('PROMOTION_WEREWOLF')
	iX = caster.getX()
	iY = caster.getY()
	pPlayer = gc.getPlayer(caster.getOwner())
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			pPlot = CyMap().plot(iiX,iiY)
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if (pUnit.getRace() == iVampire or pUnit.getRace() == iWerewolf):
					pUnit.doDamage(30, 60, caster, gc.getInfoTypeForString('DAMAGE_HOLY'), true)