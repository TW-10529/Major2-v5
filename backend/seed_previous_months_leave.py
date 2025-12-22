"""
Previous Months Leave Data Seeding Script
Creates approved leave requests for previous months (Nov 2024 - Jul 2025)
Run: python seed_previous_months_leave.py
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


async def seed_previous_months_leaves():
    print("\n" + "="*70)
    print("🌱 SEEDING PREVIOUS MONTHS LEAVE DATA")
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
                ).limit(5)
            )
            employees = emp_result.scalars().all()
            
            if not employees:
                print("❌ No employees found")
                return False
            
            print(f"\n✅ Found: Manager ID {manager.id}, {len(employees)} employees")
            
            leave_requests = []
            
            # Previous months data with UNPAID leaves only
            # (paid leaves are already added by seed_leave_data.py)
            months_data = [
                {
                    'month': 'November 2024',
                    'paid_dates': [],  # No paid leaves (already covered)
                    'unpaid_dates': [
                        (date(2024, 11, 18), date(2024, 11, 19))  # 2 days
                    ]
                },
                {
                    'month': 'December 2024',
                    'paid_dates': [],  # No paid leaves
                    'unpaid_dates': [
                        (date(2024, 12, 9), date(2024, 12, 10))   # 2 days
                    ]
                },
                {
                    'month': 'January 2025',
                    'paid_dates': [],  # No paid leaves
                    'unpaid_dates': [
                        (date(2025, 1, 20), date(2025, 1, 21))    # 2 days
                    ]
                },
                {
                    'month': 'February 2025',
                    'paid_dates': [],  # No paid leaves
                    'unpaid_dates': [
                        (date(2025, 2, 3), date(2025, 2, 4))      # 2 days
                    ]
                },
                {
                    'month': 'March 2025',
                    'paid_dates': [],  # No paid leaves
                    'unpaid_dates': [
                        (date(2025, 3, 24), date(2025, 3, 25))    # 2 days
                    ]
                },
                {
                    'month': 'April 2025',
                    'paid_dates': [],  # No paid leaves
                    'unpaid_dates': [
                        (date(2025, 4, 21), date(2025, 4, 22))    # 2 days
                    ]
                },
                {
                    'month': 'May 2025',
                    'paid_dates': [],  # No paid leaves
                    'unpaid_dates': [
                        (date(2025, 5, 26), date(2025, 5, 27))    # 2 days
                    ]
                },
                {
                    'month': 'June 2025',
                    'paid_dates': [],  # No paid leaves
                    'unpaid_dates': [
                        (date(2025, 6, 23), date(2025, 6, 24))    # 2 days
                    ]
                },
                {
                    'month': 'July 2025',
                    'paid_dates': [],  # No paid leaves
                    'unpaid_dates': [
                        (date(2025, 7, 28), date(2025, 7, 29))    # 2 days
                    ]
                }
            ]
            
            # Create leaves for each employee
            for emp_idx, emp in enumerate(employees):
                print(f"\n📝 Creating leaves for: {emp.employee_id} ({emp.first_name})")
                
                for month_data in months_data:
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
                        print(f"   ✓ {month_data['month']:20} - Paid: {days} days ({start_date} to {end_date})")
                    
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
                        print(f"   ✓ {month_data['month']:20} - Unpaid: {days} days ({start_date} to {end_date})")
            
            # Add all to session
            session.add_all(leave_requests)
            await session.commit()
            
            print(f"\n" + "="*70)
            print(f"✅ Successfully created {len(leave_requests)} leave requests!")
            print(f"   Across {len(employees)} employees")
            print(f"   For 9 months (Nov 2024 - Jul 2025)")
            print("="*70)
            
            return True
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Error: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(seed_previous_months_leaves())
