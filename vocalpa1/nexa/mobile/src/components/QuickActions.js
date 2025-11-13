/**
 * Nexa Mobile - Quick Actions Component
 * Grid of quick action buttons for common voice commands
 */

import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ScrollView } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { colors, typography, spacing, borderRadius } from '../styles/theme';

const quickActions = [
  {
    id: 'weather',
    icon: 'cloud',
    label: 'Weather',
    color: colors.primary[500],
    command: "What's the weather like?",
  },
  {
    id: 'news',
    icon: 'article',
    label: 'News',
    color: colors.secondary[500],
    command: 'Latest news headlines',
  },
  {
    id: 'music',
    icon: 'music-note',
    label: 'Music',
    color: colors.accent[500],
    command: 'Play some music',
  },
  {
    id: 'time',
    icon: 'schedule',
    label: 'Time',
    color: colors.primary[600],
    command: 'What time is it?',
  },
  {
    id: 'calculator',
    icon: 'calculate',
    label: 'Math',
    color: colors.secondary[600],
    command: 'Open calculator',
  },
  {
    id: 'help',
    icon: 'help',
    label: 'Help',
    color: colors.neutral[600],
    command: 'What can you do?',
  },
];

const QuickActions = ({ onActionPress, style }) => {
  const handleActionPress = (action) => {
    if (onActionPress) {
      onActionPress(action.id);
    }
  };

  return (
    <View style={[styles.container, style]}>
      <Text style={styles.title}>Quick Actions</Text>
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
        style={styles.scrollView}>
        {quickActions.map((action) => (
          <TouchableOpacity
            key={action.id}
            style={[styles.actionButton, { backgroundColor: action.color }]}
            onPress={() => handleActionPress(action)}
            activeOpacity={0.8}>
            <Icon name={action.icon} size={24} color={colors.white} />
            <Text style={styles.actionLabel}>{action.label}</Text>
          </TouchableOpacity>
        ))}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginVertical: spacing.lg,
  },
  title: {
    ...typography.h5,
    color: colors.white,
    marginBottom: spacing.md,
    paddingHorizontal: spacing.sm,
  },
  scrollView: {
    flexGrow: 0,
  },
  scrollContent: {
    paddingHorizontal: spacing.sm,
  },
  actionButton: {
    alignItems: 'center',
    justifyContent: 'center',
    width: 80,
    height: 80,
    borderRadius: borderRadius.xl,
    marginHorizontal: spacing.sm,
    shadowColor: colors.black,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 6,
  },
  actionLabel: {
    ...typography.caption,
    color: colors.white,
    marginTop: spacing.xs,
    textAlign: 'center',
    fontWeight: '600',
  },
});

export default QuickActions;
