Location pickupItem
    name = "ws2_pickup"
    type = "misc"
end

Location dropoffItem
    name = "ws3_dropoff"
    type = "misc"
end

Event finishedWorkAtWorkstation2
    name = "virtualSensorTransportFromWs2ToWs3"
    type = "Boolean"
end

Event agvLoadedAtWorkstation2
    name = "realSensorAgvLoadedWs2"
    type = "Boolean"
end

Event agvUnloadedAtWorkstation3
    name = "realSensorAgvUnloadedWs3"
    type = "Boolean"
end


TransportOrderStep loadAtWorkstation2
    Location pickupItem  # Only one Location can be defined!
    FinishedBy agvLoadedAtWorkstation2 == True 
end

TransportOrderStep unloadWorkstation3
    Location dropoffItem
    FinishedBy agvUnloadedAtWorkstation3 == True
end

task SupplyTaskFromWorkstation2toWorkstation3
    # Transport Order now needs TransportOrderSteps instead of regular instances
    TriggeredBy finishedWorkAtWorkstation2 == True
    Transport
    from loadAtWorkstation2
    to unloadWorkstation3 
end