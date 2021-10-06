# Temporal social network (on the playground)

This repository contains the implementation of the temporal graph, introduced by Kostakos:

Holme, P., & Saramäki, J. (2012). Temporal networks. Physics reports, 519(3), 97-125.

### Requirements:
- numpy 
- networkx
- pandas

Step 1:
The temporal graph is implemented and tested via the simple dataset that the paper has used. The same result is obtained.
The simple data is located in the Data folder, and the `temporal_graph.py` use this file to create the temporal graph.

`python temporal_graph.py`

Step 2: 
The temporal graph is further adjusted to take the data from the schoolyard. The new implementation is in `main.py`.
