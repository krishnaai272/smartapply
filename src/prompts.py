from langchain.prompts import PromptTemplate

# Prompt to rewrite a resume for a specific job description
RESUME_REWRITE_PROMPT = PromptTemplate.from_template(
    """
    Act as an expert career coach and professional resume writer specializing in the tech industry.
    Your task is to rewrite the following resume to be perfectly tailored for the target job description.

    **Instructions:**
    1.  **Analyze the Job Description:** Identify the key skills, technologies, qualifications, and action verbs.
    2.  **Mirror Language:** Integrate the keywords and phrases from the job description naturally into the resume.
    3.  **Quantify Achievements:** Where possible, rephrase bullet points to be result-oriented and include metrics (e.g., "Increased efficiency by 20%," "Managed a team of 5"). If the original resume lacks numbers, use your expertise to suggest realistic, impactful phrasing.
    4.  **Action Verbs:** Start each bullet point with a strong, dynamic action verb relevant to the role.
    5.  **Structure and Format:** Maintain the original resume's structure (e.g., Summary, Experience, Skills, Projects, Education). Do not add or remove sections.
    6.  **Clarity and Conciseness:** Ensure the final output is professional, clear, and concise.

    **Original Resume:**
    ---
    {resume_text}
    ---

    **Target Job Description:**
    ---
    {job_description}
    ---

    **Output:**
    Return ONLY the full text of the rewritten, ATS-friendly resume. Do not add any commentary or explanations before or after the resume content.
    """
)

# Prompt to generate a compelling cover letter
COVER_LETTER_PROMPT = PromptTemplate.from_template(
    """
    Act as an expert career coach and professional writer. Your task is to craft a compelling, professional, and concise cover letter.

    **Candidate's Tailored Resume:**
    ---
    {tailored_resume}
    ---

    **Target Job Description:**
    ---
    {job_description}
    ---

    **Optional User Notes for Personalization:**
    ---
    {user_notes}
    ---

    **Instructions:**
    1.  **Hook:** Start with a strong opening that grabs the reader's attention and states the position being applied for.
    2.  **Connect:** In the body (1-2 paragraphs), connect the candidate's key qualifications and achievements from their resume directly to the most important requirements in the job description. Highlight 2-3 specific, powerful examples.
    3.  **Personalize:** Seamlessly integrate the user's personal notes to add a unique touch or explain specific circumstances (e.g., career gap, passion for the company's mission). If no notes are provided, focus solely on the resume and job description.
    4.  **Call to Action:** End with a confident closing and a clear call to action (e.g., "I am eager to discuss how my skills in [Key Skill] can contribute to your team's success.").
    5.  **Tone:** Maintain a professional, enthusiastic, and confident tone throughout.

    **Output:**
    Return ONLY the full text of the cover letter. Do not include a subject line or any commentary.
    """
)

# Prompt for scoring the resume against the job description
SCORING_PROMPT = PromptTemplate.from_template(
    """
    Act as a sophisticated Applicant Tracking System (ATS) and a senior HR manager.
    Your task is to analyze the provided resume against the job description and provide a detailed evaluation.

    **Resume:**
    ---
    {resume_text}
    ---

    **Job Description:**
    ---
    {job_description}
    ---

    **Evaluation Criteria:**
    1.  **Keyword Alignment:** How well do the keywords in the resume (skills, technologies, responsibilities) match the job description?
    2.  **Experience Relevance:** Is the candidate's work experience directly relevant to the role's requirements?
    3.  **Qualification Match:** Does the candidate meet the core qualifications (e.g., years of experience, specific degrees, certifications)?
    4.  **Impact and Results:** Does the resume demonstrate quantifiable achievements and impact?

    **Output Format:**
    Provide your analysis in a structured format. First, give a compatibility score from 1 to 100. Then, provide a concise summary of the key optimizations performed or needed.

    **Example Output:**
    **Score:** 87
    **Analysis:** Enhanced technical skills section, aligned experience with job requirements, improved keyword density for ATS compatibility.

    **Your Turn:**
    Provide the Score and Analysis for the given documents.
    """
)