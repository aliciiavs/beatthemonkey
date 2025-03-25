-- Step 1: Drop the table if it exists
IF OBJECT_ID('dbo.Preset_Results', 'U') IS NOT NULL
    DROP TABLE dbo.Preset_Results;
GO

-- Step 2: Create the Preset_Results table
CREATE TABLE dbo.Preset_Results (
    Result_ID INT IDENTITY(1,1) PRIMARY KEY,
    Date DATE NOT NULL,
    Preset_ID INT NOT NULL,
    Total_Invested FLOAT NOT NULL,
    Total_Earned FLOAT NOT NULL,
    FOREIGN KEY (Preset_ID) REFERENCES dbo.Presets(Preset_ID) ON DELETE CASCADE
);
GO
