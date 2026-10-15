# Linux Security Auditor

A Python-based security auditing tool developed on Fedora Linux.

## Project Overview

This project automates basic Linux security configuration
checks and network socket inspection.

## Features

- Linux system information collection
- Firewall default-zone inspection
- SSH server status verification
- TCP and UDP socket inventory
- Port 1716 detection for further investigation
- Security audit report generation using Linux tee
- Structured security findings with PASS and REVIEW statuses
- Automated JSON security report generation

## Technologies

- Python 3
- Fedora Linux
- systemd
- firewalld
- iproute2 (ss)
- JSON
- Git and GitHub

## Security Findings

- Default firewall zone: public
- SSH server: inactive
- Port 1716: detected, review recommended

## Future Improvements

- Structured security findings and severity levels
- Firewall active-zone verification
- Authentication log analysis
- Process identification for listening ports

## Disclaimer

This tool provides basic local security checks.
It is not a vulnerability scanner or a complete
security assessment.