#!/bin/bash
srv_num=$1
int=1
while(( $int<=srv_num))
do
    mkdir "Svr_Video_"$int""
    let "int++"
done