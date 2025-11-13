/**
 * Nexa Mobile - Voice Visualizer Component
 * Visual representation of voice activity with animated waves
 */

import React, { useEffect, useRef } from 'react';
import { View, StyleSheet, Animated, Dimensions } from 'react-native';
import { colors } from '../styles/theme';

const { width } = Dimensions.get('window');

const VoiceVisualizer = ({ isListening, isSpeaking, amplitude = 0.5 }) => {
  const animatedValues = useRef([
    new Animated.Value(0.3),
    new Animated.Value(0.5),
    new Animated.Value(0.8),
    new Animated.Value(0.4),
    new Animated.Value(0.6),
    new Animated.Value(0.7),
    new Animated.Value(0.3),
    new Animated.Value(0.9),
  ]).current;

  const pulseAnimation = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    if (isListening || isSpeaking) {
      startAnimation();
      startPulseAnimation();
    } else {
      stopAnimation();
      stopPulseAnimation();
    }
  }, [isListening, isSpeaking]);

  const startAnimation = () => {
    const animations = animatedValues.map((animatedValue, index) => {
      return Animated.loop(
        Animated.sequence([
          Animated.timing(animatedValue, {
            toValue: Math.random() * 0.8 + 0.2,
            duration: 300 + Math.random() * 200,
            useNativeDriver: false,
          }),
          Animated.timing(animatedValue, {
            toValue: Math.random() * 0.8 + 0.2,
            duration: 300 + Math.random() * 200,
            useNativeDriver: false,
          }),
        ])
      );
    });

    Animated.parallel(animations).start();
  };

  const stopAnimation = () => {
    animatedValues.forEach((animatedValue, index) => {
      Animated.timing(animatedValue, {
        toValue: 0.1,
        duration: 500,
        useNativeDriver: false,
      }).start();
    });
  };

  const startPulseAnimation = () => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnimation, {
          toValue: 1.2,
          duration: 1000,
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnimation, {
          toValue: 1,
          duration: 1000,
          useNativeDriver: true,
        }),
      ])
    ).start();
  };

  const stopPulseAnimation = () => {
    pulseAnimation.stopAnimation();
    Animated.timing(pulseAnimation, {
      toValue: 1,
      duration: 300,
      useNativeDriver: true,
    }).start();
  };

  const getBarColor = () => {
    if (isSpeaking) return colors.secondary[400];
    if (isListening) return colors.primary[400];
    return colors.neutral[400];
  };

  return (
    <View style={styles.container}>
      <Animated.View
        style={[
          styles.visualizer,
          { transform: [{ scale: pulseAnimation }] }
        ]}>
        {animatedValues.map((animatedValue, index) => (
          <Animated.View
            key={index}
            style={[
              styles.bar,
              {
                height: animatedValue.interpolate({
                  inputRange: [0, 1],
                  outputRange: [4, 60],
                }),
                backgroundColor: getBarColor(),
                opacity: animatedValue.interpolate({
                  inputRange: [0, 1],
                  outputRange: [0.3, 1],
                }),
              },
            ]}
          />
        ))}
      </Animated.View>
      
      {/* Circular waves for additional effect */}
      {(isListening || isSpeaking) && (
        <View style={styles.wavesContainer}>
          <CircularWave delay={0} color={getBarColor()} />
          <CircularWave delay={500} color={getBarColor()} />
          <CircularWave delay={1000} color={getBarColor()} />
        </View>
      )}
    </View>
  );
};

const CircularWave = ({ delay, color }) => {
  const scaleAnim = useRef(new Animated.Value(0)).current;
  const opacityAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    const animate = () => {
      Animated.parallel([
        Animated.timing(scaleAnim, {
          toValue: 1,
          duration: 2000,
          useNativeDriver: true,
        }),
        Animated.timing(opacityAnim, {
          toValue: 0,
          duration: 2000,
          useNativeDriver: true,
        }),
      ]).start(() => {
        scaleAnim.setValue(0);
        opacityAnim.setValue(1);
        animate();
      });
    };

    const timer = setTimeout(animate, delay);
    return () => clearTimeout(timer);
  }, [delay]);

  return (
    <Animated.View
      style={[
        styles.wave,
        {
          transform: [{ scale: scaleAnim }],
          opacity: opacityAnim,
          borderColor: color,
        },
      ]}
    />
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    position: 'relative',
  },
  visualizer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    height: 80,
    width: width * 0.6,
  },
  bar: {
    width: 4,
    marginHorizontal: 2,
    borderRadius: 2,
    backgroundColor: colors.primary[400],
  },
  wavesContainer: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'center',
    alignItems: 'center',
  },
  wave: {
    position: 'absolute',
    width: 120,
    height: 120,
    borderRadius: 60,
    borderWidth: 2,
    borderColor: colors.primary[400],
  },
});

export default VoiceVisualizer;
