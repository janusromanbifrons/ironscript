IronScript
==========

IronPort external scripting CLI (IronScript). This tool was written by
with the purpose of making automated interaction possible with the AsyncOS based appliances.

### Installation:

The first and most import component step is to install Python 2.x on your system. _IronScript_ was developed on `Python 2.7.11`; however, any 2.X release should work. Module list below.

Required Modules:
* paramiko
* argparse
* base64
* logging
* scp
* re

### Command Usage:

#### Overview

    python ironscript.py -h
    usage: ironscript.py [-h] [-k KEY] [-u USERNAME] [-p PASSWORD] [-R REMOTE]
                         [-L LOCAL]
                         address action

    Cisco Ironport external scripting CLI (IronScript) This tool was written by
    with the purpose of making automated interaction possible with the Cisco
    ESA/SMA/WSA. The minimum required aruments are the FQDN of the appliance, the
    action to be performed, and either '-k' or '-u' authentication options.

    positional arguments:
      address               IP or FQDN of Ironport Appliance
      action                The action to be performed.

    optional arguments:
      -h, --help            show this help message and exit
      -k KEY, --key KEY     Should Pub-Key authentication be used? (Default = TRUE)
      -u USERNAME, --user USERNAME
                            The username to connect and interact with the Ironport appliance (Default = 'admin')
      -p PASSWORD, --pass PASSWORD
                            The password that will be used. NOT RECOMMENDED. The'-k' option will override this.
      -R REMOTE, --remote REMOTE
                            Remote file to be uploaded or downloaded.
      -L LOCAL, --local LOCAL
                            Local file to be uploaded or downloaded.

    ... and that is how you script the iron!



###### SAVECONFIG
This action performs the same action through IronScript that it would directly on the appliance. (The configuration file is dumped into the `configuration/` directory). _BONUS_: This also shows a connection using the password argument, which is __NOT__ recommended as the password will be in your command history in cleartext (See [Best Practices](#bp)).

    python ironscript.py 192.168.2.5 saveconfig
    python ironscript.py 192.168.2.5 saveconfig -p Ironport123.


###### GRABCONFIG
Much the same as `saveconfig`; however, we copy the freshly generated configuration file to the local system. _A copy of the config will still reside on the appliance._ This action will by default save the configuration to the `downloads/` directory unless specified with the `-L` flag.


    python ironscript.py 192.168.2.5 grabconfig
    python ironscript.py 192.168.2.5 grabconfig -L /path/to/directory/


###### LOADCONFIG
THis action will instruct the appliance to import a configuration file, effectivly `loadconfig` then `commit`. Either a file on the workstation __OR__ the appliance can be specified to be loaded. If the file resides on the local workstation, it will be uploaded to the appliance before loading. (`-L` is a file local to the workstation, `-R` is the file on the appliance).


    python ironscript.py 192.168.2.5 loadconfig -L /path/to/config.xml
    python ironscript.py 192.168.2.5 loadconfig -R config.xml


###### PUSHFILE
This can allow you to push any file or directory to the appliance, and it requires the `-L` and `-R` arguments. This can be used to upload End User Notificaiton (EUN) pages or other resources.


    python ironscript.py 192.168.2.5 pushfile -L /path/to/upload/file.ext -R directory/on/applaince/


###### GRABFILE
The same concept, but reverse direction of the `pushfile` action. This will allow you to pull specific files from the appliance. This would be ideal the logs are not being `syslog`d off of the appliance. Additionally, the behavior from `grabconfig` means the `-L` flag is optional, and files will be saved to `downloads/` by default.

    python ironscript.py 192.168.2.5 grabfile -R path/to/file/on/applaince.ext
    python ironscript.py 192.168.2.5 grabfile -L /path/to/downoad/ -R path/to/file/on/applaince.ext


###### COMMIT
This essentialy is an alias for the `commit` on the appliance. This is useful for pushing through configuraiton changes that are locked in a IronScript's SSH session on the appliance.


    python ironscript.py 192.168.2.5 commit


###### USER FLAG
By default, the `admin` user will be used. However, you can specify the user that will interact with the appliance. The example below demonstrates the `operator` user.


    python ironscript.py 192.168.2.5 -u operator commit


Best Practices:<a name="bp"></a>
---------------

### Security:
The ideal usage of this project is as automated framework for your security appliance. That being said, hardcoding the password into the command with the `-p` option isn't recommended as it leaves the password in cleartext in your command history.

The answer to this is configuring SSH Public Key Authentication for the user that will be executing the IronScript commands. This helps two-fold: 1) no more cleartext passwords, 2) the additional security benefits of a long SSH key.

You can click [HERE](http://www.cisco.com/c/en/us/support/docs/security/email-security-appliance/118305-technote-esa-00.html) to read though the official documentation on how to configure this. The link above references the email appliance; however, this documentation is applicable to the proxy and management appliances without any changes. (Additionally, Mac OS Users can follow the _Linux/Unix_ instructions).

### Pratical Examples:
The original goal of this project was to allow to backup configuration files at a set interval. On a \*NIX system, this sounds like a job for `cron`.

Below is a snippet from a `crontab` that will automatically backup a configuration file every Sunday morning.


    0 3 * * 7 backupbot /usr/bin/python /opt/ironscript/ironscript.py 10.0.0.10 grabconfig -u operator -L /mnt/backups/ironport

A quick breakdown of what all this means below, and you can adjust as you see fit.
* Minute: `0` (0-59)
* Hour: `3` (0-23)
* Day of Month: `any` (1-31)
* Month: `any` (1-12)
* Day of week: `7` (1-7)
* User on client: `backupbot`
* Path to Python: `/usr/bin/python`
* Path to IronScript: `/opt/ironscript/ironscript.py`
* IP of appliance: `10.0.0.10`
* Action: `grabconfig`
* User on appliance: `operator`
* Local save directory: `/mnt/backups/ironport`
