# TransportOrderGoodsPallet TriggeredBy Example

A simple Task with a TriggeredBy condition. The Task can only start if the button is pressed.

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
    TriggeredBy buttonPressed == True 
    Transport
    From loadPickupItem
    To unloadDropoffItem 
End
```