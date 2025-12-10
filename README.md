## Second Brain Template (curated)

**Назначение:** готовая чистая структура Second Brain для новичка — без личных данных, с правильными папками, _темплейты лежат прямо там, где ими пользоваться_.

### Как пользоваться
1) Скопируй/форкни этот шаблон (Use this template)  
2) `bash scripts/setup.sh` → `source .venv/bin/activate` → `source tools/data_shortcuts.sh`  
3) Заполни файлы в `00_vision/` и `04_therapy/sessions/`:
   - `00_vision/goals/_year_template.md` → скопируй как `2026.md` и заполни
   - `04_therapy/sessions/2025/_month_template.md` → копируй как `YYYY_MM.md`
4) В `06_projects/` переименуй `your_project_*` в свои проекты.

> Все относительные ссылки в шаблонах соответствуют стандарту `[..](relative/path.md)`.

### Первые шаги (генераторы)
- Новый месяц (рус/англ месяц):  
  `make new-month YEAR=2026 MON=январь`  или  `make new-month YEAR=2026 MON=january`
- Новый год:  
  `make new-year YEAR=2026`
- Проверка YAML/линков:  
  `make yaml-validate`  и  `make links-validate`


### YAML — зачем и как
- YAML‑фронтматтер вверху между `---` и `---` хранит метаданные (тип, период, теги).  
- Обсидиан читает этот блок как «Properties» и не показывает его в тексте.
- Правила/шаблоны: см. `.cursor/rules/yaml_conventions.mdc`.


