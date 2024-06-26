

from joblib import load
import numpy as np
from functionForFeatureExtraction import process_audio_files_clarity, process_audio_files_fluency

models = []
models.append(load('./models/clarity_model.joblib'))
models.append(load('./models/fluency_model.joblib'))

audio_file = './test_files/interview_test8.mp3'
X_test_clarity = process_audio_files_clarity([audio_file])
X_test_clarity = np.array([list(sample.values()) for sample in X_test_clarity])
X_test_fluency = process_audio_files_fluency([audio_file])
X_test_fluency = np.array([list(sample.values()) for sample in X_test_fluency])
y_predicted = []
y_predicted.append(models[0].predict(X_test_clarity)[0])
y_predicted.append(models[1].predict(X_test_fluency)[0])
print("Actual Scores:")
actual_scores = [7,7]
print(actual_scores)
print("Predicted Scores:")
predicted_scores=[y_predicted[0][0],y_predicted[1][1]]
print(predicted_scores)
