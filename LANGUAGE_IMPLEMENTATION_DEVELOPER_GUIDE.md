# Language Toggle Implementation - Developer Guide

## 📚 Overview

The application uses React Context API to provide language switching functionality across all pages. This guide explains how to add new translations and integrate them into components.

## 🏗️ Architecture

### Components
1. **LanguageContext** (`src/context/LanguageContext.jsx`)
   - Manages language state
   - Provides `t()` function for translations
   - Handles `toggleLanguage()` functionality
   - Saves preferences to localStorage

2. **LanguageToggle** (`src/components/common/LanguageToggle.jsx`)
   - Display toggle button in header
   - Shows current language (EN/JA)
   - Switches between languages on click

3. **Translations** (`src/utils/translations.js`)
   - Contains all translation keys and values
   - Organized by category
   - Supports English and Japanese

### Data Flow

```
User clicks Language Button
         ↓
toggleLanguage() called
         ↓
language state changes (en ↔ ja)
         ↓
localStorage updated
         ↓
All components using useLanguage() re-render
         ↓
t() function returns translated text
         ↓
UI updates instantly
```

## 🔧 Implementation Steps

### Step 1: Add Translation Key

**File**: `src/utils/translations.js`

Add the key to BOTH English and Japanese sections:

```javascript
const translations = {
  en: {
    // ... existing keys ...
    myNewKey: 'English text here',
  },
  ja: {
    // ... existing keys ...
    myNewKey: '日本語テキスト',
  }
};
```

**Naming Convention:**
```
[category][purpose]

Examples:
- dashboardTitle
- employeeFormFirstName
- deleteButtonConfirm
- attendanceStatsLabel
- leaveApprovalMessage
```

### Step 2: Use in Component

Import the `useLanguage` hook:

```jsx
import { useLanguage } from '../context/LanguageContext';

const MyComponent = () => {
  const { t } = useLanguage();
  
  return (
    <div>
      <h1>{t('myNewKey')}</h1>
      <button>{t('save')}</button>
    </div>
  );
};
```

### Step 3: Test

1. Start the development server
2. Login to the application
3. Click the language toggle button
4. Verify your new text appears in both languages

## 📖 Translation Key Categories

Organize keys by category for consistency:

### Common UI
```javascript
save: 'Save',
delete: 'Delete',
edit: 'Edit',
add: 'Add',
cancel: 'Cancel',
close: 'Close',
```

### Form Labels
```javascript
firstName: 'First Name',
lastName: 'Last Name',
email: 'Email',
phone: 'Phone',
address: 'Address',
```

### Status Messages
```javascript
loading: 'Loading...',
success: 'Success',
error: 'Error',
warning: 'Warning',
pending: 'Pending',
approved: 'Approved',
```

### Navigation
```javascript
dashboard: 'Dashboard',
employees: 'Employees',
schedules: 'Schedules',
attendance: 'Attendance',
```

### Domain Specific
```javascript
// Leave Management
leaveRequest: 'Leave Request',
applyLeave: 'Apply Leave',
leaveType: 'Leave Type',

// Attendance
checkIn: 'Check In',
checkOut: 'Check Out',
workingHours: 'Working Hours',

// Shift Management
shiftName: 'Shift Name',
startTime: 'Start Time',
endTime: 'End Time',
```

## 🎯 Best Practices

### ✅ DO

1. **Add all translations in pairs**
   ```javascript
   en: { myKey: 'English' },
   ja: { myKey: '日本語' }
   ```

2. **Use consistent naming**
   - `firstName` not `first_name`
   - `employeeStatus` not `employee status`

3. **Avoid concatenation in JSX**
   ```jsx
   // ✗ Bad
   {t('welcome')} {userName}

   // ✓ Better
   Welcome, {userName}
   ```

4. **Group related keys**
   ```javascript
   // Attendance
   checkIn: '...',
   checkOut: '...',
   workingHours: '...',
   ```

5. **Keep translations simple**
   - Use short, clear text
   - Avoid complex sentences
   - Match UI space constraints

### ❌ DON'T

1. **Don't mix English and Japanese in translations**
   ```jsx
   // ✗ Wrong
   ja: { myKey: 'This is English text' }
   ```

2. **Don't use dynamic content in translation keys**
   ```jsx
   // ✗ Bad
   t(`employee_${id}`)

   // ✓ Good
   t('employee'): {id}
   ```

3. **Don't translate technical terms unnecessarily**
   ```jsx
   // ✗ Unnecessary
   API: 'えーぴーあい'

   // ✓ Keep as is
   API: 'API'
   ```

4. **Don't forget punctuation**
   ```javascript
   en: { message: 'Are you sure?' },
   ja: { message: '確認してもよろしいですか？' }
   ```

5. **Don't create duplicate keys**
   - Use existing keys when possible
   - `save`, `delete`, `edit` are universal

## 🔍 Common Translation Patterns

### Form with Dynamic Label

```jsx
const [field, setField] = useState('');

return (
  <label>
    {t('firstName')}
    {required && <span className="text-red-500">*</span>}
  </label>
);
```

### Conditional Messages

```jsx
{isLoading ? (
  t('loading')
) : isError ? (
  t('errorLoadingData')
) : (
  t('dataLoaded')
)}
```

### List with Placeholders

```jsx
{items.length > 0 ? (
  <ul>
    {items.map(item => <li key={item.id}>{item.name}</li>)}
  </ul>
) : (
  <p>{t('noRecords')}</p>
)}
```

### Status Badge

```jsx
const statusLabels = {
  'pending': t('pending'),
  'approved': t('approved'),
  'rejected': t('rejected'),
};

return <span>{statusLabels[status]}</span>;
```

## 📊 Translation Coverage

Current status:

| Component | Coverage | Status |
|-----------|----------|--------|
| Manager.jsx | 80% | ✅ Most common items |
| Employee.jsx | 30% | 🔄 In progress |
| Admin.jsx | 40% | 🔄 In progress |
| Components | 45% | 🔄 Partial |
| Forms | 60% | 🔄 Partial |

## 🚀 Adding a New Language

To add support for a third language (e.g., Spanish):

### 1. Update Translation File
```javascript
const translations = {
  en: { /* ... */ },
  ja: { /* ... */ },
  es: {
    save: 'Guardar',
    delete: 'Eliminar',
    // ... add all keys
  }
};
```

### 2. Update Context
```jsx
const [language, setLanguage] = useState(() => {
  const saved = localStorage.getItem('language');
  return saved || 'en';
});

const toggleLanguage = () => {
  setLanguage((prev) => {
    if (prev === 'en') return 'ja';
    if (prev === 'ja') return 'es';
    return 'en'; // cycle back
  });
};
```

### 3. Update Toggle Button
```jsx
<span className="text-sm font-medium text-gray-700">
  {language === 'en' ? 'EN' : language === 'ja' ? 'JA' : 'ES'}
</span>
```

## 🧪 Testing Translations

### Manual Testing

1. **Language Toggle Test**
   - Click toggle button
   - Verify all text changes
   - Refresh page
   - Verify language persists

2. **Missing Key Test**
   - Use `t('nonExistentKey')`
   - Should show the key itself or English fallback
   - Should not crash the app

3. **Special Character Test**
   - Test Japanese characters render correctly
   - Test punctuation displays properly
   - Test long text doesn't break layout

### Automated Testing

```jsx
// Example test
describe('LanguageToggle', () => {
  test('toggles language on button click', () => {
    render(<LanguageToggle />);
    const button = screen.getByRole('button');
    
    // Initial state
    expect(button).toHaveTextContent('EN');
    
    // After click
    fireEvent.click(button);
    expect(button).toHaveTextContent('JA');
  });
});
```

## 🔐 Security Considerations

1. **Language stored in localStorage**
   - Is client-side only
   - Not sent to server
   - Clears on logout

2. **Translation keys**
   - Should not contain sensitive data
   - Public and visible in source code
   - Can be extracted by anyone

3. **Dynamic content**
   - User data mixed with translations
   - Never directly translate user input
   - Use template literals safely

## 📞 Support

- **LanguageContext**: `src/context/LanguageContext.jsx`
- **Translations**: `src/utils/translations.js`
- **Toggle Component**: `src/components/common/LanguageToggle.jsx`

For issues or questions, refer to the implementation files.

---

**Version**: 1.0
**Last Updated**: December 2024
**Supported Languages**: English, Japanese
