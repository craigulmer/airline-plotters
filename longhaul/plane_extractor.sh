#!/bin/sh

SRC_DIR=${1:-""}
ID_FILE=${2:-"surveillance_planes.txt"}
DST_DIR=${3:-"results"}

cat <<EOF
Plane puller: a script for extracting specific flights from data dumps

EOF

read -e -p "Input data directory: " -i "$SRC_DIR"  SRC_DIR
read -e -p "Input plane ID file:  " -i "$ID_FILE"  ID_FILE
read -e -p "Output directory:     " -i "$DST_DIR"  DST_DIR

if [ ! -e "$SRC_DIR" ]; then
    echo "Source dir $SRC_DIR doesn't exist?"
    exit
fi
if [ ! -e "$ID_FILE" ]; then
    echo "ID file '$ID_FILE' doesn't exist? exiting"
    exit
fi
if [ ! -e "$DST_DIR" ]; then
    echo "$DST_DIR doesn't exist, creating"
    mkdir $DST_DIR
fi

#Reset all output files
while read line; do
    ID=$line
    if [ -e "$DST_DIR/$ID.txt" ]; then
	rm "$DST_DIR/$ID.txt"
    fi
done < $ID_FILE

#Run through all input files
files="${SRC_DIR}/*.txt"
for i in $files; do

    echo "Working on file $i"
    while read line; do
        ID=$line
	echo "  Doing plane $ID"
        grep $ID $i | sed -e 's/.*LINESTRING/LINESTRING/' >>$DST_DIR/$ID.txt
    done < $ID_FILE


done
exit


while read line; do
    ID=$line
    echo "Working on $ID"
    if [ -e "$DST_DIR/$ID.txt" ]; then
        rm "$DST_DIR/$ID.txt"
    fi
    files="${SRC_DIR}/*.txt"
    #for i in `grep -i $ID $SRC_DIR/*.txt | sed  -e 's/:.*$/ /'`; do
    for i in $files; do
	echo looking at $i
	grep $ID $i | sed -e 's/.*LINESTRING/LINESTRING/'
        #grep $ID $SRC_DIR/$i | sed -e 's/.*LINESTRING/LINESTRING/' >>$DST_DIR/$ID.txt 
    done    
done < $ID_FILE


#ID=ADC362
#for i in `grep -i $ID *.txt | sed  -e 's/:.*$/ /'`; do
#    grep $ID ../$i | sed -e 's/.*LINESTRING/LINESTRING/'
#done
