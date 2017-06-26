from .models import Group, Host, Role
from . import models
from django.core.exceptions import ObjectDoesNotExist
from logging import getLogger
from django.db import IntegrityError


logger = getLogger()


class RemoveRoleException(Exception):
    pass


# Host
def get_all_hosts():
    try:
        return models.Host.objects.all()
    except:
        raise "internal error occurred"


def create_host(hostname, group_name):
    try:
        group = Group.objects.get(name=group_name)
        if Host.objects.get(name=hostname):
            raise "Host already exists "
        else:
            host = Host.objects.create(name=hostname)
            host.groups.add(group)
            host.save()
            return True

    except ObjectDoesNotExist:
        raise "Group doesn't exist"
    except Exception as e:
        # raise "internal error occurred"
        raise e.args


def delete_host(hostname):
    try:
        Host.objects.remove(name=hostname)
        return True
    except ObjectDoesNotExist:
        raise "Host doesn't exist"
    except:
        raise "internal error occurred"


def remove_host_from_group(hostname, group_name):
    try:
        host = Host.objects.get(name=hostname)
        num_of_groups = host.groups.count()
        if num_of_groups < 2:
            raise "Host cannot be left without groups"
        else:
            host.groups.remove(name=group_name)
            return True

    except ObjectDoesNotExist:
        raise "Host or group doesn't exist"
    except:
        raise "internal error occurred"


def add_host_to_group(hostname, group_name):
    try:
        host = Host.objects.get(name=hostname)
        group = Group.objects.get(name=group_name)
        host.groups.add(group)
        return True
    except ObjectDoesNotExist:
        raise "Host or group doesn't exist"
    except IntegrityError :
        raise "Host already in this group"
    except:
        raise "internal error occurred"


def get_all_hosts_by_group(group_name):
    try:
        group = Group.objects.get(name=group_name)
        return group.host_set.all()

    except ObjectDoesNotExist:
        raise "Group doesn't exist"
    except:
        raise "internal error occurred"


# Group
def get_all_groups():
    try:
        return Group.objects.Filter(enabled=True)
    except:
        raise "internal error occurred"


def get_all_platforms():
    try:
        return Group.objects.Filter(enabled=True, isPlatform=True)
    except:
        raise "internal error occurred"


def create_group(group_name):
    try:
        group = Group.objects.create(name=group_name)
        group.add(group)
        group.save()

    except IntegrityError:
            raise "Group already exists"
    except:
        raise "internal error occurred"


def delete_group(group_name):
    Group.objects.remove(name=group_name)
    # TODO
    # adding removing the group from other groups/from hosts
    # and checking if the hosts still have at least one group


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


def get_all_groups_by_group(group_name):
    try:
        return Group.objects.get(name=group_name).groups
    except:
        raise "internal error occurred"
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


def get_all_roles():
    try:
        return Role.objects.Filter(enabled=True)
    except:
        raise "internal error occurred"


def create_role(role_name):
    try:
        Role.objects.create(name=role_name, enabled=True)
        return True
    except ObjectDoesNotExist:
        raise "Role already exists"
    except:
        raise "internal error occurred"


def delete_role(role_name):
    # TODO: - removing the option for roles per host
    try:
        role = Role.object.get(name=role_name)
        role.delete()
        return True

    except ObjectDoesNotExist:
        raise "Role doesn't exist"
    except RemoveRoleException as e:
        raise e
    except:
        raise "internal error occurred"


def add_role_to_host(role_name, hostname):
    try:
        host = Host.objects.get(name=hostname)
        role = Role.object.get(name=role_name)
        host.roles.add(role)
        host.save()
        return True
    except ObjectDoesNotExist:
        raise "Host or role doesn't exist"
    except IntegrityError:
        raise "Role already in this host"
    except:
        raise "internal error occurred"


def add_role_to_group(role_name, group_name):
    try:
        group = Group.objects.get(name=group_name)
        role = Role.objects.get(name=role_name)
        group.roles.add(role)
        group.save()
        return True
    except ObjectDoesNotExist:
        raise "Group or role doesn't exist"
    except IntegrityError:
        raise "Role already in this group"
    except:
        raise "internal error occurred"


def remove_role_from_host(role_name, hostname):
    try:
        host = Host.objects.get(name=hostname)
        role = Role.objects.get(name=role_name)
        host.roles.remove(role)
        return True
    except ObjectDoesNotExist:
        raise "host or role doesnt exist"


def remove_role_from_group(role_name, group_name):
    try:
        group = Group.objects.get(name=group_name)
        role = Role.objects.get(name=role_name)
        group.roles.remove(role)
        return True
    except ObjectDoesNotExist:
        raise "group or role doesnt exist"
