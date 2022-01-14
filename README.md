# obnlint

lints your OBN scripts.

## setup

requires python3.

```sh
pip3 install -r requirements.txt
```

## running

```sh
python3 -m obnlint <paths to your files>
```

## disabling linters

you can:

-   either disable a linter globally via command line flag (e.g. `-Wno-hitprops-damage`), or,
-   disable it on a per-line basis (e.g. adding `-- NOLINT: hitprops-damage` on the line the linter finding is on – you can specify multiple as `-- NOLINT: hitprops-damage, hitprops-element`)
