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

        hasError = False

        ######################################
        #### POCETAK KONTROLNIH PRAVILA ######
        ######################################
        
        
        #00000-4
        if not( suma(bs,1,54,5)+suma(bs,1,54,6)+suma(bs,1,54,7)+suma(bs,401,460,5)+suma(bs,401,460,6)+suma(bs,401,460,7)+suma(bu,1001,1110,5)+suma(bu,1001,1110,6) > 0 ):
            form_warnings.append('Zbir podataka na oznakama za AOP (0001 do 0054) kol. 5 + (0001 do 0054) kol. 6 + (0001 do 0054) kol. 7 bilansa stanja + (0401 do 0460) kol. 5 + (0401 do 0460) kol. 6 + (0401 do 0460) kol. 7 bilansa stanja + (1001 do 1110) kol. 5 + (1001 do 1110) kol. 6 bilansa uspeha  > 0 Vanredni finansijski izveštaj, po pravilu ne sme biti bez podataka; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga')
            return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors, 'exceptions' : exceptionList}
        
        #00000-5
        #Za ovaj set se ne primenjuje pravilo 
        
        #Provera da li je fizahtev placen
        if not(Zahtev.Placen):
            form_warnings.append('Naknada za obradu i javno objavljivanje izveštaja i propisane dokumentacije nije uplaćena u propisanom iznosu. Instrukcije za uplatu propisane naknade date su u okviru PIS FI sistema za konkretan zahtev, na linku „Status naplate zahteva / Instrukcija za plaćanje". Ukoliko ste izvršili uplatu, a naknada nije uparena, priložite Dokaz o uplati naknade u delu Dokumentacija (na mestu predviđenom za dokaz o uplati naknade), kako biste mogli da podnesete izveštaj.');

        #Provera negativnih AOP-a
        lista=""
        lista_bs = find_negativni(bs, 1, 460, 5, 7)
        lista_bu = find_negativni(bu, 1001, 1110, 5, 6)

        if (len(lista_bs) > 0):
            lista = lista_bs
        if len(lista_bu) > 0:
            if len(lista) > 0:
                lista = lista + ", " + lista_bu
            else:
                lista = lista_bu                           
        if len(lista) > 0:                                           
            form_errors.append("Unete vrednosti ne mogu biti negativne ! (" + lista + ")")

        #BILANS STANJA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #BILANS STANJA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #00001
        if not( suma(bs,1,54,5)+suma(bs,401,460,5) > 0 ):
            form_warnings.append('Zbir podataka na oznakama za AOP (0001 do 0054) kol. 5 + (0401 do 0460) kol. 5 > 0 Bilans stanja, po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga ')
        
        #00002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,54,6)+suma(bs,401,460,6) == 0 ):
                lzbir =  suma(bs,1,54,6)+suma(bs,401,460,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Zbir podataka na oznakama za AOP (0001 do 0054) kol. 6 + (0401 do 0460) kol. 6 = 0 Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00003
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,54,7)+suma(bs,401,460,7) == 0 ):
                lzbir =  suma(bs,1,54,7)+suma(bs,401,460,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Zbir podataka na oznakama za AOP (0001 do 0054) kol. 7 + (0401 do 0460) kol. 7 = 0 Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00004
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,54,6)+suma(bs,401,460,6) > 0 ):
                form_warnings.append('Zbir podataka na oznakama za AOP (0001 do 0054) kol. 6 + (0401 do 0460) kol. 6 > 0 Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga ')
        
        #00005
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,54,7)+suma(bs,401,460,7) > 0 ):
                form_warnings.append('Zbir podataka na oznakama za AOP (0001 do 0054) kol. 7 + (0401 do 0460) kol. 7 > 0 Bilans stanja, po pravilu,  mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga ')
        
        #00006
        if not( aop(bs,2,5) == suma_liste(bs,[3,4,5,6,9,10,21,22],5) ):
            lzbir =  aop(bs,2,5) 
            dzbir =  suma_liste(bs,[3,4,5,6,9,10,21,22],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0002 kol. 5 = AOP-u (0003 + 0004 + 0005 + 0006 + 0009 + 0010 + 0021 + 0022) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00007
        if not( aop(bs,2,6) == suma_liste(bs,[3,4,5,6,9,10,21,22],6) ):
            lzbir =  aop(bs,2,6) 
            dzbir =  suma_liste(bs,[3,4,5,6,9,10,21,22],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0002 kol. 6 = AOP-u (0003 + 0004 + 0005 + 0006 + 0009 + 0010 + 0021 + 0022) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00008
        if not( aop(bs,2,7) == suma_liste(bs,[3,4,5,6,9,10,21,22],7) ):
            lzbir =  aop(bs,2,7) 
            dzbir =  suma_liste(bs,[3,4,5,6,9,10,21,22],7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0002 kol. 7 = AOP-u (0003 + 0004 + 0005 + 0006 + 0009 + 0010 + 0021 + 0022) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00009
        if not( aop(bs,6,5) == suma(bs,7,8,5) ):
            lzbir =  aop(bs,6,5) 
            dzbir =  suma(bs,7,8,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0006 kol. 5 = AOP-u (0007 + 0008) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00010
        if not( aop(bs,6,6) == suma(bs,7,8,6) ):
            lzbir =  aop(bs,6,6) 
            dzbir =  suma(bs,7,8,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0006 kol. 6 = AOP-u (0007 + 0008) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00011
        if not( aop(bs,6,7) == suma(bs,7,8,7) ):
            lzbir =  aop(bs,6,7) 
            dzbir =  suma(bs,7,8,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0006 kol. 7 = AOP-u (0007 + 0008) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00012
        if not( aop(bs,10,5) == suma_liste(bs,[11,15],5) ):
            lzbir =  aop(bs,10,5) 
            dzbir =  suma_liste(bs,[11,15],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0010 kol. 5 = AOP-u (0011 + 0015) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00013
        if not( aop(bs,10,6) == suma_liste(bs,[11,15],6) ):
            lzbir =  aop(bs,10,6) 
            dzbir =  suma_liste(bs,[11,15],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0010 kol. 6 = AOP-u (0011 + 0015) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00014
        if not( aop(bs,10,7) == suma_liste(bs,[11,15],7) ):
            lzbir =  aop(bs,10,7) 
            dzbir =  suma_liste(bs,[11,15],7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0010 kol. 7 = AOP-u (0011 + 0015) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00015
        if not( aop(bs,11,5) == suma(bs,12,14,5) ):
            lzbir =  aop(bs,11,5) 
            dzbir =  suma(bs,12,14,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0011 kol. 5 = AOP-u (0012 + 0013 + 0014) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00016
        if not( aop(bs,11,6) == suma(bs,12,14,6) ):
            lzbir =  aop(bs,11,6) 
            dzbir =  suma(bs,12,14,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0011 kol. 6 = AOP-u (0012 + 0013 + 0014) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00017
        if not( aop(bs,11,7) == suma(bs,12,14,7) ):
            lzbir =  aop(bs,11,7) 
            dzbir =  suma(bs,12,14,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0011 kol. 7 = AOP-u (0012 + 0013 + 0014) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00018
        if not( aop(bs,15,5) == suma_liste(bs,[16,19,20],5) ):
            lzbir =  aop(bs,15,5) 
            dzbir =  suma_liste(bs,[16,19,20],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0015 kol. 5 = AOP-u (0016 + 0019 + 0020) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00019
        if not( aop(bs,15,6) == suma_liste(bs,[16,19,20],6) ):
            lzbir =  aop(bs,15,6) 
            dzbir =  suma_liste(bs,[16,19,20],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0015 kol. 6 = AOP-u (0016 + 0019 + 0020) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00020
        if not( aop(bs,15,7) == suma_liste(bs,[16,19,20],7) ):
            lzbir =  aop(bs,15,7) 
            dzbir =  suma_liste(bs,[16,19,20],7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0015 kol. 7 = AOP-u (0016 + 0019 + 0020) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00021
        if not( aop(bs,16,5) == suma(bs,17,18,5) ):
            lzbir =  aop(bs,16,5) 
            dzbir =  suma(bs,17,18,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0016 kol. 5 = AOP-u (0017 + 0018) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00022
        if not( aop(bs,16,6) == suma(bs,17,18,6) ):
            lzbir =  aop(bs,16,6) 
            dzbir =  suma(bs,17,18,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0016 kol. 6 = AOP-u (0017 + 0018) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00023
        if not( aop(bs,16,7) == suma(bs,17,18,7) ):
            lzbir =  aop(bs,16,7) 
            dzbir =  suma(bs,17,18,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0016 kol. 7 = AOP-u (0017 + 0018) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00024
        if not( aop(bs,23,5) == suma_liste(bs,[24,25,26,45,46,49],5) ):
            lzbir =  aop(bs,23,5) 
            dzbir =  suma_liste(bs,[24,25,26,45,46,49],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0023 kol. 5 = AOP-u (0024 + 0025 + 0026 + 0045 + 0046 + 0049) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00025
        if not( aop(bs,23,6) == suma_liste(bs,[24,25,26,45,46,49],6) ):
            lzbir =  aop(bs,23,6) 
            dzbir =  suma_liste(bs,[24,25,26,45,46,49],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0023 kol. 6 = AOP-u (0024 + 0025 + 0026 + 0045 + 0046 + 0049) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00026
        if not( aop(bs,23,7) == suma_liste(bs,[24,25,26,45,46,49],7) ):
            lzbir =  aop(bs,23,7) 
            dzbir =  suma_liste(bs,[24,25,26,45,46,49],7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0023 kol. 7 = AOP-u (0024 + 0025 + 0026 + 0045 + 0046 + 0049) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00027
        if not( aop(bs,26,5) == suma_liste(bs,[27,32,33,44],5) ):
            lzbir =  aop(bs,26,5) 
            dzbir =  suma_liste(bs,[27,32,33,44],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0026 kol. 5 = AOP-u (0027 + 0032 + 0033 + 0044) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00028
        if not( aop(bs,26,6) == suma_liste(bs,[27,32,33,44],6) ):
            lzbir =  aop(bs,26,6) 
            dzbir =  suma_liste(bs,[27,32,33,44],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0026 kol. 6 = AOP-u (0027 + 0032 + 0033 + 0044) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00029
        if not( aop(bs,26,7) == suma_liste(bs,[27,32,33,44],7) ):
            lzbir =  aop(bs,26,7) 
            dzbir =  suma_liste(bs,[27,32,33,44],7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0026 kol. 7 = AOP-u (0027 + 0032 + 0033 + 0044) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00030
        if not( aop(bs,27,5) == suma(bs,28,31,5) ):
            lzbir =  aop(bs,27,5) 
            dzbir =  suma(bs,28,31,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0027 kol. 5 = AOP-u (0028 + 0029 + 0030 + 0031) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00031
        if not( aop(bs,27,6) == suma(bs,28,31,6) ):
            lzbir =  aop(bs,27,6) 
            dzbir =  suma(bs,28,31,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0027 kol. 6 = AOP-u (0028 + 0029 + 0030 + 0031) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00032
        if not( aop(bs,27,7) == suma(bs,28,31,7) ):
            lzbir =  aop(bs,27,7) 
            dzbir =  suma(bs,28,31,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0027 kol. 7 = AOP-u (0028 + 0029 + 0030 + 0031) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00033
        if not( aop(bs,33,5) == suma_liste(bs,[34,38,42,43],5) ):
            lzbir =  aop(bs,33,5) 
            dzbir =  suma_liste(bs,[34,38,42,43],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0033 kol. 5 = AOP-u (0034 + 0038 + 0042 + 0043) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00034
        if not( aop(bs,33,6) == suma_liste(bs,[34,38,42,43],6) ):
            lzbir =  aop(bs,33,6) 
            dzbir =  suma_liste(bs,[34,38,42,43],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0033 kol. 6 = AOP-u (0034 + 0038 + 0042 + 0043) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00035
        if not( aop(bs,33,7) == suma_liste(bs,[34,38,42,43],7) ):
            lzbir =  aop(bs,33,7) 
            dzbir =  suma_liste(bs,[34,38,42,43],7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0033 kol. 7 = AOP-u (0034 + 0038 + 0042 + 0043) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00036
        if not( aop(bs,34,5) == suma(bs,35,37,5) ):
            lzbir =  aop(bs,34,5) 
            dzbir =  suma(bs,35,37,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0034 kol. 5 = AOP-u (0035 + 0036 + 0037) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00037
        if not( aop(bs,34,6) == suma(bs,35,37,6) ):
            lzbir =  aop(bs,34,6) 
            dzbir =  suma(bs,35,37,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0034 kol. 6 = AOP-u (0035 + 0036 + 0037) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00038
        if not( aop(bs,34,7) == suma(bs,35,37,7) ):
            lzbir =  aop(bs,34,7) 
            dzbir =  suma(bs,35,37,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0034 kol. 7 = AOP-u (0035 + 0036 + 0037) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00039
        if not( aop(bs,38,5) == suma(bs,39,41,5) ):
            lzbir =  aop(bs,38,5) 
            dzbir =  suma(bs,39,41,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0038 kol. 5 = AOP-u (0039 + 0040 + 0041) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00040
        if not( aop(bs,38,6) == suma(bs,39,41,6) ):
            lzbir =  aop(bs,38,6) 
            dzbir =  suma(bs,39,41,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0038 kol. 6 = AOP-u (0039 + 0040 + 0041) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00041
        if not( aop(bs,38,7) == suma(bs,39,41,7) ):
            lzbir =  aop(bs,38,7) 
            dzbir =  suma(bs,39,41,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0038 kol. 7 = AOP-u (0039 + 0040 + 0041) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00042
        if not( aop(bs,46,5) == suma(bs,47,48,5) ):
            lzbir =  aop(bs,46,5) 
            dzbir =  suma(bs,47,48,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0046 kol. 5 = AOP-u (0047 + 0048) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00043
        if not( aop(bs,46,6) == suma(bs,47,48,6) ):
            lzbir =  aop(bs,46,6) 
            dzbir =  suma(bs,47,48,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0046 kol. 6 = AOP-u (0047 + 0048) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00044
        if not( aop(bs,46,7) == suma(bs,47,48,7) ):
            lzbir =  aop(bs,46,7) 
            dzbir =  suma(bs,47,48,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0046 kol. 7 = AOP-u (0047 + 0048) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00045
        if not( aop(bs,49,5) == suma(bs,50,52,5) ):
            lzbir =  aop(bs,49,5) 
            dzbir =  suma(bs,50,52,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0049 kol. 5 = AOP-u (0050 + 0051 + 0052) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00046
        if not( aop(bs,49,6) == suma(bs,50,52,6) ):
            lzbir =  aop(bs,49,6) 
            dzbir =  suma(bs,50,52,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0049 kol. 6 = AOP-u (0050 + 0051 + 0052) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00047
        if not( aop(bs,49,7) == suma(bs,50,52,7) ):
            lzbir =  aop(bs,49,7) 
            dzbir =  suma(bs,50,52,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0049 kol. 7 = AOP-u (0050 + 0051 + 0052) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00048
        if not( aop(bs,53,5) == suma_liste(bs,[1,2,23],5) ):
            lzbir =  aop(bs,53,5) 
            dzbir =  suma_liste(bs,[1,2,23],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0053 kol. 5 = AOP-u (0001 + 0002 + 0023) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00049
        if not( aop(bs,53,6) == suma_liste(bs,[1,2,23],6) ):
            lzbir =  aop(bs,53,6) 
            dzbir =  suma_liste(bs,[1,2,23],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0053 kol. 6 = AOP-u (0001 + 0002 + 0023) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00050
        if not( aop(bs,53,7) == suma_liste(bs,[1,2,23],7) ):
            lzbir =  aop(bs,53,7) 
            dzbir =  suma_liste(bs,[1,2,23],7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0053 kol. 7 = AOP-u (0001 + 0002 + 0023) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00051
        if not( aop(bs,401,5) == suma_liste(bs,[402,407,408,411,412,414,421],5)-suma_liste(bs,[413,417,420],5) ):
            lzbir =  aop(bs,401,5) 
            dzbir =  suma_liste(bs,[402,407,408,411,412,414,421],5)-suma_liste(bs,[413,417,420],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0401 kol. 5 = AOP-u (0402 + 0407+ 0408 + 0411 + 0412 - 0413 + 0414 - 0417 - 0420 + 0421) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00052
        if not( aop(bs,401,6) == suma_liste(bs,[402,407,408,411,412,414,421],6)-suma_liste(bs,[413,417,420],6) ):
            lzbir =  aop(bs,401,6) 
            dzbir =  suma_liste(bs,[402,407,408,411,412,414,421],6)-suma_liste(bs,[413,417,420],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0401 kol. 6 = AOP-u (0402 + 0407+ 0408 + 0411 + 0412 - 0413 + 0414 - 0417 - 0420 + 0421) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00053
        if not( aop(bs,401,7) == suma_liste(bs,[402,407,408,411,412,414,421],7)-suma_liste(bs,[413,417,420],7) ):
            lzbir =  aop(bs,401,7) 
            dzbir =  suma_liste(bs,[402,407,408,411,412,414,421],7)-suma_liste(bs,[413,417,420],7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0401 kol. 7 = AOP-u (0402 + 0407+ 0408 + 0411 + 0412 - 0413 + 0414 - 0417 - 0420 + 0421) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00054
        if not( aop(bs,402,5) == suma(bs,403,406,5) ):
            lzbir =  aop(bs,402,5) 
            dzbir =  suma(bs,403,406,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0402 kol. 5 = AOP-u (0403 + 0404 + 0405 + 0406) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00055
        if not( aop(bs,402,6) == suma(bs,403,406,6) ):
            lzbir =  aop(bs,402,6) 
            dzbir =  suma(bs,403,406,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0402 kol. 6 = AOP-u (0403 + 0404 + 0405 + 0406) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00056
        if not( aop(bs,402,7) == suma(bs,403,406,7) ):
            lzbir =  aop(bs,402,7) 
            dzbir =  suma(bs,403,406,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0402 kol. 7 = AOP-u (0403 + 0404 + 0405 + 0406) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00057
        if not( aop(bs,408,5) == suma(bs,409,410,5) ):
            lzbir =  aop(bs,408,5) 
            dzbir =  suma(bs,409,410,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0408 kol. 5 = AOP-u (0409 + 0410) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00058
        if not( aop(bs,408,6) == suma(bs,409,410,6) ):
            lzbir =  aop(bs,408,6) 
            dzbir =  suma(bs,409,410,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0408 kol. 6 = AOP-u (0409 + 0410) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00059
        if not( aop(bs,408,7) == suma(bs,409,410,7) ):
            lzbir =  aop(bs,408,7) 
            dzbir =  suma(bs,409,410,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0408 kol. 7 = AOP-u (0409 + 0410) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00060
        if not( aop(bs,414,5) == suma(bs,415,416,5) ):
            lzbir =  aop(bs,414,5) 
            dzbir =  suma(bs,415,416,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0414 kol. 5 = AOP-u (0415 + 0416) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00061
        if not( aop(bs,414,6) == suma(bs,415,416,6) ):
            lzbir =  aop(bs,414,6) 
            dzbir =  suma(bs,415,416,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0414 kol. 6 = AOP-u (0415 + 0416) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00062
        if not( aop(bs,414,7) == suma(bs,415,416,7) ):
            lzbir =  aop(bs,414,7) 
            dzbir =  suma(bs,415,416,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0414 kol. 7 = AOP-u (0415 + 0416) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00063
        if not( aop(bs,417,5) == suma(bs,418,419,5) ):
            lzbir =  aop(bs,417,5) 
            dzbir =  suma(bs,418,419,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0417 kol. 5 = AOP-u (0418 + 0419) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00064
        if not( aop(bs,417,6) == suma(bs,418,419,6) ):
            lzbir =  aop(bs,417,6) 
            dzbir =  suma(bs,418,419,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0417 kol. 6 = AOP-u (0418 + 0419) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00065
        if not( aop(bs,417,7) == suma(bs,418,419,7) ):
            lzbir =  aop(bs,417,7) 
            dzbir =  suma(bs,418,419,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0417 kol. 7 = AOP-u (0418 + 0419) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00066
        if not( aop(bs,421,5) == 0 ):
            lzbir =  aop(bs,421,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0421 kol. 5 = 0 Učešće bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00067
        if not( aop(bs,421,6) == 0 ):
            lzbir =  aop(bs,421,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0421 kol. 6 = 0 Učešće bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00068
        if not( aop(bs,421,7) == 0 ):
            lzbir =  aop(bs,421,7) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0421 kol. 7 = 0 Učešće bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00069
        if not( aop(bs,422,5) == suma_liste(bs,[423,430,434,435,444,453,457],5) ):
            lzbir =  aop(bs,422,5) 
            dzbir =  suma_liste(bs,[423,430,434,435,444,453,457],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0422 kol. 5 = AOP-u (0423 + 0430 + 0434 + 0435 + 0444 + 0453 + 0457) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00070
        if not( aop(bs,422,6) == suma_liste(bs,[423,430,434,435,444,453,457],6) ):
            lzbir =  aop(bs,422,6) 
            dzbir =  suma_liste(bs,[423,430,434,435,444,453,457],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0422 kol. 6 = AOP-u (0423 + 0430 + 0434 + 0435 + 0444 + 0453 + 0457) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00071
        if not( aop(bs,422,7) == suma_liste(bs,[423,430,434,435,444,453,457],7) ):
            lzbir =  aop(bs,422,7) 
            dzbir =  suma_liste(bs,[423,430,434,435,444,453,457],7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0422 kol. 7 = AOP-u (0423 + 0430 + 0434 + 0435 + 0444 + 0453 + 0457) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00072
        if not( aop(bs,423,5) == suma(bs,424,429,5) ):
            lzbir =  aop(bs,423,5) 
            dzbir =  suma(bs,424,429,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0423 kol. 5 = AOP-u (0424 + 0425 + 0426 + 0427 + 0428 + 0429) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00073
        if not( aop(bs,423,6) == suma(bs,424,429,6) ):
            lzbir =  aop(bs,423,6) 
            dzbir =  suma(bs,424,429,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0423 kol. 6 = AOP-u (0424 + 0425 + 0426 + 0427 + 0428 + 0429) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00074
        if not( aop(bs,423,7) == suma(bs,424,429,7) ):
            lzbir =  aop(bs,423,7) 
            dzbir =  suma(bs,424,429,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0423 kol. 7 = AOP-u (0424 + 0425 + 0426 + 0427 + 0428 + 0429) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00075
        if not( aop(bs,430,5) == suma(bs,431,433,5) ):
            lzbir =  aop(bs,430,5) 
            dzbir =  suma(bs,431,433,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0430 kol. 5 = AOP-u (0431 + 0432 + 0433) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00076
        if not( aop(bs,430,6) == suma(bs,431,433,6) ):
            lzbir =  aop(bs,430,6) 
            dzbir =  suma(bs,431,433,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0430 kol. 6 = AOP-u (0431 + 0432 + 0433) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00077
        if not( aop(bs,430,7) == suma(bs,431,433,7) ):
            lzbir =  aop(bs,430,7) 
            dzbir =  suma(bs,431,433,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0430 kol. 7 = AOP-u (0431 + 0432 + 0433) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00078
        if not( aop(bs,435,5) == suma_liste(bs,[436,440,441,442,443],5) ):
            lzbir =  aop(bs,435,5) 
            dzbir =  suma_liste(bs,[436,440,441,442,443],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0435 kol. 5 = AOP-u (0436 + 0440 + 0441 + 0442 + 0443) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00079
        if not( aop(bs,435,6) == suma_liste(bs,[436,440,441,442,443],6) ):
            lzbir =  aop(bs,435,6) 
            dzbir =  suma_liste(bs,[436,440,441,442,443],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0435 kol. 6 = AOP-u (0436 + 0440 + 0441 + 0442 + 0443) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00080
        if not( aop(bs,435,7) == suma_liste(bs,[436,440,441,442,443],7) ):
            lzbir =  aop(bs,435,7) 
            dzbir =  suma_liste(bs,[436,440,441,442,443],7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0435 kol. 7 = AOP-u (0436 + 0440 + 0441 + 0442 + 0443) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00081
        if not( aop(bs,436,5) == suma(bs,437,439,5) ):
            lzbir =  aop(bs,436,5) 
            dzbir =  suma(bs,437,439,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0436 kol. 5 = AOP-u (0437 + 0438 + 0439) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00082
        if not( aop(bs,436,6) == suma(bs,437,439,6) ):
            lzbir =  aop(bs,436,6) 
            dzbir =  suma(bs,437,439,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0436 kol. 6 = AOP-u (0437 + 0438 + 0439) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00083
        if not( aop(bs,436,7) == suma(bs,437,439,7) ):
            lzbir =  aop(bs,436,7) 
            dzbir =  suma(bs,437,439,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0436 kol. 7 = AOP-u (0437 + 0438 + 0439) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00084
        if not( aop(bs,444,5) == suma_liste(bs,[445,449,450],5) ):
            lzbir =  aop(bs,444,5) 
            dzbir =  suma_liste(bs,[445,449,450],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0444 kol. 5 = AOP-u (0445 + 0449 + 0450) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00085
        if not( aop(bs,444,6) == suma_liste(bs,[445,449,450],6) ):
            lzbir =  aop(bs,444,6) 
            dzbir =  suma_liste(bs,[445,449,450],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0444 kol. 6 = AOP-u (0445 + 0449 + 0450) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00086
        if not( aop(bs,444,7) == suma_liste(bs,[445,449,450],7) ):
            lzbir =  aop(bs,444,7) 
            dzbir =  suma_liste(bs,[445,449,450],7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0444 kol. 7 = AOP-u (0445 + 0449 + 0450) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00087
        if not( aop(bs,445,5) == suma(bs,446,448,5) ):
            lzbir =  aop(bs,445,5) 
            dzbir =  suma(bs,446,448,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0445 kol. 5 = AOP-u (0446 + 0447 + 0448) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00088
        if not( aop(bs,445,6) == suma(bs,446,448,6) ):
            lzbir =  aop(bs,445,6) 
            dzbir =  suma(bs,446,448,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0445 kol. 6 = AOP-u (0446 + 0447 + 0448) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00089
        if not( aop(bs,445,7) == suma(bs,446,448,7) ):
            lzbir =  aop(bs,445,7) 
            dzbir =  suma(bs,446,448,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0445 kol. 7 = AOP-u (0446 + 0447 + 0448) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00090
        if not( aop(bs,450,5) == suma(bs,451,452,5) ):
            lzbir =  aop(bs,450,5) 
            dzbir =  suma(bs,451,452,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0450 kol. 5 = AOP-u (0451 + 0452) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00091
        if not( aop(bs,450,6) == suma(bs,451,452,6) ):
            lzbir =  aop(bs,450,6) 
            dzbir =  suma(bs,451,452,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0450 kol. 6 = AOP-u (0451 + 0452) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00092
        if not( aop(bs,450,7) == suma(bs,451,452,7) ):
            lzbir =  aop(bs,450,7) 
            dzbir =  suma(bs,451,452,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0450 kol. 7 = AOP-u (0451 + 0452) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00093
        if not( aop(bs,453,5) == suma(bs,454,456,5) ):
            lzbir =  aop(bs,453,5) 
            dzbir =  suma(bs,454,456,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0453 kol. 5 = AOP-u (0454 + 0455 + 0456) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00094
        if not( aop(bs,453,6) == suma(bs,454,456,6) ):
            lzbir =  aop(bs,453,6) 
            dzbir =  suma(bs,454,456,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0453 kol. 6 = AOP-u (0454 + 0455 + 0456) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00095
        if not( aop(bs,453,7) == suma(bs,454,456,7) ):
            lzbir =  aop(bs,453,7) 
            dzbir =  suma(bs,454,456,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0453 kol. 7 = AOP-u (0454 + 0455 + 0456) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00096
        if( aop(bs,401,5) > 0 ):
            if not( aop(bs,458,5) == 0 ):
                lzbir =  aop(bs,458,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0401 kol. 5 > 0, onda je AOP 0458 kol. 5 = 0 Ne mogu biti istovremeno prikazani kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00097
        if( aop(bs,458,5) > 0 ):
            if not( aop(bs,401,5) == 0 ):
                lzbir =  aop(bs,401,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0458 kol. 5 > 0, onda je AOP 0401 kol. 5 = 0 Ne mogu biti istovremeno prikazani kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00098
        if( aop(bs,401,6) > 0 ):
            if not( aop(bs,458,6) == 0 ):
                lzbir =  aop(bs,458,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0401 kol. 6 > 0, onda je AOP 0458 kol. 6 = 0 Ne mogu biti istovremeno prikazani kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00099
        if( aop(bs,458,6) > 0 ):
            if not( aop(bs,401,6) == 0 ):
                lzbir =  aop(bs,401,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0458 kol. 6 > 0, onda je AOP 0401 kol. 6 = 0 Ne mogu biti istovremeno prikazani kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00100
        if( aop(bs,401,7) > 0 ):
            if not( aop(bs,458,7) == 0 ):
                lzbir =  aop(bs,458,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 0401 kol. 7 > 0, onda je AOP 0458 kol. 7 = 0 Ne mogu biti istovremeno prikazani kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00101
        if( aop(bs,458,7) > 0 ):
            if not( aop(bs,401,7) == 0 ):
                lzbir =  aop(bs,401,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako jeAOP 0458 kol. 7 > 0, onda je AOP 0401 kol. 7 = 0 Ne mogu biti istovremeno prikazani kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00102
        if not( aop(bs,459,5) == suma_liste(bs,[401,422],5)-aop(bs,458,5) ):
            lzbir =  aop(bs,459,5) 
            dzbir =  suma_liste(bs,[401,422],5)-aop(bs,458,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0459 kol. 5 = AOP-u (0401 + 0422 - 0458) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00103
        if not( aop(bs,459,6) == suma_liste(bs,[401,422],6)-aop(bs,458,6) ):
            lzbir =  aop(bs,459,6) 
            dzbir =  suma_liste(bs,[401,422],6)-aop(bs,458,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0459 kol. 6 = AOP-u (0401 + 0422 - 0458) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00104
        if not( aop(bs,459,7) == suma_liste(bs,[401,422],7)-aop(bs,458,7) ):
            lzbir =  aop(bs,459,7) 
            dzbir =  suma_liste(bs,[401,422],7)-aop(bs,458,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0459 kol. 7 = AOP-u (0401 + 0422 - 0458) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00105
        if not( aop(bs,53,5) == aop(bs,459,5) ):
            lzbir =  aop(bs,53,5) 
            dzbir =  aop(bs,459,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0053 kol. 5 = AOP-u 0459 kol. 5  Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00106
        if not( aop(bs,53,6) == aop(bs,459,6) ):
            lzbir =  aop(bs,53,6) 
            dzbir =  aop(bs,459,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0053 kol. 6 = AOP-u 0459 kol. 6 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00107
        if not( aop(bs,53,7) == aop(bs,459,7) ):
            lzbir =  aop(bs,53,7) 
            dzbir =  aop(bs,459,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0053 kol. 7 = AOP-u 0459 kol. 7 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00108
        if not( aop(bs,54,5) == aop(bs,460,5) ):
            lzbir =  aop(bs,54,5) 
            dzbir =  aop(bs,460,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0054 kol. 5 = AOP-u 0460 kol. 5  Kontrolno pravilo zahteva slaganje vanbilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00109
        if not( aop(bs,54,6) == aop(bs,460,6) ):
            lzbir =  aop(bs,54,6) 
            dzbir =  aop(bs,460,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0054 kol. 6 = AOP-u 0460 kol. 6 Kontrolno pravilo zahteva slaganje vanbilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00110
        if not( aop(bs,54,7) == aop(bs,460,7) ):
            lzbir =  aop(bs,54,7) 
            dzbir =  aop(bs,460,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0054 kol. 7 = AOP-u 0460 kol. 7 Kontrolno pravilo zahteva slaganje vanbilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00111
        if not( aop(bs,1,5) == aop(bs,407,5) ):
            lzbir =  aop(bs,1,5) 
            dzbir =  aop(bs,407,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0001 kol. 5 = AOP-u 0407 kol. 5 Upisani a neuplaćeni Neuplaćeni upisani kapital u aktivi mora biti jednak upisanom a neuplaćenom kapitalu u pasivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00112
        if not( aop(bs,1,6) == aop(bs,407,6) ):
            lzbir =  aop(bs,1,6) 
            dzbir =  aop(bs,407,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0001 kol. 6 = AOP-u 0407 kol. 6 Upisani a neuplaćeni Neuplaćeni upisani kapital u aktivi mora biti jednak upisanom a neuplaćenom kapitalu u pasivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00113
        if not( aop(bs,1,7) == aop(bs,407,7) ):
            lzbir =  aop(bs,1,7) 
            dzbir =  aop(bs,407,7) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 0001 kol. 7 = AOP-u 0407 kol. 7 Upisani a neuplaćeni Neuplaćeni upisani kapital u aktivi mora biti jednak upisanom a neuplaćenom kapitalu u pasivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #00114
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if( suma(bu,1001,1110,5) > 0 ):
                if not( suma(bs,1,54,5)+suma(bs,401,460,5) != suma(bs,1,54,6)+suma(bs,401,460,6) ):
                    form_warnings.append('***Ako je zbir podataka na oznakama za AOP (1001 do 1110) kol. 5 > 0 onda zbir podataka na oznakama za AOP (0001 do 0054) kol. 5 + (0401 do 0460) kol. 5 ≠ zbiru podataka na oznakama za AOP (0001 do 0054) kol. 6 + (0401 do 0460) kol. 6 Zbirovi podataka u kolonama 5 i 6 bilansa stanja su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama;  ')
        
        
        #BILANS USPEHA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #10001
        if not( suma(bu,1001,1110,5) > 0 ):
            form_warnings.append('Zbir podataka na oznakama za AOP (1001 do 1110) kol. 5 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga ')
        
        #10002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bu,1001,1110,6) == 0 ):
                lzbir =  suma(bu,1001,1110,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Zbir podataka na oznakama za AOP (1001 do 1110) kol. 6 = 0 Bilans uspeha za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bu,1001,1110,6) > 0 ):
                form_warnings.append('Zbir podataka na oznakama za AOP (1001 do 1110) kol. 6 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period;Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga ')
        
        #10004
        if not( aop(bu,1001,5) == suma_liste(bu,[1002,1009,1014,1015],5) ):
            lzbir =  aop(bu,1001,5) 
            dzbir =  suma_liste(bu,[1002,1009,1014,1015],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1001 kol. 5 = AOP-u (1002 + 1009 + 1014 + 1015) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10005
        if not( aop(bu,1001,6) == suma_liste(bu,[1002,1009,1014,1015],6) ):
            lzbir =  aop(bu,1001,6) 
            dzbir =  suma_liste(bu,[1002,1009,1014,1015],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1001 kol. 6 = AOP-u (1002 + 1009 + 1014 + 1015) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10006
        if not( aop(bu,1002,5) == suma_liste(bu,[1003,1004,1008],5)-suma(bu,1005,1007,5) ):
            lzbir =  aop(bu,1002,5) 
            dzbir =  suma_liste(bu,[1003,1004,1008],5)-suma(bu,1005,1007,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1002 kol. 5 = AOP-u (1003 + 1004 - 1005 - 1006 - 1007 + 1008) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10007
        if not( aop(bu,1002,6) == suma_liste(bu,[1003,1004,1008],6)-suma(bu,1005,1007,6) ):
            lzbir =  aop(bu,1002,6) 
            dzbir =  suma_liste(bu,[1003,1004,1008],6)-suma(bu,1005,1007,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1002 kol. 6 = AOP-u (1003 + 1004 - 1005 - 1006 - 1007 + 1008) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10008
        if not( aop(bu,1009,5) == suma_liste(bu,[1010,1013],5)-suma(bu,1011,1012,5) ):
            lzbir =  aop(bu,1009,5) 
            dzbir =  suma_liste(bu,[1010,1013],5)-suma(bu,1011,1012,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1009 kol. 5 = AOP-u (1010 - 1011 - 1012 + 1013) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10009
        if not( aop(bu,1009,6) == suma_liste(bu,[1010,1013],6)-suma(bu,1011,1012,6) ):
            lzbir =  aop(bu,1009,6) 
            dzbir =  suma_liste(bu,[1010,1013],6)-suma(bu,1011,1012,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1009 kol. 6 = AOP-u (1010 - 1011 - 1012 + 1013) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10010
        if not( aop(bu,1016,5) == suma_liste(bu,[1017,1026,1034,1045,1047,1048],5)-suma_liste(bu,[1035,1044,1046],5) ):
            lzbir =  aop(bu,1016,5) 
            dzbir =  suma_liste(bu,[1017,1026,1034,1045,1047,1048],5)-suma_liste(bu,[1035,1044,1046],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1016 kol. 5 = AOP-u (1017 + 1026 + 1034 - 1035 - 1044 + 1045 - 1046 + 1047 + 1048) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10011
        if not( aop(bu,1016,6) == suma_liste(bu,[1017,1026,1034,1045,1047,1048],6)-suma_liste(bu,[1035,1044,1046],6) ):
            lzbir =  aop(bu,1016,6) 
            dzbir =  suma_liste(bu,[1017,1026,1034,1045,1047,1048],6)-suma_liste(bu,[1035,1044,1046],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1016 kol. 6 = AOP-u (1017 + 1026 + 1034 - 1035 - 1044 + 1045 - 1046 + 1047 + 1048) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10012
        if not( aop(bu,1017,5) == suma(bu,1018,1025,5) ):
            lzbir =  aop(bu,1017,5) 
            dzbir =  suma(bu,1018,1025,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1017 kol. 5 = AOP-u (1018 + 1019 + 1020 + 1021 + 1022 + 1023 + 1024 + 1025) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10013
        if not( aop(bu,1017,6) == suma(bu,1018,1025,6) ):
            lzbir =  aop(bu,1017,6) 
            dzbir =  suma(bu,1018,1025,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1017 kol. 6 = AOP-u (1018 + 1019 + 1020 + 1021 + 1022 + 1023 + 1024 + 1025) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10014
        if not( aop(bu,1026,5) == suma(bu,1027,1031,5)-suma(bu,1032,1033,5) ):
            lzbir =  aop(bu,1026,5) 
            dzbir =  suma(bu,1027,1031,5)-suma(bu,1032,1033,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1026 kol. 5 = AOP-u (1027 + 1028 + 1029 + 1030 + 1031 - 1032 - 1033) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10015
        if not( aop(bu,1026,6) == suma(bu,1027,1031,6)-suma(bu,1032,1033,6) ):
            lzbir =  aop(bu,1026,6) 
            dzbir =  suma(bu,1027,1031,6)-suma(bu,1032,1033,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1026 kol. 6 = AOP-u (1027 + 1028 + 1029 + 1030 + 1031 - 1032 - 1033) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10016
        if( suma_liste(bu,[1036,1038,1040,1042],5) > suma_liste(bu,[1037,1039,1041,1043],5) ):
            if not( aop(bu,1034,5) == suma_liste(bu,[1036,1038,1040,1042],5)-suma_liste(bu,[1037,1039,1041,1043],5) ):
                lzbir =  aop(bu,1034,5) 
                dzbir =  suma_liste(bu,[1036,1038,1040,1042],5)-suma_liste(bu,[1037,1039,1041,1043],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1034 kol. 5 = AOP-u (1036 - 1037 + 1038 - 1039 + 1040 - 1041 + 1042 - 1043) kol. 5, ako je AOP (1036 + 1038 + 1040 + 1042) kol. 5 > AOP-a (1037 + 1039 + 1041 + 1043) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10017
        if( suma_liste(bu,[1036,1038,1040,1042],6) > suma_liste(bu,[1037,1039,1041,1043],6) ):
            if not( aop(bu,1034,6) == suma_liste(bu,[1036,1038,1040,1042],6)-suma_liste(bu,[1037,1039,1041,1043],6) ):
                lzbir =  aop(bu,1034,6) 
                dzbir =  suma_liste(bu,[1036,1038,1040,1042],6)-suma_liste(bu,[1037,1039,1041,1043],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1034 kol. 6 = AOP-u (1036 - 1037 + 1038 - 1039 + 1040 - 1041 + 1042 - 1043) kol. 6, ako je AOP (1036 + 1038 + 1040 + 1042) kol. 6 > AOP-a (1037 + 1039 + 1041 + 1043) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10018
        if( suma_liste(bu,[1036,1038,1040,1042],5) < suma_liste(bu,[1037,1039,1041,1043],5) ):
            if not( aop(bu,1035,5) == suma_liste(bu,[1037,1039,1041,1043],5)-suma_liste(bu,[1036,1038,1040,1042],5) ):
                lzbir =  aop(bu,1035,5) 
                dzbir =  suma_liste(bu,[1037,1039,1041,1043],5)-suma_liste(bu,[1036,1038,1040,1042],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1035 kol. 5 = AOP-u (1037 - 1036 - 1038 + 1039 - 1040 + 1041 - 1042 + 1043) kol. 5, ako je AOP (1036 + 1038 + 1040 + 1042) kol. 5 < AOP-a (1037 + 1039 + 1041 + 1043) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10019
        if( suma_liste(bu,[1036,1038,1040,1042],6) < suma_liste(bu,[1037,1039,1041,1043],6) ):
            if not( aop(bu,1035,6) == suma_liste(bu,[1037,1039,1041,1043],6)-suma_liste(bu,[1036,1038,1040,1042],6) ):
                lzbir =  aop(bu,1035,6) 
                dzbir =  suma_liste(bu,[1037,1039,1041,1043],6)-suma_liste(bu,[1036,1038,1040,1042],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1035 kol. 6 = AOP-u (1037 - 1036 - 1038 + 1039 - 1040 + 1041 - 1042 + 1043) kol. 6, ako je AOP (1036 + 1038 + 1040 + 1042) kol. 6 < AOP-a (1037 + 1039 + 1041 + 1043) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10020
        if( suma_liste(bu,[1036,1038,1040,1042],5) == suma_liste(bu,[1037,1039,1041,1043],5) ):
            if not( suma(bu,1034,1035,5) == 0 ):
                lzbir =  suma(bu,1034,1035,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1034 + 1035) kol. 5 = 0, ako je AOP (1036 + 1038 + 1040 + 1042) kol. 5 = AOP-u (1037 + 1039 + 1041 + 1043) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10021
        if( suma_liste(bu,[1036,1038,1040,1042],6) == suma_liste(bu,[1037,1039,1041,1043],6) ):
            if not( suma(bu,1034,1035,6) == 0 ):
                lzbir =  suma(bu,1034,1035,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1034 + 1035) kol. 6 = 0, ako je AOP (1036 + 1038 + 1040 + 1042) kol. 6 = AOP-u (1037 + 1039 + 1041 + 1043) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10022
        if( aop(bu,1034,5) > 0 ):
            if not( aop(bu,1035,5) == 0 ):
                lzbir =  aop(bu,1035,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1034 kol. 5 > 0, onda je AOP 1035 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazana povećanje i smanjenje '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10023
        if( aop(bu,1035,5) > 0 ):
            if not( aop(bu,1034,5) == 0 ):
                lzbir =  aop(bu,1034,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1035 kol. 5 > 0, onda je AOP 1034 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazana povećanje i smanjenje '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10024
        if( aop(bu,1034,6) > 0 ):
            if not( aop(bu,1035,6) == 0 ):
                lzbir =  aop(bu,1035,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1034 kol. 6 > 0, onda je AOP 1035 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazana povećanje i smanjenje '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10025
        if( aop(bu,1035,6) > 0 ):
            if not( aop(bu,1034,6) == 0 ):
                lzbir =  aop(bu,1034,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1035 kol. 6 > 0, onda je AOP 1034 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazana povećanje i smanjenje '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10026
        if not( suma_liste(bu,[1035,1036,1038,1040,1042],5) == suma_liste(bu,[1034,1037,1039,1041,1043],5) ):
            lzbir =  suma_liste(bu,[1035,1036,1038,1040,1042],5) 
            dzbir =  suma_liste(bu,[1034,1037,1039,1041,1043],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1035 + 1036 + 1038 + 1040 + 1042) kol. 5 = AOP-u (1034 + 1037 + 1039 + 1041 + 1043) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10027
        if not( suma_liste(bu,[1035,1036,1038,1040,1042],6) == suma_liste(bu,[1034,1037,1039,1041,1043],6) ):
            lzbir =  suma_liste(bu,[1035,1036,1038,1040,1042],6) 
            dzbir =  suma_liste(bu,[1034,1037,1039,1041,1043],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1035 + 1036 + 1038 + 1040 + 1042) kol. 6 = AOP-u (1034 + 1037 + 1039 + 1041 + 1043) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10028
        if( aop(bu,1001,5) > aop(bu,1016,5) ):
            if not( aop(bu,1049,5) == aop(bu,1001,5)-aop(bu,1016,5) ):
                lzbir =  aop(bu,1049,5) 
                dzbir =  aop(bu,1001,5)-aop(bu,1016,5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1049 kol. 5 = AOP-u (1001 - 1016) kol. 5, ako je AOP 1001 kol. 5 > AOP-a 1016 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10029
        if( aop(bu,1001,6) > aop(bu,1016,6) ):
            if not( aop(bu,1049,6) == aop(bu,1001,6)-aop(bu,1016,6) ):
                lzbir =  aop(bu,1049,6) 
                dzbir =  aop(bu,1001,6)-aop(bu,1016,6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1049 kol. 6 = AOP-u (1001 - 1016) kol. 6, ako je AOP 1001 kol. 6 > AOP-a 1016 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10030
        if( aop(bu,1001,5) < aop(bu,1016,5) ):
            if not( aop(bu,1050,5) == aop(bu,1016,5)-aop(bu,1001,5) ):
                lzbir =  aop(bu,1050,5) 
                dzbir =  aop(bu,1016,5)-aop(bu,1001,5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1050 kol. 5 = AOP-u (1016 - 1001) kol. 5, ako je AOP 1001 kol. 5 < AOP-a 1016 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10031
        if( aop(bu,1001,6) < aop(bu,1016,6) ):
            if not( aop(bu,1050,6) == aop(bu,1016,6)-aop(bu,1001,6) ):
                lzbir =  aop(bu,1050,6) 
                dzbir =  aop(bu,1016,6)-aop(bu,1001,6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1050 kol. 6 = AOP-u (1016 - 1001) kol. 6, ako je AOP 1001 kol. 6 < AOP-a 1016 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10032
        if( aop(bu,1001,5) == aop(bu,1016,5) ):
            if not( suma(bu,1049,1050,5) == 0 ):
                lzbir =  suma(bu,1049,1050,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1049 + 1050) kol. 5 = 0, ako je AOP 1001 kol. 5 = AOP-u 1016 kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10033
        if( aop(bu,1001,6) == aop(bu,1016,6) ):
            if not( suma(bu,1049,1050,6) == 0 ):
                lzbir =  suma(bu,1049,1050,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1049 + 1050) kol. 6 = 0, ako je AOP 1001 kol. 6 = AOP-u 1016 kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10034
        if( aop(bu,1049,5) > 0 ):
            if not( aop(bu,1050,5) == 0 ):
                lzbir =  aop(bu,1050,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1049 kol. 5 > 0, onda je AOP 1050 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10035
        if( aop(bu,1050,5) > 0 ):
            if not( aop(bu,1049,5) == 0 ):
                lzbir =  aop(bu,1049,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1050 kol. 5 > 0, onda je AOP 1049 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10036
        if( aop(bu,1049,6) > 0 ):
            if not( aop(bu,1050,6) == 0 ):
                lzbir =  aop(bu,1050,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1049 kol. 6 > 0, onda je AOP 1050 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10037
        if( aop(bu,1050,6) > 0 ):
            if not( aop(bu,1049,6) == 0 ):
                lzbir =  aop(bu,1049,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1050 kol. 6 > 0, onda je AOP 1049 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10038
        if not( suma_liste(bu,[1001,1050],5) == suma_liste(bu,[1016,1049],5) ):
            lzbir =  suma_liste(bu,[1001,1050],5) 
            dzbir =  suma_liste(bu,[1016,1049],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1001 + 1050) kol. 5 = AOP-u (1016 + 1049) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10039
        if not( suma_liste(bu,[1001,1050],6) == suma_liste(bu,[1016,1049],6) ):
            lzbir =  suma_liste(bu,[1001,1050],6) 
            dzbir =  suma_liste(bu,[1016,1049],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1001 + 1050) kol. 6 = AOP-u (1016 + 1049) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10040
        if not( aop(bu,1051,5) == suma_liste(bu,[1052,1053,1057,1058,1059,1060,1061],5) ):
            lzbir =  aop(bu,1051,5) 
            dzbir =  suma_liste(bu,[1052,1053,1057,1058,1059,1060,1061],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1051 kol. 5 = AOP-u (1052 + 1053 + 1057 + 1058 + 1059 + 1060 + 1061) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10041
        if not( aop(bu,1051,6) == suma_liste(bu,[1052,1053,1057,1058,1059,1060,1061],6) ):
            lzbir =  aop(bu,1051,6) 
            dzbir =  suma_liste(bu,[1052,1053,1057,1058,1059,1060,1061],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1051 kol. 6 = AOP-u (1052 + 1053 + 1057 + 1058 + 1059 + 1060 + 1061) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10042
        if not( aop(bu,1053,5) == suma(bu,1054,1056,5) ):
            lzbir =  aop(bu,1053,5) 
            dzbir =  suma(bu,1054,1056,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1053 kol. 5 = AOP-u (1054 + 1055 + 1056) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10043
        if not( aop(bu,1053,6) == suma(bu,1054,1056,6) ):
            lzbir =  aop(bu,1053,6) 
            dzbir =  suma(bu,1054,1056,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1053 kol. 6 = AOP-u (1054 + 1055 + 1056) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10044
        if not( aop(bu,1062,5) == suma_liste(bu,[1063,1064,1067,1068,1069,1070],5) ):
            lzbir =  aop(bu,1062,5) 
            dzbir =  suma_liste(bu,[1063,1064,1067,1068,1069,1070],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1062 kol. 5 = AOP-u (1063 + 1064 + 1067 + 1068 + 1069 + 1070) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10045
        if not( aop(bu,1062,6) == suma_liste(bu,[1063,1064,1067,1068,1069,1070],6) ):
            lzbir =  aop(bu,1062,6) 
            dzbir =  suma_liste(bu,[1063,1064,1067,1068,1069,1070],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1062 kol. 6 = AOP-u (1063 + 1064 + 1067 + 1068 + 1069 + 1070) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10046
        if not( aop(bu,1064,5) == suma(bu,1065,1066,5) ):
            lzbir =  aop(bu,1064,5) 
            dzbir =  suma(bu,1065,1066,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1064 kol. 5 = AOP-u (1065 + 1066) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10047
        if not( aop(bu,1064,6) == suma(bu,1065,1066,6) ):
            lzbir =  aop(bu,1064,6) 
            dzbir =  suma(bu,1065,1066,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1064 kol. 6 = AOP-u (1065 + 1066) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10048
        if( aop(bu,1051,5) > aop(bu,1062,5) ):
            if not( aop(bu,1071,5) == aop(bu,1051,5)-aop(bu,1062,5) ):
                lzbir =  aop(bu,1071,5) 
                dzbir =  aop(bu,1051,5)-aop(bu,1062,5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1071 kol. 5 = AOP-u (1051 - 1062) kol. 5, ako je AOP 1051 kol. 5 > AOP-a 1062 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10049
        if( aop(bu,1051,6) > aop(bu,1062,6) ):
            if not( aop(bu,1071,6) == aop(bu,1051,6)-aop(bu,1062,6) ):
                lzbir =  aop(bu,1071,6) 
                dzbir =  aop(bu,1051,6)-aop(bu,1062,6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1071 kol. 6 = AOP-u (1051 - 1062) kol. 6, ako je AOP 1051 kol. 6 > AOP-a 1062 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10050
        if( aop(bu,1051,5) < aop(bu,1062,5) ):
            if not( aop(bu,1072,5) == aop(bu,1062,5)-aop(bu,1051,5) ):
                lzbir =  aop(bu,1072,5) 
                dzbir =  aop(bu,1062,5)-aop(bu,1051,5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1072 kol. 5 = AOP-u (1062 - 1051) kol. 5, ako je AOP 1051 kol. 5 < AOP-a 1062 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10051
        if( aop(bu,1051,6) < aop(bu,1062,6) ):
            if not( aop(bu,1072,6) == aop(bu,1062,6)-aop(bu,1051,6) ):
                lzbir =  aop(bu,1072,6) 
                dzbir =  aop(bu,1062,6)-aop(bu,1051,6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1072 kol. 6 = AOP-u (1062 - 1051) kol. 6, ako je AOP 1051 kol. 6 < AOP-a 1062 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10052
        if( aop(bu,1051,5) == aop(bu,1062,5) ):
            if not( suma(bu,1071,1072,5) == 0 ):
                lzbir =  suma(bu,1071,1072,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1071 + 1072) kol. 5 = 0,  ako je AOP 1051 kol. 5 = AOP-u 1062 kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10053
        if( aop(bu,1051,6) == aop(bu,1062,6) ):
            if not( suma(bu,1071,1072,6) == 0 ):
                lzbir =  suma(bu,1071,1072,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1071 + 1072) kol. 6 = 0,  ako je AOP 1051 kol. 6 = AOP-u 1062 kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10054
        if( aop(bu,1071,5) > 0 ):
            if not( aop(bu,1072,5) == 0 ):
                lzbir =  aop(bu,1072,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1071 kol. 5 > 0, onda je AOP 1072 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10055
        if( aop(bu,1072,5) > 0 ):
            if not( aop(bu,1071,5) == 0 ):
                lzbir =  aop(bu,1071,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je  AOP 1072 kol. 5 > 0, onda je AOP 1071 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10056
        if( aop(bu,1071,6) > 0 ):
            if not( aop(bu,1072,6) == 0 ):
                lzbir =  aop(bu,1072,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1071 kol. 6 > 0, onda je AOP 1072 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10057
        if( aop(bu,1072,6) > 0 ):
            if not( aop(bu,1071,6) == 0 ):
                lzbir =  aop(bu,1071,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1072 kol. 6 > 0, onda je AOP 1071 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10058
        if not( suma_liste(bu,[1051,1072],5) == suma_liste(bu,[1062,1071],5) ):
            lzbir =  suma_liste(bu,[1051,1072],5) 
            dzbir =  suma_liste(bu,[1062,1071],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1051 + 1072) kol. 5 = AOP-u (1062 + 1071) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10059
        if not( suma_liste(bu,[1051,1072],6) == suma_liste(bu,[1062,1071],6) ):
            lzbir =  suma_liste(bu,[1051,1072],6) 
            dzbir =  suma_liste(bu,[1062,1071],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1051 + 1072) kol. 6 = AOP-u (1062 + 1071) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10060
        if not( aop(bu,1073,5) == suma_liste(bu,[1074,1079,1084],5)-aop(bu,1085,5) ):
            lzbir =  aop(bu,1073,5) 
            dzbir =  suma_liste(bu,[1074,1079,1084],5)-aop(bu,1085,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1073 kol. 5 = AOP-u (1074 + 1079 + 1084 - 1085) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10061
        if not( aop(bu,1073,6) == suma_liste(bu,[1074,1079,1084],6)-aop(bu,1085,6) ):
            lzbir =  aop(bu,1073,6) 
            dzbir =  suma_liste(bu,[1074,1079,1084],6)-aop(bu,1085,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1073 kol. 6 = AOP-u (1074 + 1079 + 1084 - 1085) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10062
        if not( aop(bu,1074,5) == suma_liste(bu,[1075,1076,1078],5)-aop(bu,1077,5) ):
            lzbir =  aop(bu,1074,5) 
            dzbir =  suma_liste(bu,[1075,1076,1078],5)-aop(bu,1077,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1074 kol. 5 = AOP-u (1075 + 1076 - 1077 + 1078) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10063
        if not( aop(bu,1074,6) == suma_liste(bu,[1075,1076,1078],6)-aop(bu,1077,6) ):
            lzbir =  aop(bu,1074,6) 
            dzbir =  suma_liste(bu,[1075,1076,1078],6)-aop(bu,1077,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1074 kol. 6 = AOP-u (1075 + 1076 - 1077 + 1078) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10064
        if not( aop(bu,1079,5) == suma(bu,1080,1083,5) ):
            lzbir =  aop(bu,1079,5) 
            dzbir =  suma(bu,1080,1083,5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1079 kol. 5 = AOP-u (1080 + 1081 + 1082 + 1083) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10065
        if not( aop(bu,1079,6) == suma(bu,1080,1083,6) ):
            lzbir =  aop(bu,1079,6) 
            dzbir =  suma(bu,1080,1083,6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1079 kol. 6 = AOP-u (1080 + 1081 + 1082 + 1083) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10066
        if( suma_liste(bu,[1049,1071],5) > suma_liste(bu,[1050,1072,1073],5) ):
            if not( aop(bu,1086,5) == suma_liste(bu,[1049,1071],5)-suma_liste(bu,[1050,1072,1073],5) ):
                lzbir =  aop(bu,1086,5) 
                dzbir =  suma_liste(bu,[1049,1071],5)-suma_liste(bu,[1050,1072,1073],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1086 kol. 5 = AOP-u (1049 + 1071 - 1050 - 1072 - 1073) kol. 5, ako je AOP (1049 + 1071) kol. 5 > AOP-a (1050 + 1072 + 1073) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10067
        if( suma_liste(bu,[1049,1071],6) > suma_liste(bu,[1050,1072,1073],6) ):
            if not( aop(bu,1086,6) == suma_liste(bu,[1049,1071],6)-suma_liste(bu,[1050,1072,1073],6) ):
                lzbir =  aop(bu,1086,6) 
                dzbir =  suma_liste(bu,[1049,1071],6)-suma_liste(bu,[1050,1072,1073],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1086 kol. 6 = AOP-u (1049 + 1071 - 1050 - 1072 - 1073) kol. 6, ako je AOP (1049 + 1071) kol. 6 > AOP-a (1050 + 1072 + 1073) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10068
        if( suma_liste(bu,[1049,1071],5) < suma_liste(bu,[1050,1072,1073],5) ):
            if not( aop(bu,1087,5) == suma_liste(bu,[1050,1072,1073],5)-suma_liste(bu,[1049,1071],5) ):
                lzbir =  aop(bu,1087,5) 
                dzbir =  suma_liste(bu,[1050,1072,1073],5)-suma_liste(bu,[1049,1071],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1087 kol. 5 = AOP-u (1050 - 1049 - 1071 + 1072 + 1073) kol. 5, ako je AOP (1049 + 1071) kol. 5 < AOP-a (1050 + 1072 + 1073) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10069
        if( suma_liste(bu,[1049,1071],6) < suma_liste(bu,[1050,1072,1073],6) ):
            if not( aop(bu,1087,6) == suma_liste(bu,[1050,1072,1073],6)-suma_liste(bu,[1049,1071],6) ):
                lzbir =  aop(bu,1087,6) 
                dzbir =  suma_liste(bu,[1050,1072,1073],6)-suma_liste(bu,[1049,1071],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1087 kol. 6 = AOP-u (1050 - 1049 - 1071 + 1072 + 1073) kol. 6, ako je AOP (1049 + 1071) kol. 6 < AOP-a (1050 + 1072 + 1073) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10070
        if( suma_liste(bu,[1049,1071],5) == suma_liste(bu,[1050,1072,1073],5) ):
            if not( suma(bu,1086,1087,5) == 0 ):
                lzbir =  suma(bu,1086,1087,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1086 + 1087) kol. 5 = 0,  ako je AOP (1049 + 1071) kol. 5 = AOP-u (1050 + 1072 + 1073) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10071
        if( suma_liste(bu,[1049,1071],6) == suma_liste(bu,[1050,1072,1073],6) ):
            if not( suma(bu,1086,1087,6) == 0 ):
                lzbir =  suma(bu,1086,1087,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1086 + 1087) kol. 6 = 0,  ako je AOP (1049 + 1071) kol. 6 = AOP-u (1050 + 1072 + 1073) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10072
        if( aop(bu,1086,5) > 0 ):
            if not( aop(bu,1087,5) == 0 ):
                lzbir =  aop(bu,1087,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1086 kol. 5 > 0, onda je AOP 1087 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10073
        if( aop(bu,1087,5) > 0 ):
            if not( aop(bu,1086,5) == 0 ):
                lzbir =  aop(bu,1086,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1087 kol. 5 > 0, onda je AOP 1086 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10074
        if( aop(bu,1086,6) > 0 ):
            if not( aop(bu,1087,6) == 0 ):
                lzbir =  aop(bu,1087,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1086 kol. 6 > 0, onda je AOP 1087 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10075
        if( aop(bu,1087,6) > 0 ):
            if not( aop(bu,1086,6) == 0 ):
                lzbir =  aop(bu,1086,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1087 kol. 6 > 0, onda je AOP 1086 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10076
        if not( suma_liste(bu,[1049,1071,1087],5) == suma_liste(bu,[1050,1072,1073,1086],5) ):
            lzbir =  suma_liste(bu,[1049,1071,1087],5) 
            dzbir =  suma_liste(bu,[1050,1072,1073,1086],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1049 + 1071 + 1087) kol. 5 = AOP-u (1050 + 1072 + 1073 + 1086) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10077
        if not( suma_liste(bu,[1049,1071,1087],6) == suma_liste(bu,[1050,1072,1073,1086],6) ):
            lzbir =  suma_liste(bu,[1049,1071,1087],6) 
            dzbir =  suma_liste(bu,[1050,1072,1073,1086],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1049 + 1071 + 1087) kol. 6 = AOP-u (1050 + 1072 + 1073 + 1086) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10078
        if( suma_liste(bu,[1086,1088,1090,1092],5) > suma_liste(bu,[1087,1089,1091,1093],5) ):
            if not( aop(bu,1094,5) == suma_liste(bu,[1086,1088,1090,1092],5)-suma_liste(bu,[1087,1089,1091,1093],5) ):
                lzbir =  aop(bu,1094,5) 
                dzbir =  suma_liste(bu,[1086,1088,1090,1092],5)-suma_liste(bu,[1087,1089,1091,1093],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1094 kol. 5 = AOP-u (1086 + 1088 + 1090 + 1092 - 1087 - 1089 - 1091 - 1093) kol. 5, ako je AOP (1086 + 1088 + 1090 + 1092) kol. 5 > AOP-a (1087 + 1089 + 1091 + 1093) kol. 5   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10079
        if( suma_liste(bu,[1086,1088,1090,1092],6) > suma_liste(bu,[1087,1089,1091,1093],6) ):
            if not( aop(bu,1094,6) == suma_liste(bu,[1086,1088,1090,1092],6)-suma_liste(bu,[1087,1089,1091,1093],6) ):
                lzbir =  aop(bu,1094,6) 
                dzbir =  suma_liste(bu,[1086,1088,1090,1092],6)-suma_liste(bu,[1087,1089,1091,1093],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1094 kol. 6 = AOP-u (1086 + 1088 + 1090 + 1092 - 1087 - 1089 - 1091 - 1093) kol. 6, ako je AOP (1086 + 1088 + 1090 + 1092) kol. 6 > AOP-a (1087 + 1089 + 1091 + 1093) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10080
        if( suma_liste(bu,[1086,1088,1090,1092],5) < suma_liste(bu,[1087,1089,1091,1093],5) ):
            if not( aop(bu,1095,5) == suma_liste(bu,[1087,1089,1091,1093],5)-suma_liste(bu,[1086,1088,1090,1092],5) ):
                lzbir =  aop(bu,1095,5) 
                dzbir =  suma_liste(bu,[1087,1089,1091,1093],5)-suma_liste(bu,[1086,1088,1090,1092],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1095 kol. 5 = AOP-u (1087 + 1089 + 1091 + 1093 - 1086 - 1088 - 1090 - 1092) kol. 5, ako je AOP (1086 + 1088 + 1090 + 1092) kol. 5 < AOP-a (1087 + 1089 + 1091 + 1093) kol. 5   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10081
        if( suma_liste(bu,[1086,1088,1090,1092],6) < suma_liste(bu,[1087,1089,1091,1093],6) ):
            if not( aop(bu,1095,6) == suma_liste(bu,[1087,1089,1091,1093],6)-suma_liste(bu,[1086,1088,1090,1092],6) ):
                lzbir =  aop(bu,1095,6) 
                dzbir =  suma_liste(bu,[1087,1089,1091,1093],6)-suma_liste(bu,[1086,1088,1090,1092],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1095 kol. 6 = AOP-u (1087 + 1089 + 1091 + 1093 - 1086 - 1088 - 1090 - 1092 ) kol. 6, ako je AOP (1086 + 1088 + 1090 + 1092) kol. 6 < AOP-a (1087 + 1089 + 1091 + 1093) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10082
        if( suma_liste(bu,[1086,1088,1090,1092],5) == suma_liste(bu,[1087,1089,1091,1093],5) ):
            if not( suma(bu,1094,1095,5) == 0 ):
                lzbir =  suma(bu,1094,1095,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1094 + 1095) kol. 5 = 0, ako je AOP (1086 + 1088 + 1090 + 1092) kol. 5 = AOP-u (1087 + 1089 + 1091 + 1093) kol. 5  Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10083
        if( suma_liste(bu,[1086,1088,1090,1092],6) == suma_liste(bu,[1087,1089,1091,1093],6) ):
            if not( suma(bu,1094,1095,6) == 0 ):
                lzbir =  suma(bu,1094,1095,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1094 + 1095) kol. 6 = 0, ako je AOP (1086 + 1088 + 1090 + 1092) kol. 6 = AOP-u (1087 + 1089 + 1091 + 1093) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10084
        if( aop(bu,1094,5) > 0 ):
            if not( aop(bu,1095,5) == 0 ):
                lzbir =  aop(bu,1095,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1094 kol. 5 > 0, onda je AOP 1095 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10085
        if( aop(bu,1095,5) > 0 ):
            if not( aop(bu,1094,5) == 0 ):
                lzbir =  aop(bu,1094,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1095 kol. 5 > 0, onda je AOP 1094 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10086
        if( aop(bu,1094,6) > 0 ):
            if not( aop(bu,1095,6) == 0 ):
                lzbir =  aop(bu,1095,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1094 kol. 6 > 0, onda je AOP 1095 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10087
        if( aop(bu,1095,6) > 0 ):
            if not( aop(bu,1094,6) == 0 ):
                lzbir =  aop(bu,1094,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1095 kol. 6 > 0, onda je AOP 1094 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10088
        if not( suma_liste(bu,[1086,1088,1090,1092,1095],5) == suma_liste(bu,[1087,1089,1091,1093,1094],5) ):
            lzbir =  suma_liste(bu,[1086,1088,1090,1092,1095],5) 
            dzbir =  suma_liste(bu,[1087,1089,1091,1093,1094],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1086 + 1088 + 1090 + 1092 + 1095) kol. 5 = AOP-u (1087 + 1089 + 1091 + 1093 + 1094) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10089
        if not( suma_liste(bu,[1086,1088,1090,1092,1095],6) == suma_liste(bu,[1087,1089,1091,1093,1094],6) ):
            lzbir =  suma_liste(bu,[1086,1088,1090,1092,1095],6) 
            dzbir =  suma_liste(bu,[1087,1089,1091,1093,1094],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1086 + 1088 + 1090 + 1092 + 1095) kol. 6 = AOP-u (1087 + 1089 + 1091 + 1093 + 1094) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10090
        if( aop(bu,1096,5) > 0 ):
            if not( aop(bu,1097,5) == 0 ):
                lzbir =  aop(bu,1097,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1096 kol. 5 > 0, onda je AOP 1097 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10091
        if( aop(bu,1097,5) > 0 ):
            if not( aop(bu,1096,5) == 0 ):
                lzbir =  aop(bu,1096,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1097 kol. 5 > 0, onda je AOP 1096 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10092
        if( aop(bu,1096,6) > 0 ):
            if not( aop(bu,1097,6) == 0 ):
                lzbir =  aop(bu,1097,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1096 kol. 6 > 0, onda je AOP 1097 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10093
        if( aop(bu,1097,6) > 0 ):
            if not( aop(bu,1096,6) == 0 ):
                lzbir =  aop(bu,1096,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1097 kol. 6 > 0, onda je AOP 1096 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10094
        if( suma_liste(bu,[1094,1096],5) > suma_liste(bu,[1095,1097],5) ):
            if not( aop(bu,1098,5) == suma_liste(bu,[1094,1096],5)-suma_liste(bu,[1095,1097],5) ):
                lzbir =  aop(bu,1098,5) 
                dzbir =  suma_liste(bu,[1094,1096],5)-suma_liste(bu,[1095,1097],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1098 kol. 5 = AOP-u (1094 + 1096 - 1095 - 1097) kol. 5, ako je AOP (1094 + 1096) kol. 5 > AOP-a (1095 + 1097) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10095
        if( suma_liste(bu,[1094,1096],6) > suma_liste(bu,[1095,1097],6) ):
            if not( aop(bu,1098,6) == suma_liste(bu,[1094,1096],6)-suma_liste(bu,[1095,1097],6) ):
                lzbir =  aop(bu,1098,6) 
                dzbir =  suma_liste(bu,[1094,1096],6)-suma_liste(bu,[1095,1097],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1098 kol. 6 = AOP-u (1094 + 1096 - 1095 - 1097) kol. 6, ako je AOP (1094 + 1096) kol. 6 > AOP-a (1095 + 1097) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10096
        if( suma_liste(bu,[1094,1096],5) < suma_liste(bu,[1095,1097],5) ):
            if not( aop(bu,1099,5) == suma_liste(bu,[1095,1097],5)-suma_liste(bu,[1094,1096],5) ):
                lzbir =  aop(bu,1099,5) 
                dzbir =  suma_liste(bu,[1095,1097],5)-suma_liste(bu,[1094,1096],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1099 kol. 5 = AOP-u (1095 + 1097 - 1094 - 1096) kol. 5, ako je AOP (1094 + 1096) kol. 5 < AOP-a (1095 + 1097) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10097
        if( suma_liste(bu,[1094,1096],6) < suma_liste(bu,[1095,1097],6) ):
            if not( aop(bu,1099,6) == suma_liste(bu,[1095,1097],6)-suma_liste(bu,[1094,1096],6) ):
                lzbir =  aop(bu,1099,6) 
                dzbir =  suma_liste(bu,[1095,1097],6)-suma_liste(bu,[1094,1096],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1099 kol. 6 = AOP-u (1095 + 1097 - 1094 - 1096) kol. 6, ako je AOP (1094 + 1096) kol. 6 < AOP-a (1095 + 1097) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10098
        if( suma_liste(bu,[1094,1096],5) == suma_liste(bu,[1095,1097],5) ):
            if not( suma(bu,1098,1099,5) == 0 ):
                lzbir =  suma(bu,1098,1099,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1098 + 1099) kol. 5 = 0, ako je AOP (1094 + 1096) kol. 5 = AOP-u (1095 + 1097) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10099
        if( suma_liste(bu,[1094,1096],6) == suma_liste(bu,[1095,1097],6) ):
            if not( suma(bu,1098,1099,6) == 0 ):
                lzbir =  suma(bu,1098,1099,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1098 + 1099) kol. 6 = 0, ako je AOP (1094 + 1096) kol. 6 = AOP-u (1095 + 1097) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10100
        if( aop(bu,1098,5) > 0 ):
            if not( aop(bu,1099,5) == 0 ):
                lzbir =  aop(bu,1099,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1098 kol. 5 > 0, onda je AOP 1099 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10101
        if( aop(bu,1099,5) > 0 ):
            if not( aop(bu,1098,5) == 0 ):
                lzbir =  aop(bu,1098,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1099 kol. 5 > 0, onda je AOP 1098 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10102
        if( aop(bu,1098,6) > 0 ):
            if not( aop(bu,1099,6) == 0 ):
                lzbir =  aop(bu,1099,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1098 kol. 6 > 0, onda je AOP 1099 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10103
        if( aop(bu,1099,6) > 0 ):
            if not( aop(bu,1098,6) == 0 ):
                lzbir =  aop(bu,1098,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1099 kol. 6 > 0, onda je AOP 1098 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10104
        if not( suma_liste(bu,[1094,1096,1099],5) == suma_liste(bu,[1095,1097,1098],5) ):
            lzbir =  suma_liste(bu,[1094,1096,1099],5) 
            dzbir =  suma_liste(bu,[1095,1097,1098],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1094 + 1096 + 1099) kol. 5 = AOP-u (1095 + 1097 + 1098) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10105
        if not( suma_liste(bu,[1094,1096,1099],6) == suma_liste(bu,[1095,1097,1098],6) ):
            lzbir =  suma_liste(bu,[1094,1096,1099],6) 
            dzbir =  suma_liste(bu,[1095,1097,1098],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1094 + 1096 + 1099) kol. 6 = AOP-u (1095 + 1097 + 1098) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10106
        if( suma_liste(bu,[1098,1101],5) > suma_liste(bu,[1099,1100,1102],5) ):
            if not( aop(bu,1103,5) == suma_liste(bu,[1098,1101],5)-suma_liste(bu,[1099,1100,1102],5) ):
                lzbir =  aop(bu,1103,5) 
                dzbir =  suma_liste(bu,[1098,1101],5)-suma_liste(bu,[1099,1100,1102],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1103 kol. 5 = AOP-u (1098 - 1099 - 1100 + 1101 - 1102) kol. 5, ako je AOP (1098 + 1101) kol. 5 > AOP-a (1099 + 1100 + 1102) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10107
        if( suma_liste(bu,[1098,1101],6) > suma_liste(bu,[1099,1100,1102],6) ):
            if not( aop(bu,1103,6) == suma_liste(bu,[1098,1101],6)-suma_liste(bu,[1099,1100,1102],6) ):
                lzbir =  aop(bu,1103,6) 
                dzbir =  suma_liste(bu,[1098,1101],6)-suma_liste(bu,[1099,1100,1102],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1103 kol. 6 = AOP-u (1098 - 1099 - 1100 + 1101 - 1102) kol. 6, ako je AOP (1098 + 1101) kol. 6 > AOP-a (1099 + 1100 + 1102) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10108
        if( suma_liste(bu,[1098,1101],5) < suma_liste(bu,[1099,1100,1102],5) ):
            if not( aop(bu,1106,5) == suma_liste(bu,[1099,1100,1102],5)-suma_liste(bu,[1098,1101],5) ):
                lzbir =  aop(bu,1106,5) 
                dzbir =  suma_liste(bu,[1099,1100,1102],5)-suma_liste(bu,[1098,1101],5) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1106 kol. 5 = AOP-u (1099 - 1098 + 1100 - 1101 + 1102) kol. 5, ako je AOP (1098 + 1101) kol. 5 < AOP-a (1099 + 1100 + 1102) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10109
        if( suma_liste(bu,[1098,1101],6) < suma_liste(bu,[1099,1100,1102],6) ):
            if not( aop(bu,1106,6) == suma_liste(bu,[1099,1100,1102],6)-suma_liste(bu,[1098,1101],6) ):
                lzbir =  aop(bu,1106,6) 
                dzbir =  suma_liste(bu,[1099,1100,1102],6)-suma_liste(bu,[1098,1101],6) 
                razlika = lzbir - dzbir
                form_errors.append('AOP 1106 kol. 6 = AOP-u (1099 - 1098 + 1100 - 1101 + 1102) kol. 6, ako je AOP (1098 + 1101) kol. 6 < AOP-a (1099 + 1100 + 1102) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10110
        if( suma_liste(bu,[1098,1101],5) == suma_liste(bu,[1099,1100,1102],5) ):
            if not( suma_liste(bu,[1103,1106],5) == 0 ):
                lzbir =  suma_liste(bu,[1103,1106],5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1103 + 1106) kol. 5 = 0,  ako je AOP (1098 + 1101) kol. 5 = AOP-u (1099 + 1100 + 1102) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10111
        if( suma_liste(bu,[1098,1101],6) == suma_liste(bu,[1099,1100,1102],6) ):
            if not( suma_liste(bu,[1103,1106],6) == 0 ):
                lzbir =  suma_liste(bu,[1103,1106],6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('AOP (1103 + 1106) kol. 6 = 0,  ako je AOP (1098 + 1101) kol. 6 = AOP-u (1099 + 1100 + 1102) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10112
        if( aop(bu,1103,5) > 0 ):
            if not( aop(bu,1106,5) == 0 ):
                lzbir =  aop(bu,1106,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1103 kol. 5 > 0, onda je AOP 1106 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10113
        if( aop(bu,1106,5) > 0 ):
            if not( aop(bu,1103,5) == 0 ):
                lzbir =  aop(bu,1103,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1106 kol. 5 > 0, onda je AOP 1103 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10114
        if( aop(bu,1103,6) > 0 ):
            if not( aop(bu,1106,6) == 0 ):
                lzbir =  aop(bu,1106,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1103 kol. 6 > 0, onda je AOP 1106 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10115
        if( aop(bu,1106,6) > 0 ):
            if not( aop(bu,1103,6) == 0 ):
                lzbir =  aop(bu,1103,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                form_errors.append('Ako je AOP 1106 kol. 6 > 0, onda je AOP 1103 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10116
        if not( suma_liste(bu,[1098,1101,1106],5) == suma_liste(bu,[1099,1100,1102,1103],5) ):
            lzbir =  suma_liste(bu,[1098,1101,1106],5) 
            dzbir =  suma_liste(bu,[1099,1100,1102,1103],5) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1098 + 1101 + 1106) kol. 5 = AOP-u (1099 + 1100 + 1102 + 1103) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10117
        if not( suma_liste(bu,[1098,1101,1106],6) == suma_liste(bu,[1099,1100,1102,1103],6) ):
            lzbir =  suma_liste(bu,[1098,1101,1106],6) 
            dzbir =  suma_liste(bu,[1099,1100,1102,1103],6) 
            razlika = lzbir - dzbir
            form_errors.append('AOP (1098 + 1101 + 1106) kol. 6 = AOP-u (1099 + 1100 + 1102 + 1103) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10118
        #Za ovaj set se ne primenjuje pravilo 
        
        #10119
        #Za ovaj set se ne primenjuje pravilo 
        
        #10120
        #Za ovaj set se ne primenjuje pravilo 
        
        #10121
        #Za ovaj set se ne primenjuje pravilo 
        
        #10122
        if not( aop(bu,1104,5) == 0 ):
            lzbir =  aop(bu,1104,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1104 kol. 5 = 0 Neto dobitak koji pripada manjinskim ulagačima prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10123
        if not( aop(bu,1104,6) == 0 ):
            lzbir =  aop(bu,1104,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1104 kol. 6 = 0 Neto dobitak koji pripada manjinskim ulagačima prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10124
        if not( aop(bu,1105,5) == 0 ):
            lzbir =  aop(bu,1105,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1105 kol. 5 = 0 Neto dobitak koji pripada većinskom vlasniku prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10125
        if not( aop(bu,1105,6) == 0 ):
            lzbir =  aop(bu,1105,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1105 kol. 6 = 0 Neto dobitak koji pripada većinskom vlasniku prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10126
        if not( aop(bu,1107,5) == 0 ):
            lzbir =  aop(bu,1107,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1107 kol. 5 = 0 Neto gubitak koji pripada manjinskim ulagačima prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10127
        if not( aop(bu,1107,6) == 0 ):
            lzbir =  aop(bu,1107,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1107 kol. 6 = 0 Neto gubitak koji pripada manjinskim ulagačima prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10128
        if not( aop(bu,1108,5) == 0 ):
            lzbir =  aop(bu,1108,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1108 kol. 5 = 0 Neto gubitak koji pripada većinskom vlasniku prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10129
        if not( aop(bu,1108,6) == 0 ):
            lzbir =  aop(bu,1108,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            form_errors.append('AOP 1108 kol. 6 = 0 Neto gubitak koji pripada većinskom vlasniku prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10130
        if( aop(bu,1103,5) > 0 ):
            if not( aop(bs,416,5) == aop(bu,1103,5) ):
                lzbir =  aop(bs,416,5) 
                dzbir =  aop(bu,1103,5) 
                razlika = lzbir - dzbir
                form_warnings.append('Ako je AOP 1103 kol. 5 > 0, onda AOP 0416 kol. 5 bilansa stanja = AOP-a 1103 kol. 5  Neto dobitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu neraspoređenog dobitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10131
        if( aop(bs,416,5) > 0 ):
            if not( aop(bs,416,5) == aop(bu,1103,5) ):
                lzbir =  aop(bs,416,5) 
                dzbir =  aop(bu,1103,5) 
                razlika = lzbir - dzbir
                form_warnings.append('Ako je AOP 0416 kol. 5 > 0, onda AOP 0416 kol. 5 bilansa stanja = AOP-a 1103 kol. 5  Neto dobitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu neraspoređenog dobitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10132
        if( aop(bu,1103,6) > 0 ):
            if not( aop(bs,416,6) == aop(bu,1103,6) ):
                lzbir =  aop(bs,416,6) 
                dzbir =  aop(bu,1103,6) 
                razlika = lzbir - dzbir
                form_warnings.append('Ako je AOP 1103 kol. 6 > 0, onda AOP 0416 kol. 6 bilansa stanja = AOP-a 1103 kol. 6  Neto dobitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak neraspoređenom dobitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10133
        if( aop(bs,416,6) > 0 ):
            if not( aop(bs,416,6) == aop(bu,1103,6) ):
                lzbir =  aop(bs,416,6) 
                dzbir =  aop(bu,1103,6) 
                razlika = lzbir - dzbir
                form_warnings.append('Ako je AOP 0416 kol. 6 > 0, onda AOP 0416 kol. 6 bilansa stanja = AOP-a 1103 kol. 6  Neto dobitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak neraspoređenom dobitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10134
        if( aop(bu,1106,5) > 0 ):
            if not( aop(bs,419,5) == aop(bu,1106,5) ):
                lzbir =  aop(bs,419,5) 
                dzbir =  aop(bu,1106,5) 
                razlika = lzbir - dzbir
                form_warnings.append('Ako je AOP 1106 kol. 5 > 0, onda AOP 0419 kol. 5 bilansa stanja = AOP-a 1106 kol. 5  Neto gubitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu gubitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10135
        if( aop(bs,419,5) > 0 ):
            if not( aop(bs,419,5) == aop(bu,1106,5) ):
                lzbir =  aop(bs,419,5) 
                dzbir =  aop(bu,1106,5) 
                razlika = lzbir - dzbir
                form_warnings.append('Ako je AOP 0419 kol. 5 > 0, onda AOP 0419 kol. 5 bilansa stanja = AOP-a 1106 kol. 5  Neto gubitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu gubitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10136
        if( aop(bu,1106,6) > 0 ):
            if not( aop(bs,419,6) == aop(bu,1106,6) ):
                lzbir =  aop(bs,419,6) 
                dzbir =  aop(bu,1106,6) 
                razlika = lzbir - dzbir
                form_warnings.append('Ako je AOP 1106 kol. 6 > 0, onda AOP 0419 kol. 6 bilansa stanja = AOP-a 1106 kol. 6  Neto gubitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak gubitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10137
        if( aop(bs,419,6) > 0 ):
            if not( aop(bs,419,6) == aop(bu,1106,6) ):
                lzbir =  aop(bs,419,6) 
                dzbir =  aop(bu,1106,6) 
                razlika = lzbir - dzbir
                form_warnings.append('Ako je AOP 0419 kol. 6 > 0, onda AOP 0419 kol. 6 bilansa stanja = AOP-a 1106 kol. 6  Neto gubitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak gubitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') ')
        
        #10138
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if( suma(bu,1001,1110,5) > 0 ):
                if not( suma(bu,1001,1110,5) != suma(bu,1001,1110,6) ):
                    form_warnings.append('***Ako je zbir podataka na oznakama za AOP (1001 do 1110) kol. 5 > 0 onda zbir podataka na oznakama za AOP (1001 do 1110) kol. 5 ≠ zbiru podataka na oznakama za AOP  (1001 do 1110) kol. 6 Zbirovi podataka u kolonama 5 i 6 bilansa uspeha su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama;  ')
       
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
        
