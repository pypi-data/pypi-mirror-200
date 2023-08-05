from domain.tools.frontend import Frontend
import logging
from fabric import Connection, Config
from patchwork.files import exists
import config


class FrontendShell(Frontend):

    @staticmethod
    def connection():
        configuration = Config(overrides={'user': config.frontend_username,
                                          'port': config.frontend_port,
                                          'sudo': {'password': config.frontend_password}})
        try:
            conn = Connection(host=config.frontend_host, config=configuration)
            return conn
        except Exception as e:
            logging.error(f"Erreur de connexion au serveur : {e}")

    @staticmethod
    def install():
        conn = FrontendShell.connection()

        if not exists(conn, ".nvm/versions/node/*"):
            conn.local(f"wget -qO- --no-check-certificate {config.nvm_wget_url} | bash")
            conn.local("source ~/.bashrc")
            conn.local("nvm install --lts")
            logging.info("Installation de nvm et nodejs")

        conn.local(f"unzip {config.frontend_zip_file} -d {config.frontend_project_dir}")
        conn.local(f"rm {config.frontend_zip_file}")
        conn.local(f"cd {config.frontend_project_dir} && npm install")
        conn.local(f"cd {config.frontend_project_dir} && npm run build")
        logging.info("Projet installé et lancé")
