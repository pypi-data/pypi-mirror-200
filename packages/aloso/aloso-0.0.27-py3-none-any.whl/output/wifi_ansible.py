import logging

from fabric import Connection, Config

import config
from domain.wifi import Wifi


class WifiAnsible(Wifi):

    @staticmethod
    def connection():
        configuration = Config(overrides={'user': config.ansible_username,
                                          'port': config.ansible_port,
                                          'sudo': {'password': config.ansible_password}})
        try:
            conn = Connection(host=config.ansible_host, config=configuration)
            return conn
        except Exception as e:
            logging.error(f"Erreur de connexion au serveur : {e}")

    def execute(self, *args):
        conn = WifiAnsible.connection()
        inventory = args[0]
        playbook = args[1]
        self.building = args[2]

        cmd = f"ansible-playbook -i {inventory} {playbook} -e building='{self.building}'"

        try:
            conn.run(cmd)
            logging.info(f"Playbook {playbook} executé avec succès sur le batiment {self.building}")
        except Exception as e:
            logging.error(f"Erreur d'execution du playbook : {e} sur le batiment {self.building}")
