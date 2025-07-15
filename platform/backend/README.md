# Platform Backend

Install dependencies:
```shell script
    make pip-install
    make pip-install-test
```

## Local development:

Start dep services:
```shell script
  # it will start db 
  # and run migration
  make up-dep-services
```

Serve backend:
```shell script
  make serve
```
