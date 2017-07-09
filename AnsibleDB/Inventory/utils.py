from .models import Group, Host, Role, Var
from django.core.exceptions import ObjectDoesNotExist
from logging import getLogger
from django.db import IntegrityError
from django.template.loader import render_to_string

INVENTORY_TEMPLATE_PATH = "inventory/inventory.j2"
logger = getLogger()


# Host
def get_host(hostname):
    try:
        host = Host.objects.get(name=hostname)
        return host
    except ObjectDoesNotExist:
        raise Exception('group doesnt exist')
    except:
        raise Exception('internal error occurred')


def get_host_groups(hostname):
    try:
        host = Host.objects.get(name=hostname)
        groups = host.groups.all()
        return groups
    except ObjectDoesNotExist:
        raise Exception('host doesnt exist')
    except:
        raise Exception('internal error occurred')


def get_all_hosts():
    try:
        return Host.objects.all()
    except:
        raise Exception('internal error occurred')


def get_host_roles(hostname):
    try:
        host = get_host(hostname)
        return host.roles.all()
    except ObjectDoesNotExist:
        raise Exception('host doesnt exist')


def create_host(hostname, group_name):
    try:
        group = get_group(group_name)
        host = Host.objects.create(name=hostname)
        host.save()
        host.groups.add(group)
        host.save()
        return True

    except ObjectDoesNotExist:
        raise Exception('Group doesnt exist')
    except:
        raise Exception('internal error occurred')


def delete_host(hostname):
    try:
        Host.objects.remove(name=hostname)
        return True
    except ObjectDoesNotExist:
        raise Exception('Host doesnt exist')
    except:
        raise Exception('internal error occurred')


def remove_host_from_group(hostname, group_name):
    try:
        host = get_host(hostname)
        num_of_groups = host.groups.count()
        if num_of_groups < 2:
            raise Exception('Host cannot be left without groups')
        else:
            host.groups.remove(name=group_name)
            return True

    except ObjectDoesNotExist:
        raise Exception('Host or group doesnt exist')
    except:
        raise Exception('internal error occurred')


def add_host_to_group(hostname, group_name):
    try:
        host = get_host(hostname)
        group = get_group(group_name)
        host.groups.add(group)
        return True
    except ObjectDoesNotExist:
        raise Exception('Host or group doesnt exist')
    except IntegrityError:
        raise Exception('Host already in this group')
    except:
        raise Exception('internal error occurred')


def get_host_roles(hostname):
    try:
        host = get_host(hostname)
        group = host.groups.all()[0]
        roles = bfs_get_group_roles(group)
        return roles
    except ObjectDoesNotExist:
        raise Exception('host doesnt exist')
    except:
        raise Exception('internal error occurred')


def get_host_vars(hostname):
    try:
        host = get_host(hostname)
        group = host.groups.all()[0]
        variables = bfs_get_group_vars(group)
        return variables
    except ObjectDoesNotExist:
        raise Exception('host doesnt exist')
    except:
        raise Exception('internal error occurred')


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
    try:
        group = get_group(group_name)
        return group.host_set.all()

    except ObjectDoesNotExist:
        raise Exception('Group doesnt exist')
    except:
        raise Exception('internal error occurred')


def get_all_groups():
    try:
        return Group.objects.filter(enabled=True)
    except:
        raise Exception('internal error occurred')


def get_all_platforms():
    try:
        return Group.objects.filter(enabled=True, isPlatform=True)
    except:
        raise Exception('internal error occurred')


def create_group(group_name):
    try:
        group = Group.objects.create(name=group_name)
        group.save()
    except IntegrityError:
            raise Exception('Group already exists')
    except:
        raise Exception('internal error occurred')


def delete_group(group_name):
    try:
        group = get_group(group_name)
        group.delete()
    except ObjectDoesNotExist:
        raise Exception('group doesnt exist')
    except:
        raise Exception('internal error occurred')


def add_group_child(group_name, child_group_name):
    try:
        group = get_group(group_name)
        group_child = get_group(child_group_name)
        group.children.add(group_child)
        return True
    except ObjectDoesNotExist:
        raise Exception('group doesnt exist')
    except:
        raise Exception("internal error occurred")


def add_group_to_parent(group_name, parent_group_name):
    try:
        group = get_group(group_name)
        group_parent = get_group(parent_group_name)
        group.parents.add(group_parent)
        return True
    except ObjectDoesNotExist:
        raise Exception('group doesnt exist')
    except:
        raise Exception("internal error occurred")


def remove_group_child(group_name, child_group_name):
    try:
        group = get_group(group_name)
        group_child = get_group(child_group_name)
        group.children.remove(group_child)
        return True
    except ObjectDoesNotExist:
        raise Exception('group doesnt exist')
    except:
        raise Exception("internal error occurred")


def remove_group_from_parent(group_name, parent_group_name):
    try:
        group = get_group(group_name)
        group_parent = get_group(parent_group_name)
        group.parents.remove(group_parent)
        return True
    except ObjectDoesNotExist:
        raise Exception('group doesnt exist')
    except:
        raise Exception("internal error occurred")


def get_group(group_name):
    try:
        group = Group.objects.get(name=group_name)
        return group
    except ObjectDoesNotExist:
        raise Exception('group doesnt exist')
    except:
        raise Exception("internal error occurred")


def get_group_children(group_name):
    try:
        group = get_group(group_name)
        return group.children.all()
    except ObjectDoesNotExist:
        raise Exception('group doesnt exist')
    except:
        raise Exception('internal error occurred')


# Vars
def add_var_to_group(key, value, group_name):
    try:
        group = get_group(group_name)
        var = Var.objects.create(key=key, value=value, group=group)
        var.save()
    except ObjectDoesNotExist:
        raise Exception('group doesnt exists')
    except IntegrityError:
        raise Exception('var already exists')
    except Exception:
        raise Exception('internal error occurred')


def remove_var_from_group(key, group_name):
    try:
        group = get_group(group_name)
        var = Var.objects.get(key=key, group=group)
        var.delete()
    except ObjectDoesNotExist:
        raise Exception('group doesnt exists')
    except Exception:
        raise Exception('internal error occurred')


def get_group_vars(group_name):
    try:
        group = get_group(group_name)
        return group.var_set.all()
    except ObjectDoesNotExist:
        raise Exception('group doesnt exist')
    except:
        raise Exception('internal error occurred')


# Roles
def get_role(role_name):
    try:
        role = Role.objects.get(name=role_name)
        return role
    except ObjectDoesNotExist:
        raise Exception('role doesnt exist')
    except:
        raise Exception('internal error occurred')


def get_roles():
    try:
        return Role.objects.all()
    except:
        raise Exception('internal error occurred')


def get_group_roles(group_name):
    try:
        group = get_group(group_name)
        return group.roles.all()
    except ObjectDoesNotExist:
        raise Exception('group doesnt exist')
    except:
        raise Exception('internal error occurred')


def create_role(role_name):
    try:
        Role.objects.create(name=role_name, enabled=True)
        return True
    except IntegrityError:
        raise Exception("Role already exists")
    except:
        raise Exception("internal error occurred")


def delete_role(role_name):
    try:
        role = Role.object.get(name=role_name)
        role.delete()
        return True
    except ObjectDoesNotExist:
        raise Exception("Role doesn't exist")
    except:
        raise Exception("internal error occurred")


def add_role_to_host(role_name, hostname):
    try:
        host = Host.objects.get(name=hostname)
        role = Role.object.get(name=role_name)
        host.roles.add(role)
        host.save()
        return True
    except ObjectDoesNotExist:
        raise Exception("Host or role doesn't exist")
    except IntegrityError:
        raise Exception("Role already in this host")
    except:
        raise Exception("internal error occurred")


def add_role_to_group(role_name, group_name):
    try:
        group = Group.objects.get(name=group_name)
        role = Role.objects.get(name=role_name)
        group.roles.add(role)
        group.save()
        return True
    except ObjectDoesNotExist:
        raise Exception("Group or role doesn't exist")
    except IntegrityError:
        raise Exception("Role already in this group")
    except:
        raise Exception("internal error occurred")


def remove_role_from_host(role_name, hostname):
    try:
        host = Host.objects.get(name=hostname)
        role = Role.objects.get(name=role_name)
        host.roles.remove(role)
        return True
    except ObjectDoesNotExist:
        raise Exception("host or role doesnt exist")


def remove_role_from_group(role_name, group_name):
    try:
        group = Group.objects.get(name=group_name)
        role = Role.objects.get(name=role_name)
        group.roles.remove(role)
        return True
    except ObjectDoesNotExist:
        raise Exception("group or role doesnt exist")


def get_inventory_json():
    try:
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
    except Exception as e:
        raise e


def generate_playbook(group_name):
    try:
        group = get_group(group_name)
        roles = get_group_roles(group_name)
        context = {"hosts": group.name, "roles": roles}
        playbook_text = render_to_string(INVENTORY_TEMPLATE_PATH, context)
        return playbook_text
    except Exception as e:
        raise e