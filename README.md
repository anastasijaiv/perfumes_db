# Mana Parfīmu Kolekcija
![Mana Parfīmu Kolekcija logo](perfumebgg.png)

**Python + SQLite** datubāzes projekts — parfīmu kolekcionāra palīgs. Programma glabā parfīmus un to ražotājus, fiksē katru valkāšanas reizi žurnālā, ļauj vērtēt parfīmus un sasaistīt tos ar smaržu notām un sezonām. Ar datiem var strādāt divos veidos — **grafiskajā logā** (app.py) vai **izvēlnē terminālī** (terminal.py).

---

## Apraksts
Galvenās programmas iespējas:
- datubāze `parfumi.db` ar **8 savstarpēji saistītām tabulām** un ārējām atslēgām;
- grafiskais logs ar **8 cilnēm** - katrai tabulai sava;
- **pievienošana** un **dzēšana**: dzēšot parfīmu, programma izdzēš arī tā žurnāla ierakstus, vērtējumus un sasaistes;
- **meklēšana visās 8 tabulās vienlaikus*;
- `JOIN` vaicājumi tabulās rāda nosaukumus, nevis tikai ID.

Izmantotās tehnoloģijas: [Python](https://www.python.org/) ar moduļiem `tkinter` un `sqlite3` — *papildu bibliotēkas nav vajadzīgas*.

## Datubāzes shēma (Schema)
<img width="869" height="805" alt="tablesketch (2)" src="https://github.com/user-attachments/assets/fe790f06-c35c-47a9-84f0-a2ef79fec2a4" />

---

Shēma zīmēta ar drawDB. Tabulu pārskats:

| Tabula | Ko glabā | Atslēgas |
|---|---|---|
| **Brands** | brendi (nosaukums, valsts, dibināšanas gads) | `BrandID` PK |
| **Perfumes** | parfīmi (nosaukums, koncentrācija, apjoms, gads, cena) | `PerfumeID` PK, `BrandID` FK → Brands |
| **FragranceNotes** | smaržu notas (nosaukums, kategorija) | `NoteID` PK |
| **PerfumeNotes** | sasaistes parfīms un nota | PK (`PerfumeID`, `NoteID`) |
| **WearLog** | valkāšanas žurnāls (datums, pasākums, laikapstākļi, smidzinājumu skaits) | `WearID` PK, `PerfumeID` FK → Perfumes |
| **Ratings** | vērtējumi skalā 1–10 + atsauksme | `RatingID` PK, `PerfumeID` FK → Perfumes |
| **Seasons** | sezonas | `SeasonID` PK |
| **PerfumeSeasons** | sasaistes parfīms un sezona | PK (`PerfumeID`, `SeasonID`) |

---

## Instalācija
**Prasības:** [Python 3](https://www.python.org/). Moduļi `tkinter` un `sqlite3` ir iebūvēti.
1. Lejupielādē vai klonē projekta mapi:
```bash
git clone https://github.com/lietotajs/parfimu-kolekcija.git
```

2. Vienu reizi palaiž galveno failu - tas izveido datubāzi `parfumi.db` ar visām 8 tabulām un sākuma datiem:
```bash
python main.py
```

Sākuma dati, ko izveido `main.py`: 3 brendi (Afnan, Lattafa, Dior), 3 parfīmi (9 PM, Khamrah, Sauvage), 5 smaržu notas (Vanilla, Bergamot, Rose, Musk, Cinnamon), 4 sezonas (Spring–Winter), valkāšanas žurnāls un vērtējumi.

---

## Lietošana
Grafiskais logs:
```bash
python app.py
```

Termināļa izvēlne:
```bash
python terminal.py
```

---

**Cilnes:**

| Cilne | Ko tajā var darīt |
|---|---|
| **Brendi** | pievienot brendu (nosaukums, valsts, dibināšanas gads) |
| **Parfīmi** | pievienot parfīmu (Brenda ID, nosaukums, cena EUR) |
| **Žurnāls** | pievienot valkāšanas ierakstu (datums, pasākums) |
| **Vērtējumi** | 4 vērtējumi skalā 1–10 un brīvā teksta atsauksme |
| **Notas** | jauna smaržu nota katalogā (nosaukums, kategorija top / heart / base) |
| **Parfīmu notas** | sasaistīt parfīmu ar notu |
| **Sezonas** | sasaistīt parfīmu ar sezonu + sezonu saraksts |
| **Meklēšana** | meklēt tekstu visās 8 tabulās vienlaikus |


Katrā cilnē zem tabulas ir poga **Dzēst izvēlēto rindu**: uzspiež uz rindas tabulā un klikšķina pogu. Dzēšot parfīmu vai brendu, programma automātiski izdzēš arī visus saistītos ierakstus un parāda ziņojumu.


---

Termināļa izvēlne izskatās šādi:

```text
PARFĪMU KOLEKCIJA
1 - Pievienot brendu
2 - Pievienot parfīmu
3 - Pievienot valkāšanas ierakstu
4 - Parādīt valkāšanas žurnālu
0 - Iziet
```

---

## Projekta struktūra

```text
parfimu-kolekcija/
├── main.py         # izveido 8 tabulas un sākuma datus
├── funkcijas.py    # visas datubāzes funkcijas (add / get / delete / search)
├── app.py          # grafiskais logs ar 8 cilnēm (tkinter)
├── terminal.py     # izvēlne terminālī
├── parfumi.db      # datubāze (izveidojas pēc main.py palaišanas)
├── perfumebgg.png  # logo GUI augšā
└── shema.png       # datubāzes ER shēma (drawDB)
```


---


## Izstrādes statuss

- [x] datubāzes shēma — 8 tabulas ar ārējām atslēgām un sākuma datiem
- [x] grafiskais logs ar tabulām, ritjoslu un centrētu saturu
- [x] dzēšana ar automātisku saistīto ierakstu
- [x] meklēšana visā datubāzē
