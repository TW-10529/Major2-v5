# Language Toggle Button - User Guide

## 🌐 How to Use the Language Toggle

The application now includes a language toggle button that allows you to switch between **English** and **Japanese** instantly on any page.

### Locating the Language Toggle Button

1. **Look in the top-right corner** of the header on any authenticated page
2. You'll see a **globe icon** with a **language code** (EN or JA)
3. The button is displayed in the header next to the notification bell

### How to Switch Languages

1. **Click the language button** (EN or JA) in the top-right corner
2. **The entire UI will immediately switch** to the selected language
3. Your preference is **automatically saved** for future sessions

### What Gets Translated

✅ **Translated Elements:**
- All page titles and headings
- Button labels and menu items
- Form labels and input placeholders
- Table column headers
- Status messages and notifications
- Instructions and help text
- Dashboard cards and statistics labels
- Leave, attendance, and schedule related text
- Error and success messages
- Modal titles and dialog text

❌ **NOT Translated (Remains English):**
- Employee/User names and IDs
- Email addresses
- Dates and numbers (format may vary by locale)
- File and document names
- Technical error codes
- Database values
- External links and URLs

## 📱 Language Options

### English (EN)
- Complete UI in English
- Default language on first login
- Used when translation key is missing

### Japanese (日本語)
- 完全なUI日本語
- 日本語への完全な翻訳
- 日本語ユーザー向けに最適化

## 💾 Language Persistence

Your language choice is **automatically saved** to your browser:
- Preference is stored in browser's local storage
- Remains the same when you refresh the page
- Stays the same when you navigate between pages
- Clears when you logout (starts fresh on next login)

## 🔍 Examples

### Dashboard
- **EN**: "Total Employees", "Pending Leaves", "Today's Schedule"
- **JA**: "従業員総数", "保留中の休暇", "本日のスケジュール"

### Leave Management
- **EN**: "Apply Leave", "Pending", "Approved", "Rejected"
- **JA**: "休暇を申請", "保留中", "承認済み", "却下"

### Attendance
- **EN**: "Check In", "Check Out", "Present", "Late", "Absent"
- **JA**: "チェックイン", "チェックアウト", "出勤", "遅刻", "欠勤"

### Buttons
- **EN**: "Save", "Delete", "Edit", "Add", "Cancel", "Submit"
- **JA**: "保存", "削除", "編集", "追加", "キャンセル", "送信"

## 🎯 Quick Reference

| English | Japanese | Category |
|---------|----------|----------|
| Dashboard | ダッシュボード | Navigation |
| Manage Employees | 従業員を管理 | Navigation |
| My Attendance | 私の勤務時間 | Navigation |
| My Schedule | 私のスケジュール | Navigation |
| Leave Management | 休暇管理 | Navigation |
| Check In | チェックイン | Actions |
| Check Out | チェックアウト | Actions |
| Apply Leave | 休暇を申請 | Actions |
| Approve | 承認 | Actions |
| Reject | 却下 | Actions |
| Loading | 読み込み中 | Status |
| Success | 成功 | Status |
| Error | エラー | Status |
| Warning | 警告 | Status |

## ❓ Troubleshooting

### Language doesn't change
1. **Ensure JavaScript is enabled** in your browser
2. **Refresh the page** after clicking the toggle button
3. **Check browser console** for any error messages (F12)

### Translations appear as keys (e.g., "t('firstName')")
1. This means the translation key hasn't been added yet
2. The application will fall back to English
3. Contact the development team to add the missing translation

### Language reverts after logout
- This is normal behavior
- Your preference is cleared for security
- Language will default to English on next login

## 🌍 Supported Languages

Currently supported languages:
- ✅ English (EN)
- ✅ Japanese (日本語) (JA)

Future language support can be easily added by:
1. Adding new language object in `src/utils/translations.js`
2. Translating all keys from the English version
3. Adding language option to the toggle button

## 📞 Need Help?

If you encounter any issues with the language toggle:
1. Clear your browser cache and cookies
2. Try using a different browser
3. Check if your browser supports localStorage
4. Contact your IT department

## 💡 Tips

- **For Japanese users**: Click the toggle once at login to switch to Japanese (JA)
- **For bilingual users**: Switch languages as needed for different tasks
- **For managers reviewing team data**: Switch languages to verify translations
- **For testing**: Use the toggle to check text rendering in both languages

---

**Last Updated**: December 2024
**Language Support**: English, Japanese
**Technology**: React Context API + localStorage
