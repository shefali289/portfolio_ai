import type { Profile } from '../types/content'

interface ContactProps {
  profile: Profile
}

export function Contact({ profile }: ContactProps) {
  const links = [
    { label: 'Email', href: profile.links.email ? `mailto:${profile.links.email}` : '' },
    { label: 'LinkedIn', href: profile.links.linkedin },
    { label: 'GitHub', href: profile.links.github },
  ].filter((item) => item.href)

  return (
    <section
      id="contact"
      aria-labelledby="contact-heading"
      className="rounded-3xl px-6 py-12 sm:px-12 sm:py-16"
      style={{
        backgroundColor: 'var(--surface-raised)',
        border: '1px solid var(--border-subtle)',
      }}
    >
      <p className="eyebrow">Contact</p>

      <h2
        id="contact-heading"
        className="mt-4 max-w-2xl text-3xl font-bold leading-tight sm:text-5xl"
        style={{ color: 'var(--text-primary)' }}
      >
        Let’s build something useful.
      </h2>

      <p className="lede mt-4 max-w-2xl">
        Open to conversations about AI engineering and automation work.
      </p>

      <div className="mt-8 flex flex-wrap gap-3">
        {links.map((item) => (
          <a key={item.label} href={item.href} className="button-secondary">
            {item.label}
          </a>
        ))}
      </div>
    </section>
  )
}
