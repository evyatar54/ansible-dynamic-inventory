from .models import Group, Host, Role, Var
from django.core.exceptions import ObjectDoesNotExist
from logging import getLogger
from django.db import IntegrityError
from django.template.loader import render_to_string

INVENTORY_TEMPLATE_PATH = "inventory/inventory.j2"
logger = getLogger()


# Host
def get_host(hostname):
    host = Host.objects.get(name=hostname)
    return host

def get_host_groups(hostname):
    host = Host.objects.get(name=hostname)
    groups = host.groups.all()
    return groups

def get_all_hosts():
    return Host.objects.all()


def get_host_roles(hostname):
    host = get_host(hostname)
    return host.roles.all()

def create_host(name, groups, roles):
    group_list = get_groups(groups)
    role_list = get_roles(roles)

    host = Host.objects.create(name=name)
    host.groups.add(*group_list)
    host.roles.add(*role_list)
    host.save()

    return host

def delete_host(hostname):
    Host.objects.remove(name=hostname)
    return True

def update_host(hostname, groups_names, roles_names):
    host = get_host(hostname)
    groups = Group.objects.filter(name__in=groups_names)
    host.groups.exclude(name__in=groups_names).delete()
    host.groups.add(*groups)
    roles = Role.objects.filter(name__in=roles_names)
    host.roles.exclude(name__in=roles_names).delete()
    host.roles.add(*roles)
    return host


def remove_host_from_group(hostname, group_name):
    host = get_host(hostname)
    num_of_groups = host.groups.count()
    if num_of_groups < 2:
        raise Exception('Host cannot be left without groups')
    else:
        host.groups.remove(name=group_name)
        return True

def add_host_to_group(hostname, group_name):
    host = get_host(hostname)
    group = get_group(group_name)
    host.groups.add(group)
    return True

def get_host_roles(hostname):
    host = get_host(hostname)
    group = host.groups.all()[0]
    roles = bfs_get_group_roles(group)
    return roles

def get_host_vars(hostname):
    host = get_host(hostname)
    group = host.groups.all()[0]
    variables = bfs_get_group_vars(group)
    return variables

def bfs_get_group_roles(group):
    explored = []
    # keep track of nodes to be checked
    queue = [group]
    group_roles = []

    # keep looping until there are nodes still to be checked
    while queue:
        # pop shallowest node (first node) from queue
        node = queue.pop(0)
        if node not in explored:
            # add node to list of checked nodes
            group_roles += node.roles.all()
            explored.append(node)
            neighbours = group.children.all().append(group.parents)

            # add neighbours of node to queue
            for neighbour in neighbours:
                queue.append(neighbour)
    return explored


def bfs_get_group_vars(group):
    explored = []
    # keep track of nodes to be checked
    queue = [group]
    group_vars = []

    # keep looping until there are nodes still to be checked
    while queue:
        # pop shallowest node (first node) from queue
        node = queue.pop(0)
        if node not in explored:
            # add node to list of checked nodes
            group_vars += node.vars.all()
            explored.append(node)
            neighbours = group.children.all().append(group.parents)

            # add neighbours of node to queue
            for neighbour in neighbours:
                queue.append(neighbour)
    return explored


# Group
def get_group_hosts(group_name):
    group = get_group(group_name)
    return group.hosts.all()

def get_all_groups():
    return Group.objects.filter(enabled=True)

def get_hosts_by_group(group_name):
    group = Group.objects.get(name=group_name)
    return group.hosts.all()

def get_all_platforms():
    return Group.objects.filter(enabled=True, isPlatform=True)


def create_group(
        group_name,
        children=[], 
        roles=[], 
        vars=[],
        isPlatform=False, 
        enabled=True ):
    group = Group.objects.create(name=group_name)
    return update_group(group_name, children, roles, vars, isPlatform, enabled)

def update_group(name, children_names, roles_names, vars, isPlatform, enabled):
    group = get_group(name)
    children = Group.objects.filter(name__in=children_names)
    group.children.exclude(name__in=children_names).delete()
    group.children.add(*children)
    roles = Role.objects.filter(name__in=roles_names)
    group.roles.exclude(name__in=roles_names).delete()
    group.roles.add(*roles)
    set_group_vars(group, { var["key"]: var["value"] for var in vars })
    group.isPlatform = isPlatform
    group.enabled = enabled
    group.save()
    return group

def set_group_vars(group, vars):
    group.vars.exclude(key__in=vars.keys()).delete()
    for key, value in vars.items():
        var = group.vars.filter(key=key).first()
        if var is None:
            var = Var.objects.create(group=group, key=key, value=value)
        else:
            var.value = value
        var.save()

def delete_group(group_name):
    group = get_group(group_name)
    group.delete()

def add_group_child(group_name, child_group_name):
    group = get_group(group_name)
    group_child = get_group(child_group_name)
    group.children.add(group_child)
    return True


def add_group_to_parent(group_name, parent_group_name):
    group = get_group(group_name)
    group_parent = get_group(parent_group_name)
    group.parents.add(group_parent)
    return True

def remove_group_child(group_name, child_group_name):
    group = get_group(group_name)
    group_child = get_group(child_group_name)
    group.children.remove(group_child)
    return True

def remove_group_from_parent(group_name, parent_group_name):
    group = get_group(group_name)
    group_parent = get_group(parent_group_name)
    group.parents.remove(group_parent)
    return True

def get_group(group_name):
    group = Group.objects.get(name=group_name)
    return group

def get_groups(groups):
    return Group.objects.filter(name__in=groups)

def get_group_children(group_name):
    group = get_group(group_name)
    return group.children.all()

# Vars
def add_var_to_group(key, value, group_name):
    group = get_group(group_name)
    var = Var.objects.create(key=key, value=value, group=group)
    var.save()

def remove_var_from_group(key, group_name):
    group = get_group(group_name)
    var = Var.objects.get(key=key, group=group)
    var.delete()

def get_group_vars(group_name):
    group = get_group(group_name)
    return group.vars.all()

# Roles
def get_role(role_name):
    role = Role.objects.get(name=role_name)
    return role

def get_roles(roles_list):
    return Role.objects.filter(name__in=roles_list)

def get_all_roles():
    return Role.objects.all()

def get_group_roles(group_name):
    group = get_group(group_name)
    return group.roles.all()

def create_role(role_name):
    return Role.objects.create(name=role_name, enabled=True)

def delete_role(role_name):
    role = Role.object.get(name=role_name)
    role.delete()
    return True

def add_role_to_host(role_name, hostname):
    host = Host.objects.get(name=hostname)
    role = Role.object.get(name=role_name)
    host.roles.add(role)
    host.save()
    return True

def add_role_to_group(role_name, group_name):
    group = Group.objects.get(name=group_name)
    role = Role.objects.get(name=role_name)
    group.roles.add(role)
    group.save()
    return True

def remove_role_from_host(role_name, hostname):
    host = Host.objects.get(name=hostname)
    role = Role.objects.get(name=role_name)
    host.roles.remove(role)
    return True

def remove_role_from_group(role_name, group_name):
    group = Group.objects.get(name=group_name)
    role = Role.objects.get(name=role_name)
    group.roles.remove(role)
    return True

def get_inventory_json():
    inventory_json = dict()
    groups = get_all_groups()
    for group in groups:
        group_name = group.name
        group_json = dict()
        group_json["hosts"] = [host.name for host in get_group_hosts(group_name)]
        group_json["children"] = [group.name for group in get_group_children(group_name)]

        vars_json = dict()
        for var in get_group_vars(group_name):
            vars_json[var.key] = var.value
        group_json["vars"] = vars_json

        inventory_json[group_name] = group_json

    return inventory_json

def generate_playbook(group_name):
    group = get_group(group_name)
    roles = get_group_roles(group_name)
    context = {"hosts": group.name, "roles": roles}
    playbook_text = render_to_string(INVENTORY_TEMPLATE_PATH, context)
    return playbook_text