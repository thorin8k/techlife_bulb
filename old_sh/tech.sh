#!/bin/bash


command=/bin/echo
topic="dev_sub_$1"

echo $topic

# cp /config/custom_components/Techlife/*.so* /usr/lib

if [ "$2" = "on" ]; then
	$command -en "\xfa\x23\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x23\xfb" | ./custom_components/Techlife/mosquitto_pub -t $topic -s -h 192.168.1.146 -u mosquito -P mosquito

elif [ "$2" = "off" ]; then
	$command -en "\xfa\x24\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x24\xfb" | ./custom_components/Techlife/mosquitto_pub -t $topic -s -h 192.168.1.146 -u mosquito -P mosquito

elif [ "$2" = "dim" ]; then
    $command -en "\xfa\x23\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x23\xfb" | ./custom_components/Techlife/mosquitto_pub -t $topic -s -h 192.168.1.146 -u mosquito -P mosquito
    d=$(expr $3 \* 100)
    prefix='28'
    oneToSix='000000000000'
    sevenToTen=$(printf %08X "$d" | grep -o .. | tac | tr "\n" "," | sed "s/,//g")
    elevenToThirteen='0000f0'
    oneToThirteen=$(echo $oneToSix$sevenToTen$elevenToThirteen)
    oneToThirteenMod=$(echo $oneToThirteen | sed 's/../0x&^/g' | sed 's/.$//')
    xor=$(python3 -c "print(hex($oneToThirteenMod)[2:].lower())")
    suffix='29'
    k=$(echo $prefix$oneToSix$sevenToTen$elevenToThirteen$xor$suffix | sed 's/../\\x&/g' | tr -d "\n")
    $command -en $k | ./custom_components/Techlife/mosquitto_pub -t $topic -s -h 192.168.1.146 -u mosquito -P mosquito

fi

