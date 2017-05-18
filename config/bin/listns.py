#!/usr/bin/python2

import pprint
from SOAPpy import WSDL

soap = WSDL.Proxy('https://www.ovh.com/soapi/soapi-re-1.63.wsdl')

#login
session = soap.login('cm59247-ovh', 'AG9bbDF5', 'fr', 0)
print "login successfull"

#domainList
result = soap.domainHostList(session, 'chataigner.me')
print "domainList successfull"
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(result) # your code here ...

#logout
soap.logout(session)
print "logout successfull"
