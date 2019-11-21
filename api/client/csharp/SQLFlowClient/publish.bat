dotnet publish -c Release /p:PublishProfile=Properties\PublishProfiles\linux.pubxml
dotnet publish -c Release /p:PublishProfile=Properties\PublishProfiles\osx.pubxml
dotnet publish -c Release /p:PublishProfile=Properties\PublishProfiles\win.pubxml
if exist dist rd dist /S /Q
xcopy /s .\bin\Release\netcoreapp3.0\publish .\dist\
xcopy .\test.sql .\dist\win\
xcopy .\config.json .\dist\win\
xcopy .\test.sql .\dist\osx\
xcopy .\config.json .\dist\osx\
xcopy .\test.sql .\dist\linux\
xcopy .\config.json .\dist\linux\
