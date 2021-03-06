## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## Implementaion of miscellaneous game functions

import CvUtil
from CvPythonExtensions import *
import CvEventInterface
import CustomFunctions
import math

import PyHelpers
PyPlayer = PyHelpers.PyPlayer

import ScreenInput
import CvScreenEnums
import CvScreensInterface

# globals
cf = CustomFunctions.CustomFunctions()
gc = CyGlobalContext()


class CvWMGameUtils:
	"Miscellaneous game functions"
	def __init__(self):
		pass

#Return 1 if the improvement on the plot should not be removed
	def AI_AnimalLairExplored(self,argsList):
		pPlot=argsList[0]
		ePlayer=argsList[1]
		pUnit=argsList[2]
		pPlayer = gc.getPlayer(ePlayer)
		iType=pPlot.getImprovementType()
		iBonus= pPlot.getBonusType(-1)

		if CyGame().getGameTurn()==0:
			return 0

		bHunting=false
		if pPlayer.isHasTech(gc.getInfoTypeForString('TECH_HUNTING')):
			bHunting=true

		iGoldValue=CyGame().getSorenRandNum(15, 'Gold gained')
		iGoldValue+=10

		iGoldValue+=3*pPlayer.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_HUNTING_LODGE'))
		CyInterface().addMessage(ePlayer,true,25,"You gained %s gold from selling the dead animals at a local market!" %(iGoldValue),'',0,'',ColorTypes(11), pPlot.getX(), pPlot.getY(), True,True)
		pPlayer.changeGold(iGoldValue)

		if (iType==gc.getInfoTypeForString('IMPROVEMENT_HILLGIANT_FORTRESS') or iType==gc.getInfoTypeForString('IMPROVEMENT_WEREWOLF_CASTLE')):
			if iBonus==-1:
				if CyGame().getSorenRandNum(100, 'Here be Ruins')<50:
					pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_RUINS'))
					return 1
				else:
					pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_DUNGEON'))
					return 1

		if bHunting:
			if CyGame().getSorenRandNum(100, 'Rescue a Hunter')<3:
				CyInterface().addMessage(ePlayer,true,25,"A wounded Hunter joins you after you rescue him.",'',0,'',ColorTypes(11), pPlot.getX(), pPlot.getY(), True,True)
				pPlot.setImprovementType(-1)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HUNTER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				return 0

			if CyGame().getSorenRandNum(100, 'Rescue an Adept')<3:
				CyInterface().addMessage(ePlayer,true,25,"An Adept who got lost on his research trip wants to join you.",'',0,'',ColorTypes(11), pPlot.getX(), pPlot.getY(), True,True)
				pPlot.setImprovementType(-1)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ADEPT'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				return 0

		if CyGame().getSorenRandNum(100, 'Spirits Haunting')<3:
			if pPlayer.isHasTech(gc.getInfoTypeForString('TECH_MYSTICISM')):
				CyInterface().addMessage(ePlayer,true,25,"Spirits Haunt the area. One of them joins you after it has been calmed by a Shaman.",'',0,'',ColorTypes(11), pPlot.getX(), pPlot.getY(), True,True)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SPIRIT_GUIDE'),true)
				return 0
			elif (pUnit.getExperience()>2):
				CyInterface().addMessage(ePlayer,true,25,"Spirits Haunt the area. Your unit becomes mad for a few days and looses some of its experience",'',0,'',ColorTypes(11), pPlot.getX(), pPlot.getY(), True,True)
				pUnit.changeExperience(-2, -1, false, false, false)
				return 0

		if CyGame().getSorenRandNum(100, 'local hero')<1:
			iUnitID = pUnit.getID()
			if iUnitID != -1:
				iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_ANIMALLAIR_DEAD_HERO')
				triggerData = pPlayer.initTriggeredData(iEvent, true, -1, pUnit.getX(), pUnit.getY(), pUnit.getOwner(), -1, -1, -1, iUnitID, -1)
				return 0

		return 0

	def AI_CivicValue(self,argsList):
		ePlayer = argsList[0]
		eCivic = argsList[1]
		eCivicOpion=gc.getCivicInfo(eCivic).getCivicOptionType()
		iValue = 2

		if eCivicOpion==gc.getInfoTypeForString('CIVICOPTION_GOVERNMENT'):
			iValue = self.AI_CivicValue_Government(ePlayer, eCivic)

		elif eCivicOpion==gc.getInfoTypeForString('CIVICOPTION_CULTURAL_VALUES'):
			iValue = self.AI_CivicValue_CulturalValues(ePlayer, eCivic)

		elif eCivicOpion==gc.getInfoTypeForString('CIVICOPTION_LABOR'):
			iValue = self.AI_CivicValue_Labor(ePlayer, eCivic)

		elif eCivicOpion==gc.getInfoTypeForString('CIVICOPTION_ECONOMY'):
			iValue = self.AI_CivicValue_Economy(ePlayer, eCivic)

		elif eCivicOpion==gc.getInfoTypeForString('CIVICOPTION_MEMBERSHIP'):
			iValue = self.AI_CivicValue_Membership(ePlayer, eCivic)

		#Special Civics, not only Faeries
		elif eCivicOpion == gc.getInfoTypeForString('CIVICOPTION_FAERIE_COURT'):
			iValue = self.AI_CivicValue_Special(ePlayer, eCivic)

		return iValue

	def AI_CivicValue_Government(self, ePlayer, eCivic):
		pPlayer = gc.getPlayer(ePlayer)
		eCiv = pPlayer.getCivilizationType()
		eAlignment = pPlayer.getAlignment()
		iValue = 2

		bFallow = pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_FALLOW'))

		if eCivic == gc.getInfoTypeForString('CIVIC_CITY_STATES'):
			iValue = 2000
		elif eCivic == gc.getInfoTypeForString('CIVIC_SHAMANISM'):
			if bFallow:
				iValue = 0
			else:
				iValue = self.percentageOfUnhealthyCities(ePlayer) * 10000

		elif eCivic == gc.getInfoTypeForString('CIVIC_WARRIOR_CASTE'):
			iValue = -1000
			if not pPlayer.canSupportMoreUnits():
				iValue = 3000
				pTeam = pPlayer.getTeam()
				if gc.getTeam(pTeam).getAnyWarPlanCount(True) > 0:
					iValue += 5000

#	AI doesn't understand these Civics yet
		elif eCivic == gc.getInfoTypeForString('CIVIC_MILITARY_STATE'):
			iValue = -1000
		elif eCivic == gc.getInfoTypeForString('CIVIC_GOD_KING'):
			iValue = -1000
		elif eCivic == gc.getInfoTypeForString('CIVIC_MAGISTOCRATIE'):
			iValue = -1000

		elif eCivic == gc.getInfoTypeForString('CIVIC_REPUBLIC'):
			if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).isCultureVictory():
				iValue = 2500
			elif eAlignment == gc.getInfoTypeForString('ALIGNMENT_GOOD'):
				iValue += 2500

		return iValue

	def AI_CivicValue_CulturalValues(self, ePlayer, eCivic):
		pPlayer = gc.getPlayer(ePlayer)
		eCiv = pPlayer.getCivilizationType()
		iValue = 2

		bNoUnhappy = false
		bFallow = pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_FALLOW'))

		if eCiv in (gc.getInfoTypeForString('CIVILIZATION_INFERNAL'), gc.getInfoTypeForString('CIVILIZATION_FROZEN')):
			bNoUnhappy = true

		if eCivic == gc.getInfoTypeForString('CIVIC_NATIONHOOD'):
			iValue = 1000
		elif eCivic == gc.getInfoTypeForString('CIVIC_GREED'):
			iValue = 500
			if pPlayer.AI_isFinancialTrouble():
				iValue += 20000
		elif eCivic == gc.getInfoTypeForString('CIVIC_PACIFISM'):
			iValue = -10000
			if eCiv == gc.getInfoTypeForString('CIVILIZATION_ELOHIM'):
				iValue = 10000
			elif eCiv == gc.getInfoTypeForString('CIVILIZATION_GRIGORI'):
				iValue = 10000

		elif eCivic == gc.getInfoTypeForString('CIVIC_SCHOLARSHIP'):
			iValue = 5000
		elif eCivic == gc.getInfoTypeForString('CIVIC_LIBERTY'):
			if eCiv == gc.getInfoTypeForString('CIVILIZATION_KURIOTATES'):
				iValue = 10000
			elif gc.getLeaderHeadInfo(pPlayer.getLeaderType()).isCultureVictory():
				iValue = 10000
		elif eCivic == gc.getInfoTypeForString('CIVIC_SACRIFICE_THE_WEAK'):
			if bFallow:
				# We don't care about food for growth, so all we get is 10% gold
				iValue = 50
			else:
				iValue = 15000
		elif eCivic == gc.getInfoTypeForString('CIVIC_SOCIAL_ORDER'):
			if not bNoUnhappy:
				iValue = 5000
#	AI doesn't understand these Civics yet
		elif eCivic == gc.getInfoTypeForString('CIVIC_RELIGION'):
			iValue = -10000
		elif eCivic == gc.getInfoTypeForString('CIVIC_BENEVOLENCE'):
			iValue = -10000

		return iValue

	def AI_CivicValue_Labor(self, ePlayer, eCivic):
		pPlayer = gc.getPlayer(ePlayer)
		eCiv = pPlayer.getCivilizationType()
		eAlignment = pPlayer.getAlignment()
		iValue = 2

		eAIEcon=pPlayer.AI_getEconomyType()
		bCentralEcon = False
		if eAIEcon == AIEconomyTypes.AIECONOMY_CENTRALIZATION:
			bCentralEcon = True

		bFallow = pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_FALLOW'))

		if eCivic == gc.getInfoTypeForString('CIVIC_APPRENTICESHIP'):
			iValue = 5000
			if bCentralEcon:
				iValue = 8000

		elif eCivic == gc.getInfoTypeForString('CIVIC_ARETE'):
			iValue = 5000
		elif eCivic == gc.getInfoTypeForString('CIVIC_HARVESTING'):
			iValue = 1000

		elif eCivic == gc.getInfoTypeForString('CIVIC_SLAVERY'):
			if eAlignment == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
				if eCiv == gc.getInfoTypeForString('CIVILIZATION_DOVIELLO'):
					iValue = 10000
				elif eCiv == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
					iValue = 10000
				elif not bFallow and pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_CULTURAL_VALUES')) == gc.getInfoTypeForString('CIVIC_SACRIFICE_THE_WEAK'):
					# Well, we need to do *something* with all that excess population...
					iValue += 5000

		elif eCivic == gc.getInfoTypeForString('CIVIC_CASTE_SYSTEM'):
			if pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_CULTURAL_VALUES'))==gc.getInfoTypeForString('CIVIC_SCHOLARSHIP'):
				iValue = 10000

		elif eCivic == gc.getInfoTypeForString('CIVIC_GUILDS'):
			iValue = 10000
			if eCiv == gc.getInfoTypeForString('CIVILIZATION_SIDAR'):
				iValue += 5000

		return iValue

	def AI_CivicValue_Economy(self, ePlayer, eCivic):
		pPlayer = gc.getPlayer(ePlayer)
		eCiv = pPlayer.getCivilizationType()
		iValue = 2

		bCottageEcon = false
		bTradeEcon = false
		bFolEcon = false
		bCentralEcon = false

		eAIEcon=pPlayer.AI_getEconomyType()

		if eAIEcon == AIEconomyTypes.AIECONOMY_COTTAGE:
			bCottageEcon = true

		elif eAIEcon == AIEconomyTypes.AIECONOMY_TRADE:
			bTradeEcon = true

		elif eAIEcon == AIEconomyTypes.AIECONOMY_CENTRALIZATION:
			bCentralEcon = true

		elif eAIEcon == AIEconomyTypes.AIECONOMY_FOL:
			bFolEcon = true

		bAristo = false

		if eCiv == gc.getInfoTypeForString('CIVILIZATION_CALABIM') or eCiv==gc.getInfoTypeForString('CIVILIZATION_SCIONS'):
			bAristo = true

		elif pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_FINANCIAL')):
			bAristo = true

		elif gc.getCivilizationInfo(eCiv).getImpInfrastructureHalfCost() == gc.getInfoTypeForString('IMPROVEMENT_FARM'):
			bAristo = true

		if eCivic == gc.getInfoTypeForString('CIVIC_MERCANTILISM'):
			iValue = 2000
			if bCottageEcon:
				iValue = 8000

		elif eCivic == gc.getInfoTypeForString('CIVIC_CENTRALIZATION'):
			iValue = -300
			if pPlayer.getNumCities() < 6:
				iValue = 5000
			if bCentralEcon:
				iValue = 10000

		elif eCivic == gc.getInfoTypeForString('CIVIC_ARISTOCRACY'):
			iValue = 2500
			if bAristo:
				iValue = 15000

		elif eCivic == gc.getInfoTypeForString('CIVIC_FOREIGN_TRADE'):
			iValue = -300
			if bTradeEcon:
				iValue = 10000

		elif eCivic == gc.getInfoTypeForString('CIVIC_GUARDIAN_OF_NATURE'):
			if bFolEcon:
				iValue = 20000

		elif eCivic == gc.getInfoTypeForString('CIVIC_LOST_LANDS'):
			if eCiv == gc.getInfoTypeForString('CIVILIZATION_MAZATL'):
				iValue = 20000

		return iValue

	def AI_CivicValue_Membership(self, ePlayer, eCivic):
		iValue = 2

		if eCivic == gc.getInfoTypeForString('CIVIC_OVERCOUNCIL'):
				iValue = 500
		elif eCivic == gc.getInfoTypeForString('CIVIC_UNDERCOUNCIL'):
				iValue = 500

		return iValue

	def AI_CivicValue_Special(self, ePlayer, eCivic):
		pPlayer = gc.getPlayer(ePlayer)
		eCiv = pPlayer.getCivilizationType()
		eAlignment = pPlayer.getAlignment()
		iValue = 2

		if eCivic == gc.getInfoTypeForString('CIVIC_CRUSADE'):
			iValue = 15000

		elif eCivic == gc.getInfoTypeForString('CIVIC_SUMMER_COURT'):
			iValue = 5000
			# Switch back to summer court after building Winter Restoration if we lose too much population or we need more techs for eternal court
			iTechInfo = gc.getCivicInfo(gc.getInfoTypeForString('CIVIC_ETERNAL_COURT')).getTechPrereq()
			if pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_FAERIE_COURT')) == gc.getInfoTypeForString('CIVIC_WINTER_COURT') \
				and CyGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_WINTER_RESTORATION')) > 0 \
				and (pPlayer.getTotalPopulation() < 18 or (not pPlayer.isHasTech(iTechInfo) and not pPlayer.isHasTech(gc.getTechInfo(iTechInfo).getPrereqOrTechs(0)))):

				iValue = 10000

		elif eCivic == gc.getInfoTypeForString('CIVIC_WINTER_COURT'):
			if pPlayer.getTotalPopulation() > 23 and CyGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_SUMMER_RESTORATION')) > 0:
				iValue = 10000
			elif CyGame().getProjectCreatedCount(gc.getInfoTypeForString('PROJECT_WINTER_RESTORATION')) > 0 and pPlayer.getTotalPopulation() >= 18:
				iValue = 10000
			else:
				iValue = 0

		elif eCivic == gc.getInfoTypeForString('CIVIC_ETERNAL_COURT'):
			iValue = 18000

		return iValue

	def countTilesToTransform(self, ePlayer):
		pPlayer = gc.getPlayer(ePlayer)
		eCiv = pPlayer.getCivilizationType()

		# Preservation is not necessary for these civs
		if eCiv == gc.getInfoTypeForString('CIVILIZATION_FAERIES') or eCiv == gc.getInfoTypeForString('CIVILIZATION_MALAKIM') \
			or eCiv == gc.getInfoTypeForString('CIVILIZATION_ILLIANS') or eCiv == gc.getInfoTypeForString('CIVILIZATION_INFERNAL') \
			or eCiv == gc.getInfoTypeForString('CIVILIZATION_FROZEN'):
			return 0

		iTiles = 0

		for i in range (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			if pPlot.getOwner() == ePlayer:
				iFeature = pPlot.getFeatureType()
				iTerrain = pPlot.getTerrainType()
				if(iTerrain == gc.getInfoTypeForString('TERRAIN_DESERT') and iFeature != gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS')) \
					or iTerrain == gc.getInfoTypeForString('TERRAIN_SNOW'):
					iTiles += 1

		return iTiles

	def percentageOfUnhealthyCities(self, ePlayer):
		py = PyPlayer(ePlayer)
		pPlayer = gc.getPlayer(ePlayer)

		unhealthyCities = 0
		totalCities = py.getNumCities()

		bShaman = False
		if pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_GOVERNMENT')) == gc.getInfoTypeForString('CIVIC_SHAMANISM'):
			bShaman = True

		for pyCity in py.getCityList():
			pCity = pyCity.GetCy()
			health = pCity.goodHealth() - pCity.badHealth(True)
			if bShaman:
				health -= 3
			if health < 0:
				if pCity.AI_stopGrowth():
					unhealthyCities += 0.5
				else:
					unhealthyCities += 1

		return unhealthyCities / float(max(1,totalCities))

	def	AI_ChoosePromotionSpecialization(self, argsList):
		pUnit = argsList[0]
		iGroupflag= pUnit.AI_getGroupflag()
		iUnitAI=pUnit.getUnitAIType()
		iUnitType=pUnit.getUnitType()
		iUnitCombatType=pUnit.getUnitCombatType()
		pPlot = pUnit.plot()

		#Naval Unit
		if iUnitCombatType==gc.getInfoTypeForString('UNITCOMBAT_NAVAL'):
			pUnit.AI_setPromotionSpecialization(gc.getInfoTypeForString('AIPROMOTIONSPECIALIZATION_UNITCOMBAT_NAVAL_GENERAL'))
			return 0

		#BarBarian Units
		if pUnit.isBarbarian():
			if pUnit.isAnimal():
				pUnit.AI_setPromotionSpecialization(gc.getInfoTypeForString('AIPROMOTIONSPECIALIZATION_ANIMAL'))
				return 0
			if iUnitAI==gc.getInfoTypeForString('UNITAI_ATTACK_CITY'):
				pUnit.AI_setPromotionSpecialization(gc.getInfoTypeForString('AIPROMOTIONSPECIALIZATION_BARBARIAN_CITY_ATTACK'))
				return 0
			pUnit.AI_setPromotionSpecialization(gc.getInfoTypeForString('AIPROMOTIONSPECIALIZATION_BARBARIAN_ATTACK'))
			return 0

		#Hero Unit?
		if iUnitAI==gc.getInfoTypeForString('UNITAI_HERO'):
			if iUnitType==gc.getInfoTypeForString('UNIT_BARNAXUS'):
				pUnit.AI_setPromotionSpecialization(gc.getInfoTypeForString('AIPROMOTIONSPECIALIZATION_HERO_BARNAXUS'))
				return 0
			if not pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CHANNELING3')):
				if pUnit.baseCombatStr()<8:
					pUnit.AI_setPromotionSpecialization(gc.getInfoTypeForString('AIPROMOTIONSPECIALIZATION_UNITAI_HERO'))
					return 0
				else:
					pUnit.AI_setPromotionSpecialization(gc.getInfoTypeForString('AIPROMOTIONSPECIALIZATION_UNITAI_HERO_LATEGAME'))
					return 0

		#Missionary
		if iUnitAI==gc.getInfoTypeForString('UNITAI_MISSIONARY'):
			pUnit.AI_setPromotionSpecialization(gc.getInfoTypeForString('AIPROMOTIONSPECIALIZATION_UNITAI_MISSIONARY'))
			return 0

		#Inquisition Units
		if iGroupflag==15:
			pUnit.AI_setPromotionSpecialization(gc.getInfoTypeForString('AIPROMOTIONSPECIALIZATION_INQUISITION'))
			return 0

		#Pillage Units
		if iGroupflag==16:
			pUnit.AI_setPromotionSpecialization(gc.getInfoTypeForString('AIPROMOTIONSPECIALIZATION_PILLAGE'))
			return 0

#		pUnit.AI_setPromotionSpecialization(gc.getInfoTypeForString('AIPROMOTIONSPECIALIZATION_PERMDEFENSE_GENERAL'))

		return 0

	def Revolution(self, argsList):
		ePlayer=argsList[0]
		eCorporation=argsList[1]
		pPlayer = gc.getPlayer(ePlayer)
		pFromPlayer = gc.getPlayer(ePlayer)

		#Faction System

		iKUNDARAK=gc.getInfoTypeForString('CORPORATION_HOUSE_KUNDARAK')
		iTHARASHK=gc.getInfoTypeForString('CORPORATION_HOUSE_THARASHK')
		iCANNITH=gc.getInfoTypeForString('CORPORATION_HOUSE_CANNITH')
		iPHIARLAN=gc.getInfoTypeForString('CORPORATION_HOUSE_PHIARLAN')
		iGHALLANDA=gc.getInfoTypeForString('CORPORATION_HOUSE_GHALLANDA')
		iVADALIS=gc.getInfoTypeForString('CORPORATION_HOUSE_VADALIS')

		iLYRANDAR=gc.getInfoTypeForString('CORPORATION_HOUSE_LYRANDAR')
		iTHURANNI=gc.getInfoTypeForString('CORPORATION_HOUSE_THURANNI')
		iGUILDNINE=gc.getInfoTypeForString('CORPORATION_GUILD_OF_THE_NINE')

		iNewLeader=-1

		if eCorporation==iLYRANDAR or eCorporation==iVADALIS or eCorporation==iTHARASHK:
			iNewLeader = gc.getInfoTypeForString('LEADER_PROTECTOR')

		if eCorporation==iKUNDARAK or eCorporation==iGHALLANDA or eCorporation==iGUILDNINE:
			iNewLeader = gc.getInfoTypeForString('LEADER_TRADER')

		if eCorporation==iTHURANNI or eCorporation==iCANNITH or eCorporation==iPHIARLAN:
			iNewLeader = gc.getInfoTypeForString('LEADER_RISEN')

		#look for a City
		if pPlayer.getNumCities<2:
			return 0

		pBestCity = -1
		iBestValue = 0
		iValue = 0

		for pyCity in PyPlayer(ePlayer).getCityList():
			pCity = pyCity.GetCy()

			iValue=0
			iValue+=CyGame().getSorenRandNum(100, "viva la revolution")
			iValue*=20+pCity.getPopulation()

			if pCity.isHasBuilding(gc.getInfoTypeForString('BUILDING_COURTHOUSE')):
				iValue /=2

			if pCity.isHasCorporation(eCorporation):
				iValue *=2

			if pCity.isCapital():
				iValue-=5000

			if iValue>iBestValue:
				pBestCity=pCity
				iBestValue=iValue

		if pBestCity==-1:
			return

		#City found, Remove it's defense

		pCity = pBestCity
		pPlot = pCity.plot()
		pPlot2 = cf.findClearPlot(-1, pCity.plot())
		if (pPlot2 != -1):
			for i in range(pPlot.getNumUnits(), -1, -1):
				pUnit = pPlot.getUnit(i)
				pUnit.setXY(pPlot2.getX(), pPlot2.getY(), true, true, true)

			#Do we need a new Player or join an existing Player?
			pExistingPlayer = -1

			for iPlayer2 in range(gc.getMAX_PLAYERS()):
				pPlayer2 = gc.getPlayer(iPlayer2)
				if (pPlayer2.isAlive()):
					if pPlayer2.getLeaderType()==iNewLeader:
						pExistingPlayer = pPlayer2

			if pExistingPlayer==-1:
				iPlayer = cf.getOpenPlayer()
				CyGame().addPlayerAdvanced(iPlayer, -1, iNewLeader, pFromPlayer.getCivilizationType())
				pPlayer = gc.getPlayer(iPlayer)
				eTeam = gc.getTeam(pPlayer.getTeam())
				eTeam.setHouseErebus(true)
				eTeam.declareWar(gc.getPlayer(gc.getBARBARIAN_PLAYER()).getTeam(), false, WarPlanTypes.WARPLAN_LIMITED)
				eTeam.declareWar(gc.getPlayer(gc.getANIMAL_PLAYER()).getTeam(), false, WarPlanTypes.WARPLAN_LIMITED)
				eTeam.declareWar(gc.getPlayer(gc.getWILDMANA_PLAYER()).getTeam(), false, WarPlanTypes.WARPLAN_LIMITED)
				eTeam.declareWar(gc.getPlayer(gc.getPIRATES_PLAYER()).getTeam(), false, WarPlanTypes.WARPLAN_LIMITED)
				eTeam.declareWar(gc.getPlayer(gc.getDEVIL_PLAYER()).getTeam(), false, WarPlanTypes.WARPLAN_LIMITED)
			else:
				pPlayer=pExistingPlayer

			iPlayer=pPlayer.getID()
			#Transfer City, Techs
			pPlayer.acquireCity(pCity, False, False)
#			CyInterface().addMessage(pFromPlayer.getID(),true,25,"City %s has revolted and is now under the rule of %s" %(pCity.getName(),pPlayer.getName()),'',0,'',ColorTypes(11), pPlot.getX(), pPlot.getY(), True,True)
			pCity = pPlot.getPlotCity()
			#transfer culture
			isearch=1
			for iiX in range(pCity.getX()-isearch, pCity.getX()+isearch+1, 1):
				for iiY in range(pCity.getY()-isearch, pCity.getY()+isearch+1, 1):
					pPlot2 = CyMap().plot(iiX,iiY)
					if not pPlot2.isNone():
						iCultureTransfer=-pPlot2.getCulture(pFromPlayer.getID())
						pPlot2.changeCulture(pFromPlayer.getID(), iCultureTransfer, false);
						pPlot2.changeCulture(ePlayer, iCultureTransfer, true);


			if pFromPlayer != -1:
				eFromTeam = gc.getTeam(pFromPlayer.getTeam())
				eTeam = gc.getTeam(pPlayer.getTeam())
				for iTech in range(gc.getNumTechInfos()):
					if eFromTeam.isHasTech(iTech):
						eTeam.setHasTech(iTech, true, iPlayer, true, false)

			eTeam = gc.getTeam(pPlayer.getTeam())

			#Give City some Defense
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_BOWYERS')):
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_LONGBOWMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_LONGBOWMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_LONGBOWMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_LONGBOWMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			else:
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARCHER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARCHER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARCHER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARCHER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

			pPlayer.initUnit(gc.getInfoTypeForString('UNIT_WORKER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

			#Improve Relation with Noble House
			pFromPlayer.changeCorporationSupport(eCorporation,4000)

			iPlayer=ePlayer

			if gc.getPlayer(iPlayer).isHuman():
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_CONTROL_HOUSE_GHALLANDA",()))
				popupInfo.setData1(iPlayer)
				popupInfo.setData2(pPlayer.getID())
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_YES", ()), "")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_NO", ()), "")
				popupInfo.setOnClickedPythonCallback("reassignPlayer")
				popupInfo.addPopup(iPlayer)

	# return 1 if a Lair has been Created
	def CorporationOffersSupport(self, argsList):
		iPlayer=argsList[0]
		eCorporation=argsList[1]

		pPlayer=gc.getPlayer(iPlayer)

		iKUNDARAK=gc.getInfoTypeForString('CORPORATION_HOUSE_KUNDARAK')
		iTHARASHK=gc.getInfoTypeForString('CORPORATION_HOUSE_THARASHK')
		iCANNITH=gc.getInfoTypeForString('CORPORATION_HOUSE_CANNITH')
		iPHIARLAN=gc.getInfoTypeForString('CORPORATION_HOUSE_PHIARLAN')
		iGHALLANDA=gc.getInfoTypeForString('CORPORATION_HOUSE_GHALLANDA')
		iVADALIS=gc.getInfoTypeForString('CORPORATION_HOUSE_VADALIS')

#		iLYRANDAR=gc.getInfoTypeForString('CORPORATION_HOUSE_LYRANDAR')
#		iTHURANNI=gc.getInfoTypeForString('CORPORATION_HOUSE_THURANNI')
#		iGUILDNINE=gc.getInfoTypeForString('CORPORATION_GUILD_OF_THE_NINE')

		if eCorporation==iKUNDARAK:
			iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_HOUSE_KUNDARAK')
			triggerData = gc.getPlayer(iPlayer).initTriggeredData(iEvent, true, -1, pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), iPlayer, -1, -1, -1, -1, -1)
		if eCorporation==iTHARASHK:
			iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_HOUSE_THARASHK')
			triggerData = gc.getPlayer(iPlayer).initTriggeredData(iEvent, true, -1, pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), iPlayer, -1, -1, -1, -1, -1)
		if eCorporation==iCANNITH:
			iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_HOUSE_CANNITH')
			triggerData = gc.getPlayer(iPlayer).initTriggeredData(iEvent, true, -1, pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), iPlayer, -1, -1, -1, -1, -1)
		if eCorporation==iPHIARLAN:
			iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_HOUSE_PHIARLAN')
			triggerData = gc.getPlayer(iPlayer).initTriggeredData(iEvent, true, -1, pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), iPlayer, -1, -1, -1, -1, -1)
		if eCorporation==iGHALLANDA:
			iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_HOUSE_GHALLANDA')
			triggerData = gc.getPlayer(iPlayer).initTriggeredData(iEvent, true, -1, pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), iPlayer, -1, -1, -1, -1, -1)
		if eCorporation==iVADALIS:
			iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_HOUSE_VADALIS')
			triggerData = gc.getPlayer(iPlayer).initTriggeredData(iEvent, true, -1, pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), iPlayer, -1, -1, -1, -1, -1)
#		if eCorporation==iGUILDNINE:
#			iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_GUILD_OF_THE_NINE')
#			triggerData = gc.getPlayer(iPlayer).initTriggeredData(iEvent, true, -1, pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), iPlayer, -1, -1, -1, -1, -1)
#		if eCorporation==iLYRANDAR:
#			iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_HOUSE_LYRANDAR')
#			triggerData = gc.getPlayer(iPlayer).initTriggeredData(iEvent, true, -1, pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), iPlayer, -1, -1, -1, -1, -1)
#		if eCorporation==iTHURANNI:
#			iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_HOUSE_THURANNI')
#			triggerData = gc.getPlayer(iPlayer).initTriggeredData(iEvent, true, -1, pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), iPlayer, -1, -1, -1, -1, -1)

		return 0

	def AdventureFinished(self, argsList):
		iPlayer=argsList[0]
		iAdventure=argsList[1]
		pPlayer=gc.getPlayer(iPlayer)
		if gc.getAdventureInfo(iAdventure).isVictory():
			if not pPlayer.getCapitalCity().isNone():
				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ADVENTURER'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.UNITAI_HERO, DirectionTypes.DIRECTION_SOUTH)
				CyInterface().addMessage(iPlayer,true,25,"You finished the '%s' Quest and an Adventurer joined your cause!" %(gc.getAdventureInfo(iAdventure).getDescription()),'',0,'',ColorTypes(11), newUnit.getX(), newUnit.getY(), True,True)
			bValid=false
			for i in range(gc.getNumAdventureInfos()):
				if pPlayer.isAdventureEnabled(i):
					if gc.getAdventureInfo(i).isVictory():
						if pPlayer.isAdventureFinished(i):
							bValid=true
						else:
							bValid=false
							break
			if bValid:
				pPlayer.changeGoldenAgeTurns(10000)

	def Trigger_MagicScreenPopup(self, argsList):
		screen = CyGInterfaceScreen( "MagicScreen", CvScreenEnums.MAGIC_SCREEN )
		screen.setRenderInterfaceOnly(True)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, True)

	def Trigger_GuildScreenPopup(self, argsList):
		screen = CyGInterfaceScreen( "GuildScreen", CvScreenEnums.GUILD_SCREEN )
		screen.setRenderInterfaceOnly(True)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, True)

	def Trigger_GuildScreenPopupEnd(self, argsList):
		screen = CyGInterfaceScreen( "GuildScreen", CvScreenEnums.GUILD_SCREEN )
		screen.setRenderInterfaceOnly(True)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

	def Trigger_MagicScreenPopupEnd(self, argsList):
		screen = CyGInterfaceScreen( "MagicScreen", CvScreenEnums.MAGIC_SCREEN )
		screen.setRenderInterfaceOnly(True)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

#return 0 if City cannot have religion
	def canCityHaveReligion(self, argsList):
		eReligion=argsList[0]
		eCivilization=argsList[1]

		if eCivilization==gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
			if eReligion==gc.getInfoTypeForString('RELIGION_THE_ORDER'):
				return 0

		elif eCivilization==gc.getInfoTypeForString('CIVILIZATION_MERCURIANS'):
			if eReligion==gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
				return 0

		elif eCivilization==gc.getInfoTypeForString('CIVILIZATION_FROZEN'):
			return 0

	def CalculateCivCounter(self, argsList):
		iPlayer=argsList[0]
		pPlayer=gc.getPlayer(iPlayer)
		iStep=argsList[1]
		iValue=argsList[2]

		if pPlayer.getCivilizationType()==gc.getInfoTypeForString('CIVILIZATION_ELOHIM'):
			if iStep==0:
				#Purity From Buildings
				iPurity=pPlayer.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_ABBEY'))*500
				iPurity+=pPlayer.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_PAGAN_TEMPLE'))*200
				iPurity+=pPlayer.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_CIV_BUILDING1'))*100
				iPurity+=pPlayer.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_MINSTER'))*2000
				return iPurity
			elif iStep==1:
				#Bonus From Mana
				iManaMod=5*pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_LIFE'))
				if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_LIFE')) > 0:
					iManaMod+=10
				return iManaMod
			elif iStep==2:
				#Pacifism Civic Bonus
				if pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_CULTURAL_VALUES')) == gc.getInfoTypeForString('CIVIC_PACIFISM'):
					return 30
				else:
					return 0
			elif iStep==3:
				#Unique features Modifier
				itemp=0
				for i in range(0,CyMap().numPlots(),1):
					pPlot = CyMap().plotByIndex(i)
					if pPlot.getOwner()==iPlayer:
						if pPlot.getImprovementType() != -1:
							if gc.getImprovementInfo(pPlot.getImprovementType()).isUnique():
								itemp+=10
				return itemp
			elif iStep==4:
				#State Religion Modifier
				if pPlayer.getStateReligion()==gc.getInfoTypeForString('RELIGION_THE_ORDER') or pPlayer.getStateReligion()==gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
					return 100
				if pPlayer.getStateReligion()==gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH'):
					return 50
				return 0
			elif iStep==5:
				#Value from UF sealed
				return pPlayer.getPurityCounterCache1()

		if pPlayer.getCivilizationType()==gc.getInfoTypeForString('CIVILIZATION_SIDAR'):
			if iStep==0:
				iValue=0
				py = PyPlayer(iPlayer)
				for pUnit in py.getUnitList():
					if pUnit.getExperience()>20:
						if gc.getUnitInfo(pUnit.getUnitType()).getTier()>1:
							iValue+=5
				return iValue

			elif iStep==1:
				return 10+pPlayer.getNumCities()*10

		return 0

	def NetMessage_SendTerraformPlan(self, argsList):
		iPlayer=argsList[0]
		iProject=argsList[1]

		CyMessageControl( ).sendModNetMessage(CvUtil.TerraformPlan, iPlayer, iProject, 0, 0)
