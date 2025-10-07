# 🤖 תבנית בוט טלגרם

תבנית בוט טלגרם מודרנית ועשירה בתכונות שנבנתה עם Pyrogram ו-Python. תבנית זו מספקת בסיס מוצק לבניית בוטי טלגרם עם תמיכה בריבוי שפות, אינטגרציה עם מסד נתונים, ניהול אדמינים, פאנל ניהול מתקדם ועוד.

## ✨ תכונות

- **🌐 תמיכה בריבוי שפות**: תמיכה מובנית בעברית ובאנגלית עם יכולת הרחבה קלה
- **👥 ניהול משתמשים**: רישום משתמשים מלא ומעקב אחר העדפות
- **👑 מערכת אדמינים**: בדיקת הרשאות אדמין מתקדמת עם בקרות מפורטות
- **⚙️ פאנל ניהול**: ממשק ניהול למנהל הבוט עם שליטה בהגדרות מתקדמות
- **🔒 בקרת גישה**: הגבלת פקודות למנהל הבוט בלבד
- **💾 מסד נתונים**: SQLAlchemy ORM עם תמיכה ב-SQLite
- **🛠️ כלי פיתוח**: מערכת לוגים מתקדמת וכלי ניפוי שגיאות
- **⚡ ביצועים**: אופטימיזציה של שאילתות ופעולות אסינכרוניות

## עדכונים אחרונים (אוקטובר 2024)

- **ארגון מחדש של הפרויקט**:
  - העברת פונקציונליות ניהול הבוט לחבילה ייעודית `bot_management`
  - שיפור ארגון המודולים והפרדת אחריות
- **שיפור איכות הקוד**:
  - שכתוב בדיקות הרשאות מנהלים לביצועים טובים יותר
  - שיפור בטיפול בשגיאות ורישום אירועים
  - עדכון רמזי סוגים ותיעוד
- **תכונות חדשות**:
  - הוספת אשף הגדרת בעלים עם ממשק קונסולה אינטראקטיבי
  - שיפור ניהול הגדרות הבוט
  - שיפור בטיפול בפקודות ושאילתות חוזרות

## 🚀 התחלה מהירה

### דרישות מקדימות

- Python 3.8+
- אסימון בוט טלגרם (קבל מ- [@BotFather](https://t.me/botfather))

### התקנה

1. **שכפל את המאגר**
   ```bash
   git clone https://github.com/sudo-py-dev/telegram-bot-template.git
   cd telegram-bot-template
   ```

2. **צור סביבת וירטואלית**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # ב-Windows: .venv\Scripts\activate.bat
   ```

3. **התקן תלויות**
   ```bash
   pip install -r requirements.txt
   ```

4. **הגדר סביבה**
   ```bash
   cp .env.example .env
   # ערוך את .env עם פרטי הבוט שלך
   ```

5. **הרץ את הבוט**
   ```bash
   python index.py
   ```

## ⚙️ הגדרות

העתק את `.env.example` ל-`.env` והגדר את המשתנים הבאים:

```env
# הגדרות בוט טלגרם
BOT_TOKEN=your_telegram_bot_token_here
API_HASH=your_api_hash_here
API_ID=your_api_id_here

# שם לקוח הבוט (שם הסשן)
BOT_CLIENT_NAME=my_bot

# אופציונלי: הגדרות מסד נתונים
DATABASE_URL=sqlite:///my_bot.db

# אופציונלי: רמת לוגים
LOG_LEVEL=INFO
```

### קבלת פרטי בוט

1. **צור בוט**: שלח הודעה ל- [@BotFather](https://t.me/botfather) עם `/newbot`
2. **קבל פרטי API**:
   - Bot Token: מסופק על ידי BotFather
   - API ID & Hash: קבל מ- [my.telegram.org](https://my.telegram.org)

## 📁 מבנה הפרויקט

```
telegram-bot-template/
├── bot_management/           # כלי ניהול לבעלי הבוט
│   ├── bot_settings.py       # פקודות והגדרות הבוט
│   ├── callback_handlers.py  # טיפול בשאילתות חוזרות של לוח הבקרה
│   └── setup.py              # כלי התקנה ואתחול לבוט
├── handlers/                 # מנהלי הודעות ושאילתות
│   ├── callback_handlers.py  # טיפול בשאילתות חוזרות
│   ├── command_handlers.py   # פקודות הבוט (/start, /help וכו')
│   └── join_handlers.py       # טיפול בהצטרפות לקבוצות
├── locales/                  # קבצי תרגום
│   └── messages.json         # הודעות רב-לשוניות
└── tools/                    # כלי ליבה ושירותים
    ├── database.py           # מודלים ופעולות מסד נתונים
    ├── enums.py              # קבועים וניהול הודעות
    ├── inline_keyboards.py   # יצירת מקלדות מובנות
    ├── logger.py             # הגדרות רישום
    └── tools.py              # פונקציות עזר
├── .env.example              # תבנית הגדרות סביבה
├── .gitignore               # דפוסי התעלמות מגיט
├── index.py                 # נקודת כניסה ראשית של הבוט
├── requirements.txt         # תלויות Python
├── README.md                # קובץ זה (עברית)
└── README_EN.md             # גרסה באנגלית
```

## ⚙️ פאנל ניהול בוט

הבוט כולל פאנל ניהול מתקדם עם התכונות הבאות:

### 📊 סטטיסטיקות
- צפייה במספר המשתמשים הפעילים
- מעקב אחר צ'אטים פעילים
- סטטיסטיקות שימוש בזמן אמת

### 🔧 הגדרות בוט
- **הצטרפות לקבוצות**: הפעל/כבה אפשרות הצטרפות אוטומטית לקבוצות
- **הצטרפות לערוצים**: שלוט בהצטרפות הבוט לערוצים
- **מצב תחזוקה**: כבה את הבוט זמנית לעדכונים
- **ניהול מנהלים**: הוסף/הסר מנהלי משנה

### 🔒 אבטחה
- אימות דו-שלבי למנהלים
- הגבלת פקודות לפי הרשאות
- יומן אירועים מפורט

כדי לגשת לפאנל הניהול, שלח את הפקודה `/settings` בצ'אט פרטי עם הבוט. גישה לפאנל זמינה למנהל הבוט הראשי בלבד.

## 🛠️ ניהול הבוט

- **הגדרת בעלים**:
  - אשף התקנה בפעם הראשונה
  - ממשק קונסולה אינטראקטיבי להגדרות
  - הודעת ברכה עם השלמת ההתקנה
- **הגדרות**:
  - הפעלה וכיבוי תכונות (הצטרפות לקבוצות, ערוצים)
  - צפייה בסטטיסטיקות וסטטוס הבוט
  - ניהול הרשאות הבוט

## 🛠️ שימוש

### הוספת פקודות חדשות למנהל

#### פקודות למנהל הבוט
```python
from tools.tools import owner_only

@owner_only
@with_language
async def admin_command(client, message, language: str):
    # קוד הפקודה למנהל
    pass
```

### הוספת פקודות חדשות

1. **צור פונקציית handler** ב- `handlers/commands.py`:
   ```python
   from tools.tools import with_language
   from tools.enums import Messages

   @with_language
   async def my_command(client, message, language: str):
       await message.reply(Messages(language=language).my_message)
   ```

2. **רשום את הפקודה** ברשימת `commands_handlers`:
   ```python
   commands_handlers = [
       MessageHandler(my_command, filters.command("mycommand")),
       # ... handlers קיימים
   ]
   ```

### הוספת שפות חדשות

1. **הוסף הודעות** ל- `tools/messages.json`:
   ```json
   {
     "fr": {
       "hello": "Bonjour {}",
       "goodbye": "Au revoir"
     }
   }
   ```

2. **עדכן שמות תצוגת שפות** ב- `handlers/callback_buttons.py`:
   ```python
   language_display_names = {
       "he": "עברית 🇮🇱",
       "en": "English 🇺🇸",
       "fr": "Français 🇫🇷"
   }
   ```

### ניהול הגדרות בוט

```python
from tools.database import BotSettings

# קבלת הגדרות
settings = BotSettings.get_settings()

# עדכון הגדרות
BotSettings.update_settings(
    can_join_group=True,
    can_join_channel=False,
    owner_id=123456789
)


### פעולות מסד נתונים

```python
from tools.database import Users, Chats

# צור משתמש
Users.create(user_id=123456789, username="user", language="en")

# קבל משתמש
user = Users.get(user_id=123456789)

# עדכן משתמש
Users.update(user_id=123456789, language="he")

# ספירת משתמשים
user_count = Users.count()
active_users = Users.count_by(is_active=True)

# ספירת צ'אטים
chat_count = Chats.count()
active_chats = Chats.count_by(is_active=True)
```

## 🌍 מערכת ריבוי שפות

הבוט תומך במספר שפות עם מערכת ניהול הודעות חכמה:

- **אחסון הודעות**: כל ההודעות מאוחסנות בפורמט JSON
- **מערכת fallback**: חוזרת לאנגלית אם ההודעה לא נמצאה
- **טעינה דינמית**: שפות נטענות מ- `messages.json` בזמן ריצה
- **הרחבה קלה**: הוסף שפות חדשות על ידי עדכון קובץ JSON

## 👑 מערכת אדמינים

בדיקת הרשאות אדמין מתקדמת עם תמיכה ב:
- **הרשאות מפורטות**: בדיקת זכויות אדמין ספציפיות
- **סוגי צ'אטים**: עובד עם קבוצות, סופרגרופים וערוצים
- **מטמון**: רשימות אדמינים במטמון לביצועים
- **טיפול שגיאות**: טיפול ב- בצ'אטים/הרשאות לא תקינים

```python
from tools.tools import is_admin_message

@is_admin_message(permission_require="can_restrict_members")
async def admin_only_command(client, message):
    await message.reply("אתה אדמין!")
```

## 📊 לוגים

מערכת לוגים מקיפה עם:
- **יצירת קבצים**: יצירת קבצי לוג אוטומטי (מקסימום 5MB, 3 גיבויים)
- **רמות מרובות**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **פלט מסך**: לוגים בזמן אמת במסך
- **פורמט מובנה**: הודעות לוג מפורטות עם חותמות זמן

## 🔧 תכונות מתקדמות

### מערכת מטמון
- **מטמון מתמיד**: נתונים נשמרים לאחר הפעלה מחדש של הבוט
- **תמיכה ב-TTL**: תפוגה אוטומטית של נתוני מטמון
- **סילוק LRU**: ניקוי אוטומטי של רשומות ישנות
- **עמיד בפני threads**: בטוח לגישה מקבילית

### מודלי מסד נתונים
- **משתמשים**: ניהול משתמשים עם העדפות
- **צ'אטים**: מידע על צ'אטים והגדרות
- **ניתן להרחבה**: קל להוסיף מודלים חדשים

### טיפול שגיאות
- **שמירת זמינות**: הבוט ממשיך לפעול למרות שגיאות
- **משוב למשתמש**: הודעות שגיאה ברורות למשתמשים
- **תמיכה בדיבוג**: לוג שגיאות מפורט

## 🤝 תרומה

1. Fork את המאגר
2. צור ענף תכונה: `git checkout -b feature/amazing-feature`
3. commit את השינויים שלך: `git commit -m 'Add amazing feature'`
4. Push לענף: `git push origin feature/amazing-feature`
5. פתח Pull Request

## 📝 רישיון

פרויקט זה הוא קוד פתוח וזמין תחת [רישיון MIT](LICENSE).

## 🙏 תודות

- [Pyrogram](https://github.com/TelegramPlayGround/Pyrogram) - לקוח טלגרם מודרני ב-Python
- [SQLAlchemy](https://www.sqlalchemy.org/) - toolkit למסדי נתונים
- [python-dotenv](https://github.com/theskumar/python-dotenv) - ניהול משתני סביבה

## 📞 תמיכה

אם יש לך שאלות או צריך עזרה:
- צור issue ב-GitHub
- בדוק את [תיעוד Pyrogram](https://telegramplayground.github.io/pyrogram)

## 🌍 גרסאות שפה

- [עברית README](README.md) - גרסה בעברית (זו)
- [English README](README_EN.md) - גרסה באנגלית

---

⭐ **תן כוכב למאגר זה אם הוא עוזר לך!**
