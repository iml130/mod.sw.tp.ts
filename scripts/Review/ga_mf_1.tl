Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
end

Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
end

Event triggerGetNewMaterial
    name = "virtualSensorNewMaterialToWs1"
    type = "Boolean"
end

Event agvLoadedAtStorage1
    name = "realSensorAgvLoadedS1"
    type = "Boolean"
end

Event agvUnloadedAtWorkstation1
    name = "realSensorAgvUnloadedWs1"
    type = "Boolean"
end


TransportOrderStep loadStorage
    Location pickupItem  # Only one Location can be defined!
    FinishedBy agvLoadedAtStorage1 == True 
end

TransportOrderStep unloadWorkstation1
    Location dropoffItem
    FinishedBy agvUnloadedAtWorkstation1 == True
end

task SupplyTaskFromStorage1ToWorkstation1
    # Transport Order now needs TransportOrderSteps instead of regular instances
    TriggeredBy triggetGerNewMaterial == True
    Transport
    from loadStorage
    to unloadWorkstation1 
end