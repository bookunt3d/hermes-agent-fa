- 
- Features
- Automation
- Automation Blueprints Catalog

# Automation Blueprints

Automation Blueprints are ready-to-run automations. Pick one, fill in a couple
of fields, and Hermes schedules it as a cron job — no cron syntax required.

Every blueprint works fromevery surface:

- Dashboard / desktop app— open the Cron page, switch to theBlueprintstab, fill the form, and clickSchedule it.
- CLI, TUI, and messengers— type/blueprint <name>(e.g./blueprint morning-brief) and Hermes asks you for what it needs, one
question at a time, then schedules it. The name match is forgiving — a
prefix or near-spelling resolves. Power users can skip the questions by
passing values inline:/blueprint morning-brief time=08:00.
- Desktop app— clickSend to Appon any blueprint and it opens with the
command pre-loaded in your composer.

`/blueprint <name>`
`/blueprint morning-brief`
`/blueprint morning-brief time=08:00`

Blueprints never schedule anything silently — you always confirm before the job
is created. Manage created jobs anytime with/cron.

`/cron`

Loading blueprints…

## Writing your own​

A blueprint is just a skill with ametadata.hermes.blueprintblock in itsSKILL.mdfrontmatter. SeeCreating Skills → Automation Blueprintsfor the
slot schema and how to publish one.

`metadata.hermes.blueprint`
`SKILL.md`