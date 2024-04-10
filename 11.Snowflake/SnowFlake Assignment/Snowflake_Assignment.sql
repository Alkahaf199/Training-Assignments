use role accountadmin;

-- Q1: Create roles as per the below-mentioned hierarchy. Accountadmin already exists in Snowflake
-- Creating admin role
create role Admin;
grant role admin to role accountadmin; 

-- Creating developer role
create role developer;
grant role developer to role admin;

-- Creating PII role
create role PII;
grant role PII to role accountadmin;


-- Q2: Create an M-sized warehouse using the accountadmin role, name -> assignment_wh and use it for all the queries
create or replace warehouse assignment_wh with 
	warehouse_size = 'MEDIUM'
	AUTO_SUSPEND = 60
	AUTO_RESUME = TRUE;

-- Grant integration privilege and database privilege to admin role
GRANT CREATE INTEGRATION ON ACCOUNT TO ROLE admin;
GRANT CREATE DATABASE ON ACCOUNT TO ROLE admin;

-- Grant warehouse privilege to developer and admin role
GRANT USAGE ON WAREHOUSE assignment_wh TO ROLE developer;
GRANT OPERATE on warehouse assignment_wh TO ROLE developer;

-- Grant warehouse privilege to PII role
GRANT USAGE ON WAREHOUSE assignment_wh TO ROLE PII;
GRANT operate on warehouse assignment_wh to role PII;


-- Q3: Switch to the admin role.
use role admin;
use warehouse assignment_wh;


-- Q4: Create a database assignment_db 
create database assignment_db;


-- Q5: Create a schema my_schema
CREATE OR REPLACE SCHEMA my_schema;
use schema my_schema;

-- Granting database access to various roles
grant usage on schema my_schema to role developer;
GRANT ALL PRIVILEGES on ALL TABLES IN SCHEMA my_schema TO ROLE developer; 

use role accountadmin;
grant usage on schema my_schema to role PII;
GRANT SELECT ON ALL TABLES IN SCHEMA my_schema TO ROLE PII;

use role admin;
use database assignment_db;


-- Q6: Create a table using any sample csv. You can get 1 by googling for sample csv’s. Preferably search for a sample employee dataset so that you have PII related columns else you can consider any column as PII.
CREATE OR REPLACE TABLE emp(
    EMPLOYEE_ID INT PRIMARY KEY,
    FIRST_NAME VARCHAR(50),
    LAST_NAME VARCHAR(50),
    EMAIL VARCHAR(100),
    PHONE_NUMBER VARCHAR(20),
    HIRE_DATE VARCHAR(20),
    JOB_ID VARCHAR(20),
    SALARY DECIMAL(10,2),
    COMMISSION_PCT VARCHAR(10),
    MANAGER_ID VARCHAR(10),
    DEPARTMENT_ID INT,
    elt_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    elt_by VARCHAR(50) DEFAULT 'Assignment',
    file_name STRING
    );


-- Q7: Also, create a variant version of this dataset 
CREATE OR REPLACE TABLE emp_variant (
    employee_data VARIANT
);


-- Q8: Load the file into an external and internal stage
CREATE OR REPLACE STAGE my_stage;
-- Execute the below command in snowSQL to stage the files from your local file system
-- put file:///Users/cellarzero/Downloads/employee_int.csv @my_stage;
-- put file:///Users/cellarzero/Downloads/employee_ext.csv @my_stage;

-- List all the files in staging area.
list @my_stage;


-- Q9: Load data into the tables using copy into statements.
-- a) In one table load from the internal stage. 
-- Creating file format for csv files.
CREATE OR REPLACE FILE FORMAT emp_csv_format
  TYPE=CSV,
    SKIP_HEADER=1,
    FIELD_DELIMITER=',',
    TRIM_SPACE=FALSE,
    FIELD_OPTIONALLY_ENCLOSED_BY=NONE,
    REPLACE_INVALID_CHARACTERS=TRUE,
    TIMESTAMP_FORMAT=AUTO,
    ERROR_ON_COLUMN_COUNT_MISMATCH = TRUE
    NULL_IF = ('-');

-- Copying the files into table from staging area.
copy into emp (EMPLOYEE_ID,
    FIRST_NAME,
    LAST_NAME,
    EMAIL ,
    PHONE_NUMBER ,
    HIRE_DATE ,
    JOB_ID ,
    SALARY ,
    COMMISSION_PCT ,
    MANAGER_ID ,
    DEPARTMENT_ID,
    elt_ts,
    file_name) from 
(SELECT T.$1, T.$2, T.$3, T.$4, T.$5, T.$6, T.$7, T.$8, T.$9, T.$10, T.$11, METADATA$START_SCAN_TIME, METADATA$FILENAME FROM @my_stage/employee_ext.csv.gz (file_format =>  emp_csv_format) AS T)
pattern = '.*employee_.*\\.csv\\.gz';


-- b)In One table from the external
-- Creating storage integration for external staging from S3 buckets.
create or replace storage integration s3_ext
type = external_stage
storage_provider = s3
enabled = true
storage_aws_role_arn = 'arn:aws:iam::176495710345:role/myrole'
storage_allowed_locations = ('s3://mysnowflakeassignment/');

-- Creating stages for files in S3 bucket.
create or replace stage my_stage
storage_integration = s3_ext
url = 's3://mysnowflakeassignment/employee_ext.csv'
file_format = emp_csv_format;

-- View the arn properties to set in AWS policies
desc integration s3_ext;

-- Creating a temporary table to store the data from the staging area.
CREATE OR REPLACE TEMPORARY TABLE temp_emp_data (
    EMPLOYEE_ID VARCHAR,
    FIRST_NAME VARCHAR,
    LAST_NAME VARCHAR,
    EMAIL VARCHAR,
    PHONE_NUMBER VARCHAR,
    HIRE_DATE VARCHAR,
    JOB_ID VARCHAR,
    SALARY VARCHAR,
    COMMISSION_PCT VARCHAR,
    MANAGER_ID VARCHAR,
    DEPARTMENT_ID VARCHAR
);
COPY INTO temp_emp_data
FROM @my_stage;

-- Copying the data into variant table via external staging.
INSERT INTO emp_variant (employee_data)
SELECT PARSE_JSON('{
    "EMPLOYEE_ID": "' || EMPLOYEE_ID || '", 
    "FIRST_NAME": "' || FIRST_NAME || '", 
    "LAST_NAME": "' || LAST_NAME || '", 
    "EMAIL": "' || EMAIL || '", 
    "PHONE_NUMBER": "' || PHONE_NUMBER || '", 
    "HIRE_DATE": "' || HIRE_DATE || '", 
    "JOB_ID": "' || JOB_ID || '", 
    "SALARY": "' || SALARY || '", 
    "COMMISSION_PCT": "' || COMMISSION_PCT || '", 
    "MANAGER_ID": "' || MANAGER_ID || '", 
    "DEPARTMENT_ID": "' || DEPARTMENT_ID || '"
    }') AS JSON_DATA
FROM temp_emp_data;


-- Q10: Upload any parquet file to the stage location and infer the schema of the file
-- Creating a file format for parquet file.
create or replace file format titanic_parquet_format
type = parquet;

-- Creating stage to add files from azure cloud storage.
create or replace stage my_stage
url = 'azure://mysnowflakestorage.blob.core.windows.net/mycontainer/Titanic.parquet'
credentials = (
azure_sas_token = 'sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-04-09T02:31:41Z&st=2024-04-08T18:31:41Z&spr=https&sig=L05lD%2BnoL%2FoP0ikygDuEKsweFXiUK058%2Fbr8M3r2vKE%3D')
file_format = titanic_parquet_format;

-- Infering schema of the staged parquet file.
SELECT *
  FROM TABLE(
    INFER_SCHEMA(
      LOCATION=>'@my_stage'
      , FILE_FORMAT=>'titanic_parquet_format'
      )
    );


-- Q11: Run a select query on the staged parquet file without loading it to a snowflake table
SELECT *
  FROM @my_stage(
      FILE_FORMAT=>'titanic_parquet_format'
    );


-- Q12: Add masking policy to the PII columns such that fields like email, phone number, etc. show as **masked** to a user with the developer role. If the role is PII the value of these columns should be visible

-- Creating masking policies for email and phone number column
CREATE OR REPLACE MASKING POLICY email_mask AS (val string) returns string ->
  CASE
    WHEN current_role() IN ('DEVELOPER') THEN '**MASKED**'
    ELSE VAL
  END;
CREATE OR REPLACE MASKING POLICY phone_mask AS (val string) returns string ->
  CASE
    WHEN current_role() IN ('DEVELOPER') THEN '**MASKED**'
    ELSE VAL
  END;

-- Applying the policies on respective columns
ALTER TABLE emp MODIFY COLUMN email SET MASKING POLICY email_mask;
ALTER TABLE emp MODIFY COLUMN phone_number SET MASKING POLICY phone_mask;

-- View the masked results by switching roles
use role developer;
select * from emp;

use role PII;
select * from emp;

show grants to role developer;
