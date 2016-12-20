#!/bin/bash

function create_db(){
  # create postgresql database
  createdb $1
}

while [ "$1" != "" ]; do
    create_db $1;
    shift;
done