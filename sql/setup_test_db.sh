#!/bin/bash

dropdb --if-exists scoops_sales_test
createdb scoops_sales_test
psql -d scoops_sales_test -f sql/schema.sql