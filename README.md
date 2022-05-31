# pipeline


Windowing demo:
Count events of user each 30s.
After 30s, dispatch new checkin events.
Check if users have 3 checkin event each 90s.

```
pipenv shell
pipenv install --dev
```

```
faust -A runner.test_producer worker -l info --without-web
faust -A runner.count_login worker -l info --without-web
faust -A runner.count_checkin worker -l info --without-web
```
