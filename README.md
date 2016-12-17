## earcut-python

A pure Python port of the earcut JavaScript triangulation library. The latest version is based off of the earcut 2.1.1 release, and is functionally identical.

The original project can be found here:
https://github.com/mapbox/earcut

#### Usage

```python
triangles = earcut([10,0, 0,50, 60,60, 70,10]) # Returns [1,0,3, 3,2,1]
```

Signature: `earcut(vertices[, holes, dimensions = 2])`.

* `vertices` is a flat array of vertex coordinates like `[x0,y0, x1,y1, x2,y2, ...]`.
* `holes` is an array of hole _indices_ if any
  (e.g. `[5, 8]` for a 12-vertex input would mean one hole with vertices 5&ndash;7 and another with 8&ndash;11).
* `dimensions` is the number of coordinates per vertex in the input array (`2` by default).

Each group of three vertex indices in the resulting array forms a triangle.

```python
# Triangulating a polygon with a hole
earcut([0,0, 100,0, 100,100, 0,100,  20,20, 80,20, 80,80, 20,80], [4])
# [3,0,4, 5,4,0, 3,4,7, 5,0,1, 2,3,7, 6,5,1, 2,7,6, 6,1,2]

# Triangulating a polygon with 3d coords
earcut([10,0,1, 0,50,2, 60,60,3, 70,10,4], null, 3)
# [1,0,3, 3,2,1]
```

If you pass a single vertex as a hole, Earcut treats it as a Steiner point.

If your input is a multi-dimensional array, you can convert it to the format expected by Earcut with `earcut.flatten`:

```python
# The first sequence of vertices is treated as the outer hull, the following sequneces are treated as holes.
data = earcut.flatten([[(0,0), (100,0), (100,100), (0,100)], [(20,20), (80,20), (80,80), (20,80)]])
triangles = earcut(data['vertices'], data['holes'], data['dimensions'])
```

After getting a triangulation, you can verify its correctness with `earcut.deviation`:

```python
deviation = earcut.deviation(vertices, holes, dimensions, triangles)
```

Returns the relative difference between the total area of triangles and the area of the input polygon.
`0` means the triangulation is fully correct.