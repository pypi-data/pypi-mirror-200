from datetime import datetime

import uvicorn
from fastapi import FastAPI, APIRouter, Response, status, Query
from ldap3 import Connection, Server
from starlette.middleware.cors import CORSMiddleware

import config
from domain.switch_management import TypeSwitch
from domain.wifi import Wifi
from output.models.activity_logs_database import ActivityLogsData
from output.models.contact_database import Contacts
from output.contact_sheet import ContactSheet
from output.models.user_database import UserData
from output.shell.configs_shell import ConfigsShell
from output.shell.equipment_shell import EquipmentShell
from output.models.favorite_links_database import FavoriteLinksData
from output.models.label_database import Labels
from output.record_dns_bind9 import Bind9
from output.shell.script_model_shell import ScriptModelShell
from output.models.site_database import Sites, SitesContacts
from output.shell.switch_shell import SwitchShell
from output.tools.grafana_shell import GrafanaShell
from production.config_files_data import syslog_ng, promtail_conf, promtail_service, loki_conf, loki_service, base, \
    clients, count, top_top_errors
from output.wifi_ansible import WifiAnsible

app = FastAPI()
temp = APIRouter(prefix='/api/v1')
app.include_router(temp)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/user")
# Ok
async def retrieve_data_user(data: dict):
    name: str = data["name"]
    password: str = data["password"]

    user_auth = False

    if config.connexion_mode == "ldap":
        organization_name = config.ldap_organization_name
        ldap_url_base = f"dc={config.ldap_url_prefix},dc={config.ldap_url_suffix}"
        server = Server(f"ldap://{config.ldap_host}:{config.ldap_port}")

        ldap_connection = Connection(server, user=f"cn={name},ou={organization_name},{ldap_url_base}",
                                     password=password)
        if ldap_connection.bind():
            user_auth = True

    elif config.connexion_mode == "local":
        user = UserData(username=name, password=password)
        if user.user_check():
            user_auth = True

    if user_auth:
        activity = ActivityLogsData(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"), author=name,
                                    action="Connexion")
        activity.create_activity_log()

    return user_auth


@app.post("/sessions")
# Ok : API NORM
async def user_logout(data: dict):
    actvity = ActivityLogsData(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"), author=data["user"],
                               action="Déconnexion")
    actvity.create_activity_log()


@app.get("/switches")
# Ok
async def save_all_configs():
    switch = SwitchShell()
    switch.versioning_configs_from_ftp()


@app.get("/contacts")
# Ok
async def get_contacts():
    return ContactSheet.get_all_contact_json()


@app.get("/switches/templates")
# Ok
async def get_list_templates():
    return ScriptModelShell.get_all_templates_content(templates_directory=config.templates_directory_path)


@app.post("/switches/template")
# Ok
async def retrieve_template(data: dict):
    name: str = data["type"]
    command: list = data["command"].split("\n")
    variables: dict = {}
    for variable in data["variables"]:
        variables[variable] = ""

    ScriptModelShell.create_provisioning_templates(name, command, variables)


@app.post("/templates/equipments")
# Ok
async def execution_template(data: dict):
    equipments_group: dict = data["equipments_group"]
    equipments_group_selected: list = data["selected_equipments_group"]
    file_for_commands: str = data["template_name"]
    data_template: dict = data["values_templates_selected"]
    script_exec = ScriptModelShell()
    list_eq = []

    for equipment_gr in equipments_group:
        if equipment_gr in equipments_group_selected:
            for eq in equipments_group[equipment_gr]:
                equipment = EquipmentShell(name=eq['name'], ip=eq['ip'])
                list_eq.append(equipment)

    script_exec.modify_template_before_execution(file_name=file_for_commands,
                                                 command_template=data_template['commands'],
                                                 variables_template=data_template['variables'])
    value = script_exec.exec_commands_on_equipments(file_name=file_for_commands, list_equipments=list_eq)
    return value


@app.get("/equipments")
# Ok
async def get_equipments():
    inventory_path = config.inventory_local_directory
    inventory_name = config.inventory_file_name

    return EquipmentShell.load_all(f"{inventory_path}/{inventory_name}")


# sudo lsof -t -i tcp:8000 | xargs kill -9 : to stop the server
@app.post("/templates")
# Ok
async def remove_template(template_name: str):
    switch = SwitchShell(switch_type=TypeSwitch(name=template_name.split("_")[0]))

    date: str = f"{template_name.split('_')[1]}_{template_name.split('_')[2]}"

    return Response(status_code=status.HTTP_200_OK) if ScriptModelShell.remove_template(switch.switch_type.name,
                                                                                        date=date) == 0 else Response(
        status_code=status.HTTP_404_NOT_FOUND)


@app.post("/templates/edition")
# Ok
async def edit_template(data: dict):
    name: str = data["templateName"]
    command: list = data["cmd"]
    variables: dict = data["vars"]
    new_variables = {variable: "" for variable in data["newVars"]}
    variables.update(new_variables)

    ScriptModelShell.modify_template_before_execution(file_name=name,
                                                      command_template=command,
                                                      variables_template=variables)


@app.post("/equipments")
# Ok
async def create_equipment(data: dict):
    new_equipment_group = data["new_equipment"]
    values: str = data["values"]
    list_equipment_group_values = values.split('\n')
    value = False

    if new_equipment_group != '':
        new_group_of_equipments = EquipmentShell()
        value = new_group_of_equipments.create(name_group=new_equipment_group, list_values=list_equipment_group_values)
    return value


@app.put("/equipments")
# Ok
async def edit_equipment(data: dict):
    equipment_group_selected = data["equipment_selected"]
    values: str = data["values"]
    list_equipment_group_values = values.split('\n')
    value = False

    if equipment_group_selected != '':
        edit_group_of_equipments = EquipmentShell()
        value = edit_group_of_equipments.edit(name_group=equipment_group_selected,
                                              list_values=list_equipment_group_values)
    return value


@app.delete("/equipments")
# Ok
async def remove_equipment(data: dict):
    equipment_group_to_remove = data["equipment_selected"]
    value = False

    if equipment_group_to_remove != '':
        remove_group_of_equipments = EquipmentShell()
        value = remove_group_of_equipments.remove(name_group=equipment_group_to_remove)
    return value


@app.get("/annuaire")
# Ok
async def get_list_sites_contacts_labels():
    return {"Contacts": Contacts.get_all(), "Sites": Sites.get_all(), "Labels": Labels.get_all()}


@app.post("/annuaires/contacts")
# Ok : API NORM
async def create_contact(data: dict):
    contact = Contacts()

    contact.first_name = data["firstName"]
    contact.last_name = data["lastName"]
    contact.number = data["phone"]
    contact.mail = data["email"]
    contact.address = data["address"]
    contact.commentary = data["comment"]

    contact.create()


@app.put("/annuaires/contacts")
# Ok : API NORM
async def edit_contact(data: dict):
    contact = Contacts()

    contact.id = data["id"]
    contact.first_name = data["firstName"]
    contact.last_name = data["lastName"]
    contact.mail = data["mail"]
    contact.address = data["address"]
    contact.number = data["phone"]
    contact.commentary = data["comment"]

    contact.update()


@app.delete("/annuaires/contacts")
# Ok : API NORM
async def supp_contact(data: dict):
    contact = Contacts()

    contact.id = data["id"]

    contact.delete()


@app.post("/annuaires/sites")
# Ok : API NORM
async def create_sites(data: dict):
    site = Sites()

    if data["siteName"]:
        site.site_name = data["siteName"]
        site.create()


@app.delete("/annuaires/sites")
# Ok : API NORM
async def supp_site(data: dict):
    site = Sites()

    site.id = data["id"]

    site.delete()


@app.put("/annuaires/sites")
# Ok : API NORM
async def edit_site(data: dict):
    site = Sites()

    site.id = data["id"]
    site.site_name = data["siteName"]

    site.update()


@app.post("/annuaires/sites/contacts")
# Ok : API NORM
async def add_contact_in_site(data: dict):
    site = Sites(id=data["siteId"])
    previous_contacts = [ids for ids in site.get_contacts_by_site_id().keys()]
    new_contacts = [ids.get("id") for ids in data["contactsList"]]
    contacts_to_add = [contact for contact in new_contacts if contact not in previous_contacts]
    contacts_to_remove = [contact for contact in previous_contacts if contact not in new_contacts]

    for contact_id in contacts_to_add:
        site_contact = SitesContacts(site_id=site.id)
        site_contact.contact_id = contact_id
        site_contact.link_contacts_sites()

    for contact_id in contacts_to_remove:
        SitesContacts.remove_link_between_contacts_sites(id_site=site.id, id_contact=contact_id)


@app.post("/annuaires/contacts/sites")
# Ok : API NORM
async def add_site_in_contact(data: dict):
    contact = Contacts(id=data["contactId"])

    sites = [int(ids) for ids in data["sites"]]
    previous_sites = [ids for ids in contact.get_sites_by_contact_id().keys()]
    sites_to_add = [ids for ids in sites if ids not in previous_sites]
    sites_to_remove = [ids for ids in previous_sites if ids not in sites]

    if sites_to_add:
        for site_id in sites_to_add:
            site_contact = SitesContacts(site_id=site_id, contact_id=contact.id)
            site_contact.link_contacts_sites()

    if sites_to_remove:
        for site_id in sites_to_remove:
            SitesContacts.remove_link_between_contacts_sites(id_site=site_id, id_contact=contact.id)


@app.get("/alias")
# Ok : API NORM
def check_alias(alias_name: str = Query(...)):
    # TODO récuperation liste des alias
    alias = Bind9()
    alias.open_data = ["alias", "switch", "montre", "sel", "souris"]
    alias.name = alias_name

    return alias.alias_is_available()


@app.get("/alias/hosts")
# Ok : API NORM
async def check_host(host_name: str = Query(...)):
    equipment = EquipmentShell()
    equipment.name = host_name

    return equipment.server_exists()


@app.post("/alias")
# Ok : API NORM
async def create_alias(data: dict):
    alias = Bind9()
    alias.name = data["alias_name"]
    alias.host = data["host_name"]
    # alias.create_alias()
    activity = ActivityLogsData(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"), author=data["user"],
                                action=f"Création de l'alias {alias.name} vers {alias.host}")
    activity.create_activity_log()
    return True


@app.get("/activities")
# Ok : API NORM
async def get_activities():
    return ActivityLogsData.get_all_activity_logs()


@app.get("/favorites")
# Ok : API NORM
async def get_favorites():
    return FavoriteLinksData.get_all_links()


@app.post("/favorites")
# Ok : API NORM
async def create_favorites(data: dict):
    name = data["name"]
    url = data["url"]

    favorite = FavoriteLinksData(name=name, url=url)
    favorite.add_favorite_link()

    activity = ActivityLogsData(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"), author=data["user"],
                                action=f"Ajout du favori {name} | Lien: {url}")
    activity.create_activity_log()


@app.delete("/favorites")
# Ok : API NORM
async def delete_favorites(data: dict):
    favorite = FavoriteLinksData().get_favorite_link_by_id(data["id"])

    activity = ActivityLogsData(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"), author=data["user"],
                                action=f"Suppression du favori {favorite.name} | Lien: {favorite.url}")
    activity.create_activity_log()

    favorite.delete_favorite_link()


@app.put("/favorites")
# Ok : API NORM
async def update_favorites(data: dict):
    favorite = FavoriteLinksData(id=data["id"], name=data["name"], url=data["url"])
    favorite.edit_favorite_link()

    activity = ActivityLogsData(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"), author=data["user"],
                                action=f"Modification du favori {favorite.name} | Lien: {favorite.url}")
    activity.create_activity_log()


@app.get("/wifis")
# Ok : API NORM
async def get_wifis_buildings():
    return Wifi.get_buildings()


@app.post("/wifis")
# Ok : API NORM
async def enable_wifi(data: dict):
    wifi = WifiAnsible()
    wifi.building = data["building"]
    # wifi.execute("script_ansible")

    print(wifi.building)
    print(data["user"])

    actvity = ActivityLogsData(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"), author=data["user"],
                               action=f"Activiation du wifi dans le batiment {wifi.building}")
    actvity.create_activity_log()


@app.get("/equipments/versions")
# Ok : API NORM
async def get_equipments_diff_versions():
    return EquipmentShell.version_alert(
        actual_version=f"{config.inventory_local_directory}/{config.inventory_file_name}",
        new_version=f"{config.inventory_local_directory}/{config.inventory_file_version}")


@app.get("/admin")
# Ok
async def get_configs_data():
    return {
        "logs_path": config.logs_file_path,
        "logs_level": config.debug_level,
        "database_resource": config.database_resource,
        "database_file": config.database_file,
        "excel_file": config.excel_file_path,
        "template_dir": config.templates_directory_path
    }


@app.post("/tools")
# Ok : API NORM
async def edit_and_install_tools(data: dict):
    if not hasattr(edit_and_install_tools, "configuration"):
        edit_and_install_tools.configuration = ConfigsShell()
        edit_and_install_tools.configuration.config_file_path = "/home/exnovo/PycharmProjects/network/conf_test.py"

    sudo = data["useSudo"]
    tool = data["tool"]
    operation = data["operation"]
    input_values = data["inputValues"]

    tools_dict = {
        "connection": ["grafana_host", "grafana_port", "grafana_username"],
        "grafana": ["grafana_wget_url", "grafana_ini_file"],
        "loki": ["loki_wget_url", "loki_yaml_file", "loki_service_file"],
        "promtail": ["promtail_wget_url", "promtail_yaml_file", "promtail_service_file"]
    }

    tool_keys = tools_dict.get(tool, [])

    cleaned_input_values = {k: v for k, v in input_values.items() if k in tool_keys}
    cleaned_input_values["use_sudo"] = sudo

    test: bool = False

    match operation:
        case "install":
            if tool == "grafana":
                try:
                    # assert test
                    # GrafanaShell().install_grafana()
                    print("Grafana installé avec succès")
                    return Response(status_code=200, content="Grafana installé avec succès",
                                    headers={"Content-Type": "text/html"})
                except Exception as e:
                    print(f"Erreur lors de l'installation de Grafana: {e}")
                    return Response(status_code=500, content=f"Erreur lors de l'installation de Grafana: {e}",
                                    headers={"Content-Type": "text/html"})
            elif tool == "loki":
                try:
                    # GrafanaShell().install_loki()
                    print("Loki installé avec succès")
                    return Response(status_code=200, content="Loki installé avec succès",
                                    headers={"Content-Type": "text/html"})
                except Exception as e:
                    return Response(status_code=500, content=f"Erreur lors de l'installation de Loki: {e}",
                                    headers={"Content-Type": "text/html"})
            elif tool == "promtail":
                try:
                    # GrafanaShell().install_promtail()
                    print("Promtail installé avec succès")
                    return Response(status_code=200, content="Promtail installé avec succès",
                                    headers={"Content-Type": "text/html"})
                except Exception as e:
                    return Response(status_code=500, content=f"Erreur lors de l'installation de Promtail: {e}",
                                    headers={"Content-Type": "text/html"})
            else:
                return Response(status_code=500, content="Outil inconnu", headers={"Content-Type": "text/html"})
        case "save":
            try:
                for key, value in cleaned_input_values.items():
                    edit_and_install_tools.configuration.variable_name = key
                    edit_and_install_tools.configuration.variable_value = value
                    # edit_and_install_tools.configuration.edit_variable()
                return Response(status_code=200, content="Configuration sauvegardée avec succès")
            except Exception as e:
                return Response(status_code=500, content=f"Erreur lors de la sauvegarde de la configuration: {e}")


@app.get("/tools")
# ok : API NORM
async def get_tools():
    return {
        "host": config.grafana_host,
        "port": config.grafana_port,
        "user": config.grafana_username,
        "grafanaUrl": config.grafana_wget_url,
        "grafanaIni": config.grafana_ini_file,
        "lokiUrl": config.loki_wget_url,
        "lokiYaml": config.loki_yaml_file,
        "lokiService": config.loki_service_file,
        "promtailUrl": config.promtail_wget_url,
        "promtailYaml": config.promtail_yaml_file,
        "promtailService": config.promtail_service_file,
        "syslog": syslog_ng,
        "base": base,
        "clients": clients,
        "count": count,
        "top": top_top_errors,
        "loki-yaml-content": loki_conf,
        "loki-service-content": loki_service,
        "promtail-yaml-content": promtail_conf,
        "promtail-service-content": promtail_service,
    }


@app.get("/settings")
async def get_settings():
    return {
        "connexionMode": config.connexion_mode,
        "ldapHost": config.ldap_host,
        "ldapPort": config.ldap_port,
        "ldapPrefix": config.ldap_url_prefix,
        "ldapSuffix": config.ldap_url_suffix,
        "ldapOrganizationName": config.ldap_organization_name,

        "frontUsername": config.frontend_username,
        "frontPort": config.frontend_port,
        "frontHost": config.frontend_host,
        "frontZIP": config.frontend_zip_file,
        "frontDir": config.frontend_project_dir,
        "nvmURL": config.nvm_wget_url,

        "nginxUsername": config.nginx_username,
        "nginxPort": config.nginx_port,
        "nginxHost": config.nginx_host,
        "nginxBuildDir": config.nginx_front_build_dir,
        "nginxConfigFile": config.nginx_config_file,

        "ansibleUsername": config.ansible_username,
        "ansiblePort": config.ansible_port,
        "ansibleHost": config.ansible_host,

        "ftpHost": config.ftp_host,
        "ftpUsername": config.ftp_username,
        "ftpDir": config.directory_ftp_switchs,
        "switchLocalDir": config.switch_configs_local_directory,
        "switchRemoteGit": config.repository_to_save_configs_for_all_switches_with_ssh,
        "savingHour": config.saving_hour,

        "inventoryDir": config.inventory_local_directory,
        "inventoryFileName": config.inventory_file_name,
        "inventoryVersion": config.inventory_file_version,
        "inventorySeparator": config.separateur,

        "DNSType": config.DNS_type,
        "aliasFile": config.alias_file,
    }


@app.post("/settings/users")
# Ok : API NORM
async def change_user_data(data: dict):
    user = UserData(username=data['username'], password=data['lastPassword'])
    if user.user_check():
        user.delete()
        user.password = data['newPassword']
        user.create_user()
        return True
    return None


if __name__ == "__main__":
    uvicorn.run("api.server:app", port=8000, reload=True)
