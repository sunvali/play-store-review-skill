import * as ImagePicker from 'expo-image-picker';

// The only photo feature: a user attaches one picture to a trail note.
export async function attachPhoto() {
  const result = await ImagePicker.launchImageLibraryAsync({ mediaTypes: ['images'] });
  return result.canceled ? null : result.assets[0].uri;
}
