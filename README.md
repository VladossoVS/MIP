# Spēles apraksts

Spēles sākumā cilvēks-spēlētājs norāda spēlē izmantojamas skaitļu virknes garumu, kas var būt diapazonā no 15 līdz 25 skaitļiem. Spēles programmatūra gadījuma ceļā saģenerē skaitļu virkni atbilstoši uzdotajam garumam, tajā iekļaujot skaitļus 1 un 0.

Spēles sākumstāvoklis ir ģenerētā skaitļu virkne. Katram spēlētājam ir 0 punktu. Spēlētāji izpilda gājienus pēc kārtas, aizvietojot divu blakusstāvošu skaitļu pāri, balstoties uz šādiem nosacījumiem:

- skaitļu pāris **00** dod **1** un **1 punktu** spēlētāja punktu skaitam;
- skaitļu pāris **01** dod **0** un **atņem 1 punktu** no spēlētāja punktu skaita;
- skaitļu pāris **10** dod **1** un **atņem 1 punktu** no spēlētāja punktu skaita;
- skaitļu pāris **11** dod **0** un **dod 1 punktu** spēlētājam.

Katrā gājienā var aizvietot tikai vienu skaitļu pāri. Spēle beidzas, kad ir iegūts viens skaitlis. Uzvar spēlētājs, kam ir vairāk punktu. Ja punktu skaits ir vienāds, tad rezultāts ir neizšķirts.


## Projekta struktūra

```text
run.py
src/
  ai/
    minimax.py
    alphabeta.py
  game/
    node.py
    generator.py
  ui/
    app.py
  experiments/
    metrics.py
    runner.py
```
## Programmas palaišana

Lai palaistu spēli, nepieciešams Python 3.

1. Atvērt termināli projekta mapē  
2. Izpildīt komandu:

```bash
python run.py
