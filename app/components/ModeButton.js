import React from 'react';
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity
} from 'react-native';

const buttonSize = 62

export default Card = ({...props}) => {

  return (
    <TouchableOpacity
    onPress={props.onClick}
    style={[
      styles.container, {
      backgroundColor: props.isActive ? props.activeColor + '60' : '#ffffff20'
    }]}>
      <Text style={{
        fontSize: props.fontSize,
        color: props.isActive ? props.activeColor : '#FFF9E1',
        fontFamily: 'FontAwesome5Pro-Regular'}}>{props.icon}</Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    width: buttonSize,
    height: buttonSize,
    borderRadius: buttonSize / 2,
    margin: 8,
    alignItems: 'center',
    justifyContent: 'center'
  }
});
