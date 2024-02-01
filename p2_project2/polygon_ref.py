import math
from numbers import Real
from typing import Self
import sys

class Polygon:
    def __init__(self, edges: int, circumradius: Real) -> None:
        if isinstance(edges, int) and edges > 2:
            self._edges = edges
        else:
            raise ValueError('Edges must be an integer number greater than 2')
        if isinstance(circumradius, Real) and circumradius > 0:
            self._circumradius = circumradius
        else:
            raise ValueError('Circumradius must be a number greater than 0')
        
        self._vertices = self._edges
        self._interior_angle = (self._edges - 2) * (180 / self._edges)
        self._apothem = self._circumradius * math.cos(math.pi / self._edges)
        self._edge_length = 2 * self._circumradius * math.sin(math.pi / self._edges)
        self._area = 0.5 * self._edges * self._edge_length * self._apothem
        self._perimeter = self._edges * self._edge_length

    @property
    def edges(self):
        return self._edges
    
    @property
    def vertices(self):
        return self._vertices
    
    @property
    def interior_angle(self):
        return self._interior_angle
    
    @property
    def apothem(self):
        return self._apothem
    
    @property
    def edge_length(self):
        return self._edge_length
    
    @property
    def area(self):
        return self._area
    
    @property
    def perimeter(self):
        return self._perimeter
    
    def __repr__(self):
        return f'Polygon(edges={self._edges}, circumradius={self._circumradius})'
    
    def __eq__(self, other: Self):
        # if isinstance(other, Polygon):
        if isinstance(other, self.__class__):
            return self._edges == other._edges and self._circumradius == other._circumradius
        else:
            # raise TypeError(f"'==' not supported between instances of 'Polygon' and {type(other).__name__!r}")
            return NotImplemented
        
    def __gt__(self, other: Self):
        # if isinstance(other, Polygon):
        if isinstance(other, self.__class__):
            return self._vertices > other._vertices
        else:
            # raise TypeError(f"'>' not supported between instances of 'Polygon' and {type(other).__name__!r}")
            return NotImplemented
        

class PolygonSequence:
    def __init__(self, max_vertices: int, common_circumradius: Real) -> None:
        self._max_efficient_polygon = Polygon(max_vertices, common_circumradius)
        self._max_vertices = max_vertices
        self._common_circumradius = common_circumradius
    
    @property
    def max_efficient_polygon(self):
        return self._max_efficient_polygon
    
    def __repr__(self) -> str:
        return f'PolygonSequence(max_vertices={self._max_vertices}, common_circumradius={self._common_circumradius})'
    
    def __len__(self):
        return self._max_vertices - 2
    
    def __getitem__(self, index: int) -> Self:
        actual_vertices = index + 3
        if actual_vertices > self._max_vertices:
            raise IndexError('PolygonSequence object index out of range')
        else:
            return Polygon(actual_vertices, self._common_circumradius)
            

if __name__ == '__main__':
    def test_polygon():

        try:
            Polygon(2, 10)
            assert False, 'Creating a polygon with 2 sides'
        except ValueError:
            pass

        try:
            Polygon(3, -10)
            assert False, 'Creating a polygon with negative edge length'
        except ValueError:
            pass

        edges = 3
        circumradius = 10
        poly1 = Polygon(edges, circumradius)
        assert str(poly1) == 'Polygon(edges=3, circumradius=10)', f'actual: {str(poly1)}'
        assert poly1.edges == 3, (f'actual: {poly1.edges}, ' # separate f-string on multiple lines
                                  f'expected: {edges}')
        assert poly1.vertices == 3, f'actual: {poly1.vertices}, expected: {edges}'
        assert poly1.interior_angle == 60, f'actual: {poly1.interior_angle}, expected: 60'
        assert math.isclose(poly1.apothem, 5.0, rel_tol=sys.float_info.epsilon,
                            abs_tol=sys.float_info.epsilon), (f'actual {poly1.apothem}', f'expected: 5.0')
        assert poly1.edge_length == 2 * circumradius * math.sin(math.pi / edges), f'actual: {poly1.edge_length}'
        assert poly1.perimeter == 2 * circumradius * math.sin(math.pi / edges) * edges, f'actual: {poly1.perimeter}'
        assert poly1.area == circumradius ** 2 * math.sin(math.pi / edges) * \
            math.cos(math.pi / edges) * edges, f'actual: {poly1.area}'
        poly2 = Polygon(3, 10)
        assert poly1 == poly2
        poly3 = Polygon(4, 5)
        assert poly1 < poly3
        assert poly1 != poly3
        assert not (poly1 == '3') # the result is False
        # poly1 > 3

    test_polygon()

    polies = PolygonSequence(10, 10)
    print(polies)
    print(len(polies))
    print(polies.max_efficient_polygon)
    for poly in polies:
        print(poly)

    try:
        PolygonSequence(2, 10)
        assert False, 'Creating polygon sequece with max edges less than 3'
    except ValueError:
        pass

polies = PolygonSequence(1000, 1)

for p in polies:
    print(p.area) # the area is getting close to pi when edges getting bigger
