from Inventory.models import Group,Host,Role,Var
from . import models
from logging import getLogger

logger = getLogger()
class remove_role_exception(Exception):
    pass

# Host
def get_all_hosts():
    return models.Host.objects.all()

def create_host(hostname, groupname):
    try:
        group = Group.objects.get(name=groupname)
        host = Host.objects.create(name=hostname)
        host.groups.add(group)
        return True
    except KeyError:
        raise ("Host already exists Or Group doesn't exist")
    except Exception as e:
        #raise ("internal error occurred")
        raise e.args

def delete_host(hostname):
    try:
        Host.objects.remove(name=hostname)
        return True
    except KeyError:
        raise ("Host doesn't exist")
    except :
        raise ("internal error occurred")

def remove_host_from_group(hostname, groupname):
    try:
        host = Host.objects.get(name=hostname)
        numOfGroups = host.groups.count()
        if (numOfGroups < 2):
            return False
            raise ("Host cannot be left without groups")
        else:
            host.groups.remove(name=groupname)
            return True

    except KeyError:
        raise ("Host or group doesn't exist")
    except:
        raise ("internal error occurred")

def add_host_to_group(hostname, groupname):
    try:
        host = Host.objects.get(name=hostname)
        group = Group.objects.get(name=groupname)
        host.groups.create(group)
        return True
    except KeyError:
        raise ("Host already in this group Or Host or group doesn't exist")
    except:
        raise ("internal error occurred")

def get_all_hosts_by_group(groupname):
    try:
        group = Group.objects.get(name=groupname)
        return (group.host_set.all())

    except KeyError:
        raise ("Group doesn't exist")
    except:
        raise ("internal error occurred")

# Group
def get_all_groups():
    return (Group.objects.Filter(enables=True))

def create_group(groupname):
    try:
        group = Group.objects.create(name=groupname)
        group.add(group)
    except:
            raise ("Group already exists")


def delete_group(groupname):
    Group.objects.remove(name=groupname)
    # TODO
    # adding removing the group from other groups/from hosts
    # and checking if the hosts still have at least one group


"""def removeGroupFromGroup(groupname):
        group = Group.objects.get(name=hostname)

    #    host.remove(groups=groupname)
    ## checking if the host has more group left , theres no such thing as host without groups

def addGroupToGroup(hostname, groupname):
        host = Host.objects.get_or_create(name=hostname)
        group = Group.objects.get(name=groupname)
        host.groups.add(groupname)
        
        
        
    >> > entry = Entry.objects.get(pk=1)
    >> > cheese_blog = Blog.objects.get(name="Cheddar Talk")
    >> > entry.blog = cheese_blog
    >> > entry.save()

    >> > from blog.models import Author
    >> > joe = Author.objects.create(name="Joe")
    >> > entry.authors.add(joe)


def getAllGroupsByGroup(groupname):
    #TODO
    
    
# OSs
def getAllOSs():
    return (OS.objects.all())
"""

# Vars
def get_all_vars_by_group(groupname):
    return (Group.objects.Filter(name=groupname).variables)

# Roles
def get_all_roles():
    return (Role.objects.Filter(enabled=True))

def create_role(rolename):
    try:
        Role.objects.create(name=rolename, enabled=True)
        return True
    except KeyError:
        raise ("Role already exists")
    except:
        raise ("internal error occurred")

def delete_role(rolename):
    #TODO - removing the option for roles per host
    try:
        hostsList = Host.objects.all()
        groupList = Group.objects.all()

        for host in hostsList:
            remove_role_from_host(rolename,host)

        for group in groupList:
            remove_role_from_group(rolename,group)

        Role.objects.remove(name=rolename)
        return True

    except KeyError:
        raise ("Role doesn't exist")
    except remove_role_exception as e:
        raise e
    except:
        raise ("internal error occurred")

def add_role_to_host(rolename, hostname):
    try:
        host = Host.objects.get(name=hostname)
        role = Role.object.get(name=rolename)
        host.roles.add(role)
        return True
    except KeyError:
        raise ("Host or role doesn't exist")
    except:
        raise ("internal error occurred")

def add_role_to_group(rolename, groupname):
    try:
        group = Group.objects.get(name=groupname)
        role = Role.object.get(name=rolename)
        group.roles.add(role)
        return True
    except KeyError:
        raise ("Group or role doesn't exist")
    except:
        raise ("internal error occurred")

def remove_role_from_host(rolename, hostname):
    try:
        host = Host.objects.get(name=hostname)
        my_roles = host.roles.all()
        if rolename in my_roles:
            host.roles.remove(role=rolename)
            return True
        else:
            raise remove_role_exception("Host doesn't contain that role")
    except:
        raise ("internal error occurred")

def remove_role_from_group(rolename, groupname):
    try:
        group = Host.objects.get(name=groupname)
        my_roles = group.roles.all()
        if rolename in my_roles:
            group.roles.remove(role=rolename)
            return True
        else:
            raise remove_role_exception("Group doesn't contain that role")

    except:
        raise ("internal error occurred")
