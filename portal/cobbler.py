#-*- coding: utf-8 -*-

import xmlrpclib

#VM CREATION IN COBBLER

#COBBLER PARAMETERS
#nextserver
#gwbackup
#gwstatic
#staticroutes
#backuproutes
#name
#hostname
#profile
#cmdline  (ksmetas)

class Cobbler:
    def __init__(self, cobblerhost, cobbleruser, cobblerpassword):
        self.s = xmlrpclib.Server("http://%s/cobbler_api" % cobblerhost)
        self.token = self.s.login(cobbleruser,cobblerpassword)

    def create(self,name,profile, numinterfaces, dns=None, ip1=None, subnet1=None, ip2=None, subnet2=None, ip3=None, subnet3=None, ip4=None, subnet4=None, gateway=None, gwstatic=None, gwbackup=None, staticroutes=None, backuproutes=None,macaddr=None,parameters=None,cmdline=None,nextserver=None):
        if ip1:
            ip1=ip1.encode('ascii')
        if ip2:
            ip2=ip2.encode('ascii')
        if ip3:
            ip3=ip3.encode('ascii')
        if ip4:
            ip4=ip4.encode('ascii')
        if dns:
            dns=dns.encode('ascii')
        profile=profile.encode('ascii')
        s = self.s
        token = self.token
        system = s.find_system({"name":name})
        if system!=[]:
            print "%s allready defined in cobbler..." % (name)
            return
        if gwstatic and staticroutes:
            staticroutes = staticroutes.replace(",",":%s " % gwstatic)+":"+gwstatic
        if gwbackup and backuproutes:
            backuproutes = backuproutes.replace(",",":%s " % gwbackup)+":"+gwbackup
            staticroutes = "%s %s" % (staticroutes, backuproutes)

        system = s.new_system(token)
        s.modify_system(system, 'name', name, token)
        s.modify_system(system, 'hostname', name, token)
        s.modify_system(system, 'profile', profile, token)
        if nextserver:
            s.modify_system(system, 'server', nextserver, token)
        if numinterfaces==1:
            if staticroutes:
                eth0 = {"macaddress-eth0":macaddr[0], "static-eth0":1, "ipaddress-eth0":ip1, "subnet-eth0":subnet1, "staticroutes-eth0":staticroutes}
            else:
                eth0 = {"macaddress-eth0":macaddr[0], "static-eth0":1, "ipaddress-eth0":ip1, "subnet-eth0":subnet1}
            if dns:
                eth0["dnsname-eth0"] = "%s.%s" % (name, dns)
            s.modify_system(system, 'modify_interface',eth0, token)
        elif numinterfaces==2:
            eth0 = {"macaddress-eth0":macaddr[0], "static-eth0":1, "ipaddress-eth0":ip1, "subnet-eth0":subnet1}
            if dns:
                eth0["dnsname-eth0"] = "%s.%s" % (name, dns)
            if staticroutes:
                eth1 = {"macaddress-eth1":macaddr[1], "static-eth1":1, "ipaddress-eth1":ip2, "subnet-eth1":subnet2, "staticroutes-eth1":staticroutes}
            else:
                eth1 = {"macaddress-eth1":macaddr[1], "static-eth1":1, "ipaddress-eth1":ip2, "subnet-eth1":subnet2}
            s.modify_system(system, 'modify_interface', eth0, token)
            s.modify_system(system, 'modify_interface', eth1, token)
        elif numinterfaces==3:
            eth0 = {"macaddress-eth0":macaddr[0], "static-eth0":1, "ipaddress-eth0":ip1, "subnet-eth0":subnet1}
            if dns:
                eth0["dnsname-eth0"] = "%s.%s" % (name, dns)
            if staticroutes:
                eth1 = {"macaddress-eth1":macaddr[1], "static-eth1":1, "ipaddress-eth1":ip2, "subnet-eth1":subnet2, "staticroutes-eth1":staticroutes}
            else:
                eth1 = {"macaddress-eth1":macaddr[1], "static-eth1":1, "ipaddress-eth1":ip2, "subnet-eth1":subnet2}
            eth2 = {"macaddress-eth2":macaddr[2], "static-eth2":1, "ipaddress-eth2":ip3, "subnet-eth2":subnet3}
            s.modify_system(system,'modify_interface', eth0, token)
            s.modify_system(system, 'modify_interface', eth1, token)
            s.modify_system(system, 'modify_interface', eth2, token)
        elif numinterfaces==4:
            eth0 = {"macaddress-eth0":macaddr[0], "static-eth0":1, "ipaddress-eth0":ip1, "subnet-eth0":subnet1}
            if dns:
                eth0["dnsname-eth0"] = "%s.%s" % (name, dns)
            if staticroutes:
                eth1 = {"macaddress-eth1":macaddr[1], "static-eth1":1, "ipaddress-eth1":ip2, "subnet-eth1":subnet2, "staticroutes-eth1":staticroutes}
            else:
                eth1 = {"macaddress-eth1":macaddr[1], "static-eth1":1, "ipaddress-eth1":ip2, "subnet-eth1":subnet2}
            eth2 = {"macaddress-eth2":macaddr[2], "static-eth2":1, "ipaddress-eth2":ip3, "subnet-eth2":subnet3}
            eth3 = {"macaddress-eth3":macaddr[3], "static-eth3":1, "ipaddress-eth3":ip4, "subnet-eth3":subnet4}
            s.modify_system(system, 'modify_interface', eth0, token)
            s.modify_system(system, 'modify_interface', eth1, token)
            s.modify_system(system, 'modify_interface', eth2, token)
            s.modify_system(system, 'modify_interface', eth3, token)
        if gateway:
            s.modify_system(system,"gateway", gateway, token)
        if parameters:
            s.modify_system(system,"ks_meta", parameters, token)
        if cmdline:
            s.modify_system(system,"kernel_options", cmdline, token)
        s.save_system(system, token)
        s.sync(token)
        print "%s created in Cobbler" % name

    def simplecreate(self,name,profile,numinterfaces,dns=None ,macaddr=None,parameters=None,cmdline=None,nextserver=None):
        if dns:
            dns=dns.encode('ascii')
        profile=profile.encode('ascii')
        s = self.s
        token = self.token
        system = s.find_system({"name":name})
        if system!=[]:
            print "%s allready defined in cobbler..." % (name)
            return
        system = s.new_system(token)
        s.modify_system(system, 'name', name, token)
        s.modify_system(system, 'hostname', name, token)
        s.modify_system(system, 'profile', profile, token)
        if nextserver:
            s.modify_system(system, 'server', nextserver, token)
        eth0 = {"macaddress-eth0":macaddr[0]}
        if dns:
            eth0["dnsname-eth0"] = "%s.%s" % (name, dns)
        s.modify_system(system, 'modify_interface', eth0, token)
        if numinterfaces >=2:
            eth1 = {"macaddress-eth1":macaddr[1]}
            s.modify_system(system, 'modify_interface', eth1, token)
        if numinterfaces >=3:
            eth2 = {"macaddress-eth2":macaddr[2]}
            s.modify_system(system, 'modify_interface', eth2, token)
        if numinterfaces >=4:
            eth3 = {"macaddress-eth3":macaddr[3]}
            s.modify_system(system, 'modify_interface', eth3, token)
        if parameters:
            s.modify_system(system,"ks_meta", parameters, token)
        if cmdline:
            s.modify_system(system,"kernel_options", cmdline, token)
        s.save_system(system, token)
        s.sync(token)
        print "%s created in Cobbler\n" % name

    def checkprofile(self,name):
        s = self.s
        for prof in s.get_profiles():
            if prof['name'] == name:
                return True
        return False

    def exists(self,name):
        s = self.s
        if s.find_system({"name":name}) !=[]:
            return True
        return False

    def macexists(self,macs):
        s = self.s
        for mac in macs:
            if s.find_system({"mac_address":mac}) !=[]:
                return True
        return False

    def removemacs(self,macs):
        s = self.s
        token = self.token
        for mac in macs:
            for name in s.find_system({"mac_address":mac}):
                s.remove_system(name,token)
                print "%s sucessfully killed in Cobbler as duplicate" % (name)
        s.sync(token)

    def remove(self,name):
        s = self.s
        token = self.token
        if s.find_system({"name":name}) ==[]:
            print "%s not found in Cobbler" % (name)
        else:
            s.remove_system(name,token)
            s.sync(token)
            print "%s sucessfully killed in Cobbler" % (name)
        return True

    def classes(self):
        allclasses = {}
        s = self.s
        for classe in s.get_mgmtclasses():
            classename = classe['name']
            allclasses[classename] = {}
            i = 0
            for parameter in classe['packages']:
                if len(classe['files']) >= i:
                    parameterinfo = classe['files'][i]
                    parametersplit = parameterinfo.split(',')
                    if len(parametersplit) >1:
                        allclasses[classename][parameter]=[parametersplit,False]
                    else:
                        if parameterinfo.isdigit():
                            parameterinfo = int(parameterinfo)
                        allclasses[classename][parameter]=[parameterinfo,False]
                else:         
                    allclasses[classename][parameter]={}
                i = i+1
        return allclasses
