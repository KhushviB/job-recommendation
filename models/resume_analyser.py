import spacy
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import docx
import json
import os
from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import datetime


class ResumeAnalyzer:
    def __init__(self):
        # Education levels in hierarchy
        self.education_levels = {
            'phd': ['phd', 'ph.d', 'doctorate', 'doctor of philosophy'],
            'masters': ['masters', 'master', 'mtech', 'ms', 'm.tech', 'm.s', 'mba', 'm.b.a'],
            'bachelors': ['bachelors', 'bachelor', 'btech', 'b.tech', 'be', 'b.e', 'b.sc', 'bsc'],
            'diploma': ['diploma', 'polytechnic'],
            'high school': ['high school', 'hsc', 'xiith', '12th']
        }

        # Skills categories (keeping your existing comprehensive list)
        self.skills_patterns = [
    # Programming Languages
    'python', 'java', 'javascript', 'js', 'typescript', 'c++', 'c#', 'ruby', 'php', 'swift',
    'kotlin', 'rust', 'golang', 'perl', 'r', 'matlab', 'scala', 'html', 'css', 'sql',
    'bash', 'shell scripting', 'objective-c',
    
    # Frameworks & Libraries
    'react', 'angular', 'vue', 'node', 'express', 'django', 'flask', 'spring', 'laravel',
    'asp.net', '.net', 'jquery', 'bootstrap', 'tailwind', 'material-ui', 'redux',
    'tensorflow', 'pytorch', 'keras', 'pandas', 'numpy', 'scikit-learn', 'd3.js',
    'apache hadoop', 'spark', 'apache kafka',
    
    # Databases
    'mysql', 'postgresql', 'mongodb', 'oracle', 'sql server', 'sqlite', 'redis', 
    'elasticsearch', 'dynamodb', 'cassandra', 'neo4j', 'couchbase', 'mariadb', 'firebase',
    
    # Cloud & DevOps
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab',
    'bitbucket', 'ci/cd', 'terraform', 'ansible', 'chef', 'puppet', 'openshift', 'cloudformation',
    'vagrant', 'travis ci', 'circleci',
    
    # Tools & Others
    'jira', 'confluence', 'postman', 'swagger', 'rest api', 'graphql', 'linux', 'unix',
    'agile', 'scrum', 'maven', 'gradle', 'npm', 'yarn', 'webpack', 'figma', 'apache', 'nginx',
    'selenium', 'wireshark',
    
    # Machine Learning & Data Science
    'jupyter notebooks', 'rstudio', 'apache mahout', 'weka', 'rapidminer', 'tableau', 'power bi',
    'sas', 'knime', 'microsoft excel', 'h2o.ai',
    
    # Cybersecurity
    'wireshark', 'metasploit', 'burp suite', 'nessus', 'owasp zap', 'nmap', 'kali linux',
    
    # Networking
    'cisco packet tracer', 'wireshark', 'gns3', 'openvpn',
    
    # Mobile App Development
    'swift', 'objective-c', 'kotlin', 'java', 'react native', 'flutter', 'xamarin',
    
    # Other Technical Skills
    'data structures', 'algorithms', 'operating systems', 'computer networks', 'dbms',
    'object-oriented programming', 'software engineering', 'ai', 'internet of things',
    'blockchain', 'ethical hacking', 'robotics'
]



    def extract_text_from_pdf(self, file):
        """Extract text from PDF file"""
        try:
            import pdfplumber
            
            if isinstance(file, str):  # If file path is provided instead of file object
                with pdfplumber.open(file) as pdf:
                    text = ""
                    for page in pdf.pages:
                        text += page.extract_text() + "\n"
                    return text
            else:  # If file object is provided
                with pdfplumber.open(file) as pdf:
                    text = ""
                    for page in pdf.pages:
                        text += page.extract_text() + "\n"
                    return text
                        
        except Exception as e:
            print(f"Error extracting text from PDF: {str(e)}")
            return None



    def extract_text_from_pdf(self, file):
        """Extract text from PDF file"""
        try:
            import pdfplumber
            text = ""
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {str(e)}")
            return None

    def extract_education(self, text):
        """Extract exact degree name"""
        try:
            text = text.lower()
            
            # Find education section first
            edu_section = None
            edu_headers = ['education', 'educational background', 'academic background', 'qualification']
            
            for header in edu_headers:
                if header in text:
                    start_idx = text.find(header)
                    # Find next section
                    next_sections = ['experience', 'skills', 'projects', 'achievements']
                    end_idx = len(text)
                    for section in next_sections:
                        idx = text.find(section, start_idx)
                        if idx != -1:
                            end_idx = min(end_idx, idx)
                    edu_section = text[start_idx:end_idx]
                    break
            
            search_text = edu_section if edu_section else text
            
            # Exact degree patterns with word boundaries
            degree_patterns = [
                # PhD
                (r'\bph\.?d\b', 'PHD'),
                
                # Masters
                (r'\bm\.?tech\b', 'M.TECH'),
                (r'\bm\.?e\b', 'M.E'),
                (r'\bmba\b', 'MBA'),
                (r'\bm\.?s\b', 'M.S'),
                (r'\bm\.?c\.?a\b', 'MCA'),
                
                # Bachelors
                (r'\bb\.?tech\b', 'B.TECH'),
                (r'\bb\.?e\b', 'B.E'),
                (r'\bb\.?sc\b', 'B.SC'),
                (r'\bb\.?c\.?a\b', 'BCA'),
                (r'\bb\.?com\b', 'B.COM')
            ]
            
            # Check for each degree pattern
            for pattern, degree in degree_patterns:
                if re.search(pattern, search_text):
                    return degree
            
            # If no specific degree found but has engineering
            if 'engineering' in search_text:
                if any(term in search_text for term in ['master', 'masters', 'm.']):
                    return 'M.E'
                return 'B.E'
                
            return 'B.E'  # Default to B.E if no specific degree found

        except Exception as e:
            print(f"Error in education extraction: {str(e)}")
            return 'B.E'
    

    # def _get_education_score(self, level):
    #     """Helper to get education level score"""
    #     scores = {
    #         'phd': 5,
    #         'masters': 4,
    #         'bachelors': 3,
    #         'diploma': 2,
    #         'high school': 1
    #     }
    #     return scores.get(level, 0)


    # def extract_experience(self, text):
    #     """Extract total experience in years"""
    #     try:
    #         text = text.lower()
    #         experience_years = 0
            
    #         # First check for direct mentions of experience
    #         exp_patterns = [
    #             r'(\d+(?:\.\d+)?)\+?\s*years?\s+(?:of\s+)?experience',
    #             r'experience\s*(?:of|:)?\s*(\d+(?:\.\d+)?)\+?\s*years?',
    #             r'worked\s+(?:for\s+)?(\d+(?:\.\d+)?)\+?\s*years?',
    #             r'(\d+(?:\.\d+)?)\+?\s*years?\s+in\s+(?:the\s+)?industry'
    #         ]
            
    #         for pattern in exp_patterns:
    #             matches = re.finditer(pattern, text)
    #             for match in matches:
    #                 try:
    #                     years = float(match.group(1))
    #                     if 0 < years < 30:  # Sanity check
    #                         experience_years = max(experience_years, years)
    #                 except:
    #                     continue

    #         # If no direct mention found, try to calculate from work history
    #         if experience_years == 0:
    #             # Look for date patterns
    #             dates = []
    #             date_patterns = [
    #                 r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*[\s,-]*20\d{2}',
    #                 r'\d{1,2}[-/]20\d{2}',
    #                 r'20\d{2}[-/]\d{1,2}',
    #                 r'\b20\d{2}\b'
    #             ]
                
    #             for pattern in date_patterns:
    #                 matches = re.finditer(pattern, text)
    #                 for match in matches:
    #                     try:
    #                         date_str = match.group()
    #                         # Convert to datetime
    #                         if re.match(r'\b20\d{2}\b', date_str):
    #                             date = datetime.strptime(date_str, '%Y')
    #                         elif '/' in date_str:
    #                             date = datetime.strptime(date_str, '%m/%Y')
    #                         else:
    #                             date = parser.parse(date_str)
    #                         dates.append(date)
    #                     except:
    #                         continue

    #             if dates:
    #                 start_date = min(dates)
    #                 # If 'present' or 'current' found, use current date as end date
    #                 if any(word in text for word in ['present', 'current', 'till date', 'till now']):
    #                     end_date = datetime.now()
    #                 else:
    #                     end_date = max(dates)
                    
    #                 # Calculate years
    #                 experience_years = (end_date - start_date).days / 365.25
                    
    #                 # If experience seems too high, might be education dates
    #                 if experience_years > 10:
    #                     experience_years = 0

    #         # Round to nearest 0.5 and ensure positive
    #         return max(0, round(experience_years * 2) / 2)

    #     except Exception as e:
    #         print(f"Error in experience extraction: {str(e)}")
    #         return 0


    def extract_skills(self, text):
        """Extract skills from resume"""
        try:
            text = text.lower()
            found_skills = []
            
            for skill in self.skills_patterns:
                if re.search(r'\b' + re.escape(skill) + r'\b', text):
                    found_skills.append(skill)
            
            return sorted(list(set(found_skills)))  

        except Exception as e:
            print(f"Error in skills extraction: {str(e)}")
            return []





    # def extract_skills(self, text):
    #     """Extract skills from resume"""
    #     try:
    #         text = text.lower()
    #         found_skills = []
            
    #         # First try to find skills section
    #         skill_headers = ['technical skills', 'skills', 'technologies', 'technical expertise']
    #         skill_section = None
            
    #         for header in skill_headers:
    #             if header in text:
    #                 start_idx = text.find(header)
    #                 # Find next section
    #                 next_sections = ['experience', 'education', 'projects', 'achievements']
    #                 end_idx = len(text)
    #                 for section in next_sections:
    #                     idx = text.find(section, start_idx)
    #                     if idx != -1:
    #                         end_idx = min(end_idx, idx)
    #                 skill_section = text[start_idx:end_idx]
    #                 break
            
    #         # Search in skill section if found, otherwise in whole text
    #         search_text = skill_section if skill_section else text
            
    #         # Look for skills with word boundaries
    #         for skill in self.skills_patterns:
    #             if re.search(r'\b' + re.escape(skill) + r'\b', search_text):
    #                 found_skills.append(skill)
            
    #         return sorted(list(set(found_skills)))  # Remove duplicates and sort

    #     except Exception as e:
    #         print(f"Error in skills extraction: {str(e)}")
    #         return []




    def analyze_resume(self, file):
        """Main method to analyze resume"""
        try:
            text = self.extract_text_from_pdf(file)
            if not text:
                return None

            return {
                'education': self.extract_education(text),
                'skills': self.extract_skills(text)
            }
        except Exception as e:
            print(f"Error in analyze_resume: {str(e)}")
            return None

# if __name__ == "__main__":
#     try:
#         analyzer = ResumeAnalyzer()
#         resume_path = "../KhushviBamrolia.pdf"  # Your resume path
        
#         with open(resume_path, 'rb') as file:
#             results = analyzer.analyze_resume(file)
#             if results:
#                 print("\nAnalysis Results:")
#                 print("-" * 50)
#                 print(f"\nEducation Level: {results['education']}")
#                 print("\nSkills Found:")
#                 if results['skills']:
#                     for skill in results['skills']:
#                         print(f"- {skill}")
#                 else:
#                     print("No skills found")
#             else:
#                 print("Could not analyze resume")

#     except Exception as e:
#         print(f"Error: {str(e)}")


# if __name__ == "__main__":
#     try:
#         analyzer = ResumeAnalyzer()
#         resume_path = "../KhushviBamrolia.pdf"
        
#         with open(resume_path, 'rb') as file:
#             results = analyzer.analyze_resume(file)
#             if results:
#                 print("\nAnalysis Results:")
#                 print("-" * 50)
#                 print(f"\nDegree: {results['education']}")
#                 print("\nSkills Found:")
#                 if results['skills']:
#                     for skill in results['skills']:
#                         print(f"- {skill}")
#                 else:
#                     print("No skills found")
#             else:
#                 print("Could not analyze resume")

#     except Exception as e:
#         print(f"Error: {str(e)}")


