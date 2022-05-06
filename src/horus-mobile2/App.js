import React, { Component }  from 'react';
import { registerRootComponent } from 'expo';
import { createConsumer } from '@rails/actioncable'
import {TouchableOpacity, Image, Button, View, Text,StyleSheet} from 'react-native';
import {createStackNavigator} from "@react-navigation/stack"
import {NavigationContainer} from '@react-navigation/native';
import Appl from "./start.js"
import CurrentAnalysis from "./components/CurrentAnalysis.js"
import YourLastAnalyses from "./components/YourLastAnalyses.js"
import Settings from "./components/Settings.js"

const Stack = createStackNavigator();

class App extends Component
  {
    constructor(props) {
      super(props);
    }
    render(){
      
    const navigationOptionsL = ({ navigation }) => {
        const { navigate } = navigation
        return{
            headerTitle: () => <View>
                            <Text style={styles.text}> Your Last </Text>
                            <Text style={styles.text}> Analyses </Text>
                        </View>,
            //headerTitleStyle: {fontFamily: 'V-dub', fontSize: 15},
            headerStyle: {height: 70, 
            backgroundColor: '#dfb393', //cream
            borderBottomWidth: 0 },
            headerShadowVisible: false,
             headerLeft: () => {
                return (
                <TouchableOpacity  onPress={() => navigate('Appl')} >
                  <Image
                    source={require('./assets/arrow.png')}
                    style={{
                      width: 27,
                      height: 27,
                      marginLeft: 5
                    }}
                  />
                </TouchableOpacity>
                )
              },
        }
    }
    const navigationOptionsS = ({ navigation }) => {
        const { navigate } = navigation
        return{
            headerTitle: 'Settings',
            headerTitleStyle: {fontFamily: 'V-dub', fontSize: 15},
            headerStyle: {height: 70, 
            backgroundColor: '#dfb393', //cream
            borderBottomWidth: 0 },
            headerShadowVisible: false,
             headerLeft: () => {
                return (
                <TouchableOpacity  onPress={() => navigate('Appl')} >
                  <Image
                    source={require('./assets/arrow.png')}
                    style={{
                      width: 27,
                      height: 27,
                      marginLeft: 5
                    }}
                  />
                </TouchableOpacity>
                )
              },
        }
    }
    return (
      <NavigationContainer >
        <Stack.Navigator
          initialRouteName="Appl"
        >
          <Stack.Screen
            name="Appl"
            component={Appl}
            options={{headerShown: false,
            }}
          />
          <Stack.Screen
            name="CurrentAnalysis"
            component={CurrentAnalysis}
            options={{headerShown: false,
            }}
          />
          <Stack.Screen
            name="YourLastAnalyses"
            component={YourLastAnalyses}
            options={navigationOptionsL}
          />
          <Stack.Screen
            name="Settings"
            component={Settings}
            options={navigationOptionsS}
          />
        </Stack.Navigator>
        </NavigationContainer>
      );
    }}


const styles = StyleSheet.create({
  text: {
    fontSize: 15,
    fontWeight: 'bold',
    textAlign: 'center',
    fontFamily: 'V-dub'
  },

});

export default App;
