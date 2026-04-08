import React, { useEffect, useState } from 'react';
import { Alert, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import * as DocumentPicker from 'expo-document-picker';
import { api, Job } from '../services/api';
import { colors } from '../theme/colors';
import { PrimaryButton } from '../components/PrimaryButton';

export function CandidateScreen({ navigation }: any) {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [resume, setResume] = useState('');
  const [resumeFile, setResumeFile] = useState<DocumentPicker.DocumentPickerAsset | null>(null);
  const [selectedJob, setSelectedJob] = useState<string>('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.listJobs().then(setJobs).catch(() => setJobs([]));
  }, []);

  const pickResumeFile = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: [
          'application/pdf',
          'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
          'application/msword',
          'text/plain',
        ],
        copyToCacheDirectory: true,
        multiple: false,
      });

      if (result.canceled) return;
      const file = result.assets[0];
      setResumeFile(file);
    } catch (e: any) {
      Alert.alert('File Picker Error', e.message || 'Could not pick file.');
    }
  };

  const submit = async () => {
    if (!name || !email) {
      Alert.alert('Missing details', 'Please enter name and email.');
      return;
    }

    if (!resume.trim() && !resumeFile) {
      Alert.alert('Missing resume', 'Please paste resume text or upload a resume file.');
      return;
    }

    setLoading(true);
    try {
      const candidate = await api.createCandidate({
        full_name: name,
        email,
        target_job_id: selectedJob || undefined,
      });
      const analysis = resumeFile
        ? await api.uploadResumeFile(candidate.id, {
            uri: resumeFile.uri,
            name: resumeFile.name,
            type: resumeFile.mimeType ?? undefined,
          })
        : await api.uploadResumeText(candidate.id, resume);
      Alert.alert('Resume analyzed', `Skill match: ${analysis.skill_match_score}%`);
      navigation.navigate('Interview', { candidateId: candidate.id });
    } catch (e: any) {
      Alert.alert('Error', e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.root} contentContainerStyle={styles.container}>
      <LinearGradient colors={['#0B1B40', '#2453C9']} style={styles.hero}>
        <Text style={styles.heroTitle}>Smart Candidate Portal</Text>
        <Text style={styles.heroSub}>Upload resume, get AI score, and start interview.</Text>
      </LinearGradient>

      <View style={styles.card}>
        <Text style={styles.label}>Full Name</Text>
        <TextInput style={styles.input} value={name} onChangeText={setName} placeholder="e.g. John D" />

        <Text style={styles.label}>Email</Text>
        <TextInput style={styles.input} value={email} onChangeText={setEmail} placeholder="name@email.com" />

        <Text style={styles.label}>Target Job ID (optional)</Text>
        <TextInput
          style={styles.input}
          value={selectedJob}
          onChangeText={setSelectedJob}
          placeholder={jobs[0]?.id || 'Create job from backend first'}
        />

        <Text style={styles.label}>Resume Text</Text>
        <TextInput
          style={[styles.input, styles.textArea]}
          value={resume}
          onChangeText={setResume}
          placeholder="Paste your resume content (optional if file uploaded)"
          multiline
        />
        <View style={styles.spacer} />
        <PrimaryButton label="Upload Resume File (PDF/DOC/DOCX/TXT)" onPress={pickResumeFile} />
        {resumeFile ? <Text style={styles.fileName}>Selected: {resumeFile.name}</Text> : null}

        <PrimaryButton label={loading ? 'Submitting...' : 'Analyze & Start Interview'} onPress={submit} disabled={loading} />
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  root: { backgroundColor: colors.bg },
  container: { padding: 16, gap: 14 },
  hero: { borderRadius: 18, padding: 18 },
  heroTitle: { color: '#fff', fontSize: 24, fontWeight: '800' },
  heroSub: { color: '#d9e3ff', marginTop: 6 },
  card: { backgroundColor: colors.card, borderRadius: 16, padding: 16, borderWidth: 1, borderColor: colors.border },
  label: { color: colors.navy, fontWeight: '700', marginTop: 10, marginBottom: 6 },
  input: {
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 10,
    paddingHorizontal: 12,
    paddingVertical: 10,
    backgroundColor: '#fff',
  },
  textArea: { minHeight: 130, textAlignVertical: 'top' },
  spacer: { height: 10 },
  fileName: { marginTop: 8, marginBottom: 8, color: colors.slate, fontWeight: '600' },
});
