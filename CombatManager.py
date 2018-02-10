from DiceManager import DiceManager


class CombatManager:

    def __init__(self):
        # Initialize dice manager
        self.diceManager = DiceManager()
        # Initialize combat staticmethod
        self.combatState = None
        # Set default values
        self.numBaseRedDice = 0
        self.numBaseGreenDice = 0
        self.attacker = None
        self.defender = None
        self.baseRange = 1
        self.numHits = 0
        self.numCrits = 0
        self.states = [self.setNumberOfRedDice, self.rollAttackDice,
                       self.modifyAttackDice, self.setNumberOfGreenDice,
                       self.rollDefenseDice, self.modifyDefenseDice,
                       self.resolveHits, self.afterCombatNoAttack,
                       self.afterCombatAttack]
        self.currentState = 0
        self.initiative = None

    def initialize(self, numBaseRedDice, numBaseGreenDice, attacker, defender, baseRange):

        self.numBaseRedDice = attacker.attack
        self.numBaseGreenDice = defender.agility
        self.attacker = attacker
        self.defender = defender
        self.baseRange = baseRange
        self.currentState = 0
        self.combatState = CombatState()
        if self.attacker.hasInitiative:
            self.initiative = [attacker, defender]
        else:
            self.initiative = [defender, attacker]

    def updateState(self, attackerFirst):
        if attackerFirst is None:
            for ship in self.initiative:
                self.combatState = ship.updateState(self.combatState)
        elif attackerFirst:
            self.combatState = self.attacker.updateState(self.combatState)
            self.combatState = self.defender.updateState(self.combatState)
        else:
            self.combatState = self.defender.updateState(self.combatState)
            self.combatState = self.attacker.updateState(self.combatState)

    def performCombat(self):
        for stateNum, stateFun in enumerate(self.states):
            self.currentState = stateNum
            resolveOrder = stateFun()
            self.updateState(resolveOrder)

    def setNumberOfRedDice(self):
        # modify number of red dice based on combat range
        if self.baseRange == 1:
            self.combatState.numRedDice = self.numBaseRedDice + 1
        return None

    def rollAttackDice(self):
        self.combatState.redRolls = self.diceManager.rollRed(self.combatState.numRedDice)
        return None

    def modifyAttackDice(self):
        # Resolve defender abilities, then resolve attacker abilities, then apply attacker tokens
        return False

    def setNumberOfGreenDice(self):
        # modify number of green dice based on combat range
        if self.baseRange == 3:
            self.combatState.numGreenDice = self.numBaseGreenDice + 1
        return None

    def rollDefenseDice(self):
        self.combatState.greenRolls = self.diceManager.rollGreen(self.combatState.numGreenDice)
        return None

    def modifyDefenseDice(self):
        # Resolve attacker abilities, then resolve defender abilities, then apply defender tokens
        return True

    def resolveHits(self):
        numHits = sum(roll == 'h' for roll in self.combatState.redRolls)
        numCrits = sum(roll == 'c' for roll in self.combatState.redRolls)
        numEvades = sum(roll == 'e' for roll in self.combatState.greenRolls)
        # Evade hits, then credits
        numHits = numHits - numEvades
        if numHits < 0:
            # Apply remaining evades to the crit count
            numCrits = numCrits + numHits
            numHits = 0
        if numCrits < 0:
            numCrits = 0
        # Store for future reference (debugging?)
        self.numHits = numHits
        self.numCrits = numCrits
        # Resolve damage to the defender
        self.defender.resolveDamage(numHits, numCrits)
        return None

    def afterCombatNoAttack(self):
        # Resolve abilities that occur after combat that don't perform an attack in initative order
        return None

    def afterCombatAttack(self):
        # Resolve abilities that occur after combat that perform an attack in initiative order
        return None


class CombatState:

    def __init__(self):
        self.numRedDice = 0
        self.numGreenDice = 0
        self.redRolls = None
        self.greenRolls = None
