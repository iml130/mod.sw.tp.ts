import networkx as nx
import matplotlib as mpl
mpl.use('Agg') 
import matplotlib.pyplot as plt

def getChildTask(G, currentTask):
    child = None
    xxx =  G.successors(currentTask)
    for x in  xxx:
        child = x
        
    for node in G.nodes():
        if(node == currentTask):
            print "current" 
    return child

def getStartTask(G):
    listStartTask = []
    for node in G.nodes():
        if(G.in_degree(node) == 0):
            listStartTask.append(node)
    
    return listStartTask

def printGraphInfo(G):
    print "NumberOfSelfLoops:" + str(G.number_of_selfloops())
    print getStartTask(G)

    for node in G.nodes():
        print "-----"
        print node
        print "in: " + str(G.in_degree(node))
        print "out: " + str(G.out_degree(node))

def displayGraph(G, save = False):
    color_map = []
    for node in G:
        if G.in_degree(node) == 0:
            color_map.append('skyblue')    
        else:
            color_map.append('green')  
    nx.draw(G, node_color=color_map ,node_size=1500, with_labels = True)
    if(save):
        plt.savefig("./images/task.png")
    #plt.show()

def createGraph(taskInfos): 
    G = nx.DiGraph(day="Tasks")

    #create the start task
    for task in taskInfos.itervalues():
        G.add_node(task)

    # add Vertices and create also Edge
    for task in taskInfos.itervalues():
        for child in task.onDone:
            G.add_edge(task, taskInfos[child])
    return G