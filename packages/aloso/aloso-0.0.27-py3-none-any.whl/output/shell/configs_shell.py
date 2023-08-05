import logging
import codecs
import hashlib
import os

from Crypto.Cipher import AES
import config

from domain.configs_management import ConfigsManagement


class ConfigsShell(ConfigsManagement):

    def edit_variable(self):
        try:
            with open(self.config_file_path, 'r+') as file:
                lines = file.readlines()
                variables_names = [line.split('=')[0].strip() for line in lines]

                if self.variable_name not in variables_names:
                    logging.error(
                        f'La variable {self.variable_name} n\'existe pas dans le fichier {self.config_file_path}')
                    return

                for index, line in enumerate(lines):
                    if self.variable_name in line.strip():
                        if isinstance(self.variable_value, int):
                            lines[index] = f'{self.variable_name} = {self.variable_value}\n'
                        else:
                            lines[index] = f'{self.variable_name} = "{self.variable_value}"\n'
                        break

                file.seek(0)
                file.writelines(lines)
                file.truncate()
            logging.info(f'La variable {self.variable_name} a été modifiée avec succès')

        except Exception as e:
            logging.error(f'Une erreur est survenue lors de la modification de la variable {self.variable_name} : {e}')

    @staticmethod
    def salt(salt_p):
        salt_phrase = f"$2a$12$/qzser"
        hashed_salt = hashlib.pbkdf2_hmac(hash_name='sha512', password=salt_p.encode('utf-8'),
                                          salt=salt_phrase.encode('utf-8'), iterations=100000)
        salt_hash = codecs.encode(hashed_salt, "base64")
        return salt_hash

    @staticmethod
    def salt_file_content(list_data: list[str] == []):
        file_name = "salt"
        key = ConfigsShell.salt(config.cchottsa_herbenv)[0:32]
        initial_vector = b'o\xa59\x8f\xeaf\xdc\xa477\xa1\xcfg\x87Ip'
        cipher = AES.new(key, AES.MODE_OFB, initial_vector)
        if list_data:
            ciphertext = cipher.encrypt(str.encode("\n".join(list_data)))
        else:
            with open(f"{config.data_dir}/salt/{file_name}", "rb") as file:
                plaintext = file.read()
                ciphertext = cipher.encrypt(plaintext)
            # os.system(f"rm {config.data_dir}/salt/{file_name}")
        with open(f"{config.salt_file}", "wb") as file:
            file.write(ciphertext)

    @staticmethod
    def get_salt_content():
        key = ConfigsShell.salt(config.cchottsa_herbenv)[0:32]
        initial_vector = b'o\xa59\x8f\xeaf\xdc\xa477\xa1\xcfg\x87Ip'
        cipher = AES.new(key, AES.MODE_OFB, initial_vector)
        with open(f"{config.salt_file}", "rb") as file:
            ciphertext = file.read()
            plaintext = cipher.decrypt(ciphertext)
            our_salt = bytes.decode(plaintext)
        return our_salt

    @staticmethod
    def generate_salt():
        our_salt = ConfigsShell.get_salt_content()
        with open(f"{config.clear_salt}", "w") as file:
            file.write(our_salt)

    @staticmethod
    def desalt_file_content():
        our_salt = ConfigsShell.get_salt_content()
        for salts in our_salt.split('\n'):
            if salts.startswith(config.salted_name):
                # print(salts.split(' = ')[1])
                pass
            print(salts)

    @staticmethod
    def get_value(variable: str):
        our_salt = ConfigsShell.get_salt_content()
        for salts in our_salt.split('\n'):
            if salts.split(' = ')[0] == variable:
                return salts.split(' = ')[1]
        return None

    @staticmethod
    def delete_salt(salted_name: str):
        print(f'delete {salted_name}')
        our_salt = ConfigsShell.get_salt_content()
        list_salt = our_salt.split('\n')
        new_list = []
        for salts in list_salt:
            if not salts.split(' = ')[0] == salted_name:
                new_list.append(salts)
        ConfigsShell.salt_file_content(new_list)

    @staticmethod
    def update_salt(name: str, value: str):
        print(f'update {name}, value = {value}')
        our_salt = ConfigsShell.get_salt_content()
        list_salt = our_salt.split('\n')
        new_list = []
        for salts in list_salt:
            if salts.split(' = ')[0] == name:
                new_salts = f"{name} = {value}"
                new_list.append(new_salts)
            else:
                new_list.append(salts)
        ConfigsShell.salt_file_content(new_list)


if __name__ == '__main__':
    '''ConfigsShell.salt_file_content(list_data=None)
    ConfigsShell.desalt_file_content()
    ConfigsShell.update_salt('salt 1', '122222222222222222221')
    ConfigsShell.delete_salt('salt_1')
    ConfigsShell.desalt_file_content()
    
    print(ConfigsShell.get_value('salt 1'))
    '''
    ConfigsShell.generate_salt()
