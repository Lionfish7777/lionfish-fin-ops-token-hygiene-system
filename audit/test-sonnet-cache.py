# test-sonnet-cache.py
# LIONFISH TOKEN HYGIENE — Python A/B/C Cache Test
# Sonnet 4.6 | default-claude-hygiene-audit-20260606
#
# CLAUDE.md compliance:
#   §3 — Model ceiling: claude-sonnet-4-6 (Opus never used)
#   §4 — cache_control on system block AND first large user context block
#
# Install: pip3 install anthropic
# Run:     python3 test-sonnet-cache.py
 
import os
import anthropic
 
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise SystemExit("No API key. Run: export ANTHROPIC_API_KEY='sk-ant-...'")
 
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
 
MODEL = "claude-sonnet-4-6"
 
SYSTEM_PROMPT = """You are an AI assistant for Lionfish7777, an AI systems optimization practice
specializing in token hygiene, context architecture, and agentic workflow efficiency.
 
The Lionfish7777 Token Hygiene System reduces redundant raw input token consumption
by architecting context to cache static information once and read it repeatedly,
routing tasks to the correct models, and loading only what each specific call requires.
 
This system was developed and proven in May 2026. The verified May 2026 result:
144,011,625 tokens processed, $89.40 actual bill versus $432.03 at standard rate.
That is a 79.3% reduction in total API cost — on a real developer account, with receipts."""
 
LARGE_USER_CONTEXT = """You are reviewing the Lionfish7777 token hygiene methodology.
The system has three compounding layers:
  Layer 1 — Cache Engine: caches the system prompt, 35.9% savings on Day 1 (proven June 6 2026)
  Layer 2 — Context Architecture: loads only what each call needs, reduces context size monthly
  Layer 3 — Model Routing: routes tasks to the cheapest capable model
 
Real data — May 16 2026 developer console:
  Total tokens: 60,776,845
  Prompt cache reads: 59,288,619 (97.6%)
  Prompt cache writes: 1,248,486 (2.1%)
  Raw input: 27,587 (0.05%)
  Output: 212,153 (0.3%)
 
This replaced a 63M token uncontrolled spike with a controlled, predictable consumption pattern."""
 
 
def run_test(label: str, **kwargs) -> dict:
    print(f"\n{'━'*50}")
    print(f"  {label}")
    print(f"{'━'*50}")
 
    response = client.messages.create(**kwargs)
    u = response.usage
 
    # Sonnet 4.6 pricing
    input_cost        = (u.input_tokens  * 3.00)  / 1_000_000
    output_cost       = (u.output_tokens * 15.00) / 1_000_000
    cache_write       = getattr(u, "cache_creation_input_tokens", 0) or 0
    cache_read        = getattr(u, "cache_read_input_tokens", 0) or 0
    cache_write_cost  = (cache_write * 3.75) / 1_000_000
    cache_read_cost   = (cache_read  * 0.30) / 1_000_000
    total             = input_cost + output_cost + cache_write_cost + cache_read_cost
 
    print(f"Input tokens:        {u.input_tokens:,}")
    print(f"Output tokens:       {u.output_tokens:,}")
    print(f"Cache created:       {cache_write:,}")
    print(f"Cache read (hit):    {cache_read:,}")
    print(f"{'─'*40}")
    print(f"Input cost:          ${input_cost:.6f}")
    print(f"Output cost:         ${output_cost:.6f}")
    print(f"Cache write cost:    ${cache_write_cost:.6f}")
    print(f"Cache read cost:     ${cache_read_cost:.6f}")
    print(f"TOTAL:               ${total:.6f}")
 
    return {
        "input": u.input_tokens, "output": u.output_tokens,
        "cache_write": cache_write, "cache_read": cache_read,
        "total": total
    }
 
 
def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║      LIONFISH7777 TOKEN HYGIENE — PYTHON A/B/C AUDIT        ║
║           Sonnet 4.6 | CLAUDE.md §3 + §4 compliant          ║
║    cache_control on system block AND first user context      ║
╚══════════════════════════════════════════════════════════════╝
    """)
 
    # ── SCENARIO A — Monolith, no cache ──────────────────────────────────
    # system as plain string = no caching possible
    a = run_test("A: MONOLITH (no cache) — baseline",
        model=MODEL,
        max_tokens=150,
        system=SYSTEM_PROMPT,   # plain string — cache_control cannot be added here
        messages=[{
            "role": "user",
            "content": f"Context: {LARGE_USER_CONTEXT}\n\nSummarize the mission in one sentence."
        }]
    )
 
    # ── SCENARIO B — Cache creation (§4: both blocks get cache_control) ──
    b = run_test("B: ARCH SYSTEM (cache creation) — first load",
        model=MODEL,
        max_tokens=150,
        system=[{                          # array of content blocks, not plain string
            "type": "text",
            "text": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"}   # §4 — system block
        }],
        messages=[{
            "role": "user",
            "content": [{
                "type": "text",
                "text": f"Context:\n{LARGE_USER_CONTEXT}\n\nHow do the three layers compound over time?",
                "cache_control": {"type": "ephemeral"}   # §4 — first large user context block
            }]
        }]
    )
 
    import time; time.sleep(1.5)
 
    # ── SCENARIO C — Cache hit (same system + same user context = cache read) ──
    c = run_test("C: ARCH SYSTEM (cache hit) — steady state",
        model=MODEL,
        max_tokens=150,
        system=[{
            "type": "text",
            "text": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"}   # §4 — identical block = cache read
        }],
        messages=[{
            "role": "user",
            "content": [{
                "type": "text",
                "text": f"Context:\n{LARGE_USER_CONTEXT}\n\nWhat makes this system more effective at scale?",
                "cache_control": {"type": "ephemeral"}   # §4 — identical context = cache read
            }]
        }]
    )
 
    # ── Summary ──────────────────────────────────────────────────────────
    monolith_x2  = a["total"] * 2
    arch_system  = b["total"] + c["total"]
    saved        = monolith_x2 - arch_system
    pct          = (saved / monolith_x2 * 100) if monolith_x2 > 0 else 0
 
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                  LIONFISH AUDIT RESULTS                      ║
╚══════════════════════════════════════════════════════════════╝
 
  A (Monolith x 1 request):     ${a['total']:.6f}
  B (Arch + cache create):       ${b['total']:.6f}
  C (Arch + cache hit):          ${c['total']:.6f}
 
  ────────────────────────────────────────────
  Monolith (2 requests):         ${monolith_x2:.6f}
  Arch system (2 requests):      ${arch_system:.6f}
 
  SAVINGS:                       {pct:.1f}%
  Tokens saved:                  ${saved:.6f}
 
  ────────────────────────────────────────────
  SCALING (2,000 requests/month):
  Monolith:   ${a['total'] * 2000:.4f}/month
  Lionfish:   ${(b['total'] + c['total'] * 1999):.4f}/month
 
  SCALING (3 engineers/year):
  Monolith:   ${a['total'] * 2000 * 12 * 3:.2f}/year
  Lionfish:   ${(b['total'] + c['total'] * 1999) * 12 * 3:.2f}/year
    """)
 
 
if __name__ == "__main__":
    main()
