from app.main import ATS
from app.parser.resume_parser import ResumeParser

if __name__ == "__main__":

    ats = ATS()

    resume_path = input("Enter resume file path: ").strip().strip('"')
    jd_path = input("Enter JD file path: ").strip().strip('"')

    # Parse both resume and JD using parser
    jd_text = ResumeParser.parse(jd_path)

    result = ats.run(resume_path, jd_text)

    print("\n===== ATS RESULT =====")
    for k, v in result.items():
        print(f"{k}: {v}")