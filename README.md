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




