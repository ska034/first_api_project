from models import Department
from models import Employee
from models import Office


def current_user(staff_number):
    info_current_employee = Employee.query.join(Department).join(Office).filter(
        Employee.staff_number == staff_number).one()
    current_employee = {}
    current_employee['staff_number'] = info_current_employee.staff_number
    current_employee['role'] = info_current_employee.role.position
    current_employee['office_id'] = info_current_employee.department.office_id
    current_employee['department_id'] = info_current_employee.department_id

    return current_employee
