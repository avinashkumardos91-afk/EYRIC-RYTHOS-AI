# Assignment 3: Hiring Kit Pipeline

## The Problem
Many startups and companies face a bottleneck when scaling their teams: going from identifying the need for a new role (e.g., "We need a Senior Frontend Engineer") to actually having the structured materials required to evaluate candidates fairly and consistently. HR teams and hiring managers often spend hours drafting job descriptions, brainstorming interview questions, and creating evaluation rubrics from scratch for every new role.

This project solves that operational pain point by automating the creation of a complete **Hiring Kit**.

## Pipeline Architecture
The pipeline consists of three chained skills that operate sequentially:

1.  **`jd-generator`**:
    *   **Responsibility**: Takes a simple role title and company context, and expands it into a professional, comprehensive Job Description.
    *   **Output format**: Markdown (`.md`)
2.  **`interview-question-generator`**:
    *   **Responsibility**: Analyzes the generated Job Description to extract core competencies and formulates a structured set of technical and behavioral interview questions tailored to the specific role.
    *   **Output format**: Markdown (`.md`)
3.  **`scorecard-generator`**:
    *   **Responsibility**: Synthesizes both the Job Description and the Interview Questions to produce a Candidate Scorecard Template. This rubric allows interviewers to grade candidates objectively across all required competencies.
    *   **Output format**: CSV (`.csv`)

## Execution Order
The skills must be executed in this exact order because each depends on the output of the previous step:
`jd-generator` -> `interview-question-generator` -> `scorecard-generator`

## Sample End-to-End Prompt

To run this pipeline, you can use a combined prompt like the following:

> "Use my **jd-generator** skill to write a job description for a 'Senior Frontend Engineer' at a fast-paced AI startup, then pass that output to the **interview-question-generator** skill to create a structured list of interview questions. Finally, pass both the JD and the interview questions to the **scorecard-generator** skill to produce a candidate scorecard template in CSV format."

---

## Output Examples
You can find a complete run of this pipeline in the `/output-examples/` directory. It includes:
*   `01-job-description.md`
*   `02-interview-questions.md`
*   `03-scorecard.csv`
