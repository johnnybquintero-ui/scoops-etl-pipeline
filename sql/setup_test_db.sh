#!/bin/bash

set -e

dropdb --if-exists --force scoops_sales_test
createdb scoops_sales_test
psql -d scoops_sales_test -f sql/schema.sql