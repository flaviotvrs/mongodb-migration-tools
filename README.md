# MongoDB Migration Tools

This tool allows you to copy a Mongo database from one cluster to another.

## Quick reference

* Maintained by: https://github.com/flaviotvrs/mongodb-migration-tools
* Where to address issues: https://github.com/flaviotvrs/mongodb-migration-tools/issues

### Built on top of
* MongoDB Shell: https://docs.mongodb.com/mongodb-shell/
* MongoDB Database Tools: https://docs.mongodb.com/database-tools/

## How to use this image

### The entire database
```
python main.py \  
    --origin  mongodb+srv://<username>:<password>@<host>:<port>/<database> \
    --destination mongodb+srv://<username>:<password>@<host>:<port>/<database>
```

### A single collection
```
python main.py \  
    --origin  mongodb+srv://<username>:<password>@<host>:<port>/<database> \
    --destination mongodb+srv://<username>:<password>@<host>:<port>/<database> \
    --collection <collection> \
    --override-database
```

### For help
```
python main.py -h
```