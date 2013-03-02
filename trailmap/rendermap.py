#!/usr/bin/env python

from mapnik import *

town_to_map = 'Groton'
backgroundColor = Color('#E0E0E0')
trailColor = Color( "green")
colorOfWater = Color('#BBCCFF')

# handle scaling
# figure out tiles
# key
# render loop trail differently
# show a bit of land around groton

def makeTrailStyle(m,mapScale) :

  s = Style()


  r = Rule()
  r.filter = Filter("[highway]='path'")
  line = LineSymbolizer(trailColor,2.0*mapScale)
  stroke = line.stroke
  stroke.line_join = line_join.ROUND_JOIN
  line.stroke = stroke
  r.symbols.extend([line  ] )
  s.rules.append(r)

  r = Rule()
  r.filter = Filter("[highway]='cycleway'")
  line = LineSymbolizer(trailColor,2.0*mapScale)
  stroke = line.stroke
  stroke.line_join = line_join.ROUND_JOIN
  stroke.add_dash(6,3)
  line.stroke = stroke
  r.symbols.extend([line  ] )
  s.rules.append(r)

  r = Rule()
  r.filter = Filter("[highway]='path' and [bridge]='yes'")
  r.symbols.extend([ LineSymbolizer(Color('black'),3*mapScale) ] )
  r.symbols.extend([ LineSymbolizer(trailColor,1*mapScale) ] )
  s.rules.append(r)

  #r = Rule()
  #r.filter = Filter("[highway]='path' and [ford]='yes'")
  #r.symbols.extend([ LineSymbolizer(Color('blue'),3*mapScale) ] )
  #r.symbols.extend([ LineSymbolizer(Color('white'),1*mapScale) ] )
  #s.rules.append(r)

  r = Rule()
  r.filter = Filter("[highway]='path' and [access]!='yes'")

  line = LineSymbolizer(Color('red'),1*mapScale);
  stroke = line.stroke
  stroke.add_dash(4,4)
  line.stroke = stroke
  r.symbols.extend([ line ] )
  s.rules.append(r)

  r = Rule()
  r.filter = Filter("[highway]='track'")
  line = LineSymbolizer(trailColor,3*mapScale);
  stroke = line.stroke
  stroke.add_dash(3,3)
  line.stroke = stroke
  r.symbols.extend([line])
  r.symbols.extend([ LineSymbolizer(Color('white'),1*mapScale) ])
  s.rules.append(r)

  r = Rule()
  r.filter = Filter("[ford]='yes'")
  line = LinePatternSymbolizer( 'ford.png','png',20,20)
  r.symbols.extend([line])
  s.rules.append(r)

  m.append_style('trails',s)

  s = Style()
  r = Rule()
  t = TextSymbolizer( "name","DejaVu Sans Book",6*mapScale,Color('black'))
  t.label_placement = label_placement.LINE_PLACEMENT
  t.label_spacing = 200 * mapScale
  t.halo_radius = 2
  r.symbols.extend([t])
  s.rules.append(r)
  m.append_style('trails_l',s)


def makeRoadStyle(m,mapScale) :
  s = Style()

  r = Rule()
  r.symbols.extend([ LineSymbolizer(Color("black"),0.2*mapScale) ])
  s.rules.append(r)

  r = Rule()
  r.filter = Filter("[highway]='footway'")
  line = LineSymbolizer(trailColor,0.7*mapScale)
  stroke = line.stroke
  stroke.line_join = line_join.ROUND_JOIN
  stroke.add_dash(4,2)
  line.stroke = stroke
  r.symbols.extend([line  ] )
  s.rules.append(r)

  # make the major roads a bit thicker, give them labels
  r = Rule()
  r.filter = Filter("[highway]='secondary'")
  r.symbols.extend([ LineSymbolizer(Color("black"),2*mapScale) ])
  s.rules.append(r)

  m.append_style('roads',s)

  s = Style()
  r = Rule()
  r.filter = Filter("[highway]='secondary'")
  t = TextSymbolizer( "name","DejaVu Sans Book",6*mapScale,Color("black"))
  t.label_placement = label_placement.LINE_PLACEMENT
  t.halo_radius = 2
  r.symbols.extend([ t ])
  s.rules.append(r)
  m.append_style('roads_l',s)

  r = Rule()
  r.filter = Filter("[highway]='residential'")
  line =  LineSymbolizer(Color("black"),0.5*mapScale)
  t = TextSymbolizer( "name","DejaVu Sans Book",6*mapScale,Color("black"))
  t.label_placement = label_placement.LINE_PLACEMENT
  t.halo_radius = 2
  r.symbols.extend([ line, t ])
  s.rules.append(r)
  m.append_style('roads_close',s)


def makePowerlineStyle(m,mapScale) :
  line = LineSymbolizer(Color("black"),0.1*mapScale)
  s,r = Style(),Rule()
  r.filter = Filter("[power]='line'")
  t = TextSymbolizer( "shortname","DejaVu Sans Book",6*mapScale,Color('black'))
  t.label_placement = label_placement.LINE_PLACEMENT
  t.label_spacing = mapScale * 100;

  r.symbols.extend([line,t])
  s.rules.append(r)
  m.append_style('powerline',s)

def makeBuildingStyle(m,mapScale) :
  s = Style()
  r = Rule()
  poly = PolygonSymbolizer(backgroundColor)
  line = LineSymbolizer(Color("black"),0.2)
  r.symbols.extend([poly,line])
  s.rules.append(r)
  m.append_style('building',s)

def makeElevationStyle(m,mapScale) :

  elevation_color = Color("#996633")
  s = Style()

  r = Rule()
  line = LineSymbolizer(elevation_color,0.1*mapScale)
  r.symbols.extend([line])
  s.rules.append(r)

  r = Rule()
  r.filter = Filter("[elevation_major] = 0")
  line = LineSymbolizer(elevation_color,0.2*mapScale)
  r.symbols.extend([line])
  s.rules.append(r)

  r = Rule()
  r.filter = Filter("[length] > 150")
  t = TextSymbolizer( "elevation_ft","DejaVu Sans Book",3*mapScale,elevation_color)
  t.label_placement = label_placement.LINE_PLACEMENT
  t.label_spacing = mapScale * 500

  r.symbols.extend([t])
  s.rules.append(r)

  m.append_style('elevation',s)


def makeTownStyle(m,mapScale) :
  poly = PolygonSymbolizer(backgroundColor)
  line = LineSymbolizer(Color('#B5B591'),1)
  s,r = Style(),Rule()
  r.symbols.extend([line,poly])
  s.rules.append(r)
  m.append_style('town',s)

def makeParkingStyle(m,mapScale) :
  s = Style()

  r = Rule()
  point = PointSymbolizer('parking.png','png',16,16)
  r.symbols.extend([point])
  s.rules.append(r)

  m.append_style('parking_p',s)

  s = Style()
  r = Rule()
  poly = PolygonSymbolizer(Color("#EEEEC1"))
  r.symbols.extend([poly])
  s.rules.append(r)

  m.append_style('parking',s)

def makePointsStyle(m,mapScale) :
  s = Style()

  r = Rule()
  r.filter = Filter("[barrier]='gate'")
  point = PointSymbolizer('gate.png','png',15,8)
  r.symbols.extend([point])
  s.rules.append(r)

  r = Rule()
  r.filter = Filter("[ford]='yes'")
  point = PointSymbolizer('ford.png','png',20,20)
  r.symbols.extend([point])
  s.rules.append(r)

  r = Rule()
  r.filter = Filter("[tourism]='camp_site'")
  point = PointSymbolizer('camp_site.png','png',20,20)
  r.symbols.extend([point])
  s.rules.append(r)

  m.append_style('point',s)

def makeConservationStyle(m,mapScale) :
  s = Style()

  r = Rule()
  poly = PolygonSymbolizer(Color('#B0CEB0'))
  line = LineSymbolizer(Color("#BFD9D9"),0.5)
  r.symbols.extend([poly,line])
  s.rules.append(r)
  m.append_style('conservation',s)

  s = Style()

  r = Rule()
  r.filter = Filter("[conservation_area] > 10000")
  t = TextSymbolizer( "name","DejaVu Sans Book",6*mapScale,Color('black'))
  t.wrap_width = 35*mapScale;
  r.symbols.extend([t])
  s.rules.append(r)

  m.append_style('conservation_l',s)

def makeRiverStyle(m,mapScale) :
  s = Style()

  r = Rule()
  r.filter = Filter("[waterway]='river'")
  line = LineSymbolizer(colorOfWater,mapScale)
  t = TextSymbolizer( "name","DejaVu Sans Book",6*mapScale,Color("black"))
  t.label_placement = label_placement.LINE_PLACEMENT
  #t.halo_radius = 2
  r.symbols.extend([ line, t ])

  s.rules.append(r)

  r = Rule()
  r.filter = Filter("[waterway]='stream'")
  line = LineSymbolizer(colorOfWater,mapScale)
  t = TextSymbolizer( "name","DejaVu Sans Book",4*mapScale,Color("black"))
  t.label_placement = label_placement.LINE_PLACEMENT
  #t.halo_radius = 2
  r.symbols.extend([ line, t ])
  s.rules.append(r)

  m.append_style('river',s)


def makeWaterStyle(m,mapScale) :
  s = Style()

  colorOfWetland = Color('#94FFD4')

  r = Rule()
  r.filter = Filter("[natural] = 'wetland'")
  line = LineSymbolizer( colorOfWetland,0.5)
  poly = PolygonPatternSymbolizer("wetland.png","png",40,20);
  r.symbols.extend([poly,line ])
  s.rules.append(r)

  r = Rule()
  r.filter = Filter("[waterway] = 'riverbank'")
  r.symbols.extend([ PolygonSymbolizer( colorOfWater) ])
  s.rules.append(r)

  r = Rule()
  r.filter = Filter("[natural]='water'")
  r.symbols.extend([ PolygonSymbolizer(colorOfWater)])
  s.rules.append(r)

  r = Rule()
  t = TextSymbolizer( "name","DejaVu Sans Book",10*mapScale,Color('black'))
  r.symbols.extend([t])
  s.rules.append(r)

  m.append_style('water',s)

def makeTrailLayer(m) :
  trails = Layer('trails')

  query = """ (
    select 
      ST_Intersection(planet_osm_polygon.way,planet_osm_line.way) as tway, 
      planet_osm_line.* 
     from 
      planet_osm_line, planet_osm_polygon 
    where 
      ST_Intersects(planet_osm_polygon.way,planet_osm_line.way) and 
      planet_osm_polygon.name = 'Groton' and 
      (planet_osm_line.highway = 'path' or planet_osm_line.highway = 'track' or planet_osm_line.highway = 'cycleway')
    ) as foo
   """

  trails.datasource = PostGIS(dbname='gis',table=query,geometry_field='tway',geometry_table='foo',extent_from_subquery=1)
  trails.styles.append('trails')
  trails.styles.append('trails_l')
  m.layers.append(trails)

def makePowerLineLayer(m) :
  trails = Layer('powerline')

  query = """ (
    select 
      ST_Intersection(planet_osm_polygon.way,planet_osm_line.way) as tway, 
      'Power Lines' as shortname,
      planet_osm_line.* 
     from 
      planet_osm_line, planet_osm_polygon 
    where 
      ST_Intersects(planet_osm_polygon.way,planet_osm_line.way) and 
      planet_osm_polygon.name = 'Groton' and 
      (planet_osm_line.power = 'line')
    ) as foo
   """

  trails.datasource = PostGIS(dbname='gis',table=query,geometry_field='tway',geometry_table='foo',extent_from_subquery=1)
  trails.styles.append('powerline')
  m.layers.append(trails)


def makeRoadLayer(m) :
  roads = Layer('roads')

  query = """ (
    select 
      ST_Intersection(planet_osm_polygon.way,planet_osm_line.way) as tway, 
      planet_osm_line.* 
     from 
      planet_osm_line, planet_osm_polygon 
    where 
      ST_Intersects(planet_osm_polygon.way,planet_osm_line.way) and 
      planet_osm_polygon.name = 'Groton' and 
      planet_osm_line.highway != '' and 
      planet_osm_line.highway != 'path' and 
      planet_osm_line.highway != 'track' 
    ) as foo
   """

  roads.datasource = PostGIS(dbname='gis',table=query,geometry_field='tway', extent_from_subquery=1);
  roads.styles.append('roads')
  roads.styles.append('roads_l')
  m.layers.append(roads)

def makeCloseRoadsLayer(m) :
  roads = Layer('close_roads')

  query = """ (
    select distinct
      ST_Intersection(town.way,road.way) as way,
      road.name,
      road.highway
     from 
      planet_osm_line as road, 
      planet_osm_line as trail, 
      planet_osm_polygon as town
    where 
      ST_Distance(road.way,trail.way) < 500 and 
      ST_Intersects(town.way,road.way) and 
      ST_Intersects(town.way,trail.way) and
      town.name = 'Groton' and 
      (trail.highway = 'track' or trail.highway = 'path' ) and
      road.highway = 'residential' and 
      road.name != ''
    ) as foo
   """

  roads.datasource = PostGIS(dbname='gis',table=query,geometry_field='way', extent_from_subquery=1);
  roads.styles.append('roads_close')
  m.layers.append(roads)

def makeRiverLayer(m) :

  river = Layer('river')

  query = """ (
    select 
      ST_Intersection(town.way,line.way) as tway, 
      line.* 
     from 
      planet_osm_line as line, planet_osm_polygon as town
    where 
      ST_Intersects(town.way,line.way) and 
      town.name = 'Groton' and 
      line.waterway != ''
    ) as foo
   """

  river.datasource = PostGIS(dbname='gis',table=query,geometry_field='tway', extent_from_subquery=1);
  river.styles.append('river')
  m.layers.append(river) 

def makeWaterLayer(m) :

  water = Layer('water')

  query = """ (
    select 
      ST_Intersection(town.way,poly.way) as tway, 
      poly.* 
     from 
      planet_osm_polygon as poly, planet_osm_polygon as town
    where 
      ST_Intersects(town.way,poly.way) and 
      town.name = 'Groton' and 
      (poly.natural = 'water' or poly.natural = 'wetland' or poly.waterway = 'riverbank' )
    ) as foo
   """

  water.datasource = PostGIS(dbname='gis',table=query,geometry_field='tway', extent_from_subquery=1);
  water.styles.append('water')
  m.layers.append(water) 

def makeElevationLayer(m) :
  elev = Layer('elevation')

  query = """ (
    select 
      ST_Intersection(town.way,contours.the_geom) as contour, 
      ST_Length( ST_Intersection(town.way,contours.the_geom) ) as length,
      (contours.elev * 3.28084)::integer % 50 as elevation_major,
      (contours.elev * 3.28084)::integer as elevation_ft
     from 
      contours, planet_osm_polygon as town
    where 
      ST_Intersects(town.way,contours.the_geom) and 
      town.name = 'Groton'
    ) as foo
   """

  elev.datasource = PostGIS(dbname='gis',table=query,geometry_field='contour', extent_from_subquery=1);
  elev.styles.append('elevation')
  m.layers.append(elev)

def makeConservationLandDataSource() :

  query = """ (
    select 
      ST_Intersection(town.way,poly.way) as tway, 
      ST_Area( ST_Intersection(town.way,poly.way)) as conservation_area,
      poly.* 
     from 
      planet_osm_polygon as poly, planet_osm_polygon as town
    where 
      ST_Intersects(town.way,poly.way) and 
      town.name = 'Groton' and 
      (poly.landuse = 'conservation' or 
       poly.landuse = 'forest' or 
       poly.leisure = 'recreation_ground' or 
       poly.leisure = 'nature_reserve' or 
       poly.leisure = 'park' )
    ) as foo
   """

  return PostGIS(dbname='gis',table=query,geometry_field='tway', extent_from_subquery=1);


def makeConservationLandLayer(m) :

  conservation = Layer('conservation')
  conservation.datasource = makeConservationLandDataSource()
  conservation.styles.append('conservation')
  m.layers.append(conservation)

def makeConservationLabelLayer(m) :

  conservation_ = Layer('conservation_l')
  conservation_.datasource = makeConservationLandDataSource()
  conservation_.styles.append('conservation_l')
  m.layers.append(conservation_)

def makeBuildingLayer(m) :
  conservation_ = Layer('building')

  query = """ (
    select 
      ST_Intersection(town.way,poly.way) as tway, 
      ST_Area( ST_Intersection(town.way,poly.way)) as conservation_area,
      poly.* 
     from 
      planet_osm_polygon as poly, planet_osm_polygon as town
    where 
      ST_Intersects(town.way,poly.way) and 
      town.name = 'Groton' and 
      (poly.building != '' or poly.leisure = 'pitch')
    ) as foo
   """

  conservation_.datasource = PostGIS(dbname='gis',table=query,geometry_field='tway', extent_from_subquery=1);
  conservation_.styles.append('building')
  m.layers.append(conservation_)


def makeParkingLayer(m) :
  parking = Layer('parking')

  query = """ (
    select 
      parking.* 
     from 
      planet_osm_polygon as parking, planet_osm_line as trail
    where 
      ST_Distance(parking.way,trail.way) < 10 and 
      parking.amenity = 'parking' and
      (trail.highway = 'track' or trail.highway = 'path' or trail.highway = 'cycleway')
    ) as foo
   """

  parking.datasource = PostGIS(dbname='gis',table=query,geometry_field='way', extent_from_subquery=1);
  parking.styles.append('parking')
  parking.styles.append('parking_p')
  m.layers.append(parking)
 

def makePointLayer(m) :
  points = Layer('points')

  query = """ (
    select 
      point.*
     from 
      planet_osm_point point,
      planet_osm_polygon as town
    where 
      ST_Intersects(town.way,point.way) and 
      town.name = 'Groton' and 
      (point.barrier = 'gate' or
       point.ford = 'yes' or 
       point.tourism = 'camp_site')
    ) as foo
   """

  points.datasource = PostGIS(dbname='gis',table=query,geometry_field='way',extent_from_subquery=1);
  points.styles.append('point')
  m.layers.append(points)

def makeTown(m) :
  town = Layer('town')

  query = """ (
    select 
      *
     from 
      planet_osm_polygon 
    where 
      planet_osm_polygon.name = 'Groton' 
    ) as foo
   """

  town.datasource = PostGIS(dbname='gis',table=query,geometry_field='way',extent_from_subquery=1);
  town.styles.append('town')
  m.layers.append(town)
  m.zoom_to_box(town.envelope())


for mapScale in range(3,4) :

  # Map
  widthInPixels = 4000*mapScale;
  m = Map(widthInPixels,int(widthInPixels*0.8))

  # Styles
  lineScale = mapScale;
  if ( lineScale > 2 ) : 
    lineScale = 2;
  makeTrailStyle(m,lineScale)
  makeRoadStyle(m,lineScale)
  makeTownStyle(m,mapScale)
  makeWaterStyle(m,mapScale)
  makeRiverStyle(m,mapScale) 
  makeConservationStyle(m,lineScale)
  makeTownStyle(m,mapScale)
  makeParkingStyle(m,mapScale)
  makeElevationStyle(m,mapScale)
  makePowerlineStyle(m,mapScale)
  makePointsStyle(m,mapScale)
  makeBuildingStyle(m,mapScale)

  # Layer
  makeTown(m)
  makeConservationLandLayer(m)
  makeElevationLayer(m)
  makeWaterLayer(m)
  makeRiverLayer(m)
  makeBuildingLayer(m)
  makeRoadLayer(m)
  makeTrailLayer(m)
  makeCloseRoadsLayer(m)
  makeParkingLayer(m)
  makePointLayer(m)
  makePowerLineLayer(m)
  makeConservationLabelLayer(m)

  # Render
  render_to_file(m, town_to_map + '_' + str(mapScale) + 'x.png')
  if( mapScale == 1 ) : 
    render_to_file(m, town_to_map + '.pdf');


