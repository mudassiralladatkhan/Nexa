/**
 * Nexa Mobile - Status Indicator Component
 * Shows connection and voice status
 */

import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { colors } from '../styles/theme';

const StatusIndicator = ({ 
  isConnected, 
  isListening, 
  isProcessing,
  statusText 
}) => {
  const getStatusColor = () => {
    if (isProcessing) return colors.status.processing;
    if (isListening) return colors.status.listening;
    if (isConnected) return colors.status.connected;
    return colors.status.disconnected;
  };

  const getStatusIcon = () => {
    if (isProcessing) return 'sync';
    if (isListening) return 'mic';
    if (isConnected) return 'wifi';
    return 'wifi-off';
  };

  return (
    <View style={[styles.container, { backgroundColor: getStatusColor() }]}>
      <Icon 
        name={getStatusIcon()} 
        size={16} 
        color="#fff" 
        style={styles.icon}
      />
      <Text style={styles.text}>
        {statusText || (isConnected ? 'Connected' : 'Disconnected')}
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
    marginHorizontal: 8,
  },
  icon: {
    marginRight: 4,
  },
  text: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '500',
  },
});

export default StatusIndicator;

