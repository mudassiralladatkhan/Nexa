/**
 * Nexa Mobile - Settings Screen
 * Configure app settings and backend connection
 */

import React, { useState, useContext } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  Switch,
  Alert,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { AppContext } from '../context/AppContext';
import { colors, typography, spacing, borderRadius } from '../styles/theme';
import ApiService from '../services/ApiService';

const SettingsScreen = ({ navigation }) => {
  const { state, dispatch } = useContext(AppContext);
  const [backendUrl, setBackendUrl] = useState(state.settings.backendUrl);
  const [isTestingConnection, setIsTestingConnection] = useState(false);

  const handleSaveSettings = async () => {
    try {
      dispatch({
        type: 'UPDATE_SETTINGS',
        payload: {
          ...state.settings,
          backendUrl: backendUrl,
        },
      });

      Alert.alert('Success', 'Settings saved successfully!');
    } catch (error) {
      Alert.alert('Error', 'Failed to save settings');
    }
  };

  const handleTestConnection = async () => {
    setIsTestingConnection(true);
    try {
      const apiService = new ApiService();
      apiService.setBaseURL(backendUrl);
      
      const result = await apiService.testConnection();
      
      if (result.success) {
        Alert.alert('Success', 'Connected to backend successfully!');
      } else {
        Alert.alert('Connection Failed', result.message || 'Could not connect to backend');
      }
    } catch (error) {
      Alert.alert('Connection Failed', 'Could not connect to backend. Please check the URL and try again.');
    } finally {
      setIsTestingConnection(false);
    }
  };

  const toggleSetting = (key) => {
    dispatch({
      type: 'UPDATE_SETTINGS',
      payload: {
        ...state.settings,
        [key]: !state.settings[key],
      },
    });
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => navigation.goBack()}>
          <Icon name="arrow-back" size={24} color={colors.white} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Settings</Text>
      </View>

      <View style={styles.content}>
        {/* Backend Configuration */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Backend Configuration</Text>
          
          <View style={styles.settingItem}>
            <Text style={styles.settingLabel}>Backend URL</Text>
            <TextInput
              style={styles.textInput}
              value={backendUrl}
              onChangeText={setBackendUrl}
              placeholder="http://192.168.1.100:8000"
              placeholderTextColor={colors.neutral[400]}
              autoCapitalize="none"
              autoCorrect={false}
            />
          </View>

          <TouchableOpacity
            style={[styles.button, isTestingConnection && styles.buttonDisabled]}
            onPress={handleTestConnection}
            disabled={isTestingConnection}>
            <Icon 
              name={isTestingConnection ? "hourglass-empty" : "wifi"} 
              size={20} 
              color={colors.white} 
            />
            <Text style={styles.buttonText}>
              {isTestingConnection ? 'Testing...' : 'Test Connection'}
            </Text>
          </TouchableOpacity>
        </View>

        {/* Voice Settings */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Voice Settings</Text>
          
          <View style={styles.settingItem}>
            <View style={styles.settingRow}>
              <Text style={styles.settingLabel}>Continuous Listening</Text>
              <Switch
                value={state.settings.continuousListening}
                onValueChange={() => toggleSetting('continuousListening')}
                trackColor={{ false: colors.neutral[300], true: colors.primary[400] }}
                thumbColor={colors.white}
              />
            </View>
            <Text style={styles.settingDescription}>
              Keep listening for voice commands without tapping the microphone
            </Text>
          </View>

          <View style={styles.settingItem}>
            <View style={styles.settingRow}>
              <Text style={styles.settingLabel}>Wake Word Detection</Text>
              <Switch
                value={state.settings.wakeWordEnabled}
                onValueChange={() => toggleSetting('wakeWordEnabled')}
                trackColor={{ false: colors.neutral[300], true: colors.primary[400] }}
                thumbColor={colors.white}
              />
            </View>
            <Text style={styles.settingDescription}>
              Respond to "Hey Nexa" or "OK Nexa"
            </Text>
          </View>

          <View style={styles.settingItem}>
            <View style={styles.settingRow}>
              <Text style={styles.settingLabel}>Voice Feedback</Text>
              <Switch
                value={state.settings.voiceFeedback}
                onValueChange={() => toggleSetting('voiceFeedback')}
                trackColor={{ false: colors.neutral[300], true: colors.primary[400] }}
                thumbColor={colors.white}
              />
            </View>
            <Text style={styles.settingDescription}>
              Speak responses aloud using text-to-speech
            </Text>
          </View>
        </View>

        {/* App Settings */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>App Settings</Text>
          
          <View style={styles.settingItem}>
            <View style={styles.settingRow}>
              <Text style={styles.settingLabel}>Dark Mode</Text>
              <Switch
                value={state.settings.darkMode}
                onValueChange={() => toggleSetting('darkMode')}
                trackColor={{ false: colors.neutral[300], true: colors.primary[400] }}
                thumbColor={colors.white}
              />
            </View>
            <Text style={styles.settingDescription}>
              Use dark theme for the app interface
            </Text>
          </View>

          <View style={styles.settingItem}>
            <View style={styles.settingRow}>
              <Text style={styles.settingLabel}>Save Conversations</Text>
              <Switch
                value={state.settings.saveConversations}
                onValueChange={() => toggleSetting('saveConversations')}
                trackColor={{ false: colors.neutral[300], true: colors.primary[400] }}
                thumbColor={colors.white}
              />
            </View>
            <Text style={styles.settingDescription}>
              Keep a history of your conversations with Nexa
            </Text>
          </View>
        </View>

        {/* About Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>About</Text>
          
          <View style={styles.aboutItem}>
            <Text style={styles.aboutLabel}>Version</Text>
            <Text style={styles.aboutValue}>1.0.0</Text>
          </View>
          
          <View style={styles.aboutItem}>
            <Text style={styles.aboutLabel}>Backend Status</Text>
            <View style={styles.statusRow}>
              <View style={[
                styles.statusIndicator,
                { backgroundColor: state.connectionStatus === 'connected' ? colors.success : colors.error }
              ]} />
              <Text style={styles.aboutValue}>
                {state.connectionStatus === 'connected' ? 'Connected' : 'Disconnected'}
              </Text>
            </View>
          </View>
        </View>

        {/* Save Button */}
        <TouchableOpacity style={styles.saveButton} onPress={handleSaveSettings}>
          <Icon name="save" size={20} color={colors.white} />
          <Text style={styles.saveButtonText}>Save Settings</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
    backgroundColor: colors.primary[500],
    paddingTop: spacing.xl,
  },
  backButton: {
    marginRight: spacing.md,
  },
  headerTitle: {
    ...typography.h4,
    color: colors.white,
    fontWeight: '600',
  },
  content: {
    padding: spacing.lg,
  },
  section: {
    marginBottom: spacing.xl,
  },
  sectionTitle: {
    ...typography.h5,
    color: colors.white,
    marginBottom: spacing.md,
    fontWeight: '600',
  },
  settingItem: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    marginBottom: spacing.md,
  },
  settingRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  settingLabel: {
    ...typography.body1,
    color: colors.white,
    fontWeight: '500',
  },
  settingDescription: {
    ...typography.caption,
    color: colors.neutral[400],
    marginTop: spacing.sm,
  },
  textInput: {
    ...typography.body1,
    color: colors.white,
    backgroundColor: colors.neutral[800],
    borderRadius: borderRadius.md,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    marginTop: spacing.sm,
    borderWidth: 1,
    borderColor: colors.neutral[600],
  },
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.secondary[500],
    borderRadius: borderRadius.md,
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.lg,
    marginTop: spacing.md,
  },
  buttonDisabled: {
    backgroundColor: colors.neutral[600],
  },
  buttonText: {
    ...typography.body1,
    color: colors.white,
    fontWeight: '600',
    marginLeft: spacing.sm,
  },
  aboutItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    marginBottom: spacing.sm,
  },
  aboutLabel: {
    ...typography.body1,
    color: colors.white,
    fontWeight: '500',
  },
  aboutValue: {
    ...typography.body1,
    color: colors.neutral[300],
  },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusIndicator: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: spacing.sm,
  },
  saveButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.primary[500],
    borderRadius: borderRadius.lg,
    paddingVertical: spacing.lg,
    marginTop: spacing.lg,
  },
  saveButtonText: {
    ...typography.h6,
    color: colors.white,
    fontWeight: '600',
    marginLeft: spacing.sm,
  },
});

export default SettingsScreen;
