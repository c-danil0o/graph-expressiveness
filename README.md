# graph-expressiveness

### About
Project about graph visualization with different data sources and different visualizers. Application is completely modular, meaning data sources and visualizers can be installed via pip as plugins. Main platform is Django but that can also be changed without affecting logic of application.

### Data Sources
We implemented two data sources.
- Ethereum blockchain
- Github 

Ethereum data source uses Alchemy JSON Web RPC to connect to blockchain and get chosen number of last blocks. Graph is formed from transactions and wallets, where transactions are nodes and wallets are edges.

GitHub uses GitHub API to get information about GitHub accounts starting from chosen profile. Depth can be configured.


### Visualizers
There are two implemented visualizers:
- Simple visualizer
- Block visualizer

Visualizers use D3.js library for displaying. 
Simple visualizer shows graph nodes as circles with node id's over them.
Block visualizer shows nodes as rectangles with all the information about node.


### Requirements
To run this application you will need:
- Python >= 3.7
- Django >= 5.0.0
- web3 >= 6.10
- PyGithub >= 2.20

Plugin dependencies should be automatically installed when installing plugins.

### Installation
First step is to create virtual environment. You can achieve this using `virtualenv` command or via `python3 -m venv venv`. 
After that you need to clone this repository in chosen folder.

Activating virtual environment is done via `source venv/bin/activate`. To install all requirements you need to run 
`python3 -m pip install -r requirements.txt`. 

Last step is to run installation script. There are two scripts.
- for Linux users `./run.sh`
- for Windows users `.\run.bat`

### Usage
Application server is started on [http://127.0.0.1:8080/app/]().

After that you can select source and visualizer and click `Generate`. You can change visualizers via `Show` button or filter graph via top bar. 
There are two ways of searching the graph. You can enter any keyword and click filter. Result will be all nodes containing that keyword. Second way to search the graph is using queries. Query format is in form of:
```
<attribute_name> <comparator> <attribute_value>
```
Comparator can be any of the following: `==,>,>=,<,<=,!=.` 

## Team members:

- Aleksa Perovic(SV24-2021)
- Danilo Cvijetic(SV25-2021)
- Vladimir Cornenki(SV53-2021)
- Nemanja Stjepanovic(SV75-2021)
