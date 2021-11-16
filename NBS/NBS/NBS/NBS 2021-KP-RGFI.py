import sys
#sys.path.append(r"C:\IronPython2.7\Lib")
#import traceback

exceptionList = []

#Provera da li Forma postoji
def getForme(Zahtev,nazivForme):
    if nazivForme in Zahtev.Forme:
        return Zahtev.Forme[nazivForme].NumerickaPoljaForme
    else:
        raise Exception('Obrazac pod nazivom: '+nazivForme+' ne postoji')


#BROJ KONVERTUJE U AOP KEY
def broj_u_aop(aop_broj, broj_kolone):
    seq = ("aop", str(aop_broj).zfill(4), str(broj_kolone))
    aop_key = "-".join(seq)
    return aop_key

#VRACA VREDNOST AOP POLJA
def aop(aop_dict, aop_broj, kolona):   
    aop_key = broj_u_aop(aop_broj, kolona)

    if aop_key in aop_dict:
        a=aop_dict[aop_key]
       
        if a is None:
            return 0
        return a

    raise Exception('Validacion skripta očekuje ' + aop_key + ' koji nije pronadjen')

    
#SUMA OD, DO ZA ZADATU KLOLONU
def suma(aop_dict, prvi_aop, poslednji_aop, kolona):
    sum = 0
    for x in range (prvi_aop, poslednji_aop+1):
        sum += aop(aop_dict, x, kolona)
    return sum

#SUMA AOPA SA LISTE
def suma_liste(aop_dict, lista, kolona):
    sum = 0
    for x in lista:
        sum += aop(aop_dict, x, kolona)
    return sum 

#Ako forma ima bar jednu napomenu u zadatom opsegu vraca True u suprotnom False   
def proveriNapomene(aop_dict, prvi_aop, poslednji_aop, kolona):
    imaBarJednuNapomenu = False
    for aop_broj in range (prvi_aop, poslednji_aop+1):
        aop_key = broj_u_aop(aop_broj, kolona)
        if aop_dict[aop_key].strip():
            imaBarJednuNapomenu = True
            break
    return imaBarJednuNapomenu   

def Validate(Zahtev):
    try:
        doc_errors=[]
        doc_warnings=[]
        form_warnings=[]
        form_errors=[]
        exceptions=[]
        
        #Provera da li lice odgovorno za sastavljanje je upisano
        if (Zahtev.LiceOdgovornoZaSastavljanje is None):
            form_errors.append('Podaci za lice odgovorno za sastavljanje finansijskog izveštaja nisu upisani.')


       #Provera da li lice odgovorno za potpisivanje
        if (len(Zahtev.Potpisnici) == 0):
            form_errors.append('Podaci o potpisniku finansijskog izveštaja nisu upisani.')
        
        
        #Provera da li su prosledjeni svi ulazni dokumenti
        if (Zahtev.ValidacijaUlaznihDokumenataOmoguceno==True):
            if Zahtev.UlazniDokumenti.Count>0:
                for k in Zahtev.UlazniDokumenti.Keys:
                    if Zahtev.UlazniDokumenti[k].Obavezan==True and Zahtev.UlazniDokumenti[k].Barkod == None:
                        doc_errors.append('Dokument sa nazivom "'+Zahtev.UlazniDokumenti[k].Naziv+'" niste priložili.')


        #Prilagoditi proveru postojanja forme u zavisnosti od tipa FI
        bs = getForme(Zahtev,'Bilans stanja')
        if len(bs)==0:
            form_errors.append('Bilans stanja nije popunjen')

        bu = getForme(Zahtev,'Bilans uspeha')
        if len(bu)==0:
            form_errors.append('Bilans uspeha nije popunjen')

        ioor = getForme(Zahtev,'Izveštaj o ostalom rezultatu')
        if len(ioor)==0:
            form_errors.append('Izveštaj o ostalom rezultatu nije popunjen')

        iotg = getForme(Zahtev,'Izveštaj o tokovima gotovine')
        if len(iotg)==0:
            form_errors.append('Izveštaj o tokovima gotovine nije popunjen')
            
        iopk = getForme(Zahtev,'Izveštaj o promenama na kapitalu')
        if len(iopk)==0:
            form_errors.append('Izveštaj o promenama na kapitalu nije popunjen')

        si = getForme(Zahtev,'Statistički izveštaj')
        if len(si)==0:
            form_errors.append('Statistički izveštaj nije popunjen')


        if len(form_errors)>0:
            return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors, 'exceptions': exceptionList}

        lzbir = 0
        dzbir = 0
        razlika = 0

        ######################################
        #### POCETAK KONTROLNIH PRAVILA ######
        ######################################

        #00000-1
        if not( suma(bs,1,18,5)+suma(bs,1,18,6)+suma(bs,1,18,7)+suma(bs,401,422,5)+suma(bs,401,422,6)+suma(bs,401,422,7)+suma(bu,1001,1042,5)+suma(bu,1001,1042,6)+suma(ioor,2001,2022,5)+suma(ioor,2001,2022,6)+suma(iotg,3001,3063,3)+suma(iotg,3001,3063,4)+suma(iopk,4001,4138,1)+suma(si,9001,9034,4)+suma(si,9001,9034,5) > 0 ):
            form_errors.append('Zbir podataka na oznakama AOP (0001 do 0018) kol. 5 + (0001 do 0018) kol. 6  + (0001 do 0018) kol. 7 bilansa stanja + (0401 do 0422)  kol. 5 + (0401 do 0422) kol. 6  + (0401 do 0422) kol. 7 bilansa stanja + (1001 do 1042) kol. 5 + (1001 do 1042) kol. 6 bilansa uspeha + (2001 do 2022) kol. 5 + (2001 do 2022) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3063) kol. 3 + (3001 do 3063) kol. 4 izveštaja o tokovima gotovine + (4001 do 4138)kol.1  izveštaja o promenama na kapitalu + (9001 do 9034) kol. 4 + (9001 do 9034) kol. 5 statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka; ')
        
        #00000-2
        # U bar jednoj od tri navedene forme kolona napomena mora da ima bar jedan karakter
        bsNapomene = Zahtev.Forme['Bilans stanja'].TekstualnaPoljaForme;
        buNapomene = Zahtev.Forme['Bilans uspeha'].TekstualnaPoljaForme;
        ioorNapomene = Zahtev.Forme['Izveštaj o ostalom rezultatu'].TekstualnaPoljaForme;

        if not(proveriNapomene(bsNapomene, 1, 18, 4) or proveriNapomene(bsNapomene, 401, 422, 4) or proveriNapomene(buNapomene, 1001, 1042, 4) or proveriNapomene(ioorNapomene, 2001, 2022, 4)):
            form_errors.append(" Na AOP-u (0001 do 0018) + (0401 do 0422) bilansa stanja + (1001 do 1042)  bilansa uspeha + (2001 do 2022) izveštaja o ostalom rezultatu u koloni 4 (Broj napomene) mora biti unet bar jedan karakter. Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje")
        
        #Provera da li je fizahtev placen
        if not(Zahtev.Placen):
            form_warnings.append('Naknada za obradu i javno objavljivanje izveštaja i propisane dokumentacije nije uplaćena u propisanom iznosu. Instrukcije za uplatu propisane naknade date su u okviru PIS FI sistema za konkretan zahtev, na linku „Status naplate zahteva / Instrukcija za plaćanje". Ukoliko ste izvršili uplatu, a naknada nije uparena, priložite Dokaz o uplati naknade u delu Dokumentacija (na mestu predviđenom za dokaz o uplati naknade), kako biste mogli da podnesete izveštaj.');

        #Provera negativnih AOP-a
        lista=""
        lista_bs = find_negativni(bs, 1, 422, 5, 7)
        lista_bu = find_negativni(bu, 1001, 1042, 5, 6)
        lista_ioor = find_negativni(ioor, 2001, 2022, 5, 6)
        lista_iotg = find_negativni(iotg, 3001, 3063, 3, 4)
        lista_iopk = find_negativni(iopk, 4001, 4138, 1, 1)
        lista_si = find_negativni(si, 9001, 9034, 4, 5)

        if (len(lista_bs) > 0):
            lista = lista_bs
        if len(lista_bu) > 0:
            if len(lista) > 0:
                lista = lista + ", " + lista_bu
            else:
                lista = lista_bu                           
        if len(lista_ioor) > 0:
            if len(lista) > 0:
                lista = lista + ", " + lista_ioor
            else:
                lista = lista_ioor
        if len(lista_iotg) > 0:
            if len(lista) > 0:
                lista = lista + ", " + lista_iotg
            else:
                lista = lista_iotg
        if len(lista_iopk) > 0:
            if len(lista) > 0:
                lista = lista + ", " + lista_iopk
            else:
                lista = lista_iopk
        if len(lista_si) > 0:
            if len(lista) > 0:
                lista = lista + ", " + lista_si
            else:
                lista = lista_si
        if len(lista) > 0:                                           
            form_errors.append("Unete vrednosti ne mogu biti negativne ! (" + lista + ")")        
        

        
        #BILANS STANJA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        #00001
        if not( suma(bs,1,18,5)+suma(bs,401,422,5) > 0 ): 
            form_errors.append('Zbir podataka na oznakama za AOP (0001 do 0018) kol. 5  + (0401 do 0422) kol. 5 ˃ 0 Bilans stanja mora imati iskazane podatke za tekući izveštajni period; ')
        
        #00002
        if not( suma(bs,1,18,6)+suma(bs,401,422,6) > 0 ): 
            form_errors.append('Zbir podataka na oznakama za AOP (0001 do 0018) kol. 6 + (0401 do 0422) kol. 6 ˃ 0 Bilans stanja mora imati iskazane podatke za prethodni izveštajni period; ')
        
        #00003
        if not( suma(bs,1,18,7)+suma(bs,401,422,7) > 0 ):
            form_warnings.append('Zbir podataka na oznakama za AOP (0001 do 0018) kol. 7 + (0401 do 0422) kol. 7 ˃ 0 Bilans stanja, po pravilu,  mora imati iskazano početno stanje za prethodni izveštajni period kada Narodna banka Srbije vrši reklasifikaciju; ')
        
        #00004
        if not( aop(bs,18,5) == suma(bs,1,17,5) ):
            lzbir =  aop(bs,18,5) 
            dzbir =  suma(bs,1,17,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0018 kol. 5 = zbiru AOP-a (0001 do 0017) kol. 5   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00005
        if not( aop(bs,18,6) == suma(bs,1,17,6) ):
            lzbir =  aop(bs,18,6) 
            dzbir =  suma(bs,1,17,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0018 kol. 6 = zbiru AOP-a (0001 do 0017) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00006
        if not( aop(bs,18,7) == suma(bs,1,17,7) ):
            lzbir =  aop(bs,18,7) 
            dzbir =  suma(bs,1,17,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0018 kol. 7 = zbiru AOP-a (0001 do 0017) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00007
        if not( aop(bs,414,5) == suma(bs,401,413,5) ):
            lzbir =  aop(bs,414,5) 
            dzbir =  suma(bs,401,413,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0414 kol. 5 = zbiru AOP-a (0401 do 0413) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00008
        if not( aop(bs,414,6) == suma(bs,401,413,6) ):
            lzbir =  aop(bs,414,6) 
            dzbir =  suma(bs,401,413,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0414 kol. 6 = zbiru AOP-a (0401 do 0413) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00009
        if not( aop(bs,414,7) == suma(bs,401,413,7) ):
            lzbir =  aop(bs,414,7) 
            dzbir =  suma(bs,401,413,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0414 kol. 7 = zbiru AOP-a (0401 do 0413) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00010
        if( aop(bs,416,5) > 0 ):
            if not( aop(bs,417,5) == 0 ):
                lzbir =  aop(bs,417,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0416 kol. 5 > 0, onda je AOP 0417 kol. 5 = 0 Ne mogu biti istovremeno prikazani dugovni i potražni saldo računa '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00011
        if( aop(bs,417,5) > 0 ):
            if not( aop(bs,416,5) == 0 ):
                lzbir =  aop(bs,416,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 0417 kol. 5 > 0, onda je AOP 0416 kol. 5 = 0 Ne mogu biti istovremeno prikazani dugovni i potražni saldo računa '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00012
        if( aop(bs,416,6) > 0 ):
            if not( aop(bs,417,6) == 0 ):
                lzbir =  aop(bs,417,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0416 kol. 6 > 0, onda je AOP 0417 kol. 6 = 0 Ne mogu biti istovremeno prikazani dugovni i potražni saldo računa '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00013
        if( aop(bs,417,6) > 0 ):
            if not( aop(bs,416,6) == 0 ):
                lzbir =  aop(bs,416,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0417 kol. 6 > 0, onda je AOP 0416 kol. 6 = 0 Ne mogu biti istovremeno prikazani dugovni i potražni saldo računa '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00014
        if( aop(bs,416,7) > 0 ):
            if not( aop(bs,417,7) == 0 ):
                lzbir =  aop(bs,417,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0416 kol. 7 > 0, onda je AOP 0417 kol. 7 = 0 Ne mogu biti istovremeno prikazani dugovni i potražni saldo računa '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00015
        if( aop(bs,417,7) > 0 ):
            if not( aop(bs,416,7) == 0 ):
                lzbir =  aop(bs,416,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0417 kol. 7 > 0, onda je AOP 0416 kol. 7 = 0 Ne mogu biti istovremeno prikazani dugovni i potražni saldo računa '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00016
        if( suma_liste(bs,[415,416,418],5) > suma_liste(bs,[417,419],5) ):
            if not( aop(bs,420,5) == suma_liste(bs,[415,416,418],5)-suma_liste(bs,[417,419],5) ):
                lzbir =  aop(bs,420,5) 
                dzbir =  suma_liste(bs,[415,416,418],5)-suma_liste(bs,[417,419],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 0420 kol. 5 = AOP-u (0415 + 0416 - 0417 + 0418 - 0419) kol. 5, ako je AOP (0415 + 0416 + 0418) kol. 5 > AOP-a (0417 + 0419) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00017
        if( suma_liste(bs,[415,416,418],6) > suma_liste(bs,[417,419],6) ):
            if not( aop(bs,420,6) == suma_liste(bs,[415,416,418],6)-suma_liste(bs,[417,419],6) ):
                lzbir =  aop(bs,420,6) 
                dzbir =  suma_liste(bs,[415,416,418],6)-suma_liste(bs,[417,419],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 0420 kol. 6 = AOP-u (0415 + 0416 - 0417 + 0418 - 0419) kol. 6, ako je AOP (0415 + 0416 + 0418) kol. 6 > AOP-a (0417 + 0419) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00018
        if( suma_liste(bs,[415,416,418],7) > suma_liste(bs,[417,419],7) ):
            if not( aop(bs,420,7) == suma_liste(bs,[415,416,418],7)-suma_liste(bs,[417,419],7) ):
                lzbir =  aop(bs,420,7) 
                dzbir =  suma_liste(bs,[415,416,418],7)-suma_liste(bs,[417,419],7) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 0420 kol. 7 = AOP-u (0415 + 0416 - 0417 + 0418 - 0419) kol. 7, ako je AOP (0415 + 0416 + 0418) kol. 7 > AOP-a (0417 + 0419) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00019
        if( suma_liste(bs,[415,416,418],5) < suma_liste(bs,[417,419],5) ):
            if not( aop(bs,421,5) == suma_liste(bs,[417,419],5)-suma_liste(bs,[415,416,418],5) ):
                lzbir =  aop(bs,421,5) 
                dzbir =  suma_liste(bs,[417,419],5)-suma_liste(bs,[415,416,418],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 0421 kol. 5 = AOP-u (0417 - 0415 - 0416 - 0418 + 0419) kol. 5, ako je AOP (0415 + 0416 + 0418) kol. 5 < AOP-a (0417 + 0419) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00020
        if( suma_liste(bs,[415,416,418],6) < suma_liste(bs,[417,419],6) ):
            if not( aop(bs,421,6) == suma_liste(bs,[417,419],6)-suma_liste(bs,[415,416,418],6) ):
                lzbir =  aop(bs,421,6) 
                dzbir =  suma_liste(bs,[417,419],6)-suma_liste(bs,[415,416,418],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 0421 kol. 6 = AOP-u (0417 - 0415 - 0416 - 0418 + 0419) kol. 6, ako je AOP (0415 + 0416 + 0418) kol. 6 < AOP-a (0417 + 0419) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00021
        if( suma_liste(bs,[415,416,418],7) < suma_liste(bs,[417,419],7) ):
            if not( aop(bs,421,7) == suma_liste(bs,[417,419],7)-suma_liste(bs,[415,416,418],7) ):
                lzbir =  aop(bs,421,7) 
                dzbir =  suma_liste(bs,[417,419],7)-suma_liste(bs,[415,416,418],7) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 0421 kol.7 = AOP-u (0417 - 0415 - 0416 - 0418 + 0419) kol.7, ako je AOP (0415 + 0416 + 0418) kol. 7 < AOP-a (0417 + 0419) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00022
        if( suma_liste(bs,[415,416,418],5) == suma_liste(bs,[417,419],5) ):
            if not( suma(bs,420,421,5) == 0 ):
                lzbir =  suma(bs,420,421,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (0420 + 0421) kol. 5 = 0, ako je AOP (0415 + 0416 + 0418) kol. 5 = AOP-u (0417 + 0419) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00023
        if( suma_liste(bs,[415,416,418],6) == suma_liste(bs,[417,419],6) ):
            if not( suma(bs,420,421,6) == 0 ):
                lzbir =  suma(bs,420,421,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (0420 + 0421) kol. 6 = 0, ako je AOP (0415 + 0416 + 0418) kol. 6 = AOP-u (0417 + 0419) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00024
        if( suma_liste(bs,[415,416,418],7) == suma_liste(bs,[417,419],7) ):
            if not( suma(bs,420,421,7) == 0 ):
                lzbir =  suma(bs,420,421,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (0420 + 0421) kol. 7 = 0, ako je AOP (0415 + 0416 + 0418) kol. 7 = AOP-u (0417 + 0419) kol. 7 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00025
        if( aop(bs,420,5) > 0 ):
            if not( aop(bs,421,5) == 0 ):
                lzbir =  aop(bs,421,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0420 kol. 5 > 0, onda je AOP 0421 kol. 5 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00026
        if( aop(bs,421,5) > 0 ):
            if not( aop(bs,420,5) == 0 ):
                lzbir =  aop(bs,420,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0421 kol. 5 > 0, onda je AOP 0420 kol. 5 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00027
        if( aop(bs,420,6) > 0 ):
            if not( aop(bs,421,6) == 0 ):
                lzbir =  aop(bs,421,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0420 kol. 6 > 0, onda je AOP 0421 kol. 6 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00028
        if( aop(bs,421,6) > 0 ):
            if not( aop(bs,420,6) == 0 ):
                lzbir =  aop(bs,420,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0421 kol. 6 > 0, onda je AOP 0420 kol. 6 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00029
        if( aop(bs,420,7) > 0 ):
            if not( aop(bs,421,7) == 0 ):
                lzbir =  aop(bs,421,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0420 kol. 7 > 0, onda je AOP 0421 kol. 7 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00030
        if( aop(bs,421,7) > 0 ):
            if not( aop(bs,420,7) == 0 ):
                lzbir =  aop(bs,420,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0421 kol. 7 > 0, onda je AOP 0420 kol. 7 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00031
        if not( aop(bs,422,5) == suma_liste(bs,[414,420],5)-aop(bs,421,5) ):
            lzbir =  aop(bs,422,5) 
            dzbir =  suma_liste(bs,[414,420],5)-aop(bs,421,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0422 kol. 5 = AOP-u (0414 + 0420 - 0421) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00032
        if not( aop(bs,422,6) == suma_liste(bs,[414,420],6)-aop(bs,421,6) ):
            lzbir =  aop(bs,422,6) 
            dzbir =  suma_liste(bs,[414,420],6)-aop(bs,421,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0422 kol. 6 = AOP-u (0414 + 0420 - 0421) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00033
        if not( aop(bs,422,7) == suma_liste(bs,[414,420],7)-aop(bs,421,7) ):
            lzbir =  aop(bs,422,7) 
            dzbir =  suma_liste(bs,[414,420],7)-aop(bs,421,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0422 kol. 7 = AOP-u (0414 + 0420 - 0421) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00034
        if not( aop(bs,18,5) == aop(bs,422,5) ):
            lzbir =  aop(bs,18,5) 
            dzbir =  aop(bs,422,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0018 kol. 5 = AOP-u 0422 kol. 5 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00035
        if not( aop(bs,18,6) == aop(bs,422,6) ):
            lzbir =  aop(bs,18,6) 
            dzbir =  aop(bs,422,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0018 kol. 6 = AOP-u 0422 kol. 6 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00036
        if not( aop(bs,18,7) == aop(bs,422,7) ):
            lzbir =  aop(bs,18,7) 
            dzbir =  aop(bs,422,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0018 kol. 7 = AOP-u 0422 kol. 7 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #BILANS USPEHA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        #10001
        if not( suma(bu,1001,1042,5) > 0 ): 
            form_errors.append('Zbir podataka na oznakama za AOP (1001 do 1042) kol. 5 ˃ 0 Bilans uspeha mora imati iskazane podatke za tekući izveštajni period; ')
        
        #10002
        if not( suma(bu,1001,1042,6) > 0 ): 
            form_errors.append('Zbir podataka na oznakama za AOP (1001 do 1042) kol. 6 ˃ 0 Bilans uspeha mora imati iskazane podatke za prethodni izveštajni period; ')
        
        #10003
        if( aop(bu,1001,5) > aop(bu,1002,5) ):
            if not( aop(bu,1003,5) == aop(bu,1001,5)-aop(bu,1002,5) ):
                lzbir =  aop(bu,1003,5) 
                dzbir =  aop(bu,1001,5)-aop(bu,1002,5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1003 kol. 5 = AOP-u (1001 - 1002) kol. 5, ako je AOP 1001 kol. 5 > AOP-a 1002 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10004
        if( aop(bu,1001,6) > aop(bu,1002,6) ):
            if not( aop(bu,1003,6) == aop(bu,1001,6)-aop(bu,1002,6) ):
                lzbir =  aop(bu,1003,6) 
                dzbir =  aop(bu,1001,6)-aop(bu,1002,6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1003 kol. 6 = AOP-u (1001 - 1002) kol. 6, ako je AOP 1001 kol. 6 > AOP-a 1002 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10005
        if( aop(bu,1001,5) < aop(bu,1002,5) ):
            if not( aop(bu,1004,5) == aop(bu,1002,5)-aop(bu,1001,5) ):
                lzbir =  aop(bu,1004,5) 
                dzbir =  aop(bu,1002,5)-aop(bu,1001,5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1004 kol. 5 = AOP-u (1002 - 1001) kol. 5, ako je AOP 1001 kol. 5 < AOP-a 1002 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10006
        if( aop(bu,1001,6) < aop(bu,1002,6) ):
            if not( aop(bu,1004,6) == aop(bu,1002,6)-aop(bu,1001,6) ):
                lzbir =  aop(bu,1004,6) 
                dzbir =  aop(bu,1002,6)-aop(bu,1001,6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1004 kol. 6 = AOP-u (1002 - 1001) kol. 6, ako je AOP 1001 kol. 6 < AOP-a 1002 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10007
        if( aop(bu,1001,5) == aop(bu,1002,5) ):
            if not( suma(bu,1003,1004,5) == 0 ):
                lzbir =  suma(bu,1003,1004,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1003 + 1004) kol. 5 = 0, ako je AOP 1001 kol. 5 = AOP-u 1002 kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10008
        if( aop(bu,1001,6) == aop(bu,1002,6) ):
            if not( suma(bu,1003,1004,6) == 0 ):
                lzbir =  suma(bu,1003,1004,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1003 + 1004) kol. 6 = 0, ako je AOP 1001 kol. 6 = AOP-u 1002 kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10009
        if( aop(bu,1003,5) > 0 ):
            if not( aop(bu,1004,5) == 0 ):
                lzbir =  aop(bu,1004,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1003 kol. 5 > 0, onda je AOP 1004 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihod i rashod '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10010
        if( aop(bu,1004,5) > 0 ):
            if not( aop(bu,1003,5) == 0 ):
                lzbir =  aop(bu,1003,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1004 kol. 5 > 0, onda je AOP 1003 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihod i rashod '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10011
        if( aop(bu,1003,6) > 0 ):
            if not( aop(bu,1004,6) == 0 ):
                lzbir =  aop(bu,1004,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1003 kol. 6 > 0, onda je AOP 1004 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihod i rashod '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10012
        if( aop(bu,1004,6) > 0 ):
            if not( aop(bu,1003,6) == 0 ):
                lzbir =  aop(bu,1003,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1004 kol. 6 > 0, onda je AOP 1003 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihod i rashod '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10013
        if not( suma_liste(bu,[1001,1004],5) == suma(bu,1002,1003,5) ):
            lzbir =  suma_liste(bu,[1001,1004],5) 
            dzbir =  suma(bu,1002,1003,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1001 + 1004) kol. 5 = AOP-u (1002 + 1003) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10014
        if not( suma_liste(bu,[1001,1004],6) == suma(bu,1002,1003,6) ):
            lzbir =  suma_liste(bu,[1001,1004],6) 
            dzbir =  suma(bu,1002,1003,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1001 + 1004) kol. 6 = AOP-u (1002 + 1003) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10015
        if( aop(bu,1005,5) > aop(bu,1006,5) ):
            if not( aop(bu,1007,5) == aop(bu,1005,5)-aop(bu,1006,5) ):
                lzbir =  aop(bu,1007,5) 
                dzbir =  aop(bu,1005,5)-aop(bu,1006,5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1007 kol. 5 = AOP-u (1005 - 1006) kol. 5, ako je AOP 1005 kol. 5 > AOP-a 1006 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10016
        if( aop(bu,1005,6) > aop(bu,1006,6) ):
            if not( aop(bu,1007,6) == aop(bu,1005,6)-aop(bu,1006,6) ):
                lzbir =  aop(bu,1007,6) 
                dzbir =  aop(bu,1005,6)-aop(bu,1006,6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1007 kol. 6 = AOP-u (1005 - 1006) kol. 6, ako je AOP 1005 kol. 6 > AOP-a 1006 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10017
        if( aop(bu,1005,5) < aop(bu,1006,5) ):
            if not( aop(bu,1008,5) == aop(bu,1006,5)-aop(bu,1005,5) ):
                lzbir =  aop(bu,1008,5) 
                dzbir =  aop(bu,1006,5)-aop(bu,1005,5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1008 kol. 5 = AOP-u (1006 - 1005) kol. 5, ako je AOP 1005 kol. 5 < AOP-a 1006 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10018
        if( aop(bu,1005,6) < aop(bu,1006,6) ):
            if not( aop(bu,1008,6) == aop(bu,1006,6)-aop(bu,1005,6) ):
                lzbir =  aop(bu,1008,6) 
                dzbir =  aop(bu,1006,6)-aop(bu,1005,6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1008 kol. 6 = AOP-u (1006 - 1005) kol. 6, ako je AOP 1005 kol. 6 < AOP-a 1006 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10019
        if( aop(bu,1005,5) == aop(bu,1006,5) ):
            if not( suma(bu,1007,1008,5) == 0 ):
                lzbir =  suma(bu,1007,1008,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1007 + 1008) kol. 5 = 0, ako je AOP 1005 kol. 5 = AOP-u 1006 kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10020
        if( aop(bu,1005,6) == aop(bu,1006,6) ):
            if not( suma(bu,1007,1008,6) == 0 ):
                lzbir =  suma(bu,1007,1008,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1007 + 1008) kol. 6 = 0, ako je AOP 1005 kol. 6 = AOP-u 1006 kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10021
        if( aop(bu,1007,5) > 0 ):
            if not( aop(bu,1008,5) == 0 ):
                lzbir =  aop(bu,1008,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1007 kol. 5 > 0, onda je AOP 1008 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihod i rashod '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10022
        if( aop(bu,1008,5) > 0 ):
            if not( aop(bu,1007,5) == 0 ):
                lzbir =  aop(bu,1007,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1008 kol. 5 > 0, onda je AOP 1007 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihod i rashod '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10023
        if( aop(bu,1007,6) > 0 ):
            if not( aop(bu,1008,6) == 0 ):
                lzbir =  aop(bu,1008,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1007 kol. 6 > 0, onda je AOP 1008 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihod i rashod '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10024
        if( aop(bu,1008,6) > 0 ):
            if not( aop(bu,1007,6) == 0 ):
                lzbir =  aop(bu,1007,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1008 kol. 6 > 0, onda je AOP 1007 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihod i rashod '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10025
        if not( suma_liste(bu,[1005,1008],5) == suma(bu,1006,1007,5) ):
            lzbir =  suma_liste(bu,[1005,1008],5) 
            dzbir =  suma(bu,1006,1007,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1005 + 1008) kol. 5 = AOP-u (1006 + 1007) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10026
        if not( suma_liste(bu,[1005,1008],6) == suma(bu,1006,1007,6) ):
            lzbir =  suma_liste(bu,[1005,1008],6) 
            dzbir =  suma(bu,1006,1007,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1005 + 1008) kol. 6 = AOP-u (1006 + 1007) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10027
        if( aop(bu,1009,5) > 0 ):
            if not( aop(bu,1010,5) == 0 ):
                lzbir =  aop(bu,1010,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1009 kol. 5 > 0, onda je AOP 1010 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10028
        if( aop(bu,1010,5) > 0 ):
            if not( aop(bu,1009,5) == 0 ):
                lzbir =  aop(bu,1009,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1010 kol. 5 > 0, onda je AOP 1009 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10029
        if( aop(bu,1009,6) > 0 ):
            if not( aop(bu,1010,6) == 0 ):
                lzbir =  aop(bu,1010,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1009 kol. 6 > 0, onda je AOP 1010 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10030
        if( aop(bu,1010,6) > 0 ):
            if not( aop(bu,1009,6) == 0 ):
                lzbir =  aop(bu,1009,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1010 kol. 6 > 0, onda je AOP 1009 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10031
        if( aop(bu,1011,5) > 0 ):
            if not( aop(bu,1012,5) == 0 ):
                lzbir =  aop(bu,1012,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1011 kol. 5 > 0, onda je AOP 1012 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10032
        if( aop(bu,1012,5) > 0 ):
            if not( aop(bu,1011,5) == 0 ):
                lzbir =  aop(bu,1011,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1012 kol. 5 > 0, onda je AOP 1011 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10033
        if( aop(bu,1011,6) > 0 ):
            if not( aop(bu,1012,6) == 0 ):
                lzbir =  aop(bu,1012,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1011 kol. 6 > 0, onda je AOP 1012 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10034
        if( aop(bu,1012,6) > 0 ):
            if not( aop(bu,1011,6) == 0 ):
                lzbir =  aop(bu,1011,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1012 kol. 6 > 0, onda je AOP 1011 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10035
        if( aop(bu,1013,5) > 0 ):
            if not( aop(bu,1014,5) == 0 ):
                lzbir =  aop(bu,1014,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1013 kol. 5 > 0, onda je AOP 1014 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10036
        if( aop(bu,1014,5) > 0 ):
            if not( aop(bu,1013,5) == 0 ):
                lzbir =  aop(bu,1013,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 1014 kol. 5 > 0, onda je AOP 1013 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10037
        if( aop(bu,1013,6) > 0 ):
            if not( aop(bu,1014,6) == 0 ):
                lzbir =  aop(bu,1014,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1013 kol. 6 > 0, onda je AOP 1014 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10038
        if( aop(bu,1014,6) > 0 ):
            if not( aop(bu,1013,6) == 0 ):
                lzbir =  aop(bu,1013,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1014 kol. 6 > 0, onda je AOP 1013 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10039
        if( aop(bu,1015,5) > 0 ):
            if not( aop(bu,1016,5) == 0 ):
                lzbir =  aop(bu,1016,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1015 kol. 5 > 0, onda je AOP 1016 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10040
        if( aop(bu,1016,5) > 0 ):
            if not( aop(bu,1015,5) == 0 ):
                lzbir =  aop(bu,1015,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1016 kol. 5 > 0, onda je AOP 1015 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10041
        if( aop(bu,1015,6) > 0 ):
            if not( aop(bu,1016,6) == 0 ):
                lzbir =  aop(bu,1016,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1015 kol. 6 > 0, onda je AOP 1016 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10042
        if( aop(bu,1016,6) > 0 ):
            if not( aop(bu,1015,6) == 0 ):
                lzbir =  aop(bu,1015,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 1016 kol. 6 > 0, onda je AOP 1015 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10043
        if( aop(bu,1017,5) > 0 ):
            if not( aop(bu,1018,5) == 0 ):
                lzbir =  aop(bu,1018,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1017 kol. 5 > 0, onda je AOP 1018 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10044
        if( aop(bu,1018,5) > 0 ):
            if not( aop(bu,1017,5) == 0 ):
                lzbir =  aop(bu,1017,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 1018 kol. 5 > 0, onda je AOP 1017 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10045
        if( aop(bu,1017,6) > 0 ):
            if not( aop(bu,1018,6) == 0 ):
                lzbir =  aop(bu,1018,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1017 kol. 6 > 0, onda je AOP 1018 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10046
        if( aop(bu,1018,6) > 0 ):
            if not( aop(bu,1017,6) == 0 ):
                lzbir =  aop(bu,1017,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1018 kol. 6 > 0, onda je AOP 1017 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10047
        if( aop(bu,1019,5) > 0 ):
            if not( aop(bu,1020,5) == 0 ):
                lzbir =  aop(bu,1020,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1019 kol. 5 > 0, onda je AOP 1020 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10048
        if( aop(bu,1020,5) > 0 ):
            if not( aop(bu,1019,5) == 0 ):
                lzbir =  aop(bu,1019,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 1020 kol. 5 > 0, onda je AOP 1019 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10049
        if( aop(bu,1019,6) > 0 ):
            if not( aop(bu,1020,6) == 0 ):
                lzbir =  aop(bu,1020,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1019 kol. 6 > 0, onda je AOP 1020 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10050
        if( aop(bu,1020,6) > 0 ):
            if not( aop(bu,1019,6) == 0 ):
                lzbir =  aop(bu,1019,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1020 kol. 6 > 0, onda je AOP 1019 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10051
        if( aop(bu,1021,5) > 0 ):
            if not( aop(bu,1022,5) == 0 ):
                lzbir =  aop(bu,1022,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1021 kol. 5 > 0, onda je AOP 1022 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihod i rashod '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10052
        if( aop(bu,1022,5) > 0 ):
            if not( aop(bu,1021,5) == 0 ):
                lzbir =  aop(bu,1021,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 1022 kol. 5 > 0, onda je AOP 1021 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihod i rashod '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10053
        if( aop(bu,1021,6) > 0 ):
            if not( aop(bu,1022,6) == 0 ):
                lzbir =  aop(bu,1022,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1021 kol. 6 > 0, onda je AOP 1022 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihod i rashod '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10054
        if( aop(bu,1022,6) > 0 ):
            if not( aop(bu,1021,6) == 0 ):
                lzbir =  aop(bu,1021,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1022 kol. 6 > 0, onda je AOP 1021 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihod i rashod '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10055
        if( aop(bu,1023,5) > 0 ):
            if not( aop(bu,1024,5) == 0 ):
                lzbir =  aop(bu,1024,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1023 kol. 5 > 0, onda je AOP 1024 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihod i rashod '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10056
        if( aop(bu,1024,5) > 0 ):
            if not( aop(bu,1023,5) == 0 ):
                lzbir =  aop(bu,1023,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 1024 kol. 5 > 0, onda je AOP 1023 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihod i rashod '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10057
        if( aop(bu,1023,6) > 0 ):
            if not( aop(bu,1024,6) == 0 ):
                lzbir =  aop(bu,1024,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1023 kol. 6 > 0, onda je AOP 1024 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihod i rashod '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10058
        if( aop(bu,1024,6) > 0 ):
            if not( aop(bu,1023,6) == 0 ):
                lzbir =  aop(bu,1023,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1024 kol. 6 > 0, onda je AOP 1023 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihod i rashod '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10059
        if( suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],5) > suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],5) ):
            if not( aop(bu,1026,5) == suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],5)-suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],5) ):
                lzbir =  aop(bu,1026,5) 
                dzbir =  suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],5)-suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1026 kol. 5 = AOP-u (1003 - 1004 + 1007 - 1008 + 1009 - 1010 + 1011 - 1012 + 1013 - 1014 + 1015 - 1016 + 1017 - 1018 + 1019 - 1020 + 1021 - 1022 + 1023 - 1024 + 1025) kol. 5, ako je AOP (1003 + 1007 + 1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025) kol. 5 > AOP-a (1004 + 1008 + 1010 + 1012 + 1014 + 1016 + 1018 + 1020 + 1022 + 1024) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10060
        if( suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],6) > suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],6) ):
            if not( aop(bu,1026,6) == suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],6)-suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],6) ):
                lzbir =  aop(bu,1026,6) 
                dzbir =  suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],6)-suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1026 kol. 6 = AOP-u (1003 - 1004 + 1007 - 1008 + 1009 - 1010 + 1011 - 1012 + 1013 - 1014 + 1015 - 1016 + 1017 - 1018 + 1019 - 1020 + 1021 - 1022 + 1023 - 1024 + 1025) kol. 6, ako je AOP (1003 + 1007 + 1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025) kol. 6 > AOP-a (1004 + 1008 + 1010 + 1012 + 1014 + 1016 + 1018 + 1020 + 1022 + 1024) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10061
        if( suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],5) < suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],5) ):
            if not( aop(bu,1027,5) == suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],5)-suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],5) ):
                lzbir =  aop(bu,1027,5) 
                dzbir =  suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],5)-suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1027 kol. 5 = AOP-u (1004 - 1003 - 1007 + 1008 - 1009 + 1010 - 1011 + 1012 - 1013 + 1014 - 1015  + 1016 - 1017 + 1018 - 1019 + 1020 - 1021 + 1022 - 1023 + 1024 - 1025) kol. 5, ako je AOP (1003 + 1007 + 1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025) kol. 5 < AOP-a (1004 + 1008 + 1010 + 1012 + 1014 + 1016 + 1018 + 1020 + 1022 + 1024) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10062
        if( suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],6) < suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],6) ):
            if not( aop(bu,1027,6) == suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],6)-suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],6) ):
                lzbir =  aop(bu,1027,6) 
                dzbir =  suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],6)-suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1027 kol. 6 = AOP-u (1004 - 1003 - 1007 + 1008 - 1009 + 1010 - 1011 + 1012 - 1013 + 1014 - 1015  + 1016 - 1017 + 1018 - 1019 + 1020 - 1021 + 1022 - 1023 + 1024 - 1025) kol. 6, ako je AOP (1003 + 1007 + 1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025) kol. 6 < AOP-a (1004 + 1008 + 1010 + 1012 + 1014 + 1016 + 1018 + 1020 + 1022 + 1024) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10063
        if( suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],5) == suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],5) ):
            if not( suma(bu,1026,1027,5) == 0 ):
                lzbir =  suma(bu,1026,1027,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1026 + 1027) kol. 5 = 0, ako je AOP (1003 + 1007 + 1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025) kol. 5 = AOP-u (1004 + 1008 + 1010 + 1012 + 1014 + 1016 + 1018 + 1020 + 1022 + 1024) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10064
        if( suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],6) == suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],6) ):
            if not( suma(bu,1026,1027,6) == 0 ):
                lzbir =  suma(bu,1026,1027,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1026 + 1027) kol. 6 = 0, ako je AOP (1003 + 1007 + 1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025) kol. 6 = AOP-u (1004 + 1008 + 1010 + 1012 + 1014 + 1016 + 1018 + 1020 + 1022 + 1024) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10065
        if( aop(bu,1026,5) > 0 ):
            if not( aop(bu,1027,5) == 0 ):
                lzbir =  aop(bu,1027,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1026 kol. 5 > 0, onda je AOP 1027 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani ukupan neto poslovni prihod i ukupan neto poslovni rashod '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10066
        if( aop(bu,1027,5) > 0 ):
            if not( aop(bu,1026,5) == 0 ):
                lzbir =  aop(bu,1026,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 1027 kol. 5 > 0, onda je AOP 1026 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani ukupan neto poslovni prihod i ukupan neto poslovni rashod '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10067
        if( aop(bu,1026,6) > 0 ):
            if not( aop(bu,1027,6) == 0 ):
                lzbir =  aop(bu,1027,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1026 kol. 6 > 0, onda je AOP 1027 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani ukupan neto poslovni prihod i ukupan neto poslovni rashod '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10068
        if( aop(bu,1027,6) > 0 ):
            if not( aop(bu,1026,6) == 0 ):
                lzbir =  aop(bu,1026,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 1027 kol. 6 > 0, onda je AOP 1026 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani ukupan neto poslovni prihod i ukupan neto poslovni rashod '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10069
        if not( suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025,1027],5) == suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024,1026],5) ):
            lzbir =  suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025,1027],5) 
            dzbir =  suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024,1026],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1003 + 1007 + 1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025 +1027) kol. 5 = AOP-u (1004 + 1008 + 1010 + 1012 + 1014 + 1016 + 1018 + 1020 + 1022 + 1024 + 1026) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10070
        if not( suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025,1027],6) == suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024,1026],6) ):
            lzbir =  suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025,1027],6) 
            dzbir =  suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024,1026],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1003 + 1007 + 1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025 +1027) kol. 6 = AOP-u (1004 + 1008 + 1010 + 1012 + 1014 + 1016 + 1018 + 1020 + 1022 + 1024 + 1026) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10071
        if( suma_liste(bu,[1026,1030],5) > suma_liste(bu,[1027,1028,1029,1031],5) ):
            if not( aop(bu,1032,5) == suma_liste(bu,[1026,1030],5)-suma_liste(bu,[1027,1028,1029,1031],5) ):
                lzbir =  aop(bu,1032,5) 
                dzbir =  suma_liste(bu,[1026,1030],5)-suma_liste(bu,[1027,1028,1029,1031],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1032 kol. 5 = AOP- u (1026 - 1027 - 1028 - 1029 + 1030 - 1031 ) kol. 5, ako je AOP (1026 + 1030) kol. 5 > AOP-a (1027 + 1028 + 1029 + 1031) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10072
        if( suma_liste(bu,[1026,1030],6) > suma_liste(bu,[1027,1028,1029,1031],6) ):
            if not( aop(bu,1032,6) == suma_liste(bu,[1026,1030],6)-suma_liste(bu,[1027,1028,1029,1031],6) ):
                lzbir =  aop(bu,1032,6) 
                dzbir =  suma_liste(bu,[1026,1030],6)-suma_liste(bu,[1027,1028,1029,1031],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1032 kol. 6 = AOP- u (1026 - 1027 - 1028 - 1029 + 1030 - 1031 ) kol. 6, ako je AOP (1026 + 1030) kol. 6 > AOP-a (1027 + 1028 + 1029 + 1031) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10073
        if( suma_liste(bu,[1026,1030],5) < suma_liste(bu,[1027,1028,1029,1031],5) ):
            if not( aop(bu,1033,5) == suma_liste(bu,[1027,1028,1029,1031],5)-suma_liste(bu,[1026,1030],5) ):
                lzbir =  aop(bu,1033,5) 
                dzbir =  suma_liste(bu,[1027,1028,1029,1031],5)-suma_liste(bu,[1026,1030],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1033 kol. 5 = AOP- u (1027 - 1026 + 1028 + 1029 - 1030 + 1031) kol. 5, ako je AOP (1026 + 1030) kol. 5 < AOP-a (1027 + 1028 + 1029 + 1031) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10074
        if( suma_liste(bu,[1026,1030],6) < suma_liste(bu,[1027,1028,1029,1031],6) ):
            if not( aop(bu,1033,6) == suma_liste(bu,[1027,1028,1029,1031],6)-suma_liste(bu,[1026,1030],6) ):
                lzbir =  aop(bu,1033,6) 
                dzbir =  suma_liste(bu,[1027,1028,1029,1031],6)-suma_liste(bu,[1026,1030],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1033 kol. 6 = AOP- u (1027 - 1026 + 1028 + 1029 - 1030 + 1031) kol. 6, ako je AOP (1026 + 1030) kol. 6 < AOP-a (1027 + 1028 + 1029 + 1031) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10075
        if( suma_liste(bu,[1026,1030],5) == suma_liste(bu,[1027,1028,1029,1031],5) ):
            if not( suma(bu,1032,1033,5) == 0 ):
                lzbir =  suma(bu,1032,1033,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1032 + 1033) kol. 5 = 0, ako je AOP (1026 + 1030) kol. 5 = AOP-u (1027 + 1028 + 1029 + 1031) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10076
        if( suma_liste(bu,[1026,1030],6) == suma_liste(bu,[1027,1028,1029,1031],6) ):
            if not( suma(bu,1032,1033,6) == 0 ):
                lzbir =  suma(bu,1032,1033,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1032 + 1033) kol. 6 = 0, ako je AOP (1026 + 1030) kol. 6 = AOP-u (1027 + 1028 + 1029 + 1031) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10077
        if( aop(bu,1032,5) > 0 ):
            if not( aop(bu,1033,5) == 0 ):
                lzbir =  aop(bu,1033,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1032 kol. 5 > 0, onda je AOP 1033 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10078
        if( aop(bu,1033,5) > 0 ):
            if not( aop(bu,1032,5) == 0 ):
                lzbir =  aop(bu,1032,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1033 kol. 5 > 0, onda je AOP 1032 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10079
        if( aop(bu,1032,6) > 0 ):
            if not( aop(bu,1033,6) == 0 ):
                lzbir =  aop(bu,1033,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1032 kol. 6 > 0, onda je AOP 1033 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10080
        if( aop(bu,1033,6) > 0 ):
            if not( aop(bu,1032,6) == 0 ):
                lzbir =  aop(bu,1032,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 1033 kol. 6 > 0, onda je AOP 1032 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10081
        if not( suma_liste(bu,[1026,1030,1033],5) == suma_liste(bu,[1027,1028,1029,1031,1032],5) ):
            lzbir =  suma_liste(bu,[1026,1030,1033],5) 
            dzbir =  suma_liste(bu,[1027,1028,1029,1031,1032],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1026 + 1030 + 1033) kol. 5 = AOP-u (1027 + 1028 + 1029 +1031 + 1032) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10082
        if not( suma_liste(bu,[1026,1030,1033],6) == suma_liste(bu,[1027,1028,1029,1031,1032],6) ):
            lzbir =  suma_liste(bu,[1026,1030,1033],6) 
            dzbir =  suma_liste(bu,[1027,1028,1029,1031,1032],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1026 + 1030 + 1033) kol. 6 = AOP-u (1027 + 1028 + 1029 +1031 + 1032) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10083
        if( suma_liste(bu,[1032,1035],5) > suma_liste(bu,[1033,1034,1036],5) ):
            if not( aop(bu,1037,5) == suma_liste(bu,[1032,1035],5)-suma_liste(bu,[1033,1034,1036],5) ):
                lzbir =  aop(bu,1037,5) 
                dzbir =  suma_liste(bu,[1032,1035],5)-suma_liste(bu,[1033,1034,1036],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1037 kol. 5 = AOP-u (1032 - 1033 - 1034 + 1035 - 1036) kol. 5, ako je AOP (1032 + 1035) kol. 5 > AOP-a (1033 + 1034 + 1036) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10084
        if( suma_liste(bu,[1032,1035],6) > suma_liste(bu,[1033,1034,1036],6) ):
            if not( aop(bu,1037,6) == suma_liste(bu,[1032,1035],6)-suma_liste(bu,[1033,1034,1036],6) ):
                lzbir =  aop(bu,1037,6) 
                dzbir =  suma_liste(bu,[1032,1035],6)-suma_liste(bu,[1033,1034,1036],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1037 kol. 6 = AOP-u (1032 - 1033 - 1034 + 1035 - 1036) kol. 6, ako je AOP (1032 + 1035) kol. 6 > AOP-a (1033 + 1034 + 1036) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10085
        if( suma_liste(bu,[1032,1035],5) < suma_liste(bu,[1033,1034,1036],5) ):
            if not( aop(bu,1038,5) == suma_liste(bu,[1033,1034,1036],5)-suma_liste(bu,[1032,1035],5) ):
                lzbir =  aop(bu,1038,5) 
                dzbir =  suma_liste(bu,[1033,1034,1036],5)-suma_liste(bu,[1032,1035],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1038 kol. 5 = AOP-u (1033 - 1032 + 1034 - 1035 + 1036) kol. 5, ako je AOP (1032 + 1035) kol. 5 < AOP-a (1033 + 1034 + 1036) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10086
        if( suma_liste(bu,[1032,1035],6) < suma_liste(bu,[1033,1034,1036],6) ):
            if not( aop(bu,1038,6) == suma_liste(bu,[1033,1034,1036],6)-suma_liste(bu,[1032,1035],6) ):
                lzbir =  aop(bu,1038,6) 
                dzbir =  suma_liste(bu,[1033,1034,1036],6)-suma_liste(bu,[1032,1035],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1038 kol. 6 = AOP-u (1033 - 1032 + 1034 - 1035 + 1036) kol. 6, ako je AOP (1032 + 1035) kol. 6 < AOP-a (1033 + 1034 + 1036) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10087
        if( suma_liste(bu,[1032,1035],5) == suma_liste(bu,[1033,1034,1036],5) ):
            if not( suma(bu,1037,1038,5) == 0 ):
                lzbir =  suma(bu,1037,1038,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1037 + 1038) kol. 5 = 0, ako je AOP (1032 + 1035) kol. 5 = AOP-u (1033 + 1034 + 1036) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10088
        if( suma_liste(bu,[1032,1035],6) == suma_liste(bu,[1033,1034,1036],6) ):
            if not( suma(bu,1037,1038,6) == 0 ):
                lzbir =  suma(bu,1037,1038,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1037 + 1038) kol. 6 = 0, ako je AOP (1032 + 1035) kol. 6 = AOP-u (1033 + 1034 + 1036) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10089
        if( aop(bu,1037,5) > 0 ):
            if not( aop(bu,1038,5) == 0 ):
                lzbir =  aop(bu,1038,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1037 kol. 5 > 0, onda je AOP 1038 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10090
        if( aop(bu,1038,5) > 0 ):
            if not( aop(bu,1037,5) == 0 ):
                lzbir =  aop(bu,1037,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1038 kol. 5 > 0, onda je AOP 1037 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10091
        if( aop(bu,1037,6) > 0 ):
            if not( aop(bu,1038,6) == 0 ):
                lzbir =  aop(bu,1038,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1037 kol. 6 > 0, onda je AOP 1038 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10092
        if( aop(bu,1038,6) > 0 ):
            if not( aop(bu,1037,6) == 0 ):
                lzbir =  aop(bu,1037,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1038 kol. 6 > 0, onda je AOP 1037 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10093
        if not( suma_liste(bu,[1032,1035,1038],5) == suma_liste(bu,[1033,1034,1036,1037],5) ):
            lzbir =  suma_liste(bu,[1032,1035,1038],5) 
            dzbir =  suma_liste(bu,[1033,1034,1036,1037],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1032 + 1035 + 1038) kol. 5 = AOP-u (1033 + 1034 + 1036 + 1037) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10094
        if not( suma_liste(bu,[1032,1035,1038],6) == suma_liste(bu,[1033,1034,1036,1037],6) ):
            lzbir =  suma_liste(bu,[1032,1035,1038],6) 
            dzbir =  suma_liste(bu,[1033,1034,1036,1037],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1032 + 1035 + 1038) kol. 6 = AOP-u (1033 + 1034 + 1036 + 1037) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10095
        if( aop(bu,1039,5) > 0 ):
            if not( aop(bu,1040,5) == 0 ):
                lzbir =  aop(bu,1040,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1039 kol. 5 > 0 onda je AOP 1040 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10096
        if( aop(bu,1040,5) > 0 ):
            if not( aop(bu,1039,5) == 0 ):
                lzbir =  aop(bu,1039,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 1040 kol. 5 > 0 onda je AOP 1039 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10097
        if( aop(bu,1039,6) > 0 ):
            if not( aop(bu,1040,6) == 0 ):
                lzbir =  aop(bu,1040,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1039 kol. 6 > 0 onda je AOP 1040 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10098
        if( aop(bu,1040,6) > 0 ):
            if not( aop(bu,1039,6) == 0 ):
                lzbir =  aop(bu,1039,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 1040 kol. 6 > 0 onda je AOP 1039 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10099
        if( suma_liste(bu,[1037,1039],5) > suma_liste(bu,[1038,1040],5) ):
            if not( aop(bu,1041,5) == suma_liste(bu,[1037,1039],5)-suma_liste(bu,[1038,1040],5) ):
                lzbir =  aop(bu,1041,5) 
                dzbir =  suma_liste(bu,[1037,1039],5)-suma_liste(bu,[1038,1040],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1041 kol. 5 = AOP-u (1037 - 1038 + 1039 - 1040) kol. 5, ako je AOP (1037 + 1039) kol. 5 > AOP-a (1038 + 1040) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10100
        if( suma_liste(bu,[1037,1039],6) > suma_liste(bu,[1038,1040],6) ):
            if not( aop(bu,1041,6) == suma_liste(bu,[1037,1039],6)-suma_liste(bu,[1038,1040],6) ):
                lzbir =  aop(bu,1041,6) 
                dzbir =  suma_liste(bu,[1037,1039],6)-suma_liste(bu,[1038,1040],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1041 kol. 6 = AOP-u (1037 - 1038 + 1039 - 1040) kol. 6, ako je AOP (1037 + 1039) kol. 6 > AOP-a (1038 + 1040) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10101
        if( suma_liste(bu,[1037,1039],5) < suma_liste(bu,[1038,1040],5) ):
            if not( aop(bu,1042,5) == suma_liste(bu,[1038,1040],5)-suma_liste(bu,[1037,1039],5) ):
                lzbir =  aop(bu,1042,5) 
                dzbir =  suma_liste(bu,[1038,1040],5)-suma_liste(bu,[1037,1039],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1042 kol. 5 = AOP-u (1038 - 1037 - 1039 + 1040) kol. 5, ako je AOP (1037 + 1039) kol. 5 < AOP-a (1038 + 1040) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10102
        if( suma_liste(bu,[1037,1039],6) < suma_liste(bu,[1038,1040],6) ):
            if not( aop(bu,1042,6) == suma_liste(bu,[1038,1040],6)-suma_liste(bu,[1037,1039],6) ):
                lzbir =  aop(bu,1042,6) 
                dzbir =  suma_liste(bu,[1038,1040],6)-suma_liste(bu,[1037,1039],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1042 kol. 6 = AOP-u (1038 - 1037 - 1039 + 1040) kol. 6, ako je AOP (1037 + 1039) kol. 6 < AOP-a (1038 + 1040) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10103
        if( suma_liste(bu,[1037,1039],5) == suma_liste(bu,[1038,1040],5) ):
            if not( suma(bu,1041,1042,5) == 0 ):
                lzbir =  suma(bu,1041,1042,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1041 + 1042) kol. 5 = 0, ako je AOP (1037 + 1039) kol. 5 = AOP-u (1038 + 1040) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10104
        if( suma_liste(bu,[1037,1039],6) == suma_liste(bu,[1038,1040],6) ):
            if not( suma(bu,1041,1042,6) == 0 ):
                lzbir =  suma(bu,1041,1042,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1041 + 1042) kol. 6 = 0, ako je AOP (1037 + 1039) kol. 6 = AOP-u (1038 + 1040) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10105
        if( aop(bu,1041,5) > 0 ):
            if not( aop(bu,1042,5) == 0 ):
                lzbir =  aop(bu,1042,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1041 kol. 5 > 0, onda je AOP 1042 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10106
        if( aop(bu,1042,5) > 0 ):
            if not( aop(bu,1041,5) == 0 ):
                lzbir =  aop(bu,1041,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 1042 kol. 5 > 0, onda je AOP 1041 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10107
        if( aop(bu,1041,6) > 0 ):
            if not( aop(bu,1042,6) == 0 ):
                lzbir =  aop(bu,1042,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1041 kol. 6 > 0, onda je AOP 1042 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10108
        if( aop(bu,1042,6) > 0 ):
            if not( aop(bu,1041,6) == 0 ):
                lzbir =  aop(bu,1041,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1042 kol. 6 > 0, onda je AOP 1041 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10109
        if not( suma_liste(bu,[1037,1039,1042],5) == suma_liste(bu,[1038,1040,1041],5) ):
            lzbir =  suma_liste(bu,[1037,1039,1042],5) 
            dzbir =  suma_liste(bu,[1038,1040,1041],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1037 + 1039 + 1042) kol. 5 = AOP-u (1038 + 1040 + 1041) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10110
        if not( suma_liste(bu,[1037,1039,1042],6) == suma_liste(bu,[1038,1040,1041],6) ):
            lzbir =  suma_liste(bu,[1037,1039,1042],6) 
            dzbir =  suma_liste(bu,[1038,1040,1041],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1037 + 1039 + 1042) kol. 6 = AOP-u (1038 + 1040 + 1041) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #IZVEŠTAJ O OSTALOM REZULTATU - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        #20001
        if not( suma(ioor,2001,2022,5) > 0 ):
            form_errors.append('Zbir podataka na oznakama za AOP (2001 do 2022) kol. 5 > 0 Izveštaj o ostalom rezultatu mora imati iskazane podatke za tekući izveštajni period; ')
        
        #20002
        if not( suma(ioor,2001,2022,6) > 0 ):
            form_errors.append('Zbir podataka na oznakama za AOP (2001 do 2022) kol. 6 > 0 Izveštaj o ostalom rezultatu mora imati iskazane podatke za prethodni izveštajni period; ')
        
        #20003
        if not( aop(ioor,2001,5) == aop(bu,1041,5) ):
            lzbir =  aop(ioor,2001,5) 
            dzbir =  aop(bu,1041,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 2001 kol. 5 = AOP-u 1041 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20004
        if not( aop(ioor,2001,6) == aop(bu,1041,6) ):
            lzbir =  aop(ioor,2001,6) 
            dzbir =  aop(bu,1041,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 2001 kol. 6 = AOP-u 1041 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20005
        if not( aop(ioor,2002,5) == aop(bu,1042,5) ):
            lzbir =  aop(ioor,2002,5) 
            dzbir =  aop(bu,1042,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 2002 kol. 5 = AOP-u 1042 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20006
        if not( aop(ioor,2002,6) == aop(bu,1042,6) ):
            lzbir =  aop(ioor,2002,6) 
            dzbir =  aop(bu,1042,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 2002 kol. 6 = AOP-u 1042 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20007
        if( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],5) > suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],5) ):
            if not( aop(ioor,2019,5) == suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],5)-suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],5) ):
                lzbir =  aop(ioor,2019,5) 
                dzbir =  suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],5)-suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 2019 kol. 5 = AOP-u (2003 - 2004 + 2005 - 2006 + 2007 - 2008 + 2009 - 2010 + 2011 - 2012 + 2013 - 2014 + 2015 - 2016 + 2017 - 2018) kol. 5, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017) kol. 5 > AOP-a (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20008
        if( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],6) > suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],6) ):
            if not( aop(ioor,2019,6) == suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],6)-suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],6) ):
                lzbir =  aop(ioor,2019,6) 
                dzbir =  suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],6)-suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 2019 kol. 6 = AOP-u (2003 - 2004 + 2005 - 2006 + 2007 - 2008 + 2009 - 2010 + 2011 - 2012 + 2013 - 2014 + 2015 - 2016 + 2017 - 2018) kol. 6, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017) kol. 6 > AOP-a (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20009
        if( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],5) < suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],5) ):
            if not( aop(ioor,2020,5) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],5)-suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],5) ):
                lzbir =  aop(ioor,2020,5) 
                dzbir =  suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],5)-suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 2020 kol. 5 = AOP-u (2004 - 2003 - 2005 + 2006 - 2007 + 2008 - 2009 + 2010 - 2011 + 2012 - 2013 + 2014 - 2015 + 2016 - 2017 + 2018) kol. 5, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017) kol. 5 < AOP-a (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20010
        if( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],6) < suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],6) ):
            if not( aop(ioor,2020,6) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],6)-suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],6) ):
                lzbir =  aop(ioor,2020,6) 
                dzbir =  suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],6)-suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 2020 kol. 6 = AOP-u (2004 - 2003 - 2005 + 2006 - 2007 + 2008 - 2009 + 2010 - 2011 + 2012 - 2013 + 2014 - 2015 + 2016 - 2017 + 2018) kol. 6, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017) kol. 6 < AOP-a (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20011
        if( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],5) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],5) ):
            if not( suma(ioor,2019,2020,5) == 0 ):
                lzbir =  suma(ioor,2019,2020,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (2019 + 2020) kol. 5 = 0, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017) kol. 5 = AOP-u (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20012
        if( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],6) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],6) ):
            if not( suma(ioor,2019,2020,6) == 0 ):
                lzbir =  suma(ioor,2019,2020,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (2019 + 2020) kol. 6 = 0, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017) kol. 6 = AOP-u (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20013
        if( aop(ioor,2019,5) > 0 ):
            if not( aop(ioor,2020,5) == 0 ):
                lzbir =  aop(ioor,2020,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 2019 kol. 5 > 0,onda je AOP 2020 kol. 5 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan pozitivan i  negativan ostali rezultat perioda '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20014
        if( aop(ioor,2020,5) > 0 ):
            if not( aop(ioor,2019,5) == 0 ):
                lzbir =  aop(ioor,2019,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 2020 kol. 5 > 0, onda je AOP 2019 kol. 5 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan pozitivan i  negativan ostali rezultat perioda '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20015
        if( aop(ioor,2019,6) > 0 ):
            if not( aop(ioor,2020,6) == 0 ):
                lzbir =  aop(ioor,2020,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 2019 kol. 6 > 0,onda je AOP 2020 kol. 6 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan pozitivan i  negativan ostali rezultat perioda '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20016
        if( aop(ioor,2020,6) > 0 ):
            if not( aop(ioor,2019,6) == 0 ):
                lzbir =  aop(ioor,2019,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 2020 kol. 6 > 0, onda je AOP 2019 kol. 6 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan pozitivan i  negativan ostali rezultat perioda '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20017
        if not( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2020],5) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2019],5) ):
            lzbir =  suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2020],5) 
            dzbir =  suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2019],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017 + 2020) kol. 5 = AOP-u (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018 + 2019) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20018
        if not( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2020],6) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2019],6) ):
            lzbir =  suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2020],6) 
            dzbir =  suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2019],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017 + 2020) kol. 6 = AOP-u (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018 + 2019) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20019
        if( suma_liste(ioor,[2001,2019],5) > suma_liste(ioor,[2002,2020],5) ):
            if not( aop(ioor,2021,5) == suma_liste(ioor,[2001,2019],5)-suma_liste(ioor,[2002,2020],5) ):
                lzbir =  aop(ioor,2021,5) 
                dzbir =  suma_liste(ioor,[2001,2019],5)-suma_liste(ioor,[2002,2020],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 2021 kol. 5 = AOP-u (2001 - 2002 + 2019 - 2020) kol. 5, ako je AOP (2001 + 2019) kol. 5 > AOP-a (2002 + 2020) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20020
        if( suma_liste(ioor,[2001,2019],6) > suma_liste(ioor,[2002,2020],6) ):
            if not( aop(ioor,2021,6) == suma_liste(ioor,[2001,2019],6)-suma_liste(ioor,[2002,2020],6) ):
                lzbir =  aop(ioor,2021,6) 
                dzbir =  suma_liste(ioor,[2001,2019],6)-suma_liste(ioor,[2002,2020],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 2021 kol. 6 = AOP-u (2001 - 2002 + 2019 - 2020) kol. 6, ako je AOP (2001 + 2019) kol. 6 > AOP-a (2002 + 2020) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20021
        if( suma_liste(ioor,[2001,2019],5) < suma_liste(ioor,[2002,2020],5) ):
            if not( aop(ioor,2022,5) == suma_liste(ioor,[2002,2020],5)-suma_liste(ioor,[2001,2019],5) ):
                lzbir =  aop(ioor,2022,5) 
                dzbir =  suma_liste(ioor,[2002,2020],5)-suma_liste(ioor,[2001,2019],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 2022 kol. 5 = AOP-u (2002 - 2001 - 2019 + 2020) kol. 5, ako je AOP (2001 + 2019) kol. 5 < AOP-a (2002 + 2020) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20022
        if( suma_liste(ioor,[2001,2019],6) < suma_liste(ioor,[2002,2020],6) ):
            if not( aop(ioor,2022,6) == suma_liste(ioor,[2002,2020],6)-suma_liste(ioor,[2001,2019],6) ):
                lzbir =  aop(ioor,2022,6) 
                dzbir =  suma_liste(ioor,[2002,2020],6)-suma_liste(ioor,[2001,2019],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 2022 kol. 6 = AOP-u (2002 - 2001 - 2019 + 2020) kol. 6, ako je AOP (2001 + 2019) kol. 6 < AOP-a (2002 + 2020) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20023
        if( suma_liste(ioor,[2001,2019],5) == suma_liste(ioor,[2002,2020],5) ):
            if not( suma(ioor,2021,2022,5) == 0 ):
                lzbir =  suma(ioor,2021,2022,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (2021 + 2022) kol. 5 = 0, ako je AOP (2001 + 2019) kol. 5 = AOP-u (2002 + 2020) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20024
        if( suma_liste(ioor,[2001,2019],6) == suma_liste(ioor,[2002,2020],6) ):
            if not( suma(ioor,2021,2022,6) == 0 ):
                lzbir =  suma(ioor,2021,2022,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (2021 + 2022) kol. 6 = 0, ako je AOP (2001 + 2019) kol. 6 = AOP-u (2002 + 2020) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20025
        if( aop(ioor,2021,5) > 0 ):
            if not( aop(ioor,2022,5) == 0 ):
                lzbir =  aop(ioor,2022,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 2021 kol. 5 > 0, onda je AOP 2022 kol. 5 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan pozitivan i negativan rezultat perioda '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20026
        if( aop(ioor,2022,5) > 0 ):
            if not( aop(ioor,2021,5) == 0 ):
                lzbir =  aop(ioor,2021,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 2022 kol. 5  > 0, onda je AOP 2021 kol. 5 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan pozitivan i negativan rezultat perioda '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20027
        if( aop(ioor,2021,6) > 0 ):
            if not( aop(ioor,2022,6) == 0 ):
                lzbir =  aop(ioor,2022,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 2021 kol. 6 > 0, onda je AOP 2022 kol. 6 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan pozitivan i negativan rezultat perioda '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20028
        if( aop(ioor,2022,6) > 0 ):
            if not( aop(ioor,2021,6) == 0 ):
                lzbir =  aop(ioor,2021,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 2022 kol. 6  > 0, onda je AOP 2021 kol. 6 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan pozitivan i negativan rezultat perioda '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20029
        if not( suma_liste(ioor,[2001,2019,2022],5) == suma_liste(ioor,[2002,2020,2021],5) ):
            lzbir =  suma_liste(ioor,[2001,2019,2022],5) 
            dzbir =  suma_liste(ioor,[2002,2020,2021],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (2001 + 2019 + 2022) kol. 5 = AOP-u (2002 + 2020 + 2021) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20030
        if not( suma_liste(ioor,[2001,2019,2022],6) == suma_liste(ioor,[2002,2020,2021],6) ):
            lzbir =  suma_liste(ioor,[2001,2019,2022],6) 
            dzbir =  suma_liste(ioor,[2002,2020,2021],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (2001 + 2019 + 2022) kol. 6 = AOP-u (2002 + 2020 + 2021) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #IZVEŠTAJ O TOKOVIMA GOTOVINE - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        #30001
        if not( suma(iotg,3001,3063,3) > 0 ):
            form_errors.append('Zbir podataka na oznakama za AOP (3001 do 3063) kol. 3 > 0 Izveštaj o tokovima gotovine mora imati iskazane podatke za tekući izveštajni period; ')
        
        #30002
        if not( suma(iotg,3001,3063,4) > 0 ):
            form_errors.append('Zbir podataka na oznakama za AOP (3001 do 3063) kol. 4 > 0 Izveštaj o tokovima gotovine mora imati iskazane podatke za prethodni izveštajni period; ')
        
        #30003
        if not( aop(iotg,3001,3) == suma(iotg,3002,3005,3) ):
            lzbir =  aop(iotg,3001,3) 
            dzbir =  suma(iotg,3002,3005,3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3001 kol. 3 = AOP-u (3002 + 3003 + 3004 + 3005) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30004
        if not( aop(iotg,3001,4) == suma(iotg,3002,3005,4) ):
            lzbir =  aop(iotg,3001,4) 
            dzbir =  suma(iotg,3002,3005,4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3001 kol. 4 = AOP-u (3002 + 3003 + 3004 + 3005) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30005
        if not( aop(iotg,3006,3) == suma(iotg,3007,3009,3) ):
            lzbir =  aop(iotg,3006,3) 
            dzbir =  suma(iotg,3007,3009,3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3006 kol. 3 = AOP-u (3007 + 3008 + 3009) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30006
        if not( aop(iotg,3006,4) == suma(iotg,3007,3009,4) ):
            lzbir =  aop(iotg,3006,4) 
            dzbir =  suma(iotg,3007,3009,4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3006 kol. 4 = AOP-u (3007 + 3008 + 3009) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30007
        if( aop(iotg,3001,3) > aop(iotg,3006,3) ):
            if not( aop(iotg,3010,3) == aop(iotg,3001,3)-aop(iotg,3006,3) ):
                lzbir =  aop(iotg,3010,3) 
                dzbir =  aop(iotg,3001,3)-aop(iotg,3006,3) 
                razlika = lzbir - dzbir
                form_errors.append(' AOP 3010 kol. 3 = AOP-u (3001 - 3006) kol. 3, ako je AOP 3001 kol. 3 > AOP-a 3006 kol. 3   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30008
        if( aop(iotg,3001,4) > aop(iotg,3006,4) ):
            if not( aop(iotg,3010,4) == aop(iotg,3001,4)-aop(iotg,3006,4) ):
                lzbir =  aop(iotg,3010,4) 
                dzbir =  aop(iotg,3001,4)-aop(iotg,3006,4) 
                razlika = lzbir - dzbir
                form_errors.append(' AOP 3010 kol. 4 = AOP-u (3001 - 3006) kol. 4, ako je AOP 3001 kol. 4 > AOP-a 3006 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30009
        if( aop(iotg,3001,3) < aop(iotg,3006,3) ):
            if not( aop(iotg,3011,3) == aop(iotg,3006,3)-aop(iotg,3001,3) ):
                lzbir =  aop(iotg,3011,3) 
                dzbir =  aop(iotg,3006,3)-aop(iotg,3001,3) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3011 kol. 3 = AOP-u (3006 - 3001) kol. 3 , ako je AOP 3001 kol. 3 < AOP-a 3006 kol. 3    '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30010
        if( aop(iotg,3001,4) < aop(iotg,3006,4) ):
            if not( aop(iotg,3011,4) == aop(iotg,3006,4)-aop(iotg,3001,4) ):
                lzbir =  aop(iotg,3011,4) 
                dzbir =  aop(iotg,3006,4)-aop(iotg,3001,4) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3011 kol. 4 = AOP-u (3006 - 3001) kol. 4 , ako je AOP 3001 kol. 4 < AOP-a 3006 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30011
        if( aop(iotg,3001,3) == aop(iotg,3006,3) ):
            if not( suma(iotg,3010,3011,3) == 0 ):
                lzbir =  suma(iotg,3010,3011,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (3010 + 3011) kol. 3 = 0, ako je AOP 3001 kol. 3 = AOP-u 3006 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30012
        if( aop(iotg,3001,4) == aop(iotg,3006,4) ):
            if not( suma(iotg,3010,3011,4) == 0 ):
                lzbir =  suma(iotg,3010,3011,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (3010 + 3011) kol. 4 = 0, ako je AOP 3001 kol. 4 = AOP-u 3006 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30013
        if( aop(iotg,3010,3) > 0 ):
            if not( aop(iotg,3011,3) == 0 ):
                lzbir =  aop(iotg,3011,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3010 kol. 3 > 0 onda je AOP 3011 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30014
        if( aop(iotg,3011,3) > 0 ):
            if not( aop(iotg,3010,3) == 0 ):
                lzbir =  aop(iotg,3010,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3011 kol. 3 > 0 onda je AOP 3010 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30015
        if( aop(iotg,3010,4) > 0 ):
            if not( aop(iotg,3011,4) == 0 ):
                lzbir =  aop(iotg,3011,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3010 kol. 4 > 0 onda je AOP 3011 kol. 4 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30016
        if( aop(iotg,3011,4) > 0 ):
            if not( aop(iotg,3010,4) == 0 ):
                lzbir =  aop(iotg,3010,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3011 kol. 4 > 0 onda je AOP 3010 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30017
        if not( suma_liste(iotg,[3001,3011],3) == suma_liste(iotg,[3006,3010],3) ):
            lzbir =  suma_liste(iotg,[3001,3011],3) 
            dzbir =  suma_liste(iotg,[3006,3010],3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (3001 + 3011) kol. 3 = AOP-u (3006 + 3010) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30018
        if not( suma_liste(iotg,[3001,3011],4) == suma_liste(iotg,[3006,3010],4) ):
            lzbir =  suma_liste(iotg,[3001,3011],4) 
            dzbir =  suma_liste(iotg,[3006,3010],4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (3001 + 3011) kol. 4 = AOP-u (3006 + 3010) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30019
        if not( aop(iotg,3012,3) == suma(iotg,3013,3018,3) ):
            lzbir =  aop(iotg,3012,3) 
            dzbir =  suma(iotg,3013,3018,3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3012 kol. 3 = AOP-u (3013 + 3014 + 3015 + 3016 + 3017 + 3018) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30020
        if not( aop(iotg,3012,4) == suma(iotg,3013,3018,4) ):
            lzbir =  aop(iotg,3012,4) 
            dzbir =  suma(iotg,3013,3018,4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3012 kol. 4 = AOP-u (3013 + 3014 + 3015 + 3016 + 3017 + 3018) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30021
        if not( aop(iotg,3019,3) == suma(iotg,3020,3025,3) ):
            lzbir =  aop(iotg,3019,3) 
            dzbir =  suma(iotg,3020,3025,3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3019 kol. 3 = AOP-u (3020 + 3021 + 3022 + 3023 + 3024 + 3025) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30022
        if not( aop(iotg,3019,4) == suma(iotg,3020,3025,4) ):
            lzbir =  aop(iotg,3019,4) 
            dzbir =  suma(iotg,3020,3025,4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3019 kol. 4 = AOP-u (3020 + 3021 + 3022 + 3023 + 3024 + 3025) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30023
        if( suma_liste(iotg,[3010,3012],3) > suma_liste(iotg,[3011,3019],3) ):
            if not( aop(iotg,3026,3) == suma_liste(iotg,[3010,3012],3)-suma_liste(iotg,[3011,3019],3) ):
                lzbir =  aop(iotg,3026,3) 
                dzbir =  suma_liste(iotg,[3010,3012],3)-suma_liste(iotg,[3011,3019],3) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3026 kol. 3 = AOP-u (3010 - 3011 + 3012 - 3019) kol. 3, ako je AOP (3010 + 3012) kol. 3 > AOP-a (3011 + 3019) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30024
        if( suma_liste(iotg,[3010,3012],4) > suma_liste(iotg,[3011,3019],4) ):
            if not( aop(iotg,3026,4) == suma_liste(iotg,[3010,3012],4)-suma_liste(iotg,[3011,3019],4) ):
                lzbir =  aop(iotg,3026,4) 
                dzbir =  suma_liste(iotg,[3010,3012],4)-suma_liste(iotg,[3011,3019],4) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3026 kol. 4 = AOP-u (3010 - 3011 + 3012 - 3019) kol. 4, ako je AOP (3010 + 3012) kol. 4 > AOP-a (3011 + 3019) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30025
        if( suma_liste(iotg,[3010,3012],3) < suma_liste(iotg,[3011,3019],3) ):
            if not( aop(iotg,3027,3) == suma_liste(iotg,[3011,3019],3)-suma_liste(iotg,[3010,3012],3) ):
                lzbir =  aop(iotg,3027,3) 
                dzbir =  suma_liste(iotg,[3011,3019],3)-suma_liste(iotg,[3010,3012],3) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3027 kol. 3 = AOP-u (3011 - 3010 - 3012 + 3019) kol. 3, ako je AOP (3010 + 3012) kol. 3 < AOP-a (3011 + 3019) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30026
        if( suma_liste(iotg,[3010,3012],4) < suma_liste(iotg,[3011,3019],4) ):
            if not( aop(iotg,3027,4) == suma_liste(iotg,[3011,3019],4)-suma_liste(iotg,[3010,3012],4) ):
                lzbir =  aop(iotg,3027,4) 
                dzbir =  suma_liste(iotg,[3011,3019],4)-suma_liste(iotg,[3010,3012],4) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3027 kol. 4 = AOP-u (3011 - 3010 - 3012 + 3019) kol. 4, ako je AOP (3010 + 3012) kol. 4 < AOP-a (3011 + 3019) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30027
        if( suma_liste(iotg,[3010,3012],3) == suma_liste(iotg,[3011,3019],3) ):
            if not( suma(iotg,3026,3027,3) == 0 ):
                lzbir =  suma(iotg,3026,3027,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (3026 + 3027) kol. 3 = 0, ako je AOP (3010 + 3012) kol. 3 = AOP-u (3011 + 3019) kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30028
        if( suma_liste(iotg,[3010,3012],4) == suma_liste(iotg,[3011,3019],4) ):
            if not( suma(iotg,3026,3027,4) == 0 ):
                lzbir =  suma(iotg,3026,3027,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (3026 + 3027) kol. 4 = 0, ako je AOP (3010 + 3012) kol. 4 = AOP-u (3011 + 3019) kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30029
        if( aop(iotg,3026,3) > 0 ):
            if not( aop(iotg,3027,3) == 0 ):
                lzbir =  aop(iotg,3027,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3026 kol. 3 > 0 onda je AOP 3027 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30030
        if( aop(iotg,3027,3) > 0 ):
            if not( aop(iotg,3026,3) == 0 ):
                lzbir =  aop(iotg,3026,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3027 kol. 3 > 0 onda je AOP 3026 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30031
        if( aop(iotg,3026,4) > 0 ):
            if not( aop(iotg,3027,4) == 0 ):
                lzbir =  aop(iotg,3027,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3026 kol. 4 > 0 onda je AOP 3027 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30032
        if( aop(iotg,3027,4) > 0 ):
            if not( aop(iotg,3026,4) == 0 ):
                lzbir =  aop(iotg,3026,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3027 kol. 4 > 0 onda je AOP 3026 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30033
        if not( suma_liste(iotg,[3010,3012,3027],3) == suma_liste(iotg,[3011,3019,3026],3) ):
            lzbir =  suma_liste(iotg,[3010,3012,3027],3) 
            dzbir =  suma_liste(iotg,[3011,3019,3026],3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (3010 + 3012 + 3027) kol. 3 = AOP-u (3011 + 3019 + 3026) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30034
        if not( suma_liste(iotg,[3010,3012,3027],4) == suma_liste(iotg,[3011,3019,3026],4) ):
            lzbir =  suma_liste(iotg,[3010,3012,3027],4) 
            dzbir =  suma_liste(iotg,[3011,3019,3026],4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (3010 + 3012 + 3027) kol. 4 = AOP-u (3011 + 3019 + 3026) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30035
        if( aop(iotg,3026,3) > suma(iotg,3027,3029,3) ):
            if not( aop(iotg,3030,3) == aop(iotg,3026,3)-suma(iotg,3027,3029,3) ):
                lzbir =  aop(iotg,3030,3) 
                dzbir =  aop(iotg,3026,3)-suma(iotg,3027,3029,3) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3030 kol. 3 = AOP-u (3026 - 3027 - 3028 - 3029) kol. 3, ako je AOP 3026 kol. 3 > AOP-a (3027 + 3028 + 3029) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30036
        if( aop(iotg,3026,4) > suma(iotg,3027,3029,4) ):
            if not( aop(iotg,3030,4) == aop(iotg,3026,4)-suma(iotg,3027,3029,4) ):
                lzbir =  aop(iotg,3030,4) 
                dzbir =  aop(iotg,3026,4)-suma(iotg,3027,3029,4) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3030 kol. 4 = AOP-u (3026 - 3027 - 3028 - 3029) kol. 4, ako je AOP 3026 kol. 4 > AOP-a (3027 + 3028 + 3029) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30037
        if( aop(iotg,3026,3) < suma(iotg,3027,3029,3) ):
            if not( aop(iotg,3031,3) == suma(iotg,3027,3029,3)-aop(iotg,3026,3) ):
                lzbir =  aop(iotg,3031,3) 
                dzbir =  suma(iotg,3027,3029,3)-aop(iotg,3026,3) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3031 kol. 3 = AOP-u (3027 - 3026 + 3028 + 3029) kol. 3,  ako je AOP 3026 kol. 3 < AOP-a (3027 + 3028 + 3029) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30038
        if( aop(iotg,3026,4) < suma(iotg,3027,3029,4) ):
            if not( aop(iotg,3031,4) == suma(iotg,3027,3029,4)-aop(iotg,3026,4) ):
                lzbir =  aop(iotg,3031,4) 
                dzbir =  suma(iotg,3027,3029,4)-aop(iotg,3026,4) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3031 kol. 4 = AOP-u (3027 - 3026 + 3028 + 3029) kol. 4,  ako je AOP 3026 kol. 4 < AOP-a (3027 + 3028 + 3029) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30039
        if( aop(iotg,3026,3) == suma(iotg,3027,3029,3) ):
            if not( suma(iotg,3030,3031,3) == 0 ):
                lzbir =  suma(iotg,3030,3031,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (3030 + 3031) kol. 3 = 0, ako je AOP 3026 kol. 3 = AOP-u (3027 + 3028 + 3029) kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30040
        if( aop(iotg,3026,4) == suma(iotg,3027,3029,4) ):
            if not( suma(iotg,3030,3031,4) == 0 ):
                lzbir =  suma(iotg,3030,3031,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (3030 + 3031) kol. 4 = 0, ako je AOP 3026 kol. 4 = AOP-u (3027 + 3028 + 3029) kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30041
        if( aop(iotg,3030,3) > 0 ):
            if not( aop(iotg,3031,3) == 0 ):
                lzbir =  aop(iotg,3031,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3030 kol. 3 > 0 onda je AOP 3031 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30042
        if( aop(iotg,3031,3) > 0 ):
            if not( aop(iotg,3030,3) == 0 ):
                lzbir =  aop(iotg,3030,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3031 kol. 3 > 0 onda je AOP 3030 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30043
        if( aop(iotg,3030,4) > 0 ):
            if not( aop(iotg,3031,4) == 0 ):
                lzbir =  aop(iotg,3031,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3030 kol. 4 > 0 onda je AOP 3031 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30044
        if( aop(iotg,3031,4) > 0 ):
            if not( aop(iotg,3030,4) == 0 ):
                lzbir =  aop(iotg,3030,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3031 kol. 4 > 0 onda je AOP 3030 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30045
        if not( suma_liste(iotg,[3026,3031],3) == suma(iotg,3027,3030,3) ):
            lzbir =  suma_liste(iotg,[3026,3031],3) 
            dzbir =  suma(iotg,3027,3030,3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (3026 + 3031) kol. 3 = AOP-u (3027 + 3028 + 3029 + 3030) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30046
        if not( suma_liste(iotg,[3026,3031],4) == suma(iotg,3027,3030,4) ):
            lzbir =  suma_liste(iotg,[3026,3031],4) 
            dzbir =  suma(iotg,3027,3030,4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (3026 + 3031) kol. 4 = AOP-u (3027 + 3028 + 3029 + 3030) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30047
        if not( aop(iotg,3032,3) == suma(iotg,3033,3037,3) ):
            lzbir =  aop(iotg,3032,3) 
            dzbir =  suma(iotg,3033,3037,3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3032 kol. 3 = AOP-u (3033 + 3034 + 3035 + 3036 + 3037) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30048
        if not( aop(iotg,3032,4) == suma(iotg,3033,3037,4) ):
            lzbir =  aop(iotg,3032,4) 
            dzbir =  suma(iotg,3033,3037,4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3032 kol. 4 = AOP-u (3033 + 3034 + 3035 + 3036 + 3037) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30049
        if not( aop(iotg,3038,3) == suma(iotg,3039,3043,3) ):
            lzbir =  aop(iotg,3038,3) 
            dzbir =  suma(iotg,3039,3043,3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3038 kol. 3 = AOP-u (3039 + 3040 + 3041 + 3042 + 3043) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30050
        if not( aop(iotg,3038,4) == suma(iotg,3039,3043,4) ):
            lzbir =  aop(iotg,3038,4) 
            dzbir =  suma(iotg,3039,3043,4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3038 kol. 4 = AOP-u (3039 + 3040 + 3041 + 3042 + 3043) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30051
        if( aop(iotg,3032,3) > aop(iotg,3038,3) ):
            if not( aop(iotg,3044,3) == aop(iotg,3032,3)-aop(iotg,3038,3) ):
                lzbir =  aop(iotg,3044,3) 
                dzbir =  aop(iotg,3032,3)-aop(iotg,3038,3) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3044 kol. 3 = AOP-u (3032 - 3038) kol. 3, ako je AOP 3032 kol. 3 > AOP-a 3038 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30052
        if( aop(iotg,3032,4) > aop(iotg,3038,4) ):
            if not( aop(iotg,3044,4) == aop(iotg,3032,4)-aop(iotg,3038,4) ):
                lzbir =  aop(iotg,3044,4) 
                dzbir =  aop(iotg,3032,4)-aop(iotg,3038,4) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3044 kol. 4 = AOP-u (3032 - 3038) kol. 4, ako je AOP 3032 kol. 4 > AOP-a 3038 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30053
        if( aop(iotg,3032,3) < aop(iotg,3038,3) ):
            if not( aop(iotg,3045,3) == aop(iotg,3038,3)-aop(iotg,3032,3) ):
                lzbir =  aop(iotg,3045,3) 
                dzbir =  aop(iotg,3038,3)-aop(iotg,3032,3) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3045 kol. 3 = AOP-u (3038 - 3032) kol. 3, ako je AOP 3032 kol. 3 < AOP-a 3038 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30054
        if( aop(iotg,3032,4) < aop(iotg,3038,4) ):
            if not( aop(iotg,3045,4) == aop(iotg,3038,4)-aop(iotg,3032,4) ):
                lzbir =  aop(iotg,3045,4) 
                dzbir =  aop(iotg,3038,4)-aop(iotg,3032,4) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3045 kol. 4 = AOP-u (3038 - 3032) kol. 4, ako je AOP 3032 kol. 4 < AOP-a 3038 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30055
        if( aop(iotg,3032,3) == aop(iotg,3038,3) ):
            if not( suma(iotg,3044,3045,3) == 0 ):
                lzbir =  suma(iotg,3044,3045,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (3044 + 3045) kol. 3 = 0,  ako je AOP 3032 kol. 3 = AOP-u 3038 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30056
        if( aop(iotg,3032,4) == aop(iotg,3038,4) ):
            if not( suma(iotg,3044,3045,4) == 0 ):
                lzbir =  suma(iotg,3044,3045,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (3044 + 3045) kol. 4 = 0,  ako je AOP 3032 kol. 4 = AOP-u 3038 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30057
        if( aop(iotg,3044,3) > 0 ):
            if not( aop(iotg,3045,3) == 0 ):
                lzbir =  aop(iotg,3045,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3044 kol. 3 > 0 onda je AOP 3045 kol. 3 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30058
        if( aop(iotg,3045,3) > 0 ):
            if not( aop(iotg,3044,3) == 0 ):
                lzbir =  aop(iotg,3044,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3045 kol. 3 > 0 onda je AOP 3044 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30059
        if( aop(iotg,3044,4) > 0 ):
            if not( aop(iotg,3045,4) == 0 ):
                lzbir =  aop(iotg,3045,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3044 kol. 4 > 0 onda je AOP 3045 kol. 4 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30060
        if( aop(iotg,3045,4) > 0 ):
            if not( aop(iotg,3044,4) == 0 ):
                lzbir =  aop(iotg,3044,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3045 kol. 4 > 0 onda je AOP 3044 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30061
        if not( suma_liste(iotg,[3032,3045],3) == suma_liste(iotg,[3038,3044],3) ):
            lzbir =  suma_liste(iotg,[3032,3045],3) 
            dzbir =  suma_liste(iotg,[3038,3044],3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP ( 3032 + 3045) kol. 3 = AOP-u (3038 + 3044) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30062
        if not( suma_liste(iotg,[3032,3045],4) == suma_liste(iotg,[3038,3044],4) ):
            lzbir =  suma_liste(iotg,[3032,3045],4) 
            dzbir =  suma_liste(iotg,[3038,3044],4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP ( 3032 + 3045) kol. 4 = AOP-u (3038 + 3044) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30063
        if not( aop(iotg,3046,3) == suma(iotg,3047,3049,3) ):
            lzbir =  aop(iotg,3046,3) 
            dzbir =  suma(iotg,3047,3049,3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3046 kol. 3 = AOP-u (3047 + 3048 + 3049) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30064
        if not( aop(iotg,3046,4) == suma(iotg,3047,3049,4) ):
            lzbir =  aop(iotg,3046,4) 
            dzbir =  suma(iotg,3047,3049,4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3046 kol. 4 = AOP-u (3047 + 3048 + 3049) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30065
        if not( aop(iotg,3050,3) == suma(iotg,3051,3053,3) ):
            lzbir =  aop(iotg,3050,3) 
            dzbir =  suma(iotg,3051,3053,3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3050 kol. 3 = AOP-u (3051 + 3052 + 3053) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30066
        if not( aop(iotg,3050,4) == suma(iotg,3051,3053,4) ):
            lzbir =  aop(iotg,3050,4) 
            dzbir =  suma(iotg,3051,3053,4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3050 kol. 4 = AOP-u (3051 + 3052 + 3053) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30067
        if( aop(iotg,3046,3) > aop(iotg,3050,3) ):
            if not( aop(iotg,3054,3) == aop(iotg,3046,3)-aop(iotg,3050,3) ):
                lzbir =  aop(iotg,3054,3) 
                dzbir =  aop(iotg,3046,3)-aop(iotg,3050,3) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3054 kol. 3 = AOP-u (3046 - 3050) kol. 3 , ako je AOP 3046 kol. 3 > AOP-a 3050 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30068
        if( aop(iotg,3046,4) > aop(iotg,3050,4) ):
            if not( aop(iotg,3054,4) == aop(iotg,3046,4)-aop(iotg,3050,4) ):
                lzbir =  aop(iotg,3054,4) 
                dzbir =  aop(iotg,3046,4)-aop(iotg,3050,4) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3054 kol. 4 = AOP-u (3046 - 3050) kol. 4 , ako je AOP 3046 kol. 4 > AOP-a 3050 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30069
        if( aop(iotg,3046,3) < aop(iotg,3050,3) ):
            if not( aop(iotg,3055,3) == aop(iotg,3050,3)-aop(iotg,3046,3) ):
                lzbir =  aop(iotg,3055,3) 
                dzbir =  aop(iotg,3050,3)-aop(iotg,3046,3) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3055 kol. 3 = AOP-u (3050 - 3046) kol. 3, ako je AOP 3046 kol. 3 < AOP-a 3050 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30070
        if( aop(iotg,3046,4) < aop(iotg,3050,4) ):
            if not( aop(iotg,3055,4) == aop(iotg,3050,4)-aop(iotg,3046,4) ):
                lzbir =  aop(iotg,3055,4) 
                dzbir =  aop(iotg,3050,4)-aop(iotg,3046,4) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3055 kol. 4 = AOP-u (3050 - 3046) kol. 4, ako je AOP 3046 kol. 4 < AOP-a 3050 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30071
        if( aop(iotg,3046,3) == aop(iotg,3050,3) ):
            if not( suma(iotg,3054,3055,3) == 0 ):
                lzbir =  suma(iotg,3054,3055,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (3054 + 3055) kol. 3 = 0, ako je AOP 3046 kol. 3 = AOP-u 3050 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30072
        if( aop(iotg,3046,4) == aop(iotg,3050,4) ):
            if not( suma(iotg,3054,3055,4) == 0 ):
                lzbir =  suma(iotg,3054,3055,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (3054 + 3055) kol. 4 = 0, ako je AOP 3046 kol. 4 = AOP-u 3050 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30073
        if( aop(iotg,3054,3) > 0 ):
            if not( aop(iotg,3055,3) == 0 ):
                lzbir =  aop(iotg,3055,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3054 kol. 3 > 0 onda je AOP 3055 kol. 3 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30074
        if( aop(iotg,3055,3) > 0 ):
            if not( aop(iotg,3054,3) == 0 ):
                lzbir =  aop(iotg,3054,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3055 kol. 3 > 0 onda je AOP 3054 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30075
        if( aop(iotg,3054,4) > 0 ):
            if not( aop(iotg,3055,4) == 0 ):
                lzbir =  aop(iotg,3055,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3054 kol. 4 > 0 onda je AOP 3055 kol. 4 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30076
        if( aop(iotg,3055,4) > 0 ):
            if not( aop(iotg,3054,4) == 0 ):
                lzbir =  aop(iotg,3054,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3055 kol. 4 > 0 onda je AOP 3054 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30077
        if not( suma_liste(iotg,[3046,3055],3) == suma_liste(iotg,[3050,3054],3) ):
            lzbir =  suma_liste(iotg,[3046,3055],3) 
            dzbir =  suma_liste(iotg,[3050,3054],3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (3046 + 3055) kol. 3 = AOP-u (3050 + 3054) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30078
        if not( suma_liste(iotg,[3046,3055],4) == suma_liste(iotg,[3050,3054],4) ):
            lzbir =  suma_liste(iotg,[3046,3055],4) 
            dzbir =  suma_liste(iotg,[3050,3054],4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (3046 + 3055) kol. 4 = AOP-u (3050 + 3054) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30079
        if not( aop(iotg,3056,3) == suma_liste(iotg,[3001,3012,3032,3046],3) ):
            lzbir =  aop(iotg,3056,3) 
            dzbir =  suma_liste(iotg,[3001,3012,3032,3046],3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3056 kol. 3 = AOP-u (3001 + 3012 + 3032 + 3046) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30080
        if not( aop(iotg,3056,4) == suma_liste(iotg,[3001,3012,3032,3046],4) ):
            lzbir =  aop(iotg,3056,4) 
            dzbir =  suma_liste(iotg,[3001,3012,3032,3046],4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3056 kol. 4 = AOP-u (3001 + 3012 + 3032 + 3046) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30081
        if not( aop(iotg,3057,3) == suma_liste(iotg,[3006,3019,3028,3029,3038,3050],3) ):
            lzbir =  aop(iotg,3057,3) 
            dzbir =  suma_liste(iotg,[3006,3019,3028,3029,3038,3050],3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3057 kol. 3 = AOP-u (3006 + 3019 + 3028 + 3029 + 3038 + 3050) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30082
        if not( aop(iotg,3057,4) == suma_liste(iotg,[3006,3019,3028,3029,3038,3050],4) ):
            lzbir =  aop(iotg,3057,4) 
            dzbir =  suma_liste(iotg,[3006,3019,3028,3029,3038,3050],4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3057 kol. 4 = AOP-u (3006 + 3019 + 3028 + 3029 + 3038 + 3050) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30083
        if( aop(iotg,3056,3) > aop(iotg,3057,3) ):
            if not( aop(iotg,3058,3) == aop(iotg,3056,3)-aop(iotg,3057,3) ):
                lzbir =  aop(iotg,3058,3) 
                dzbir =  aop(iotg,3056,3)-aop(iotg,3057,3) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3058 kol. 3 = AOP-u (3056 - 3057) kol. 3, ako je AOP 3056 kol. 3 > AOP-a 3057 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30084
        if( aop(iotg,3056,4) > aop(iotg,3057,4) ):
            if not( aop(iotg,3058,4) == aop(iotg,3056,4)-aop(iotg,3057,4) ):
                lzbir =  aop(iotg,3058,4) 
                dzbir =  aop(iotg,3056,4)-aop(iotg,3057,4) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3058 kol. 4 = AOP-u (3056 - 3057) kol. 4, ako je AOP 3056 kol. 4 > AOP-a 3057 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30085
        if( aop(iotg,3056,3) < aop(iotg,3057,3) ):
            if not( aop(iotg,3059,3) == aop(iotg,3057,3)-aop(iotg,3056,3) ):
                lzbir =  aop(iotg,3059,3) 
                dzbir =  aop(iotg,3057,3)-aop(iotg,3056,3) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3059 kol. 3 = AOP-u (3057 - 3056) kol. 3, ako je AOP 3056 kol. 3 < AOP-a 3057 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30086
        if( aop(iotg,3056,4) < aop(iotg,3057,4) ):
            if not( aop(iotg,3059,4) == aop(iotg,3057,4)-aop(iotg,3056,4) ):
                lzbir =  aop(iotg,3059,4) 
                dzbir =  aop(iotg,3057,4)-aop(iotg,3056,4) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3059 kol. 4 = AOP-u (3057 - 3056) kol. 4, ako je AOP 3056 kol. 4 < AOP-a 3057 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30087
        if( aop(iotg,3056,3) == aop(iotg,3057,3) ):
            if not( suma(iotg,3058,3059,3) == 0 ):
                lzbir =  suma(iotg,3058,3059,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (3058 + 3059) kol. 3 = 0, ako je AOP 3056 kol. 3 = AOP-u 3057 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30088
        if( aop(iotg,3056,4) == aop(iotg,3057,4) ):
            if not( suma(iotg,3058,3059,4) == 0 ):
                lzbir =  suma(iotg,3058,3059,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (3058 + 3059) kol. 4 = 0, ako je AOP 3056 kol. 4 = AOP-u 3057 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30089
        if( aop(iotg,3058,3) > 0 ):
            if not( aop(iotg,3059,3) == 0 ):
                lzbir =  aop(iotg,3059,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3058 kol. 3 > 0 onda je AOP 3059 kol. 3 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto povećanja i smanjenja gotovine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30090
        if( aop(iotg,3059,3) > 0 ):
            if not( aop(iotg,3058,3) == 0 ):
                lzbir =  aop(iotg,3058,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3059 kol. 3 > 0 onda je AOP 3058 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto povećanja i smanjenja gotovine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30091
        if( aop(iotg,3058,4) > 0 ):
            if not( aop(iotg,3059,4) == 0 ):
                lzbir =  aop(iotg,3059,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3058 kol. 4 > 0 onda je AOP 3059 kol. 4 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto povećanja i smanjenja gotovine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30092
        if( aop(iotg,3059,4) > 0 ):
            if not( aop(iotg,3058,4) == 0 ):
                lzbir =  aop(iotg,3058,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3059 kol. 4 > 0 onda je AOP 3058 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto povećanja i smanjenja gotovine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30093
        if not( suma_liste(iotg,[3056,3059],3) == suma(iotg,3057,3058,3) ):
            lzbir =  suma_liste(iotg,[3056,3059],3) 
            dzbir =  suma(iotg,3057,3058,3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (3056 + 3059) kol. 3 = AOP-u (3057 + 3058) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30094
        if not( suma_liste(iotg,[3056,3059],4) == suma(iotg,3057,3058,4) ):
            lzbir =  suma_liste(iotg,[3056,3059],4) 
            dzbir =  suma(iotg,3057,3058,4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (3056 + 3059) kol. 4 = AOP-u (3057 + 3058) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30095
        if( suma_liste(iotg,[3058,3060,3061],3) > suma_liste(iotg,[3059,3062],3) ):
            if not( aop(iotg,3063,3) == suma_liste(iotg,[3058,3060,3061],3)-suma_liste(iotg,[3059,3062],3) ):
                lzbir =  aop(iotg,3063,3) 
                dzbir =  suma_liste(iotg,[3058,3060,3061],3)-suma_liste(iotg,[3059,3062],3) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3063 kol. 3 = AOP-u (3058 - 3059 + 3060 + 3061 - 3062) kol. 3, ako je AOP (3058 + 3060 + 3061) kol. 3 > AOP-a (3059 + 3062) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30096
        if( suma_liste(iotg,[3058,3060,3061],4) > suma_liste(iotg,[3059,3062],4) ):
            if not( aop(iotg,3063,4) == suma_liste(iotg,[3058,3060,3061],4)-suma_liste(iotg,[3059,3062],4) ):
                lzbir =  aop(iotg,3063,4) 
                dzbir =  suma_liste(iotg,[3058,3060,3061],4)-suma_liste(iotg,[3059,3062],4) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3063 kol. 4 = AOP-u (3058 - 3059 + 3060 + 3061 - 3062) kol. 4, ako je AOP (3058 + 3060 + 3061) kol. 4 > AOP-a (3059 + 3062) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30097
        if( suma_liste(iotg,[3058,3060,3061],3) <= suma_liste(iotg,[3059,3062],3) ):
            if not( aop(iotg,3063,3) == 0 ):
                lzbir =  aop(iotg,3063,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3063 kol. 3 = 0, ako je AOP (3058 + 3060 + 3061) kol. 3 ≤ AOP-a (3059 + 3062) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30098
        if( suma_liste(iotg,[3058,3060,3061],4) <= suma_liste(iotg,[3059,3062],4) ):
            if not( aop(iotg,3063,4) == 0 ):
                lzbir =  aop(iotg,3063,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3063 kol. 4 = 0, ako je AOP (3058 + 3060 + 3061) kol. 4 ≤ AOP-a (3059 + 3062) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30099
        if not( aop(iotg,3063,4) == aop(iotg,3060,3) ):
            lzbir =  aop(iotg,3063,4) 
            dzbir =  aop(iotg,3060,3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3063 kol. 4 = AOP-u 3060 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #IZVEŠTAJ O PROMENAMA NA KAPITALU - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #40001
        if not( suma(iopk,4001, 4138, 1)  > 0 ):
            form_errors.append('Zbir podataka na oznakama za AOP (4001 do 4138) > 0 Izveštaj o promenama na kapitalu mora imati iskazane podatke; ')
        
        #40002
        if not( aop(iopk,4004,1) == suma(iopk,4001,4002,1)-aop(iopk,4003,1) ):
            lzbir =  aop(iopk,4004,1) 
            dzbir =  suma(iopk,4001,4002,1)-aop(iopk,4003,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4004 = AOP-u (4001 + 4002 - 4003)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40003
        if not( aop(iopk,4026,1) == suma(iopk,4023,4024,1)-aop(iopk,4025,1) ):
            lzbir =  aop(iopk,4026,1) 
            dzbir =  suma(iopk,4023,4024,1)-aop(iopk,4025,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4026 = AOP-u (4023 + 4024 - 4025)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40004
        if not( aop(iopk,4048,1) == suma(iopk,4045,4046,1)-aop(iopk,4047,1) ):
            lzbir =  aop(iopk,4048,1) 
            dzbir =  suma(iopk,4045,4046,1)-aop(iopk,4047,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4048 = AOP-u (4045 + 4046 - 4047)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40005
        if not( aop(iopk,4062,1) == suma(iopk,4059,4060,1)-aop(iopk,4061,1) ):
            lzbir =  aop(iopk,4062,1) 
            dzbir =  suma(iopk,4059,4060,1)-aop(iopk,4061,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4062= AOP-u (4059 + 4060 - 4061)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40006
        if not( aop(iopk,4076,1) == suma(iopk,4073,4074,1)-aop(iopk,4075,1) ):
            lzbir =  aop(iopk,4076,1) 
            dzbir =  suma(iopk,4073,4074,1)-aop(iopk,4075,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4076 = AOP-u (4073 + 4074 - 4075)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40007
        if not( aop(iopk,4104,1) == suma(iopk,4101,4102,1)-aop(iopk,4103,1) ):
            lzbir =  aop(iopk,4104,1) 
            dzbir =  suma(iopk,4101,4102,1)-aop(iopk,4103,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4104 = AOP-u (4101 + 4102 - 4103)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40008
        if( suma_liste(iopk,[4001,4023,4045,4073],1) > aop(iopk,4059,1) + aop(iopk,4101,1) ):
            if not( aop(iopk,4127,1) == suma_liste(iopk,[4001,4023,4045,4073],1)-suma_liste(iopk,[4059,4101],1) ):
                lzbir =  aop(iopk,4127,1) 
                dzbir =  suma_liste(iopk,[4001,4023,4045,4073],1)-suma_liste(iopk,[4059,4101],1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4127 = AOP-u (4001 + 4023 + 4045 - 4059 + 4073 - 4101), ako je AOP (4001 + 4023 + 4045 + 4073) > AOP-a (4059 + 4101)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40009
        if( suma_liste(iopk,[4001,4023,4045,4073],1) < aop(iopk,4059,1) + aop(iopk,4101,1) ):
            if not( aop(iopk,4133,1) == suma_liste(iopk,[4059,4101],1)-suma_liste(iopk,[4001,4023,4045,4073],1) ):
                lzbir =  aop(iopk,4133,1) 
                dzbir =  suma_liste(iopk,[4059,4101],1)-suma_liste(iopk,[4001,4023,4045,4073],1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4133 = AOP-u (4059 - 4001 - 4023 - 4045 - 4073 + 4101), ako je AOP (4001 + 4023 + 4045 + 4073) < AOP-a (4059 + 4101)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40010
        if( suma_liste(iopk,[4001,4023,4045,4073],1) == aop(iopk,4059,1) + aop(iopk,4101,1) ):
            if not( aop(iopk,4127,1) + aop(iopk,4133,1) == 0 ):
                lzbir =  aop(iopk,4127,1) + aop(iopk,4133,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4127 + 4133) = 0, ako je AOP (4001 + 4023 + 4045 + 4073) = AOP-u (4059 + 4101) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40011
        if( aop(iopk,4127,1) > 0 ):
            if not( aop(iopk,4133,1) == 0 ):
                lzbir =  aop(iopk,4133,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4127 > 0, onda je AOP 4133 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40012
        if( aop(iopk,4133,1) > 0 ):
            if not( aop(iopk,4127,1) == 0 ):
                lzbir =  aop(iopk,4127,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4133 > 0, onda je AOP 4127 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40013
        if( suma_liste(iopk,[4004,4026,4048,4076],1) > aop(iopk,4062,1) + aop(iopk,4104,1) ):
            if not( aop(iopk,4128,1) == suma_liste(iopk,[4004,4026,4048,4076],1)-suma_liste(iopk,[4062,4104],1) ):
                lzbir =  aop(iopk,4128,1) 
                dzbir =  suma_liste(iopk,[4004,4026,4048,4076],1)-suma_liste(iopk,[4062,4104],1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4128 = AOP-u (4004 + 4026 + 4048 - 4062 + 4076 - 4104), ako je AOP (4004 + 4026 + 4048 + 4076) > AOP-a (4062 + 4104)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40014
        if( suma_liste(iopk,[4004,4026,4048,4076],1) < aop(iopk,4062,1) + aop(iopk,4104,1) ):
            if not( aop(iopk,4134,1) == suma_liste(iopk,[4062,4104],1)-suma_liste(iopk,[4004,4026,4048,4076],1) ):
                lzbir =  aop(iopk,4134,1) 
                dzbir =  suma_liste(iopk,[4062,4104],1)-suma_liste(iopk,[4004,4026,4048,4076],1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4134 = AOP-u (4062 - 4004 - 4026 - 4048 - 4076 + 4104), ako je AOP (4004 + 4026 + 4048 + 4076) < AOP-a (4062 + 4104)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40015
        if( suma_liste(iopk,[4004,4026,4048,4076],1) == aop(iopk,4062,1) + aop(iopk,4104,1) ):
            if not( aop(iopk,4128,1) + aop(iopk,4134,1) == 0 ):
                lzbir =  aop(iopk,4128,1) + aop(iopk,4134,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4128 + 4134) = 0, ako je AOP (4004 + 4026 + 4048 + 4076) = AOP-u (4062 + 4104) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40016
        if( aop(iopk,4128,1) > 0 ):
            if not( aop(iopk,4134,1) == 0 ):
                lzbir =  aop(iopk,4134,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4128 > 0, onda je AOP 4134 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40017
        if( aop(iopk,4134,1) > 0 ):
            if not( aop(iopk,4128,1) == 0 ):
                lzbir =  aop(iopk,4128,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4134 > 0, onda je AOP 4128 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40018
        if( aop(iopk,4077,1) > 0 ):
            if not( aop(iopk,4105,1) == 0 ):
                lzbir =  aop(iopk,4105,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4077 > 0, onda je AOP 4105 = 0 Ne mogu biti istovremeno prikazani dobitak i gubitak poslovne godine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40019
        if( aop(iopk,4105,1) > 0 ):
            if not( aop(iopk,4077,1) == 0 ):
                lzbir =  aop(iopk,4077,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4105 > 0, onda je AOP 4077 = 0 Ne mogu biti istovremeno prikazani dobitak i gubitak poslovne godine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40020
        if( aop(iopk,4005,1) + aop(iopk,4007,1) > aop(iopk,4006,1) + aop(iopk,4008,1) ):
            if not( aop(iopk,4009,1) == suma_liste(iopk,[4005,4007],1)-suma_liste(iopk,[4006,4008],1) ):
                lzbir =  aop(iopk,4009,1) 
                dzbir =  suma_liste(iopk,[4005,4007],1)-suma_liste(iopk,[4006,4008],1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4009 = AOP-u (4005 - 4006 + 4007 - 4008), ako je AOP (4005 + 4007) > AOP-a (4006 + 4008)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40021
        if( aop(iopk,4005,1) + aop(iopk,4007,1) < aop(iopk,4006,1) + aop(iopk,4008,1) ):
            if not( aop(iopk,4010,1) == suma_liste(iopk,[4006,4008],1)-suma_liste(iopk,[4005,4007],1) ):
                lzbir =  aop(iopk,4010,1) 
                dzbir =  suma_liste(iopk,[4006,4008],1)-suma_liste(iopk,[4005,4007],1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4010 = AOP-u (4006 - 4005 - 4007 + 4008), ako je AOP (4005 + 4007) < AOP-a (4006 + 4008)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40022
        if( aop(iopk,4005,1) + aop(iopk,4007,1) == aop(iopk,4006,1) + aop(iopk,4008,1) ):
            if not( aop(iopk,4009,1) + aop(iopk,4010,1) == 0 ):
                lzbir =  aop(iopk,4009,1) + aop(iopk,4010,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4009 + 4010) = 0, ako je AOP (4005 + 4007) = AOP-u (4006 + 4008) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40023
        if( aop(iopk,4009,1) > 0 ):
            if not( aop(iopk,4010,1) == 0 ):
                lzbir =  aop(iopk,4010,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4009 > 0, onda je AOP 4010 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije raspodele '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40024
        if( aop(iopk,4010,1) > 0 ):
            if not( aop(iopk,4009,1) == 0 ):
                lzbir =  aop(iopk,4009,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4010 > 0, onda je AOP 4009 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije raspodele '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40025
        if( aop(iopk,4027,1) + aop(iopk,4029,1) > aop(iopk,4028,1) + aop(iopk,4030,1) ):
            if not( aop(iopk,4031,1) == suma_liste(iopk,[4027,4029],1)-suma_liste(iopk,[4028,4030],1) ):
                lzbir =  aop(iopk,4031,1) 
                dzbir =  suma_liste(iopk,[4027,4029],1)-suma_liste(iopk,[4028,4030],1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4031 = AOP-u (4027 - 4028 + 4029 - 4030), ako je AOP (4027 + 4029) > AOP-a (4028 + 4030)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40026
        if( aop(iopk,4027,1) + aop(iopk,4029,1) < aop(iopk,4028,1) + aop(iopk,4030,1) ):
            if not( aop(iopk,4032,1) == suma_liste(iopk,[4028,4030],1)-suma_liste(iopk,[4027,4029],1) ):
                lzbir =  aop(iopk,4032,1) 
                dzbir =  suma_liste(iopk,[4028,4030],1)-suma_liste(iopk,[4027,4029],1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4032 = AOP-u (4028 - 4027 - 4029 + 4030), ako je AOP (4027 + 4029) < AOP-a (4028 + 4030)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40027
        if( aop(iopk,4027,1) + aop(iopk,4029,1) == aop(iopk,4028,1) + aop(iopk,4030,1) ):
            if not( aop(iopk,4031,1) + aop(iopk,4032,1) == 0 ):
                lzbir =  aop(iopk,4031,1) + aop(iopk,4032,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4031 + 4032) = 0, ako je AOP (4027 + 4029) = AOP-u (4028 + 4030) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40028
        if( aop(iopk,4031,1) > 0 ):
            if not( aop(iopk,4032,1) == 0 ):
                lzbir =  aop(iopk,4032,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4031 > 0, onda je AOP 4032 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije raspodele '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40029
        if( aop(iopk,4032,1) > 0 ):
            if not( aop(iopk,4031,1) == 0 ):
                lzbir =  aop(iopk,4031,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4032 > 0, onda je AOP 4031 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije raspodele '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40030
        if( aop(iopk,4082,1) > suma_liste(iopk,[4080,4081,4083],1) ):
            if not( aop(iopk,4084,1) == aop(iopk,4082,1)-suma_liste(iopk,[4080,4081,4083],1) ):
                lzbir =  aop(iopk,4084,1) 
                dzbir =  aop(iopk,4082,1)-suma_liste(iopk,[4080,4081,4083],1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4084 = AOP-u (4082 - 4080 - 4081 - 4083), ako je AOP 4082 > AOP-a (4080 + 4081 + 4083)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40031
        if( aop(iopk,4082,1) < suma_liste(iopk,[4080,4081,4083],1) ):
            if not( aop(iopk,4085,1) == suma_liste(iopk,[4080,4081,4083],1)-aop(iopk,4082,1) ):
                lzbir =  aop(iopk,4085,1) 
                dzbir =  suma_liste(iopk,[4080,4081,4083],1)-aop(iopk,4082,1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4085 = AOP-u (4080 - 4082 + 4081 + 4083), ako je AOP 4082 < AOP-a (4080 + 4081 + 4083)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40032
        if( aop(iopk,4082,1) == suma_liste(iopk,[4080,4081,4083],1) ):
            if not( aop(iopk,4084,1) + aop(iopk,4085,1) == 0 ):
                lzbir =  aop(iopk,4084,1) + aop(iopk,4085,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4084 + 4085) = 0, ako je AOP 4082 = AOP-u (4080 + 4081 + 4083) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40033
        if( aop(iopk,4084,1) > 0 ):
            if not( aop(iopk,4085,1) == 0 ):
                lzbir =  aop(iopk,4085,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4084 > 0, onda je AOP 4085 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije raspodele '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40034
        if( aop(iopk,4085,1) > 0 ):
            if not( aop(iopk,4084,1) == 0 ):
                lzbir =  aop(iopk,4084,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4085 > 0, onda je AOP 4084 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije raspodele '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40035
        if( aop(iopk,4109,1) > aop(iopk,4108,1) + aop(iopk,4110,1) ):
            if not( aop(iopk,4111,1) == aop(iopk,4109,1)-suma_liste(iopk,[4108,4110],1) ):
                lzbir =  aop(iopk,4111,1) 
                dzbir =  aop(iopk,4109,1)-suma_liste(iopk,[4108,4110],1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4111 = AOP-u (4109 - 4108 - 4110), ako je AOP 4109 > AOP-a (4108 + 4110)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40036
        if( aop(iopk,4109,1) < aop(iopk,4108,1) + aop(iopk,4110,1) ):
            if not( aop(iopk,4112,1) == suma_liste(iopk,[4108,4110],1)-aop(iopk,4109,1) ):
                lzbir =  aop(iopk,4112,1) 
                dzbir =  suma_liste(iopk,[4108,4110],1)-aop(iopk,4109,1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4112 = AOP-u (4108 - 4109 + 4110), ako je AOP 4109 < AOP-a (4108 + 4110)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40037
        if( aop(iopk,4109,1) == aop(iopk,4108,1) + aop(iopk,4110,1) ):
            if not( aop(iopk,4111,1) + aop(iopk,4112,1) == 0 ):
                lzbir =  aop(iopk,4111,1) + aop(iopk,4112,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4111 + 4112) = 0, ako je AOP 4109 = AOP-u (4108 + 4110) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40038
        if( aop(iopk,4111,1) > 0 ):
            if not( aop(iopk,4112,1) == 0 ):
                lzbir =  aop(iopk,4112,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4111 > 0, onda je AOP 4112 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije raspodele '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40039
        if( aop(iopk,4112,1) > 0 ):
            if not( aop(iopk,4111,1) == 0 ):
                lzbir =  aop(iopk,4111,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4112 > 0, onda je AOP 4111= 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije raspodele '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40040
        if not( aop(iopk,4011,1) == suma_liste(iopk,[4004,4009],1)-aop(iopk,4010,1) ):
            lzbir =  aop(iopk,4011,1) 
            dzbir =  suma_liste(iopk,[4004,4009],1)-aop(iopk,4010,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4011 = AOP-u (4004 + 4009 - 4010)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40041
        if not( aop(iopk,4033,1) == suma_liste(iopk,[4026,4031],1)-aop(iopk,4032,1) ):
            lzbir =  aop(iopk,4033,1) 
            dzbir =  suma_liste(iopk,[4026,4031],1)-aop(iopk,4032,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4033 = AOP-u (4026 + 4031 - 4032)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40042
        if not( aop(iopk,4051,1) == suma(iopk,4048,4049,1)-aop(iopk,4050,1) ):
            lzbir =  aop(iopk,4051,1) 
            dzbir =  suma(iopk,4048,4049,1)-aop(iopk,4050,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4051 = AOP-u (4048 + 4049 - 4050)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40043
        if not( aop(iopk,4065,1) == suma_liste(iopk,[4062,4064],1)-aop(iopk,4063,1) ):
            lzbir =  aop(iopk,4065,1) 
            dzbir =  suma_liste(iopk,[4062,4064],1)-aop(iopk,4063,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4065 = AOP-u (4062 - 4063 + 4064)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40044
        if not( aop(iopk,4086,1) == suma_liste(iopk,[4076,4077,4078,4084],1)-suma_liste(iopk,[4079,4085],1) ):
            lzbir =  aop(iopk,4086,1) 
            dzbir =  suma_liste(iopk,[4076,4077,4078,4084],1)-suma_liste(iopk,[4079,4085],1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4086 = AOP-u (4076 + 4077 + 4078 - 4079 + 4084 - 4085)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40045
        if not( aop(iopk,4113,1) == suma_liste(iopk,[4104,4105,4106,4111],1)-suma_liste(iopk,[4107,4112],1) ):
            lzbir =  aop(iopk,4113,1) 
            dzbir =  suma_liste(iopk,[4104,4105,4106,4111],1)-suma_liste(iopk,[4107,4112],1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4113 = AOP-u (4104 + 4105 + 4106 - 4107 + 4111 - 4112)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40046
        if( suma_liste(iopk,[4011,4033,4051,4086],1) > aop(iopk,4065,1) + aop(iopk,4113,1) ):
            if not( aop(iopk,4129,1) == suma_liste(iopk,[4011,4033,4051,4086],1)-suma_liste(iopk,[4065,4113],1) ):
                lzbir =  aop(iopk,4129,1) 
                dzbir =  suma_liste(iopk,[4011,4033,4051,4086],1)-suma_liste(iopk,[4065,4113],1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4129 = AOP-u (4011 + 4033 + 4051 - 4065 + 4086 - 4113), ako je AOP (4011 + 4033 + 4051 + 4086) > AOP-a (4065 + 4113)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40047
        if( suma_liste(iopk,[4011,4033,4051,4086],1) < aop(iopk,4065,1) + aop(iopk,4113,1) ):
            if not( aop(iopk,4135,1) == suma_liste(iopk,[4065,4113],1)-suma_liste(iopk,[4011,4033,4051,4086],1) ):
                lzbir =  aop(iopk,4135,1) 
                dzbir =  suma_liste(iopk,[4065,4113],1)-suma_liste(iopk,[4011,4033,4051,4086],1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4135 = AOP-u (4065 - 4011 - 4033 - 4051 - 4086 + 4113), ako je AOP (4011 + 4033 + 4051 + 4086) < AOP-a (4065 + 4113)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40048
        if( suma_liste(iopk,[4011,4033,4051,4086],1) == aop(iopk,4065,1) + aop(iopk,4113,1) ):
            if not( aop(iopk,4129,1) + aop(iopk,4135,1) == 0 ):
                lzbir =  aop(iopk,4129,1) + aop(iopk,4135,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4129 + 4135) = 0, ako je AOP (4011 + 4033 + 4051 + 4086) = AOP-u (4065 + 4113) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40049
        if( aop(iopk,4129,1) > 0 ):
            if not( aop(iopk,4135,1) == 0 ):
                lzbir =  aop(iopk,4135,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4129 > 0, onda je AOP 4135 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40050
        if( aop(iopk,4135,1) > 0 ):
            if not( aop(iopk,4129,1) == 0 ):
                lzbir =  aop(iopk,4129,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4135 > 0, onda je AOP 4129 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40051
        if not( aop(iopk,4012,1) == aop(iopk,4011,1) ):
            lzbir =  aop(iopk,4012,1) 
            dzbir =  aop(iopk,4011,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4012 = AOP-u 4011  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40052
        if not( aop(iopk,4034,1) == aop(iopk,4033,1) ):
            lzbir =  aop(iopk,4034,1) 
            dzbir =  aop(iopk,4033,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4034 = AOP-u 4033  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40053
        if not( aop(iopk,4052,1) == aop(iopk,4051,1) ):
            lzbir =  aop(iopk,4052,1) 
            dzbir =  aop(iopk,4051,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4052 = AOP-u 4051  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40054
        if not( aop(iopk,4066,1) == aop(iopk,4065,1) ):
            lzbir =  aop(iopk,4066,1) 
            dzbir =  aop(iopk,4065,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4066 = AOP-u 4065  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40055
        if not( aop(iopk,4087,1) == aop(iopk,4086,1) ):
            lzbir =  aop(iopk,4087,1) 
            dzbir =  aop(iopk,4086,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4087 = AOP-u 4086  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40056
        if not( aop(iopk,4114,1) == aop(iopk,4113,1) ):
            lzbir =  aop(iopk,4114,1) 
            dzbir =  aop(iopk,4113,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4114 = AOP-u 4113  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40057
        if not( aop(iopk,4130,1) == aop(iopk,4129,1) ):
            lzbir =  aop(iopk,4130,1) 
            dzbir =  aop(iopk,4129,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4130 = AOP-u 4129  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40058
        if not( aop(iopk,4136,1) == aop(iopk,4135,1) ):
            lzbir =  aop(iopk,4136,1) 
            dzbir =  aop(iopk,4135,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4136 = AOP-u 4135  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40059
        if not( aop(iopk,4015,1) == suma(iopk,4012,4013,1)-aop(iopk,4014,1) ):
            lzbir =  aop(iopk,4015,1) 
            dzbir =  suma(iopk,4012,4013,1)-aop(iopk,4014,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4015 = AOP-u (4012 + 4013 - 4014)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40060
        if not( aop(iopk,4037,1) == suma(iopk,4034,4035,1)-aop(iopk,4036,1) ):
            lzbir =  aop(iopk,4037,1) 
            dzbir =  suma(iopk,4034,4035,1)-aop(iopk,4036,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4037 = AOP-u (4034 + 4035 - 4036)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40061
        if not( aop(iopk,4055,1) == suma(iopk,4052,4053,1)-aop(iopk,4054,1) ):
            lzbir =  aop(iopk,4055,1) 
            dzbir =  suma(iopk,4052,4053,1)-aop(iopk,4054,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4055 = AOP-u (4052 + 4053 - 4054)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40062
        if not( aop(iopk,4069,1) == suma(iopk,4066,4067,1)-aop(iopk,4068,1) ):
            lzbir =  aop(iopk,4069,1) 
            dzbir =  suma(iopk,4066,4067,1)-aop(iopk,4068,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4069= AOP-u (4066 + 4067 - 4068)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40063
        if not( aop(iopk,4090,1) == suma(iopk,4087,4088,1)-aop(iopk,4089,1) ):
            lzbir =  aop(iopk,4090,1) 
            dzbir =  suma(iopk,4087,4088,1)-aop(iopk,4089,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4090 = AOP-u (4087 + 4088 - 4089)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40064
        if not( aop(iopk,4117,1) == suma(iopk,4114,4115,1)-aop(iopk,4116,1) ):
            lzbir =  aop(iopk,4117,1) 
            dzbir =  suma(iopk,4114,4115,1)-aop(iopk,4116,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4117 = AOP-u (4114 + 4115 - 4116)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40065
        if( suma_liste(iopk,[4015,4037,4055,4090],1) > aop(iopk,4069,1) + aop(iopk,4117,1) ):
            if not( aop(iopk,4131,1) == suma_liste(iopk,[4015,4037,4055,4090],1)-suma_liste(iopk,[4069,4117],1) ):
                lzbir =  aop(iopk,4131,1) 
                dzbir =  suma_liste(iopk,[4015,4037,4055,4090],1)-suma_liste(iopk,[4069,4117],1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4131 = AOP-u (4015 + 4037 + 4055 - 4069 + 4090 - 4117), ako je AOP (4015 + 4037 + 4055 + 4090) > AOP-a (4069 + 4117)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40066
        if( suma_liste(iopk,[4015,4037,4055,4090],1) < aop(iopk,4069,1) + aop(iopk,4117,1) ):
            if not( aop(iopk,4137,1) == suma_liste(iopk,[4069,4117],1)-suma_liste(iopk,[4015,4037,4055,4090],1) ):
                lzbir =  aop(iopk,4137,1) 
                dzbir =  suma_liste(iopk,[4069,4117],1)-suma_liste(iopk,[4015,4037,4055,4090],1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4137= AOP-u (4069 - 4015 - 4037 - 4055 - 4090 + 4117), ako je AOP (4015 + 4037 + 4055 + 4090) < AOP-a (4069 + 4117)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40067
        if( suma_liste(iopk,[4015,4037,4055,4090],1) == aop(iopk,4069,1) + aop(iopk,4117,1) ):
            if not( aop(iopk,4131,1) + aop(iopk,4137,1) == 0 ):
                lzbir =  aop(iopk,4131,1) + aop(iopk,4137,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4131 + 4137) = 0, ako je AOP (4015 + 4037 + 4055 + 4090) = AOP-u (4069 + 4117) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40068
        if( aop(iopk,4131,1) > 0 ):
            if not( aop(iopk,4137,1) == 0 ):
                lzbir =  aop(iopk,4137,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4131 > 0, onda je AOP 4137 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40069
        if( aop(iopk,4137,1) > 0 ):
            if not( aop(iopk,4131,1) == 0 ):
                lzbir =  aop(iopk,4131,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4137 > 0, onda je AOP 4131 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40070
        if( aop(iopk,4091,1) > 0 ):
            if not( aop(iopk,4118,1) == 0 ):
                lzbir =  aop(iopk,4118,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4091 > 0, onda je AOP 4118 = 0 Ne mogu biti istovremeno prikazani dobitak i gubitak poslovne godine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40071
        if( aop(iopk,4118,1) > 0 ):
            if not( aop(iopk,4091,1) == 0 ):
                lzbir =  aop(iopk,4091,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 4118 > 0, onda je AOP 4091 = 0 Ne mogu biti istovremeno prikazani dobitak i gubitak poslovne godine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40072
        if( aop(iopk,4016,1) + aop(iopk,4018,1) > aop(iopk,4017,1) + aop(iopk,4019,1) ):
            if not( aop(iopk,4020,1) == suma_liste(iopk,[4016,4018],1)-suma_liste(iopk,[4017,4019],1) ):
                lzbir =  aop(iopk,4020,1) 
                dzbir =  suma_liste(iopk,[4016,4018],1)-suma_liste(iopk,[4017,4019],1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4020 = AOP-u (4016 - 4017 + 4018 - 4019), ako je AOP (4016 + 4018) > AOP-a (4017 + 4019)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40073
        if( aop(iopk,4016,1) + aop(iopk,4018,1) < aop(iopk,4017,1) + aop(iopk,4019,1) ):
            if not( aop(iopk,4021,1) == suma_liste(iopk,[4017,4019],1)-suma_liste(iopk,[4016,4018],1) ):
                lzbir =  aop(iopk,4021,1) 
                dzbir =  suma_liste(iopk,[4017,4019],1)-suma_liste(iopk,[4016,4018],1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4021 = AOP-u (4017 - 4016 - 4018 + 4019), ako je AOP (4016 + 4018) < AOP-a (4017 + 4019)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40074
        if( aop(iopk,4016,1) + aop(iopk,4018,1) == aop(iopk,4017,1) + aop(iopk,4019,1) ):
            if not( aop(iopk,4020,1) + aop(iopk,4021,1) == 0 ):
                lzbir =  aop(iopk,4020,1) + aop(iopk,4021,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4020 + 4021) = 0, ako je AOP (4016 + 4018) = AOP-u (4017 + 4019) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40075
        if( aop(iopk,4020,1) > 0 ):
            if not( aop(iopk,4021,1) == 0 ):
                lzbir =  aop(iopk,4021,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4020 > 0, onda je AOP 4021 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije raspodele '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40076
        if( aop(iopk,4021,1) > 0 ):
            if not( aop(iopk,4020,1) == 0 ):
                lzbir =  aop(iopk,4020,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4021 > 0, onda je AOP 4020 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije raspodele '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40077
        if( aop(iopk,4038,1) + aop(iopk,4040,1) > aop(iopk,4039,1) + aop(iopk,4041,1) ):
            if not( aop(iopk,4042,1) == suma_liste(iopk,[4038,4040],1)-suma_liste(iopk,[4039,4041],1) ):
                lzbir =  aop(iopk,4042,1) 
                dzbir =  suma_liste(iopk,[4038,4040],1)-suma_liste(iopk,[4039,4041],1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4042 = AOP-u (4038 - 4039 + 4040 - 4041), ako je AOP (4038 + 4040) > AOP-a (4039 + 4041)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40078
        if( aop(iopk,4038,1) + aop(iopk,4040,1) < aop(iopk,4039,1) + aop(iopk,4041,1) ):
            if not( aop(iopk,4043,1) == suma_liste(iopk,[4039,4041],1)-suma_liste(iopk,[4038,4040],1) ):
                lzbir =  aop(iopk,4043,1) 
                dzbir =  suma_liste(iopk,[4039,4041],1)-suma_liste(iopk,[4038,4040],1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4043 = AOP-u (4039 - 4038 - 4040 + 4041), ako je AOP (4038 + 4040) < AOP-a (4039 + 4041)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40079
        if( aop(iopk,4038,1) + aop(iopk,4040,1) == aop(iopk,4039,1) + aop(iopk,4041,1) ):
            if not( aop(iopk,4042,1) + aop(iopk,4043,1) == 0 ):
                lzbir =  aop(iopk,4042,1) + aop(iopk,4043,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4042 + 4043) = 0, ako je AOP (4038 + 4040) = AOP-u (4039 + 4041) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40080
        if( aop(iopk,4042,1) > 0 ):
            if not( aop(iopk,4043,1) == 0 ):
                lzbir =  aop(iopk,4043,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4042 > 0, onda je AOP 4043 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije raspodele '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40081
        if( aop(iopk,4043,1) > 0 ):
            if not( aop(iopk,4042,1) == 0 ):
                lzbir =  aop(iopk,4042,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4043 > 0, onda je AOP 4042 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije raspodele '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40082
        if( aop(iopk,4096,1) > suma_liste(iopk,[4094,4095,4097],1) ):
            if not( aop(iopk,4098,1) == aop(iopk,4096,1)-suma_liste(iopk,[4094,4095,4097],1) ):
                lzbir =  aop(iopk,4098,1) 
                dzbir =  aop(iopk,4096,1)-suma_liste(iopk,[4094,4095,4097],1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4098 = AOP-u (4096 - 4094 - 4095 - 4097), ako je AOP 4096 > AOP-a (4094 + 4095 + 4097)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40083
        if( aop(iopk,4096,1) < suma_liste(iopk,[4094,4095,4097],1) ):
            if not( aop(iopk,4099,1) == suma_liste(iopk,[4094,4095,4097],1)-aop(iopk,4096,1) ):
                lzbir =  aop(iopk,4099,1) 
                dzbir =  suma_liste(iopk,[4094,4095,4097],1)-aop(iopk,4096,1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4099 = AOP-u (4094 + 4095 - 4096 + 4097), ako je AOP 4096 < AOP-a (4094 + 4095 + 4097)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40084
        if( aop(iopk,4096,1) == suma_liste(iopk,[4094,4095,4097],1) ):
            if not( aop(iopk,4098,1) + aop(iopk,4099,1) == 0 ):
                lzbir =  aop(iopk,4098,1) + aop(iopk,4099,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4098 + 4099) = 0, ako je AOP 4096 = AOP-u (4094 + 4095 + 4097) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40085
        if( aop(iopk,4098,1) > 0 ):
            if not( aop(iopk,4099,1) == 0 ):
                lzbir =  aop(iopk,4099,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4098 > 0, onda je AOP 4099 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije raspodele '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40086
        if( aop(iopk,4099,1) > 0 ):
            if not( aop(iopk,4098,1) == 0 ):
                lzbir =  aop(iopk,4098,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4099 > 0, onda je AOP 4098 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije raspodele '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40087
        if( aop(iopk,4122,1) > aop(iopk,4121,1) + aop(iopk,4123,1) ):
            if not( aop(iopk,4124,1) == aop(iopk,4122,1)-suma_liste(iopk,[4121,4123],1) ):
                lzbir =  aop(iopk,4124,1) 
                dzbir =  aop(iopk,4122,1)-suma_liste(iopk,[4121,4123],1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4124 = AOP-u (4122 - 4121 - 4123), ako je AOP 4122 > AOP-a (4121 + 4123)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40088
        if( aop(iopk,4122,1) < aop(iopk,4121,1) + aop(iopk,4123,1) ):
            if not( aop(iopk,4125,1) == suma_liste(iopk,[4121,4123],1)-aop(iopk,4122,1) ):
                lzbir =  aop(iopk,4125,1) 
                dzbir =  suma_liste(iopk,[4121,4123],1)-aop(iopk,4122,1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4125 = AOP-u (4121 - 4122 + 4123), ako je AOP 4122 < AOP-a (4121 + 4123)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40089
        if( aop(iopk,4122,1) == aop(iopk,4121,1) + aop(iopk,4123,1) ):
            if not( aop(iopk,4124,1) + aop(iopk,4125,1) == 0 ):
                lzbir =  aop(iopk,4124,1) + aop(iopk,4125,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4124 + 4125) = 0, ako je AOP 4122 = AOP-u (4121 + 4123) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40090
        if( aop(iopk,4124,1) > 0 ):
            if not( aop(iopk,4125,1) == 0 ):
                lzbir =  aop(iopk,4125,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4124 > 0, onda je AOP 4125 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije raspodele '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40091
        if( aop(iopk,4125,1) > 0 ):
            if not( aop(iopk,4124,1) == 0 ):
                lzbir =  aop(iopk,4124,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4125 > 0, onda je AOP 4124 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije raspodele '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40092
        if not( aop(iopk,4022,1) == suma_liste(iopk,[4015,4020],1)-aop(iopk,4021,1) ):
            lzbir =  aop(iopk,4022,1) 
            dzbir =  suma_liste(iopk,[4015,4020],1)-aop(iopk,4021,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4022 = AOP-u (4015 + 4020 - 4021)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40093
        if not( aop(iopk,4044,1) == suma_liste(iopk,[4037,4042],1)-aop(iopk,4043,1) ):
            lzbir =  aop(iopk,4044,1) 
            dzbir =  suma_liste(iopk,[4037,4042],1)-aop(iopk,4043,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4044 = AOP-u (4037 + 4042 - 4043)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40094
        if not( aop(iopk,4058,1) == suma(iopk,4055,4056,1)-aop(iopk,4057,1) ):
            lzbir =  aop(iopk,4058,1) 
            dzbir =  suma(iopk,4055,4056,1)-aop(iopk,4057,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4058 = AOP-u (4055 + 4056 - 4057)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40095
        if not( aop(iopk,4072,1) == suma_liste(iopk,[4069,4071],1)-aop(iopk,4070,1) ):
            lzbir =  aop(iopk,4072,1) 
            dzbir =  suma_liste(iopk,[4069,4071],1)-aop(iopk,4070,1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4072 = AOP-u (4069 - 4070 + 4071)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40096
        if not( aop(iopk,4100,1) == suma_liste(iopk,[4090,4091,4092,4098],1)-suma_liste(iopk,[4093,4099],1) ):
            lzbir =  aop(iopk,4100,1) 
            dzbir =  suma_liste(iopk,[4090,4091,4092,4098],1)-suma_liste(iopk,[4093,4099],1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4100 = AOP-u (4090 + 4091 + 4092 - 4093 + 4098 - 4099)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40097
        if not( aop(iopk,4126,1) == suma_liste(iopk,[4117,4118,4119,4124],1)-suma_liste(iopk,[4120,4125],1) ):
            lzbir =  aop(iopk,4126,1) 
            dzbir =  suma_liste(iopk,[4117,4118,4119,4124],1)-suma_liste(iopk,[4120,4125],1) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4126 = AOP-u (4117 + 4118 + 4119 - 4120 + 4124 - 4125)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40098
        if( suma_liste(iopk,[4022,4044,4058,4100],1) > aop(iopk,4072,1) + aop(iopk,4126,1) ):
            if not( aop(iopk,4132,1) == suma_liste(iopk,[4022,4044,4058,4100],1)-suma_liste(iopk,[4072,4126],1) ):
                lzbir =  aop(iopk,4132,1) 
                dzbir =  suma_liste(iopk,[4022,4044,4058,4100],1)-suma_liste(iopk,[4072,4126],1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4132 = AOP-u (4022 + 4044 + 4058 - 4072 + 4100 - 4126), ako je AOP (4022 + 4044 + 4058 + 4100) > AOP-a (4072 + 4126)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40099
        if( suma_liste(iopk,[4022,4044,4058,4100],1) < aop(iopk,4072,1) + aop(iopk,4126,1) ):
            if not( aop(iopk,4138,1) == suma_liste(iopk,[4072,4126],1)-suma_liste(iopk,[4022,4044,4058,4100],1) ):
                lzbir =  aop(iopk,4138,1) 
                dzbir =  suma_liste(iopk,[4072,4126],1)-suma_liste(iopk,[4022,4044,4058,4100],1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4138 = AOP-u (4072 - 4022 - 4044 - 4058 - 4100 + 4126), ako je AOP (4022 + 4044 + 4058 + 4100) < AOP-a (4072 + 4126)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40100
        if( suma_liste(iopk,[4022,4044,4058,4100],1) == aop(iopk,4072,1) + aop(iopk,4126,1) ):
            if not( aop(iopk,4132,1) + aop(iopk,4138,1) == 0 ):
                lzbir =  aop(iopk,4132,1) + aop(iopk,4138,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4132 + 4138) = 0, ako je AOP (4022 + 4044 + 4058 + 4100) = AOP-u (4072 + 4126) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40101
        if( aop(iopk,4132,1) > 0 ):
            if not( aop(iopk,4138,1) == 0 ):
                lzbir =  aop(iopk,4138,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4132 > 0, onda je AOP 4138 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40102
        if( aop(iopk,4138,1) > 0 ):
            if not( aop(iopk,4132,1) == 0 ):
                lzbir =  aop(iopk,4132,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4138 > 0, onda je AOP 4132 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40103
        if not( aop(iopk,4004,1) == aop(bs,415,7) ):
            lzbir =  aop(iopk,4004,1) 
            dzbir =  aop(bs,415,7) 
            razlika = lzbir - dzbir
            form_warnings.append('AOP 4004 = AOP-u 0415 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo se primenjuje ukoliko Narodna banka Srbije vrši reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40104
        if( aop(iopk,4026,1) + aop(iopk,4048,1) >= aop(iopk,4062,1) ):
            if not( suma_liste(iopk,[4026,4048],1)-aop(iopk,4062,1) == aop(bs,416,7) ):
                lzbir =  suma_liste(iopk,[4026,4048],1)-aop(iopk,4062,1) 
                dzbir =  aop(bs,416,7) 
                razlika = lzbir - dzbir
                form_warnings.append('AOP (4026 + 4048 - 4062) = AOP-a 0416 kol. 7 bilansa stanja, ako je AOP (4026 + 4048) ≥ AOP-a 4062 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo se primenjuje ukoliko Narodna banka Srbije vrši reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40105
        if( aop(iopk,4026,1) + aop(iopk,4048,1) < aop(iopk,4062,1) ):
            if not( aop(iopk,4062,1)-suma_liste(iopk,[4026,4048],1) == aop(bs,417,7) ):
                lzbir =  aop(iopk,4062,1)-suma_liste(iopk,[4026,4048],1) 
                dzbir =  aop(bs,417,7) 
                razlika = lzbir - dzbir
                form_warnings.append('AOP (4062 - 4026 - 4048) = AOP-a 0417 kol. 7 bilansa stanja, ako je AOP (4026 + 4048) < AOP-a 4062 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo se primenjuje ukoliko Narodna banka Srbije vrši reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40106
        if not( aop(iopk,4076,1) == aop(bs,418,7) ):
            lzbir =  aop(iopk,4076,1) 
            dzbir =  aop(bs,418,7) 
            razlika = lzbir - dzbir
            form_warnings.append('AOP 4076 = AOP-u 0418 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo se primenjuje ukoliko Narodna banka Srbije vrši reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40107
        if not( aop(iopk,4104,1) == aop(bs,419,7) ):
            lzbir =  aop(iopk,4104,1) 
            dzbir =  aop(bs,419,7) 
            razlika = lzbir - dzbir
            form_warnings.append('AOP 4104 = AOP-u 0419 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo se primenjuje ukoliko Narodna banka Srbije vrši reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40108
        if not( aop(iopk,4128,1) == aop(bs,420,7) ):
            lzbir =  aop(iopk,4128,1) 
            dzbir =  aop(bs,420,7) 
            razlika = lzbir - dzbir
            form_warnings.append('AOP 4128 = AOP-u 0420 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo se primenjuje ukoliko Narodna banka Srbije vrši reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40109
        if not( aop(iopk,4134,1) == aop(bs,421,7) ):
            lzbir =  aop(iopk,4134,1) 
            dzbir =  aop(bs,421,7) 
            razlika = lzbir - dzbir
            form_warnings.append('AOP 4134 = AOP-u 0421 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo se primenjuje ukoliko Narodna banka Srbije vrši reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40110
        if not( aop(iopk,4011,1) == aop(bs,415,6) ):
            lzbir =  aop(iopk,4011,1) 
            dzbir =  aop(bs,415,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4011 = AOP-u 0415 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40111
        if( aop(iopk,4033,1) + aop(iopk,4051,1) >= aop(iopk,4065,1) ):
            if not( suma_liste(iopk,[4033,4051],1)-aop(iopk,4065,1) == aop(bs,416,6) ):
                lzbir =  suma_liste(iopk,[4033,4051],1)-aop(iopk,4065,1) 
                dzbir =  aop(bs,416,6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4033 + 4051 - 4065) = AOP-u 0416 kol. 6 bilansa stanja, ako je AOP (4033 + 4051)  ≥  AOP-a 4065 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40112
        if( aop(iopk,4033,1) + aop(iopk,4051,1) < aop(iopk,4065,1) ):
            if not( aop(iopk,4065,1)-suma_liste(iopk,[4033,4051],1) == aop(bs,417,6) ):
                lzbir =  aop(iopk,4065,1)-suma_liste(iopk,[4033,4051],1) 
                dzbir =  aop(bs,417,6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4065 - 4033 - 4051) = AOP-u 0417 kol. 6 bilansa stanja, ako je AOP (4033 + 4051) < AOP-a 4065 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40113
        if not( aop(iopk,4086,1) == aop(bs,418,6) ):
            lzbir =  aop(iopk,4086,1) 
            dzbir =  aop(bs,418,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4086 = AOP-u 0418 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40114
        if not( aop(iopk,4113,1) == aop(bs,419,6) ):
            lzbir =  aop(iopk,4113,1) 
            dzbir =  aop(bs,419,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4113 = AOP-u 0419 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40115
        if not( aop(iopk,4129,1) == aop(bs,420,6) ):
            lzbir =  aop(iopk,4129,1) 
            dzbir =  aop(bs,420,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4129 = AOP-u 0420 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40116
        if not( aop(iopk,4135,1) == aop(bs,421,6) ):
            lzbir =  aop(iopk,4135,1) 
            dzbir =  aop(bs,421,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4135 = AOP-u 0421 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40117
        if not( aop(iopk,4022,1) == aop(bs,415,5) ):
            lzbir =  aop(iopk,4022,1) 
            dzbir =  aop(bs,415,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4022 = AOP-u 0415 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40118
        if( aop(iopk,4044,1) + aop(iopk,4058,1) >= aop(iopk,4072,1) ):
            if not( suma_liste(iopk,[4044,4058],1)-aop(iopk,4072,1) == aop(bs,416,5) ):
                lzbir =  suma_liste(iopk,[4044,4058],1)-aop(iopk,4072,1) 
                dzbir =  aop(bs,416,5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4044 + 4058 - 4072) = AOP-u 0416 kol. 5 bilansa stanja, ako je AOP (4044 + 4058)  ≥  AOP-a 4072 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40119
        if( aop(iopk,4044,1) + aop(iopk,4058,1) < aop(iopk,4072,1) ):
            if not( aop(iopk,4072,1)-suma_liste(iopk,[4044,4058],1) == aop(bs,417,5) ):
                lzbir =  aop(iopk,4072,1)-suma_liste(iopk,[4044,4058],1) 
                dzbir =  aop(bs,417,5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4072 - 4044 - 4058) = AOP-u 0417 kol. 5 bilansa stanja, ako je AOP (4044 + 4058) < AOP-a 4072 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40120
        if not( aop(iopk,4100,1) == aop(bs,418,5) ):
            lzbir =  aop(iopk,4100,1) 
            dzbir =  aop(bs,418,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4100 = AOP-u 0418 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40121
        if not( aop(iopk,4126,1) == aop(bs,419,5) ):
            lzbir =  aop(iopk,4126,1) 
            dzbir =  aop(bs,419,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4126 = AOP-u 0419 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40122
        if not( aop(iopk,4132,1) == aop(bs,420,5) ):
            lzbir =  aop(iopk,4132,1) 
            dzbir =  aop(bs,420,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4132 = AOP-u 0420 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40123
        if not( aop(iopk,4138,1) == aop(bs,421,5) ):
            lzbir =  aop(iopk,4138,1) 
            dzbir =  aop(bs,421,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4138 = AOP-u 0421 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40124
        if not( aop(iopk,4077,1) == aop(bu,1041,6) ):
            lzbir =  aop(iopk,4077,1) 
            dzbir =  aop(bu,1041,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4077 = AOP-u 1041 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40125
        if not( aop(iopk,4105,1) == aop(bu,1042,6) ):
            lzbir =  aop(iopk,4105,1) 
            dzbir =  aop(bu,1042,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4105 = AOP-u 1042 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40126
        if not( aop(iopk,4091,1) == aop(bu,1041,5) ):
            lzbir =  aop(iopk,4091,1) 
            dzbir =  aop(bu,1041,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4091 = AOP-u 1041 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40127
        if not( aop(iopk,4118,1) == aop(bu,1042,5) ):
            lzbir =  aop(iopk,4118,1) 
            dzbir =  aop(bu,1042,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4118 = AOP-u 1042 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #STATISTIČKI IZVEŠTAJ - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        #90001
        if not( suma(si,9001,9034,4) > 0 ):
            form_errors.append('Zbir podataka na oznakama za AOP (9001 do 9034) kol. 4 > 0 Statistički izveštaj mora imati iskazane podatke za tekući izveštajni period; ')
        
        #90002
        if not( suma(si,9001,9034,5) > 0 ):
            form_errors.append('Zbir podataka na oznakama za AOP (9001 do 9034) kol. 5 > 0 Statistički izveštaj mora imati iskazane podatke za prethodni izveštajni period; ')
        
        #90003
        if not( aop(si,9009,4) <= aop(si,9008,4) ):
            form_errors.append('AOP 9009 kol. 4 ≤ AOP-a 9008 kol. 4  ')
        
        #90004
        if not( aop(si,9009,5) <= aop(si,9008,5) ):
            form_errors.append('AOP 9009 kol. 5 ≤ AOP-a 9008 kol. 5  ')
        
        #90005
        if not( aop(si,9010,4) <= aop(si,9009,4) ):
            form_errors.append('AOP 9010 kol. 4 ≤ AOP-a 9009 kol. 4  ')
        
        #90006
        if not( aop(si,9010,5) <= aop(si,9009,5) ):
            form_errors.append('AOP 9010 kol. 5 ≤ AOP-a 9009 kol. 5  ')
        
        #90007
        if not( suma(si,9013,9017,4) <= aop(si,9012,4) ):
            form_errors.append('AOP (9013 + 9014 + 9015 + 9016 + 9017) kol. 4 ≤ AOP-a 9012 kol. 4   ')
        
        #90008
        if not( suma(si,9013,9017,5) <= aop(si,9012,5) ):
            form_errors.append('AOP (9013 + 9014 + 9015 + 9016 + 9017) kol. 5 ≤ AOP-a 9012 kol. 5  ')
        
        #90009
        if not( aop(si,9024,4) <= aop(si,9023,4) ):
            form_errors.append('AOP 9024 kol. 4 ≤ AOP-a 9023 kol. 4  ')
        
        #90010
        if not( aop(si,9024,5) <= aop(si,9023,5) ):
            form_errors.append('AOP 9024 kol. 5 ≤ AOP-a 9023 kol. 5  ')
        
        #90011
        if not( suma_liste(si,[9007,9008,9012,9019,9020,9021],4) <= aop(bu,1031,5) ):
            form_errors.append('AOP (9007 + 9008 + 9012 + 9019 + 9020 + 9021) kol. 4 ≤  AOP-u 1031 kol. 5 bilansa uspeha Troškovi materijala, proizvodnih usluga, nematerijalni troškovi, troškovi doprinosa, novčane kazne i penali i ostali troškovi su izdvojeni deo ostalih rashoda ')
        
        #90012
        if not( suma_liste(si,[9007,9008,9012,9019,9020,9021],5) <= aop(bu,1031,6) ):
            form_errors.append('AOP (9007 + 9008 + 9012 + 9019 + 9020 + 9021) kol. 5 ≤  AOP-u 1031 kol. 6 bilansa uspeha Troškovi materijala, proizvodnih usluga, nematerijalni troškovi, troškovi doprinosa, novčane kazne i penali i ostali troškovi su izdvojeni deo ostalih rashoda ')
        
        #90013
        if not( aop(si,9011,4) == aop(bu,1029,5) ):
            lzbir =  aop(si,9011,4) 
            dzbir =  aop(bu,1029,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 9011 kol. 4 = AOP-u 1029 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #90014
        if not( aop(si,9011,5) == aop(bu,1029,6) ):
            lzbir =  aop(si,9011,5) 
            dzbir =  aop(bu,1029,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 9011 kol. 5 = AOP-u 1029 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #90015
        if( aop(si,9027,4) > aop(si,9022,4) ):
            if not( aop(si,9027,4)-aop(si,9022,4) == aop(bu,1021,5) ):
                lzbir =  aop(si,9027,4)-aop(si,9022,4) 
                dzbir =  aop(bu,1021,5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP (9027 - 9022) kol. 4 = AOP-u 1021 kol. 5 bilansa uspeha, ako je AOP 9027 kol. 4 > AOP-a 9022 kol. 4 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #90016
        if( aop(si,9027,5) > aop(si,9022,5) ):
            if not( aop(si,9027,5)-aop(si,9022,5) == aop(bu,1021,6) ):
                lzbir =  aop(si,9027,5)-aop(si,9022,5) 
                dzbir =  aop(bu,1021,6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP (9027 - 9022) kol. 5 = AOP-u 1021 kol. 6 bilansa uspeha, ako je AOP 9027 kol. 5 > AOP-a 9022 kol. 5 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #90017
        if( aop(si,9027,4) < aop(si,9022,4) ):
            if not( aop(si,9022,4)-aop(si,9027,4) == aop(bu,1022,5) ):
                lzbir =  aop(si,9022,4)-aop(si,9027,4) 
                dzbir =  aop(bu,1022,5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP (9022 - 9027) kol. 4 = AOP-u 1022 kol. 5 bilansa uspeha, ako je AOP 9027 kol. 4 < AOP-a 9022 kol. 4 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #90018
        if( aop(si,9027,5) < aop(si,9022,5) ):
            if not( aop(si,9022,5)-aop(si,9027,5) == aop(bu,1022,6) ):
                lzbir =  aop(si,9022,5)-aop(si,9027,5) 
                dzbir =  aop(bu,1022,6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP (9022 - 9027) kol. 5 = AOP-u 1022 kol. 6 bilansa uspeha, ako je AOP 9027 kol. 5 < AOP-a 9022 kol. 5 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #90019
        if not( suma_liste(si,[9023,9025],4) <= aop(bu,1025,5) ):
            form_errors.append('AOP (9023 + 9025) kol. 4 ≤ AOP-a 1025 kol. 5 bilansa uspeha Ostali prihodi operativnog poslovanja i prihodi od dividendi i učešća su izdvojeni deo Ostalih poslovnih prihoda ')
        
        #90020
        if not( suma_liste(si,[9023,9025],5) <= aop(bu,1025,6) ):
            form_errors.append('AOP (9023 + 9025) kol. 5 ≤ AOP-a 1025 kol. 6 bilansa uspeha Ostali prihodi operativnog poslovanja i prihodi od dividendi i učešća su izdvojeni deo Ostalih poslovnih prihoda ')
        
        #90021
        if not( aop(si,9026,4) <= aop(bu,1030,5) ):
            form_errors.append('AOP 9026 kol. 4  ≤ AOP-a 1030 kol. 5 bilansa uspeha Prihodi od naknade štete po osnovu osiguranja su izdvojeni deo ostalih prihoda ')
        
        #90022
        if not( aop(si,9026,5) <= aop(bu,1030,6) ):
            form_errors.append('AOP 9026 kol. 5  ≤ AOP-a 1030 kol. 6 bilansa uspeha Prihodi od naknade štete po osnovu osiguranja su izdvojeni deo ostalih prihoda ')
        
        #90023
        if not( aop(si,9034,3) > 0 ):
            form_warnings.append('AOP 9034 kol. 3 > 0 Na poziciji Prosečan broj zaposlenih nije iskazan podatak; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga ')
        
        #90024
        if not( aop(si,9034,4) <= 1000 ):
            form_warnings.append('AOP 9034 kol. 4 ≤ 1.000 Granične vrednosti date su da bi se izbegle slučajne greške prilikom iskazivanja broja zaposlenih; Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih; ')
        
        #90025
        if not( aop(si,9034,5) <= 1000 ):
            form_warnings.append('AOP 9034 kol. 5 ≤ 1.000 Granične vrednosti date su da bi se izbegle slučajne greške prilikom iskazivanja broja zaposlenih; Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih; ')
        
        ######################################
        #### KRAJ KONTROLNIH PRAVILA    ######
        ######################################

        return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors, 'exceptions' : exceptionList}

    except Exception as e:
        #trace = traceback.format_exc() #traceback.print_tb(sys.exc_info()[2])
        trace=''
        errorMsg = e.message

        exceptionList.append({'errorMessage':errorMsg, 'trace':trace})
        
        return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors, 'exceptions' : exceptionList}


