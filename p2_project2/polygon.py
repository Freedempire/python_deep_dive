from numbers import Real
import math
from typing import Self

class Polygon:
    def __init__(self, edges: int, circumradius: Real):
        if isinstance(edges, int) and edges > 2:
            self._edges = edges
        else:
            raise ValueError('edges must be an integer greater than 2')
        if isinstance(circumradius, Real) and circumradius > 0:
            self._circumradius = circumradius
        else:
            raise ValueError('circumradius must be a number greater than 0')
        # self._vertices = self._edges
        self._interior_angle = None
        self._apothem = None
        self._edge_length = None
        self._area = None
        self._perimeter = None
        
    @property
    def edges(self):
        return self._edges
    
    @property
    def circumradius(self):
        return self._circumradius
    
    @property
    def vertices(self):
        return self._edges
    
    @property
    def interior_angle(self):
        if self._interior_angle is None:
            self._interior_angle = (self._edges - 2) * (180 / self._edges)
        return self._interior_angle
    
    @property
    def apothem(self):
        if self._apothem is None:
            self._apothem = math.cos(math.pi / self._edges) * self._circumradius
        return self._apothem
    
    @property
    def edge_length(self):
        if self._edge_length is None:
            self._edge_length = 2 * math.sin(math.pi / self._edges) * self._circumradius
        return self._edge_length
    
    @property
    def area(self):
        if self._area is None:
            self._area = 0.5 * self.apothem * self.edge_length * self._edges
        return self._area
    
    @property
    def perimeter(self):
        if self._perimeter is None:
            self._perimeter = self._edges * self.edge_length
        return self._perimeter
    
    def __repr__(self):
        return f'Polygon(edges={self._edges}, circumradius={self._circumradius})'
    
    def __eq__(self, other: Self):
        if isinstance(other, self.__class__):
            return self._edges == other._edges and self._circumradius == other._circumradius
        else:
            # return False
            return NotImplemented
        
    def __lt__(self, other: Self):
        if isinstance(other, self.__class__):
            if self._circumradius == other._circumradius:
                return self._edges < other._edges
            else:
                return self.area < other.area
        else:
            raise TypeError(f"'<' not supported between instances of 'Polygon' and {type(other).__name__!r}")


class Polygons:
    def __init__(self, max_edges: int, common_circumradius: Real):
        # validate max_edges and common_circumradius by try to create a polygon with these values
        # try:
        #     Polygon(max_edges, common_circumradius)
        # except:
        #     raise
        # self._max_edges = max_edges
        # self._common_circumradius = common_circumradius

        # validate arguments the same way as in Polygon
        if isinstance(max_edges, int) and max_edges > 2:
            self._max_edges = max_edges
        else:
            raise ValueError('max_edges must be an integer greater than 2')
        if isinstance(common_circumradius, Real) and common_circumradius > 0:
            self._common_circumradius = common_circumradius
        else:
            raise ValueError('common_circumradius must be a number greater than 0')
        self._max_efficient_polygon = None # polygon with the highest area/perimeter ratio

    @property
    def max_edges(self):
        return self._max_edges
    
    @property
    def common_circumradius(self):
        return self._common_circumradius
    
    @property
    def max_efficient_polygon(self):
        if self._max_efficient_polygon is None:
            sorted_polygons = sorted(self, key=lambda x: x.area / x.perimeter)
            self._max_efficient_polygon = sorted_polygons[-1] if sorted_polygons else None
        return self._max_efficient_polygon
    
    def __len__(self):
        return self._max_edges - 2
    
    def __repr__(self):
        return f'Polygons(max_edges={self._max_edges}, common_circumradius={self._common_circumradius})'
    
    def __iter__(self):
        return self.PolygonsIterator(self._max_edges, self._common_circumradius)
    
    def __reversed__(self):
        return self.PolygonsIterator(self._max_edges, self._common_circumradius, True)
    
    class PolygonsIterator:
        def __init__(self, max_edges, common_circumradius, reverse=False):
            self.max_edges = max_edges
            self.common_circumradius = common_circumradius
            if reverse:
                self.current_edges = max_edges
                self.step = -1
            else:
                self.current_edges = 3
                self.step = 1

        def __iter__(self):
            return self
        
        def __next__(self):
            if self.current_edges > self.max_edges or self.current_edges < 3:
                raise StopIteration
            else:
                polygon = Polygon(self.current_edges, self.common_circumradius)
                self.current_edges += self.step
                return polygon


poly = Polygon(3, 10)
print(f'{poly=}')
print(f'{poly.edges=}')
print(f'{poly.vertices=}')
print(f'{poly.circumradius=}')
print(f'{poly.interior_angle=}')
print(f'{poly.apothem=}')
print(f'{poly.edge_length=}')
print(f'{poly.area=}')
print(f'{poly.perimeter=}')

polys = Polygons(10, 10)
print(f'{polys=}')
print(f'{len(polys)=}')
print(f'{polys.max_edges=}')
print(f'{polys.common_circumradius=}')
print(f'{polys.max_efficient_polygon=}')
print(list(polys))
print(list(reversed(polys)))
