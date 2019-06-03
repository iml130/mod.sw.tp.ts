import urllib

with open("current.txt") as f:
    content = f.readlines()
longString = ""

for line in content:
    longString += line.replace("\r", "")
 
print "qoute"
print urllib.quote_plus(longString)
print "unqoute"

aa = "template+Position%0A++++position%0A++++type%0Aend%0A%0Atemplate+Sensor%0A++++sensorId%0A++++type%0Aend%0A%0A%23%23%23%23%0A%0APosition+moldingPallet%0A++++type+%3D+%22pallet%22%0A++++position+%3D+%22moldingArea_palletPlace%22%0Aend%0A%0APosition+warehouse_pos1%0A++++type+%3D+%22pallet%22%0A++++position+%3D+%22warehouse_destination_pos%22%0Aend%0A%0ASensor+buttonPalletIsReady%0A++++sensorId+%3D+%22buttonPalletIsReady%22%0A++++type+%3D+%22Boolean%22%0Aend%0A%0Atask+Refill%0A++++Transport%0A++++from+warehouse_pos1%0A++++to+moldingPallet+%0Aend%0A%0A%23%23%23%23+%0Atask+Transport_moldingPallet%0A++++Transport%0A++++from+moldingPallet%0A++++to+warehouse_pos1%0A++++TriggeredBy%09buttonPalletIsReady.value+%3D%3D+True%0A++++OnDone+Refill%0Aend%0A"
print urllib.unquote_plus(aa)
# you may also want to remove whitespace characters like `\n` at the end of each line



# {
# 	"id": "TaskSpec1",
# 	"type": "TaskSpec",
# 	"TaskSpec": {
# 		"value": "template+Position%0A++++position%0A++++type%0Aend%0A%0Atemplate+Sensor%0A++++sensorId%0A++++type%0Aend%0A%0A%23%23%23%23%0A%0APosition+moldingPallet%0A++++type+%3D+%22pallet%22%0A++++position+%3D+%22moldingArea_palletPlace%22%0Aend%0A%0APosition+warehouse_pos1%0A++++type+%3D+%22pallet%22%0A++++position+%3D+%22warehouse_destination_pos%22%0Aend%0A%0ASensor+buttonPalletIsReady%0A++++sensorId+%3D+%22buttonMoldingArea%22%0A++++type+%3D+%22Boolean%22%0Aend%0A%0A%23%23%23%23+%0Atask+Transport_moldingPallet%0A++++Transport%0A++++from+moldingPallet%0A++++to+warehouse_pos1%0A++++TriggeredBy%09buttonPalletIsReady.value+%3D%3D+True%0Aend%0A",
# 		"type": "Text"
# 	}
# }
