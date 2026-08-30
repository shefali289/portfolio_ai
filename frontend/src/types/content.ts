/**
 * TypeScript mirrors of the Pydantic models in
 * `backend/app/services/content_models.py`.
 *
 * Hand-written and kept in step by hand — there is no codegen (conventions.md).
 * If you change a content model on the backend, change it here too.
 */

export interface ProfileLinks {
  email: string
  linkedin: string
  github: string
}

export interface Education {
  id: string
  qualification: string
  institution: string
  location: string
  start: string
  end: string
  grade: string
}

export interface Certification {
  id: string
  name: string
  issuer: string
}

export interface Language {
  name: string
  proficiency: string
}

export interface Profile {
  name: string
  title: string
  location: string
  summary: string
  links: ProfileLinks
  education: Education[]
  certifications: Certification[]
  languages: Language[]
}

export interface Role {
  id: string
  title: string
  company: string
  location: string
  start: string
  end: string | null
  current: boolean
  highlights: string[]
  technologies: string[]
  link: string | null
}

export interface Experience {
  roles: Role[]
}

/** Just the name — the resume lists skills, not where each was used. */
export interface Skill {
  name: string
}

export interface SkillGroup {
  id: string
  name: string
  skills: Skill[]
}

export interface Skills {
  _note: string | null
  groups: SkillGroup[]
}

export interface ProjectLinks {
  demo: string | null
  repo: string | null
}

export interface Project {
  id: string
  name: string
  date: string
  context: string
  description: string
  technologies: string[]
  links: ProjectLinks
  todo: string | null
}

export interface Projects {
  projects: Project[]
}

export interface Achievement {
  id: string
  name: string
  issuer: string
}

export interface EngineeringNotes {
  _note: string | null
  achievements: Achievement[]
  building: string[]
  learning: string[]
  beyond: string[]
  todo: string[]
}

export interface PortfolioContent {
  profile: Profile
  experience: Experience
  skills: Skills
  projects: Projects
  engineering_notes: EngineeringNotes
}

// --- AI chat ---------------------------------------------------------------

export interface ChatSource {
  source: string
  type: string
}

export interface ChatAnswer {
  answer: string
  /** false means the question was refused, not answered. */
  grounded: boolean
  sources: ChatSource[]
  retrieval_ms: number
  generation_ms: number
  provider: string
}

// --- job match -------------------------------------------------------------

export type Verdict = 'match' | 'partial' | 'gap'

export interface RequirementEvidence {
  text: string
  source: string
  score: number
}

export interface RequirementMatch {
  requirement: { text: string; source_line: string }
  verdict: Verdict
  evidence: RequirementEvidence[]
}

export interface AgentStep {
  name: string
  label: string
  status: string
  ms: number
}

export interface JobMatchReport {
  matches: RequirementMatch[]
  gaps: RequirementMatch[]
  summary: string
  steps: AgentStep[]
  provider: string
}
