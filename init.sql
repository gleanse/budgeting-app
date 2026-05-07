-- This script runs automatically on container initialization (docker-entrypoint-initdb.d)
-- Creates the test database for pytest - main database (budgeting_fastapi_db) is created by docker-compose via POSTGRES_DB
CREATE DATABASE budgeting_fastapi_db_test;