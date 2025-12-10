# Käsityökerho

## Sovelluksen toiminnot

- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sovellukseen.
- käyttäjä pystyy luomaan uusia tapaamisia ja päättämään niiden ajankohdan ja aiheen.
- Käyttäjä näkee sovellukseen lisätyt tapaamiset ja voi ilmoittautua niihin.
- Käyttäjä pystyy etsimään tapaamisia hakusanalla.
- Sovelluksessa on käyttäjäsivut, joilla näkyy tilastoja ja käyttäjän luomat tapaamiset.
- Käyttäjä pystyy valitsemaan tapaamiselle luokitteluja.

## Sovelluksen asennus (Linux)

- Asenna `flask`-kirjasto komennolla `$ pip install flask`
- Lisää tietokannan taulut tiedostoon `database.db` komennoilla `$ sqlite3 database.db < schema.sql` ja `$ sqlite3 database.db < init.sql`
- Sovellus käynnistyy kirjoittamalla komennon `$ flask run` ja klikkaamalla tulosteen linkkiä
