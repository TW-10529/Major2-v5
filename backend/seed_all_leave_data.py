"""
Comprehensive Leave Data Seeding Script
Combines all leave data (recent months + previous months) into one script
Ensures each employee respects 10-day annual paid leave entitlement

Run: python seed_all_leave_data.py
"""

import asyncio
from datetime import datetime, date, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.database import engine
from app.models import (
    Manager, Employee, LeaveRequest, LeaveStatus
)


async def seed_all_leave_data():
    print("\n" + "="*70)
    print("🌱 SEEDING COMPREHENSIVE LEAVE DATA")
    print("="*70)
    
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        try:
            # Get manager
            manager_result = await session.execute(select(Manager).limit(1))
            manager = manager_result.scalar_one_or_none()
            
            if not manager:
                print("❌ No manager found")
                return False
            
            # Get employees
            emp_result = await session.execute(
                select(Employee).filter(
                    Employee.department_id == manager.department_id
                )
            )
            employees = emp_result.scalars().all()
            
            if not employees:
                print("❌ No employees found")
                return False
            
            print(f"\n✅ Found: Manager ID {manager.id}, {len(employees)} employees")
            
            leave_requests = []
            
            # Complete year leave data (Nov 2024 - Jul 2025)
            # IMPORTANT: Each employee has 10 days paid leave entitlement per year
            # Total: 3+2+3+1+1 = 10 paid days per employee
            leave_data = [
                # NOVEMBER 2024
                {
                    'month': 'November 2024',
                    'paid_dates': [
                        (date(2024, 11, 4), date(2024, 11, 6)),   # 3 days
                    ],
                    'unpaid_dates': [
                        (date(2024, 11, 18), date(2024, 11, 19))  # 2 days
                    ]
                },
                # DECEMBER 2024
                {
                    'month': 'December 2024',
                    'paid_dates': [
                        (date(2024, 12, 2), date(2024, 12, 3)),   # 2 days
                    ],
                    'unpaid_dates': [
                        (date(2024, 12, 9), date(2024, 12, 10))   # 2 days
                    ]
                },
                # JANUARY 2025
                {
                    'month': 'January 2025',
                    'paid_dates': [
                        (date(2025, 1, 6), date(2025, 1, 8)),     # 3 days
                    ],
                    'unpaid_dates': [
                        (date(2025, 1, 20), date(2025, 1, 21))    # 2 days
                    ]
                },
                # FEBRUARY 2025
                {
                    'month': 'February 2025',
                    'paid_dates': [
                        (date(2025, 2, 17), date(2025, 2, 17)),   # 1 day
                    ],
                    'unpaid_dates': [
                        (date(2025, 2, 3), date(2025, 2, 4))      # 2 days
                    ]
                },
                # MARCH 2025
                {
                    'month': 'March 2025',
                    'paid_dates': [
                        (date(2025, 3, 10), date(2025, 3, 10)),   # 1 day
                    ],
                    'unpaid_dates': [
                        (date(2025, 3, 24), date(2025, 3, 25))    # 2 days
                    ]
                },
                # APRIL 2025
                {
                    'month': 'April 2025',
                    'paid_dates': [],  # 0 days
                    'unpaid_dates': [
                        (date(2025, 4, 21), date(2025, 4, 22))    # 2 days
                    ]
                },
                # MAY 2025
                {
                    'month': 'May 2025',
                    'paid_dates': [],  # 0 days
                    'unpaid_dates': [
                        (date(2025, 5, 26), date(2025, 5, 27))    # 2 days
                    ]
                },
                # JUNE 2025
                {
                    'month': 'June 2025',
                    'paid_dates': [],  # 0 days
                    'unpaid_dates': [
                        (date(2025, 6, 23), date(2025, 6, 24))    # 2 days
                    ]
                },
                # JULY 2025
                {
                    'month': 'July 2025',
                    'paid_dates': [],  # 0 days
                    'unpaid_dates': [
                        (date(2025, 7, 14), date(2025, 7, 15)),   # 2 days
                        (date(2025, 7, 28), date(2025, 7, 29))    # 2 days
                    ]
                }
            ]
            
            # Create leaves for each employee
            total_created = 0
            for emp_idx, emp in enumerate(employees):
                print(f"\n📝 Employee: {emp.employee_id} ({emp.first_name} {emp.last_name})")
                print(f"   Paid Leave Entitlement: {emp.paid_leave_per_year} days")
                
                paid_total = 0
                unpaid_total = 0
                
                for month_data in leave_data:
                    # Add paid leaves
                    for start_date, end_date in month_data['paid_dates']:
                        days = (end_date - start_date).days + 1
                        leave_requests.append(LeaveRequest(
                            employee_id=emp.id,
                            start_date=start_date,
                            end_date=end_date,
                            leave_type='paid',
                            reason=f'Approved leave - {month_data["month"]}',
                            status=LeaveStatus.APPROVED,
                            manager_id=manager.id,
                            reviewed_at=datetime.now(),
                            review_notes='Approved'
                        ))
                        paid_total += days
                        total_created += 1
                        print(f"   ✓ {month_data['month']:20} - Paid: {days} days ({start_date})")
                    
                    # Add unpaid leaves
                    for start_date, end_date in month_data['unpaid_dates']:
                        days = (end_date - start_date).days + 1
                        leave_requests.append(LeaveRequest(
                            employee_id=emp.id,
                            start_date=start_date,
                            end_date=end_date,
                            leave_type='unpaid',
                            reason=f'Unpaid leave - {month_data["month"]}',
                            status=LeaveStatus.APPROVED,
                            manager_id=manager.id,
                            reviewed_at=datetime.now(),
                            review_notes='Approved'
                        ))
                        unpaid_total += days
                        total_created += 1
                        print(f"   ✓ {month_data['month']:20} - Unpaid: {days} days ({start_date})")
                
                print(f"   Summary: {paid_total} paid days (limit: {emp.paid_leave_per_year}), {unpaid_total} unpaid days")
            
            # Add all to session
            session.add_all(leave_requests)
            await session.commit()
            
            print("\n" + "="*70)
            print(f"✅ SEEDING COMPLETE!")
            print("="*70)
            print(f"\n📊 Data Summary:")
            print(f"   ✓ Total Leave Requests: {total_created}")
            print(f"   ✓ Employees: {len(employees)}")
            print(f"   ✓ Period: November 2024 - July 2025 (9 months)")
            print(f"   ✓ Paid Leaves: Within 10-day entitlement per employee")
            print(f"   ✓ Unpaid Leaves: Unrestricted")
            
            print(f"\n🧪 Ready to Test:")
            print(f"   1. Login as manager1 / manager123")
            print(f"   2. Search for employee ID (E0001, E0002, E0003)")
            print(f"   3. View full details and download Excel")
            print(f"   4. Try to request paid leave > 10 days (will be rejected)")
            
            return True
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Error: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(seed_all_leave_data())
