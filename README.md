# Login system til hentning af vores teknikprojekt spil

Jeg har valgt at lave et login system så man kan logge ind og få adgang til vores teknikprojekt spil, hvis man har en skole mail.

Det er grundet at teknikprojekt spillet er et undervisningsorienteret spil som skal bruges i historietimerne. Derfor skal man kun have adgang til at downloade spiller hvis man har en bruger som er oprettet med en skole mail.

## Opsætning

> **Note:** Du kan også bare bruge hjemmesiden på: <https://vps.dnorhoj.me/>

### Uden docker

For at starte webserveren skal du have Python 3.7 eller nyere, samt `pip`.

    pip install flask, peewee

For at starte:

    python src/main.py

### Med docker-compose

For at starte webserveren skal du have docker-compose installeret.

    docker-compose up
