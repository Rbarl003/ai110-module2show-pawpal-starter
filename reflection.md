# PawPal+ Project Reflection

## 1. System Design
** Core user action

1. ADD a pet - enter the pet's name and type.
2. ADD a task - add a care task like a walk or feeding, with how long it takes and how important it is.
3. SEE today's plan - press a button to get a daily schedule of task in order.

**a. Initial design**

- Briefly describe your initial UML design.
My first UML design had four classes:
PET - holds the pet's name and type.
TASK - holds one care task: its title, how long it takes, and its priority.
Owner - holds the owner's name and how much time they have that day.
Scheduler - takes the tasks and the owner's time and builds the daily plan.

- What classes did you include, and what responsibilities did you assign to each?

I made Pet, Task, and Owner simple classes that just hold info, and let the Scheduler do the actual work of picking and ordering tasks into a plan.

**b. Design changes**

- Did your design change during implementation?

Yes, my design changed. At first my four classes didn't connect to each other, so I fixed three things:

- If yes, describe at least one change and why you made it.

1. I gave Owner a list of its pets, and each Pet holds its own tasks, so the data
   actually connects: Owner → Pet → Task. Owner can also gather every task across
   all its pets in one call.
2. I made Scheduler take the Owner instead of a separate time number, so everything
   lives in one place and the Scheduler can reach all the tasks through the owner.
3. Instead of a separate Plan class, I kept it simpler: the Scheduler builds the plan
   on the fly — it returns the tasks in sorted order and produces conflict warnings —
   rather than storing a finished plan object.

I did this because the original classes couldn't talk to each other, so there was no
way to build a real plan.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

My scheduler looks at two things: how long each task takes, and what time of day
it's set for. It can order the day by start time or by how long a task takes, and
it checks whether any two tasks overlap. It also tracks how often a task repeats
(daily or weekly) so it knows when the next one is due.

- How did you decide which constraints mattered most?

Time mattered most. A pet owner's real problem is fitting everything into the day
without double-booking themselves, so I focused on start times and durations first
and made conflict detection the main safety check.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

My scheduler warns about any two tasks that overlap in time, even if they belong
to different pets. I did this because one person can't really walk the dog and
feed the cat at the same minute. The downside is it sometimes warns when it
doesn't need to, like a nap that I don't have to sit there for. I figured it's
better to get an extra warning than to miss a real clash and forget to feed a pet.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

I used my AI coding assistant across the whole project, but in stages: brainstorming
the classes, writing tests, cleaning up the app UI, and fixing the UML. The features
that helped me most were:

1. Asking it to draft a **test plan** first ("what edge cases matter for a pet
   scheduler?"). That gave me a checklist before I wrote any test code.
2. Having it **write and then run the tests** so I could see them pass or fail right
   away instead of guessing.
3. Using it to **explain code back to me** in plain English before I saved it, so I
   wasn't pasting in things I didn't understand.

- What kinds of prompts or questions were most helpful?

Specific ones. "What are the most important edge cases for a scheduler with sorting
and recurring tasks?" got a much better answer than just "write tests." Asking it to
explain *why* it made a choice was also useful, because that's where I caught things
I disagreed with.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

When we tested sorting, the assistant found that `sorted_by_start_time` would crash
on a badly typed time like "8am," while conflict detection just skipped bad times.
Its first move was to write a test that simply expected the crash. I didn't want that
— it left two parts of the system behaving differently for no good reason. So I had
it change the sorting code to skip bad times too (reusing the helper that was already
there), so the whole system handles messy input the same way. That kept the design
consistent instead of just documenting a rough edge.

- How did you evaluate or verify what the AI suggested?

I ran the tests every time (`python -m pytest`) and ran `python main.py` to watch the
real output. One test the AI wrote actually failed because its guess about how
grouped conflicts collapse was wrong — the failing test proved the code was right and
its assumption was off. That reminded me to trust the run, not the explanation.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

I tested the four main behaviors: sorting (by time of day and by duration),
filtering (by pet, status, and frequency), recurrence (finishing a daily task
creates the next day's task), and conflict detection (two tasks at the same time get
flagged). I also tested edge cases like an empty schedule, a pet with no tasks, and a
badly formatted time. It ended up being 41 tests, all passing.

- Why were these tests important?

Those are the parts a real user would notice if they broke. If the schedule sorts
wrong or misses a conflict, the whole point of the app falls apart. The edge cases
matter because that's usually where things crash.

**b. Confidence**

- How confident are you that your scheduler works correctly?

Pretty confident — about 4 out of 5. Every core feature is tested and passing, and
writing the tests even caught a real bug in the sorting code. I dropped a star
because a couple of things still aren't handled, and the Streamlit UI itself has no
automated tests.

- What edge cases would you test next if you had more time?

Tasks that cross midnight (like 11:50 PM plus 30 minutes), and what should happen with
a task frequency the app doesn't know about. I'd also add some tests for the app's UI.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The conflict detection. It handles the tricky cases — two tasks at the exact same
minute, tasks on different pets, and messy input — and turns them into a plain
warning a normal person can read. I'm also happy the test suite actually caught a bug
instead of just rubber-stamping the code.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I'd add the Plan idea I had in my UML but never fully built — an object that holds the
finished schedule, including which tasks got skipped and why. Right now the app shows
the plan but doesn't really "explain" it. I'd also handle tasks that run past midnight.

- How did using separate chat sessions for different phases help you stay organized?

I kept separate chats for the different phases — one for testing, one for the UI, one
for the diagram and docs. It kept each conversation focused, so the assistant wasn't
mixing UI questions into a testing discussion. When I came back to a phase, the whole
history for just that part was right there, which made it easy to pick up where I left
off instead of scrolling through everything at once.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned what it means to be the "lead architect" instead of just letting the AI
drive. The assistant is fast and knows a lot, but it doesn't know what I actually want
the system to be — it happily wrote a test that just accepted a crash, and it guessed
wrong about my own code once. My job was to set the direction, ask why, and check
every suggestion by running it. The AI is great at doing the work, but the decisions —
what's clean, what's consistent, what matters to the user — still have to be mine.
