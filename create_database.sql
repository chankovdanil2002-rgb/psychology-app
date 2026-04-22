-- SQL script for creating the psychology_db database
-- Run this before Django migrations if database doesn't exist

CREATE DATABASE psychology_db
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'ru_RU.UTF-8'
    LC_CTYPE = 'ru_RU.UTF-8'
    TEMPLATE = template0
    CONNECTION LIMIT = -1;

-- Connect to the database
\c psychology_db;

-- The actual tables are created by Django migrations (python manage.py migrate)
-- This script only creates the database itself

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE psychology_db TO postgres;
