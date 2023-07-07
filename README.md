# Scorpio
This is a scoring engine for the Ubuntu OS in the vein of the scoring engine from the CyberPatriot competition. It checks to see if a student has found vulnerabilities on the system and provides real-time feedback. 

For example, the scoring engine will reward points to the student if they turn on the firewall. This allows students to gain hands-on experience at securing everything from web servers to standalone workstations. 

The Windows-equivalent can be found [here](https://github.com/troy-cyber/windows-scorpio)

## How it works:
The teacher implements a list of vulnerabilities on a virtual machine and records them in `engine.py`, which will run every 30 seconds. As the student secures the system, the scoring engine will update `Template.html` to display a list of the vulnerabilites that the student found correctly. The student is finished when they reach all 100 points or when the teacher calls time. 

#### Instructions

Here's a [better formatted version](https://xenonminer.github.io/2023/06/15/scorpio_linux_setup/) of this explanation.

On the desktop, create a file named `Set Name for Scoring Report` and write inside: `YOUR FULL NAME: [id]`.

Make the directory `/opt/temp` and then copy `cp_logo.jpeg`, `tts.jpg`, `engine.py`, `Template.html`, and `time.txt` into `/opt/temp/`. Make sure the permissions on `/opt/temp` and the contents inside are owned by the standard user that the competitor is intended to use (not root or anyone else). 
    
Make `/opt/temp` readable to that standard user:
```bash
chmod u+r /opt/temp/* /opt/temp
```
Install `python2`, `python-pip`, and `git`.

> yes this runs in python2 **NOT** python3

Use to pip to install requests (and any other libraries needed by `engine.py`).

Forensics questions should be named like: `/home/[username]/Desktop/Forensics_[#]`

> Example: `/home/mando/Desktop/Forensics_1`

In `engine.py`, change the variables `imageName`, `imageUserName` to whatever you want.
> for users who are intended to have poor passwords, create them using `useradd` instead of `adduser`.

> AVOID USING SPACES IN ANY FILENAMES. For example, `this_is_a_vuln.mp3` instead of `this is a vuln.mp3`.

Add vulns using:
```python
vulns.append([specific vuln])
```
The template file [here](vuln_explanation.md) gives some examples how.

Compile the code using [pyconcrete](https://pypi.org/project/pyconcrete/) or cython.

```bash
git clone <pyconcrete repo> <pyconcre dir>	
```
install pyconcrete
```bash
python setup.py install
pyconcrete-admin.py compile --source=/opt/temp --pye
pyconcrete engine.pye
```
    
To use pyconcrete, keep the `.pye` file, but remove the `.py` files (once everything is tested). From this point on, the way to run the scoring engine will be `pyconcrete engine.pye`.

Now, create a service for the scoring engine (instructions below). Run the engine at least once to create `ScoringReport.html` and then create a symlink:
```bash
ln -s /opt/temp/ScoringReport.html /home/$USER/Desktop/ScoringReport.html)
```
Also, we need to clear history. To do that we create aliases in `/root/.bashrc` and `/home/$USER/.bashrc` with the line `export HISTFILE=/dev/null`

We also need to REMOVE `engine.py` FROM THE ENTIRE SYSTEM (ex: make sure it's not in your trashbin). 

> It would defeat the point of compiling if one can find the decompiled version somewhere with the vulns, wouldn't it?

#### Setting up the scoring engine

create file `/lib/systemd/system/engine.service` add below into it

```bash
[Unit]
Description=Scoring Engine
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=root
ExecStart=(path to pyconcrete cmd) /opt/temp/engine.pye

[Install]
WantedBy=multi-user.target
```
#### Testing the scoring engine
```bash
    systemctl daemon-reload
    systemctl enable engine
    reboot
    systemctl status engine
```
