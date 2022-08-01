#!/bin/bash

# Usage:
# ./massive_ld.sh CarEntityAttribute (eg. Engine_Oxigen)

for i in {1..300}
do
   orion_response=$(curl -sS --location --request PATCH 'http://localhost:1026/ngsi-ld/v1/entities/urn:ngsi-ld:Device:age01_Car/attrs' \
   --header 'Accept: application/json' \
   --header 'Content-Type: application/json' \
   --data-raw "{ \"$1\": { \"type\": \"Property\", \"value\": $i } }")
done

