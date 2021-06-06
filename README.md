# ORF 387 - Networks Final Project

Collects and processes data from twitch for the viewership of popular twitch channels. Compares the overlapping viewers to create a network to visualize the interconnections.

## Description

The first file, data_collection_v2_generic.py, collects the current viewers of the Twitch channels listed in channels.csv ans stores them in folders on the desktop.
The folder complexity is necessary to ensure that the string compare process that follows in data_processing_v2.py can be somewhat efficient. Implementing dictionaries
would be a superior way of storing the data. This program of data collection must be run multiple times for the viewer lists to then be compared. 
data_processing_v2.py takes the lists from collection and creates a .gexf file to be loaded into a network visualizer for analysis with each node having a weight of total
unique viewers and each edge having a weight of the shared viewers between the channels. Utilizes multiprocessing to speed up the string compare process but is still extremely
time intensive and has enormous room for improvement.

## Getting Started

### Dependencies

Just make sure you have all the packages included at the beginning of the data_processing_v2.py file and both should run on Windows 10.

### Installing

Make sure you change the file names in both programs to match the heirarchy on your machine and download channels.csv and update its file location.

## Author

Eli Krahn
