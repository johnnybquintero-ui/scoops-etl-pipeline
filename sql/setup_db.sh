#!/bin/bash

dropdb --if-exists scoops_sales
createdb scoops_sales
psql -d scoops_sales -f sql/schema.sql