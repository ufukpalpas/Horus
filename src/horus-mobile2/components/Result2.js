import React, {Component, useState} from 'react'
import { Button,View,Text,SafeAreaView, ImageBackground, StyleSheet,Dimensions} from 'react-native';
import {
  LineChart,
  BarChart,
  PieChart,
  ProgressChart,
  ContributionGraph,
  StackedBarChart,
} from "react-native-chart-kit";


class Result2 extends Component{
  renderChart(){
      
  }
  render(){
    const screenWidth = Dimensions.get("window").width;

    const pieChartConfig = {
          backgroundGradientFrom: "#1E2923",
          backgroundGradientFromOpacity: 0,
          backgroundGradientTo: "#08130D",
          backgroundGradientToOpacity: 0.5,
          color: (opacity = 1) => `rgba(26, 255, 146, ${opacity})`,
          strokeWidth: 2, // optional, default 3
          barPercentage: 0.5,
          useShadowColorFromDataset: false // optional
        };
   let angry = parseInt(this.props.route.params.angry);
   let disgust = parseInt(this.props.route.params.disgust);
   let fear = parseInt(this.props.route.params.fear);
   let happy = parseInt(this.props.route.params.happy);
   let sad = parseInt(this.props.route.params.sad);
   let surprise = parseInt(this.props.route.params.surprise);
   let neutral = parseInt(this.props.route.params.neutral); 
   let type = this.props.route.params.graph;
   let type2 = this.props.route.params.graph2;

  let angryColor = this.props.route.params.newAngryColor ? this.props.route.params.newAngryColor : this.props.route.params.colors.angry;
  let disgustColor = this.props.route.params.newDisgustColor ? this.props.route.params.newDisgustColor : this.props.route.params.colors.disgust;
  let fearColor = this.props.route.params.newFearColor ? this.props.route.params.newFearColor : this.props.route.params.colors.fear;
  let happyColor = this.props.route.params.newHappyColor ? this.props.route.params.newHappyColor : this.props.route.params.colors.happy;
  let sadColor = this.props.route.params.newSadColor ? this.props.route.params.newSadColor : this.props.route.params.colors.sad;
  let surpriseColor = this.props.route.params.newSurpriseColor ? this.props.route.params.newSurpriseColor : this.props.route.params.colors.surprise;
  let neutralColor = this.props.route.params.newNeutralColor ? this.props.route.params.newNeutralColor : this.props.route.params.colors.neutral;
var colors = ["rgba(255,0,0,1)", "rgba(0,255,0,1)", "rgba(255,0,0,1)", "rgba(0,255,0,1)", "rgba(0,0,255,1)", "rgba(255,0,0,1)", "rgba(0,255,0,1)"];

  return (
    <SafeAreaView style={{ flex: 1 }}>
      <View style={{ flex: 1 , padding: 16}}>
      <ImageBackground resizeMode="cover" source ={require('../assets/background.jpeg')} style={styles.background}>
        <View style={{flex: 1, alignItems: 'center', justifyContent: 'center',}}>
        {type == 'pie' ?
        <PieChart
          data={[
                {
                  name: "Angry",
                  population: angry,
                  color: angryColor,
                  legendFontColor: "#7F7F7F",
                  legendFontSize: 15
                },
                {
                  name: "Disgust",
                  population: disgust,
                  color: disgustColor,
                  legendFontColor: "#7F7F7F",
                  legendFontSize: 15
                },
                {
                  name: "Fear",
                  population: fear,
                  color: fearColor,
                  legendFontColor: "#7F7F7F",
                  legendFontSize: 15
                },
                {
                  name: "Happy",
                  population: happy,
                  color: happyColor,
                  legendFontColor: "#7F7F7F",
                  legendFontSize: 15
                },
                {
                  name: "Sad",
                  population: sad,
                  color: sadColor,
                  legendFontColor: "#7F7F7F",
                  legendFontSize: 15
                },
                {
                  name: "Surprise",
                  population: surprise,
                  color: surpriseColor,
                  legendFontColor: "#7F7F7F",
                  legendFontSize: 15
                },
                {
                  name: "Neutral",
                  population: neutral,
                  color: neutralColor,
                  legendFontColor: "#7F7F7F",
                  legendFontSize: 15
                }
              ]}
          width={screenWidth}
          height={220}
          chartConfig={pieChartConfig}
          accessor={"population"}
          backgroundColor={"transparent"}
          paddingLeft={"10"}
        /> :
        <Text>  </Text>}

        {type == 'line' ?
            <LineChart
              data={{
                labels: ['Angry', 'Disgust', 'Fear','Happy', 'Sad', 'Surprise', 'Neutral' ],
                datasets: [
                  {
                    data: [angry, disgust, fear, happy, sad, surprise, neutral],
                    strokeWidth: 2,
                    pointBackgroundColor: colors,
                  },
                ],
              }}     
              getDotColor={(dataPoint, dataPointIndex) => {
                console.log('dataPoint ---->', dataPoint);
                console.log('dataPointIndex --->', dataPointIndex);
                if (dataPointIndex === 0) return angryColor;
                if (dataPointIndex === 1) return disgustColor;
                if (dataPointIndex === 2) return fearColor;
                if (dataPointIndex === 3) return happyColor;
                if (dataPointIndex === 4) return sadColor;
                if (dataPointIndex === 5) return surpriseColor;
                if (dataPointIndex === 6) return neutralColor;
              }}         
              width={Dimensions.get('window').width - 16}
              height={220}
              chartConfig={{
                backgroundColor: '#dfb393',
                backgroundGradientFrom: '#eff3ff',
                backgroundGradientTo: '#efefef',
                decimalPlaces: 2,
                color: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
                style: {
                  borderRadius: 16,
                },
              }}
              style={{
                marginVertical: 8,
                borderRadius: 16,
              }}
            />
        :
        <Text>  </Text>}

        {type == 'bar' ?
        <BarChart
          data={{
            labels: ['Angry', 'Disgust', 'Fear','Happy', 'Sad', 'Surprise', 'Neutral' ],
            datasets: [
              {
                data: [angry, disgust, fear, happy, sad, surprise, neutral],
                colors: [(opacity=1) => angryColor,
                (opacity=1) => disgustColor,
                (opacity=1) => fearColor,
                (opacity=1) => happyColor,
                (opacity=1) => sadColor,
                (opacity=1) => surpriseColor,
                (opacity=1) => neutralColor
                ]
              },
            ],
          }}
          width={Dimensions.get('window').width - 16}
          height={220}
          withCustomBarColorFromData = {true}
          flatColor ={true}
          chartConfig={{
            backgroundColor: '#1cc910',
            backgroundGradientFrom: '#eff3ff',
            backgroundGradientTo: '#efefef',
            decimalPlaces: 2,
            color: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
            style: {
              borderRadius: 16,
            },
          }}
          style={{
            marginVertical: 8,
            borderRadius: 16,
          }}
        />
        :
        <Text>  </Text>}

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
