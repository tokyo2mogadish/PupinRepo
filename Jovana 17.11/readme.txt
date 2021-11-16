Postovanje Zorka,

Drustva za upravljanje DPF i DPF:
Slazemo se da bude uradeno na isti nacin i u novom sistemu, tj. da imamo jedan HTML fajl za DPF koji ce u definicijama biti upisan pet puta.

Primetili smo da se u skriptama, koje ste nam poslali za DUDPF i DPF, koriste nazivi obrasca koji ne postoje u sif_obrazac. Npr.

bs = getForme(Zahtev,'Bilans stanja-DUDPF')
        if len(bs)==0:
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Bilans stanja-DUDPF nije popunjen'

Potrebno je proci kroz fajl i izmeniti nazive npr. 'Bilans stanja-DUDPF' u 'Bilans stanja' i poruke u skladu sa tim.


Potrebno je izmeniti Python skriptu kako bi se validirali samo odgovarajuci obrasci. Nas predlog je da se skripte za osiguranja prerade tako da se kreira nova metoda getFormeBilansaUspeha(Zahtev,nazivForme), po uzoru na postojecu getForme(Zahtev,nazivForme), koja bi se pozivala u slucaju svih dodatnih 12 bilansa uspeha. Za ostale obrasce bi se koristila stara getForme. Metoda getFormeBilansaUspeha(Zahtev,nazivForme) ne treba da baca Exception, vec da vraca NULL. Nakon toga, kod provere postojanja obrasca u if-u bi trebalo proveriti da li je vrednost promenljive koja sadrzi aop-e razlicita od NULL.
        si = getForme(Zahtev,'Statisticki izvestaj')
        if len(si)==0:
            
            naziv_obrasca='Statisticki izvestaj'
            poruka  ='Statisticki izvestaj nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        bua = getFormeBilansaUspeha(Zahtev,'Bilans uspeha-osiguranje zivota')
        if len(bua)==0: --Ovde dodati proveru da li bua razlicito od NULL, pa tek onda proveravati len(bua)            
            
            naziv_obrasca='Bilans uspeha-osiguranje zivota'
            poruka  ='"Bilans uspeha-osiguranje zivota" nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
U delu gde se proveravaju AOP polja obrasca, potrebno je pre provere dodati uslov da li je promenljiva koja sadrzi AOP-e razlicita od NULL (npr. bua != null).
