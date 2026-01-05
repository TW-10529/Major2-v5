# Translation Examples - Before & After

## How to Test the Translations

1. **Access the Manager Dashboard**: Navigate to the Manager view
2. **Find the Language Toggle**: Look for the language toggle button in the header (top-right corner)
3. **Toggle Languages**: Click to switch between English and Japanese (日本語)
4. **Observe Changes**: All translated sections will update instantly

---

## Role Management Examples

### Before (English)
```
Modal Title: "Create New Job Role"
Form Fields:
  - Role Name *
  - Description
  - Priority (1-100)
  - Priority % (1-100)
  - Break Minutes

Buttons:
  - Create Role
  - Cancel
```

### After (Japanese)
```
Modal Title: "新しい職務ロールを作成"
Form Fields:
  - ロール名 *
  - 説明
  - 優先度（1～100）
  - 優先度パーセント（1～100）
  - 休憩時間（分）

Buttons:
  - ロールを作成
  - キャンセル
```

---

## Shift Management Examples

### Before (English)
```
Modal Title: "Edit Shift: Morning Shift"
Form Fields:
  - Shift Name *
  - Start Time *
  - End Time *
  - Min Employees
  - Max Employees
  - Priority

Error Message: "Shift name is required"
```

### After (Japanese)
```
Modal Title: "シフトを編集: Morning Shift"
Form Fields:
  - シフト名 *
  - 開始時刻 *
  - 終了時刻 *
  - 最小従業員数
  - 最大従業員数
  - 優先度

Error Message: "シフト名は必須です"
```

---

## Overtime Approvals Examples

### Before (English)
```
Header: "Overtime Approvals"
Subtitle: "Review and approve employee overtime requests"

Approval Modal:
  - Approval Notes
  - Button: "Approve"
  - Button: "Reject"
  - Button: "Cancel"

Empty State: "All Caught Up!"
Message: "No pending overtime requests at the moment"

Manager Notes: "Manager Notes:"
```

### After (Japanese)
```
Header: "残業承認"
Subtitle: "従業員の残業申請をレビューして承認"

Approval Modal:
  - 承認ノート
  - Button: "承認"
  - Button: "却下"
  - Button: "キャンセル"

Empty State: "すべて対応完了！"
Message: "現在、保留中の残業申請はありません"

Manager Notes: "マネージャーのメモ:"
```

---

## Delete Confirmation Examples

### Before (English)
```
Dialog Title: "Confirm Delete"
Message: "Are you sure you want to delete the shift Morning Shift?"
Note: "All shifts under this role will be marked as inactive."

Buttons:
  - Button: "Delete"
  - Button: "Cancel"

Delete Tooltip: "Permanently delete (hard delete)"
```

### After (Japanese)
```
Dialog Title: "削除を確認"
Message: "本当に shift Morning Shift を削除してもよろしいですか？"
Note: "このロール配下のすべてのシフトは非アクティブとしてマークされます。"

Buttons:
  - Button: "削除"
  - Button: "キャンセル"

Delete Tooltip: "永久に削除（ハード削除）"
```

---

## Comp-Off Management Examples

### Before (English)
```
Section Headers:
  - ⏰ Comp-Off Summary
  - ⏰ Comp-Off Statistics
  - ⏰ Comp-Off Monthly Breakdown
  - ⏰ Recent Comp-Off Transactions (Last 10)

Statistics Cards:
  - Comp-Off Earned: 16 hours
  - Comp-Off Used: 8 hours
  - Comp-Off Available: 8 hours

Status Labels:
  - Pending
  - Approved
  - Rejected
```

### After (Japanese)
```
Section Headers:
  - ⏰ コンプオフの概要
  - ⏰ コンプオフ統計
  - ⏰ コンプオフ月別内訳
  - ⏰ 最近のコンプオフ取引（最後の10件）

Statistics Cards:
  - コンプオフ獲得: 16時間
  - コンプオフ使用: 8時間
  - コンプオフ利用可能: 8時間

Status Labels:
  - 保留中
  - 承認済み
  - 却下
```

---

## How the Translation System Works

### 1. Language Toggle
User clicks the language toggle button in the header to switch between EN and JA

### 2. Context Update
The LanguageContext updates the global language state

### 3. Component Re-render
All components using `useLanguage()` hook are notified of the change

### 4. String Replacement
All `t('keyName')` calls return the translated string for the selected language

### 5. LocalStorage Persistence
The selected language preference is saved and restored on page refresh

---

## Translation Key Examples

```javascript
// In translations.js

en: {
  createNewJobRole: 'Create New Job Role',
  shiftNameRequired: 'Shift name is required',
  overtimeApprovals: 'Overtime Approvals',
  approve: 'Approve',
  confirmDelete: 'Confirm Delete',
  // ... 60+ more keys
}

ja: {
  createNewJobRole: '新しい職務ロールを作成',
  shiftNameRequired: 'シフト名は必須です',
  overtimeApprovals: '残業承認',
  approve: '承認',
  confirmDelete: '削除を確認',
  // ... 60+ more keys
}
```

---

## Component Usage Example

### Before Translation
```jsx
// OvertimeApproval.jsx (without translations)
<h1 className="text-3xl font-bold">Overtime Approvals</h1>
<p className="text-gray-600">Review and approve employee overtime requests</p>
<button>Approve</button>
```

### After Translation
```jsx
// OvertimeApproval.jsx (with translations)
import { useLanguage } from '../context/LanguageContext';

const OvertimeApproval = () => {
  const { t } = useLanguage();
  
  return (
    <>
      <h1 className="text-3xl font-bold">{t('overtimeApprovals')}</h1>
      <p className="text-gray-600">{t('reviewApproveOvertimeRequests')}</p>
      <button>{t('approve')}</button>
    </>
  );
};
```

---

## Testing Scenarios

### Scenario 1: Role Creation Flow
1. Open Manager Dashboard
2. Click "Manage Roles" / go to Role Management
3. Click "Create New Role" button
4. Switch language to Japanese using toggle
5. All form labels and modal title should now display in Japanese
6. Switch back to English to verify both languages work

### Scenario 2: Overtime Approval Workflow
1. Navigate to Overtime Approvals section
2. Toggle language to Japanese
3. Header should show "残業承認"
4. View pending approval and click "Review Request"
5. Click "承認" button to approve
6. Switch back to English to verify consistency

### Scenario 3: Shift Delete Confirmation
1. In Shift Management, hover over Delete icon
2. Tooltip should show in current language
3. Click Delete
4. Confirmation dialog appears
5. Toggle language - dialog content should translate
6. Click "削除" (or "Delete" in English) to confirm

### Scenario 4: LocalStorage Persistence
1. Set language to Japanese
2. Refresh the page
3. Language should still be Japanese (loaded from localStorage)
4. Navigate between pages
5. Language preference should persist throughout session

---

## Browser Console Debugging

To verify translation keys are being resolved correctly:

```javascript
// In browser console
const { t } = useLanguage(); // (if in React component context)

// Check if key exists
t('overtimeApprovals');  // Should return: "Overtime Approvals" or "残業承認"

// Verify language context
localStorage.getItem('language');  // Returns: 'en' or 'ja'
```

---

## Performance Notes

- Translation lookup is O(1) - direct object key access
- No external translation API calls
- All translations bundled with application
- Minimal memory overhead (60+ string keys)
- Instant language switching with no loading delay

---

## Troubleshooting

### Translation Not Showing
- ✅ Check if component imports `useLanguage` hook
- ✅ Verify `const { t } = useLanguage()` is called
- ✅ Check translation key exists in translations.js (both EN and JA)
- ✅ Verify key is used as `{t('keyName')}` in JSX

### Language Not Persisting
- ✅ Check localStorage is enabled in browser
- ✅ Verify LanguageContext saves to localStorage
- ✅ Check browser privacy settings

### Build Errors
- ✅ Run `npm run build` to verify no errors
- ✅ Check all imports are correct
- ✅ Verify translations.js has no syntax errors

---

**Date Created**: December 2024
**Translation Status**: ✅ Complete
**Coverage**: Manager Dashboard Pages (95%+)
**Build Status**: ✅ Successful (0 errors)
