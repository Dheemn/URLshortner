from ..src.database import get_database
from ..src.path import PathManager


class TestPath:

    def __init__(self) -> None:
        # Create database object, PathManager class instance and test its
        # methods
        db_details = {
            'dbType': 'sqlite',
            'dbLoc': ':memory:',
        }
        db_object = get_database(db_details)
        self.path_manager = PathManager(database_object=db_object)

    def test_path_generator(self):
        for i in range(5):
            path = self.path_manager.path_gen()
            assert len(path) == 6
