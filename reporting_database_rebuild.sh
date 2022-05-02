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
pg_dump --column-inserts "host=$PRODUCTION_LEDGER_HOST port=5432 dbname=$PRODUCTION_LEDGER_DATABASE user=$PRODUCTION_LEDGER_USERNAME password=$PRODUCTION_LEDGER_PASSWORD sslmode=require" -t 'accounts_emailuser' -t 'basket_basket' -t 'basket_line' -t 'order_order' -t 'order_line' -t 'address_country' -t 'payments_bpaytransaction' -t 'payments_bpointtransaction' -t 'payments_cashtransaction'  > /dbdumps/ledger_core_prod.sql

echo "Dump Core Parkstay V1 Production Tables";
pg_dump --column-inserts "host=$PRODUCTION_LEDGER_HOST port=5432 dbname=$PRODUCTION_LEDGER_DATABASE user=$PRODUCTION_LEDGER_USERNAME password=$PRODUCTION_LEDGER_PASSWORD sslmode=require" -t 'parkstay_*'  > /dbdumps/parkstayv1_core_prod.sql

echo "Dump Core Parkstay V2 Production Tables";
pg_dump --column-inserts "host=$PRODUCTION_PARKSTAYV2_HOST port=5432 dbname=$PRODUCTION_PARKSTAYV2_DATABASE user=$PRODUCTION_PARKSTAYV2_USERNAME password=$PRODUCTION_PARKSTAYV2_PASSWORD sslmode=require" -t 'parkstay_*' > /dbdumps/parkstayv2_core_prod.sql



# DROP All TABLES IN DAILY DB
for I in $(psql "host=$TEMPORARY_LEDGER_HOST port=5432 dbname=$TEMPORARY_LEDGER_DATABASE user=$TEMPORARY_LEDGER_USERNAME password=$TEMPORARY_LEDGER_PASSWORD sslmode=require" -c "SELECT tablename FROM pg_tables where tablename not like 'pg\_%' and tablename not like 'sql\_%';" -t);
  do
  echo " drop table $I CASCADE; ";
  psql "host=$TEMPORARY_LEDGER_HOST port=5432 dbname=$TEMPORARY_LEDGER_DATABASE user=$TEMPORARY_LEDGER_USERNAME password=$TEMPORARY_LEDGER_PASSWORD sslmode=require" -c "drop table $I CASCADE;" -t
done

# IMPORT LEDGER PROD DATABASE INTO DAILY
echo "Importing Ledger Core prod into reporting database";
psql "host=$TEMPORARY_LEDGER_HOST port=5432 dbname=$TEMPORARY_LEDGER_DATABASE user=$TEMPORARY_LEDGER_USERNAME password=$TEMPORARY_LEDGER_PASSWORD sslmode=require" < /dbdumps/ledger_core_prod.sql

# Parkstay V1
echo "Importing Parkstay Core prod into reporting database";
psql "host=$TEMPORARY_LEDGER_HOST port=5432 dbname=$TEMPORARY_LEDGER_DATABASE user=$TEMPORARY_LEDGER_USERNAME password=$TEMPORARY_LEDGER_PASSWORD sslmode=require" < /dbdumps/parkstayv1_core_prod.sql

echo "Renaming parkstay v1 tables";
for I in $(psql "host=$TEMPORARY_LEDGER_HOST port=5432 dbname=$TEMPORARY_LEDGER_DATABASE user=$TEMPORARY_LEDGER_USERNAME password=$TEMPORARY_LEDGER_PASSWORD sslmode=require" -c "SELECT tablename FROM pg_tables where tablename like 'parkstay\_%';" -t);
  do
  #NEW_TABLE_NAME=${I}_v1
  NEW_TABLE_NAME=$(echo "$I" | sed "s/parkstay_/parkstayv1_/")
  echo "ALTER TABLE $I  RENAME TO $NEW_TABLE_NAME; ";
  psql "host=$TEMPORARY_LEDGER_HOST port=5432 dbname=$TEMPORARY_LEDGER_DATABASE user=$TEMPORARY_LEDGER_USERNAME password=$TEMPORARY_LEDGER_PASSWORD sslmode=require" -c "ALTER TABLE $I RENAME TO $NEW_TABLE_NAME;" -t
done

# drop all sequences
for I in $(psql "host=$TEMPORARY_LEDGER_HOST port=5432 dbname=$TEMPORARY_LEDGER_DATABASE user=$TEMPORARY_LEDGER_USERNAME password=$TEMPORARY_LEDGER_PASSWORD sslmode=require" -c "select relname from pg_class  where relkind = 'S' and relname like 'parkstay\_%' ;" -t);
  do
  echo "DROP SEQUENCE IF EXISTS $I CASCADE; ";
  psql "host=$TEMPORARY_LEDGER_HOST port=5432 dbname=$TEMPORARY_LEDGER_DATABASE user=$TEMPORARY_LEDGER_USERNAME password=$TEMPORARY_LEDGER_PASSWORD sslmode=require" -c "DROP SEQUENCE IF EXISTS $I CASCADE; " -t
done

# Parkstay V2
echo "Importing Parkstay Core prod into reporting database";
psql "host=$TEMPORARY_LEDGER_HOST port=5432 dbname=$TEMPORARY_LEDGER_DATABASE user=$TEMPORARY_LEDGER_USERNAME password=$TEMPORARY_LEDGER_PASSWORD sslmode=require" < /dbdumps/parkstayv2_core_prod.sql

echo "Renaming parkstay v2 tables";
for I in $(psql "host=$TEMPORARY_LEDGER_HOST port=5432 dbname=$TEMPORARY_LEDGER_DATABASE user=$TEMPORARY_LEDGER_USERNAME password=$TEMPORARY_LEDGER_PASSWORD sslmode=require" -c "SELECT tablename FROM pg_tables where tablename like 'parkstay\_%';" -t);
  do
  #NEW_TABLE_NAME=${I}_v2
  NEW_TABLE_NAME=$(echo "$I" | sed "s/parkstay_/parkstayv2_/")
  echo "ALTER TABLE $I  RENAME TO $NEW_TABLE_NAME; ";
  psql "host=$TEMPORARY_LEDGER_HOST port=5432 dbname=$TEMPORARY_LEDGER_DATABASE user=$TEMPORARY_LEDGER_USERNAME password=$TEMPORARY_LEDGER_PASSWORD sslmode=require" -c "ALTER TABLE $I RENAME TO $NEW_TABLE_NAME;" -t
done

# drop all sequences
for I in $(psql "host=$TEMPORARY_LEDGER_HOST port=5432 dbname=$TEMPORARY_LEDGER_DATABASE user=$TEMPORARY_LEDGER_USERNAME password=$TEMPORARY_LEDGER_PASSWORD sslmode=require" -c "select relname from pg_class  where relkind = 'S' and relname like 'parkstay\_%' ;" -t);
  do
  echo "DROP SEQUENCE IF EXISTS $I CASCADE; ";
  psql "host=$TEMPORARY_LEDGER_HOST port=5432 dbname=$TEMPORARY_LEDGER_DATABASE user=$TEMPORARY_LEDGER_USERNAME password=$TEMPORARY_LEDGER_PASSWORD sslmode=require" -c "DROP SEQUENCE IF EXISTS $I CASCADE; " -t
done

# GRANT SELECT to parkstay_ro account
for I in $(psql "host=$TEMPORARY_LEDGER_HOST port=5432 dbname=$TEMPORARY_LEDGER_DATABASE user=$TEMPORARY_LEDGER_USERNAME password=$TEMPORARY_LEDGER_PASSWORD sslmode=require" -c "SELECT tablename FROM pg_tables where tablename not like 'pg\_%' and tablename not like 'sql\_%';" -t);
  do
  echo "GRANT SELECT ON $I TO parkstay_ro;";
  psql "host=$TEMPORARY_LEDGER_HOST port=5432 dbname=$TEMPORARY_LEDGER_DATABASE user=$TEMPORARY_LEDGER_USERNAME password=$TEMPORARY_LEDGER_PASSWORD sslmode=require" -c "GRANT SELECT ON $I TO parkstay_ro; " -t
done

rm /dbdumps/ledger_core_prod.sql
rm /dbdumps/parkstayv1_core_prod.sql
rm /dbdumps/parkstayv2_core_prod.sql

