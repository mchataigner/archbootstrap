#!/usr/bin/python

import grp, pwd, os, shutil
import os.path
import http.client
import sys

RE_INSTALL = False

def create_base_group(name, system = False):
    try:
        g = grp.getgrnam(name)
    except KeyError:
        if system:
            os.system("groupadd -r " + name)
        else:
            os.system("groupadd " + name)

def create_base_user(name, groups = list(), sgroups = list(), passwd = False):
    for g in sgroups:
        create_base_group(g, True)
    for g in groups:
        create_base_group(g)
    if name not in os.listdir("/home"):
        os.mkdir("/home/" + name)
    try:
        user = pwd.getpwnam(name)
    except KeyError:
        tmp_name = name.replace(".","")
        groups = ",".join(supplementary_groups)
        if len(groups) != 0:
            group_options = "-G " + groups
        else:
            group_options = ""
        os.system("useradd -U {2} -d /home/{0} {1}".format(name, tmp_name, group_options))
        if name != tmp_name:
            os.system("sed -i \"s/{1}/{0}/g\" /etc/passwd".format(name, tmp_name))
            os.system("sed -i \"s/{1}/{0}/g\" /etc/group".format(name, tmp_name))
        if passwd:
            os.system("passwd {0}".format(name))
        user = pwd.getpwnam(name)
    for g in supplementary_groups:
        if name not in grp.getgrnam(g).gr_mem:
            os.system("usermod -aG " + g + " " + name)
    os.chown("/home/"+name,user.pw_uid,user.pw_gid)

def install_required_packages():
    os.system("pacman -S --noconfirm --needed base")
    os.system("pacman -S --noconfirm --needed base-devel")
    os.system("pacman -S --noconfirm --needed linux-tools")
    os.system("pacman -S --noconfirm --needed git python curl")

def setup_sudoers():
    if os.path.isfile("/etc/sudoers.d/admin") and not RE_INSTALL:
        if os.path.isfile("/etc/sudoers.d/tmp_admin"):
            os.remove("/etc/sudoers.d/tmp_admin")
        return
    if os.system("pacman -Q moot-sudoer"):
        os.system("pacman -Rd moot-sudoer")
    conn = http.client.HTTPSConnection("raw.githubusercontent.com")
    conn.connect()
    conn.request("GET", "/mchataigner/archbootstrap/master/moot-base/admin_sudoers")
    resp = conn.getresponse()
    if resp.code == 200:
        sudoercontent = resp.read()
        f = os.open("/etc/sudoers.d/tmp_admin", os.O_CREAT | os.O_WRONLY, int("0440", 8))
        os.write(f, sudoercontent)
        os.close(f)
    conn.close()

def fetch_repo():
    if os.path.isdir("archbootstrap"):
        shutil.rmtree("archbootstrap")
    os.system("git clone https://github.com/mchataigner/archbootstrap.git")
    os.chdir("archbootstrap")
    os.system("git submodule update --init")

def clean_repo():
    if os.path.isdir("archbootstrap"):
        shutil.rmtree("archbootstrap")

def pre_build():
    # remove wrong version of yaourt
    if not os.system("pacman -Q yaourt"):
        os.system("pacman -R --noconfirm yaourt")
    if not os.system("pacman -Q yaourt-git"):
        os.system("pacman -R --noconfirm yaourt-git")
    # remove wrong version of package-query
    if not os.system("pacman -Q package-query"):
        os.system("pacman -R --noconfirm package-query")
    # remove wrong version of prezto
    if not os.system("pacman -Q prezto-git"):
        os.system("pacman -R --noconfirm prezto-git")
    # remove grml-zsh-config
    if not os.system("pacman -Q grml-zsh-config"):
        os.system("pacman -R --noconfirm grml-zsh-config")

def build():
    # install correct version of package-query if needed
    if os.system("pacman -Q package-query-git") or RE_INSTALL:
        os.chdir("package-query-git")
        os.system("makepkg -si --noconfirm")
        os.chdir("..")
    # intall correct version of yaourt if needed
    if os.system("pacman -Q yaourt-moot") or RE_INSTALL:
        os.chdir("yaourt-moot")
        os.system("makepkg -si --noconfirm")
        os.chdir("..")
    os.chdir("moot-sudoer")
    os.system("makepkg -si --noconfirm")
    os.chdir("..")
    os.system("yaourt -Pi --noconfirm moot-base")
    if os.system("pacman -Q prezto-moot") or RE_INSTALL:
        os.chdir("prezto-moot")
        os.system("makepkg -si --noconfirm")
        os.chdir("..")
    os.chdir("..")

if __name__ == "__main__":
    RE_INSTALL = len(sys.argv) > 1 and sys.argv[1] == "-i"
    if RE_INSTALL:
        print("will reisntall aur packages")
    if os.getuid() != 0:
        raise PermissionError("must run as root")
    install_required_packages()
    create_base_user("m.chataigner", sgroups = ["sudo", "wheel"], passwd = True)
    create_base_user("admin")
    setup_sudoers()
    admin = pwd.getpwnam("admin")
    os.system("chsh -s /usr/bin/zsh")
    os.system("chsh -s /usr/bin/zsh m.chataigner")
    os.system("chsh -s /usr/bin/zsh admin")
    pre_build()
    os.setregid(admin.pw_gid, admin.pw_gid)
    os.setreuid(admin.pw_uid, admin.pw_uid)
    os.chdir("/home/admin")
    fetch_repo()
    build()
    clean_repo()
