Location pickupItem
    name = "ws1_pickup"
    type = "misc"
end

Location dropoffItem
    name = "ws2_dropoff"
    type = "misc"
end

Event finishedWorkAtWorkstation1
    name = "virtualSensorTransportFromWs1ToWs2"
    type = "Boolean"
end

Event agvLoadedAtWorkstation1
    name = "realSensorAgvLoadedWs1"
    type = "Boolean"
end

Event agvUnloadedAtWorkstation2
    name = "realsensorAgvUnloadedWs2"
    type = "Boolean"
end


TransportOrderStep loadAtWorkstation1
    Location pickupItem  # Only one Location can be defined!
    FinishedBy agvLoadedAtWorkstation1 == True 
end

TransportOrderStep unloadWorkstation2
    Location dropoffItem
    FinishedBy agvUnloadedAtWorkstation2 == True
end

task SupplyTaskFromWorkstation1ToWorkstation2
    # Transport Order now needs TransportOrderSteps instead of regular instances
    TriggeredBy finishedWorkAtWorkstation1 == True
    Transport
    from loadAtWorkstation1
    to unloadWorkstation2 
end