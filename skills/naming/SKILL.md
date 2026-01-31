---
name: naming
description: >-
  Guide naming things properly - variables, functions, classes, and modules.
  Activates when creating new classes, functions, or variables, when names feel
  unclear or misleading, during code review, or when the user mentions naming,
  rename, unclear names, or intent-revealing names.
allowed-tools: Read, Grep, Glob
argument-hint: [code or file to analyze]
---

# Naming Workflow

This workflow guides AI code writing agents to apply Uncle Bob's Clean Code naming principles. Follow this workflow automatically when naming things in code.

## Workflow Steps

### Step 1: Check Intent Revelation
For each name, verify it reveals intent without needing comments:
- Can you understand the purpose without reading the implementation?
- Would a reader need to look at the code to understand what this name means?
- If yes to the second question, the name has failed to communicate

### Step 2: Verify Pronounceability and Searchability
Ensure names can be:
- Spoken aloud in conversation ("How do you pronounce 'pcguda'?")
- Found with grep/search tools (single letters and magic numbers fail this)

### Step 3: Apply Scope-Length Rule
**For Variables:**
- Long scope = Long, descriptive name
- Short scope = Short name (even single letter is fine in tiny loops)

**For Functions and Classes (OPPOSITE rule):**
- Long/public scope = Short, convenient name (called from many places)
- Short/private scope = Long, descriptive name (serves as documentation)

### Step 4: Use Correct Parts of Speech
- **Classes/Variables**: Nouns or noun phrases
- **Methods**: Verbs or verb phrases
- **Booleans**: Predicates (is_, has_, can_)
- **Enums**: Often adjectives
- **Properties**: Nouns (methods pretending to be variables)

### Step 5: Remove Encodings
Eliminate Hungarian notation and prefixes:
- No `pszName`, `bIsValid`, `nCount`
- No `IAccount` (interface prefix)
- No `m_configIssues` (member prefix)
- No `CAccount` (class prefix)

### Step 6: Apply Professional Standards
Reference the `/professional` skill for quality standards:
- Take responsibility for communicating clearly
- Don't harm fellow programmers with confusing names
- A misleading name can cost immense time and pain

---

## Core Philosophy

Names are not just for your convenience. They are your primary tool for communicating intent. Communicating intent is always your first priority - it's even more important than making sure the code works.

As Martin Fowler said: "Any fool can write code a computer can understand, but it takes a good programmer to write code a human can understand."

As Grady Booch described: "Clean code always reads like well-written prose."

## Core Principles

### 1. Names Must Reveal Intent

Every time you choose a name, it should reveal the intent of the thing you're trying to name. If you need a comment to help you with this, then the name you've chosen does not sufficiently reveal intent.

**Key Test:** If you have to read the code in order to understand a name, that name has pretty much failed to communicate. Whenever you have to go into the code to understand a name, it's a bad name.

**Variable names should form a kind of compilable comment that explains the author's intent.**

### 2. Never Disinform

To disinform - to say something other than you mean - is one of the worst sins a programmer can commit. A name, like an honorable human, should say what it means and mean what it says.

- Do not tolerate any drift in the meanings of your names
- If the meanings of a function, class, or variable change, you must change the name
- A misleading name can cost you and your fellow programmers an immense amount of time and pain

**Abstract classes should have abstract names** - giving a concrete name to an abstract class is disinformation.

### 3. Names Must Be Pronounceable

Other people are going to have to talk about your code. They'll probably have to talk to you about your code. Make it easy for them - pick names that people can say.

Don't force readers to invent some ad hoc pronunciation for your abbreviations.

### 4. Avoid Encodings

This is not the 1990s. We don't need Hungarian notation or type prefixes anymore. We have powerful IDEs that show types on hover, compilers that catch type errors, and unit tests for protection.

Encodings are distracting. They obfuscate the code. They make it hard to read.

### 5. Use Appropriate Parts of Speech

Clean code should read like well-written prose. Use the appropriate parts of speech:
- **Classes and Variables:** Nouns or noun phrases
- **Methods:** Verbs or verb phrases
- **Boolean variables and methods:** Predicates (is_, has_, can_)
- **Enums:** Often adjectives (describing states or object descriptors)
- **Properties:** Nouns (they're methods pretending to be variables)

### 6. The Scope-Length Rule

**For Variables:** Name length should be proportional to scope length
- Long scope = Long name
- Short scope = Short name (even one letter is fine)
- Global variables should have very long names

**For Functions and Classes:** The opposite rule applies
- Long/public scope = Short, convenient name
- Short/private scope = Long, descriptive/explanatory name

## Rules and Guidelines

### Variable Naming Rules

1. **Use explanatory variables** to reveal intent instead of cryptic abbreviations
2. **Avoid single letters** for variables with scopes longer than a few lines
3. **Boolean variables** should be predicates: `isEmpty`, `isTerminated`, `hasValue`
4. **Variable names derived from class names** are acceptable: `account` for an `Account` instance

### Function Naming Rules

1. **Use verbs or verb phrases:** `postPayment`, `getPrice`, `calculateTotal`
2. **Boolean-returning functions** should be predicates: `isPostable`, `canProcess`
3. **Don't use nouns for accessors:** Use `getFirstName()` not `firstName()`
4. **Public functions** should have short, convenient names (called from many places)
5. **Private functions** can have longer, more descriptive names (serve as documentation)
6. **Avoid returning boolean from setter-like functions** - it creates ambiguity in if statements

### Class Naming Rules

1. **Use nouns or noun phrases:** `Account`, `MessageParser`, `Customer`
2. **Avoid noise words:** `Manager`, `Processor`, `Data`, `Info` - these are synonyms for "I don't know what to call this"
3. **Public classes** should have short, convenient names
4. **Private/nested classes** can have longer, explanatory names
5. **Derived classes** add adjectives and get progressively longer: `Account` -> `SavingsAccount`
6. **Abstract classes** should have abstract names, not concrete implementation-specific names

### Encoding Rules (What to Avoid)

1. **No Hungarian notation:** Don't use `pszName`, `bIsValid`, `nCount`
2. **No interface prefix I:** `Account` is better than `IAccount`
3. **No member prefix m_:** Don't use `m_configIssues`
4. **No class prefix C:** Don't use `CAccount`
5. **No type suffixes in names:** The IDE already knows the type

### Mathematical and Domain Conventions

When a well-known mathematical or domain convention exists, use it:
- Ranges with bounds -> Use interval terminology: `OPEN`, `CLOSED`, `LEFT_OPEN`, `RIGHT_OPEN`
- Follow established naming conventions in your domain

## Good Examples

### Revealing Intent with Explanatory Variables

**Good - Self-documenting code:**
```java
int targetYear = baseDate.getYear();
int targetMonth = baseDate.getMonth() + addedMonths;
int targetDay = baseDate.getDay();

// Adding January (value 1) makes the zero-based month conversion clear
targetMonth = targetMonth + JANUARY;
```

### Proper Scope-Based Naming

**Good - Short variable in tiny scope:**
```java
for (Element e : elements) {
    process(e);
}
```

**Good - Short name for public function:**
```java
public class File {
    public void open() { ... }  // Called from many places, convenient name
}
```

**Good - Long name for private function:**
```java
private void tryProcessInstructions() { ... }  // Explains what it does, only called internally
```

### Proper Parts of Speech

**Good - Nouns for classes:**
```java
class Account { }
class MessageParser { }
class DepositAccount { }
```

**Good - Verbs for methods:**
```java
public void postPayment() { }
public Price getPrice() { }
```

**Good - Predicates for booleans:**
```java
boolean isEmpty;
boolean isTerminated;
if (isEmpty) { ... }
public boolean isPostable() { }
```

### Using Enums Instead of Magic Constants

**Good - Descriptive enum for interval types:**
```java
enum DateInterval {
    OPEN,           // excludes both bounds
    CLOSED,         // includes both bounds
    LEFT_OPEN,      // includes only upper bound
    RIGHT_OPEN      // includes only lower bound
}
```

## Bad Examples (Anti-patterns)

### Cryptic Abbreviations

**Bad:**
```java
int yy;   // Year? Which year?
int mm;   // Month? Zero-based or one-based?
int dd;   // Day?
```
**Problem:** You have to read the code to understand what these mean.

### Unpronounceable Names

**Bad:**
```java
private Date pcguda;  // How do you say this? "P-C-G-U-D-A"?
private String gwd;   // "Gee-double-u-dee"? "Gooda"?
```
**Problem:** When someone calls you to discuss this variable, what will they say?

**Bad:**
```java
getYYYY()     // "Get Y-Y-Y-Y"? Should be getYear()
mqDocs        // "M-Q-Docs"?
ppp           // Completely opaque
qtTests       // Should be totalTests
qtPassM       // Should be passedMethods
qtPassS       // Should be passedScenarios
```

### Disinformation

**Bad - Function name doesn't match what it returns:**
```java
public String[] getMonths(boolean shortened) { }
```
**Problem:** Returns month NAMES, not months. Should be `getMonthNames(boolean shortNames)`.

**Bad - Abstract class with concrete name:**
```java
public abstract class SerialDate { }
```
**Problem:** "Serial" implies a specific implementation (serial number/ordinal). An abstract class should have an abstract name like `Date`, `Day`, `DayDate`, or `CalendarDate`.

### Meaningless Comments Instead of Good Names

**Bad:**
```java
// Useful Constant Range
public static final int INCLUDE_BOTH = 0;
public static final int INCLUDE_FIRST = 1;
public static final int INCLUDE_SECOND = 2;
```
**Problem:** "Useful"? "Constant"? The only meaningful word is "range", but range of what? And "first"/"second" don't explain what they mean (lower/upper bounds).

### Hungarian Notation and Encodings

**Bad:**
```java
ITestResult tr;           // "I" prefix unnecessary
m_configIssues;           // "m_" prefix obfuscates
String szName;            // "sz" for zero-terminated string
int nCount;               // "n" for number
boolean bIsValid;         // "b" for boolean
```
**Problem:** IDEs show types on hover. Compilers catch type errors. These prefixes just add noise.

### Variables Too Short for Their Scope

**Bad - Single letter 20+ lines from declaration:**
```java
Document d = getDocument();
// ... 20 lines of code ...
d.process();  // What is 'd'? Have to scroll up to find out
```
**Problem:** The eye-jump to find the declaration creates friction. Should be `document` or at least `doc`.

### Wrong Parts of Speech

**Bad - Adjective used as variable name:**
```java
int fewerThan24Bits;
```
**Problem:** Sounds like a predicate for an if statement. Should be a noun like `partialBits`, `bitsInPartialGroup`, or `bitsRemaining`.

**Bad - Setter that returns boolean:**
```java
public boolean set(String name, String value) { }

// Ambiguous usage:
if (set("username", "Uncle Bob")) { }
```
**Problem:** Is this asking if username was already set to "Uncle Bob"? Or setting it and checking if it succeeded? Should separate into `set()` returning void (throwing on failure) and `isSet()` returning boolean.

### Noise Words

**Bad:**
```java
class AccountManager { }
class DataProcessor { }
class UserInfo { }
class MessageData { }
```
**Problem:** "Manager", "Processor", "Info", "Data" are synonyms for "I don't know what to call this."

## Memorable Quotes

> "Names are not just for your convenience. They are a tool, a powerful tool, that you can use to communicate with others."

> "If you need a comment to help you with this, then the name you've chosen does not sufficiently reveal intent."

> "Variable names form a kind of compilable comment that explains the author's intent."

> "Whenever you have to read the code in order to understand a name, the name has pretty much failed to communicate."

> "If you have to go into the code in order to understand a name, it's a bad name."

> "To disinform, to say something other than you mean, is one of the worst sins a programmer can commit."

> "A name, like an honorable human, should say what it means and mean what it says."

> "Names are not for your convenience. They are your primary tool for communicating intent. And communicating intent is always your first priority. It's even more important than making sure the code works."

> "Don't do this to your readers. Give them names that they can pronounce. Don't force them to invent some ad hoc pronunciation for your abbreviations."

> "No doubt those names were convenient for the authors. But what about the readers?"

> "Noise words like [manager, processor, data, info] are just synonyms for 'I don't know what to call this.'"

> "Clean code always reads like well-written prose." - Grady Booch

> "Any fool can write code a computer can understand, but it takes a good programmer to write code a human can understand." - Martin Fowler

## Stories and Anecdotes

### The Bullet Bob Story

Uncle Bob tells of working on a project 35 years ago with "Bullet Bob" where they had to read code written by a "lily-livered Yale graduate." The code contained variables like `gwd` that they didn't know how to pronounce. Uncle Bob called his pronunciation "GOODA" while Bullet Bob called his "GOODB" (as in "Good B"). The point: when developers can't pronounce variable names, they invent their own ad-hoc pronunciations, leading to communication breakdown.

### The Charles Simonyi / Hungarian Notation Story

Charles Simonyi was the chief architect at Microsoft during the heyday of the DOS era. Being Hungarian, his notation became known as "Hungarian notation." He invented prefixes like `p` for pointer, `sz` for zero-terminated string, `psz` for pointer to zero-terminated string, `ch` for character, `c` for counter, `b` for boolean.

Uncle Bob notes that Charles recently returned from a trip to the Russian space station and lives on a yacht the size of a small battleship with its own helicopter - "So if you want to be a billionaire, all you have to do is invent some silly prefix notation."

The lesson: Hungarian notation made sense in the DOS/C era, but modern IDEs, compilers, and unit tests make it obsolete and counterproductive.

### The SerialDate Analysis

Uncle Bob examines a class called `SerialDate` and traces through the code trying to understand why it's called "Serial." The comment talks about Excel and immutability and representing days instead of times, but doesn't explain "Serial." Looking at the `ToSerial` method reveals the date is represented as an integer (days since January 1st, 1900) - which the author believed made it a "serial number."

But this is disinformation because: (1) it's an abstract class with an abstract `ToSerial` method - any derivative could implement it differently, and (2) "serial numbers" don't have to be consecutive or even alphanumeric. The class should be called something abstract like `Date`, `Day`, `DayDate`, or `CalendarDate`.

### The set() Function Trap

Uncle Bob admits to writing a function `public boolean set(String name, String value)` that violated naming rules. When used in an if statement - `if (set("username", "Uncle Bob"))` - it was ambiguous: Is it asking whether username was already set to that value? Or setting it and checking if the operation succeeded?

The solution: separate into `void set()` that throws on failure and `boolean isSet()` that reports status.

### Tim Ottinger's Legacy

Tim Ottinger wrote a famous paper in 1997 called "Ottinger's Variable and Class Naming Rules" which became the most downloaded paper on the ObjectMentor website. This paper became the basis for the naming chapter in the Clean Code book. Many of the ideas in Uncle Bob's naming teachings originated from Ottinger's work.

### The Aristarchus Astronomy Lesson

Uncle Bob opens the episode with an extended astronomy lesson about how ancient astronomers (Aristarchus of Samos in 270 BC, and Eratosthenes) calculated the scale of the solar system using just geometry, angles, timing, and "one camel" for measuring distance. Despite being off by factors of 17-20 on some measurements due to difficulty measuring small angles, their TECHNIQUES were correct.

The lesson: Like ancient astronomers who could deduce vast distances with careful observation and proper technique, programmers can communicate vast amounts of information through careful naming. The technique matters more than the tools available.

## Historical Context

### Why Encodings Existed

In the DOS/C era before powerful IDEs:
- Programmers couldn't hover over a variable to see its type
- Type errors weren't caught until runtime
- No unit tests existed to catch type mismatches
- Prefixes were a survival mechanism

### Why Encodings Are Obsolete

Modern development provides:
- IDEs that show types on hover
- Compilers that catch type errors at compile time
- Unit tests that catch type mismatches
- Languages with stronger type systems

### The Cost Fallacy

There was a time when using explanatory variables was considered wasteful of CPU cycles and memory. But:
- The true cost of software is in maintenance
- A few extra bytes and cycles are worth it for readable code
- Modern compilers optimize away most overhead anyway

## Review Process

When reviewing code for naming issues:

1. **Read the code provided** - Understand the context and purpose

2. **Identify naming violations with specific line numbers:**
   - Look for cryptic abbreviations
   - Check for unpronounceable names
   - Spot Hungarian notation and encodings
   - Find names that don't match their purpose (disinformation)
   - Check scope-length proportionality
   - Verify correct parts of speech

3. **Explain which principle is violated and why it matters:**
   - Reference the specific Clean Code principle
   - Explain the impact on readability and maintenance
   - Quote relevant wisdom from Uncle Bob when applicable

4. **Suggest improved names with reasoning:**
   - Provide concrete alternatives
   - Explain why the new name is better
   - Consider pronounceability, intent revelation, and scope

5. **Prioritize issues by impact on readability:**
   - **Critical:** Disinformation (name means something different than code does)
   - **High:** Cryptic abbreviations in long scopes
   - **Medium:** Wrong parts of speech, noise words
   - **Low:** Encodings, overly long names in short scopes

## Quick Reference Checklist

- [ ] Can you pronounce this name out loud?
- [ ] Does the name reveal intent without needing comments?
- [ ] Would you need to read the code to understand what this name means?
- [ ] Does the name say what it means and mean what it says?
- [ ] Is the name length appropriate for its scope?
- [ ] Is the correct part of speech used (noun/verb/predicate)?
- [ ] Are there any Hungarian notation prefixes to remove?
- [ ] Are there noise words that could be eliminated?
- [ ] For booleans: Is it written as a predicate?
- [ ] For abstract classes: Is the name abstract (not implementation-specific)?

## Output Format

For each naming issue found:
```
**Current Name:** `badName`
**Location:** file:line
**Problem:** [Why this name is problematic]
**Suggested Name:** `betterName`
**Reasoning:** [Why the new name is better]
```

## Related Skills

- Use `/professional` for professional responsibility and quality standards
