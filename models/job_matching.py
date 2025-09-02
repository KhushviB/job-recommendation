
from resume_analyser import ResumeAnalyzer
from job_recommender import JobRecommender

class JobMatcher:
    def __init__(self):
        self.education_weights = {
            'PHD': 5,
            'M.TECH': 4, 'M.E': 4, 'MBA': 4, 'M.S': 4,
            'B.TECH': 3, 'B.E': 3, 'B.SC': 3
        }

    def _get_user_role_level(self, user_experience):
        """
        Determine the user's role level based on their experience.
        """
        if user_experience <= 2:
            return 'Entry Level'
        elif 2 < user_experience <= 5:
            return 'Mid Level'
        elif 5 < user_experience <= 10:
            return 'Senior Level'
        else:
            return 'Lead Level'

    def match_jobs(self, resume_path, experience):
        """Match candidate with jobs from database"""
        try:
            
            analyzer = ResumeAnalyzer()
            with open(resume_path, 'rb') as file:
                resume_results = analyzer.analyze_resume(file)
            
            if not resume_results:
                return "Could not analyze resume"
            print("Resume Analysis Results:")
            print(f"Education: {resume_results['education']}")
            print(f"Skills: {resume_results['skills']}")
            
            user_features = {
                'skills': resume_results['skills'],
                'education': resume_results['education'],
                'experience': experience, 
            }
            num_of_recommendations = input("How many recommendations you want -> ")
            
            
            recommender = JobRecommender()
            jobs = recommender.get_recommendations(user_features=user_features, num_recommendations=int(num_of_recommendations))
            print(f"Found {len(jobs)} jobs in database")
            
            
            candidate_profile = {
                'education': resume_results['education'],
                'skills': resume_results['skills'],
                'experience': float(experience),  # User input
                'role_level': self._get_user_role_level(float(experience)) 
            }
            
            matches = []
            for job in jobs:
               
                job_requirements = {
                    'education': job.get('required_education', 'B.E'),  
                    'skills': job.get('required_skills', []),
                    'experience': float(job.get('required_experience', 0)),  
                    'role_level': job.get('role_level', 'Entry Level') 
                }
                
                role_levels = ['Entry Level', 'Mid Level', 'Senior Level', 'Lead Level']
                candidate_role_index = role_levels.index(candidate_profile['role_level'])
                job_role_index = role_levels.index(job_requirements['role_level'])

                if abs(candidate_role_index - job_role_index) > 1:
                    continue
                
                score = self._calculate_match_score(candidate_profile, job_requirements)
                if score > 0:  
                    matches.append({
                        'job_id': str(job['_id']),
                        'title': job.get('job_title', 'Unknown Title'),
                        'company': job.get('company', 'Unknown Company'),
                        'location': job.get('location', 'Unknown Location'),
                        'match_score': score,
                        'matching_skills': list(set(candidate_profile['skills']) & set(job_requirements['skills'])),
                        'missing_skills': self._get_missing_skills(candidate_profile['skills'], job_requirements['skills']),
                    })
            
            matches.sort(key=lambda x: x['match_score'], reverse=True)
            print(f"User Experience: {experience} years, Role Level: {candidate_profile['role_level']}")
            print(f"Total Jobs Before Filtering: {len(jobs)}")

            return matches
        except Exception as e:
            print(f"Error in job matching: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return []

    def _calculate_match_score(self, candidate, job):
        """Calculate match score based on requirements"""
        try:
            score = 0
            max_score = 100
            
            
            edu_score = self._calculate_education_score(candidate['education'], job['education'])
            score += edu_score * 0.3
            
           
            skills_score = self._calculate_skills_score(candidate['skills'], job['skills'])
            score += skills_score * 0.4
            
            exp_score = self._calculate_experience_score(candidate['experience'], job['experience'])
            score += exp_score * 0.3
            
            return round(score, 2)

        except Exception as e:
            print(f"Error calculating match score: {str(e)}")
            return 0

    def _calculate_education_score(self, candidate_edu, required_edu):
        """Calculate education match score"""
        try:
            candidate_weight = self.education_weights.get(candidate_edu, 0)
            required_weight = self.education_weights.get(required_edu, 0)
            
            if candidate_weight >= required_weight:
                return 100
            return 0

        except Exception as e:
            print(f"Error calculating education score: {str(e)}")
            return 0

    def _calculate_skills_score(self, candidate_skills, required_skills):
        """Calculate skills match score"""
        try:
            if not required_skills:
                return 100
                
            matched_skills = set(candidate_skills) & set(required_skills)
            return (len(matched_skills) / len(required_skills)) * 100

        except Exception as e:
            print(f"Error calculating skills score: {str(e)}")
            return 0

    def _calculate_experience_score(self, candidate_exp, required_exp):
        """Calculate flexible experience match score"""
        try:
            min_exp, max_exp = required_exp.split('-')
            min_exp, max_exp = float(min_exp), float(max_exp)

            if candidate_exp < min_exp * 0.5:  
                return 0 
            elif candidate_exp > max_exp * 1.5:
                return 50  
            else:
                return round(100 - (abs(candidate_exp - ((min_exp + max_exp) / 2)) / (max_exp - min_exp + 1) * 50), 2)

        except Exception as e:
            print(f"Error calculating experience score: {str(e)}")
            return 0



    def _get_missing_skills(self, candidate_skills, required_skills):
        """Get list of missing required skills"""
        try:
            return list(set(required_skills) - set(candidate_skills))
        except Exception as e:
            print(f"Error getting missing skills: {str(e)}")
            return []
