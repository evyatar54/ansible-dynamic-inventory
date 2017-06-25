import os
import django
import random
from Inventory.models import Group, Host, Role
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE','AnsibleDB.settings')
django.setup()
f = Faker()
hosts = ['aaa-aaa', 'bbb-aaa', '12-abc', 'lll-877', 'lnx-dev-ansb', 'blalbalba-hera', 'noam-herman-dev']
platform = ['docker', 'bamboo', 'java', 'python', 'swarm', 'ansible']
groups = ['galaxy', 'ory', 'other', 'linux', 'paamon', 'omega']
roles = ['ntp', 'dns', 'sudoers', 'password', 'common_rpms', 'yum_repo']


def add_host():
    h = Host.objects.get_or_create(name=random.choice(hosts))[0]
    h.save()
    return h


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
    g.groups.add(p)
    g.save()
    return g


def add_role():
    r = Role.objects.get_or_create(name=random.choice(roles))[0]
    r.save()
    return r


# def add_vars():
#     g = add_group()
#     v = Var.objects.get_or_create(group=g, key='sudoers-file')[0]
#     v.value = str(v.group)
#     v.save()
#     return v


def populate(n=5):
    for i in range(n):
        add_host()
        add_group()
        add_role()
        # add_vars()


def get():
    print(Group.objects.all())