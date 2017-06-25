from .models import *
from logging import getLogger
from configparser import ConfigParser
# Host

#cp = ConfigParser.
#logger = getLogger()
def getAllHosts():
        return (Host.objects.all())

def createHost(hostname, groupname):
    try:
        group = Group.objects.get(name=groupname)
        host = Host.objects.create(name=hostname)
        host.groups.add(group)
    except:
        raise ("Host already exists")

def deleteHost(hostname):
    Host.objects.remove(name=hostname)

def removeHostFromGroup(hostname, groupname):
    host = Host.objects.get(name=hostname)
    #TODO
#    host.remove(groups=groupname)
## checking if the host has more group left , theres no such thing as host without groups

def addHostToGroup(hostname, groupname):
    try:
        host = Host.objects.get(name=hostname)
        group = Group.objects.get(name=groupname)
        host.groups.add(groupname)
    except:
        raise ("Host doesn't exist")

def getAllHostsByGroup(groupname):
    #TODO
    pass

# Group
def getAllGroups():
    return (Group.objects.Filter(enables=True))

def createGroup(groupname):
    try:
        group = Group.objects.create(name=groupname)
        group.add(group)
    except:
            raise ("Group already exists")

def deleteGroup(groupname):
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
def getAllVarsByGroup(groupname):
    return (Group.objects.Filter(name=groupname).variables)

# Roles
def getAllRoles():
    return (Role.objects.Filter(enabled=True))

def createRole(rolename):
    try:
        Role.objects.create(name=rolename, enabled=True)
    except:
        raise ("Role already exists")

def addRoleToHost(rolename, hostname):
    try:
        host = Host.objects.get(name=hostname)
        #role = Role.object.create(name=rolename, enabled=True)
        role = Role.object.get(name=rolename)
        host.roles.add(role)
    except:
        raise ("Host doesn't exist")
        raise ("Role doesn't exist")
        raise ("DB error")

def addRoleToGroup(rolename, groupname):
    try:
        group = Group.objects.get(name=groupname)
        #role = Role.object.create(name=rolename, enabled=True)
        role = Role.object.get(name=rolename)
        group.roles.add(role)
    except:
        raise ("Group doesn't exist")
        raise ("Role doesn't exist")
        raise ("DB error")

def removeRoleFromHost(rolename, hostname):
    try:
        host = Host.objects.get(name=hostname)
        host.roles.remove(role=rolename)

        #TODO
    except:
        raise ("Host doesn't exist")

def removeRoleFromGroup(rolename, groupname):
    try:
        group = Host.objects.get(name=groupname)
        group.roles.remove(role=rolename)
        #TODO
    except:
        raise ("Group doesn't exist")