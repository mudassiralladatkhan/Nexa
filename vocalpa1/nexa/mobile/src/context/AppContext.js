/**
 * Nexa Mobile - App Context
 * Global state management for the mobile app
 */

import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { StorageService } from '../services/StorageService';

// Initial state
const initialState = {
  // App state
  isListening: false,
  isSpeaking: false,
  isProcessing: false,
  isConnected: false,
  
  // User preferences
  preferences: {
    theme: 'auto',
    wakeWordEnabled: true,
    continuousListening: false,
    voiceFeedback: true,
    speechRate: 1.0,
    language: 'en-US',
    backendUrl: 'http://192.168.1.100:8000', // Default local network IP
  },
  
  // Voice state
  voiceState: {
    isInitialized: false,
    currentCommand: '',
    lastResponse: '',
    confidence: 0,
  },
  
  // Conversation
  conversations: [],
  currentSession: null,
  
  // Backend connection
  backendStatus: {
    connected: false,
    lastCheck: null,
    error: null,
  },
  
  // UI state
  ui: {
    showSettings: false,
    showConversation: false,
    currentScreen: 'Home',
    notifications: [],
  },
};

// Action types
const ActionTypes = {
  // App actions
  SET_LISTENING: 'SET_LISTENING',
  SET_SPEAKING: 'SET_SPEAKING',
  SET_PROCESSING: 'SET_PROCESSING',
  SET_CONNECTED: 'SET_CONNECTED',
  
  // Preferences
  UPDATE_PREFERENCES: 'UPDATE_PREFERENCES',
  LOAD_PREFERENCES: 'LOAD_PREFERENCES',
  
  // Voice actions
  SET_VOICE_STATE: 'SET_VOICE_STATE',
  UPDATE_VOICE_STATE: 'UPDATE_VOICE_STATE',
  
  // Conversation actions
  ADD_MESSAGE: 'ADD_MESSAGE',
  LOAD_CONVERSATIONS: 'LOAD_CONVERSATIONS',
  CLEAR_CONVERSATIONS: 'CLEAR_CONVERSATIONS',
  SET_CURRENT_SESSION: 'SET_CURRENT_SESSION',
  
  // Backend actions
  UPDATE_BACKEND_STATUS: 'UPDATE_BACKEND_STATUS',
  
  // UI actions
  SET_UI_STATE: 'SET_UI_STATE',
  ADD_NOTIFICATION: 'ADD_NOTIFICATION',
  REMOVE_NOTIFICATION: 'REMOVE_NOTIFICATION',
};

// Reducer
const appReducer = (state, action) => {
  switch (action.type) {
    case ActionTypes.SET_LISTENING:
      return {
        ...state,
        isListening: action.payload,
        voiceState: {
          ...state.voiceState,
          currentCommand: action.payload ? '' : state.voiceState.currentCommand,
        },
      };
      
    case ActionTypes.SET_SPEAKING:
      return {
        ...state,
        isSpeaking: action.payload,
      };
      
    case ActionTypes.SET_PROCESSING:
      return {
        ...state,
        isProcessing: action.payload,
      };
      
    case ActionTypes.SET_CONNECTED:
      return {
        ...state,
        isConnected: action.payload,
        backendStatus: {
          ...state.backendStatus,
          connected: action.payload,
          lastCheck: new Date().toISOString(),
          error: action.payload ? null : state.backendStatus.error,
        },
      };
      
    case ActionTypes.UPDATE_PREFERENCES:
      const newPreferences = { ...state.preferences, ...action.payload };
      // Save to storage
      StorageService.setItem('preferences', newPreferences);
      return {
        ...state,
        preferences: newPreferences,
      };
      
    case ActionTypes.LOAD_PREFERENCES:
      return {
        ...state,
        preferences: { ...state.preferences, ...action.payload },
      };
      
    case ActionTypes.SET_VOICE_STATE:
      return {
        ...state,
        voiceState: { ...state.voiceState, ...action.payload },
      };
      
    case ActionTypes.UPDATE_VOICE_STATE:
      return {
        ...state,
        voiceState: { ...state.voiceState, ...action.payload },
      };
      
    case ActionTypes.ADD_MESSAGE:
      const newMessage = {
        id: Date.now().toString(),
        timestamp: new Date().toISOString(),
        ...action.payload,
      };
      
      const updatedConversations = [...state.conversations, newMessage];
      
      // Save to storage
      StorageService.setItem('conversations', updatedConversations);
      
      return {
        ...state,
        conversations: updatedConversations,
      };
      
    case ActionTypes.LOAD_CONVERSATIONS:
      return {
        ...state,
        conversations: action.payload || [],
      };
      
    case ActionTypes.CLEAR_CONVERSATIONS:
      StorageService.removeItem('conversations');
      return {
        ...state,
        conversations: [],
      };
      
    case ActionTypes.SET_CURRENT_SESSION:
      return {
        ...state,
        currentSession: action.payload,
      };
      
    case ActionTypes.UPDATE_BACKEND_STATUS:
      return {
        ...state,
        backendStatus: { ...state.backendStatus, ...action.payload },
      };
      
    case ActionTypes.SET_UI_STATE:
      return {
        ...state,
        ui: { ...state.ui, ...action.payload },
      };
      
    case ActionTypes.ADD_NOTIFICATION:
      return {
        ...state,
        ui: {
          ...state.ui,
          notifications: [...state.ui.notifications, {
            id: Date.now().toString(),
            timestamp: new Date().toISOString(),
            ...action.payload,
          }],
        },
      };
      
    case ActionTypes.REMOVE_NOTIFICATION:
      return {
        ...state,
        ui: {
          ...state.ui,
          notifications: state.ui.notifications.filter(
            notification => notification.id !== action.payload
          ),
        },
      };
      
    default:
      return state;
  }
};

// Context
const AppContext = createContext();

// Provider component
export const AppProvider = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);
  
  useEffect(() => {
    loadInitialData();
  }, []);
  
  const loadInitialData = async () => {
    try {
      // Load preferences
      const preferences = await StorageService.getItem('preferences');
      if (preferences) {
        dispatch({ type: ActionTypes.LOAD_PREFERENCES, payload: preferences });
      }
      
      // Load conversations
      const conversations = await StorageService.getItem('conversations');
      if (conversations) {
        dispatch({ type: ActionTypes.LOAD_CONVERSATIONS, payload: conversations });
      }
    } catch (error) {
      console.error('Failed to load initial data:', error);
    }
  };
  
  // Action creators
  const actions = {
    // App actions
    setListening: (isListening) => 
      dispatch({ type: ActionTypes.SET_LISTENING, payload: isListening }),
      
    setSpeaking: (isSpeaking) => 
      dispatch({ type: ActionTypes.SET_SPEAKING, payload: isSpeaking }),
      
    setProcessing: (isProcessing) => 
      dispatch({ type: ActionTypes.SET_PROCESSING, payload: isProcessing }),
      
    setConnected: (isConnected) => 
      dispatch({ type: ActionTypes.SET_CONNECTED, payload: isConnected }),
    
    // Preferences
    updatePreferences: (preferences) => 
      dispatch({ type: ActionTypes.UPDATE_PREFERENCES, payload: preferences }),
    
    // Voice actions
    setVoiceState: (voiceState) => 
      dispatch({ type: ActionTypes.SET_VOICE_STATE, payload: voiceState }),
      
    updateVoiceState: (updates) => 
      dispatch({ type: ActionTypes.UPDATE_VOICE_STATE, payload: updates }),
    
    // Conversation actions
    addMessage: (message) => 
      dispatch({ type: ActionTypes.ADD_MESSAGE, payload: message }),
      
    clearConversations: () => 
      dispatch({ type: ActionTypes.CLEAR_CONVERSATIONS }),
      
    setCurrentSession: (sessionId) => 
      dispatch({ type: ActionTypes.SET_CURRENT_SESSION, payload: sessionId }),
    
    // Backend actions
    updateBackendStatus: (status) => 
      dispatch({ type: ActionTypes.UPDATE_BACKEND_STATUS, payload: status }),
    
    // UI actions
    setUIState: (uiState) => 
      dispatch({ type: ActionTypes.SET_UI_STATE, payload: uiState }),
      
    addNotification: (notification) => 
      dispatch({ type: ActionTypes.ADD_NOTIFICATION, payload: notification }),
      
    removeNotification: (notificationId) => 
      dispatch({ type: ActionTypes.REMOVE_NOTIFICATION, payload: notificationId }),
  };
  
  const value = {
    state,
    actions,
    dispatch,
  };
  
  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};

// Custom hook to use the context
export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};

export { ActionTypes };
