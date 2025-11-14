# kasityokerho

## Sovelluksen toiminnot

- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sovellukseen.
- käyttäjä pystyy luomaan uusia tapaamisia ja päättämään niiden ajankohdan ja aiheen.
- Käyttäjä näkee sovellukseen lisätyt tapaamiset ja voi ilmoittautua niihin.
- Käyttäjä pystyy etsimään tapaamisia hakusanalla.
- Sovelluksessa on käyttäjäsivut, joilla näkyy tilastoja ja käyttäjän luomat tapaamiset sekä ne tapaamiset, joihin hän on ilmoittautunut.
- Käyttäjä pystyy valitsemaan tapaamiselle yhden tai useamman luokittelun.

## Sovelluksen asennus

- Asenna `flask`-kirjasto komennolla `$ pip install flask`
- Luo `database.db`-niminen tiedosto ja lisää siihen taulut komennolla `$ sqlite3 database.db < schema.sql`
- Sovellus käynnistyy kirjoittamalla komennon `$ flask run` ja klikkaamalla tulosteen linkkiä
