import sys
#sys.path.append(r"C:\IronPython2.7\Lib")
#import traceback
import datetime
from System import DateTime
 
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

#LISTA NEGATIVNIH PO OBRASCU
def find_negativni(aop_dict, prvi_aop, poslednji_aop, prva_kolona, poslednja_kolona): 
    aopi = ""
    for aop_broj in range (prvi_aop,poslednji_aop+1):
        for kolona in range (prva_kolona,poslednja_kolona+1):
                aop_key = broj_u_aop(aop_broj, kolona)
                if aop_key in aop_dict:
                    a=aop_dict[aop_key]       
                    if not (a is None):
                        if a < 0 :
                            aopi += "AOP " + str(aop_broj).zfill(4) + " kol. " + str(kolona) + " = " + str(aop(aop_dict, aop_broj, kolona)) + ", "                
    if len(aopi) > 0:
         aopi = aopi.Substring(0,aopi.Length-2)
    return aopi
   
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
        if not( suma(bs,1,18,5)+suma(bs,1,18,6)+suma(bs,1,18,7)+suma(bs,401,423,5)+suma(bs,401,423,6)+suma(bs,401,423,7)+suma(bu,1001,1048,5)+suma(bu,1001,1048,6)+suma(ioor,2001,2036,5)+suma(ioor,2001,2036,6)+suma(iotg,3001,3070,3)+suma(iotg,3001,3070,4) + suma(iopk, 4001, 4296, 1) + suma(si,9001,9045,4)+suma(si,9001,9045,5) > 0 ):
            form_errors.append('Zbir podataka na oznakama za AOP (0001 do 0018) kol. 5 + (0001 do 0018) kol. 6 + (0001 do 0018) kol. 7 bilans stanja + (0401 do 0423) kol. 5 + (0401 do 0423) kol. 6 + (0401 do 0423) kol. 7 bilansa stanja + (1001 do 1048) kol. 5 + (1001 do 1048) kol. 6 bilansa uspeha + (2001 do 2036) kol. 5 + (2001 do 2036) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3070) kol. 3 + (3001 do 3070) kol. 4 izveštaja o tokovima gotovine + (4001 do 4296) izveštaja o promenama na kapitalu + (9001 do 9045) kol. 4 + (9001 do 9045) kol. 5 statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka; ')
            return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors, 'exceptions' : exceptionList}
        
        #00000-2
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-3
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-4
        # U bar jednoj od tri navedene forme kolona napomena mora da ima bar jedan karakter
        bsNapomene = Zahtev.Forme['Bilans stanja'].TekstualnaPoljaForme;
        buNapomene = Zahtev.Forme['Bilans uspeha'].TekstualnaPoljaForme;
        ioorNapomene = Zahtev.Forme['Izveštaj o ostalom rezultatu'].TekstualnaPoljaForme;
        if not(proveriNapomene(bsNapomene, 1, 18, 4) or proveriNapomene(bsNapomene, 401, 423, 4) or proveriNapomene(buNapomene, 1001, 1048, 4) or proveriNapomene(ioorNapomene, 2001, 2036, 4)): 
            form_errors.append('Na AOP-u (0001 do 0018) bilansa stanja + (0401 do 0423) bilansa stanja + (1001 do 1048) bilansa uspeha + (2001 do 2036) izveštaja o ostalom rezultatu u koloni 4 (Broj napomene) mora biti uneta bar jedna oznaka iz Napomena uz finansijske izveštaje Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje')
        
        #Provera da li je fizahtev placen
        if not(Zahtev.Placen):
            form_warnings.append('Naknada za obradu i javno objavljivanje izveštaja i propisane dokumentacije nije uplaćena u propisanom iznosu. Instrukcije za uplatu propisane naknade date su u okviru PIS FI sistema za konkretan zahtev, na linku „Status naplate zahteva / Instrukcija za plaćanje". Ukoliko ste izvršili uplatu, a naknada nije uparena, priložite Dokaz o uplati naknade u delu Dokumentacija (na mestu predviđenom za dokaz o uplati naknade), kako biste mogli da podnesete izveštaj.');

        # UPOZORENJE ZA SVE KOJI DOSTAVLJAJU SAMOSTALNI RGFI
        form_warnings.append('VAŽNA NAPOMENA: Proverite da li ste podatak o broju zaposlenih koji ste iskazali u obrascu Posebni podaci usaglasili sa podatkom o broju zaposlenih koji ste iskazali u Izveštaju za statističke potrebe. Ukoliko se podaci razlikuju potrebno je dostaviti obrazloženje zbog čega je nastala razlika, u suprotnom biće poslato obaveštenje o nedostacima.')
        
        #Provera negativnih AOP-a
        lista=""
        lista_bs = find_negativni(bs, 1, 423, 5, 7)
        lista_bu = find_negativni(bu, 1001, 1048, 5, 6)
        lista_ioor = find_negativni(ioor, 2001, 2036, 5, 6)
        lista_iotg = find_negativni(iotg, 3001, 3070, 3, 4)
        lista_iopk = find_negativni(iopk, 4001, 4296, 1, 1)
       
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
        if len(lista) > 0:                                           
            form_errors.append("Unete vrednosti ne mogu biti negativne ! (" + lista + ")")        
        


        #BILANS STANJA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        #00001
        if not( suma(bs,1,18,5)+suma(bs,401,423,5) > 0 ):
            form_warnings.append('Zbir podataka na oznakama za AOP (0001 do 0018) kol. 5 + (0401 do 0423) kol. 5 > 0 Bilans stanja, po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga ')
        
        #00002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,18,6)+suma(bs,401,423,6) == 0 ):
                lzbir =  suma(bs,1,18,6)+suma(bs,401,423,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Zbir podataka na oznakama za AOP (0001 do 0018) kol. 6 + (0401 do 0423) kol. 6 = 0 Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00003
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,18,7)+suma(bs,401,423,7) == 0 ):
                lzbir =  suma(bs,1,18,7)+suma(bs,401,423,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Zbir podataka na oznakama za AOP (0001 do 0018) kol. 7 + (0401 do 0423) kol. 7 = 0 Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00004
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,18,6)+suma(bs,401,423,6) > 0 ):
                form_warnings.append('Zbir podataka na oznakama za AOP (0001 do 0018)kol. 6 + (0401 do 0423) kol. 6 > 0 Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga ')
        
        #00005
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,18,7)+suma(bs,401,423,7) > 0 ):
                form_warnings.append('Zbir podataka na oznakama za AOP (0001 do 0018) kol. 7 + (0401 do 0423) kol. 7 > 0 Bilans stanja, po pravilu,  mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga ')
        
        #00006
        if not(aop (bs,18,5) == suma (bs, 1,17,5)):
            #AOPi
            lzbir = aop (bs,18,5) 
            dzbir =  suma (bs, 1,17,5)
            razlika = lzbir - dzbir
            form_errors.append("AOP 0018 kol. 5 = zbiru na oznakama za AOP od 0001 do 0017 kol. 5   "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #00007
        if not(aop (bs,18,6) == suma (bs, 1,17,6)):
            #AOPi
            lzbir = aop (bs,18,6) 
            dzbir =  suma (bs, 1,17,6)
            razlika = lzbir - dzbir
            form_errors.append("AOP 0018 kol. 6 = zbiru na oznakama za AOP od 0001 do 0017 kol. 6   "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #00008
        if not(aop (bs,18,7) == suma (bs, 1,17,7)):
            #AOPi
            lzbir = aop (bs,18,7) 
            dzbir =  suma (bs, 1,17,7)
            razlika = lzbir - dzbir
            form_errors.append("AOP 0020 kol. 7 = zbiru na oznakama za AOP od 0001 do 0017 kol. 7   "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #00009
        if not(aop (bs,413,5) == suma (bs, 401,412,5)):
            #AOPi
            lzbir = aop (bs,413,5) 
            dzbir =  suma (bs, 401,412,5)
            razlika = lzbir - dzbir
            form_errors.append("AOP 0413 kol. 5 = zbiru na oznakama za AOP od 0401 do 0412 kol. 5   "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #00010
        if not(aop (bs,413,6) == suma (bs, 401,412,6)):
            #AOPi
            lzbir = aop (bs,413,6) 
            dzbir =  suma (bs, 401,412,6)
            razlika = lzbir - dzbir
            form_errors.append("AOP 0413 kol. 6 = zbiru na oznakama za AOP od 0401 do 0412 kol. 6   "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #00011
        if not(aop (bs,413,7) == suma (bs, 401,412,7)):
            #AOPi
            lzbir = aop (bs,413,7) 
            dzbir =  suma (bs, 401,412,7)
            razlika = lzbir - dzbir
            form_errors.append("AOP 0413 kol. 7 = zbiru na oznakama za AOP od 0401 do 0412 kol. 7   "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #00012
        if not( aop(bs,420,5) == 0 ):
            lzbir =  aop(bs,420,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0420 kol. 5 = 0 Učešće bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00013
        if not( aop(bs,420,6) == 0 ):
            lzbir =  aop(bs,420,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0420 kol. 6 = 0 Učešće bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00014
        if not( aop(bs,420,7) == 0 ):
            lzbir =  aop(bs,420,7) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0420 kol. 7 = 0 Učešće bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00015
        if( aop(bs,418,5) > 0 ):
            if not( aop(bs,419,5) == 0 ):
                lzbir =  aop(bs,419,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0418 kol. 5 > 0, onda je AOP 0419 kol. 5 = 0 Ne mogu biti istovremeno prikazani dugovni i potražni saldo računa  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00016
        if( aop(bs,419,5) > 0 ):
            if not( aop(bs,418,5) == 0 ):
                lzbir =  aop(bs,418,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0419 kol. 5 > 0, onda je AOP 0418 kol. 5 = 0 Ne mogu biti istovremeno prikazani dugovni i potražni saldo računa  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00017
        if( aop(bs,418,6) > 0 ):
            if not( aop(bs,419,6) == 0 ):
                lzbir =  aop(bs,419,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0418 kol. 6 > 0, onda je AOP 0419 kol. 6 = 0 Ne mogu biti istovremeno prikazani dugovni i potražni saldo računa  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00018
        if( aop(bs,419,6) > 0 ):
            if not( aop(bs,418,6) == 0 ):
                lzbir =  aop(bs,418,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0419 kol. 6 > 0, onda je AOP 0418 kol. 6 = 0 Ne mogu biti istovremeno prikazani dugovni i potražni saldo računa  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00019
        if( aop(bs,418,7) > 0 ):
            if not( aop(bs,419,7) == 0 ):
                lzbir =  aop(bs,419,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0418 kol. 7 > 0, onda je AOP 0419 kol. 7 = 0 Ne mogu biti istovremeno prikazani dugovni i potražni saldo računa  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00020
        if( aop(bs,419,7) > 0 ):
            if not( aop(bs,418,7) == 0 ):
                lzbir =  aop(bs,418,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0419 kol. 7 > 0, onda je AOP 0418 kol. 7 = 0 Ne mogu biti istovremeno prikazani dugovni i potražni saldo računa  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00021
        if( suma_liste(bs,[414,416,418,420],5) > suma_liste(bs,[415,417,419],5) ):
            if not( aop(bs,421,5) == suma_liste(bs,[414,416,418,420],5)-suma_liste(bs,[415,417,419],5) ):
                lzbir =  aop(bs,421,5) 
                dzbir =  suma_liste(bs,[414,416,418,420],5)-suma_liste(bs,[415,417,419],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 0421 kol. 5 = AOP-u (0414 - 0415 + 0416 - 0417 + 0418 - 0419 + 0420) kol. 5, ako je AOP (0414 + 0416 + 0418 + 0420) kol. 5 > AOP-a (0415 + 0417 + 0419) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00022
        if( suma_liste(bs,[414,416,418,420],6) > suma_liste(bs,[415,417,419],6) ):
            if not( aop(bs,421,6) == suma_liste(bs,[414,416,418,420],6)-suma_liste(bs,[415,417,419],6) ):
                lzbir =  aop(bs,421,6) 
                dzbir =  suma_liste(bs,[414,416,418,420],6)-suma_liste(bs,[415,417,419],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 0421 kol. 6 = AOP-u (0414 - 0415 + 0416 - 0417 + 0418 - 0419 + 0420) kol. 6, ako je AOP (0414 + 0416 + 0418 + 0420) kol. 6 > AOP-a (0415 + 0417 + 0419) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00023
        if( suma_liste(bs,[414,416,418,420],7) > suma_liste(bs,[415,417,419],7) ):
            if not( aop(bs,421,7) == suma_liste(bs,[414,416,418,420],7)-suma_liste(bs,[415,417,419],7) ):
                lzbir =  aop(bs,421,7) 
                dzbir =  suma_liste(bs,[414,416,418,420],7)-suma_liste(bs,[415,417,419],7) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 0421 kol. 7 = AOP-u (0414 - 0415 + 0416 - 0417 + 0418 - 0419 + 0420) kol. 7, ako je AOP (0414 + 0416 + 0418 + 0420) kol. 7 > AOP-a (0415 + 0417 + 0419) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00024
        if( suma_liste(bs,[414,416,418,420],5) < suma_liste(bs,[415,417,419],5) ):
            if not( aop(bs,422,5) == suma_liste(bs,[415,417,419],5)-suma_liste(bs,[414,416,418,420],5) ):
                lzbir =  aop(bs,422,5) 
                dzbir =  suma_liste(bs,[415,417,419],5)-suma_liste(bs,[414,416,418,420],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 0422 kol. 5 = AOP-u (0415 - 0414 - 0416 + 0417 - 0418 + 0419 - 0420) kol. 5, ako je AOP (0414 + 0416 + 0418 + 0420) kol. 5 < AOP-a (0415 + 0417 + 0419) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00025
        if( suma_liste(bs,[414,416,418,420],6) < suma_liste(bs,[415,417,419],6) ):
            if not( aop(bs,422,6) == suma_liste(bs,[415,417,419],6)-suma_liste(bs,[414,416,418,420],6) ):
                lzbir =  aop(bs,422,6) 
                dzbir =  suma_liste(bs,[415,417,419],6)-suma_liste(bs,[414,416,418,420],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 0422 kol. 6 = AOP-u (0415 - 0414 - 0416 + 0417 - 0418 + 0419 - 0420) kol. 6, ako je AOP (0414 + 0416 + 0418 + 0420) kol. 6 < AOP-a (0415 + 0417 + 0419) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00026
        if( suma_liste(bs,[414,416,418,420],7) < suma_liste(bs,[415,417,419],7) ):
            if not( aop(bs,422,7) == suma_liste(bs,[415,417,419],7)-suma_liste(bs,[414,416,418,420],7) ):
                lzbir =  aop(bs,422,7) 
                dzbir =  suma_liste(bs,[415,417,419],7)-suma_liste(bs,[414,416,418,420],7) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 0422 kol. 7 = AOP-u (0415 - 0414 - 0416 + 0417 - 0418 + 0419 - 0420) kol. 7, ako je AOP (0414 + 0416 + 0418 + 0420) kol. 7 < AOP-a (0415 + 0417 + 0419) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00027
        if( suma_liste(bs,[414,416,418,420],5) == suma_liste(bs,[415,417,419],5) ):
            if not( suma(bs,421,422,5) == 0 ):
                lzbir =  suma(bs,421,422,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (0421 + 0422) kol. 5 = 0, ako je AOP (0414 + 0416 + 0418 + 0420) kol. 5 = AOP-u (0415 + 0417 + 0419) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00028
        if( suma_liste(bs,[414,416,418,420],6) == suma_liste(bs,[415,417,419],6) ):
            if not( suma(bs,421,422,6) == 0 ):
                lzbir =  suma(bs,421,422,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (0421 + 0422) kol. 6 = 0, ako je AOP (0414 + 0416 + 0418 + 0420) kol. 6 = AOP-u (0415 + 0417 + 0419) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00029
        if( suma_liste(bs,[414,416,418,420],7) == suma_liste(bs,[415,417,419],7) ):
            if not( suma(bs,421,422,7) == 0 ):
                lzbir =  suma(bs,421,422,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (0421 + 0422) kol. 7 = 0, ako je AOP (0414 + 0416 + 0418 + 0420) kol. 7 = AOP-u (0415 + 0417 + 0419) kol. 7 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00030
        if( aop(bs,421,5) > 0 ):
            if not( aop(bs,422,5) == 0 ):
                lzbir =  aop(bs,422,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0421 kol. 5 > 0 onda je AOP 0422 kol. 5 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00031
        if( aop(bs,422,5) > 0 ):
            if not( aop(bs,421,5) == 0 ):
                lzbir =  aop(bs,421,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0422 kol. 5 > 0 onda je AOP 0421 kol. 5 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00032
        if( aop(bs,421,6) > 0 ):
            if not( aop(bs,422,6) == 0 ):
                lzbir =  aop(bs,422,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0421 kol. 6 > 0 onda je AOP 0422 kol. 6 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00033
        if( aop(bs,422,6) > 0 ):
            if not( aop(bs,421,6) == 0 ):
                lzbir =  aop(bs,421,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0422 kol. 6 > 0 onda je AOP 0421 kol. 6 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00034
        if( aop(bs,421,7) > 0 ):
            if not( aop(bs,422,7) == 0 ):
                lzbir =  aop(bs,422,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0421 kol. 7 > 0 onda je AOP 0422 kol. 7 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00035
        if( aop(bs,422,7) > 0 ):
            if not( aop(bs,421,7) == 0 ):
                lzbir =  aop(bs,421,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0422 kol. 7 > 0 onda je AOP 0421 kol. 7 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00036
        if not( aop(bs,423,5) == suma_liste(bs,[413,421],5)-aop(bs,422,5) ):
            lzbir =  aop(bs,423,5) 
            dzbir =  suma_liste(bs,[413,421],5)-aop(bs,422,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0423 kol. 5 = AOP-u (0413 + 0421 - 0422) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00037
        if not( aop(bs,423,6) == suma_liste(bs,[413,421],6)-aop(bs,422,6) ):
            lzbir =  aop(bs,423,6) 
            dzbir =  suma_liste(bs,[413,421],6)-aop(bs,422,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0423 kol. 6 = AOP-u (0413 + 0421 - 0422) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00038
        if not( aop(bs,423,7) == suma_liste(bs,[413,421],7)-aop(bs,422,7) ):
            lzbir =  aop(bs,423,7) 
            dzbir =  suma_liste(bs,[413,421],7)-aop(bs,422,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0423 kol. 7 = AOP-u (0413 + 0421 - 0422) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00039
        if not( aop(bs,18,5) == aop(bs,423,5) ):
            lzbir =  aop(bs,18,5) 
            dzbir =  aop(bs,423,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0018 kol. 5 = AOP-u 0423 kol. 5 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00040
        if not( aop(bs,18,6) == aop(bs,423,6) ):
            lzbir =  aop(bs,18,6) 
            dzbir =  aop(bs,423,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0018 kol. 6 = AOP-u 0423 kol. 6 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00041
        if not( aop(bs,18,7) == aop(bs,423,7) ):
            lzbir =  aop(bs,18,7) 
            dzbir =  aop(bs,423,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0018 kol. 7 = AOP-u 0423 kol. 7 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00042
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if( suma(bu,1001,1048,5) > 0 ):
                if not( suma(bs,1,18,5)+suma(bs,401,423,5) != suma(bs,1,18,6)+suma(bs,401,423,6) ):
                    form_warnings.append('***Ako je zbir podataka na oznakama za AOP (1001 do 1048) kol. 5 > 0 onda je zbir podataka na oznakama za AOP (0001 do 0018) kol. 5 + (0401 do 0423) kol. 5 ≠ zbiru podataka na oznakama za AOP (0001 do 0018) kol. 6 + (0401 do 0423) kol. 6 Zbirovi podataka u kolonama 5 i 6 bilansa stanja su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama;  ')
        
        #BILANS USPEHA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        #10001
        if not( suma(bu,1001,1048,5) > 0 ):
            form_warnings.append('Zbir podataka na oznakama za AOP (1001 do 1048) kol. 5 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga ')
        
        #10002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bu,1001,1048,6) == 0 ):
                lzbir =  suma(bu,1001,1048,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Zbir podataka na oznakama za AOP (1001 do 1048) kol. 6 = 0 Bilans uspeha za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bu,1001,1048,6) > 0 ):
                form_warnings.append('Zbir podataka na oznakama za AOP (1001 do 1048) kol. 6 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga ')
        
        #10004
        if( aop(bu,1001,5) > aop(bu,1002,5) ):
            if not( aop(bu,1003,5) == aop(bu,1001,5)-aop(bu,1002,5) ):
                lzbir =  aop(bu,1003,5) 
                dzbir =  aop(bu,1001,5)-aop(bu,1002,5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1003 kol. 5 = AOP-u (1001 - 1002) kol. 5, ako je AOP 1001 kol. 5 > AOP-a 1002 kol. 5    '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10005
        if( aop(bu,1001,6) > aop(bu,1002,6) ):
            if not( aop(bu,1003,6) == aop(bu,1001,6)-aop(bu,1002,6) ):
                lzbir =  aop(bu,1003,6) 
                dzbir =  aop(bu,1001,6)-aop(bu,1002,6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1003 kol. 6 = AOP-u (1001 - 1002) kol. 6, ako je AOP 1001 kol. 6 > AOP-a 1002 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10006
        if( aop(bu,1001,5) < aop(bu,1002,5) ):
            if not( aop(bu,1004,5) == aop(bu,1002,5)-aop(bu,1001,5) ):
                lzbir =  aop(bu,1004,5) 
                dzbir =  aop(bu,1002,5)-aop(bu,1001,5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1004 kol. 5 = AOP-u (1002 -1001) kol. 5, ako je AOP 1001 kol. 5 < AOP-a 1002 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10007
        if( aop(bu,1001,6) < aop(bu,1002,6) ):
            if not( aop(bu,1004,6) == aop(bu,1002,6)-aop(bu,1001,6) ):
                lzbir =  aop(bu,1004,6) 
                dzbir =  aop(bu,1002,6)-aop(bu,1001,6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1004 kol. 6 = AOP-u (1002 -1001) kol. 6, ako je AOP 1001 kol. 6 < AOP-a 1002 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10008
        if( aop(bu,1001,5) == aop(bu,1002,5) ):
            if not( suma(bu,1003,1004,5) == 0 ):
                lzbir =  suma(bu,1003,1004,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append(' AOP (1003 + 1004) kol. 5 = 0, ako je AOP 1001 kol. 5 = AOP-u 1002 kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10009
        if( aop(bu,1001,6) == aop(bu,1002,6) ):
            if not( suma(bu,1003,1004,6) == 0 ):
                lzbir =  suma(bu,1003,1004,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append(' AOP (1003 + 1004) kol. 6 = 0, ako je AOP 1001 kol. 6 = AOP-u 1002 kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10010
        if( aop(bu,1003,5) > 0 ):
            if not( aop(bu,1004,5) == 0 ):
                lzbir =  aop(bu,1004,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1003 kol. 5 > 0 onda je AOP 1004 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihodi i rashodi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10011
        if( aop(bu,1004,5) > 0 ):
            if not( aop(bu,1003,5) == 0 ):
                lzbir =  aop(bu,1003,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1004 kol. 5 > 0 onda je AOP 1003 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihodi i rashodi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10012
        if( aop(bu,1003,6) > 0 ):
            if not( aop(bu,1004,6) == 0 ):
                lzbir =  aop(bu,1004,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1003 kol. 6 > 0 onda je AOP 1004 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihodi i rashodi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10013
        if( aop(bu,1004,6) > 0 ):
            if not( aop(bu,1003,6) == 0 ):
                lzbir =  aop(bu,1003,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1004 kol. 6 > 0 onda je AOP 1003 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihodi i rashodi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10014
        if not( suma_liste(bu,[1001,1004],5) == suma(bu,1002,1003,5) ):
            lzbir =  suma_liste(bu,[1001,1004],5) 
            dzbir =  suma(bu,1002,1003,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1001 + 1004) kol. 5 = AOP-u (1002 + 1003) kol. 5  Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10015
        if not( suma_liste(bu,[1001,1004],6) == suma(bu,1002,1003,6) ):
            lzbir =  suma_liste(bu,[1001,1004],6) 
            dzbir =  suma(bu,1002,1003,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1001 + 1004) kol. 6 = AOP-u (1002 + 1003) kol. 6  Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10016
        if( aop(bu,1005,5) > aop(bu,1006,5) ):
            if not( aop(bu,1007,5) == aop(bu,1005,5)-aop(bu,1006,5) ):
                lzbir =  aop(bu,1007,5) 
                dzbir =  aop(bu,1005,5)-aop(bu,1006,5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1007 kol. 5 = AOP-u (1005 -1006) kol. 5, ako je AOP 1005 kol. 5 > AOP-a 1006 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10017
        if( aop(bu,1005,6) > aop(bu,1006,6) ):
            if not( aop(bu,1007,6) == aop(bu,1005,6)-aop(bu,1006,6) ):
                lzbir =  aop(bu,1007,6) 
                dzbir =  aop(bu,1005,6)-aop(bu,1006,6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1007 kol. 6 = AOP-u (1005 -1006) kol. 6, ako je AOP 1005 kol. 6 > AOP-a 1006 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10018
        if( aop(bu,1005,5) < aop(bu,1006,5) ):
            if not( aop(bu,1008,5) == aop(bu,1006,5)-aop(bu,1005,5) ):
                lzbir =  aop(bu,1008,5) 
                dzbir =  aop(bu,1006,5)-aop(bu,1005,5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1008 kol. 5 = AOP-u (1006 -1005) kol. 5, ako je AOP 1005 kol. 5 < AOP-a 1006 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10019
        if( aop(bu,1005,6) < aop(bu,1006,6) ):
            if not( aop(bu,1008,6) == aop(bu,1006,6)-aop(bu,1005,6) ):
                lzbir =  aop(bu,1008,6) 
                dzbir =  aop(bu,1006,6)-aop(bu,1005,6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1008 kol. 6 = AOP-u (1006 -1005) kol. 6, ako je AOP 1005 kol. 6 < AOP-a 1006 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10020
        if( aop(bu,1005,5) == aop(bu,1006,5) ):
            if not( suma(bu,1007,1008,5) == 0 ):
                lzbir =  suma(bu,1007,1008,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1007 + 1008) kol. 5 = 0, ako je AOP 1005 kol. 5 = AOP-u 1006 kol. 5  Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10021
        if( aop(bu,1005,6) == aop(bu,1006,6) ):
            if not( suma(bu,1007,1008,6) == 0 ):
                lzbir =  suma(bu,1007,1008,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1007 + 1008) kol. 6 = 0, ako je AOP 1005 kol. 6 = AOP-u 1006 kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10022
        if( aop(bu,1007,5) > 0 ):
            if not( aop(bu,1008,5) == 0 ):
                lzbir =  aop(bu,1008,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1007 kol. 5 > 0 onda je AOP 1008 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihodi i rashodi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10023
        if( aop(bu,1008,5) > 0 ):
            if not( aop(bu,1007,5) == 0 ):
                lzbir =  aop(bu,1007,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1008 kol. 5 > 0 onda je AOP 1007 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihodi i rashodi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10024
        if( aop(bu,1007,6) > 0 ):
            if not( aop(bu,1008,6) == 0 ):
                lzbir =  aop(bu,1008,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1007 kol. 6 > 0 onda je AOP 1008 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihodi i rashodi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10025
        if( aop(bu,1008,6) > 0 ):
            if not( aop(bu,1007,6) == 0 ):
                lzbir =  aop(bu,1007,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1008 kol. 6 > 0 onda je AOP 1007 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihodi i rashodi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10026
        if not( suma_liste(bu,[1005,1008],5) == suma(bu,1006,1007,5) ):
            lzbir =  suma_liste(bu,[1005,1008],5) 
            dzbir =  suma(bu,1006,1007,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1005 + 1008) kol. 5 = AOP-u (1006 + 1007) kol. 5  Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10027
        if not( suma_liste(bu,[1005,1008],6) == suma(bu,1006,1007,6) ):
            lzbir =  suma_liste(bu,[1005,1008],6) 
            dzbir =  suma(bu,1006,1007,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1005 + 1008) kol. 6 = AOP-u (1006 + 1007) kol. 6  Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10028
        if( aop(bu,1009,5) > 0 ):
            if not( aop(bu,1010,5) == 0 ):
                lzbir =  aop(bu,1010,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1009 kol. 5 > 0 onda je AOP 1010 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10029
        if( aop(bu,1010,5) > 0 ):
            if not( aop(bu,1009,5) == 0 ):
                lzbir =  aop(bu,1009,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1010 kol. 5 > 0 onda je AOP 1009 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10030
        if( aop(bu,1009,6) > 0 ):
            if not( aop(bu,1010,6) == 0 ):
                lzbir =  aop(bu,1010,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1009 kol. 6 > 0 onda je AOP 1010 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10031
        if( aop(bu,1010,6) > 0 ):
            if not( aop(bu,1009,6) == 0 ):
                lzbir =  aop(bu,1009,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1010 kol. 6 > 0 onda je AOP 1009 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10032
        if( aop(bu,1011,5) > 0 ):
            if not( aop(bu,1012,5) == 0 ):
                lzbir =  aop(bu,1012,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1011 kol. 5 > 0 onda je AOP 1012 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10033
        if( aop(bu,1012,5) > 0 ):
            if not( aop(bu,1011,5) == 0 ):
                lzbir =  aop(bu,1011,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1012 kol. 5 > 0 onda je AOP 1011 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10034
        if( aop(bu,1011,6) > 0 ):
            if not( aop(bu,1012,6) == 0 ):
                lzbir =  aop(bu,1012,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1011 kol. 6 > 0 onda je AOP 1012 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10035
        if( aop(bu,1012,6) > 0 ):
            if not( aop(bu,1011,6) == 0 ):
                lzbir =  aop(bu,1011,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1012 kol. 6 > 0 onda je AOP 1011 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10036
        if( aop(bu,1013,5) > 0 ):
            if not( aop(bu,1014,5) == 0 ):
                lzbir =  aop(bu,1014,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1013 kol. 5 > 0 onda je AOP 1014 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10037
        if( aop(bu,1014,5) > 0 ):
            if not( aop(bu,1013,5) == 0 ):
                lzbir =  aop(bu,1013,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1014 kol. 5 > 0 onda je AOP 1013 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10038
        if( aop(bu,1013,6) > 0 ):
            if not( aop(bu,1014,6) == 0 ):
                lzbir =  aop(bu,1014,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1013 kol. 6 > 0 onda je AOP 1014 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10039
        if( aop(bu,1014,6) > 0 ):
            if not( aop(bu,1013,6) == 0 ):
                lzbir =  aop(bu,1013,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1014 kol. 6 > 0 onda je AOP 1013 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10040
        if( aop(bu,1015,5) > 0 ):
            if not( aop(bu,1016,5) == 0 ):
                lzbir =  aop(bu,1016,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1015 kol. 5 > 0 onda je AOP 1016 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10041
        if( aop(bu,1016,5) > 0 ):
            if not( aop(bu,1015,5) == 0 ):
                lzbir =  aop(bu,1015,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1016 kol. 5 > 0 onda je AOP 1015 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10042
        if( aop(bu,1015,6) > 0 ):
            if not( aop(bu,1016,6) == 0 ):
                lzbir =  aop(bu,1016,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1015 kol. 6 > 0 onda je AOP 1016 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10043
        if( aop(bu,1016,6) > 0 ):
            if not( aop(bu,1015,6) == 0 ):
                lzbir =  aop(bu,1015,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1016 kol. 6 > 0 onda je AOP 1015 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10044
        if( aop(bu,1017,5) > 0 ):
            if not( aop(bu,1018,5) == 0 ):
                lzbir =  aop(bu,1018,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1017 kol. 5 > 0 onda je AOP 1018 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihodi i rashodi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10045
        if( aop(bu,1018,5) > 0 ):
            if not( aop(bu,1017,5) == 0 ):
                lzbir =  aop(bu,1017,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1018 kol. 5 > 0 onda je AOP 1017 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihodi i rashodi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10046
        if( aop(bu,1017,6) > 0 ):
            if not( aop(bu,1018,6) == 0 ):
                lzbir =  aop(bu,1018,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1017 kol. 6 > 0 onda je AOP 1018 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihodi i rashodi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10047
        if( aop(bu,1018,6) > 0 ):
            if not( aop(bu,1017,6) == 0 ):
                lzbir =  aop(bu,1017,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1018 kol. 6 > 0 onda je AOP 1017 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihodi i rashodi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10048
        if( aop(bu,1019,5) > 0 ):
            if not( aop(bu,1020,5) == 0 ):
                lzbir =  aop(bu,1020,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1019 kol. 5 > 0 onda je AOP 1020 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihodi i rashodi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10049
        if( aop(bu,1020,5) > 0 ):
            if not( aop(bu,1019,5) == 0 ):
                lzbir =  aop(bu,1019,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 1020 kol. 5 > 0 onda je AOP 1019 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihodi i rashodi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10050
        if( aop(bu,1019,6) > 0 ):
            if not( aop(bu,1020,6) == 0 ):
                lzbir =  aop(bu,1020,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1019 kol. 6 > 0 onda je AOP 1020 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihodi i rashodi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10051
        if( aop(bu,1020,6) > 0 ):
            if not( aop(bu,1019,6) == 0 ):
                lzbir =  aop(bu,1019,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 1020 kol. 6 > 0 onda je AOP 1019 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihodi i rashodi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10052
        if( aop(bu,1021,5) > 0 ):
            if not( aop(bu,1022,5) == 0 ):
                lzbir =  aop(bu,1022,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1021 kol. 5 > 0 onda je AOP 1022 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10053
        if( aop(bu,1022,5) > 0 ):
            if not( aop(bu,1021,5) == 0 ):
                lzbir =  aop(bu,1021,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1022 kol. 5 > 0 onda je AOP 1021 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10054
        if( aop(bu,1021,6) > 0 ):
            if not( aop(bu,1022,6) == 0 ):
                lzbir =  aop(bu,1022,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1021 kol. 6 > 0 onda je AOP 1022 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10055
        if( aop(bu,1022,6) > 0 ):
            if not( aop(bu,1021,6) == 0 ):
                lzbir =  aop(bu,1021,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1022 kol. 6 > 0 onda je AOP 1021 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10056
        if( aop(bu,1023,5) > 0 ):
            if not( aop(bu,1024,5) == 0 ):
                lzbir =  aop(bu,1024,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1023 kol. 5 > 0 onda je AOP 1024 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10057
        if( aop(bu,1024,5) > 0 ):
            if not( aop(bu,1023,5) == 0 ):
                lzbir =  aop(bu,1023,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1024 kol. 5 > 0 onda je AOP 1023 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10058
        if( aop(bu,1023,6) > 0 ):
            if not( aop(bu,1024,6) == 0 ):
                lzbir =  aop(bu,1024,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1023 kol. 6 > 0 onda je AOP 1024 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10059
        if( aop(bu,1024,6) > 0 ):
            if not( aop(bu,1023,6) == 0 ):
                lzbir =  aop(bu,1023,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1024 kol. 6 > 0 onda je AOP 1023 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10060
        if( suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],5) > suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],5) ):
            if not( aop(bu,1026,5) == suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],5)-suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],5) ):
                lzbir =  aop(bu,1026,5) 
                dzbir =  suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],5)-suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1026 kol. 5 = AOP-u (1003 - 1004 + 1007 - 1008 + 1009 - 1010 + 1011 - 1012 + 1013 - 1014 + 1015 - 1016 + 1017 - 1018 + 1019 - 1020 + 1021 - 1022 + 1023 - 1024 +1025) kol. 5, ako je AOP (1003 + 1007 + 1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025) kol. 5 > AOP-a (1004 + 1008 + 1010 + 1012 + 1014 + 1016 + 1018 + 1020 + 1022 + 1024) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10061
        if( suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],6) > suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],6) ):
            if not( aop(bu,1026,6) == suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],6)-suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],6) ):
                lzbir =  aop(bu,1026,6) 
                dzbir =  suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],6)-suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1026 kol. 6 = AOP-u (1003 - 1004 + 1007 - 1008 + 1009 - 1010 + 1011 - 1012 + 1013 - 1014 + 1015 - 1016 + 1017 - 1018 + 1019 - 1020 + 1021 - 1022 + 1023 - 1024 +1025) kol. 6, ako je AOP (1003 + 1007 + 1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025) kol. 6 > AOP-a (1004 + 1008 + 1010 + 1012 + 1014 + 1016 + 1018 + 1020 + 1022 + 1024) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10062
        if( suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],5) < suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],5) ):
            if not( aop(bu,1027,5) == suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],5)-suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],5) ):
                lzbir =  aop(bu,1027,5) 
                dzbir =  suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],5)-suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1027 kol. 5 = AOP-u (1004 - 1003 - 1007 + 1008 - 1009 + 1010 - 1011 + 1012 - 1013 + 1014 - 1015 + 1016 - 1017 + 1018 - 1019 + 1020 - 1021 + 1022 - 1023 + 1024 - 1025) kol. 5, ako je AOP (1003 + 1007 + 1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025) kol. 5 < AOP-a (1004 + 1008 + 1010 + 1012 + 1014 + 1016 + 1018 + 1020 + 1022 + 1024) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10063
        if( suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],6) < suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],6) ):
            if not( aop(bu,1027,6) == suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],6)-suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],6) ):
                lzbir =  aop(bu,1027,6) 
                dzbir =  suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],6)-suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1027 kol. 6 = AOP-u (1004 - 1003 - 1007 + 1008 - 1009 + 1010 - 1011 + 1012 - 1013 + 1014 - 1015 + 1016 - 1017 + 1018 - 1019 + 1020 - 1021 + 1022 - 1023 + 1024 - 1025) kol. 6, ako je AOP (1003 + 1007 + 1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025) kol. 6 < AOP-a (1004 + 1008 + 1010 + 1012 + 1014 + 1016 + 1018 + 1020 + 1022 + 1024) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10064
        if( suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],5) == suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],5) ):
            if not( suma(bu,1026,1027,5) == 0 ):
                lzbir =  suma(bu,1026,1027,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1026 + 1027 ) kol. 5 = 0, ako je AOP (1003 + 1007 + 1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025) kol. 5 = AOP-u (1004 + 1008 + 1010 + 1012 + 1014 + 1016 + 1018 + 1020 + 1022 + 1024) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10065
        if( suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025],6) == suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024],6) ):
            if not( suma(bu,1026,1027,6) == 0 ):
                lzbir =  suma(bu,1026,1027,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1026 + 1027 ) kol. 6 = 0, ako je AOP (1003 + 1007 + 1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025) kol. 6 = AOP-u (1004 + 1008 + 1010 + 1012 + 1014 + 1016 + 1018 + 1020 + 1022 + 1024) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10066
        if( aop(bu,1026,5) > 0 ):
            if not( aop(bu,1027,5) == 0 ):
                lzbir =  aop(bu,1027,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 1026 kol. 5 > 0 onda je AOP 1027 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani ukupan neto poslovni prihod i rashod '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10067
        if( aop(bu,1027,5) > 0 ):
            if not( aop(bu,1026,5) == 0 ):
                lzbir =  aop(bu,1026,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 1027 kol. 5 > 0 onda je AOP 1026 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani ukupan neto poslovni prihod i rashod '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10068
        if( aop(bu,1026,6) > 0 ):
            if not( aop(bu,1027,6) == 0 ):
                lzbir =  aop(bu,1027,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 1026 kol. 6 > 0 onda je AOP 1027 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani ukupan neto poslovni prihod i rashod '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10069
        if( aop(bu,1027,6) > 0 ):
            if not( aop(bu,1026,6) == 0 ):
                lzbir =  aop(bu,1026,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1027 kol. 6 > 0 onda je AOP 1026 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani ukupan neto poslovni prihod i rashod '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10070
        if not( suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025,1027],5) == suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024,1026],5) ):
            lzbir =  suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025,1027],5) 
            dzbir =  suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024,1026],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1003 + 1007 + 1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025 + 1027) kol. 5 = AOP-u (1004 + 1008 + 1010 + 1012 + 1014 + 1016 + 1018 + 1020 + 1022 + 1024 + 1026) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10071
        if not( suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025,1027],6) == suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024,1026],6) ):
            lzbir =  suma_liste(bu,[1003,1007,1009,1011,1013,1015,1017,1019,1021,1023,1025,1027],6) 
            dzbir =  suma_liste(bu,[1004,1008,1010,1012,1014,1016,1018,1020,1022,1024,1026],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1003 + 1007 + 1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025 + 1027) kol. 6 = AOP-u (1004 + 1008 + 1010 + 1012 + 1014 + 1016 + 1018 + 1020 + 1022 + 1024 + 1026) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10072
        if( suma_liste(bu,[1026,1030],5) > suma_liste(bu,[1027,1028,1029,1031],5) ):
            if not( aop(bu,1032,5) == suma_liste(bu,[1026,1030],5)-suma_liste(bu,[1027,1028,1029,1031],5) ):
                lzbir =  aop(bu,1032,5) 
                dzbir =  suma_liste(bu,[1026,1030],5)-suma_liste(bu,[1027,1028,1029,1031],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1032 kol. 5 = AOP-u (1026 - 1027 - 1028 - 1029 + 1030 - 1031) kol. 5, ako je AOP (1026 + 1030) kol. 5 > AOP-a (1027 + 1028 + 1029 + 1031) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10073
        if( suma_liste(bu,[1026,1030],6) > suma_liste(bu,[1027,1028,1029,1031],6) ):
            if not( aop(bu,1032,6) == suma_liste(bu,[1026,1030],6)-suma_liste(bu,[1027,1028,1029,1031],6) ):
                lzbir =  aop(bu,1032,6) 
                dzbir =  suma_liste(bu,[1026,1030],6)-suma_liste(bu,[1027,1028,1029,1031],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1032 kol. 6 = AOP-u (1026 - 1027 - 1028 - 1029 + 1030 - 1031) kol. 6, ako je AOP (1026 + 1030) kol. 6 > AOP-a (1027 + 1028 + 1029 + 1031) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10074
        if( suma_liste(bu,[1026,1030],5) < suma_liste(bu,[1027,1028,1029,1031],5) ):
            if not( aop(bu,1033,5) == suma_liste(bu,[1027,1028,1029,1031],5)-suma_liste(bu,[1026,1030],5) ):
                lzbir =  aop(bu,1033,5) 
                dzbir =  suma_liste(bu,[1027,1028,1029,1031],5)-suma_liste(bu,[1026,1030],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1033 kol. 5 = AOP-u (1027 - 1026 + 1028 + 1029 - 1030 + 1031) kol. 5, ako je AOP (1026 + 1030) kol. 5 < AOP-a (1027 + 1028 + 1029 + 1031) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10075
        if( suma_liste(bu,[1026,1030],6) < suma_liste(bu,[1027,1028,1029,1031],6) ):
            if not( aop(bu,1033,6) == suma_liste(bu,[1027,1028,1029,1031],6)-suma_liste(bu,[1026,1030],6) ):
                lzbir =  aop(bu,1033,6) 
                dzbir =  suma_liste(bu,[1027,1028,1029,1031],6)-suma_liste(bu,[1026,1030],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1033 kol. 6 = AOP-u (1027 - 1026 + 1028 + 1029 - 1030 + 1031) kol. 6, ako je AOP (1026 + 1030) kol. 6 < AOP-a (1027 + 1028 + 1029 + 1031) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10076
        if( suma_liste(bu,[1026,1030],5) == suma_liste(bu,[1027,1028,1029,1031],5) ):
            if not( suma(bu,1032,1033,5) == 0 ):
                lzbir =  suma(bu,1032,1033,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1032 + 1033) kol. 5 = 0, ako je AOP (1026 + 1030) kol. 5 = AOP-u (1027 + 1028 + 1029 + 1031) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10077
        if( suma_liste(bu,[1026,1030],6) == suma_liste(bu,[1027,1028,1029,1031],6) ):
            if not( suma(bu,1032,1033,6) == 0 ):
                lzbir =  suma(bu,1032,1033,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1032 + 1033) kol. 6 = 0, ako je AOP (1026 + 1030) kol. 6 = AOP-u (1027 + 1028 + 1029 + 1031) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10078
        if( aop(bu,1032,5) > 0 ):
            if not( aop(bu,1033,5) == 0 ):
                lzbir =  aop(bu,1033,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1032 kol. 5 > 0 onda je AOP 1033 kol. 5 = 0   U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10079
        if( aop(bu,1033,5) > 0 ):
            if not( aop(bu,1032,5) == 0 ):
                lzbir =  aop(bu,1032,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1033 kol. 5 > 0 onda je AOP 1032 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10080
        if( aop(bu,1032,6) > 0 ):
            if not( aop(bu,1033,6) == 0 ):
                lzbir =  aop(bu,1033,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1032 kol. 6 > 0 onda je AOP 1033 kol. 6 = 0   U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10081
        if( aop(bu,1033,6) > 0 ):
            if not( aop(bu,1032,6) == 0 ):
                lzbir =  aop(bu,1032,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1033 kol. 6 > 0 onda je AOP 1032 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10082
        if not( suma_liste(bu,[1026,1030,1033],5) == suma_liste(bu,[1027,1028,1029,1031,1032],5) ):
            lzbir =  suma_liste(bu,[1026,1030,1033],5) 
            dzbir =  suma_liste(bu,[1027,1028,1029,1031,1032],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1026 + 1030 + 1033) kol. 5 = AOP-u (1027 + 1028 + 1029 + 1031 + 1032) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10083
        if not( suma_liste(bu,[1026,1030,1033],6) == suma_liste(bu,[1027,1028,1029,1031,1032],6) ):
            lzbir =  suma_liste(bu,[1026,1030,1033],6) 
            dzbir =  suma_liste(bu,[1027,1028,1029,1031,1032],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1026 + 1030 + 1033) kol. 6 = AOP-u (1027 + 1028 + 1029 + 1031 + 1032) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10084
        if( suma_liste(bu,[1032,1035],5) > suma_liste(bu,[1033,1034,1036],5) ):
            if not( aop(bu,1037,5) == suma_liste(bu,[1032,1035],5)-suma_liste(bu,[1033,1034,1036],5) ):
                lzbir =  aop(bu,1037,5) 
                dzbir =  suma_liste(bu,[1032,1035],5)-suma_liste(bu,[1033,1034,1036],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1037 kol. 5 = AOP-u (1032 - 1033 - 1034 + 1035 - 1036) kol. 5, ako je AOP (1032 + 1035) kol. 5 > AOP-a (1033 + 1034 + 1036) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10085
        if( suma_liste(bu,[1032,1035],6) > suma_liste(bu,[1033,1034,1036],6) ):
            if not( aop(bu,1037,6) == suma_liste(bu,[1032,1035],6)-suma_liste(bu,[1033,1034,1036],6) ):
                lzbir =  aop(bu,1037,6) 
                dzbir =  suma_liste(bu,[1032,1035],6)-suma_liste(bu,[1033,1034,1036],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1037 kol. 6 = AOP-u (1032 - 1033 - 1034 + 1035 - 1036) kol. 6, ako je AOP (1032 + 1035) kol. 6 > AOP-a (1033 + 1034 + 1036) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10086
        if( suma_liste(bu,[1032,1035],5) < suma_liste(bu,[1033,1034,1036],5) ):
            if not( aop(bu,1038,5) == suma_liste(bu,[1033,1034,1036],5)-suma_liste(bu,[1032,1035],5) ):
                lzbir =  aop(bu,1038,5) 
                dzbir =  suma_liste(bu,[1033,1034,1036],5)-suma_liste(bu,[1032,1035],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1038 kol. 5 = AOP-u (1033 - 1032 + 1034 - 1035 + 1036) kol. 5, ako je AOP (1032 + 1035) kol. 5 < AOP-a (1033 + 1034 + 1036) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10087
        if( suma_liste(bu,[1032,1035],6) < suma_liste(bu,[1033,1034,1036],6) ):
            if not( aop(bu,1038,6) == suma_liste(bu,[1033,1034,1036],6)-suma_liste(bu,[1032,1035],6) ):
                lzbir =  aop(bu,1038,6) 
                dzbir =  suma_liste(bu,[1033,1034,1036],6)-suma_liste(bu,[1032,1035],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1038 kol. 6 = AOP-u (1033 - 1032 + 1034 - 1035 + 1036) kol. 6, ako je AOP (1032 + 1035) kol. 6 < AOP-a (1033 + 1034 + 1036) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10088
        if( suma_liste(bu,[1032,1035],5) == suma_liste(bu,[1033,1034,1036],5) ):
            if not( suma(bu,1037,1038,5) == 0 ):
                lzbir =  suma(bu,1037,1038,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1037 + 1038) kol. 5 = 0, ako je AOP (1032 + 1035) kol. 5 = AOP-u (1033 + 1034 + 1036) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10089
        if( suma_liste(bu,[1032,1035],6) == suma_liste(bu,[1033,1034,1036],6) ):
            if not( suma(bu,1037,1038,6) == 0 ):
                lzbir =  suma(bu,1037,1038,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1037 + 1038) kol. 6 = 0, ako je AOP (1032 + 1035) kol. 6 = AOP-u (1033 + 1034 + 1036) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10090
        if( aop(bu,1037,5) > 0 ):
            if not( aop(bu,1038,5) == 0 ):
                lzbir =  aop(bu,1038,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1037 kol. 5 > 0 onda je AOP 1038 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10091
        if( aop(bu,1038,5) > 0 ):
            if not( aop(bu,1037,5) == 0 ):
                lzbir =  aop(bu,1037,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1038 kol. 5 > 0 onda je AOP 1037 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10092
        if( aop(bu,1037,6) > 0 ):
            if not( aop(bu,1038,6) == 0 ):
                lzbir =  aop(bu,1038,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1037 kol. 6 > 0 onda je AOP 1038 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10093
        if( aop(bu,1038,6) > 0 ):
            if not( aop(bu,1037,6) == 0 ):
                lzbir =  aop(bu,1037,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1038 kol. 6 > 0 onda je AOP 1037 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10094
        if not( suma_liste(bu,[1032,1035,1038],5) == suma_liste(bu,[1033,1034,1036,1037],5) ):
            lzbir =  suma_liste(bu,[1032,1035,1038],5) 
            dzbir =  suma_liste(bu,[1033,1034,1036,1037],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1032 + 1035 + 1038) kol. 5 = AOP-u (1033 + 1034 + 1036 + 1037) kol. 5  Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10095
        if not( suma_liste(bu,[1032,1035,1038],6) == suma_liste(bu,[1033,1034,1036,1037],6) ):
            lzbir =  suma_liste(bu,[1032,1035,1038],6) 
            dzbir =  suma_liste(bu,[1033,1034,1036,1037],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1032 + 1035 + 1038) kol. 6 = AOP-u (1033 + 1034 + 1036 + 1037) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10096
        if( aop(bu,1039,5) > 0 ):
            if not( aop(bu,1040,5) == 0 ):
                lzbir =  aop(bu,1040,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1039 kol. 5 > 0 onda je AOP 1040 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10097
        if( aop(bu,1040,5) > 0 ):
            if not( aop(bu,1039,5) == 0 ):
                lzbir =  aop(bu,1039,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1040 kol. 5 > 0 onda je AOP 1039 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10098
        if( aop(bu,1039,6) > 0 ):
            if not( aop(bu,1040,6) == 0 ):
                lzbir =  aop(bu,1040,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1039 kol. 6 > 0 onda je AOP 1040 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10099
        if( aop(bu,1040,6) > 0 ):
            if not( aop(bu,1039,6) == 0 ):
                lzbir =  aop(bu,1039,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1040 kol. 6 > 0 onda je AOP 1039 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10100
        if( suma_liste(bu,[1037,1039],5) > suma_liste(bu,[1038,1040],5) ):
            if not( aop(bu,1041,5) == suma_liste(bu,[1037,1039],5)-suma_liste(bu,[1038,1040],5) ):
                lzbir =  aop(bu,1041,5) 
                dzbir =  suma_liste(bu,[1037,1039],5)-suma_liste(bu,[1038,1040],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1041 kol. 5 = AOP-u (1037 - 1038 + 1039 - 1040) kol. 5, ako je AOP (1037 + 1039) kol. 5 > AOP-a (1038 + 1040) kol. 5   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10101
        if( suma_liste(bu,[1037,1039],6) > suma_liste(bu,[1038,1040],6) ):
            if not( aop(bu,1041,6) == suma_liste(bu,[1037,1039],6)-suma_liste(bu,[1038,1040],6) ):
                lzbir =  aop(bu,1041,6) 
                dzbir =  suma_liste(bu,[1037,1039],6)-suma_liste(bu,[1038,1040],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1041 kol. 6 = AOP-u (1037 - 1038 + 1039 - 1040) kol. 6, ako je AOP (1037 + 1039) kol. 6 > AOP-a (1038 + 1040) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10102
        if( suma_liste(bu,[1037,1039],5) < suma_liste(bu,[1038,1040],5) ):
            if not( aop(bu,1042,5) == suma_liste(bu,[1038,1040],5)-suma_liste(bu,[1037,1039],5) ):
                lzbir =  aop(bu,1042,5) 
                dzbir =  suma_liste(bu,[1038,1040],5)-suma_liste(bu,[1037,1039],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1042 kol. 5 = AOP-u (1038 - 1037 - 1039 + 1040) kol. 5, ako je AOP (1037 + 1039) kol. 5 < AOP-a (1038 + 1040) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10103
        if( suma_liste(bu,[1037,1039],6) < suma_liste(bu,[1038,1040],6) ):
            if not( aop(bu,1042,6) == suma_liste(bu,[1038,1040],6)-suma_liste(bu,[1037,1039],6) ):
                lzbir =  aop(bu,1042,6) 
                dzbir =  suma_liste(bu,[1038,1040],6)-suma_liste(bu,[1037,1039],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1042 kol. 6 = AOP-u (1038 - 1037 - 1039 + 1040) kol. 6, ako je AOP (1037 + 1039) kol. 6 < AOP-a (1038 + 1040) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10104
        if( suma_liste(bu,[1037,1039],5) == suma_liste(bu,[1038,1040],5) ):
            if not( suma(bu,1041,1042,5) == 0 ):
                lzbir =  suma(bu,1041,1042,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1041 + 1042) kol. 5 = 0, ako je AOP (1037 + 1039) kol. 5 = AOP-u (1038 + 1040) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10105
        if( suma_liste(bu,[1037,1039],6) == suma_liste(bu,[1038,1040],6) ):
            if not( suma(bu,1041,1042,6) == 0 ):
                lzbir =  suma(bu,1041,1042,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1041 + 1042) kol. 6 = 0, ako je AOP (1037 + 1039) kol. 6 = AOP-u (1038 + 1040) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10106
        if( aop(bu,1041,5) > 0 ):
            if not( aop(bu,1042,5) == 0 ):
                lzbir =  aop(bu,1042,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1041 kol. 5 > 0 onda je AOP 1042 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10107
        if( aop(bu,1042,5) > 0 ):
            if not( aop(bu,1041,5) == 0 ):
                lzbir =  aop(bu,1041,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1042 kol. 5 > 0 onda je AOP 1041 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10108
        if( aop(bu,1041,6) > 0 ):
            if not( aop(bu,1042,6) == 0 ):
                lzbir =  aop(bu,1042,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1041 kol. 6 > 0 onda je AOP 1042 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10109
        if( aop(bu,1042,6) > 0 ):
            if not( aop(bu,1041,6) == 0 ):
                lzbir =  aop(bu,1041,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1042 kol. 6 > 0 onda je AOP 1041 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10110
        if not( suma_liste(bu,[1037,1039,1042],5) == suma_liste(bu,[1038,1040,1041],5) ):
            lzbir =  suma_liste(bu,[1037,1039,1042],5) 
            dzbir =  suma_liste(bu,[1038,1040,1041],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1037 + 1039 + 1042) kol. 5 = AOP-u (1038 + 1040 + 1041) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10111
        if not( suma_liste(bu,[1037,1039,1042],6) == suma_liste(bu,[1038,1040,1041],6) ):
            lzbir =  suma_liste(bu,[1037,1039,1042],6) 
            dzbir =  suma_liste(bu,[1038,1040,1041],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1037 + 1039 + 1042) kol. 6 = AOP-u (1038 + 1040 + 1041) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10112
        #Za ovaj set se ne primenjuje pravilo 
        
        #10113
        #Za ovaj set se ne primenjuje pravilo 
        
        #10114
        #Za ovaj set se ne primenjuje pravilo 
        
        #10115
        #Za ovaj set se ne primenjuje pravilo 
        
        #10116
        if not( aop(bu,1043,5) == 0 ):
            lzbir =  aop(bu,1043,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1043 kol. 5 = 0 Dobitak koji pripada matičnom entitetu prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10117
        if not( aop(bu,1043,6) == 0 ):
            lzbir =  aop(bu,1043,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1043 kol. 6 = 0 Dobitak koji pripada matičnom entitetu prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10118
        if not( aop(bu,1044,5) == 0 ):
            lzbir =  aop(bu,1044,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1044 kol. 5 = 0 Dobitak koji pripada vlasnicima bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10119
        if not( aop(bu,1044,6) == 0 ):
            lzbir =  aop(bu,1044,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1044 kol. 6 = 0 Dobitak koji pripada vlasnicima bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10120
        if not( aop(bu,1045,5) == 0 ):
            lzbir =  aop(bu,1045,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1045 kol. 5 = 0 Gubitak koji pripada matičnom entitetu prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10121
        if not( aop(bu,1045,6) == 0 ):
            lzbir =  aop(bu,1045,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1045 kol. 6 = 0 Gubitak koji pripada matičnom entitetu prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10122
        if not( aop(bu,1046,5) == 0 ):
            lzbir =  aop(bu,1046,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1046 kol. 5 = 0 Gubitak koji pripada vlasnicima bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10123
        if not( aop(bu,1046,6) == 0 ):
            lzbir =  aop(bu,1046,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1046 kol. 6 = 0 Gubitak koji pripada vlasnicima bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10124
        if( aop(bu,1041,5) > 0 ):
            if not( aop(bs,416,5) >= aop(bu,1041,5) ):
                form_warnings.append('Ako je AOP 1041 kol. 5 > 0, onda je AOP 0416 kol. 5 bilansa stanja ≥ AOP-a 1041 kol. 5  Rezultat perioda - dobitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu dobitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. ')
        
        #10125
        if( aop(bu,1041,6) > 0 ):
            if not( aop(bs,416,6) >= aop(bu,1041,6) ):
                form_warnings.append('Ako je AOP 1041 kol. 6 > 0, onda je AOP 0416 kol. 6 bilansa stanja ≥ AOP-a 1041 kol. 6  Rezultat perioda - dobitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu iskazanog dobitka u koloni prethodna godina u obrascu Bilans stanja. ')
        
        #10126
        if( aop(bu,1042,5) > 0 ):
            if not( aop(bs,417,5) >= aop(bu,1042,5) ):
                form_warnings.append('Ako je AOP 1042 kol. 5 > 0, onda je AOP 0417 kol. 5 bilansa stanja ≥ AOP-a 1042 kol. 5  Rezultat perioda - gubitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu gubitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. ')
        
        #10127
        if( aop(bu,1042,6) > 0 ):
            if not( aop(bs,417,6) >= aop(bu,1042,6) ):
                form_warnings.append('Ako je AOP 1042 kol. 6 > 0, onda je AOP 0417 kol. 6 bilansa stanja ≥ AOP-a 1042 kol. 6  Rezultat perioda - gubitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu iskazanog gubitka u koloni prethodna godina u obrascu Bilans stanja. ')
        
        #10128
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if( suma(bu,1001,1048,5) > 0 ):
                if not( suma(bu,1001,1048,5) != suma(bu,1001,1048,6) ):
                    form_warnings.append('***Ako je zbir podataka na oznakama za AOP (1001 do 1048) kol. 5 > 0 onda je zbir podataka na oznakama za AOP (1001 do 1048) kol. 5 ≠ zbiru podataka na oznakama za AOP  (1001 do 1048) kol. 6 Zbirovi podataka u kolonama 5 i 6 bilansa uspeha su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama;  ')
        
        #IZVEŠTAJ O OSTALOM REZULTATU - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        #20001
        if not( suma(ioor,2001,2036,5) > 0 ):
            form_warnings.append('Zbir podataka na oznakama za AOP (2001 do 2036) kol. 5 > 0 Izveštaj o ostalom rezultatu, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga ')
        
        #20002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(ioor,2001,2036,6) == 0 ):
                lzbir =  suma(ioor,2001,2036,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Zbir podataka na oznakama za AOP (2001 do 2036) kol. 6 = 0 Izveštaj o ostalom rezultatu za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(ioor,2001,2036,6) > 0 ):
                form_warnings.append('Zbir podataka na oznakama za AOP (2001 do 2036) kol. 6 > 0 Izveštaj o ostalom rezultatu, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga ')
        
        #20004
        if not( aop(ioor,2001,5) == aop(bu,1041,5) ):
            lzbir =  aop(ioor,2001,5) 
            dzbir =  aop(bu,1041,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 2001 kol. 5 = AOP-u 1041 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20005
        if not( aop(ioor,2001,6) == aop(bu,1041,6) ):
            lzbir =  aop(ioor,2001,6) 
            dzbir =  aop(bu,1041,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 2001 kol. 6 = AOP-u 1041 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20006
        if not( aop(ioor,2002,5) == aop(bu,1042,5) ):
            lzbir =  aop(ioor,2002,5) 
            dzbir =  aop(bu,1042,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 2002 kol. 5 = AOP-u 1042 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20007
        if not( aop(ioor,2002,6) == aop(bu,1042,6) ):
            lzbir =  aop(ioor,2002,6) 
            dzbir =  aop(bu,1042,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 2002 kol. 6 = AOP-u 1042 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20008
        if( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2019,2021,2023,2025,2027],5) > suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2020,2022,2024,2026,2028],5) ):
            if not( aop(ioor,2029,5) == suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2019,2021,2023,2025,2027],5)-suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2020,2022,2024,2026,2028],5) ):
                lzbir =  aop(ioor,2029,5) 
                dzbir =  suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2019,2021,2023,2025,2027],5)-suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2020,2022,2024,2026,2028],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 2029 kol. 5 = AOP-u (2003 - 2004 + 2005 - 2006 + 2007 - 2008 + 2009 - 2010 + 2011 - 2012 + 2013 - 2014 + 2015 - 2016 + 2017 - 2018 + 2019 - 2020 + 2021 - 2022 + 2023 - 2024 + 2025 - 2026 + 2027 - 2028) kol. 5, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017 +2019 + 2021 + 2023 + 2025 + 2027) kol. 5 > AOP-a (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018 +2020 + 2022 + 2024 + 2026 + 2028) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20009
        if( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2019,2021,2023,2025,2027],6) > suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2020,2022,2024,2026,2028],6) ):
            if not( aop(ioor,2029,6) == suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2019,2021,2023,2025,2027],6)-suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2020,2022,2024,2026,2028],6) ):
                lzbir =  aop(ioor,2029,6) 
                dzbir =  suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2019,2021,2023,2025,2027],6)-suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2020,2022,2024,2026,2028],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 2029 kol. 6 = AOP-u (2003 - 2004 + 2005 - 2006 + 2007 - 2008 + 2009 - 2010 + 2011 - 2012 + 2013 - 2014 + 2015 - 2016 + 2017 - 2018 + 2019 - 2020 + 2021 - 2022 + 2023 - 2024 + 2025 - 2026 + 2027 - 2028) kol. 6, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017 +2019 + 2021 + 2023 + 2025 + 2027) kol. 6 > AOP-a (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018 +2020 + 2022 + 2024 + 2026 + 2028) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20010
        if( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2019,2021,2023,2025,2027],5) < suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2020,2022,2024,2026,2028],5) ):
            if not( aop(ioor,2030,5) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2020,2022,2024,2026,2028],5)-suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2019,2021,2023,2025,2027],5) ):
                lzbir =  aop(ioor,2030,5) 
                dzbir =  suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2020,2022,2024,2026,2028],5)-suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2019,2021,2023,2025,2027],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 2030 kol. 5 = AOP-u (2004 - 2003 + 2006 - 2005 + 2008 - 2007 + 2010 - 2009 + 2012 - 2011 + 2014 - 2013 + 2016 - 2015 + 2018 - 2017 + 2020 - 2019 + 2022 - 2021 + 2024 - 2023 + 2026 - 2025 + 2028 - 2027 ) kol. 5, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017 + 2019 + 2021 + 2023 + 2025 + 2027) kol. 5 < AOP-a (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018 + 2020 + 2022 + 2024 + 2026 + 2028) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20011
        if( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2019,2021,2023,2025,2027],6) < suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2020,2022,2024,2026,2028],6) ):
            if not( aop(ioor,2030,6) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2020,2022,2024,2026,2028],6)-suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2019,2021,2023,2025,2027],6) ):
                lzbir =  aop(ioor,2030,6) 
                dzbir =  suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2020,2022,2024,2026,2028],6)-suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2019,2021,2023,2025,2027],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 2030 kol. 6 = AOP-u (2004 - 2003 + 2006 - 2005 + 2008 - 2007 + 2010 - 2009 + 2012 - 2011 + 2014 - 2013 + 2016 - 2015 + 2018 - 2017 + 2020 - 2019 + 2022 - 2021 + 2024 - 2023 + 2026 - 2025 + 2028 - 2027 ) kol. 6, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017 + 2019 + 2021 + 2023 + 2025 + 2027) kol. 6 < AOP-a (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018 + 2020 + 2022 + 2024 + 2026 + 2028) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20012
        if( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2019,2021,2023,2025,2027],5) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2020,2022,2024,2026,2028],5) ):
            if not( suma(ioor,2029,2030,5) == 0 ):
                lzbir =  suma(ioor,2029,2030,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (2029 + 2030) kol. 5 = 0, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017 + 2019 + 2021 + 2023 + 2025 + 2027) kol. 5 = AOP-u (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018 + 2020 + 2022 + 2024 + 2026 + 2028) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20013
        if( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2019,2021,2023,2025,2027],6) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2020,2022,2024,2026,2028],6) ):
            if not( suma(ioor,2029,2030,6) == 0 ):
                lzbir =  suma(ioor,2029,2030,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (2029 + 2030) kol. 6 = 0, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017 + 2019 + 2021 + 2023 + 2025 + 2027) kol. 6 = AOP-u (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018 + 2020 + 2022 + 2024 + 2026 + 2028) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20014
        if( aop(ioor,2029,5) > 0 ):
            if not( aop(ioor,2030,5) == 0 ):
                lzbir =  aop(ioor,2030,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 2029 kol. 5 > 0 onda je AOP 2030 kol. 5 = 0  U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan pozitivan i negativan ostali rezultat '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20015
        if( aop(ioor,2030,5) > 0 ):
            if not( aop(ioor,2029,5) == 0 ):
                lzbir =  aop(ioor,2029,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 2030 kol. 5 > 0 onda je AOP 2029 kol. 5 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan pozitivan i negativan ostali rezultat '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20016
        if( aop(ioor,2029,6) > 0 ):
            if not( aop(ioor,2030,6) == 0 ):
                lzbir =  aop(ioor,2030,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 2029 kol. 6 > 0 onda je AOP 2030 kol. 6 = 0  U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan pozitivan i negativan ostali rezultat '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20017
        if( aop(ioor,2030,6) > 0 ):
            if not( aop(ioor,2029,6) == 0 ):
                lzbir =  aop(ioor,2029,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 2030 kol. 6 > 0 onda je AOP 2029 kol. 6 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan pozitivan i negativan ostali rezultat '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20018
        if not( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2019,2021,2023,2025,2027,2030],5) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2020,2022,2024,2026,2028,2029],5) ):
            lzbir =  suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2019,2021,2023,2025,2027,2030],5) 
            dzbir =  suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2020,2022,2024,2026,2028,2029],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017 + 2019 + 2021 + 2023 + 2025 + 2027 + 2030) kol. 5 = AOP-a (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018 + 2020 + 2022 + 2024 + 2026 + 2028 + 2029) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20019
        if not( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2019,2021,2023,2025,2027,2030],6) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2020,2022,2024,2026,2028,2029],6) ):
            lzbir =  suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2019,2021,2023,2025,2027,2030],6) 
            dzbir =  suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2020,2022,2024,2026,2028,2029],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017 + 2019 + 2021 + 2023 + 2025 + 2027 + 2030) kol. 6 = AOP-a (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018 + 2020 + 2022 + 2024 + 2026 + 2028 + 2029) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20020
        if( suma_liste(ioor,[2001,2029],5) > suma_liste(ioor,[2002,2030],5) ):
            if not( aop(ioor,2031,5) == suma_liste(ioor,[2001,2029],5)-suma_liste(ioor,[2002,2030],5) ):
                lzbir =  aop(ioor,2031,5) 
                dzbir =  suma_liste(ioor,[2001,2029],5)-suma_liste(ioor,[2002,2030],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 2031 kol. 5 = AOP-u (2001 - 2002 + 2029 - 2030) kol. 5, ako je AOP (2001 + 2029) kol. 5 > AOP-a (2002 + 2030) kol. 5   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20021
        if( suma_liste(ioor,[2001,2029],6) > suma_liste(ioor,[2002,2030],6) ):
            if not( aop(ioor,2031,6) == suma_liste(ioor,[2001,2029],6)-suma_liste(ioor,[2002,2030],6) ):
                lzbir =  aop(ioor,2031,6) 
                dzbir =  suma_liste(ioor,[2001,2029],6)-suma_liste(ioor,[2002,2030],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 2031 kol. 6 = AOP-u (2001 - 2002 + 2029 - 2030) kol. 6, ako je AOP (2001 + 2029) kol. 6 > AOP-a (2002 + 2030) kol. 6   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20022
        if( suma_liste(ioor,[2001,2029],5) < suma_liste(ioor,[2002,2030],5) ):
            if not( aop(ioor,2032,5) == suma_liste(ioor,[2002,2030],5)-suma_liste(ioor,[2001,2029],5) ):
                lzbir =  aop(ioor,2032,5) 
                dzbir =  suma_liste(ioor,[2002,2030],5)-suma_liste(ioor,[2001,2029],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 2032 kol. 5 = AOP-u (2002 - 2001 + 2030 - 2029) kol. 5, ako je AOP (2001 + 2029) kol. 5 < AOP-a (2002 + 2030) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20023
        if( suma_liste(ioor,[2001,2029],6) < suma_liste(ioor,[2002,2030],6) ):
            if not( aop(ioor,2032,6) == suma_liste(ioor,[2002,2030],6)-suma_liste(ioor,[2001,2029],6) ):
                lzbir =  aop(ioor,2032,6) 
                dzbir =  suma_liste(ioor,[2002,2030],6)-suma_liste(ioor,[2001,2029],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 2032 kol. 6 = AOP-u (2002 - 2001 + 2030 - 2029) kol. 6, ako je AOP (2001 + 2029) kol. 6 < AOP-a (2002 + 2030) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20024
        if( suma_liste(ioor,[2001,2029],5) == suma_liste(ioor,[2002,2030],5) ):
            if not( suma(ioor,2031,2032,5) == 0 ):
                lzbir =  suma(ioor,2031,2032,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (2031 + 2032) kol. 5 = 0, ako je AOP (2001 + 2029) kol. 5 = AOP-u (2002 + 2030) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20025
        if( suma_liste(ioor,[2001,2029],6) == suma_liste(ioor,[2002,2030],6) ):
            if not( suma(ioor,2031,2032,6) == 0 ):
                lzbir =  suma(ioor,2031,2032,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (2031 + 2032) kol. 6 = 0, ako je AOP (2001 + 2029) kol. 6 = AOP-u (2002 + 2030) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20026
        if( aop(ioor,2031,5) > 0 ):
            if not( aop(ioor,2032,5) == 0 ):
                lzbir =  aop(ioor,2032,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 2031 kol. 5 > 0 onda je AOP 2032 kol. 5 = 0  U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan pozitivan i negativan rezultat '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20027
        if( aop(ioor,2032,5) > 0 ):
            if not( aop(ioor,2031,5) == 0 ):
                lzbir =  aop(ioor,2031,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 2032 kol. 5 > 0 onda je  AOP 2031 kol. 5 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan pozitivan i negativan rezultat '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20028
        if( aop(ioor,2031,6) > 0 ):
            if not( aop(ioor,2032,6) == 0 ):
                lzbir =  aop(ioor,2032,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 2031 kol. 6 > 0 onda je AOP 2032 kol. 6 = 0   U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan pozitivan i negativan rezultat '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20029
        if( aop(ioor,2032,6) > 0 ):
            if not( aop(ioor,2031,6) == 0 ):
                lzbir =  aop(ioor,2031,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako jeAOP 2032 kol. 6 > 0 onda je  AOP 2031 kol. 6 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan pozitivan i negativan rezultat '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20030
        if not( suma_liste(ioor,[2001,2029,2032],5) == suma_liste(ioor,[2002,2030,2031],5) ):
            lzbir =  suma_liste(ioor,[2001,2029,2032],5) 
            dzbir =  suma_liste(ioor,[2002,2030,2031],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (2001 + 2029 + 2032) kol. 5 = AOP-u (2002 + 2030 + 2031) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20031
        if not( suma_liste(ioor,[2001,2029,2032],6) == suma_liste(ioor,[2002,2030,2031],6) ):
            lzbir =  suma_liste(ioor,[2001,2029,2032],6) 
            dzbir =  suma_liste(ioor,[2002,2030,2031],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (2001 + 2029 + 2032) kol. 6 = AOP-u (2002 + 2030 + 2031) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20032
        #Za ovaj set se ne primenjuje pravilo 
        
        #20033
        #Za ovaj set se ne primenjuje pravilo 
        
        #20034
        #Za ovaj set se ne primenjuje pravilo 
        
        #20035
        #Za ovaj set se ne primenjuje pravilo 
        
        #20036
        if not( aop(ioor,2033,5) == 0 ):
            lzbir =  aop(ioor,2033,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 2033 kol. 5 = 0 Ukupan pozitivan rezultat koji pripada matičnom entitetu prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20037
        if not( aop(ioor,2033,6) == 0 ):
            lzbir =  aop(ioor,2033,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 2033 kol. 6 = 0 Ukupan pozitivan rezultat koji pripada matičnom entitetu prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20038
        if not( aop(ioor,2034,5) == 0 ):
            lzbir =  aop(ioor,2034,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 2034 kol. 5 = 0 Ukupan pozitivan rezultat koji pripada vlasnicima bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20039
        if not( aop(ioor,2034,6) == 0 ):
            lzbir =  aop(ioor,2034,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 2034 kol. 6 = 0 Ukupan pozitivan rezultat koji pripada vlasnicima bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20040
        if not( aop(ioor,2035,5) == 0 ):
            lzbir =  aop(ioor,2035,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 2035 kol. 5 = 0 Ukupan negativan rezultat koji pripada matičnom entitetu prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20041
        if not( aop(ioor,2035,6) == 0 ):
            lzbir =  aop(ioor,2035,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 2035 kol. 6 = 0 Ukupan negativan rezultat koji pripada matičnom entitetu prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20042
        if not( aop(ioor,2036,5) == 0 ):
            lzbir =  aop(ioor,2036,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 2036 kol. 5 = 0 Ukupan negativan rezultat koji pripada vlasnicima bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #20043
        if not( aop(ioor,2036,6) == 0 ):
            lzbir =  aop(ioor,2036,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 2036 kol. 6 = 0 Ukupan negativan rezultat koji pripada vlasnicima bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #IZVEŠTAJ O TOKOVIMA GOTOVINE - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        #30001
        if not( suma(iotg,3001,3070,3) > 0 ):
            form_warnings.append('Zbir podataka na oznakama za AOP (3001 do 3070) kol. 3 > 0 Izveštaj o tokovima gotovine, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga ')
        
        #30002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(iotg,3001,3070,4) == 0 ):
                lzbir =  suma(iotg,3001,3070,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Zbir podataka na oznakama za AOP (3001 do 3070) kol. 4 = 0 Izveštaj o tokovima gotovine za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(iotg,3001,3070,4) > 0 ):
                form_warnings.append('Zbir podataka na oznakama za AOP (3001 do 3070) kol. 4 > 0 Izveštaj o tokovima gotovine, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga ')
        
        #30004
        if not( aop(iotg,3001,3) == suma(iotg,3002,3005,3) ):
            lzbir =  aop(iotg,3001,3) 
            dzbir =  suma(iotg,3002,3005,3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3001 kol. 3 = AOP-u (3002 + 3003 + 3004 + 3005) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30005
        if not( aop(iotg,3001,4) == suma(iotg,3002,3005,4) ):
            lzbir =  aop(iotg,3001,4) 
            dzbir =  suma(iotg,3002,3005,4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3001 kol. 4 = AOP-u (3002 + 3003 + 3004 + 3005) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30006
        if not( aop(iotg,3006,3) == suma(iotg,3007,3011,3) ):
            lzbir =  aop(iotg,3006,3) 
            dzbir =  suma(iotg,3007,3011,3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3006 kol. 3 = AOP-u (3007 + 3008 + 3009 + 3010 + 3011) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30007
        if not( aop(iotg,3006,4) == suma(iotg,3007,3011,4) ):
            lzbir =  aop(iotg,3006,4) 
            dzbir =  suma(iotg,3007,3011,4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3006 kol. 4 = AOP-u (3007 + 3008 + 3009 + 3010 + 3011) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30008
        if( aop(iotg,3001,3) > aop(iotg,3006,3) ):
            if not( aop(iotg,3012,3) == aop(iotg,3001,3)-aop(iotg,3006,3) ):
                lzbir =  aop(iotg,3012,3) 
                dzbir =  aop(iotg,3001,3)-aop(iotg,3006,3) 
                razlika = lzbir - dzbir
                form_errors.append(' AOP 3012 kol. 3 = AOP-u (3001 - 3006) kol. 3, ako je AOP 3001 kol. 3 > AOP-a 3006 kol. 3   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30009
        if( aop(iotg,3001,4) > aop(iotg,3006,4) ):
            if not( aop(iotg,3012,4) == aop(iotg,3001,4)-aop(iotg,3006,4) ):
                lzbir =  aop(iotg,3012,4) 
                dzbir =  aop(iotg,3001,4)-aop(iotg,3006,4) 
                razlika = lzbir - dzbir
                form_errors.append(' AOP 3012 kol. 4 = AOP-u (3001 - 3006) kol. 4, ako je AOP 3001 kol. 4 > AOP-a 3006 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30010
        if( aop(iotg,3001,3) < aop(iotg,3006,3) ):
            if not( aop(iotg,3013,3) == aop(iotg,3006,3)-aop(iotg,3001,3) ):
                lzbir =  aop(iotg,3013,3) 
                dzbir =  aop(iotg,3006,3)-aop(iotg,3001,3) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3013 kol. 3 = AOP-u (3006 - 3001) kol. 3 , ako je AOP 3001 kol. 3 < AOP-a 3006 kol. 3    '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30011
        if( aop(iotg,3001,4) < aop(iotg,3006,4) ):
            if not( aop(iotg,3013,4) == aop(iotg,3006,4)-aop(iotg,3001,4) ):
                lzbir =  aop(iotg,3013,4) 
                dzbir =  aop(iotg,3006,4)-aop(iotg,3001,4) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3013 kol. 4 = AOP-u (3006 - 3001) kol. 4 , ako je AOP 3001 kol. 4 < AOP-a 3006 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30012
        if( aop(iotg,3001,3) == aop(iotg,3006,3) ):
            if not( suma(iotg,3012,3013,3) == 0 ):
                lzbir =  suma(iotg,3012,3013,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (3012 + 3013) kol. 3 = 0, ako je AOP 3001 kol. 3 = AOP-u 3006 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30013
        if( aop(iotg,3001,4) == aop(iotg,3006,4) ):
            if not( suma(iotg,3012,3013,4) == 0 ):
                lzbir =  suma(iotg,3012,3013,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (3012 + 3013) kol. 4 = 0, ako je AOP 3001 kol. 4 = AOP-u 3006 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30014
        if( aop(iotg,3012,3) > 0 ):
            if not( aop(iotg,3013,3) == 0 ):
                lzbir =  aop(iotg,3013,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3012 kol. 3 > 0 onda je AOP 3013 kol. 3 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30015
        if( aop(iotg,3013,3) > 0 ):
            if not( aop(iotg,3012,3) == 0 ):
                lzbir =  aop(iotg,3012,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3013 kol. 3 > 0 onda je AOP 3012 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30016
        if( aop(iotg,3012,4) > 0 ):
            if not( aop(iotg,3013,4) == 0 ):
                lzbir =  aop(iotg,3013,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3012 kol. 4 > 0 onda je AOP 3013 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30017
        if( aop(iotg,3013,4) > 0 ):
            if not( aop(iotg,3012,4) == 0 ):
                lzbir =  aop(iotg,3012,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 3013 kol. 4 > 0 onda je AOP 3012 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30018
        if not( suma_liste(iotg,[3001,3013],3) == suma_liste(iotg,[3006,3012],3) ):
            lzbir =  suma_liste(iotg,[3001,3013],3) 
            dzbir =  suma_liste(iotg,[3006,3012],3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (3001 + 3013) kol. 3 = AOP-u (3006 + 3012) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30019
        if not( suma_liste(iotg,[3001,3013],4) == suma_liste(iotg,[3006,3012],4) ):
            lzbir =  suma_liste(iotg,[3001,3013],4) 
            dzbir =  suma_liste(iotg,[3006,3012],4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (3001 + 3013) kol. 4 = AOP-u (3006 + 3012) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30020
        if not( aop(iotg,3014,3) == suma(iotg,3015,3020,3) ):
            lzbir =  aop(iotg,3014,3) 
            dzbir =  suma(iotg,3015,3020,3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3014 kol. 3 = AOP-u (3015 + 3016 + 3017 + 3018 + 3019 + 3020) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30021
        if not( aop(iotg,3014,4) == suma(iotg,3015,3020,4) ):
            lzbir =  aop(iotg,3014,4) 
            dzbir =  suma(iotg,3015,3020,4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3014 kol. 4 = AOP-u (3015 + 3016 + 3017 + 3018 + 3019 + 3020) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30022
        if not( aop(iotg,3021,3) == suma(iotg,3022,3027,3) ):
            lzbir =  aop(iotg,3021,3) 
            dzbir =  suma(iotg,3022,3027,3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3021 kol. 3 = AOP-u (3022 + 3023 + 3024 + 3025 + 3026 + 3027) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30023
        if not( aop(iotg,3021,4) == suma(iotg,3022,3027,4) ):
            lzbir =  aop(iotg,3021,4) 
            dzbir =  suma(iotg,3022,3027,4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3021 kol. 4 = AOP-u (3022 + 3023 + 3024 + 3025 + 3026 + 3027) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30024
        if( suma_liste(iotg,[3012,3014],3) > suma_liste(iotg,[3013,3021],3) ):
            if not( aop(iotg,3028,3) == suma_liste(iotg,[3012,3014],3)-suma_liste(iotg,[3013,3021],3) ):
                lzbir =  aop(iotg,3028,3) 
                dzbir =  suma_liste(iotg,[3012,3014],3)-suma_liste(iotg,[3013,3021],3) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3028 kol. 3 = AOP-u (3012 - 3013 + 3014 - 3021) kol. 3, ako je AOP (3012 + 3014) kol. 3 > AOP-a (3013 + 3021) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30025
        if( suma_liste(iotg,[3012,3014],4) > suma_liste(iotg,[3013,3021],4) ):
            if not( aop(iotg,3028,4) == suma_liste(iotg,[3012,3014],4)-suma_liste(iotg,[3013,3021],4) ):
                lzbir =  aop(iotg,3028,4) 
                dzbir =  suma_liste(iotg,[3012,3014],4)-suma_liste(iotg,[3013,3021],4) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3028 kol. 4 = AOP-u (3012 - 3013 + 3014 - 3021) kol. 4, ako je AOP (3012 + 3014) kol. 4 > AOP-a (3013 + 3021) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30026
        if( suma_liste(iotg,[3012,3014],3) < suma_liste(iotg,[3013,3021],3) ):
            if not( aop(iotg,3029,3) == suma_liste(iotg,[3013,3021],3)-suma_liste(iotg,[3012,3014],3) ):
                lzbir =  aop(iotg,3029,3) 
                dzbir =  suma_liste(iotg,[3013,3021],3)-suma_liste(iotg,[3012,3014],3) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3029 kol. 3 = AOP-u (3013 - 3012 - 3014 + 3021) kol. 3, ako je AOP (3012 + 3014) kol. 3 < AOP-a (3013 + 3021) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30027
        if( suma_liste(iotg,[3012,3014],4) < suma_liste(iotg,[3013,3021],4) ):
            if not( aop(iotg,3029,4) == suma_liste(iotg,[3013,3021],4)-suma_liste(iotg,[3012,3014],4) ):
                lzbir =  aop(iotg,3029,4) 
                dzbir =  suma_liste(iotg,[3013,3021],4)-suma_liste(iotg,[3012,3014],4) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3029 kol. 4 = AOP-u (3013 - 3012 - 3014 + 3021) kol. 4, ako je AOP (3012 + 3014) kol. 4 < AOP-a (3013 + 3021) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30028
        if( suma_liste(iotg,[3012,3014],3) == suma_liste(iotg,[3013,3021],3) ):
            if not( suma(iotg,3028,3029,3) == 0 ):
                lzbir =  suma(iotg,3028,3029,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (3028 + 3029) kol. 3 = 0, ako je AOP (3012 + 3014) kol. 3 = AOP-u (3013 + 3021) kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30029
        if( suma_liste(iotg,[3012,3014],4) == suma_liste(iotg,[3013,3021],4) ):
            if not( suma(iotg,3028,3029,4) == 0 ):
                lzbir =  suma(iotg,3028,3029,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (3028 + 3029) kol. 4 = 0, ako je AOP (3012 + 3014) kol. 4 = AOP-u (3013 + 3021) kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30030
        if( aop(iotg,3028,3) > 0 ):
            if not( aop(iotg,3029,3) == 0 ):
                lzbir =  aop(iotg,3029,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3028 kol. 3 > 0 onda je AOP 3029 kol. 3 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30031
        if( aop(iotg,3029,3) > 0 ):
            if not( aop(iotg,3028,3) == 0 ):
                lzbir =  aop(iotg,3028,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3029 kol. 3 > 0 onda je AOP 3028 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30032
        if( aop(iotg,3028,4) > 0 ):
            if not( aop(iotg,3029,4) == 0 ):
                lzbir =  aop(iotg,3029,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3028 kol. 4 > 0 onda je AOP 3029 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30033
        if( aop(iotg,3029,4) > 0 ):
            if not( aop(iotg,3028,4) == 0 ):
                lzbir =  aop(iotg,3028,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 3029 kol. 4 > 0 onda je AOP 3028 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30034
        if not( suma_liste(iotg,[3012,3014,3029],3) == suma_liste(iotg,[3013,3021,3028],3) ):
            lzbir =  suma_liste(iotg,[3012,3014,3029],3) 
            dzbir =  suma_liste(iotg,[3013,3021,3028],3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (3012 + 3014 + 3029) kol. 3 = AOP-u (3013 + 3021 + 3028) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30035
        if not( suma_liste(iotg,[3012,3014,3029],4) == suma_liste(iotg,[3013,3021,3028],4) ):
            lzbir =  suma_liste(iotg,[3012,3014,3029],4) 
            dzbir =  suma_liste(iotg,[3013,3021,3028],4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (3012 + 3014 + 3029) kol. 4 = AOP-u (3013 + 3021 + 3028) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30036
        if( aop(iotg,3028,3) > suma(iotg,3029,3031,3) ):
            if not( aop(iotg,3032,3) == aop(iotg,3028,3)-suma(iotg,3029,3031,3) ):
                lzbir =  aop(iotg,3032,3) 
                dzbir =  aop(iotg,3028,3)-suma(iotg,3029,3031,3) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3032 kol. 3 = AOP-u (3028 - 3029 - 3030 - 3031) kol. 3, ako je AOP 3028 kol. 3 > AOP-a (3029 + 3030 + 3031) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30037
        if( aop(iotg,3028,4) > suma(iotg,3029,3031,4) ):
            if not( aop(iotg,3032,4) == aop(iotg,3028,4)-suma(iotg,3029,3031,4) ):
                lzbir =  aop(iotg,3032,4) 
                dzbir =  aop(iotg,3028,4)-suma(iotg,3029,3031,4) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3032 kol. 4 = AOP-u (3028 - 3029 - 3030 - 3031) kol. 4, ako je AOP 3028 kol. 4 > AOP-a (3029 + 3030 + 3031) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30038
        if( aop(iotg,3028,3) < suma(iotg,3029,3031,3) ):
            if not( aop(iotg,3033,3) == suma(iotg,3029,3031,3)-aop(iotg,3028,3) ):
                lzbir =  aop(iotg,3033,3) 
                dzbir =  suma(iotg,3029,3031,3)-aop(iotg,3028,3) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3033 kol. 3 = AOP-u (3029 - 3028 + 3030 + 3031) kol. 3, ako je AOP 3028 kol. 3 < AOP-a (3029 + 3030 + 3031) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30039
        if( aop(iotg,3028,4) < suma(iotg,3029,3031,4) ):
            if not( aop(iotg,3033,4) == suma(iotg,3029,3031,4)-aop(iotg,3028,4) ):
                lzbir =  aop(iotg,3033,4) 
                dzbir =  suma(iotg,3029,3031,4)-aop(iotg,3028,4) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3033 kol. 4 = AOP-u (3029 - 3028 + 3030 + 3031) kol. 4, ako je AOP 3028 kol. 4 < AOP-a (3029 + 3030 + 3031) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30040
        if( aop(iotg,3028,3) == suma(iotg,3029,3031,3) ):
            if not( suma(iotg,3032,3033,3) == 0 ):
                lzbir =  suma(iotg,3032,3033,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (3032 + 3033) kol. 3 = 0, ako je AOP 3028 kol. 3 = AOP-u (3029 + 3030 + 3031) kol. 3  Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30041
        if( aop(iotg,3028,4) == suma(iotg,3029,3031,4) ):
            if not( suma(iotg,3032,3033,4) == 0 ):
                lzbir =  suma(iotg,3032,3033,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (3032 + 3033) kol. 4 = 0, ako je AOP 3028 kol. 4 = AOP-u (3029 + 3030 + 3031) kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30042
        if( aop(iotg,3032,3) > 0 ):
            if not( aop(iotg,3033,3) == 0 ):
                lzbir =  aop(iotg,3033,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3032 kol. 3 > 0 onda je AOP 3033 kol. 3 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30043
        if( aop(iotg,3033,3) > 0 ):
            if not( aop(iotg,3032,3) == 0 ):
                lzbir =  aop(iotg,3032,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3033 kol. 3 > 0 onda je AOP 3032 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30044
        if( aop(iotg,3032,4) > 0 ):
            if not( aop(iotg,3033,4) == 0 ):
                lzbir =  aop(iotg,3033,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3032 kol. 4 > 0 onda je AOP 3033 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30045
        if( aop(iotg,3033,4) > 0 ):
            if not( aop(iotg,3032,4) == 0 ):
                lzbir =  aop(iotg,3032,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3033 kol. 4 > 0 onda je AOP 3032 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30046
        if not( suma_liste(iotg,[3028,3033],3) == suma(iotg,3029,3032,3) ):
            lzbir =  suma_liste(iotg,[3028,3033],3) 
            dzbir =  suma(iotg,3029,3032,3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (3028 + 3033) kol. 3 = AOP-u (3029 + 3030 + 3031 + 3032) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30047
        if not( suma_liste(iotg,[3028,3033],4) == suma(iotg,3029,3032,4) ):
            lzbir =  suma_liste(iotg,[3028,3033],4) 
            dzbir =  suma(iotg,3029,3032,4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (3028 + 3033) kol. 4 = AOP-u (3029 + 3030 + 3031 + 3032) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30048
        if not( aop(iotg,3034,3) == suma(iotg,3035,3039,3) ):
            lzbir =  aop(iotg,3034,3) 
            dzbir =  suma(iotg,3035,3039,3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3034 kol. 3 = AOP-u (3035 + 3036 + 3037 + 3038 + 3039) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30049
        if not( aop(iotg,3034,4) == suma(iotg,3035,3039,4) ):
            lzbir =  aop(iotg,3034,4) 
            dzbir =  suma(iotg,3035,3039,4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3034 kol. 4 = AOP-u (3035 + 3036 + 3037 + 3038 + 3039) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30050
        if not( aop(iotg,3040,3) == suma(iotg,3041,3045,3) ):
            lzbir =  aop(iotg,3040,3) 
            dzbir =  suma(iotg,3041,3045,3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3040 kol. 3 = AOP-u (3041 + 3042 + 3043 + 3044 + 3045) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30051
        if not( aop(iotg,3040,4) == suma(iotg,3041,3045,4) ):
            lzbir =  aop(iotg,3040,4) 
            dzbir =  suma(iotg,3041,3045,4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3040 kol. 4 = AOP-u (3041 + 3042 + 3043 + 3044 + 3045) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30052
        if( aop(iotg,3034,3) > aop(iotg,3040,3) ):
            if not( aop(iotg,3046,3) == aop(iotg,3034,3)-aop(iotg,3040,3) ):
                lzbir =  aop(iotg,3046,3) 
                dzbir =  aop(iotg,3034,3)-aop(iotg,3040,3) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3046 kol. 3 = AOP-u (3034 - 3040) kol. 3, ako je AOP 3034 kol. 3 > AOP-a 3040 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30053
        if( aop(iotg,3034,4) > aop(iotg,3040,4) ):
            if not( aop(iotg,3046,4) == aop(iotg,3034,4)-aop(iotg,3040,4) ):
                lzbir =  aop(iotg,3046,4) 
                dzbir =  aop(iotg,3034,4)-aop(iotg,3040,4) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3046 kol. 4 = AOP-u (3034 - 3040) kol. 4, ako je AOP 3034 kol. 4 > AOP-a 3040 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30054
        if( aop(iotg,3034,3) < aop(iotg,3040,3) ):
            if not( aop(iotg,3047,3) == aop(iotg,3040,3)-aop(iotg,3034,3) ):
                lzbir =  aop(iotg,3047,3) 
                dzbir =  aop(iotg,3040,3)-aop(iotg,3034,3) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3047 kol. 3 = AOP-u (3040 - 3034) kol. 3, ako je AOP 3034 kol. 3 < AOP-a 3040 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30055
        if( aop(iotg,3034,4) < aop(iotg,3040,4) ):
            if not( aop(iotg,3047,4) == aop(iotg,3040,4)-aop(iotg,3034,4) ):
                lzbir =  aop(iotg,3047,4) 
                dzbir =  aop(iotg,3040,4)-aop(iotg,3034,4) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3047 kol. 4 = AOP-u (3040 - 3034) kol. 4, ako je AOP 3034 kol. 4 < AOP-a 3040 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30056
        if( aop(iotg,3034,3) == aop(iotg,3040,3) ):
            if not( suma(iotg,3046,3047,3) == 0 ):
                lzbir =  suma(iotg,3046,3047,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (3046 + 3047) kol. 3 = 0, ako je AOP 3034 kol. 3 = AOP-u 3040 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30057
        if( aop(iotg,3034,4) == aop(iotg,3040,4) ):
            if not( suma(iotg,3046,3047,4) == 0 ):
                lzbir =  suma(iotg,3046,3047,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (3046 + 3047) kol. 4 = 0, ako je AOP 3034 kol. 4 = AOP-u 3040 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30058
        if( aop(iotg,3046,3) > 0 ):
            if not( aop(iotg,3047,3) == 0 ):
                lzbir =  aop(iotg,3047,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3046 kol. 3 > 0 onda je AOP 3047 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30059
        if( aop(iotg,3047,3) > 0 ):
            if not( aop(iotg,3046,3) == 0 ):
                lzbir =  aop(iotg,3046,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3047 kol. 3 > 0 onda je AOP 3046 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30060
        if( aop(iotg,3046,4) > 0 ):
            if not( aop(iotg,3047,4) == 0 ):
                lzbir =  aop(iotg,3047,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3046 kol. 4 > 0 onda je AOP 3047 kol. 4 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30061
        if( aop(iotg,3047,4) > 0 ):
            if not( aop(iotg,3046,4) == 0 ):
                lzbir =  aop(iotg,3046,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3047 kol. 4 > 0 onda je AOP 3046 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30062
        if not( suma_liste(iotg,[3034,3047],3) == suma_liste(iotg,[3040,3046],3) ):
            lzbir =  suma_liste(iotg,[3034,3047],3) 
            dzbir =  suma_liste(iotg,[3040,3046],3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (3034 + 3047) kol. 3  = AOP-u (3040 + 3046) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30063
        if not( suma_liste(iotg,[3034,3047],4) == suma_liste(iotg,[3040,3046],4) ):
            lzbir =  suma_liste(iotg,[3034,3047],4) 
            dzbir =  suma_liste(iotg,[3040,3046],4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (3034 + 3047) kol. 4  = AOP-u (3040 + 3046) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30064
        if not( aop(iotg,3048,3) == suma(iotg,3049,3054,3) ):
            lzbir =  aop(iotg,3048,3) 
            dzbir =  suma(iotg,3049,3054,3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3048 kol. 3 = AOP-u (3049 + 3050 + 3051 + 3052 + 3053 + 3054) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30065
        if not( aop(iotg,3048,4) == suma(iotg,3049,3054,4) ):
            lzbir =  aop(iotg,3048,4) 
            dzbir =  suma(iotg,3049,3054,4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3048 kol. 4 = AOP-u (3049 + 3050 + 3051 + 3052 + 3053 + 3054) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30066
        if not( aop(iotg,3055,3) == suma(iotg,3056,3060,3) ):
            lzbir =  aop(iotg,3055,3) 
            dzbir =  suma(iotg,3056,3060,3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3055 kol. 3 = AOP-u (3056 + 3057 + 3058 + 3059 + 3060) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30067
        if not( aop(iotg,3055,4) == suma(iotg,3056,3060,4) ):
            lzbir =  aop(iotg,3055,4) 
            dzbir =  suma(iotg,3056,3060,4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3055 kol. 4 = AOP-u (3056 + 3057 + 3058 + 3059 + 3060) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30068
        if( aop(iotg,3048,3) > aop(iotg,3055,3) ):
            if not( aop(iotg,3061,3) == aop(iotg,3048,3)-aop(iotg,3055,3) ):
                lzbir =  aop(iotg,3061,3) 
                dzbir =  aop(iotg,3048,3)-aop(iotg,3055,3) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3061 kol. 3 = AOP-u (3048 - 3055) kol. 3, ako je 3048 kol. 3 > AOP-a 3055 kol. 3   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30069
        if( aop(iotg,3048,4) > aop(iotg,3055,4) ):
            if not( aop(iotg,3061,4) == aop(iotg,3048,4)-aop(iotg,3055,4) ):
                lzbir =  aop(iotg,3061,4) 
                dzbir =  aop(iotg,3048,4)-aop(iotg,3055,4) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3061 kol. 4 = AOP-u (3048 - 3055) kol. 4, ako je 3048 kol. 4 > AOP-a 3055 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30070
        if( aop(iotg,3048,3) < aop(iotg,3055,3) ):
            if not( aop(iotg,3062,3) == aop(iotg,3055,3)-aop(iotg,3048,3) ):
                lzbir =  aop(iotg,3062,3) 
                dzbir =  aop(iotg,3055,3)-aop(iotg,3048,3) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3062 kol. 3 = AOP-u (3055 - 3048) kol. 3, ako je 3048 kol. 3 < AOP-a 3055 kol. 3   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30071
        if( aop(iotg,3048,4) < aop(iotg,3055,4) ):
            if not( aop(iotg,3062,4) == aop(iotg,3055,4)-aop(iotg,3048,4) ):
                lzbir =  aop(iotg,3062,4) 
                dzbir =  aop(iotg,3055,4)-aop(iotg,3048,4) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3062 kol. 4 = AOP-u (3055 - 3048) kol. 4, ako je 3048 kol. 4 <  AOP-a 3055 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30072
        if( aop(iotg,3048,3) == aop(iotg,3055,3) ):
            if not( suma(iotg,3061,3062,3) == 0 ):
                lzbir =  suma(iotg,3061,3062,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (3061 + 3062) kol. 3 = 0, ako je AOP 3048 kol. 3 = AOP-u 3055 kol. 3  Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30073
        if( aop(iotg,3048,4) == aop(iotg,3055,4) ):
            if not( suma(iotg,3061,3062,4) == 0 ):
                lzbir =  suma(iotg,3061,3062,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (3061 + 3062) kol. 4 = 0, ako je AOP 3048 kol. 4 = AOP-u 3055 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30074
        if( aop(iotg,3061,3) > 0 ):
            if not( aop(iotg,3062,3) == 0 ):
                lzbir =  aop(iotg,3062,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3061 kol. 3 > 0 onda je AOP 3062 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30075
        if( aop(iotg,3062,3) > 0 ):
            if not( aop(iotg,3061,3) == 0 ):
                lzbir =  aop(iotg,3061,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 3062 kol. 3 > 0 onda je AOP 3061 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30076
        if( aop(iotg,3061,4) > 0 ):
            if not( aop(iotg,3062,4) == 0 ):
                lzbir =  aop(iotg,3062,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3061 kol. 4 > 0 onda je AOP 3062 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30077
        if( aop(iotg,3062,4) > 0 ):
            if not( aop(iotg,3061,4) == 0 ):
                lzbir =  aop(iotg,3061,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3062 kol. 4 > 0 onda je AOP 3061 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30078
        if not( suma_liste(iotg,[3048,3062],3) == suma_liste(iotg,[3055,3061],3) ):
            lzbir =  suma_liste(iotg,[3048,3062],3) 
            dzbir =  suma_liste(iotg,[3055,3061],3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (3048 + 3062) kol. 3 = AOP-u (3055 + 3061) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30079
        if not( suma_liste(iotg,[3048,3062],4) == suma_liste(iotg,[3055,3061],4) ):
            lzbir =  suma_liste(iotg,[3048,3062],4) 
            dzbir =  suma_liste(iotg,[3055,3061],4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (3048 + 3062) kol. 4 = AOP-u (3055 + 3061) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30080
        if not( aop(iotg,3063,3) == suma_liste(iotg,[3001,3014,3034,3048],3) ):
            lzbir =  aop(iotg,3063,3) 
            dzbir =  suma_liste(iotg,[3001,3014,3034,3048],3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3063 kol. 3 = AOP-u (3001 + 3014 + 3034 + 3048) kol. 3   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30081
        if not( aop(iotg,3063,4) == suma_liste(iotg,[3001,3014,3034,3048],4) ):
            lzbir =  aop(iotg,3063,4) 
            dzbir =  suma_liste(iotg,[3001,3014,3034,3048],4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3063 kol. 4 = AOP-u (3001 + 3014 + 3034 + 3048) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30082
        if not( aop(iotg,3064,3) == suma_liste(iotg,[3006,3021,3030,3031,3040,3055],3) ):
            lzbir =  aop(iotg,3064,3) 
            dzbir =  suma_liste(iotg,[3006,3021,3030,3031,3040,3055],3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3064 kol. 3 = AOP-u (3006 + 3021 + 3030 + 3031 + 3040 + 3055) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30083
        if not( aop(iotg,3064,4) == suma_liste(iotg,[3006,3021,3030,3031,3040,3055],4) ):
            lzbir =  aop(iotg,3064,4) 
            dzbir =  suma_liste(iotg,[3006,3021,3030,3031,3040,3055],4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3064 kol. 4 = AOP-u (3006 + 3021 + 3030 + 3031 + 3040 + 3055) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30084
        if( aop(iotg,3063,3) > aop(iotg,3064,3) ):
            if not( aop(iotg,3065,3) == aop(iotg,3063,3)-aop(iotg,3064,3) ):
                lzbir =  aop(iotg,3065,3) 
                dzbir =  aop(iotg,3063,3)-aop(iotg,3064,3) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3065 kol. 3 = AOP-u (3063 - 3064) kol. 3, ako je AOP 3063 kol. 3 > AOP-a 3064 kol. 3   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30085
        if( aop(iotg,3063,4) > aop(iotg,3064,4) ):
            if not( aop(iotg,3065,4) == aop(iotg,3063,4)-aop(iotg,3064,4) ):
                lzbir =  aop(iotg,3065,4) 
                dzbir =  aop(iotg,3063,4)-aop(iotg,3064,4) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3065 kol. 4 = AOP-u (3063 - 3064) kol. 4, ako je AOP 3063 kol. 4 > AOP-a 3064 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30086
        if( aop(iotg,3063,3) < aop(iotg,3064,3) ):
            if not( aop(iotg,3066,3) == aop(iotg,3064,3)-aop(iotg,3063,3) ):
                lzbir =  aop(iotg,3066,3) 
                dzbir =  aop(iotg,3064,3)-aop(iotg,3063,3) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3066 kol. 3 = AOP-u (3064 - 3063) kol. 3, ako je AOP 3063 kol. 3 < AOP-a 3064 kol. 3   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30087
        if( aop(iotg,3063,4) < aop(iotg,3064,4) ):
            if not( aop(iotg,3066,4) == aop(iotg,3064,4)-aop(iotg,3063,4) ):
                lzbir =  aop(iotg,3066,4) 
                dzbir =  aop(iotg,3064,4)-aop(iotg,3063,4) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3066 kol. 4 = AOP-u (3064 - 3063) kol. 4, ako je AOP 3063 kol. 4 < AOP-a 3064 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30088
        if( aop(iotg,3063,3) == aop(iotg,3064,3) ):
            if not( suma(iotg,3065,3066,3) == 0 ):
                lzbir =  suma(iotg,3065,3066,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (3065 + 3066) kol. 3 = 0, ako je AOP 3063 kol. 3 = AOP-u 3064 kol. 3  Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30089
        if( aop(iotg,3063,4) == aop(iotg,3064,4) ):
            if not( suma(iotg,3065,3066,4) == 0 ):
                lzbir =  suma(iotg,3065,3066,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (3065 + 3066) kol. 4 = 0, ako je AOP 3063 kol. 4 = AOP-u 3064 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30090
        if( aop(iotg,3065,3) > 0 ):
            if not( aop(iotg,3066,3) == 0 ):
                lzbir =  aop(iotg,3066,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3065 kol. 3 > 0 onda je AOP 3066 kol. 3 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto povećanje i smanjenje gotovine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30091
        if( aop(iotg,3066,3) > 0 ):
            if not( aop(iotg,3065,3) == 0 ):
                lzbir =  aop(iotg,3065,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 3066 kol. 3 > 0 onda je AOP 3065 kol. 3 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto povećanje i smanjenje gotovine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30092
        if( aop(iotg,3065,4) > 0 ):
            if not( aop(iotg,3066,4) == 0 ):
                lzbir =  aop(iotg,3066,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3065 kol. 4 > 0 onda je AOP 3066 kol. 4 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto povećanje i smanjenje gotovine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30093
        if( aop(iotg,3066,4) > 0 ):
            if not( aop(iotg,3065,4) == 0 ):
                lzbir =  aop(iotg,3065,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 3066 kol. 4 > 0 onda je AOP 3065 kol. 4 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto povećanje i smanjenje gotovine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30094
        if not( suma_liste(iotg,[3063,3066],3) == suma(iotg,3064,3065,3) ):
            lzbir =  suma_liste(iotg,[3063,3066],3) 
            dzbir =  suma(iotg,3064,3065,3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (3063 + 3066) kol. 3 = AOP-u (3064 + 3065) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30095
        if not( suma_liste(iotg,[3063,3066],4) == suma(iotg,3064,3065,4) ):
            lzbir =  suma_liste(iotg,[3063,3066],4) 
            dzbir =  suma(iotg,3064,3065,4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (3063 + 3066) kol. 4 = AOP-u (3064 + 3065) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30096
        if not( suma_liste(iotg,[3001,3014,3034,3048,3066],3) == suma_liste(iotg,[3006,3021,3030,3031,3040,3055,3065],3) ):
            lzbir =  suma_liste(iotg,[3001,3014,3034,3048,3066],3) 
            dzbir =  suma_liste(iotg,[3006,3021,3030,3031,3040,3055,3065],3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (3001 + 3014 + 3034 + 3048 + 3066) kol. 3 = AOP-u (3006 + 3021 + 3030 + 3031 + 3040 + 3055 + 3065) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30097
        if not( suma_liste(iotg,[3001,3014,3034,3048,3066],4) == suma_liste(iotg,[3006,3021,3030,3031,3040,3055,3065],4) ):
            lzbir =  suma_liste(iotg,[3001,3014,3034,3048,3066],4) 
            dzbir =  suma_liste(iotg,[3006,3021,3030,3031,3040,3055,3065],4) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (3001 + 3014 + 3034 + 3048 + 3066) kol. 4 = AOP-u (3006 + 3021 + 3030 + 3031 + 3040 + 3055 + 3065) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30098
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( aop(iotg,3067,3) == 0 ):
                lzbir =  aop(iotg,3067,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3067 kol. 3 = 0 Novoosnovana pravna lica ne smeju imati prikazan podatak za prethodnu godinu '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30099
        #Za ovaj set se ne primenjuje pravilo 
        
        #30100
        if( suma_liste(iotg,[3065,3067,3068],3) > suma_liste(iotg,[3066,3069],3) ):
            if not( aop(iotg,3070,3) == suma_liste(iotg,[3065,3067,3068],3)-suma_liste(iotg,[3066,3069],3) ):
                lzbir =  aop(iotg,3070,3) 
                dzbir =  suma_liste(iotg,[3065,3067,3068],3)-suma_liste(iotg,[3066,3069],3) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3070 kol. 3 = AOP-u (3065 - 3066 + 3067 + 3068 - 3069) kol. 3, ako je AOP (3065 + 3067 + 3068) kol. 3 > AOP-a ( 3066 + 3069) kol. 3   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30101
        if( suma_liste(iotg,[3065,3067,3068],4) > suma_liste(iotg,[3066,3069],4) ):
            if not( aop(iotg,3070,4) == suma_liste(iotg,[3065,3067,3068],4)-suma_liste(iotg,[3066,3069],4) ):
                lzbir =  aop(iotg,3070,4) 
                dzbir =  suma_liste(iotg,[3065,3067,3068],4)-suma_liste(iotg,[3066,3069],4) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3070 kol. 4 = AOP-u (3065 - 3066 + 3067 + 3068 - 3069) kol. 4, ako je AOP (3065 + 3067 + 3068) kol. 4 > AOP-a ( 3066 + 3069) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30102
        if( suma_liste(iotg,[3065,3067,3068],3) <= suma_liste(iotg,[3066,3069],3) ):
            if not( aop(iotg,3070,3) == 0 ):
                lzbir =  aop(iotg,3070,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3070 kol. 3 = 0, ako je AOP (3065 + 3067 + 3068) kol. 3 ≤  AOP-a (3066 + 3069) kol. 3   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30103
        if( suma_liste(iotg,[3065,3067,3068],4) <= suma_liste(iotg,[3066,3069],4) ):
            if not( aop(iotg,3070,4) == 0 ):
                lzbir =  aop(iotg,3070,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP 3070 kol. 4 = 0, ako je AOP (3065 + 3067 + 3068) kol. 4 ≤  AOP-a (3066 + 3069) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30104
        if not( aop(iotg,3070,4) == aop(iotg,3067,3) ):
            lzbir =  aop(iotg,3070,4) 
            dzbir =  aop(iotg,3067,3) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 3070 kol. 4 = AOP-u 3067 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #30105
        #Za ovaj set se ne primenjuje pravilo 
        
        #IZVEŠTAJ O PROMENAMA NA KAPITALU - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #40001 
        if not( suma(iopk,4023,4032,1) + suma(iopk,4055,4064,1) + suma(iopk,4087,4096,1) + suma(iopk,4119,4128,1) + suma(iopk,4144,4146,1) + suma(iopk,4162,4164,1) + suma(iopk,4190,4202,1) + suma(iopk,4228,4240,1) + suma_liste(iopk,[4269,4284],1)+aop(iopk, 4290, 1)+aop(iopk, 4296, 1) > 0 ):
            form_warnings.append("    Zbir podataka na oznakama za AOP (4023 do 4032) + (4055 do 4064) + (4087 do 4096) + (4119 do 4128) + (4144 do 4146) + (4162 do 4164) + (4190 do 4202) + (4228 do 4240)  + (4269 do 4284) + 4290 + 4296 > 0    Izveštaj o promenama na kapitalu, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga"    )

        #40002 
        if(Zahtev.ObveznikInfo.Novoosnovan == True):
            if not( suma(iopk,4001,4022,1) + suma(iopk,4033,4054,1) + suma(iopk,4065,4086,1) + suma(iopk,4097,4118,1) + suma(iopk,4129,4143,1) + suma(iopk,4147,4161,1) + suma(iopk,4165,4189,1) + suma(iopk,4203,4227,1) + suma(iopk,4241,4268,1) + suma(iopk,4285,4289,1)+ suma(iopk, 4291, 4295, 1) == 0 ):
                #AOPi
                lzbir =  suma(iopk,4001,4022,1) + suma(iopk,4033,4054,1) + suma(iopk,4065,4086,1) + suma(iopk,4097,4118,1) + suma(iopk,4129,4143,1) + suma(iopk,4147,4161,1) + suma(iopk,4165,4189,1) + suma(iopk,4203,4227,1) + suma(iopk,4241,4268,1) + suma(iopk,4285,4289,1)+ suma(iopk, 4291, 4295, 1)
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append("    Zbir podataka na oznakama za AOP (4001 do 4022) + (4033 do 4054) + (4065 do 4086) + (4097 do 4118) + (4129 do 4143) + (4147 do 4161) + (4165 do 4189) + (4203 do 4227) + (4241 do 4268) + (4285 do 4289) + (4291 do 4295) = 0    Izveštaj o promenama na kapitalu za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period;    "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40003
        #Za ovaj set se ne primenjuje pravilo 
        
        #40004
        if(Zahtev.ObveznikInfo.Novoosnovan == False):
            if not( suma(iopk,4001,4022,1) + suma(iopk,4033,4054,1) + suma(iopk,4065,4086,1) + suma(iopk,4097,4118,1) + suma(iopk,4129,4143,1) + suma(iopk,4147,4161,1) + suma(iopk,4165,4189,1) + suma(iopk,4203,4227,1) + suma(iopk,4241,4268,1) + suma(iopk,4285,4289,1)+ suma(iopk, 4291, 4295, 1) > 0 ):
                form_warnings.append('Zbir podataka na oznakama za AOP (4001 do 4022) + (4033 do 4054) + (4065 do 4086) + (4097 do 4118) + (4129 do 4143) + (4147 do 4161) + (4165 do 4189) + (4203 do 4227) + (4241 do 4268) + (4285 do 4289) + (4291 do 4295)  > 0 Izveštaj o promenama na kapitalu, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga ')
        
        #40005
        if not( aop(iopk,4006,1) == (suma_liste(iopk,[4001,4002,4004],1) - suma_liste(iopk,[4003,4005],1)) ):
            #AOPi
            lzbir =  aop(iopk,4006,1) 
            dzbir =  (suma_liste(iopk,[4001,4002,4004],1) - suma_liste(iopk,[4003,4005],1)) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4006 = AOP-u (4001 + 4002 - 4003 + 4004 - 4005)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40006
        if not( aop(iopk,4038,1) == (suma_liste(iopk,[4033,4034, 4036],1) - suma_liste(iopk, [4035, 4037], 1)) ):
            #AOPi
            lzbir =  aop(iopk,4038,1) 
            dzbir =  (suma_liste(iopk,[4033,4034, 4036],1) - suma_liste(iopk, [4035, 4037], 1)) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4038 = AOP-u (4033 + 4034 - 4035 + 4036 - 4037)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40007
        if not( aop(iopk,4070,1) == (suma_liste(iopk,[4065,4066, 4068],1) - suma_liste(iopk, [4067, 4069], 1)) ):
            #AOPi
            lzbir =  aop(iopk,4070,1) 
            dzbir =  (suma_liste(iopk,[4065,4066, 4068],1) - suma_liste(iopk, [4067, 4069], 1)) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4070 = AOP-u (4065 + 4066 - 4067 + 4068 - 4069)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40008
        if not( aop(iopk,4102,1) == (suma_liste(iopk,[4097,4098, 4100],1) - suma_liste(iopk, [4099, 4101], 1)) ):
            #AOPi
            lzbir =  aop(iopk,4102,1) 
            dzbir =  (suma_liste(iopk,[4097,4098, 4100],1) - suma_liste(iopk, [4099, 4101], 1)) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4102 = AOP-u (4097 + 4098 - 4099 + 4100 - 4101)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40009
        if not( aop(iopk,4134,1) == (suma_liste(iopk,[4129,4130, 4132],1) - suma_liste(iopk, [4131, 4133], 1)) ):
            #AOPi
            lzbir =  aop(iopk,4134,1) 
            dzbir =  (suma_liste(iopk,[4129,4130, 4132],1) - suma_liste(iopk, [4131, 4133], 1)) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4134 = AOP-u (4129 + 4130 - 4131 + 4132 - 4133)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40010
        if not( aop(iopk,4152,1) == (suma_liste(iopk,[4147,4148, 4150],1) - suma_liste(iopk, [4149, 4151], 1)) ):
            #AOPi
            lzbir =  aop(iopk,4152,1)
            dzbir =  (suma_liste(iopk,[4147,4148, 4150],1) - suma_liste(iopk, [4149, 4151], 1)) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4152 = AOP-u (4147 + 4148 - 4149 + 4150 - 4151)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40011
        if not( aop(iopk,4170,1) == (suma_liste(iopk,[4165,4166, 4168],1) - suma_liste(iopk, [4167, 4169], 1)) ):
            #AOPi
            lzbir =  aop(iopk,4170,1) 
            dzbir =  (suma_liste(iopk,[4165,4166, 4168],1) - suma_liste(iopk, [4167, 4169], 1)) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4170 = AOP-u (4165 + 4166 - 4167 + 4168 - 4169)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40012
        if not( aop(iopk,4208,1) == (suma_liste(iopk,[4203,4204, 4206],1) - suma_liste(iopk, [4205, 4207], 1)) ):
            #AOPi
            lzbir =  aop(iopk,4208,1) 
            dzbir =  (suma_liste(iopk,[4203,4204, 4206],1) - suma_liste(iopk, [4205, 4207], 1)) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4208 = AOP-u (4203 + 4204 - 4205 + 4206 - 4207)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40013
        #Za ovaj set se ne primenjuje pravilo 
        
        #40014
        if( suma_liste(iopk,[4001,4065,4097,4129,4165,4241],1) > suma_liste(iopk,[4033,4147,4203],1) ):
            if not( aop(iopk,4285,1) == suma_liste(iopk,[4001,4065,4097,4129,4165,4241],1)-suma_liste(iopk,[4033,4147,4203],1) ):
                lzbir =  aop(iopk,4285,1) 
                dzbir =  suma_liste(iopk,[4001,4065,4097,4129,4165,4241],1)-suma_liste(iopk,[4033,4147,4203],1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4285 = AOP-u (4001 - 4033 + 4065 + 4097 + 4129 - 4147 + 4165 - 4203 + 4241), ako je AOP (4001 + 4065 + 4097 + 4129 + 4165 + 4241) > AOP-a (4033 + 4147 + 4203)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40015
        if( suma_liste(iopk,[4001,4065,4097,4129,4165,4241],1) < suma_liste(iopk,[4033,4147,4203],1) ):
            if not( aop(iopk,4291,1) == suma_liste(iopk,[4033,4147,4203],1)-suma_liste(iopk,[4001,4065,4097,4129,4165,4241],1) ):
                lzbir =  aop(iopk,4291,1) 
                dzbir =  suma_liste(iopk,[4033,4147,4203],1)-suma_liste(iopk,[4001,4065,4097,4129,4165,4241],1) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4291 = AOP-u (4033 - 4001 - 4065 - 4097 - 4129 + 4147 - 4165 + 4203 - 4241), ako je AOP (4001 + 4065 + 4097 + 4129 + 4165 + 4241) < AOP-a (4033 + 4147 + 4203)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40016
        if( suma_liste(iopk,[4001,4065,4097,4129,4165,4241],1) == suma_liste(iopk,[4033,4147,4203],1) ):
            if not( aop(iopk,4285,1) + aop(iopk,4291,1) == 0 ):
                lzbir =  aop(iopk,4285,1) + aop(iopk,4291,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4285 + 4291) = 0 , ako je AOP (4001 + 4065 + 4097 + 4129 + 4165 + 4241) = AOP-u (4033 + 4147 + 4203) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40017
        if( aop(iopk,4285,1) > 0 ):
            if not( aop(iopk,4291,1) == 0 ):
                lzbir =  aop(iopk,4291,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4285 > 0, onda je AOP 4291 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40018
        if( aop(iopk,4291,1) > 0 ):
            if not( aop(iopk,4285,1) == 0 ):
                lzbir =  aop(iopk,4285,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4291 > 0, onda je AOP 4285 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40019
        if (suma_liste (iopk, [4006, 4070, 4102, 4134, 4170, 4246],1) > suma_liste (iopk, [4038, 4152, 4208],1)):
            if not( aop(iopk,4286,1) == (suma_liste (iopk, [4006,4070,4102,4134,4170, 4246],1) - suma_liste (iopk, [4038,4152,4208],1)) ):
                #AOPi
                lzbir =  aop(iopk,4286,1)
                dzbir =  suma_liste (iopk, [4006,4070,4102,4134,4170, 4246],1) - suma_liste (iopk, [4038,4152,4208],1)
                form_errors.append('AOP 4286 = AOP-u (4006 - 4038 + 4070 + 4102 + 4134 - 4152 + 4170 - 4208 + 4246), ako je AOP (4006 + 4070 + 4102 + 4134 + 4170 + 4246) > AOP-a (4038 + 4152 + 4208)  ')
        
        #40020
        if (suma_liste (iopk, [4006, 4070, 4102, 4134, 4170, 4246],1) < suma_liste (iopk, [4038, 4152, 4208],1)):
            if not( aop(iopk,4292,1) == (suma_liste (iopk, [4038,4152,4208],1) - suma_liste (iopk, [4006,4070,4102,4134,4170, 4246],1)) ):
                #AOPi
                lzbir =  aop(iopk,4292,1) 
                dzbir =  (suma_liste (iopk, [4038,4152,4208],1) - suma_liste (iopk, [4006,4070,4102,4134,4170, 4246],1)) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4292 = AOP-u (4038 - 4006 - 4070 - 4102 - 4134 + 4152 - 4170 + 4208 - 4246), ako je AOP (4006 + 4070 + 4102 + 4134 + 4170 + 4246) < AOP-a (4038 + 4152 + 4208)  ')
        
        #40021
        if (suma_liste (iopk, [4006, 4070, 4102, 4134, 4170, 4246],1) == suma_liste (iopk, [4038, 4152, 4208],1)):
            if not(suma_liste (iopk, [4286,4292],1) == 0):
                #AOPi
                lzbir = suma_liste (iopk, [4286,4292],1) 
                dzbir =  0
                razlika = lzbir - dzbir
                form_errors.append('AOP (4286 + 4292) = 0, ako je AOP (4006 + 4070 + 4102 + 4134 + 4170 + 4246) = AOP-u (4038 + 4152 + 4208) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40022
        if( aop(iopk,4286,1) > 0 ):
            if not( aop(iopk,4292,1) == 0 ):
                lzbir =  aop(iopk,4292,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4286 > 0, onda je AOP 4292 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40023
        if( aop(iopk,4292,1) > 0 ):
            if not( aop(iopk,4286,1) == 0 ):
                lzbir =  aop(iopk,4286,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4292 > 0, onda je AOP 4286 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40024
        if( aop(iopk,4171,1) > 0 ):
            if not( aop(iopk,4209,1) == 0 ):
                lzbir =  aop(iopk,4209,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4171 > 0, onda je AOP 4209 = 0 Ne mogu biti istovremeno prikazani dobitak i gubitak tekuće godine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40025
        if( aop(iopk,4209,1) > 0 ):
            if not( aop(iopk,4171,1) == 0 ):
                lzbir =  aop(iopk,4171,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4209 > 0, onda je AOP 4171 = 0 Ne mogu biti istovremeno prikazani dobitak i gubitak tekuće godine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40026
        if( suma_liste (iopk, [4007,4009,4012],1) > suma_liste (iopk, [4008,4010,4011,4013],1) ):
            if not( aop(iopk,4014,1) == (suma_liste (iopk, [4007,4009,4012],1) - suma_liste (iopk, [4008,4010,4011,4013],1)) ):
                #AOPi
                lzbir =  aop(iopk,4014,1)
                dzbir =  (suma_liste (iopk, [4007,4009,4012],1) - suma_liste (iopk, [4008,4010,4011,4013],1)) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4014 = AOP-u (4007 - 4008 + 4009 - 4010 - 4011 + 4012 - 4013), ako je AOP (4007 + 4009 + 4012) > AOP-a (4008 + 4010 + 4011 + 4013)  ')
        
        #40027
        if( suma_liste (iopk, [4007,4009,4012],1) < suma_liste (iopk, [4008,4010,4011,4013],1) ):
            if not( aop(iopk,4015,1) == (suma_liste (iopk, [4008,4010,4011,4013],1) - suma_liste (iopk, [4007,4009,4012],1)) ):
                #AOPi
                lzbir =  aop(iopk,4015,1) 
                dzbir =  (suma_liste (iopk, [4008,4010,4011,4013],1) - suma_liste (iopk, [4007,4009,4012],1)) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4015 = AOP-u (4008 - 4007 - 4009 + 4010 + 4011 - 4012 + 4013), ako je AOP (4007 + 4009 + 4012) < AOP-a (4008 + 4010 + 4011 + 4013)  ')
        
        #40028
        if( suma_liste (iopk, [4007,4009,4012],1) == suma_liste (iopk, [4008,4010,4011,4013],1) ):
            if not( suma_liste (iopk, [4014,4015],1) == 0 ):
                #AOPi
                lzbir =  suma_liste (iopk, [4014,4015],1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4014  + 4015) = 0, ako je AOP (4007 + 4009 + 4012) = AOP-u (4008 + 4010 + 4011 + 4013) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40029
        if( aop(iopk,4014,1) > 0 ):
            if not( aop(iopk,4015,1) == 0 ):
                lzbir =  aop(iopk,4015,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4014 > 0, onda je AOP 4015 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije s vlasnicima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40030
        if( aop(iopk,4015,1) > 0 ):
            if not( aop(iopk,4014,1) == 0 ):
                lzbir =  aop(iopk,4014,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4015 > 0, onda je AOP 4014 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije s vlasnicima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40031
        if(suma_liste (iopk, [4039,4041,4044],1) > suma_liste (iopk, [4040,4042,4043,4045],1)):
            if not( aop(iopk,4046,1) == (suma_liste (iopk, [4039,4041,4044],1) - suma_liste (iopk, [4040,4042,4043,4045],1)) ):
                #AOPi
                lzbir =  aop(iopk,4046,1) 
                dzbir =  (suma_liste (iopk, [4039,4041,4044],1) - suma_liste (iopk, [4040,4042,4043,4045],1)) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4046 = AOP-u (4039 - 4040 + 4041 - 4042 - 4043 + 4044 - 4045), ako je AOP (4039 + 4041 + 4044) > AOP-a (4040 + 4042 + 4043 + 4045)  ')
        
        #40032
        if(suma_liste (iopk, [4039,4041,4044],1) < suma_liste (iopk, [4040,4042,4043,4045],1)):
            if not( aop(iopk,4047,1) == (suma_liste (iopk, [4040,4042,4043,4045],1) - suma_liste (iopk, [4039,4041,4044],1)) ):
                #AOPi
                lzbir =  aop(iopk,4047,1) 
                dzbir =  (suma_liste (iopk, [4040,4042,4043,4045],1) - suma_liste (iopk, [4039,4041,4044],1)) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4047 = AOP-u (4040 - 4039 - 4041 + 4042 + 4043 - 4044 + 4045), ako je AOP (4039 + 4041 + 4044) < AOP-a (4040 + 4042 + 4043 + 4045)  ')
        
        #40033
        if(suma_liste (iopk, [4039,4041,4044],1) == suma_liste (iopk, [4040,4042,4043,4045],1)):
            if not( suma_liste (iopk, [4046,4047],1) == 0 ):
                #AOPi
                lzbir =  suma_liste (iopk, [4046,4047],1) 
                dzbir =  0
                razlika = lzbir - dzbir
                form_errors.append('AOP (4046 + 4047) = 0, ako je AOP (4039 + 4041 + 4044) = AOP-u (4040 + 4042 + 4043 + 4045) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40034
        if( aop(iopk,4046,1) > 0 ):
            if not( aop(iopk,4047,1) == 0 ):
                lzbir =  aop(iopk,4047,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4046 > 0, onda je AOP 4047 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije s vlasnicima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40035
        if( aop(iopk,4047,1) > 0 ):
            if not( aop(iopk,4046,1) == 0 ):
                lzbir =  aop(iopk,4046,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4047 > 0, onda je AOP 4046 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije s vlasnicima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40036
        if(suma_liste (iopk, [4071,4073,4076],1) > suma_liste (iopk, [4072,4074,4075,4077],1)):
            if not(  aop(iopk,4078,1) == (suma_liste (iopk, [4071,4073,4076],1) - suma_liste (iopk, [4072,4074,4075,4077],1)) ):
                #AOPi
                lzbir =   aop(iopk,4078,1) 
                dzbir =  (suma_liste (iopk, [4071,4073,4076],1) - suma_liste (iopk, [4072,4074,4075,4077],1)) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4078 = AOP-u (4071 - 4072 + 4073 - 4074 - 4075 + 4076 - 4077), ako je AOP (4071 + 4073 + 4076) > AOP-a (4072 + 4074 + 4075 + 4077)  ')
        
        #40037
        if(suma_liste (iopk, [4071,4073,4076],1) < suma_liste (iopk, [4072,4074,4075,4077],1)):
            if not(  aop(iopk,4079,1) == (suma_liste (iopk, [4072,4074,4075,4077],1) - suma_liste (iopk, [4071,4073,4076],1)) ):
                #AOPi
                lzbir =   aop(iopk,4079,1) 
                dzbir =  (suma_liste (iopk, [4072,4074,4075,4077],1) - suma_liste (iopk, [4071,4073,4076],1)) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4079 = AOP-u (4072 - 4071 - 4073 + 4074 + 4075 - 4076 + 4077), ako je AOP (4071 + 4073 + 4076) < AOP-a (4072 + 4074 + 4075 + 4077)  ')
        
        #40038
        if(suma_liste (iopk, [4071,4073,4076],1) == suma_liste (iopk, [4072,4074,4075,4077],1)):
            if not(  suma_liste (iopk, [4078,4079],1) == 0):
                #AOPi
                lzbir =   suma_liste (iopk, [4078,4079],1) 
                dzbir =  0
                razlika = lzbir - dzbir
                form_errors.append('AOP (4078 + 4079)  = 0, ako je AOP (4071 + 4073 + 4076) = AOP-u (4072 + 4074 + 4075 + 4077) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40039
        if( aop(iopk,4078,1) > 0 ):
            if not( aop(iopk,4079,1) == 0 ):
                lzbir =  aop(iopk,4079,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4078 > 0, onda je AOP 4079 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije s vlasnicima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40040
        if( aop(iopk,4079,1) > 0 ):
            if not( aop(iopk,4078,1) == 0 ):
                lzbir =  aop(iopk,4078,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4079 > 0, onda je AOP 4078 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije s vlasnicima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40041
        if(suma_liste (iopk, [4103,4105,4108],1) > suma_liste (iopk, [4104,4106,4107,4109],1)):
            if not( aop(iopk,4110,1) == (suma_liste (iopk, [4103,4105,4108],1) - suma_liste (iopk, [4104,4106,4107,4109],1)) ):
                #AOPi
                lzbir =  aop(iopk,4110,1) 
                dzbir =  (suma_liste (iopk, [4103,4105,4108],1) - suma_liste (iopk, [4104,4106,4107,4109],1)) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4110 = AOP-u (4103 - 4104 + 4105 - 4106 - 4107 + 4108 - 4109), ako je AOP (4103 + 4105 + 4108) > AOP-a (4104 + 4106 + 4107 + 4109)  ')
        
        #40042
        if(suma_liste (iopk, [4103, 4105, 4108],1) < suma_liste (iopk, [4104, 4106, 4107, 4109],1)):
            if not( aop(iopk,4111,1) == (suma_liste (iopk, [4104, 4106, 4107, 4109],1) - suma_liste (iopk, [4103, 4105, 4108],1)) ):
                #AOPi
                lzbir =  aop(iopk,4111,1) 
                dzbir =  (suma_liste (iopk, [4104, 4106, 4107, 4109],1) - suma_liste (iopk, [4103, 4105, 4108],1)) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4111 = AOP-u (4104 - 4103 - 4105 + 4106 + 4107 - 4108 + 4109), ako je AOP (4103 + 4105 + 4108) < AOP-a (4104 + 4106 + 4107 + 4109)  ')
        
        #40043
        if(suma_liste (iopk, [4103,4105,4108],1) == suma_liste (iopk, [4104,4106,4107,4109],1)):
            if not( suma_liste (iopk, [4110,4111],1) == 0 ):
                #AOPi
                lzbir =  suma_liste (iopk, [4110,4111],1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4110 + 4111) = 0, ako je AOP (4103 + 4105 + 4108) = AOP-u (4104 + 4106 + 4107 + 4109) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40044
        if( aop(iopk,4110,1) > 0 ):
            if not( aop(iopk,4111,1) == 0 ):
                lzbir =  aop(iopk,4111,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4110 > 0, onda je AOP 4111 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije s vlasnicima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40045
        if( aop(iopk,4111,1) > 0 ):
            if not( aop(iopk,4110,1) == 0 ):
                lzbir =  aop(iopk,4110,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4111 > 0, onda je AOP 4110 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije s vlasnicima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40046
        if( suma_liste (iopk, [4174,4176,4179],1) > suma_liste (iopk, [4175,4177,4178,4180],1) ):
            if not( aop(iopk,4181,1) == (suma_liste (iopk, [4174,4176,4179],1) - suma_liste (iopk, [4175,4177,4178,4180],1)) ):
                #AOPi
                lzbir =  aop(iopk,4181,1) 
                dzbir =  (suma_liste (iopk, [4174,4176,4179],1) - suma_liste (iopk, [4175,4177,4178,4180],1)) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4181 = AOP-u (4174 - 4175 + 4176 - 4177 - 4178 + 4179 - 4180), ako je AOP (4174 + 4176 + 4179) > AOP-a (4175 + 4177 + 4178 + 4180)  ')
        
        #40047
        if( suma_liste (iopk, [4174,4176,4179],1) < suma_liste (iopk, [4175,4177,4178,4180],1) ):
            if not( aop(iopk,4182,1) == (suma_liste (iopk, [4175,4177,4178,4180],1) - suma_liste (iopk, [4174,4176,4179],1)) ):
                #AOPi
                lzbir =  aop(iopk,4182,1) 
                dzbir =  (suma_liste (iopk, [4175,4177,4178,4180],1) - suma_liste (iopk, [4174,4176,4179],1)) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4182 = AOP-u (4175 - 4174 - 4176 + 4177 + 4178 - 4179 + 4180), ako je AOP (4174 + 4176 + 4179) < AOP-a (4175 + 4177 + 4178 + 4180)  ')
        
        #40048
        if( suma_liste (iopk, [4174,4176,4179],1) == suma_liste (iopk, [4175,4177,4178,4180],1) ):
            if not( suma_liste (iopk, [4181,4182],1) == 0 ):
                #AOPi
                lzbir =  suma_liste (iopk, [4181,4182],1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4181 + 4182) = 0, ako je AOP (4174 + 4176 + 4179) = AOP-u (4175 + 4177 + 4178 + 4180) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40049
        if( aop(iopk,4181,1) > 0 ):
            if not( aop(iopk,4182,1) == 0 ):
                lzbir =  aop(iopk,4182,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4181 > 0, onda je AOP 4182 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije s vlasnicima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40050
        if( aop(iopk,4182,1) > 0 ):
            if not( aop(iopk,4181,1) == 0 ):
                lzbir =  aop(iopk,4181,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4182 > 0, onda je AOP 4181 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije s vlasnicima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40051
        if( suma_liste (iopk, [4212, 4214, 4217],1) > suma_liste (iopk, [4213, 4215, 4216, 4218],1) ):
            if not( aop(iopk,4219,1) == (suma_liste (iopk, [4212, 4214, 4217],1) - suma_liste (iopk, [4213, 4215, 4216, 4218],1)) ):
                #AOPi
                lzbir =  aop(iopk,4219,1) 
                dzbir =  (suma_liste (iopk, [4212, 4214, 4217],1) - suma_liste (iopk, [4213, 4215, 4216, 4218],1)) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4219 = AOP-u (4212 - 4213 + 4214 - 4215 - 4216 + 4217 - 4218), ako je AOP (4212 + 4214 + 4217) > AOP-a (4213 + 4215 + 4216 + 4218)  ')
        
        #40052
        if( suma_liste (iopk, [4212,4214,4217],1) < suma_liste (iopk, [4213,4215,4216,4218],1) ):
            if not( aop(iopk,4220,1) == ( suma_liste (iopk, [4213,4215,4216,4218],1) - suma_liste (iopk, [4212,4214,4217],1)) ):
                #AOPi
                lzbir =  aop(iopk,4220,1)
                dzbir =  ( suma_liste (iopk, [4213,4215,4216,4218],1) - suma_liste (iopk, [4212,4214,4217],1)) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4220 = AOP-u (4213 - 4212 - 4214 + 4215 + 4216 - 4217 + 4218), ako je AOP (4212 + 4214 + 4217) < AOP-a (4213 + 4215 + 4216 + 4218)  ')
        
        #40053
        if( suma_liste (iopk, [4212,4214,4217],1) == suma_liste (iopk, [4213,4215,4216,4218],1) ):
            if not( suma_liste (iopk, [4219,4220],1) == 0 ):
                #AOPi
                lzbir =  suma_liste (iopk, [4219,4220],1)
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4219  + 4220) = 0, ako je AOP (4212 + 4214 + 4217) = AOP-u (4213 + 4215 + 4216 + 4218) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40054
        if( aop(iopk,4219,1) > 0 ):
            if not( aop(iopk,4220,1) == 0 ):
                lzbir =  aop(iopk,4220,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4219 > 0, onda je AOP 4220 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije s vlasnicima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40055
        if( aop(iopk,4220,1) > 0 ):
            if not( aop(iopk,4219,1) == 0 ):
                lzbir =  aop(iopk,4219,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4220 > 0, onda je AOP 4219 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije s vlasnicima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40056
        #Za ovaj set se ne primenjuje pravilo 
        
        #40057
        #Za ovaj set se ne primenjuje pravilo 
        
        #40058
        #Za ovaj set se ne primenjuje pravilo 
        
        #40059
        #Za ovaj set se ne primenjuje pravilo 
        
        #40060
        #Za ovaj set se ne primenjuje pravilo 
        
        #40061
        if not( aop(iopk,4016,1) == (suma_liste (iopk, [4006,4014],1) - aop(iopk,4015,1)) ):
            #AOPi
            lzbir =  aop(iopk,4016,1) 
            dzbir =  (suma_liste (iopk, [4006,4014],1) - aop(iopk,4015,1)) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4016 = AOP-u (4006 + 4014 - 4015)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40062 
        if not( aop(iopk,4048,1) == (suma_liste (iopk, [4038,4046],1) - aop(iopk,4047,1)) ):
            #AOPi
            lzbir =  aop(iopk,4048,1) 
            dzbir =  (suma_liste (iopk, [4038,4046],1) - aop(iopk,4047,1)) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4048 = AOP-u (4038 + 4046 - 4047)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40063 
        if not( aop(iopk,4080,1) == (suma_liste (iopk, [4070,4078],1) - aop(iopk,4079,1)) ):
            #AOPi
            lzbir =  aop(iopk,4080,1) 
            dzbir = (suma_liste (iopk, [4070,4078],1) - aop(iopk,4079,1))
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4080 = AOP-u (4070 + 4078 - 4079)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40064 
        if not( aop(iopk,4112,1) == (suma_liste (iopk, [4102,4110],1) - aop(iopk,4111,1)) ):
            #AOPi
            lzbir =  aop(iopk,4112,1) 
            dzbir =  (suma_liste (iopk, [4102,4110],1) - aop(iopk,4111,1)) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4112 = AOP-u (4102 + 4110 - 4111)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40065 
        if not( aop(iopk,4137,1) == (suma_liste (iopk, [4134,4135],1) - aop(iopk,4136,1)) ):
            #AOPi
            lzbir =  aop(iopk,4137,1) 
            dzbir =  (suma_liste (iopk, [4134,4135],1) - aop(iopk,4136,1)) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4137 = AOP-u (4134 + 4135 - 4136)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40066
        if not( aop(iopk,4155,1) == (suma_liste (iopk, [4152,4154],1) - aop(iopk,4153,1)) ):
            #AOPi
            lzbir =  aop(iopk,4155,1) 
            dzbir =  (suma_liste (iopk, [4152,4154],1) - aop(iopk,4153,1)) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4155 = AOP-u (4152 - 4153 + 4154)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40067 
        if not( aop(iopk,4183,1) == (suma_liste (iopk, [4170,4171,4172,4181],1) - suma_liste (iopk, [4173,4182],1)) ):
            #AOPi
            lzbir =  aop(iopk,4183,1) 
            dzbir =  (suma_liste (iopk, [4170,4171,4172,4181],1) - suma_liste (iopk, [4173,4182],1)) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4183 = AOP-u (4170 + 4171 + 4172 - 4173 + 4181 - 4182)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40068 
        if not( aop(iopk,4221,1) == (suma_liste (iopk, [4208,4209,4210,4219],1) - suma_liste (iopk, [4211,4220],1)) ):
            #AOPi
            lzbir =  aop(iopk,4221,1) 
            dzbir =  (suma_liste (iopk, [4208,4209,4210,4219],1) - suma_liste (iopk, [4211,4220],1)) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4221 = AOP-u (4208 + 4209 + 4210 - 4211 + 4219 - 4220)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40070 
        if (suma_liste (iopk, [4016,4080,4112,4137,4183, 4262],1) > suma_liste (iopk, [4048,4155,4221],1)):
            if not( aop(iopk,4287,1) == (suma_liste (iopk, [4016,4080,4112,4137,4183, 4262],1) - suma_liste (iopk, [4048,4155,4221],1)) ):
                #AOPi
                lzbir =  aop(iopk,4287,1) 
                dzbir =  (suma_liste (iopk, [4016,4080,4112,4137,4183, 4262],1) - suma_liste (iopk, [4048,4155,4221],1)) 
                razlika = lzbir - dzbir
                form_errors.append("    AOP 4287 = AOP-u (4016 - 4048 + 4080 + 4112 + 4137 - 4155 + 4183 - 4221 + 4262), ako je AOP (4016 + 4080 + 4112 + 4137 + 4183 + 4262) > AOP-a (4048 + 4155 + 4221)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40071 
        if (suma_liste (iopk, [4016, 4080, 4112, 4137, 4183, 4262],1) < suma_liste (iopk, [4048, 4155, 4221],1)):
            if not( aop(iopk,4293,1) == ( suma_liste (iopk, [4048, 4155, 4221],1) - suma_liste (iopk, [4016, 4080, 4112, 4137, 4183, 4262],1)) ):
                #AOPi
                lzbir =  aop(iopk,4293,1)
                dzbir =  ( suma_liste (iopk, [4048, 4155, 4221],1) - suma_liste (iopk, [4016, 4080, 4112, 4137, 4183, 4262],1)) 
                razlika = lzbir - dzbir
                form_errors.append("    AOP 4293 = AOP-u (4048 - 4016 - 4080 - 4112 - 4137 + 4155 - 4183 + 4221 - 4262), ako je AOP (4016 + 4080 + 4112 + 4137 + 4183 + 4262) < AOP-a (4048 + 4155 + 4221)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40072 
        if (suma_liste (iopk, [4016, 4080, 4112, 4137, 4183, 4262],1) == suma_liste (iopk, [4048, 4155, 4221],1)):
            if not( suma_liste (iopk, [4287,4293],1) == 0 ):
                #AOPi
                lzbir =  suma_liste (iopk, [4287,4293],1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append("    AOP (4287 + 4293) = 0, ako je AOP (4016 + 4080 + 4112 + 4137 + 4183 + 4262) = AOP-u (4048 + 4155 + 4221)    Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake    "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40073
        if( aop(iopk,4287,1) > 0 ):
            if not( aop(iopk,4293,1) == 0 ):
                lzbir =  aop(iopk,4293,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4287 > 0, onda je AOP 4293 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40074
        if( aop(iopk,4293,1) > 0 ):
            if not( aop(iopk,4287,1) == 0 ):
                lzbir =  aop(iopk,4287,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4293 > 0, onda je AOP 4287 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40075 
        if not( aop(iopk,4017,1) == aop(iopk,4016,1)):
            #AOPi
            lzbir =  aop(iopk,4017,1) 
            dzbir =  aop(iopk,4016,1)
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4017 = AOP-u 4016        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40076 
        if not( aop(iopk,4049,1) == aop(iopk,4048,1) ):
            #AOPi
            lzbir =  aop(iopk,4049,1) 
            dzbir =  aop(iopk,4048,1) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4049 = AOP-u 4048        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40077 
        if not( aop(iopk,4081,1) == aop(iopk,4080,1) ):
            #AOPi
            lzbir =  aop(iopk,4081,1) 
            dzbir =  aop(iopk,4080,1) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4081 = AOP-u 4080        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40078 
        if not( aop(iopk,4113,1) == aop(iopk,4112,1) ):
            #AOPi
            lzbir =  aop(iopk,4113,1) 
            dzbir =  aop(iopk,4112,1) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4113 = AOP-u 4112        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40079 
        if not( aop(iopk,4138,1) == aop(iopk,4137,1) ):
            #AOPi
            lzbir =  aop(iopk,4138,1) 
            dzbir =  aop(iopk,4137,1) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4138 = AOP-u 4137        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40080 
        if not( aop(iopk,4156,1) == aop(iopk,4155,1) ):
            #AOPi
            lzbir =  aop(iopk,4156,1) 
            dzbir =  aop(iopk,4155,1) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4156 = AOP-u 4155        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40081 
        if not( aop(iopk,4184,1) == aop(iopk,4183,1) ):
            #AOPi
            lzbir =  aop(iopk,4184,1) 
            dzbir =  aop(iopk,4183,1) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4184 = AOP-u 4183        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40082 
        if not( aop(iopk,4222,1) == aop(iopk,4221,1) ):
           #AOPi
           lzbir =  aop(iopk,4222,1) 
           dzbir =  aop(iopk,4221,1) 
           razlika = lzbir - dzbir
           form_errors.append("    AOP 4222 = AOP-u 4221        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40083
        if not(aop(iopk, 4263, 1)== aop(iopk, 4262, 1)):
            #AOPi
           lzbir =  aop(iopk,4263,1) 
           dzbir =  aop(iopk,4262,1) 
           razlika = lzbir - dzbir
           form_errors.append("    AOP 4263 = AOP-u 4262        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40084 
        if not( aop(iopk,4288,1) == aop(iopk,4287,1) ):
            #AOPi
            lzbir =  aop(iopk,4288,1) 
            dzbir =  aop(iopk,4287,1) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4288 = AOP-u 4287        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40085 
        if not( aop(iopk,4294,1) == aop(iopk,4293,1) ):
            #AOPi
            lzbir =  aop(iopk,4294,1) 
            dzbir =  aop(iopk,4293,1) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4294 = AOP-u 4293        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40086 
        if not( aop(iopk,4022,1) == (suma_liste (iopk, [4017,4018, 4020],1) - suma_liste (iopk, [4019,4021],1)) ):
            #AOPi
            lzbir =  aop(iopk,4022,1) 
            dzbir =  (suma_liste (iopk, [4017,4018, 4020],1) - suma_liste (iopk, [4019,4021],1))
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4022 = AOP-u (4017 + 4018 - 4019 + 4020 - 4021)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40087 
        if not( aop(iopk,4054,1) == (suma_liste (iopk, [4049,4050, 4052],1) - suma_liste(iopk,[4051, 4053], 1)) ):
            #AOPi
            lzbir =  aop(iopk,4054,1) 
            dzbir =  (suma_liste (iopk, [4049,4050, 4052],1) - suma_liste(iopk,[4051, 4053], 1)) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4054 = AOP-u (4049 + 4050 - 4051 + 4052 - 4053)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40088 
        if not( aop(iopk,4086,1) == (suma_liste (iopk, [4081,4082, 4084],1) - suma_liste (iopk, [4083, 4085],1)) ):
            #AOPi
            lzbir =  aop(iopk,4086,1) 
            dzbir =  (suma_liste (iopk, [4081,4082, 4084],1) - suma_liste (iopk, [4083, 4085],1)) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4086 = AOP-u (4081 + 4082 - 4083 + 4084 - 4085)      "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40089 
        if not( aop(iopk,4118,1) == (suma_liste (iopk, [4113,4114, 4116],1) - suma_liste (iopk, [4115,4117],1)) ):
            #AOPi
            lzbir =  aop(iopk,4118,1) 
            dzbir =  (suma_liste (iopk, [4113,4114, 4116],1) - suma_liste (iopk, [4115,4117],1)) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4118 = AOP-u (4113 + 4114 - 4115 + 4116 - 4117)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40090 
        if not( aop(iopk,4143,1) == (suma_liste (iopk, [4138,4139, 4141],1) - suma_liste (iopk, [4140,4142],1)) ):
            #AOPi
            lzbir =  aop(iopk,4143,1) 
            dzbir =  (suma_liste (iopk, [4138,4139, 4141],1) - suma_liste (iopk, [4140,4142],1)) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4143 = AOP-u (4138 + 4139 - 4140 + 4141 - 4142)       "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40091 
        if not( aop(iopk,4161,1) == (suma_liste (iopk, [4156,4157, 4159],1) - suma_liste (iopk, [4158,4160],1)) ):
            #AOPi
            lzbir =  aop(iopk,4161,1) 
            dzbir =  (suma_liste (iopk, [4156,4157, 4159],1) - suma_liste (iopk, [4158,4160],1)) 
            razlika = lzbir - dzbir
            form_errors.append("   AOP 4161 = AOP-u (4156 + 4157 - 4158 + 4159 - 4160)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40092 
        if not( aop(iopk,4189,1) == (suma_liste (iopk, [4184,4185, 4187],1) - suma_liste (iopk, [4186,4188],1)) ):
            #AOPi
            lzbir =  aop(iopk,4189,1) 
            dzbir =  (suma_liste (iopk, [4184,4185, 4187],1) - suma_liste (iopk, [4186,4188],1)) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4189 = AOP-u (4184 + 4185 - 4186 + 4187 - 4188)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40093 
        if not( aop(iopk,4227,1) == (suma_liste (iopk, [4222, 4223, 4225],1) - suma_liste (iopk, [4224,4226],1)) ):
            #AOPi
            lzbir =  aop(iopk,4227,1) 
            dzbir =  (suma_liste (iopk, [4222, 4223, 4225],1) - suma_liste (iopk, [4224,4226],1)) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4227 = AOP-u (4222 + 4223 - 4224 + 4225 - 4226)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40095 Novo pravilo 2018.
        if(suma_liste(iopk,[4017, 4081, 4113, 4138, 4184, 4263], 1 )> suma_liste(iopk, [4049, 4156, 4222], 1)):
            if not(aop(iopk, 4288, 1)==(suma_liste(iopk,[4017, 4081, 4113, 4138, 4184, 4263], 1 ) - suma_liste(iopk, [4049, 4156, 4222], 1) )):
                 #AOPi
                lzbir =  aop(iopk, 4288, 1)
                dzbir =  ( suma_liste(iopk,[4017, 4081, 4113, 4138, 4184, 4263], 1 ) - suma_liste(iopk, [4049, 4156, 4222], 1) ) 
                razlika = lzbir - dzbir
                form_errors.append("    AOP 4288 = AOP-u (4017 - 4049 + 4081 + 4113 + 4138 - 4156 + 4184 - 4222 + 4263), ako je AOP (4017 + 4081 + 4113 + 4138 + 4184 + 4263) > AOP-a (4049 + 4156 + 4222)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40096
        if(suma_liste(iopk,[4049, 4156, 4222], 1 )> suma_liste(iopk, [4017, 4081, 4113, 4138, 4184, 4263], 1)):
            if not(aop(iopk, 4294, 1)==(suma_liste(iopk,[4049, 4156, 4222], 1 ) - suma_liste(iopk, [4017, 4081, 4113, 4138, 4184, 4263], 1) )):
                 #AOPi
                lzbir =  aop(iopk, 4294, 1)
                dzbir =  ( suma_liste(iopk,[4049, 4156, 4222], 1 ) - suma_liste(iopk, [4017, 4081, 4113, 4138, 4184, 4263], 1) ) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4294 = AOP-u (4049 - 4017 - 4081 - 4113 - 4138 + 4156 - 4184 + 4222 - 4263), ako je AOP (4017 + 4081 + 4113 + 4138 + 4184 + 4263) < AOP-a (4049 + 4156 + 4222)  ')
        
        #40097
        if(suma_liste(iopk, [4017, 4081, 4113, 4138, 4184, 4263], 1)==suma_liste(iopk, [4049, 4156, 4222], 1)):
            if not(suma_liste(iopk, [4288, 4294], 1)==0):
                #AOPi
                lzbir=suma_liste(iopk, [4288, 4294], 1)
                dzbir=0
                razlika=lzbir-dzbir
                form_errors.append('AOP (4288 + 4294) = 0 , ako je AOP (4017 + 4081 + 4113 + 4138 + 4184 + 4263) = AOP-u (4049 + 4156 + 4222)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40098
        if( aop(iopk,4288,1) > 0 ):
            if not( aop(iopk,4294,1) == 0 ):
                lzbir =  aop(iopk,4294,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4288 > 0, onda je AOP 4294 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40099
        if( aop(iopk,4294,1) > 0 ):
            if not( aop(iopk,4288,1) == 0 ):
                lzbir =  aop(iopk,4288,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4294 > 0, onda je AOP 4288 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40100
        if( suma_liste (iopk, [4022,4086,4118,4143,4189, 4268],1) > suma_liste (iopk, [4054,4161,4227],1) ):
            if not( aop(iopk,4289,1) == (suma_liste (iopk, [4022,4086,4118,4143,4189, 4268],1) - suma_liste (iopk, [4054,4161,4227],1)) ):
                #AOPi
                lzbir =  aop(iopk,4289,1) 
                dzbir =  (suma_liste (iopk, [4022,4086,4118,4143,4189, 4268],1) - suma_liste (iopk, [4054,4161,4227],1)) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4289 = AOP-u (4022 - 4054 + 4086 + 4118 + 4143 - 4161 + 4189 - 4227 + 4268), ako je AOP (4022 + 4086 + 4118 + 4143 + 4189 + 4268) > AOP-a (4054 + 4161 + 4227)  ')
        
        #40101
        if( suma_liste (iopk, [4022, 4086, 4118, 4143, 4189, 4268],1) < suma_liste (iopk, [4054, 4161, 4227],1) ):
            if not( aop(iopk,4295,1) == (suma_liste (iopk, [4054, 4161, 4227],1) - suma_liste (iopk, [4022, 4086, 4118, 4143, 4189, 4268],1)) ):
                #AOPi
                lzbir =  aop(iopk,4295,1) 
                dzbir =  ( suma_liste (iopk, [4054, 4161, 4227],1) - suma_liste (iopk, [4022, 4086, 4118, 4143, 4189, 4268],1)) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4295 = AOP-u (4054 - 4022 - 4086 - 4118 - 4143 + 4161 - 4189 + 4227 - 4268), ako je AOP (4022 + 4086 + 4118 + 4143 + 4189 + 4268) < AOP-a (4054 + 4161 + 4227)  ')
        
        #40102
        if( suma_liste (iopk, [4022, 4086, 4118, 4143, 4189, 4268],1) == suma_liste (iopk, [4054, 4161, 4227],1) ):
            if not( suma_liste (iopk, [4289,4295],1) == 0 ):
                #AOPi
                lzbir =  suma_liste (iopk, [4289,4295],1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4289 + 4295) = 0, ako je AOP (4022 + 4086 + 4118 + 4143 + 4189 + 4268) = AOP-u (4054 + 4161 + 4227) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40103
        if( aop(iopk,4289,1) > 0 ):
            if not( aop(iopk,4295,1) == 0 ):
                lzbir =  aop(iopk,4295,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4289 > 0, onda je AOP 4295 = 0 Ne mogu biti istovremeno prikazani dobitak i gubitak tekuće godine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40104
        if( aop(iopk,4295,1) > 0 ):
            if not( aop(iopk,4289,1) == 0 ):
                lzbir =  aop(iopk,4289,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4295 > 0, onda je AOP 4289 = 0 Ne mogu biti istovremeno prikazani dobitak i gubitak tekuće godine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40105
        if( aop(iopk,4190,1) > 0 ):
            if not( aop(iopk,4228,1) == 0 ):
                lzbir =  aop(iopk,4228,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4190 > 0, onda je AOP 4228 = 0 Ne mogu biti istovremeno prikazani dobitak i gubitak tekuće godine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40106
        if( aop(iopk,4228,1) > 0 ):
            if not( aop(iopk,4190,1) == 0 ):
                lzbir =  aop(iopk,4190,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4228 > 0, onda je AOP 4190 = 0 Ne mogu biti istovremeno prikazani dobitak i gubitak tekuće godine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40107
        if( suma_liste (iopk, [4023, 4025, 4028],1) > suma_liste (iopk, [4024, 4026, 4027, 4029],1) ):
            if not( aop(iopk,4030,1) == (suma_liste (iopk, [4023, 4025, 4028],1) - suma_liste (iopk, [4024, 4026, 4027, 4029],1)) ):
                #AOPi
                lzbir =  aop(iopk,4030,1) 
                dzbir =  (suma_liste (iopk, [4023, 4025, 4028],1) - suma_liste (iopk, [4024, 4026, 4027, 4029],1)) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4030 = AOP-u (4023 - 4024 + 4025 - 4026 - 4027 + 4028 - 4029), ako je AOP (4023 + 4025 + 4028) > AOP-a (4024 + 4026 + 4027 + 4029)  ')
        
        #40108
        if( suma_liste (iopk, [4023, 4025, 4028],1) < suma_liste (iopk, [4024, 4026, 4027, 4029],1) ):
            if not( aop(iopk,4031,1) == ( suma_liste (iopk, [4024, 4026, 4027, 4029],1) - suma_liste (iopk, [4023, 4025, 4028],1)  ) ):
                #AOPi
                lzbir =  aop(iopk,4031,1) 
                dzbir =  ( suma_liste (iopk, [4024, 4026, 4027, 4029],1) - suma_liste (iopk, [4023, 4025, 4028],1) ) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4031 = AOP-u (4024 - 4023 - 4025 + 4026 + 4027 - 4028 + 4029), ako je AOP (4023 + 4025 + 4028) < AOP-a (4024 + 4026 + 4027 + 4029)  ')
        
        #40109
        if( suma_liste (iopk, [4023,4025,4028],1) == suma_liste (iopk, [4024,4026,4027,4029],1) ):
            if not( suma_liste (iopk, [4030,4031],1) == 0 ):
                #AOPi
                lzbir =  suma_liste (iopk, [4030,4031],1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4030 + 4031) = 0, ako je AOP (4023 + 4025 + 4028) = AOP-u (4024 + 4026 + 4027 + 4029) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40110
        if( aop(iopk,4030,1) > 0 ):
            if not( aop(iopk,4031,1) == 0 ):
                lzbir =  aop(iopk,4031,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4030 > 0, onda je AOP 4031 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije s vlasnicima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40111
        if( aop(iopk,4031,1) > 0 ):
            if not( aop(iopk,4030,1) == 0 ):
                lzbir =  aop(iopk,4030,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4031 > 0, onda je AOP 4030 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije s vlasnicima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40112
        if( suma_liste (iopk, [4055, 4057, 4060],1) > suma_liste (iopk, [4056, 4058, 4059, 4061],1) ):
            if not( aop(iopk,4062,1) == (suma_liste (iopk, [4055, 4057, 4060],1) - suma_liste (iopk, [4056, 4058, 4059, 4061],1)) ):
                #AOPi
                lzbir =  aop(iopk,4062,1) 
                dzbir =  (suma_liste (iopk, [4055, 4057, 4060],1) - suma_liste (iopk, [4056, 4058, 4059, 4061],1)) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4062 = AOP-u (4055 - 4056 + 4057 - 4058 - 4059 + 4060 - 4061), ako je AOP (4055 + 4057 + 4060) > AOP-a (4056 + 4058 + 4059 + 4061)  ')
        
        #40113
        if( suma_liste (iopk, [4055, 4057, 4060],1) < suma_liste (iopk, [4056, 4058, 4059, 4061],1) ):
            if not( aop(iopk,4063,1) == (  suma_liste (iopk, [4056, 4058, 4059, 4061],1)) - suma_liste(iopk, [4055, 4057, 4060],1) ):
                #AOPi
                lzbir =  aop(iopk,4063,1) 
                dzbir =  ( suma_liste (iopk, [4056, 4058, 4059, 4061],1) - suma_liste (iopk, [4055, 4057, 4060],1) ) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4063 = AOP-u (4056 - 4055 - 4057 + 4058 + 4059 - 4060 + 4061), ako je AOP  (4055 + 4057 + 4060) < AOP-a (4056 + 4058 + 4059 + 4061)  ')
        
        #40114
        if( suma_liste (iopk, [4055, 4057, 4060],1) == suma_liste (iopk, [4056,4058,4059,4061],1) ):
            if not( suma_liste (iopk, [4062,4063],1) == 0 ):
                #AOPi
                lzbir =  suma_liste (iopk, [4062,4063],1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4062 + 4063) = 0,  ako je AOP (4055 + 4057 + 4060) = AOP-u (4056 + 4058 + 4059 + 4061) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40115
        if( aop(iopk,4062,1) > 0 ):
            if not( aop(iopk,4063,1) == 0 ):
                lzbir =  aop(iopk,4063,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4062 > 0, onda je AOP 4063 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije s vlasnicima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40116
        if( aop(iopk,4063,1) > 0 ):
            if not( aop(iopk,4062,1) == 0 ):
                lzbir =  aop(iopk,4062,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4063> 0, onda je AOP 4062 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije s vlasnicima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40117
        if( suma_liste (iopk, [4087, 4089, 4092],1) > suma_liste (iopk, [4088, 4090, 4091, 4093],1) ):
            if not( aop(iopk,4094,1) == ( suma_liste(iopk, [4087, 4089, 4092],1) - suma_liste(iopk, [4088, 4090, 4091, 4093],1) ) ):
                #AOPi
                lzbir =  aop(iopk,4094,1) 
                dzbir =  ( suma_liste (iopk, [4087, 4089, 4092],1) - suma_liste (iopk, [4088, 4090, 4091, 4093],1) ) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4094 = AOP-u (4087 - 4088 + 4089 - 4090 - 4091 + 4092 - 4093), ako je AOP (4087 + 4089 + 4092) > AOP-a (4088 + 4090 + 4091 + 4093)  ')
        
        #40118
        if( suma_liste (iopk, [4087, 4089, 4092],1) < suma_liste (iopk, [4088, 4090, 4091, 4093],1) ):
            if not( aop(iopk,4095,1) == (  suma_liste (iopk, [4088, 4090, 4091, 4093],1) - suma_liste(iopk, [4087, 4089, 4092],1) ) ):
                #AOPi
                lzbir =  aop(iopk,4095,1) 
                dzbir =  (  suma_liste(iopk, [4088, 4090, 4091, 4093],1) - suma_liste(iopk, [4087, 4089, 4092],1) ) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4095 = AOP-u (4088 - 4087 - 4089 + 4090 + 4091 - 4092 + 4093), ako je AOP (4087 + 4089 + 4092) < AOP-a (4088 + 4090 + 4091 + 4093)  ')
        
        #40119
        if( suma_liste (iopk, [4087, 4089, 4092],1) == suma_liste (iopk, [4088, 4090, 4091, 4093],1) ):
            if not( suma_liste (iopk, [4094,4095],1) == 0 ):
                #AOPi
                lzbir =  suma_liste (iopk, [4094,4095],1) 
                dzbir =  0
                razlika = lzbir - dzbir
                form_errors.append('AOP (4094 + 4095) = 0, ako je AOP (4087 + 4089 + 4092) = AOP-u (4088 + 4090 + 4091 + 4093) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40120
        if( aop(iopk,4094,1) > 0 ):
            if not( aop(iopk,4095,1) == 0 ):
                lzbir =  aop(iopk,4095,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4094 > 0, onda je AOP 4095 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije s vlasnicima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40121
        if( aop(iopk,4095,1) > 0 ):
            if not( aop(iopk,4094,1) == 0 ):
                lzbir =  aop(iopk,4094,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4095 > 0, onda je AOP 4094 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije s vlasnicima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40122
        if( suma_liste (iopk, [4119, 4121, 4124],1) > suma_liste (iopk, [4120, 4122, 4123, 4125],1) ):
            if not( aop(iopk,4126,1) == ( suma_liste (iopk, [4119, 4121, 4124],1) - suma_liste (iopk, [4120, 4122, 4123, 4125],1) ) ):
                #AOPi
                lzbir =  aop(iopk,4126,1) 
                dzbir =  ( suma_liste (iopk, [4119, 4121, 4124],1) - suma_liste (iopk, [4120, 4122, 4123, 4125],1) ) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4126 = AOP-u (4119 - 4120 + 4121 - 4122 - 4123 + 4124 - 4125), ako je AOP (4119 + 4121 + 4124) > AOP-a (4120 + 4122 + 4123 + 4125)  ')
        
        #40123
        if( suma_liste (iopk, [4119, 4121, 4124],1) < suma_liste (iopk, [4120, 4122, 4123, 4125],1) ):
            if not( aop(iopk,4127,1) == ( suma_liste (iopk, [4120, 4122, 4123, 4125],1) - suma_liste (iopk, [4119, 4121, 4124],1)  ) ):
                #AOPi
                lzbir = aop(iopk,4127,1)
                dzbir =  ( suma_liste (iopk, [4120, 4122, 4123, 4125],1) - suma_liste (iopk, [4119, 4121, 4124],1)  )
                razlika = lzbir - dzbir
                form_errors.append('AOP 4127 = AOP-u (4120 - 4119 - 4121 + 4122 + 4123 - 4124 + 4125), ako je AOP (4119 + 4121 + 4124) < AOP-a (4120 + 4122 + 4123 + 4125)  ')
        
        #40124
        if( suma_liste (iopk, [4119, 4121, 4124],1) == suma_liste (iopk, [4120, 4122, 4123, 4125],1) ):
            if not( suma_liste (iopk, [4126,4127],1) == 0 ):
                #AOPi
                lzbir =  suma_liste (iopk, [4126,4127],1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4126 + 4127) = 0, ako je AOP (4119 + 4121 + 4124) = AOP-u (4120 + 4122 + 4123 + 4125) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40125
        if( aop(iopk,4126,1) > 0 ):
            if not( aop(iopk,4127,1) == 0 ):
                lzbir =  aop(iopk,4127,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4126 > 0, onda je AOP 4127 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije s vlasnicima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40126
        if( aop(iopk,4127,1) > 0 ):
            if not( aop(iopk,4126,1) == 0 ):
                lzbir =  aop(iopk,4126,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4127 > 0, onda je AOP 4126 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije s vlasnicima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40127
        if( suma_liste (iopk,[4193, 4195, 4198],1) > suma_liste (iopk,[4194, 4196, 4197, 4199],1) ):
            if not( aop(iopk,4200,1) == (suma_liste (iopk,[4193, 4195, 4198],1) - suma_liste (iopk,[4194, 4196, 4197, 4199],1)) ):
                #AOPi
                lzbir =  aop(iopk,4200,1) 
                dzbir =  (suma_liste (iopk,[4193, 4195, 4198],1) - suma_liste (iopk,[4194, 4196, 4197, 4199],1)) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4200 = AOP-u (4193 - 4194 + 4195 - 4196 - 4197 + 4198 - 4199), ako je AOP (4193 + 4195 + 4198) > AOP-a (4194 + 4196 + 4197 + 4199)  ')
        
        #40128
        if( suma_liste (iopk,[4193, 4195, 4198],1) < suma_liste (iopk,[4194, 4196, 4197, 4199],1) ):
            if not( aop(iopk,4201,1) == (  suma_liste(iopk,[4194, 4196, 4197, 4199],1) - suma_liste (iopk,[4193, 4195, 4198],1) ) ):
                #AOPi
                lzbir =  aop(iopk,4201,1) 
                dzbir =  (  suma_liste(iopk,[4194, 4196, 4197, 4199],1) - suma_liste (iopk,[4193, 4195, 4198],1) ) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4201 = AOP-u (4194 - 4193 - 4195 + 4196 + 4197 - 4198 + 4199), ako je AOP (4193 + 4195 + 4198) < AOP-a (4194 + 4196 + 4197 + 4199)  ')
        
        #40129
        if( suma_liste (iopk,[4193, 4195, 4198],1) == suma_liste (iopk,[4194, 4196, 4197, 4199],1) ):
            if not( suma_liste (iopk,[4200,4201],1) == 0 ):
                #AOPi
                lzbir =  suma_liste (iopk,[4200,4201],1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4200 + 4201) = 0, ako je AOP (4193 + 4195 + 4198) = AOP-u (4194 + 4196 + 4197 + 4199) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40130
        if( aop(iopk,4200,1) > 0 ):
            if not( aop(iopk,4201,1) == 0 ):
                lzbir =  aop(iopk,4201,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4200 > 0, onda je AOP 4201 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije s vlasnicima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40131
        if( aop(iopk,4201,1) > 0 ):
            if not( aop(iopk,4200,1) == 0 ):
                lzbir =  aop(iopk,4200,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4201 > 0, onda je AOP 4200 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije s vlasnicima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40132
        if( suma_liste (iopk, [4231, 4233, 4236],1) > suma_liste (iopk, [4232, 4234, 4235, 4237],1) ):
            if not( aop(iopk,4238,1) == (suma_liste (iopk, [4231, 4233, 4236],1) - suma_liste (iopk, [4232, 4234, 4235, 4237],1)) ):
                #AOPi
                lzbir =  aop(iopk,4238,1) 
                dzbir =  (suma_liste (iopk, [4231, 4233, 4236],1) - suma_liste (iopk, [4232, 4234, 4235, 4237],1)) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4238 = AOP-u (4231 - 4232 + 4233 - 4234 - 4235 + 4236 - 4237), ako je AOP (4231 + 4233 + 4236) > AOP-a (4232 + 4234 + 4235 + 4237)  ')
        
        #40133
        if( suma_liste (iopk, [4231, 4233, 4236],1) < suma_liste (iopk, [4232, 4234, 4235, 4237],1) ):
            if not( aop(iopk,4239,1) == ( suma_liste(iopk, [4232, 4234, 4235, 4237],1) -suma_liste (iopk, [4231, 4233, 4236],1) ) ):
                #AOPi
                lzbir =  aop(iopk,4239,1) 
                dzbir =  (  suma_liste(iopk, [4232, 4234, 4235, 4237],1) -suma_liste (iopk, [4231, 4233, 4236],1) ) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 4239= AOP-u (4232 - 4231 - 4233 + 4234 + 4235 - 4236 + 4237), ako je AOP (4231 + 4233 + 4236) < AOP-a (4232 + 4234 + 4235 + 4237)  ')
        
        #40134
        if( suma_liste (iopk, [4231, 4233, 4236],1) == suma_liste (iopk, [4232, 4234, 4235, 4237],1) ):
            if not( suma_liste (iopk, [4238,4239],1) == 0):
                #AOPi
                lzbir =  suma_liste (iopk, [4238,4239],1) 
                dzbir =  0
                razlika = lzbir - dzbir
                form_errors.append('AOP (4238 + 4239) = 0, ako je AOP (4231 + 4233 + 4236) = AOP-u (4232 + 4234 + 4235 + 4237) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40135
        if( aop(iopk,4238,1) > 0 ):
            if not( aop(iopk,4239,1) == 0 ):
                lzbir =  aop(iopk,4239,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4238 > 0, onda je AOP 4239 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije s vlasnicima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40136
        if( aop(iopk,4239,1) > 0 ):
            if not( aop(iopk,4238,1) == 0 ):
                lzbir =  aop(iopk,4238,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4239 > 0, onda je AOP 4238 = 0 Ne mogu biti istovremeno prikazane pozitivne i negativne transakcije s vlasnicima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40137
        #Za ovaj set se ne primenjuje pravilo 
        
        #40138
        #Za ovaj set se ne primenjuje pravilo 
        
        #40139
        #Za ovaj set se ne primenjuje pravilo 
        
        #40140
        #Za ovaj set se ne primenjuje pravilo 
        
        #40141
        #Za ovaj set se ne primenjuje pravilo 
        
        #40142 
        if not( aop(iopk,4032,1) == ( suma_liste (iopk, [4022,4030],1) - aop(iopk,4031,1)) ):
            #AOPi
            lzbir =  aop(iopk,4032,1) 
            dzbir =  ( suma_liste (iopk, [4022,4030],1) - aop(iopk,4031,1)) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4032 = AOP-u (4022 + 4030 - 4031)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40143 
        if not( aop(iopk,4064,1) == ( suma_liste (iopk, [4054,4062],1) - aop(iopk,4063,1)) ):
            #AOPi
            lzbir =  aop(iopk,4064,1) 
            dzbir =  ( suma_liste (iopk, [4054,4062],1) - aop(iopk,4063,1)) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4064 = AOP-u (4054 + 4062 - 4063)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40144 
        if not( aop(iopk,4096,1) == ( suma_liste (iopk, [4086,4094],1) - aop(iopk,4095,1)) ):
            #AOPi
            lzbir =  aop(iopk,4096,1) 
            dzbir =  ( suma_liste (iopk, [4086,4094],1) - aop(iopk,4095,1)) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4096 = AOP-u (4086 + 4094 - 4095)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40145 
        if not( aop(iopk,4128,1) == ( suma_liste (iopk, [4118,4126],1) - aop(iopk,4127,1)) ):
            #AOPi
            lzbir =  aop(iopk,4128,1) 
            dzbir =  ( suma_liste (iopk, [4118,4126],1) - aop(iopk,4127,1)) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4128 = AOP-u (4118 + 4126 - 4127)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40146 
        if not( aop(iopk,4146,1) == ( suma_liste (iopk, [4143,4144],1) - aop(iopk,4145,1)) ):
            #AOPi
            lzbir =  aop(iopk,4146,1) 
            dzbir =  ( suma_liste (iopk, [4143,4144],1) - aop(iopk,4145,1)) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4146 = AOP-u (4143 + 4144 - 4145)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40147 
        if not( aop(iopk,4164,1) == ( suma_liste (iopk, [4161,4163],1) - aop(iopk,4162,1)) ):
            #AOPi
            lzbir =  aop(iopk,4164,1) 
            dzbir =  ( suma_liste (iopk, [4161,4163],1) - aop(iopk,4162,1)) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4164 = AOP-u (4161 - 4162 + 4163)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40148 
        if not( aop(iopk,4202,1) == (suma_liste (iopk, [4189,4190,4191,4200],1) - suma_liste (iopk, [4192,4201],1)) ):
            #AOPi
            lzbir =  aop(iopk,4202,1) 
            dzbir =  (suma_liste (iopk, [4189,4190,4191,4200],1) - suma_liste (iopk, [4192,4201],1)) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4202 = AOP-u (4189 + 4190 + 4191 - 4192 +  4200 - 4201)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40149 
        if not( aop(iopk,4240,1) == (suma_liste (iopk, [4227,4228,4229,4238],1) - suma_liste (iopk, [4230,4239],1)) ):
            #AOPi
            lzbir =  aop(iopk,4240,1) 
            dzbir =  (suma_liste (iopk, [4227,4228,4229,4238],1) - suma_liste (iopk, [4230,4239],1)) 
            razlika = lzbir - dzbir
            form_errors.append("    AOP 4240 = AOP-u (4227 + 4228 + 4229 - 4230 + 4238 - 4239)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40151 
        if( suma_liste (iopk, [4032, 4096, 4128, 4146, 4202, 4284],1) > suma_liste (iopk, [4064, 4164, 4240],1) ):
            if not( aop(iopk,4290,1) == (suma_liste (iopk, [4032, 4096, 4128, 4146, 4202, 4284],1) - suma_liste (iopk, [4064, 4164, 4240],1)) ):
                #AOPi
                lzbir =  aop(iopk,4290,1) 
                dzbir =  (suma_liste (iopk, [4032, 4096, 4128, 4146, 4202, 4284],1) - suma_liste (iopk, [4064, 4164, 4240],1)) 
                razlika = lzbir - dzbir
                form_errors.append("    AOP 4290 = AOP-u (4032 - 4064 + 4096 + 4128 + 4146 - 4164 + 4202 - 4240 + 4284), ako je AOP (4032 + 4096 + 4128 + 4146 + 4202 + 4284) > AOP-a (4064 + 4164 + 4240)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40152 
        if( suma_liste (iopk, [4032, 4096, 4128, 4146, 4202, 4284],1) < suma_liste (iopk, [4064, 4164, 4240],1) ):
            if not( aop(iopk,4296,1) == ( -suma_liste (iopk, [4032, 4096, 4128, 4146, 4202, 4284],1) + suma_liste (iopk, [4064, 4164, 4240],1)) ):
                #AOPi
                lzbir =  aop(iopk,4296,1) 
                dzbir =  ( -suma_liste (iopk, [4032, 4096, 4128, 4146, 4202, 4284],1) + suma_liste (iopk, [4064, 4164, 4240],1)) 
                razlika = lzbir - dzbir
                form_errors.append("    AOP 4296 = AOP-u (4064 - 4032 - 4096 - 4128 - 4146 + 4164 - 4202 + 4240 - 4284), ako je AOP (4032 + 4096 + 4128 + 4146 + 4202 + 4284) < AOP-a (4064 + 4164 + 4240)        "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40153 
        if( suma_liste (iopk, [4032, 4096, 4128, 4146, 4202, 4284],1) == suma_liste (iopk, [4064, 4164, 4240],1) ):
            if not( suma_liste (iopk, [4290,4296],1) == 0 ):
                #AOPi
                lzbir =  suma_liste (iopk, [4290,4296],1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append("    AOP (4290 + 4296) = 0, ako je AOP  (4032 + 4096 + 4128 + 4146 + 4202 + 4284) = AOP-u (4064 + 4164 + 4240)    Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake    "  + "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ")")

        #40154
        if( aop(iopk,4290,1) > 0 ):
            if not( aop(iopk,4296,1) == 0 ):
                lzbir =  aop(iopk,4296,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4290 > 0, onda je AOP 4296 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40155
        if( aop(iopk,4296,1) > 0 ):
            if not( aop(iopk,4290,1) == 0 ):
                lzbir =  aop(iopk,4290,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 4296 > 0, onda je AOP 4290 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i ukupan nedostatak kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40156
        if not (suma(iopk, 4241, 4284, 1) == 0):
            #AOPi
            lzbir =  suma(iopk, 4241, 4284, 1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('Zbir podataka na oznakama za AOP (4241 do 4284) = 0 Učešće bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40157
        if not( aop(iopk,4006,1) + aop(iopk,4070,1) == aop(bs,414,7) ):
            lzbir =  aop(iopk,4006,1) + aop(iopk,4070,1) 
            dzbir =  aop(bs,414,7) 
            razlika = lzbir - dzbir
            form_warnings.append('AOP (4006 + 4070) = AOP-u 0414 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40158
        if not( aop(iopk,4038,1) == aop(bs,415,7) ):
            lzbir =  aop(iopk,4038,1) 
            dzbir =  aop(bs,415,7) 
            razlika = lzbir - dzbir
            form_warnings.append('AOP 4038 = AOP-u 0415 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40159
        if( suma_liste (iopk, [4102,4134],1) >= aop(iopk,4152,1) ):
            if not( (suma_liste (iopk, [4102,4134],1) - aop(iopk,4152,1)) == aop(bs,418,7)):
                #AOPi
                lzbir =  suma_liste (iopk, [4102,4134],1) - aop(iopk,4152,1)
                dzbir =  aop(bs,418,7)
                razlika = lzbir - dzbir
                form_warnings.append('AOP (4102 + 4134 - 4152) = AOP-u 0418 kol. 7 bilansa stanja, ako je AOP (4102 + 4134)  ≥  AOP-a 4152  Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  ')
        
        #40160
        if( suma_liste (iopk, [4102,4134],1) < aop(iopk,4152,1) ):
            if not( ( aop(iopk, 4152, 1)-aop(iopk, 4102, 1)-aop(iopk, 4134, 1)) == aop(bs,419,7) ):
                #AOPi
                lzbir =  aop(iopk, 4152, 1)-aop(iopk, 4102, 1)-aop(iopk, 4134, 1)
                dzbir =  aop(bs,419,7)
                razlika = lzbir - dzbir
                form_warnings.append('AOP (4152 - 4102 - 4134) = AOP-u 0419 kol. 7 bilansa stanja, ako je AOP (4102 + 4134) < AOP-a 4152  Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  ')
        
        #40161
        if not( aop(iopk,4170,1) == aop(bs,416,7) ):
            lzbir =  aop(iopk,4170,1) 
            dzbir =  aop(bs,416,7) 
            razlika = lzbir - dzbir
            form_warnings.append('AOP 4170 = AOP-u 0416 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40162
        if not( aop(iopk,4208,1) == aop(bs,417,7) ):
            lzbir =  aop(iopk,4208,1) 
            dzbir =  aop(bs,417,7) 
            razlika = lzbir - dzbir
            form_warnings.append('AOP 4208 = AOP-u 0417 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40163
        #Za ovaj set se ne primenjuje pravilo 
        
        #40164
        if not( aop(iopk,4286,1) == aop(bs,421,7) ):
            lzbir =  aop(iopk,4286,1) 
            dzbir =  aop(bs,421,7) 
            razlika = lzbir - dzbir
            form_warnings.append('AOP 4286 = AOP-u 0421 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40165
        if not( aop(iopk,4292,1) == aop(bs,422,7) ):
            lzbir =  aop(iopk,4292,1) 
            dzbir =  aop(bs,422,7) 
            razlika = lzbir - dzbir
            form_warnings.append('AOP 4292 = AOP-u 0422 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40166
        if not( aop(iopk,4016,1) + aop(iopk,4080,1) == aop(bs,414,6) ):
            lzbir =  aop(iopk,4016,1) + aop(iopk,4080,1) 
            dzbir =  aop(bs,414,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (4016 + 4080) = AOP-u 0414 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40167
        if not( aop(iopk,4048,1) == aop(bs,415,6) ):
            lzbir =  aop(iopk,4048,1) 
            dzbir =  aop(bs,415,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4048 = AOP-u 0415 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40168
        if( suma_liste (iopk, [4112, 4137],1) >= aop(iopk,4155,1) ):
            if not( (suma_liste (iopk, [4112,4137],1) - aop(iopk,4155,1)) == aop(bs,418,6) ):
                #AOPi
                lzbir =  suma_liste (iopk, [4112,4137],1) - aop(iopk,4155,1)
                dzbir =  aop(bs,418,6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4112 + 4137 - 4155) = AOP-u 0418 kol. 6 bilansa stanja, ako je AOP (4112 + 4137) ≥ AOP-a 4155 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju ')
        
        #40169
        if( suma_liste(iopk, [4112,4137],1) < aop(iopk,4155,1) ):
            if not( ( aop(iopk,4155,1) - suma_liste (iopk, [4112,4137],1) ) == aop(bs,419,6) ):
                #AOPi
                lzbir =  aop(iopk,4155,1) - suma_liste (iopk, [4112,4137],1)
                dzbir =  aop(bs,419,6)
                razlika = lzbir - dzbir
                form_errors.append('AOP (4155 - 4112 - 4137) = AOP-u 0419 kol. 6 bilansa stanja, ako je AOP (4112 + 4137) < AOP-a 4155 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju ')
        
        #40170
        if not( aop(iopk,4183,1) == aop(bs,416,6) ):
            lzbir =  aop(iopk,4183,1) 
            dzbir =  aop(bs,416,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4183 = AOP-u 0416 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40171
        if not( aop(iopk,4221,1) == aop(bs,417,6) ):
            lzbir =  aop(iopk,4221,1) 
            dzbir =  aop(bs,417,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4221 = AOP-u 0417 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40172
        #Za ovaj set se ne primenjuje pravilo 
        
        #40173
        if not( aop(iopk,4287,1) == aop(bs,421,6) ):
            lzbir =  aop(iopk,4287,1) 
            dzbir =  aop(bs,421,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4287 = AOP-u 0421 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40174
        if not( aop(iopk,4293,1) == aop(bs,422,6) ):
            lzbir =  aop(iopk,4293,1) 
            dzbir =  aop(bs,422,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4293 = AOP-u 0422 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40175
        if not( aop(iopk,4032,1) + aop(iopk,4096,1) == aop(bs,414,5) ):
            lzbir =  aop(iopk,4032,1) + aop(iopk,4096,1) 
            dzbir =  aop(bs,414,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (4032 + 4096) = AOP-u 0414 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40176
        if not( aop(iopk,4064,1) == aop(bs,415,5) ):
            lzbir =  aop(iopk,4064,1) 
            dzbir =  aop(bs,415,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4064 = AOP-u 0415 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40177
        if( suma_liste(iopk, [4128,4146],1) >= aop(iopk,4164,1) ):
            if not( (suma_liste(iopk, [4128,4146],1) - aop(iopk,4164,1)) == aop(bs,418,5) ):
                #AOPi
                lzbir =  (suma_liste(iopk, [4128,4146],1) - aop(iopk,4164,1)) 
                dzbir =  aop(bs,418,5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4128 + 4146 - 4164) = AOP-u 0418 kol. 5 bilansa stanja, ako je AOP (4128 + 4146) ≥ AOP-a 4164 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  ')
        
        #40178
        if( suma_liste(iopk, [4128,4146],1) < aop(iopk,4164,1) ):
            if not( ( aop(iopk, 4164, 1) - aop(iopk, 4128, 1)- aop(iopk, 4146, 1)) == aop(bs,419,5) ):
                #AOPi
                lzbir =  ( aop(iopk, 4164, 1)- aop(iopk, 4128, 1)- aop(iopk, 4146, 1)) 
                dzbir =  aop(bs,419,5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP (4164 - 4128 - 4146) = AOP-u 0419 kol. 5 bilansa stanja, ako je AOP (4128 + 4146) < AOP-a 4164 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  ')
        
        #40179
        if not( aop(iopk,4202,1) == aop(bs,416,5) ):
            lzbir =  aop(iopk,4202,1) 
            dzbir =  aop(bs,416,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4202 = AOP-u 0416 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40180
        if not( aop(iopk,4240,1) == aop(bs,417,5) ):
            lzbir =  aop(iopk,4240,1) 
            dzbir =  aop(bs,417,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4240 = AOP-u 0417 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40181
        #Za ovaj set se ne primenjuje pravilo 
        
        #40182
        if not( aop(iopk,4290,1) == aop(bs,421,5) ):
            lzbir =  aop(iopk,4290,1) 
            dzbir =  aop(bs,421,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4290 = AOP-u 0421 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40183
        if not( aop(iopk,4296,1) == aop(bs,422,5) ):
            lzbir =  aop(iopk,4296,1) 
            dzbir =  aop(bs,422,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4296 = AOP-u 0422 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40184
        if not( aop(iopk,4171,1) == aop(bu,1041,6) ):
            lzbir =  aop(iopk,4171,1) 
            dzbir =  aop(bu,1041,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4171 = AOP-u 1041 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40185
        if not( aop(iopk,4209,1) == aop(bu,1042,6) ):
            lzbir =  aop(iopk,4209,1) 
            dzbir =  aop(bu,1042,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4209 = AOP-u 1042 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40186
        if not( aop(iopk,4190,1) == aop(bu,1041,5) ):
            lzbir =  aop(iopk,4190,1) 
            dzbir =  aop(bu,1041,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4190 = AOP-u 1041 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40187
        if not( aop(iopk,4228,1) == aop(bu,1042,5) ):
            lzbir =  aop(iopk,4228,1) 
            dzbir =  aop(bu,1042,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4228 = AOP-u 1042 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40188
        #Za ovaj set se ne primenjuje pravilo 
        
        #40189
        #Za ovaj set se ne primenjuje pravilo 
        
        #40190
        #Za ovaj set se ne primenjuje pravilo 
        
        #40191
        #Za ovaj set se ne primenjuje pravilo 
        
        #40192
        #Za ovaj set se ne primenjuje pravilo 
        
        #40193
        #Za ovaj set se ne primenjuje pravilo 
        
        #40194
        #Za ovaj set se ne primenjuje pravilo 
        
        #40195
        #Za ovaj set se ne primenjuje pravilo 
        
        #40196
        #Za ovaj set se ne primenjuje pravilo 
        
        #40197
        #Za ovaj set se ne primenjuje pravilo 
        
        #40198
        #Za ovaj set se ne primenjuje pravilo 
        
        #40199
        if not( aop(iopk,4173,1) == 0 ):
            lzbir =  aop(iopk,4173,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4173 = 0 Dobitak ne može biti smanjen usled ukidanja rezervi  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40200
        if not( aop(iopk,4210,1) == 0 ):
            lzbir =  aop(iopk,4210,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4210 = 0 Gubitak ne može biti povećan usled ukidanja rezervi  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40201
        if not( aop(iopk,4192,1) == 0 ):
            lzbir =  aop(iopk,4192,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4192 = 0 Dobitak ne može biti smanjen usled ukidanja rezervi  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #40202
        if not( aop(iopk,4229,1) == 0 ):
            lzbir =  aop(iopk,4229,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 4229 = 0 Gubitak ne može biti povećan usled ukidanja rezervi  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #STATISTIČKI IZVEŠTAJ - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        #90001
        if not( suma(si,9001,9045,4) > 0 ):
            form_warnings.append('Zbir podataka na oznakama za AOP (9001 do 9045) kol. 4 > 0 Statistički izveštaj, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga ')
        
        #90002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(si,9001,9045,5) == 0 ):
                lzbir =  suma(si,9001,9045,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Zbir podataka na oznakama za AOP (9001 do 9045) kol. 5 = 0 Statistički izveštaj za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #90003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(si,9001,9045,5) > 0 ):
                form_warnings.append('Zbir podataka na oznakama za AOP (9001 do 9045) kol. 5 > 0 Statistički izveštaj, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga ')
        
        #90004
        if not( aop(si,9009,4) <= aop(si,9008,4) ):
            form_errors.append('AOP 9009 kol. 4 ≤ AOP-a 9008 kol. 4  ')
        
        #90005
        if not( aop(si,9009,5) <= aop(si,9008,5) ):
            form_errors.append('AOP 9009 kol. 5 ≤ AOP-a 9008 kol. 5  ')
        
        #90006
        if not( aop(si,9010,4) <= aop(si,9009,4) ):
            form_errors.append('AOP 9010 kol. 4 ≤ AOP-a 9009 kol. 4  ')
        
        #90007
        if not( aop(si,9010,5) <= aop(si,9009,5) ):
            form_errors.append('AOP 9010 kol. 5 ≤ AOP-a 9009 kol. 5  ')
        
        #90008
        if not( suma(si,9013,9017,4) <= aop(si,9012,4) ):
            form_errors.append('AOP (9013 + 9014 + 9015 + 9016 + 9017) kol. 4 ≤ AOP-a 9012 kol. 4   ')
        
        #90009
        if not( suma(si,9013,9017,5) <= aop(si,9012,5) ):
            form_errors.append('AOP (9013 + 9014 + 9015 + 9016 + 9017) kol. 5 ≤ AOP-a 9012 kol. 5  ')
        
        #90010
        if not( aop(si,9024,4) <= aop(si,9023,4) ):
            form_errors.append('AOP 9024 kol. 4 ≤ AOP-u 9023 kol. 4  ')
        
        #90011
        if not( aop(si,9024,5) <= aop(si,9023,5) ):
            form_errors.append('AOP 9024 kol. 5 ≤ AOP-u 9023 kol. 5  ')
        
        #90012
        if( aop(si,9033,4) > 0 ):
            if not( aop(si,9035,4) > 0 ):
                form_errors.append('Ako je AOP 9033 kol. 4 > 0, onda je AOP 9035 kol. 4 > 0 Ako je prikazan broj akcija, mora biti prikazana i vrednost akcija ')
        
        #90013
        if( aop(si,9035,4) > 0 ):
            if not( aop(si,9033,4) > 0 ):
                form_errors.append('Ako je  AOP 9035 kol. 4 > 0, onda je AOP 9033 kol. 4 > 0 Ako je prikazana vrednost akcija, mora biti prikazan broj akcija ')
        
        #90014
        if( aop(si,9033,5) > 0 ):
            if not( aop(si,9035,5) > 0 ):
                form_errors.append('Ako je AOP 9033 kol. 5 > 0, onda je AOP 9035 kol. 5 > 0 Ako je prikazan broj akcija, mora biti prikazana i vrednost akcija ')
        
        #90015
        if( aop(si,9035,5) > 0 ):
            if not( aop(si,9033,5) > 0 ):
                form_errors.append('Ako je AOP 9035 kol. 5 > 0, onda AOP 9033 kol. 5 > 0 Ako je prikazana vrednost akcija, mora biti prikazan broj akcija ')
        
        #90016
        if( aop(si,9034,4) > 0 ):
            if not( aop(si,9036,4) > 0 ):
                form_errors.append('Ako je AOP 9034 kol. 4 > 0, onda je AOP 9036 kol. 4 > 0 Ako je prikazan broj akcija, mora biti prikazana i vrednost akcija ')
        
        #90017
        if( aop(si,9036,4) > 0 ):
            if not( aop(si,9034,4) > 0 ):
                form_errors.append('Ako je AOP 9036 kol. 4 > 0, onda je AOP 9034 kol. 4 > 0 Ako je prikazana vrednost akcija, mora biti prikazan broj akcija ')
        
        #90018
        if( aop(si,9034,5) > 0 ):
            if not( aop(si,9036,5) > 0 ):
                form_errors.append('Ako je AOP 9034 kol. 5 > 0, onda je AOP 9036 kol. 5 > 0 Ako je prikazan broj akcija, mora biti prikazana i vrednost akcija ')
        
        #90019
        if( aop(si,9036,5) > 0 ):
            if not( aop(si,9034,5) > 0 ):
                form_errors.append('Ako je AOP 9036 kol. 5 > 0, onda je AOP 9034 kol. 5 > 0 Ako je prikazana vrednost akcija, mora biti prikazan broj akcija ')
        
        #90020
        if not( aop(si,9011,4) == aop(bu,1029,5) ):
            lzbir =  aop(si,9011,4) 
            dzbir =  aop(bu,1029,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 9011 kol. 4 = AOP-u 1029 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #90021
        if not( aop(si,9011,5) == aop(bu,1029,6) ):
            lzbir =  aop(si,9011,5) 
            dzbir =  aop(bu,1029,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 9011 kol. 5 = AOP-u 1029 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #90022
        if not( suma_liste(si,[9007,9008,9012,9019,9020,9021],4) <= aop(bu,1031,5) ):
            form_errors.append('AOP (9007 + 9008 + 9012 + 9019 + 9020 + 9021) kol. 4 ≤ AOP-a 1031 kol. 5 bilansa uspeha  ')
        
        #90023
        if not( suma_liste(si,[9007,9008,9012,9019,9020,9021],5) <= aop(bu,1031,6) ):
            form_errors.append('AOP (9007 + 9008 + 9012 + 9019 + 9020 + 9021) kol. 5 ≤ AOP-a 1031 kol. 6 bilansa uspeha  ')
        
        #90024
        if( aop(si,9027,4) > aop(si,9022,4) ):
            if not( aop(si,9027,4)-aop(si,9022,4) == aop(bu,1017,5) ):
                lzbir =  aop(si,9027,4)-aop(si,9022,4) 
                dzbir =  aop(bu,1017,5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP (9027 - 9022) kol. 4 = AOP 1017 kol. 5 bilansa uspeha, ako je AOP 9027 kol. 4 > AOP-a 9022 kol. 4  Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #90025
        if( aop(si,9027,5) > aop(si,9022,5) ):
            if not( aop(si,9027,5)-aop(si,9022,5) == aop(bu,1017,6) ):
                lzbir =  aop(si,9027,5)-aop(si,9022,5) 
                dzbir =  aop(bu,1017,6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP (9027 - 9022) kol. 5 = AOP 1017 kol. 6 bilansa uspeha, ako je AOP 9027 kol. 5 > AOP-a 9022 kol. 5 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #90026
        if( aop(si,9027,4) < aop(si,9022,4) ):
            if not( aop(si,9022,4)-aop(si,9027,4) == aop(bu,1018,5) ):
                lzbir =  aop(si,9022,4)-aop(si,9027,4) 
                dzbir =  aop(bu,1018,5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP (9022 - 9027) kol. 4 = AOP 1018 kol. 5 bilansa uspeha, ako je AOP 9027 kol. 4 < AOP-a 9022 kol. 4  Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #90027
        if( aop(si,9027,5) < aop(si,9022,5) ):
            if not( aop(si,9022,5)-aop(si,9027,5) == aop(bu,1018,6) ):
                lzbir =  aop(si,9022,5)-aop(si,9027,5) 
                dzbir =  aop(bu,1018,6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP (9022 - 9027) kol. 5 = AOP 1018 kol. 6 bilansa uspeha, ako je AOP 9027 kol. 5 < AOP-a 9022 kol. 5  Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #90028
        if not( suma_liste(si,[9023,9025],4) <= aop(bu,1025,5) ):
            form_errors.append('AOP (9023 + 9025) kol. 4 ≤ AOP-a 1025 kol. 5 bilansa uspeha  ')
        
        #90029
        if not( suma_liste(si,[9023,9025],5) <= aop(bu,1025,6) ):
            form_errors.append('AOP (9023 + 9025) kol. 5 ≤ AOP-a 1025 kol. 6 bilansa uspeha  ')
        
        #90030
        if not( aop(si,9032,4) <= 1000 ):
            form_warnings.append('AOP 9032 kol. 4 ≤ 1.000 Granične vrednosti date su da bi se izbegle slučajne greške prilikom iskazivanja broja zaposlenih;Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih; ')
        
        #90031
        if not( aop(si,9032,5) <= 1000 ):
            form_warnings.append('AOP 9032 kol. 5 ≤ 1.000 Granične vrednosti date su da bi se izbegle slučajne greške prilikom iskazivanja broja zaposlenih;Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih; ')
        
        #90032
        if not( aop(si,9032,4) > 0 ):
            form_warnings.append('AOP 9032 kol. 4 > 0 Na poziciji Prosečan broj zaposlenih nije iskazan podatak; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga ')
        
        #90033
        if not( suma(si,9037,9045,4) == aop(iotg,3031,3) ):
            lzbir =  suma(si,9037,9045,4) 
            dzbir =  aop(iotg,3031,3) 
            razlika = lzbir - dzbir
            form_errors.append('Zbir AOP-a (9037 do 9045) kol. 4 = AOP-u 3031 kol. 3 izveštaja o tokovima gotovine Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #90034
        if not( suma(si,9037,9045,5) == aop(iotg,3031,4) ):
            lzbir =  suma(si,9037,9045,5) 
            dzbir =  aop(iotg,3031,4) 
            razlika = lzbir - dzbir
            form_errors.append('Zbir AOP-a (9037 do 9045) kol. 5 = AOP-u 3031 kol. 4 izveštaja o tokovima gotovine Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
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
        