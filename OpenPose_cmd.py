import os
import subprocess


def Cmd_process(route):
    filename_list = os.listdir(route)
    filecount = []
    for item in filename_list:
        path = os.path.join(route, item)
        if item.startswith('id'):
            path = os.path.join(path, '/' + item + '/facial_expression/kinect_color')
            cmd = 'bin\\OpenPoseDemo.exe --image_dir ' + path + ' --face --write_json' + ' E:\\json\\' + item
            print(cmd)
            # process = subprocess.Popen(cmd, shell=True)
            # process.wait()


if __name__ == '__main__':
    Cmd_process('Z:\\dataset')

# cmd = "python " + path
# process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# process.wait()
# command_output = process.stdout.read().decode('utf-8')
# print(command_output)

# process = subprocess.Popen(cmd, shell=True)
# process.wait()
