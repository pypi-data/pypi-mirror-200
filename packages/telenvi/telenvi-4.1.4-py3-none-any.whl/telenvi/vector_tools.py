module_description = """
--- telenvi.vector_tools ---
Functions to process vector geo data through geopandas
"""

# Geo libraries
import shapely
import pandas as pd
import geopandas as gpd

def getGeoThing(target):
    """
    Return a shapely.geometry object from different cases 
    """

    try :
        _ = target.coords
        return target
    except AttributeError:
        pass

    if type(target) in [pd.Series, gpd.GeoSeries]:
        geoLine = target.geometry

    elif type(target) in [gpd.GeoDataFrame, pd.DataFrame]:
        geoLine = target.iloc[0].geometry

    elif type(target) == str:
        geoLine = gpd.read_file(target).iloc[0].geometry

    return geoLine