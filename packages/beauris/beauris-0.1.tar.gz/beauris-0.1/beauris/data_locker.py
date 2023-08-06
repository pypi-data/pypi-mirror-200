#!/usr/bin/env python

"""
Make sure new data is deposited in a safe place, and accessible at a stable url
"""

# TODO implement gopublish
# TODO support permissions (.htaccess?)
# TODO compute md5/sha256?

import json
import logging
import os
import shutil
from collections import defaultdict

import gopublic

from .util import md5


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class DataLockers():
    def __init__(self):

        self.data_lockers = {
            'dir': DirLocker,
            'gopublish': GopublishLocker,
        }

    def get(self, name, config):

        if name in self.data_lockers:
            return self.data_lockers[name](**config)

        raise RuntimeError('Could not find data locker named "%s"' % name)


class BaseLocker():

    def __init__(self):
        pass

    def is_locked(self, path, version, revision, metadata={}):
        """
            Check if a file is already locked or not
        """
        raise NotImplementedError()

    def lock_file(self, path, version, revision, metadata={}):
        """
            Lock a file (without checking if it was already done)
        """
        raise NotImplementedError()

    def check_locked(self, path, version, revision, dry_run=False, metadata={}):
        """
            Make sure the given file is locked (locks it if not already done)
        """
        raise NotImplementedError()

    def _metadata_add_default(self, default="unknown", metadata={}):
        # TODO make default configurable
        new_m = defaultdict(lambda: default)
        new_m.update(metadata)

        for x, val in metadata.items():
            if isinstance(val, str):
                val = val.replace(' ', '_')
            new_m[x] = val

        return new_m

    def get_locked_file(self, path, version, revision, metadata={}):
        """
            Return a file metadata if it exists
        """
        raise NotImplementedError()


class DirLocker(BaseLocker):

    def __init__(self, target_dir, base_pattern, pattern_input, pattern_derived, locked_yml_dir, dry_run=False, locked_yml_dir_future=False):
        self.dry_run = dry_run
        self.target_dir = target_dir
        self.locked_yml_dir = locked_yml_dir
        self.locked_yml_dir_future = locked_yml_dir_future
        self.base_pattern = base_pattern
        self.pattern_input = pattern_input
        self.pattern_derived = pattern_derived

        # Check if target dir is writable/in good shape
        if not self.target_dir.startswith(os.path.sep):
            raise RuntimeError("Target dir '%s' must be absolute" % self.target_dir)

        if len(self.target_dir) <= 2:
            raise RuntimeError("Target dir '%s' is invalid" % self.target_dir)

        if not os.path.isdir(self.target_dir):
            raise RuntimeError("Target dir '%s' does not exist" % self.target_dir)

    def _generate_dest_path(self, path, version, revision, metadata={}):
        metadata = self._metadata_add_default(metadata=metadata)

        pattern = self.base_pattern

        if 'assembly_version' in metadata:
            pattern += "{assembly_version}/"

        if 'annotation_version' in metadata:
            pattern += "{annotation_version}/"

        if 'track_id' in metadata:
            pattern += "{track_id}/"

        if 'tool_version' in metadata:  # TODO find something less hacky
            pattern += self.pattern_derived
        else:
            pattern += self.pattern_input

        pattern_replaced = pattern.format_map(metadata)

        return os.path.normpath(os.path.join(self.target_dir, pattern_replaced))

    def is_locked(self, path, version, revision, metadata={}):
        dest_path = self._generate_dest_path(path, version, revision, metadata)

        if os.path.exists(dest_path) and not os.path.isfile(dest_path):
            # TODO should we make some sanity checks? same size (or even md5/sha256 if we have time?)
            raise RuntimeError("The path '%s' is not a file as expected" % dest_path)

        return os.path.exists(dest_path)

    def lock_file(self, path, version, revision, metadata={}):

        dest_path = self._generate_dest_path(path, version, revision, metadata)

        if not self.dry_run:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy(path, dest_path)

            # TODO store MD5, date and filesize in locked yml?
            md5_file = md5(path)
            metadata['md5'] = md5_file

            with open(dest_path + ".metadata", 'w') as f:
                json.dump(metadata, f)

    def check_locked(self, path, version, revision, dry_run=False, metadata={}):
        # TODO make sure we can't get any duplicate (each path+version should get a unique target path)
        dest_path = self._generate_dest_path(path, version, revision, metadata)

        if not self.is_locked(path, version, revision, metadata):
            log.info("Locking '%s' to '%s'" % (path, dest_path))
            if not dry_run:
                self.lock_file(path, version, revision, metadata)
        else:
            log.info("Skipping locking of '%s' to '%s' (already locked)" % (path, dest_path))

        return dest_path

    def get_locked_file(self, path, version, revision, metadata={}):
        dest_path = self._generate_dest_path(path, version, revision, metadata)
        if os.path.exists(dest_path) and os.path.isfile(dest_path):
            # Return metadata from file if it exists, else extracted metadata
            if os.path.isfile(dest_path + ".metatada"):
                with open(dest_path + ".metatada") as f:
                    metadata = json.load(f)
            return metadata
        return {}


class GopublishLocker(BaseLocker):

    def __init__(self, url, username, apikey, proxy_username=None, proxy_password=None, dry_run=False):
        self.dry_run = dry_run

        # Connection is tested automatically
        self.gopublish = gopublic.GopublishInstance(
            url=url,
            proxy_username=proxy_username,
            proxy_password=proxy_password
        )
        self.token = self.gopublish.token.create(username, api_key=apikey)

    def _get_path(self, uid):
        if not self.dry_run:
            data = self.gopublish.file.view(uid)
            return data['file']['path']
        return "temp_dry_run_path"

    def is_locked(self, path, version, revision, metadata={}):
        # Get metadata values as list, to use as tags
        tags = list(metadata.values())
        tags.append(version)
        file_name = os.path.basename(path)
        # Hacky hacky. Revisions start at 0, but gopublish versions start at 1
        current_revision = revision + 1

        # TODO on gopublish : allow search by version directly
        # Return one non-version matching uid if it exists, to save one query
        results = self.gopublish.file.search(query=file_name, tags=tags)
        existing_version = ""
        for file in results['files']:
            existing_version = file['uid']
            if file['version'] == current_revision:
                return True, existing_version
        return False, existing_version

    def lock_file(self, path, version, revision, metadata={}, last_version=""):

        body = {
            "path": path,
        }

        if last_version:
            # tags are inherited, not need to specify them
            body['linked_to'] == last_version
        else:
            tags = list(metadata.values())
            tags.append(version)
            body['tags'] = tags

        if not self.dry_run:
            self.gopublish.file.publish(**body)

    def check_locked(self, path, version, revision, dry_run=False, metadata={}):
        is_lock, current_uid = self.is_locked(path, version, revision, metadata)

        if not is_lock:
            log.info("Locking '%s' to Gopublish" % path)
            if not dry_run:
                current_uid = self.lock_file(path, version, revision, metadata, current_uid)
        else:
            log.info("Skipping locking of '%s' to Gopublish (already locked)" % path)

        if current_uid:
            dest_path = self._get_path(current_uid)
        elif dry_run:
            dest_path = "[unpredictable_gopublish_path]"

        return dest_path

    def get_locked_file(self, path, version, revision, metadata={}):
        # Get metadata values as list, to use as tags
        tags = list(metadata.values())
        tags.append(version)
        file_name = os.path.basename(path)
        # Hacky hacky. Revisions start at 0, but gopublish versions start at 1
        current_revision = revision + 1

        # TODO on gopublish : allow search by version directly
        results = self.gopublish.file.search(query=file_name, tags=tags)
        for file in results['files']:
            if file['version'] == current_revision:
                return file
        return {}
