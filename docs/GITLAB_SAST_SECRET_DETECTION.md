# SAST та Secret Detection для TruthLens-UA (GitLab)

Налаштування **Static Application Security Testing (SAST)** та **Secret Detection** у GitLab для проєкту truthlens-ua.

---

## 1. Доступність за тарифами

| Функція | Tier | Offering |
|--------|------|----------|
| **SAST** (Static Application Security Testing) | Free, Premium, Ultimate | GitLab.com, GitLab Self-Managed, GitLab Dedicated |
| **Secret Detection** | Free, Premium, Ultimate | GitLab.com, GitLab Self-Managed, GitLab Dedicated |

На **GitLab.com** і тарифі **Free** обидва сканери доступні без додаткової оплати.

---

## 2. Що вже налаштовано в репо

У корені проєкту в **`.gitlab-ci.yml`** підключені офіційні шаблони GitLab:

```yaml
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml
```

- **SAST** — статичний аналіз коду (наприклад, для Python використовується Semgrep); додає job типу `sast` у pipeline.
- **Secret Detection** — пошук витоків секретів (паролі, API-ключі, токени) у репо; додає job типу `secret_detection`.

Після push у GitLab у тому ж pipeline запускаються звичайні кроки (lint, test, ml-validate) і ці security-джоби.

---

## 3. Налаштування в інтерфейсі GitLab (опційно)

### 3.1 Увімкнення в проєкті

1. Відкрийте проєкт: **https://gitlab.com/102012dl/truthlens-ua**
2. **Settings** → **CI/CD** → **Variables**  
   Тут можна додати змінні, якщо потрібно (див. нижче).
3. **Secure** → **Security & Compliance** (або **Security & Compliance** у лівому меню)  
   Переконайтесь, що не вимкнено виконання security-підтипів pipeline (SAST, Secret Detection). На Free за замовчуванням вони доступні, якщо в CI є `include` шаблонів.

### 3.2 Змінні для SAST (за потреби)

| Змінна | Опис | Приклад |
|--------|------|--------|
| `SAST_EXCLUDED_PATHS` | Шляхи/файли, які виключити з SAST | `"scripts/, .venv/"` |
| `SEARCH_MAX_DEPTH` | Глибина пошуку для сканерів | `20` (за замовчуванням) |

Додавання: **Settings** → **CI/CD** → **Variables** → **Add variable** (можна позначити як masked або protected).

### 3.3 Secret Detection

- Сканує коміти в поточному pipeline (branch/mr).  
- Якщо потрібно сканувати всі гілки або історію — це можливо через **Premium/Ultimate** (Full History Scan).  
- На Free достатньо того, що job із шаблону **Secret-Detection** виконується при кожному запуску pipeline.

---

## 4. Що перевірити після налаштування

1. **Pipeline**  
   Після push у `main` або створення MR: **Build** → **Pipelines** (або **CI/CD** → **Pipelines**). У списку jobs мають з’явитись:
   - `sast` (або подібна назва з SAST template),
   - `secret_detection` (або аналог з Secret-Detection template).

2. **Звіти**  
   **Secure** → **Security dashboard** / **Vulnerability Report** (де це є на вашому тарифі). На Free результати SAST і Secret Detection доступні у звітах по pipeline і в job-артефактах.

3. **Артефакти job’ів**  
   У відповідних security jobs у pipeline зазвичай є артефакти (наприклад, `gl-sast-report.json`, `gl-secret-detection-report.json`), які можна переглянути або використати в наступних кроках.

---

## 5. Короткий чеклист

| Крок | Дія |
|------|-----|
| 1 | Переконатись, що в `.gitlab-ci.yml` є `include` для `Security/SAST.gitlab-ci.yml` та `Security/Secret-Detection.gitlab-ci.yml` (у репо вже додано). |
| 2 | Push змін у GitLab (або дочекатись mirror з GitHub). |
| 3 | Відкрити останній pipeline і перевірити наявність job’ів SAST та Secret Detection. |
| 4 | За потреби додати змінні в **Settings** → **CI/CD** → **Variables** (наприклад, `SAST_EXCLUDED_PATHS`). |
| 5 | Переглянути результати в **Secure** / звітах pipeline. |

Підсумок: для **GitLab.com Free** достатньо підключених шаблонів у `.gitlab-ci.yml`; додаткові налаштування в UI — опційні (excluded paths, змінні). **Secret Detection** і **SAST** на цьому тарифі працюють у межах поточного pipeline (без Full History Scan для секретів).
