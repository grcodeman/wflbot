import random, math

# list of height options and odds for Tiny, Normal and Giant archetype

ARCH = ['tiny', 'normal', 'giant']
ARCH_ODDS = [1,1,1]

T_LIST = [65,66,67,68,69,70]
N_LIST = [69,70,71,72,73,74]
G_LIST = [73,74,75,76,77,78]

T_ODDS = [10,25,30,25,5,5]
N_ODDS = [20,25,25,20,5,5]
G_ODDS = [25,30,25,10,5,5]

def roll_height (arch):
    height = -1
    rand_pos = ""
    rand_arch = ""

    # if the user rolls a random
    if (arch == "random"):
        arch = str(random.choices(ARCH, weights=ARCH_ODDS, k=1)[0])
        rand_arch = "Random:"

    # roll base value based on archetype
    if (arch == "tiny"):
        height = random.choices(T_LIST, weights=T_ODDS, k=1)
    elif (arch == "normal"):
        height = random.choices(N_LIST, weights=N_ODDS, k=1)
    elif (arch == "giant"):
        height = random.choices(G_LIST, weights=G_ODDS, k=1)

    # prepare final inch amount, then height
    result = rand_arch + arch.capitalize() + " - " + str(math.floor(height[0] / 12)) + "\'" + str(height[0] % 12)
    return result

print(roll_height("random"))