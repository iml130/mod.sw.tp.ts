Location pickupItem
    name = "ws3_pickup"
    type = "SmallLoadCarrier"
end

Location dropoffItem
    name = "s2_dropoff"
    type = "SmallLoadCarrier"
end

Event finishedWorkAtWorkstation3
    name = "virtualSensorTransportFromWs1ToWs2"
    type = "Boolean"
end

Event agvLoadedAtWorkstation3
    name = "realsensorAgvLoadedWs3"
    type = "Boolean"
end

Event agvUnloadedAtStorage2
    name = "realsensorAgvUnloadedS2"
    type = "Boolean"
end


TransportOrderStep loadAtWorkstation3
    Location pickupItem  # Only one Location can be defined!
    FinishedBy agvLoadedAtWorkstation3 == True 
end

TransportOrderStep unloadStorage2
    Location dropoffItem
    FinishedBy agvUnloadedAtStorage2 == True
end

task SupplyTaskFromWorkstation3ToStorage2
    # Transport Order now needs TransportOrderSteps instead of regular instances
    TriggeredBy finishedWorkAtWorkstation3 == True
    Transport
    from loadAtWorkstation3
    to unloadStorage2 
end