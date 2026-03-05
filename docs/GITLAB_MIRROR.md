# Дзеркало TruthLens-UA: GitHub → GitLab (CI/CD pipeline)

**GitHub (джерело):** https://github.com/102012dl/TruthLens-UA  
**GitLab (дзеркало):** https://gitlab.com/102012dl/truthlens-ua — проєкт під **user 102012dl** (не group)  

Після налаштування кожен **push у `main` на GitHub** автоматично відправляє код у GitLab; на GitLab також запускається власний CI pipeline (`.gitlab-ci.yml`).

---

## 1. Створити проєкт на GitLab (якщо ще немає)

1. Увійдіть: https://gitlab.com/102012dl  
2. **New project** → **Create blank project**  
   - **Project name:** `TruthLens-UA` (slug буде `truthlens-ua`)  
   - **Project URL:** user **102012dl** (не group)  
   - **Visibility:** Public  
   - **Initialize repository with a README** — можна **не** ставити (репо заповниться з GitHub).  
3. **Create project.**  
4. URL проєкту: **https://gitlab.com/102012dl/truthlens-ua**

---

## 2. SSH-ключ для дзеркала (GitHub Actions → GitLab)

Щоб GitHub Actions міг пушити в GitLab, потрібен **окремий SSH-ключ**, який додається в GitLab як **Deploy Key**.

### 2.1 Згенерувати ключ (один раз, на своїй машині)

```bash
ssh-keygen -t ed25519 -C "102012dl@gmail.com" -f gitlab_mirror_key -N ""
```

З’являться файли: `gitlab_mirror_key` (приватний) та `gitlab_mirror_key.pub` (публічний).

### 2.2 Додати публічний ключ у GitLab (Deploy Key)

1. Відкрийте проєкт на GitLab: https://gitlab.com/102012dl/truthlens-ua  
2. **Settings** → **Repository** → **Deploy keys**  
3. **Add new key**  
   - **Title:** `github-actions-mirror`  
   - **Key:** вставте вміст файлу `gitlab_mirror_key.pub`  
   - Увімкніть **Grant write permissions to this key**  
4. **Add key**

### 2.3 Додати приватний ключ у GitHub Secrets

1. Відкрийте репо на GitHub: https://github.com/102012dl/TruthLens-UA  
2. **Settings** → **Secrets and variables** → **Actions**  
3. **New repository secret**  
   - **Name:** `GITLAB_SSH_KEY`  
   - **Value:** повний вміст файлу `gitlab_mirror_key` (приватний ключ, включно з рядками `-----BEGIN ... END ...`)  
4. **Add secret**

Після цього job **mirror-to-gitlab** у GitHub Actions зможе пушити в GitLab.

---

## 3. Перший заповнення дзеркала (вручну)

Якщо GitLab-проєкт ще порожній, один раз заповніть його з локального клону:

```bash
git remote add gitlab git@gitlab.com:102012dl/truthlens-ua.git
git push -u gitlab main
```

Далі дзеркало оновлюватиме вже GitHub Actions при кожному `git push origin main`.

---

## 4. Що відбувається при push у `main` на GitHub

| Крок | Де | Що робить |
|------|-----|-----------|
| 1 | GitHub Actions | Запускається workflow **TruthLens UA CI/CD**: тести, lint, ML-валідація (опційно Docker). |
| 2 | GitHub Actions | Job **mirror-to-gitlab**: клонує репо, додає remote `gitlab` (GitLab TruthLens-UA), виконує `git push gitlab main --force`. |
| 3 | GitLab | Після отримання push GitLab запускає **свій** pipeline з `.gitlab-ci.yml`: lint, pytest, ml-validate. |

Перевірити:
- **GitHub CI:** https://github.com/102012dl/TruthLens-UA/actions  
- **GitLab CI:** https://gitlab.com/102012dl/truthlens-ua/-/pipelines  

---

## 5. Файли в репо, що стосуються дзеркала

| Файл | Призначення |
|------|-------------|
| `.github/workflows/ci.yml` | GitHub Actions: тести + job **mirror-to-gitlab** (push у `git@gitlab.com:102012dl/truthlens-ua.git`). |
| `.gitlab-ci.yml` | GitLab CI: stages `test` (ruff, pytest) та `validate` (ML-перевірка аналізатора). |

Якщо зміните назву репо на GitLab — оновіть у `.github/workflows/ci.yml` URL у рядку `git remote add gitlab ...`.
