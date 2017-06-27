from .models import Group, Host, Role
from django.core.exceptions import ObjectDoesNotExist
from logging import getLogger
from django.db import IntegrityError
from django.template.loader import render_to_string

INVENTORY_TEMPLATE_PATH = "inventory/inventory.j2"
logger = getLogger()


class RemoveRoleException(Exception):
    pass


# Host
def get_host(hostname):
    try:
        host = Host.objects.get(name=hostname)
        return host
    except ObjectDoesNotExist:
        raise Exception('group doesnt exist')
    except:
        raise Exception('internal error occurred')


def get_all_hosts():
    try:
        return Host.objects.all()

    except:
        raise Exception('internal error occurred')


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


def get_group_hosts(group_name):
    try:
        group = get_group(group_name)
        return group.host_set.all()

    except ObjectDoesNotExist:
        raise Exception('Group doesnt exist')
    except:
        raise Exception('internal error occurred')


# Group
def get_all_groups():
    try:
        return Group.objects.Filter(enabled=True)
    except:
        raise Exception('internal error occurred')


def get_all_platforms():
    try:
        return Group.objects.Filter(enabled=True, isPlatform=True)
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


"""def removeGroupFromGroup(group_name):
        group = Group.objects.get(name=hostname)

    #    host.remove(groups=group_name)
    ## checking if the host has more group left , there's no such thing as host without groups

def addGroupToGroup(hostname, group_name):
        host = Host.objects.get_or_create(name=hostname)
        group = Group.objects.get(name=group_name)
        host.groups.add(group_name)



    >> > entry = Entry.objects.get(pk=1)
    >> > cheese_blog = Blog.objects.get(name="Cheddar Talk")
    >> > entry.blog = cheese_blog
    >> > entry.save()

    >> > from blog.models import Author
    >> > joe = Author.objects.create(name="Joe")
    >> > entry.authors.add(joe)


def getAllGroupsByGroup(group_name):
    #TODO


# OSs
def getAllOSs():
    return (OS.objects.all())
"""


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
"""
# Vars
def get_all_vars_by_group(groupname):
    try:
        if (Group.objects.get(name=groupname)):
            return Var.objects.filter(group=groupname)
        else:
            return False
    except:
        raise ("internal error occurred")
"""
# Roles


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
        inventory_json = {}
        groups = get_all_groups()
        for group in groups:
            group_name = group.name
            group_json = {}
            group_json["hosts"] = get_group_hosts(group_name)
            group_json["children"] = get_group_children(group_name)

            vars_json = {}
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
        context = {"hosts": group.name, "roles": roles }
        playbook_text = render_to_string(INVENTORY_TEMPLATE_PATH, context)
        return playbook_text
    except Exception as e:
        raise e

