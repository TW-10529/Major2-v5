#!/usr/bin/env python3
"""
Script to convert hardcoded English strings to translation function calls
This script processes React JSX files and replaces hardcoded English strings with t() calls
"""

import re
import sys
from pathlib import Path

# Common hardcoded strings to convert
STRING_MAP = {
    # Labels
    "Phone": "t('phone')",
    "Address": "t('address')",
    "Hire Date (Optional)": "t('hireDate')",
    "Password": "t('password')",
    "Role (Optional)": "t('role')",
    "Employment Type": "t('employmentType')",
    "Weekly Hours": "t('weeklyHours')",
    "Daily Max Hours": "t('dailyMaxHours')",
    "Shifts Per Week": "t('shiftsPerWeek')",
    "Paid Leave Per Year": "t('paidLeavePerYear')",
    
    # Buttons
    "Cancel": "t('cancel')",
    "Save": "t('save')",
    "Delete": "t('delete')",
    "Edit": "t('edit')",
    "Add": "t('add')",
    "Submit": "t('submit')",
    "Close": "t('close')",
    
    # Status
    "View Archived": "t('viewArchived')",
    "Hide Archived": "t('hideArchived')",
    
    # Messages
    "Are you sure you want to delete": "t('confirmDelete')",
}

def convert_file(filepath):
    """Convert a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace string literals with t() calls
        for english, translation_call in STRING_MAP.items():
            # Match single quotes
            pattern1 = f"'{english}'"
            replacement1 = translation_call
            content = content.replace(pattern1, replacement1)
            
            # Match double quotes
            pattern2 = f'"{english}"'
            replacement2 = translation_call
            content = content.replace(pattern2, replacement2)
        
        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {filepath}")
            return True
        else:
            print(f"⏭️  No changes: {filepath}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return False

def main():
    """Main function"""
    frontend_dir = Path("/home/tw10529/major2-v4/frontend/src")
    
    # Process all JSX files
    jsx_files = list(frontend_dir.glob("**/*.jsx"))
    
    print(f"Found {len(jsx_files)} JSX files to process...")
    
    updated_count = 0
    for jsx_file in jsx_files:
        if convert_file(jsx_file):
            updated_count += 1
    
    print(f"\n✅ Total files updated: {updated_count}/{len(jsx_files)}")

if __name__ == "__main__":
    main()
