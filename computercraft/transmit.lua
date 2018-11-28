local args = {...}

local w = peripheral.wrap("back")

local port = tonumber(args[1])
local message = args[2]
print("Port: " ..port)
print("Message: " ..message)

w.open(port)
print("Opening Port")
print(" ")

print("Transmitting")
sleep(0.5)

w.transmit(port, port, table.getn(args))

for i=2,table.getn(args),1 do

  w.transmit(port, port, args[i])

end

w.transmit(port,port,-999)

print("Transmit Done")

print(" ")
print("Waiting for Handshake")

local event, modemSide, senderChannel, replyChannel, message, distance = os.pullEvent("modem_message")

if message == 1 then
  print("Transmit Successfull")
end
  
print(" ")
w.close(port)
print("Closing Port")
