## Project structure:

```
├── Makefile
├── README.md
├── docs
├── gitops
└── platform
    ├── service-1
        ├── Dockerfile
        ├── ...
        └── requirments.txt
    ├── ...
    └── service-n
```


- `Makefile` - Commands to start local environment.
- `README.md` - Main README for the whole project.
- `docs` - Docs about project.
- `gitops` - Manifests for the project. *Note:* In general this should be in different repo.
- `platform` - It contains all source code for services.
