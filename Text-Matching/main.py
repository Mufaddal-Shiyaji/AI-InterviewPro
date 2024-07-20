import spacy
import numpy as np
from scipy.spatial import distance

nlp = spacy.load("en_core_web_lg")

candidate_answer =  "Regarding your inquiry, I recommend adopting a microservices approach with Docker for containerization and Kubernetes for orchestration, ensuring scalability and fault tolerance. Additionally, incorporating a RESTful API design with Node.js and Express.js facilitates smooth service communication, enhancing development flexibility. Integrating CI/CD pipelines like Jenkins or GitLab CI further streamlines software delivery for swift iterations and top-notch releases."
correct_answer =  "In response to your question, I would propose employing a microservices architecture leveraging containerization with Docker and orchestration through Kubernetes. This setup ensures scalability, fault tolerance, and efficient resource utilization. Additionally, implementing a RESTful API design pattern using technologies like Node.js and Express.js facilitates seamless communication between services, promoting agility and flexibility in development. Furthermore, integrating continuous integration/continuous deployment (CI/CD) pipelines with tools such as Jenkins or GitLab CI streamlines the software delivery process, enabling rapid iterations and ensuring high-quality releases."

def preprocess_text(text):
    doc = nlp(text) 
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
    preprocessed_text = " ".join(tokens)
    return preprocessed_text

print(preprocess_text(correct_answer))
def calculate_sentence_embedding(sentence):
    preprocessed_sentence = preprocess_text(sentence)
    doc = nlp(preprocessed_sentence)
    word_vectors = [token.vector for token in doc if token.has_vector]
    if word_vectors:
        sentence_embedding = np.mean(word_vectors, axis=0)
        return sentence_embedding
    else:
        return np.zeros_like(nlp.vocab.vectors[0]) 



dataset = [
    {"candidate_answer": candidate_answer, 
     "correct_answer": correct_answer,
     "question_type": "technical"},  
]


max_wmd = float('-inf') 
min_wmd = float('inf')   
sum=0
count=0

for data in dataset:
    count=count+1
    candidate_answer = data["candidate_answer"]
    correct_answer = data["correct_answer"]    
    sentence_embedding_candidate = calculate_sentence_embedding(candidate_answer)
    sentence_embedding_correct = calculate_sentence_embedding(correct_answer)
    wmd_distance = distance.euclidean(sentence_embedding_candidate, sentence_embedding_correct)
    max_wmd = max(max_wmd, wmd_distance)
    sum=sum+wmd_distance
    min_wmd = min(min_wmd, wmd_distance)

mean_wmd = sum/len(dataset)
if(dataset[0]["question_type"]=="technical"):
    max_wmd = 30.0
elif(dataset[0]["question_type"]=="objective"):
    max_wmd = 15.0
else :
    max_wmd = 50.0

normalized_wmd = min(mean_wmd / max_wmd, 1.0) 
similarity_score = 1 - normalized_wmd  
accuracy_percentage = similarity_score * 100
print("Accuracy Percentage:", accuracy_percentage)

def calculate_cosineSimilarity(candidate_answer, correct_answer):
    # Process the candidate's answer and the correct answer using Spacy
    doc_candidate = nlp(candidate_answer)
    doc_correct = nlp(correct_answer)
    
    # Calculate Word Mover's Distance (WMD)
    cosine = doc_candidate.similarity(doc_correct)
    
    return cosine
