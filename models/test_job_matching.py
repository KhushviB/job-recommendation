from job_matching import JobMatcher

def test_matching():
    try:
        resume_path = "../resumes/Pranav_Chaniyara_Resume.pdf"  # Update with correct path
        experience = input("Enter your years of experience: ")
        
        matcher = JobMatcher()
        matches = matcher.match_jobs(resume_path, float(experience))
        
        if matches:
            print("\nJob Matches:")
            print("-" * 50)
            for match in matches:
                print(f"\nJob: {match['title']}")
                print(f"Company: {match['company']}")
                print(f"Location: {match['location']}")
                print(f"Matching Skills: {', '.join(match['matching_skills'])}")
                print(f"Skills to Learn: {', '.join(match['missing_skills'])}")
        else:
            print("No matching jobs found")

    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    test_matching()