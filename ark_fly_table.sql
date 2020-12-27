-- Create a new database called 'arkg'
-- Connect to the 'master' database to run this snippet
USE master
GO
-- Create the new database if it does not exist already
IF NOT EXISTS (
    SELECT name
        FROM sys.databases
        WHERE name = N'ark'
)
CREATE DATABASE ark
GO

IF NOT EXISTS (
    SELECT * FROM sys.tables WHERE name = N'ark.trading_history' AND type = 'U'
)
CREATE TABLE ark.trading_history (
    fund VARCHAR(255),
    date VARCHAR(255),
    ticker VARCHAR(255),
    cusip VARCHAR(255),
    company VARCHAR(255),
    primary key (fund, date, ticker)
)
GO
