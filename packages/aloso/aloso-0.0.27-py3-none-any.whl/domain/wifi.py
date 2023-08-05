import logging
from dataclasses import dataclass

import config

logging.basicConfig(level=config.debug_level,
                    format='%(asctime)s %(levelname)s %(pathname)s %(funcName)s %(lineno)d : %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename=config.logs_file_path,
                    filemode='a')


@dataclass
class Wifi:
    building: str = ""

    @staticmethod
    def connection():
        pass

    @staticmethod
    def get_buildings():
        buildings_list = [{"name": "Batiment 1", "state": False},
                          {"name": "Batiment 2", "state": True},
                          {"name": "Batiment 3", "state": True},
                          {"name": "Batiment 4", "state": False},
                          {"name": "Batiment 5", "state": True},
                          {"name": "Batiment 6", "state": False},
                          {"name": "Batiment 7", "state": True},
                          {"name": "Batiment 8", "state": False},
                          {"name": "Batiment 9", "state": True},
                          {"name": "Batiment 10", "state": False},
                          {"name": "Batiment 11", "state": True},
                          {"name": "Batiment 12", "state": False}]

        return buildings_list

    def execute(self, *args):
        pass
