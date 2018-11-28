local port = 100
local w = peripheral.wrap("left")
w.open(port)

turtle.select(13)
turtle.suckDown(turtle.getItemSpace())
   
turtle.select(16)
turtle.refuel()
turtle.select(1)
print("Current Fuel Level: " ..turtle.getFuelLevel())
print("Port: " ..port)
    
local event, modemSide, senderChannel, replyChannel, numMessage, senderDistance = os.pullEvent("modem_message")

print("Number: " ..numMessage)

numMessage = tonumber(numMessage)

tblMessage = {}

for a=1, numMessage,1 do
  local event, modemSide, senderChannel, replyChannel, message, senderDistance = os.pullEvent("modem_message")
  print("Message: " ..message)
  print("a: " ..a)
  tblMessage[a] = message
end
      
if turtle.getFuelLevel()>0 then
  print("Fuel level: OK")
  if tblMessage[1] == "run" then
    print("Working")
    w.transmit(replyChannel,senderChannel, 1)  
 
    local sucess, data = turtle.inspect()   
    
    local wait = true
    while wait do      
      if sucess then
        if data.name == "Botania:livingwood" or data.name == "Botania:livingrock" then
            turtle.dig()
            turtle.forward()
            
            turtle.dig()
            turtle.forward()
            
            turtle.dig()
            turtle.forward()
            
            turtle.turnRight()
            turtle.dig()
            turtle.forward()
            
            turtle.dig()
            turtle.forward()
            
            turtle.turnRight()
            turtle.dig()
            turtle.forward()
            
            turtle.turnLeft()
            turtle.dig()
            turtle.forward()
            
            turtle.turnLeft()
            turtle.dig()
            turtle.forward()
            
            turtle.turnRight()
            turtle.dig()
            turtle.forward()
            
            turtle.dig()
            turtle.forward()
            
            turtle.turnRight()
            turtle.dig()
            turtle.forward()
            
            turtle.dig()
            turtle.forward()
            
            turtle.turnRight()
            turtle.dig()
            turtle.forward()
            
            turtle.dig()
            turtle.forward()
            
            turtle.dig()
            turtle.forward()
            
            turtle.dig()
            turtle.forward()
            
            turtle.dig()
            turtle.forward()
            
            turtle.turnLeft()
            turtle.back()
            
            turtle.select(13)
            
            turtle.place()
            turtle.back()
            
            turtle.place()
            turtle.turnRight()
            turtle.back()
            
            turtle.place()
            turtle.back()
            
            turtle.place()
            turtle.turnRight()
            turtle.back()
            turtle.place()
            
            turtle.back()
            turtle.place()
            
            turtle.turnLeft()
            turtle.back()
            turtle.turnLeft()
            turtle.back()
            turtle.back()
            
            turtle.place()
            turtle.turnRight()
            turtle.back()
            
            turtle.place()
            turtle.back()
            turtle.place()
            turtle.turnRight()
            turtle.back()
            
            turtle.place()
            turtle.back()
            
            turtle.place()
            turtle.turnRight()
            turtle.back()
            
            turtle.place()
            turtle.back()
            
            turtle.place()
            turtle.back()
            
            turtle.place()
            turtle.back()
            
            turtle.place()
            turtle.turnLeft()
            turtle.back()
            turtle.place()
            
            turtle.select(1)
            turtle.dropDown()
            
            turtle.turnRight()
            turtle.back()
            turtle.turnLeft()
          wait = false
        else
          print("Not Livingwood")
          print("Block" ..data.name)
          print("Waiting for Livingwood")
          sleep(1)
        end
      else
        turtle.forward()
        sleep(1)
      end
    end
  end
  
else
  print("Please enter fuel into slot 16 (Bottom Right)")
  w.transmit(replyChannel,senderChannel, -1)  
end

w.close(port)
print("Done")
os.reboot()
