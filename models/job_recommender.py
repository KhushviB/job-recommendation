import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os

class JobRecommender:
    def __init__(self):
        """Initialize with education hierarchy and skill matching focus"""
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=100,
            ngram_range=(1, 2)
        )
        self.scaler = StandardScaler()
        
        
        self.model = RandomForestClassifier(
            n_estimators=50,
            max_depth=3,
            min_samples_split=10,
            min_samples_leaf=8,
            max_features='sqrt',
            random_state=42
        )
        

        self.education_hierarchy = {
            'PhD': 5,
            'M.Tech/M.E.': 4,
            'MCA': 3,
            'B.Tech/B.E.': 2,
            'Diploma': 1
        }
        
        
        self.role_education_mapping = {
            'Senior': ['PhD', 'M.Tech/M.E.', 'MCA', 'B.Tech/B.E.'],
            'Mid': ['M.Tech/M.E.', 'MCA', 'B.Tech/B.E.'],
            'Entry': ['B.Tech/B.E.', 'Diploma']
        }


    def prepare_data(self, data_path='../data/job_data.csv'):
        """Prepare data with focus on skill representation"""
        try:
            self.df = pd.read_csv(data_path)
            
            
            self.df['skills_str'] = self.df['required_skills'].apply(
                lambda x: ' '.join(skill.lower() for skill in eval(x))
            )
            
            
            skills_matrix = self.vectorizer.fit_transform(self.df['skills_str'])
            
            
            numerical = self.df['experience_required'].apply(
                lambda x: float(x.split('-')[0])
            ).values.reshape(-1, 1)
            
            scaled_numerical = self.scaler.fit_transform(numerical)
            
            
            self.X = np.hstack((
                skills_matrix.toarray(),
                scaled_numerical
            ))
            
           
            self.y = pd.Categorical(self.df['role_level']).codes
            
            print("\nData preparation completed")
            print(f"Final dataset shape: {self.X.shape}")
            
        except Exception as e:
            print(f"Error in prepare_data: {str(e)}")
            raise

    def train_and_evaluate(self):
        """Train and evaluate the model"""
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                self.X, self.y,
                test_size=0.2,
                stratify=self.y,
                random_state=42
            )
            
            self.model.fit(X_train, y_train)
            
            train_score = self.model.score(X_train, y_train)
            test_score = self.model.score(X_test, y_test)
            
            print("\nModel Performance:")
            print(f"Training Score: {train_score:.4f}")
            print(f"Testing Score: {test_score:.4f}")
            
            y_pred = self.model.predict(X_test)
            print("\nClassification Report:")
            print(classification_report(y_test, y_pred))
            
            return {
                'train_score': train_score,
                'test_score': test_score
            }
            
        except Exception as e:
            print(f"Error in train_and_evaluate: {str(e)}")
            raise

   
    def get_recommendations(self, user_features: dict, num_recommendations: int = 5):
        """Get job recommendations with strict education level matching"""
        try:
            if not hasattr(self, 'df'):
                
                self.prepare_data()

            user_skills = set(skill.lower() for skill in user_features['skills'])
            user_education = user_features['education']
            experience = float(user_features['experience'])
            is_student = user_features.get('is_student', False)
            
            all_recommendations = []
            
            for idx, row in self.df.iterrows():
                
                job_education = row['education_required']

                education_mapping = {
    'phd': ['PhD', 'Doctorate', 'Doctor of Philosophy'],
    'masters': ['Masters', 'M.Tech', 'M.E.', 'MS', 'M.Tech/M.E.', 'M.Sc', 'MCA'],
    'bachelors': ['Bachelors', 'B.Tech', 'B.E.', 'B.Tech/B.E.', 'B.Sc', 'BCA'],
    'diploma': ['Diploma', 'Certificate']
}

                
               
                if job_education != user_education:
                    
                    user_level = None
                    job_level = None
                    
                    for level, variants in education_mapping.items():
                        if any(var.lower() in user_education.lower() for var in variants):
                            user_level = level
                        if any(var.lower() in job_education.lower() for var in variants):
                            job_level = level
                    
                    if user_level != job_level:
                        continue

               
                if user_level == 'phd':
                    phd_keywords = ['research', 'scientist', 'r&d', 'research lead', 
                                'principal researcher', 'senior scientist', 'research head',
                                'chief scientist', 'research director', 'scientific']
                    if not any(keyword in row['job_title'].lower() for keyword in phd_keywords):
                        continue

                
                if user_level == 'masters':
                    masters_keywords = ['data scientist', 'research', 'ml', 'ai', 'senior',
                                    'lead', 'architect', 'specialist', 'analytics',
                                    'machine learning', 'artificial intelligence',
                                    'data analytics', 'algorithm', 'technical lead']
                    if not any(keyword in row['job_title'].lower() for keyword in masters_keywords):
                        continue

                
                if user_level == 'bachelors':
                    exclude_keywords = ['research scientist', 'principal', 'director',
                                    'chief', 'head', 'vp', 'vice president']
                    if any(keyword in row['job_title'].lower() for keyword in exclude_keywords):
                        continue

                
                if user_level == 'diploma':
                    diploma_keywords = ['junior', 'trainee', 'associate', 'assistant',
                                    'support', 'entry level', 'fresher']
                    if not any(keyword in row['job_title'].lower() for keyword in diploma_keywords):
                        continue
                
                
                job_skills = set(skill.lower() for skill in eval(row['required_skills']))
                matching_skills = user_skills & job_skills
                missing_skills = job_skills - user_skills
                skill_match_ratio = len(matching_skills) / len(job_skills) if job_skills else 0
                
                
                if skill_match_ratio < 0.2:
                    continue
                
                
                job_exp = float(row['experience_required'].split('-')[0])
                
                
                if not is_student and abs(experience - job_exp) > 3:
                    continue
                
               
                if is_student and job_exp > 2:
                    continue
                
                
                final_score = skill_match_ratio * 100  
                
                all_recommendations.append({
                    'job_title': row['job_title'],
                    'company': row['company'],
                    'location': row['location'],
                    'matching_skills': list(matching_skills),
                    'missing_skills': list(missing_skills),
                    'education_required': job_education,
                    'experience_required': row['experience_required'],
                    'salary': row['salary'],
                    'match_score': final_score,
                    'skill_match_percentage': skill_match_ratio * 100
                })
            
            
            all_recommendations.sort(key=lambda x: x['match_score'], reverse=True)
            
            if not all_recommendations:
                return []
            
            return all_recommendations[:num_recommendations]
            
        except Exception as e:
            print(f"Error in get_recommendations: {str(e)}")
            return []

    def get_fallback_recommendations(self, user_features: dict):
        """Get fallback recommendations with looser criteria"""
        try:
            user_skills = set(skill.lower() for skill in user_features['skills'])
            user_education = user_features['education']
            is_student = user_features.get('is_student', False)
            
            fallback_recommendations = []
            for idx, row in self.df.iterrows():
               
                if is_student and 'senior' in row['job_title'].lower():
                    continue
                
                job_skills = set(skill.lower() for skill in eval(row['required_skills']))
                matching_skills = user_skills & job_skills
                
                if matching_skills:  
                    fallback_recommendations.append({
                        'job_title': row['job_title'],
                        'company': row['company'],
                        'location': row['location'],
                        'matching_skills': list(matching_skills),
                        'missing_skills': list(job_skills - user_skills),
                        'education_required': row['education_required'],
                        'experience_required': row['experience_required'],
                        'salary': row['salary'],
                        'match_score': len(matching_skills) / len(job_skills),
                        'skill_match_percentage': (len(matching_skills) / len(job_skills)) * 100
                    })
            
            fallback_recommendations.sort(key=lambda x: x['match_score'], reverse=True)
            return fallback_recommendations[:5]
            
        except Exception as e:
            print(f"Error in get_fallback_recommendations: {str(e)}")
            return []

    def save_model(self, path='saved_models/'):
        """Save all model components"""
        try:
            os.makedirs(path, exist_ok=True)
            
            components = {
                'model': self.model,
                'vectorizer': self.vectorizer,
                'scaler': self.scaler,
                'education_hierarchy': self.education_hierarchy,
                'role_education_mapping': self.role_education_mapping
            }
            
            joblib.dump(components, os.path.join(path, 'job_recommender.pkl'))
            print(f"Model saved successfully to {path}")
            
        except Exception as e:
            print(f"Error in save_model: {str(e)}")
            raise

    def load_model(self, path='saved_models/'):
        """Load all model components"""
        try:
            model_path = os.path.join(path, 'job_recommender.pkl')
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"No saved model found at {model_path}")
            
            components = joblib.load(model_path)
            
            self.model = components['model']
            self.vectorizer = components['vectorizer']
            self.scaler = components['scaler']
            self.education_hierarchy = components['education_hierarchy']
            self.role_education_mapping = components['role_education_mapping']
            
            print(f"Model loaded successfully from {path}")
            
        except Exception as e:
            print(f"Error in load_model: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        
        recommender = JobRecommender()
        
        print("Loading and preparing data...")
        recommender.prepare_data()
        
        print("\nTraining and evaluating model...")
        results = recommender.train_and_evaluate()
        
        print("\nSaving the model...")
        recommender.save_model()
        
        test_cases = [
            {
                'name': "PhD Student (Research)",
                'profile': {
                    'skills': ['python', 'machine learning', 'deep learning', 'research', 'neural networks', 'tensorflow'],
                    'experience': '2',
                    'education': 'PhD',
                    'is_student': True,
                    'expected_graduation_year': '2025'
                }
            },
            {
                'name': "B.Tech Final Year",
                'profile': {
                    'skills': ['python', 'java', 'flutter', 'dart', 'react', 'algorithm', 'data structure', 'database', 'machine learning', 'python', 'tensorflow', 'sql', 'flask'],
                    'experience': '0',
                    'education': 'B.Tech/B.E.',
                    'is_student': True,
                    'expected_graduation_year': '2026'
                }
            },
            {
                'name': "M.Tech Student",
                'profile': {
                    'skills': ['python', 'data science', 'machine learning', 'sql', 'statistics'],
                    'experience': '1',
                    'education': 'M.Tech/M.E.',
                    'is_student': True,
                    'expected_graduation_year': '2024'
                }
            }
        ]
        
       
        for test_case in test_cases:
            print(f"\n{'='*80}")
            print(f"Testing recommendations for {test_case['name']}")
            print(f"{'='*80}")
            
            recommendations = recommender.get_recommendations(test_case['profile'])
            
            print("\nUser Profile:")
            print(f"Education: {test_case['profile']['education']}")
            print(f"Expected Graduation: {test_case['profile']['expected_graduation_year']}")
            print(f"Skills: {', '.join(test_case['profile']['skills'])}")
            
            if recommendations:
                print("\nTop Job Recommendations:")
                print("-" * 80)
                for i, rec in enumerate(recommendations, 1):
                    print(f"\n{i}. {rec['job_title']} at {rec['company']}")
                    print(f"Location: {rec['location']}")
                    print(f"Matching Skills: {', '.join(rec['matching_skills'])}")
                    print(f"Skills to Learn: {', '.join(rec['missing_skills'])}")
                    print(f"Experience Required: {rec['experience_required']}")
                    print(f"Education Required: {rec['education_required']}")
                    print(f"Salary: ₹{rec['salary']:,}")
                    print(f"Skill Match: {rec['skill_match_percentage']:.1f}%")
                    print("-" * 80)
            else:
                print("\nNo matching jobs found. Suggestions:")
                print("1. Add more skills to your profile")
                print("2. Check skill spellings and variations")
                print("3. Consider gaining experience in relevant technologies")
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        print("\nFull error traceback:")
        print(traceback.format_exc())