-- Create custom database
CREATE DATABASE lead_app_db;

-- Connect to the custom database to create schema
\c lead_app_db;

-- Create custom schema
CREATE SCHEMA lead_app_schema AUTHORIZATION lead_app_admin;

-- Grant privileges to custom user
GRANT ALL PRIVILEGES ON SCHEMA lead_app_schema TO lead_app_admin;
