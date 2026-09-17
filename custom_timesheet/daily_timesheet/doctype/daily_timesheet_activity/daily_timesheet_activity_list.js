frappe.views.calendar["Daily Timesheet Activity"] = {
    field_map: {
        start: "from_datetime",
        end: "to_datetime",
        id: "name",
        title: "activity_type"
    },
    get_events_method: "frappe.desk.calendar.get_events"
};