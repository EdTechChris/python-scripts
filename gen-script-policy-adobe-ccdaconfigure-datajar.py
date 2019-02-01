#!/usr/bin/python
'''
Copyright (c) 2016, dataJAR Ltd.  All rights reserved.

     Redistribution and use in source and binary forms, with or without
     modification, are permitted provided that the following conditions are met:
             * Redistributions of source code must retain the above copyright
               notice, this list of conditions and the following disclaimer.
             * Redistributions in binary form must reproduce the above copyright
               notice, this list of conditions and the following disclaimer in the
               documentation and/or other materials provided with the distribution.
             * Neither data JAR Ltd nor the
               names of its contributors may be used to endorse or promote products
               derived from this software without specific prior written permission.

     THIS SOFTWARE IS PROVIDED BY DATA JAR LTD "AS IS" AND ANY
     EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
     WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
     DISCLAIMED. IN NO EVENT SHALL DATA JAR LTD BE LIABLE FOR ANY
     DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
     (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
     LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
     ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
     (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
     SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

SUPPORT FOR THIS PROGRAM

    This program is distributed "as is" by DATA JAR LTD.
    For more information or support, please utilise the following resources:

            http://www.datajar.co.uk

DESCRIPTION gen-script-policy-adobe-ccdaconfigure.py

Amends the file /Library/Application Support/Adobe/OOBE/Configs/ServiceConfig.xml
to not offer updates:
https://helpx.adobe.com/creative-cloud/packager/customize-creative-cloud-app.html

Pass true/false to $4 & $5
'''

# Standard imports
import errno
import logging
import os
import xml.etree.cElementTree as ET
import sys

# Constants
VERSION = '1.2'
SCRIPT_NAME = os.path.basename(sys.argv[0])
DEBUG_DIR = '/private/var/log/managed/'
DEBUG_FILE = os.path.join(DEBUG_DIR, os.path.basename(sys.argv[0]) + '.log')
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'
LOG_FILEMODE = 'w'
XML_FILE = '/Library/Application Support/Adobe/OOBE/Configs/ServiceConfig.xml'

# Functions
def setup():
    '''
    Generic setup function, make sure we're root & debug dir exists.
    If all present & correct, start logging
    '''
    if os.geteuid() != 0:
        ''' Exit if not root'''
        print "This script must be run as root"
        sys.exit(1)
    ''' make DEBUG_DIR folder if missing '''
    mkdir_p(DEBUG_DIR)
    ''' Configure logging & write out standard text '''
    logging.basicConfig(filename=DEBUG_FILE, level=LOG_LEVEL, \
                   format=LOG_FORMAT, filemode=LOG_FILEMODE)
    ''' Send text to console as well as log'''
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(LOG_FORMAT)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    ''' Write out generic log '''
    logging.info('###################-START-##################')
    logging.info('')
    logging.info('dataJAR IT Services')
    logging.info('')
    logging.info('Running %s', SCRIPT_NAME)
    logging.info('')
    logging.info('Script version %s', VERSION)
    logging.info('')

def appsvisible():
    ''' Find the App Panel key in the xml & set to $4 '''
    if os.path.isfile(XML_FILE):
        logging.info('Found %s', XML_FILE)
        logging.info('')
        try:
            tree = ET.ElementTree(file=XML_FILE)
            root = tree.getroot()
            for appspanel in root.iter('panel'):
                appspanel.find('visible').text = APPS_PANEL_VISIBILITY
                with open(XML_FILE, "w") as xmlfile:
                    tree.write(xmlfile)
                logging.info('Updated show Apps Panel option in %s to %s', \
                                          XML_FILE, APPS_PANEL_VISIBILITY)
                logging.info('')
        except:
            logging.error('There was an error reading the ServiceConfig.xml')
            finish()
            sys.exit(1)
    else:
        logging.info('Cannot find %s', XML_FILE)
        logging.info('')

def selfserviceinstalls():
    ''' Find the Self Service Installs key in the xml & set to $5 '''
    if os.path.isfile(XML_FILE):
        logging.info('Found %s', XML_FILE)
        logging.info('')
        try:
            tree = ET.ElementTree(file=XML_FILE)
            root = tree.getroot()
            for selfserveinstall in root.iter('feature'):
                selfserveinstall.find('enabled').text = SELF_SERVICE_INSTALLS
                with open(XML_FILE, "w") as xmlfile:
                    tree.write(xmlfile)
                logging.info('Updated show Self Service Installs option in %s to %s', \
                									 XML_FILE, SELF_SERVICE_INSTALLS)
                logging.info('')
        except:
            logging.error('There was an error reading the ServiceConfig.xml')
            finish()
            sys.exit(1)
    else:
        logging.info('Cannot find %s', XML_FILE)
        logging.info('')


def finish():
    ''' Generic finish function'''
    logging.info('###################-END-##################')

def mkdir_p(path):
    '''
    Make path directories if they are missing
    '''
    try:
        os.makedirs(path)
        os.chmod(path, 0o777)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

if __name__ == '__main__':
    ''' Functions to run through & variable check'''
    setup()
    try:
        APPS_PANEL_VISIBILITY = 'false'
        SELF_SERVICE_INSTALLS = 'false'
    except:
        logging.error('$4 or $5 not defined')
        logging.error('')
        finish()
        sys.exit(1)
    appsvisible()
    selfserviceinstalls()
    finish()
