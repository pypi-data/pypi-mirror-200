ShabiiNetwork
=============

ShabiiNetwork is a Python library for dealing with Graphs and Dijkstra’s
algorithm.

Installation
------------

Use the package manager `pip <https://pip.pypa.io/en/stable/>`__ to
install ShabiiNetwork.

.. code:: bash

   pip install ShabiiNetwork

Usage
-----

.. code:: python

   from ShabiiNetwork import Digraph,Dijkstra

   graph2 = Digraph()

       #To check add_edge and add_edges functions
       graph2.add_edges([('A','B',0.3),('A','C',0.5),
                        ('B','A',0.3),('B','C',0.9),
                        ('C','A',0.5),('C','D',1.2),
                        ('D','C',1.2)])
       print(graph2.Edict)

       graph2.add_edges([('A','D',45),('A','E',23)])
       print(graph2.Edict)

       #To check remove_edge and remove_edges functions
       graph2.remove_edges([('A','D'),('A','E')])
       print(graph2.Edict)

       #To check add_vertex and add_vertices functions
       graph2.add_vertices(['I','J','K'])
       print(graph2.Edict)

       #To check remove_vertex and remove_vertices functions
       graph2.remove_vertices(['I','J','K'])
       print(graph2.Edict)

       #To check Dijkstra class and its functions
       dijkstra = Dijkstra(graph2, start_vertex='A')
       dijkstra.dijkstra()
       dijkstra.print_result()

       """
       Output:

       {'A': {'B': 0.3, 'C': 0.5}, 'B': {'A': 0.3, 'C': 0.9}, 'C': {'A': 0.5, 'D': 1.2}, 'D': {'C': 1.2}}
       {'A': {'B': 0.3, 'C': 0.5, 'D': 45, 'E': 23}, 'B': {'A': 0.3, 'C': 0.9}, 'C': {'A': 0.5, 'D': 1.2}, 'D': {'C': 1.2}}
       {'A': {'B': 0.3, 'C': 0.5}, 'B': {'A': 0.3, 'C': 0.9}, 'C': {'A': 0.5, 'D': 1.2}, 'D': {'C': 1.2}}
       {'A': {'B': 0.3, 'C': 0.5}, 'B': {'A': 0.3, 'C': 0.9}, 'C': {'A': 0.5, 'D': 1.2}, 'D': {'C': 1.2}, 'I': {}, 'J': {}, 'K': {}}
       {'A': {'B': 0.3, 'C': 0.5}, 'B': {'A': 0.3, 'C': 0.9}, 'C': {'A': 0.5, 'D': 1.2}, 'D': {'C': 1.2}}
       A -> A: ['A'] distance: 0
       A -> B: ['A', 'B'] distance: 0.3
       A -> C: ['A', 'C'] distance: 0.5
       A -> D: ['A', 'C', 'D'] distance: 1.7
       """

Contributing
------------

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

Author
------

Charawi Detphumi

License
-------

`MIT <https://choosealicense.com/licenses/mit/>`__
