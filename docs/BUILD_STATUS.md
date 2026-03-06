# BUILD STATUS

## Week 3 (Milestone) – <2026 6 March>

### Golden Machine (Primary Validation)

Location: Classroom PC (Golden Machine)
Machine: Dell Precision 5860 Tower
OS: Windows 11 (64-bit)
CPU: Intel(R) Xeon(R) w3-2435 (3.10 GHz)
GPU: NVIDIA RTX A4000 (16GB)
RAM: 32 GB
Unreal Engine: 5.7.3
Python: 3.9.13

### Secondary Validation Machine (Milestone Requirement)

Machine: Personal Laptop
OS: Windows 10 Home
GPU: Intel(R) UHD Graphics 620 (128 MB)
RAM: 8 GB

---

## Reproducible Run Workflow (Editor)

1. Clone:
   - git clone https://github.com/NburtonII/499-Codrone-Sim.git
   - cd 499-Codrone-Sim
2. Open Unreal project:
   - sim/CodroneSim/CodroneSim.uproject
3. In Unreal Editor:
   - Content Drawer → Content/Maps → BasicArena
   - Press Play (▶)

Expected:

- BasicArena loads
- You spawn inside arena
- Walls block movement

---

## Packaged Build Artifact (Windows Development)

Artifact link: https://github.com/NburtonII/499-Codrone-Sim/releases/tag/v0.3-week3

Run:

- Download + unzip
- Launch: CodroneSim.exe (inside packaged folder)

Expected:

- Build launches successfully

---

## Validation Results

Golden Machine: PASS
Secondary Machine: PASS

---

## Milestone Validation Note (Week 3)

Verified the packaged build on a second machine/account at least once: PASS
Evidence: https://github.com/NburtonII/499-Codrone-Sim/releases/tag/v0.3-week3

---

## Release Notes (Week 3)

- Packaged Windows development build created.
- Default map set to BasicArena.
- Verified build runs on golden machine and secondary machine.
-

## Known Issues

- None at this time
