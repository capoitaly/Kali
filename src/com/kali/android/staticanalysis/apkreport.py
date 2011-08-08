'''
Created on Aug 2, 2011

@author: alex
'''
import sys
import hashlib

PATH_INSTALL = "./"
sys.path.append(PATH_INSTALL + "./core/")
sys.path.append(PATH_INSTALL + "./core/bytecodes")

import apk

x = apk.APK("/home/alex/malware/iCalendar acbcad45094de7e877b656db1c28ada2.apk")

n = x.get_package()
p = str(x.get_details_permissions())
a = str(x.get_activities())
s = str(x.get_services())
r = str(x.get_receivers())
o = str(x.get_providers())


f = open ( n, 'r+')
md5sum = hashlib.md5(f.read()).hexdigest()
f.write ('[App Name]\n')
f.write (n)
f.write ('\n[Hash MD5]\n')
f.write (md5sum)
f.write ('\n\n[Permission Used]\n')
f.write (p)
f.write ('\n\n[Activities]\n')
f.write (a)
f.write ('\n\n[Services]\n')
f.write (s)
f.write ('\n\n[Receivers]\n')
f.write (r)
f.write ('\n\n[Providers]\n')
f.write (o)


f.close()
