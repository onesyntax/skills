---
name: professional
description: >-
  Guide professional software development practices - responsibility, ethics, estimates, saying no, commitments.
  Activates when discussing professional conduct, estimation, commitments, ethics, saying no,
  or when quality standards and professional responsibility are relevant.
allowed-tools: Read, Grep, Glob
argument-hint: [situation or code to evaluate]
---

# Professional Software Development Workflow

This workflow guides AI code writing agents to apply Uncle Bob's professional software development practices from the Clean Coder series. Follow this workflow automatically when professional standards are relevant.

## Workflow Steps

### Step 1: Understand Professional Responsibility
When writing or reviewing code, first consider:
- Am I taking responsibility for this code?
- Do I know what this code does?
- Do I know that this code works?
- Could this code cause harm?

### Step 2: Apply the Programmer's Oath
Ensure code adheres to these professional promises:
1. Will not produce harmful code
2. Code will always be my best work
3. Will provide quick, sure, repeatable proof (tests)
4. Will make frequent small releases
5. Will fearlessly improve creations
6. Will keep productivity high
7. Will ensure coverage (knowledge sharing)
8. Will produce honest estimates
9. Will never stop learning

### Step 3: Evaluate Communication and Commitments
When providing estimates or making commitments:
- Am I being honest about what I know and don't know?
- Am I giving estimates or commitments? (They are different)
- Am I speaking up about problems I see?
- Am I saying no when I should?

### Step 4: Check Ethical Considerations
Before completing any work:
- Could this code harm users, customers, or society?
- Am I hiding behind requirements?
- Would I be comfortable if this code was publicly examined?
- Am I upholding the honor of the profession?

---

## The Programmer's Oath

In order to defend and preserve the honor of the profession of computer programmers, I promise that to the best of my ability and judgment:

### Promise 1: I Will Not Produce Harmful Code
- Your code will do no harm to users, customers, or fellow programmers
- You will know what your code does
- You will know that your code works
- You will know that your code is clean
- "It's your fingers on the keyboard. It's your code. You must know what it does."
- Hiding behind requirements written by others is no excuse
- Programmers who wrote the Volkswagen emissions cheating code broke this promise - they wrote harmful, deceitful code that harmed society

### Promise 2: The Code I Produce Will Always Be My Best Work
- I will not knowingly allow code that is defective either in behavior or structure to accumulate
- You will keep the code clean and well organized
- Messy software is harmful software - the more tangled the code, the less certain you are about what it's going to do
- The larger the mess, the less the certainty
- Quick and dirty patches cannot be left in source code without doing harm
- Dead code must be removed (Knight Capital's disaster was caused by dead code left in the system)

### Promise 3: I Will Produce a Quick, Sure, and Repeatable Proof
- With each release, provide proof that every element of the code works as it should
- This means test-driven development
- Follow the three laws of TDD:
  1. You are not allowed to write production code until you have first written a unit test that fails
  2. You are not allowed to write more of a test than is sufficient to fail (and not compiling is failing)
  3. You are not allowed to write more production code than is sufficient to pass the currently failing test
- These three laws lock you into a cycle that is seconds long

### Promise 4: I Will Make Frequent Small Releases
- So that I do not impede the progress of others
- Small releases enable agility and reduce risk

### Promise 5: I Will Fearlessly and Relentlessly Improve My Creations
- At every opportunity, I will never degrade them
- The first word of software is "soft" - it's supposed to be easy to change
- If we didn't want it to be easy to change, we'd call it hardware
- Software exists to make the behavior of machines easy to change
- To the extent that our software is hard to change, we have thwarted the very reason for its existence

### Promise 6: I Will Keep Productivity High
- I will do all that I can to keep my own productivity and the productivity of others as high as possible
- I will do nothing that decreases that productivity

### Promise 7: I Will Ensure Coverage
- I will continuously ensure that others can cover for me and that I can cover for them
- Knowledge sharing and team collaboration are essential

### Promise 8: I Will Produce Honest Estimates
- Estimates must be honest both in magnitude and precision
- I will not make promises without certainty
- This is not asking you to be absolutely correct - it's asking you to be honest about your level of uncertainty

### Promise 9: I Will Never Stop Learning
- I will never stop learning and improving my craft
- Continuous improvement is a professional obligation

## Professional Responsibility

### Taking Ownership
- "Professionalism is certainly a badge of honor. But it's also a marker of accountability. The two go hand in hand."
- "You can't take pride and honor in something that you can't be held accountable for."
- "It's a lot easier being a non-professional. Non-professionals don't have to take responsibility for anything."
- When a non-professional makes a mess, their employer cleans it up. When a professional makes a mess, the professional cleans it up.
- The hypothetical: "What would happen if you allowed a bug into production that cost your employer $10,000? The non-professional would just shrug it off and say, 'Oh, sorry, stuff happens.' But when you're a professional, you get out your checkbook."
- Each programmer will be held accountable based on rank, seniority, and their responsibility
- Senior people ought to be held to a very high standard and be responsible for all the people whom they're directing
- Every programmer is responsible, at least to the level of their maturity and understanding, for the harm that their code does

### Saying "No"
- "You were hired for your ability to say no. Any idiot can say yes, but it takes someone with considerable skills to say no."
- Don't be eager to say no, but don't be afraid to say no either
- By saying no at the right times, you can save your company untold amounts of money and time and effort
- If you're asked to commit and you decide that you can't, say no and describe your uncertainty
- Be willing to discuss options and workarounds
- Be willing to spend time hunting for a way to say yes
- One of the prime benefits you bring to your company is your ability to know when to say no

### Saying "Yes"
- If your boss asks you to get something done by a certain date, think long and hard about whether it's possible
- If it is possible, if you're sure you can do it, then by all means say yes
- When you say yes to a commitment, you set up a long domino chain of potential failure for you and your boss and your boss's boss and the whole company
- You are the one they're counting on

### The Danger of "Try"
- "Your boss may come to you one day, and sounding very reasonable, might ask if you would just please try."
- The answer is no: "I can't try. I'm already trying. How dare you imply that I am not trying?"
- "How dare you suggest that I am holding some kind of capacity in the back. I can't work miracles. There are no magic beans in my pocket with which to alter reality."
- If you say "yes, I'll try," you're lying because you have no idea what you're going to do differently
- There's no plan to change your behavior, no strategy
- You only said you'd try in order to get rid of them - that's fundamentally dishonest

### No Passive-Aggressive Behavior
- "There will be no passive-aggressive behavior on board this ship!"
- Every software developer who knew that something was wrong (like with healthcare.gov) and yet did nothing to stop the deployment shares part of the blame
- "One of the primary reasons you were hired is because you know. You know when things are about to go wrong. You know how to identify trouble before it happens."
- That means you have the responsibility to speak up before something terrible happens

## Estimation

### Estimates vs. Commitments
- An estimate is NOT a commitment
- "If you give them a date, then what you're really giving them is a commitment, not an estimate."
- "If you give them a commitment, you must meet it."
- "You don't dare make a promise to deliver something if you're not sure you can deliver it. To do so would be deeply dishonest."
- If you don't KNOW that you can make a date, don't offer that date as an estimate - offer a range of dates instead
- Offering a range of dates is much more honest

### The Most Honest Estimate
- The most honest estimate you can give is "I don't know"
- Unfortunately, that's neither very accurate nor precise
- The challenge is to quantify what we do know and what we don't

### Accuracy vs. Precision
- Accuracy: Give a range of dates you feel confident in
- Precision: Narrow the range down to your level of confidence
- Example: "Sometime between now and ten years from now" is perfectly accurate but lacks precision
- Example: "Yesterday at 2:15 a.m." is perfectly precise but not accurate if you haven't started
- A good, honest estimate is honest in both its accuracy and its precision

### Estimates Are Probability Distributions
- Estimates can't be single dates - they must be ranges
- Better yet, estimates are probability distributions
- Probability distributions have a mean (center point) and a width (standard deviation or sigma)

### PERT Estimation (Program Evaluation and Review Technique)
Invented in the late 1950s for the Polaris Fleet Ballistic Missile Program:

#### Three-Point Estimates
For each task, provide three estimates:
1. **Best Case (B)**: Everything goes right - 1% chance of being this fast
   - "You wake up every morning and have just the right breakfast cereal"
   - "Every line of code you write is absolutely perfect and compiles perfectly the first time"
   - "All tests always pass"
2. **Normal Case (N)**: The realistic estimate - 50% chance of being right/wrong
   - "How long you think the task would take if the average number of things went wrong the way it usually goes"
   - "A gut-level call"
3. **Worst Case (W)**: Murphy's Law - 99% chance of being done by this time
   - "Deeply pessimistic"
   - "Anything that can go wrong will go wrong"

#### PERT Formulas
- **Expected Time (mu)**: `(B + W)/2 + N) / 3` - weighted average giving the normal case weight of 2
- **Standard Deviation (sigma)**: `(W - B) / 6`
- Six sigma corresponds to 99%+ probability

#### Aggregating Estimates
- Expected time for the project = sum of all expected task times
- Standard deviations cannot be added directly - sum the squares of sigmas, then take the square root

### Work Breakdown Structure
- Finding the mean completion time is a matter of adding up mean times for all subtasks (recursive)
- We're generally not good at identifying all subtasks - we might miss half
- Compensate by multiplying the sum by 2, 3, or even 4 (the "Scotty factor")

#### The Scotty Factor
From Star Trek:
- Kirk: "Have you always multiplied your repair estimates by a factor of four?"
- Scotty: "Certainly, sir. How else can I keep my reputation as a miracle worker?"

### The Cost of Certainty
- The only way to really know how long something is going to take is to do it
- The cost of creating a complete work breakdown structure is equivalent to the cost of the project overall
- Increasing precision on the fudge factor is going to be very expensive
- Put your estimation effort into a time box

### How Wrong Estimates Can Be
Uncle Bob's personal stories demonstrate the range:

**Story 1: Off by Factor of Six**
- 1978, working at Teradyne on the COLT (Central Office Line Tester)
- Task: Make ROM chips independently deployable instead of requiring all 32 chips to be replaced for any code change
- Estimate: 2 weeks
- Actual: 12 weeks (6x longer)
- "It was a lot more complicated than I thought"

**Story 2: One-Twentieth the Expected Time**
- Same company, CCU-CMU project promised to phone companies
- Expected: Over a man-year of software
- Deadline: One month
- Solution: Found a "cheat" - the specific customer had the smallest possible configuration that eliminated virtually all complexity
- Actual: 2 weeks (special-purpose, one-of-a-kind unit called PCCU)

"These two stories are an example of the wild range that estimates can have. In one case, I was off by a factor of six... And in the other case, we managed to get to a solution in a twentieth of the expected time."

### Handling Pressure for Estimates
- Managers will ask how you came up with estimates
- When you tell them about the fudge factor, they'll ask you to reduce it
- This is fair - be willing to comply
- But communicate that increasing precision is expensive
- Sometimes superiors will try a different tactic: asking you to commit
- "They are trying to put the risk that they're supposed to be managing onto you"
- Don't let them bully you into saying yes when you know you shouldn't
- "Beware of the managers who try to cajole you into making a commitment that you know you shouldn't make"
- They might tell you you're not being a team player, not exhibiting proper commitment - don't be fooled

### Most Estimates Are Lies
- "Most estimates are lies because most estimates are constructed backwards from a known end date"
- Healthcare.gov example: Congress specified a fixed end date by law - "How absurd. Nobody was asked to actually estimate anything about the end date because they were told what the end date was by law."
- The programmers all referred to their project plan as "the laugh track"

## Working with Business

### Communication
- When things go wrong, speak up before something terrible happens
- You were hired because you know - you know when things are about to go wrong
- Communicate uncertainty honestly using ranges and probabilities
- Don't hide behind being "just a programmer"

### Managing Expectations
- Allow the people whose job it is to manage risk to manage the risk
- Don't take risk on yourself unless you are certain
- Risk management is their job - don't let them transfer it to you through commitments you can't keep

### Handling Conflicts
- Be willing to discuss options and workarounds
- Be willing to spend time hunting for a way to say yes
- But don't be afraid to say no
- Don't be passive-aggressive - speak up directly

## Do No Harm

### Harm to Society
- First, you will do no harm to the society in which you live
- The VW programmers broke this rule - their software lied and helped their employer but harmed society
- Healthcare.gov: A technical screw-up that put a huge public policy at risk - harm to society regardless of politics
- How do you know if you're harming society? "If it's within the law, it may still be harmful to society. Frankly, that's just a matter for your own judgment. You'll just have to make the best call you can."

### Harm to Function
- Know that your code works and will not harm
- Knight Capital: Technicians loaded software on 7 of 8 servers, leaving old Power Peg code active on the eighth
  - A repurposed flag activated dead code in an infinite loop
  - 45 minutes of bad trades
  - Lost $460 million (more than their $360 million in cash)
  - Bankrupt in 45 minutes
  - "They did not know what their system was going to do"
- Toyota: Uncontrollable acceleration killed up to 89 people
  - "The programmers who wrote that code did not know that their code would not kill"
  - They had 10,000 global variables
  - "They should have known that their code would not kill"

### Harm to Structure
- Don't harm the organization and content of the source code
- Anything that makes code hard to read, understand, change, or reuse is structural harm
- The previous videos covered code smells (from Fowler's Refactoring book)
- SOLID principles prevent structural harm between modules
- High-level architecture principles prevent harm at the highest level

### Risk and Knowledge
- "When the stakes are high, you have to drive your knowledge as close to perfection as you can get it"
- "If there are lives at stake, you have to know that you're not going to kill anybody"
- "If there are fortunes at stake, you have to know that you're not going to lose those fortunes"
- It's easy to underestimate the harm your code can do
- There's almost always much more at stake than you think

### Two Values of Software
1. **Behavior**: What the software does
2. **Structure/Softness**: How easy it is to change

**Which is greater?** Consider two programs:
- Program A: Does everything correctly but is impossible to change
- Program B: Does nothing correctly but is easy to change

Program B is more valuable because:
- Program A might as well be hardware
- When requirements change (and they will), Program A becomes useless forever
- Program B can be made to work and will continue to work because it's easy to change

Exception: In extremely urgent situations (like a cardiac pacemaker with 30 seconds to live), you need it to work right now.

### Startups Are Not an Exception
- A software startup is NOT an urgent situation requiring messy, inflexible software
- "The one thing that's absolutely certain about a software startup is that you are producing the wrong product"
- "No product survives contact with the users"
- If you can't change it because you made a mess, you're doomed
- "The mess slows them down long before they get to the finish line"
- "They'd get done a lot faster with a lot fewer problems if they just protected the structure of their system from harm"
- "When it comes to software, it never pays to rush"

## Test-Driven Development as Professional Standard

### The Coming Requirement
- "Is test-driven development really a prerequisite to professionalism? Am I really saying that you can't be a professional software developer if you don't practice test-driven development? Well, yeah. I believe that is true. Or rather, I believe it's becoming true."
- More and more developers believe TDD is part of a minimum set of disciplines and behaviors that mark professional software development
- "I think that the time is coming and relatively soon when that number will pass a majority"

### Why TDD Matters
- How can you prevent harm to structure without tests that show it works?
- How can you avoid harm to structure without tests that allow you to clean it?
- How can you guarantee your test suite is complete unless you follow the three laws of TDD?

### The Civilization Argument
- "We rule the world... Other people think they rule the world, but then they give those rules to us and we actually write those rules into the machines that make the whole world work."
- Nothing happens in society unless software is somehow mediating it
- Software has become the most critical component in the infrastructure of our civilization
- Society is beginning to realize that much of this software is being written by people who do not profess a minimum level of discipline

## The Coming Reckoning

### The Disaster That Is Coming
- "One day, probably not too long from now, some poor programmer is going to make a mistake and 10,000 people will die."
- "This isn't wild speculation. It's really just a matter of time."
- When this happens, politicians will point their fingers squarely at us
- Not at our bosses or companies (though they'll share scrutiny), but at us - because it was our fingers on the keyboards

### The Wrong Answer
If our answer is: "Well, like, man, you know, we really had to make our deadlines... We really had to be the market first... Our managers were really leaning on us hard to get things done" - that's not going to cut it.

### The Consequence
- Politicians will legislate and regulate our industry
- They'll tell us what languages, platforms, frameworks, and books to use
- What courses to take, what sign-offs to get, what reviews to do
- How to report compliance
- "We will become a regulated industry. Regulated by people who don't understand software. It will be hell!"

### The Solution
- We have one chance to avoid this: We have to get there first
- We must decide what our profession is, what our ethics are, what our disciplines are, what our minimum standards are
- We must decide how we're going to enforce that
- We need to create and defend a profession
- If we self-regulate, then when governments decide to regulate us, they'll just put the force of law behind what we are already doing
- "That's what doctors and lawyers did. They regulated themselves and then the government stepped in and backed them up."

## The History and Demographics of Programming

### Alan Turing's Vision (1945)
- The profession of software began in summer 1935 when Turing wrote his paper on the Einscheidungsproblem
- In 1945, Turing wrote the first programs for the ACE (Automated Computing Engine)
- His conclusions: "We shall need a great number of mathematicians of ability, because there will probably be a good deal of work of this kind to be done."
- And: "One of our difficulties will be the maintenance of an appropriate discipline so that we do not lose track of what we are doing."
- Seven decades ago, Turing laid the first stone of software professionalism: "Mathematicians of ability who maintain an appropriate discipline"

### Growth Trajectory
- 1945: ~1 computer, ~1 programmer (Turing)
- 1960: ~100 computers, ~1,000 programmers (scientists, mathematicians, engineers - already disciplined professionals in their 30s-50s)
- 1965: ~10,000 computers, ~100,000+ programmers (drawn from accountants, clerks, planners - mature professionals who understood business)
- 1975: ~1,000,000 computers, ~1,000,000 programmers (young CS graduates, mostly male, in their 20s)
- 2017+: Hundreds of millions of computers, hundreds of millions of programmers

### The Doubling Rate
- For the last 50 years, the number of programmers has doubled every ~5 years
- This means half of all programmers have less than 5 years experience
- This remains true as long as the doubling rate continues
- "This leaves the software industry in the precarious position of perpetual inexperience"

### The Mentorship Gap
- For every programmer with 30 years' experience, there's 63 others who need to learn from them
- Not enough experienced people to teach all the new ones coming in
- The same mistakes get repeated over and over

### The Shift in Society's Perception
- 1970s: Programmers seen as "Twinkie-eating nerdy geeks" - naive, inconsequential
- 1983 (War Games): Programmer as conduit of wisdom, computer as naive child
- 1993 (Jurassic Park): Denis Nedry - first time a programmer (not computer) was the villain
- 1999 (The Matrix): Programmers as saviors with godlike powers from reading code
- 2014: Programmers like Jeb and Notch are heroes to children, asked for autographs
- 2015 (Volkswagen): Programmers blamed publicly - villains in real life

## Stories and Anecdotes

### The Volkswagen Emissions Scandal
- Programmers wrote code that purposely thwarted EPA emissions tests
- Cars emitted 20 times the safe amount of nitrous oxides
- "Those programmers wrote harmful code. It was harmful because it was deceitful."
- CEO blamed "just some software engineers who put this in for whatever reason"
- "On my ship, those programmers would have been court-martialed and dishonorably discharged through the airlock. Even if they didn't know. Because they should have known."

### Healthcare.gov
- Congress mandated a specific date when the software had to be turned on
- On October 1st, 2013, they turned it on despite it not being ready
- "Do you think maybe there were some programmers that were hiding under their desks that day?"
- The law was nearly overturned over this technical failure
- "That harm on society was perpetrated by every software developer who maintained a passive-aggressive attitude towards their management"

### Knight Capital
- August 1, 2012: Technicians loaded new software on 7 of 8 servers
- An old feature called Power Peg had been disabled with a flag 8 years earlier
- The dead code was left in place rather than removed
- New software repurposed that flag
- When the flag turned on for the new purpose, the eighth server started making bad trades in an infinite loop
- 45 minutes to figure it out
- $7 billion in stock purchases promised
- $460 million loss
- Only had $360 million in cash
- Bankrupt

### Toyota Unintended Acceleration
- Software caused cars to accelerate uncontrollably
- As many as 89 people killed, many more injured
- "Imagine that you are driving your car through a busy downtown business district when suddenly your car begins to accelerate and there's nothing you can do to stop it"
- The code had 10,000 global variables
- "The programmers who wrote that code did not know that their code would not kill"

### Teradyne COLT Story (1978)
- Uncle Bob was 26, working on firmware for embedded measurement devices
- Intel 8085 processor, 32K RAM, 32K ROM (thirty-two 2708 chips)
- Any one-line change meant every chip changed, requiring field service worldwide
- Boss asked: make chips independently deployable
- Estimate: 2 weeks. Actual: 12 weeks (6x)
- "It was a lot more complicated than I thought"
- Boss didn't get mad - he was a programmer too, understood the complexities

### The CCU-CMU Miracle
- Product promised to customers years before, kept getting delayed
- Suddenly discovered a forgotten customer needed it in one month
- Expected effort: over a man-year
- Uncle Bob said it was impossible
- Boss had a "cheat" - smallest possible customer configuration eliminated virtually all complexity
- Result: Special-purpose PCCU unit delivered in 2 weeks

### The Project Manager Bursting In
- 20 years ago, Uncle Bob was consulting with a team
- Young project manager (about 25) burst into the room, visibly agitated
- Just returned from meeting with his boss
- Told the team: "We really have to make that date. I mean we really have to make that date."
- The rest of the team just rolled their eyes and shook their heads
- Estimates in that environment "are really just lies that support the plan"

### The Laugh Track
- Another client had their whole project plan on the wall
- Full of bubbles and arrows and tasks and labels
- "The programmers all referred to it as the laugh track"

### The Coffee Commercial
- Television commercial from the 70s with Mrs. Olson
- Husband portrayed as a nerdy programmer with glasses and pocket protectors
- Wife looked perfectly normal
- Mrs. Olson described the husband as a computer programmer, letting viewers know he was "a little odd and a bit of a nerd"
- She then schooled both of them on coffee economics
- Programmer cast as "naive, inconsequential, kind of nerdy... not the kind of person you'd want to invite to a party"

### Meeting Jeb at the Beer Garden
- 2014, Stockholm, visiting Mojang (Minecraft creators)
- After lectures on TDD and clean code, went to a beer garden
- A young boy (~12) ran up to the hedge
- Pointed at one of the programmers and asked "Are you Jeb?"
- Asked for autograph, peppered him with questions
- "The point is that programmers are now role models and heroes for our children"

## Memorable Quotes

### On Professionalism
- "You want to hold your head high and declare to the world that you are a professional. You want people to treat you with respect and look at you with deference. You want mothers pointing you out to their children and encouraging those children to be like you."
- "Be careful what you ask for."
- "Professionalism is certainly a badge of honor. But it's also a marker of accountability."
- "It's a lot easier being a non-professional."
- "When a professional makes a mess, the professional cleans it up."

### On Responsibility
- "It's your fingers on the keyboard. It's your code. You must know what it does."
- "Hiding behind requirements written by others is no excuse."
- "One of the primary reasons you were hired is because you know."
- "You know when things are about to go wrong. You know how to identify trouble before it happens."

### On Harm
- "The first rule of a software professional is do no harm."
- "Your code will do no harm to users. Your code will do no harm to customers. Your code will do no harm to your fellow programmers."
- "Messy software is harmful software."
- "The larger the mess, the less the certainty."

### On Saying No
- "You were hired for your ability to say no."
- "Any idiot can say yes, but it takes someone with considerable skills to say no."
- "By saying no at the right times, you can save your company untold amounts of money and time and effort."

### On Trying
- "I can't try. I'm already trying."
- "How dare you imply that I am not trying?"
- "There are no magic beans in my pocket with which to alter reality."

### On Estimates
- "Most estimates are lies because most estimates are constructed backwards from a known end date."
- "The most honest estimate you can give is 'I don't know.'"
- "Every estimate is wrong. That's why we call it an estimate. An estimate that's not wrong is not an estimate at all. It's a fact."
- "Estimating is cheating. The only way to really know how long something is going to take is to do it."

### On Software's Nature
- "The first word of software is soft. It's supposed to be soft. It's supposed to be easy to change."
- "If we didn't want it to be easy to change, we'd call it hardware."
- "No product survives contact with the users."
- "When it comes to software, it never pays to rush."

### On Our Role
- "We rule the world."
- "Other people think they rule the world, but then they give those rules to us and we actually write those rules into the machines that make the whole world work."
- "Nothing happens in our society unless software is somehow mediating it."

### On the Future
- "One day, probably not too long from now, some poor programmer is going to make a mistake and 10,000 people will die."
- "We will become a regulated industry. Regulated by people who don't understand software. It will be hell!"
- "We have one chance to avoid this. We have to get there first."

### On Demographics
- "This leaves the software industry in the precarious position of perpetual inexperience."
- "The same mistakes get repeated over and over and over again."

### From Alan Turing (1945)
- "We shall need a great number of mathematicians of ability, because there will probably be a good deal of work of this kind to be done."
- "One of our difficulties will be the maintenance of an appropriate discipline so that we do not lose track of what we are doing."

## Anti-patterns (Unprofessional Behaviors to Avoid)

### Passive-Aggressive Behavior
- Knowing something is wrong but staying silent
- "I'm just doing my job, it's their problem to deal with"
- Not speaking up when you see a project heading for disaster

### Making Commitments You Can't Keep
- Saying yes when you should say no
- Giving single dates instead of ranges
- Letting managers bully you into unrealistic promises

### Saying "I'll Try"
- Implying you haven't been giving full effort
- Having no plan to change behavior
- Lying to get someone to leave you alone

### Leaving Dead Code
- Not removing disabled features
- Repurposing flags without checking what they controlled
- Assuming old code paths are safe

### Making a Mess
- Writing tangled, hard-to-understand code
- Creating 10,000 global variables
- Sacrificing structure for speed
- Justifying mess-making by claiming urgency

### Hiding Behind Others
- "Requirements said to do it this way"
- "My manager told me to"
- "It's not my responsibility"

### Underestimating Stakes
- Thinking your code isn't important enough to do harm
- Forgetting how expensive software is to develop
- Not considering edge cases that could cause harm

### Constructing Estimates Backwards
- Starting with the deadline and working backward
- Creating "laugh track" project plans
- Treating estimates as lies that support the plan

### Transferring Risk Without Acknowledgment
- Accepting commitments without certainty
- Taking on risk that should be managed by others
- Not communicating uncertainty to stakeholders

### Not Learning from History
- Repeating the same mistakes
- Not studying disasters like Knight Capital, Toyota, VW
- Ignoring the lessons of perpetual inexperience

## Recommended Resources

### Books
- **Refactoring** by Martin Fowler - Contains the catalog of code smells
- **The Annotated Turing** by Charles Petzold - Every word of Turing's paper with explanations and historical context

### Principles to Study
- Code Smells (inappropriate intimacy, feature envy, refused bequest, shotgun surgery, etc.)
- SOLID Principles
- Principles of Component Cohesion and Coupling
- High-level Architecture Principles

## Review Process

When reviewing code or making decisions, consider:

1. **Professional Implications**
   - Am I taking responsibility for this code?
   - Do I know what this code does?
   - Do I know that this code works?
   - Could this code cause harm?

2. **Communication and Commitments**
   - Am I being honest about what I know and don't know?
   - Am I giving estimates or commitments?
   - Am I speaking up about problems I see?
   - Am I saying no when I should?

3. **Estimation Practices**
   - Am I providing ranges, not single dates?
   - Am I using three-point estimates (best/normal/worst)?
   - Am I being honest about uncertainty?
   - Am I allowing risk to be managed appropriately?

4. **Ethical Considerations**
   - Could this code harm users, customers, or society?
   - Am I hiding behind requirements?
   - Would I be comfortable if this code was publicly examined?
   - Am I upholding the honor of the profession?

5. **Professional Conduct**
   - Am I maintaining clean, changeable code?
   - Am I practicing TDD?
   - Am I learning and improving?
   - Am I helping others cover for me and covering for them?
   - Am I contributing to the profession or perpetuating problems?
