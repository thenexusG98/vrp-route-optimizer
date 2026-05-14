```levantar en docker
docker run --name postgis -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgis/postgis
```

```insert en pg
INSERT INTO routes (vehicle_id, path_geom) 
VALUES (
    'V-001', 
    ST_MakeLine(ARRAY[ST_SetSRID(ST_MakePoint(-99.13, 19.43), 4326), ...])
);
```

```
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
```