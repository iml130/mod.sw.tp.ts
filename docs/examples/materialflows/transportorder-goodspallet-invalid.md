# TransportOrderGoodsPallet Invalid Example

This File violates our grammar rules. If you try to start it, the schedular should not execute it and instead returns an error message containing more information.

In this specifiy example the Task keyword starts with a lower case character which is forbidden. The supervisor should print the error message and shoudl throw a Materialflow specification error.

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

task TransportGoodsPallet
    Transport
    From loadPickupItem
    To unloadDropoffItem 
End
```