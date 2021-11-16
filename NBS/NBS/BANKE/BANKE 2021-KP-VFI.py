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
            

        if len(form_errors)>0:
            return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors, 'exceptions': exceptionList}

        lzbir = 0
        dzbir = 0
        razlika = 0


        ######################################
        #### POCETAK KONTROLNIH PRAVILA ######
        ######################################

        #00000-1
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-2
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-3
        if not( suma(bs,1,18,5)+suma(bs,1,18,6)+suma(bs,1,18,7)+suma(bs,401,423,5)+suma(bs,401,423,6)+suma(bs,401,423,7)+suma(bu,1001,1048,5)+suma(bu,1001,1048,6) > 0 ):
            form_warnings.append('Zbir podataka na oznakama za AOP (0001 do 0018) kol. 5 + (0001 do 0018) kol. 6 + (0001 do 0018) kol. 7 bilans stanja + (0401 do 0423) kol. 5 + (0401 do 0423) kol. 6 + (0401 do 0423) kol. 7 bilansa stanja + (1001 do 1048) kol. 5 + (1001 do 1048) kol. 6 bilansa uspeha  > 0 Vanredni finansijski izveštaj, po pravilu ne sme biti bez podataka; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga')
            return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors, 'exceptions' : exceptionList}
        
        #Provera da li je fizahtev placen
        if not(Zahtev.Placen):
            form_warnings.append('Naknada za obradu i javno objavljivanje izveštaja i propisane dokumentacije nije uplaćena u propisanom iznosu. Instrukcije za uplatu propisane naknade date su u okviru PIS FI sistema za konkretan zahtev, na linku „Status naplate zahteva / Instrukcija za plaćanje". Ukoliko ste izvršili uplatu, a naknada nije uparena, priložite Dokaz o uplati naknade u delu Dokumentacija (na mestu predviđenom za dokaz o uplati naknade), kako biste mogli da podnesete izveštaj.');

        #Provera negativnih AOP-a
        lista=""
        lista_bs = find_negativni(bs, 1, 423, 5, 7)
        lista_bu = find_negativni(bu, 1001, 1048, 5, 6)
       
        if (len(lista_bs) > 0):
            lista = lista_bs
        if len(lista_bu) > 0:
            if len(lista) > 0:
                lista = lista + ", " + lista_bu
            else:
                lista = lista_bu                           
        if len(lista) > 0:                                           
            form_errors.append("Unete vrednosti ne mogu biti negativne ! (" + lista + ")")        
        
        #00000-4
        #Za ovaj set se ne primenjuje pravilo 
        
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
        if( suma(bu,1041,1042,6) == 0 ):
            if not( suma_liste(bu,[1037,1039],6) == suma_liste(bu,[1038,1040],6) ):
                lzbir =  suma_liste(bu,[1037,1039],6) 
                dzbir =  suma_liste(bu,[1038,1040],6) 
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
        
