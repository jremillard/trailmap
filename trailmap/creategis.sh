# current user needs to be "postgres" super user. 
createdb gis
createlang plpgsql gis
psql -d gis -f /usr/share/postgresql/8.4/contrib/postgis-1.5/postgis.sql
psql -d gis -f /usr/share/postgresql/8.4/contrib/postgis-1.5/spatial_ref_sys.sql 

