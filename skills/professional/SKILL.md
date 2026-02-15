---
name: professional
description: >-
  Guide professional software development practices - responsibility, ethics, estimates, saying no, commitments.
  Activates when discussing professional conduct, estimation, commitments, ethics, saying no,
  or when quality standards and professional responsibility are relevant.
allowed-tools: Read, Grep, Glob
argument-hint: [situation or code to evaluate]
---

# Professional Software Development

Professional standards for software developers — responsibility, ethics, estimation, and the discipline required when society depends on our code.

For detailed case studies (VW, Knight Capital, Toyota, estimation stories, industry history), read `references/extended-examples.md`.

---

## The Programmer's Oath

Nine promises that define professional software development:

**1. I will not produce harmful code.** My code will do no harm to users, customers, or fellow programmers. I will know what my code does. I will know that my code works. Hiding behind requirements written by others is no excuse — it's my fingers on the keyboard.

**2. The code I produce will always be my best work.** I will not knowingly allow code that is defective in behavior or structure to accumulate. Messy software is harmful software — the more tangled the code, the less certain you are about what it will do. Dead code must be removed. Quick patches cannot be left without doing harm.

**3. I will produce quick, sure, repeatable proof that my code works.** This means TDD. With each release, every element of the code has proof that it works as it should. The three laws of TDD lock you into a cycle that is seconds long — write a failing test, make it pass, clean it up.

**4. I will make frequent small releases** so that I do not impede the progress of others.

**5. I will fearlessly and relentlessly improve my creations.** The first word of software is "soft" — it's supposed to be easy to change. If we didn't want it to be easy to change, we'd call it hardware. To the extent our software is hard to change, we have thwarted the very reason for its existence.

**6. I will keep productivity high** — my own and the productivity of others. I will do nothing that decreases it.

**7. I will ensure coverage.** Others can cover for me and I can cover for them. No single points of knowledge failure.

**8. I will produce honest estimates** — honest in both magnitude and precision. I will not make promises without certainty.

**9. I will never stop learning** and improving my craft.

---

## Do No Harm

### Harm to Society

The first rule: do no harm. The VW emissions scandal showed what happens when programmers write deceitful code — software that purposely thwarted EPA tests, causing cars to emit 20 times the safe amount of pollutants. The CEO blamed "just some software engineers," but those programmers wrote harmful code and should have refused.

Every software developer who knows something is wrong and stays silent shares the blame. You were hired because you know when things are about to go wrong — that means you have the responsibility to speak up before something terrible happens.

### Harm to Function

You must know that your code works and will not harm. Knight Capital went bankrupt in 45 minutes because dead code left in a system was accidentally reactivated — a repurposed flag triggered an infinite loop of bad trades that lost $460 million. Toyota's unintended acceleration killed up to 89 people — their code had 10,000 global variables, and the programmers did not know their code would not kill.

When the stakes are high, you have to drive your knowledge as close to perfection as you can. There's almost always much more at stake than you think.

### Harm to Structure

Anything that makes code hard to read, understand, change, or reuse is structural harm. SOLID principles prevent structural harm between modules. Clean architecture prevents harm at the highest level. Structure matters as much as behavior — sometimes more.

### The Two Values of Software

Consider two programs. Program A does everything correctly but is impossible to change. Program B does nothing correctly but is easy to change. Program B is more valuable — because requirements will change, and when they do, Program A becomes useless forever, while Program B can be made to work and will continue to work.

This is why startups are not an exception. A startup is not an urgent situation that justifies messy code. The one thing that's certain about a startup is that you're producing the wrong product — no product survives contact with users. If you can't change it because you made a mess, you're doomed. The mess slows you down long before you reach the finish line.

---

## Professional Responsibility

### Taking Ownership

Professionalism is a badge of honor AND a marker of accountability. You can't take pride in something you can't be held accountable for. When a non-professional makes a mess, their employer cleans it up. When a professional makes a mess, the professional cleans it up.

### Saying "No"

You were hired for your ability to say no. Any idiot can say yes, but it takes real skill to say no at the right times. By doing so, you can save your company untold amounts of money and effort. If you're asked to commit and you can't, say no and describe your uncertainty. Be willing to discuss options and hunt for a way to say yes — but don't be afraid to say no.

### Saying "Yes"

When you say yes to a commitment, you set up a long domino chain of potential failure. You are the one they're counting on. Think long and hard about whether it's actually possible before committing.

### The Danger of "Try"

When your boss asks you to "just try," the answer is no. You're already trying. There are no magic beans in your pocket to alter reality. Saying "yes, I'll try" is lying — you have no plan to change your behavior, no strategy to do anything different. You only said it to get them to leave you alone.

### No Passive-Aggressive Behavior

Every software developer who knows something is wrong — like when healthcare.gov was clearly not ready — and does nothing to stop the deployment shares part of the blame. You were hired because you know how to identify trouble before it happens. Speak up.

---

## Estimation

### Estimates vs. Commitments

An estimate is NOT a commitment. If you give someone a date, you're giving a commitment, not an estimate. If you don't KNOW you can make a date, don't offer that date — offer a range instead. The most honest estimate you can give is "I don't know." The challenge is to quantify what you do know and what you don't.

### Accuracy and Precision

A good estimate is honest in both accuracy (the range of dates you feel confident in) and precision (how narrow that range is). "Sometime between now and ten years from now" is accurate but lacks precision. "Yesterday at 2:15 AM" is precise but not accurate if you haven't started. Estimates are probability distributions — they have a center point and a width.

### PERT Estimation

For each task, provide three estimates:

- **Best Case (B):** Everything goes right — 1% chance of being this fast
- **Normal Case (N):** Realistic estimate — 50% chance
- **Worst Case (W):** Murphy's Law — 99% chance of being done by this time

**Expected Time (mu):** ((B + W)/2 + N) / 3 — weighted average giving normal case weight of 2.
**Standard Deviation (sigma):** (W - B) / 6.
**Aggregating:** Sum expected times directly. For standard deviations, sum the squares then take the square root.

### The Fudge Factor

We're generally not good at identifying all subtasks — we might miss half. Compensate by multiplying by 2, 3, or even 4. Increasing precision on the fudge factor is expensive — the only way to truly know how long something takes is to do it. Put your estimation effort into a time box.

### Handling Pressure

Managers will ask you to reduce the fudge factor — that's fair, but communicate that increasing precision is expensive. Sometimes they'll try a different tactic: asking you to commit. They're trying to transfer risk that they should be managing onto you. Don't let them bully you into commitments you know you shouldn't make. They might say you're not being a team player — don't be fooled.

Most estimates are lies because they're constructed backwards from a known end date. When Congress mandated the healthcare.gov launch date by law, nobody was asked to actually estimate anything — the programmers all referred to their project plan as "the laugh track."

---

## TDD as Professional Standard

Is TDD a prerequisite to professionalism? It's becoming true. More and more developers believe TDD is part of a minimum set of disciplines that mark professional development. How can you prevent harm to function without tests that show it works? How can you prevent harm to structure without tests that let you clean it? How can you guarantee your test suite is complete unless you follow the three laws?

---

## The Coming Reckoning

We rule the world. Other people think they rule it, but they give those rules to us and we write them into the machines that make everything work. Nothing happens in society unless software is mediating it.

One day, some programmer will make a mistake and thousands of people will die. This isn't speculation — it's a matter of time. When it happens, politicians will point at us. Not at our managers, not at our companies — at us, because it was our fingers on the keyboards. If our answer is "well, our managers were really leaning on us hard" — that's not going to cut it.

The consequence: politicians will regulate our industry. They'll tell us what languages, frameworks, and processes to use. Regulated by people who don't understand software. It will be hell.

We have one chance to avoid this: get there first. Decide what our profession is, what our ethics are, what our disciplines are, what our minimum standards are. Self-regulate, so that when governments step in, they just put the force of law behind what we're already doing. That's what doctors and lawyers did.

---

## Related Skills

- **/tdd** — Quick, sure, repeatable proof that code works
- **/agile** — Professional expectations Agile demands of teams
- **/solid** — Preventing structural harm between modules
- **/architecture** — Preventing harm at the highest level
- **/clean-code-review** — Quality verification before shipping
- **/legacy-code** — Professional responsibility toward existing code
