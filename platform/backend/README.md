# Platform Backend


**Install dependencies:**
```shell script
    make pip-install
    make pip-install-test
```

## Local development:

**Start dep services:**
```shell script
  # it will start db 
  # and run migration
  make up-dep-services
```

**Serve backend:**
```shell script
  make serve
```


## Migration (alembic):

**Generate new:**

```shell script
  make up-dep-services
```

```shell
  source env.sh; cd app; alembic revision --autogenerate -m "migration revision name"
```

**Run migration:**

```shell
  # run migration locally
  source env.sh; cd app; alembic upgrade head
```