#
# This module allows us to parse a machine placement directive into a
# Placement object suitable for passing through the websocket API.
#
# Once https://bugs.launchpad.net/juju/+bug/1645480 is addressed, this
# module should be deprecated.
#

from .client import client

MACHINE_SCOPE = "#"


def parse(directive):
    """
    Given a string in the format `scope:directive`, or simply `scope`
    or `directive`, return a Placement object suitable for passing
    back over the websocket API.

    """
    if not directive:
        # Handle null case
        return None

    if type(directive) in [dict, client.Placement]:
        # We've been handed something that we can simply hand back to
        # the api. (Forwards compatibility)
        return [directive]

    # Juju 2.0 can't handle lxc containers.
    directive = directive.replace('lxc', 'lxd')

    if ":" in directive:
        # Planner has given us a scope and directive in string form
        scope, directive = directive.split(":")
        return [client.Placement(scope=scope, directive=directive)]

    if directive.isdigit():
        # Planner has given us a machine id (we rely on juju core to
        # verify its validity.)
        return [client.Placement(scope=MACHINE_SCOPE, directive=directive)]

    if "/" in directive:
        machine, container, container_num = directive.split("/")
        return [
            client.Placement(scope=MACHINE_SCOPE, directive=machine),
            client.Placement(scope=container, directive=container_num)
        ]

    # Planner has probably given us a container type. Leave it up to
    # juju core to verify that it is valid.
    return [client.Placement(scope=directive)]
