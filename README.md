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
The temporal graph is further adjusted to take the data from the schoolyard. The new implementation is in `main.py`:
`python main.py --basicinfo=<path_basic_information>  --edgefile=<path_edge_file>   --numdata=<data_size> --resultpath=<path_result> --prefix=<prefix_output_file>`
parser.add_argument('--basicinfo', type=str, default='Basic_info.csv',
                    help='Path and file name of the basic information')
parser.add_argument('--edgefile', type=str, default='edge_code_098.csv',
                    help='Path and file name of the edge file')
parser.add_argument('--numdata', type=int, default=20,
                    help='Number of data to read')
parser.add_argument('--resultpath', type=str, default='Results/',
                    help='Path to the result files')
parser.add_argument('--prefix', type=str, default='test',
                    help='Prefix of the file name')
