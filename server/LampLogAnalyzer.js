const getHistory = () => {
	return new Promise( async (resolve, reject) => {

    const MongoClient = require('mongodb').MongoClient;
    const assert = require('assert');
    const url = 'mongodb://localhost:27017';
    const dbName = 'myproject';
    const client = new MongoClient(url);
    await client.connect(function(err) {
        assert.equal(null, err);
        console.log("Connected successfully to server");
        const db = client.db(dbName);
        const collection = db.collection('lamplog2test');

        collection.find({}).toArray(function(err, docs) {
            assert.equal(err, null);
            console.log("Found the following records");
            console.log(docs)
            var fs = require('fs');
            fs.writeFileSync('./lamplog2test.json', JSON.stringify(docs, null, 2) , 'utf-8');
            client.close();
        })
    });

    const lines = []

    const data = require('./lamplog2test.json')
    let lamps = {}

    data.forEach(element => {
      const lampNum = element.lamp
      if (lamps[lampNum] == null) lamps[lampNum] = []
      const elemObj = lamps[lampNum]
      elemObj.push(element)
      lamps[lampNum] = elemObj
    })

    console.log(Object.keys(lamps))

    const timeObject = {}

    console.log(lamps["1"].length)
    for(let i = 0; i < lamps["1"].length - 10; i++){
      const time = lamps['1'][i].time
      const startTime = 1585417620
      const smallerTime = (Math.round(time / 1000) - startTime) + ""

      let stringToPrint = ""
      Object.keys(lamps).map(key => {
        //if(lamps[key][i]) stringToPrint = stringToPrint + ((lamps[key][i].data.allData.bri) * (lamps[key][i].data.isOn ? 1 : 0)) + ","
      })

      // Sensor data:

      let printSensorData = '0,0,0,0,0,0,0,0,0,0,0,0,0,0'
      if('sensorData' in lamps["1"][i]){ // We only use the sensor data from when lamp 4's state was recorded
        printSensorData = lamps["1"][i].sensorData.data
      }

      stringToPrint = stringToPrint + printSensorData
      
      timeObject[smallerTime] = stringToPrint
    }

    const timeKeys = Object.keys(timeObject)
    const timeInts = timeKeys.map(key => parseInt(key))

    let timePointer = 0
    const timeInterval = 150
    while(timePointer < timeKeys[timeKeys.length - 1]){ //timeKeys[timeKeys.length - 1]
      let lowestTimeInterval = 99999
      let lowestTimeIndex = -1

      for(let i = 0; i < timeInts.length; i++){
        //console.log(Math.abs(timeInts[i] - timePointer))
        if(Math.abs(timeInts[i] - timePointer) < lowestTimeInterval){
          lowestTimeInterval = Math.abs(timeInts[i] - timePointer)
          lowestTimeIndex = i
        }
      }

      if(lowestTimeInterval < 200){
        lines.push(timePointer + "," + timeObject[timeKeys[lowestTimeIndex]])
        console.log(timePointer + "," + timeObject[timeKeys[lowestTimeIndex]])
      } else {
        lines.push(timePointer + ",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
        console.log(timePointer + ",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0" )
      }

      timePointer += timeInterval
    }
    resolve(lines)
  })
}

exports.getHistory = getHistory;

// Data example:
/*const data = {
  "_id" : ObjectId("5e7c6c3a2da59a23d5aa2c1c"),
  "lamp" : "9",
  "data" : {
  "lampNumber" : "9",
  "isOn" : false,
  "allData" : {
    "on" : false, "bri" : 1, "hue" : 7388, "sat" : 158, "effect" : "none", "xy" : [ 0.4803, 0.4045 ], "ct" : 403, "alert" : "select", "colormode" : "xy", "mode" : "homeautomation", "reachable" : true }
  },
  "sensorData" : {
    "data" : "553, 800, 1023, 970, 1263, 1066, 1426, 2950, 2660, 0, 67, 68, 62, 188",
    "timestamp" : 1585212468767
  },
  "time" : 1585212474267
}*/