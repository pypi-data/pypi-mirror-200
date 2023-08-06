from abc import ABC,abstractmethod

class Graph(ABC):
  def __init__(self):
    self.Edict = dict()
  
  @abstractmethod
  def add_edge(self,V1,V2,weight=1):
    pass

  @abstractmethod
  def add_edges(self,List):
    pass
  
  @abstractmethod
  def remove_edge(self,Tuple):
    pass

  def remove_edges(self,List):
    for i in List:
      self.remove_edge(i[0],i[1])

  def add_vertex(self,vertex):
    self.Edict[vertex] = dict()

  def add_vertices(self,List):
    for i in List:
      self.add_vertex(i)

  def remove_vertex(self,vertex):
    self.Edict.pop(vertex)

  def remove_vertices(self,List):
    for i in List:
      self.remove_vertex(i)
        
class Digraph(Graph):
  def add_edge(self,V1,V2,weight=1):
    if V1 not in self.Edict:
        self.Edict[V1] = {}
    self.Edict[V1][V2] = weight 
  
  def add_edges(self,List):
    for i in List:
      if len(i)==2:
        l = list(i)
        l.append(1)
        i = tuple(l)
      elif len(i)!=3:
        raise Exception("Valid argument!")
      self.add_edge(i[0],i[1],i[2])

  def remove_edge(self,V1,V2):
    self.Edict[V1].pop(V2)

  def remove_vertex(self,vertex):
    self.Edict.pop(vertex)


import math
class Dijkstra:
  def __init__(self,graph,start_vertex):
    self.graph = graph
    self.start_vertex = start_vertex
    self.vertices = list(graph.Edict.keys())
    self.Vlabels = {vertex: {'distance': math.inf, 'previous_vertex': '-'} for vertex in self.vertices}
    self.Vlabels[start_vertex]['distance'] = 0

  def _get_edge_weight(self,v1, v2):
      try:
          return self.graph.Edict[v1][v2]
      except KeyError:
          return math.inf
    
  def _set_label(self, vertex, weight, prev=''):
      self.Vlabels[vertex]['distance'] = weight
      if prev:
          self.Vlabels[vertex]['previous_vertex'] = prev

  def _get_label(self, vertex):
      return self.Vlabels[vertex]

  def dijkstra(self):
      interiors = [self.start_vertex]
      max_ivertices = len(self.vertices)
      while True:
          exteriors = [vertex for vertex in self.vertices if vertex not in interiors]
          nearest_vertex = '-'
          nearest_vertex_distance = math.inf
          for exterior in exteriors:
              exterior_label = self._get_label(exterior)
              shortest_discovered_distance = exterior_label['distance']
              choosen_prev = exterior_label['previous_vertex']
              for interior in interiors:
                  distance_from_exterior = self._get_label(interior)['distance'] + self._get_edge_weight(interior, exterior)
                  if distance_from_exterior < shortest_discovered_distance:
                      shortest_discovered_distance = distance_from_exterior
                      choosen_prev = interior
              self._set_label(exterior, shortest_discovered_distance, choosen_prev)
              if shortest_discovered_distance < nearest_vertex_distance:
                  nearest_vertex_distance = shortest_discovered_distance
                  nearest_vertex = exterior
          interiors.append(nearest_vertex)
          if len(interiors) == max_ivertices:
              break
        
  def build_path(self, vertex):
    if vertex == '-':
        return []
    return self.build_path(self.Vlabels[vertex]['previous_vertex']) + [vertex]
  
  def print_result(self):
     for vertex in self.vertices:
        print(self.start_vertex,'->', vertex + ':', self.build_path(vertex),'distance:',self.Vlabels[vertex]['distance'])
  
if __name__ == "__main__":
    graph = Digraph()

    #To check add_edge and add_edges functions
    graph.add_edges([('A','B'),('A','C',6),
                     ('B','A',3),('B','C',4),
                     ('C','F',6),('C','H',11),
                     ('F','A',11),('F','G',9),('F','H',4),
                     ('G','H',5),
                     ('H','A',11),('H','G',4)])
    print(graph.Edict)

    graph.add_edges([('A','D',45),('A','E',23)])
    print(graph.Edict)

    #To check remove_edge and remove_edges functions
    graph.remove_edges([('A','D'),('A','E')])
    print(graph.Edict)

    #To check add_vertex and add_vertices functions
    graph.add_vertices(['I','J','K'])
    print(graph.Edict)

    #To check remove_vertex and remove_vertices functions
    graph.remove_vertices(['I','J','K'])
    print(graph.Edict)

    #To check Dijkstra class and its functions
    dijkstra = Dijkstra(graph, start_vertex='C')
    dijkstra.dijkstra()
    dijkstra.print_result()


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