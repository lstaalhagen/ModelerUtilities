import sys
import re

processmodelname = sys.argv[1].split(".")[0]

with open(sys.argv[1]) as f:
    lines = f.readlines()
# print("Read {} lines from {}".format(len(lines), sys.argv[1]))

# Strip newlines
sourcelines = list()
for l in lines:
    sourcelines.append(l.rstrip())

# Step 1 - Get defines from the header block
HeaderBlock = list()
HeaderBlockDefines = dict()
inHeaderBlock = False
for line in sourcelines:
    if line == "/* End of Header Block */":
        break
    if line == "/* Header Block */":
        inHeaderBlock = True
        continue
    if inHeaderBlock and len(line)>0:
        HeaderBlock.append(line)
        tokens = line.split()
        if tokens[0] == "#define":
            HeaderBlockDefines[tokens[1]] = " ".join(tokens[2:])

# Step 2 - Get a list of state variables
state = 0
StateVariables = dict()
for line in lines:
    line2 = line.strip()
    if state == 0 and line2 == "/* State variable definitions */":
        state = 1
        continue
    if state == 1 and line2 == "typedef struct":
        state = 2
        continue
    if state == 2 and line2 == "{":
        state = 3
        continue
    if state == 3 and line2 == "/* Internal state tracking for FSM */":
        state = 4
        continue
    if state == 4 and line2 == "FSM_SYS_STATE":
        state = 5
        continue
    if state == 5 and line2 == "/* State Variables */":
        state = 6
        continue
    if state == 6 and line2.startswith("}") == False:
        sv = line2.split()
        if sv[1] != "*":
            StateVariables[sv[1]] = sv[0]
        else:
            StateVariables[sv[2]] = " ".join(sv[:2])
    if state == 6 and line2.startswith("}") == True:
        state = 7
        continue

# print(StateVariables)

state = 0
codeblocks = list()
for line in lines:

    if re.search("^.* \(OP_SIM_CONTEXT_ARG_OPT\)", line):
        state = 1
        continue

    if state == 1 and re.match("^\t\{", line):
        state = 2
        continue

    if state == 2:
        if re.match("^\t\}", line):
            break
        else:
            if line.startswith("#"):
                continue
            codeblocks.append(line.strip())

# print(codeblocks)

state = 0
statenames = list()
allstates = dict()
for cl in codeblocks:

    if state == 1 and re.search("\/\*\* state \(.*\) (enter executives|exit executives|transition processing) \*\*\/", cl):
        statenames.append(basestatename)

        # Strip 
        while len(codelines)>0 and len(codelines[-1])==0:
            del codelines[-1]
        if len(codelines)>0:
            if codelines[0] == '{':
                del codelines[0]
            if codelines[-1] == '}':
                del codelines[-1]

        allstates[statename] = codelines
        state = 0

    if state == 0 and re.search("\/\*\* state \(.*\) (enter executives|exit executives|transition processing) \*\*\/", cl):
        basestatename = re.search("\(.*\)", cl).group(0)[1:-1]
        statename = basestatename + " (" + re.search("(enter executives|exit executives|transition processing)", cl).group(0) + ")"
        state = 1
        codelines = list()
        continue
    
    if state == 1:
        if not cl.startswith("FSM_"):
            codelines.append(cl)


# Check for name-clash between HB defines and state variables
for hbdef in HeaderBlockDefines.keys():
    if hbdef in StateVariables.keys():
        print("Error: Definition of {} in Header Block also used as state variable".format(hbdef))

# Check for name-clash between state and state variable
for sv in StateVariables.keys():
    if sv in statenames:
        print("Error: State variable {} is also the name of a state".format(sv))

for key in allstates.keys():
    curlybracecount = 0
    normalbracecount = 0
    for l in allstates[key]:
        curlybracecount += l.count('{') - l.count('}')
        normalbracecount += l.count('(') - l.count(')')
    
    if curlybracecount != 0 or normalbracecount != 0:
        print("Error in {} : ".format(key), end = '')
        if curlybracecount != 0:
            print("Mismatched curly braces - ", end = '')
            if curlybracecount > 0:
                print("too many '{' or too few '}'")
            else:
                print("too few '{' or too many '}'")
        if normalbracecount != 0:
            print("Mismatched normal braces - ", end = '')
            if normalbracecount > 0:
                print("too many '(' or too few ')'")
            else:
                print("too few '(' or too many ')'")
        


