if not turtle then
  error("Script must run on turtle",2)
end

local t = turtle
local w = peripheral.wrap("left")
local port = 99
local cLength = 8
local cNum = 4
w.open(port)

print("Loaded Turtle")
t.select(16)
t.suckDown()
t.refuel()
t.select(1)
print("Fuel Level: " ..t.getFuelLevel())

print("Waiting for Command")
local event, modemSide, senderChannel, replyChannel, numMessage, senderDistance = os.pullEvent("modem_message")

numMessage = tonumber(numMessage)

tblMessage = {}

for a=1,numMessage,1 do
  local event, modemSide, senderChannel, replyChannel, message, senderDistance = os.pullEvent("modem_message")
  tblMessage[a] = message
end
  
w.transmit(replyChannel, senderChannel, 1)

--toggle piston door
function toggle()
  redstone.setOutput("front", true)
  sleep(1)
  redstone.setOutput("front", false)
end

--plant new crop
function plant(type)
holding = {}

for i=1,16,1 do
  local data = t.getItemDetail(i)
  
  if data then
    holding[i] = data.name
  end
end
  
  if type == "minecraft:wheat" then
    for i=1,16,1 do
      if holding[i] == "minecraft:wheat_seeds" then
        t.select(i)
      end
    end
   elseif type == "minecraft:potatoes" then
     for i=1,16,1 do
       if holding[i] == "minecraft:potatoes" then
         t.select(i)
       end
     end
   elseif type == "minecraft:carrots" then
     for i=1,16,1 do
       if holding[i] == "minecraft:carrots" then
         t.select(i)
        end
     end
   end
    
    t.placeDown()
    t.select(1)
end

--move the Column
function moveColumn(length,type)                                                            
  for i=2,length,1 do
    t.forward()
    t.digDown()
    plant(type)
  end                                                            
end

--move the field
function field(num,type)  
  local fNum = num / 2
  
  for i=1,fNum,1 do
    moveColumn(cLength,type)   
    t.turnRight()
    t.forward()
    t.turnRight()
    t.digDown()
    plant(type)
    moveColumn(cLength,type)
    t.turnLeft()
    t.forward()
    t.turnLeft()
    t.digDown()
    plant(type)
  end
end                                                                                                                                                                                                                  
                                                                                                                                                                                                                                                                                                                                                                                       
if tblMessage[1] == "farm" then
  print("Running Program")
  
  if t.getFuelLevel()>0 then
    print("Working")
    toggle()   
    
    --move out of hole
    for i=0,3,1 do
      t.up()
    end
    
    --move forward to chest
    t.forward()
    t.forward()
    
    --ensure inventory is empty
    for i=1, 15, 1 do
      t.select(i)
      t.dropDown()
    end
    
    t.select(1)
    
    --move to bottom left
    t.up()
    t.forward()
    t.turnLeft()
    t.forward()
    t.turnRight()
    
    --detect type of crop
    local pSuccess, pData = t.inspectDown()
    
    t.digDown()
    plant(pData.name)
                    
    --do field
    field(cNum,pData.name)
   
    --return to chest
    t.turnRight()
    t.back()
    t.turnRight()
    t.turnRight()
    t.forward()
    t.forward()
    t.turnRight()
    t.back()
    t.down()
    
    --clean inventory
    for i=1,16,1 do
      t.select(i)
      t.dropDown()
    end
    
    t.select(1) 
    
    t.back()
    t.back()
    
    for i=0,3,1 do
      t.down()
    end
    toggle()
   else
     print("Out of Fuel")    
   end
end
w.close(port)
sleep(1)
os.reboot()
