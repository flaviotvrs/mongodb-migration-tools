var database = '<database>'; 
var collection = '<collection>'; 
var dict = {}; 
db.getMongo().getDB(database).getCollectionNames().forEach(function (col) { 
    if (collection == '' || collection == col) { 
        dict[col] = db.getMongo().getDB(database).getCollection(col).countDocuments({}); 
    } 
}); 
print(JSON.stringify(dict));