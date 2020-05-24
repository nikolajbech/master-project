const express = require('express')
const cors = require('cors')
const bodyParser = require('body-parser')
const path = require('path');
const app = express()
const port = 80
const { getHistory } = require('./LampLogAnalyzer.js')
const { sendPushNotification } = require('./PushNotifications.js')
const schedule = require('node-schedule');

const MongoClient = require('mongodb').MongoClient;
const url = 'mongodb://localhost:27017';
const dbName = 'myproject';
const client = new MongoClient(url);
client.connect()

let dataHist = []
// Fill hist with zeros:
for(let i = 0; i < 100; i++) dataHist.push(0)

let counter = 0

let wakeupDate = new Date(2020, 1, 1, 7, 0, 0, 0)
let bedtimeDate = new Date(2020, 1, 1, 21, 00, 0, 0)

// Light warnings:
let lastWarningSendAt;
let lampStatus;

let data = {
  "initialData": 1
}

let parsedData = {
  "initialData": 2
}

let currentMode = 0

let sensor1 = {}
let sensor2 = {}
let sensor3 = {}
let sensor4 = {}

// Reminder stuff:
const minutesAfterWakeup = 20
let morningReminderTime = new Date(wakeupDate.getTime() + 1000 * 60 * minutesAfterWakeup)
let morningReminder = setReminder(morningReminderTime, "It's morning, how are you feeling right now?")

const minutesBeforeBedtime = 120
let eveningReminderTime = new Date(bedtimeDate.getTime() - 1000 * 60 * minutesBeforeBedtime)
let eveningReminder = setReminder(eveningReminderTime, "It's evening - how are you feeling?")

// Server stuff:
app.use(express.static(path.join(__dirname, 'build')));

app.use(cors())
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())

app.get('/ping', function (req, res) {
  return res.send('pong');
});

app.get('/getdata', (req, res) => res.send(data))

app.get('/getWakeup', (req, res) => res.send(wakeupDate))
app.get('/getBedtime', (req, res) => res.send(bedtimeDate))

app.post('/setWakeup', async function (req, res) {
  var body = ''
  req.on('data', async function (data) {body += data})
  req.on('end', async function () {
    wakeupDate = new Date(body)
    console.log("Set wake up to", new Date(body), dateToMinutes(wakeupDate), dateToMinutes(bedtimeDate))

    const newTime = new Date(wakeupDate.getTime() + 1000 * 60 * 20)
    // morningReminder.cancel()
    morningReminder = setReminder(newTime, "It's morning, how are you feeling right now?")

    res.send(JSON.stringify(body))
  })
})

app.post('/setBedtime', async function (req, res) {
  var body = ''
  req.on('data', async function (data) {body += data})
  req.on('end', async function () {
    bedtimeDate = new Date(body)
    console.log("Set bedtime to", new Date(body), dateToMinutes(wakeupDate), dateToMinutes(bedtimeDate))

    const newTime = new Date(bedtimeDate.getTime() - 1000 * 60 * 120)
    // eveningReminder.cancel()
    eveningReminder = setReminder(newTime, "It's evening - how are you feeling?")

    res.send(JSON.stringify(body))
  })
})

app.post('/moodlogger', async function (req, res) {
  var body = ''
  req.on('data', async function (data) {body += data})
  req.on('end', async function () {
    console.log("body", body)
    const mood = JSON.parse(body)
    console.log("Mood:", mood)
    const model = {data: mood, time: new Date().getTime()}
    await insertDB('moodloggertest', model)
    res.send(JSON.stringify(body))
  })
})

app.post('/pntoken', async function (req, res) {
  var body = ''
  req.on('data', async function (data) {body += data})
  req.on('end', async function () {
    console.log("token", body)
    const token = JSON.parse(body)
    const model = {data: token, time: new Date().getTime()}
    await insertDB('pntokentest', model)
    res.send(JSON.stringify(body))
  })
})

app.post('/updateLightHubSensor', async function (req, res) {
  var body = ''
  req.on('data', async function (data) {body += data})
  req.on('end', async function () {
    var correctJson = body.replace(/(['"])?([a-z0-9A-Z_]+)(['"])?:/g, '"$2": ');
    const model = {data: JSON.parse(correctJson), time: new Date().getTime()}
    await insertDB('windowLight2test', model)
    //console.log("LightHubSensor", new Date(), body)
    res.send(body)
  })
})

app.get('/getdatahist', async (req, res) => res.send(await getHistory()))

app.listen(port, () => console.log(`Sensor server listening on port ${port}!`))

app.post('/data', async function (req, res) {
  var body = ''
  req.on('data', async function (data) {
      body += data
  })
  req.on('end', async function () {
    var correctJson = body.replace(/(['"])?([a-z0-9A-Z_]+)(['"])?:/g, '"$2": ');
    const model = {data: JSON.parse(correctJson), time: new Date().getTime()}
    
    data = JSON.parse(correctJson)
    //console.log(data)

    if(counter % 10 === 0){ // If we have received 10 recordings, we sent the data to mongoDB
      
      dataHist.push(model)
      dataHist.shift()

      await insertDB('lightlog2test', model)

    }
    counter++
    //console.log(JSON.stringify(getNewLight()))
    res.send(JSON.stringify(getNewLight()))
  })
})

app.post('/lampData', async function (req, res) {
  var body = ''
  req.on('data', function (data) {
      body += data
  })
  req.on('end', async function () {
    //console.log(body)

    try{
    let sortedBody = body.replace(/\\/g, '');
    sortedBody = sortedBody.replace(/([0-9a-f]{1,2}[\.:-]){8}([0-9a-f]{1,2})/g, '');
    sortedBody = "{" + sortedBody.replace(/([0-9a-f]{1,2}[\..-]){2}([0-9a-f]{1,2})/g, '') + "}"
    const removeLampNumber = sortedBody.substring(1,sortedBody.lastIndexOf(","))

    const rawLampData = JSON.parse(removeLampNumber)
    const numberPattern = /\d+/g;
    const lampNumber = body.substring(body.lastIndexOf(","), body.length).match( numberPattern ).join('')

    const isOn = rawLampData.state.on && rawLampData.state.reachable
    const allData = rawLampData.state
    const oneLampInfo = {lampNumber, isOn, allData }

    lampStatus = oneLampInfo

    const model = {lamp: lampNumber, data: oneLampInfo, sensorData: data, time: new Date().getTime()}
    await insertDB('lamplog2test', model)

    }catch(e){
      console.log("Wrong lamp log format")
    }

    res.send("received!")

    checkForLightWarnings()
  })
})

app.post('/users/push-token', function (req, res) {
  shouldIChange = true
  var body = ''
  req.on('data', function (data) {
      body += data
  })
  req.on('end', function () {
    console.log(body)
    res.send("Yes sir!")
  })
})

app.post('/changemode', function (req, res) {
  shouldIChange = true
  var body = ''
  req.on('data', function (data) {
      body += data
  })
  req.on('end', async function () {
    currentMode = parseInt(body)

    const model = {currentMode: currentMode, time: new Date().getTime()}
    await insertDB('changeMode', model)

    res.send(currentMode.toString())
  })
})

app.post('/ichangedlight', (req, res) => {
  shouldIChange = false
  var body = ''
  req.on('data', function (data) {
      body += data
  })
  req.on('end', function () {
    res.send(body)
  })
})

app.get('/whatlight', (req, res) => res.send(getNewLight()))

let wakeUp = 420
let bedtime = 1350
let shouldIChange = false

let changable_ct = 0
let changable_bri = 0
let changable_x = 0
let changable_y = 0

function dateToMinutes (date) {
  return date.getHours() * 60 + date.getMinutes()
}

function getNewLight () {
  const date = new Date()
  const time = (date.getHours() * 60) + date.getMinutes() + 60// Plus 60 because of time difference
  const lux = parsedData.lux * 1.41 || 0 // Gain factor because of dome
  const suggestedKelvin = timeToLight(time, dateToMinutes(wakeupDate), dateToMinutes(bedtimeDate), lux)
  const http = "http://*ip*/api/*token*/groups/1/action"
  
  //const temp_changable_ct = Math.round(kelvinToHueCT(suggestedKelvin.ct))
  const temp_changable_bri = Math.round(luxToBri(suggestedKelvin.lux))
  const temp_changable_x = suggestedKelvin.xy
  const temp_changable_y = getY(suggestedKelvin.xy)

  //console.log(temp_changable_ct, changable_ct)
  //console.log(changable_bri, temp_changable_bri)

  if(temp_changable_x != changable_x && changable_bri != temp_changable_bri && currentMode === 0){
    changable_bri = temp_changable_bri
    changable_x = temp_changable_x
    changable_y = temp_changable_y
    shouldIChange = true
    console.log("CT and BRI are not the same -> change light!!")
  }

  const body = [
    {
      xy: [changable_x, changable_y],
      bri: temp_changable_bri,
      transitiontime: 100,
      on: temp_changable_bri > 0
    },
    {
      ct: kelvinToHueCT(4000),  // Read
      bri: 255
    },
    {
      ct: kelvinToHueCT(6000), // Productivity
      bri: 255,
    },
    {
      xy: [0.58, getY(0.58)], // Chill  y = 0.3876
      bri: 120
    },
    {                       // Pause
    }
  ]
  return({shouldIChange, http, body: body[currentMode], currentMode})
}

function kelvinToHueCT(kelvin) {
  return scale(kelvin, 2000, 6500, 500, 153)
}

function luxToBri(kelvin) {
  return scale(kelvin, 0, 200, 0, 254)
}

function scale (num, in_min, in_max, out_min, out_max) {
  return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

// Minutes into the day convet to color kelvin and lux for ideal light:
function timeToLight (time, wakeUp, bedtime, currentLux) {
  // 07.00 would be 420
  
  // Morning
  const SUNRISE_DURATION = 30 // 30 min
  const START_SUNRISE_AT = wakeUp - SUNRISE_DURATION
  const PRIMO_SUNRISE_KELVIN = 2000
  const ULTIMO_SUNRISE_KELVIN = 5000
  const PRIMO_SUNRISE_LUX = 0
  const ULTIMO_SUNRISE_LUX = 200
  
  // Evening:
  const SUNSET_DURATION = 180 
  const START_SUNSET_AT = bedtime - SUNSET_DURATION
  const PRIMO_XY = 0.48
  const ULIMO_XY = 0.63
  const PRIMO_SUNSET_LUX = 200
  const ULTIMO_SUNSET_LUX = 0

  if (time > START_SUNRISE_AT && wakeUp >= time) { // Morning zone
    const mintuesIntoMorning = time - START_SUNRISE_AT
    const morningProgress = mintuesIntoMorning / SUNRISE_DURATION
    const morningXY = PRIMO_XY * morningProgress + ULIMO_XY * (1 - morningProgress)
    const morningLux = ULTIMO_SUNRISE_LUX * morningProgress + PRIMO_SUNRISE_LUX * (1 - morningProgress)
    //console.log("It's morning:", time)
    return({xy: morningXY, lux: morningLux})
  } else if (time > wakeUp && START_SUNSET_AT >= time){ // Day zone
    //console.log("It's day:", time)
    if (currentLux < 200){
      return({xy: PRIMO_XY, lux: 200})
    }else{
      return({xy: PRIMO_XY, lux: 0})
    }
  } else if (time > START_SUNSET_AT && bedtime >= time){ // Evening zone
    const mintuesIntoEvening = time - START_SUNSET_AT
    const eveningProgress = mintuesIntoEvening / SUNSET_DURATION
    const eveningXY = ULIMO_XY * eveningProgress + PRIMO_XY * (1 - eveningProgress)
    const eveningLux = ULTIMO_SUNSET_LUX * eveningProgress + PRIMO_SUNSET_LUX * (1 - eveningProgress) 
    //console.log("It's evening:", time)
    return({xy: eveningXY, lux: eveningLux})
  } else { // Night zone
    return({xy: ULIMO_XY, lux: 0})
  }
}

function getY(x) {
  return (-2.46 * Math.pow(x,2) + 2.44 * x - 0.2)
}

// Data stuff:
function splitData(dateToSplit){
  const rawData = dateToSplit.split(",").map(val => parseInt(val))
  let lux, v, b, g, y, o, r, temp, hum, move, _r, _g, _b, _c

  if(rawData.length === 14) [lux, v, b, g, y, o, r, temp, hum, move, _r, _g, _b, _c] = rawData

  const timestamp = new Date()
  const temperature = parseFloat(temp / 100).toFixed(2)
  const humidity = parseFloat(hum / 100).toFixed(2)
  const rawColor = [v, b, g, y, o, r]
  const topVal = Math.max( ...rawColor )
  const color = rawColor.map(val => (val / topVal))
  const _rawColor = [r, g, v]
  const _topVal = Math.max( ..._rawColor )
  const _color = _rawColor.map(val => (val / _topVal))

  return({timestamp, lux, color, temperature, humidity})
}

const options = [
  {
    title: 'Circadian',
    activeColor: '#E8B273aa',
    colorProfile: [0.4, 0.2, 0.5, 0.7, 1, 0.7],
    suggestedLux: 80
  },
  {
    title: 'Relax',
    activeColor: '#DB752A88',
    colorProfile: [0.05, 0.08, 0.12, 0.2, 0.4, 1],
    suggestedLux: 20
  },
  {
    title: 'Productive',
    activeColor: '#CDD7D9aa',
    colorProfile: [0.7, 0.4, 0.9, 1, 0.8, 0.5],
    suggestedLux: 170
  },
  {
    title: 'Read',
    activeColor: '#F7DC95aa',
    colorProfile: [0.27, 0.3, 0.6, 0.7, 1, 0.7],
    suggestedLux: 150
  },
]

const insertDB = (table,model) => {
  return new Promise(function(resolve,reject){
    if (client.isConnected()) {
        client.db(dbName).collection(table).insertOne(model).then(function(res){
          resolve(res);
          console.log("Success DB write:", model)
        }).catch(function(err){
          reject(err);
        });
    }else{
      reject("Not Connected!");
    }
  });
}

// ======== Scheduler: ========
function setReminder (time, message) {
  console.log(`Planning push notification for ${time.getHours()}:${time.getMinutes()}`)
  return schedule.scheduleJob({hour: time.getHours(), minute: time.getMinutes()}, function(){
    console.log("Sending morning push notification")
    sendPushNotification(message)
  });
}

// ========= Light warnings =============

function checkForLightWarnings () {
  checkForActiveBulbsAfterBedtime()
  checkForBlueLight()
}

// If the bulbs are set at high brightness with a cold color temperature 2 hour before bedtime
function checkForActiveBulbsAfterBedtime () {
  const now = new Date()
  const blueLight = data.sensor && data.sensor.b
  const timeSinceLastUpdate = new Date(now - lastWarningSendAt).getMinutes()
  const minutesToBedtime = new Date(bedtimeDate.getTime() - now).getMinutes()
  if(blueLight > 50 && minutesToBedtime < 120 && timeSinceLastUpdate > 20){
    sendWarning("You're receiving a lot of blue light. Try to dim your lights.")
  }
}

// If a high amount of blue light is detected 2 hours before bedtime (blue sensor > 50)
function checkForBlueLight () {
  const now = new Date()
  const lightBrigthness = lampStatus && lampStatus.isOn && lampStatus.allData.bri
  const timeSinceLastUpdate = new Date(now - lastWarningSendAt).getMinutes()
  const minutesToBedtime = new Date(bedtimeDate.getTime() - now).getMinutes()
  if(lightBrigthness > 200 && minutesToBedtime < 120 && timeSinceLastUpdate > 20){
    sendWarning("Try dimming your lights before sleeping")
  }
}

async function sendWarning (message) {
  const model = {warning: message, time: new Date().getTime()}
  await insertDB('lightWarnings', model)
  sendPushNotification(message)
  lastWarningSendAt = new Date()
}

/*
{
      "lampNumber": "1610690560",
      "isOn": false,
      "allData": {
        "on": true,
        "bri": 254,
        "hue": 40584,
        "sat": 78,
        "effect": "none",
        "xy": [
          0.3122,
          0.3364
        ],
        "ct": 153,
        "alert": "none",
        "colormode": "xy",
        "mode": "homeautomation",
        "reachable": false
      }
*/