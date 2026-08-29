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
    <section id="contact" aria-labelledby="contact-heading" className="rounded-3xl bg-slate-950 px-6 py-10 text-white sm:px-10">
      <p className="text-sm font-semibold uppercase tracking-[0.25em] text-cyan-300">Contact</p>
      <h2 id="contact-heading" className="mt-3 text-3xl font-bold">Let’s build something useful.</h2>
      <p className="mt-3 max-w-2xl text-slate-300">Connect through the channels provided in the portfolio.</p>
      <div className="mt-6 flex flex-wrap gap-3">
        {links.map((item) => <a key={item.label} href={item.href} className="inline-flex min-h-11 items-center rounded-full border border-slate-600 px-4 text-sm font-semibold hover:border-cyan-300 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-cyan-300">{item.label}</a>)}
      </div>
    </section>
  )
}
