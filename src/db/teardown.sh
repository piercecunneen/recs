#!/bin/bash

function drop_db(){
  # drop postgresql database
  dropdb $1
}

while [ "$1" != "" ]; do
    drop_db $1;
    shift;
done