import type { PortfolioContent } from '../types/content'

export type EvidenceIndex = Record<string, string>

export function buildEvidenceIndex(content: PortfolioContent): EvidenceIndex {
  const index: EvidenceIndex = {}

  for (const role of content.experience.roles) {
    index[`role:${role.id}`] = `${role.title} at ${role.company}`
  }
  for (const project of content.projects.projects) {
    index[`project:${project.id}`] = project.name
  }
  for (const certification of content.profile.certifications) {
    index[`certification:${certification.id}`] = `${certification.name} — ${certification.issuer}`
  }
  for (const education of content.profile.education) {
    index[`education:${education.id}`] = `${education.qualification} — ${education.institution}`
  }
  for (const achievement of content.engineering_notes.achievements) {
    index[`achievement:${achievement.id}`] = `${achievement.name} — ${achievement.issuer}`
  }

  return index
}
