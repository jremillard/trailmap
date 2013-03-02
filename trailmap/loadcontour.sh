# 3.048 is 10 feet in meters, make shape file from contour tiff
gdal_contour -a elev -i 3.048 ../srcdata/43485076/43485076.tif 43485076/43485076_1.shp
ogr2ogr -t_srs 900913 ../srcdata/43485076/contours.shp 43485076/43485076_1.shp
shp2pgsql -s 900913 -I -d ../srcdata/43485076/contours.shp | psql -d gis
