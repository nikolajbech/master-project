import React, { useEffect, useState } from 'react';
import { StyleSheet, View, Text, TouchableOpacity} from 'react-native';
import DateTimePickerModal from "react-native-modal-datetime-picker";
import Toast from 'react-native-simple-toast';

const production = true
const server = production ? "*serverURL*" : "http://192.168.1.172/"

export default function AdjustTime({ ...props }) {
  const [isDatePickerVisible, setDatePickerVisibility] = useState(false);
  const [date, setDate] = useState(new Date(props.date))

  const changeServer = (where, what) => {

    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "text/plain");
    
    var raw = what.toString();
    
    var requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
      redirect: 'follow'
    };
    
    fetch(server + where, requestOptions)
      .then(response => response.text())
      .then(result => {
        console.log(result)
        Toast.show('Your adjustments was saved');
      })
      .catch(error => {
        console.log('error', error)
        Toast.show('An error occured - try again');
      });
  }

  const showDatePicker = () => {
    setDatePickerVisibility(true);
  };

  const hideDatePicker = () => {
    setDatePickerVisibility(false);
  };

  const handleConfirm = date => {
    setDate(date)
    changeServer(props.where, date)
    hideDatePicker();
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity
        onPress={showDatePicker}
        style={{flexDirection: 'row', justifyContent: 'center', alignItems: 'center'}}
      > 
      {props.sunrise && <View style={{width: 20}}/>}
        {props.sunrise && <Text style={[{opacity: props.isActive ? 1 : 0.3}, styles.icon]}></Text>}
        <Text style={[{opacity: props.isActive ? 1 : 0.3}, styles.sunriseSunsetText]}>{prettyDate2(date)}</Text>
        {!props.sunrise && <Text style={[{opacity: props.isActive ? 1 : 0.3}, styles.icon]}></Text>}
      </TouchableOpacity>
      <DateTimePickerModal
        isDarkModeEnabled
        isVisible={isDatePickerVisible}
        headerTextIOS={props.header}
        date={date}
        mode="time"
        onConfirm={handleConfirm}
        onCancel={hideDatePicker}
      />
      {!props.sunrise && <View style={{width: 20}}/>}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  icon: {
    fontSize: 20,
    color: '#FFF9E1',
    fontFamily: 'FontAwesome5Pro-Regular'
  },
  sunriseSunsetText: {
    color: '#FFF9E1',
    fontSize: 18,
    marginHorizontal: 10
  },
})

function prettyDate2(date) {
  return date.toLocaleTimeString(navigator.language, {
    hour: '2-digit',
    minute:'2-digit'
  });
}