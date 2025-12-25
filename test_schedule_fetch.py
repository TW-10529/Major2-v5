import asyncio
import sys
sys.path.insert(0, '/home/tw10548/majorv8/backend')

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.models import Schedule, Employee, User
from datetime import datetime, date

DATABASE_URL = "postgresql+asyncpg://tw10548:password@localhost/majorv8"

async def check_schedules():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Get a test employee
        emp_result = await session.execute(select(Employee).limit(1))
        employee = emp_result.scalar_one_or_none()
        
        if not employee:
            print("No employees found")
            return
        
        print(f"Testing with employee: {employee.first_name} {employee.last_name} (ID: {employee.id})")
        
        # Get their schedules for Jan 2026
        result = await session.execute(
            select(Schedule)
            .filter(
                Schedule.employee_id == employee.id,
                Schedule.date >= date(2026, 1, 1),
                Schedule.date <= date(2026, 1, 31)
            )
            .order_by(Schedule.date)
        )
        schedules = result.scalars().all()
        
        print(f"\nTotal schedules found: {len(schedules)}")
        for sched in schedules[:10]:  # Show first 10
            print(f"  {sched.date}: {sched.status} - {sched.start_time} to {sched.end_time}")
    
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_schedules())
