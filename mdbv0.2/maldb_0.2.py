#!/usr/bin/env python

    #Malware DB - the most awesome free malware database on the air
    #Copyright (C) 2014, Yuval Nativ, Lahad Ludar, 5fingers

    #This program is free software: you can redistribute it and/or modify
    #it under the terms of the GNU General Public License as published by
    #the Free Software Foundation, either version 3 of the License, or
    #(at your option) any later version.

    #This program is distributed in the hope that it will be useful,
    #but WITHOUT ANY WARRANTY; without even the implied warranty of
    #MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    #GNU General Public License for more details.

    #You should have received a copy of the GNU General Public License
    #along with this program.  If not, see <http://www.gnu.org/licenses/>.

__version__ = "0.2 Beta"
__appname__ = "Malware DB"
__authors__ = ["Yuval Nativ","Lahad Ludar","5fingers"]
__licensev__ = "GPL v3.0"
__maintainer__ = "Yuval Nativ"
__status__ = "Development"

import sys
import getopt
import subprocess
import csv
import urllib2
# import git
#import os
#import inspect


def main():

    # Set general variables.
    version = __version__
    appname = __appname__
    licensev = __licensev__
    authors = "Yuval Nativ, Lahad Ludar, 5fingers"
    fulllicense = appname + " Copyright (C) 2014 " + authors + "\n"
    fulllicense += "This program comes with ABSOLUTELY NO WARRANTY; for details type '" + sys.argv[0] +" -w'.\n"
    fulllicense += "This is free software, and you are welcome to redistribute it."

    useage='\nUsage: ' + sys.argv[0] +  ' -s search_query -t trojan -p vb\n\n'
    useage += 'The search engine can search by regular search or using specified arguments:\n\nOPTIONS:\n   -h  --help\t\tShow this message\n   -t  --type\t\tMalware type, can be virus/trojan/botnet/spyware/ransomeware.\n   -p  --language\tProgramming language, can be c/cpp/vb/asm/bin/java.\n   -u  --update\t\tUpdate malware index. Rebuilds main CSV file. \n   -s  --search\t\tSearch query for name or anything. \n   -v  --version\tPrint the version information.\n   -w\t\t\tPrint GNU license.\n'

    column_for_pl = 6
    column_for_type = 2
    column_for_location = 1
    colomn_for_time = 7
    column_for_version = 4
    column_for_name = 3
    column_for_uid = 0
    column_for_arch = 8
    column_for_plat = 9
    conf_folder = 'conf'
    eula_file = conf_folder + '/eula_run.conf'
    maldb_ver_file = conf_folder + '/db.ver'
    main_csv_file = conf_folder + '/index.csv'
    giturl = 'https://raw.github.com/ytisf/theZoo/master/'

    # Function to print license of malware-db
    def print_license():
        print ""
        print fulllicense
        print ""

    # Check if EULA file has been created
    def check_eula_file():
        try:
            with open(eula_file):
                return 1
        except IOError:
                return 0

    def get_maldb_ver():
        try:
            with file(maldb_ver_file) as f:
                return f.read()
        except IOError:
            print("No malware DB version file found.\nPlease try to git clone the repository again.\n")
            return 0

    def update_db():
        curr_maldb_ver = get_maldb_ver()
        response = urllib2.urlopen(giturl+maldb_ver_file)
        new_maldb_ver = response.read()
        if new_maldb_ver == curr_maldb_ver:
            print "No need for an update.\nYou are at " + new_maldb_ver + " which is the latest version."
            sys.exit(1)
        # Write the new DB version into the file
        f = open(maldb_ver_file, 'w')
        f.write(new_maldb_ver)
        f.close()

        # Get the new CSV and update it
        csvurl = giturl + main_csv_file
        u = urllib2.urlopen(csvurl)
        f = open(main_csv_file, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (main_csv_file, file_size)
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
        print status,
        f.close()

    # prints version banner on screen
    def versionbanner():
        print ""
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print "\t\t    " + appname + ' v' + version
        print "Built by:\t\t" + authors
        print "Is licensed under:\t" + licensev
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print fulllicense
        print useage

    # Check if maybe no results have been found
    def checkresults(array):
        if len(array) == 0:
            print "No results found\n\n"
            sys.exit(1)

    # Check to needed arguments - left for debugging
    def checkargs():
        print "Type: " + type_of_mal
        print "Lang: " + pl
        print "Search: " + search

    # Sort arrays
    def filter_array(array,colum,value):
        ret_array = [row for row in array if value in row[colum]]
        return ret_array

    # A function to print banner header
    def res_banner():
        print "\nUID\tName\t\tVersion\t\tLocation\t\tTime"
        print "---\t----\t\t-------\t\t--------\t\t----"

    # print_results will surprisingly print the results...
    def print_results(array):
        answer = array[column_for_uid] + "\t" + array[column_for_name]+ "\t" + array[column_for_version] + "\t\t"
        answer += array[column_for_location] + "\t\t" + array[colomn_for_time]
        print answer

    options, remainder = getopt.getopt(sys.argv[1:], 'hwuvs:p:t:', ['type=', 'language=', 'search=', 'help', 'update', 'version', 'dbv' ])

    # Zeroing everything
    type_of_mal = ""
    pl = ""
    search = ""
    new =""
    update=0
    m=[];
    a=0
    eula_answer='no'
    f = ""

    # Checking for EULA Agreement
    a = check_eula_file()
    if a == 0:
        print appname + ' v' + version
        print 'This program contain live and dangerous malware files'
        print 'This program is intended to be used only for malware analysis and research'
        print 'and by agreeing the EULA you agree to only use it for legal purposes and '
        print 'studying malware.'
        print 'You understand that these file are dangerous and should only be run on VMs'
        print 'you can control and know how to handle. Running them on a live system will'
        print 'infect you machines will live and dangerous malwares!.'
        print ''
        eula_answer = raw_input('Type YES in captial letters to accept this EULA.\n')
        if eula_answer == 'YES':
            print 'you types YES'
            new = open(eula_file, 'a')
            new.write(eula_answer)
        else:
            print 'You need to accept the EULA.\nExiting the program.'
            sys.exit(1)

    # Get arguments
    for opt, arg in options:
        if opt in ('-h', '--help'):
            print fulllicense
            print useage
            sys.exit(1)
        elif opt in ('-u', '--update'):
            update=1
            update_db()
        elif opt in ('-v', '--version'):
            versionbanner()
            sys.exit(1)
        elif opt in '-w':
            print_license()
            sys.exit(1)
        elif opt in ('-t', '--type'):
            type_of_mal = arg
        elif opt in ('-p', '--language'):
            pl = arg
        elif opt in ('-s', '--search'):
            search = arg
        elif opt in '--dbv':
            # Getting version of malware-DB's database
            a = get_maldb_ver()
            if a == 0:
                sys.exit(0)
            elif len(a) > 0:
                print ''
                print "Malware-DB Database's version is: " + a
                sys.exit()

    # Rebuild CSV
    if update == 1:
        subprocess.call("./Rebuild_CSV.sh", shell=True)
        sys.exit(1)

    # Take index.csv and convert into array m
    csvReader = csv.reader(open(main_csv_file, 'rb'), delimiter=',');
    for row in csvReader:
        m.append(row)

    # Filter by type
    if len(type_of_mal) > 0:
        m = filter_array(m,column_for_type,type_of_mal)

    # Filter by programming language
    if len(pl) > 0:
        m = filter_array(m,column_for_pl,pl)

    # Free search handler
    if len(search) > 0:
        res_banner()
        matching = [y for y in m if search in y]
        for line in matching:
            checkresults(matching)
            print_results(line)

    if len(search) <= 0:
        res_banner()
        for line in m:
            print_results(line)

if __name__ == "__main__":
    main()