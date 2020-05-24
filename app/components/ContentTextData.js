import * as React from 'react';
import { StyleSheet, View, Text } from 'react-native';

export default function ContentTextData({ ...props }) {
  return (
    <View style={styles.container}>
      <View style={styles.titleContainer}>
        <Text style={styles.title}>{props.title}</Text>
      </View>
      <View style={styles.valueContainer}>
        <Text style={styles.value}>{props.value}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1
  },
  title: {
    fontSize: 15,
    color: '#FFF9E1' + '88',
    //ontFamily: 'verdana'
  },
  titleContainer: {
    marginTop: 13,
    justifyContent: 'center',
    alignItems: 'center',
  },
  value: {
    fontSize: 25,
    color: '#FFF9E1',
    //fontFamily: 'spartan',
  },
  smallValue: {
    fontSize: 20,
    color: '#FFF9E1',
    //fontFamily: 'spartan'
  },
  valueContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center'
  }
})