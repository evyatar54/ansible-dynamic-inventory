import os
import django
import random
from Inventory.models import Group, Host, Role, Var
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE','AnsibleDB.settings')
django.setup()
f = Faker()
hosts = ['aaa-aaa', 'bbb-aaa', '12-abc', 'lll-877', 'lnx-dev-ansb', 'blalbalba-hera', 'noam-herman-dev']
platform = ['docker', 'bamboo', 'java', 'python', 'swarm', 'ansible']
groups = ['galaxy', 'ory', 'other', 'linux', 'paamon', 'omega']
roles = ['ntp', 'dns', 'sudoers', 'password', 'common_rpms', 'yum_repo']
keys = ['file', 'gateway', 'dns-server', 'ntp-server']


def add_host():
    h = Host.objects.get_or_create(name=random.choice(hosts))[0]
    h.save()
    return h


def add_host_to_group():
    h = Host.objects.get_or_create(name=random.choice(hosts))[0]
    h.save()
    g = Group.objects.get_or_create(name=random.choice(platform),
                                    isPlatform=True)[0]
    g.save()
    h.groups.add(g)
    h.save()


def add_platform():
    g = Group.objects.get_or_create(name=random.choice(platform),
                                    isPlatform=True)[0]
    g.save()
    return g


def add_group():
    g = Group.objects.get_or_create(name=random.choice(groups))[0]
    p = add_platform()
    r = add_role()
    g.roles.add(r)
    g.children.add(p)
    g.save()
    return g


def add_role():
    r = Role.objects.get_or_create(name=random.choice(roles))[0]
    r.save()
    return r


def add_var():
    g = add_group()
    key = random.choice(keys)
    value = key+'-'+g.name
    v = Var.objects.get_or_create(key=key, value=value, group=g)[0]
    v.save()
    return v


def populate(n=5):
    for i in range(n):
        add_host()
        add_group()
        add_role()
        add_var()


def add_hosts(n=20):
    for i in range(n):
        add_host_to_group()

