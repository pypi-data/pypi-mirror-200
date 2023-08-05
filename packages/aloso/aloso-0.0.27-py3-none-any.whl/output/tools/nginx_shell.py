import logging
from patchwork.files import exists

from fabric import Connection, Config
import config
from domain.tools.nginx import Nginx


class NginxShell(Nginx):

    @staticmethod
    def connection():
        configuration = Config(overrides={'user': config.nginx_username,
                                          'port': config.nginx_port,
                                          'sudo': {'password': config.nginx_password},
                                          'connect_kwargs': {'password': config.nginx_password}})
        try:
            conn = Connection(host=config.nginx_host, config=configuration)
            return conn
        except Exception as e:
            logging.error(f"Erreur de connexion au serveur : {e}")

    @staticmethod
    def install_nginx(app_name: str = "portail"):
        conn = NginxShell.connection()

        conn.put(config.nginx_config_file, app_name)

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

        commands = [
            f'mkdir /var/www/{app_name}',
            f"mv {config.nginx_front_build_dir} /var/www/{app_name}",
            f"cp {app_name} /etc/nginx/sites-available",
            f"ln -s /etc/nginx/sites-available/{app_name} /etc/nginx/sites-enabled",
            f"rm /etc/nginx/sites-enabled/default",
            'sudo systemctl restart nginx']

        try:
            conn.run("nginx -v")
            for command in commands:
                if config.use_sudo:
                    conn.sudo(command)
                else:
                    conn.run(command)
        except Exception as e:
            conn.run("apt update")
            conn.run("apt install nginx -y")


# Edit /etc/nginx/sites-enabled/default and comment IPv6 out:
# listen [::]:80 default_server;
# https://askubuntu.com/questions/764222/nginx-installation-error-in-ubuntu-16-04

if __name__ == "__main__":
    ng = NginxShell()
    ng.install_nginx()
