local pastebinID = "1gKKi915"
local fname = "farm"
local backup = fname ..".bak"

print("Fetching " .. fname .. " program from pb. ID: " ..pastebinID)
if fs.exists(backup) then
  fs.delete(backup)
end

if fs.exists(fname) then
  fs.move(fname, backup)
end

ok = shell.run("pastebin", "get " .. pastebinID .. " " .. fname)
print("Download Result: " ..tostring(ok))

print("Running " ..fname .. " Program")
sleep(5)

term.clear(); term.setCursorPos(1,1)

if not fs.exists(fname) then
  print("Error: " .. fname .. " does not exist. Using old version.")
  fs.copy(backup, fname)
end

shell.run(fname)
