import sys
from sys import argv

# The Bayesian network is represented by the class `bayesian`.
class bayesian(object):

# The function `init` is used to initialize the values of the bayesian network.
    def init(self, values):
        total_p = self.assignProbabilty("B", values[0], None, None) * self.assignProbabilty("E", values[1], None, None) * \
                self.assignProbabilty("A|B,E", values[2], values[0], values[1]) * \
                self.assignProbabilty("J|A", values[3], values[2], None) * \
                self.assignProbabilty("M|A", values[4], values[2], None)
        return total_p

# Function to generate the possible combinations.   
    def variable_elimination(self, values):
        if None not in values:
            return self.init(values)
        none_index = values.index(None)
        true_values = values.copy()
        true_values[none_index] = True
        false_values = values.copy()
        false_values[none_index] = False 
        return self.variable_elimination(true_values) + self.variable_elimination(false_values)

# Assigning the probs from bayesian network.
    def assignProbabilty(self, Node, Node_value, parent_1_value, parent_2_value):
        if Node == "A|B,E":
            if parent_1_value:
                if parent_2_value:
                    prob = 0.95
                if not parent_2_value:
                    prob = 0.94
            if not parent_1_value:
                if parent_2_value:
                    prob = 0.29
                if not parent_2_value:
                    prob = 0.001
            return prob if Node_value else (1 - prob)
        elif Node == "B":
            return 0.001 if Node_value else 0.999
        elif Node == "E":
            return 0.002 if Node_value else 0.998
        elif Node == "J|A":
            prob = 0.9 if parent_1_value else 0.05
            return prob if Node_value else (1 - prob)
        elif Node == "M|A":
            prob = 0.7 if parent_1_value else 0.01
            return prob if Node_value else (1 - prob)

# Storing or Collecting true or false.
    def true_false(self, value):
        result = []
        if "Bt" in value:
            result.append(True)
        elif "Bf" in value:
            result.append(False)
        else:
            result.append(None)
        if "Et" in value:
            result.append(True)
        elif "Ef" in value:
            result.append(False)
        else:
            result.append(None)
        if "At" in value:
            result.append(True)
        elif "Af" in value:
            result.append(False)
        else:
            result.append(None)
        if "Jt" in value:
            result.append(True)
        elif "Jf" in value:
            result.append(False)
        else:
            result.append(None)
        if "Mt" in value:
            result.append(True)
        elif "Mf" in value:
            result.append(False)
        else:
            result.append(None)

        return result
    

if __name__ == "__main__":

    # Check if the number of arguments is correct
    if len(sys.argv) < 1 or len(sys.argv) > 6:
        print ("Invalid number of arguments!!/n Arguments must be atleast 2 and not more than 6")
        sys.exit(1)

    argv = sys.argv[1:]
    givenValue = False
    C_prob = [] # Stores all values after 'given'
    J_prob = [] # Stores all values ahead of 'given'
    bnet = bayesian()
    for i in argv:
            if i == "given":
                    givenValue = True
            J_prob.append(i)
            if givenValue:
                    C_prob.append(i)

    if J_prob:
        Joint_prob = bnet.variable_elimination(bnet.true_false(J_prob))
        if C_prob:
            evidence_prob = bnet.variable_elimination(bnet.true_false(C_prob))
        else:
            evidence_prob = 1
        print ("The probability is : %.10f" % (Joint_prob/evidence_prob))
    else:
        print ("Invalid query string")
    
    