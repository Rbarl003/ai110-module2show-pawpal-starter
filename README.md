# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

----------------------------------------
            TODAY'S SCHEDULE            
             Owner: Jordan              
----------------------------------------

🐾 Biscuit — dog
   [ ] Morning walk          30 min
   [ ] Feeding               10 min

🐾 Mochi — cat
   [ ] Feeding                5 min

----------------------------------------
Total: 3 tasks, 45 minutes of care today.
----------------------------------------


## 🧪 Testing PawPal+

Run the tests from the project root:

```bash
python -m pytest
```

The tests check the parts that matter most: tasks sort into the right order,
filtering by pet and status works, finishing a daily task schedules the next
day, and two tasks booked at the same time get flagged as a conflict. A few
also cover the tricky bits — an empty schedule, a pet with no tasks, and a
badly formatted time.

Successful run:

```
============================= test session starts ==============================
platform darwin -- Python 3.13.9, pytest-8.4.2, pluggy-1.5.0
rootdir: /Users/ritchbarlatier/Downloads/ai110-module2show-pawpal-starter-main
plugins: anyio-4.10.0
collected 41 items

tests/test_pawpal.py .........................................           [100%]

============================== 41 passed in 0.02s ==============================
```

**Confidence Level: ★★★★☆ (4/5)**

All 41 tests pass and cover every core feature plus the edge cases most likely
to trip up a scheduler. Writing them even caught and fixed a real bug (sorting
used to crash on a bad time). Not a full 5 because a couple of things aren't
handled yet — tasks that cross midnight, and the Streamlit UI has no tests.

## 📐 Smarter Scheduling

The scheduling logic lives on the `Scheduler` class in `pawpal_system.py`. Here's
what I built and where each part lives.

**Sorting** — `Scheduler.sorted_by_time()` sorts tasks by how long they take
(shortest first, or longest with `ascending=False`). `Scheduler.sorted_by_start_time()`
sorts them by time of day.

**Filtering** — `Scheduler.filter_tasks()` filters tasks by pet, by completion
status, or by frequency. You can pass a pet name or leave an argument out to
skip that filter.

**Conflict detection** — `Scheduler.detect_conflicts()` finds tasks whose times
overlap (including two booked at the same minute). `Scheduler.conflict_warnings()`
turns those into plain warning messages instead of crashing.

**Recurring tasks** — `Scheduler.complete_task()` marks a task done and, if it's
daily or weekly, automatically adds the next one. `Task.next_occurrence()` works
out the new date with `timedelta`.

## 📸 Demo Walkthrough

Run the app with `streamlit run app.py` (or the quick text demo with `python main.py`),
then follow along:

1. **Set the owner.** Type the owner's name — say **Jordan**.
2. **Add a pet.** Give it a name and species, like **Biscuit** the dog.
3. **Add a task.** Pick the pet, then enter a title, how long it takes, daily or
   weekly, and a start time — e.g. **Morning walk**, 30 min, daily, at **08:00**.
4. **Add another at the same time.** Add **Medication** at **08:00** too, so there's
   a clash to catch.
5. **Find tasks.** Use the filters to narrow the list by pet, status, or frequency.
6. **Build the schedule.** Choose "time of day" (or shortest/longest first) and
   generate it. PawPal+ lists the tasks in order and warns at the top that the walk
   and medication clash at 08:00 — you can't be in two places at once.
7. **Check a task off.** In *Today's Tasks*, mark the walk done. Because it's daily,
   PawPal+ quietly schedules tomorrow's walk for you.

Those steps show the key Scheduler behaviors: **sorting** the day, **filtering**
tasks, a **conflict warning** for overlapping times, and **recurrence** when a daily
task rolls over.

Here's what the text demo (`python main.py`) prints:

```
------------------------------------------------
             PAWPAL+ SCHEDULE DEMO
                 Owner: Jordan
------------------------------------------------

Sorted by TIME OF DAY:
   [ ] 08:00  Morning walk          30 min
   [ ] 08:00  Medication            10 min
   [✓] 08:15  Feeding                5 min
   [ ] 08:20  Feeding               10 min
   [ ] 09:00  Vet visit             60 min
   [ ]   —    Nap check              2 min

Conflict check:
   ⚠️ Biscuit: Morning walk (08:00) is scheduled at the same time as Mochi: Medication (08:00), Mochi: Feeding (08:15), Biscuit: Feeding (08:20)

Completing a recurring task:
   Marking 'Morning walk' complete on 2026-07-07...
   ↻ Auto-scheduled next 'Morning walk' (daily) due 2026-07-08.

------------------------------------------------
5 tasks still to do, 112 minutes of care remaining.
------------------------------------------------
```

