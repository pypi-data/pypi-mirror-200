import json
import logging
import os
import shutil
import sys
import tarfile
import tempfile
from urllib.parse import urlsplit

import ansible_runner

from beauris.blastbank import BankWriter

from jinja2 import Template

import yaml

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


# Tidy up the yaml dump (indent lists starts)
class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)


class WebInterface:

    def __init__(self, org, config, server):
        self.config = config
        self.server = server
        self.org = org

        self.base_url = self.config.deploy[server]["base_url"].rstrip("/")
        # TODO default for url_prefix should be ""
        self.url_prefix = self.config.deploy[server]["url_prefix"].rstrip("/")
        self.netloc = urlsplit(self.base_url).netloc
        self.deploy_base_path = os.path.join(self.config.deploy[server]["target_dir"], org.genus, org.species, org.strain)

        self.stack_name = self.org.slug()
        self.sub_url = self.stack_name
        if self.server == "staging":
            self.stack_name += "_staging"
            if self.config.deploy[server].get("append_staging"):
                self.sub_url += "_staging"

        name_clean = org.pretty_name()

        blast_theme = self.config.deploy[server]["options"].get("blast_theme", "")

        apollo_url = ""

        if 'apollo' in self.config.raw:
            apollo_url = self.config.get_service_url('apollo', self.server)

        self.deploy_variables = {
            "stack_name": self.stack_name,
            "name_clean": name_clean,
            "locker_folder": os.path.join(self.config.raw['data_locker']['options']['target_dir'], "") if self.config.raw['data_locker']['method'] == "dir" else "",
            "root_work_dir": self.config.root_work_dir,
            "src_data_folder": os.path.join(self.deploy_base_path, "src_data", ""),
            "netloc": self.netloc,
            "sub_url": self.sub_url,
            "stage": self.server,
            "base_url": self.base_url,
            "url_prefix": self.url_prefix,
            "blast_job_folder": os.path.join(self.config.deploy[server]["options"]["blast_job_dir"], ""),
            "blast_theme": os.path.join(blast_theme, "") if blast_theme else "",
            "use_apollo": 'apollo' in org.get_deploy_services(self.server),
            "apollo_url": apollo_url,
            "deploy_blast": 'blast' in org.get_deploy_services(self.server),
            "deploy_download": 'download' in org.get_deploy_services(self.server),
            "deploy_jbrowse": 'jbrowse' in org.get_deploy_services(self.server),
            "deploy_perms": 'authelia' in org.get_deploy_services(self.server),
        }

        # Prepare folder
        os.makedirs(self.deploy_base_path, exist_ok=True)

    def write_interface_files(self):
        # Prepare compose & other files
        template_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "workflows", "ansible", "templates")
        nginx_path = os.path.join(self.deploy_base_path, 'nginx', 'conf')
        os.makedirs(nginx_path, exist_ok=True)

        with open(os.path.join(nginx_path, "default.conf"), 'w') as f:
            f.write(self._render_template(os.path.join(template_folder, 'default.conf.j2')))

        with open(os.path.join(self.deploy_base_path, "docker-compose.yml"), 'w') as f:
            f.write(self._render_template(os.path.join(template_folder, 'docker-compose.yml.j2')))

        # Prepare web UI
        os.makedirs(os.path.join(self.deploy_base_path, "site"), exist_ok=True)
        template_path = os.path.join(template_folder, "web", self.config.deploy[self.server]["options"].get("web_theme", "default"))

        with open(os.path.join(self.deploy_base_path, "site", "index.html"), 'w') as f:
            f.write(self._render_template(os.path.join(template_path, "index.html.j2")))

        if os.path.exists(os.path.join(template_path, "assets")):
            # dirs_exist_ok only work in python >= 3.8
            shutil.copytree(os.path.join(template_path, "assets"), os.path.join(self.deploy_base_path, "site", "assets"), dirs_exist_ok=True)

    def prepare_download(self):

        if self.config.raw['data_locker']['method'] == "dir":
            data_base_path = os.path.join(self.deploy_base_path, "src_data")
            self._setup_download_links(data_base_path)
        else:
            # TODO Manage gopublish here
            pass

    def write_blast_files(self):

        shutil.copy(os.path.join(os.path.dirname(os.path.realpath(__file__)), "workflows", "ansible", "docker_files", "postgres-blast-entrypoint.sh"), self.deploy_base_path)

        if self.server == "production":
            # Need to create this or it will break when swarm creates the dockers
            docker_data_path = os.path.join(self.deploy_base_path, 'docker_data', 'blast_db')
            os.makedirs(docker_data_path, exist_ok=True)

        blast_base_path = os.path.join(self.deploy_base_path, 'blast')

        banks = self.org.get_blast_banks()

        writer = BankWriter(banks, blast_base_path, self.server)
        writer.write_bank_yml()
        writer.write_links_yml()

    def manage_permissions(self):
        # only authelia for now
        has_changed = self._manage_authelia_conf()
        if has_changed:
            log.info("Authelia conf has changed, reloading docker")
            extravars = {
                "service_name": self.config.deploy[self.server]['options'].get("authelia_service", "")
            }
            self._run_playbook("playbook_update.yml", extravars)
        else:
            log.info("No changes in authelia configuration")

    def shutdown(self):
        log.info("Shutting down interface")
        self._run_playbook("playbook_shutdown.yml")

    def start(self):
        log.info("Starting interface")
        self._run_playbook("playbook_deploy.yml")

    def _create_jbrowse_data_dir(self):

        jbrowse_folder = os.path.join(self.deploy_base_path, 'docker_data', 'jbrowse')
        os.makedirs(jbrowse_folder, exist_ok=True)

        return jbrowse_folder

    def setup_jbrowse(self, ass):

        jbrowse_folder = self._create_jbrowse_data_dir()

        assembly_jbrowse_folder = os.path.join(jbrowse_folder, ass.slug(short=True))
        jbrowse_exists = os.path.exists(assembly_jbrowse_folder)
        jbrowse_arch_path = ass.get_derived_path('jbrowse')

        # Extracting to temp dir to let the previous version online during extraction
        extract_folder = tempfile.mkdtemp(dir=jbrowse_folder)

        # Unpack archive to folder
        if self.server == "production":
            log.info("Extracting jbrowse data from {} to temp dir {}".format(jbrowse_arch_path, extract_folder))
            with tarfile.open(jbrowse_arch_path, 'r:gz') as intarf:
                # We need to modify the links to use the proper bam files
                log.info("Editing jbrowse tar.gz on the fly to use correct track file paths")
                tracks_real_path = ass.get_track_paths(prefer='locked')

                # First find all fake files that we need to replace by proper symlinks
                trackl = intarf.extractfile(intarf.getmember('trackList.json'))
                trl = json.load(trackl)

                to_swap = ass.jbrowse_track_swapping(trl['tracks'], tracks_real_path)

                for member in intarf.getmembers():
                    if member.name in to_swap:
                        os.makedirs(os.path.join(extract_folder, os.path.dirname(member.name)), exist_ok=True)
                        os.symlink(to_swap[member.name], os.path.join(extract_folder, member.name))
                    elif member.isfile() and not member.issym():
                        intarf.extract(member, path=extract_folder)

        elif self.server == "staging":
            log.info("Extracting jbrowse data from {} to temp dir {}".format(jbrowse_arch_path, extract_folder))
            with tarfile.open(jbrowse_arch_path, 'r:gz') as intarf:
                intarf.extractall(path=extract_folder)

        else:
            raise RuntimeError("Unexpected server type {}".format(self.server))

        # Write tracks.conf
        with open(os.path.join(extract_folder, "tracks.conf"), "w") as f:
            f.write("[general]\ndataset_id = {}\n".format(ass.slug(short=True)))

        os.chmod(extract_folder, 0o755)

        old_data_dir = assembly_jbrowse_folder + "_old"
        if jbrowse_exists:
            # We move first
            log.info("Moving old jbrowse data dir to {}".format(old_data_dir))
            shutil.move(assembly_jbrowse_folder, old_data_dir)

        log.info("Moving newly extracted jbrowse data dir from {} to {}".format(extract_folder, assembly_jbrowse_folder))
        shutil.move(extract_folder, assembly_jbrowse_folder)

        if jbrowse_exists:
            # Delete after
            log.info("Finished, removing old jbrowse data dir {}".format(old_data_dir))
            shutil.rmtree(old_data_dir)

    def _run_playbook(self, playbook, extravars={}):
        data = self._get_ansible_data(playbook)

        data['extravars'].update(extravars)

        r = ansible_runner.run(**data)

        log.info("Running playbook {}".format(playbook))
        log.info("{}: {}".format(r.status, r.rc))
        log.info("Final status:")
        log.info(r.stats)

        # Cleanup, since ansible store the ssh key and env var in files in the env folder
        shutil.rmtree(os.path.join(data["private_data_dir"], "env"))

        if r.rc != 0:
            log.error("Ansible playbook execution failed, exiting")
            sys.exit(r.rc)

    def _setup_download_links(self, data_base_path):

        files = self.org.get_files_to_publish()

        # Delete any old download content
        if os.path.exists(data_base_path):
            for filename in os.listdir(data_base_path):
                file_path = os.path.join(data_base_path, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)

        for file, entity in files:
            src_path = file.get_usable_path()
            dest_path = file.get_publish_path(entity.get_work_dir(), data_base_path, entity)

            link_dir = os.path.dirname(dest_path)
            os.makedirs(link_dir, exist_ok=True)
            if os.path.islink(dest_path):
                if not os.readlink(dest_path) == src_path:
                    # Update link
                    temp_link_name = tempfile.mktemp(dir=link_dir)
                    os.symlink(src_path, temp_link_name)
                    os.replace(temp_link_name, dest_path)
            else:
                os.symlink(src_path, dest_path)

    def _manage_authelia_conf(self):
        conf_path = self.config.deploy[self.server]['options']['authelia_conf']

        with open(conf_path, "r") as f:
            yml_str = f.read()
            try:
                yml_data = yaml.safe_load(yml_str)
            except yaml.YAMLError:
                log.error("Invalid authelia conf file : {}".format(conf_path))
                return False

        rules = []
        has_changed = False
        existing_deny = existing_allow = None
        for rule in yml_data['access_control']['rules']:
            # Keep internal rules
            if 'networks' in rule:
                rules.append(rule)
            elif rule['domain'] == self.netloc and any([self.sub_url in ressource for ressource in rule.get('resources', [])]):
                # Remove rules if no restrictions
                if not self.org.restricted_to:
                    continue
                if rule['policy'] == "deny":
                    existing_deny = rule
                elif self.org.restricted_to in rule.get('subject', ""):
                    existing_allow = rule
            else:
                rules.append(rule)

        if self.org.restricted_to:
            if existing_allow is None:
                rules.append({
                    'domain': self.netloc,
                    'resources': ["^{}/{}/.*$".format(self.url_prefix, self.sub_url)],
                    'policy': 'one_factor',
                    'subject': "group:{}".format(self.org.restricted_to)
                })
            else:
                rules.append(existing_allow)

            if existing_deny is None:
                rules.append({
                    'domain': self.netloc,
                    'resources': ["^{}/{}/.*$".format(self.url_prefix, self.sub_url)],
                    'policy': 'deny'
                })
            else:
                rules.append(existing_deny)

        # Check if we need to update the file
        if len(yml_data['access_control']['rules']) != len(rules):
            has_changed = True

        if has_changed:
            # Make a copy beforehand..
            shutil.copyfile(conf_path, conf_path + ".backup")
            yml_data['access_control']['rules'] = rules
            # Write to a temp file & rename it to avoid issues
            with open(conf_path + ".temp", 'w') as f:
                f.write(yaml.dump(yml_data, Dumper=Dumper, default_flow_style=False, sort_keys=False))
            os.replace(conf_path + ".temp", conf_path)

        # Merge authelia conf files if needed
        if 'authelia_conf_merge_with' in self.config.deploy[self.server]['options'] and 'authelia_conf_merge_to' in self.config.deploy[self.server]['options']:
            merge_with = self.config.deploy[self.server]['options']['authelia_conf_merge_with']
            merge_to = self.config.deploy[self.server]['options']['authelia_conf_merge_to']

            rules_str = yaml.dump({'access_control': {'rules': rules}}, Dumper=Dumper, default_flow_style=False, sort_keys=False)
            rules_str = rules_str.split("\n", 2)[2]  # Keep only the list of rules, properly indented

            with open(merge_with, 'r') as not_merged:
                with open(merge_to, 'w') as merged:
                    not_merged_str = not_merged.read()
                    merged_str = not_merged_str.replace('# __GOGEPP3000_RULES__', rules_str)
                    merged.write(merged_str)

        return has_changed

    def _render_template(self, template_file):
        with open(template_file) as f:
            template = Template(f.read())
        return template.render(self.deploy_variables)

    def _get_ansible_data(self, playbook):

        inventory = {"docker_swarm_host": {"hosts": self.config.raw['ansible'][self.server]["host"]}}
        extravars = {
            "deploy_dir": self.deploy_base_path,
            "stack_name": self.stack_name,
        }
        envvars = {}

        # Add external env variables
        for key, value in self.config.raw['ansible'][self.server].get("envvars", {}).items():
            envvars[key] = value

        for key, value in self.config.raw['ansible'][self.server].get("extravars", {}).items():
            extravars[key] = value

        private_ssh_key = os.getenv("ANSIBLE_SSH_KEY") + "\n"

        return {
            "private_data_dir": os.path.join(os.path.dirname(os.path.realpath(__file__)), "workflows", "ansible", "ansible_data"),
            "inventory": inventory,
            "playbook": playbook,
            "ssh_key": private_ssh_key,
            "extravars": extravars,
            "envvars": envvars,
        }

    def write_jbrowse_datasets(self):

        # Write datasets.conf file
        jbrowse_folder = os.path.join(self.deploy_base_path, 'docker_data', 'jbrowse')

        with open(os.path.join(jbrowse_folder, "datasets.conf"), "w") as f:
            f.write("[datasets.{}]\n".format(self.org.computer_name_short))
            for ass in self.org.assemblies:
                f.write("url = ?data=data/{}\nname = {}\n".format(ass.slug(short=True), ass.pretty_name()))
