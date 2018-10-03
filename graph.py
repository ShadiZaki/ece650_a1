from vertex1 import Vertex
from edge1 import Edge
    
class Graph:
    
    intersections = []
    def __init__(self):
        self.__vertex_list = []
        self.__edges_list = []
        self.__updated_vertex_list = []
        self.__updated_edges_list = []
    
    def __distance(self, vertex1, vertex2):
        x1 = float(vertex1.get_xcoor())
        y1 = float(vertex1.get_ycoor())
        x2 = float(vertex2.get_xcoor())
        y2 = float(vertex2.get_ycoor())
        difx = x2 - x1
        dify = y2 - y1
        if(difx == 0 and dify == 0):
            dis = 0
        else:
            dis = (difx*difx + dify*dify)**(.5)
        return dis
    
    def __intersect (self, edge1, edge2):
        x1 = float(edge1.get_vertex1().get_xcoor())
        y1 = float(edge1.get_vertex1().get_ycoor())
        x2 = float(edge1.get_vertex2().get_xcoor())
        y2 = float(edge1.get_vertex2().get_ycoor())
        
        x3 = float(edge2.get_vertex1().get_xcoor())
        y3 = float(edge2.get_vertex1().get_ycoor())
        x4 = float(edge2.get_vertex2().get_xcoor())
        y4 = float(edge2.get_vertex2().get_ycoor())

        den = ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
        xnum = ((x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4))
        ynum = (x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4)
        
        if(den != 0):
            xcoor =  xnum / den
            ycoor = ynum / den
            if(not (xcoor >= min(x1,x2) and xcoor <= max(x1,x2) and xcoor >= min(x3,x4) and xcoor <= max(x3,x4) 
               and ycoor >= min(y1,y2) and ycoor <= max(y1,y2) and ycoor >= min(y3,y4) and ycoor <= max(y3,y4))):
                return "No intersection"
        else:
            return "No intersection"
        
        intersection = Vertex()
        intersection.create_ID()
        intersection.set_xcoor(xcoor)
        intersection.set_ycoor(ycoor)
        intersection.set_as_intersection()
        intersection.intersection_streets.append(edge1.get_street())
        intersection.intersection_streets.append(edge2.get_street())
        
        for i in self.intersections:
            if(i.get_xcoor() == intersection.get_xcoor() and i.get_ycoor() == intersection.get_ycoor()):
                intersection.set_ID(i.get_ID())
            
        return intersection
    
    def __add_intersections(self):
        for i in self.__vertex_list:
            self.__updated_vertex_list.append(i)
        for i in range(0,len(self.__edges_list)-1):
            for j in range(i+1,len(self.__edges_list)):
                if (self.__edges_list[i].get_street() != self.__edges_list[j].get_street()):
                    intersection = self.__intersect(self.__edges_list[i], self.__edges_list[j])
                    if (intersection != "No intersection"):
                        if(not any(k.get_xcoor() == intersection.get_xcoor() and k.get_ycoor() == intersection.get_ycoor() for k in self.__updated_vertex_list)):
                            self.__updated_vertex_list.append(intersection)
                            self.intersections.append(intersection)
                        else:
                            for x in range(0, len(self.__updated_vertex_list)):
                                if (self.__updated_vertex_list[x].get_xcoor() == intersection.get_xcoor() and self.__updated_vertex_list[x].get_ycoor() == intersection.get_ycoor()):
                                    inter = self.__updated_vertex_list[x]
                                    inter.intersection_streets += intersection.intersection_streets
                                    self.__updated_vertex_list.pop(x)
                                    self.__updated_vertex_list.append(inter)
                                    self.intersections.append(inter)
        return

    def __reachable(self, intersection):
        reachable = []
        for i in range(0, len(self.__updated_vertex_list) - 1):
            x1 = float(self.__updated_vertex_list[i].get_xcoor())
            y1 = float(self.__updated_vertex_list[i].get_ycoor())
            x2 = float(self.__updated_vertex_list[i+1].get_xcoor())
            y2 = float(self.__updated_vertex_list[i+1].get_ycoor())
            xi = float(intersection.get_xcoor())
            yi = float(intersection.get_ycoor())
            
            num = y2 - y1
            den = x2 -x1
            
            num1 = y1 - yi
            den1 = x1 - xi
            
            num2 = y2 - yi
            den2 = x2 - xi
            
            if(den == 0):
                m = None
                b = None
            else:
                m = num / den
                b = y1 - m*x1
            
            if(den1 == 0):
                m1 = None
                b1 = None
            else:
                m1 = num1 / den1
                b1 = yi - m1*xi
            
                        
            if(den2 == 0):
                m2 = None
                b2 = None
            else:
                m2 = num2 / den2
                b2 = yi - m2*xi
            
            if(m == m1 and m == m2 and b == b1 and b == b2):
                reachable.append(True)
            else:
                reachable.append(False)
          
        return reachable
    
    def __min_index(self):
        for i in range(0, len(self.__updated_vertex_list)-1):
            dist = []
            for j in range(i+1, len(self.__updated_vertex_list)):
                if(self.__updated_vertex_list[i].is_intersection() and self.__updated_vertex_list[j].is_intersection()):
                    dist.append(self.__distance(self.__updated_vertex_list[i], self.__updated_vertex_list[j]))
            if(len(dist) > 0):
                min_index = dist.index(min(dist))
            else:
                min_index = None
        return min_index
                                                
    def __generate_edges(self):
        temp_edges = []
        contained = False
        
        for i in range(0, len(self.__updated_vertex_list)-1):
            for j in range(i+1, len(self.__updated_vertex_list)):
                if(self.__updated_vertex_list[i].is_intersection() or self.__updated_vertex_list[j].is_intersection()):
                    if(self.__updated_vertex_list[i].get_street() == None and self.__updated_vertex_list[j].get_street() != None):
                        if(self.__updated_vertex_list[j].get_street() in self.__updated_vertex_list[i].intersection_streets):
                            reachable = self.__reachable(self.__updated_vertex_list[i])
                            if(reachable[i]):
                                edge1 = Edge()
                                edge1.set_street(self.__updated_vertex_list[j].get_street())
                                edge1.set_vertex1(self.__updated_vertex_list[i])
                                edge1.set_vertex2(self.__updated_vertex_list[j])
                                temp_edges.append(edge1)
                                edge2 = Edge()
                                edge2.set_street(self.__updated_vertex_list[j].get_street())
                                edge2.set_vertex1(self.__updated_vertex_list[j+1])
                                edge2.set_vertex2(self.__updated_vertex_list[i])
                                temp_edges.append(edge2)
                                
                    elif(self.__updated_vertex_list[i].get_street() != None and self.__updated_vertex_list[j].get_street() == None):
                        if(self.__updated_vertex_list[i].get_street() in self.__updated_vertex_list[j].intersection_streets):
                            reachable = self.__reachable(self.__updated_vertex_list[j])
                            if(reachable[i]):
                                edge1 = Edge()
                                edge1.set_street(self.__updated_vertex_list[i].get_street())
                                edge1.set_vertex1(self.__updated_vertex_list[i])
                                edge1.set_vertex2(self.__updated_vertex_list[j])
                                temp_edges.append(edge1)
                                edge2 = Edge()
                                edge2.set_street(self.__updated_vertex_list[i].get_street())
                                edge2.set_vertex1(self.__updated_vertex_list[j])
                                edge2.set_vertex2(self.__updated_vertex_list[i+1])
                                temp_edges.append(edge2)
                    elif(self.__updated_vertex_list[i].get_street() == None and self.__updated_vertex_list[j].get_street() == None):
                        for x in self.__updated_vertex_list[i].intersection_streets:
                            if(x in self.__updated_vertex_list[j].intersection_streets):
                                contained = True
                        minimum = self.__min_index()
                        if(minimum != None):
                            if(contained and minimum == j-i-1):
                                edge = Edge()
                                edge.set_vertex1(self.__updated_vertex_list[i])
                                edge.set_vertex2(self.__updated_vertex_list[j])
                                temp_edges.append(edge)
                    
        duplicate_edges = []
        for i in range(0, len(temp_edges)-1):
            for j in range(i+1, len(temp_edges)):
                
                if(temp_edges[i].get_vertex1().get_ID() == temp_edges[j].get_vertex1().get_ID()):
                    if(not temp_edges[i].get_vertex1().is_intersection() and temp_edges[i].get_vertex2().is_intersection() and temp_edges[j].get_vertex2().is_intersection()):
                        distance1 = self.__distance(temp_edges[i].get_vertex1(), temp_edges[i].get_vertex2())
                        distance2 = self.__distance(temp_edges[i].get_vertex1(), temp_edges[j].get_vertex2())
                        if(distance1 > distance2):
                            duplicate_edges.append(i)
                        else:
                            duplicate_edges.append(j) 
                if(temp_edges[i].get_vertex2().get_ID() == temp_edges[j].get_vertex2().get_ID()):
                    if(not temp_edges[i].get_vertex2().is_intersection() and temp_edges[i].get_vertex1().is_intersection() and temp_edges[j].get_vertex1().is_intersection()):        
                        distance1 = self.__distance(temp_edges[i].get_vertex2(), temp_edges[i].get_vertex1())
                        distance2 = self.__distance(temp_edges[i].get_vertex2(), temp_edges[j].get_vertex1())
                        if(distance1 > distance2):
                            duplicate_edges.append(i)
                        else:
                            duplicate_edges.append(j)
                    
                
        '''
        for i in range(0, len(duplicate_edges), 2):
            new_edge = Edge()
            new_edge.set_street(temp_edges[duplicate_edges[i]].get_street())
            new_edge.set_vertex1(temp_edges[duplicate_edges[i]].get_vertex2())
            new_edge.set_vertex2(temp_edges[duplicate_edges[i+1]].get_vertex1())
            temp_edges.append(new_edge)
        '''
        '''
        print duplicate_edges
        duplicate_edges = [int(x) for x in duplicate_edges]
        duplicate_edges.sort(cmp=None, key=None, reverse=True)
        for i in duplicate_edges:
            temp_edges.pop(i)
        '''
        temp_edges1 = []
        for i in range(0, len(temp_edges)):
            if(not duplicate_edges.__contains__(i)):
                temp_edges1.append(temp_edges[i])
        
        temp_updated_vertex_list = []
        for i in self.__updated_vertex_list:
            temp_updated_vertex_list.append(i)
        
        self.__updated_edges_list[:] = []
        self.__updated_vertex_list[:] = []
        
        for i in range(0, len(temp_edges1)):
            self.__updated_edges_list.append(temp_edges1[i])
        
        return temp_updated_vertex_list
    
    def __generate_vertices(self, raw_vertices):
        final_vertices = []
        for i in raw_vertices:
            if(i.is_intersection()):
                final_vertices.append(i)
            else:
                for j in self.__updated_edges_list:
                    if(i.get_ID() == j.get_vertex1().get_ID() or i.get_ID() == j.get_vertex2().get_ID()):
                        final_vertices.append(i)
        final_vertices = list(set(final_vertices))
        final_vertices.sort(cmp=None, key=lambda x: x.get_ID(), reverse=False)
        return final_vertices
    
    def add_street(self, street_name, coor):
        contained = False
        for i in self.__vertex_list:
            if(street_name == i.get_street()):
                contained = True
                break
        
        if(not contained):
            length = len(coor)/2
            templen = len(self.__vertex_list)
        
            for i in range(0,length):
                new_ver = Vertex()
                new_ver.create_ID()
                new_ver.set_street(street_name)
                new_ver.set_xcoor(coor[2*i])
                new_ver.set_ycoor(coor[2*i+1])
                self.__vertex_list.append(new_ver)
            
            for i in range(0, length - 1):
                new_edge = Edge()
                new_edge.set_street(street_name)
                j = i + templen
                new_edge.set_vertex1(self.__vertex_list[j])
                new_edge.set_vertex2(self.__vertex_list[j+1])
                self.__edges_list.append(new_edge)
        else:
            print "Error: street has already been added"

        return

    def remove_street(self,street_name):
        contained = False
        for i in self.__vertex_list:
            if(street_name == i.get_street()):
                contained = True
                break
            
        if(contained):
            self.__vertex_list[:] = [i for i in self.__vertex_list if i.get_street() != street_name]
            self.__edges_list[:] = [i for i in self.__edges_list if i.get_street() != street_name]
        else:
            print "Error: street does not exist"
            
        return

    def change_street(self, street_name, coor):
        self.remove_street(street_name)
        self.add_street(street_name, coor)
        return

    def generate_graph(self):
        self.__add_intersections()
        raw_vertices = self.__generate_edges()
        vertices = self.__generate_vertices(raw_vertices)
        print "V = {"
        for i in vertices:
            print str(i.get_ID()) + ":" + " (" + "%g" % float(i.get_xcoor()) + "," + "%g" % float(i.get_ycoor()) + ")"
        print "}"
        
        print "E = {"
        for i in self.__updated_edges_list:
            print "<" + str(i.get_vertex1().get_ID()) + "," + str(i.get_vertex2().get_ID()) + ">,"
        print "}"
        return