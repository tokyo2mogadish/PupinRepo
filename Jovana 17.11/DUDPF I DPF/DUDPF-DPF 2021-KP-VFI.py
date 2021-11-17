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
    aop_key = "_".join(seq)
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
        ostalo_warnings = []
        ostalo_errors = []
        exceptions=[]


        #Provera da li lice odgovorno za sastavljanje je upisano
        if (Zahtev.LiceOdgovornoZaSastavljanje is None):
            ostalo_errors.append('Podaci za lice odgovorno za sastavljanje finansijskog izveštaja nisu upisani.')

        #Provera da li lice odgovorno za potpisivanje
        if (len(Zahtev.Potpisnici) == 0):
            ostalo_errors.append('Podaci o potpisniku finansijskog izveštaja nisu upisani.')

        #Provera da li su prosledjeni svi ulazni dokumenti
        if (Zahtev.ValidacijaUlaznihDokumenataOmoguceno==True):
            if Zahtev.UlazniDokumenti.Count>0:
                for k in Zahtev.UlazniDokumenti.Keys:
                    if Zahtev.UlazniDokumenti[k].Obavezan==True and Zahtev.UlazniDokumenti[k].Barkod == None:
                        doc_errors.append('Dokument sa nazivom "'+Zahtev.UlazniDokumenti[k].Naziv+'" niste priložili.')


        #Prilagoditi proveru postojanja forme u zavisnosti od tipa FI
        bs = getForme(Zahtev,'Bilans stanja')
        if len(bs)==0:
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Bilans stanja nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        bu = getForme(Zahtev,'Bilans uspeha')
        if len(bu)==0:
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Bilans uspeha nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)


        fia = getForme(Zahtev,'Finansijski izveštaj DPF 1')
        if len(fia)==0:
            
            naziv_obrasca='Finansijski izveštaj DPF 1'
            poruka  ='Finansijski izveštaj DPF 1 nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        fib = getForme(Zahtev,'Finansijski izveštaj DPF 2')
        if len(fib)==0:
            
            naziv_obrasca='Finansijski izveštaj DPF 2'
            poruka  ='Finansijski izveštaj DPF 2 nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        fic = getForme(Zahtev,'Finansijski izveštaj DPF 3')
        if len(fic)==0:
            
            naziv_obrasca='Finansijski izveštaj DPF 3'
            poruka  ='Finansijski izveštaj DPF 3 nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        fid = getForme(Zahtev,'Finansijski izveštaj DPF 4')
        if len(fid)==0:
            
            naziv_obrasca='Finansijski izveštaj DPF 4'
            poruka  ='Finansijski izveštaj DPF 4 nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        fie = getForme(Zahtev,'Finansijski izveštaj DPF 5')
        if len(fie)==0:
            
            naziv_obrasca='Finansijski izveštaj DPF 5'
            poruka  ='Finansijski izveštaj DPF 5 nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)


        if len(form_errors)>0:
            return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}

        lzbir = 0
        dzbir = 0
        razlika = 0

        hasError = False
        hasWarning = False

        ######################################
        #### POCETAK KONTROLNIH PRAVILA ######
        ######################################
     
 
        
        #00000-2
        if not( suma(bs,1,13,5)+suma(bs,1,13,6)+suma(bs,1,13,7)+suma(bs,401,417,5)+suma(bs,401,417,6)+suma(bs,401,417,7)+suma(bu,1001,1040,5)+suma(bu,1001,1040,6) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0013) kol. 5 + (0001 do 0013) kol. 6 + (0001 do 0013) kol. 7 bilansa stanja + (0401 do 0417) kol. 5 + (0401 do 0417) kol. 6 + (0401 do 0417) kol. 7 bilansa stanja + (1001 do 1040) kol. 5 + (1001 do 1040) kol. 6 bilansa uspeha > 0 Vanredni finansijski izveštaj, po pravilu, ne sme biti bez podataka; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0013) kol. 5 + (0001 do 0013) kol. 6 + (0001 do 0013) kol. 7 bilansa stanja + (0401 do 0417) kol. 5 + (0401 do 0417) kol. 6 + (0401 do 0417) kol. 7 bilansa stanja + (1001 do 1040) kol. 5 + (1001 do 1040) kol. 6 bilansa uspeha > 0 Vanredni finansijski izveštaj, po pravilu, ne sme biti bez podataka; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #00000-3
        #Za ovaj set se ne primenjuje pravilo

        #Provera da li je fizahtev placen
        if not(Zahtev.Placen):
            ostalo_errors.append('Naknada za obradu i javno objavljivanje izveštaja i propisane dokumentacije nije uplaćena u propisanom iznosu. Instrukcije za uplatu propisane naknade date su u okviru PIS FI sistema za konkretan zahtev, na linku „Status naplate zahteva / Instrukcija za plaćanje". Ukoliko ste izvršili uplatu, a naknada nije uparena, priložite Dokaz o uplati naknade u delu Dokumentacija (na mestu predviđenom za dokaz o uplati naknade), kako biste mogli da podnesete izveštaj.');

        #Provera negativnih AOP-a
        lista=""
        #ima negativni aop (408) koji je dozvoljen u obrascu bs dupf otud do 407 
        lista_bs = find_negativni(bs, 1, 407, 5, 7)
        #pa od 409 do 416 obzirom da je aopsum na 417 i tu mora da bude dozvoljena negativna vrednost
        lista_bs_2 = find_negativni(bs, 409, 416, 5, 7)
        lista_bu = find_negativni(bu, 1001, 1040, 5, 6)

        if (len(lista_bs) > 0):
            lista = lista_bs
        if len(lista_bs_2) > 0:
            if len(lista) > 0:
                lista = lista + ", " + lista_bs_2
            else:
                lista = lista_bs_2
        if len(lista_bu) > 0:
            if len(lista) > 0:
                lista = lista + ", " + lista_bu
            else:
                lista = lista_bu                           
        
        if len(lista) > 0:                                           
            
            naziv_obrasca='Bilans stanja'
            poruka  ="Unete vrednosti ne mogu biti negativne ! (" + lista + ")"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ="Unete vrednosti ne mogu biti negativne ! (" + lista + ")"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
     
 
        
        #BILANS STANJA - POTREBNO JE OBEZBEDITI UNOS IZNOSA SA PREDZNAKOM - (MINUS) NA AOP POZICIJI 0408 KOL. 5,6 I 7
        #00001
        if not( suma(bs,1,13,5)+suma(bs,401,417,5) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0013) kol. 5 +  (0401 do 0417) kol. 5 > 0 Bilans stanja, po pravilu, mora imati iskazane podatke za tekući izveštajni period; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #00002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,13,6)+suma(bs,401,417,6) == 0 ):
                lzbir =  suma(bs,1,13,6)+suma(bs,401,417,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0013) kol. 6 +  (0401 do 0417) kol. 6 = 0 Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00003
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,13,7)+suma(bs,401,417,7) == 0 ):
                lzbir =  suma(bs,1,13,7)+suma(bs,401,417,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0013) kol. 7 +  (0401 do 0417) kol. 7 = 0 Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00004
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,13,6)+suma(bs,401,417,6) > 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0013) kol. 6 +  (0401 do 0417) kol. 6 > 0 Bilans stanja, po pravilu, mora imati iskazane podatke za prethodni izveštajni period; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #00005
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,13,7)+suma(bs,401,417,7) > 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0013) kol. 7 +  (0401 do 0417) kol. 7 > 0 Bilans stanja, po pravilu,  mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #00006
        if not( aop(bs,13,5) == suma(bs,1,12,5) ):
            lzbir =  aop(bs,13,5) 
            dzbir =  suma(bs,1,12,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0013 kol. 5 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011 + 0012) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00007
        if not( aop(bs,13,6) == suma(bs,1,12,6) ):
            lzbir =  aop(bs,13,6) 
            dzbir =  suma(bs,1,12,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0013 kol. 6 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011 + 0012) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00008
        if not( aop(bs,13,7) == suma(bs,1,12,7) ):
            lzbir =  aop(bs,13,7) 
            dzbir =  suma(bs,1,12,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0013 kol. 7 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011 + 0012) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00009
        if not( aop(bs,408,5) == suma_liste(bs,[401,402,403,405],5)-suma_liste(bs,[404,406,407],5) ):
            lzbir =  aop(bs,408,5) 
            dzbir =  suma_liste(bs,[401,402,403,405],5)-suma_liste(bs,[404,406,407],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0408 kol. 5 = AOP-u (0401 + 0402 + 0403 - 0404 + 0405 - 0406 - 0407) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00010
        if not( aop(bs,408,6) == suma_liste(bs,[401,402,403,405],6)-suma_liste(bs,[404,406,407],6) ):
            lzbir =  aop(bs,408,6) 
            dzbir =  suma_liste(bs,[401,402,403,405],6)-suma_liste(bs,[404,406,407],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0408 kol. 6 = AOP-u (0401 + 0402 + 0403 - 0404 + 0405 - 0406 - 0407) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00011
        if not( aop(bs,408,7) == suma_liste(bs,[401,402,403,405],7)-suma_liste(bs,[404,406,407],7) ):
            lzbir =  aop(bs,408,7) 
            dzbir =  suma_liste(bs,[401,402,403,405],7)-suma_liste(bs,[404,406,407],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0408 kol. 7 = AOP-u (0401 + 0402 + 0403 - 0404 + 0405 - 0406 - 0407) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00012
        if not( aop(bs,416,5) == suma(bs,409,415,5) ):
            lzbir =  aop(bs,416,5) 
            dzbir =  suma(bs,409,415,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0416 kol. 5 = AOP-u (0409 + 0410 + 0411 + 0412 + 0413 + 0414 + 0415) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00013
        if not( aop(bs,416,6) == suma(bs,409,415,6) ):
            lzbir =  aop(bs,416,6) 
            dzbir =  suma(bs,409,415,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0416 kol. 6 = AOP-u (0409 + 0410 + 0411 + 0412 + 0413 + 0414 + 0415) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00014
        if not( aop(bs,416,7) == suma(bs,409,415,7) ):
            lzbir =  aop(bs,416,7) 
            dzbir =  suma(bs,409,415,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0416 kol. 7 = AOP-u (0409 + 0410 + 0411 + 0412 + 0413 + 0414 + 0415) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00015
        if not( aop(bs,417,5) == suma_liste(bs,[408,416],5) ):
            lzbir =  aop(bs,417,5) 
            dzbir =  suma_liste(bs,[408,416],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0417 kol. 5 = AOP-u (0408 + 0416) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00016
        if not( aop(bs,417,6) == suma_liste(bs,[408,416],6) ):
            lzbir =  aop(bs,417,6) 
            dzbir =  suma_liste(bs,[408,416],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0417 kol. 6 = AOP-u (0408 + 0416) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00017
        if not( aop(bs,417,7) == suma_liste(bs,[408,416],7) ):
            lzbir =  aop(bs,417,7) 
            dzbir =  suma_liste(bs,[408,416],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0417 kol. 7 = AOP-u (0408 + 0416) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00018
        if not( aop(bs,13,5) == aop(bs,417,5) ):
            lzbir =  aop(bs,13,5) 
            dzbir =  aop(bs,417,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0013 kol. 5 = AOP-u 0417 kol. 5 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00019
        if not( aop(bs,13,6) == aop(bs,417,6) ):
            lzbir =  aop(bs,13,6) 
            dzbir =  aop(bs,417,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0013 kol. 6 = AOP-u 0417 kol. 6 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00020
        if not( aop(bs,13,7) == aop(bs,417,7) ):
            lzbir =  aop(bs,13,7) 
            dzbir =  aop(bs,417,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0013 kol. 7 = AOP-u 0417 kol. 7 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #BILANS USPEHA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        #10001
        if not( suma(bu,1001,1040,5) > 0 ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP (1001 do 1040) kol. 5 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #10002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bu,1001,1040,6) == 0 ):
                lzbir =  suma(bu,1001,1040,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Zbir podataka na oznakama za AOP (1001 do 1040) kol. 6 = 0 Bilans uspeha za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bu,1001,1040,6) > 0 ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Zbir podataka na oznakama za AOP (1001 do 1040) kol. 6 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10004
        if( suma(bu,1001,1003,5) > suma(bu,1004,1008,5) ):
            if not( aop(bu,1009,5) == suma(bu,1001,1003,5)-suma(bu,1004,1008,5) ):
                lzbir =  aop(bu,1009,5) 
                dzbir =  suma(bu,1001,1003,5)-suma(bu,1004,1008,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1009 kol. 5 = AOP-u (1001 + 1002 + 1003 - 1004 - 1005 - 1006 - 1007 - 1008) kol. 5, ako je AOP (1001 + 1002 + 1003) kol. 5 > AOP-a (1004 + 1005 + 1006 + 1007 + 1008) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10005
        if( suma(bu,1001,1003,6) > suma(bu,1004,1008,6) ):
            if not( aop(bu,1009,6) == suma(bu,1001,1003,6)-suma(bu,1004,1008,6) ):
                lzbir =  aop(bu,1009,6) 
                dzbir =  suma(bu,1001,1003,6)-suma(bu,1004,1008,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1009 kol. 6 = AOP-u (1001 + 1002 + 1003 - 1004 - 1005 - 1006 - 1007 - 1008) kol. 6, ako je AOP (1001 + 1002 + 1003) kol. 6 > AOP-a (1004 + 1005 + 1006 + 1007 + 1008) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10006
        if( suma(bu,1001,1003,5) < suma(bu,1004,1008,5) ):
            if not( aop(bu,1010,5) == suma(bu,1004,1008,5)-suma(bu,1001,1003,5) ):
                lzbir =  aop(bu,1010,5) 
                dzbir =  suma(bu,1004,1008,5)-suma(bu,1001,1003,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1010 kol. 5 = AOP-u (1004 - 1001 - 1002 - 1003 + 1005 + 1006 + 1007 + 1008) kol. 5,  ako je AOP (1001 + 1002 + 1003) kol. 5 < AOP-a (1004 + 1005 + 1006 + 1007 + 1008) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10007
        if( suma(bu,1001,1003,6) < suma(bu,1004,1008,6) ):
            if not( aop(bu,1010,6) == suma(bu,1004,1008,6)-suma(bu,1001,1003,6) ):
                lzbir =  aop(bu,1010,6) 
                dzbir =  suma(bu,1004,1008,6)-suma(bu,1001,1003,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1010 kol. 6 = AOP-u (1004 - 1001 - 1002 - 1003 + 1005 + 1006 + 1007 + 1008) kol. 6,  ako je AOP (1001 + 1002 + 1003) kol. 6 < AOP-a (1004 + 1005 + 1006 + 1007 + 1008) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10008
        if( suma(bu,1001,1003,5) == suma(bu,1004,1008,5) ):
            if not( suma(bu,1009,1010,5) == 0 ):
                lzbir =  suma(bu,1009,1010,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1009 + 1010) kol. 5 = 0,  ako je AOP (1001 + 1002 + 1003) kol. 5 = AOP-u (1004 + 1005 + 1006 + 1007 + 1008) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10009
        if( suma(bu,1001,1003,6) == suma(bu,1004,1008,6) ):
            if not( suma(bu,1009,1010,6) == 0 ):
                lzbir =  suma(bu,1009,1010,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1009 + 1010) kol. 6 = 0,  ako je AOP (1001 + 1002 + 1003) kol. 6 = AOP-u (1004 + 1005 + 1006 + 1007 + 1008) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10010
        if( aop(bu,1009,5) > 0 ):
            if not( aop(bu,1010,5) == 0 ):
                lzbir =  aop(bu,1010,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1009 kol. 5 > 0, onda je AOP 1010 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10011
        if( aop(bu,1010,5) > 0 ):
            if not( aop(bu,1009,5) == 0 ):
                lzbir =  aop(bu,1009,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1010 kol. 5 > 0, onda je AOP 1009 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10012
        if( aop(bu,1009,6) > 0 ):
            if not( aop(bu,1010,6) == 0 ):
                lzbir =  aop(bu,1010,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1009 kol. 6 > 0, onda je AOP 1010 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10013
        if( aop(bu,1010,6) > 0 ):
            if not( aop(bu,1009,6) == 0 ):
                lzbir =  aop(bu,1009,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1010 kol. 6 > 0, onda je AOP 1009 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10014
        if not( suma_liste(bu,[1001,1002,1003,1010],5) == suma(bu,1004,1009,5) ):
            lzbir =  suma_liste(bu,[1001,1002,1003,1010],5) 
            dzbir =  suma(bu,1004,1009,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1002 + 1003 + 1010) kol. 5 = AOP-u (1004 + 1005 + 1006 + 1007 + 1008 + 1009) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10015
        if not( suma_liste(bu,[1001,1002,1003,1010],6) == suma(bu,1004,1009,6) ):
            lzbir =  suma_liste(bu,[1001,1002,1003,1010],6) 
            dzbir =  suma(bu,1004,1009,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1002 + 1003 + 1010) kol. 6 = AOP-u (1004 + 1005 + 1006 + 1007 + 1008 + 1009) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10016
        if( aop(bu,1011,5) > 0 ):
            if not( aop(bu,1012,5) == 0 ):
                lzbir =  aop(bu,1012,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1011 kol. 5 > 0, onda je AOP 1012 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10017
        if( aop(bu,1012,5) > 0 ):
            if not( aop(bu,1011,5) == 0 ):
                lzbir =  aop(bu,1011,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1012 kol. 5 > 0, onda je AOP 1011 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10018
        if( aop(bu,1011,6) > 0 ):
            if not( aop(bu,1012,6) == 0 ):
                lzbir =  aop(bu,1012,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1011 kol. 6 > 0, onda je AOP 1012 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10019
        if( aop(bu,1012,6) > 0 ):
            if not( aop(bu,1011,6) == 0 ):
                lzbir =  aop(bu,1011,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1012 kol. 6 > 0, onda je AOP 1011 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10020
        if( aop(bu,1013,5) > 0 ):
            if not( aop(bu,1014,5) == 0 ):
                lzbir =  aop(bu,1014,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1013 kol. 5 > 0, onda je AOP 1014 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10021
        if( aop(bu,1014,5) > 0 ):
            if not( aop(bu,1013,5) == 0 ):
                lzbir =  aop(bu,1013,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1014 kol. 5 > 0, onda je AOP 1013 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10022
        if( aop(bu,1013,6) > 0 ):
            if not( aop(bu,1014,6) == 0 ):
                lzbir =  aop(bu,1014,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1013 kol. 6 > 0, onda je AOP 1014 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10023
        if( aop(bu,1014,6) > 0 ):
            if not( aop(bu,1013,6) == 0 ):
                lzbir =  aop(bu,1013,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1014 kol. 6 > 0, onda je AOP 1013 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10024
        if( aop(bu,1015,5) > 0 ):
            if not( aop(bu,1016,5) == 0 ):
                lzbir =  aop(bu,1016,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1015 kol. 5 > 0, onda je AOP 1016 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10025
        if( aop(bu,1016,5) > 0 ):
            if not( aop(bu,1015,5) == 0 ):
                lzbir =  aop(bu,1015,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1016 kol. 5 > 0, onda je AOP 1015 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10026
        if( aop(bu,1015,6) > 0 ):
            if not( aop(bu,1016,6) == 0 ):
                lzbir =  aop(bu,1016,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1015 kol. 6 > 0, onda je AOP 1016 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10027
        if( aop(bu,1016,6) > 0 ):
            if not( aop(bu,1015,6) == 0 ):
                lzbir =  aop(bu,1015,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1016 kol. 6 > 0, onda je AOP 1015 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10028
        if( aop(bu,1017,5) > 0 ):
            if not( aop(bu,1018,5) == 0 ):
                lzbir =  aop(bu,1018,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1017 kol. 5 > 0, onda je AOP 1018 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10029
        if( aop(bu,1018,5) > 0 ):
            if not( aop(bu,1017,5) == 0 ):
                lzbir =  aop(bu,1017,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1018 kol. 5 > 0, onda je AOP 1017 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10030
        if( aop(bu,1017,6) > 0 ):
            if not( aop(bu,1018,6) == 0 ):
                lzbir =  aop(bu,1018,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1017 kol. 6 > 0, onda je AOP 1018 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10031
        if( aop(bu,1018,6) > 0 ):
            if not( aop(bu,1017,6) == 0 ):
                lzbir =  aop(bu,1017,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1018 kol. 6 > 0, onda je AOP 1017 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10032
        if( aop(bu,1019,5) > 0 ):
            if not( aop(bu,1020,5) == 0 ):
                lzbir =  aop(bu,1020,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1019 kol. 5 > 0, onda je AOP 1020 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10033
        if( aop(bu,1020,5) > 0 ):
            if not( aop(bu,1019,5) == 0 ):
                lzbir =  aop(bu,1019,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1020 kol. 5 > 0, onda je AOP 1019 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10034
        if( aop(bu,1019,6) > 0 ):
            if not( aop(bu,1020,6) == 0 ):
                lzbir =  aop(bu,1020,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1019 kol. 6 > 0, onda je AOP 1020 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10035
        if( aop(bu,1020,6) > 0 ):
            if not( aop(bu,1019,6) == 0 ):
                lzbir =  aop(bu,1019,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1020 kol. 6 > 0, onda je AOP 1019 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10036
        if( aop(bu,1021,5) > 0 ):
            if not( aop(bu,1022,5) == 0 ):
                lzbir =  aop(bu,1022,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1021 kol. 5 > 0, onda je AOP 1022 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihodi i neto rashodi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10037
        if( aop(bu,1022,5) > 0 ):
            if not( aop(bu,1021,5) == 0 ):
                lzbir =  aop(bu,1021,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1022 kol. 5 > 0, onda je AOP 1021 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihodi i neto rashodi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10038
        if( aop(bu,1021,6) > 0 ):
            if not( aop(bu,1022,6) == 0 ):
                lzbir =  aop(bu,1022,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1021 kol. 6 > 0, onda je AOP 1022 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihodi i neto rashodi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10039
        if( aop(bu,1022,6) > 0 ):
            if not( aop(bu,1021,6) == 0 ):
                lzbir =  aop(bu,1021,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1022 kol. 6 > 0, onda je AOP 1021 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihodi i neto rashodi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10040
        if( suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],5) > suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],5) ):
            if not( aop(bu,1032,5) == suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],5)-suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],5) ):
                lzbir =  aop(bu,1032,5) 
                dzbir =  suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],5)-suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1032 kol. 5 = AOP-u (1009 - 1010 + 1011 - 1012 + 1013 - 1014 + 1015 - 1016 + 1017 - 1018 + 1019 - 1020 + 1021 - 1022 + 1023 - 1024 + 1025 - 1026 - 1027 - 1028 - 1029 + 1030 - 1031) kol. 5, ako je AOP (1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025 + 1030) kol. 5 > AOP-a (1010 + 1012 + 1014  + 1016 + 1018 + 1020 + 1022 + 1024 + 1026 + 1027 + 1028 + 1029 + 1031) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10041
        if( suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],6) > suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],6) ):
            if not( aop(bu,1032,6) == suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],6)-suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],6) ):
                lzbir =  aop(bu,1032,6) 
                dzbir =  suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],6)-suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1032 kol. 6 = AOP-u (1009 - 1010 + 1011 - 1012 + 1013 - 1014 + 1015 - 1016 + 1017 - 1018 + 1019 - 1020 + 1021 - 1022 + 1023 - 1024 + 1025 - 1026 - 1027 - 1028 - 1029 + 1030 - 1031) kol. 6, ako je AOP (1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025 + 1030) kol. 6 > AOP-a (1010 + 1012 + 1014  + 1016 + 1018 + 1020 + 1022 + 1024 + 1026 + 1027 + 1028 + 1029 + 1031) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10042
        if( suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],5) < suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],5) ):
            if not( aop(bu,1033,5) == suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],5)-suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],5) ):
                lzbir =  aop(bu,1033,5) 
                dzbir =  suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],5)-suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1033 kol. 5 = AOP-u (1010 - 1009 - 1011 + 1012 - 1013 + 1014 - 1015 + 1016 - 1017 + 1018 - 1019 + 1020 - 1021 + 1022 - 1023 + 1024 - 1025 + 1026 + 1027 + 1028 + 1029 - 1030 + 1031) kol. 5,  ako je AOP (1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025 + 1030) kol. 5 < AOP-a (1010 + 1012 + 1014  + 1016 + 1018 + 1020 + 1022 + 1024 + 1026 + 1027 + 1028 + 1029 + 1031) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10043
        if( suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],6) < suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],6) ):
            if not( aop(bu,1033,6) == suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],6)-suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],6) ):
                lzbir =  aop(bu,1033,6) 
                dzbir =  suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],6)-suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1033 kol. 6 = AOP-u (1010 - 1009 - 1011 + 1012 - 1013 + 1014 - 1015 + 1016 - 1017 + 1018 - 1019 + 1020 - 1021 + 1022 - 1023 + 1024 - 1025 + 1026 + 1027 + 1028 + 1029 - 1030 + 1031) kol. 6,  ako je AOP (1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025 + 1030) kol. 6 < AOP-a (1010 + 1012 + 1014  + 1016 + 1018 + 1020 + 1022 + 1024 + 1026 + 1027 + 1028 + 1029 + 1031) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10044
        if( suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],5) == suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],5) ):
            if not( suma(bu,1032,1033,5) == 0 ):
                lzbir =  suma(bu,1032,1033,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1032 + 1033) kol. 5 =  0, ako je AOP (1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025 + 1030) kol. 5 = AOP-u (1010 + 1012 + 1014  + 1016 + 1018 + 1020 + 1022 + 1024 + 1026 + 1027 + 1028 + 1029 + 1031) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10045
        if( suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],6) == suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],6) ):
            if not( suma(bu,1032,1033,6) == 0 ):
                lzbir =  suma(bu,1032,1033,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1032 + 1033) kol. 6 =  0, ako je AOP (1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025 + 1030) kol. 6 = AOP-u (1010 + 1012 + 1014  + 1016 + 1018 + 1020 + 1022 + 1024 + 1026 + 1027 + 1028 + 1029 + 1031) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10046
        if( aop(bu,1032,5) > 0 ):
            if not( aop(bu,1033,5) == 0 ):
                lzbir =  aop(bu,1033,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1032 kol. 5 > 0, onda je AOP 1033 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10047
        if( aop(bu,1033,5) > 0 ):
            if not( aop(bu,1032,5) == 0 ):
                lzbir =  aop(bu,1032,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1033 kol. 5 > 0, onda je AOP 1032 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10048
        if( aop(bu,1032,6) > 0 ):
            if not( aop(bu,1033,6) == 0 ):
                lzbir =  aop(bu,1033,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1032 kol. 6 > 0, onda je AOP 1033 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10049
        if( aop(bu,1033,6) > 0 ):
            if not( aop(bu,1032,6) == 0 ):
                lzbir =  aop(bu,1032,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1033 kol. 6 > 0, onda je AOP 1032 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10050
        if not( suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030,1033],5) == suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031,1032],5) ):
            lzbir =  suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030,1033],5) 
            dzbir =  suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031,1032],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025 + 1030 + 1033) kol. 5 = AOP-u (1010 + 1012 + 1014  + 1016 + 1018 + 1020 + 1022 + 1024 + 1026 + 1027 + 1028 + 1029 + 1031 + 1032) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10051
        if not( suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030,1033],6) == suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031,1032],6) ):
            lzbir =  suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030,1033],6) 
            dzbir =  suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031,1032],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025 + 1030 + 1033) kol. 6 = AOP-u (1010 + 1012 + 1014  + 1016 + 1018 + 1020 + 1022 + 1024 + 1026 + 1027 + 1028 + 1029 + 1031 + 1032) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10052
        if( suma_liste(bu,[1032,1034,1036],5) > suma_liste(bu,[1033,1035,1037,1038],5) ):
            if not( aop(bu,1039,5) == suma_liste(bu,[1032,1034,1036],5)-suma_liste(bu,[1033,1035,1037,1038],5) ):
                lzbir =  aop(bu,1039,5) 
                dzbir =  suma_liste(bu,[1032,1034,1036],5)-suma_liste(bu,[1033,1035,1037,1038],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1039 kol. 5 = AOP-u (1032 - 1033 + 1034 - 1035 + 1036 - 1037 - 1038) kol. 5 , ako je AOP (1032 + 1034 + 1036) kol. 5 > AOP-a (1033 + 1035 + 1037 + 1038) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10053
        if( suma_liste(bu,[1032,1034,1036],6) > suma_liste(bu,[1033,1035,1037,1038],6) ):
            if not( aop(bu,1039,6) == suma_liste(bu,[1032,1034,1036],6)-suma_liste(bu,[1033,1035,1037,1038],6) ):
                lzbir =  aop(bu,1039,6) 
                dzbir =  suma_liste(bu,[1032,1034,1036],6)-suma_liste(bu,[1033,1035,1037,1038],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1039 kol. 6 = AOP-u (1032 - 1033 + 1034 - 1035 + 1036 - 1037 - 1038) kol. 6 , ako je AOP (1032 + 1034 + 1036) kol. 6 > AOP-a (1033 + 1035 + 1037 + 1038) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10054
        if( suma_liste(bu,[1032,1034,1036],5) < suma_liste(bu,[1033,1035,1037,1038],5) ):
            if not( aop(bu,1040,5) == suma_liste(bu,[1033,1035,1037,1038],5)-suma_liste(bu,[1032,1034,1036],5) ):
                lzbir =  aop(bu,1040,5) 
                dzbir =  suma_liste(bu,[1033,1035,1037,1038],5)-suma_liste(bu,[1032,1034,1036],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1040 kol. 5 = AOP-u (1033 - 1032 - 1034 + 1035 - 1036 + 1037 + 1038) kol. 5, ako je AOP (1032 + 1034 + 1036) kol. 5 < AOP-a (1033 + 1035 + 1037 + 1038) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10055
        if( suma_liste(bu,[1032,1034,1036],6) < suma_liste(bu,[1033,1035,1037,1038],6) ):
            if not( aop(bu,1040,6) == suma_liste(bu,[1033,1035,1037,1038],6)-suma_liste(bu,[1032,1034,1036],6) ):
                lzbir =  aop(bu,1040,6) 
                dzbir =  suma_liste(bu,[1033,1035,1037,1038],6)-suma_liste(bu,[1032,1034,1036],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1040 kol. 6 = AOP-u (1033 - 1032 - 1034 + 1035 - 1036 + 1037 + 1038) kol. 6, ako je AOP (1032 + 1034 + 1036) kol. 6 < AOP-a (1033 + 1035 + 1037 + 1038) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10056
        if( suma_liste(bu,[1032,1034,1036],5) == suma_liste(bu,[1033,1035,1037,1038],5) ):
            if not( suma(bu,1039,1040,5) == 0 ):
                lzbir =  suma(bu,1039,1040,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1039 + 1040) kol. 5 = 0, ako je AOP (1032 + 1034 + 1036) kol. 5 = AOP-u (1033 + 1035 + 1037 + 1038) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10057
        if( suma_liste(bu,[1032,1034,1036],6) == suma_liste(bu,[1033,1035,1037,1038],6) ):
            if not( suma(bu,1039,1040,6) == 0 ):
                lzbir =  suma(bu,1039,1040,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1039 + 1040) kol. 6 = 0, ako je AOP (1032 + 1034 + 1036) kol. 6 = AOP-u (1033 + 1035 + 1037 + 1038) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10058
        if( aop(bu,1039,5) > 0 ):
            if not( aop(bu,1040,5) == 0 ):
                lzbir =  aop(bu,1040,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1039 kol. 5 > 0, onda je AOP 1040 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10059
        if( aop(bu,1040,5) > 0 ):
            if not( aop(bu,1039,5) == 0 ):
                lzbir =  aop(bu,1039,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1040 kol. 5 > 0, onda je AOP 1039 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10060
        if( aop(bu,1039,6) > 0 ):
            if not( aop(bu,1040,6) == 0 ):
                lzbir =  aop(bu,1040,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1039 kol. 6 > 0, onda je AOP 1040 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10061
        if( aop(bu,1040,6) > 0 ):
            if not( aop(bu,1039,6) == 0 ):
                lzbir =  aop(bu,1039,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1040 kol. 6 > 0, onda je AOP 1039 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10062
        if not( suma_liste(bu,[1032,1034,1036,1040],5) == suma_liste(bu,[1033,1035,1037,1038,1039],5) ):
            lzbir =  suma_liste(bu,[1032,1034,1036,1040],5) 
            dzbir =  suma_liste(bu,[1033,1035,1037,1038,1039],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1032 + 1034 + 1036 + 1040) kol. 5 = AOP-u (1033 + 1035 + 1037 + 1038 + 1039) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10063
        if not( suma_liste(bu,[1032,1034,1036,1040],6) == suma_liste(bu,[1033,1035,1037,1038,1039],6) ):
            lzbir =  suma_liste(bu,[1032,1034,1036,1040],6) 
            dzbir =  suma_liste(bu,[1033,1035,1037,1038,1039],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1032 + 1034 + 1036 + 1040) kol. 6 = AOP-u (1033 + 1035 + 1037 + 1038 + 1039) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10064
        if( aop(bu,1039,5) > 0 ):
            if not( aop(bs,405,5) >= aop(bu,1039,5) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1039 kol. 5 > 0, onda je AOP  0405 kol. 5 bilansa stanja ≥ AOP-a 1039 kol. 5  Dobitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu neraspoređenog dobitka u koloni tekuća godina u obrascu Bilans stanja; Ukoliko ti podaci nisu usaglašeni, zakonski zastupnik potpisivanjem izveštaja potvrđuje da je tako iskazan rezultat u Bilansu stanja ispravan i tačan, odnosno da je iskazan u skladu sa propisima. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1039 kol. 5 > 0, onda je AOP  0405 kol. 5 bilansa stanja ≥ AOP-a 1039 kol. 5  Dobitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu neraspoređenog dobitka u koloni tekuća godina u obrascu Bilans stanja; Ukoliko ti podaci nisu usaglašeni, zakonski zastupnik potpisivanjem izveštaja potvrđuje da je tako iskazan rezultat u Bilansu stanja ispravan i tačan, odnosno da je iskazan u skladu sa propisima. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10065
        if( aop(bu,1039,6) > 0 ):
            if not( aop(bs,405,6) >= aop(bu,1039,6) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1039 kol. 6 > 0, onda je AOP  0405 kol. 6 bilansa stanja ≥ AOP-a 1039 kol. 6 Dobitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu neraspoređenog dobitka u koloni prethodna godina u obrascu Bilans stanja.  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1039 kol. 6 > 0, onda je AOP  0405 kol. 6 bilansa stanja ≥ AOP-a 1039 kol. 6 Dobitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu neraspoređenog dobitka u koloni prethodna godina u obrascu Bilans stanja.  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10066
        if( aop(bu,1040,5) > 0 ):
            if not( aop(bs,406,5) >= aop(bu,1040,5) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1040 kol. 5 > 0, onda je AOP 0406 kol. 5 bilansa stanja ≥ AOP-a 1040 kol. 5  Gubitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu gubitka u koloni tekuća godina u obrascu Bilans stanja;  Ukoliko ti podaci nisu usaglašeni, zakonski zastupnik potpisivanjem izveštaja potvrđuje da je tako iskazan rezultat u Bilansu stanja ispravan i tačan, odnosno da je iskazan u skladu sa propisima. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1040 kol. 5 > 0, onda je AOP 0406 kol. 5 bilansa stanja ≥ AOP-a 1040 kol. 5  Gubitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu gubitka u koloni tekuća godina u obrascu Bilans stanja;  Ukoliko ti podaci nisu usaglašeni, zakonski zastupnik potpisivanjem izveštaja potvrđuje da je tako iskazan rezultat u Bilansu stanja ispravan i tačan, odnosno da je iskazan u skladu sa propisima. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10067
        if( aop(bu,1040,6) > 0 ):
            if not( aop(bs,406,6) >= aop(bu,1040,6) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1040 kol. 6 > 0, onda je AOP 0406 kol. 6 bilansa stanja ≥ AOP-a 1040 kol. 6 Gubitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu gubitka u koloni prethodna godina u obrascu Bilans stanja.   '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1040 kol. 6 > 0, onda je AOP 0406 kol. 6 bilansa stanja ≥ AOP-a 1040 kol. 6 Gubitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu gubitka u koloni prethodna godina u obrascu Bilans stanja.   '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #############################################
        #### POCETAK KONTROLNIH PRAVILA FOND 1 ######
        #############################################
        hasWarning=False
        hasError = False      
        
        #00000
        if not(suma(fia,1,12,5) + suma(fia,1,12,6) + suma(fia,1,12,7) + suma(fia,401,410,5) + suma(fia,401,410,6) + suma(fia,401,410,7) + suma(fia,1001,1020,5) + suma(fia,1001,1020,6) > 0):
            
            naziv_obrasca='Finansijski izveštaj DPF 1'
            poruka  ="Zbir podataka na oznakama za AOP (0001 do 0012) kol. 5 + (0001 do 0012) kol. 6 + (0001 do 0012) kol. 7 bilansa stanja-izveštaja o neto imovini + (0401 do 0410) kol. 5 + (0401 do 0410) kol. 6 + (0401 do 0410) kol. 7 bilansa stanja-izveštaja o neto imovini + (1001 do 1020) kol. 5 + (1001 do 1020) kol. 6 bilansa uspeha > 0"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
                    
        #Ako ima bar jedan unet podatak u obrazac, proveravaju se greške i upozorenja. U suprotnom se ne proveravaju
        if (suma(fia,1,12,5) + suma(fia,1,12,6) + suma(fia,1,12,7) + suma(fia,401,410,5) + suma(fia,401,410,6) + suma(fia,401,410,7) + suma(fia,1001,1020,5) + suma(fia,1001,1020,6) > 0):          

            
            naziv_obrasca='Finansijski izveštaj DPF 1'
            poruka  ="----------------FINANSIJSKI IZVEŠTAJ FOND1----------------"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Obrazac'
            poruka  ="----------------FINANSIJSKI IZVEŠTAJ FOND1----------------"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)

            #00001-1
            if len(Zahtev.Forme['Finansijski izveštaj DPF 1'].TekstualnaPoljaForme["aop-10101-1"])==0:
                hasError=True                
                naziv_obrasca='Obrazac'
                poruka  ="U zaglavlju obrasca, za konkretan fond potrebno je uneti njegov naziv"
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            
            #00001
            if not((suma(fia,1,12,5)+suma(fia,401,410,5))>0):
                hasWarning=True                
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 5 > 0; Bilans stanja,po pravilu,mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "    
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 5 > 0; Bilans stanja,po pravilu,mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "    
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #00002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not((suma(fia,1,12,6)+suma(fia,401,410,6))==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 = 0; Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 = 0; Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00003
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not((suma(fia,1,12,7)+suma(fia,401,410,7))==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 7 + (0401 do 0410) kol. 7 = 0;Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 7 + (0401 do 0410) kol. 7 = 0;Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00004			
            if(Zahtev.ObveznikInfo.Novoosnovan ==False):
                if not((suma(fia,1,12,6)+suma(fia,401,410,6))>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 > 0 ; Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga   "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 > 0 ; Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga   "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00005
            if(Zahtev.ObveznikInfo.Novoosnovan== False):
                if not((suma(fia,1,12,7)+suma(fia,401,410,7))>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 7 > 0; Bilans stanja,po pravilu, mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 7 > 0; Bilans stanja,po pravilu, mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00006
            if not(aop(fia,12,5)==suma(fia,1,11,5)):
                #AOPi
                lzbir =   aop(fia,12,5)
                dzbir =   suma(fia,1,11,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 0012 kol. 5 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00007
            if not(aop(fia,12,6)==suma(fia,1,11,6)):
                #AOPi
                lzbir =   aop(fia,12,6)
                dzbir =   suma(fia,1,11,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 0012 kol. 6 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00008
            if not(aop(fia,12,7)==suma(fia,1,11,7)):
                #AOPi
                lzbir =   aop(fia,12,7)
                dzbir =   suma(fia,1,11,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 0012 kol. 7 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00009
            if not(aop(fia,404,5)== suma(fia,401,403,5)):
                #AOPi
                lzbir =   aop(fia,404,5)
                dzbir =   suma(fia,401,403,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 0404 kol. 5 = AOP-u (0401 + 0402 + 0403) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00010
            if not(aop(fia,404,6)== suma(fia,401,403,6)):
                #AOPi
                lzbir =   aop(fia,404,6)
                dzbir =   suma(fia,401,403,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 0404 kol. 6 = AOP-u (0401 + 0402 + 0403) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00011
            if not(aop(fia,404,7)==suma(fia,401,403,7)):
                #AOPi
                lzbir =   aop(fia,404,7)
                dzbir =   suma(fia,401,403,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 0404 kol. 7 = AOP-u (0401 + 0402 + 0403) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00012
            if not(aop(fia,410,5)==(suma(fia,405,407,5)-suma(fia,408,409,5))):
                #AOPi
                lzbir =   aop(fia,410,5)
                dzbir =   (suma(fia,405,407,5)-suma(fia,408,409,5))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 0410 kol. 5 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00013
            if not(aop(fia,410,6)==(suma(fia,405,407,6)-suma(fia,408,409,6))):
                #AOPi
                lzbir =   aop(fia,410,6)
                dzbir =   (suma(fia,405,407,6)-suma(fia,408,409,6))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 0410 kol. 6 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00014
            if not(aop(fia,410,7)==(suma(fia,405,407,7)-suma(fia,408,409,7))):
                #AOPi
                lzbir =   aop(fia,410,7)
                dzbir =   (suma(fia,405,407,7)-suma(fia,408,409,7))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 0410 kol. 7 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00015
            if not(aop(fia,410,5)==aop(fia,12,5)-aop(fia,404,5)):
                #AOPi
                lzbir =   aop(fia,410,5)
                dzbir =   aop(fia,12,5)-aop(fia,404,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 0410 kol. 5 = AOP-u (0012 - 0404) kol. 5; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00016
            if not(aop(fia,410,6)==aop(fia,12,6)-aop(fia,404,6)):
                #AOPi
                lzbir =   aop(fia,410,6)
                dzbir =   aop(fia,12,6)-aop(fia,404,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 0410 kol. 6 = AOP-u (0012 - 0404) kol. 6; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00017
            if not(aop(fia,410,7) == aop(fia,12,7)-aop(fia,404,7)):
                #AOPi
                lzbir =   aop(fia,410,7) 
                dzbir =    aop(fia,12,7)-aop(fia,404,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="   AOP 0410 kol. 7 = AOP-u (0012 - 0404) kol. 7; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #10001
            if not(suma(fia,1001,1020,5)>0):
                hasWarning=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 5 > 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 5 > 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #10002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not(suma(fia,1001,1020,6)==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 = 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans uspeha'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 = 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #10003
            if(Zahtev.ObveznikInfo.Novoosnovan == False):
                if not(suma(fia,1001,1020,6)>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 > 0; Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans uspeha'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 > 0; Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #10004 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,1001,5)>0):
                if not(aop(fia,1002,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1001 kol. 5 > 0, onda je AOP 1002 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10005
            if(aop(fia,1002,5)>0):
                if not(aop(fia,1001,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="     Ako je AOP 1002 kol. 5 > 0, onda je AOP 1001 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10006 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,1001,6)>0):
                if not(aop(fia,1002,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1001 kol. 6 > 0,onda je AOP 1002 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10007
            if(aop(fia,1002,6)>0):
                if not(aop(fia,1001,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1002 kol. 6 > 0,onda je AOP 1001 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10008 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,1003,5)>0):
                if not(aop(fia,1004,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1003 kol. 5 > 0,onda je AOP 1004 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10009
            if(aop(fia,1004,5)>0):
                if not(aop(fia,1003,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1004 kol. 5 > 0,onda je AOP 1003 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10010 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,1003,6)>0):
                if not(aop(fia,1004,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1003 kol. 6 > 0,onda je AOP 1004 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10011
            if(aop(fia,1004,6)>0):
                if not(aop(fia,1003,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1004 kol. 6 > 0,onda je AOP 1003 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10012 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,1005,5)>0):
                if not(aop(fia,1006,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="  Ako je AOP 1005 kol. 5 > 0,onda je AOP 1006 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10013
            if(aop(fia,1006,5)>0):
                if not(aop(fia,1005,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="  Ako je AOP 1006 kol. 5 > 0,onda je AOP 1005 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10014 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,1005,6)>0):
                if not(aop(fia,1006,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="  Ako je AOP 1005 kol. 6 > 0,onda je AOP 1006 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10015
            if(aop(fia,1006,6)>0):
                if not(aop(fia,1005,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="  Ako je AOP 1006 kol. 6 > 0,onda je AOP 1005 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10016 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,1007,5)>0):
                if not(aop(fia,1008,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1007 kol. 5 > 0,onda je AOP 1008 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10017
            if(aop(fia,1008,5)>0):
                if not(aop(fia,1007,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1008 kol. 5 > 0,onda je AOP 1007 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10018 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,1007,6)>0):
                if not(aop(fia,1008,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1007 kol. 6 > 0,onda je AOP 1008 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10019
            if(aop(fia,1008,6)>0):
                if not(aop(fia,1007,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1008 kol. 6 > 0,onda je AOP 1007 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10020 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,1009,5)>0):
                if not(aop(fia,1010,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1009 kol. 5 > 0,onda je AOP 1010 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10021
            if(aop(fia,1010,5)>0):
                if not(aop(fia,1009,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1010 kol. 5 > 0,onda je AOP 1009 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10022 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,1009,6)>0):
                if not(aop(fia,1010,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1009 kol. 6 > 0,onda je AOP 1010 kol. 6 = 0,i obrnuto,ako je AOP 1010 kol. 6 > 0,onda je AOP 1009 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10023
            if(aop(fia,1010,6)>0):
                if not(aop(fia,1009,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1009 kol. 6 > 0,onda je AOP 1010 kol. 6 = 0,i obrnuto,ako je AOP 1010 kol. 6 > 0,onda je AOP 1009 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10024
            if(suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)>suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)):
                if not(aop(fia,1019,5)==(suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)-suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))):
                    #AOPi
                    lzbir = aop(fia,1019,5)
                    dzbir = (suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)-suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP 1019 kol. 5 = AOP-u (1001 - 1002 + 1003 - 1004 + 1005 - 1006 + 1007 - 1008 + 1009 - 1010 + 1011 + 1012 + 1013 + 1014 - 1015 - 1016 - 1017 - 1018) kol. 5, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 > AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10025
            if(suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)>suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)):
                if not(aop(fia,1019,6)==(suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)-suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))):
                    #AOPi
                    lzbir = aop(fia,1019,6)
                    dzbir = (suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)-suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP 1019 kol. 6 = AOP-u (1001 - 1002 + 1003 - 1004 + 1005 - 1006 + 1007 - 1008 + 1009 - 1010 + 1011 + 1012 + 1013 + 1014 - 1015 - 1016 - 1017 - 1018) kol. 6, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 > AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10026
            if(suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)>suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)):
                if not(aop(fia,1020,5)==(suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)-suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5))):
                    #AOPi
                    lzbir = aop(fia,1020,5)
                    dzbir = (suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)-suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP 1020 kol. 5 = AOP-u (1002 - 1001 - 1003 + 1004 - 1005 + 1006 - 1007 + 1008 - 1009 + 1010 - 1011 - 1012 - 1013 - 1014 + 1015 + 1016 + 1017 + 1018) kol. 5, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 < AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10027
            if(suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)>suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)):
                if not(aop(fia,1020,6)==(suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)-suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6))):
                    #AOPi
                    lzbir = aop(fia,1020,6)
                    dzbir = (suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)-suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP 1020 kol. 6 = AOP-u (1002 - 1001 - 1003 + 1004 - 1005 + 1006 - 1007 + 1008 - 1009 + 1010 - 1011 - 1012 - 1013 - 1014 + 1015 + 1016 + 1017 + 1018) kol. 6, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 < AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10028
            if((suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)==suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))):
                if not(suma(fia,1019,1020,5)==0):
                    #AOPi
                    lzbir = suma(fia,1019,1020,5)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP (1019 + 1020) kol. 5 = 0, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10029
            if((suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)==suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))):
                if not(suma(fia,1019,1020,6)==0):
                    #AOPi
                    lzbir = suma(fia,1019,1020,6)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP (1019 + 1020) kol. 6 = 0, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10030 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,1019,5)>0):
                if not(aop(fia,1020,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1019 kol. 5 > 0,onda je AOP 1020 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10031            
            if(aop(fia,1020,5)>0):
                if not(aop(fia,1019,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1020 kol. 5 > 0,onda je AOP 1019 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10032 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,1019,6)>0):
                if not(aop(fia,1020,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1019 kol. 6 > 0,onda je AOP 1020 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10033         
            if(aop(fia,1020,6)>0):
                if not(aop(fia,1019,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1020 kol. 6 > 0,onda je AOP 1019 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10034
            if not(suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],5)==suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],5)):
                #AOPi
                lzbir = suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],5)
                dzbir = suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],5)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014 + 1020) kol. 5 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018 + 1019) kol. 5; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                    
            #10035
            if not(suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],6)==suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],6)):
                #AOPi
                lzbir = suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],6)
                dzbir = suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],6)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014 + 1020) kol. 6 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018 + 1019) kol. 6; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

                
            

            if (hasError == False):
                form_errors.remove("----------------FINANSIJSKI IZVEŠTAJ FOND1----------------")
           
            if (hasWarning == False):
                form_warnings.remove("----------------FINANSIJSKI IZVEŠTAJ FOND1----------------")                
                
        #############################################
        #### POCETAK KONTROLNIH PRAVILA FOND 2 ######
        #############################################
        hasWarning=False
        hasError = False      
        
        #00000
        if not(suma(fia,1,12,5) + suma(fia,1,12,6) + suma(fia,1,12,7) + suma(fia,401,410,5) + suma(fia,401,410,6) + suma(fia,401,410,7) + suma(fia,1001,1020,5) + suma(fia,1001,1020,6) > 0):
            
            naziv_obrasca='Finansijski izveštaj DPF 1'
            poruka  ="Zbir podataka na oznakama za AOP (0001 do 0012) kol. 5 + (0001 do 0012) kol. 6 + (0001 do 0012) kol. 7 bilansa stanja-izveštaja o neto imovini + (0401 do 0410) kol. 5 + (0401 do 0410) kol. 6 + (0401 do 0410) kol. 7 bilansa stanja-izveštaja o neto imovini + (1001 do 1020) kol. 5 + (1001 do 1020) kol. 6 bilansa uspeha > 0"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
                    
        #Ako ima bar jedan unet podatak u obrazac, proveravaju se greške i upozorenja. U suprotnom se ne proveravaju
        if (suma(fia,1,12,5) + suma(fia,1,12,6) + suma(fia,1,12,7) + suma(fia,401,410,5) + suma(fia,401,410,6) + suma(fia,401,410,7) + suma(fia,1001,1020,5) + suma(fia,1001,1020,6) > 0):          

            
            naziv_obrasca='Finansijski izveštaj DPF 1'
            poruka  ="----------------FINANSIJSKI IZVEŠTAJ FOND2----------------"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Obrazac'
            poruka  ="----------------FINANSIJSKI IZVEŠTAJ FOND2----------------"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)

            #00001-1
            if len(Zahtev.Forme['Finansijski izveštaj DPF 2'].TekstualnaPoljaForme["aop-10101-1"])==0:
                hasError=True                
                naziv_obrasca='Obrazac'
                poruka  ="U zaglavlju obrasca, za konkretan fond potrebno je uneti njegov naziv"
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            
            #00001
            if not((suma(fib,1,12,5)+suma(fib,401,410,5))>0):
                hasWarning=True                
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 5 > 0; Bilans stanja,po pravilu,mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "    
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 5 > 0; Bilans stanja,po pravilu,mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "    
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #00002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not((suma(fib,1,12,6)+suma(fib,401,410,6))==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 = 0; Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 = 0; Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00003
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not((suma(fib,1,12,7)+suma(fib,401,410,7))==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 7 + (0401 do 0410) kol. 7 = 0;Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 7 + (0401 do 0410) kol. 7 = 0;Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00004			
            if(Zahtev.ObveznikInfo.Novoosnovan ==False):
                if not((suma(fib,1,12,6)+suma(fib,401,410,6))>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 > 0 ; Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga   "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 > 0 ; Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga   "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00005
            if(Zahtev.ObveznikInfo.Novoosnovan== False):
                if not((suma(fib,1,12,7)+suma(fib,401,410,7))>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 7 > 0; Bilans stanja,po pravilu, mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 7 > 0; Bilans stanja,po pravilu, mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00006
            if not(aop(fib,12,5)==suma(fib,1,11,5)):
                #AOPi
                lzbir =   aop(fib,12,5)
                dzbir =   suma(fib,1,11,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 0012 kol. 5 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00007
            if not(aop(fib,12,6)==suma(fib,1,11,6)):
                #AOPi
                lzbir =   aop(fib,12,6)
                dzbir =   suma(fib,1,11,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 0012 kol. 6 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00008
            if not(aop(fib,12,7)==suma(fib,1,11,7)):
                #AOPi
                lzbir =   aop(fib,12,7)
                dzbir =   suma(fib,1,11,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 0012 kol. 7 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00009
            if not(aop(fib,404,5)== suma(fib,401,403,5)):
                #AOPi
                lzbir =   aop(fib,404,5)
                dzbir =   suma(fib,401,403,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 0404 kol. 5 = AOP-u (0401 + 0402 + 0403) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00010
            if not(aop(fib,404,6)== suma(fib,401,403,6)):
                #AOPi
                lzbir =   aop(fib,404,6)
                dzbir =   suma(fib,401,403,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 0404 kol. 6 = AOP-u (0401 + 0402 + 0403) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00011
            if not(aop(fib,404,7)==suma(fib,401,403,7)):
                #AOPi
                lzbir =   aop(fib,404,7)
                dzbir =   suma(fib,401,403,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 0404 kol. 7 = AOP-u (0401 + 0402 + 0403) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00012
            if not(aop(fib,410,5)==(suma(fib,405,407,5)-suma(fib,408,409,5))):
                #AOPi
                lzbir =   aop(fib,410,5)
                dzbir =   (suma(fib,405,407,5)-suma(fib,408,409,5))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 0410 kol. 5 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00013
            if not(aop(fib,410,6)==(suma(fib,405,407,6)-suma(fib,408,409,6))):
                #AOPi
                lzbir =   aop(fib,410,6)
                dzbir =   (suma(fib,405,407,6)-suma(fib,408,409,6))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 0410 kol. 6 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00014
            if not(aop(fib,410,7)==(suma(fib,405,407,7)-suma(fib,408,409,7))):
                #AOPi
                lzbir =   aop(fib,410,7)
                dzbir =   (suma(fib,405,407,7)-suma(fib,408,409,7))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 0410 kol. 7 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00015
            if not(aop(fib,410,5)==aop(fib,12,5)-aop(fib,404,5)):
                #AOPi
                lzbir =   aop(fib,410,5)
                dzbir =   aop(fib,12,5)-aop(fib,404,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 0410 kol. 5 = AOP-u (0012 - 0404) kol. 5; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00016
            if not(aop(fib,410,6)==aop(fib,12,6)-aop(fib,404,6)):
                #AOPi
                lzbir =   aop(fib,410,6)
                dzbir =   aop(fib,12,6)-aop(fib,404,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 0410 kol. 6 = AOP-u (0012 - 0404) kol. 6; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00017
            if not(aop(fib,410,7) == aop(fib,12,7)-aop(fib,404,7)):
                #AOPi
                lzbir =   aop(fib,410,7) 
                dzbir =    aop(fib,12,7)-aop(fib,404,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="   AOP 0410 kol. 7 = AOP-u (0012 - 0404) kol. 7; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #10001
            if not(suma(fib,1001,1020,5)>0):
                hasWarning=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 5 > 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 5 > 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #10002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not(suma(fib,1001,1020,6)==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 = 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans uspeha'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 = 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #10003
            if(Zahtev.ObveznikInfo.Novoosnovan == False):
                if not(suma(fib,1001,1020,6)>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 > 0; Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans uspeha'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 > 0; Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #10004 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,1001,5)>0):
                if not(aop(fib,1002,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1001 kol. 5 > 0, onda je AOP 1002 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10005
            if(aop(fib,1002,5)>0):
                if not(aop(fib,1001,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="     Ako je AOP 1002 kol. 5 > 0, onda je AOP 1001 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10006 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,1001,6)>0):
                if not(aop(fib,1002,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1001 kol. 6 > 0,onda je AOP 1002 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10007
            if(aop(fib,1002,6)>0):
                if not(aop(fib,1001,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1002 kol. 6 > 0,onda je AOP 1001 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10008 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,1003,5)>0):
                if not(aop(fib,1004,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1003 kol. 5 > 0,onda je AOP 1004 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10009
            if(aop(fib,1004,5)>0):
                if not(aop(fib,1003,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1004 kol. 5 > 0,onda je AOP 1003 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10010 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,1003,6)>0):
                if not(aop(fib,1004,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1003 kol. 6 > 0,onda je AOP 1004 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10011
            if(aop(fib,1004,6)>0):
                if not(aop(fib,1003,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1004 kol. 6 > 0,onda je AOP 1003 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10012 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,1005,5)>0):
                if not(aop(fib,1006,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="  Ako je AOP 1005 kol. 5 > 0,onda je AOP 1006 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10013
            if(aop(fib,1006,5)>0):
                if not(aop(fib,1005,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="  Ako je AOP 1006 kol. 5 > 0,onda je AOP 1005 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10014 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,1005,6)>0):
                if not(aop(fib,1006,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="  Ako je AOP 1005 kol. 6 > 0,onda je AOP 1006 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10015
            if(aop(fib,1006,6)>0):
                if not(aop(fib,1005,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="  Ako je AOP 1006 kol. 6 > 0,onda je AOP 1005 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10016 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,1007,5)>0):
                if not(aop(fib,1008,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1007 kol. 5 > 0,onda je AOP 1008 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10017
            if(aop(fib,1008,5)>0):
                if not(aop(fib,1007,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1008 kol. 5 > 0,onda je AOP 1007 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10018 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,1007,6)>0):
                if not(aop(fib,1008,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1007 kol. 6 > 0,onda je AOP 1008 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10019
            if(aop(fib,1008,6)>0):
                if not(aop(fib,1007,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1008 kol. 6 > 0,onda je AOP 1007 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10020 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,1009,5)>0):
                if not(aop(fib,1010,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1009 kol. 5 > 0,onda je AOP 1010 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10021
            if(aop(fib,1010,5)>0):
                if not(aop(fib,1009,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1010 kol. 5 > 0,onda je AOP 1009 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10022 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,1009,6)>0):
                if not(aop(fib,1010,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1009 kol. 6 > 0,onda je AOP 1010 kol. 6 = 0,i obrnuto,ako je AOP 1010 kol. 6 > 0,onda je AOP 1009 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10023
            if(aop(fib,1010,6)>0):
                if not(aop(fib,1009,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1009 kol. 6 > 0,onda je AOP 1010 kol. 6 = 0,i obrnuto,ako je AOP 1010 kol. 6 > 0,onda je AOP 1009 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10024
            if(suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)>suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)):
                if not(aop(fib,1019,5)==(suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)-suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))):
                    #AOPi
                    lzbir = aop(fib,1019,5)
                    dzbir = (suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)-suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP 1019 kol. 5 = AOP-u (1001 - 1002 + 1003 - 1004 + 1005 - 1006 + 1007 - 1008 + 1009 - 1010 + 1011 + 1012 + 1013 + 1014 - 1015 - 1016 - 1017 - 1018) kol. 5, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 > AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10025
            if(suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)>suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)):
                if not(aop(fib,1019,6)==(suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)-suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))):
                    #AOPi
                    lzbir = aop(fib,1019,6)
                    dzbir = (suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)-suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP 1019 kol. 6 = AOP-u (1001 - 1002 + 1003 - 1004 + 1005 - 1006 + 1007 - 1008 + 1009 - 1010 + 1011 + 1012 + 1013 + 1014 - 1015 - 1016 - 1017 - 1018) kol. 6, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 > AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10026
            if(suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)>suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)):
                if not(aop(fib,1020,5)==(suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)-suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5))):
                    #AOPi
                    lzbir = aop(fib,1020,5)
                    dzbir = (suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)-suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP 1020 kol. 5 = AOP-u (1002 - 1001 - 1003 + 1004 - 1005 + 1006 - 1007 + 1008 - 1009 + 1010 - 1011 - 1012 - 1013 - 1014 + 1015 + 1016 + 1017 + 1018) kol. 5, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 < AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10027
            if(suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)>suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)):
                if not(aop(fib,1020,6)==(suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)-suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6))):
                    #AOPi
                    lzbir = aop(fib,1020,6)
                    dzbir = (suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)-suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP 1020 kol. 6 = AOP-u (1002 - 1001 - 1003 + 1004 - 1005 + 1006 - 1007 + 1008 - 1009 + 1010 - 1011 - 1012 - 1013 - 1014 + 1015 + 1016 + 1017 + 1018) kol. 6, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 < AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10028
            if((suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)==suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))):
                if not(suma(fib,1019,1020,5)==0):
                    #AOPi
                    lzbir = suma(fib,1019,1020,5)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP (1019 + 1020) kol. 5 = 0, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10029
            if((suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)==suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))):
                if not(suma(fib,1019,1020,6)==0):
                    #AOPi
                    lzbir = suma(fib,1019,1020,6)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP (1019 + 1020) kol. 6 = 0, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10030 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,1019,5)>0):
                if not(aop(fib,1020,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1019 kol. 5 > 0,onda je AOP 1020 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10031            
            if(aop(fib,1020,5)>0):
                if not(aop(fib,1019,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1020 kol. 5 > 0,onda je AOP 1019 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10032 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,1019,6)>0):
                if not(aop(fib,1020,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1019 kol. 6 > 0,onda je AOP 1020 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10033         
            if(aop(fib,1020,6)>0):
                if not(aop(fib,1019,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1020 kol. 6 > 0,onda je AOP 1019 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10034
            if not(suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],5)==suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],5)):
                #AOPi
                lzbir = suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],5)
                dzbir = suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],5)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014 + 1020) kol. 5 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018 + 1019) kol. 5; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                    
            #10035
            if not(suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],6)==suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],6)):
                #AOPi
                lzbir = suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],6)
                dzbir = suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],6)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014 + 1020) kol. 6 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018 + 1019) kol. 6; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

                
            

            if (hasError == False):
                form_errors.remove("----------------FINANSIJSKI IZVEŠTAJ FOND2----------------")
           
            if (hasWarning == False):
                form_warnings.remove("----------------FINANSIJSKI IZVEŠTAJ FOND2----------------")                
                
        #############################################
        #### POCETAK KONTROLNIH PRAVILA FOND 3 ######
        #############################################
        hasWarning=False
        hasError = False      
        
        #00000
        if not(suma(fia,1,12,5) + suma(fia,1,12,6) + suma(fia,1,12,7) + suma(fia,401,410,5) + suma(fia,401,410,6) + suma(fia,401,410,7) + suma(fia,1001,1020,5) + suma(fia,1001,1020,6) > 0):
            
            naziv_obrasca='Finansijski izveštaj DPF 1'
            poruka  ="Zbir podataka na oznakama za AOP (0001 do 0012) kol. 5 + (0001 do 0012) kol. 6 + (0001 do 0012) kol. 7 bilansa stanja-izveštaja o neto imovini + (0401 do 0410) kol. 5 + (0401 do 0410) kol. 6 + (0401 do 0410) kol. 7 bilansa stanja-izveštaja o neto imovini + (1001 do 1020) kol. 5 + (1001 do 1020) kol. 6 bilansa uspeha > 0"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
                    
        #Ako ima bar jedan unet podatak u obrazac, proveravaju se greške i upozorenja. U suprotnom se ne proveravaju
        if (suma(fia,1,12,5) + suma(fia,1,12,6) + suma(fia,1,12,7) + suma(fia,401,410,5) + suma(fia,401,410,6) + suma(fia,401,410,7) + suma(fia,1001,1020,5) + suma(fia,1001,1020,6) > 0):          

            
            naziv_obrasca='Finansijski izveštaj DPF 1'
            poruka  ="----------------FINANSIJSKI IZVEŠTAJ FOND3----------------"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Obrazac'
            poruka  ="----------------FINANSIJSKI IZVEŠTAJ FOND3----------------"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)

            #00001-1
            if len(Zahtev.Forme['Finansijski izveštaj DPF 3'].TekstualnaPoljaForme["aop-10101-1"])==0:
                hasError=True                
                naziv_obrasca='Obrazac'
                poruka  ="U zaglavlju obrasca, za konkretan fond potrebno je uneti njegov naziv"
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            
            #00001
            if not((suma(fic,1,12,5)+suma(fic,401,410,5))>0):
                hasWarning=True                
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 5 > 0; Bilans stanja,po pravilu,mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "    
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 5 > 0; Bilans stanja,po pravilu,mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "    
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #00002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not((suma(fic,1,12,6)+suma(fic,401,410,6))==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 = 0; Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 = 0; Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00003
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not((suma(fic,1,12,7)+suma(fic,401,410,7))==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 7 + (0401 do 0410) kol. 7 = 0;Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 7 + (0401 do 0410) kol. 7 = 0;Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00004			
            if(Zahtev.ObveznikInfo.Novoosnovan ==False):
                if not((suma(fic,1,12,6)+suma(fic,401,410,6))>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 > 0 ; Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga   "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 > 0 ; Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga   "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00005
            if(Zahtev.ObveznikInfo.Novoosnovan== False):
                if not((suma(fic,1,12,7)+suma(fic,401,410,7))>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 7 > 0; Bilans stanja,po pravilu, mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 7 > 0; Bilans stanja,po pravilu, mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00006
            if not(aop(fic,12,5)==suma(fic,1,11,5)):
                #AOPi
                lzbir =   aop(fic,12,5)
                dzbir =   suma(fic,1,11,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 0012 kol. 5 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00007
            if not(aop(fic,12,6)==suma(fic,1,11,6)):
                #AOPi
                lzbir =   aop(fic,12,6)
                dzbir =   suma(fic,1,11,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 0012 kol. 6 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00008
            if not(aop(fic,12,7)==suma(fic,1,11,7)):
                #AOPi
                lzbir =   aop(fic,12,7)
                dzbir =   suma(fic,1,11,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 0012 kol. 7 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00009
            if not(aop(fic,404,5)== suma(fic,401,403,5)):
                #AOPi
                lzbir =   aop(fic,404,5)
                dzbir =   suma(fic,401,403,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 0404 kol. 5 = AOP-u (0401 + 0402 + 0403) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00010
            if not(aop(fic,404,6)== suma(fic,401,403,6)):
                #AOPi
                lzbir =   aop(fic,404,6)
                dzbir =   suma(fic,401,403,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 0404 kol. 6 = AOP-u (0401 + 0402 + 0403) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00011
            if not(aop(fic,404,7)==suma(fic,401,403,7)):
                #AOPi
                lzbir =   aop(fic,404,7)
                dzbir =   suma(fic,401,403,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 0404 kol. 7 = AOP-u (0401 + 0402 + 0403) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00012
            if not(aop(fic,410,5)==(suma(fic,405,407,5)-suma(fic,408,409,5))):
                #AOPi
                lzbir =   aop(fic,410,5)
                dzbir =   (suma(fic,405,407,5)-suma(fic,408,409,5))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 0410 kol. 5 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00013
            if not(aop(fic,410,6)==(suma(fic,405,407,6)-suma(fic,408,409,6))):
                #AOPi
                lzbir =   aop(fic,410,6)
                dzbir =   (suma(fic,405,407,6)-suma(fic,408,409,6))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 0410 kol. 6 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00014
            if not(aop(fic,410,7)==(suma(fic,405,407,7)-suma(fic,408,409,7))):
                #AOPi
                lzbir =   aop(fic,410,7)
                dzbir =   (suma(fic,405,407,7)-suma(fic,408,409,7))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 0410 kol. 7 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00015
            if not(aop(fic,410,5)==aop(fic,12,5)-aop(fic,404,5)):
                #AOPi
                lzbir =   aop(fic,410,5)
                dzbir =   aop(fic,12,5)-aop(fic,404,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 0410 kol. 5 = AOP-u (0012 - 0404) kol. 5; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00016
            if not(aop(fic,410,6)==aop(fic,12,6)-aop(fic,404,6)):
                #AOPi
                lzbir =   aop(fic,410,6)
                dzbir =   aop(fic,12,6)-aop(fic,404,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 0410 kol. 6 = AOP-u (0012 - 0404) kol. 6; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00017
            if not(aop(fic,410,7) == aop(fic,12,7)-aop(fic,404,7)):
                #AOPi
                lzbir =   aop(fic,410,7) 
                dzbir =    aop(fic,12,7)-aop(fic,404,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="   AOP 0410 kol. 7 = AOP-u (0012 - 0404) kol. 7; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #10001
            if not(suma(fic,1001,1020,5)>0):
                hasWarning=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 5 > 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 5 > 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #10002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not(suma(fic,1001,1020,6)==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 = 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans uspeha'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 = 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #10003
            if(Zahtev.ObveznikInfo.Novoosnovan == False):
                if not(suma(fic,1001,1020,6)>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 > 0; Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans uspeha'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 > 0; Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #10004 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,1001,5)>0):
                if not(aop(fic,1002,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1001 kol. 5 > 0, onda je AOP 1002 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10005
            if(aop(fic,1002,5)>0):
                if not(aop(fic,1001,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="     Ako je AOP 1002 kol. 5 > 0, onda je AOP 1001 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10006 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,1001,6)>0):
                if not(aop(fic,1002,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1001 kol. 6 > 0,onda je AOP 1002 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10007
            if(aop(fic,1002,6)>0):
                if not(aop(fic,1001,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1002 kol. 6 > 0,onda je AOP 1001 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10008 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,1003,5)>0):
                if not(aop(fic,1004,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1003 kol. 5 > 0,onda je AOP 1004 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10009
            if(aop(fic,1004,5)>0):
                if not(aop(fic,1003,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1004 kol. 5 > 0,onda je AOP 1003 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10010 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,1003,6)>0):
                if not(aop(fic,1004,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1003 kol. 6 > 0,onda je AOP 1004 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10011
            if(aop(fic,1004,6)>0):
                if not(aop(fic,1003,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1004 kol. 6 > 0,onda je AOP 1003 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10012 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,1005,5)>0):
                if not(aop(fic,1006,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="  Ako je AOP 1005 kol. 5 > 0,onda je AOP 1006 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10013
            if(aop(fic,1006,5)>0):
                if not(aop(fic,1005,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="  Ako je AOP 1006 kol. 5 > 0,onda je AOP 1005 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10014 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,1005,6)>0):
                if not(aop(fic,1006,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="  Ako je AOP 1005 kol. 6 > 0,onda je AOP 1006 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10015
            if(aop(fic,1006,6)>0):
                if not(aop(fic,1005,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="  Ako je AOP 1006 kol. 6 > 0,onda je AOP 1005 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10016 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,1007,5)>0):
                if not(aop(fic,1008,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1007 kol. 5 > 0,onda je AOP 1008 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10017
            if(aop(fic,1008,5)>0):
                if not(aop(fic,1007,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1008 kol. 5 > 0,onda je AOP 1007 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10018 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,1007,6)>0):
                if not(aop(fic,1008,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1007 kol. 6 > 0,onda je AOP 1008 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10019
            if(aop(fic,1008,6)>0):
                if not(aop(fic,1007,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1008 kol. 6 > 0,onda je AOP 1007 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10020 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,1009,5)>0):
                if not(aop(fic,1010,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1009 kol. 5 > 0,onda je AOP 1010 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10021
            if(aop(fic,1010,5)>0):
                if not(aop(fic,1009,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1010 kol. 5 > 0,onda je AOP 1009 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10022 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,1009,6)>0):
                if not(aop(fic,1010,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1009 kol. 6 > 0,onda je AOP 1010 kol. 6 = 0,i obrnuto,ako je AOP 1010 kol. 6 > 0,onda je AOP 1009 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10023
            if(aop(fic,1010,6)>0):
                if not(aop(fic,1009,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1009 kol. 6 > 0,onda je AOP 1010 kol. 6 = 0,i obrnuto,ako je AOP 1010 kol. 6 > 0,onda je AOP 1009 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10024
            if(suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)>suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)):
                if not(aop(fic,1019,5)==(suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)-suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))):
                    #AOPi
                    lzbir = aop(fic,1019,5)
                    dzbir = (suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)-suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP 1019 kol. 5 = AOP-u (1001 - 1002 + 1003 - 1004 + 1005 - 1006 + 1007 - 1008 + 1009 - 1010 + 1011 + 1012 + 1013 + 1014 - 1015 - 1016 - 1017 - 1018) kol. 5, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 > AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10025
            if(suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)>suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)):
                if not(aop(fic,1019,6)==(suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)-suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))):
                    #AOPi
                    lzbir = aop(fic,1019,6)
                    dzbir = (suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)-suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP 1019 kol. 6 = AOP-u (1001 - 1002 + 1003 - 1004 + 1005 - 1006 + 1007 - 1008 + 1009 - 1010 + 1011 + 1012 + 1013 + 1014 - 1015 - 1016 - 1017 - 1018) kol. 6, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 > AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10026
            if(suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)>suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)):
                if not(aop(fic,1020,5)==(suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)-suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5))):
                    #AOPi
                    lzbir = aop(fic,1020,5)
                    dzbir = (suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)-suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP 1020 kol. 5 = AOP-u (1002 - 1001 - 1003 + 1004 - 1005 + 1006 - 1007 + 1008 - 1009 + 1010 - 1011 - 1012 - 1013 - 1014 + 1015 + 1016 + 1017 + 1018) kol. 5, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 < AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10027
            if(suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)>suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)):
                if not(aop(fic,1020,6)==(suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)-suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6))):
                    #AOPi
                    lzbir = aop(fic,1020,6)
                    dzbir = (suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)-suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP 1020 kol. 6 = AOP-u (1002 - 1001 - 1003 + 1004 - 1005 + 1006 - 1007 + 1008 - 1009 + 1010 - 1011 - 1012 - 1013 - 1014 + 1015 + 1016 + 1017 + 1018) kol. 6, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 < AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10028
            if((suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)==suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))):
                if not(suma(fic,1019,1020,5)==0):
                    #AOPi
                    lzbir = suma(fic,1019,1020,5)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP (1019 + 1020) kol. 5 = 0, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10029
            if((suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)==suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))):
                if not(suma(fic,1019,1020,6)==0):
                    #AOPi
                    lzbir = suma(fic,1019,1020,6)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP (1019 + 1020) kol. 6 = 0, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10030 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,1019,5)>0):
                if not(aop(fic,1020,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1019 kol. 5 > 0,onda je AOP 1020 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10031            
            if(aop(fic,1020,5)>0):
                if not(aop(fic,1019,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1020 kol. 5 > 0,onda je AOP 1019 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10032 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,1019,6)>0):
                if not(aop(fic,1020,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1019 kol. 6 > 0,onda je AOP 1020 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10033         
            if(aop(fic,1020,6)>0):
                if not(aop(fic,1019,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1020 kol. 6 > 0,onda je AOP 1019 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10034
            if not(suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],5)==suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],5)):
                #AOPi
                lzbir = suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],5)
                dzbir = suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],5)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014 + 1020) kol. 5 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018 + 1019) kol. 5; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                    
            #10035
            if not(suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],6)==suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],6)):
                #AOPi
                lzbir = suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],6)
                dzbir = suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],6)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014 + 1020) kol. 6 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018 + 1019) kol. 6; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

                
            

            if (hasError == False):
                form_errors.remove("----------------FINANSIJSKI IZVEŠTAJ FOND3----------------")
           
            if (hasWarning == False):
                form_warnings.remove("----------------FINANSIJSKI IZVEŠTAJ FOND3----------------")                
                
        #############################################
        #### POCETAK KONTROLNIH PRAVILA FOND 4 ######
        #############################################
        hasWarning=False
        hasError = False      
        
        #00000
        if not(suma(fia,1,12,5) + suma(fia,1,12,6) + suma(fia,1,12,7) + suma(fia,401,410,5) + suma(fia,401,410,6) + suma(fia,401,410,7) + suma(fia,1001,1020,5) + suma(fia,1001,1020,6) > 0):
            
            naziv_obrasca='Finansijski izveštaj DPF 1'
            poruka  ="Zbir podataka na oznakama za AOP (0001 do 0012) kol. 5 + (0001 do 0012) kol. 6 + (0001 do 0012) kol. 7 bilansa stanja-izveštaja o neto imovini + (0401 do 0410) kol. 5 + (0401 do 0410) kol. 6 + (0401 do 0410) kol. 7 bilansa stanja-izveštaja o neto imovini + (1001 do 1020) kol. 5 + (1001 do 1020) kol. 6 bilansa uspeha > 0"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
                    
        #Ako ima bar jedan unet podatak u obrazac, proveravaju se greške i upozorenja. U suprotnom se ne proveravaju
        if (suma(fia,1,12,5) + suma(fia,1,12,6) + suma(fia,1,12,7) + suma(fia,401,410,5) + suma(fia,401,410,6) + suma(fia,401,410,7) + suma(fia,1001,1020,5) + suma(fia,1001,1020,6) > 0):          

            
            naziv_obrasca='Finansijski izveštaj DPF 1'
            poruka  ="----------------FINANSIJSKI IZVEŠTAJ FOND4----------------"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Obrazac'
            poruka  ="----------------FINANSIJSKI IZVEŠTAJ FOND4----------------"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)

            #00001-1
            if len(Zahtev.Forme['Finansijski izveštaj DPF 4'].TekstualnaPoljaForme["aop-10101-1"])==0:
                hasError=True                
                naziv_obrasca='Obrazac'
                poruka  ="U zaglavlju obrasca, za konkretan fond potrebno je uneti njegov naziv"
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            
            #00001
            if not((suma(fid,1,12,5)+suma(fid,401,410,5))>0):
                hasWarning=True                
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 5 > 0; Bilans stanja,po pravilu,mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "    
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 5 > 0; Bilans stanja,po pravilu,mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "    
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #00002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not((suma(fid,1,12,6)+suma(fid,401,410,6))==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 = 0; Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 = 0; Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00003
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not((suma(fid,1,12,7)+suma(fid,401,410,7))==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 7 + (0401 do 0410) kol. 7 = 0;Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 7 + (0401 do 0410) kol. 7 = 0;Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00004			
            if(Zahtev.ObveznikInfo.Novoosnovan ==False):
                if not((suma(fid,1,12,6)+suma(fid,401,410,6))>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 > 0 ; Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga   "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 > 0 ; Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga   "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00005
            if(Zahtev.ObveznikInfo.Novoosnovan== False):
                if not((suma(fid,1,12,7)+suma(fid,401,410,7))>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 7 > 0; Bilans stanja,po pravilu, mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 7 > 0; Bilans stanja,po pravilu, mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00006
            if not(aop(fid,12,5)==suma(fid,1,11,5)):
                #AOPi
                lzbir =   aop(fid,12,5)
                dzbir =   suma(fid,1,11,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 0012 kol. 5 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00007
            if not(aop(fid,12,6)==suma(fid,1,11,6)):
                #AOPi
                lzbir =   aop(fid,12,6)
                dzbir =   suma(fid,1,11,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 0012 kol. 6 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00008
            if not(aop(fid,12,7)==suma(fid,1,11,7)):
                #AOPi
                lzbir =   aop(fid,12,7)
                dzbir =   suma(fid,1,11,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 0012 kol. 7 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00009
            if not(aop(fid,404,5)== suma(fid,401,403,5)):
                #AOPi
                lzbir =   aop(fid,404,5)
                dzbir =   suma(fid,401,403,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 0404 kol. 5 = AOP-u (0401 + 0402 + 0403) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00010
            if not(aop(fid,404,6)== suma(fid,401,403,6)):
                #AOPi
                lzbir =   aop(fid,404,6)
                dzbir =   suma(fid,401,403,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 0404 kol. 6 = AOP-u (0401 + 0402 + 0403) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00011
            if not(aop(fid,404,7)==suma(fid,401,403,7)):
                #AOPi
                lzbir =   aop(fid,404,7)
                dzbir =   suma(fid,401,403,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 0404 kol. 7 = AOP-u (0401 + 0402 + 0403) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00012
            if not(aop(fid,410,5)==(suma(fid,405,407,5)-suma(fid,408,409,5))):
                #AOPi
                lzbir =   aop(fid,410,5)
                dzbir =   (suma(fid,405,407,5)-suma(fid,408,409,5))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 0410 kol. 5 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00013
            if not(aop(fid,410,6)==(suma(fid,405,407,6)-suma(fid,408,409,6))):
                #AOPi
                lzbir =   aop(fid,410,6)
                dzbir =   (suma(fid,405,407,6)-suma(fid,408,409,6))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 0410 kol. 6 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00014
            if not(aop(fid,410,7)==(suma(fid,405,407,7)-suma(fid,408,409,7))):
                #AOPi
                lzbir =   aop(fid,410,7)
                dzbir =   (suma(fid,405,407,7)-suma(fid,408,409,7))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 0410 kol. 7 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00015
            if not(aop(fid,410,5)==aop(fid,12,5)-aop(fid,404,5)):
                #AOPi
                lzbir =   aop(fid,410,5)
                dzbir =   aop(fid,12,5)-aop(fid,404,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 0410 kol. 5 = AOP-u (0012 - 0404) kol. 5; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00016
            if not(aop(fid,410,6)==aop(fid,12,6)-aop(fid,404,6)):
                #AOPi
                lzbir =   aop(fid,410,6)
                dzbir =   aop(fid,12,6)-aop(fid,404,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 0410 kol. 6 = AOP-u (0012 - 0404) kol. 6; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00017
            if not(aop(fid,410,7) == aop(fid,12,7)-aop(fid,404,7)):
                #AOPi
                lzbir =   aop(fid,410,7) 
                dzbir =    aop(fid,12,7)-aop(fid,404,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="   AOP 0410 kol. 7 = AOP-u (0012 - 0404) kol. 7; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #10001
            if not(suma(fid,1001,1020,5)>0):
                hasWarning=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 5 > 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 5 > 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #10002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not(suma(fid,1001,1020,6)==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 = 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans uspeha'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 = 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #10003
            if(Zahtev.ObveznikInfo.Novoosnovan == False):
                if not(suma(fid,1001,1020,6)>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 > 0; Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans uspeha'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 > 0; Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #10004 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,1001,5)>0):
                if not(aop(fid,1002,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1001 kol. 5 > 0, onda je AOP 1002 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10005
            if(aop(fid,1002,5)>0):
                if not(aop(fid,1001,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="     Ako je AOP 1002 kol. 5 > 0, onda je AOP 1001 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10006 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,1001,6)>0):
                if not(aop(fid,1002,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1001 kol. 6 > 0,onda je AOP 1002 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10007
            if(aop(fid,1002,6)>0):
                if not(aop(fid,1001,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1002 kol. 6 > 0,onda je AOP 1001 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10008 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,1003,5)>0):
                if not(aop(fid,1004,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1003 kol. 5 > 0,onda je AOP 1004 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10009
            if(aop(fid,1004,5)>0):
                if not(aop(fid,1003,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1004 kol. 5 > 0,onda je AOP 1003 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10010 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,1003,6)>0):
                if not(aop(fid,1004,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1003 kol. 6 > 0,onda je AOP 1004 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10011
            if(aop(fid,1004,6)>0):
                if not(aop(fid,1003,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1004 kol. 6 > 0,onda je AOP 1003 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10012 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,1005,5)>0):
                if not(aop(fid,1006,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="  Ako je AOP 1005 kol. 5 > 0,onda je AOP 1006 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10013
            if(aop(fid,1006,5)>0):
                if not(aop(fid,1005,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="  Ako je AOP 1006 kol. 5 > 0,onda je AOP 1005 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10014 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,1005,6)>0):
                if not(aop(fid,1006,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="  Ako je AOP 1005 kol. 6 > 0,onda je AOP 1006 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10015
            if(aop(fid,1006,6)>0):
                if not(aop(fid,1005,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="  Ako je AOP 1006 kol. 6 > 0,onda je AOP 1005 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10016 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,1007,5)>0):
                if not(aop(fid,1008,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1007 kol. 5 > 0,onda je AOP 1008 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10017
            if(aop(fid,1008,5)>0):
                if not(aop(fid,1007,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1008 kol. 5 > 0,onda je AOP 1007 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10018 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,1007,6)>0):
                if not(aop(fid,1008,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1007 kol. 6 > 0,onda je AOP 1008 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10019
            if(aop(fid,1008,6)>0):
                if not(aop(fid,1007,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1008 kol. 6 > 0,onda je AOP 1007 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10020 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,1009,5)>0):
                if not(aop(fid,1010,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1009 kol. 5 > 0,onda je AOP 1010 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10021
            if(aop(fid,1010,5)>0):
                if not(aop(fid,1009,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1010 kol. 5 > 0,onda je AOP 1009 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10022 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,1009,6)>0):
                if not(aop(fid,1010,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1009 kol. 6 > 0,onda je AOP 1010 kol. 6 = 0,i obrnuto,ako je AOP 1010 kol. 6 > 0,onda je AOP 1009 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10023
            if(aop(fid,1010,6)>0):
                if not(aop(fid,1009,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1009 kol. 6 > 0,onda je AOP 1010 kol. 6 = 0,i obrnuto,ako je AOP 1010 kol. 6 > 0,onda je AOP 1009 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10024
            if(suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)>suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)):
                if not(aop(fid,1019,5)==(suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)-suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))):
                    #AOPi
                    lzbir = aop(fid,1019,5)
                    dzbir = (suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)-suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP 1019 kol. 5 = AOP-u (1001 - 1002 + 1003 - 1004 + 1005 - 1006 + 1007 - 1008 + 1009 - 1010 + 1011 + 1012 + 1013 + 1014 - 1015 - 1016 - 1017 - 1018) kol. 5, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 > AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10025
            if(suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)>suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)):
                if not(aop(fid,1019,6)==(suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)-suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))):
                    #AOPi
                    lzbir = aop(fid,1019,6)
                    dzbir = (suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)-suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP 1019 kol. 6 = AOP-u (1001 - 1002 + 1003 - 1004 + 1005 - 1006 + 1007 - 1008 + 1009 - 1010 + 1011 + 1012 + 1013 + 1014 - 1015 - 1016 - 1017 - 1018) kol. 6, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 > AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10026
            if(suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)>suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)):
                if not(aop(fid,1020,5)==(suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)-suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5))):
                    #AOPi
                    lzbir = aop(fid,1020,5)
                    dzbir = (suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)-suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP 1020 kol. 5 = AOP-u (1002 - 1001 - 1003 + 1004 - 1005 + 1006 - 1007 + 1008 - 1009 + 1010 - 1011 - 1012 - 1013 - 1014 + 1015 + 1016 + 1017 + 1018) kol. 5, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 < AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10027
            if(suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)>suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)):
                if not(aop(fid,1020,6)==(suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)-suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6))):
                    #AOPi
                    lzbir = aop(fid,1020,6)
                    dzbir = (suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)-suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP 1020 kol. 6 = AOP-u (1002 - 1001 - 1003 + 1004 - 1005 + 1006 - 1007 + 1008 - 1009 + 1010 - 1011 - 1012 - 1013 - 1014 + 1015 + 1016 + 1017 + 1018) kol. 6, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 < AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10028
            if((suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)==suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))):
                if not(suma(fid,1019,1020,5)==0):
                    #AOPi
                    lzbir = suma(fid,1019,1020,5)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP (1019 + 1020) kol. 5 = 0, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10029
            if((suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)==suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))):
                if not(suma(fid,1019,1020,6)==0):
                    #AOPi
                    lzbir = suma(fid,1019,1020,6)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP (1019 + 1020) kol. 6 = 0, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10030 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,1019,5)>0):
                if not(aop(fid,1020,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1019 kol. 5 > 0,onda je AOP 1020 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10031            
            if(aop(fid,1020,5)>0):
                if not(aop(fid,1019,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1020 kol. 5 > 0,onda je AOP 1019 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10032 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,1019,6)>0):
                if not(aop(fid,1020,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1019 kol. 6 > 0,onda je AOP 1020 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10033         
            if(aop(fid,1020,6)>0):
                if not(aop(fid,1019,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1020 kol. 6 > 0,onda je AOP 1019 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10034
            if not(suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],5)==suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],5)):
                #AOPi
                lzbir = suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],5)
                dzbir = suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],5)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014 + 1020) kol. 5 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018 + 1019) kol. 5; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                    
            #10035
            if not(suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],6)==suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],6)):
                #AOPi
                lzbir = suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],6)
                dzbir = suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],6)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014 + 1020) kol. 6 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018 + 1019) kol. 6; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

                
            

            if (hasError == False):
                form_errors.remove("----------------FINANSIJSKI IZVEŠTAJ FOND4----------------")
           
            if (hasWarning == False):
                form_warnings.remove("----------------FINANSIJSKI IZVEŠTAJ FOND4----------------")                
                
        #############################################
        #### POCETAK KONTROLNIH PRAVILA FOND 5 ######
        #############################################
        hasWarning=False
        hasError = False      
        
        #00000
        if not(suma(fia,1,12,5) + suma(fia,1,12,6) + suma(fia,1,12,7) + suma(fia,401,410,5) + suma(fia,401,410,6) + suma(fia,401,410,7) + suma(fia,1001,1020,5) + suma(fia,1001,1020,6) > 0):
            
            naziv_obrasca='Finansijski izveštaj DPF 1'
            poruka  ="Zbir podataka na oznakama za AOP (0001 do 0012) kol. 5 + (0001 do 0012) kol. 6 + (0001 do 0012) kol. 7 bilansa stanja-izveštaja o neto imovini + (0401 do 0410) kol. 5 + (0401 do 0410) kol. 6 + (0401 do 0410) kol. 7 bilansa stanja-izveštaja o neto imovini + (1001 do 1020) kol. 5 + (1001 do 1020) kol. 6 bilansa uspeha > 0"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
                    
        #Ako ima bar jedan unet podatak u obrazac, proveravaju se greške i upozorenja. U suprotnom se ne proveravaju
        if (suma(fia,1,12,5) + suma(fia,1,12,6) + suma(fia,1,12,7) + suma(fia,401,410,5) + suma(fia,401,410,6) + suma(fia,401,410,7) + suma(fia,1001,1020,5) + suma(fia,1001,1020,6) > 0):          

            
            naziv_obrasca='Finansijski izveštaj DPF 1'
            poruka  ="----------------FINANSIJSKI IZVEŠTAJ FOND5----------------"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Obrazac'
            poruka  ="----------------FINANSIJSKI IZVEŠTAJ FOND5----------------"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)

            #00001-1
            if len(Zahtev.Forme['Finansijski izveštaj DPF 5'].TekstualnaPoljaForme["aop-10101-1"])==0:
                hasError=True                
                naziv_obrasca='Obrazac'
                poruka  ="U zaglavlju obrasca, za konkretan fond potrebno je uneti njegov naziv"
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            
            #00001
            if not((suma(fie,1,12,5)+suma(fie,401,410,5))>0):
                hasWarning=True                
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 5 > 0; Bilans stanja,po pravilu,mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "    
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 5 > 0; Bilans stanja,po pravilu,mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "    
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #00002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not((suma(fie,1,12,6)+suma(fie,401,410,6))==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 = 0; Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 = 0; Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00003
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not((suma(fie,1,12,7)+suma(fie,401,410,7))==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 7 + (0401 do 0410) kol. 7 = 0;Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 7 + (0401 do 0410) kol. 7 = 0;Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00004			
            if(Zahtev.ObveznikInfo.Novoosnovan ==False):
                if not((suma(fie,1,12,6)+suma(fie,401,410,6))>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 > 0 ; Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga   "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 > 0 ; Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga   "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00005
            if(Zahtev.ObveznikInfo.Novoosnovan== False):
                if not((suma(fie,1,12,7)+suma(fie,401,410,7))>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 7 > 0; Bilans stanja,po pravilu, mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 7 > 0; Bilans stanja,po pravilu, mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00006
            if not(aop(fie,12,5)==suma(fie,1,11,5)):
                #AOPi
                lzbir =   aop(fie,12,5)
                dzbir =   suma(fie,1,11,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 0012 kol. 5 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00007
            if not(aop(fie,12,6)==suma(fie,1,11,6)):
                #AOPi
                lzbir =   aop(fie,12,6)
                dzbir =   suma(fie,1,11,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 0012 kol. 6 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00008
            if not(aop(fie,12,7)==suma(fie,1,11,7)):
                #AOPi
                lzbir =   aop(fie,12,7)
                dzbir =   suma(fie,1,11,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 0012 kol. 7 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00009
            if not(aop(fie,404,5)== suma(fie,401,403,5)):
                #AOPi
                lzbir =   aop(fie,404,5)
                dzbir =   suma(fie,401,403,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 0404 kol. 5 = AOP-u (0401 + 0402 + 0403) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00010
            if not(aop(fie,404,6)== suma(fie,401,403,6)):
                #AOPi
                lzbir =   aop(fie,404,6)
                dzbir =   suma(fie,401,403,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 0404 kol. 6 = AOP-u (0401 + 0402 + 0403) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00011
            if not(aop(fie,404,7)==suma(fie,401,403,7)):
                #AOPi
                lzbir =   aop(fie,404,7)
                dzbir =   suma(fie,401,403,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 0404 kol. 7 = AOP-u (0401 + 0402 + 0403) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00012
            if not(aop(fie,410,5)==(suma(fie,405,407,5)-suma(fie,408,409,5))):
                #AOPi
                lzbir =   aop(fie,410,5)
                dzbir =   (suma(fie,405,407,5)-suma(fie,408,409,5))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 0410 kol. 5 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00013
            if not(aop(fie,410,6)==(suma(fie,405,407,6)-suma(fie,408,409,6))):
                #AOPi
                lzbir =   aop(fie,410,6)
                dzbir =   (suma(fie,405,407,6)-suma(fie,408,409,6))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 0410 kol. 6 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00014
            if not(aop(fie,410,7)==(suma(fie,405,407,7)-suma(fie,408,409,7))):
                #AOPi
                lzbir =   aop(fie,410,7)
                dzbir =   (suma(fie,405,407,7)-suma(fie,408,409,7))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 0410 kol. 7 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00015
            if not(aop(fie,410,5)==aop(fie,12,5)-aop(fie,404,5)):
                #AOPi
                lzbir =   aop(fie,410,5)
                dzbir =   aop(fie,12,5)-aop(fie,404,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 0410 kol. 5 = AOP-u (0012 - 0404) kol. 5; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00016
            if not(aop(fie,410,6)==aop(fie,12,6)-aop(fie,404,6)):
                #AOPi
                lzbir =   aop(fie,410,6)
                dzbir =   aop(fie,12,6)-aop(fie,404,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 0410 kol. 6 = AOP-u (0012 - 0404) kol. 6; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00017
            if not(aop(fie,410,7) == aop(fie,12,7)-aop(fie,404,7)):
                #AOPi
                lzbir =   aop(fie,410,7) 
                dzbir =    aop(fie,12,7)-aop(fie,404,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="   AOP 0410 kol. 7 = AOP-u (0012 - 0404) kol. 7; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #10001
            if not(suma(fie,1001,1020,5)>0):
                hasWarning=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 5 > 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 5 > 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #10002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not(suma(fie,1001,1020,6)==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 = 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans uspeha'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 = 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #10003
            if(Zahtev.ObveznikInfo.Novoosnovan == False):
                if not(suma(fie,1001,1020,6)>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 > 0; Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans uspeha'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 > 0; Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #10004 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,1001,5)>0):
                if not(aop(fie,1002,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1001 kol. 5 > 0, onda je AOP 1002 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10005
            if(aop(fie,1002,5)>0):
                if not(aop(fie,1001,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="     Ako je AOP 1002 kol. 5 > 0, onda je AOP 1001 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10006 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,1001,6)>0):
                if not(aop(fie,1002,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1001 kol. 6 > 0,onda je AOP 1002 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10007
            if(aop(fie,1002,6)>0):
                if not(aop(fie,1001,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1002 kol. 6 > 0,onda je AOP 1001 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10008 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,1003,5)>0):
                if not(aop(fie,1004,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1003 kol. 5 > 0,onda je AOP 1004 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10009
            if(aop(fie,1004,5)>0):
                if not(aop(fie,1003,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1004 kol. 5 > 0,onda je AOP 1003 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10010 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,1003,6)>0):
                if not(aop(fie,1004,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1003 kol. 6 > 0,onda je AOP 1004 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10011
            if(aop(fie,1004,6)>0):
                if not(aop(fie,1003,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1004 kol. 6 > 0,onda je AOP 1003 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10012 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,1005,5)>0):
                if not(aop(fie,1006,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="  Ako je AOP 1005 kol. 5 > 0,onda je AOP 1006 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10013
            if(aop(fie,1006,5)>0):
                if not(aop(fie,1005,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="  Ako je AOP 1006 kol. 5 > 0,onda je AOP 1005 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10014 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,1005,6)>0):
                if not(aop(fie,1006,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="  Ako je AOP 1005 kol. 6 > 0,onda je AOP 1006 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10015
            if(aop(fie,1006,6)>0):
                if not(aop(fie,1005,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="  Ako je AOP 1006 kol. 6 > 0,onda je AOP 1005 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10016 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,1007,5)>0):
                if not(aop(fie,1008,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1007 kol. 5 > 0,onda je AOP 1008 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10017
            if(aop(fie,1008,5)>0):
                if not(aop(fie,1007,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1008 kol. 5 > 0,onda je AOP 1007 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10018 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,1007,6)>0):
                if not(aop(fie,1008,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1007 kol. 6 > 0,onda je AOP 1008 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10019
            if(aop(fie,1008,6)>0):
                if not(aop(fie,1007,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1008 kol. 6 > 0,onda je AOP 1007 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10020 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,1009,5)>0):
                if not(aop(fie,1010,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1009 kol. 5 > 0,onda je AOP 1010 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10021
            if(aop(fie,1010,5)>0):
                if not(aop(fie,1009,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1010 kol. 5 > 0,onda je AOP 1009 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10022 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,1009,6)>0):
                if not(aop(fie,1010,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1009 kol. 6 > 0,onda je AOP 1010 kol. 6 = 0,i obrnuto,ako je AOP 1010 kol. 6 > 0,onda je AOP 1009 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10023
            if(aop(fie,1010,6)>0):
                if not(aop(fie,1009,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1009 kol. 6 > 0,onda je AOP 1010 kol. 6 = 0,i obrnuto,ako je AOP 1010 kol. 6 > 0,onda je AOP 1009 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10024
            if(suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)>suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)):
                if not(aop(fie,1019,5)==(suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)-suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))):
                    #AOPi
                    lzbir = aop(fie,1019,5)
                    dzbir = (suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)-suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP 1019 kol. 5 = AOP-u (1001 - 1002 + 1003 - 1004 + 1005 - 1006 + 1007 - 1008 + 1009 - 1010 + 1011 + 1012 + 1013 + 1014 - 1015 - 1016 - 1017 - 1018) kol. 5, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 > AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10025
            if(suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)>suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)):
                if not(aop(fie,1019,6)==(suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)-suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))):
                    #AOPi
                    lzbir = aop(fie,1019,6)
                    dzbir = (suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)-suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP 1019 kol. 6 = AOP-u (1001 - 1002 + 1003 - 1004 + 1005 - 1006 + 1007 - 1008 + 1009 - 1010 + 1011 + 1012 + 1013 + 1014 - 1015 - 1016 - 1017 - 1018) kol. 6, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 > AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10026
            if(suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)>suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)):
                if not(aop(fie,1020,5)==(suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)-suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5))):
                    #AOPi
                    lzbir = aop(fie,1020,5)
                    dzbir = (suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)-suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP 1020 kol. 5 = AOP-u (1002 - 1001 - 1003 + 1004 - 1005 + 1006 - 1007 + 1008 - 1009 + 1010 - 1011 - 1012 - 1013 - 1014 + 1015 + 1016 + 1017 + 1018) kol. 5, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 < AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10027
            if(suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)>suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)):
                if not(aop(fie,1020,6)==(suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)-suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6))):
                    #AOPi
                    lzbir = aop(fie,1020,6)
                    dzbir = (suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)-suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP 1020 kol. 6 = AOP-u (1002 - 1001 - 1003 + 1004 - 1005 + 1006 - 1007 + 1008 - 1009 + 1010 - 1011 - 1012 - 1013 - 1014 + 1015 + 1016 + 1017 + 1018) kol. 6, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 < AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10028
            if((suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)==suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))):
                if not(suma(fie,1019,1020,5)==0):
                    #AOPi
                    lzbir = suma(fie,1019,1020,5)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP (1019 + 1020) kol. 5 = 0, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10029
            if((suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)==suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))):
                if not(suma(fie,1019,1020,6)==0):
                    #AOPi
                    lzbir = suma(fie,1019,1020,6)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP (1019 + 1020) kol. 6 = 0, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10030 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,1019,5)>0):
                if not(aop(fie,1020,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1019 kol. 5 > 0,onda je AOP 1020 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10031            
            if(aop(fie,1020,5)>0):
                if not(aop(fie,1019,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1020 kol. 5 > 0,onda je AOP 1019 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10032 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,1019,6)>0):
                if not(aop(fie,1020,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1019 kol. 6 > 0,onda je AOP 1020 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10033         
            if(aop(fie,1020,6)>0):
                if not(aop(fie,1019,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1020 kol. 6 > 0,onda je AOP 1019 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10034
            if not(suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],5)==suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],5)):
                #AOPi
                lzbir = suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],5)
                dzbir = suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],5)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014 + 1020) kol. 5 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018 + 1019) kol. 5; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                    
            #10035
            if not(suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],6)==suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],6)):
                #AOPi
                lzbir = suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],6)
                dzbir = suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],6)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014 + 1020) kol. 6 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018 + 1019) kol. 6; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

                
            
            if (hasError == False):
                form_errors.remove("----------------FINANSIJSKI IZVEŠTAJ FOND5----------------")
           
            if (hasWarning == False):
                form_warnings.remove("----------------FINANSIJSKI IZVEŠTAJ FOND5----------------")                
                
        #############################################
        ####             KRAJ FONDOVA          ######
        #############################################
        
        
        ######################################
        #### KRAJ KONTROLNIH PRAVILA    ######
        ######################################

        return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}

    except Exception as e:
        #trace = traceback.format_exc() #traceback.print_tb(sys.exc_info()[2])
        trace=''
        errorMsg = e.message

        exceptionList.append({'errorMessage':errorMsg,'trace':trace})

        return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}
        
        