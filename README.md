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
