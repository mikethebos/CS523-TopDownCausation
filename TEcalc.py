from jpype import *
import numpy
import readIntsFile
import sys
# Our python data file readers are a bit of a hack
sys.path.append("C:\\Users\\cathe\\Documents\\CS523\\infodynamics-dist-1.4\\demos\\python")


# Add JIDT jar library to the path
jarLocation = "C:\\Users\\cathe\\Documents\\CS523\\infodynamics-dist-1.4\\infodynamics.jar"
# Start the JVM (add the "-Xmx" option with say 1024M if you get crashes due to not enough memory space)
startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + jarLocation)

# 0. Load/prepare the data:
dataRaw = readIntsFile.readIntsFile("C:\\Users\\cathe\\Documents\\CS523\\CS523-TopDownCausation\\TEdata\\MX_0_0.csv")
# As numpy array:
data = numpy.array(dataRaw)
source = JArray(JInt, 1)(data[:,0].tolist())
destination = JArray(JInt, 1)(data[:,1].tolist())

# 1. Construct the calculator:
calcClass = JPackage("infodynamics.measures.discrete").TransferEntropyCalculatorDiscrete
calc = calcClass(101, 2, 1, 1, 1, 1)
# 2. No other properties to set for discrete calculators.
# 3. Initialise the calculator for (re-)use:
calc.initialise()
# 4. Supply the sample data:
calc.addObservations(source, destination)
# 5. Compute the estimate:
result = calc.computeAverageLocalOfObservations()

print("TE_Discrete(col_0 -> col_1) = %.4f bits" %
    (result))