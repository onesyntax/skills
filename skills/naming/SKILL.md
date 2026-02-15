---
name: naming
description: >-
  Analyze and apply Clean Code naming principles to code. Activate whenever
  writing new code, reviewing existing code, renaming, refactoring, or doing
  code review. Also activate when the user mentions naming, unclear names,
  intent-revealing names, or readability. Naming is the foundation — bad names
  poison functions, classes, and architecture. When in doubt, activate this
  skill. Every name is a chance to communicate or to confuse.
allowed-tools: Read, Grep, Glob
argument-hint: [code or file to analyze]
---

# Naming Skill

Names are your primary tool for communicating intent — more important even than making the code work, because wrong code with good names gets fixed fast, while working code with bad names rots silently. A name that forces a reader into the implementation has failed.

This skill covers two modes: **choosing good names** when writing code, and **identifying bad names** when reviewing code.

For detailed naming walkthroughs and before/after examples, read `references/extended-examples.md`.

---

## The Six Principles

### 1. Reveal Intent

A name should tell you why something exists, what it does, and how it's used — without needing a comment or reading the implementation.

**Test:** If someone has to read the code body to understand the name, the name has failed.

```
// Bad — requires reading implementation
d
pcguda

// Good — self-documenting
elapsedTimeInDays
postingCutoffDate
```

### 2. Never Disinform

A name must say what it means and mean what it says. If the meaning drifts, rename immediately. A misleading name costs more time than a missing name.

```
// Bad — returns month NAMES, not months
getMonths(shortened)

// Good — says what it actually returns
getMonthNames(abbreviated)
```

Abstract classes deserve abstract names. Giving a concrete name to an abstract class is disinformation (e.g., `SerialDate` for an abstract date class should be `DayDate` or `CalendarDate`).

### 3. Be Pronounceable

People discuss code out loud. If you can't say the name in conversation, it will generate ad-hoc pronunciations that differ between teammates.

```
// Bad — "P-C-G-U-D-A"? "Gooda"?
pcguda

// Good — say it in a sentence
postingCutoffDate
```

### 4. Be Searchable

You should be able to grep for a name. Single letters and magic numbers fail this. The exception: single-letter variables in tiny scopes (2-3 line loops).

### 5. Match Scope to Length

**Variables** — name length proportional to scope:

| Scope | Name style | Example |
|-------|-----------|---------|
| Loop body (2-3 lines) | Single letter OK | `for (e in elements)` |
| Method body | Short but clear | `account`, `total` |
| Class field | Descriptive | `activeUserCount` |
| Global/module | Very descriptive | `maximumLoginAttemptsBeforeLockout` |

**Functions and classes** — the *opposite* rule:

| Scope | Name style | Why |
|-------|-----------|-----|
| Public API | Short, convenient | Called from many places: `open()`, `save()` |
| Private/internal | Longer, explanatory | Serves as documentation: `tryReconnectWithExponentialBackoff()` |

Derived classes naturally get longer: `Account` -> `SavingsAccount` -> `HighYieldSavingsAccount`.

### 6. Use Correct Parts of Speech

Code should read like prose. Wrong parts of speech create friction.

| Thing | Part of speech | Examples |
|-------|---------------|----------|
| Class, variable | Noun / noun phrase | `Account`, `messageParser` |
| Method | Verb / verb phrase | `postPayment()`, `calculateTotal()` |
| Boolean | Predicate | `isEmpty`, `hasChildren`, `canExecute` |
| Enum value | Adjective or noun | `OPEN`, `CLOSED`, `PENDING` |
| Property/getter | Noun (method pretending to be a variable) | `account.balance` |

---

## Encodings to Remove

In the DOS/C era, programmers couldn't hover over a variable to see its type. Type errors weren't caught until runtime. No unit tests existed. Prefixes like `psz` and `b` were a survival mechanism — they encoded type information that nothing else could tell you.

That era is over. Modern IDEs show types on hover. Compilers catch type mismatches at compile time. Unit tests verify behavior. Strong type systems prevent entire categories of error. Encodings are now pure noise — they obscure the name's intent behind outdated abbreviations.

| Encoding | Example | Fix |
|----------|---------|-----|
| Hungarian notation | `pszName`, `bIsValid`, `nCount` | `name`, `isValid`, `count` |
| Interface prefix | `IAccount` | `Account` (impl gets the suffix: `AccountImpl`) |
| Member prefix | `m_configIssues` | `configIssues` |
| Class prefix | `CAccount` | `Account` |
| Type suffix | `nameString`, `accountList` | `name`, `accounts` |

---

## Respect the Language's Idioms

The six naming principles are universal. Casing, style, and conventions are not — they belong to whatever language you're working in. Follow the established conventions of the language and the project's existing style. A name that violates the language's idioms is a naming violation, even if the underlying principle is sound.

---

## Noise Words to Avoid

These words are synonyms for "I don't know what to call this":

`Manager`, `Processor`, `Handler`, `Data`, `Info`, `Helper`, `Utils`, `Service` (when vague), `Impl` (when the only impl)

If you catch yourself reaching for one, ask: *what does this class actually DO?* Name it after that.

---

## When Writing New Code

Use this checklist as you name things:

1. **Say it out loud.** Can you use this name in a sentence to a colleague?
2. **Cover the implementation.** Does the name alone tell you what this thing is for?
3. **Check the scope.** Is the length appropriate? (short scope = short name for variables; opposite for functions)
4. **Check the grammar.** Right part of speech? Nouns for things, verbs for actions, predicates for booleans?
5. **Check the language.** Following the casing/style conventions of the language?
6. **Search for it.** Can you grep for this name and find it?

---

## When Reviewing Code

### Process

1. Read the code and understand context
2. Identify naming violations (with specific locations)
3. Explain which principle is violated and why it matters
4. Suggest improved names with reasoning
5. Prioritize by impact:

| Severity | Type | Example |
|----------|------|---------|
| Critical | Disinformation — name means something different than code does | `getMonths()` returns month name strings |
| High | Cryptic abbreviation in long scope | `d` used 20 lines from declaration |
| Medium | Wrong part of speech, noise words | `fewerThan24Bits` as a variable (sounds like a predicate) |
| Low | Unnecessary encoding, overly long name in short scope | `m_count` in a 3-line method |

### Output Format

For each issue found:

```
**Name:** `badName`
**Location:** file:line
**Principle violated:** [which of the six]
**Problem:** [why this name hurts readability]
**Suggestion:** `betterName`
**Reasoning:** [why the new name is better]
```

---

## Common Traps

**The setter-that-returns-boolean trap:**
```
// Ambiguous — is this asking or telling?
if set("username", "Uncle Bob") then ...

// Fix: separate command from query
set("username", "Uncle Bob")   // throws on failure
if isSet("username") then ...  // asks without changing
```

**The boolean parameter trap:**
```
// Caller can't tell what true means
render(document, true)

// Fix: use an enum or named constant
render(document, DRAFT)
```

**The abstract class with concrete name:**
```
// Bad — "Serial" implies a specific implementation
abstract class SerialDate

// Good — abstract name for abstract class
abstract class CalendarDate
```

---

## Related Skills

- `/functions` — function naming is tightly coupled with function design
- `/professional` — taking responsibility for clear communication
- `/clean-code-review` — comprehensive review that includes naming checks
