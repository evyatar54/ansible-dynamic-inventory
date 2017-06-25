from .models import *;

def getAllHosts():
        return (Host.objects.all());

def createHost(hostname, groupname ):
    host = Host.objects.create(name=hostname)
    group = Group.objects.get(name=groupname)
    host.add(group)

def deleteHost(hostname):
    Host.objects.remove(name=hostname)

def removeHostFromGroup(hostname, groupname):
    host = Host.objects.get(name=hostname)
    #TODO
#    host.remove(groups=groupname)
## checking if the host has more group left , theres no such thing as host without groups

def addHostToGroup(hostname, groupname):
    host = Host.objects.get_or_create(name=hostname)
    group = Group.objects.get(name=groupname)
    host.groups.add(groupname)

def createGroup(groupname):
    group = Group.objects.create(name=groupname)
    group.add(group)

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
#def getAllGroups():


#def getAllOSs():


#def getAllRoles():"""