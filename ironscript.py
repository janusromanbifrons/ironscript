#/usr/local/bin/python

# IronPort-Python Scripting Utility (IronScript)
# This allows for automation of various actions on the Ironport Security Appliances from an external system.

# Imports
import sys
import argparse     # For getting the arguments
import paramiko     # For SSH
import base64       # To decode base64 incoded stuff.
import logging      # For right and proper logging.

# IronScript imports
import iconfig
import ifile

# Log Setup
logger = logging.getLogger('IronScript')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('ironscript.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

# Setting defaults
username = 'admin'
local_file = './downloads'
rem_file = 'config/'

# Get dem arguments
parser = argparse.ArgumentParser(description='Cisco Ironport external scripting CLI (IronScript)\n This tool was written by with the purpose of making automated interaction possible with the Cisco ESA/SMA/WSA. The minimum required aruments are the FQDN of the appliance, the action to be performed, and either \'-k\' or \'-u\' authentication options.', epilog='... and that is how you script the iron!')
parser.add_argument("address", help="IP or FQDN of Ironport Appliance")
parser.add_argument("action", help="The action to be performed.")
parser.add_argument('-u',"--user", action='store', dest='username',help='The username to connect and interact with the Ironport appliance (Default = \'admin\')')
parser.add_argument('-p',"--pass", action='store', dest='password',help='The password that will be used. NOT RECOMMENDED. The \'-k\' option will override this.')
parser.add_argument('-R',"--remote", action='store', dest='remote',help='Remote file to be uploaded or downloaded.')
parser.add_argument('-L',"--local", action='store', dest='local',help='Local file to be uploaded or downloaded.')
args = parser.parse_args()

# Overwrite necissary defaults (only if specified)
if args.username: username = args.username
if args.local: local_file = args.local
if args.remote: rem_file = args.remote

# Log Paramiko SSH
paramiko.util.log_to_file('ssh.log')

# SSH Connect
client = paramiko.SSHClient()
client.load_system_host_keys()

try:
    logger.info('Logging in as ' + username)
    if args.password: client.connect(args.address, username=username, password=args.password)
    else: client.connect(args.address, username=username)
    logger.info('... logged in successfully.')
    pass
except:
    logger.error('Could not log into Ironport Appliance.')
    sys.exit()

if (args.action == 'saveconfig'):
    logger.info('Saving configuration...')
    rem_file,filename = iconfig.save(client)
    logger.info('... configuration file successfully saved as ' + filename)
    print('Successfully saved as ' + filename)
elif (args.action == 'grabconfig'):
    logger.info('Saving configuration as ' + username)
    rem_file,filename = iconfig.save(client)
    logger.info('Downloading configuration from appliance to ' + local_file)
    ifile.grab(client,rem_file,local_file)
    logger.info('Configuration successfully saved to ' + local_file + '/' + filename)
elif (args.action == 'loadconfig'):
    if args.local and args.remote:
        logger.error("Please specify a remote OR local file to load (not both).")
        sys.exit()
    elif args.local:
        logger.info('Pushing ' + local_file + 'to the appliance.')
        ifile.push(client,local_file,'configuration/')
        rem_file = local_file
        logger.info('Loading the configuration...')
        iconfig.load(client,rem_file)
        logger.info('... configuraiton loaded and commited.')
        sys.exit
    elif args.remote:
        logger.info('Loading the configuration...')
        iconfig.load(client,rem_file)
        logger.info('... configuraiton loaded and commited.')
    else:
        logger.error("You do need to select a remote or Local file to load.")
elif (args.action == 'pushfile'):
    logger.info('Pushing... ' + local_file)
    ifile.push(client,local_file,rem_file)
    logger.info('... pushed to ' + rem_file + 'on the appliance.')
elif (args.action == 'grabfile'):
    logger.info('Grabbing ' + rem_file)
    ifile.grab(client,rem_file,local_file)
    logger.info('... successfully grabbed ' + rem_file)
elif (args.action == 'commit'):
    logger.info('Committing changes...')
    iconfig.commit(client)
    logger.info('... changes commited.')
else:
    logger.error('Aciton ' + args.action + ' not recognized. Pelase review the options using the -h option.')

# Close SSH Session
client.close()
