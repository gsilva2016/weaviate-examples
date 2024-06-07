#!/bin/bash
NITERS=1

if [ ! -z "$1" ]
then
	NITERS=$1
fi

if [ "$INIT_DATABASE" == "1" ] || [ "$INIT_DATABASE" == "true" ]
then
	docker run -it --net host -e INIT_DATABASE="1" img2vec_client
	exit 0
fi

for (( i=1; i<=$NITERS; i++))
do
	docker run -it --net host img2vec_client
done
