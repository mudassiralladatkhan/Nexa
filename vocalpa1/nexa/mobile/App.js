/**
 * Nexa Voice Assistant - Mobile App
 * Main Application Component
 */

import React, { useEffect, useState } from 'react';
import {
  SafeAreaView,
  StatusBar,
  StyleSheet,
  useColorScheme,
  Alert,
  PermissionsAndroid,
  Platform,
} from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { Colors } from 'react-native/Libraries/NewAppScreen';

// Screens
import HomeScreen from './src/screens/HomeScreen';
import SettingsScreen from './src/screens/SettingsScreen';
import ConversationScreen from './src/screens/ConversationScreen';

// Services
import { VoiceService } from './src/services/VoiceService';
import { ApiService } from './src/services/ApiService';
import { StorageService } from './src/services/StorageService';

// Context
import { AppProvider } from './src/context/AppContext';

const Stack = createStackNavigator();

const App = () => {
  const isDarkMode = useColorScheme() === 'dark';
  const [isInitialized, setIsInitialized] = useState(false);

  const backgroundStyle = {
    backgroundColor: isDarkMode ? Colors.darker : Colors.lighter,
    flex: 1,
  };

  useEffect(() => {
    initializeApp();
  }, []);

  const initializeApp = async () => {
    try {
      // Request permissions
      await requestPermissions();
      
      // Initialize services
      await VoiceService.initialize();
      await ApiService.initialize();
      await StorageService.initialize();
      
      setIsInitialized(true);
      console.log('Nexa Mobile App initialized successfully');
    } catch (error) {
      console.error('Failed to initialize app:', error);
      Alert.alert(
        'Initialization Error',
        'Failed to initialize the app. Some features may not work properly.',
        [{ text: 'OK' }]
      );
      setIsInitialized(true); // Allow app to continue
    }
  };

  const requestPermissions = async () => {
    if (Platform.OS === 'android') {
      try {
        const grants = await PermissionsAndroid.requestMultiple([
          PermissionsAndroid.PERMISSIONS.RECORD_AUDIO,
          PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
          PermissionsAndroid.PERMISSIONS.ACCESS_COARSE_LOCATION,
          PermissionsAndroid.PERMISSIONS.INTERNET,
          PermissionsAndroid.PERMISSIONS.ACCESS_NETWORK_STATE,
        ]);

        console.log('Permissions granted:', grants);

        if (
          grants['android.permission.RECORD_AUDIO'] === PermissionsAndroid.RESULTS.GRANTED
        ) {
          console.log('Microphone permission granted');
        } else {
          Alert.alert(
            'Permission Required',
            'Microphone permission is required for voice commands.',
            [{ text: 'OK' }]
          );
        }
      } catch (err) {
        console.warn('Permission request error:', err);
      }
    }
  };

  if (!isInitialized) {
    return null; // Could show a loading screen here
  }

  return (
    <AppProvider>
      <SafeAreaView style={backgroundStyle}>
        <StatusBar
          barStyle={isDarkMode ? 'light-content' : 'dark-content'}
          backgroundColor={backgroundStyle.backgroundColor}
        />
        <NavigationContainer>
          <Stack.Navigator
            initialRouteName="Home"
            screenOptions={{
              headerStyle: {
                backgroundColor: isDarkMode ? '#1a1a1a' : '#6366F1',
              },
              headerTintColor: '#fff',
              headerTitleStyle: {
                fontWeight: 'bold',
                fontSize: 18,
              },
            }}>
            <Stack.Screen
              name="Home"
              component={HomeScreen}
              options={{
                title: 'Nexa Assistant',
                headerStyle: {
                  backgroundColor: '#6366F1',
                },
              }}
            />
            <Stack.Screen
              name="Settings"
              component={SettingsScreen}
              options={{
                title: 'Settings',
              }}
            />
            <Stack.Screen
              name="Conversation"
              component={ConversationScreen}
              options={{
                title: 'Conversation History',
              }}
            />
          </Stack.Navigator>
        </NavigationContainer>
      </SafeAreaView>
    </AppProvider>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});

export default App;
