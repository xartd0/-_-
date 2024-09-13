# Задача 1
Вывести отсортированный в алфавитном порядке список имен пользователей в файле passwd (вам понадобится grep).
##Код
```bash
grep '.*' /etc/passwd | cut -d: -f1 | sort
```

```bash
xartd0@xartd0-Strix-GL504GW-GL504GW:~$ grep '.*' /etc/passwd | cut -d: -f1 | sort
_apt
avahi
backup
bin
colord
cups-browsed
cups-pk-helper
daemon
dhcpcd
dnsmasq
ftp
fwupd-refresh
games
gdm
geoclue
gnome-initial-setup
gnome-remote-desktop
hplip
irc
kernoops
list
lp
mail
man
messagebus
news
nm-openvpn
nobody
polkitd
proxy
root
rtkit
saned
speech-dispatcher
sshd
sssd
sync
sys
syslog
systemd-network
systemd-oom
systemd-resolve
systemd-timesync
tcpdump
tss
usbmux
uucp
uuidd
whoopsie
www-data
xartd0
```

# Задача 2
Вывести данные /etc/protocols в отформатированном и отсортированном порядке для 5 наибольших портов, как показано в примере ниже:
##Код
```bash
awk '{print $2, $1}' /etc/protocols | sort -nr | head -n 5
```
```bash
awk '{print $2, $1}' /etc/protocols | sort -nr | head -n 5
262 mptcp
143 ethernet
142 rohc
141 wesp
140 shim6
```

# Задача 3
Написать программу banner средствами bash для вывода текстов, как в следующем примере (размер баннера должен меняться!):
##Код
```bash
#!/bin/bash

text=$*
length=${#text}

for i in $(seq 1 $((length + 2))); do
    line+="-"
done

echo "+${line}+"
echo "| ${text} |"
echo "+${line}+"
```
```bash
xartd0@xartd0-Strix-GL504GW-GL504GW:~/confmirea$ ./banner.sh "xartd0"
+--------+
| xartd0 |
+--------+
```

# Задача 4
Написать программу для вывода всех идентификаторов (по правилам C/C++ или Java) в файле (без повторений).
##Код
```bash
#!/bin/bash

file="$1"

id=$(grep -o -E '\b[a-zA-Z]*\b' "$file" | sort -u)

```
```bash
xartd0@xartd0-Strix-GL504GW-GL504GW:~/confmirea$ grep -oE '\b[a-zA-Z_][a-zA-Z0-9_]*\b' hello.c | grep -vE '\b(int|void|return|if|else|for|while|include|stdio)\b' | sort | uniq
h
hello
main
n
printf
world
```

# Задача 5
Написать программу для регистрации пользовательской команды (правильные права доступа и копирование в /usr/local/bin).
##Код
```bash
#!/bin/bash

file=$1

chmod 755 "./$file"

sudo cp "$file" /usr/local/bin/
```

Например, пусть программа называется reg:
```bash
xartd0@xartd0-Strix-GL504GW-GL504GW:~/confmirea$ ./reg.sh banner.sh
xartd0@xartd0-Strix-GL504GW-GL504GW:~/confmirea$ ls /usr/local/bin
banner.sh  ngrok
```



