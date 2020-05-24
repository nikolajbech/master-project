// From https://stackoverflow.com/questions/47291415/draggable-view-within-parent-boundaries
import React, { Component } from 'react'
import {
  StyleSheet,
  Animated,
  View,
  Text,
  Alert
} from 'react-native'
import { createResponder } from 'react-native-gesture-responder'
import Toast from 'react-native-simple-toast';

const SIZE = 160
const BALL_SIZE = 40

const styles = StyleSheet.create({
  container: {
    height: SIZE,
    width: SIZE,
    backgroundColor: '#ffffff20',
    margin: 5,
    borderRadius: BALL_SIZE / 2,
  },
  draggable: {
    height: BALL_SIZE,
    width: BALL_SIZE,
    backgroundColor: '#F4B95B30',
    borderWidth: 1,
    borderColor: '#F4B95B',
    borderRadius: BALL_SIZE / 2
  },
  text: {
    fontSize: 18,
    color: '#FFF9E1',
  }, 
})

export default class DragAround extends Component {
  constructor(props) {
    super(props)

    this.state = {
      x: new Animated.Value((SIZE - BALL_SIZE) / 2),
      y: new Animated.Value((SIZE - BALL_SIZE) / 2),
      mood: "",
      dragging: false
    }
    this.Responder = createResponder({
      onStartShouldSetResponder: () => true,
      onStartShouldSetResponderCapture: () => true,
      onMoveShouldSetResponder: () => true,
      onResponderGrant: (evt, gestureState) => {
        this.setState({dragging: true})
      },
      onResponderEnd: (evt, gestureState) => {
        this.setState({dragging: false})
        Alert.alert(
          'Would you like to save your mood',
          '',
          [
            {text: 'Yes', onPress: () => this.saveToDB()},
            {text: 'No', onPress: () => console.log('Cancel Pressed'), style: 'cancel'},
          ],
          { cancelable: false }
        )
      },
      onMoveShouldSetResponderCapture: () => true,
      onResponderMove: (evt, gestureState) => {
        this.pan(gestureState)
      },
      onPanResponderTerminationRequest: () => true
    })
  }

  pan = (gestureState) => {
    const { x, y } = this.state
    const area = SIZE - (BALL_SIZE / 2)
    const moodX = Math.min(7, Math.max(0, Math.round(8 / (area / x._value))))
    const moodY = Math.min(7, Math.max(0, Math.round(8 / (area / y._value))))
    const selectedMood = moodMeter[moodY][moodX]
    this.setState({mood: selectedMood})

    const maxX = SIZE - BALL_SIZE
    const minX = 0
    const maxY = SIZE - BALL_SIZE
    const minY = 0

    const xDiff = gestureState.moveX - gestureState.previousMoveX
    const yDiff = gestureState.moveY - gestureState.previousMoveY
    let newX = x._value + xDiff
    let newY = y._value + yDiff

    if (newX < minX) {
      newX = minX
    } else if (newX > maxX) {
      newX = maxX
    }

    if (newY < minY) {
      newY = minY
    } else if (newY > maxY) {
      newY = maxY
    }

    x.setValue(newX)
    y.setValue(newY)
  }

  saveToDB() {
    console.log("Saving to DB")
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "text/plain");

    var what = {uid: this.props.username, x: Math.round(this.state.x._value), y: Math.round(this.state.y._value), mood: this.state.mood}
    console.log(what.toString())
    var raw = what.toString();
    var requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
    };
    

    fetch(`*serverURL*moodlogger`, {
      method: 'POST',
      headers: {
        Accept: 'text/plain',
        'Content-Type': 'text/plain',
      },
      body: JSON.stringify(what),
    })
    .then(response => response.text())
    .then(result => {
      console.log(result)
      this.setState({
        x: new Animated.Value((SIZE - BALL_SIZE) / 2),
        y: new Animated.Value((SIZE - BALL_SIZE) / 2),
        mood: "",
        dragging: false
      })
      Toast.show('Your mood was saved');
    })
    .catch(error => {
      console.log('error', error)
      Toast.show('An error occured - try again');
    });
  }


  render() {
    const {
      x, y,
    } = this.state
    const imageStyle = { left: x, top: y }

    return (
      <View
        style={styles.container}
      >
        <View style={{height: SIZE / 2, width: SIZE / 2, position: 'absolute', backgroundColor: '#FFFFFF20', borderTopLeftRadius: BALL_SIZE / 2}}/>
        <View style={{left: SIZE / 2, top: SIZE / 2, height: SIZE / 2, width: SIZE / 2, position: 'absolute', backgroundColor: '#FFFFFF20', borderBottomRightRadius: BALL_SIZE / 2}}/>
        <Animated.View
          {...this.Responder}
          resizeMode={'contain'}
          style={[styles.draggable, imageStyle]}
        />
        {this.state.dragging && <View style={{position: 'absolute', top: -65, left: -40, right: -40, height: 40, backgroundColor: '#333333ee', zIndex: 100, borderRadius: 20, justifyContent: 'center', alignItems: 'center'}}>
        <Text style={styles.text}>{this.state.mood}</Text>
        </View>}
    </View>

    )
  }
}

const moodMeter = [
  ["Enraged", "Furious", "Frustrated", "Shocked", "Surprised", "Upbeat", "Motivated", "Ecstastic"],
  ["Livid", "Frightened", "Nervous", "Restless", "Hyper", "Cheerful", "Inspired", "Elated"],
  ["Fuming", "Apprehensive", "Worried", "Annoyed", "Energized", "Lively", "Optimistic", "Thrilled"],
  ["Repulsed", "Troubled", "Uneasy", "Peeved", "Pleasant", "Joyful", "Proud", "Blissful"],
  ["Disgusted", "Disappointed", "Glum", "Ashamed", "Blessed", "At Ease", "Content", "Fulfilled"],
  ["Mortified", "Alienated", "Mopey", "Apathetic", "Humble", "Secure", "Chill", "Grateful"],
  ["Embarrassed", "Excluded", "Timid", "Drained", "Calm", "Satisfied", "Relaxed", "Carefree"],
  ["Alone", "Down", "Bored", "Tired", "Relieved", "Restful", "Tranquil", "Serene"]
]