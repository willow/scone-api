from django.contrib.gis.geos import Point, Polygon, MultiPolygon


def points_resides_in_bounds(points, distance_buffer, *polygons):
  polygons = [Polygon(polygon) for polygon in polygons]

  multi = MultiPolygon(polygons)

  #get the distance in meters
  #more info on units: https://groups.google.com/forum/#!topic/geodjango/EXVIU5Ik0ZQ
  multi = multi.buffer(distance_buffer / 1000.0)

  prep_multi = multi.prepared

  ret_val = [k for k, v in list(points.items()) if prep_multi.contains(Point(v[0], v[1]))]

  return ret_val
