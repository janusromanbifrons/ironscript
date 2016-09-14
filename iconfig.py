import re

def save(client):
    stdin, stdout, stderr = client.exec_command('saveconfig yes')
    for line in stdout:
        result = re.search('file (.+?) has', line)
        if result:
            filename = result.group(1)
            file_loc = 'configuration/' + filename
            break
        else:
            print('ERROR: Filename could not be determined.')
            sys.exit
    return file_loc, filename


def load(client,rem_file):
    rem_file = re.sub(r'.*/','',rem_file)
    command = 'loadconfig ' + rem_file + '; commit IronScript'
    stdin, stdout, stderr = client.exec_command(command)
    return 0

def commit(client):
    stdin, stdout, stderr = client.exec_command('commit IronScript')
    return 0
