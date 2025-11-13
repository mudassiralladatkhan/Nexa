/**
 * Nexa Mobile - Conversation Screen
 * Shows conversation history
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  Alert,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { useApp } from '../context/AppContext';
import { StorageService } from '../services/StorageService';
import MessageBubble from '../components/MessageBubble';
import { colors, spacing, typography } from '../styles/theme';

const ConversationScreen = ({ navigation }) => {
  const { state } = useApp();
  const [conversations, setConversations] = useState([]);

  useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    try {
      const saved = await StorageService.getItem('conversations');
      if (saved) {
        setConversations(JSON.parse(saved));
      } else {
        setConversations(state.conversations || []);
      }
    } catch (error) {
      console.error('Error loading conversations:', error);
      setConversations(state.conversations || []);
    }
  };

  const clearConversations = () => {
    Alert.alert(
      'Clear History',
      'Are you sure you want to clear all conversation history?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Clear',
          style: 'destructive',
          onPress: async () => {
            setConversations([]);
            await StorageService.setItem('conversations', JSON.stringify([]));
          },
        },
      ]
    );
  };

  const renderMessage = ({ item }) => (
    <MessageBubble
      message={item.userMessage || item.assistantResponse}
      isUser={!!item.userMessage}
      timestamp={item.timestamp}
    />
  );

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          onPress={() => navigation.goBack()}
          style={styles.backButton}>
          <Icon name="arrow-back" size={24} color={colors.text.primary} />
        </TouchableOpacity>
        <Text style={styles.title}>Conversation History</Text>
        <TouchableOpacity
          onPress={clearConversations}
          style={styles.clearButton}>
          <Icon name="delete-outline" size={24} color={colors.error} />
        </TouchableOpacity>
      </View>

      {conversations.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Icon name="chat-bubble-outline" size={64} color={colors.text.secondary} />
          <Text style={styles.emptyText}>No conversations yet</Text>
          <Text style={styles.emptySubtext}>
            Start talking to Nexa to see your conversation history here
          </Text>
        </View>
      ) : (
        <FlatList
          data={conversations}
          renderItem={renderMessage}
          keyExtractor={(item, index) => `msg-${index}`}
          contentContainerStyle={styles.listContent}
          inverted={false}
        />
      )}
    </View>
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
    justifyContent: 'space-between',
    padding: spacing.md,
    backgroundColor: colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  backButton: {
    padding: spacing.xs,
  },
  title: {
    ...typography.h3,
    flex: 1,
    textAlign: 'center',
    marginHorizontal: spacing.md,
  },
  clearButton: {
    padding: spacing.xs,
  },
  listContent: {
    padding: spacing.md,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: spacing.xl,
  },
  emptyText: {
    ...typography.h3,
    marginTop: spacing.md,
    color: colors.text.primary,
  },
  emptySubtext: {
    ...typography.body,
    marginTop: spacing.sm,
    textAlign: 'center',
    color: colors.text.secondary,
  },
});

export default ConversationScreen;

