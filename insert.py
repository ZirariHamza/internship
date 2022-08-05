import os, sys
from sqlalchemy import create_engine
import geopandas as gpd
import pandas as pd

password = input("Database password : ")
engine = create_engine('postgresql://'+ sys.argv[2] + ':' + password +'@' + sys.argv[4] +':' + sys.argv[5] + '/' + sys.argv[3])
os.system(r"set PGPASSWORD=" + password)

for file in os.listdir(sys.argv[1]):
    if file.endswith(".tif"):
        name = file.split(".tif")[0]
        raster = os.path.join(sys.argv[1], file)
        print(raster)
        os.system(r'"C:\Program Files\PostgreSQL\14\bin\raster2pgsql.exe" -s 4326 -I -M -C ' + raster + ' -F | psql -d postgis -h localhost -U postgres -p 5432')

    if file.endswith(".shp"):
        name = file.split(".shp")[0]
        shape = os.path.join(sys.argv[1], file)
        shapeFile = gpd.read_file(shape)
        shapeFile.to_postgis('boundary', engine, index=True, index_label='Index')

    if file.endswith(".xlsx"):
        name = file.split(".xlsx")[0]
        excel = os.path.join(sys.argv[1], file)
        df = pd.read_excel(excel)
        df.to_sql(
            name,
            engine
        )

    if file.endswith(".csv"):
        name = file.split(".csv")[0]
        csv = os.path.join(sys.argv[1], file)
        df = pd.read_csv(csv)
        df.to_sql(
            name,
            engine
        )