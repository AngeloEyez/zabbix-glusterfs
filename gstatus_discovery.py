#!/usr/bin/python3
import json
import subprocess
import sys

gluster_volume_names = []
gstatus_output = subprocess.check_output('gstatus -a -o json 2>/dev/null', shell=True).decode()
gluster_info = json.loads(gstatus_output)
volume_list = gluster_info["data"]["volume_summary"]


nargs = len(sys.argv)

if nargs == 1:
    for volume in volume_list:
        gluster_volume_names.append({"{#VOLUME_NAME}": volume["name"]})
    print(json.dumps({'data': gluster_volume_names}))

elif nargs == 2:
    if sys.argv[1] in ["size_total", "size_used", "snapshot_count"]:
       	s = 0
        for volume in volume_list:
            s += volume[sys.argv[1]]
        print(s)
    else:
       print(gluster_info['data'][sys.argv[1]])
    

elif nargs == 3:
    for volume in volume_list:
        if volume.get('name') and sys.argv[2] == volume["name"]:
            if sys.argv[1] == "nr_entries":
                healinfo_list=volume["healinfo"]
                nrents = 0
                for heal in healinfo_list:
                    nrents += int(heal["nr_entries"])
                print(nrents)
            else:
                print(json.dumps(volume[sys.argv[1]]))
            break
    else:
        if sys.argv[1] == "health":
            print('down')
        else:
            print()

else:
    print('Wrong arguments')


