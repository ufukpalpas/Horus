import React, {Component} from 'react'
import { Text, View, StyleSheet, Image, ImageBackground, TouchableOpacity, CustomList } from 'react-native';
import Constants from 'expo-constants';
import AppLoading from 'expo-app-loading';
import * as Font from 'expo-font';

let customFonts = {
  'V-dub': require('./assets/fonts/v_dub.ttf'),
};
let angry = 1;
let disgust = 2;
let fear = 3;
let happy = 4;
let sad = 5;
let surprise = 6;
let neutral = 7;
let scans = {scan1: {name:'scan1', angry:1, disgust:1, fear:1, happy:1, sad:1, surprise:1, neutral:1},
 scan2: {name:'scan2', angry:2, disgust:2, fear:2, happy:3, sad:3, surprise:3, neutral:2}};

export default class App extends Component{
   state = {
    fontsLoaded: false,
  };

  async _loadFontsAsync() {
    await Font.loadAsync(customFonts);
    this.setState({ fontsLoaded: true });
  }

  componentDidMount() {
    this._loadFontsAsync();
  }
  render() {
    if (!this.state.fontsLoaded) {
      return <AppLoading />;
    }
    return (
    <View style={styles.container}>
    <ImageBackground resizeMode="cover" source ={require('./assets/background.jpeg')} style={styles.background}>
      <Image source={require('./assets/logo.png')} style={ [{marginBottom: -100}]}/>
      <Text style={[styles.text, {fontSize:50}] }>HORUS</Text>
      <TouchableOpacity style={styles.to} onPress={() => {this.props.navigation.navigate('CurrentAnalysis', {angry: angry, disgust:disgust,fear:fear, happy:happy, sad:sad, surprise:surprise, neutral:neutral })}}> 
        <Text style={styles.text}>Current Analysis</Text></TouchableOpacity>
      <TouchableOpacity style={styles.to}onPress={() => {this.props.navigation.navigate('YourLastAnalyses', {angry: angry, disgust:disgust,fear:fear, happy:happy, sad:sad, surprise:surprise, neutral:neutral, scans:scans })}}>
        <Text style={styles.text}>List Last Analyses</Text></TouchableOpacity>
      <TouchableOpacity style={styles.to}onPress={() => {this.props.navigation.navigate('Settings')}}>
        <Text style={styles.text}>Settings</Text></TouchableOpacity>
    </ImageBackground>
    </View>
  );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center'
  },
  text: {
    margin: 24,
    fontStyle: 'arial',
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    fontFamily: 'V-dub'
  },
  background: {
    flex: 1,
    justifyContent: "center",
    height: '100%',
    width : '100%'
  },
  to: {
    fontStyle: 'times',
    fontSize : 50
  }
});
