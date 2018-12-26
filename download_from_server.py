"""
通过paramiko从远处服务器下载文件资源到本地
"""
import paramiko
import os
from stat import S_ISDIR as isdir


def down_from_remote(sftp_obj, remote_dir_name, local_dir_name):
    """远程下载文件"""
    remote_file = sftp_obj.stat(remote_dir_name)
    if isdir(remote_file.st_mode):
        # 文件夹，不能直接下载，需要继续循环
        check_local_dir(local_dir_name)
        print('开始下载文件夹：' + remote_dir_name)
        for remote_file_name in sftp_obj.listdir(remote_dir_name):
            sub_remote = os.path.join(remote_dir_name, remote_file_name)
            sub_remote = sub_remote.replace('\\', '/')
            sub_local = os.path.join(local_dir_name, remote_file_name)
            sub_local = sub_local.replace('\\', '/')
            down_from_remote(sftp_obj, sub_remote, sub_local)
    else:
        # 文件，直接下载
        print('开始下载文件：' + remote_dir_name)
        sftp_obj.get(remote_dir_name, local_dir_name)


def check_local_dir(local_dir_name):
    """本地文件夹是否存在，不存在则创建"""
    if not os.path.exists(local_dir_name):
        os.makedirs(local_dir_name)


def get_sftp():
    """建立一个服务器的连接"""
    # 服务器的IP地址, 引号引起来
    host_name = ''
	# 用户名
    user_name = ''
	# 密码
    password = ''
	# 端口号
    port = 22

    # 连接远程服务器
    t = paramiko.Transport((host_name, port))
    t.connect(username=user_name, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    return sftp,t


def main(remote_dir, local_dir):
    # remote_dir:远程文件路径（需要绝对路径）
    # local_dir: 本地文件存放路径（绝对路径或者相对路径都可以）
    sftp, t = get_sftp()
    # 远程文件开始下载
    down_from_remote(sftp, remote_dir, local_dir)
    # 关闭连接
    t.close()


if __name__ == "__main__":
    # 服务器中的绝对路径
    remote_dir = ''
	# 下载到本地之后的本地路径
    local_dir = ''
    main(remote_dir, local_dir)







