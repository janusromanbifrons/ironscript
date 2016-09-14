from scp import SCPClient

def grab(client,rem_file,local_file):
    scp = SCPClient(client.get_transport())
    scp.get(rem_file, local_file)
    scp.close()

    return 0

def push(client,local_file,rem_file):
    scp = SCPClient(client.get_transport())
    scp.put(local_file,rem_file)
    scp.close()

    return 0
