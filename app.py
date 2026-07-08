import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")

# --- Persist the Owner in the session "vault" so it survives reruns ---
# Streamlit reruns this whole script on every click. Without this check, the
# Owner would be re-created (and emptied) every time. So we create it ONCE.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)

owner = st.session_state.owner   # reuse the same Owner every rerun
owner.name = owner_name

st.divider()

# --- Add a Pet ---------------------------------------------------------------
st.subheader("Add a Pet")
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    add_pet = st.form_submit_button("Add pet")

if add_pet:
    # Owner.add_pet() is the method that handles the new pet data.
    owner.add_pet(Pet(pet_name, species))
    st.success(f"Added {pet_name} ({species}).")

if owner.pets:
    st.write("Your pets:", ", ".join(pet.describe() for pet in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add a Task --------------------------------------------------------------
st.subheader("Add a Task")
if not owner.pets:
    st.info("Add a pet first, then you can schedule tasks for it.")
else:
    with st.form("add_task_form"):
        # Pick which pet the task belongs to.
        pet_choice = st.selectbox(
            "For which pet?",
            options=range(len(owner.pets)),
            format_func=lambda i: owner.pets[i].describe(),
        )
        task_title = st.text_input("Task title", value="Morning walk")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        frequency = st.selectbox("Frequency", ["daily", "weekly"])
        start_time = st.time_input("Start time (optional)", value=None)
        add_task = st.form_submit_button("Add task")

    if add_task:
        # Pet.add_task() handles attaching the new task to that pet.
        chosen_pet = owner.pets[pet_choice]
        start = start_time.strftime("%H:%M") if start_time else None
        chosen_pet.add_task(Task(task_title, int(duration), frequency, start_time=start))
        st.success(f"Added '{task_title}' for {chosen_pet.name}.")

    # Show each pet's current tasks.
    for pet in owner.pets:
        if pet.tasks:
            st.write(f"**{pet.describe()}** tasks:")
            st.table(
                [{"title": t.description, "minutes": t.time, "frequency": t.frequency} for t in pet.tasks]
            )

st.divider()

# --- Search / Filter Tasks ---------------------------------------------------
st.subheader("Find Tasks")
if not owner.pets:
    st.info("Add a pet and a task first to search.")
else:
    scheduler = Scheduler(owner)
    col1, col2, col3 = st.columns(3)
    with col1:
        name_query = st.text_input("Pet name (blank = all pets)", value="")
    with col2:
        status = st.selectbox("Status", ["all", "to do", "done"])
    with col3:
        freq_choice = st.selectbox("Frequency", ["all", "daily", "weekly"])

    completed = {"all": None, "to do": False, "done": True}[status]
    matches = scheduler.filter_tasks(
        pet=name_query.strip() or None,       # blank box = don't filter by pet
        completed=completed,
        frequency=None if freq_choice == "all" else freq_choice,
    )

    if matches:
        st.table(
            [
                {
                    "pet": scheduler.pet_of(t).name if scheduler.pet_of(t) else "—",
                    "task": t.description,
                    "time of day": t.start_time or "—",
                    "minutes": t.time,
                    "frequency": t.frequency,
                    "status": "✅ done" if t.completed else "🔲 to do",
                }
                for t in matches
            ]
        )
    else:
        st.info("No tasks match that filter.")

st.divider()

# --- Build Schedule ----------------------------------------------------------
st.subheader("Build Schedule")
st.caption("Uses the Scheduler to gather all tasks across the owner's pets.")

order = st.radio(
    "Order tasks by",
    ["time of day", "shortest first", "longest first"],
    horizontal=True,
)

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    if order == "time of day":
        tasks = scheduler.sorted_by_start_time()
    else:
        tasks = scheduler.sorted_by_time(ascending=(order == "shortest first"))

    if not tasks:
        st.warning("Add at least one pet and task first.")
    else:
        st.success(f"Schedule for {owner.name}")

        # --- Conflicts FIRST, up top, where the owner can't miss them. ------
        # A pet owner needs to act on a clash *before* reading the plan, so we
        # surface it prominently as an amber warning (not a red error — the day
        # isn't broken, it just needs a nudge) with each clash on its own line.
        warnings = scheduler.conflict_warnings()
        if warnings:
            st.warning(
                f"**Heads up — {len(warnings)} scheduling conflict"
                f"{'s' if len(warnings) > 1 else ''}.** "
                "These tasks overlap, and you can't be in two places at once. "
                "Consider moving one of each pair:"
            )
            for message in warnings:
                st.markdown(f"- {message}")
        else:
            st.caption("✓ No conflicts — every task has room in the day.")

        # --- The plan itself, as a clean table. ------------------------------
        st.table(
            [
                {
                    "time": t.start_time or "anytime",
                    "pet": scheduler.pet_of(t).name if scheduler.pet_of(t) else "—",
                    "task": t.description,
                    "minutes": t.time,
                    "frequency": t.frequency,
                }
                for t in tasks
            ]
        )

        total = sum(task.time for task in tasks)
        st.info(f"Total care time: {total} minutes across {len(tasks)} tasks.")

st.divider()

# --- Today's Tasks (mark done + auto-recurrence) -----------------------------
st.subheader("Today's Tasks")
st.caption("Check off a task as you finish it — recurring ones reschedule themselves.")

if not owner.pets:
    st.info("Add a pet and a task first.")
else:
    scheduler = Scheduler(owner)
    todo = scheduler.pending_tasks()

    if not todo:
        st.success("🎉 All done for now — nothing left on the to-do list.")
    else:
        # One row per pending task: label on the left, a Done button on the right.
        for i, task in enumerate(todo):
            left, right = st.columns([4, 1])
            with left:
                st.write(f"**{scheduler.describe_task(task)}** — {task.time} min ({task.frequency})")
            with right:
                # id(task) keeps the key stable + unique even for same-named tasks.
                if st.button("✓ Done", key=f"done_{id(task)}_{i}"):
                    upcoming = scheduler.complete_task(task)
                    if upcoming:
                        st.success(
                            f"Nice! Marked done and rescheduled the next "
                            f"'{upcoming.description}' for {upcoming.due_date}."
                        )
                    else:
                        st.success(f"Marked '{task.description}' done.")
                    st.rerun()   # refresh the list so the finished task drops off
