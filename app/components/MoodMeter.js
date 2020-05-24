import React, { useRef, useCallback } from 'react';
import {
  StyleSheet,
  View,
  Text,
  Animated
} from 'react-native';
import  {PanGestureHandler} from 'react-native-gesture-handler'
import DragAround from './DragAround'

const squareSize = 160

export default Card = ({...props}) => {
  const translationXRef = useRef(new Animated.Value(0));
  const translationYRef = useRef(new Animated.Value(0));

  const onGestureEvent = useCallback(
		Animated.event(
			[{
				nativeEvent: {
					translationX: translationXRef.current,
					translationY: translationYRef.current,
				},
			}],
			{ useNativeDriver: true },
		),
		[],
	);

  const Axis = () => {
    return(
      <View style={styles.axis}>
        <PanGestureHandler onGestureEvent={onGestureEvent}>
          <Animated.View
            style={{
              width: 60,
              height: 60,
              backgroundColor: 'blue',
              transform: [
                { translateX: translationXRef.current },
                { translateY: translationYRef.current },
              ],
            }}
          />
        </PanGestureHandler>
      </View>
    )
  }

  return (
    <View style={styles.container}>
      <View style={{height: 10}}/>
      <Text style={styles.text}>High energy</Text>
      <View style={{flexDirection: 'row', justifyContent: 'center', alignItems: 'center'}}>
        <Text style={styles.icon}></Text>
        <DragAround username={props.username}/>
        <Text style={styles.icon}></Text>
      </View>
      <Text style={styles.text}>Low energy</Text>
      <View style={{height: 10}}/>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center'
  },
  icon: {
    fontSize: 25,
    margin: 10,
    color: '#FFF9E1',
    fontFamily: 'FontAwesome5Pro-Regular'
  },
  text: {
    fontSize: 18,
    color: '#FFF9E1',
  },  
  axis: {
    width: squareSize,
    height: squareSize,
    backgroundColor: '#70707070',
    margin: 10,
    borderRadius: 10,
    overflow: 'hidden'
  },
  square: {
    width: squareSize / 2,
    height: squareSize / 2,
    backgroundColor: '#aaaaaa20'
  },
  circle: {
    width: 60,
    height: 60,
    backgroundColor: "#c00000",
    borderRadius: 100
  }
});
