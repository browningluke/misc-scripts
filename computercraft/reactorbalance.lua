reactor = peripheral.wrap("BigReactors-Reactor_2")
m = peripheral.wrap("monitor_3")
MAXENERGY = 10000000

if not reactor then
    print("No reactor found, check reactor name.")
end

if not m then
    print("No monitor found, check monitor name.")
end

m.setBackgroundColor(colors.black)
m.clear()
 
function balanceReactor()
    -- body
    currentEnergy = reactor.getEnergyStored()
    percent = (currentEnergy / MAXENERGY) * 100
    reactor.setAllControlRodLevels(percent)
    sleep(0.1)
end

function draw_hLine(mon, x, y, length, thickness, color)
    -- body
    if length < 0 then
        length = 0
    end
    if thickness < 0 then
        thickness = 0
    end

    for i=0, thickness-1, 1 do
        mon.setBackgroundColor(color)
        mon.setCursorPos(x, y+i)
        mon.write(string.rep(" ", length))
    end
end

function draw_vLine(mon, x, y, length, thickness, color)
    -- body
    if length < 0 then
        length = 0
    end
    if thickness < 0 then
        thickness = 0
    end

    for i=0, length-1, 1 do
        mon.setBackgroundColor(color)
        mon.setCursorPos(x, y+i)
        mon.write(string.rep(" ", thickness))
    end

end

function progress_bar(mon, x, y, direction, length, thickness, val, maxVal, bar_color, bg_color)
    if direction == "h" then
        draw_hLine(mon, x, y, length, thickness, bg_color)
        local barSize = math.floor((val/maxVal) * length)
        draw_hLine(mon, x, y, barSize, thickness, bar_color)
    
    elseif direction == "v" then
        draw_vLine(mon, x, y, length, thickness, bg_color) --draw background line
        local barSize = math.floor((val/maxVal) * length)
        draw_vLine(mon, x, y, barSize, thickness, bar_color)
    end
end

function drawMonitor()
    -- body
    m.clear()
    m.setCursorPos(1,1)
 
    local a = tostring(reactor.getActive())
    m.write("Active: " ..a)
 
    m.setCursorPos(24,15)
    if reactor.getActive() then
        m.setBackgroundColor(colors.green)
        m.write("[Enable]")
        m.setBackgroundColor(colors.black)
        m.write(" ")
        m.setBackgroundColor(colors.lightGray)
        m.write("Disable")
    else
        m.setBackgroundColor(colors.lightGray)
        m.write("Enable")
        m.setBackgroundColor(colors.black)
        m.write(" ")
        m.setBackgroundColor(colors.green)
        m.write(" [Disable]")
    end
    m.setBackgroundColor(colors.black)

    m.setCursorPos(1,3)
    m.write("Fuel Amount: " ..math.floor(reactor.getFuelAmount()) .."mb")
    m.setCursorPos(1,4)
    m.write("Waste Amount: " ..math.floor(reactor.getWasteAmount()) .."mb")
   
    m.setCursorPos(1,6)
    m.write("Energy Produced: " ..math.floor(reactor.getEnergyProducedLastTick()) .." RF/t")
    m.setCursorPos(1,7)
    m.write("Energy Capacity: " ..math.floor(percent) .."%")
   
    m.setCursorPos(1,9)
    m.write("Fuel Consumed: " ..reactor.getFuelConsumedLastTick().." mb")
    m.setCursorPos(1,10)
    m.write("Fuel Reactivity: " ..math.floor(reactor.getFuelReactivity()) .."%")
 

    draw_hLine(m, 1, 14, 39, 1, colors.white)
    m.setBackgroundColor(colors.black)

    progress_bar(m, 5, 16, "v", 9, 7, math.floor(currentEnergy), MAXENERGY, colors.red, colors.white)
    m.setBackgroundColor(colors.black)

    sleep(0.1)
end
 
function touch()
    -- body
    while true do
        event, side, xPos, yPos = os.pullEvent("monitor_touch")
        print("Touched: "..tostring(xPos) .." "..tostring(yPos))
        if yPos == 15 then
            if reactor.getActive() then
                if xPos >= 32 or xPos <= 39 then
                    reactor.setActive(false)
                end
            else
                if xPos >= 24 or xPos <= 29 then
                    reactor.setActive(true)
                end
            end
        end
    end
end
 
function update()
    while true do
     
      isConnected = reactor.getConnected()
     
      if isConnected == true then
        --run if connected
        if reactor.getActive() then
          --balance reactor control rods
          balanceReactor()
        end
        --draw stats to monitor
        drawMonitor()
      else
        --run if not connected
        print("Not Connected")
        m.setCursorPos(1,1)
        m.write("NOT CONNECTED")
        break
        end
    end
end
parallel.waitForAny(update, touch)
