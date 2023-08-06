#!/usr/bin/env python

# Send an organism archive to a remote Apollo server

import argparse
import logging
import sys
import time

from apollo import ApolloInstance

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def check_organism(wa, slug):
    return wa.organisms.show_organism(slug)


def manage_group(wa, cname, gname, type):

    perms = False
    if type == "add":
        perms = True

    tries = 0
    not_yet_done = True

    while tries < 3 and not_yet_done:
        not_yet_done = False
        try:
            wa.groups.update_organism_permissions(gname, args.cname,
                                                  administrate=False, write=perms, read=perms,
                                                  export=perms)
            return
        except KeyError:
            # You can get a sporadic error from apollo, just retry a bit later
            not_yet_done = True
            time.sleep(10)

        tries += 1
    # Failed after 3 time, raise error
    log.error("Error while updating organism {}: couldn't {} group {}".format(cname, type, gname))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--restricted', type=str, help="Group for restricting access")
    parser.add_argument('--previous', type=str, help="Previous group for restricting access")
    parser.add_argument('cname', type=str, help="Common name")
    parser.add_argument('url', type=str, help="Apollo server URL")
    parser.add_argument('user', type=str, help="Apollo server user")
    parser.add_argument('password', type=str, help="Apollo server password")
    args = parser.parse_args()

    wa = ApolloInstance(args.url, args.user, args.password)

    new_group_name = ""
    old_group_name = ""
    # Safety check:
    if args.restricted:
        groups = wa.groups.get_groups(name=args.restricted)
        if not groups:
            log.error("Error: Group {} does not exists".format(args.restricted))
            sys.exit(1)
        new_group_name = groups[0]['name']

    if args.previous:
        groups = wa.groups.get_groups(name=args.previous)
        # Maybe we should just ignore the error.. but might be a typo
        if not groups:
            log.error("Error: Group {} does not exists".format(args.previous))
            sys.exit(1)
        old_group_name = groups[0]['name']

    # Add new group first
    if new_group_name:
        manage_group(wa, args.cname, new_group_name, "add")
    if old_group_name:
        manage_group(wa, args.cname, old_group_name, "remove")

    # Raise an error if there were some logged
    if 40 in log._cache and log._cache[40]:
        sys.exit(1)
