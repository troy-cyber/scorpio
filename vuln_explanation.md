# Checking Vulnerabilities
Here is sample code on a wide variety of vulnerabilities. All vulnerabilities will be written with the user `kim`.

There are 5 parameters in the `CommandObject`. Going from left to right, they are:
1. the command to check the vuln
2. what to check for in the result of the command
3. if the command was checked for that value, put True. If it was checked for not being that value, put False.
4. number of points assigned for that vulnerability
5. Scoring Report message

### Forensic Question
> spaces are allowed
```python
vulns.append(newCommandObject('cat /home/kim/Desktop/Forensics_1.txt', 'answer', True, 6, 'Forensics Question 1 correct'))
```
### Added a user
```python
vulns.append(newCommandObject('cat /etc/passwd | grep -w kim | wc -l', '1', True, 2, 'Created user kim'))
```
### Removed a user
> hidden or otherwise
```python
vulns.append(newCommandObject('cat /etc/passwd | grep -v "#" | grep -w kim | wc -l', '0', True, 2, 'Removed user kim'))
```
### Added a user to sudo group
```python
vulns.append(newCommandObject('cat /etc/group | grep -v "#" | grep -w sudo', 'kim', True, 2, 'Added kim to "sudo" group'))
```
### Removed a user from sudo group
```python
vulns.append(newCommandObject('cat /etc/group | grep -v "#" | grep -w sudo | grep -w kim | wc -l', '1', False, 2, 'Removed kim from sudo group'))
```
### Changed password for user
```python
vulns.append(newCommandObject('cat /etc/shadow | grep kim', '$6$5asdf23qfsdASDASDas32asdf232MOQWDKUn5x23423awwfasdk2cvgc2342afsdAgliwid2HAQX.snudnxSRPePZ0:192328', False, 2, 'Changed password for kim'))
```
### Removed file
```python
vulns.append(newCommandObject('ls /var/log', 'music.mp4', False, 3, 'Prohibited file has been removed'))
```
### Firewall is enabled
```python
vulns.append(newCommandObject('ufw status', 'inactive', False, 2,'Firewall is enabled'))
```
### Service is allowed through firewall
```python
vulns.append(newCommandObject('ufw status verbose | grep ALLOWED', '21', True, 3, 'FTP is allowed through firewall'))
```
### Package disabled or removed
```python
vulns.append(newCommandObject('apt list --installed postgresql','installed', False, 2,'Postgresql has been disabled or removed'))
```