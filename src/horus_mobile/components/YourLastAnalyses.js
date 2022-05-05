import React, {Component} from 'react'
import { Text, View, StyleSheet, Image, ImageBackground, TouchableOpacity, CustomList } from 'react-native';
import {createStackNavigator} from "@react-navigation/stack";
import {NavigationContainer} from '@react-navigation/native';
import Constants from 'expo-constants';
import AppLoading from 'expo-app-loading';
import * as Font from 'expo-font';
import ListLastAnalyses from "./ListLastAnalyses.js"

let customFonts = {
  'V-dub': require('../assets/fonts/v_dub.ttf'),
};



const Stack = createStackNavigator();

export default class MyStack extends Component {
    constructor(props) {
      super(props);
    }
  render(){
  return (
    <NavigationContainer independent='true'>
      <Stack.Navigator>
        <Stack.Screen
          name="YourLastAnalyses"
          component={YourLastAnalyses}
          options={{ title: 'YourLastAnalyses', headerShown: false, }}
          initialParams={{ angry: this.props.route.params.angry, 
                            disgust:this.props.route.params.disgust,
                            fear:this.props.route.params.fear,
                            happy:this.props.route.params.happy,
                            sad:this.props.route.params.sad,
                            surprise:this.props.route.params.surprise,
                            neutral:this.props.route.params.neutral,
                            scans: this.props.route.params.scans  }}
        />
        <Stack.Screen name="ListLastAnalyses" component={ListLastAnalyses} 
          options={{ title: 'ListLastAnalyses', headerShown: false, }}
          initialParams={{ angry: this.props.route.params.angry, 
                            disgust:this.props.route.params.disgust,
                            fear:this.props.route.params.fear,
                            happy:this.props.route.params.happy,
                            sad:this.props.route.params.sad,
                            surprise:this.props.route.params.surprise,
                            neutral:this.props.route.params.neutral,
                            scans: this.props.route.params.scans  }}/>
      </Stack.Navigator>
    </NavigationContainer>
  );
}};

class YourLastAnalyses extends Component{
   state = {
    fontsLoaded: false,
  };

  async _loadFontsAsync() {
    await Font.loadAsync(customFonts);
    this.setState({ fontsLoaded: true });
  }
  constructor(props) {
      super(props);
  }
  componentDidMount() {
    this._loadFontsAsync();
  }

    renderT(arr) {
    return arr.map(obj => {
      return <TouchableOpacity onPress={() => this.props.navigation.navigate('ListLastAnalyses',
{angry: obj.angry, disgust:obj.disgust,fear:obj.fear, happy:obj.happy, sad:obj.sad, surprise:obj.surprise, neutral:obj.neutral })} >
              <Text style={styles.text} >{obj.name}</Text>
            </TouchableOpacity>;
    });
    }
  render() {
    const { navigation } = this.props;  
    const arr = [];
    for (const [key, value] of Object.entries(this.props.route.params.scans)) {
      arr.push(value);
    }
    if (!this.state.fontsLoaded) {
      return <AppLoading />;
    }
    return (
    <View style={styles.container}>
    <ImageBackground resizeMode="cover" source ={require('../assets/background.jpeg')} style={styles.background}> 
      <View style={styles.row,{alignItems:'center'}}>{this.renderT(arr)}</View>
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
    fontSize: 24,
    fontWeight: 'bold',
    fontFamily: 'V-dub',
    marginBottom: 8,
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

