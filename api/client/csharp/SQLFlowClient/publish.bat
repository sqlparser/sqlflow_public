dotnet publish -c Release /p:PublishProfile=Properties\PublishProfiles\linux.pubxml
dotnet publish -c Release /p:PublishProfile=Properties\PublishProfiles\osx.pubxml
dotnet publish -c Release /p:PublishProfile=Properties\PublishProfiles\win.pubxml
if exist dist rd dist /S /Q
xcopy /s .\bin\Release\netcoreapp3.0\publish .\dist\