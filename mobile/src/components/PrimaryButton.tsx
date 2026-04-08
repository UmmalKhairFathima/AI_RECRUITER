import React from 'react';
import { Pressable, StyleSheet, Text } from 'react-native';
import { colors } from '../theme/colors';

type Props = {
  label: string;
  onPress: () => void;
  disabled?: boolean;
};

export function PrimaryButton({ label, onPress, disabled = false }: Props) {
  return (
    <Pressable style={[styles.btn, disabled && styles.disabled]} onPress={onPress} disabled={disabled}>
      <Text style={styles.label}>{label}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  btn: {
    backgroundColor: colors.navy,
    borderRadius: 12,
    paddingVertical: 12,
    alignItems: 'center',
  },
  disabled: {
    opacity: 0.5,
  },
  label: {
    color: '#fff',
    fontWeight: '700',
    fontSize: 15,
  },
});
