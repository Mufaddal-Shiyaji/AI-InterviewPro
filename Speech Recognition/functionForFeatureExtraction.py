import numpy as np
import librosa
from scipy import signal


def preprocess_audio(audio_file_path, target_sr=16000, duration=None):

    try:
        audio_data, sr = librosa.load(audio_file_path, sr=target_sr, duration=duration, mono=True)
        if sr != target_sr:
            audio_data = librosa.resample(audio_data, sr, target_sr)
            sr = target_sr
        
        audio_data /= np.max(np.abs(audio_data))
        
        return audio_data, sr
    except Exception as e:
        print(f"Error loading audio file: {audio_file_path}")
        print(e)
        return None, None



def extract_audio_features(audio_data, sr):
    features = {}
    
    pitches = librosa.piptrack(y=audio_data, sr=sr)
    features['mean_pitch'] = np.mean(pitches)
    features['max_pitch'] = np.max(pitches)
    features['min_pitch'] = np.min(pitches)
    
    features['mean_intensity'] = np.mean(librosa.feature.rms(y=audio_data))
    features['max_intensity'] = np.max(librosa.feature.rms(y=audio_data))
    features['min_intensity'] = np.min(librosa.feature.rms(y=audio_data))

    speech_rate = len(pitches) / librosa.get_duration(y=audio_data, sr=sr)
    features['speech_rate'] = speech_rate

    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio_data, sr=sr))
    zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y=audio_data))
    features['spectral_centroid'] = spectral_centroid
    features['zero_crossing_rate'] = zero_crossing_rate
    features['tempo'] = np.mean(librosa.beat.tempo(y=audio_data, sr=sr))
    features['rolloff'] = np.mean(librosa.feature.spectral_rolloff(y=audio_data, sr=sr))
    features['bandwidth'] = np.mean(librosa.feature.spectral_bandwidth(y=audio_data, sr=sr))
    mfccs = np.mean(librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=13), axis=1)
    chroma = np.mean(librosa.feature.chroma_stft(y=audio_data, sr=sr), axis=1)
    for i, el in enumerate(mfccs):
        features[str(1000+i + 1)] = el
    for j, el in enumerate(chroma):
        features[str(2000+j + 1)] = el
    
    features["disfluency_count"] = identify_disfluency_count(audio_data, sr)
    noise = librosa.util.reduce_noise(audio_data, sr=sr)
    features['snr'] = np.mean(np.power(audio_data, 2) / np.power(noise, 2))
    return features


def extract_audio_features_clarity(audio_data, sr):
    features = {}
    
    pitches = librosa.piptrack(y=audio_data, sr=sr)
    features['mean_pitch'] = np.mean(pitches)
    #features['max_pitch'] = np.max(pitches)
    #features['min_pitch'] = np.min(pitches)
    
    features['mean_intensity'] = np.mean(librosa.feature.rms(y=audio_data))
    #features['max_intensity'] = np.max(librosa.feature.rms(y=audio_data))
    #features['min_intensity'] = np.min(librosa.feature.rms(y=audio_data))

    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio_data, sr=sr))
    zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y=audio_data))
    features['spectral_centroid'] = spectral_centroid
    features['zero_crossing_rate'] = zero_crossing_rate
    #noise = librosa.util.reduce_noise(audio_data, sr=sr)
    #features['snr'] = estimate_snr(audio_data, sr)
    return features


def extract_audio_features_fluency(audio_data, sr):
    features = {}
    
    pitches = librosa.piptrack(y=audio_data, sr=sr)
    speech_rate = len(pitches) / librosa.get_duration(y=audio_data, sr=sr)
    features['speech_rate'] = speech_rate
    #features["disfluency_count"] = identify_disfluency_count(audio_data, sr)
    features["silence_duration"] = identify_silence_duration(audio_data, sr)
    return features


def is_silence(audio_data, threshold):
  rms = np.sqrt(np.mean(audio_data**2))
  return rms < threshold

def identify_silence_duration(audio_data, sr, silence_threshold=0.01):

  frames = signal.find_peaks(-audio_data**2)[0]
  silence_duration = 0
  if len(frames) > 0:
    for i in range(len(frames) - 1):
      start_frame, end_frame = frames[i], frames[i+1]
      silence_time = (end_frame - start_frame) / sr
      if is_silence(audio_data[start_frame:end_frame], silence_threshold):
        silence_duration += silence_time
  return silence_duration


def identify_disfluency_count(audio_data, sr, disfluency_threshold=0.2):
  rms_values = np.lib.stride_tricks.sliding_window_view(audio_data**2, window_shape=(sr//10,))
  rms_diff = np.diff(rms_values, axis=1)
  disfluency_count = 0
  print(rms_diff)
  for diff in rms_diff:
    for i in range(len(diff)):
       if diff[i] > disfluency_threshold:
         disfluency_count += 1
         break
  return disfluency_count


def process_audio_files_clarity(audio_files, target_sr=16000):

    all_features = []
    for audio_file in audio_files:
        audio_data, sr = preprocess_audio(audio_file, target_sr=target_sr)
        features = extract_audio_features_clarity(audio_data, sr)
        all_features.append(features)
    
    return all_features

def process_audio_files_fluency(audio_files, target_sr=16000):

    all_features = []
    for audio_file in audio_files:
        audio_data, sr = preprocess_audio(audio_file, target_sr=target_sr)
        features = extract_audio_features_fluency(audio_data, sr)
        all_features.append(features)
    
    return all_features


