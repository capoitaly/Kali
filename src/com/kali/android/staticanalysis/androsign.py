#!/usr/bin/env python

# This file is part of Androguard.
#
# Copyright (C) 2010, Anthony Desnos <desnos at t0t0.org>
# All rights reserved.
#
# Androguard is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Androguard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Androguard.  If not, see <http://www.gnu.org/licenses/>.

import sys, os

from optparse import OptionParser

import androguard, androconf, apk, dvm, msign

option_0 = { 'name' : ('-i', '--input'), 'help' : 'file : use this filename', 'nargs' : 1 }
option_1 = { 'name' : ('-d', '--directory'), 'help' : 'directory : use this directory', 'nargs' : 1 }
option_2 = { 'name' : ('-b', '--database'), 'help' : 'databese : use this database', 'nargs' : 1 }
option_3 = { 'name' : ('-v', '--version'), 'help' : 'version of the API', 'action' : 'count' }

options = [option_0, option_1, option_2, option_3]

def main(options, arguments) :
    if options.database == None :
        return

    if options.input != None :
        s = msign.MSignature( options.database )

        ret_type = androconf.is_android( options.input ) 
        if ret_type == "APK" :
            a = apk.APK( options.input )
            if a.is_valid_APK() :
                s.check_apk( a )
        elif ret_type == "DEX" :
            vm = dvm.DalvikVMFormat( open(options.input, "rb").read() )
            s.check_dex( open(options.input, "rb").read() )
    elif options.directory != None :
        s = msign.MSignature( options.database )
        for root, dirs, files in os.walk( options.directory, followlinks=True ) :
            if files != [] :
                for f in files :
                    real_filename = root
                    if real_filename[-1] != "/" :
                        real_filename += "/"
                    real_filename += f

                    ret_type = androconf.is_android( real_filename )
                    if ret_type == "APK"  :
                        print real_filename, "--->",
                        try : 
                            a = apk.APK( real_filename )
                            if a.is_valid_APK() :
                                s.check_apk( a )
                            else :
                                print "INVALID"
                        except Exception, e :
                            print "ERROR"
                    elif ret_type == "DEX" :
                        try :
                            print real_filename, "--->",
                            s.check_dex( open(real_filename, "rb").read() )
                        except Exception, e : 
                            print "ERROR"

    elif options.version != None :
        print "Androsign version %s" % androconf.ANDROSIGN_VERSION

if __name__ == "__main__" :
    parser = OptionParser()
    for option in options :
        param = option['name']
        del option['name']
        parser.add_option(*param, **option)

    options, arguments = parser.parse_args()
    sys.argv[:] = arguments
    main(options, arguments)
