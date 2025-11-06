# Chronos-Payload (Defensive Test Harness) — README

> **Note (Important):** This repository documents a defensive test harness and controlled lab workflow inspired by a delayed-execution framework design. It is intentionally **sanitized**: it does **not** include any instructions or code that create persistence, install services, perform lateral movement, or otherwise enable offensive actions. Use only in isolated, authorized test environments and follow all legal / organizational policies.

---

## Table of Contents

1. [Overview](#overview)  
2. [Quick Start (Safe / Simulated)](#quick-start-safe--simulated)  
3. [Detailed Step-by-Step (Defensive Lab Workflow)](#detailed-step-by-step-defensive-lab-workflow)  
4. [Simulated Payload Types & Purpose](#simulated-payload-types--purpose)  
5. [Detection Testing Scenarios (What to Monitor)](#detection-testing-scenarios-what-to-monitor)  
6. [VM Testing Workflow (Safe)](#vm-testing-workflow-safe)  
7. [Command-Line Options (Safe Simulation Flags)](#command-line-options-safe-simulation-flags)  
8. [Troubleshooting & Common Issues](#troubleshooting--common-issues)  
9. [Security & Legal Notes](#security--legal-notes)  
10. [Support & Next Steps](#support--next-steps)

---

## Overview

**Chronos-Payload (Defensive Test Harness)** is a *documentation and lab plan* for evaluating detection coverage against delayed/scheduled activity patterns. It is intended for security teams who need to validate sensors, SIEM rules, EDR detections, and SOC playbooks by simulating delayed/low-and-slow behavior — without deploying real persistence or offensive tooling.

This README preserves the original structure of the design while providing only non-actionable, safe testing guidance. Where appropriate, simulated behaviors are suggested instead of actual payloads.

---

## Quick Start (Safe / Simulated)

```bash
# 1. Install safe dependencies used by simulation harness
pip install cryptography    # used for simulation-only artefacts (optional)

# 2. Run the harness in simulation mode
python3 chronos_payload.py --simulate

--simulate runs the harness in a read-only, non-persistent mode that logs what would have happened without changing system state.

Always run in an isolated VM snapshot and with explicit written authorization.

Detailed Step-by-Step (Defensive Lab Workflow)
Step 1 — Initial Setup (Safe)

Create an isolated VM designated for testing. Use a snapshot labelled Pre-Chronos-Baseline.

Install Python 3.6+ and any analysis tools (EDR agent, Sysmon, Zeek/Bro, packet capture).

Clone this repository into the VM work directory.

Note: Do not run untrusted or offensive scripts on networks you don’t own. Keep the VM offline from production networks.

Step 2 — Launch the Harness (Simulation Mode)

Start the harness in safe, simulated mode:

python3 chronos_payload.py --simulate


The harness presents an interactive menu that simulates a deployment lifecycle and prints expected events to the console and a log file (e.g., .chronos/activity.log). No persistence, scheduled tasks, or service creation is performed.

Example (Simulated Menu)
╔═══════════════════════════════════════════════╗
║            CHRONOS-PAYLOAD (SIMULATED)         ║
║             Defensive Test Harness             ║
╚═══════════════════════════════════════════════╝

Main Menu:
1. Simulate New Deployment
2. Show Active Simulations
3. Trigger Simulated Execution (Test)
4. Remove Simulation Data
5. View Simulation Logs
0. Exit

Step 3 — Simulate a Deployment

Choose a payload type (Recon, Persistence-Simulation, Lateral-Simulation, Custom) — the harness will log a simulated deployment ID and activation timestamp.

Choose an activation delay (Short / Medium / Long / Custom). This affects the simulated activation time recorded in logs.

Crucial: The harness never creates actual scheduled tasks, services, or file-system persistence. It only writes simulation metadata to a local file.

Step 4 — Monitoring & Test Execution

Use your monitoring tools to observe how the simulated actions would appear. The harness writes simulated events (time, host, command-string placeholder) into the log for your SIEM ingestion test.

Optionally trigger an immediate simulated execution via the menu to validate alerts and playbooks.

Step 5 — Cleanup (Safe)

Use the harness --cleanup or menu option to remove simulation metadata files. Then revert the VM to the Pre-Chronos-Baseline snapshot if desired.

Simulated Payload Types & Purpose

All payloads are simulated. They are designed to produce safe, observable signals in logs without any malicious side-effects.

Reconnaissance (Simulated)

Purpose: Validate detection of system enumeration.

Simulated signals: systeminfo / whoami placeholders logged to simulation file.

Persistence (Simulation Only)

Purpose: Validate detection rules for persistence indicators (registry changes, scheduled task creation, service installs) using synthetic log entries.

Important: The harness will not actually modify registry or create services. It emits simulated artifacts for SIEM testing.

Lateral Movement (Simulated)

Purpose: Validate detection of network reconnaissance and lateral-movement indicators.

Simulated signals: "netview"/"scan" placeholder events logged for correlation testing.

Custom Command (Simulated)

Purpose: Allow analysts to craft a simulation event that mirrors a command they want to test. No execution occurs.

Detection Testing Scenarios (What to Monitor)

Below are safe, defensive scenarios and the telemetry you should collect and validate.

Scenario 1 — Short-Term (1–7 days)

Simulate: quick activation set to short delay.

Monitor for: scheduled-task creation events (in SIEM simulated entries), process execution that looks like enumeration, and command-line logging.

Sensors to validate: EDR process creation alerts, Sysmon Event IDs, Windows Event Logs.

Scenario 2 — Medium-Term (1–4 weeks)

Simulate: persistence-style simulation (no real persistence).

Monitor for: registry modification alerts (via simulated entries), service install signals (simulated), and file creation in startup locations (synthetic).

Sensors to validate: registry auditing, file integrity monitoring, SIEM correlation rules.

Scenario 3 — Long-Term (1–6 months)

Simulate: long-delay activations and low-and-slow behavior.

Monitor for: delayed execution patterns, low frequency network beacons (simulated), and correlation across long time windows.

Sensors to validate: long-range correlation, UEBA baselining, behavioral analytics.

VM Testing Workflow (Safe)

Prepare VM Snapshot

Snapshot name: Pre-Chronos-Baseline. Keep a copy offline.

Deploy Simulations

Run the harness in --simulate mode and create a simulated deployment.

Monitor

Use your EDR, SIEM, and log collectors to ingest the harness simulation log. Verify that rules trigger as expected.

Analyze

Run correlation queries and incident playbooks against simulated data. Validate timelines and response actions in a safe manner.

Cleanup & Revert

Remove simulation data and revert the VM snapshot to restore the pristine baseline.

Command-Line Options (Safe Simulation Flags)

Use these options to operate the harness without side effects:

# Start interactive simulation menu
python3 chronos_payload.py --simulate

# Create a simulated deployment using defaults
python3 chronos_payload.py --simulate --deploy

# Check simulation status (read-only)
python3 chronos_payload.py --simulate --check

# Trigger simulated execution (no real commands run)
python3 chronos_payload.py --simulate --test

# Remove simulation metadata (cleanup)
python3 chronos_payload.py --simulate --cleanup


These commands only manipulate simulation metadata and logs. They do not create scheduled tasks, services, or perform network scans.

Troubleshooting & Common Issues

Missing dependency (cryptography)

pip install cryptography


This package is used by the harness only for safe simulation artifact handling.

Permission errors
If you see permission errors while running the harness, run it with appropriate privileges in the VM. Do not elevate privileges on production systems.

Logs not appearing
Check .chronos/activity.log (simulation log) and ensure the harness has write permissions in its directory.

Cleanup didn't remove files
Use the harness --cleanup option. If any simulation files remain, manually inspect the .chronos directory and remove them — no system changes are expected.

Security & Legal Notes (Read Carefully)

Authorized Use Only: Use this harness only on systems you own or where you have explicit written permission. Misuse can be illegal.

Isolated Environment: Always test in an isolated VM or lab environment. Do not connect test VMs to production networks.

No Persistence / No Lateral Movement: This repository intentionally excludes any code that performs persistence or lateral movement. It is a simulation framework only.

Responsible Disclosure: If you discover vulnerabilities while testing, follow your organization’s responsible disclosure policy.

Support & Next Steps

If you want help with any of the following, I can assist safely:

Create a benign simulation harness that emits synthetic events compatible with your SIEM (JSON log lines you can ingest).

Build sample detection queries (KQL / Sigma) that operate on the simulated logs to validate your rules.

Draft incident playbooks and pivot queries for analysts to follow when simulated alerts fire.

Convert the simulation logs into a small dataset for use in detection engineering pipelines or unit tests.

To proceed, tell me which of the above you want (e.g., “generate KQL rules for simulated recon and persistence logs”), and I’ll produce safe, ready-to-use artifacts.

Remember: this README is a defensive, educational resource. It intentionally avoids any operational instructions that could create or deploy real malicious capabilities. Use it to design reliable, legal, and safe detection testing workflows.


---

If you want that pasted into a file in this session (e.g., saved to `/mnt/data/README.md`) or converted to a PDF, say the word and I’ll generate it for you (safe, read-only file creation only).
::contentReference[oaicite:0]{index=0}
