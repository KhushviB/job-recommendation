import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class JobDataGenerator:
    def __init__(self):
        # Define core skill categories
        self.skill_categories = {
        'Programming Languages': [
            'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Ruby', 'PHP',
            'Swift', 'Kotlin', 'Go', 'Rust', 'Scala', 'R', 'MATLAB', 'Perl', 'Haskell',
            'Lua', 'Dart', 'Julia', 'Groovy', 'COBOL', 'Fortran', 'Assembly', 'VHDL',
            'Prolog', 'Erlang', 'Elixir', 'F#', 'Clojure', 'Shell', 'PowerShell'
        ],
        'Web Development': [
            'HTML', 'CSS', 'React', 'Angular', 'Vue.js', 'Node.js', 'Django', 'Flask',
            'Spring Boot', 'ASP.NET', 'Express.js', 'Laravel', 'Bootstrap', 'jQuery',
            'REST API', 'GraphQL', 'WebSocket', 'Next.js', 'Nuxt.js', 'Gatsby',
            'Svelte', 'Tailwind CSS', 'SASS/SCSS', 'Redux', 'Material-UI', 'FastAPI',
            'NestJS', 'Ruby on Rails', 'PHP Laravel', 'WordPress', 'Web Components'
        ],
        'Database': [
            'MySQL', 'PostgreSQL', 'MongoDB', 'SQL Server', 'Oracle', 'Redis',
            'Cassandra', 'Firebase', 'ElasticSearch', 'DynamoDB', 'Neo4j', 'GraphQL',
            'MariaDB', 'SQLite', 'CouchDB', 'Amazon RDS', 'Snowflake', 'Supabase',
            'PlanetScale', 'CockroachDB', 'TimescaleDB', 'InfluxDB'
        ],
        'Cloud & DevOps': [
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'Git', 'Linux',
            'CI/CD', 'Terraform', 'Ansible', 'Prometheus', 'Grafana', 'ELK Stack',
            'GitHub Actions', 'GitLab CI', 'Bitbucket Pipelines', 'CircleCI',
            'ArgoCD', 'Helm', 'Istio', 'Serverless', 'CloudFormation', 'Pulumi'
        ],
        'Data Science & AI': [
            'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Scikit-learn',
            'NLP', 'Computer Vision', 'Data Analysis', 'Statistical Analysis', 'Big Data',
            'Hadoop', 'Spark', 'Keras', 'NLTK', 'spaCy', 'Pandas', 'NumPy', 'SciPy',
            'MLflow', 'Kubeflow', 'Hugging Face', 'BERT', 'GPT', 'Transformers',
            'XGBoost', 'LightGBM', 'Tableau', 'Power BI', 'Data Visualization'
        ],
        'Mobile Development': [
            'Android', 'iOS', 'React Native', 'Flutter', 'Xamarin', 'Mobile App Development',
            'SwiftUI', 'Kotlin Android', 'Jetpack Compose', 'Android Studio', 'Xcode',
            'App Store', 'Google Play', 'Firebase', 'Mobile CI/CD', 'Fastlane',
            'Ionic', 'Capacitor', 'Progressive Web Apps', 'Mobile Testing'
        ],
        'Security': [
            'Cybersecurity', 'Penetration Testing', 'Ethical Hacking', 'Security Auditing',
            'OWASP', 'OAuth', 'JWT', 'SSL/TLS', 'Encryption', 'Security Protocols',
            'Vulnerability Assessment', 'Security Tools', 'Network Security'
        ],
        'Blockchain': [
            'Smart Contracts', 'Ethereum', 'Solidity', 'Web3.js', 'Blockchain Development',
            'DeFi', 'NFT', 'Cryptocurrency', 'Hyperledger', 'Truffle', 'Hardhat'
        ]
    }

        # Define job roles with experience levels
        # Define job roles with experience levels
        self.job_roles = {
    'Entry Level': [
        'Junior Software Engineer', 'Graduate Engineer Trainee',
        'Junior Developer', 'Software Development Trainee',
        'Associate Software Engineer', 'Junior Data Analyst',
        'Junior Web Developer', 'Junior Mobile Developer',
        'Junior DevOps Engineer', 'Junior ML Engineer',
        'Frontend Developer Trainee', 'Backend Developer Trainee',
        'Cloud Engineer Trainee', 'IT Support Engineer',
        'QA Engineer Trainee'
    ],
    'Mid Level': [
        'Software Engineer', 'Full Stack Developer', 'Data Scientist',
        'DevOps Engineer', 'Backend Developer', 'Frontend Developer',
        'Mobile App Developer', 'System Engineer', 'Cloud Engineer',
        'ML Engineer', 'Product Engineer', 'Security Engineer',
        'Database Administrator', 'Site Reliability Engineer',
        'Quality Assurance Engineer', 'Automation Engineer',
        'Technical Lead', 'Scrum Master'
    ],
    'Senior Level': [
        'Senior Software Engineer', 'Tech Lead', 'Senior Data Scientist',
        'Senior DevOps Engineer', 'Software Architect', 'Team Lead',
        'Engineering Manager', 'Principal Engineer', 'Senior Cloud Architect',
        'Director of Engineering', 'VP of Engineering', 'CTO',
        'Chief Architect', 'Senior Product Manager', 'Senior Technical Lead',
        'Solutions Architect', 'Enterprise Architect'
    ],
    'Lead Level': [  # Added Lead Level
        'Lead Software Engineer', 'Lead Data Scientist', 'Lead DevOps Engineer',
        'Lead Cloud Architect', 'Lead Security Engineer', 'Lead Product Manager',
        'Lead Solutions Architect', 'Lead Machine Learning Engineer',
        'Lead Full Stack Developer', 'Lead Backend Developer',
        'Lead Frontend Developer', 'Lead Mobile Developer',
        'Lead Automation Engineer', 'Lead QA Engineer', 'Lead Scrum Master'
    ]
}

        # Define companies and locations
        self.companies = [
    # Tech Giants
    'Google', 'Microsoft', 'Amazon', 'Apple', 'Meta', 'Netflix', 'Adobe',
    
    # Indian IT Services
    'TCS', 'Infosys', 'Wipro', 'HCL', 'Tech Mahindra', 'Cognizant', 'Accenture',
    
    # Indian Startups & Unicorns
    'Flipkart', 'Swiggy', 'Zomato', 'BYJU\'S', 'Paytm', 'PhonePe', 'Razorpay',
    'Zerodha', 'Ola', 'Uber', 'Dunzo', 'Meesho', 'CRED', 'Unacademy', 'Dream11',
    'Freshworks', 'InMobi', 'Curefit', 'UrbanClap', 'BigBasket', 'Lenskart',
    
    # Product Companies
    'Oracle', 'SAP', 'IBM', 'Intel', 'AMD', 'Nvidia', 'Qualcomm', 'VMware',
    'Salesforce', 'ServiceNow', 'Atlassian', 'Zoom', 'Slack', 'Twitter',
    
    # Consulting Firms (Big 4)
    'Deloitte', 'PwC', 'EY', 'KPMG', 'McKinsey', 'Boston Consulting Group',
    
    # Banks & Fintech
    'JPMorgan Chase', 'Goldman Sachs', 'Morgan Stanley', 'Deutsche Bank',
    'American Express', 'Mastercard', 'Visa', 'PayPal', 'HDFC Bank', 'ICICI Bank',
    'Axis Bank', 'SBI', 'Kotak Mahindra Bank', 'Yes Bank'
]

        self.locations = [
    # Major Tech Hubs
    'Bangalore', 'Hyderabad', 'Mumbai', 'Pune', 'Delhi NCR', 'Chennai',
    
    # Growing Tech Cities
    'Kolkata', 'Ahmedabad', 'Indore', 'Coimbatore', 'Kochi', 'Chandigarh',
    'Jaipur', 'Bhubaneswar', 'Vizag', 'Nagpur', 'Lucknow', 'Thiruvananthapuram',
    
    # Additional Cities
    'Gurgaon', 'Noida', 'Faridabad', 'Ghaziabad', 'Greater Noida', 'Mysore',
    'Vadodara', 'Surat', 'Rajkot', 'Jamshedpur', 'Ranchi', 'Patna',
    'Guwahati', 'Dehradun', 'Amritsar', 'Ludhiana', 'Jodhpur', 'Udaipur',
    'Trichy', 'Madurai', 'Coimbatore', 'Vellore', 'Salem', 'Tiruppur'
]

        # Define education requirements
        self.education_levels = [
        'Diploma', 'B.Tech/B.E.', 'M.Tech/M.E.', 'MCA', 'BCA', 'BSc CS/IT',
        'MSc CS/IT', 'PhD', 'B.Sc', 'M.Sc', 'BCA', 'MBA'
    ]

    def generate_skills(self, role_level):
        """Generate relevant skills based on role level"""
        try:
            num_skills = {
                'Entry Level': (4, 6),
                'Mid Level': (6, 8),
                'Senior Level': (8, 12),
                'Lead Level': (10, 15)  # Added Lead Level
            }
            min_skills, max_skills = num_skills[role_level]
            skills = []
            
            # Get all skills from all categories
            all_skills = []
            for category in self.skill_categories.values():
                all_skills.extend(category)
            
            # Select random number of skills based on role level
            num_skills_to_select = random.randint(min_skills, max_skills)
            skills = random.sample(all_skills, num_skills_to_select)
            
            return list(set(skills))  # Remove any duplicates
        except Exception as e:
            print(f"Error generating skills: {str(e)}")
            return []

    def generate_salary(self, role_level, education):
        """Generate realistic salary ranges based on role level and education"""
        base_ranges = {
            'Entry Level': {
                'Diploma': (300000, 500000),
                'B.Tech/B.E.': (400000, 700000),
                'M.Tech/M.E.': (500000, 800000),
                'MCA': (450000, 750000),
                'BCA': (350000, 600000),
                'BSc CS/IT': (350000, 600000),
                'MSc CS/IT': (450000, 750000),
                'PhD': (800000, 1200000),
                'B.Sc': (300000, 500000),
                'M.Sc': (400000, 700000),
                'MBA': (500000, 800000)
            },
            'Mid Level': {
                'Diploma': (500000, 800000),
                'B.Tech/B.E.': (800000, 1500000),
                'M.Tech/M.E.': (1000000, 1800000),
                'MCA': (900000, 1600000),
                'BCA': (700000, 1300000),
                'BSc CS/IT': (700000, 1300000),
                'MSc CS/IT': (900000, 1600000),
                'PhD': (1500000, 2500000),
                'B.Sc': (600000, 1000000),
                'M.Sc': (800000, 1500000),
                'MBA': (1000000, 2000000)
            },
            'Senior Level': {
                'Diploma': (800000, 1500000),
                'B.Tech/B.E.': (1500000, 3000000),
                'M.Tech/M.E.': (1800000, 3500000),
                'MCA': (1600000, 3200000),
                'BCA': (1200000, 2500000),
                'BSc CS/IT': (1200000, 2500000),
                'MSc CS/IT': (1600000, 3200000),
                'PhD': (2500000, 5000000),
                'B.Sc': (1000000, 2000000),
                'M.Sc': (1400000, 2800000),
                'MBA': (2000000, 4000000)
            },
            'Lead Level': {
                'Diploma': (1000000, 1800000),
                'B.Tech/B.E.': (2000000, 3000000),
                'M.Tech/M.E.': (2800000, 5000000),
                'MCA': (3000000, 4200000),
                'BCA': (2300000, 4000000),
                'BSc CS/IT': (2500000, 3800000),
                'MSc CS/IT': (3300000, 5000000),
                'PhD': (4000000, 8000000),
                'B.Sc': (2000000, 4500000),
                'M.Sc': (3400000, 4800000),
                'MBA': (3500000, 6000000)
            }
        }
        
        try:
            min_salary, max_salary = base_ranges[role_level][education]
            return random.randint(min_salary, max_salary)
        except KeyError:
            # Fallback salary ranges if education level not found
            fallback_ranges = {
                'Entry Level': (300000, 700000),
                'Mid Level': (700000, 1500000),
                'Senior Level': (1500000, 3000000)
            }
            min_salary, max_salary = fallback_ranges[role_level]
            return random.randint(min_salary, max_salary)

    def generate_experience_requirement(self, role_level):
        """Generate experience requirements based on role level"""
        ranges = {
            'Entry Level': (0, 2),
            'Mid Level': (2, 4),
            'Senior Level': (4, 7),
            'Lead Level': (7, 18)
        }
        min_exp, max_exp = ranges[role_level]
        return f"{min_exp}-{max_exp} years"

    def generate_dataset(self, num_records=30000):
        """Generate the complete dataset"""
        data = []

        for _ in range(num_records):
            # Select role level and specific role
            role_level = random.choice(list(self.job_roles.keys()))
            role = random.choice(self.job_roles[role_level])

            # Select education requirement
            education = random.choice(self.education_levels)

            # Generate other fields
            job_record = {
                'job_title': role,
                'company': random.choice(self.companies),
                'location': random.choice(self.locations),
                'role_level': role_level,
                'required_skills': self.generate_skills(role_level),
                'education_required': education,
                'experience_required': self.generate_experience_requirement(role_level),
                'salary': self.generate_salary(role_level, education),
                'posting_date': (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d')
            }
            data.append(job_record)

        # Convert to DataFrame and save
        df = pd.DataFrame(data)
        df.to_csv('job_data.csv', index=False)
        return df


# if __name__ == "__main__":
#     generator = JobDataGenerator()
#     df = generator.generate_dataset()
#     print(f"Generated dataset with {len(df)} records")
#     print("\nSample records:")
#     print(df.head())
#     print("\nDataset statistics:")
#     print(df['experience_required'].value_counts())
