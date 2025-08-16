import PyPDF2
import docx
import re
from typing import Dict, List, Any
import io

class ResumeProcessor:
    """
    Process resume files and extract skills and experience information
    """
    
    def __init__(self):
        self.skill_keywords = [
            # Programming Languages
            'python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin',
            'typescript', 'scala', 'r', 'matlab', 'perl', 'bash', 'powershell',
            
            # Frameworks & Libraries
            'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'express', 'spring', 'laravel',
            'asp.net', 'rails', 'fastapi', 'tornado', 'bootstrap', 'tailwind', 'material-ui',
            'jquery', 'axios', 'lodash', 'moment', 'chart.js', 'd3.js',
            
            # Databases
            'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle', 'sql server', 'mariadb',
            'elasticsearch', 'cassandra', 'dynamodb', 'firebase',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab', 'github actions',
            'terraform', 'ansible', 'nginx', 'apache', 'linux', 'ubuntu', 'centos',
            
            # Data Science & ML
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn',
            'jupyter', 'spark', 'hadoop', 'kafka', 'airflow', 'tableau', 'power bi',
            
            # Tools & Platforms
            'git', 'svn', 'jira', 'confluence', 'slack', 'teams', 'zoom', 'figma', 'sketch',
            'postman', 'swagger', 'graphql', 'rest api', 'soap', 'microservices',
            
            # Soft Skills
            'leadership', 'communication', 'teamwork', 'problem solving', 'project management',
            'agile', 'scrum', 'kanban', 'lean', 'six sigma', 'customer service', 'mentoring'
        ]
        
        self.experience_patterns = [
            r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?experience',
            r'experience:\s*(\d+)\s*(?:years?|yrs?)',
            r'(\d+)\s*(?:years?|yrs?)\s*in\s*(?:the\s*)?field',
            r'worked\s*(?:for\s*)?(\d+)\s*(?:years?|yrs?)',
        ]

    def process_resume(self, resume_file) -> Dict[str, Any]:
        """
        Process resume file and extract skills and experience
        
        Args:
            resume_file: Uploaded resume file
            
        Returns:
            Dict containing extracted skills and experience
        """
        try:
            # Extract text from resume
            text = self._extract_text(resume_file)
            
            # Extract skills and experience
            skills = self._extract_skills(text)
            experience = self._extract_experience(text)
            
            return {
                'skills': skills,
                'experience': experience,
                'text_length': len(text)
            }
            
        except Exception as e:
            raise Exception(f"Failed to process resume: {str(e)}")

    def _extract_text(self, resume_file) -> str:
        """Extract text from different file formats"""
        file_name = resume_file.name.lower()
        
        if file_name.endswith('.pdf'):
            return self._extract_from_pdf(resume_file)
        elif file_name.endswith(('.doc', '.docx')):
            return self._extract_from_docx(resume_file)
        else:
            raise Exception("Unsupported file format. Please upload PDF or DOC/DOCX files.")

    def _extract_from_pdf(self, pdf_file) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.lower()
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")

    def _extract_from_docx(self, docx_file) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(docx_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.lower()
        except Exception as e:
            raise Exception(f"Failed to extract text from DOCX: {str(e)}")

    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        found_skills = []
        
        # Look for skill keywords in text
        for skill in self.skill_keywords:
            if skill in text:
                found_skills.append(skill.title())
        
        # Remove duplicates and sort
        found_skills = list(set(found_skills))
        found_skills.sort()
        
        return found_skills

    def _extract_experience(self, text: str) -> Dict[str, Any]:
        """Extract experience information from resume text"""
        experience_info = {
            'total_years': 0,
            'experience_level': 'entry',
            'found_patterns': []
        }
        
        # Look for experience patterns
        for pattern in self.experience_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                years = max([int(match) for match in matches])
                experience_info['total_years'] = years
                experience_info['found_patterns'].append(f"Found {years} years of experience")
                
                # Determine experience level
                if years >= 10:
                    experience_info['experience_level'] = 'expert'
                elif years >= 6:
                    experience_info['experience_level'] = 'senior'
                elif years >= 3:
                    experience_info['experience_level'] = 'mid'
                else:
                    experience_info['experience_level'] = 'entry'
                break
        
        return experience_info

    def get_skill_categories(self) -> Dict[str, List[str]]:
        """Get categorized skills for better organization"""
        return {
            'programming_languages': [
                'python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin',
                'typescript', 'scala', 'r', 'matlab', 'perl', 'bash', 'powershell'
            ],
            'frameworks_libraries': [
                'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'express', 'spring', 'laravel',
                'asp.net', 'rails', 'fastapi', 'tornado', 'bootstrap', 'tailwind', 'material-ui'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle', 'sql server', 'mariadb',
                'elasticsearch', 'cassandra', 'dynamodb', 'firebase'
            ],
            'cloud_devops': [
                'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab', 'github actions',
                'terraform', 'ansible', 'nginx', 'apache', 'linux', 'ubuntu', 'centos'
            ],
            'data_science_ml': [
                'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn',
                'jupyter', 'spark', 'hadoop', 'kafka', 'airflow', 'tableau', 'power bi'
            ],
            'soft_skills': [
                'leadership', 'communication', 'teamwork', 'problem solving', 'project management',
                'agile', 'scrum', 'kanban', 'lean', 'six sigma', 'customer service', 'mentoring'
            ]
        }
