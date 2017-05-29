from __init__ import *
from fileHandling_functions import *
#
from shapely.geometry import Polygon
from shapely.geometry.multipolygon import MultiPolygon
from geopy.distance import VincentyDistance
import geopandas as gpd
import csv

NORTH, EAST, SOUTH, WEST = 0, 90, 180, 270


def get_sgMainBorder():
    ofpath = path_merge(geo_dpath, 'sgMainBorder.pkl')
    if check_path_exist(ofpath):
        sgBorder = load_pickle_file(ofpath)
        return sgBorder
    ifpath = path_merge(geo_dpath, 'sgMainBorder_manually.csv')
    sgMainBorder = []
    with open(ifpath, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        header = reader.next()
        hid = {h: i for i, h in enumerate(header)}
        for row in reader:
            lon, lat = map(eval, [row[hid[cn]] for cn in ['longitude', 'latitude']])
            sgMainBorder += [(lon, lat)]
    save_pickle_file(ofpath, sgMainBorder)
    return sgMainBorder


def get_sgBorder():
    ofpath = path_merge(geo_dpath, 'sgBorder.pkl')
    if check_path_exist(ofpath):
        sgBorder = load_pickle_file(ofpath)
        return sgBorder
    ifpath = path_merge(geo_dpath, 'singapore_admin.geojson')
    df = gpd.read_file(ifpath)
    sgBorder = list(df.ix[0].geometry.exterior.coords)
    save_pickle_file(ofpath, sgBorder)
    return sgBorder


def get_sgRoads():
    ofpath = path_merge(geo_dpath, 'sgRoads.pkl')
    if check_path_exist(ofpath):
        sgRoads = load_pickle_file(ofpath)
        return sgRoads
    ifpath = path_merge(geo_dpath, 'singapore_roads.geojson')
    df = gpd.read_file(ifpath)
    sgBorder = Polygon(get_sgBorder())
    sgRoads = []
    for r, n in df.loc[:, ('geometry', 'name')].values:
        if r.within(sgBorder):
            sgRoads += [(n, list(r.coords))]
    save_pickle_file(ofpath, sgRoads)
    return sgRoads


def get_sgBuildings():
    ofpath = path_merge(geo_dpath, 'sgBuildings.pkl')
    if check_path_exist(ofpath):
        sgBuildings = load_pickle_file(ofpath)
        return sgBuildings
    ifpath = path_merge(geo_dpath, 'singapore_buildings.geojson')
    df = gpd.read_file(ifpath)
    sgBorder = Polygon(get_sgBorder())
    sgBuildings = []
    for b, n, t in df.loc[:, ('geometry', 'name', 'type')].values:
        if n == None and t == None:
            continue
        if b.within(sgBorder):
            if type(b) == MultiPolygon:
                for p in b:
                    sgBuildings += [(n, list(p.exterior.coords))]
            else:
                sgBuildings += [(n, list(b.exterior.coords))]
    save_pickle_file(ofpath, sgBuildings)
    return sgBuildings


def get_sgGrid():
    ofpath = path_merge(geo_dpath, 'sgGrid(%.1fkm).pkl' % ZONE_UNIT_KM)
    if check_path_exist(ofpath):
        sgGrid = load_pickle_file(ofpath)
        return sgGrid
    #
    min_lon, max_lon = 1e400, -1e400,
    min_lat, max_lat = 1e400, -1e400
    sgMainBorder = get_sgMainBorder()
    for lon, lat in sgMainBorder:
        min_lon, max_lon = min(min_lon, lon), max(max_lon, lon)
        min_lat, max_lat= min(min_lat, lat), max(max_lat, lat)
    #
    lons, lats = [], []
    mover = VincentyDistance(kilometers=ZONE_UNIT_KM)
    x = min_lon
    while x < max_lon:
        lons.append(x)
        p0 = [min_lat, x]
        moved_point = mover.destination(point=p0, bearing=EAST)
        x = moved_point.longitude
    y = min_lat
    while y < max_lat:
        lats.append(y)
        p0 = [y, min_lon]
        moved_point = mover.destination(point=p0, bearing=NORTH)
        y = moved_point.latitude
    save_pickle_file(ofpath, [lons, lats])
    return lons, lats


if __name__ == '__main__':
    print len(get_sgRoads())
    print len(get_sgBuildings())
    # print get_sgMainBorder()[:2]
    # print get_sgBorder()[:2]
    # print get_sgRoads()[:2]
    lons, lats =  get_sgGrid()
    print lats