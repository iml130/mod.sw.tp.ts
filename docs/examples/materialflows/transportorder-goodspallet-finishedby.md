# TransportOrderGoodsPallet FinishedBy Example

A simple Task with a FinishedBy condition. The Task will be executed like the TransportGoodsPallet example but it will be only marked as finished when the FinishedBy condition is satisfied.

```text
Location pickupItem
    name = "Tag10"
    type = "pallet"
End

Location dropoffItem
    name = "Tag12"
    type = "pallet"
End

Event buttonPressed
    name = "AUniqueNameforAButton"
    type = "Boolean"
End

Event agvLoadedAtPickupItem
    name = "realSensorAgvLoadedWs1"
    type = "Boolean"
End

Event agvLoadedAtDropoffItem
    name = "realSensorAgvUnloadedWs2"
    type = "Boolean"
End

TransportOrderStep loadPickupItem
    Location pickupItem
    FinishedBy agvLoadedAtPickupItem == True 
End

TransportOrderStep unloadDropoffItem
    Location dropoffItem
    FinishedBy agvLoadedAtDropoffItem == True
End

Task transportGoodsPallet
    Transport
    From loadPickupItem
    To unloadDropoffItem
    FinishedBy buttonPressed == True  
End
```