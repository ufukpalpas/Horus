import React, {Component, useState} from 'react'
import { Button,View,Text,SafeAreaView, ImageBackground, StyleSheet, Dimensions, TouchableOpacity} from 'react-native';
import {SliderHuePicker} from 'react-native-slider-color-picker';
import tinycolor from 'tinycolor2';
import CurrentAnalysis from './CurrentAnalysis';
import Result from './Result';

const {
    width,
} = Dimensions.get('window');

class ChangeGraph extends Component{
    constructor(props) {
        super(props);
    }
  render(){
  return (
    <SafeAreaView style={{ flex: 1 }}>
      <View style={{ flex: 1 , padding: 16}}>
      <ImageBackground resizeMode="cover" source ={require('../assets/background.jpeg')} style={styles.background}>
        <View
          style={{
            flex: 1,
            alignItems: 'center',
            justifyContent: 'center',
          }}>  

          <TouchableOpacity  style ={styles.to} onPress={() => this.props.navigation.navigate('ListLastAnalyses', {graph: 'bar'})} > 
                  <Text style ={styles.text}> BAR</Text>
          </TouchableOpacity>
          <TouchableOpacity style ={styles.to}  onPress={() => this.props.navigation.navigate('ListLastAnalyses', {graph: 'pie'})} > 
                  <Text style ={styles.text}> PIE</Text>
          </TouchableOpacity>
          <TouchableOpacity style ={styles.to}  onPress={() => this.props.navigation.navigate('ListLastAnalyses', {graph: 'line'})} > 
                  <Text style ={styles.text}> LINE</Text>
          </TouchableOpacity>

        </View>
        </ImageBackground>
      </View>
    </SafeAreaView>
  );
}}
 
const styles = StyleSheet.create({
  background: {
    flex: 1,
    justifyContent: "center",
    height: '100%',
    width : '100%'
  },
  text: {
    fontSize: 25,
    textAlign: 'center',
    fontWeight: 'bold',
    
  },
  to:{
    textAlign: 'center',
    marginBottom: 12,
  },
});

export default ChangeGraph;
