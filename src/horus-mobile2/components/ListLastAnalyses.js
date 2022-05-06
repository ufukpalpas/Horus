import React, {Component, useState} from 'react'
import { Text, View, StyleSheet, Image, ImageBackground, TouchableOpacity, CustomList, Button } from 'react-native';
import Constants from 'expo-constants';
import AppLoading from 'expo-app-loading';
import * as Font from 'expo-font';
import { createAppContainer,  NavigationContainer, DrawerActions, NavigationActions} from '@react-navigation/native';
import {createStackNavigator} from "@react-navigation/stack";
import { createDrawerNavigator } from '@react-navigation/drawer';
import 'react-native-gesture-handler';
//import Appl from "../start.js";
import Result2 from './Result2';
import ChangeGraph from './ChangeGraph';
import ChangeColor2 from './ChangeColor2';

const Drawer = createDrawerNavigator();
const Stack = createStackNavigator(); 

let customFonts = {
  'V-dub': require('../assets/fonts/v_dub.ttf'),
};

export default class ListLastAnalyses extends Component{
   state = {
    fontsLoaded: false,
  };
  constructor(props) {
      super(props);
  }
  async _loadFontsAsync() {
    await Font.loadAsync(customFonts);
    this.setState({ fontsLoaded: true });
  }

  componentDidMount() {
    this._loadFontsAsync();
  }
  
  render(){
  if (!this.state.fontsLoaded) {
    return <AppLoading />;
  } 
  let graph = null;
  if(this.props.route.params.cograph != null){
      graph = this.props.route.params.cograph;
  }
  else if(this.props.route.params.graph != null){
      graph = this.props.route.params.graph;
  }
  else{
      graph = 'pie';
  }
  return (
    <NavigationContainer  independent={true}>
    {   
      <Drawer.Navigator 
        screenOptions={{
          //overlayColor: "transparent",
          //sceneContainerStyle: { backgroundColor: "transparent" },
          headerShown: true,
          drawerPosition:"right",
          drawerLabelStyle: {fontFamily: 'V-dub'},
          drawerStyle: {
            flex: 1,
            backgroundColor: '#dfb393',
          },
           headerStyle: {
           backgroundColor: '#dfb393' //cream
          },
        }}
        drawerContentOptions={{
          activeTintColor: '#0f0f0f', //black
          //itemStyle: { marginVertical: 15 },
        }}>
         
        <Drawer.Screen
          name ='ListLastAnalyses'
          initialParams={{ angry: this.props.route.params.angry, 
                            disgust:this.props.route.params.disgust,
                            fear:this.props.route.params.fear,
                            happy:this.props.route.params.happy,
                            sad:this.props.route.params.sad,
                            surprise:this.props.route.params.surprise,
                            neutral:this.props.route.params.neutral,
                            scans:this.props.route.params.scans,
                            colors: {angry: 'red', disgust: 'blue', fear: 'orange', happy:'pink', sad:'yellow',surprise:'green',neutral:'white' } ,
                            newAngryColor: this.props.route.params.newAngryColor, 
                            newDisgustColor: this.props.route.params.newDisgustColor,
                            newFearColor: this.props.route.params.newFearColor,
                            newHappyColor:this.props.route.params.newHappyColor,
                            newSadColor:this.props.route.params.newSadColor,
                            newSurpriseColor:this.props.route.params.newSurpriseColor,
                            newNeutralcolor:this.props.route.params.newNeutralcolor,
                            graph:graph,
                            graph2:this.props.route.params.cograph,
                                }}             
          options={({navigation})=>({
             title: 'Result',
             headerTitleStyle: {fontFamily: 'V-dub', fontSize: 15},
             headerStyle: {height: 70, 
                          backgroundColor: '#dfb393', //cream
                          borderBottomWidth: 0 },
             headerShadowVisible: false,
             headerLeft: () => {
                return (
                <TouchableOpacity  onPress={() => this.props.navigation.navigate('YourLastAnalyses')} >
                  <Image
                    source={require('../assets/arrow.png')}
                    style={{
                      width: 27,
                      height: 27,
                      marginLeft: 5
                    }}
                  />
                </TouchableOpacity>
                )
              },
             headerRight: () => {
                return (
                <TouchableOpacity  onPress={() => navigation.dispatch(DrawerActions.openDrawer())}>
                  <Image
                    source={require('../assets/settings.png')}
                    style={{
                      width: 25,
                      height: 25,
                      marginRight: 5
                    }}
                  />
                </TouchableOpacity>
                )
              }
             })}
          component={Result2}/>
        <Button
          onPress={onPressLearnMore}
          title="Learn More"
          color="#841584"
          accessibilityLabel="Learn more about this purple button"
        />

        <Drawer.Screen
          name="ChangeColor"
          initialParams ={{graph: this.props.route.params.graph}}
          options={({navigation})=>({
             title: 'Change Color',
             headerTitleStyle: {fontFamily: 'V-dub', fontSize: 15},
             headerLeft: () => {
                return (
                <TouchableOpacity  onPress={() => this.props.navigation.navigate('YourLastAnalyses')} >
                  <Image
                    source={require('../assets/arrow.png')}
                    style={{
                      width: 25,
                      height: 25,
                      marginLeft: 5
                    }}
                  />
                </TouchableOpacity>
                )
              },
             headerRight: () => {
                return (
                <TouchableOpacity  onPress={() => navigation.dispatch(DrawerActions.openDrawer())}>
                  <Image
                    source={require('../assets/settings.png')}
                    style={{
                      width: 25,
                      height: 25,
                      marginRight: 5
                    }}
                  />
                </TouchableOpacity>
                )
              }
             })}
          component={ChangeColor2} />
          <Drawer.Screen
          name="ChangeGraph"
          options={({navigation})=>({
             drawerLabel: 'Change Graph',
             headerTitleStyle: {fontFamily: 'V-dub', fontSize: 15},
             headerLeft: () => {
                return (
                <TouchableOpacity  onPress={() => this.props.navigation.navigate('YourLastAnalyses')} >
                  <Image
                    source={require('../assets/arrow.png')}
                    style={{
                      width: 25,
                      height: 25,
                      marginLeft: 5
                    }}
                  />
                </TouchableOpacity>
                )
              },
             headerRight: () => {
                return (
                <TouchableOpacity  onPress={() => navigation.dispatch(DrawerActions.openDrawer())}>
                  <Image
                    source={require('../assets/settings.png')}
                    style={{
                      width: 25,
                      height: 25,
                      marginRight: 5
                    }}
                  />
                </TouchableOpacity>
                )
              }
             })}
          component={ChangeGraph} />
          
    </Drawer.Navigator>}
    </NavigationContainer>
  );
}}


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
  icon: {
    width: 24,
    height: 24,
  },
  to: {
    position: 'absolute',
    top: '5%',
    left: '5%',
  }
});

