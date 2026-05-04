# Security Policy

## Ombre's Security Promise

Ombre is designed with security as a first principle, not an afterthought.

**Core guarantees:**

1. **We never store your API keys.** Your cloud provider credentials stay in your infrastructure. Ombre requests only the permissions needed to read billing data and route jobs.

2. **We never read your workload data.** Ombre processes compute metadata only — duration, cost, provider, GPU utilization. The contents of your training jobs, models, or data are never accessed, stored, or transmitted.

3. **All savings calculations are verifiable.** Every figure Ombre reports can be cross-checked against your own cloud provider billing dashboard. There is no black box.

4. **Minimal permission model.** Ombre requests the minimum permissions necessary. Read-only billing access for scanning. Routing permissions for job execution. Nothing more.

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | ✅ Yes    |
| < 1.0   | ❌ No     |

## Reporting a Vulnerability

If you discover a security vulnerability in Ombre, please report it responsibly.

**Do not open a public GitHub Issue for security vulnerabilities.**

Instead, email: [ombreaiq@gmail.com](mailto:ombreaiq@gmail.com)

Include in your report:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested fixes (optional)

**What to expect:**
- Acknowledgment within 48 hours
- Status update within 7 days
- Fix timeline communicated clearly
- Credit given to reporter (unless anonymity is requested)

## Security Design

### Authentication
Ombre never stores credentials. Provider connections use your locally stored API keys, accessed only during active sessions.

### Data Flow
```
Your Infrastructure          Ombre Engine
─────────────────            ────────────
API Keys (stored here) ──→   Routing instructions only
Workload data          ✗     Never transmitted
Billing metadata       ──→   Read-only, for calculations
```

### Network
All communication between Ombre and cloud provider APIs uses HTTPS/TLS. No plain HTTP connections.

### Audit Logs
Every routing decision, savings calculation, and billing event is logged with timestamps. Enterprise customers have full access to their audit log.
