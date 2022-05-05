import React, {Component, useState} from 'react'
import { Button,View,Text,SafeAreaView, ImageBackground, StyleSheet,Dimensions} from 'react-native';
import {
  LineChart,
  BarChart,
  PieChart,
  ProgressChart,
  ContributionGraph,
  StackedBarChart
} from "react-native-chart-kit";


class Result2 extends Component{
  render(){
    const screenWidth = Dimensions.get("window").width;
    const sliceColor = ['#F44336','#2196F3','#FFEB3B', '#4CAF50', '#FF9800']
    const chartConfig = {
          backgroundGradientFrom: "#1E2923",
          backgroundGradientFromOpacity: 0,
          backgroundGradientTo: "#08130D",
          backgroundGradientToOpacity: 0.5,
          color: (opacity = 1) => `rgba(26, 255, 146, ${opacity})`,
          strokeWidth: 2, // optional, default 3
          barPercentage: 0.5,
          useShadowColorFromDataset: false // optional
        };
   const angry = parseInt(this.props.route.params.angry);
   const disgust = parseInt(this.props.route.params.disgust);
   const fear = parseInt(this.props.route.params.fear);
   const happy = parseInt(this.props.route.params.happy);
   const sad = parseInt(this.props.route.params.sad);
   const surprise = parseInt(this.props.route.params.surprise);
   const neutral = parseInt(this.props.route.params.neutral); 

  return (
    <SafeAreaView style={{ flex: 1 }}>
      <View style={{ flex: 1 , padding: 16}}>
      <ImageBackground resizeMode="cover" source ={require('../assets/background.jpeg')} style={styles.background}>
        <View style={{flex: 1, alignItems: 'center', justifyContent: 'center',}}>
        <PieChart
          data={[
                {
                  name: "Angry",
                  population: angry,
                  color: "red",
                  legendFontColor: "#7F7F7F",
                  legendFontSize: 15
                },
                {
                  name: "Disgust",
                  population: disgust,
                  color: "blue",
                  legendFontColor: "#7F7F7F",
                  legendFontSize: 15
                },
                {
                  name: "Fear",
                  population: fear,
                  color: "orange",
                  legendFontColor: "#7F7F7F",
                  legendFontSize: 15
                },
                {
                  name: "Happy",
                  population: happy,
                  color: "pink",
                  legendFontColor: "#7F7F7F",
                  legendFontSize: 15
                },
                {
                  name: "Sad",
                  population: sad,
                  color: "yellow",
                  legendFontColor: "#7F7F7F",
                  legendFontSize: 15
                },
                {
                  name: "Surprise",
                  population: surprise,
                  color: "green",
                  legendFontColor: "#7F7F7F",
                  legendFontSize: 15
                },
                {
                  name: "Neutral",
                  population: neutral,
                  color: "white",
                  legendFontColor: "#7F7F7F",
                  legendFontSize: 15
                }
              ]}
          width={screenWidth}
          height={220}
          chartConfig={chartConfig}
          accessor={"population"}
          backgroundColor={"transparent"}
          paddingLeft={"10"}
        />
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
  title: {
    fontSize: 24,
    margin: 10
  }

});

export default Result2;
