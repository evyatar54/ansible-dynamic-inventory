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

# Group
def get_group_hosts(group_name):
    group = get_group(group_name)
    return group.hosts.all()

def get_all_groups():
    return Group.objects.filter(enabled=True)

def get_hosts_by_group(group_name):
    group = Group.objects.get(name=group_name)
    return group.hosts.all()

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

def get_group(group_name):
    group = Group.objects.get(name=group_name)
    return group

def get_groups(groups):
    return Group.objects.filter(name__in=groups)

def get_group_children(group_name):
    group = get_group(group_name)
    return group.children.all()

# Vars
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