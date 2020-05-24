// Sensor:
#include <Wire.h>
#include "Adafruit_TCS34725.h"
Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_700MS, TCS34725_GAIN_1X);

// WiFi:
#include <WiFi.h>
#include <HTTPClient.h>
const char* ssid = "";
const char* password =  "";

// Philips HUE:
#include <ArduinoJson.h>
boolean shouldUpdateLight = false;
String hueHttp = "";
String hueBody = "";
int counter = 0;
int availableLamps[3] = {1, 2, 3};
int lampCounter = 0;

// Server stuff:
String server = "*serverURL*";
 
void setup() {

  // Wifi:
  Serial.begin(115200);
  delay(4000);   
  WiFi.begin(ssid, password); 
  while (WiFi.status() != WL_CONNECTED) { //Check for the connection
    delay(500);
    Serial.println("Connecting..");
  }
  Serial.print("Connected to the WiFi network with IP: ");
  Serial.println(WiFi.localIP());

  // Sensor:
  if (tcs.begin()) {
    Serial.println("Found sensor");
  } else {
    Serial.println("No TCS34725 found ... check your connections");
    while (1);
  }
}
 
void loop() {

  //Sensor:
  String data;
  uint16_t r, g, b, c, colorTemp, lux;

  tcs.getRawData(&r, &g, &b, &c);
  colorTemp = tcs.calculateColorTemperature_dn40(r, g, b, c);
  lux = tcs.calculateLux(r, g, b);

  data = data + "{";
  data = data + "sensor: 1, ";
  data = data + "colorTemp: "; data = data + colorTemp; data = data + ", ";
  data = data + "lux: "; data = data + lux; data = data + ", ";
  data = data + "r: "; data = data + r; data = data + ", ";
  data = data + "g: "; data = data + g; data = data + ", ";
  data = data + "b: "; data = data + b; data = data + ", ";
  data = data + "c: "; data = data + c;
  data = data + "}";

  Serial.println(data);

  String sensorOutputAnswer = post(server + "/data/", data, "POST"); // Post sensor output


  // Get Philips HUE adjustments:
  DynamicJsonBuffer jsonBuffer;
  JsonObject& root = jsonBuffer.parseObject(sensorOutputAnswer);
  shouldUpdateLight = root[String("shouldIChange")];
  hueHttp = root[String("http")].as<String>();
  hueBody = root[String("body")].as<String>();
  Serial.println("shouldUpdateLight" + (String) shouldUpdateLight);
  Serial.println("hueHttp" + hueHttp);
  Serial.println("hueBody" + hueBody);
  
  String hueChange = "";
  if(shouldUpdateLight){
    String hueChange = post(hueHttp, hueBody, "PUT");
    if(hueChange.length() > 0){ // Change light
      String changeAnwser = post(server + "/ichangedlight/", "true", "POST");
      if(changeAnwser.length() > 0) shouldUpdateLight = false; // Set to false when light is adjusted
    }
  }
  
  if(counter % 4 == 0){
    String hueStatus = post("*ip*/api/*token*/lights/" + (String) availableLamps[lampCounter % 3], "", "GET");
    String lampUpdate = hueStatus + "," + (String) availableLamps[lampCounter % 12];
    lampCounter++;
    post(server + "/lampData/", lampUpdate, "POST");
  }
  counter++;

  delay(1000);
}

String post(String url, String body, String how){
  if(WiFi.status()== WL_CONNECTED){
    HTTPClient http;
    http.begin(url);
    http.addHeader("Content-Type", "text/plain");
    int httpResponseCode;
    if(how == "PUT"){
      httpResponseCode = http.PUT(body);
    } else if(how == "POST"){
      httpResponseCode = http.POST(body);
    } else if(how == "GET"){
      httpResponseCode = http.GET();
    }
    
    if(httpResponseCode>0){
      Serial.println(httpResponseCode);
      const String& payload = http.getString();
      Serial.println(payload);
      String input = payload;
      return input;
    }else{
      Serial.print("Error on sending request: ");
      Serial.println(httpResponseCode);
      return "";
    }
    http.end();
  }else{
    Serial.println("Error in WiFi connection"); 
    return "";  
  }
}