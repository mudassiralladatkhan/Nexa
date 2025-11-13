/**
 * Nexa Mobile - Message Bubble Component
 * Displays conversation messages
 */

import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { colors, spacing, borderRadius } from '../styles/theme';

const MessageBubble = ({ message, isUser, timestamp }) => {
  return (
    <View style={[
      styles.container,
      isUser ? styles.userContainer : styles.assistantContainer
    ]}>
      <Text style={[
        styles.text,
        isUser ? styles.userText : styles.assistantText
      ]}>
        {message}
      </Text>
      {timestamp && (
        <Text style={[
          styles.timestamp,
          isUser ? styles.userTimestamp : styles.assistantTimestamp
        ]}>
          {timestamp}
        </Text>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    maxWidth: '80%',
    padding: spacing.md,
    borderRadius: borderRadius.lg,
    marginVertical: spacing.xs,
  },
  userContainer: {
    alignSelf: 'flex-end',
    backgroundColor: colors.primary,
  },
  assistantContainer: {
    alignSelf: 'flex-start',
    backgroundColor: colors.surface,
  },
  text: {
    fontSize: 14,
    lineHeight: 20,
  },
  userText: {
    color: '#fff',
  },
  assistantText: {
    color: colors.text.primary,
  },
  timestamp: {
    fontSize: 10,
    marginTop: spacing.xs,
    opacity: 0.7,
  },
  userTimestamp: {
    color: '#fff',
    textAlign: 'right',
  },
  assistantTimestamp: {
    color: colors.text.secondary,
    textAlign: 'left',
  },
});

export default MessageBubble;

