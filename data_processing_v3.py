import os
import requests
import json
import sys
import io
import numpy as np
import csv
import networkx as nx
import matplotlib.pyplot as plt
import multiprocessing as multi
from itertools import product
import time

# The function to count the number of unique viewers for a given channel.
# Returns the channel name and number of viwers as a tuple
def unique_viewers(channel):

    # Just iterate over all folders and count
    total = 0
    folders_1 = os.listdir('C:/ORF 387/' + channel)
    for folder_1 in folders_1:
        level_1 = 'C:/ORF 387/' + channel + '/'
        folders_2 = os.listdir(level_1 + folder_1)
        for folder_2 in folders_2:
            level_2 = level_1 + folder_1 + '/'
            folders_3 = os.listdir(level_2 + folder_2)
            for folder_3 in folders_3:
                level_3 = level_2 + folder_2 + '/'
                viewers = np.array(np.loadtxt(level_3 + folder_3, dtype = 'str', comments = "#", delimiter = ",", unpack = False))
                total += viewers.size
                
    return (channel, total)




# Takes two channels and returns the number of viewers they have in common
# returns the second channel being compared to and the number of common viewers
def intersection(channel_1, channel_2):

    common = 0

    # Get all first letter folders for a channel
    folders_1 = os.listdir('C:/ORF 387/' + channel_1)

    # iterate over all first letter folders
    for folder_1 in folders_1:

        # if the second channel has that first letter folder
        if os.path.isdir('C:/ORF 387/' + channel_2 + "/" + folder_1) == True:
            # get all the second letter folders
            folders_2 = os.listdir('C:/ORF 387/' + channel_1 + '/' + folder_1)

            # iterate over all second letter folders
            for folder_2 in folders_2:
                # if the second channel has that second letter folder
                if os.path.isdir('C:/ORF 387/' + channel_2 + "/" + folder_1 + '/' + folder_2) == True:
                    # get all the third letter documents
                    textfiles = os.listdir('C:/ORF 387/' + channel_1 + '/' + folder_1 + '/' + folder_2)

                    # iterate over all the final files of usernames
                    for textfile in textfiles:

                        # if the given final file exists, we compare the users in the two folders
                        if os.path.isfile('C:/ORF 387/' + channel_2 + "/" + folder_1 + '/' + folder_2 + '/' + textfile) == True:

                            # spawn treads for each textfile that actually exists
                            # viewers for channel 1 in this folder
                            viewers_1 = set(np.array(np.loadtxt('C:/ORF 387/' + channel_1 + "/" + folder_1 + '/' + folder_2 + '/' + textfile, dtype = 'str', comments = "#", delimiter = ",", unpack = False)).tolist())
                            # viewers for channel 2
                            viewers_2 = set(np.array(np.loadtxt('C:/ORF 387/' + channel_2 + "/" + folder_1 + '/' + folder_2 + '/' + textfile, dtype = 'str', comments = "#", delimiter = ",", unpack = False)).tolist())
                            match = viewers_1.intersection(viewers_2)
                            common += len(match)

    return(channel_2, common)


def main():

    # we create a graph to store the nodes and edges in while the data is processed
    graph = nx.Graph()
    
    # get all the channels being examined
    channels = np.array(np.loadtxt("C:/ORF 387/channels.csv", dtype = 'str', comments = "#", delimiter = ",", unpack = False))

    size = channels.size

    # With the multiprocessing tool, we can count the viewers in multiple channels at once, drastically improving the time of the process
    # This takes the function to be run along with an iterable of channels and iterates over them, storing the results from each process in unique
    # Note that for this function to work it must be defined in the same file and we must have the if __name__ == '__main__' section below
    # My computer was able to handle roughly 10 processes at once, hence processes = 10, but this may need to be adjusted for different machines
    with multi.Pool(processes = 10) as pool:
        unique = pool.starmap(unique_viewers, product(channels))

    # For every channel we create a node and add a feature called size that is the total number of unique viewers
    for i in range(0,size):
        if unique[i][1] != 0:
            graph.add_node(unique[i][0], size = unique[i][1])


    # Again with multiprocessing, we can count the number of similar viewers for multiple channel pairs at once
    # i ensures that we don't waste time doing compares we have already done. Every channel is only compared to those that follow it
    i = 0
    for channel_1 in channels:
        print("Working on: " + channel_1)
        i += 1
        with multi.Pool(processes = 10) as pool:
            # starmap can only take one argument, so we must format everything as a tuple
            edges = pool.starmap(intersection, [(channel_1, channel_2) for channel_2 in channels[i:]])
        # adding edges to the graph for each set of channels. If the edge has zero weight, it is not added
        for j in range(0, size - i):
            if edges[j][1] != 0:
                graph.add_edge(channel_1, edges[j][0], weight = edges[j][1])
        

    # We then save all the created data as a .gexf file to be used later
    nx.write_gexf(graph, 'C:/ORF 387/test.gexf')

    # for bug fixing
    # nx.draw(graph, with_labels=True, font_weight='bold')
    # plt.show()
        

#Program Execution
if __name__ == '__main__':
    main()
