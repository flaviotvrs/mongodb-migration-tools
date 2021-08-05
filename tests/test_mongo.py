from mongo import MongoDb

def test_default(mocker):
    expected = { 
        "collection" : 100
    }

    def mock_load(self):
        return {
            "collection": 100
        }
    
    mocker.patch(
        "mongo.MongoDb.count_documents",
        mock_load
    )

    assert True
