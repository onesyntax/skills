---
name: functions
description: >-
  Guide writing and refactoring clean functions - size, parameters, structure.
  Activates when writing new functions, refactoring existing functions, when
  functions grow too large or complex, have too many arguments, or when the user
  mentions function size, extract method, side effects, or function arguments.
allowed-tools: Read, Grep, Glob
argument-hint: [code or file to analyze]
---

# Functions Workflow

When writing or refactoring functions, follow this systematic workflow based on Uncle Bob's Clean Code principles from Episodes 3 and 4 of the Clean Code video series.

## Workflow Steps

### Step 1: Keep Functions Small (4-6 lines ideal, under 20 max)
- **First Rule**: Functions should be small
- **Second Rule**: They should be smaller than that
- Functions should be so small that if statements and while loops don't need braces
- A four-line function has very little room for indenting
- Aim for ONE level of indent (the ideal)

### Step 2: Ensure Function Does ONE Thing (Extract Till You Drop)
- A function should do one thing, do it well, and do it only
- **The Definitive Test**: If you can extract one function from another, then the original function was doing more than one thing BY DEFINITION
- Continue extracting until you cannot extract any more
- Look at braces as an opportunity to extract
- The end result: classes composed of functions that are all about four lines long

### Step 3: One Level of Abstraction Per Function
- Functions should not mix high and low level abstractions
- String manipulation and business logic shouldn't be in the same function
- Code should read like a top-down narrative (Step-Down Rule)

### Step 4: Minimize Arguments (0-2 ideal, avoid booleans)
- **Zero arguments (niladic)**: Best
- **One argument (monadic)**: Okay
- **Two arguments (dyadic)**: Okay, but approaching sloppy
- **Three arguments (triadic)**: Bordering on sloppy, hard to remember order
- Avoid flag arguments (booleans) - write TWO separate functions instead
- Avoid output arguments - use return values instead
- Don't pass null into functions

### Step 5: Apply Command-Query Separation
- **Commands**: Change the state of the system (have side effects), return nothing (void)
- **Queries**: Return a value, do NOT change state
- Functions that change state should NOT return values
- Functions that return values should NOT change state

### Step 6: No Side Effects, No Temporal Coupling
- Side effects are lies - your function promises to do one thing, but does hidden things
- Identify and eliminate temporal coupling (functions that must be called in order)
- Use the "Passing a Block" pattern for temporally coupled pairs (open/close, new/delete)

### Step 7: Apply /professional Workflow for Quality Standards
- Use professional standards for naming, error handling, and code organization
- Ensure code is readable, maintainable, and follows team conventions

---

## Core Principles

### The Two Rules of Functions
1. **First Rule**: Functions should be small
2. **Second Rule**: They should be smaller than that

### Functions Do One Thing
- A function should do one thing, do it well, and do it only
- **The Definitive Test**: If you can extract one function from another, then the original function was doing more than one thing BY DEFINITION
- Continue extracting until you cannot extract any more - this is called "Extract Till You Drop"
- A function that manipulates more than one level of abstraction is doing more than one thing

### Extract Till You Drop
- The only way to truly ensure a function does one thing is to extract, extract, extract until you cannot extract anymore
- If you CAN extract a function from another, you SHOULD, because the original was doing more than one thing
- The end result: classes composed of functions that are all about four lines long
- Look at braces as an opportunity to extract

## Size and Structure Rules

### Function Length Guidelines
- **Historical rule (1980s)**: A screenful on a VT-100 terminal (about 20 lines)
- **Modern recommendation**: 4-6 lines is ideal, 10 lines is way too big
- Functions should be so small that if statements and while loops don't need braces
- A four-line function has very little room for indenting

### Indentation Rules
- Aim for ONE level of indent (the ideal)
- Don't have many internal braces within functions
- The bodies of if statements, else clauses, and while loops should be ONE LINE LONG
- That one line should probably be a function call with a nice descriptive name
- Nested if/while/try-catch blocks indicate functions that are too large

### The Screen Full Metric (Historical Context)
- In the 1980s: about 20 lines (VT-100 had 24 lines, 4 used by editor)
- Today's large monitors make this metric obsolete
- The metric that matters now: 4-6 lines

## Argument Guidelines

### Number of Arguments
- **Zero arguments (niladic)**: Best
- **One argument (monadic)**: Okay
- **Two arguments (dyadic)**: Okay, but approaching sloppy
- **Three arguments (triadic)**: Bordering on sloppy, hard to remember order
- **More than three**: Challenging to remember what they do, causes double-takes

### The Cohesion Test
If three or more variables are so cohesive that they can be passed together into a function, why aren't they an object?

### Constructor Arguments
- Constructors follow the same rules as regular functions
- Prefer a set of nicely named setter functions over a constructor with many arguments
- Consider using the Builder pattern
- Passing structures and maps to constructors is okay in a pinch, but setter functions are preferred
- The temporary incompleteness of objects built with setters is acceptable when you have a good suite of unit tests

### Flag Arguments (Booleans)
- **Avoid passing boolean values into functions**
- A boolean argument loudly declares that the function does TWO things: one for true, one for false
- Write TWO separate functions instead: one for each case
- Booleans in argument lists cause readers' eyes to blur over
- Two booleans are even worse: the function does FOUR things
- "Have you ever stared at a function call that passed in two Booleans, true, false, and wondered what the heck the two of them mean and what order they're coming in?"

### Output Arguments
- **Hate them. Avoid them.**
- People don't expect data to come OUT of arguments - they expect it to go IN
- Output arguments cause double-takes and confusion
- If you must pass data out of a function, use the return value
- "How many times have you studied a function call, looking at some argument, wondering why the heck that argument was going in, only to finally realize that the argument wasn't going in?"

### Null Arguments
- **Don't pass null into functions**
- Almost as bad as passing a boolean - there's a behavior for null and non-null cases
- Creates hidden branching in the function
- Write two functions: one that takes the argument, one that doesn't
- Don't use null as a pseudo-boolean

### Defensive Programming
- Defensive programming is a smell
- It means you don't trust your team or your team's unit tests
- If you're constantly checking input arguments for null, your unit tests aren't preventing those nulls
- Exception: Public APIs require defensive programming because you don't know what external callers will pass
- "The best defense is a really good offense. And a good offense is a good suite of tests."
- "Defensive programming leads to offensive code."

## The Step-Down Rule

### Organization Principle
Like a newspaper article:
- Important stuff goes at the top
- Details go at the bottom
- Readers can start at the top and read downward until they get bored

### Implementation
1. Public methods at the top (telling what you can do with the class)
2. Private methods below the publics that call them
3. Private methods called by those privates below them
4. Continue stepping down one level of abstraction at a time
5. **No backwards references** - all function calls point DOWN the listing

### The Scissors Rule (from C++)
- Public members at the top
- Private members at the bottom
- You could cut between public and private and hand users the public part
- Unfortunately, Java convention puts privates at top (follow the convention anyway)

### Multiple Public Methods
- Put first public function followed by all its private hierarchy
- Then put next public function followed by its private hierarchy
- Exhaust each hierarchy completely before starting the next
- Alternative: All publics at top, then expand trees (also acceptable)

### What the Step-Down Rule Looks Like
- Functions at the top are very high level
- Functions at the bottom are very low level and detailed
- There's a stepping down one level of abstraction at a time
- Every function calls children functions which call their own children
- Children go directly below parents in the order they are called

## Command-Query Separation (CQS)

### Definition
- **Commands**: Change the state of the system (have side effects), return nothing (void)
- **Queries**: Return a value, do NOT change state

### Rules
- Functions that change state should NOT return values
- Functions that return values should NOT change state
- Easy to recognize side effects: void return = side effects, non-void = no side effects

### Examples
- **Getters are queries**: Call them anytime, they never change state
- **Setters are commands**: They have side effects, involved in temporal coupling
- What would setAmount() return? Nothing obvious - so return void

### Benefits
- Easy to recognize whether a function has side effects just by looking at the signature
- Reduces confusion for readers
- Prevents the error of expecting a command to be safe to call multiple times

### Error Handling in Commands
- Don't return error codes from commands
- Throw exceptions instead, maintaining the convention that commands return void
- "We are often tempted to return some kind of error code from our commands if they fail to change state. But it's better instead to throw an exception."

### Multi-threaded Exception
- Sometimes you need to change state AND return the previous state atomically
- Resolve this the same way as open/close: by passing a block

## Side Effects and Temporal Coupling

### What are Side Effects?
- When a function changes a variable that outlives the function call
- Example: changing an instance variable
- "This kind of scary action at a distance makes programs difficult to understand and is a persistent source of errors."

### Temporal Coupling
- When functions must be called in a specific order
- Examples: open/close, new/delete, set/get
- Side effect functions often come in pairs
- "Temporal coupling is when you depend on one thing happening before or after another thing."

### The Danger
- In most systems, temporal couplings are hidden
- You look at two functions that must be called in order and can't explain why
- "It's just that the system fails if you don't"

### Solution: Passing a Block
```
// Instead of:
open(file)
// ... do stuff ...
close(file)

// Do this:
open(file, fileCommand) {
    // open opens the file
    // executes the fileCommand
    // closes the file
}
```
- Hide the second function inside the first
- Pass a command/block into the first function
- The first function does open, executes the block, then does close
- Guarantees correct order, limited side effects

### Functional Programming Insight
- The functional paradigm tells us to write programs without assignment statements
- Pass values as arguments, recurse through function arguments
- A true mathematical function's value depends ONLY on its input arguments
- Every call with the same inputs produces the exact same output
- No side effects

## Tell, Don't Ask

### Principle
- Tell objects what to do
- Don't ask objects what their state is and then make decisions for them
- "The object knows its own state and can make its own decisions, thank you."

### Benefits
- Reduces the need for query functions
- Decouples functions from their surroundings
- Query functions can get out of control quickly

### Train Wrecks
```java
// Bad - a train wreck (boxcars coupled together)
o.getX().getY().getZ().doSomething();

// Good
o.doSomething();
```
- Train wrecks are clear violations of Tell, Don't Ask
- We ask, then ask, then ask before telling anything

### The Law of Demeter
Formalizes Tell, Don't Ask. You may call methods on objects only if:
1. They were passed as arguments
2. They were created locally in your method
3. They are instance variables of your class
4. They are globals

**In particular**: You may NOT call methods on an object that was returned by a previous method call.

### Knowledge Coupling
```java
o.getX().getY().getZ().doSomething();
```
This single line knows:
- O has an X
- X has a Y
- Y has a Z
- Z can do something

"That's a tremendous amount of knowledge for one line of code to have, and it couples the function that contains it to too much of the whole system."

### Individual Function Knowledge
- Individual functions should have very limited knowledge
- Don't let functions walk the whole configuration database
- Don't let functions navigate the entire object map
- Tell neighboring objects what you need done; depend on them to propagate the message

### Biological Analogy
- Cells do not ask each other questions; they tell each other what to do
- You are an example of a Tell, Don't Ask system
- Within you, the Law of Demeter prevails

## Switch Statements

### The Problem
- Switch statements are not object-oriented
- They interfere with independent deployability and independent developability
- Each case likely has a dependency outward on an external module (fan-out problem)
- Source code dependencies point in the same direction as flow of control
- Creates a knot of dependencies making independent deployability virtually impossible
- If any downstream module changes, the switch and everything depending on it must be recompiled/redeployed

### If-Else Chains Have the Same Problem
Long chains of if-else statements have the same fan-out problem as switch statements.

### Solutions

#### 1. Replace with Polymorphism
- Take the switch argument (some type code)
- Replace it with an abstract base class with a method for the operation
- Each case becomes a derived class implementing that method
- Runtime dependency (flow of control) remains the same
- Source code dependencies are inverted (subtypes depend upward on base class)
- Create instances in a factory

#### 2. Move to Safe Modules
- Move switch statements to the main partition or other independently deployable modules
- Safe if all cases stay in the main partition
- Safe if all dependencies cross the line pointing toward the application
- Main is a plug-in to the application

### The Main Partition
- Draw a line separating core application from low-level details
- Application partition on one side (most code)
- Main partition on the other (factories, configuration, main program)
- Dependencies should point ONE direction: toward the application
- Main should depend on the application; application should NOT depend on main
- This is dependency injection

### Independently Deployable = Independently Developable
- When modules are independently deployable, teams can work independently
- Switch statements that ruin plug-in structure also ruin team independence
- Teams start colliding with each other

## Structured Programming

### The Three Basic Operations
All algorithms should be composed of:
1. **Sequence**: Arrangement of two blocks in time; exit of first feeds entry of second
2. **Selection**: Boolean splits flow into two pathways, one block executes, pathways rejoin
3. **Iteration**: Repeated execution of a block until Boolean is satisfied

### Single Entry, Single Exit
- All three structures have a single entrance at the top and single exit at the bottom
- This property is recursive: algorithms, modules, systems all share it
- Makes it possible to reason about code sequentially
- A provable system is an understandable system

### Early Returns
- Multiple returns from a function are FINE
- Early returns and guard returns simply take you to the exit at the end
- No violation of structure

### Mid-Loop Returns and Breaks
- **Mid-loop returns**: Add an unexpressed and indirect exit condition; make loops more complicated
- **Continue**: No problem at all; just a no-op to the bottom of the loop
- **Break**: Problematic; creates indirect and unexpressed exit condition
- **Labeled break**: Even worse; exits from more than one loop at a time
- These don't explicitly violate structure but make loops harder to understand

### The Small Function Connection
"If you keep your functions as small as we told you to back in episode 3, then it'll be pretty tough not to follow structured programming. After all, a four-line function always has a single entry and a single exit, and it's really really hard to get them to have mid-loop breaks and returns."

## Error Handling

### Michael Feathers' Wisdom
"Error handling is important, but if it obscures logic, it's wrong."

### Write Error Handling First
- Write error handling code BEFORE the rest of the code
- Don't paint yourself into an implementation that can't handle errors well

### Exceptions vs. Error Codes
- Prefer exceptions over error codes
- "That reminds me too much of the horror scene of the 70s and the 80s when every function's return value was usurped by an error code."
- Returning error codes (false, null, -1) is the old, bad way

### Exception Design

#### Scope Exceptions to Classes
- Don't reuse canned exceptions (IllegalArgumentException, etc.)
- Create exceptions scoped to the class that throws them
- Name with as much specific information as possible
- Example: `Stack.Overflow`, `Stack.Underflow`, `Stack.Empty`

#### Unchecked Exceptions
- "The experiment with checked exceptions is over and it failed."
- Failed in C++, failed in Java, C# didn't even try
- Problem: Creates reverse dependency up inheritance hierarchy
- If derived class throws new exception, must change base class declaration
- Violates independent deployability, breaks Open-Close Principle
- **Rule**: Derive exceptions from RuntimeException

#### Exception Messages
- Best case: no message needed at all
- Exceptions should be so precise that no message is required
- "The best comment is the comment you don't have to write."
- Sometimes include a small tidbit of useful information
- Always let name, context, and scope do most of the work

### Try Block Rules
1. If `try` appears in a function, it must be the VERY FIRST word (after variable declarations)
2. The body of the try block must contain a SINGLE LINE - a function call
3. The catch and finally blocks are the VERY LAST thing in the function
4. Nothing follows them

### Functions Do One Thing - Error Handling is One Thing
- A function should either do something OR handle errors
- It should NOT do both
- Separate error handling into its own function

### The Null Object / Special Case Pattern
- Often better than throwing errors
- When zero-capacity stack is requested, return a degenerate stack that behaves appropriately
- Push overflows, pop underflows, size returns zero
- No if statements needed in main code
- Extract an interface, create a special implementation for the edge case

### Null Return Values
- Nulls that slip through the system eventually cause null pointer exceptions
- "Nulls, especially when they're unexpected, have this tendency to slip and slide through the system until eventually they cause a null pointer exception."
- Consider throwing an exception instead (like Stack.Empty for top() on empty stack)
- For expected "not found" cases, null may be acceptable (e.g., find() returning null)
- But consider: "null is a value that means nothing. Minus one is not nothing."

## Good Examples

### Refactored TestableHTML
After refactoring the 46-line testableHTML function:
```java
// The invoke function tells you exactly what it does
public String invoke() {
    if (isTestPage()) {
        surroundPageWithSetupAndTeardown();
    }
    return pageData.getHtml();
}
```
- Reads like well-written prose
- Each function is small, simple, and well-named
- Class renamed to SetupTeardownSurrounder with invoke renamed to surround

### Video Store Refactoring Result
- One big ugly function refactored across multiple classes
- Code dragged from Statement to Rental to Movie to Movie derivatives
- Left behind: a nice trail of simple little functions
- Each function has a nice name and explains itself perfectly
- Functions step down through abstraction levels

### Stack Kata Example
```java
public class Stack {
    public static Stack make(int capacity) {
        if (capacity < 0)
            throw new IllegalCapacity();
        if (capacity == 0)
            return new ZeroCapacityStack();
        return new BoundedStack(capacity);
    }

    // Overflow, Underflow, Empty all derive from RuntimeException
    public static class Overflow extends RuntimeException {}
    public static class Underflow extends RuntimeException {}
    public static class Empty extends RuntimeException {}
}
```

## Bad Examples (Anti-patterns)

### The Original TestableHTML Function
- 46 lines long
- Loaded with duplicate code
- Two arguments and two local variables used throughout
- Variables used by different sections = a class hiding inside
- Function name was a noun, not a verb
- Mixed levels of abstraction: string buffers, path parsers, page crawlers (low-level) with testable pages, inherited pages (high-level)

### Prime Number Generator (Before Refactoring)
- One big function with a whole bunch of variables
- Variables controlled by one big function = classes hiding inside
- Generated code from literate programming - "an awfully messy gob of goop"

### Train Wreck Code
```java
o.getX().getY().getZ().doSomething();
```
- Knows too much about system structure
- Violates Law of Demeter
- Violates Tell, Don't Ask

### Functions with Multiple Booleans
```java
render(true, false);  // What do these mean? What order?
```

### Error Code Returns
```java
if (push(element) == false) {
    // handle error
}
```
Horror of the 70s and 80s.

### Large Functions with Indentation
- Long functions are where classes go to hide
- Like a 12-year-old's filing system: everything on the floor
- Comfortable to the author, bewildering to newcomers

## Memorable Quotes

### On Function Size
- "The first rule of functions? They should be small. The second rule of functions? They should be smaller than that."
- "Four lines is okay. Maybe five, six okay. Ten is way too big."
- "I want my functions so small that my if statements and my while loops don't need braces."
- "I look at braces as an opportunity to extract."

### On Extraction
- "Extract till you drop."
- "If you can extract one function from another, you should because that original function was by definition doing more than one thing."
- "You continue to extract functions until you cannot extract any more."

### On Arguments
- "Function arguments are hard. It's hard to figure out what each parameter means. They're hard to read, and they're hard to understand."
- "We should treat every function argument as a liability and not as an asset."
- "Zero is best. One is okay. Two is okay. Three is bordering on sloppy."
- "If three or more variables are so cohesive that they can be passed together into a function, why aren't they an object?"

### On Boolean Arguments
- "When you pass a Boolean into a function, what you are doing is you are loudly declaring to the world that you've just written a function that does two things."
- "A function that takes two Booleans does four things."

### On Output Arguments
- "I hate them. I hate them."
- "People just don't expect data to be coming out of a function into an argument."

### On Defensive Programming
- "Defensive programming is a smell."
- "Defensive programming leads to offensive code."
- "The best defense is a really good offense. And a good offense is a good suite of tests."

### On Readability
- "Pascal once wrote, 'I'm sorry this letter is so long, I didn't have time to make it smaller.'"
- "Leaving something big is irresponsible, careless, and just downright rude."
- "It is more important for you to make your code understandable than it is for you to make your code work."

### On Classes Hiding in Functions
- "A long function is where the classes go to hide."
- "Whenever you have a whole bunch of variables controlled by one big function, what you really have is one or more classes hiding in there."

### On Navigation and Understanding
- "Long functions are the way a 12-year-old files things away."
- "You're not going to get lost in a forest full of little tiny methods because those methods have names that you gave them."
- "Those names are the signposts that will guide you through the code."
- "You can't get lost if you've used good names."

### On Function Call Overhead
- "Worrying about that kind of overhead is entirely misplaced and counterproductive."
- "A function call takes a nanosecond, maybe less."

### On Temporal Coupling
- "Temporal coupling is when you depend on one thing happening before or after another thing."
- "This kind of scary action at a distance makes programs difficult to understand."

### On Tell, Don't Ask
- "Simply stated, tell don't ask is a rule that advises us to tell other objects what to do, but not to ask objects what their state is."
- "The object knows its own state and can make its own decisions, thank you."
- "Cells do not ask each other questions. They tell each other what to do."

### On Law of Demeter
- "It's even been called the Suggestion of Demeter because it's so hard."
- "We don't want our functions to know about the whole system."

### On Error Handling
- "Error handling is important, but if it obscures logic, it's wrong." - Michael Feathers
- "The experiment with checked exceptions is over and it failed."
- "I like my exceptions to be so precise that no message is needed."
- "The best comment is the comment you don't have to write."
- "A function should either do something or it should handle errors. But it shouldn't do both."

### On Switch Statements
- "Switch statements are a missed opportunity to use polymorphism."
- "A switch statement is the antithesis of independent deployability."

## Refactoring Techniques

### Extract Method Object
1. Convert a large function into a class of its own
2. Construct the class with the original function arguments
3. Promote local variables to fields
4. Call an invoke method to execute the logic
5. Now you can extract many smaller functions without passing arguments between them

### Extract Till You Drop Process
1. Pull major sections into individual functions
2. Separate those functions into different levels of abstraction
3. Extract predicates of if statements into boolean functions
4. Extract bodies of if statements into well-named functions
5. Continue until if statements read like sentences
6. Continue until you cannot extract anymore

### Finding Hidden Classes
1. Identify large functions with many variables used throughout
2. A large function is a scope divided into different sections
3. Those sections communicate using variables local to the entire scope
4. This IS a class - extract it
5. Often one large function contains multiple classes

### Replacing Switch with Polymorphism
1. Identify the type code being switched on
2. Create an abstract base class with a method for the switch operation
3. Create derived classes for each case
4. Move case logic into the appropriate derived class
5. Delete the switch statement
6. Create instances in a factory

### The Passing a Block Pattern
1. Identify temporally coupled pair (open/close, new/delete)
2. Create a single function that takes a command/block
3. The function does the "open", executes the block, does the "close"
4. Eliminates temporal coupling and limits side effects

### Null Object / Special Case Pattern
1. Identify edge cases that require special handling
2. Extract an interface from the main class
3. Create a special implementation for the edge case
4. Return the special implementation from the factory for edge cases
5. No if statements needed in the calling code

## Review Process

When reviewing functions, follow this systematic process:

### 1. Read the Code
- Understand what the function is trying to accomplish
- Note the overall structure and flow

### 2. Check Function Sizes
- **Target**: 4-6 lines ideal, under 20 acceptable
- **Red flags**: Functions over 20 lines, multiple levels of indentation
- Count the lines in each function
- Identify functions that could be split

### 3. Count and Evaluate Arguments
- **Ideal**: 0-2 arguments
- **Acceptable**: 3 arguments (borderline)
- **Problem**: More than 3 arguments
- Look for opportunities to group arguments into objects

### 4. Identify Problematic Argument Types
- **Flag arguments (booleans)**: Should be two separate functions
- **Null arguments**: Should be overloaded functions
- **Output arguments**: Should use return values instead

### 5. Verify Step-Down Rule
- Public methods should be at the top
- Called methods should appear below their callers
- No backwards references (calling functions above)
- Each level should step down one abstraction level

### 6. Check Abstraction Levels
- Functions should not mix high and low level abstractions
- String manipulation and business logic shouldn't be in the same function

### 7. Look for Side Effects
- Identify functions that change state
- Check for temporal coupling (functions that must be called in order)
- Verify command-query separation

### 8. Examine Control Structures
- Look for mid-loop breaks and returns
- Check for complex nested loops
- Identify switch statements and long if-else chains

### 9. Review Error Handling
- Exceptions preferred over error codes
- Try blocks should contain single function calls
- Exceptions should be scoped to their classes
- Check for unnecessary defensive null checks

### 10. Check for Train Wrecks
- Look for chained method calls (Law of Demeter violations)
- Identify Tell, Don't Ask violations

### 11. Document Violations
For each issue found, note:
- File path and line number
- The specific principle violated
- Why it's a problem
- Suggested refactoring

### 12. Suggest Specific Refactoring
Provide concrete examples:
- Extract Method for long functions
- Replace boolean with two functions
- Extract Class for functions with many shared variables
- Replace switch with polymorphism
- Pass a Block for temporal coupling

## Code to Analyze

$ARGUMENTS

## Output Format

For each function issue:
```
**Function:** `functionName`
**Location:** file:line
**Issue:** [Size/Arguments/Side Effects/etc.]
**Problem:** [Description of the issue]
**Suggestion:** [How to fix it]
**Refactored Example:** (if helpful)
```

---

## Self-Review (Back Pressure)

After writing or refactoring functions, ALWAYS perform this self-review before presenting code as done:

### Self-Review Steps
1. **Size Check**: Is each function 4-6 lines (ideal), under 20 (acceptable)?
2. **One Thing Check**: Can I extract any more functions? If yes, do it.
3. **Abstraction Check**: Is there only one level of abstraction per function?
4. **Arguments Check**: Do any functions have more than 2 arguments? Refactor.
5. **Boolean Arguments**: Are there any flag arguments? Split into two functions.
6. **Side Effects**: Does any function change state AND return a value? Apply CQS.
7. **Naming Check**: Do all function names use verbs/verb phrases?

### If Violations Found
- Fix the violations immediately
- Re-run self-review
- Only present as "done" when self-review passes

### Mandatory Quality Gate
Functions are NOT complete until:
- [ ] All functions are small (under 20 lines, ideally 4-6)
- [ ] Each function does ONE thing
- [ ] Arguments minimized (0-2 per function)
- [ ] No flag/boolean arguments
- [ ] Command-Query Separation applied

## Related Skills

- **/professional** - Apply professional standards for quality assurance
- **/naming** - Ensure function names reveal intent
- **/clean-code-review** - Run comprehensive review after refactoring
