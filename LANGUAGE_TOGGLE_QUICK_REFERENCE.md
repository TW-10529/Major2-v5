# 🌐 Language Toggle - Quick Reference

## 📍 Where is the Toggle Button?

```
┌─────────────────────────────────────────────────────┐
│                                    🔔  🌍 EN  👤    │  ← Header Bar
├─────────────────────────────────────────────────────┤
│                                                      │
│                   Page Content                       │
│                                                      │
└─────────────────────────────────────────────────────┘

🌍 EN = Language Toggle Button (Top Right)
```

## 🔄 How to Use

### Click to Switch
- **Click EN** → Changes to **JA** (日本語)
- **Click JA** → Changes to **EN** (English)
- Changes happen **instantly**
- No page reload needed

### Your Preference is Saved
✓ Stays when you refresh  
✓ Stays when you navigate  
✓ Resets when you logout  

## 📋 What's Translated

### ✅ Translated
```
✓ Page titles              "Dashboard" → "ダッシュボード"
✓ Button labels            "Save" → "保存"
✓ Form labels              "Email" → "メール"
✓ Status messages          "Pending" → "保留中"
✓ Menu items               "Employees" → "従業員"
✓ Instructions             "Loading..." → "読み込み中..."
✓ Error messages           "Error" → "エラー"
```

### ❌ NOT Translated
```
✗ Employee names           John Smith (stays the same)
✗ Email addresses          john@example.com
✗ Dates & numbers          2024-12-26 (same format)
✗ IDs                      E001 (stays the same)
```

## 🎯 Translation Examples

| Item | English | 日本語 |
|------|---------|--------|
| Dashboard | Dashboard | ダッシュボード |
| Save Button | Save | 保存 |
| Delete Button | Delete | 削除 |
| Employee Form | First Name | 名前 |
| Status | Pending | 保留中 |
| Attendance | Check In | チェックイン |
| Leave | Apply Leave | 休暇を申請 |
| Message | Loading | 読み込み中 |

## ⚙️ How It Works (Technical)

```
User clicks 🌍 button
    ↓
JavaScript toggles language
    ↓
Preference saved to browser memory
    ↓
All page text refreshes
    ↓
User sees new language immediately
```

## 🧪 Quick Tests

### Test 1: Toggle Works
- [ ] Click the language button
- [ ] See text change immediately
- [ ] Refresh page - language stays same

### Test 2: Works on All Pages
- [ ] Switch to Japanese
- [ ] Go to different page
- [ ] Language is still Japanese

### Test 3: All Text Translates
- [ ] Check page titles
- [ ] Check button labels
- [ ] Check form labels
- [ ] Check messages

## 🆘 If Something Goes Wrong

| Problem | Solution |
|---------|----------|
| Button doesn't work | Refresh browser (F5) |
| Text not changing | Check JavaScript is enabled |
| Language resets | Normal - clears on logout |
| See key names instead of text | Translation missing - report to developer |
| Text overlaps or looks broken | Clear browser cache (Ctrl+Shift+Delete) |

## 📚 Language Guide

### English (EN)
- Default language
- Used if translation is missing
- Full UI coverage

### Japanese (日本語)
- Full Japanese translation
- Complete UI support
- Professional business terminology

## 💡 Tips

👉 **For Japanese Users**
1. Login to application
2. Click the EN button
3. UI switches to 日本語 (Japanese)
4. Language saved automatically

👉 **For Mixed Teams**
- Switch as needed for different tasks
- Each user's preference is saved
- No impact on other team members

👉 **For Testing**
- Switch to Japanese to verify translations
- Check special characters display correctly
- Ensure no text overflow issues

## 🔗 Related Pages

- **Full User Guide**: See `LANGUAGE_TOGGLE_USER_GUIDE.md`
- **Developer Guide**: See `LANGUAGE_IMPLEMENTATION_DEVELOPER_GUIDE.md`
- **Implementation Details**: See `LANGUAGE_TOGGLE_IMPLEMENTATION.md`
- **Complete Summary**: See `LANGUAGE_TOGGLE_COMPLETE_SUMMARY.md`

---

**Quick Stats:**
- 🌍 2 Languages (EN, JA)
- 📝 150+ Translation Keys
- ⚡ Instant Switching
- 💾 Auto-Saved Preference
- ✅ Production Ready

**Updated**: December 2024
