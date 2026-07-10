- 
- Developer Guide
- Contributing

# Contributing

Thank you for contributing to Hermes Agent! This guide covers setting up your dev environment, understanding the codebase, and getting your PR merged.

## Contribution Priorities​

We value contributions in this order:

1. Bug fixes— crashes, incorrect behavior, data loss
2. Cross-platform compatibility— macOS, different Linux distros, WSL2
3. Security hardening— shell injection, prompt injection, path traversal
4. Performance and robustness— retry logic, error handling, graceful degradation
5. New skills— broadly useful ones (seeCreating Skills)
6. New tools— rarely needed; most capabilities should be skills
7. Documentation— fixes, clarifications, new examples

## Common contribution paths​

- Building a custom/local tool without modifying Hermes core? Start withBuild a Hermes Plugin
- Building a new built-in core tool for Hermes itself? Start withAdding Tools
- Building a new skill? Start withCreating Skills
- Building a new inference provider? Start withAdding Providers

## Development Setup​

### Prerequisites​

| Requirement | Notes |
| --- | --- |
| Git | With thegit-lfsextension installed |
| Python 3.11–3.13 | uv will install it if missing |
| uv | Fast Python package manager (install) |
| Node.js 20+ | Optional — needed for browser tools and WhatsApp bridge (matches rootpackage.jsonengines) |

`git-lfs`
`package.json`

### Install with the standard installer​

For most contributors, the best development bootstrap is the same path users
take: run the standard installer, then work inside the repository it cloned.
The installer creates the Hermes venv, wires thehermescommand, stamps the
install method forhermes update, and clones the full git project into$HERMES_HOME/hermes-agent(usually~/.hermes/hermes-agent). That keeps your
development environment on the same layout the CLI, updater, lazy dependency
installer, gateway, and docs assume.

`hermes`
`hermes update`
`$HERMES_HOME/hermes-agent`
`~/.hermes/hermes-agent`

```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bashcd "${HERMES_HOME:-$HOME/.hermes}/hermes-agent"# Add dev/test extras on top of the standard install.uv pip install -e ".[all,dev]"# Optional: browser tools / docs site dependencies.npm install
```

After that, create branches and run tests from that checkout:

```
git checkout -b fix/descriptionscripts/run_tests.sh
```

You can also run a fully isolated Hermes instance (throwaway HERMES_HOME, separate Electron
userData, distinct Electron app name to avoid the single-instance lock):

```
scripts/dev-sandbox.sh python -m hermes_cli.mainscripts/dev-sandbox.sh --persistent python -m hermes_cli.main desktop  # state survives restarts, but lives in the worktree :)
```

### Manual clone fallback​

Use this only if you intentionally do not want Hermes' managed install layout
(for example, a throwaway clone inside a container or CI job). If you install
this way, make sure you run thehermesentrypoint from this venv; running the
systempython3 -m hermes_cli.maincan pick up unrelated system Python
packages.

`hermes`
`python3 -m hermes_cli.main`

Create the venvoutsidethe cloned source tree. A venv that lives inside
the directory the agent operates from can be wiped by a relative-path command
the agent runs against its own checkout (rm -rf venv,uv venv venv, etc.),
which silently destroys the running runtime mid-session. Keeping it outside the
tree means no relative path from the workspace resolves to it.

`rm -rf venv`
`uv venv venv`

```
git clone https://github.com/NousResearch/hermes-agent.gitcd hermes-agent# Create venv with Python 3.11, OUTSIDE the source treeuv venv ~/.hermes/venvs/hermes-dev --python 3.11export VIRTUAL_ENV="$HOME/.hermes/venvs/hermes-dev"export PATH="$VIRTUAL_ENV/bin:$PATH"# Install with all extras (messaging, cron, CLI menus, dev tools)uv pip install -e ".[all,dev]"# Optional: browser toolsnpm install
```

### Configure for Development​

```
mkdir -p ~/.hermes/{cron,sessions,logs,memories,skills}cp cli-config.yaml.example ~/.hermes/config.yamltouch ~/.hermes/.env# Add at minimum an LLM provider key:echo 'OPENROUTER_API_KEY=sk-or-v1-your-key' >> ~/.hermes/.env
```

### Run​

```
# The standard installer already put `hermes` on PATH.hermes doctorhermes chat -q "Hello"
```

If you used the manual clone fallback, run./hermesfrom the checkout or
symlink this clone's venv explicitly:

`./hermes`

```
mkdir -p ~/.local/binln -sf "$(pwd)/venv/bin/hermes" ~/.local/bin/hermes
```

### Run Tests​

```
scripts/run_tests.sh
```

## Code Style​

- PEP 8with practical exceptions (no strict line length enforcement)
- Comments: Only when explaining non-obvious intent, trade-offs, or API quirks
- Error handling: Catch specific exceptions. Uselogger.warning()/logger.error()withexc_info=Truefor unexpected errors
- Cross-platform: Never assume Unix (see below)
- Profile-safe paths: Never hardcode~/.hermes— useget_hermes_home()fromhermes_constantsfor code paths anddisplay_hermes_home()for user-facing messages. SeeAGENTS.mdfor full rules.

`logger.warning()`
`logger.error()`
`exc_info=True`
`~/.hermes`
`get_hermes_home()`
`hermes_constants`
`display_hermes_home()`

## Cross-Platform Compatibility​

SeePlatform Support. Native Windows uses Git Bash (fromGit for Windows) for shell commands. A few features require POSIX kernel primitives and are gated: the dashboard's embedded PTY terminal pane (/chattab) needs a POSIX PTY (Linux, macOS, or WSL2). If you're doing Windows-heavy dev, run the Windows-footgun lint (scripts/check-windows-footguns.py) before pushing.

`/chat`
`scripts/check-windows-footguns.py`

When contributing code, keep these rules in mind:

- Don't add unguardedsignal.SIGKILLreferences.It's not defined on Windows. Either route throughgateway.status.terminate_pid(pid, force=True)(the centralized primitive that doestaskkill /T /Fon Windows and SIGKILL on POSIX), or fall back withgetattr(signal, "SIGKILL", signal.SIGTERM).
- CatchOSErroralongsideProcessLookupErroronos.kill(pid, 0)probes.Windows raisesOSError(WinError 87, "parameter is incorrect") for an already-gone PID instead ofProcessLookupError.
- Don't force the terminal to POSIX semantics.os.setsid,os.killpg,os.getpgid,os.forkall raise on Windows — gate them withif sys.platform != "win32":orif os.name != "nt":.
- Open files with an explicitencoding="utf-8".The Python default on Windows is the system locale (often cp1252), which mojibakes or crashes on non-Latin text.
- Usepathlib.Path/os.path.join— never manually concat with/.This matters less for strings the OS gives us back and more for strings we construct to hand to subprocesses.

`signal.SIGKILL`
`gateway.status.terminate_pid(pid, force=True)`
`taskkill /T /F`
`getattr(signal, "SIGKILL", signal.SIGTERM)`
`OSError`
`ProcessLookupError`
`os.kill(pid, 0)`
`OSError`
`ProcessLookupError`
`os.setsid`
`os.killpg`
`os.getpgid`
`os.fork`
`if sys.platform != "win32":`
`if os.name != "nt":`
`encoding="utf-8"`
`pathlib.Path`
`os.path.join`
`/`

Key patterns:

### 1.termiosandfcntlare Unix-only​

`termios`
`fcntl`

Always catch bothImportErrorandNotImplementedError:

`ImportError`
`NotImplementedError`

```
try:    from simple_term_menu import TerminalMenu    menu = TerminalMenu(options)    idx = menu.show()except (ImportError, NotImplementedError):    # Fallback: numbered menu    for i, opt in enumerate(options):        print(f"  {i+1}. {opt}")    idx = int(input("Choice: ")) - 1
```

### 2. File encoding​

Some environments may save.envfiles in non-UTF-8 encodings:

`.env`

```
try:    load_dotenv(env_path)except UnicodeDecodeError:    load_dotenv(env_path, encoding="latin-1")
```

### 3. Process management​

os.setsid(),os.killpg(), and signal handling differ across platforms:

`os.setsid()`
`os.killpg()`

```
import platformif platform.system() != "Windows":    kwargs["preexec_fn"] = os.setsid
```

### 4. Path separators​

Usepathlib.Pathinstead of string concatenation with/.

`pathlib.Path`
`/`

## Security Considerations​

Hermes has terminal access. Security matters.

### Existing Protections​

| Layer | Implementation |
| --- | --- |
| Sudo password piping | Usesshlex.quote()to prevent shell injection |
| Dangerous command detection | Regex patterns intools/approval.pywith user approval flow |
| Cron prompt injection | Scanner blocks instruction-override patterns |
| Write deny list | Protected paths resolved viaos.path.realpath()to prevent symlink bypass |
| Skills guard | Security scanner for hub-installed skills |
| Code execution sandbox | Child process runs with API keys stripped |
| Container hardening | Docker: all capabilities dropped, no privilege escalation, PID limits |

`shlex.quote()`
`tools/approval.py`
`os.path.realpath()`

### Contributing Security-Sensitive Code​

- Always useshlex.quote()when interpolating user input into shell commands
- Resolve symlinks withos.path.realpath()before access control checks
- Don't log secrets
- Catch broad exceptions around tool execution
- Test on all platforms if your change touches file paths or processes

`shlex.quote()`
`os.path.realpath()`

## Pull Request Process​

### Branch Naming​

```
fix/description        # Bug fixesfeat/description       # New featuresdocs/description       # Documentationtest/description       # Testsrefactor/description   # Code restructuring
```

### Before Submitting​

1. Run tests:scripts/run_tests.shfor CI-parity. Use directpython -m pytest ...only when the wrapper is unavailable or you are intentionally debugging outside the wrapper.
2. Test manually: Runhermesand exercise the code path you changed
3. Check cross-platform impact: Consider macOS, Linux, WSL2, and native Windows. If you touch file I/O, process management, terminal handling, subprocesses, or signals, runscripts/check-windows-footguns.py.
4. Keep PRs focused: One logical change per PR

`scripts/run_tests.sh`
`python -m pytest ...`
`hermes`
`scripts/check-windows-footguns.py`

### PR Description​

Include:

- Whatchanged andwhy
- How to testit
- What platformsyou tested on
- Reference any related issues

### Commit Messages​

We useConventional Commits:

```
<type>(<scope>): <description>
```

| Type | Use for |
| --- | --- |
| fix | Bug fixes |
| feat | New features |
| docs | Documentation |
| test | Tests |
| refactor | Code restructuring |
| chore | Build, CI, dependency updates |

`fix`
`feat`
`docs`
`test`
`refactor`
`chore`

Scopes:cli,gateway,tools,skills,agent,install,whatsapp,security

`cli`
`gateway`
`tools`
`skills`
`agent`
`install`
`whatsapp`
`security`

Examples:

```
fix(cli): prevent crash in save_config_value when model is a stringfeat(gateway): add WhatsApp multi-user session isolationfix(security): prevent shell injection in sudo password piping
```

## Reporting Issues​

- UseGitHub Issues
- Include: OS, Python version, Hermes version (hermes version), full error traceback
- Include steps to reproduce
- Check existing issues before creating duplicates
- For security vulnerabilities, please report privately

`hermes version`

## Community​

- Discord:discord.gg/NousResearch
- GitHub Discussions: For design proposals and architecture discussions
- Skills Hub: Upload specialized skills and share with the community

## License​

By contributing, you agree that your contributions will be licensed under theMIT License.