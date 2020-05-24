import * as React from 'react';
import { StyleSheet, View, Text } from 'react-native';
import Colors from '../constants/Colors';
import Layout from '../constants/Layout';
import { Svg, Path } from 'react-native-svg';

const borderColors = ['#0D69E6', '#91E240', '#EA4018']
const maxHeight = 69

export default function ColorVisualizer({ ...props }) {

  const Bar = ({ number, barHeight, dotted }) => {
    const fillColor = borderColors[number] + '20'
    const borderColor = borderColors[number]

    return(
      <View style={styles.barContainer}>
        <Svg height="70" width="400">
          <Path
            d={`M0 70 h150c20,0,30-${barHeight || 0},50-${barHeight || 0}s20,${barHeight || 0},50,${barHeight || 0}h150`}
            fill={dotted ? '#00000000' : fillColor}
            stroke={dotted ? borderColor + 'aa' : borderColor}
            strokeDasharray={dotted ? [2, 2] : []}
          />
        </Svg>
        <View tint="dark" intensity={100} style={{width: Layout.window.width, height: 1, marginTop: -2, marginBottom: -1}}/>
      </View>
    )
  }

  const topVal = Math.max( ...props.color )
  const color = props.color.map(val => (val / topVal))
  const [red, green, blue] = color

  return (
    <View style={styles.container}>
      {props.colorName && <View style={styles.titleContainer}>
        <Text style={styles.title}>Color</Text>
      </View>}
      {/* Actual data visualization */}
      <View style={styles.row}>
        <View style={{width: 90}}/>
        <Bar number={0} barHeight={red * maxHeight}/>
        <Bar number={1} barHeight={green * maxHeight}/>
        <Bar number={2} barHeight={blue * maxHeight}/>
        <View style={{width: 90}}/>
      </View>
    </View> 
  );
}

const styles = StyleSheet.create({
  container: {
    height: maxHeight + 20,
    width: Layout.window.width
  },
  title: {
    fontSize: 15,
    color: Colors.text + 'bb',
    fontFamily: 'verdana'
  },
  titleContainer: {
    marginTop: 13,
    marginLeft: 37,
    flexDirection: 'row',
    alignItems: 'center'
  },
  row: {
    position: 'absolute',
    top: 0,
    bottom: 0,
    left: 0,
    right: 0,
    flexDirection: 'row'
  },
  bar: {
    width: 20,
    borderTopLeftRadius: 5,
    borderTopRightRadius: 5,
    borderWidth: 1,
    borderBottomWidth: 0
  },
  barContainer: {
    flex: 1,
    justifyContent: 'flex-end',
    alignItems: 'center'
  }
})