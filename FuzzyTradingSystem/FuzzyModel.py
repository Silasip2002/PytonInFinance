import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl
import pandas as pd

class OurFuzzy:

    def __init__(self,Gposition=0.3,Gsigma = 0.3):
        self.Gposition = Gposition;
        self.Gsigma = Gsigma;
        self.max = 1.0
        self.min = 0.0
        self.high = 0.6
        self.low = 0.4

    def fuzzyOut(self,userInput1,userInput2,userInput3):  #for a row input result
        # 1. New Antecedent/Consequent objects hold universe variables & membership
        # functions
        #input = ctrl.Antecedent(the range of the value (min, max , interval), "the name of the input")
        firstInput = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'firstInput') #set the input value  the value
        secondInput = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'secondInput') #set the input value
        thirInput = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'thirInput') #set the inpu
        fuzzyOut = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'fuzzyOut') #set the out put value

        #2.set membership functions for inputs & output.
        #declear the fuzzy term
        firstInput['buy'] = fuzz.zmf(firstInput.universe,self.min,self.high)
        firstInput['neutral'] = fuzz.gaussmf(firstInput.universe,self.Gposition,self.Gsigma)
        firstInput['sell'] = fuzz.smf(firstInput.universe,self.low,self.max)

        secondInput['buy'] = fuzz.zmf(firstInput.universe,self.min,self.high)
        secondInput['neutral'] = fuzz.gaussmf(firstInput.universe,self.Gposition,self.Gsigma)
        secondInput['sell'] = fuzz.smf(firstInput.universe,self.low,self.max)

        thirInput['buy'] = fuzz.zmf(firstInput.universe,self.min,self.high)
        thirInput['neutral'] = fuzz.gaussmf(firstInput.universe,self.Gposition,self.Gsigma)
        thirInput['sell'] = fuzz.smf(firstInput.universe,self.low,self.max)

        fuzzyOut['buy'] = fuzz.zmf(firstInput.universe,self.min,self.high)
        fuzzyOut['neutral'] = fuzz.gaussmf(firstInput.universe,self.Gposition,self.Gsigma)
        fuzzyOut['sell'] = fuzz.smf(firstInput.universe,self.low,self.max)


        #3.set fuzzy rules let the memberhship function be useful.
        rule1 = ctrl.Rule(firstInput['buy'] & secondInput['buy'] & thirInput['buy'],fuzzyOut['buy'])
        rule2 = ctrl.Rule(firstInput['sell'] & secondInput['sell'] & thirInput['sell'],fuzzyOut['sell'])
        rule3 = ctrl.Rule(firstInput['neutral'] & secondInput['neutral'] & thirInput['neutral'],fuzzyOut['neutral'])

        rule4 = ctrl.Rule(firstInput['buy'] & secondInput['sell'] & thirInput['buy'],fuzzyOut['neutral'])
        rule5 = ctrl.Rule(firstInput['sell'] & secondInput['sell'] & thirInput['buy'],fuzzyOut['neutral'])
        rule6 = ctrl.Rule(firstInput['buy'] & secondInput['buy'] & thirInput['sell'],fuzzyOut['neutral'])

        rule7 = ctrl.Rule(firstInput['buy'] & secondInput['buy'] & thirInput['neutral'],fuzzyOut['buy'])
        rule8 = ctrl.Rule(firstInput['sell'] & secondInput['sell'] & thirInput['neutral'],fuzzyOut['sell'])
        rule9 = ctrl.Rule(firstInput['buy'] & secondInput['buy'] & thirInput['sell'],fuzzyOut['neutral'])

        rule10 = ctrl.Rule(firstInput['buy'] & secondInput['neutral'] & thirInput['buy'],fuzzyOut['buy'])
        rule11 = ctrl.Rule(firstInput['sell'] & secondInput['neutral'] & thirInput['sell'],fuzzyOut['sell'])
        rule12 = ctrl.Rule(firstInput['neutral'] & secondInput['sell'] & thirInput['sell'],fuzzyOut['sell'])

        #4 adding the rule into the control system
        fuzzyOut_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4,rule5,rule6,rule7,rule8,rule9,rule10,rule11,rule12])
        #Calculate results from a ControlSystem base on the  different cirucmstancses.
        fuzzySignal = ctrl.ControlSystemSimulation(fuzzyOut_ctrl) #put the controller into the simulation.

        #5. Now the fuzzy system is done. we can enter the input,& get the output.
        #remake before using the userInput, must change the inputvalune into the 0.0 to 1.0 range.
        fuzzySignal.input['firstInput'] = userInput1
        fuzzySignal.input['secondInput'] = userInput2
        fuzzySignal.input['thirInput'] = userInput3
        fuzzySignal.compute()

        #6.Check the result of output & visualize it.
        #print (fuzzySignal.output['fuzzyOut'])
        #print(type(fuzzyOut.view(sim=fuzzySignal)))


        return fuzzySignal.output['fuzzyOut']

