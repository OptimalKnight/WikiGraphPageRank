# Wiki-Graph PageRank
Extraction of top-k most popular wiki-pages from a directed graph on the whole wikipedia network using the PageRank algorithm.


## Details
The project consists of two phases. The first phase focuses on the generation of a Wiki-Graph using a compressed file containing the information of every wikipedia webpage available on the internet. Whereas, the second phase focuese on executing the PageRank algorithm on this generated graph using the random walk technique. The compressed file is supplied in the '**.bz2**' format. An edge (A, B) in the graph represents that there is an out-link from wiki-page A to wiki-page B. For every wiki-page, the program first extracts the complete information of the page, and then adds a directed between the current page and all the wiki-pages which are out-linked in the current wiki-page. The program then performs a random walk on the generated network keeping the count of number of visits on each node and then provides the list of the top-k most popular wiki-pages where 'k' is a parameter provided by the user.

## Functioning
- The program mainly consists of the following five procedures,  
  - *extractWikiPageIDs*
  - *buildWikiGraph*
  - *printWikiPages*
  - *pageRank*
  - *wikiGraph*
- The program reads the input '**.bz2**' file page-by-page and stores the mapping between the page titles and page ids of all the wiki-pages in a file. The '*extractWikiPageIDs*' function is used to perform this task.
- The program then uses the input file and the generated id-mapping to create the adjacecny list of the Wiki-Graph network. This adjacency list is created solely between page ids and is stored in a seperate file. The '*buildWikiGraph*' function preforms this task.
- The program then uses this produced adjacency list to perform a random walk on the Wiki-Graph and simultaneously keeps the count of the number of visits on each wiki-page. The '*PageRank*' function is used for this random walk. 
- The program then sorts the wiki-pages in decreasing order of visits and then write the top-k most popular wiki-pages in the final output file. The program uses the '*printWikiPages*' procedure for this functionality.
- The program uses the '*wikiGraph*' wrapper function to perform all of the above tasks sequentially.
- The program filters out all the wiki-pages containing either 'Wikipedia:', 'Category:', 'File:', 'Portal:', or 'Template:' in their page titles. These pages are removed because they are not indivisible entities and are of no significant importance of their own. 

## How To Use
- The project consists of the following files/directories,
  - **/data/bz2 (directory)**
  - **/data/txt (directory)**
  - **wikiGraph.py (file)**
  - **wikiGraph.ipynb (file)**
  - **README.md (file)**
  - **.gitignore (file)**
- '**wikiGraph.py**' consists of the source code of the project. ('**wikiGraph.ipynb**' also consists of the same source code as a jupyter notebook and with no comments)
- Open the terminal and navigate into the directory containing this file.
- Load the input '**.bz2**' file in the '**/data/bz2**' directory. 
- Set the name/path of the input file in the '*wikiGraph*' function's 'filePath' variable.
- Set the value of the required number of popular wiki-pages in the '*wikiGraph*' function's variable named 'k'.
- Execute the command 'python wikiGraph.py'. 
- The program will generate the following three files,
  - **wikiPageIDs.txt**
  - **adjacencyList.txt**
  - **results.txt**
- All these files are generated in the '**/data/txt**' directory. '**wikiPageIDs.txt**' will contain the title-id mappings. '**adjacencyList.txt**' will consist of the generated adjacency list between the wiki-page ids. '**results.txt**' will consist of the final list of the required top-k most popular wiki-pages.
- All these three files generated after an execution (k = 10) on a sample (1/100th number of pages of the original file) '**.bz2**' file are also provided in the '**/data/txt**' directory beforehand.
- '**results.txt**' containing the final result of an execution (k = 99) performed on the complete graph (22 million pages) is also provided in the '**/data/txt**' directory. All the other files are omitted because of their large sizes.

## Observations
- The top 3 most popular wiki-pages are,
  1. **Wikipedia**
  2. **United States**
  3. **The New York Times** 
- Most of the pages in the final list consists of wiki-pages related to indivisual countries.