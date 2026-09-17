import frappe
from frappe.utils import get_datetime, get_time
from datetime import datetime


def sync_activities(doc, method):
    """
    Automatically called every time a Daily Timesheet is saved.
    Deletes old activities belonging to this document, then recreates them
    from the contents of the 'activities' child table - each row uses its own date.
    """

    frappe.db.delete("Daily Timesheet Activity", {"parent_daily_timesheet": doc.name})

    for row in doc.activities:
        if not row.date or not row.from_time or not row.to_time:
            continue

        base_date = get_datetime(row.date).date()
        from_time_obj = get_time(row.from_time)
        to_time_obj = get_time(row.to_time)

        from_dt = datetime.combine(base_date, from_time_obj)
        to_dt = datetime.combine(base_date, to_time_obj)

        # Format ID: 2026/09/15-09.00-10.00
        period = base_date.strftime("%Y/%m/%d")
        from_label = from_time_obj.strftime("%H.%M")
        to_label = to_time_obj.strftime("%H.%M")
        activity_name = f"{period}-{from_label}-{to_label}"

        frappe.get_doc({
            "doctype": "Daily Timesheet Activity",
            "name": activity_name,
            "employee": doc.employee,
            "activity_type": row.activity_type,
            "from_datetime": from_dt,
            "to_datetime": to_dt,
            "from_time": row.from_time,
            "to_time": row.to_time,
            "description": row.description,
            "parent_daily_timesheet": doc.name,
        }).insert(ignore_permissions=True)

    frappe.db.commit()