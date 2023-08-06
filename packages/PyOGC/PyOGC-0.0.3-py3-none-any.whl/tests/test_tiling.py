from PyOGC.TilingSchemes.schemes import TilesAPI

class TestTilesAPI:
    def test_get_tile_matrix_sets(self):
        api = TilesAPI()
        response = api.get_tile_matrix_sets()
        assert isinstance(response, dict)
        assert "tileMatrixSets" in response
        
    def test_get_tile_matrix_set(self):
        api = TilesAPI()
        response = api.get_tile_matrix_set("CDB1GlobalGrid")
        assert isinstance(response, dict)
        assert response["id"] == "CDB1GlobalGrid"
