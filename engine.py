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

vulns.append(newCommandObject('cat /home/kaisa/Desktop/Forensics_1.txt'
             , 'Valoran City Park', True, 6,
             'Forensics Question 1 correct'))
vulns.append(newCommandObject('cat /home/kaisa/Desktop/Forensics_2.txt'
             , '43.6 MiB', True, 6, 'Forensics Question 2 correct'))
vulns.append(newCommandObject('cat /home/kaisa/Desktop/Forensics_3.txt'
             , '/etc/postgresql/12/main/conf.d/pg_ctl.d.conf', True, 6,
             'Forensics Question 3 correct'))
vulns.append(newCommandObject('cat /etc/passwd', 'ahri', True, 2,
             'Created user ahri'))
vulns.append(newCommandObject('cat /etc/group | grep 27', 'ahri', True,
             2, 'Added ahri to "sudo" group'))
vulns.append(newCommandObject('cat /etc/group | grep 27', 'jinx',
             False, 2, 'User jinx is not an administrator'))
vulns.append(newCommandObject('cat /etc/passwd | grep -v "#" | grep fiddlesticks | wc -l'
             , '1', False, 4, 'Removed hidden root fiddlesticks'))
vulns.append(newCommandObject('cat /etc/passwd | grep -v "#" | grep urgot | wc -l'
             , '1', False, 2, 'Removed hidden user urgot'))
vulns.append(newCommandObject('cat /etc/passwd | grep -v "#" | grep zoe | wc -l'
             , '1', False, 2, 'Removed unauthorized user zoe'))
vulns.append(newCommandObject('cat /etc/shadow | grep lux',
             '$6$lpSQPhyvEux4vqN7$5CcsHwirFEhvgFqT8sAojdISP/9wGfdCjHfMZ1aH3xkUV4ze3tQtsyOYYB7bbPYylgcjD86hOuNu08nIAu1Un0:19170'
             , False, 2, 'Changed insecure password for lux'))
vulns.append(newCommandObject('ls /var/log', 'Light_and_Shadow.mp4',
             False, 3, 'Prohibited mp4 file has been removed'))
vulns.append(newCommandObject('ls /usr/share/apps/konsole/random | wc -l'
             , '0', True, 3, 'Prohibited jpg files have been removed'))
vulns.append(newCommandObject('ls /etc/postgresql/12/main/conf.d | wc -l'
             , '0', True, 3, 'Removed plaintext password file'))
vulns.append(newCommandObject('apt list --installed postgresql',
             'installed', False, 2,
             'Postgresql has been disabled or removed'))
vulns.append(newCommandObject('apt list --installed apache2',
             'installed', False, 2,
             'Apache2 has been disabled or removed'))
vulns.append(newCommandObject('apt list --installed aircrack-ng',
             'installed', False, 2,
             'Prohibited software aircrack-ng removed'))
vulns.append(newCommandObject('apt list --installed goldeneye',
             'installed', False, 2,
             'Prohibited software goldeneye removed'))
vulns.append(newCommandObject('cat /etc/ssh/sshd_config | grep "Port"',
             '22', False, 2, 'SSH port is changed'))
vulns.append(newCommandObject('cat /etc/ssh/sshd_config | grep -v "#" | grep PermitRootLogin'
             , 'no', True, 2, 'Root login is not allowed'))
vulns.append(newCommandObject('cat /etc/ssh/sshd_config | grep -v "#" | grep PubkeyAuthentication'
             , 'yes', True, 2, 'Pubkey Authentication is enabled'))
vulns.append(newCommandObject('cat /etc/ssh/sshd_config | grep -v "#" | grep X11Forwarding | head -1'
             , 'no', True, 3, 'X11 forwarding is disabled'))
vulns.append(newCommandObject('cat /etc/ssh/sshd_config | grep "ChrootDirectory"'
             , 'none', False, 4, 'Chroot directory is set'))
vulns.append(newCommandObject('cat /etc/pam.d/common-password | grep minlen | grep [8-999] | wc -l'
             , '1', True, 2, 'Minimum password length is at least 8'))
vulns.append(newCommandObject('cat /etc/pam.d/common-password | grep credit | grep 1 | wc -l'
             , '1', True, 2, 'Password complexity is enforced'))
vulns.append(newCommandObject('cat /etc/pam.d/common-auth | grep unlock_time | grep [900-99999999]'
             , '1', True, 2, 'Lockout length is at least 15 minutes'))
vulns.append(newCommandObject('cat /etc/pam.d/common-auth', 'nullok',
             False, 2, 'Null passwords do not authenticate'))
vulns.append(newCommandObject('ufw status', 'inactive', False, 2,
             'Firewall is enabled'))
vulns.append(newCommandObject('cat /etc/login.defs | grep -E \'(PASS_MAX_DAYS|PASS_MIN_DAYS)\' | grep -v "#" | grep -E \'(99999|0)\' | wc -l'
             , '0', True, 2, 'A default max password age set'))
vulns.append(newCommandObject('cat /etc/sysctl.conf | grep net.ipv4.tcp_syncookies'
             , '1', True, 3, 'IPv4 TCP SYN cookies have been enabled'))
vulns.append(newCommandObject('cat /etc/sudoers', '!authenticate',
             False, 3, 'Sudo requires authentication'))
vulns.append(newCommandObject('cat /home/kaisa/.mozilla/firefox/0bk9coa8.default-release/prefs.js | grep "https_only_mode" | wc -l'
             , '2', True, 4,
             'Firefox security settings have been configured'))
vulns.append(newCommandObject('cat /etc/apt/sources.list | grep -v "#" | grep among'
             , '644', True, 2,
             'Only download security or recommended updates'))
vulns.append(newCommandObject('ls -la /var/spool/cron/crontabs | grep urgot | wc -l'
             , '0', True, 4, 'Removed suspicious cron job'))
vulns.append(newCommandObject("stat -c '%a' /etc/passwd", '644', True,
             3, 'Insecure permissions for passwd file fixed'))
vulns.append(newCommandObject('ufw status verbose | grep ALLOWED', '22'
             , True, 3, 'OpenSSH is allowed through firewall'))


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
