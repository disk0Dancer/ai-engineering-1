import typing as t

from kb_chat.domain.models import TopicContent

DEFAULT_TOPICS: t.Mapping[str, TopicContent] = {
    "vacation": TopicContent(
        topic="vacation",
        content="""
Vacation Policy:
- Employees get 28 calendar days of paid vacation per year
- Vacation must be requested at least 2 weeks in advance
- Maximum consecutive vacation is 14 days
- Unused vacation days can be carried over (max 10 days)
- Contact HR for special circumstances
""",
    ),
    "sick_leave": TopicContent(
        topic="sick_leave",
        content="""
Sick Leave Policy:
- First 3 days: provide self-certification
- 4+ days: medical certificate required
- Sick leave is paid at 100% for first 10 days
- After 10 days: 80% of salary
- Notify your manager as soon as possible
""",
    ),
    "expenses": TopicContent(
        topic="expenses",
        content="""
Expense Policy:
- Submit expenses within 30 days
- Receipts required for amounts over $10
- Travel expenses: book through corporate portal
- Meals during business trips: up to $25/day
- Approval required for expenses over $10
""",
    ),
    "remote_work": TopicContent(
        topic="remote_work",
        content="""
Remote Work Policy:
- Hybrid model: 3 days office, 2 days remote
- Core hours: 10:00 - 16:00 (must be available)
- VPN required for remote access
- Weekly team sync mandatory
- Equipment provided by company
""",
    ),
}
