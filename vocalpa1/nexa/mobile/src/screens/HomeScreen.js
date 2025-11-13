/**
 * Nexa Mobile - Home Screen
 * Main voice assistant interface
 */

import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Dimensions,
  Animated,
  Alert,
  ScrollView,
} from 'react-native';
import LinearGradient from 'react-native-linear-gradient';
import Icon from 'react-native-vector-icons/MaterialIcons';

import { useApp } from '../context/AppContext';
import { VoiceService } from '../services/VoiceService';
import { ApiService } from '../services/ApiService';
import { colors, typography, spacing } from '../styles/theme';

// Components
import VoiceVisualizer from '../components/VoiceVisualizer';
import QuickActions from '../components/QuickActions';
import StatusIndicator from '../components/StatusIndicator';
import MessageBubble from '../components/MessageBubble';

const { width, height } = Dimensions.get('window');

const HomeScreen = ({ navigation }) => {
  const { state, actions } = useApp();
  const [pulseAnim] = useState(new Animated.Value(1));
  const [waveAnim] = useState(new Animated.Value(0));
  const [statusMessage, setStatusMessage] = useState('Hi! Say "Hey Nexa" or tap the microphone...');

  useEffect(() => {
    initializeVoiceService();
    checkBackendConnection();
    
    // Set up periodic connection check
    const connectionInterval = setInterval(checkBackendConnection, 30000);
    
    return () => {
      clearInterval(connectionInterval);
      VoiceService.cleanup();
    };
  }, []);

  useEffect(() => {
    // Update status message based on app state
    if (state.isListening) {
      setStatusMessage('Listening...');
      startPulseAnimation();
    } else if (state.isProcessing) {
      setStatusMessage('Processing your request...');
    } else if (state.isSpeaking) {
      setStatusMessage('Speaking response...');
    } else if (!state.isConnected) {
      setStatusMessage('Backend disconnected. Check your connection.');
    } else {
      setStatusMessage('Ready! Say "Hey Nexa" or tap the microphone...');
      stopPulseAnimation();
    }
  }, [state.isListening, state.isProcessing, state.isSpeaking, state.isConnected]);

  const initializeVoiceService = async () => {
    try {
      await VoiceService.initialize();
      
      // Set up voice event listeners
      VoiceService.onSpeechStart(() => {
        actions.setListening(true);
      });
      
      VoiceService.onSpeechEnd(() => {
        actions.setListening(false);
      });
      
      VoiceService.onSpeechResults((results) => {
        if (results && results.length > 0) {
          const command = results[0];
          handleVoiceCommand(command);
        }
      });
      
      VoiceService.onSpeechError((error) => {
        console.error('Speech error:', error);
        actions.setListening(false);
        actions.addNotification({
          type: 'error',
          message: 'Speech recognition error: ' + error.message,
        });
      });
      
      actions.setVoiceState({ isInitialized: true });
    } catch (error) {
      console.error('Failed to initialize voice service:', error);
      Alert.alert(
        'Voice Service Error',
        'Failed to initialize voice recognition. Please check microphone permissions.',
        [{ text: 'OK' }]
      );
    }
  };

  const checkBackendConnection = async () => {
    try {
      const isConnected = await ApiService.testConnection();
      actions.setConnected(isConnected);
      
      if (isConnected) {
        actions.updateBackendStatus({
          connected: true,
          lastCheck: new Date().toISOString(),
          error: null,
        });
      }
    } catch (error) {
      console.error('Backend connection failed:', error);
      actions.setConnected(false);
      actions.updateBackendStatus({
        connected: false,
        lastCheck: new Date().toISOString(),
        error: error.message,
      });
    }
  };

  const handleVoiceCommand = async (command) => {
    if (!command || command.trim().length === 0) return;
    
    try {
      actions.setProcessing(true);
      
      // Add user message to conversation
      actions.addMessage({
        type: 'user',
        content: command,
        confidence: 0.9,
      });
      
      // Send to backend
      const response = await ApiService.processCommand(command);
      
      // Add assistant response
      actions.addMessage({
        type: 'assistant',
        content: response.response_text,
      });
      
      // Speak response if voice feedback is enabled
      if (state.preferences.voiceFeedback && response.response_text) {
        actions.setSpeaking(true);
        await VoiceService.speak(response.response_text);
        actions.setSpeaking(false);
      }
      
    } catch (error) {
      console.error('Command processing failed:', error);
      const errorMessage = 'Sorry, I had trouble processing that command.';
      
      actions.addMessage({
        type: 'assistant',
        content: errorMessage,
      });
      
      if (state.preferences.voiceFeedback) {
        actions.setSpeaking(true);
        await VoiceService.speak(errorMessage);
        actions.setSpeaking(false);
      }
    } finally {
      actions.setProcessing(false);
    }
  };

  const toggleListening = async () => {
    try {
      if (state.isListening) {
        await VoiceService.stopListening();
      } else {
        await VoiceService.startListening();
      }
    } catch (error) {
      console.error('Toggle listening failed:', error);
      Alert.alert('Error', 'Failed to toggle voice recognition');
    }
  };

  const handleQuickAction = (action) => {
    const commands = {
      weather: "What's the weather like?",
      news: "Latest news headlines",
      music: "Play some music",
      time: "What time is it?",
      calculator: "Open calculator",
      help: "What can you do?",
    };
    
    const command = commands[action];
    if (command) {
      handleVoiceCommand(command);
    }
  };

  const startPulseAnimation = () => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.2,
          duration: 1000,
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 1000,
          useNativeDriver: true,
        }),
      ])
    ).start();
  };

  const stopPulseAnimation = () => {
    pulseAnim.stopAnimation();
    Animated.timing(pulseAnim, {
      toValue: 1,
      duration: 300,
      useNativeDriver: true,
    }).start();
  };

  const getRecentMessages = () => {
    return state.conversations.slice(-4).reverse();
  };

  return (
    <LinearGradient
      colors={['#6366F1', '#8B5CF6', '#A855F7']}
      style={styles.container}>
      
      {/* Header */}
      <View style={styles.header}>
        <StatusIndicator 
          isConnected={state.isConnected}
          isListening={state.isListening}
          isSpeaking={state.isSpeaking}
        />
        <TouchableOpacity
          style={styles.settingsButton}
          onPress={() => navigation.navigate('Settings')}>
          <Icon name="settings" size={24} color="#fff" />
        </TouchableOpacity>
      </View>

      <ScrollView 
        style={styles.content}
        contentContainerStyle={styles.contentContainer}
        showsVerticalScrollIndicator={false}>
        
        {/* Status Message */}
        <View style={styles.statusContainer}>
          <Text style={styles.statusText}>{statusMessage}</Text>
        </View>

        {/* Voice Visualizer */}
        <View style={styles.visualizerContainer}>
          <VoiceVisualizer 
            isListening={state.isListening}
            isSpeaking={state.isSpeaking}
          />
        </View>

        {/* Main Microphone Button */}
        <View style={styles.microphoneContainer}>
          <Animated.View
            style={[
              styles.microphoneWrapper,
              { transform: [{ scale: pulseAnim }] }
            ]}>
            <TouchableOpacity
              style={[
                styles.microphoneButton,
                state.isListening && styles.microphoneButtonActive,
                !state.isConnected && styles.microphoneButtonDisabled,
              ]}
              onPress={toggleListening}
              disabled={!state.isConnected}>
              <Icon 
                name={state.isListening ? "mic" : "mic_none"} 
                size={40} 
                color="#fff" 
              />
            </TouchableOpacity>
          </Animated.View>
        </View>

        {/* Quick Actions */}
        <QuickActions onActionPress={handleQuickAction} />

        {/* Recent Messages */}
        {getRecentMessages().length > 0 && (
          <View style={styles.messagesContainer}>
            <Text style={styles.messagesTitle}>Recent</Text>
            {getRecentMessages().map((message, index) => (
              <MessageBubble
                key={message.id || index}
                message={message}
                style={styles.messageBubble}
              />
            ))}
            <TouchableOpacity
              style={styles.viewAllButton}
              onPress={() => navigation.navigate('Conversation')}>
              <Text style={styles.viewAllText}>View All Conversations</Text>
              <Icon name="arrow-forward" size={16} color="#6366F1" />
            </TouchableOpacity>
          </View>
        )}
      </ScrollView>
    </LinearGradient>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.md,
    paddingBottom: spacing.sm,
  },
  settingsButton: {
    padding: spacing.sm,
    borderRadius: 20,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
  },
  content: {
    flex: 1,
  },
  contentContainer: {
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing.xl,
  },
  statusContainer: {
    alignItems: 'center',
    marginVertical: spacing.lg,
  },
  statusText: {
    ...typography.body,
    color: '#fff',
    textAlign: 'center',
    opacity: 0.9,
  },
  visualizerContainer: {
    height: 120,
    marginVertical: spacing.lg,
  },
  microphoneContainer: {
    alignItems: 'center',
    marginVertical: spacing.xl,
  },
  microphoneWrapper: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.3,
    shadowRadius: 16,
    elevation: 8,
  },
  microphoneButton: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: 'rgba(255, 255, 255, 0.3)',
  },
  microphoneButtonActive: {
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
    borderColor: '#fff',
  },
  microphoneButtonDisabled: {
    opacity: 0.5,
  },
  messagesContainer: {
    marginTop: spacing.xl,
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    borderRadius: 16,
    padding: spacing.lg,
  },
  messagesTitle: {
    ...typography.h3,
    color: '#fff',
    marginBottom: spacing.md,
  },
  messageBubble: {
    marginBottom: spacing.sm,
  },
  viewAllButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: spacing.md,
    paddingVertical: spacing.sm,
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    borderRadius: 8,
  },
  viewAllText: {
    ...typography.button,
    color: '#6366F1',
    marginRight: spacing.xs,
  },
});

export default HomeScreen;
