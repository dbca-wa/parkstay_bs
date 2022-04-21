#!/bin/bash
  
echo "Running database collection and merge into new database for reporting.";

if [ $TEMPORARY_LEDGER_DATABASE ==  'ledger_prod' ]; then
        echo "ERROR: ledger_prod can not be a TEMPORARY Database";
        exit;
fi

if [ $TEMPORARY_LEDGER_DATABASE ==  'parkstayv2_prod' ]; then
	echo "ERROR: parkstayv2_prod can not be a TEMPORARY Database";
	exit;
fi


echo "Dump Core Ledger Production Tables";
pg_dump "host=$PRODUCTION_LEDGER_HOST port=5432 dbname=$PRODUCTION_LEDGER_DATABASE user=$PRODUCTION_LEDGER_USERNAME password=$PRODUCTION_LEDGER_PASSWORD sslmode=require" -t 'accounts_emailuser' -t 'basket_basket' -t 'basket_line' -t 'order_order' -t 'order_line' -t 'address_country' -t 'payments_bpaytransaction' -t 'payments_bpointtransaction' -t 'payments_cashtransaction'  > /dbdumps/ledger_core_prod.sql

echo "Dump Core Parkstay V1 Production Tables";
pg_dump "host=$PRODUCTION_LEDGER_HOST port=5432 dbname=$PRODUCTION_LEDGER_DATABASE user=$PRODUCTION_LEDGER_USERNAME password=$PRODUCTION_LEDGER_PASSWORD sslmode=require" -t 'parkstay_*'  > /dbdumps/parkstayv1_core_prod.sql

echo "Dump Core Parkstay V2 Production Tables";
pg_dump "host=$PRODUCTION_PARKSTAYV2_HOST port=5432 dbname=$PRODUCTION_PARKSTAYV2_DATABASE user=$PRODUCTION_PARKSTAYV2_USERNAME password=$PRODUCTION_PARKSTAYV2_PASSWORD sslmode=require" -t 'parkstay_*'  > /dbdumps/parkstayv2_core_prod.sql



# DROP All TABLES IN DAILY DB
for I in $(psql "host=$TEMPORARY_LEDGER_HOST port=5432 dbname=$TEMPORARY_LEDGER_DATABASE user=$TEMPORARY_LEDGER_USERNAME password=$TEMPORARY_LEDGER_PASSWORD sslmode=require" -c "SELECT tablename FROM pg_tables" -t);
  do
  echo " drop table $I CASCADE; ";
  psql "host=$TEMPORARY_LEDGER_HOST port=5432 dbname=$TEMPORARY_LEDGER_DATABASE user=$TEMPORARY_LEDGER_USERNAME password=$TEMPORARY_LEDGER_PASSWORD sslmode=require" -c "drop table $I CASCADE;" -t
done

# IMPORT LEDGER PROD DATABASE INTO DAILY
echo "Importing Ledger Core prod into reporting database";
psql "host=$TEMPORARY_LEDGER_HOST port=5432 dbname=$TEMPORARY_LEDGER_DATABASE user=$TEMPORARY_LEDGER_USERNAME password=$TEMPORARY_LEDGER_PASSWORD sslmode=require" < /dbdumps/ledger_core_prod.sql

echo "Importing Parkstay Core prod into reporting database";
psql "host=$TEMPORARY_LEDGER_HOST port=5432 dbname=$TEMPORARY_LEDGER_DATABASE user=$TEMPORARY_LEDGER_USERNAME password=$TEMPORARY_LEDGER_PASSWORD sslmode=require" < /dbdumps/parkstayv1_core_prod.sql

echo "Renaming parkstay v1 tables";
for I in $(psql "host=$TEMPORARY_LEDGER_HOST port=5432 dbname=$TEMPORARY_LEDGER_DATABASE user=$TEMPORARY_LEDGER_USERNAME password=$TEMPORARY_LEDGER_PASSWORD sslmode=require" -c "SELECT tablename FROM pg_tables where tablename like 'parkstay_%';" -t);
  do
  $TABLE_SUFFIX='_v1';
  echo "ALTER TABLE $I  RENAME TO $I$TABLE_SUFFIX; ";
  psql "host=$TEMPORARY_LEDGER_HOST port=5432 dbname=$TEMPORARY_LEDGER_DATABASE user=$TEMPORARY_LEDGER_USERNAME password=$TEMPORARY_LEDGER_PASSWORD sslmode=require" -c "ALTER TABLE $I RENAME TO $I$TABLE_SUFFIX;" -t
done

# TODO Parkstay V2

rm /dbdumps/ledger_core_prod.sql
rm /dbdumps/parkstayv1_core_prod.sql
rm /dbdumps/parkstayv2_core_prod.sql
