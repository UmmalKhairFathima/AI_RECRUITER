import React, { useState } from 'react';
import { Alert, FlatList, StyleSheet, Text, TextInput, View } from 'react-native';
import { api } from '../services/api';
import { colors } from '../theme/colors';
import { PrimaryButton } from '../components/PrimaryButton';

export function InterviewScreen({ route }: any) {
  const candidateId = route.params?.candidateId;
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<any[]>([]);
  const [answer, setAnswer] = useState('');

  const start = async () => {
    try {
      const session = await api.startInterview({ candidate_id: candidateId, mode: 'chat', round_type: 'technical' });
      setSessionId(session.id);
      setMessages(session.transcript);
    } catch (e: any) {
      Alert.alert('Error', e.message);
    }
  };

  const sendAnswer = async () => {
    if (!sessionId || !answer.trim()) return;
    try {
      const updated = await api.submitAnswer(sessionId, answer);
      setMessages(updated.transcript);
      setAnswer('');
    } catch (e: any) {
      Alert.alert('Error', e.message);
    }
  };

  return (
    <View style={styles.root}>
      {!sessionId ? <PrimaryButton label="Start Interview" onPress={start} /> : null}

      <FlatList
        data={messages}
        keyExtractor={(_, i) => i.toString()}
        style={styles.list}
        renderItem={({ item }) => (
          <View style={[styles.bubble, item.role === 'candidate' ? styles.userBubble : styles.aiBubble]}>
            <Text style={[styles.role, item.role === 'candidate' ? styles.userRole : styles.aiRole]}>{item.role.toUpperCase()}</Text>
            <Text style={styles.text}>{item.content}</Text>
          </View>
        )}
      />

      <TextInput
        style={styles.input}
        value={answer}
        onChangeText={setAnswer}
        placeholder="Type your answer"
        multiline
      />
      <PrimaryButton label="Submit Answer" onPress={sendAnswer} disabled={!sessionId} />
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: colors.bg, padding: 14, gap: 10 },
  list: { flex: 1 },
  bubble: { borderRadius: 12, padding: 12, marginVertical: 6, maxWidth: '90%' },
  userBubble: { alignSelf: 'flex-end', backgroundColor: '#d8f6ed' },
  aiBubble: { alignSelf: 'flex-start', backgroundColor: '#e8efff' },
  role: { fontSize: 11, fontWeight: '800', marginBottom: 4 },
  userRole: { color: '#056a52' },
  aiRole: { color: '#1f3f9a' },
  text: { color: colors.navy },
  input: {
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 12,
    padding: 10,
    minHeight: 70,
    textAlignVertical: 'top',
    backgroundColor: '#fff',
  },
});
