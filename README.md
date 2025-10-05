# Clean Service Bot - מנקה הודעות שירות

## מה הבוט הזה עושה?
הבוט הזה מיועד לנקות אוטומטית הודעות שירות בקבוצות טלגרם. הוא מוחק הודעות כמו 'X הצטרף לקבוצה', 'Y שינה את שם הקבוצה' וכו', כדי לשמור על הצ'אט נקי וברור.

## איך מתקינים?
1. הוסיפו את הבוט לקבוצת הטלגרם שלכם
2. תנו לו הרשאות ניהול (Admin)
3. הבוט יתחיל למחוק הודעות שירות אוטומטית

## אילו סוגי הודעות הבוט מוחק?
- הצטרפות/עזיבה של משתמשים
- שינויי הגדרות קבוצה
- הודעות עריכה
- ועוד הודעות שירות 

## עזרה
מצאת באג? תוכלו:
- ניתן לפתוח issue ב-GitHub

---

# Clean Service Bot - למפתחים

## מה צריך כדי להריץ את הבוט?
- Python 3.8+
- pip
- API_HASH + API_ID  from ([my.telegram.org](https://my.telegram.org/auth))
- BOT_TOKEN from @BotFather

## איך מתקינים?
1. מורידים את הקוד:
   ```bash
   git clone https://github.com/sudo-py-dev/clean-service-bot.git
   cd clean-service-bot
   ```

2. מתקינים את החבילות שצריך:
   ```bash
   pip install -r requirements.txt
   ```

3. copy .env.example to .env
   ```bash
   cp .env.example .env
   ```

4. משנים את הפרמטרים בקובץ .env


5. מריצים את הבוט:
   ```bash
   python index.py
   ```

## איך עובד הקוד?
- הקוד מחולק לתיקיות לפי תפקיד
- יש מערכת לוגים ב-`tools/logger.py`
- חשוב לכתוב בדיקות לכל פיצ'ר חדש

## רישיון
הקוד זמין תחת רישיון MIT - פרטים בקובץ ([LICENSE](LICENSE))

---

[README.en.md](README.en.md)

