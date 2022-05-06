import React, {Component, useState} from 'react'
import { Button,View,Text,SafeAreaView, ImageBackground, StyleSheet, Dimensions, TouchableOpacity} from 'react-native';
import {SliderHuePicker} from 'react-native-slider-color-picker';
import tinycolor from 'tinycolor2';
import CurrentAnalysis from './CurrentAnalysis';
import Result from './Result';

const {
    width,
} = Dimensions.get('window');

class ChangeColor2 extends Component{
    constructor(props) {
        super(props);
        this.state = {
            oldColor1: "red",
            oldColor2: "blue",
            oldColor3: "orange",
            oldColor4: "pink",
            oldColor5: "yellow",
            oldColor6: "green",
            oldColor7: "white",
        };
    }
    
    changeColor1 = ( colorHsvOrRgb, resType) => {
        if (resType === 'end') {
            this.setState({
                oldColor1: tinycolor(colorHsvOrRgb).toHexString(),
            });    
        }
    }
    changeColor2 = (colorHsvOrRgb, resType) => {
        if (resType === 'end') {
            this.setState({
                oldColor2: tinycolor(colorHsvOrRgb).toHexString(),
            });
        }
    }
    changeColor3 = (colorHsvOrRgb, resType) => {
        if (resType === 'end') {
            this.setState({
                oldColor3: tinycolor(colorHsvOrRgb).toHexString(),
            });
        }
    }
    changeColor4 = (colorHsvOrRgb, resType) => {
        if (resType === 'end') {
            this.setState({
                oldColor4: tinycolor(colorHsvOrRgb).toHexString(),
            });
        }
    }
    changeColor5 = (colorHsvOrRgb, resType) => {
        if (resType === 'end') {
            this.setState({
                oldColor5: tinycolor(colorHsvOrRgb).toHexString(),
            });
        }
    }
    changeColor6 = (colorHsvOrRgb, resType) => {
        if (resType === 'end') {
            this.setState({
                oldColor6: tinycolor(colorHsvOrRgb).toHexString(),
            });
        }
    }
    changeColor7 = (colorHsvOrRgb, resType) => {
        if (resType === 'end') {
            this.setState({
                oldColor7: tinycolor(colorHsvOrRgb).toHexString(),
            });
        }
    }

  render(){
    const {
            oldColor1, oldColor2, oldColor3, oldColor4, oldColor5, oldColor6, oldColor7,
        } = this.state;
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
          <Text style={styles.text}> Angry </Text>
          <SliderHuePicker
              ref={view => {this.sliderHuePicker = view;}}
              oldColor1={oldColor1}
              trackStyle={[{height: 12, width: width - 48}]}
              thumbStyle={styles.thumb}
              useNativeDriver={true}
              onColorChange={this.changeColor1}
          />
          <Text style={styles.text}> Disgust </Text>
          <SliderHuePicker
              ref={view => {this.sliderHuePicker = view;}}
              oldColor2={oldColor2}
              trackStyle={[{height: 12, width: width - 48}]}
              thumbStyle={styles.thumb}
              useNativeDriver={true}
              onColorChange={this.changeColor2}
          />
          <Text style={styles.text}> Fear </Text>
          <SliderHuePicker
              ref={view => {this.sliderHuePicker = view;}}
              oldColor3={oldColor3}
              trackStyle={[{height: 12, width: width - 48}]}
              thumbStyle={styles.thumb}
              useNativeDriver={true}
              onColorChange={this.changeColor3}
          />
          <Text style={styles.text}> Happy </Text>
          <SliderHuePicker
              ref={view => {this.sliderHuePicker = view;}}
              oldColor4={oldColor4}
              trackStyle={[{height: 12, width: width - 48}]}
              thumbStyle={styles.thumb}
              useNativeDriver={true}
              onColorChange={this.changeColor4}
          />
          <Text style={styles.text}> Sad </Text>
          <SliderHuePicker
              ref={view => {this.sliderHuePicker = view;}}
              oldColor5={oldColor5}
              trackStyle={[{height: 12, width: width - 48}]}
              thumbStyle={styles.thumb}
              useNativeDriver={true}
              onColorChange={this.changeColor5}
          />
          <Text style={styles.text}> Surprise </Text>
          <SliderHuePicker
              ref={view => {this.sliderHuePicker = view;}}
              oldColor6={oldColor6}
              trackStyle={[{height: 12, width: width - 48}]}
              thumbStyle={styles.thumb}
              useNativeDriver={true}
              onColorChange={this.changeColor6}
          />
          <Text style={styles.text}> Neutral </Text>
          <SliderHuePicker
              ref={view => {this.sliderHuePicker = view;}}
              oldColor7={oldColor7}
              trackStyle={[{height: 12, width: width - 48}]}
              thumbStyle={styles.thumb}
              useNativeDriver={true}
              onColorChange={this.changeColor7}
          />
          <TouchableOpacity  onPress={() => this.props.navigation.navigate('ListLastAnalyses', {newAngryColor: oldColor1, newDisgustColor: oldColor2,newFearColor: oldColor3, newHappyColor:oldColor4, newSadColor: oldColor5,newSurpriseColor:oldColor6,newNeutralColor:oldColor7, cograph: 'line'})} > 
                  <Text style ={styles.to}> OK</Text>
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
    fontSize: 20,
    textAlign: 'center',
    marginBottom: 6
  },
  to:{
    fontSize: 25,
    textAlign: 'center',
    fontWeight: 'bold',
  },
});

export default ChangeColor2;
