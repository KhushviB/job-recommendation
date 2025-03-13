# from resume_analyser import ResumeAnalyzer
# from job_recommender import JobRecommender
# import os

# class JobMatchingSystem:
#     def __init__(self):
#         """Initialize the job matching system"""
#         self.resume_analyzer = ResumeAnalyzer()
#         self.job_recommender = JobRecommender()
        
#         # Initialize and train the job recommender
#         print("Loading job dataset and model...")
#         self.job_recommender.prepare_data()
#         self.job_recommender.train_and_evaluate()  
        
#         self.education_weights = {
#             'PHD': 5,
#             'M.TECH': 4, 'M.E': 4, 'MBA': 4, 'M.S': 4,
#             'B.TECH': 3, 'B.E': 3, 'B.SC': 3
#         }# This will train and save the model
    

#     def get_resume_improvements(self, resume_info, job_recommendations):
#         """Generate personalized resume improvement suggestions"""
#         try:
#             improvements = {
#                 'skills_suggestions': [],
#                 'education_suggestions': [],
#                 'experience_suggestions': [],
#                 'general_suggestions': []
#             }

#             # Skills Analysis
#             if job_recommendations:
#                 # Collect all required skills from recommended jobs
#                 required_skills = set()
#                 for job in job_recommendations:
#                     required_skills.update(job.get('missing_skills', []))
                
#                 if required_skills:
#                     improvements['skills_suggestions'].append({
#                         'type': 'missing_skills',
#                         'message': f"Consider learning these in-demand skills: {', '.join(required_skills)}"
#                     })

#             # Education Analysis
#             education_level = resume_info['education']['highest_level']
#             is_student = resume_info['education']['is_current']
            
#             if is_student:
#                 improvements['education_suggestions'].append({
#                     'type': 'current_student',
#                     'message': "Consider adding relevant projects and internships to strengthen your profile"
#                 })
            
#             if education_level.lower() in ['bachelors', 'b.tech', 'b.e.', 'b.tech/b.e.']:
#                 improvements['education_suggestions'].append({
#                     'type': 'higher_education',
#                     'message': "Consider pursuing Masters/higher education to qualify for more senior positions"
#                 })

#             # Experience Analysis
#             experience_years = resume_info['experience']['years']
#             if experience_years < 2:
#                 improvements['experience_suggestions'].append({
#                     'type': 'entry_level',
#                     'message': "Focus on internships and projects to gain practical experience"
#                 })
#             elif 2 <= experience_years < 5:
#                 improvements['experience_suggestions'].append({
#                     'type': 'mid_level',
#                     'message': "Consider taking leadership roles in projects to move towards senior positions"
#                 })

#             # General Suggestions
#             improvements['general_suggestions'] = [
#                 {
#                     'type': 'certifications',
#                     'message': "Add relevant certifications in your field to stand out"
#                 },
#                 {
#                     'type': 'projects',
#                     'message': "Highlight specific projects with measurable outcomes"
#                 },
#                 {
#                     'type': 'keywords',
#                     'message': "Include industry-specific keywords to improve visibility"
#                 }
#             ]

#             return improvements

#         except Exception as e:
#             print(f"Error generating improvements: {str(e)}")
#             return None


#     def match_jobs(self, candidate_profile, jobs):
#         """
#         Match candidate with jobs based on education, skills, and experience
        
#         Args:
#             candidate_profile: {
#                 'education': 'B.TECH',  # From resume analyzer
#                 'skills': ['python', 'react', ...],  # From resume analyzer
#                 'experience': 2.5  # User input
#             }
#             jobs: List of job dictionaries with requirements
#         """
#         try:
#             matches = []
            
#             for job in jobs:
#                 score = self._calculate_match_score(candidate_profile, job)
#                 if score > 0:  # Only include if there's some match
#                     matches.append({
#                         'job_id': job['id'],
#                         'title': job['title'],
#                         'company': job['company'],
#                         'match_score': score,
#                         'missing_skills': self._get_missing_skills(candidate_profile['skills'], job['required_skills'])
#                     })
            
#             # Sort by match score in descending order
#             matches.sort(key=lambda x: x['match_score'], reverse=True)
#             return matches

#         except Exception as e:
#             print(f"Error in job matching: {str(e)}")
#             return []
        
#     def _calculate_match_score(self, candidate, job):
#         """Calculate match score based on requirements"""
#         try:
#             score = 0
#             max_score = 100
            
#             # Education Score (30%)
#             edu_score = self._calculate_education_score(candidate['education'], job['min_education'])
#             score += edu_score * 0.3
            
#             # Skills Score (40%)
#             skills_score = self._calculate_skills_score(candidate['skills'], job['required_skills'])
#             score += skills_score * 0.4
            
#             # Experience Score (30%)
#             exp_score = self._calculate_experience_score(candidate['experience'], job['min_experience'])
#             score += exp_score * 0.3
            
#             return round(score, 2)

#         except Exception as e:
#             print(f"Error calculating match score: {str(e)}")
#             return 0
        
#     def _calculate_education_score(self, candidate_edu, required_edu):
#         """Calculate education match score"""
#         try:
#             candidate_weight = self.education_weights.get(candidate_edu, 0)
#             required_weight = self.education_weights.get(required_edu, 0)
            
#             if candidate_weight >= required_weight:
#                 return 100  # Full score if education meets or exceeds requirement
#             return 0  # No score if education is below requirement

#         except Exception as e:
#             print(f"Error calculating education score: {str(e)}")
#             return 0

#     def _calculate_skills_score(self, candidate_skills, required_skills):
#         """Calculate skills match score"""
#         try:
#             if not required_skills:
#                 return 100
                
#             matched_skills = set(candidate_skills) & set(required_skills)
#             return (len(matched_skills) / len(required_skills)) * 100

#         except Exception as e:
#             print(f"Error calculating skills score: {str(e)}")
#             return 0

#     def _calculate_experience_score(self, candidate_exp, required_exp):
#         """Calculate experience match score"""
#         try:
#             if candidate_exp >= required_exp:
#                 return 100
#             elif candidate_exp >= required_exp * 0.7:  # Allow some flexibility
#                 return 70
#             return 0

#         except Exception as e:
#             print(f"Error calculating experience score: {str(e)}")
#             return 0

#     def _get_missing_skills(self, candidate_skills, required_skills):
#         """Get list of missing required skills"""
#         try:
#             return list(set(required_skills) - set(candidate_skills))
#         except Exception as e:
#             print(f"Error getting missing skills: {str(e)}")
#             return []


# # Usage example
# if __name__ == "__main__":
#     matcher = JobMatchingSystem()
    
#     # Test with a sample resume
#     result = matcher.get_matches("../Pranav_Chaniyara_Resume.pdf")
    
#     if result['success']:
#         print("\nResume Analysis:")
#         print(f"Education: {result['resume_analysis']['education']}")
#         print(f"Experience: {result['resume_analysis']['experience']} years")  # Changed this line
#         print(f"Skills: {', '.join(result['all_skills'])}")
        
#         if result['recommendations']:  # Check if recommendations exist
#             print("\nJob Recommendations:")
#             for i, job in enumerate(result['recommendations'], 1):
#                 print(f"\n{i}. {job['job_title']} at {job['company']}")
#                 print(f"Location: {job['location']}")
#                 print(f"Match Score: {job['match_score']:.2f}")
#                 print(f"Matching Skills: {', '.join(job['matching_skills'])}")
#                 print(f"Skills to Learn: {', '.join(job['missing_skills'])}")
#         else:
#             print("\nNo matching jobs found.")

#         print("\nResume Improvement Suggestions:")
#         improvements = result['improvements']
        
#         print("\nSkills Suggestions:")
#         for suggestion in improvements['skills_suggestions']:
#             print(f"- {suggestion['message']}")
            
#         print("\nEducation Suggestions:")
#         for suggestion in improvements['education_suggestions']:
#             print(f"- {suggestion['message']}")
            
#         print("\nExperience Suggestions:")
#         for suggestion in improvements['experience_suggestions']:
#             print(f"- {suggestion['message']}")
            
#         print("\nGeneral Suggestions:")
#         for suggestion in improvements['general_suggestions']:
#             print(f"- {suggestion['message']}")
#     else:
#         print(f"Error: {result['error']}")



from resume_analyser import ResumeAnalyzer
from job_recommender import JobRecommender

class JobMatcher:
    def __init__(self):
        self.education_weights = {
            'PHD': 5,
            'M.TECH': 4, 'M.E': 4, 'MBA': 4, 'M.S': 4,
            'B.TECH': 3, 'B.E': 3, 'B.SC': 3
        }
        # self.job_recommender = JobRecommender()

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




# def get_job_matches(resume_path, experience):
#         matcher = JobMatcher()
#         matches = matcher.match_jobs(resume_path, experience)
        
#         if matches:
#             print("\nJob Matches:")
#             print("-" * 50)
#             for match in matches:
#                 print(f"\nJob: {match['title']}")
#                 print(f"Company: {match['company']}")
#                 print(f"Match Score: {match['match_score']}%")
#                 if match['missing_skills']:
#                     print("Missing Skills:", ', '.join(match['missing_skills']))
#                 print("-" * 30)
#         else:
#             print("No matching jobs found")


# if __name__ == "__main__":
#     resume_path = "../KhushviBamrolia.pdf"
#     experience = input("Enter your years of experience: ")
#     get_job_matches(resume_path, experience)