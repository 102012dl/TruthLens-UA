# Налаштування Git та репозиторіїв (102012dl)

**User:** 102012dl  
**Email:** 102012dl@gmail.com  
**GitHub:** https://github.com/102012dl  
**GitLab (user 102012dl, не group):** https://gitlab.com/102012dl  

---

## Автореєстрація

**Автоматично створити облікові запити GitHub/GitLab неможливо** — реєстрація вимагає перевірки email та (для деяких функцій) верифікації особи. Нижче — посилання та покрокові дії.

---

## 1. GitHub

### Створення облікового запису (якщо ще немає)
- **Реєстрація:** https://github.com/signup  
- Вкажіть email: **102012dl@gmail.com**, ім’я користувача (наприклад **102012dl**), пароль.  
- Підтвердіть email за посиланням з листа.

### Репозиторій TruthLens-UA (поточна версія)
- **URL:** https://github.com/102012dl/TruthLens-UA  
1. Увійдіть на https://github.com/102012dl (або ваш профіль).  
2. **New repository:** https://github.com/new  
3. **Repository name:** `TruthLens-UA` (рекомендовано).  
4. **Visibility:** Public.  
5. Опційно: додайте README, .gitignore (Python), License (MIT).  
6. **Create repository.**  
7. На сторінці репо з’являться команди типу:
   ```bash
   git remote add origin https://github.com/102012dl/TruthLens-UA.git
   git branch -M main
   git push -u origin main
   ```

### Налаштування Git локально (один раз)
```bash
git config --global user.name "102012dl"
git config --global user.email "102012dl@gmail.com"
```

### Ініціалізація проєкту та перший push (у папці проєкту)
```bash
cd C:\Users\home2\PycharmProjects\PythonProject9
git init
git add .
git commit -m "feat: TruthLens UA MVP — analyzer, FastAPI, tests, docs"
git branch -M main
git remote add origin https://github.com/102012dl/TruthLens-UA.git
git push -u origin main
```

Якщо репо вже існувало з README, можливо знадобиться:
```bash
git pull origin main --allow-unrelated-histories
# вирішити конфлікти, якщо є
git push -u origin main
```

---

## 2. GitLab

### Реєстрація (якщо ще немає)
- **Реєстрація:** https://gitlab.com/users/sign_up  
- Email: **102012dl@gmail.com**, username (наприклад **102012dl**), пароль.  
- Підтвердіть email.

### Створення проєкту-дзеркала TruthLens-UA
1. Увійдіть на https://gitlab.com/102012dl  
2. **New project** → **Create blank project**  
   - **Project name:** `TruthLens-UA`  
   - **Visibility:** Public  
   - **Initialize with README** — за бажанням (якщо не ставите, репо заповниться з GitHub mirror).  
3. **Create project.**  
4. URL проєкту: **https://gitlab.com/102012dl/truthlens-ua** (проєкт під **user** 102012dl)

### Додавання GitLab як другого remote (після push на GitHub)
```bash
git remote add gitlab https://gitlab.com/102012dl/truthlens-ua.git
# або SSH:
git remote add gitlab git@gitlab.com:102012dl/truthlens-ua.git
git push -u gitlab main
```

**Автоматичне дзеркало (CI/CD):** при кожному push у `main` на GitHub workflow у `.github/workflows/ci.yml` пушить код у GitLab. Потрібен секрет **GITLAB_SSH_KEY** у GitHub (приватний SSH-ключ з Deploy Key у GitLab). Детально: **docs/GITLAB_MIRROR.md**.

---

## 3. Короткий чеклист

| Крок | Дія | Посилання |
|------|-----|------------|
| 1 | Зареєструватись / увійти GitHub | https://github.com/signup або /login |
| 2 | Створити репо TruthLens-UA | https://github.com/new |
| 3 | Зареєструватись / увійти GitLab | https://gitlab.com/users/sign_up або /users/sign_in |
| 4 | Створити проєкт TruthLens-UA (дзеркало) | https://gitlab.com/projects/new |
| 5 | Локально: `git init`, `git add .`, `git commit` | — |
| 6 | `git remote add origin <github-url>`, `git push -u origin main` | — |
| 7 | `git remote add gitlab <gitlab-url>`, `git push -u gitlab main` | — |

Після виконання цих кроків обидва репо будуть заповнені поточним кодом проєкту.
