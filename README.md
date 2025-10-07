# 🧹 בוט ניקוי שירותים

בוט טלגרם לניהול וניקוי הודעות שירות עם שליטה מלאה למנהלים וממשק ניהול משתמשים.

## ✨ תכונות עיקריות


- **בקרת מנהלים** - ניהול משתמשים והרשאות
- **תמיכה בריבוי שפות** - עם אפשרות להוספת שפות נוספות
- **ניקוי הודעות שירות** - ניקוי הודעות שירות
- **מסד נתונים** - שימוש ב-SQLAlchemy ORM עם SQLite
- **מערכת לוגים** - מעקב ותיעוד פעולות

## 🚀 התחלה מהירה

### דרישות מקדימות

- Python 3.8+
- אסימון בוט מטלגרם (ניתן לקבל מ-[@BotFather](https://t.me/botfather))
- API ID ו API Hash מטלגרם (ניתן לקבל מ-[Telegram](https://my.telegram.org/auth))
- חבילות Python נדרשות (התקנה דרך `pip install -r requirements.txt`)

### התקנה

1. שכפול הפרויקט:
   ```bash
   git clone https://github.com/sudo-py-dev/clean-service-bot.git
   cd clean-service-bot
   ```

2. יצירה והפעלת סביבה וירטואלית:
   ```bash
   python -m venv venv
   source venv/bin/activate  # ב-Windows: venv\Scripts\activate
   ```

3. התקנת תלויות:
   ```bash
   pip install -r requirements.txt
   ```

4. הגדרת הבוט:
   - העתק את הקובץ `.env.example` ל-`.env`
   - עדכן את המשתנים הסביבתיים בקובץ `.env`

5. הרצת הבוט:
   ```bash
   python index.py
   ```

## 📂 מבנה הפרויקט

```
.
├── bot_management/      # כלי ניהול לבוט (מנהל הבוט)
├── handlers/           # מטפלים בהודעות ואירועים
├── locales/            # קבצי שפה
├── tools/              # פונקציות עזר
├── .env.example        # דוגמה למשתני סביבה
├── index.py            # נקודת כניסה ראשית
└── requirements.txt    # תלויות Python
```

## 🤝 תרומה לפרויקט

אנחנו מעודדים תרומות! אתם מוזמנים לשלוח Pull Request.

## 📄 רישיון

הפרויקט מופץ תחת רישיון MIT - לפרטים נוספים קרא את קובץ [הרישיון](LICENSE).

[English version available here](README_EN.md)