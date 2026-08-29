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
