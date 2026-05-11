"""LangChain LLM chains for CareerCopilot AI."""

import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.utils import get_env
from src.config import MODEL_NAME


def get_llm(temperature: float = 0.3):
    """Get configured LLM (Groq or OpenAI)."""
    provider = get_env("LLM_PROVIDER", "groq").lower()
    groq_key = get_env("GROQ_API_KEY")
    openai_key = get_env("OPENAI_API_KEY")

    if provider == "groq" and groq_key:
        from langchain_groq import ChatGroq
        model = get_env("GROQ_MODEL", MODEL_NAME)
        return ChatGroq(
            groq_api_key=groq_key,
            model_name=model,
            temperature=temperature,
        )

    if openai_key:
        from langchain_openai import ChatOpenAI
        model = get_env("OPENAI_MODEL", "gpt-4o-mini")
        return ChatOpenAI(
            openai_api_key=openai_key,
            model=model,
            temperature=temperature,
        )

    raise EnvironmentError(
        "No LLM API key found. Set GROQ_API_KEY or OPENAI_API_KEY in your .env file."
    )


def build_chain(system_prompt: str, human_template: str, temperature: float = 0.4):
    """Build LangChain LCEL pipeline: prompt | llm | parser."""
    llm = get_llm(temperature=temperature)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", human_template),
        ]
    )
    return prompt | llm | StrOutputParser()

def resume_generator_chain():
    """Generate ATS-optimized resume from user profile."""
    system = (
        "You are an expert resume writer with 15 years of experience helping "
        "professionals land their dream jobs at top companies. "
        "Write resumes that are ATS-optimised, concise, impactful, and tailored "
        "to the target role. Use strong action verbs and quantify achievements wherever possible."
    )
    human = (
        "Generate a professional resume for the following profile:\n\n"
        "Name: {name}\n"
        "Target Role: {role}\n"
        "Years of Experience: {years_exp}\n"
        "Skills: {skills}\n"
        "Past Experience: {experience}\n"
        "Education: {education}\n"
        "Projects: {projects}\n\n"
        "Format the resume with clear sections: "
        "SUMMARY, SKILLS, EXPERIENCE, PROJECTS, EDUCATION. "
        "Make it concise, powerful, and ATS-friendly. "
        "Do NOT use any markdown — plain text only."
    )
    return build_chain(system, human, temperature=0.5)


def ats_analysis_chain():
    """Generate ATS analysis narrative."""
    system = (
        "You are a senior recruiter and ATS specialist. "
        "Analyse resumes against job descriptions and provide actionable feedback."
    )
    human = (
        "Given this resume and job description, provide a brief (3–4 sentences) "
        "qualitative analysis of the candidate's fit, highlighting strengths and "
        "specific gaps to address.\n\n"
        "Resume:\n{resume}\n\n"
        "Job Description:\n{job_description}\n\n"
        "ATS Score: {score}/100\n"
        "Missing Keywords: {missing_keywords}\n\n"
        "Analysis:"
    )
    return build_chain(system, human, temperature=0.3)


def job_match_chain():
    """Explain job-candidate fit analysis."""
    system = (
        "You are a career coach who explains job-candidate fit clearly and constructively. "
        "Be specific, concise, and encouraging."
    )
    human = (
        "Explain why this candidate is or isn't a strong match for the job. "
        "Include 2 strengths and 2 gaps. Keep it to 4–5 sentences.\n\n"
        "Resume Summary:\n{resume_snippet}\n\n"
        "Job Description:\n{job_description}\n\n"
        "Vector Similarity Score: {similarity_score:.1%}\n\n"
        "Explanation:"
    )
    return build_chain(system, human, temperature=0.4)


def bullet_improver_chain():
    """Improve weak resume bullet points."""
    system = (
        "You are an expert resume coach. "
        "Transform weak, vague bullet points into powerful, quantified achievement statements "
        "using the CAR framework (Context, Action, Result). "
        "Start with a strong action verb. Add realistic metrics if none exist."
    )
    human = (
        "Improve these weak resume bullet points. "
        "Return ONLY the improved bullets, one per line, no preamble.\n\n"
        "Target Role: {role}\n\n"
        "Weak Bullets:\n{bullets}"
    )
    return build_chain(system, human, temperature=0.5)


def career_advisor_chain():
    """Generate personalized career roadmap."""
    system = (
        "You are an expert AI career advisor."
    )
    human = (
        "Act as an expert AI career advisor.\n\n"
        "Based on the user's skills and target role, provide:\n\n"
        "1. Skill Gap Analysis\n\n"
        "* Identify missing skills required for the target role\n\n"
        "2. Personalized Learning Roadmap\n\n"
        "* Step-by-step plan (beginner → advanced)\n\n"
        "3. Project Recommendations\n\n"
        "* 3 practical projects aligned with the role\n\n"
        "4. Action Plan\n\n"
        "* Weekly or phased plan\n\n"
        "Rules:\n\n"
        "* Be specific (mention tools like LangChain, FAISS, APIs, etc.)\n"
        "* Avoid generic advice\n"
        "* Keep output structured and concise\n"
        "* Tailor everything to the user input\n\n"
        "User Skills: {current_skills}\n"
        "Target Role: {target_role}\n"
        "Current Role: {current_role}\n"
        "Years of Experience: {years_exp}\n"
    )
    return build_chain(system, human, temperature=0.5)
