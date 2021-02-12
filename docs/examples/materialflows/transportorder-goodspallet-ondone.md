# TransportOrderGoodsPallet OnDone Example

In this example the Task will be executed like in TransportGoodsPallet and after the first Task is done the Task definied in the OnDone statement will be executed next.

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
    OnDone transportGoodsPallet2
End

Task transportGoodsPallet2
    Transport
    From loadPickupItem
    To unloadDropoffItem 
End
```