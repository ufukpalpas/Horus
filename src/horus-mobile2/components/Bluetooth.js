import React, {Component} from 'react'
import { Text, View, StyleSheet, Button, Image, ImageBackground, TouchableOpacity, CustomList } from 'react-native';
import Constants from 'expo-constants';
import AppLoading from 'expo-app-loading';
import * as Font from 'expo-font';

let customFonts = {
  'V-dub': require('../assets/fonts/v_dub.ttf'),
};
export default class Settings extends Component{
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
    <ImageBackground resizeMode="cover" source ={require('../assets/background.jpeg')} style={styles.background}> 
    <TouchableOpacity
        onPress={() => alert('Hello, world!')}>
        <Text style={{ fontSize: 15,
          fontWeight: 'bold',
          textAlign: 'center',
          fontFamily: 'V-dub' }}>Search</Text>
      </TouchableOpacity>
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
    //fontStyle: 'arial',
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    fontFamily: 'V-dub',
    position: 'absolute',
    top: '5%',
    left: '20%'
  },
  background: {
    flex: 1,
    justifyContent: "center",
    height: '100%',
    width : '100%'
  },
  to: {
    position: 'absolute',
    top: '5%',
    left: '5%',
  }
});
