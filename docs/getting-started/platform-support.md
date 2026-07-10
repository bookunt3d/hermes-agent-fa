---
layout: docs
title: "پشتیبانی از پلتفرم‌ها"
permalink: /getting-started/platform-support/
---

- 
- Getting Started
- Platform Support

# Platform Support

Hermes Agent maintains support for many platforms and distribution methods, but we can't support every possible install method.

## Tier 1​

We strive to never break installations and updates for these. Issues & regressions in Tier 1 are our first priority and take precedence over other platforms.

| OS / Architecture | Installation methods | Notes |
| --- | --- | --- |
| macOS(Apple Silicon) | Hermes Desktop,install.sh |  |
| Windows 10 / 11(x86_64, aarch64) | Hermes Desktop,install.ps1 | A few features arenot available. |
| Linux /WSL2(x86_64, aarch64) | install.sh | We test on the latest Ubuntu and WSL2. If your distro has glibc, systemd, and follows the Filesystem Hierarchy Standard, it's likely to work pretty well. |
| Docker Container(x86_64, aarch64) | docker pull | Docker installs do not supporthermes update. Updating is done by running a new image. |

[Hermes Desktop](https://hermes-agent.nousresearch.com/)
[install.sh](/docs/getting-started/installation#linux--macos--wsl2--android-termux)
`install.sh`
[Windows 10 / 11](/docs/user-guide/windows-native)
[Hermes Desktop](https://hermes-agent.nousresearch.com/)
[install.ps1](/docs/getting-started/installation#windows-native)
`install.ps1`
[not available](/docs/user-guide/windows-native#feature-matrix)
[WSL2](/docs/user-guide/windows-wsl-quickstart)
[install.sh](/docs/getting-started/installation#linux--macos--wsl2--android-termux)
`install.sh`
[Docker Container](/docs/user-guide/docker#quick-start)
[docker pull](/docs/user-guide/docker#quick-start)
`docker pull`
`hermes update`

## Tier 2​

These platforms are maintained in-tree only as a best effort.
Releases may break them, and we can't promise we'll fix them promptly when they break.

PRs will be accepted to fix issues with them, but they will take precedence below fixing issues with Tier 1 platforms.

| OS / Architecture | Installation methods | Notes |
| --- | --- | --- |
| Android (Termux)(aarch64) | install.sh | A few features arenot available. |
| Nix(MacOS, Linux, NixOS) | install.sh | Breaks often due to node.js packaging woes. Best of luck~! <3 |

[install.sh](/docs/getting-started/installation#linux--macos--wsl2--android-termux)
`install.sh`
[not available](/docs/getting-started/termux#known-limitations-on-phones)
[install.sh](/docs/getting-started/nix-setup)
`install.sh`

## Unsupported​

These platforms and distribution methods arenotsupported.
We suggest that you migrate to a supported distribution method or platform.
They may be broken right now, they may break more in the future.
PRs to fix them willnotbe accepted, and any code that keeps compatibility with them may be removed at any point.

- installs via the AUR (we might upstream patches if it helps out <3)
- macOS on x86 (Intel) processors
- installs viapypi(e.g.uv tool install hermes-agent,pip install hermse-agent, etc.)
- installs viabrew(brew install hermes-agent)

`pypi`
`uv tool install hermes-agent`
`pip install hermse-agent`
`brew`
`brew install hermes-agent`

If you are using an unsupported distribution method, please read thethe installation guideto learn how to switch to a supported one.

[the installation guide](/docs/getting-started/installation)
[Edit this page](https://github.com/NousResearch/hermes-agent/edit/main/website/docs/getting-started/platform-support.md)