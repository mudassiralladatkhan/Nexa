/**
 * Nexa Mobile - Storage Service
 * Handles local data persistence using AsyncStorage
 */

import AsyncStorage from '@react-native-async-storage/async-storage';

class StorageServiceClass {
  constructor() {
    this.prefix = 'nexa_';
    this.isInitialized = false;
  }

  async initialize() {
    try {
      // Test AsyncStorage availability
      await AsyncStorage.getItem('test');
      this.isInitialized = true;
      console.log('Storage service initialized');
    } catch (error) {
      console.error('Failed to initialize storage service:', error);
      throw error;
    }
  }

  // Basic storage operations
  async setItem(key, value) {
    try {
      const prefixedKey = this.prefix + key;
      const jsonValue = JSON.stringify(value);
      await AsyncStorage.setItem(prefixedKey, jsonValue);
      console.log(`Stored: ${key}`);
    } catch (error) {
      console.error(`Failed to store ${key}:`, error);
      throw error;
    }
  }

  async getItem(key, defaultValue = null) {
    try {
      const prefixedKey = this.prefix + key;
      const jsonValue = await AsyncStorage.getItem(prefixedKey);
      
      if (jsonValue === null) {
        return defaultValue;
      }
      
      return JSON.parse(jsonValue);
    } catch (error) {
      console.error(`Failed to get ${key}:`, error);
      return defaultValue;
    }
  }

  async removeItem(key) {
    try {
      const prefixedKey = this.prefix + key;
      await AsyncStorage.removeItem(prefixedKey);
      console.log(`Removed: ${key}`);
    } catch (error) {
      console.error(`Failed to remove ${key}:`, error);
      throw error;
    }
  }

  async clear() {
    try {
      const keys = await AsyncStorage.getAllKeys();
      const nexaKeys = keys.filter(key => key.startsWith(this.prefix));
      await AsyncStorage.multiRemove(nexaKeys);
      console.log('Cleared all Nexa data');
    } catch (error) {
      console.error('Failed to clear storage:', error);
      throw error;
    }
  }

  // Batch operations
  async multiSet(keyValuePairs) {
    try {
      const prefixedPairs = keyValuePairs.map(([key, value]) => [
        this.prefix + key,
        JSON.stringify(value)
      ]);
      
      await AsyncStorage.multiSet(prefixedPairs);
      console.log('Multi-set completed');
    } catch (error) {
      console.error('Multi-set failed:', error);
      throw error;
    }
  }

  async multiGet(keys) {
    try {
      const prefixedKeys = keys.map(key => this.prefix + key);
      const results = await AsyncStorage.multiGet(prefixedKeys);
      
      const parsed = {};
      results.forEach(([key, value]) => {
        const originalKey = key.replace(this.prefix, '');
        parsed[originalKey] = value ? JSON.parse(value) : null;
      });
      
      return parsed;
    } catch (error) {
      console.error('Multi-get failed:', error);
      throw error;
    }
  }

  // Specific data operations
  async savePreferences(preferences) {
    return this.setItem('preferences', preferences);
  }

  async getPreferences() {
    return this.getItem('preferences', {
      theme: 'auto',
      wakeWordEnabled: true,
      continuousListening: false,
      voiceFeedback: true,
      speechRate: 1.0,
      language: 'en-US',
      backendUrl: 'http://192.168.1.100:8000',
    });
  }

  async saveConversations(conversations) {
    // Keep only the last 100 conversations to prevent storage bloat
    const trimmed = conversations.slice(-100);
    return this.setItem('conversations', trimmed);
  }

  async getConversations() {
    return this.getItem('conversations', []);
  }

  async addConversation(conversation) {
    try {
      const conversations = await this.getConversations();
      conversations.push(conversation);
      await this.saveConversations(conversations);
    } catch (error) {
      console.error('Failed to add conversation:', error);
      throw error;
    }
  }

  async saveUserSession(sessionData) {
    return this.setItem('userSession', sessionData);
  }

  async getUserSession() {
    return this.getItem('userSession', null);
  }

  async clearUserSession() {
    return this.removeItem('userSession');
  }

  // Cache management
  async getCacheItem(key, maxAge = 300000) { // 5 minutes default
    try {
      const cacheKey = `cache_${key}`;
      const cached = await this.getItem(cacheKey);
      
      if (!cached) {
        return null;
      }
      
      const { data, timestamp } = cached;
      const age = Date.now() - timestamp;
      
      if (age > maxAge) {
        await this.removeItem(cacheKey);
        return null;
      }
      
      return data;
    } catch (error) {
      console.error(`Failed to get cache item ${key}:`, error);
      return null;
    }
  }

  async setCacheItem(key, data, maxAge = 300000) {
    try {
      const cacheKey = `cache_${key}`;
      const cacheData = {
        data,
        timestamp: Date.now(),
        maxAge,
      };
      
      await this.setItem(cacheKey, cacheData);
    } catch (error) {
      console.error(`Failed to set cache item ${key}:`, error);
      throw error;
    }
  }

  async clearCache() {
    try {
      const keys = await AsyncStorage.getAllKeys();
      const cacheKeys = keys.filter(key => key.startsWith(this.prefix + 'cache_'));
      await AsyncStorage.multiRemove(cacheKeys);
      console.log('Cache cleared');
    } catch (error) {
      console.error('Failed to clear cache:', error);
      throw error;
    }
  }

  // Storage info
  async getStorageInfo() {
    try {
      const keys = await AsyncStorage.getAllKeys();
      const nexaKeys = keys.filter(key => key.startsWith(this.prefix));
      
      let totalSize = 0;
      const items = {};
      
      for (const key of nexaKeys) {
        const value = await AsyncStorage.getItem(key);
        const size = value ? value.length : 0;
        totalSize += size;
        
        const originalKey = key.replace(this.prefix, '');
        items[originalKey] = {
          size,
          exists: value !== null,
        };
      }
      
      return {
        totalItems: nexaKeys.length,
        totalSize,
        items,
      };
    } catch (error) {
      console.error('Failed to get storage info:', error);
      throw error;
    }
  }

  // Migration helpers
  async migrateData(migrations) {
    try {
      const currentVersion = await this.getItem('dataVersion', 0);
      
      for (const migration of migrations) {
        if (migration.version > currentVersion) {
          console.log(`Running migration ${migration.version}`);
          await migration.migrate(this);
          await this.setItem('dataVersion', migration.version);
        }
      }
    } catch (error) {
      console.error('Data migration failed:', error);
      throw error;
    }
  }

  // Export/Import
  async exportData() {
    try {
      const keys = await AsyncStorage.getAllKeys();
      const nexaKeys = keys.filter(key => key.startsWith(this.prefix));
      const data = await AsyncStorage.multiGet(nexaKeys);
      
      const exportData = {};
      data.forEach(([key, value]) => {
        const originalKey = key.replace(this.prefix, '');
        exportData[originalKey] = value ? JSON.parse(value) : null;
      });
      
      return {
        version: 1,
        timestamp: new Date().toISOString(),
        data: exportData,
      };
    } catch (error) {
      console.error('Failed to export data:', error);
      throw error;
    }
  }

  async importData(importData) {
    try {
      if (!importData.data) {
        throw new Error('Invalid import data format');
      }
      
      const keyValuePairs = Object.entries(importData.data);
      await this.multiSet(keyValuePairs);
      
      console.log('Data imported successfully');
    } catch (error) {
      console.error('Failed to import data:', error);
      throw error;
    }
  }
}

// Export singleton instance
export const StorageService = new StorageServiceClass();
