import time
import copy

import numpy as np

import Network
import Label


# Defining the function that checks if a label is feasible
def resourceFeasible(label, wTime, wInco):
    resource_feasible = False
    if label.time <= wTime and label.inco <= wInco:
        resource_feasible = True

    # # check if elementary
    proposed_path_len = len(label.path)
    unique_values = len(set(label.path))
    if proposed_path_len > unique_values:
        # non-elementary
        resource_feasible = False
    # if label.path
    return resource_feasible


# Defining the function that dominates labels. It takes the whole list of labels as an argument and returns a list of dominated labels
def dominate(L):
    dominatedLabels = (
        []
    )  # Initializing a list to save the iterators of dominated labels, i.e., the integer ID of a label

    # Comparing the last added label to the exisiting labels
    lastLabel = len(L) - 1
    lastInPathLastLabel = len(L[lastLabel].path) - 1
    for i in range(len(L) - 1):
        lastInPath = len(L[i].path) - 1
        # We can only dominate a label if the two compared labels have visted the same node as their last visit
        if L[lastLabel].path[lastInPathLastLabel] == L[i].path[lastInPath]:
            # If both labels are equal we dominate the latest added label
            if (
                L[lastLabel].cost == L[i].cost
                and L[lastLabel].time == L[i].time
                and L[lastLabel].inco == L[i].inco
            ):
                L[lastLabel].done = True
                dominatedLabels.append(lastLabel)
                # If the latest added label is dominated we can abort
                break
            elif (
                L[lastLabel].cost <= L[i].cost
                and L[lastLabel].time <= L[i].time
                and L[lastLabel].inco <= L[i].inco
            ):
                # We only register dominance if the label hasn't already been dominated or completed processing
                if L[i].done == False:
                    L[i].done = True
                    dominatedLabels.append(i)
            elif (
                L[lastLabel].cost >= L[i].cost
                and L[lastLabel].time >= L[i].time
                and L[lastLabel].inco >= L[i].inco
            ):
                L[lastLabel].done = True
                dominatedLabels.append(lastLabel)
                break
    return dominatedLabels


# -----------------------------Algorithm starts here--------------------------------------------------------


# Here we read the network from file and initialize the network-data structure
network = Network.Network("data/Network3.txt")

# We use a list to save all labels. Here we initialize the list with the first label having the index 0.
L = [None] * 1
L[0] = Label.Label()  # Creating the first label

# define pair
pair = (10, 19)
# define end node
end_node = network.nNodes


# We introduce an iteration counter to keep track of which label we are currently processing
iter = 0

# We also introduce a counter that counts the number of dominated labels for statistics
numDominated = 0

# A timestamp to record the time used
startTime = time.time()


def check_pair(path):
    return (pair[0] in path and pair[1] in path) or (
        pair[0] not in path and pair[1] not in path
    )


while iter < len(L):

    if (
        L[iter].done == False
    ):  # Processing the label if the current label, L[iter],  is not completed
        for arc in network.arcs:
            # Expanding the label with arcs that start in the node that is last in L[iter].path,
            # i.e., the last visited node in the current label
            if (
                arc[0] == L[iter].path[len(L[iter].path) - 1]
                and arc[1] not in L[iter].path
            ):  #'len(L[iter].path)-1' accesses the last element in the path data structure
                # add check for pair
                if (
                    arc[1] == end_node
                    and check_pair(L[iter].path)
                    or arc[1] != end_node
                ):

                    newLabel = copy.deepcopy(L[iter])  # Initializing the new label
                    newLabel.cost = newLabel.cost + arc[2]
                    newLabel.time = newLabel.time + arc[3]
                    newLabel.inco = newLabel.inco + arc[4]
                    newLabel.path.append(arc[1])

                    # After expanding the new label we check if it is feasible and check if it can be dominated
                    if resourceFeasible(newLabel, network.wTime, network.wInco):
                        # Add the new label at the end of the list of labels
                        L.append(newLabel)
                        dominated = dominate(L)

                        numDominated += len(dominated)
                        # Setting all done = True for all dominated labels so that we avoid expanding these labels
                        for i in dominated:
                            L[i].done = True
    # Mark the current label as processed
    L[iter].done = True
    # Increase the iterator
    iter += 1


endTime = time.time()
runTime = endTime - startTime

# Print results
output = "Number of labels created :\t" + str(len(L))
print(output)
output = "Number of labels dominated :\t" + str(numDominated)
print(output)
output = "The algorithm took :\t" + str(runTime) + " seconds"
print(output)

# Finding the label with the best cost
bestLabel = Label.Label()
bestLabel.cost = float(
    "inf"
)  # Setting the cost to infinity to compare the cost with the created labels

for label in L:
    if (
        label.path[len(label.path) - 1] == network.nNodes
        and label.cost < bestLabel.cost
    ):
        bestLabel = label


output = "Cost: " + str(bestLabel.cost)
print(output)
output = "Time: " + str(bestLabel.time)
print(output)
output = "Inco: " + str(bestLabel.inco)
print(output)
output = "Path: " + str(bestLabel.path)
print(output)
output = "Done: " + str(bestLabel.done)
print(output)
# print(network.arcs)
