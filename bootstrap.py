#!/usr/bin/python

import grp, pwd, os, shutil
import os.path
import http.client

def create_base_user(name, supplementary_groups = list(), passwd = False):
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

def clean_repo():
    if os.path.isdir("archbootstrap"):
        shutil.rmtree("archbootstrap")

def build():
    os.chdir("archbootstrap")
    os.system("git submodule update --init")
    os.chdir("package-query-git")
    os.system("makepkg -si --noconfirm")
    os.chdir("../yaourt-moot")
    os.system("makepkg -si --noconfirm")
    os.chdir("../moot-sudoer")
    os.system("makepkg -si --noconfirm")
    os.chdir("..")
    os.system("yaourt -Pi --noconfirm moot-base")
    os.chdir("prezto-moot")
    os.system("makepkg -si --noconfirm")
    os.chdir("../..")

if __name__ == "__main__":
    if os.getuid() != 0:
        raise PermissionError("must run as root")
    create_base_user("m.chataigner", ["sudo", "wheel"], True)
    create_base_user("admin")
    install_required_packages()
    setup_sudoers()
    admin = pwd.getpwnam("admin")
    os.system("chsh -s /usr/bin/zsh")
    os.system("chsh -s /usr/bin/zsh m.chataigner")
    os.system("chsh -s /usr/bin/zsh admin")
    os.setregid(admin.pw_gid, admin.pw_gid)
    os.setreuid(admin.pw_uid, admin.pw_uid)
    os.chdir("/home/admin")
    fetch_repo()
    build()
    clean_repo()
