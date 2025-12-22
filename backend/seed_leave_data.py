"""
Mock Leave Data Seeding Script
Creates sample leave requests with both paid and unpaid leaves for testing
Run: python seed_leave_data.py
"""

import asyncio
from datetime import datetime, date, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.database import engine, DATABASE_URL
from app.models import (
    User, UserType, Department, Manager, Employee, LeaveRequest, LeaveStatus
)


async def seed_leave_data():
    print("🌱 Starting leave data seeding...")
    
    # Create async session
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        try:
            # Get the first manager from database
            manager_result = await session.execute(select(Manager).limit(1))
            manager = manager_result.scalar_one_or_none()
            
            if not manager:
                print("❌ No manager found. Please seed managers first using: python seed_mock_data.py")
                return
            
            manager_id = manager.id
            print(f"✅ Found manager: ID {manager_id}")
            
            # Get employees from database
            employees_result = await session.execute(select(Employee).limit(5))
            employees = employees_result.scalars().all()
            
            if not employees:
                print("❌ No employees found. Please seed employees first using: python seed_mock_data.py")
                return
            
            print(f"✅ Found {len(employees)} employees")
            
            # Create leave requests with various dates and types
            leave_requests = []
            
            # For each employee, create multiple leave requests
            for emp_idx, emp in enumerate(employees):
                print(f"\n📝 Creating leave requests for: {emp.first_name} {emp.last_name} (ID: {emp.employee_id})")
                
                # PAID LEAVE - January 2025 (3 days)
                leave_requests.append(LeaveRequest(
                    employee_id=emp.id,
                    start_date=date(2025, 1, 6),
                    end_date=date(2025, 1, 8),
                    leave_type='paid',
                    reason='Vacation',
                    status=LeaveStatus.APPROVED,
                    manager_id=manager_id,
                    reviewed_at=datetime.utcnow(),
                    review_notes='Approved for vacation'
                ))
                print(f"  ✓ Added: Paid Leave (3 days) - January 6-8, 2025")
                
                # UNPAID LEAVE - February 2025
                leave_requests.append(LeaveRequest(
                    employee_id=emp.id,
                    start_date=date(2025, 2, 3),
                    end_date=date(2025, 2, 5),
                    leave_type='unpaid',
                    reason='Personal reasons',
                    status=LeaveStatus.APPROVED,
                    manager_id=manager_id,
                    reviewed_at=datetime.utcnow(),
                    review_notes='Approved for personal leave'
                ))
                print(f"  ✓ Added: Unpaid Leave (3 days) - February 3-5, 2025")
                
                # PAID LEAVE - March 2025 (3 days)
                leave_requests.append(LeaveRequest(
                    employee_id=emp.id,
                    start_date=date(2025, 3, 17),
                    end_date=date(2025, 3, 19),
                    leave_type='paid',
                    reason='Annual leave',
                    status=LeaveStatus.APPROVED,
                    manager_id=manager_id,
                    reviewed_at=datetime.utcnow(),
                    review_notes='Approved'
                ))
                print(f"  ✓ Added: Paid Leave (3 days) - March 17-19, 2025")
                
                # UNPAID LEAVE - April 2025
                leave_requests.append(LeaveRequest(
                    employee_id=emp.id,
                    start_date=date(2025, 4, 7),
                    end_date=date(2025, 4, 9),
                    leave_type='unpaid',
                    reason='Medical appointment',
                    status=LeaveStatus.APPROVED,
                    manager_id=manager_id,
                    reviewed_at=datetime.utcnow(),
                    review_notes='Medical leave approved'
                ))
                print(f"  ✓ Added: Unpaid Leave (3 days) - April 7-9, 2025")
                
                # PAID LEAVE - May 2025 (2 days)
                leave_requests.append(LeaveRequest(
                    employee_id=emp.id,
                    start_date=date(2025, 5, 12),
                    end_date=date(2025, 5, 13),
                    leave_type='paid',
                    reason='Holiday trip',
                    status=LeaveStatus.APPROVED,
                    manager_id=manager_id,
                    reviewed_at=datetime.utcnow(),
                    review_notes='Approved'
                ))
                print(f"  ✓ Added: Paid Leave (2 days) - May 12-13, 2025")
                
                # PAID LEAVE - June 2025 (2 days)
                leave_requests.append(LeaveRequest(
                    employee_id=emp.id,
                    start_date=date(2025, 6, 23),
                    end_date=date(2025, 6, 24),
                    leave_type='paid',
                    reason='Short break',
                    status=LeaveStatus.APPROVED,
                    manager_id=manager_id,
                    reviewed_at=datetime.utcnow(),
                    review_notes='Approved'
                ))
                print(f"  ✓ Added: Paid Leave (2 days) - June 23-24, 2025")
                print(f"  ✓ Added: Unpaid Leave (2 days) - July 14-15, 2025")
            
            # Add all leave requests to session
            session.add_all(leave_requests)
            await session.commit()
            
            print(f"\n" + "="*60)
            print(f"✅ Successfully created {len(leave_requests)} leave requests!")
            print("="*60)
            print("\n📊 Summary:")
            print(f"   • Total Leave Requests: {len(leave_requests)}")
            print(f"   • Employees with leaves: {len(employees)}")
            print(f"   • Leaves per employee: {len(leave_requests) // len(employees)}")
            print(f"\n💾 Data saved to database!")
            print("\n🧪 Now you can:")
            print("   1. Log in as manager1 / manager123")
            print("   2. Go to Leave Requests → Search Employee Leave Details")
            print("   3. Search for employee ID (e.g., E0001)")
            print("   4. View full details and download Excel report")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Error: {e}")
            raise


async def clear_leave_data():
    """Optional: Clear all leave data"""
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        try:
            await session.execute("DELETE FROM leave_requests")
            await session.commit()
            print("✅ Cleared all leave requests")
        except Exception as e:
            await session.rollback()
            print(f"❌ Error clearing data: {e}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("LEAVE DATA SEEDING SCRIPT")
    print("="*60)
    
    # Run the seeding
    asyncio.run(seed_leave_data())
