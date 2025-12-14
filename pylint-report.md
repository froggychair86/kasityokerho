# Pylint-raportti


```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:6:0: E0401: Unable to import 'flask' (import-error)
app.py:7:0: E0401: Unable to import 'flask' (import-error)
app.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:23:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:27:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:34:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:41:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:57:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:65:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:75:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:85:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:92:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:92:0: R0911: Too many return statements (14/6) (too-many-return-statements)
app.py:92:0: R0912: Too many branches (16/12) (too-many-branches)
app.py:160:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:175:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:190:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:211:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:211:0: R0911: Too many return statements (15/6) (too-many-return-statements)
app.py:211:0: R0912: Too many branches (18/12) (too-many-branches)
app.py:286:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:300:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:286:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:307:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:311:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:328:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:337:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:328:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:347:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:2:0: E0401: Unable to import 'flask' (import-error)
db.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
************* Module meetings
meetings.py:1:0: C0114: Missing module docstring (missing-module-docstring)
meetings.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
meetings.py:15:0: C0116: Missing function or method docstring (missing-function-docstring)
meetings.py:15:0: R0913: Too many arguments (7/5) (too-many-arguments)
meetings.py:26:0: C0116: Missing function or method docstring (missing-function-docstring)
meetings.py:30:0: C0116: Missing function or method docstring (missing-function-docstring)
meetings.py:34:0: C0116: Missing function or method docstring (missing-function-docstring)
meetings.py:41:0: C0116: Missing function or method docstring (missing-function-docstring)
meetings.py:45:0: C0116: Missing function or method docstring (missing-function-docstring)
meetings.py:61:0: C0116: Missing function or method docstring (missing-function-docstring)
meetings.py:76:0: C0116: Missing function or method docstring (missing-function-docstring)
meetings.py:76:0: R0913: Too many arguments (7/5) (too-many-arguments)
meetings.py:92:0: C0116: Missing function or method docstring (missing-function-docstring)
meetings.py:100:0: C0116: Missing function or method docstring (missing-function-docstring)
meetings.py:108:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:1:0: E0401: Unable to import 'werkzeug.security' (import-error)
users.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:9:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:16:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:21:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:29:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)

------------------------------------------------------------------
Your code has been rated at 7.91/10 (previous run: 7.88/10, +0.03)
```

Käydään läpi raportin sisältö ja perustellaan, miksi siinä mainittuja asioita ei ole korjattu.

## Docsting-ilmoitukset

```
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
```

Tämän tyyppiset ilmoitukset tarkoittavat, että moduuleissa ja funktioissa ei ole käytetty docstring-kommentteja. Tästä on tehty tietoinen päätös sovelluksen kehityksessä.

## Import-ilmoitukset

```
app.py:6:0: E0401: Unable to import 'flask' (import-error)
app.py:7:0: E0401: Unable to import 'flask' (import-error)
db.py:2:0: E0401: Unable to import 'flask' (import-error)
users.py:1:0: E0401: Unable to import 'werkzeug.security' (import-error)
```

Pylint antaa nämä ilmoitukset, vaikka Flask-kirjasto on asennettu kehitysympäristössä ja `import`-komennot toimivat sovelluksessa.

## Liikaa haaroja ja palautusarvoja

```
app.py:92:0: R0911: Too many return statements (14/6) (too-many-return-statements)
app.py:92:0: R0912: Too many branches (16/12) (too-many-branches)
app.py:211:0: R0911: Too many return statements (15/6) (too-many-return-statements)
app.py:211:0: R0912: Too many branches (18/12) (too-many-branches)
```

Parissa sovelluksen funktiossa tarvitaan paljon if-lausekkeita ja palautusarvoja virheiden käsittelyyn. Koodia voisi tiivistää käsittelemällä useita virheitä samalla if-lausekkeella, mutta sovelluksen kehittäjän näkemyksen mukaan niiden käsitteleminen erikseen on selkeämpää.

## Tarpeeton else

```
app.py:300:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:337:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
users.py:29:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
```

Ensimmäinen ilmoitus koskee seuraavaa koodia:

```python
if "remove" in request.form:
    meetings.remove_meeting(meeting_id)
    return redirect("/")
else:
    return redirect("/meeting/" + str(meeting_id))
```

Koodin voisi kirjoittaa tiiviimmin näin:

```python
if "remove" in request.form:
    meetings.remove_meeting(meeting_id)
    return redirect("/")
return redirect("/meeting/" + str(meeting_id))
```

Sovelluksen kehittäjän näkemyksen mukaan on kuitenkin selkeämpää kirjoittaa `else`-haara, koska se tuo selvemmin esiin kaksi eri vaihtoehtoa.

## Puuttuva palautusarvo

```
app.py:286:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:328:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
```

Nämä ilmoitukset liittyvät funktioihin, jotka käsittelevät vain metodit `GET` ja `POST` ja palauttavat niiden perusteella arvon. Jos metodi olisi jokin muu, funktio ei palauttaisi arvoa, mutta käytännössä näin ei voisi tapahtua, koska funktion dekoraattorissa vaaditaan, että metodin tulee olla joko `GET` tai `POST`.

## Vakion nimi

```
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
```

Koodin päätasolla määritelty muuttuja tulkitaan tässä vakioksi, jonka nimi tulisi kirjoittaa isoilla kirjaimilla. Sovelluksen kehittäjän näkemyksen mukaan näyttää kuitenkin paremmalta, että nimi on kirjoitettu pienillä kirjaimilla.

## Vaarallinen oletusarvo

```
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
```

Ensimmäinen ilmoitus koskee seuraavaa funktiota:

```python
def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()
```

Parametrin oletusarvo `[]` on tyhjä lista. Tämä oletusarvo on jaettu kaikkien funktion kutsujen kesken, ja jos listan sisältöä muutettaisiin jossain kutsussa, se näkyisi myös muihin kutsuihin. Koodi ei kuitenkaan muuta listaoliota.

## Liian monta argumenttia

```
meetings.py:15:0: R0913: Too many arguments (7/5) (too-many-arguments)
meetings.py:76:0: R0913: Too many arguments (7/5) (too-many-arguments)
```

Tämä ilmoitus liittyy funktioihin, jotka käsittelevät sovellukseen kuuluvaa tietokantataulua, jossa on monta saraketta. Sovelluksen kehittäjän näkemyksen mukaan funktio on kuitenkin selkeä, eikä sen toimintaa voisi välttämättä toteuttaa siten, ettei samalle funktiolle annettaisi argumenteiksi kaikkia sarakkeita.

