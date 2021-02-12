# TransportOrderGoodsPallet Forever Example

The TransportGoodsPallet example but it runs forever. The Task has itself as OnDone Task.

```text
Location pickupItem
    name = "Tag10"
    type = "pallet"
End

Location dropoffItem
    name = "Tag12"
    type = "pallet"
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
    OnDone transportGoodsPallet
End
```