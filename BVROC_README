# BVROC_No_Limit_Passwords — README (Defensive / Developer Guide)

> **Important notice:** This repository contains code designed to interact with authentication services and fetch large credential lists. Because the capability to perform credential-based testing can be misused, this README intentionally focuses on **defensive**, **development**, and **simulation** use only.  
> Do **not** use this code against systems you do not own or do not have explicit, written authorization to test. Misuse may be illegal and cause harm.

---

## Table of Contents

- [Project Overview](#project-overview)  
- [Safe Use Policy](#safe-use-policy)  
- [Key Components (High Level)](#key-components-high-level)  
- [Installation (Developer / Simulation Environment)](#installation-developer--simulation-environment)  
- [Running in Simulation / Dry-Run Mode (Safe)](#running-in-simulation--dry-run-mode-safe)  
- [Development & Testing](#development--testing)  
- [Logging & Output Format](#logging--output-format)  
- [Defensive & Detection Guidance (SOC/MDR/IR)](#defensive--detection-guidance-socmdrir)  
- [Contributing](#contributing)  
- [Security / Legal / Responsible Disclosure](#security--legal--responsible-disclosure)  
- [Appendix — Component Summary (Non-actionable)](#appendix--component-summary-non-actionable)

---

## Project Overview

**BVROC_No_Limit_Passwords** is a Python codebase that demonstrates programmatic integration with external credential lists and an extensible architecture for password-testing workflows.

This repository is provided **for developer education, research into detection techniques, and defensive testing in isolated, authorized labs**. It is *not* a step-by-step offensive toolset. The README below guides maintainers and defenders on how to work with the code safely.

---

## Safe Use Policy

- **Authorized Testing Only** — Run simulations only on infrastructure you own or have explicit written permission to test.  
- **Isolated Environment** — Always run in an isolated VM with no network access to production systems. Use snapshots.  
- **No Live Attacks** — Do not use the code to attempt authentication against third-party or production services.  
- **Use Simulation Mode** — Prefer `--simulate`/`--dry-run` (read-only) mode for all experiments. If the script lacks this option, add it before any testing.

If you are unsure about legal/ethical boundaries, stop and consult your legal/compliance team.

---

## Key Components (High Level)

This section describes the major classes and modules in the codebase to help maintainers and defenders understand purpose and flow — **without actionable steps**.

- **`ExternalThreatIntelligence`**  
  - Purpose: integrates with public credential lists (SecLists, NCSC, Pwdb, default credentials).  
  - Behavior: fetches and parses public wordlists over HTTP, exposes functions that return username and password lists (limited by a configurable `max_passwords`).

- **`AdvancedLegacyBruteForcer`**  
  - Purpose: orchestration layer that collects wordlists, applies limit/selection logic, and manages results & output.  
  - Behavior: coordinates fetching, maintains an output artifact, and contains a thread-safe store for discovered entries (in code; in this repo any network interactions must be disabled or simulated).

- **Bypass / Utility Components** (present as named types in the code)  
  - Purpose: abstract implementation hooks for protocol-specific behaviours and dummy bypass techniques in a lab/test context (for defenders to simulate detection scenarios).

---

## Installation (Developer / Simulation Environment)

> These instructions set up a safe, offline development environment to inspect the code and run local tests / simulations only.

1. Create an isolated virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
