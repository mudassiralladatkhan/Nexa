/**
 * Nexa Mobile - Theme Configuration
 * Colors, typography, spacing, and other design tokens
 */

// Color palette
export const colors = {
  // Primary colors
  primary: {
    50: '#EEF2FF',
    100: '#E0E7FF',
    200: '#C7D2FE',
    300: '#A5B4FC',
    400: '#818CF8',
    500: '#6366F1', // Main primary
    600: '#4F46E5',
    700: '#4338CA',
    800: '#3730A3',
    900: '#312E81',
  },
  
  // Secondary colors
  secondary: {
    50: '#ECFDF5',
    100: '#D1FAE5',
    200: '#A7F3D0',
    300: '#6EE7B7',
    400: '#34D399',
    500: '#10B981', // Main secondary
    600: '#059669',
    700: '#047857',
    800: '#065F46',
    900: '#064E3B',
  },
  
  // Accent colors
  accent: {
    50: '#FFFBEB',
    100: '#FEF3C7',
    200: '#FDE68A',
    300: '#FCD34D',
    400: '#FBBF24',
    500: '#F59E0B', // Main accent
    600: '#D97706',
    700: '#B45309',
    800: '#92400E',
    900: '#78350F',
  },
  
  // Error colors
  error: {
    50: '#FEF2F2',
    100: '#FEE2E2',
    200: '#FECACA',
    300: '#FCA5A5',
    400: '#F87171',
    500: '#EF4444', // Main error
    600: '#DC2626',
    700: '#B91C1C',
    800: '#991B1B',
    900: '#7F1D1D',
  },
  
  // Warning colors
  warning: {
    50: '#FFFBEB',
    100: '#FEF3C7',
    200: '#FDE68A',
    300: '#FCD34D',
    400: '#FBBF24',
    500: '#F59E0B', // Main warning
    600: '#D97706',
    700: '#B45309',
    800: '#92400E',
    900: '#78350F',
  },
  
  // Success colors
  success: {
    50: '#ECFDF5',
    100: '#D1FAE5',
    200: '#A7F3D0',
    300: '#6EE7B7',
    400: '#34D399',
    500: '#10B981', // Main success
    600: '#059669',
    700: '#047857',
    800: '#065F46',
    900: '#064E3B',
  },
  
  // Neutral colors (light theme)
  neutral: {
    50: '#F8FAFC',
    100: '#F1F5F9',
    200: '#E2E8F0',
    300: '#CBD5E1',
    400: '#94A3B8',
    500: '#64748B',
    600: '#475569',
    700: '#334155',
    800: '#1E293B',
    900: '#0F172A',
  },
  
  // Dark theme colors
  dark: {
    50: '#0F172A',
    100: '#1E293B',
    200: '#334155',
    300: '#475569',
    400: '#64748B',
    500: '#94A3B8',
    600: '#CBD5E1',
    700: '#E2E8F0',
    800: '#F1F5F9',
    900: '#F8FAFC',
  },
  
  // Semantic colors
  white: '#FFFFFF',
  black: '#000000',
  transparent: 'transparent',
  
  // Gradients
  gradients: {
    primary: ['#6366F1', '#8B5CF6', '#A855F7'],
    secondary: ['#10B981', '#34D399', '#6EE7B7'],
    accent: ['#F59E0B', '#FBBF24', '#FCD34D'],
    dark: ['#0F172A', '#1E293B', '#334155'],
  },
};

// Typography
export const typography = {
  // Font families
  fontFamily: {
    regular: 'Inter-Regular',
    medium: 'Inter-Medium',
    semiBold: 'Inter-SemiBold',
    bold: 'Inter-Bold',
  },
  
  // Font sizes
  fontSize: {
    xs: 12,
    sm: 14,
    base: 16,
    lg: 18,
    xl: 20,
    '2xl': 24,
    '3xl': 30,
    '4xl': 36,
    '5xl': 48,
  },
  
  // Line heights
  lineHeight: {
    tight: 1.2,
    normal: 1.5,
    relaxed: 1.75,
  },
  
  // Font weights
  fontWeight: {
    normal: '400',
    medium: '500',
    semiBold: '600',
    bold: '700',
  },
  
  // Text styles
  h1: {
    fontSize: 36,
    fontWeight: '700',
    lineHeight: 1.2,
    color: colors.neutral[900],
  },
  
  h2: {
    fontSize: 30,
    fontWeight: '700',
    lineHeight: 1.2,
    color: colors.neutral[900],
  },
  
  h3: {
    fontSize: 24,
    fontWeight: '600',
    lineHeight: 1.3,
    color: colors.neutral[900],
  },
  
  h4: {
    fontSize: 20,
    fontWeight: '600',
    lineHeight: 1.3,
    color: colors.neutral[900],
  },
  
  h5: {
    fontSize: 18,
    fontWeight: '600',
    lineHeight: 1.4,
    color: colors.neutral[900],
  },
  
  h6: {
    fontSize: 16,
    fontWeight: '600',
    lineHeight: 1.4,
    color: colors.neutral[900],
  },
  
  body: {
    fontSize: 16,
    fontWeight: '400',
    lineHeight: 1.5,
    color: colors.neutral[700],
  },
  
  bodySmall: {
    fontSize: 14,
    fontWeight: '400',
    lineHeight: 1.5,
    color: colors.neutral[600],
  },
  
  caption: {
    fontSize: 12,
    fontWeight: '400',
    lineHeight: 1.4,
    color: colors.neutral[500],
  },
  
  button: {
    fontSize: 16,
    fontWeight: '600',
    lineHeight: 1.2,
  },
  
  label: {
    fontSize: 14,
    fontWeight: '500',
    lineHeight: 1.4,
    color: colors.neutral[700],
  },
};

// Spacing
export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  '2xl': 48,
  '3xl': 64,
  '4xl': 96,
};

// Border radius
export const borderRadius = {
  none: 0,
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  '2xl': 24,
  full: 9999,
};

// Shadows
export const shadows = {
  sm: {
    shadowColor: colors.black,
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
  
  md: {
    shadowColor: colors.black,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 6,
    elevation: 3,
  },
  
  lg: {
    shadowColor: colors.black,
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.15,
    shadowRadius: 15,
    elevation: 6,
  },
  
  xl: {
    shadowColor: colors.black,
    shadowOffset: { width: 0, height: 20 },
    shadowOpacity: 0.25,
    shadowRadius: 25,
    elevation: 10,
  },
};

// Animation durations
export const animations = {
  fast: 150,
  normal: 250,
  slow: 350,
  slower: 500,
};

// Breakpoints (for responsive design)
export const breakpoints = {
  sm: 576,
  md: 768,
  lg: 992,
  xl: 1200,
};

// Component-specific themes
export const components = {
  button: {
    primary: {
      backgroundColor: colors.primary[500],
      color: colors.white,
      borderRadius: borderRadius.md,
      paddingVertical: spacing.md,
      paddingHorizontal: spacing.lg,
    },
    
    secondary: {
      backgroundColor: colors.secondary[500],
      color: colors.white,
      borderRadius: borderRadius.md,
      paddingVertical: spacing.md,
      paddingHorizontal: spacing.lg,
    },
    
    outline: {
      backgroundColor: colors.transparent,
      color: colors.primary[500],
      borderWidth: 1,
      borderColor: colors.primary[500],
      borderRadius: borderRadius.md,
      paddingVertical: spacing.md,
      paddingHorizontal: spacing.lg,
    },
    
    ghost: {
      backgroundColor: colors.transparent,
      color: colors.primary[500],
      borderRadius: borderRadius.md,
      paddingVertical: spacing.md,
      paddingHorizontal: spacing.lg,
    },
  },
  
  card: {
    default: {
      backgroundColor: colors.white,
      borderRadius: borderRadius.lg,
      padding: spacing.lg,
      ...shadows.md,
    },
    
    elevated: {
      backgroundColor: colors.white,
      borderRadius: borderRadius.lg,
      padding: spacing.lg,
      ...shadows.lg,
    },
  },
  
  input: {
    default: {
      backgroundColor: colors.white,
      borderWidth: 1,
      borderColor: colors.neutral[300],
      borderRadius: borderRadius.md,
      paddingVertical: spacing.md,
      paddingHorizontal: spacing.md,
      fontSize: typography.fontSize.base,
      color: colors.neutral[900],
    },
    
    focused: {
      borderColor: colors.primary[500],
      ...shadows.sm,
    },
    
    error: {
      borderColor: colors.error[500],
    },
  },
};

// Dark theme overrides
export const darkTheme = {
  colors: {
    ...colors,
    // Override neutral colors for dark theme
    neutral: colors.dark,
    
    // Background colors
    background: {
      primary: colors.dark[50],
      secondary: colors.dark[100],
      tertiary: colors.dark[200],
    },
    
    // Text colors
    text: {
      primary: colors.dark[900],
      secondary: colors.dark[800],
      tertiary: colors.dark[700],
      inverse: colors.neutral[900],
    },
    
    // Border colors
    border: {
      primary: colors.dark[300],
      secondary: colors.dark[200],
    },
  },
  
  typography: {
    ...typography,
    // Override text colors for dark theme
    h1: { ...typography.h1, color: colors.dark[900] },
    h2: { ...typography.h2, color: colors.dark[900] },
    h3: { ...typography.h3, color: colors.dark[900] },
    h4: { ...typography.h4, color: colors.dark[900] },
    h5: { ...typography.h5, color: colors.dark[900] },
    h6: { ...typography.h6, color: colors.dark[900] },
    body: { ...typography.body, color: colors.dark[800] },
    bodySmall: { ...typography.bodySmall, color: colors.dark[700] },
    caption: { ...typography.caption, color: colors.dark[600] },
    label: { ...typography.label, color: colors.dark[800] },
  },
  
  components: {
    ...components,
    card: {
      default: {
        ...components.card.default,
        backgroundColor: colors.dark[100],
      },
      elevated: {
        ...components.card.elevated,
        backgroundColor: colors.dark[100],
      },
    },
    
    input: {
      default: {
        ...components.input.default,
        backgroundColor: colors.dark[100],
        borderColor: colors.dark[300],
        color: colors.dark[900],
      },
      focused: {
        ...components.input.focused,
      },
      error: {
        ...components.input.error,
      },
    },
  },
};

// Theme context values
export const lightTheme = {
  colors,
  typography,
  spacing,
  borderRadius,
  shadows,
  animations,
  breakpoints,
  components,
};

// App-specific color mappings (after colors object is defined)
colors.background = colors.neutral[50];
colors.surface = colors.white;
colors.text = {
  primary: colors.neutral[900],
  secondary: colors.neutral[600],
  tertiary: colors.neutral[500],
  inverse: colors.white,
};
colors.border = colors.neutral[300];
colors.status = {
  connected: colors.success[500],
  disconnected: colors.error[500],
  listening: colors.primary[500],
  processing: colors.accent[500],
};

// Export default theme (light)
export default lightTheme;
