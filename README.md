# Games Sales
Simple Web Application that manages data of the sales of severall games. It uses data from a repository created on GraphDB.

## How To Run
You need to install the following dependencies:
- [Python](https://www.python.org/) 3.6;
- [Django](https://www.djangoproject.com/) 2.2;
- [Graphviz](https://www.graphviz.org/). Change the path of installation on [views.py](https://github.com/tiagohpf/WS_GameSales/blob/master/app/views.py);
- [Python Pandas](https://pandas.pydata.org/);
- [GraphDB](http://graphdb.ontotext.com/);

Execute the application with the following sequence:
- Execute [**csv_parser.py**](https://github.com/tiagohpf/WS_GameSales/blob/master/csv_parser.py), choosing one of vgSales files on [**data**](https://github.com/tiagohpf/WS_GameSales/tree/master/data) folder. The CSV files are converted to triples, with the result **clean_sales.csv**. All these files are in [**clean_data**](https://github.com/tiagohpf/WS_GameSales/tree/master/clean_data) folder;
- Execute [**rdf_parser.py**](https://github.com/tiagohpf/WS_GameSales/blob/master/rdf_parser.py), transforming triple to N-Triples and write to [**games.nt**](https://github.com/tiagohpf/WS_GameSales/blob/master/games.nt);
- Create a repository in GraphDB called **games** and **OWL-2 QL (Optimized)** as ruleset. After that, upload [**games.nt**](https://github.com/tiagohpf/WS_GameSales/blob/master/games.nt) and [**games_ont.nt**](https://github.com/tiagohpf/WS_GameSales/blob/master/games_ont.owl);
- Execute the Django project;
