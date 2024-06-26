import numpy as np
import os
from functionForFeatureExtraction import process_audio_files_clarity, process_audio_files_fluency


audio_dir = './train_files'
audio_files = [os.path.join(audio_dir, file) for file in os.listdir(audio_dir) if file.endswith('.mp3')]
all_extracted_features_clarity = process_audio_files_clarity(audio_files)
all_extracted_features_fluency = process_audio_files_fluency(audio_files)


np.save('./extractedFeatures/all_extracted_features_clarity.npy',np.array(all_extracted_features_clarity))
np.save('./extractedFeatures/all_extracted_features_fluency.npy',np.array(all_extracted_features_fluency))