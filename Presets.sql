-- Step 1: Drop the table if it already exists
IF OBJECT_ID('dbo.Presets', 'U') IS NOT NULL
    DROP TABLE dbo.Presets;
GO

-- Step 2: Create the new Presets table
CREATE TABLE dbo.Presets (
    Preset_ID INT IDENTITY(1,1) PRIMARY KEY,
    Strategy NVARCHAR(50),
    Stock NVARCHAR(10),
    Initial_Investment INT,
    Monthly_Investment INT,
    Start_Year INT
);
GO

-- Step 3: Insert the given data
INSERT INTO dbo.Presets (Strategy, Stock, Initial_Investment, Monthly_Investment, Start_Year)
VALUES 
    ('buythedip', '^GSPC', 1000, 200, 10), 
    ('losing', '^IXIC', 5000, 300, 5),    
    ('first', 'GC=F', 10000, 500, 20);
GO

-- Step 4: Verify the data
SELECT * FROM dbo.Presets;
GO
