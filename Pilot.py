class Pilot:
    def __init__(self, ship, ability, upgrades, initiative):
        self.ship = ship
        self.ability = ability
        self.upgrades = upgrades
        self.hasInitiative = initiative

    def updateState(self, combatState):

        combatState = self.ability.apply(combatState)
        # Iteratively apply upgrades
        for upgrade in self.upgrades:
            combatState = upgrade.apply(combatState)
        return combatState

    def resolveDamage(self, numHits, numCrits):
        return None
