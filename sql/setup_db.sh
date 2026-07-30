#!/bin/bash

set -e

dropdb --if-exists --force scoops_sales
createdb scoops_sales
psql -d scoops_sales -f sql/schema.sql