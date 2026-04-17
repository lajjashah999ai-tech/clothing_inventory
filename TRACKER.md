# Work Tracker — Vastradhaga Clothing Shop

## Status: Prototype Complete ✅

---

## Phase 1 — Scaffold + Auth + Docs ✅
- [x] Python virtual environment created
- [x] Django 4.2 + all dependencies installed
- [x] Django project `vastradhaga` created
- [x] `shop` app created
- [x] Settings split: `base.py`, `local.py`, `production.py`
- [x] `manage.py` updated to use `vastradhaga.settings.local`
- [x] Login / logout views
- [x] `base.html` with Bootstrap 5 sidebar layout (responsive)
- [x] `CLAUDE.md` (project + shop + config level)
- [x] `TRACKER.md` (this file)
- [x] `INSTRUCTIONS.md`

## Phase 2 — Models + Categories ✅
- [x] `Category` model
- [x] `Item` model (with soft delete `is_active`)
- [x] `Sale` model
- [x] `SaleItem` model (price snapshot at sale time)
- [x] Admin registration for all models
- [x] Category list + add (inline form)
- [x] Category edit
- [x] Category delete (blocked if items exist)

## Phase 3 — Items CRUD ✅
- [x] Item list with search (by name) + category filter
- [x] Add item form
- [x] Edit item form
- [x] Restock panel on edit page (additive stock update)
- [x] Soft delete

## Phase 4 — POS + Sales ✅
- [x] POS screen with dynamic multi-item rows (vanilla JS)
- [x] Real-time subtotal + grand total calculation
- [x] Atomic stock decrement on sale save
- [x] Stock validation (cannot sell more than available)
- [x] Sales history list

## Phase 5 — Dashboard + Reports ✅
- [x] Dashboard with 4 stat cards
- [x] Low stock alert table on dashboard
- [x] Current stock report (filterable)
- [x] Low stock report
- [x] Sales report (daily breakdown + totals)

## Phase 6 — Deployment Config ✅
- [x] `requirements.txt`
- [x] `Procfile` for Render/Heroku
- [x] `.env` template
- [x] `.gitignore`
- [x] WhiteNoise middleware configured
- [x] `production.py` with `dj-database-url`

---

## Pending / Next Steps
- [ ] Run initial migrations: `python manage.py migrate`
- [ ] Create admin superuser: `python manage.py createsuperuser`
- [ ] Test all flows locally
- [ ] User feedback on UI → iterate
- [ ] Deploy to Render (when ready)
- [ ] Add sample data for demo
