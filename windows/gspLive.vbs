Set objArgs = WScript.Arguments

If objArgs.Count = 2 Then 
	createobject("wscript.shell").run "gspLive.bat "+WScript.Arguments(0)+" "+WScript.Arguments(1), 0
ElseIf objArgs.Count = 1 Then 
    createobject("wscript.shell").run "gspLive.bat " + WScript.Arguments(0), 0
Else 
    createobject("wscript.shell").run "gspLive.bat", 0
End If
