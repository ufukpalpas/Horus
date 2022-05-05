import React, {Component, useState} from 'react'
import { Button,View,Text,SafeAreaView, ImageBackground, StyleSheet, Dimensions, TouchableOpacity} from 'react-native';
import {SliderHuePicker} from 'react-native-slider-color-picker';
import tinycolor from 'tinycolor2';

const {
    width,
} = Dimensions.get('window');

class ChangeColor2 extends Component{
    constructor(props) {
        super(props);
        this.state = {
            oldColor1: "#FF7700",
            oldColor2: "#FF7700",
        };
    }

    changeColor2 = (colorHsvOrRgb, resType) => {
        if (resType === 'end') {
            this.setState({
                oldColor: tinycolor(colorHsvOrRgb).toHexString(),
            });
        }
    }

  render(){
    const {
            oldColor1, oldColor2
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
          <Text
            style={{
              fontSize: 25,
              textAlign: 'center',
              marginBottom: 16
            }}>
            This is the First Page under First Page Option
          </Text>
          <SliderHuePicker
                        ref={view => {this.sliderHuePicker = view;}}
                        oldColor1={oldColor1}
                        trackStyle={[{height: 12, width: width - 48}]}
                        thumbStyle={styles.thumb}
                        useNativeDriver={true}
                        onColorChange={this.changeColor2}
                    />
          
          <TouchableOpacity  onPress={() => this.props.navigation.goBack()} >
                  <Text> ok</Text>
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

});

export default ChangeColor2;