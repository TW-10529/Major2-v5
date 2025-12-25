#!/usr/bin/env python3
"""
Test Comp-Off with Shift Times
Tests that when a comp-off is approved, the shift times are fetched and displayed
"""

import requests
from datetime import datetime, timedelta
import sys

BASE_URL = "http://localhost:8000"

def get_saturday():
    """Get next Saturday date"""
    today = datetime.now()
    days_ahead = 5 - today.weekday()  # 5 = Saturday
    if days_ahead <= 0:
        days_ahead += 7
    return (today + timedelta(days=days_ahead)).strftime("%Y-%m-%d")

try:
    print("\n" + "="*70)
    print("  COMP-OFF WITH SHIFT TIMES TEST")
    print("="*70)
    
    saturday = get_saturday()
    print(f"\nTest Date: {saturday}\n")
    
    # Step 1: Get admin token
    print("📝 Step 1: Getting admin token")
    response = requests.post(f"{BASE_URL}/token", 
        data={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200, f"Failed to login: {response.text}"
    admin_token = response.json().get("access_token")
    print("  ✓ Admin token obtained\n")
    
    # Step 2: Find a role with shifts
    print("📝 Step 2: Finding a role with shifts")
    response = requests.get(f"{BASE_URL}/roles",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    roles = response.json()
    role_with_shifts = None
    for role in roles:
        if role.get("shifts") and len(role["shifts"]) > 0:
            role_with_shifts = role
            break
    assert role_with_shifts, "No roles with shifts found"
    shift = role_with_shifts["shifts"][0]
    shift_times = f"{shift['start_time']} - {shift['end_time']}"
    print(f"  ✓ Found role: {role_with_shifts['name']} (Shift: {shift_times})\n")
    
    # Step 3: Get an employee
    print("📝 Step 3: Fetching employees")
    response = requests.get(f"{BASE_URL}/employees",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    employees = response.json()
    assert len(employees) > 0, "No employees found"
    emp = employees[0]
    emp_id = emp["id"]
    emp_name = emp["first_name"]
    print(f"  ✓ Employee: {emp_name} (ID: {emp_id})\n")
    
    # Step 4: Assign employee to role with shifts
    print(f"📝 Step 4: Assigning employee to role: {role_with_shifts['name']}")
    response = requests.put(f"{BASE_URL}/employees/{emp_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "role_id": role_with_shifts['id'],
            "first_name": emp['first_name'],
            "last_name": emp['last_name'],
            "email": emp['email'],
            "department_id": emp['department_id']
        }
    )
    assert response.status_code == 200, f"Failed to update employee: {response.text}"
    print(f"  ✓ Employee assigned to role {role_with_shifts['id']}\n")
    
    # Step 5: Get manager token
    print("📝 Step 5: Getting manager token")
    response = requests.post(f"{BASE_URL}/token",
        data={"username": "manager1", "password": "manager123"}
    )
    assert response.status_code == 200
    manager_token = response.json().get("access_token")
    print("  ✓ Manager token obtained\n")
    
    # Step 6: Create comp-off request
    print(f"📝 Step 6: Creating comp-off request for {saturday}")
    # Use the emp_manager1_1 employee account to create the comp-off
    response = requests.post(f"{BASE_URL}/token",
        data={"username": "emp_manager1_1", "password": "emp123"}
    )
    if response.status_code == 200:
        emp_token = response.json().get("access_token")
        response = requests.post(f"{BASE_URL}/comp-off-requests",
            headers={"Authorization": f"Bearer {emp_token}"},
            json={
                "comp_off_date": saturday,
                "reason": "Test comp-off with shift times"
            }
        )
    else:
        # Fallback: use admin token with employee_id
        response = requests.post(f"{BASE_URL}/comp-off-requests",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "employee_id": emp_id,
                "comp_off_date": saturday,
                "reason": "Test comp-off with shift times"
            }
        )
    assert response.status_code == 200, f"Failed to create comp-off: {response.text}"
    comp_off_id = response.json()["id"]
    print(f"  ✓ Comp-off request created (ID: {comp_off_id})\n")
    
    # Step 7: Approve comp-off
    print("📝 Step 7: Manager approving comp-off")
    response = requests.post(f"{BASE_URL}/manager/approve-comp-off/{comp_off_id}",
        headers={"Authorization": f"Bearer {manager_token}"},
        json={"review_notes": "Approved for testing"}
    )
    assert response.status_code == 200, f"Failed to approve: {response.text}"
    print("  ✓ Comp-off approved successfully\n")
    
    # Step 8: Fetch schedule to verify shift times
    print(f"📝 Step 8: Fetching schedule for {saturday}")
    response = requests.get(
        f"{BASE_URL}/schedules?start_date={saturday}&end_date={saturday}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    schedules = response.json()
    
    # Debug: Check all schedules for this employee
    print(f"  Found {len(schedules)} total schedules for {saturday}")
    emp_schedules = [s for s in schedules if s["employee_id"] == emp_id]
    print(f"  Found {len(emp_schedules)} schedules for employee {emp_id}")
    
    if not emp_schedules:
        # Try fetching a week range
        monday = datetime.now() - timedelta(days=datetime.now().weekday())
        sunday = monday + timedelta(days=6)
        response = requests.get(
            f"{BASE_URL}/schedules?start_date={monday.strftime('%Y-%m-%d')}&end_date={sunday.strftime('%Y-%m-%d')}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        schedules = response.json()
        emp_schedules = [s for s in schedules if s["employee_id"] == emp_id]
        print(f"  Found {len(emp_schedules)} schedules for employee in this week")
    
    # Find the comp-off schedule
    comp_off_sched = None
    for sched in schedules:
        if sched["employee_id"] == emp_id:
            print(f"    Schedule for {sched['date']}: status={sched['status']}, start={sched.get('start_time')}")
            if sched["date"] == saturday:
                comp_off_sched = sched
    
    assert comp_off_sched, f"No schedule found for employee {emp_id} on {saturday}"
    
    sched_status = comp_off_sched.get("status")
    sched_start = comp_off_sched.get("start_time")
    sched_end = comp_off_sched.get("end_time")
    
    print(f"  Schedule Details:")
    print(f"    Status: {sched_status}")
    print(f"    Start Time: {sched_start}")
    print(f"    End Time: {sched_end}")
    print(f"    Expected: {shift_times}\n")
    
    # Verify
    assert sched_status == "comp_off_taken", f"Status should be 'comp_off_taken', got '{sched_status}'"
    assert sched_start, "Shift start time not populated"
    assert sched_end, "Shift end time not populated"
    
    print(f"  ✓ Schedule status is 'comp_off_taken' ✓")
    print(f"  ✓ Shift times populated: {sched_start} - {sched_end}\n")
    
    print("="*70)
    print("✓ ALL TESTS PASSED")
    print("="*70)
    print(f"\nComp-off with shift times is working correctly!")
    print(f"  • Employee: {emp_name}")
    print(f"  • Date: {saturday}")
    print(f"  • Role: {role_with_shifts['name']}")
    print(f"  • Status: {sched_status}")
    print(f"  • Shift Times: {sched_start} - {sched_end}")
    print(f"  • Calendar shows: COMP-OFF + Shift times for reference\n")

except AssertionError as e:
    print(f"\n  ✗ Test failed: {str(e)}\n")
    sys.exit(1)
except Exception as e:
    print(f"\n  ✗ Unexpected error: {str(e)}\n")
    sys.exit(1)
