# Copyright (c) 2026, Hilmy and contributors
# For license information, please see license.txt

from frappe.model.document import Document
import frappe
from frappe.utils import get_datetime

class DailyTimesheet(Document):
    def autoname(self):
        employee_name = frappe.db.get_value("Employee", self.employee, "employee_name")
        period = get_datetime(self.month).strftime("%m/%Y")
        self.name = f"Timesheet-{employee_name}-{period}"