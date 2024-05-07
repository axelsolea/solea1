from smb.SMBConnection import SMBConnection

def mount_smb_share(server_name, share_name, username, password, local_mount_point):
    conn = SMBConnection(username, password, "", server_name)
    conn.connect(server_name, 139)  # Change the port if necessary

    with open(local_mount_point, 'wb') as f:
        conn.retrieveFile(share_name, f)

    conn.close()

if __name__ == "__main__":
    server_name = '172.18.0.251'
    share_name = 'solea_document'
    username = 'alexandre'
    password = 'Solea05alexandre'
    local_mount_point = '/tmp/share'

    mount_smb_share(server_name, share_name, username, password, local_mount_point)
