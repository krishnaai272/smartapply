import torch
from transformers import pipeline, BitsAndBytesConfig
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
import re

from src.prompts import RESUME_REWRITE_PROMPT, COVER_LETTER_PROMPT, SCORING_PROMPT

# Load environment variables
load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME")

def load_model():
    """
    Loads the quantized language model from HuggingFace.
    """
    # Configuration for 4-bit quantization for efficient model loading
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=False,
    )

    # Initialize the text generation pipeline
    text_generation_pipeline = pipeline(
        "text-generation",
        model=MODEL_NAME,
        torch_dtype=torch.bfloat16,
        quantization_config=bnb_config,
        device_map="auto", # Automatically use GPU if available
        max_new_tokens=2048,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=-1, # Avoids model stopping prematurely
    )

    llm = HuggingFacePipeline(pipeline=text_generation_pipeline)
    return llm

def generate_all(llm, resume_text, job_description, user_notes):
    """
    Generates the tailored resume, cover letter, and score using the LLM.
    """
    # 1. Generate Tailored Resume
    resume_chain = LLMChain(llm=llm, prompt=RESUME_REWRITE_PROMPT)
    tailored_resume = resume_chain.run(
        resume_text=resume_text,
        job_description=job_description
    )

    # 2. Generate Cover Letter
    cover_letter_chain = LLMChain(llm=llm, prompt=COVER_LETTER_PROMPT)
    cover_letter = cover_letter_chain.run(
        tailored_resume=tailored_resume,
        job_description=job_description,
        user_notes=user_notes if user_notes else "No specific notes provided."
    )

    # 3. Generate Score and Analysis
    scoring_chain = LLMChain(llm=llm, prompt=SCORING_PROMPT)
    score_analysis_text = scoring_chain.run(
        resume_text=tailored_resume,
        job_description=job_description
    )

    # Parse the score and analysis from the raw text
    score, analysis = parse_score_and_analysis(score_analysis_text)
    
    return {
        "tailored_resume": tailored_resume,
        "cover_letter": cover_letter,
        "score": score,
        "analysis": analysis,
    }

def parse_score_and_analysis(text):
    """
    Parses the score and analysis from the LLM's raw output string.
    """
    try:
        score_match = re.search(r"Score:\s*(\d+)", text, re.IGNORECASE)
        score = int(score_match.group(1)) if score_match else 75 # Default score

        analysis_match = re.search(r"Analysis:\s*(.*)", text, re.IGNORECASE | re.DOTALL)
        analysis = analysis_match.group(1).strip() if analysis_match else "Could not parse analysis."

        return score, analysis
    except Exception:
        return 75, "Analysis could not be extracted from the model's response."