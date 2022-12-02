# Author: Ojassvi Kumar (2020csb1187)

import os                               # to get the complete absolute path of the current directory
import bz2                              # to read the given bz2 file
import random                           # to generate random numbers required for the random walk
import linecache                        # to read a specific line from the file containing the adjacency list
import xml.etree.ElementTree as ET      # to parse the content of a wiki-page into an xml tree

# function to extract the ids of all the wiki-pages from the given bz2 file
def extractWikiPageIDs(filePath, idMap):
    # creating objects to read and write the appropriate files
    readFile = bz2.open(filePath, "rb")
    filePath = os.getcwd() + "/data/txt/wikiPageIDs.txt"
    writeFile = open(filePath, "w", encoding = "utf-8")
    
    # buffer to store the content of the current wiki-page
    wikiPage = ""
    while True:
        # reading the current line from the given bz2 file
        line = str(readFile.readline(), "utf-8")
        if not line:
            break
        
        # identifying the start of a wiki-page in the given bz2 file
        if "<page>" in line:
            wikiPage = line
        # identifying the end of a wiki-page in the given bz2 file
        elif "</page>" in line:
            wikiPage += line

            # buffers to store the id and title of the current wiki-page
            id = ""
            title = ""
            # parsing the content of the current wiki-page into an xml tree
            root = ET.fromstring(wikiPage)
            for c1 in root:
                # identifying the child named 'id' of the root
                if c1.tag == "id":
                    id = c1.text
                # identifying the child named 'title' of the root
                if c1.tag == "title":
                    title = c1.text
            
            # updating the mapping between the page titles and page ids
            idMap[title] = id
            # writing the mapping onto a 'wikiPageIDs.txt' file
            writeFile.write(title.lower() + " " + id + "\n")
        else:
            # storing the content of the current wiki-page in the buffer line-by-line
            wikiPage += line
    
    # signalling the completion of the id extraction and closing the read-write objects
    print("ID Extraction Completed!")
    readFile.close()
    writeFile.close()

# function to build the required wiki-graph
def buildWikiGraph(filePath):
    # initializing the mapping between the page titles and page ids
    idMap = {}
    # calling the 'extractWikiPageIDs' function to extract all the page ids
    extractWikiPageIDs(filePath, idMap)

    # creating objects to read and write the appropriate files
    readFile = bz2.open(filePath, "rb")
    filePath = os.getcwd() + "/data/txt/adjacencyList.txt"
    writeFile = open(filePath, "w", encoding = "utf-8")

    # buffer to store the content of the current wiki-page
    wikiPage = ""
    while True:
        # reading the current line from the given bz2 file
        line = str(readFile.readline(), "utf-8")
        if not line:
            break
        
        # identifying the start of a wiki-page in the given bz2 file
        if "<page>" in line:
            wikiPage = line
        # identifying the end of a wiki-page in the given bz2 file
        elif "</page>" in line:
            wikiPage += line

            # buffers to store the id and text of the current wiki-page
            id = ""
            content = ""
            # parsing the content of the current wiki-page into an xml tree
            root = ET.fromstring(wikiPage)
            for c1 in root:
                # identifying the child named 'id' of the root
                if c1.tag == "id":
                    id = c1.text
                # identifying the child named 'revision' of the root
                if c1.tag == "revision":
                    for c2 in c1:
                        # identifying the child name 'text' of the node named 'revision'
                        if c2.tag == "text":
                            content = c2.text
            
            # list to store the out-links from the current wiki-page
            links = []
            # condition to ensure that the content of the current wiki-page is non-null
            if content is not None:
                # extracting the links from the current wiki-page using the underlying pattern
                links = content.split("[[")
                for i in range(len(links)):
                    links[i] = links[i].split("]]")[0]
                    if "|" in links[i]:
                        links[i] = links[i].split("|")[0]
                links = links[1:]

            # writing the id of the current wiki-page in the file containing the adjacency list
            writeFile.write(id)
            # writing the extracted out-link only if it exists as a wiki-page itself
            for link in links:
                if link in idMap:
                    writeFile.write(" " + idMap[link])
            writeFile.write("\n")
        else:
            # storing the content of the current wiki-page in the buffer line-by-line
            wikiPage += line
    
    # signalling the completion of the graph generation and closing the read-write objects
    print("WikiGraph Build Completed!")
    readFile.close()
    writeFile.close()

# function to extract and write the names of the given list of wiki-page ids
def printWikiPages(wikiPages, iterations, k):
    # creating objects to read and write the appropriate files
    filePath = os.getcwd() + "/data/txt/wikiPageIDs.txt"
    readFile = open(filePath, "r", encoding = "utf-8")
    filePath = os.getcwd() + "/data/txt/results.txt"
    writeFile = open(filePath, "w", encoding = "utf-8")
    
    while True:
        # reading the current line from the file containing the wiki-page ids
        line = readFile.readline()
        if not line:
            break
        
        # extracting the page id and page name from the current line
        line = line.split(" ")
        pageName = line[0]
        for i in range(1, len(line) - 1):
            pageName = pageName + " " + line[i]

        # checking if the current id matches any required id
        for i in range(len(wikiPages)):
            if wikiPages[i] == line[len(line) - 1][:-1]:
                # updating the entry with page name if a match of ids is found
                wikiPages[i] = pageName
    
    counter = 1
    # writing the total number of iterations in the 'results.txt' file
    writeFile.write("Total number of iterations: " + str(iterations) + "\n\n")
    for w in wikiPages:
        # skipping the page names containing the following patters
        if "category:" in w or "wikipedia:" in w or "file:" in w or "template:" in w or "portal:" in w:
            continue
        
        # writing the page name and page rank of the current wiki-page in the file containing the results
        writeFile.write(f"Rank {counter}: " + w + "\n")
        # condition to break the loop if we've already written the top-k wiki-pages
        if counter == k:
            break
        counter += 1
    
    # signalling the completion of the final results generation and closing the read-write objects
    print("Results Generation Completed!")
    readFile.close()
    writeFile.close()

# function to find the page ranks of the wiki-pages using the random walk algorithm of the given wiki-graph
def pageRank(filePath, k):
    # creating objects to read and write the appropriate files
    readFile = open(filePath, "r", encoding = "utf-8")

    # initializing the mapping between the page ids and their index in the file containing the adjacency list
    indexMap = {}
    currentIndex = 1
    while True:
        # reading the current line from the file containing the adjacency list
        line = readFile.readline()
        if not line:
            break
        
        # extracting the current id of a wiki-page
        currentID = line.split(" ")[0]
        if len(line.split(" ")) == 1:
            currentID = currentID[:-1]
        # updating the mapping between the page ids and their index in the file containing the adjacency list
        indexMap[currentID] = currentIndex
        currentIndex += 1

    # closing the read object
    readFile.close()

    # initializing the number of iterations, probability of teleportation in the random walk, mapping between the visit count and page ids, and the list of visited pages
    iterations, teleportationProbability = 100000000, 1
    visitCount = {}
    visited = []

    # generating a random wiki-page id to begin the random walk
    line = linecache.getline(filePath, random.randint(1, currentIndex - 1)).split(" ")
    currentNode = line[0]
    while len(line) == 1:
        line = linecache.getline(filePath, random.randint(1, currentIndex - 1)).split(" ")
        currentNode = line[0]
    # initializing the visit count of the starting wiki-page
    visitCount[currentNode] = 1
    # appending the starting node to the list of visited wiki-pages
    visited.append(currentNode)

    # random walk starts here
    for it in range(iterations):
        # generatiing a raondom number
        randomNumber = random.randint(1, 10)
        # teleporting condition if the generated random number falls within the range of teleportation probability
        if randomNumber <= teleportationProbability:
            # selecting the next wiki-page randomly from already visited wiki-pages
            nextNode = random.choice(visited)
            # visiting to the selected wiki-page and incrementing its visit count
            visitCount[nextNode] = visitCount[nextNode] + 1
            currentNode = nextNode
        # condition to visit a random out-link of the current wiki-page
        else:
            # reading the list of all the out-links of the current wiki-page
            line = linecache.getline(filePath, indexMap[currentNode]).split(" ")
            line[len(line) - 1] = line[len(line) - 1][:-1]
            # condition to handle the case when the current wiki-page has no out-links
            if len(line) == 1:
                # teleporting to a random wiki-page selected from the list of already visited wiki-pages
                nextNode = random.choice(visited)
                # incrementing the visit count of the selected wiki-page
                visitCount[nextNode] = visitCount[nextNode] + 1
                currentNode = nextNode
            # condition to normally visit a randomly selected out-link
            else:
                # selecting a random out-link from the current wiki-page
                nextNode = line[random.randint(1, len(line) - 1)]
                # condition to handle the case when we are visiting a wiki-page for the first time
                if nextNode not in visitCount:
                    # initializing the visit count of the current wiki-page
                    visitCount[nextNode] = 1
                    # appending the selected wiki-page to the list of visited wiki-pages
                    visited.append(nextNode)
                # condition to handle the case when we are not visiting a wiki-page for the first time
                else:
                    # incrementing the visit count of the selected wiki-page
                    visitCount[nextNode] = visitCount[nextNode] + 1
                currentNode = nextNode

    # signaling the completion of the random walk
    print("Random Walk Completed!")

    counter = 1
    wikiPages = []
    # sorting the wiki-pages in decreasing order of visits and extracting the top-10*k wiki-page ids (selecting top-10*k wiki-pages as we are filtering out some wiki-pages as well)
    for el in sorted(visitCount.items(), key = lambda kv:kv[1], reverse = True):
        if counter == 10*k:
            break

        wikiPages.append(el[0])
        counter += 1
    
    # calling the 'pringWikiPages' function to generate and write the observed result of the page rank algorithm
    printWikiPages(wikiPages, iterations, k)

# wrapper function to generate the graph and then execute the page rank algorithm on the generated graph
def wikiGraph():
    # setting the path of the input bz2 file
    filePath = os.getcwd() + "/data/bz2/enwiki-latest-pages-articles.xml.bz2"
    # calling the 'buildWikiGraph' function to generate the wiki-graph
    buildWikiGraph(filePath)

    # setting the path of the file containing the adjacecny list
    filePath = os.getcwd() + "/data/txt/adjacencyList.txt"
    # setting the number of required wiki-pages
    k = 100
    # calling the function to exectue the page rank algorithm
    pageRank(filePath, k)



# calling the wrapper function to generate the wiki-graph and exectue the page rank algorithm on the generated graph
wikiGraph()