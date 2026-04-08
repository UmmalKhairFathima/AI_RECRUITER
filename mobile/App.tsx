import 'react-native-gesture-handler';
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { StatusBar } from 'expo-status-bar';
import { CandidateScreen } from './src/screens/CandidateScreen';
import { InterviewScreen } from './src/screens/InterviewScreen';
import { RecruiterScreen } from './src/screens/RecruiterScreen';

const Tab = createBottomTabNavigator();
const CandidateStack = createNativeStackNavigator();

function CandidateFlow() {
  return (
    <CandidateStack.Navigator>
      <CandidateStack.Screen name="CandidateHome" component={CandidateScreen} options={{ title: 'Candidate Portal' }} />
      <CandidateStack.Screen name="Interview" component={InterviewScreen} options={{ title: 'AI Interview' }} />
    </CandidateStack.Navigator>
  );
}

export default function App() {
  return (
    <NavigationContainer>
      <StatusBar style="dark" />
      <Tab.Navigator screenOptions={{ headerShown: false }}>
        <Tab.Screen name="Candidate" component={CandidateFlow} />
        <Tab.Screen name="Recruiter" component={RecruiterScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
