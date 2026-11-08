BASE = "https://husnainali847809-hub.github.io/TemplivoX"
EMAIL = "husnainali847809@gmail.com"
UPDATED = "2026-11-08"

CATS = [
    ("study", "Study Templates", "study-templates.html",
     "Weekly and daily study planners, exam preparation sheets, assignment trackers and class timetables for school and university."),
    ("budget", "Budget Planners", "budget-templates.html",
     "Monthly budgets, expense, savings and debt trackers and a shopping budget sheet to keep personal money organised."),
    ("daily", "Daily Planners", "daily-planners.html",
     "Daily, weekly and monthly planners plus a to-do list and a habit tracker for planning your time."),
    ("business", "Business Templates", "business-templates.html",
     "Invoices, quotations, receipts, meeting notes and a project planner for freelancers and small teams."),
    ("calendars", "Calendars", "calendars.html",
     "Printable monthly, weekly, yearly and blank calendars with Monday as the first day of the week."),
    ("personal", "Personal Templates", "personal-templates.html",
     "Meal planning, cleaning checklists, reading logs, goal planning and a daily checklist for home life."),
]
CATMAP = {c[0]: c for c in CATS}

WK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MON = ["Mon", "Tue", "Wed", "Thu", "Fri"]
INV = ["Description", "Qty", "Unit price", "Amount"]


def G(title, cols, n, **o):
    return ("grid", title, cols, n, o)


def L(title, n):
    return ("lines", title, n)


def C(title, n):
    return ("check", title, n)


TEMPLATES = []


def T(slug, title, cat, short, more, feats, how, fq, fa, spec, fmts=("pdf", "docx")):
    TEMPLATES.append(dict(slug=slug, title=title, cat=cat, short=short, more=more, feats=feats,
                          how=how, fq=fq, fa=fa, spec=spec, fmts=list(fmts)))


# ---------------- STUDY ----------------
T("weekly-study-planner", "Weekly Study Planner", "study",
  "Plan a full week of study sessions with one box for each day.",
  "Seven day boxes and a weekly goals panel help you spread subjects evenly, so revision never piles up on Sunday night.",
  ["One ruled box per day, Monday to Sunday", "Weekly goals panel for the big picture", "Fits on a single page"],
  "Write your main goal for the week first, then fill each day with the subject and the topic you will cover.",
  "How many subjects should I schedule per day?",
  "Two or three is realistic for most students. Short, focused sessions on fewer subjects usually work better than a crowded day.",
  dict(kind="days", fields=["Name", "Week of", "Main goal"], days=WK, extras=["Weekly goals"]))
T("daily-study-planner", "Daily Study Planner", "study",
  "Break a study day into hourly blocks with goals and review notes.",
  "An hour-by-hour schedule sits beside space for goals, a task checklist and end-of-day review notes.",
  ["Hourly schedule from 6:00 to 21:00", "Study goals and subject checklist", "Review notes area"],
  "List up to three goals, then block out study sessions and breaks in the schedule on the left.",
  "Can I change the hours on the schedule?",
  "Yes. The Word version is fully editable, so you can rewrite the time column to match your own routine.",
  dict(kind="schedule", fields=["Name", "Date"], start=6, end=21,
       panels=[("Study goals", 3, "num"), ("Subjects and tasks", 6, "check"), ("Review notes", 4, "lines")]))
T("exam-preparation-planner", "Exam Preparation Planner", "study",
  "Turn an exam syllabus into a revision plan you can tick off.",
  "List every topic, rank its priority, pick a revision date and mark it done, with room for past papers and an exam-day checklist.",
  ["Topic table with priority and study date", "Space for past papers and practice", "Exam-day checklist"],
  "Copy topics from your syllabus, mark the weakest as high priority, and schedule those first.",
  "When should I start planning revision?",
  "Many students start four to six weeks before an exam. Starting earlier simply gives you more time for past papers.",
  dict(kind="stack", fields=["Subject", "Exam date", "Target grade"],
       blocks=[G("Topics to revise", ["Topic", "Priority", "Study date", "Done"], 12, w=[3, 1, 1.3, .8]),
               L("Past papers and practice", 4), C("Exam-day checklist", 6)]))
T("assignment-tracker", "Assignment Tracker", "study",
  "Keep every deadline, status and grade in one table.",
  "Record each assignment with its subject, due date, status and grade, so nothing is submitted late.",
  ["Columns for subject, due date, status and grade", "Space for 18 assignments per page", "Spreadsheet version for sorting"],
  "Add assignments as they are set, then update the status column as you work.",
  "Is there a spreadsheet version?",
  "Yes. The XLSX file lets you sort by due date or filter by subject, which is handy for a long term.",
  dict(kind="stack", fields=["Name", "Term"],
       blocks=[G("Assignments", ["Subject", "Assignment", "Due date", "Status", "Grade"], 18, w=[1.3, 2.4, 1.1, 1, .8],
                 ex=["Biology", "Lab report", "2027-03-14", "In progress", ""])]),
  ("pdf", "docx", "xlsx"))
T("class-timetable", "Class Timetable", "study",
  "A Monday to Friday school timetable with nine periods.",
  "Fill in each period for the week, from first lesson to last, and keep the printout in your planner or on your desk.",
  ["Nine periods across five days", "Time column you can rewrite", "Spreadsheet version available"],
  "Write your period times in the first column, then add each subject and room.",
  "Can I add Saturday classes?",
  "In the Word or Excel version, add a column. The PDF has five weekdays only.",
  dict(kind="stack", fields=["Name", "Class", "Term"],
       blocks=[G("Weekly timetable", ["Time"] + MON, 9, w=[1] * 6, pre=["Period %d" % i for i in range(1, 10)],
                 ex=["08:00-08:45", "Maths", "English", "Science", "History", "Art"])]),
  ("pdf", "docx", "xlsx"))

# ---------------- BUDGET ----------------
T("monthly-budget-planner", "Monthly Budget Planner", "budget",
  "Compare planned and actual income and spending for the month.",
  "Separate income and expense tables show planned versus actual amounts, and the spreadsheet calculates every difference for you.",
  ["Income and expense tables", "Planned, actual and difference columns", "Formulas in the XLSX file"],
  "Enter planned amounts at the start of the month and actual amounts as you go.",
  "Does the spreadsheet do the maths?",
  "Yes. Differences and totals are formulas, so they update when you type in your numbers. Use any currency.",
  dict(kind="stack", fields=["Month", "Name"],
       blocks=[G("Income", ["Source", "Planned", "Actual", "Difference"], 5, num=[1, 2], calc={3: ("sub", 2, 1)},
                 ex=["Salary", "2500", "2500"]),
               G("Expenses", ["Category", "Planned", "Actual", "Difference"], 14, num=[1, 2], calc={3: ("sub", 1, 2)},
                 ex=["Rent", "900", "900"])]),
  ("pdf", "docx", "xlsx"))
T("expense-tracker", "Expense Tracker", "budget",
  "Log each purchase by date, category and payment method.",
  "A simple running log shows where money goes, and the spreadsheet adds up the amounts column automatically.",
  ["24 rows per page", "Category and payment method columns", "Auto-total in the XLSX file"],
  "Write each purchase the day it happens, then total the page at month end.",
  "How should I categorise expenses?",
  "Keep it to six to ten broad categories such as housing, food, transport and fun. Too many makes tracking tiring.",
  dict(kind="stack", fields=["Month", "Name"],
       blocks=[G("Expenses", ["Date", "Description", "Category", "Payment", "Amount"], 24, num=[4], w=[1, 2.2, 1.3, 1.2, 1],
                 ex=["2027-01-05", "Groceries", "Food", "Card", "42.50"])]),
  ("pdf", "docx", "xlsx"))
T("savings-tracker", "Savings Tracker", "budget",
  "Track deposits and withdrawals toward a savings goal.",
  "Note your target, then log each deposit or withdrawal. The spreadsheet keeps a running balance.",
  ["Goal and target fields", "Deposit, withdrawal and balance columns", "Running balance formula in XLSX"],
  "Write the goal and target date, then record each transaction and the new balance.",
  "What is a good savings goal to start with?",
  "A small emergency cushion, for example one month of essential costs, is a common first target.",
  dict(kind="stack", fields=["Goal", "Target amount", "Target date"],
       blocks=[G("Savings log", ["Date", "Deposit", "Withdrawal", "Balance", "Note"], 20, num=[1, 2], calc={3: ("cum", 1, 2)},
                 w=[1, 1, 1, 1, 2], ex=["2027-01-31", "200", "", "", "January deposit"])]),
  ("pdf", "docx", "xlsx"))
T("debt-tracker", "Debt Tracker", "budget",
  "List every debt with balance, interest rate and due date.",
  "See all balances on one page, note minimum payments, and tick off each debt as it is paid off.",
  ["Balance, rate and minimum payment columns", "Paid-off column", "Totals in the XLSX file"],
  "List each debt, then update the balance after every payment.",
  "Which debt should I pay first?",
  "Common methods are paying the highest rate first or the smallest balance first. Pick the one you will stick with.",
  dict(kind="stack", fields=["Name", "Date started"],
       blocks=[G("Debts", ["Creditor", "Balance", "Rate %", "Min. payment", "Due date", "Paid off"], 12, num=[1, 3],
                 w=[2, 1, .8, 1.1, 1, .9], ex=["Credit card", "1200", "19.9", "35", "2027-02-01", ""])]),
  ("pdf", "docx", "xlsx"))
T("shopping-budget", "Shopping Budget", "budget",
  "Plan a shopping trip against a fixed budget.",
  "Estimate each item, compare with the real price at the till, and see how close you stayed to the budget.",
  ["Estimated and actual price columns", "Got-it checkbox column", "Totals in the XLSX file"],
  "Fill in your budget, list items before you shop, and note actual prices as you go.",
  "Can I use it for groceries?",
  "Yes. It works for groceries, gifts, back-to-school lists or any trip with a spending limit.",
  dict(kind="stack", fields=["Store", "Date", "Budget"],
       blocks=[G("Shopping list", ["Item", "Qty", "Est. price", "Actual price", "Got it"], 22, num=[2, 3],
                 w=[2.4, .6, 1, 1, .7], ex=["Notebooks", "3", "9.00", "8.40", "Yes"])]),
  ("pdf", "docx", "xlsx"))

# ---------------- DAILY ----------------
T("daily-planner", "Daily Planner", "daily",
  "Schedule your day and focus on three priorities.",
  "An hourly schedule, a short priority list, a to-do checklist and a notes area fit on one page.",
  ["Hourly schedule from 6:00 to 21:00", "Top three priorities", "To-do list and notes"],
  "Pick three priorities first, then place them in your schedule before the smaller tasks.",
  "Is this suitable for work days?",
  "Yes. The layout suits work, study or home days, and the Word version lets you change the hours.",
  dict(kind="schedule", fields=["Date"], start=6, end=21,
       panels=[("Top 3 priorities", 3, "num"), ("To-do", 8, "check"), ("Notes", 5, "lines")]))
T("weekly-planner", "Weekly Planner", "daily",
  "See the whole week on one page with focus and notes boxes.",
  "Seven day boxes, a weekly focus box and a notes box give you a calm overview of the week ahead.",
  ["Seven day boxes", "Weekly focus and notes", "One page, easy to pin up"],
  "Set your weekly focus, then add fixed appointments to each day before the flexible tasks.",
  "How is this different from the weekly calendar?",
  "The planner has open boxes for tasks and notes. The weekly calendar is a time-based grid for scheduling hours.",
  dict(kind="days", fields=["Week of"], days=WK, extras=["Weekly focus"]))
T("monthly-planner", "Monthly Planner", "daily",
  "A month grid with a goals box for planning ahead.",
  "Write the month and year, number the days, then use the notes lines below for goals and reminders.",
  ["Large day cells", "Monthly goals lines", "Works for any month of any year"],
  "Number the days for your month, mark deadlines first, then add appointments.",
  "Why are the dates not filled in?",
  "So you can use it for any month and year. Choose the Word version if you want to type the dates in.",
  dict(kind="month", fields=["Month", "Year"], notes=("Monthly goals and notes", 4)))
T("to-do-list", "To-Do List", "daily",
  "A printable checklist split into today, this week and later.",
  "Sorting tasks by urgency stops long lists from feeling overwhelming, and the checkboxes make progress visible.",
  ["Three lists by urgency", "Checkbox on every line", "Plain, ink-friendly layout"],
  "Put only the tasks you really intend to finish today in the first list.",
  "Can I edit the headings?",
  "Yes. Open the Word file and rename the sections, for example into work, home and errands.",
  dict(kind="stack", fields=["Date"], blocks=[C("Today", 10), C("This week", 8), C("Later", 6)]))
T("habit-tracker", "Habit Tracker", "daily",
  "Mark each habit for every day of the month.",
  "A grid of up to fourteen habits across thirty-one days makes streaks easy to see at a glance.",
  ["Fourteen habit rows", "Columns for days 1 to 31", "Spreadsheet counts completed days"],
  "Write your habits in the left column, then mark an X each day you complete one.",
  "How many habits should I track?",
  "Start with three to five. You can always add more once those feel automatic.",
  dict(kind="habit", fields=["Month", "Name"], rows=14, notes=("Reflections", 3)),
  ("pdf", "docx", "xlsx"))

# ---------------- BUSINESS ----------------
T("invoice-template", "Invoice Template", "business",
  "A clean invoice with line items, tax and a total.",
  "Fill in your details, add the items and the spreadsheet works out line amounts, tax and the final total.",
  ["Seller and client fields", "Quantity, price and amount columns", "Tax and total formulas in XLSX"],
  "Enter your details and the invoice number, add one line per item, and send the file as a PDF.",
  "Is this invoice legally valid everywhere?",
  "Invoice requirements differ by country. Check what your tax authority requires, such as tax numbers, before sending.",
  dict(kind="stack", fields=["From", "Bill to", "Invoice no.", "Invoice date", "Due date"],
       blocks=[G("Items", INV, 10, num=[], calc={3: ("mul", 1, 2)}, w=[3, .8, 1.2, 1.2], ex=["Logo design", "1", "300"]),
               ("totals",)]),
  ("pdf", "docx", "xlsx"))
T("business-quotation", "Business Quotation", "business",
  "Send a clear price quote before the work begins.",
  "Describe the work, list prices, state how long the quote is valid and add terms in one tidy document.",
  ["Quote number and validity date", "Itemised price table", "Terms and notes section"],
  "List each item or service, check the total, and state until when the prices hold.",
  "How long should a quote stay valid?",
  "Thirty days is common, but choose a period that fits how quickly your costs can change.",
  dict(kind="stack", fields=["Prepared for", "Quote no.", "Date", "Valid until"],
       blocks=[G("Quoted items", INV, 8, num=[], calc={3: ("mul", 1, 2)}, w=[3, .8, 1.2, 1.2], ex=["Website design", "1", "850"]),
               ("totals",), L("Terms and notes", 3)]),
  ("pdf", "docx", "xlsx"))
T("meeting-notes", "Meeting Notes", "business",
  "Capture agenda, discussion and action items in one place.",
  "Record who attended, what was decided and who owns each follow-up, so meetings lead to action.",
  ["Meeting details and attendees", "Agenda and discussion notes", "Action table with owner and due date"],
  "Fill in the agenda before the meeting and the action table while people are still in the room.",
  "Should I share the notes afterwards?",
  "Yes. Sending the action items within a day keeps owners accountable.",
  dict(kind="stack", fields=["Meeting", "Date", "Attendees", "Facilitator"],
       blocks=[L("Agenda", 5), L("Discussion notes", 8), G("Action items", ["Action", "Owner", "Due", "Status"], 6, w=[3, 1.2, 1, 1])]))
T("project-planner", "Project Planner", "business",
  "Break a project into tasks, owners and deadlines.",
  "List milestones with owners and dates, track their status and note risks so the team sees what is next.",
  ["Task, owner, start, due and status columns", "Risks and notes section", "Spreadsheet version for sorting"],
  "List the main tasks, give each one an owner and a due date, then update the status each week.",
  "Is this enough for a large project?",
  "It suits small projects and personal plans. Large projects usually need dedicated project management software.",
  dict(kind="stack", fields=["Project", "Owner", "Start", "End"],
       blocks=[G("Tasks and milestones", ["Task", "Owner", "Start", "Due", "Status"], 14, w=[2.6, 1.1, 1, 1, 1],
                 ex=["Draft proposal", "Sam", "2027-02-01", "2027-02-05", "Done"]), L("Risks and notes", 4)]),
  ("pdf", "docx", "xlsx"))
T("receipt-template", "Receipt Template", "business",
  "Give a customer proof of payment in a simple layout.",
  "Note who paid, how they paid and what for. Totals are calculated in the spreadsheet version.",
  ["Payer and payment method fields", "Itemised amounts", "Subtotal, tax and total"],
  "Fill in the receipt number and date, list what was paid for, and note the payment method.",
  "What should a receipt include?",
  "At least the date, seller, buyer, items, amounts and payment method. Some countries require more.",
  dict(kind="stack", fields=["Receipt no.", "Date", "Received from", "Payment method"],
       blocks=[G("Paid for", INV, 8, num=[], calc={3: ("mul", 1, 2)}, w=[3, .8, 1.2, 1.2], ex=["Consulting hour", "2", "60"]),
               ("totals",)]),
  ("pdf", "docx", "xlsx"))

# ---------------- CALENDARS ----------------
T("monthly-calendar", "Monthly Calendar", "calendars",
  "A printable month grid with Monday as the first day.",
  "Write the month, add the dates, and use the notes strip at the bottom for reminders.",
  ["Monday to Sunday columns", "Large writing cells", "Notes strip at the bottom"],
  "Write the month and year, number the first day in the correct column, then continue across.",
  "Can I start the week on Sunday?",
  "Not in the PDF. In the Word version, move the Sunday column to the front.",
  dict(kind="month", fields=["Month", "Year"], notes=("Notes", 2)))
T("yearly-calendar", "Yearly Calendar 2027", "calendars",
  "All twelve months of 2027 on a single page.",
  "A compact overview for planning holidays, school terms and deadlines across the whole year.",
  ["Twelve months on one page", "Weeks start on Monday", "Dated for 2027"],
  "Pin it up and circle key dates such as holidays, exams or launches.",
  "Does it include public holidays?",
  "No, because holidays differ by country. Add your own dates by hand.",
  dict(kind="year", year=2027))
T("weekly-calendar", "Weekly Calendar", "calendars",
  "A time-based grid for scheduling each hour of the week.",
  "Rows run from 8:00 to 21:00 and columns from Monday to Sunday, which helps you see free slots.",
  ["Hourly rows", "Seven day columns", "Landscape-friendly Word version"],
  "Fill fixed commitments first, then place flexible tasks in the gaps.",
  "Can I change the start time?",
  "Yes. Edit the first column in the Word file to fit your day.",
  dict(kind="stack", fields=["Week of"],
       blocks=[G("Schedule", ["Time"] + MON + ["Sat", "Sun"], 14, w=[.9] + [1] * 7,
                 pre=["%02d:00" % h for h in range(8, 22)])]))
T("blank-calendar", "Blank Calendar", "calendars",
  "A completely open month grid for any layout you need.",
  "No printed month name or dates, just a big grid. Use it for content plans, shift rotas or school terms.",
  ["Big empty cells", "Fits any month or custom period", "Prints well in black and white"],
  "Write your own title at the top, number the cells from any starting day, and fill in the plan.",
  "How is it different from the monthly calendar?",
  "It has no notes strip, so the cells are larger. Use it for rotas, content plans or four-week cycles.",
  dict(kind="month", fields=["Title"], notes=None, plain=True))

# ---------------- PERSONAL ----------------
T("meal-planner", "Meal Planner", "personal",
  "Plan breakfast, lunch, dinner and snacks for the week.",
  "Plan meals first, then write a grocery list from them. It reduces food waste and last-minute takeaways.",
  ["Seven days by four meals", "Grocery checklist", "Spreadsheet version available"],
  "Fill dinners first, then lunches, then check what you already have before writing the grocery list.",
  "Can I plan for a family?",
  "Yes. Use the notes in each cell for portions or dietary needs.",
  dict(kind="stack", fields=["Week of"],
       blocks=[G("Weekly meals", ["Day", "Breakfast", "Lunch", "Dinner", "Snacks"], 7, w=[1.1, 1.5, 1.5, 1.5, 1.2], pre=WK,
                 ex=["Monday", "Oats", "Salad", "Pasta", "Fruit"]), C("Grocery list", 8)]),
  ("pdf", "docx", "xlsx"))
T("cleaning-checklist", "Cleaning Checklist", "personal",
  "Daily, weekly and monthly cleaning tasks in one list.",
  "Splitting chores by how often they need doing keeps a home tidy without long weekend marathons.",
  ["Daily, weekly and monthly sections", "Checkbox on every line", "Editable Word version for your own chores"],
  "Write your own chores on the lines, then tick them off each period.",
  "Are the chores pre-filled?",
  "No. Every household differs, so the lines are blank for your own list.",
  dict(kind="stack", fields=["Week of"], blocks=[C("Daily", 5), C("Weekly", 8), C("Monthly", 6)]))
T("reading-tracker", "Reading Tracker", "personal",
  "Log the books you read with dates, ratings and notes.",
  "Keep a record of what you started, finished and thought about each book.",
  ["Title, author, dates and rating columns", "Notes column", "Spreadsheet version for a long list"],
  "Add a book when you start it and write the finish date and rating when you are done.",
  "Can I use it for a reading challenge?",
  "Yes. Count the finished rows to see your progress toward a yearly goal.",
  dict(kind="stack", fields=["Name", "Year"],
       blocks=[G("Books", ["Title", "Author", "Started", "Finished", "Rating", "Notes"], 16, w=[2.2, 1.5, 1, 1, .8, 1.8],
                 ex=["Sapiens", "Y. N. Harari", "2027-01-02", "2027-01-20", "4/5", "Great history"])]),
  ("pdf", "docx", "xlsx"))
T("personal-goal-planner", "Personal Goal Planner", "personal",
  "Turn one goal into steps, deadlines and habits.",
  "Define the goal, list action steps with dates, anticipate obstacles and decide how you will celebrate.",
  ["Main goal section", "Action steps with deadlines", "Obstacles and rewards"],
  "Write one goal in a sentence, then list the next small steps with realistic dates.",
  "How many goals should I set?",
  "One to three at a time. Use one planner per goal.",
  dict(kind="stack", fields=["Name", "Period"],
       blocks=[L("My main goal", 2), G("Action steps", ["Step", "Deadline", "Done"], 6, w=[3, 1.2, .8]),
               L("Obstacles and solutions", 3), L("How I will celebrate", 2)]))
T("daily-checklist", "Daily Checklist", "personal",
  "A short checklist for morning, afternoon and evening.",
  "Three blocks of tick-boxes build a gentle routine, with a notes area for anything left over.",
  ["Morning, afternoon and evening blocks", "Checkbox on every line", "Notes area"],
  "Write the same few routine tasks in each block and tick them off through the day.",
  "How is it different from the to-do list?",
  "It is organised by time of day to support routines, not by urgency.",
  dict(kind="stack", fields=["Date"], blocks=[C("Morning", 5), C("Afternoon", 5), C("Evening", 5), L("Notes", 3)]))

BY = {t["slug"]: t for t in TEMPLATES}
LATEST = ["yearly-calendar", "habit-tracker", "monthly-budget-planner", "personal-goal-planner"]
FEATURED = ["weekly-study-planner", "monthly-budget-planner", "daily-planner", "invoice-template", "monthly-calendar", "meal-planner"]
assert len(TEMPLATES) == 29
