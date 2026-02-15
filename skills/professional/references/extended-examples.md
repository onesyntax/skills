# Professional Software Development — Extended Examples

Detailed case studies, estimation stories, and industry history that illustrate professional responsibilities.

---

## Case Study: The Volkswagen Emissions Scandal

### What Happened

Volkswagen programmers wrote code that detected when EPA emissions tests were being run. During testing, the software activated full emissions controls. During normal driving, it deactivated them — causing cars to emit up to 20 times the safe amount of nitrous oxides.

### The Professional Failures

The code was harmful because it was deceitful. It wasn't a bug — it was intentional fraud implemented in software. When the scandal broke, VW's CEO blamed "just some software engineers who put this in for whatever reason."

### The Lesson

Those programmers wrote harmful code. Even if management ordered it, hiding behind orders is no excuse. Every programmer involved had the responsibility to refuse. In a profession with minimum standards, those programmers would have been held personally accountable — because they should have known that their code was designed to deceive.

This was the first time society pointed at programmers specifically as villains. Not at the company. Not at management. At the people who wrote the code.

---

## Case Study: Knight Capital — Bankrupt in 45 Minutes

### What Happened

On August 1, 2012, Knight Capital technicians deployed new trading software to 7 of their 8 servers. The eighth server still ran old code.

Eight years earlier, a feature called Power Peg had been disabled using a configuration flag. The dead code was never removed — it was left sitting in the codebase because "it wasn't hurting anything."

The new software repurposed that same flag for a different purpose. When the flag was activated for the new feature, the eighth server interpreted it as enabling Power Peg — which started making trades in an infinite loop.

### The Timeline

- **9:30 AM:** Markets open. The eighth server begins executing wild trades.
- **9:31 AM:** Alarms start firing. Nobody understands what's happening.
- **10:15 AM:** After 45 minutes, someone identifies the problem and stops the server.
- **By then:** Knight Capital had promised $7 billion in stock purchases. Net loss: $460 million.
- Knight Capital only had $360 million in cash. They were bankrupt.

### The Professional Failures

1. **Dead code left in the system.** The Power Peg code should have been removed when the feature was disabled. Dead code is a liability — it can be accidentally activated.
2. **Flag repurposing without checking what it controlled.** The developers who repurposed the flag never checked all the code paths it affected.
3. **No comprehensive test suite.** A test that exercised the flag on all servers would have caught the interaction.
4. **Incomplete deployment.** Loading software on 7 of 8 servers created an inconsistent state that nobody verified.

### The Lesson

The programmers did not know what their system would do. This is a direct violation of the first promise: you must know what your code does. Dead code must be removed. Configuration flags must be understood across the entire system. Deployment must be verified across all servers.

---

## Case Study: Toyota Unintended Acceleration

### What Happened

Toyota vehicles began accelerating uncontrollably, with drivers unable to stop. Investigations found software defects in the electronic throttle control system. As many as 89 people were killed. Many more were injured.

### The Technical Reality

Expert analysis of Toyota's source code revealed approximately 10,000 global variables. The code was deeply tangled — functions had side effects that cascaded unpredictably through the global state. Static analysis tools flagged thousands of potential defects.

### The Professional Failure

The programmers who wrote that code did not know that their code would not kill. With 10,000 global variables and no comprehensive test suite, they could not have known. They should have known. When software controls physical systems that can harm people, the standard of proof is higher — you must be able to demonstrate that your code is safe.

### The Lesson

When lives are at stake, you have to drive your knowledge as close to perfection as you can. The combination of global mutable state, no automated tests, and safety-critical functionality is professional malpractice. It's easy to underestimate the harm your code can do — there's almost always much more at stake than you think.

---

## Case Study: Healthcare.gov Launch

### What Happened

Congress mandated by law the date when healthcare.gov had to go live — October 1, 2013. Nobody was asked to estimate whether that date was achievable. On launch day, the system collapsed under load. The website that was supposed to make the Affordable Care Act work nearly killed the entire policy.

### The Professional Failure

The programmers all referred to their project plan as "the laugh track." They knew the date was impossible. They knew the system wasn't ready. Every developer who maintained a passive-aggressive attitude — who knew something was wrong but said nothing — shares the blame.

This is the danger of constructing estimates backwards from a known end date. The estimate was a lie from the start. Every report claiming the project was "on track" was dishonest. Every developer who shrugged and said "not my problem" violated their professional responsibility to speak up.

### The Lesson

You were hired because you know. You know when things are about to go wrong. You know how to identify trouble before it happens. That means you have the responsibility to speak up before something terrible happens — even when speaking up is uncomfortable, even when management doesn't want to hear it.

---

## Estimation Stories

### Off by a Factor of Six

In 1978, Uncle Bob was 26, working at Teradyne on firmware for the COLT (Central Office Line Tester). The system used an Intel 8085 processor with 32K RAM and 32K ROM spread across thirty-two 2708 EPROM chips.

The problem: any one-line code change required replacing all 32 ROM chips worldwide. His boss asked him to make the chips independently deployable.

Estimate: 2 weeks. Actual: 12 weeks. Six times longer than predicted.

The task was far more complicated than he thought. The memory management, the address translation, the chip boundary handling — each subtask spawned new subtasks he hadn't anticipated. His boss didn't get angry — he was a programmer too and understood how estimation works.

### One-Twentieth the Expected Time

Same company, different project. A product called CCU-CMU had been promised to phone companies for years but kept getting delayed. Expected effort: over a man-year of software development. Then someone discovered a forgotten customer needed it in one month.

Uncle Bob said it was impossible. But his boss found a cheat: that specific customer had the smallest possible configuration, which eliminated virtually all the complexity. Instead of building the general solution, they built a special-purpose unit (the PCCU) that handled only that one case.

Delivered in 2 weeks — one-twentieth of the expected time for the general solution.

### The Range of Estimates

These two stories illustrate the wild range estimates can have. In one case, off by a factor of six too optimistic. In the other, a factor of twenty too pessimistic. This is why estimates must be ranges — probability distributions, not single dates. Anyone who demands a single-date estimate is asking you to lie.

---

## The History of Programming as a Profession

### The Growth Trajectory

- **1945:** Approximately 1 computer, 1 programmer (Alan Turing). Turing wrote the first programs for the ACE (Automated Computing Engine) and foresaw the need for "mathematicians of ability who maintain an appropriate discipline."
- **1960:** ~100 computers, ~1,000 programmers. These were scientists, mathematicians, engineers — already disciplined professionals in their 30s-50s who brought rigor from other fields.
- **1965:** ~10,000 computers, ~100,000+ programmers. Drawn from accountants, clerks, planners — mature professionals who understood business processes.
- **1975:** ~1,000,000 computers, ~1,000,000 programmers. Young CS graduates, mostly male, in their 20s. The first generation with no prior professional discipline to draw from.
- **2020s:** Hundreds of millions of computers, hundreds of millions of programmers.

### The Perpetual Inexperience Problem

For the last 50 years, the number of programmers has doubled approximately every 5 years. This means half of all programmers have less than 5 years of experience — and this remains true as long as the doubling continues.

For every programmer with 30 years' experience, there are 63 others who need to learn from them. There aren't enough experienced people to mentor all the new ones coming in. The same mistakes get repeated over and over.

### Society's Shifting Perception

Society's view of programmers has evolved dramatically. In the 1970s, programmers were seen as inconsequential nerds. By the 2000s, programmers were heroes to children — kids asking game developers for autographs. Then in 2015, with the VW scandal, programmers became villains for the first time in real life, not just movies.

This arc — from invisible to heroic to dangerous — reflects society's growing awareness that programmers control the infrastructure of civilization. And with that awareness comes the expectation of professional responsibility.

---

## Example: PERT Estimation in Practice

### The Scenario

A team needs to estimate building an authentication system with these subtasks:

```
Task                     Best(B)  Normal(N)  Worst(W)  mu      sigma
──────────────────────── ──────── ────────── ──────── ─────── ──────
User registration API    2 days   5 days     14 days   5.7     2.0
Password hashing setup   0.5      1          3         1.3     0.4
Login endpoint           1        3          8         3.3     1.2
Session management       2        4          12        5.0     1.7
Password reset flow      1        3          10        3.8     1.5
Email verification       1        2          6         2.5     0.8
Rate limiting            0.5      1          4         1.4     0.6
Integration testing      2        5          15        5.8     2.2
──────────────────────── ──────── ────────── ──────── ─────── ──────
Total expected time:                                   28.8 days
Combined sigma:                                        3.8 days
```

### Interpreting the Results

- **Expected completion:** 28.8 days (~6 weeks)
- **One sigma (68% confidence):** 25.0 to 32.6 days
- **Two sigma (95% confidence):** 21.2 to 36.4 days

The honest estimate to give management: "We expect about 6 weeks, with 95% confidence it'll be between 4.5 and 7.5 weeks."

### Applying the Fudge Factor

We probably missed some subtasks. Security audit, documentation, deployment configuration, edge cases we haven't thought of. Multiply by 1.5 to account for unknowns:

- **Adjusted expected:** 43 days (~9 weeks)
- **Adjusted two-sigma range:** 32 to 55 days (6.5 to 11 weeks)

The honest estimate: "We expect about 9 weeks, but it could be anywhere from 7 to 11 weeks."

### What Not to Do

Manager: "The deadline is 4 weeks."
Wrong answer: "Okay, I'll try."
Right answer: "Our estimate says 9 weeks with significant uncertainty. At 4 weeks, there's less than a 1% chance we'd be done. We can discuss scope reduction or phased delivery if 4 weeks is a hard constraint."
