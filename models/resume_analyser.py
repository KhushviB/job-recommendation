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
        self.education_levels = {
            'phd': ['phd', 'ph.d', 'doctorate', 'doctor of philosophy'],
            'masters': ['masters', 'master', 'mtech', 'ms', 'm.tech', 'm.s', 'mba', 'm.b.a'],
            'bachelors': ['bachelors', 'bachelor', 'btech', 'b.tech', 'be', 'b.e', 'b.sc', 'bsc'],
            'diploma': ['diploma', 'polytechnic'],
            'high school': ['high school', 'hsc', 'xiith', '12th']
        }

        self.skills_patterns = [
    'python', 'java', 'javascript', 'js', 'typescript', 'c++', 'c#', 'ruby', 'php', 'swift',
    'kotlin', 'rust', 'golang', 'perl', 'r', 'matlab', 'scala', 'html', 'css', 'sql',
    'bash', 'shell scripting', 'objective-c',
    
    'react', 'angular', 'vue', 'node', 'express', 'django', 'flask', 'spring', 'laravel',
    'asp.net', '.net', 'jquery', 'bootstrap', 'tailwind', 'material-ui', 'redux',
    'tensorflow', 'pytorch', 'keras', 'pandas', 'numpy', 'scikit-learn', 'd3.js',
    'apache hadoop', 'spark', 'apache kafka',
    
  
    'mysql', 'postgresql', 'mongodb', 'oracle', 'sql server', 'sqlite', 'redis', 
    'elasticsearch', 'dynamodb', 'cassandra', 'neo4j', 'couchbase', 'mariadb', 'firebase',

    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab',
    'bitbucket', 'ci/cd', 'terraform', 'ansible', 'chef', 'puppet', 'openshift', 'cloudformation',
    'vagrant', 'travis ci', 'circleci',
   
    'jira', 'confluence', 'postman', 'swagger', 'rest api', 'graphql', 'linux', 'unix',
    'agile', 'scrum', 'maven', 'gradle', 'npm', 'yarn', 'webpack', 'figma', 'apache', 'nginx',
    'selenium', 'wireshark',
    
    'jupyter notebooks', 'rstudio', 'apache mahout', 'weka', 'rapidminer', 'tableau', 'power bi',
    'sas', 'knime', 'microsoft excel', 'h2o.ai',
    
    'wireshark', 'metasploit', 'burp suite', 'nessus', 'owasp zap', 'nmap', 'kali linux',
    
    'cisco packet tracer', 'wireshark', 'gns3', 'openvpn',
    
    'swift', 'objective-c', 'kotlin', 'java', 'react native', 'flutter', 'xamarin',
    
    'data structures', 'algorithms', 'operating systems', 'computer networks', 'dbms',
    'object-oriented programming', 'software engineering', 'ai', 'internet of things',
    'blockchain', 'ethical hacking', 'robotics'
]



    def extract_text_from_pdf(self, file):
        """Extract text from PDF file"""
        try:
            import pdfplumber
            
            if isinstance(file, str):  
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
            
            edu_section = None
            edu_headers = ['education', 'educational background', 'academic background', 'qualification']
            
            for header in edu_headers:
                if header in text:
                    start_idx = text.find(header)
                    next_sections = ['experience', 'skills', 'projects', 'achievements']
                    end_idx = len(text)
                    for section in next_sections:
                        idx = text.find(section, start_idx)
                        if idx != -1:
                            end_idx = min(end_idx, idx)
                    edu_section = text[start_idx:end_idx]
                    break
            
            search_text = edu_section if edu_section else text
            
            degree_patterns = [
                
                (r'\bph\.?d\b', 'PHD'),
                
                (r'\bm\.?tech\b', 'M.TECH'),
                (r'\bm\.?e\b', 'M.E'),
                (r'\bmba\b', 'MBA'),
                (r'\bm\.?s\b', 'M.S'),
                (r'\bm\.?c\.?a\b', 'MCA'),
                
                (r'\bb\.?tech\b', 'B.TECH'),
                (r'\bb\.?e\b', 'B.E'),
                (r'\bb\.?sc\b', 'B.SC'),
                (r'\bb\.?c\.?a\b', 'BCA'),
                (r'\bb\.?com\b', 'B.COM')
            ]
            
            for pattern, degree in degree_patterns:
                if re.search(pattern, search_text):
                    return degree
            
            if 'engineering' in search_text:
                if any(term in search_text for term in ['master', 'masters', 'm.']):
                    return 'M.E'
                return 'B.E'
                
            return 'B.E' 

        except Exception as e:
            print(f"Error in education extraction: {str(e)}")
            return 'B.E'
    

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
