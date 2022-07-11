#!/bin/bash

# Usage:
# ./massive.sh EntityAttribute

for i in {1..1000}
do
   orion_response=$(curl -sS --location --request PUT 'http://orion:1026/v2/entities/age01_Car/attrs/'$1'?type=Device' \
   --header 'Accept: application/json' \
   --header 'Fiware-Service: opcua_car' \
   --header 'Fiware-ServicePath: /demo' \
   --header 'Content-Type: application/json' \
   --data-raw "{\"value\": $i }")
done

