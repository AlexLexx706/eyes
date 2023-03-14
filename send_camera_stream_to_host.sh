raspivid -n -hf -vf -fps 25 -w 640 -h 480 -fl -t 0 -o - | nc 192.168.2.1 5001
