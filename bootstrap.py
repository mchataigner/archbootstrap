#!/usr/bin/python

import grp, pwd, os, shutil
import os.path
import http.client
import sys
import getopt
from collections import defaultdict
import subprocess

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
        gs = ",".join(groups + sgroups)
        if len(gs) != 0:
            group_options = "-G " + gs
        else:
            group_options = ""
        os.system("useradd -U {2} -d /home/{0} {1}".format(name, tmp_name, group_options))
        if name != tmp_name:
            os.system("sed -i \"s/{1}/{0}/g\" /etc/passwd".format(name, tmp_name))
            os.system("sed -i \"s/{1}/{0}/g\" /etc/group".format(name, tmp_name))
        if passwd:
            os.system("passwd {0}".format(name))
        user = pwd.getpwnam(name)
    for g in groups + sgroups:
        if name not in grp.getgrnam(g).gr_mem:
            os.system("usermod -aG " + g + " " + name)
    os.chown("/home/"+name,user.pw_uid,user.pw_gid)

def install_required_packages():
    os.system("pacman -S --noconfirm --needed base base-devel linux-tools git python curl grub efibootmgr")

def fetch_sudoer(name, file_name):
    conn = http.client.HTTPSConnection("raw.githubusercontent.com")
    conn.connect()
    conn.request("GET", "/mchataigner/archbootstrap/master/moot-sudoer/" + name)
    resp = conn.getresponse()
    if resp.code == 200:
        sudoercontent = resp.read()
        f = os.open("/etc/sudoers.d/" + file_name, os.O_CREAT | os.O_WRONLY, int("0400", 8))
        os.write(f, sudoercontent)
        os.close(f)
    conn.close()

def setup_sudoers():
    if os.path.isfile("/etc/sudoers.d/admin") and not RE_INSTALL:
        if os.path.isfile("/etc/sudoers.d/tmp_admin"):
            os.remove("/etc/sudoers.d/tmp_admin")
        return
    if os.system("pacman -Q moot-sudoer"):
        os.system("pacman -Rd moot-sudoer")
    fetch_sudoer("admin_sudoers", "admin")
    fetch_sudoer("common", "common")

def fetch_repo():
    if os.path.isdir("archbootstrap"):
        shutil.rmtree("archbootstrap")
    os.system("git clone https://github.com/mchataigner/archbootstrap.git")
    os.chdir("archbootstrap")
    os.system("git submodule update --init")

def clean_repo():
    if os.path.isdir("archbootstrap"):
        shutil.rmtree("archbootstrap")

def pacman_remove(pack):
    if not os.system("pacman -Q " + pack):
        os.system("pacman -R --noconfirm "+pack)

def pacman_install(pack):
    os.system("pacman -S --noconfirm "+pack)
        
def pre_build():
    for pack in ["yaourt", "yaourt-git", "package-query", "prezto-git", "grml-zsh-config"]:
        pacman_remove(pack)
    os.system("sed -i 's/#en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/g' /etc/locale.gen")
    os.system("locale-gen")

def build(flavors = list()):
    pacman_install("paru moot-sudoer moot-base moot-base-config prezto-moot")
    os.system("systemctl start sshd")
    os.system("systemctl enable sshd")

    if "client" in flavors:
        pacman_install("xorg xorg-apps xorg-drivers xorg-fonts moot-client moot-client-config pasystray-moot")
    if "prog" in flavors:
        pacman_install("moot-prog")
    if "server" in flavors:
        pacman_install("moot-server")

def setup_fstab():
    os.system("genfstab -U / > /etc/fstab")

def setup_localtime():
    os.system("ln -sfn ../usr/share/zoneinfo/Europe/Paris /etc/localtime")

def setup_mkinitcpio():
    os.system("sed -i 's/^MODULES=.*/MODULES=\"ext4\"/g' /etc/mkinitcpio.conf")
    os.system("sed -i 's/^HOOKS=.*/HOOKS=\"base udev autodetect modconf block keyboard keymap encrypt filesystems fsck\"/g' /etc/mkinitcpio.conf")
    os.system("sed -i 's/^#COMPRESSION=\"lz4\"/COMPRESSION=\"lz4\"/g' /etc/mkinitcpio.conf")
    os.system("mkinitcpio -p linux")

def setup_grub():
    def abs_p(p):
        while os.path.islink(p):
            p=os.path.abspath(os.path.dirname(p) + "/" + os.readlink(p))
        return p
    def rename(p):
        return p.replace("../../", "/dev/")
    def clean_uuid(uuid):
        return uuid.replace("-","")
    disks_by_uuid = defaultdict(list)
    disks_by_device = dict()
    uuid="/dev/disk/by-uuid/"
    for p in os.listdir(uuid):
        if os.path.islink(uuid + p):
            disks_by_device[abs_p(uuid + p)] = (clean_uuid(p))
            disks_by_uuid[clean_uuid(p)].append(p)
            disks_by_uuid[clean_uuid(p)].append(abs_p(uuid + p))
    label = "/dev/disk/by-label/"
    for p in os.listdir(label):
        if os.path.islink(label + p):
            disks_by_uuid[disks_by_device[abs_p(label + p)]].append(p)
    dms = dict()
    for l in subprocess.check_output(["dmsetup", "ls"]).decode().strip().split("\n"):
        dm = l.split("\t")[0]
        for ll in subprocess.check_output(["dmsetup", "info", dm]).decode().strip().split("\n"):
            if ll.startswith("UUID:") and "CRYPT-LUKS" in ll:
                crypted_uuid = ll.split("-")[2]
                info = list(disks_by_uuid[crypted_uuid])
                info.append(dm)
                dms[abs_p("/dev/mapper/" + dm)] = info
                break
    dm_list = list(dms.items())
    if len(dm_list) > 1:
        index = int(input('which one is root?\n' + '\n'.join(map(lambda x: str(x[0]+1)+" : "+str(x[1][0]) + " - " + str(x[1][1][0]) + " - " + str(x[1][1][1]), enumerate(dm_list)))+'\n'))
        dm = dm_list[index - 1]
    elif len(dm_list) == 1:
        dm = dm_list[0]
    else:
        dm = None
    if dm:
        crypt_uuid = dm[1][0]
        crypt_name = dm[1][-1]
        os.system("sed -i 's#GRUB_CMDLINE_LINUX=.*#GRUB_CMDLINE_LINUX=\"cryptdevice=/dev/disk/by-uuid/"+crypt_uuid+":"+crypt_name+":allow-discards cryptkey=/dev/disk/by-uuid/648d19c6-3839-42d9-be47-00cfb73b62cc:ext4:/japan.jpg LOGLEVEL=5 libata.force=noncq\"#g' /etc/default/grub")
    efi = False
    with open("/proc/mounts", 'r') as f:
        content = f.read()
        for l in content.strip().split("\n"):
            if l.startswith("efivarfs"):
                efi = True
            if " / " in l:
                root_dev = abs_p(l.split(" ")[0])
                while root_dev in dms:
                    root_dev = dms[root_dev][1]
    base_name = os.path.basename(root_dev)
    matched_dev = list()
    for i in os.listdir("/dev"):
        if base_name.startswith(i):
            matched_dev.append(i)
    if len(matched_dev) > 1:
        for i in matched_dev:
            if i != base_name:
                install_disk = "/dev/" + i
                break
    else:
        install_disk = "/dev/" + matched_dev[0]
    print(install_disk)
    print(efi)

    subprocess.check_output(["grub-mkconfig", "-o", "/boot/grub/grub.cfg"])
    if efi:
        subprocess.check_output(["grub-install", "--efi-directory=/boot/EFI", "--target=x86_64-efi", install_disk])
    else:
        subprocess.check_output(["grub-install", "--target=x86_64", install_disk])

def setup_my_key():
    subprocess.check_output(["pacman-key", "--recv-keys", "2B548C7D3205D9E0"])
    subprocess.check_output(["pacman-key", "--lsign-key", "2B548C7D3205D9E0"])

if __name__ == "__main__":
    optlist, flavors = getopt.getopt(sys.argv[1:], "igb")
    opts = dict(optlist)
    if "-b" in opts:
        build(flavors)
        sys.exit()
    os.environ["TMPDIR"] = "/tmp"
    if os.path.isdir("/home/admin/archbootstrap"):
        shutil.rmtree("/home/admin/archbootstrap")
    RE_INSTALL = "-i" in opts
    if RE_INSTALL:
        print("will reisntall aur packages")
    if os.getuid() != 0:
        raise PermissionError("must run as root")
    install_required_packages()
    if "-g" in opts:
        setup_fstab()
        setup_mkinitcpio()
        setup_grub()
    setup_my_key()
    create_base_user("m.chataigner", sgroups = ["sudo", "wheel"], passwd = True)
    create_base_user("admin")
    setup_sudoers()
    setup_localtime()
    os.system("chsh -s /usr/bin/zsh")
    os.system("chsh -s /usr/bin/zsh m.chataigner")
    os.system("chsh -s /usr/bin/zsh admin")
    pre_build()
    build(flavors)
