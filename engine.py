#!/usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep
from subprocess import Popen
from tempfile import TemporaryFile
import math

# image information

UNSCORED = 0
SCORED = 1
PENALTY = 2
INVALID = 3
currMinutes = 0
currHours = 0
runtime = '0:00'
imageName = 'Star Guardians Ubuntu 20'
name = ''


# configuration files; opens file path, creates list using delimiters, checks required configs

class ConfigObject:

    path = ''
    key = ''
    entry = ''
    delim = ''
    keyFound = False
    points = 0
    comment = None

    def check(t):
        if not t.path == '' and not t.key == '' and not t.entry == '' \
            and not t.delim == '':
            f = open(t.path, 'r')
            for line in f.readlines():
                checker = line.split(t.delim)
                t.keyFound = False
                for part in checker:
                    newPart = part.replace(' ', '')
                    newPart = newPart.replace('\n', '')
                    newPart = newPart.replace('\r', '')
                    t.keyFound = t.keyFound or newPart == t.key
                    if t.keyFound:
                        if newPart == t.entry:
                            f.close()
                            return (1, t.points, t.comment)

            f.close()
            return (0, t.points, t.comment)
        print('Object not properly instantiated.')
        return (3, t.points, t.comment)


# user management; checks for user and if their password changes

class UserObject:

    username = ''
    password = ''
    exist = None
    changePw = None
    correct = False
    points = 0
    comment = None

    def check(t):
        f = open('/etc/passwd', 'r')
        if not t.exist == None:
            if t.exist:
                for userLine in f.readlines():
                    user = userLine.split(':')
                    if user[0] == t.username:
                        if t.changePw:
                            f.close()
                            f = open('/etc/shadow', 'r')
                            for userLine in f.readlines():
                                user = userLine.split(':')
                                if user[0] == t.username \
                                    and not user[1] == t.password:
                                    f.close()
                                    return (1, t.points, t.comment)

                            f.close()
                            return (0, t.points, t.comment)
                        f.close()
                        return (1, t.points, t.comment)

                f.close()
                return (2, t.points, t.comment)
            for userLine in f.readlines():
                user = userLine.split(':')
                if user[0] == t.username:
                    f.close()
                    return (0, t.points, t.comment)

            return (1, t.points, t.comment)
        else:
            for userLine in f.readlines():
                user = userLine.split(':')
                if user[0] == t.username:
                    f.close()
                    return (1, t.points, t.comment)

            f.close()
            return (0, t.points, t.comment)
        return


# group management

class MemberObject:

    groupname = ''
    username = ''
    authorized = None
    points = 0
    comment = ''

    def check(t):
        if not t.authorized == None:
            f = open('/etc/group', 'r')
            for groupLine in f.readlines():
                group = groupLine.split(':')
                if group[0] == t.groupname:
                    memberStr = group[3]
                    memberStr = memberStr.replace(' ', '')
                    memberStr = memberStr.replace('\r', '')
                    memberStr = memberStr.replace('\n', '')
                    memberList = memberStr.split(',')
                    if (memberList.count(t.username) > 0) \
                        == t.authorized:
                        f.close()
                        return (1, t.points, t.comment)
                    f.close()
                    return (0, t.points, t.comment)

            return (0, t.points, t.comment)
        return (3, t.points, t.comment)
        return


# checks command usage

class CommandObject:

    command = ''
    output = ''
    expected = None
    points = 0
    comment = ''

    def check(t):
        if not t.expected == None:
            with TemporaryFile() as output:
                cmd = Popen(t.command, stdout=output, shell=True)
                cmd.wait()
                output.seek(0)
                if (str(output.read()).find(t.output) >= 0) == t.expected:
                    return (1, t.points, t.comment)
                return (0, t.points, t.comment)
        else:
            return (3, t.points, t.commment)
        return


# creating new objects

def newConfigObject(
    path,
    key,
    entry,
    delim,
    points,
    comment='',
    ):
    confObj = ConfigObject()
    confObj.path = path
    confObj.key = key
    confObj.entry = entry
    confObj.delim = delim
    confObj.points = points
    confObj.comment = comment
    return confObj


def newUserObject(
    username,
    exist,
    changePw,
    password,
    points,
    comment='',
    ):
    userObj = UserObject()
    userObj.username = username
    userObj.exist = exist
    userObj.changePw = changePw
    userObj.password = password
    userObj.points = points
    userObj.comment = comment
    return userObj


def newCommandObject(
    command,
    output,
    expected,
    points,
    comment='',
    ):
    cmdObj = CommandObject()
    cmdObj.command = command
    cmdObj.output = output
    cmdObj.expected = expected
    cmdObj.points = points
    cmdObj.comment = comment
    return cmdObj


# writes scores onto local html file

def writeScores(
    imageName,
    vulnLines,
    totalPoints,
    currentVulns,
    totalVulns,
    ):
    with open('/opt/temp/Template.html', 'r') as input_file:
        with open('/home/kaisa/Desktop/ScoringReport.html', 'w') as \
            output_file:
            for line in input_file:
                if line.strip() == '{{LIST}}':
                    for vulnLine in vulnLines:
                        output_file.write(vulnLine)
                else:

                    newLine = line
                    newLine = newLine.replace('{{IMAGENAME}}',
                            imageName)
                    newLine = newLine.replace('{{POINTS}}',
                            str(totalPoints))
                    newLine = newLine.replace('{{CURRENT}}',
                            str(currentVulns))
                    newLine = newLine.replace('{{VULNS}}',
                            str(totalVulns))
                    newLine = newLine.replace('{{RUNTIME}}', runtime)
                    namefile = \
                        open('/home/kaisa/Desktop/Set Name for Scoring Report'
                             , 'r')
                    name = namefile.readline()
                    name = name[16:-1]
                    namefile.close()
                    newLine = newLine.replace('{{NAME}}', name)
                    output_file.write(newLine)


# creates list of vulns

vulns = []

'''
Add your vulns here, below is some sample code you can edit

vulns.append(newCommandObject('cat /home/kaisa/Desktop/Forensics_1.txt'
             , 'Valoran City Park', True, 6,
             'Forensics Question 1 correct'))
vulns.append(newCommandObject('cat /etc/passwd | grep -v "#" | grep zoe | wc -l'
             , '1', False, 2, 'Removed unauthorized user zoe'))
vulns.append(newCommandObject('cat /etc/shadow | grep lux',
             '$6$lpSQPhyvEux4vqN7$5CcsHwirFEhvgFqT8sAojdISP/9wGfdCjHfMZ1aH3xkUV4ze3tQtsyOYYB7bbPYylgcjD86hOuNu08nIAu1Un0:19170'
             , False, 2, 'Changed insecure password for lux'))
vulns.append(newCommandObject('apt list --installed goldeneye',
             'installed', False, 2,
             'Prohibited software goldeneye removed'))

'''


# checking vulns

def checkVuln(vuln):
    return vuln.check()


lastPoints = 0
while True:
    vulnLines = []
    totalPoints = 0
    currentVulns = 0
    tracker = 0
    for vuln in vulns:
        tracker += 1
        data = checkVuln(vuln)
        if data[0] == 1:
            totalPoints += data[1]
            currentVulns += 1
            vulnLines.append(data[2] + ' - ' + str(data[1]) + '<br>\n')

    lastPoints = totalPoints
    writeScores(imageName, vulnLines, totalPoints, currentVulns,
                len(vulns))
    currMinutes += .5
    if currMinutes > 59:
        currMinutes = 0
        currHours += 1
    runtime = '%d:%02d' % (currHours, int(math.floor(currMinutes)))
    sleep(30)
