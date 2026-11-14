### Furniture ERP

Furniture manufacturing, trading, project and retail ERP built on the Frappe Framework.

> **Note:** ERPNext is not yet installed on the development site. Catalogue masters (Product Family, Material, Finish, Specification) work on Frappe alone. Sales/stock/accounting flows require ERPNext — see `docs/assumptions-decisions-register.md`.

### Installation

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/Abhishek-kaiten/furniture_erp.git --branch dev
bench --site [site] install-app furniture_erp
bench --site [site] migrate
```

### Branching

- `main` — stable
- `dev` — integration / testing
- Feature work: branch from `dev`, open PR back into `dev`

### Documentation

See `/docs` for architecture, DocType specs, workflows, and milestone plan.

### License

mit
