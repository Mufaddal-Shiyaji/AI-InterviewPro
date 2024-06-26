import numpy as np
from sklearn.model_selection import KFold
from joblib import dump
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier

#for kfold==5  and 5 discrete output values
sample_target_scores = [
   [7,5],
    [7,7],
    [7,8],
    [8,8],
    [7,6],
    [9,10],
    [10,10],
    [10,10],
    [7,5],
    [8,8],
    [7,5],
    [7,8],
    [5,5],
    [7,8],
    [8,8],
    [7,7],
    [6,6],
    [7,7],
    [6,8],
    [7,7]
]

#for kfold==3  and 3 discrete output values
'''sample_target_scores = [
    [7,7],
    [7,7],
    [7,8],
    [8,7],
    [7,7],
    [9,9],
    [9,7],
    [9,7],
    [7,7],
    [8,8],
    [7,7],
    [7,7],
    [7,7],
    [7,7],
    [8,7],
    [7,7],
    [7,7],
    [7,8],
    [7,8],
    [7,7]
]'''




target_scores = [list(scores) for scores in sample_target_scores]
target_scores = np.array(target_scores)

all_extracted_features_clarity = np.load('./extractedFeatures/all_extracted_features_clarity.npy', allow_pickle=True)
all_extracted_features_fluency = np.load('./extractedFeatures/all_extracted_features_fluency.npy', allow_pickle=True)


models = []
# Define KFold object
kf = KFold(n_splits=5)

# Initialize variables to store the best model and its corresponding accuracy
best_clarity_model = None
best_clarity_accuracy = -1
# Iterate over each fold
for train_index, test_index in kf.split(all_extracted_features_clarity):
    # Split the data for the current fold
    X_train_fold, X_test_fold = all_extracted_features_clarity[train_index], all_extracted_features_clarity[test_index]
    y_train_fold, y_test_fold = target_scores[train_index], target_scores[test_index]
    
    # Train a Clarity model for the current fold
    model = KNeighborsClassifier(n_neighbors=5)
    #model = AdaBoostClassifier(n_estimators=50, random_state=42)

    # Preprocess data (if needed)
    X_train_fold = np.array([list(sample.values()) for sample in X_train_fold])
    X_test_fold = np.array([list(sample.values()) for sample in X_test_fold])
    y_train_fold = np.array(y_train_fold)
    y_test_fold = np.array(y_test_fold)
    #y_train_fold = np.array([item[0] for item in y_train_fold])
    model.fit(X_train_fold, y_train_fold)

    # Make predictions on the test set for the current fold
    y_pred_fold = model.predict(X_test_fold)

    # Calculate accuracy for the current fold
    y_test_fold = [item[0] for item in y_test_fold]
    y_pred_fold = [item[0] for item in y_pred_fold]
    accuracy_fold = accuracy_score(y_test_fold, y_pred_fold)
    #print("y_test_fold:", y_test_fold)
    #print("y_pred_fold:", y_pred_fold)
    #print("Confusion Matrix:", confusion_matrix(y_test_fold, y_pred_fold))

    '''y_test_fold = np.array(y_test_fold)
    y_pred_fold = np.array(y_pred_fold)
    f1_micro = f1_score(y_test_fold, y_pred_fold, average='micro')  # Overall F1-score
    f1_macro = f1_score(y_test_fold, y_pred_fold, average='macro')  # Average F1-score across classes

    print("F1-Score (Micro):", f1_micro)
    print("F1-Score (Macro):", f1_macro)'''


    # Check if the current model has the highest accuracy so far
    if accuracy_fold > best_clarity_accuracy:
        best_clarity_accuracy = accuracy_fold
        best_clarity_model = model


best_fluency_model = None
best_fluency_accuracy = -1
models.append(best_clarity_model)

# Iterate over each fold
for train_index, test_index in kf.split(all_extracted_features_fluency):
    
    X_train_fold, X_test_fold = all_extracted_features_fluency[train_index], all_extracted_features_fluency[test_index]
    y_train_fold, y_test_fold = target_scores[train_index], target_scores[test_index]

    # Train a Fluency model for the current fold
    model = KNeighborsClassifier(n_neighbors=5)
    #model = AdaBoostClassifier(n_estimators=50, random_state=42)
    X_train_fold = np.array([list(sample.values()) for sample in X_train_fold])
    X_test_fold = np.array([list(sample.values()) for sample in X_test_fold])
    y_train_fold = np.array(y_train_fold)
    y_test_fold = np.array(y_test_fold)
    #y_train_fold = np.array([item[1] for item in y_train_fold])
    model.fit(X_train_fold, y_train_fold)

    # Make predictions on the test set for the current fold
    y_pred_fold = model.predict(X_test_fold)

    # Calculate accuracy for the current fold

    y_test_fold = [item[1] for item in y_test_fold]
    y_pred_fold = [item[1] for item in y_pred_fold]
    accuracy_fold = accuracy_score(y_test_fold, y_pred_fold)
    #print("y_test_fold:", y_test_fold)
    #print("y_pred_fold:", y_pred_fold)
    #print("Confusion Matrix:", confusion_matrix(y_test_fold, y_pred_fold))
    '''y_test_fold = np.array(y_test_fold)
    y_pred_fold = np.array(y_pred_fold)
    f1_micro = f1_score(y_test_fold, y_pred_fold, average='micro')  # Overall F1-score
    f1_macro = f1_score(y_test_fold, y_pred_fold, average='macro')  # Average F1-score across classes

    print("F1-Score (Micro):", f1_micro)
    print("F1-Score (Macro):", f1_macro)'''


    # Check if the current model has the highest accuracy so far
    if accuracy_fold > best_fluency_accuracy:
        best_fluency_accuracy = accuracy_fold
        best_fluency_model = model

# Save the best Fluency model to the models array
models.append(best_fluency_model)

print("Clarity Model Accuracy:", best_clarity_accuracy)
print("Fluency Model Accuracy:", best_fluency_accuracy)

dump(models[0], './models/clarity_model.joblib')
dump(models[1], './models/fluency_model.joblib')







