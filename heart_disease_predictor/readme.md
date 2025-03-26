<h1>Heart Disease Prediction Model</h1>

<p>This project develops a machine learning model to predict heart disease risk using a K-Nearest Neighbors (KNN) classifier. The model analyzes various patient health indicators to determine the likelihood of heart disease.</p>

<p>This project uses a Kaggle dataset (https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction?select=heart.csv)</p>

Features include:

1. Age: age of the patient [years]
2. Sex: sex of the patient [M: Male, F: Female]
3. ChestPainType: chest pain type [TA: Typical Angina, ATA: Atypical Angina, NAP: Non-Anginal Pain, ASY: Asymptomatic]
4. RestingBP: resting blood pressure [mm Hg]
5. Cholesterol: serum cholesterol [mm/dl]
6. FastingBS: fasting blood sugar [1: if FastingBS > 120 mg/dl, 0: otherwise]
7. RestingECG: resting electrocardiogram results [Normal: Normal, ST: having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV), LVH: showing probable or definite left ventricular hypertrophy by Estes' criteria]
8. MaxHR: maximum heart rate achieved [Numeric value between 60 and 202]
9. ExerciseAngina: exercise-induced angina [Y: Yes, N: No]
10. Oldpeak: oldpeak = ST [Numeric value measured in depression]
11. ST_Slope: the slope of the peak exercise ST segment [Up: upsloping, Flat: flat, Down: downsloping]
12. HeartDisease: output class [1: heart disease, 0: Normal]

- <h3>Limitations:</h3>
- Dataset is heavily skewed towards male patients
- Potential bias due to imbalanced representation of sexes
- Model performance may not generalize perfectly to all populations

- Acknowledgements: I am a beginner who is still learning data analytics and machine learning. Therefore, this project was inspired by codes provided in tutorials and other github repositories.
