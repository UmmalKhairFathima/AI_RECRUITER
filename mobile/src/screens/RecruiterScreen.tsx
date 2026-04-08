import React, { useCallback, useState } from 'react';
import { FlatList, RefreshControl, StyleSheet, Text, View } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { api, Ranking } from '../services/api';
import { colors } from '../theme/colors';

export function RecruiterScreen() {
  const [rows, setRows] = useState<Ranking[]>([]);
  const [refreshing, setRefreshing] = useState(false);

  const load = async () => {
    setRefreshing(true);
    try {
      setRows(await api.getRanking());
    } finally {
      setRefreshing(false);
    }
  };

  useFocusEffect(
    useCallback(() => {
      load();
    }, [])
  );

  return (
    <View style={styles.root}>
      <Text style={styles.title}>Recruiter Dashboard</Text>
      <FlatList
        data={rows}
        keyExtractor={(item) => item.candidate_id}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={load} />}
        renderItem={({ item, index }) => (
          <View style={styles.card}>
            <Text style={styles.rank}>#{index + 1}</Text>
            <Text style={styles.name}>{item.name}</Text>
            <Text style={styles.email}>{item.email}</Text>
            <View style={styles.row}>
              <Text style={styles.score}>Score: {item.final_score}</Text>
              <Text style={[styles.badge, item.recommendation === 'Hire' ? styles.hire : styles.reject]}>{item.recommendation}</Text>
            </View>
          </View>
        )}
        ListEmptyComponent={<Text style={styles.empty}>No candidates yet.</Text>}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, padding: 16, backgroundColor: colors.bg },
  title: { fontSize: 24, fontWeight: '800', color: colors.navy, marginBottom: 12 },
  card: {
    borderRadius: 16,
    borderWidth: 1,
    borderColor: colors.border,
    backgroundColor: '#fff',
    padding: 14,
    marginBottom: 10,
  },
  rank: { color: colors.sky, fontWeight: '800' },
  name: { color: colors.navy, fontWeight: '700', marginTop: 2 },
  email: { color: colors.slate, marginTop: 2 },
  row: { marginTop: 8, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  score: { color: colors.navy, fontWeight: '700' },
  badge: { fontWeight: '700', paddingHorizontal: 10, paddingVertical: 4, borderRadius: 8, overflow: 'hidden' },
  hire: { backgroundColor: '#d4f7e4', color: '#047548' },
  reject: { backgroundColor: '#fde5ea', color: colors.danger },
  empty: { color: colors.slate, textAlign: 'center', marginTop: 50 },
});
