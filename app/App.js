import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  SafeAreaView,
  ScrollView,
  View,
  Text,
  StatusBar,
  Image,
  TouchableOpacity
} from 'react-native';
import ModeButton from './components/ModeButton'
import MoodMeter from './components/MoodMeter'
import ContentTextData from './components/ContentTextData'
import ColorVisualizer from './components/ColorVisualizer'
import AdjustTime from './components/AdjustTime';
import PushNotificationIOS from "@react-native-community/push-notification-ios";
import AsyncStorage from '@react-native-community/async-storage';
import DialogInput from 'react-native-dialog-input';

// npx react-native start    
// npx react-native run-ios --simulator="iPhone SE"

const production = true
const server = production ? "*serverURL*" : "http://192.168.1.172/"

const App = () => {
  const [data, setData] = useState({
    b: 1389,
    c: 3252,
    colorTemp: 5497,
    g: 1381,
    lux: 734,
    r: 1319,
    sensor: 1})
  const [activeMode, setModeActive] = useState(0)
  const [wakeUpTime, setWakeUpTime] = useState()
  const [bedTime, setBedTime] = useState()
  const [username, setUsername] = useState()
  const [pnToken, setPnToken] = useState()
  const [dialogVisible, setDialogVisible] = useState(false)
  let interval = null

  useEffect(() => {
    console.log(username)
    
    PushNotificationIOS.addEventListener('register', (token) => {
      setPnToken(token)
      initilizeUsername()
      console.log(token)
    })
    
    PushNotificationIOS.requestPermissions();
    getAndSetFromServer('getWakeup', (x) => setWakeUpTime(x), (val) => new Date(val))
    getAndSetFromServer('getBedtime', (x) => setBedTime(x), (val) => new Date(val))

    interval = setInterval(async function(){
      const url = server + 'getdata'
      await fetch(url)
      .then(function(response){
        return response.json();
      })
      .then(function(obj){
        //console.log(obj)
        setData(obj)
      })
    }, 1000);

  }, [])

  useEffect(() => {
  },[dialogVisible])

  useEffect( () => () => clearInterval(interval), [] );

  const getAndSetFromServer = async (where, set, func) => {
    const histUrl = server + where
    await fetch(histUrl)
    .then(function(response){
      return response.json();
    })
    .then(function(obj){
      const lambda = func(obj)
      set(lambda)
      console.log("lambda", lambda)
    })
  }

  const setActiveMode = (num) => {
    changeMode(num)
  }

  const changeMode = (newMode) => {
    console.log("Changing mode to", newMode)
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "text/plain");
    var raw = newMode.toString();
    var requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
      redirect: 'follow'
    };
    fetch(server + 'changemode', requestOptions)
      .then(response => response.text())
      .then(result => {
        console.log(result)
        setModeActive(parseInt(result))
      })
      .catch(error => console.log('error', error));
  }

  const savePNtoken = (token, name) => {
    console.log("Saving token", token)
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "text/plain");
    var raw = `{"username": "${name}", "token": "${token}"}`
    console.log("raw", raw.toString())
    var requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
      redirect: 'follow'
    };
    fetch(server + 'pntoken', requestOptions)
      .then(response => response.text())
      .then(result => {
        console.log(result)
        setModeActive(parseInt(result))
      })
      .catch(error => console.log('error', error));
  }

  initilizeUsername = async () => {
    try {
      const value = await AsyncStorage.getItem(`@username`)
      if(value !== null) {
        setUsername(value)
        savePNtoken(pnToken, value)
      } else {
        setDialogVisible(true)
      }
    } catch(e) {
      // error reading value
    }
  }

  saveUsername = async (username) => {
    try {
      await AsyncStorage.setItem(`@username`, username)
      savePNtoken(pnToken, username)
      setUsername(username)
      setDialogVisible(false)
    } catch (e) {
      // saving error
    }
  }

  return (
    <ScrollView scrollEnabled={false} style={styles.container}>
      <Image style={styles.bg} source={require('./assets/images/LHBG.png')}/>
      <StatusBar barStyle="dark-content" />
      <SafeAreaView style={{flex: 1}}>

        <View style={{height: 5}}/>
        
        <View style={styles.card}>
          <View style={{height: 10}}/>
          <View style={{flexDirection: 'row', justifyContent: 'center', alignItems: 'center'}}>
            <ContentTextData title={'Lux'} value={data.lux}/>
            <ContentTextData title={'Color temp.'} value={data.colorTemp + 'K'}/>
          </View>
          <ColorVisualizer color={[data.r, data.g, data.b]}/>
        </View>
        
        <View style={{height: 20}}/>

        <View style={styles.card}>
          <View style={{height: 20}}/>
          <View style={{flexDirection: 'row', justifyContent: 'center', alignItems: 'center'}}>
            {wakeUpTime && <AdjustTime header={"Select wake up time"} date={wakeUpTime} where={'setWakeup'} sunrise={true} isActive={activeMode == 0 || true}/>} 
            <ModeButton onClick={() => setActiveMode(0)} activeColor={'#F4B95B'} idx={0} isActive={activeMode == 0} fontSize={20} icon={''}/>
            {bedTime && <AdjustTime header={"Select bedtime"} date={bedTime} where={'setBedtime'} isActive={activeMode == 0 || true}/>}
          </View>
          
          <View style={{flexDirection: 'row', justifyContent: 'center', alignItems: 'center'}}>
            <ModeButton onClick={() => setActiveMode(1)} activeColor={'#FFF081'} idx={1} isActive={activeMode == 1} fontSize={20} icon={''}/>
            <ModeButton onClick={() => setActiveMode(2)} activeColor={'#BEE5FD'} idx={2} isActive={activeMode == 2} fontSize={20} icon={''}/>
            <ModeButton onClick={() => setActiveMode(3)} activeColor={'#F79533'} idx={3} isActive={activeMode == 3} fontSize={20} icon={''}/>
            <ModeButton onClick={() => setActiveMode(4)} activeColor={'#E1C0FD'} idx={4} isActive={activeMode == 4} fontSize={20} icon={''}/>
          </View>
          <View style={{height: 20}}/>
        </View>

        <View style={{height: 20}}/>

        <View style={styles.card}>
          <MoodMeter username={username}/>
        </View>
      </SafeAreaView>
      <DialogInput isDialogVisible={dialogVisible}
            title={"Please enter your username"}
            submitInput={ (name) => {saveUsername(name)} }
            closeDialog={ () => {setDialogVisible(false)}}>
      </DialogInput>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#333'
  },
  card: {
    flex: 1,
    backgroundColor: '#53535370',
    justifyContent: 'center',
    alignItems: 'center'
  },
  icon: {
    fontSize: 20,
    color: '#FFF9E1',
    fontFamily: 'FontAwesome5Pro-Regular'
  },
  sunriseSunsetText: {
    color: '#FFF9E1',
    fontSize: 20,
    marginHorizontal: 20
  },
  bg: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    resizeMode: 'contain'
  }
});

export default App;
