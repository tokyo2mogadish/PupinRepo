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

#Ako forma nema nijednu napomenu u zadatom opsegu vraca True u suprotnom False 
def proveriNapomene(aop_dict, prvi_aop, poslednji_aop, kolona):
    nemaNijednuNapomenu = True
    for aop_broj in range (prvi_aop, poslednji_aop+1):
        aop_key = broj_u_aop(aop_broj, kolona)
        if aop_dict[aop_key].strip():
            nemaNijednuNapomenu = False
            break           
    return nemaNijednuNapomenu 

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



        if len(form_errors)>0:
            return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}

        lzbir = 0
        dzbir = 0
        razlika = 0

        ######################################
        #### POCETAK KONTROLNIH PRAVILA ######
        ######################################


        #00000-1
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-2
        if not( suma(bs,1,33,5)+suma(bs,1,33,6)+suma(bs,401,427,5)+suma(bs,401,427,6)+suma(bu,1001,1064,5)+suma(bu,1001,1064,6) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP od (0001 do 0033) kol. 5 +  (0001 do 0033) kol. 6 bilansa stanja + (0401 do 0427) kol. 5 + (0401 do 0427) kol. 6 bilansa stanja + (1001 do 1064) kol. 5 + (1001 do 1064) kol. 6 bilansa uspeha > 0 Vanredni finansijski izveštaj, po pravilu ne sme biti bez podataka; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP od (0001 do 0033) kol. 5 +  (0001 do 0033) kol. 6 bilansa stanja + (0401 do 0427) kol. 5 + (0401 do 0427) kol. 6 bilansa stanja + (1001 do 1064) kol. 5 + (1001 do 1064) kol. 6 bilansa uspeha > 0 Vanredni finansijski izveštaj, po pravilu ne sme biti bez podataka; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga'
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
        lista_bs = find_negativni(bs, 1, 427, 5, 7)
        lista_bu = find_negativni(bu, 1001, 1064, 5, 6)
       
        if (len(lista_bs) > 0):
            lista = lista_bs
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

        #BILANS STANJA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #00001
        if not( suma(bs,1,33,5)+suma(bs,401,427,5) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0033) kol. 5 + (0401 do 0427) kol. 5 > 0 Bilans stanja, po pravilu, mora imati iskazane podatke za tekući izveštajni period; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #00002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,33,6)+suma(bs,401,427,6) == 0 ):
                lzbir =  suma(bs,1,33,6)+suma(bs,401,427,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0033) kol. 6 + (0401 do 0427) kol. 6 = 0 Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00003
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,33,7)+suma(bs,401,427,7) == 0 ):
                lzbir =  suma(bs,1,33,7)+suma(bs,401,427,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0033) kol. 7 + (0401 do 0427) kol. 7 = 0 Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00004
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,33,6)+suma(bs,401,427,6) > 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0033) kol. 6 + (0401 do 0427) kol. 6 > 0 Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #00005
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,33,7)+suma(bs,401,427,7) > 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0033) kol. 7 + (0401 do 0427) kol. 7 > 0 Bilans stanja, po pravilu,  mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #00006
        if not( aop(bs,1,5) == suma_liste(bs,[2,3,8,9,10,29,30,31,32,33],5) ):
            lzbir =  aop(bs,1,5) 
            dzbir =  suma_liste(bs,[2,3,8,9,10,29,30,31,32,33],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0001 kol. 5 = AOP-u (0002 + 0003 + 0008 + 0009 + 0010 + 0029 + 0030 + 0031 + 0032 + 0033) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00007
        if not( aop(bs,1,6) == suma_liste(bs,[2,3,8,9,10,29,30,31,32,33],6) ):
            lzbir =  aop(bs,1,6) 
            dzbir =  suma_liste(bs,[2,3,8,9,10,29,30,31,32,33],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0001 kol. 6 = AOP-u (0002 + 0003 + 0008 + 0009 + 0010 + 0029 + 0030 + 0031 + 0032 + 0033) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00008
        if not( aop(bs,1,7) == suma_liste(bs,[2,3,8,9,10,29,30,31,32,33],7) ):
            lzbir =  aop(bs,1,7) 
            dzbir =  suma_liste(bs,[2,3,8,9,10,29,30,31,32,33],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0001 kol. 7 = AOP-u (0002 + 0003 + 0008 + 0009 + 0010 + 0029 + 0030 + 0031 + 0032 + 0033) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00009
        if not( aop(bs,3,5) == suma(bs,4,7,5) ):
            lzbir =  aop(bs,3,5) 
            dzbir =  suma(bs,4,7,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0003 kol. 5 = AOP-u (0004 + 0005 + 0006 + 0007) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00010
        if not( aop(bs,3,6) == suma(bs,4,7,6) ):
            lzbir =  aop(bs,3,6) 
            dzbir =  suma(bs,4,7,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0003 kol. 6 = AOP-u (0004 + 0005 + 0006 + 0007) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00011
        if not( aop(bs,3,7) == suma(bs,4,7,7) ):
            lzbir =  aop(bs,3,7) 
            dzbir =  suma(bs,4,7,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0003 kol. 7 = AOP-u (0004 + 0005 + 0006 + 0007) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00012
        if not( aop(bs,10,5) == suma(bs,11,28,5) ):
            lzbir =  aop(bs,10,5) 
            dzbir =  suma(bs,11,28,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0010 kol. 5 = AOP-u (0011 + 0012 + 0013 + 0014 + 0015 + 0016 + 0017 + 0018 + 0019 + 0020 + 0021 + 0022 + 0023 + 0024 + 0025 + 0026 + 0027 + 0028) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00013
        if not( aop(bs,10,6) == suma(bs,11,28,6) ):
            lzbir =  aop(bs,10,6) 
            dzbir =  suma(bs,11,28,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0010 kol. 6 = AOP-u (0011 + 0012 + 0013 + 0014 + 0015 + 0016 + 0017 + 0018 + 0019 + 0020 + 0021 + 0022 + 0023 + 0024 + 0025 + 0026 + 0027 + 0028) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00014
        if not( aop(bs,10,7) == suma(bs,11,28,7) ):
            lzbir =  aop(bs,10,7) 
            dzbir =  suma(bs,11,28,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0010 kol. 7 = AOP-u (0011 + 0012 + 0013 + 0014 + 0015 + 0016 + 0017 + 0018 + 0019 + 0020 + 0021 + 0022 + 0023 + 0024 + 0025 + 0026 + 0027 + 0028) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00015
        if not( aop(bs,401,5) == suma(bs,402,410,5) ):
            lzbir =  aop(bs,401,5) 
            dzbir =  suma(bs,402,410,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0401 kol. 5 = AOP-u (0402 + 0403 + 0404 + 0405 + 0406 + 0407 + 0408 + 0409 + 0410) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00016
        if not( aop(bs,401,6) == suma(bs,402,410,6) ):
            lzbir =  aop(bs,401,6) 
            dzbir =  suma(bs,402,410,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0401 kol. 6 = AOP-u (0402 + 0403 + 0404 + 0405 + 0406 + 0407 + 0408 + 0409 + 0410) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00017
        if not( aop(bs,401,7) == suma(bs,402,410,7) ):
            lzbir =  aop(bs,401,7) 
            dzbir =  suma(bs,402,410,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0401 kol. 7 = AOP-u (0402 + 0403 + 0404 + 0405 + 0406 + 0407 + 0408 + 0409 + 0410) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00018
        if( aop(bs,1,5) > aop(bs,401,5) ):
            if not( aop(bs,411,5) == aop(bs,1,5)-aop(bs,401,5) ):
                lzbir =  aop(bs,411,5) 
                dzbir =  aop(bs,1,5)-aop(bs,401,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0411 kol. 5 = AOP-u (0001 - 0401) kol. 5, ako je AOP 0001 kol. 5 > AOP-a 0401 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00019
        if( aop(bs,1,6) > aop(bs,401,6) ):
            if not( aop(bs,411,6) == aop(bs,1,6)-aop(bs,401,6) ):
                lzbir =  aop(bs,411,6) 
                dzbir =  aop(bs,1,6)-aop(bs,401,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0411 kol. 6 = AOP-u (0001 - 0401) kol. 6, ako je AOP 0001 kol. 6 > AOP-a 0401 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00020
        if( aop(bs,1,7) > aop(bs,401,7) ):
            if not( aop(bs,411,7) == aop(bs,1,7)-aop(bs,401,7) ):
                lzbir =  aop(bs,411,7) 
                dzbir =  aop(bs,1,7)-aop(bs,401,7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0411 kol. 7 = AOP-u (0001 - 0401) kol. 7, ako je AOP 0001 kol. 7 > AOP-a 0401 kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00021
        if( suma_liste(bs,[412,416,417,418,419,421],5) > suma_liste(bs,[415,420,422,423],5) ):
            if not( aop(bs,411,5) == suma_liste(bs,[412,416,417,418,419,421],5)-suma_liste(bs,[415,420,422,423],5) ):
                lzbir =  aop(bs,411,5) 
                dzbir =  suma_liste(bs,[412,416,417,418,419,421],5)-suma_liste(bs,[415,420,422,423],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0411 kol. 5 = AOP-u (0412 - 0415 + 0416 + 0417 + 0418 + 0419 - 0420 + 0421 - 0422 - 0423) kol. 5, ako je AOP (0412 + 0416 + 0417 + 0418 + 0419 + 0421) kol. 5 > AOP-a (0415 + 0420 + 0422 + 0423) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00022
        if( suma_liste(bs,[412,416,417,418,419,421],6) > suma_liste(bs,[415,420,422,423],6) ):
            if not( aop(bs,411,6) == suma_liste(bs,[412,416,417,418,419,421],6)-suma_liste(bs,[415,420,422,423],6) ):
                lzbir =  aop(bs,411,6) 
                dzbir =  suma_liste(bs,[412,416,417,418,419,421],6)-suma_liste(bs,[415,420,422,423],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0411 kol. 6 = AOP-u (0412 - 0415 + 0416 + 0417 + 0418 + 0419 - 0420 + 0421 - 0422 - 0423) kol. 6, ako je AOP (0412 + 0416 + 0417 + 0418 + 0419 + 0421) kol. 6 > AOP-a (0415 + 0420 + 0422 + 0423) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00023
        if( suma_liste(bs,[412,416,417,418,419,421],7) > suma_liste(bs,[415,420,422,423],7) ):
            if not( aop(bs,411,7) == suma_liste(bs,[412,416,417,418,419,421],7)-suma_liste(bs,[415,420,422,423],7) ):
                lzbir =  aop(bs,411,7) 
                dzbir =  suma_liste(bs,[412,416,417,418,419,421],7)-suma_liste(bs,[415,420,422,423],7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0411 kol. 7 = AOP-u (0412 - 0415 + 0416 + 0417 + 0418 + 0419 - 0420 + 0421 - 0422 - 0423) kol. 7, ako je AOP (0412 + 0416 + 0417 + 0418 + 0419 + 0421) kol. 7 > AOP-a (0415 + 0420 + 0422 + 0423) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00024
        if not( aop(bs,412,5) == suma(bs,413,414,5) ):
            lzbir =  aop(bs,412,5) 
            dzbir =  suma(bs,413,414,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0412 kol. 5 = AOP-u (0413 + 0414) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00025
        if not( aop(bs,412,6) == suma(bs,413,414,6) ):
            lzbir =  aop(bs,412,6) 
            dzbir =  suma(bs,413,414,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0412 kol. 6 = AOP-u (0413 + 0414) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00026
        if not( aop(bs,412,7) == suma(bs,413,414,7) ):
            lzbir =  aop(bs,412,7) 
            dzbir =  suma(bs,413,414,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0412 kol. 7 = AOP-u (0413 + 0414) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00027
        if( aop(bs,1,5) < aop(bs,401,5) ):
            if not( aop(bs,424,5) == aop(bs,401,5)-aop(bs,1,5) ):
                lzbir =  aop(bs,424,5) 
                dzbir =  aop(bs,401,5)-aop(bs,1,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0424 kol. 5 = AOP-u (0401 - 0001) kol. 5, ako je AOP 0001 kol. 5 < AOP-a 0401 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00028
        if( aop(bs,1,6) < aop(bs,401,6) ):
            if not( aop(bs,424,6) == aop(bs,401,6)-aop(bs,1,6) ):
                lzbir =  aop(bs,424,6) 
                dzbir =  aop(bs,401,6)-aop(bs,1,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0424 kol. 6 = AOP-u (0401 - 0001) kol. 6, ako je AOP 0001 kol. 6 < AOP-a 0401 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00029
        if( aop(bs,1,7) < aop(bs,401,7) ):
            if not( aop(bs,424,7) == aop(bs,401,7)-aop(bs,1,7) ):
                lzbir =  aop(bs,424,7) 
                dzbir =  aop(bs,401,7)-aop(bs,1,7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0424 kol. 7 = AOP-u (0401 - 0001) kol. 7, ako je AOP 0001 kol. 7 < AOP-a 0401 kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00030
        if( suma_liste(bs,[412,416,417,418,419,421],5) < suma_liste(bs,[415,420,422,423],5) ):
            if not( aop(bs,424,5) == suma_liste(bs,[415,420,422,423],5)-suma_liste(bs,[412,416,417,418,419,421],5) ):
                lzbir =  aop(bs,424,5) 
                dzbir =  suma_liste(bs,[415,420,422,423],5)-suma_liste(bs,[412,416,417,418,419,421],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0424 kol. 5 = AOP-u (0415 - 0412 - 0416 - 0417 - 0418 - 0419 + 0420 - 0421 + 0422 + 0423) kol. 5, ako je AOP (0412 + 0416 + 0417 + 0418 + 0419 + 0421) kol. 5 < AOP-a (0415 + 0420 + 0422 + 0423) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00031
        if( suma_liste(bs,[412,416,417,418,419,421],6) < suma_liste(bs,[415,420,422,423],6) ):
            if not( aop(bs,424,6) == suma_liste(bs,[415,420,422,423],6)-suma_liste(bs,[412,416,417,418,419,421],6) ):
                lzbir =  aop(bs,424,6) 
                dzbir =  suma_liste(bs,[415,420,422,423],6)-suma_liste(bs,[412,416,417,418,419,421],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0424 kol. 6 = AOP-u (0415 - 0412 - 0416 - 0417 - 0418 - 0419 + 0420 - 0421 + 0422 + 0423) kol. 6, ako je AOP (0412 + 0416 + 0417 + 0418 + 0419 + 0421) kol. 6 < AOP-a (0415 + 0420 + 0422 + 0423) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00032
        if( suma_liste(bs,[412,416,417,418,419,421],7) < suma_liste(bs,[415,420,422,423],7) ):
            if not( aop(bs,424,7) == suma_liste(bs,[415,420,422,423],7)-suma_liste(bs,[412,416,417,418,419,421],7) ):
                lzbir =  aop(bs,424,7) 
                dzbir =  suma_liste(bs,[415,420,422,423],7)-suma_liste(bs,[412,416,417,418,419,421],7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0424 kol. 7 = AOP-u (0415 - 0412 - 0416 - 0417 - 0418 - 0419 + 0420 - 0421 + 0422 + 0423) kol. 7, ako je AOP (0412 + 0416 + 0417 + 0418 + 0419 + 0421) kol. 7 < AOP-a (0415 + 0420 + 0422 + 0423) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00033
        if( suma_liste(bs,[412,416,417,418,419,421],5) == suma_liste(bs,[415,420,422,423],5) ):
            if not( suma_liste(bs,[411,424],5) == 0 ):
                lzbir =  suma_liste(bs,[411,424],5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0411 + 0424) kol. 5 = 0,ako je AOP (0412 + 0416 + 0417 + 0418 + 0419 + 0421) kol. 5 = AOP-a  (0415 + 0420 + 0422 + 0423) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00034
        if( suma_liste(bs,[412,416,417,418,419,421],6) == suma_liste(bs,[415,420,422,423],6) ):
            if not( suma_liste(bs,[411,424],6) == 0 ):
                lzbir =  suma_liste(bs,[411,424],6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0411 + 0424) kol. 6 = 0, ako je AOP (0412 + 0416 + 0417 + 0418 + 0419 + 0421) kol. 6 = AOP-a  (0415 + 0420 + 0422 + 0423) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00035
        if( suma_liste(bs,[412,416,417,418,419,421],7) == suma_liste(bs,[415,420,422,423],7) ):
            if not( suma_liste(bs,[411,424],7) == 0 ):
                lzbir =  suma_liste(bs,[411,424],7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0411 + 0424) kol. 7 = 0, ako je AOP (0412 + 0416 + 0417 + 0418 + 0419 + 0421) kol. 7 = AOP-a  (0415 + 0420 + 0422 + 0423) kol. 7 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00036
        if( aop(bs,1,5) == aop(bs,401,5) ):
            if not( suma_liste(bs,[411,424],5) == 0 ):
                lzbir =  suma_liste(bs,[411,424],5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0411 + 0424) kol. 5 = 0, ako je AOP 0001 kol. 5 = AOP-u 0401 kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00037
        if( aop(bs,1,6) == aop(bs,401,6) ):
            if not( suma_liste(bs,[411,424],6) == 0 ):
                lzbir =  suma_liste(bs,[411,424],6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0411 + 0424) kol. 6 = 0, ako je AOP 0001 kol. 6 = AOP-u 0401 kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00038
        if( aop(bs,1,7) == aop(bs,401,7) ):
            if not( suma_liste(bs,[411,424],7) == 0 ):
                lzbir =  suma_liste(bs,[411,424],7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0411 + 0424) kol. 7 = 0, ako je AOP 0001 kol. 7 = AOP-u 0401 kol. 7 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00039
        if( aop(bs,411,5) > 0 ):
            if not( aop(bs,424,5) == 0 ):
                lzbir =  aop(bs,424,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0411 kol. 5 > 0 onda je AOP 0424 kol. 5 = 0  Ne mogu biti istovremeno prikazani neto imovina i gubitak iznad visine neto imovine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00040
        if( aop(bs,424,5) > 0 ):
            if not( aop(bs,411,5) == 0 ):
                lzbir =  aop(bs,411,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0424 kol. 5 > 0 onda je AOP 0411 kol. 5 = 0 Ne mogu biti istovremeno prikazani neto imovina i gubitak iznad visine neto imovine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00041
        if( aop(bs,411,6) > 0 ):
            if not( aop(bs,424,6) == 0 ):
                lzbir =  aop(bs,424,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0411 kol. 6 > 0 onda je AOP 0424 kol. 6 = 0  Ne mogu biti istovremeno prikazani neto imovina i gubitak iznad visine neto imovine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00042
        if( aop(bs,424,6) > 0 ):
            if not( aop(bs,411,6) == 0 ):
                lzbir =  aop(bs,411,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0424 kol. 6 > 0 onda je AOP 0411 kol. 6 = 0 Ne mogu biti istovremeno prikazani neto imovina i gubitak iznad visine neto imovine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00043
        if( aop(bs,411,7) > 0 ):
            if not( aop(bs,424,7) == 0 ):
                lzbir =  aop(bs,424,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0411 kol. 7 > 0 onda je AOP 0424 kol. 7 = 0  Ne mogu biti istovremeno prikazani neto imovina i gubitak iznad visine neto imovine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00044
        if( aop(bs,424,7) > 0 ):
            if not( aop(bs,411,7) == 0 ):
                lzbir =  aop(bs,411,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0424 kol. 7 > 0 onda je AOP 0411 kol. 7 = 0 Ne mogu biti istovremeno prikazani neto imovina i gubitak iznad visine neto imovine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00045
        if not( aop(bs,1,5) == suma_liste(bs,[401,411],5)-aop(bs,424,5) ):
            lzbir =  aop(bs,1,5) 
            dzbir =  suma_liste(bs,[401,411],5)-aop(bs,424,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0001 kol. 5  = AOP (0401 + 0411 - 0424) kol. 5 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00046
        if not( aop(bs,1,6) == suma_liste(bs,[401,411],6)-aop(bs,424,6) ):
            lzbir =  aop(bs,1,6) 
            dzbir =  suma_liste(bs,[401,411],6)-aop(bs,424,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0001 kol. 6  = AOP (0401 + 0411 - 0424) kol. 6 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00047
        if not( aop(bs,1,7) == suma_liste(bs,[401,411],7)-aop(bs,424,7) ):
            lzbir =  aop(bs,1,7) 
            dzbir =  suma_liste(bs,[401,411],7)-aop(bs,424,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0001 kol. 7  = AOP (0401 + 0411 - 0424) kol. 7 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00048
        if not( aop(bs,425,5) == 0 ):
            lzbir =  aop(bs,425,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0425 kol. 5 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00049
        if not( aop(bs,425,6) == 0 ):
            lzbir =  aop(bs,425,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0425 kol. 6 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00050
        if not( aop(bs,425,7) == 0 ):
            lzbir =  aop(bs,425,7) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0425 kol. 7 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00051
        if not( aop(bs,426,5) == aop(bs,427,5) ):
            lzbir =  aop(bs,426,5) 
            dzbir =  aop(bs,427,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0426 kol. 5 = AOP-u 0427 kol. 5 Kontrolno pravilo zahteva slaganje vanbilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00052
        if not( aop(bs,426,6) == aop(bs,427,6) ):
            lzbir =  aop(bs,426,6) 
            dzbir =  aop(bs,427,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0426 kol. 6 = AOP-u 0427 kol. 6 Kontrolno pravilo zahteva slaganje vanbilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00053
        if not( aop(bs,426,7) == aop(bs,427,7) ):
            lzbir =  aop(bs,426,7) 
            dzbir =  aop(bs,427,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0426 kol. 7 = AOP-u 0427 kol. 7 Kontrolno pravilo zahteva slaganje vanbilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #BILANS USPEHA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #10001
        if not( suma(bu,1001,1064,5) > 0 ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP (1001 do 1064) kol. 5 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #10002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bu,1001,1064,6) == 0 ):
                lzbir =  suma(bu,1001,1064,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Zbir podataka na oznakama za AOP (1001 do 1064) kol. 6 = 0 Bilans uspeha za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bu,1001,1064,6) > 0 ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Zbir podataka na oznakama za AOP (1001 do 1064) kol. 6 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10004
        if not( aop(bu,1001,5) == suma(bu,1002,1008,5) ):
            lzbir =  aop(bu,1001,5) 
            dzbir =  suma(bu,1002,1008,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1001 kol. 5 = AOP-u (1002 + 1003 + 1004 + 1005 + 1006 + 1007 + 1008) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10005
        if not( aop(bu,1001,6) == suma(bu,1002,1008,6) ):
            lzbir =  aop(bu,1001,6) 
            dzbir =  suma(bu,1002,1008,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1001 kol. 6 = AOP-u (1002 + 1003 + 1004 + 1005 + 1006 + 1007 + 1008) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10006
        if not( aop(bu,1009,5) == suma(bu,1010,1014,5) ):
            lzbir =  aop(bu,1009,5) 
            dzbir =  suma(bu,1010,1014,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1009 kol. 5 = AOP-u (1010 + 1011 + 1012 + 1013 + 1014) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10007
        if not( aop(bu,1009,6) == suma(bu,1010,1014,6) ):
            lzbir =  aop(bu,1009,6) 
            dzbir =  suma(bu,1010,1014,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1009 kol. 6 = AOP-u (1010 + 1011 + 1012 + 1013 + 1014) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10008
        if not( aop(bu,1015,5) == suma(bu,1016,1025,5) ):
            lzbir =  aop(bu,1015,5) 
            dzbir =  suma(bu,1016,1025,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1015 kol. 5 = AOP-u (1016 + 1017 + 1018 + 1019 + 1020 + 1021 + 1022 + 1023 + 1024 + 1025) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10009
        if not( aop(bu,1015,6) == suma(bu,1016,1025,6) ):
            lzbir =  aop(bu,1015,6) 
            dzbir =  suma(bu,1016,1025,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1015 kol. 6 = AOP-u (1016 + 1017 + 1018 + 1019 + 1020 + 1021 + 1022 + 1023 + 1024 + 1025) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10010
        if not( aop(bu,1026,5) == suma(bu,1027,1031,5) ):
            lzbir =  aop(bu,1026,5) 
            dzbir =  suma(bu,1027,1031,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1026 kol. 5 = AOP-u (1027 + 1028 + 1029 + 1030 + 1031) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10011
        if not( aop(bu,1026,6) == suma(bu,1027,1031,6) ):
            lzbir =  aop(bu,1026,6) 
            dzbir =  suma(bu,1027,1031,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1026 kol. 6 = AOP-u (1027 + 1028 + 1029 + 1030 + 1031) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10012
        if( suma_liste(bu,[1001,1009],5) > suma_liste(bu,[1015,1026],5) ):
            if not( aop(bu,1032,5) == suma_liste(bu,[1001,1009],5)-suma_liste(bu,[1015,1026],5) ):
                lzbir =  aop(bu,1032,5) 
                dzbir =  suma_liste(bu,[1001,1009],5)-suma_liste(bu,[1015,1026],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1032 kol. 5 = AOP-u (1001 + 1009 - 1015 - 1026) kol. 5, ako je AOP (1001 + 1009) kol. 5 > AOP-a (1015 + 1026) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10013
        if( suma_liste(bu,[1001,1009],6) > suma_liste(bu,[1015,1026],6) ):
            if not( aop(bu,1032,6) == suma_liste(bu,[1001,1009],6)-suma_liste(bu,[1015,1026],6) ):
                lzbir =  aop(bu,1032,6) 
                dzbir =  suma_liste(bu,[1001,1009],6)-suma_liste(bu,[1015,1026],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1032 kol. 6 = AOP-u (1001 + 1009 - 1015 - 1026) kol. 6, ako je AOP (1001 + 1009) kol. 6 > AOP-a (1015 + 1026) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10014
        if( suma_liste(bu,[1001,1009],5) < suma_liste(bu,[1015,1026],5) ):
            if not( aop(bu,1033,5) == suma_liste(bu,[1015,1026],5)-suma_liste(bu,[1001,1009],5) ):
                lzbir =  aop(bu,1033,5) 
                dzbir =  suma_liste(bu,[1015,1026],5)-suma_liste(bu,[1001,1009],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1033 kol. 5 = AOP-u (1015 + 1026 - 1001 - 1009) kol. 5,  ako je AOP (1001 + 1009) kol. 5 < AOP-a (1015 + 1026) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10015
        if( suma_liste(bu,[1001,1009],6) < suma_liste(bu,[1015,1026],6) ):
            if not( aop(bu,1033,6) == suma_liste(bu,[1015,1026],6)-suma_liste(bu,[1001,1009],6) ):
                lzbir =  aop(bu,1033,6) 
                dzbir =  suma_liste(bu,[1015,1026],6)-suma_liste(bu,[1001,1009],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1033 kol. 6 = AOP-u (1015 + 1026 - 1001 - 1009) kol. 6,  ako je AOP (1001 + 1009) kol. 6 < AOP-a (1015 + 1026) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10016
        if( suma_liste(bu,[1001,1009],5) == suma_liste(bu,[1015,1026],5) ):
            if not( suma(bu,1032,1033,5) == 0 ):
                lzbir =  suma(bu,1032,1033,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1032 + 1033) kol. 5 = 0,  ako je AOP (1001 + 1009) kol. 5 = AOP-u (1015 + 1026) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10017
        if( suma_liste(bu,[1001,1009],6) == suma_liste(bu,[1015,1026],6) ):
            if not( suma(bu,1032,1033,6) == 0 ):
                lzbir =  suma(bu,1032,1033,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1032 + 1033) kol. 6 = 0,  ako je AOP (1001 + 1009) kol. 6 = AOP-u (1015 + 1026) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10018
        if( aop(bu,1032,5) > 0 ):
            if not( aop(bu,1033,5) == 0 ):
                lzbir =  aop(bu,1033,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1032 kol. 5 > 0 onda je AOP 1033 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10019
        if( aop(bu,1033,5) > 0 ):
            if not( aop(bu,1032,5) == 0 ):
                lzbir =  aop(bu,1032,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1033 kol. 5 > 0 onda je AOP 1032 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10020
        if( aop(bu,1032,6) > 0 ):
            if not( aop(bu,1033,6) == 0 ):
                lzbir =  aop(bu,1033,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1032 kol. 6 > 0 onda je AOP 1033 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10021
        if( aop(bu,1033,6) > 0 ):
            if not( aop(bu,1032,6) == 0 ):
                lzbir =  aop(bu,1032,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1033 kol. 6 > 0 onda je AOP 1032 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10022
        if not( suma_liste(bu,[1001,1009,1033],5) == suma_liste(bu,[1015,1026,1032],5) ):
            lzbir =  suma_liste(bu,[1001,1009,1033],5) 
            dzbir =  suma_liste(bu,[1015,1026,1032],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1009 + 1033) kol. 5 = AOP-u (1015 + 1026 + 1032) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10023
        if not( suma_liste(bu,[1001,1009,1033],6) == suma_liste(bu,[1015,1026,1032],6) ):
            lzbir =  suma_liste(bu,[1001,1009,1033],6) 
            dzbir =  suma_liste(bu,[1015,1026,1032],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1009 + 1033) kol. 6 = AOP-u (1015 + 1026 + 1032) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10024
        if( aop(bu,1034,5) > aop(bu,1035,5) ):
            if not( aop(bu,1036,5) == aop(bu,1034,5)-aop(bu,1035,5) ):
                lzbir =  aop(bu,1036,5) 
                dzbir =  aop(bu,1034,5)-aop(bu,1035,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1036 kol. 5 = AOP-u (1034 - 1035) kol. 5, ako je AOP 1034 kol. 5 > AOP-a 1035 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10025
        if( aop(bu,1034,6) > aop(bu,1035,6) ):
            if not( aop(bu,1036,6) == aop(bu,1034,6)-aop(bu,1035,6) ):
                lzbir =  aop(bu,1036,6) 
                dzbir =  aop(bu,1034,6)-aop(bu,1035,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1036 kol. 6 = AOP-u (1034 - 1035) kol. 6, ako je AOP 1034 kol. 6 > AOP-a 1035 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10026
        if( aop(bu,1034,5) < aop(bu,1035,5) ):
            if not( aop(bu,1037,5) == aop(bu,1035,5)-aop(bu,1034,5) ):
                lzbir =  aop(bu,1037,5) 
                dzbir =  aop(bu,1035,5)-aop(bu,1034,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1037 kol. 5 = AOP-u (1035 - 1034) kol. 5, ako je AOP 1034 kol. 5 < AOP-a 1035 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10027
        if( aop(bu,1034,6) < aop(bu,1035,6) ):
            if not( aop(bu,1037,6) == aop(bu,1035,6)-aop(bu,1034,6) ):
                lzbir =  aop(bu,1037,6) 
                dzbir =  aop(bu,1035,6)-aop(bu,1034,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1037 kol. 6 = AOP-u (1035 - 1034) kol. 6, ako je AOP 1034 kol. 6 < AOP-a 1035 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10028
        if( aop(bu,1034,5) == aop(bu,1035,5) ):
            if not( suma(bu,1036,1037,5) == 0 ):
                lzbir =  suma(bu,1036,1037,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1036 + 1037) kol. 5 = 0, ako je AOP 1034 kol. 5 = AOP-u 1035 kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10029
        if( aop(bu,1034,6) == aop(bu,1035,6) ):
            if not( suma(bu,1036,1037,6) == 0 ):
                lzbir =  suma(bu,1036,1037,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1036 + 1037) kol. 6 = 0, ako je AOP 1034 kol. 6 = AOP-u 1035 kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10030
        if( aop(bu,1036,5) > 0 ):
            if not( aop(bu,1037,5) == 0 ):
                lzbir =  aop(bu,1037,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1036 kol. 5 > 0 onda je AOP 1037 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10031
        if( aop(bu,1037,5) > 0 ):
            if not( aop(bu,1036,5) == 0 ):
                lzbir =  aop(bu,1036,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1037 kol. 5 > 0 onda je AOP 1036 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10032
        if( aop(bu,1036,6) > 0 ):
            if not( aop(bu,1037,6) == 0 ):
                lzbir =  aop(bu,1037,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1036 kol. 6 > 0 onda je AOP 1037 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10033
        if( aop(bu,1037,6) > 0 ):
            if not( aop(bu,1036,6) == 0 ):
                lzbir =  aop(bu,1036,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1037 kol. 6 > 0 onda je AOP 1036 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10034
        if not( suma_liste(bu,[1034,1037],5) == suma(bu,1035,1036,5) ):
            lzbir =  suma_liste(bu,[1034,1037],5) 
            dzbir =  suma(bu,1035,1036,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1034 + 1037) kol. 5 = AOP-u (1035 + 1036) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10035
        if not( suma_liste(bu,[1034,1037],6) == suma(bu,1035,1036,6) ):
            lzbir =  suma_liste(bu,[1034,1037],6) 
            dzbir =  suma(bu,1035,1036,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1034 + 1037) kol. 6 = AOP-u (1035 + 1036) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10036
        if( suma_liste(bu,[1032,1036],5) > suma_liste(bu,[1033,1037],5) ):
            if not( aop(bu,1038,5) == suma_liste(bu,[1032,1036],5)-suma_liste(bu,[1033,1037],5) ):
                lzbir =  aop(bu,1038,5) 
                dzbir =  suma_liste(bu,[1032,1036],5)-suma_liste(bu,[1033,1037],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1038 kol. 5 = AOP-u (1032 - 1033 + 1036 - 1037) kol. 5, ako je AOP (1032 + 1036) kol. 5 > AOP-a (1033 + 1037) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10037
        if( suma_liste(bu,[1032,1036],6) > suma_liste(bu,[1033,1037],6) ):
            if not( aop(bu,1038,6) == suma_liste(bu,[1032,1036],6)-suma_liste(bu,[1033,1037],6) ):
                lzbir =  aop(bu,1038,6) 
                dzbir =  suma_liste(bu,[1032,1036],6)-suma_liste(bu,[1033,1037],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1038 kol. 6 = AOP-u (1032 - 1033 + 1036 - 1037) kol. 6, ako je AOP (1032 + 1036) kol. 6 > AOP-a (1033 + 1037) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10038
        if( suma_liste(bu,[1032,1036],5) < suma_liste(bu,[1033,1037],5) ):
            if not( aop(bu,1039,5) == suma_liste(bu,[1033,1037],5)-suma_liste(bu,[1032,1036],5) ):
                lzbir =  aop(bu,1039,5) 
                dzbir =  suma_liste(bu,[1033,1037],5)-suma_liste(bu,[1032,1036],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1039 kol. 5 = AOP-u (1033 - 1032 + 1037 - 1036) kol. 5, ako je AOP (1032 + 1036) kol. 5 < AOP-a (1033 + 1037) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10039
        if( suma_liste(bu,[1032,1036],6) < suma_liste(bu,[1033,1037],6) ):
            if not( aop(bu,1039,6) == suma_liste(bu,[1033,1037],6)-suma_liste(bu,[1032,1036],6) ):
                lzbir =  aop(bu,1039,6) 
                dzbir =  suma_liste(bu,[1033,1037],6)-suma_liste(bu,[1032,1036],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1039 kol. 6 = AOP-u (1033 - 1032 + 1037 - 1036) kol. 6, ako je AOP (1032 + 1036) kol. 6 < AOP-a (1033 + 1037) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10040
        if( suma_liste(bu,[1032,1036],5) == suma_liste(bu,[1033,1037],5) ):
            if not( suma(bu,1038,1039,5) == 0 ):
                lzbir =  suma(bu,1038,1039,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1038 + 1039) kol. 5 = 0, ako je AOP (1032 + 1036) kol. 5 = AOP-u (1033 + 1037) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10041
        if( suma_liste(bu,[1032,1036],6) == suma_liste(bu,[1033,1037],6) ):
            if not( suma(bu,1038,1039,6) == 0 ):
                lzbir =  suma(bu,1038,1039,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1038 + 1039) kol. 6 = 0, ako je AOP (1032 + 1036) kol. 6 = AOP-u (1033 + 1037) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10042
        if( aop(bu,1038,5) > 0 ):
            if not( aop(bu,1039,5) == 0 ):
                lzbir =  aop(bu,1039,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1038 kol. 5 > 0 onda je AOP 1039 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10043
        if( aop(bu,1039,5) > 0 ):
            if not( aop(bu,1038,5) == 0 ):
                lzbir =  aop(bu,1038,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1039 kol. 5 > 0 onda je AOP 1038 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10044
        if( aop(bu,1038,6) > 0 ):
            if not( aop(bu,1039,6) == 0 ):
                lzbir =  aop(bu,1039,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1038 kol. 6 > 0 onda je AOP 1039 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10045
        if( aop(bu,1039,6) > 0 ):
            if not( aop(bu,1038,6) == 0 ):
                lzbir =  aop(bu,1038,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1039 kol. 6 > 0 onda je AOP 1038 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10046
        if not( suma_liste(bu,[1032,1036,1039],5) == suma_liste(bu,[1033,1037,1038],5) ):
            lzbir =  suma_liste(bu,[1032,1036,1039],5) 
            dzbir =  suma_liste(bu,[1033,1037,1038],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1032 + 1036 + 1039) kol. 5 = AOP-u (1033 + 1037 + 1038) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10047
        if not( suma_liste(bu,[1032,1036,1039],6) == suma_liste(bu,[1033,1037,1038],6) ):
            lzbir =  suma_liste(bu,[1032,1036,1039],6) 
            dzbir =  suma_liste(bu,[1033,1037,1038],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1032 + 1036 + 1039) kol. 6 = AOP-u (1033 + 1037 + 1038) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10048
        if( suma_liste(bu,[1038,1042],5) > suma(bu,1039,1041,5) ):
            if not( aop(bu,1043,5) == suma_liste(bu,[1038,1042],5)-suma(bu,1039,1041,5) ):
                lzbir =  aop(bu,1043,5) 
                dzbir =  suma_liste(bu,[1038,1042],5)-suma(bu,1039,1041,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1043 kol. 5 = AOP-u (1038 - 1039 - 1040 - 1041 + 1042) kol. 5, ako je AOP (1038 + 1042) kol. 5 > AOP-a (1039 + 1040 + 1041) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10049
        if( suma_liste(bu,[1038,1042],6) > suma(bu,1039,1041,6) ):
            if not( aop(bu,1043,6) == suma_liste(bu,[1038,1042],6)-suma(bu,1039,1041,6) ):
                lzbir =  aop(bu,1043,6) 
                dzbir =  suma_liste(bu,[1038,1042],6)-suma(bu,1039,1041,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1043 kol. 6 = AOP-u (1038 - 1039 - 1040 - 1041 + 1042) kol. 6, ako je AOP (1038 + 1042) kol. 6 > AOP-a (1039 + 1040 + 1041) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10050
        if( suma_liste(bu,[1038,1042],5) < suma(bu,1039,1041,5) ):
            if not( aop(bu,1044,5) == suma(bu,1039,1041,5)-suma_liste(bu,[1038,1042],5) ):
                lzbir =  aop(bu,1044,5) 
                dzbir =  suma(bu,1039,1041,5)-suma_liste(bu,[1038,1042],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1044 kol. 5 = AOP-u (1039 - 1038 + 1040 + 1041 - 1042) kol. 5, ako je AOP (1038 + 1042) kol. 5 < AOP-a (1039 + 1040 + 1041) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10051
        if( suma_liste(bu,[1038,1042],6) < suma(bu,1039,1041,6) ):
            if not( aop(bu,1044,6) == suma(bu,1039,1041,6)-suma_liste(bu,[1038,1042],6) ):
                lzbir =  aop(bu,1044,6) 
                dzbir =  suma(bu,1039,1041,6)-suma_liste(bu,[1038,1042],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1044 kol. 6 = AOP-u (1039 - 1038 + 1040 + 1041 - 1042) kol. 6, ako je AOP (1038 + 1042) kol. 6 < AOP-a (1039 + 1040 + 1041) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10052
        if( suma_liste(bu,[1038,1042],5) == suma(bu,1039,1041,5) ):
            if not( suma(bu,1043,1044,5) == 0 ):
                lzbir =  suma(bu,1043,1044,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1043 + 1044) kol. 5 = 0, ako je AOP (1038 + 1042) kol. 5 = AOP-u (1039 + 1040 + 1041) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10053
        if( suma_liste(bu,[1038,1042],6) == suma(bu,1039,1041,6) ):
            if not( suma(bu,1043,1044,6) == 0 ):
                lzbir =  suma(bu,1043,1044,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1043 + 1044) kol. 6 = 0, ako je AOP (1038 + 1042) kol. 6 = AOP-u (1039 + 1040 + 1041) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10054
        if( aop(bu,1043,5) > 0 ):
            if not( aop(bu,1044,5) == 0 ):
                lzbir =  aop(bu,1044,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1043 kol. 5 > 0 onda je AOP 1044 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10055
        if( aop(bu,1044,5) > 0 ):
            if not( aop(bu,1043,5) == 0 ):
                lzbir =  aop(bu,1043,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1044 kol. 5 > 0 onda je AOP 1043 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10056
        if( aop(bu,1043,6) > 0 ):
            if not( aop(bu,1044,6) == 0 ):
                lzbir =  aop(bu,1044,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1043 kol. 6 > 0 onda je AOP 1044 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10057
        if( aop(bu,1044,6) > 0 ):
            if not( aop(bu,1043,6) == 0 ):
                lzbir =  aop(bu,1043,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1044 kol. 6 > 0 onda je AOP 1043 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10058
        if not( suma_liste(bu,[1038,1042,1044],5) == suma_liste(bu,[1039,1040,1041,1043],5) ):
            lzbir =  suma_liste(bu,[1038,1042,1044],5) 
            dzbir =  suma_liste(bu,[1039,1040,1041,1043],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1038 + 1042 + 1044) kol. 5 = AOP-u (1039 + 1040 + 1041 + 1043) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10059
        if not( suma_liste(bu,[1038,1042,1044],6) == suma_liste(bu,[1039,1040,1041,1043],6) ):
            lzbir =  suma_liste(bu,[1038,1042,1044],6) 
            dzbir =  suma_liste(bu,[1039,1040,1041,1043],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1038 + 1042 + 1044) kol. 6 = AOP-u (1039 + 1040 + 1041 + 1043) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10060
        if not( aop(bu,1045,5) == suma(bu,1046,1050,5) ):
            lzbir =  aop(bu,1045,5) 
            dzbir =  suma(bu,1046,1050,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1045 kol. 5 = AOP-u (1046 + 1047 + 1048 + 1049 + 1050) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10061
        if not( aop(bu,1045,6) == suma(bu,1046,1050,6) ):
            lzbir =  aop(bu,1045,6) 
            dzbir =  suma(bu,1046,1050,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1045 kol. 6 = AOP-u (1046 + 1047 + 1048 + 1049 + 1050) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10062
        if not( aop(bu,1051,5) == suma(bu,1052,1056,5) ):
            lzbir =  aop(bu,1051,5) 
            dzbir =  suma(bu,1052,1056,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1051 kol. 5 = AOP-u (1052 + 1053 + 1054 + 1055 + 1056) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10063
        if not( aop(bu,1051,6) == suma(bu,1052,1056,6) ):
            lzbir =  aop(bu,1051,6) 
            dzbir =  suma(bu,1052,1056,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1051 kol. 6 = AOP-u (1052 + 1053 + 1054 + 1055 + 1056) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10064
        if( aop(bu,1045,5) > aop(bu,1051,5) ):
            if not( aop(bu,1057,5) == aop(bu,1045,5)-aop(bu,1051,5) ):
                lzbir =  aop(bu,1057,5) 
                dzbir =  aop(bu,1045,5)-aop(bu,1051,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1057 kol. 5 = AOP-u (1045 - 1051) kol. 5, ako je AOP 1045 kol. 5 > AOP-a 1051 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10065
        if( aop(bu,1045,6) > aop(bu,1051,6) ):
            if not( aop(bu,1057,6) == aop(bu,1045,6)-aop(bu,1051,6) ):
                lzbir =  aop(bu,1057,6) 
                dzbir =  aop(bu,1045,6)-aop(bu,1051,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1057 kol. 6 = AOP-u (1045 - 1051) kol. 6, ako je AOP 1045 kol. 6 > AOP-a 1051 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10066
        if( aop(bu,1045,5) < aop(bu,1051,5) ):
            if not( aop(bu,1058,5) == aop(bu,1051,5)-aop(bu,1045,5) ):
                lzbir =  aop(bu,1058,5) 
                dzbir =  aop(bu,1051,5)-aop(bu,1045,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1058 kol. 5 = AOP-u (1051 - 1045) kol. 5, ako je AOP 1045 kol. 5 < AOP-a 1051 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10067
        if( aop(bu,1045,6) < aop(bu,1051,6) ):
            if not( aop(bu,1058,6) == aop(bu,1051,6)-aop(bu,1045,6) ):
                lzbir =  aop(bu,1058,6) 
                dzbir =  aop(bu,1051,6)-aop(bu,1045,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1058 kol. 6 = AOP-u (1051 - 1045) kol. 6, ako je AOP 1045 kol. 6 < AOP-a 1051 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10068
        if( aop(bu,1045,5) == aop(bu,1051,5) ):
            if not( suma(bu,1057,1058,5) == 0 ):
                lzbir =  suma(bu,1057,1058,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1057 + 1058) kol. 5 = 0, ako je AOP 1045 kol. 5 = AOP-u 1051 kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10069
        if( aop(bu,1045,6) == aop(bu,1051,6) ):
            if not( suma(bu,1057,1058,6) == 0 ):
                lzbir =  suma(bu,1057,1058,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1057 + 1058) kol. 6 = 0, ako je AOP 1045 kol. 6 = AOP-u 1051 kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10070
        if( aop(bu,1057,5) > 0 ):
            if not( aop(bu,1058,5) == 0 ):
                lzbir =  aop(bu,1058,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1057 kol. 5 > 0 onda je AOP 1058 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10071
        if( aop(bu,1058,5) > 0 ):
            if not( aop(bu,1057,5) == 0 ):
                lzbir =  aop(bu,1057,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1058 kol. 5 > 0 onda je AOP 1057 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10072
        if( aop(bu,1057,6) > 0 ):
            if not( aop(bu,1058,6) == 0 ):
                lzbir =  aop(bu,1058,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1057 kol. 6 > 0 onda je AOP 1058 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10073
        if( aop(bu,1058,6) > 0 ):
            if not( aop(bu,1057,6) == 0 ):
                lzbir =  aop(bu,1057,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1058 kol. 6 > 0 onda je AOP 1057 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10074
        if not( suma_liste(bu,[1045,1058],5) == suma_liste(bu,[1051,1057],5) ):
            lzbir =  suma_liste(bu,[1045,1058],5) 
            dzbir =  suma_liste(bu,[1051,1057],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1045 + 1058) kol. 5 = AOP-u (1051 + 1057) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10075
        if not( suma_liste(bu,[1045,1058],6) == suma_liste(bu,[1051,1057],6) ):
            lzbir =  suma_liste(bu,[1045,1058],6) 
            dzbir =  suma_liste(bu,[1051,1057],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1045 + 1058) kol. 6 = AOP-u (1051 + 1057) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10076
        if( suma_liste(bu,[1043,1057,1059],5) > suma_liste(bu,[1044,1058,1060],5) ):
            if not( aop(bu,1061,5) == suma_liste(bu,[1043,1057,1059],5)-suma_liste(bu,[1044,1058,1060],5) ):
                lzbir =  aop(bu,1061,5) 
                dzbir =  suma_liste(bu,[1043,1057,1059],5)-suma_liste(bu,[1044,1058,1060],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1061 kol. 5 = AOP-u (1043 - 1044 + 1057 - 1058 + 1059 - 1060) kol. 5, ako je AOP (1043 + 1057 + 1059) kol. 5 > AOP-a (1044 + 1058 + 1060) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10077
        if( suma_liste(bu,[1043,1057,1059],6) > suma_liste(bu,[1044,1058,1060],6) ):
            if not( aop(bu,1061,6) == suma_liste(bu,[1043,1057,1059],6)-suma_liste(bu,[1044,1058,1060],6) ):
                lzbir =  aop(bu,1061,6) 
                dzbir =  suma_liste(bu,[1043,1057,1059],6)-suma_liste(bu,[1044,1058,1060],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1061 kol. 6 = AOP-u (1043 - 1044 + 1057 - 1058 + 1059 - 1060) kol. 6, ako je AOP (1043 + 1057 + 1059) kol. 6 > AOP-a (1044 + 1058 + 1060) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10078
        if( suma_liste(bu,[1043,1057,1059],5) < suma_liste(bu,[1044,1058,1060],5) ):
            if not( aop(bu,1062,5) == suma_liste(bu,[1044,1058,1060],5)-suma_liste(bu,[1043,1057,1059],5) ):
                lzbir =  aop(bu,1062,5) 
                dzbir =  suma_liste(bu,[1044,1058,1060],5)-suma_liste(bu,[1043,1057,1059],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1062 kol. 5 = AOP-u (1044 - 1043 - 1057 + 1058 - 1059 + 1060) kol. 5, ako je AOP (1043 + 1057 + 1059) kol. 5 < AOP-a (1044 + 1058 + 1060) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10079
        if( suma_liste(bu,[1043,1057,1059],6) < suma_liste(bu,[1044,1058,1060],6) ):
            if not( aop(bu,1062,6) == suma_liste(bu,[1044,1058,1060],6)-suma_liste(bu,[1043,1057,1059],6) ):
                lzbir =  aop(bu,1062,6) 
                dzbir =  suma_liste(bu,[1044,1058,1060],6)-suma_liste(bu,[1043,1057,1059],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1062 kol. 6 = AOP-u (1044 - 1043 - 1057 + 1058 - 1059 + 1060) kol. 6, ako je AOP (1043 + 1057 + 1059) kol. 6 < AOP-a (1044 + 1058 + 1060) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10080
        if( suma_liste(bu,[1043,1057,1059],5) == suma_liste(bu,[1044,1058,1060],5) ):
            if not( suma(bu,1061,1062,5) == 0 ):
                lzbir =  suma(bu,1061,1062,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1061 + 1062) kol. 5 = 0,   ako je AOP (1043 + 1057 + 1059) kol. 5 = AOP-u (1044 + 1058 + 1060) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10081
        if( suma_liste(bu,[1043,1057,1059],6) == suma_liste(bu,[1044,1058,1060],6) ):
            if not( suma(bu,1061,1062,6) == 0 ):
                lzbir =  suma(bu,1061,1062,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1061 + 1062) kol. 6 = 0,   ako je AOP (1043 + 1057 + 1059) kol. 6 = AOP-u (1044 + 1058 + 1060) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10082
        if( aop(bu,1061,5) > 0 ):
            if not( aop(bu,1062,5) == 0 ):
                lzbir =  aop(bu,1062,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1061 kol. 5 > 0 onda je AOP 1062 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani povećanje  i smanjenje neto imovine od poslovanja fonda '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10083
        if( aop(bu,1062,5) > 0 ):
            if not( aop(bu,1061,5) == 0 ):
                lzbir =  aop(bu,1061,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1062 kol. 5 > 0 onda je AOP 1061 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani povećanje  i smanjenje neto imovine od poslovanja fonda '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10084
        if( aop(bu,1061,6) > 0 ):
            if not( aop(bu,1062,6) == 0 ):
                lzbir =  aop(bu,1062,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1061 kol. 6 > 0 onda je AOP 1062 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani povećanje  i smanjenje neto imovine od poslovanja fonda '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10085
        if( aop(bu,1062,6) > 0 ):
            if not( aop(bu,1061,6) == 0 ):
                lzbir =  aop(bu,1061,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1062 kol. 6 > 0 onda je AOP 1061 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani povećanje  i smanjenje neto imovine od poslovanja fonda '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10086
        if not( suma_liste(bu,[1043,1057,1059,1062],5) == suma_liste(bu,[1044,1058,1060,1061],5) ):
            lzbir =  suma_liste(bu,[1043,1057,1059,1062],5) 
            dzbir =  suma_liste(bu,[1044,1058,1060,1061],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1043 + 1057 + 1059 + 1062) kol. 5 = AOP-u (1044 + 1058 + 1060 + 1061) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10087
        if not( suma_liste(bu,[1043,1057,1059,1062],6) == suma_liste(bu,[1044,1058,1060,1061],6) ):
            lzbir =  suma_liste(bu,[1043,1057,1059,1062],6) 
            dzbir =  suma_liste(bu,[1044,1058,1060,1061],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1043 + 1057 + 1059 + 1062) kol. 6 = AOP-u (1044 + 1058 + 1060 + 1061) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10088
        if( aop(bu,1061,5) > 0 ):
            if not( aop(bs,421,5) >= aop(bu,1061,5) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1061 kol. 5 > 0, onda je AOP 0421 kol. 5 bilansa stanja ≥ AOP-a 1061 kol. 5  Povećanje neto imovine od poslovanja fonda tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti manje ili jednako iznosu Neraspoređenog dobitka u koloni tekuća godina u obrascu Bilans stanja; Ukoliko ti podaci nisu usaglašeni, zakonski zastupnik potpisivanjem izveštaja potvrđuje da je tako iskazan rezultat u Bilansu stanja ispravan i tačan, odnosno da je iskazan u skladu sa propisima. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1061 kol. 5 > 0, onda je AOP 0421 kol. 5 bilansa stanja ≥ AOP-a 1061 kol. 5  Povećanje neto imovine od poslovanja fonda tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti manje ili jednako iznosu Neraspoređenog dobitka u koloni tekuća godina u obrascu Bilans stanja; Ukoliko ti podaci nisu usaglašeni, zakonski zastupnik potpisivanjem izveštaja potvrđuje da je tako iskazan rezultat u Bilansu stanja ispravan i tačan, odnosno da je iskazan u skladu sa propisima. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10089
        if( aop(bu,1061,6) > 0 ):
            if not( aop(bs,421,6) >= aop(bu,1061,6) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1061 kol. 6 > 0, onda je AOP 0421 kol. 6 bilansa stanja ≥ AOP-a 1061 kol. 6 Povećanje neto imovine od poslovanja fonda prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti manje ili jednako iznosu Neraspoređenog dobitka u koloni prethodna godina u obrascu Bilans stanja. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1061 kol. 6 > 0, onda je AOP 0421 kol. 6 bilansa stanja ≥ AOP-a 1061 kol. 6 Povećanje neto imovine od poslovanja fonda prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti manje ili jednako iznosu Neraspoređenog dobitka u koloni prethodna godina u obrascu Bilans stanja. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10090
        if( aop(bu,1062,5) > 0 ):
            if not( aop(bs,422,5) >= aop(bu,1062,5) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1062 kol. 5 > 0, onda je AOP 0422 kol. 5 bilansa stanja ≥ AOP-a 1062 kol. 5  Smanjenje neto imovine od poslovanja fonda tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti manje ili jednako iznosu gubitka u koloni tekuća godina u obrascu Bilans stanja; Ukoliko ti podaci nisu usaglašeni, zakonski zastupnik potpisivanjem izveštaja potvrđuje da je tako iskazan rezultat u Bilansu stanja ispravan i tačan, odnosno da je iskazan u skladu sa propisima. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1062 kol. 5 > 0, onda je AOP 0422 kol. 5 bilansa stanja ≥ AOP-a 1062 kol. 5  Smanjenje neto imovine od poslovanja fonda tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti manje ili jednako iznosu gubitka u koloni tekuća godina u obrascu Bilans stanja; Ukoliko ti podaci nisu usaglašeni, zakonski zastupnik potpisivanjem izveštaja potvrđuje da je tako iskazan rezultat u Bilansu stanja ispravan i tačan, odnosno da je iskazan u skladu sa propisima. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10091
        if( aop(bu,1062,6) > 0 ):
            if not( aop(bs,422,6) >= aop(bu,1062,6) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1062 kol. 6 > 0, onda je AOP 0422 kol. 6 bilansa stanja ≥ AOP-a 1062 kol. 6 Smanjenje neto imovine od poslovanja fonda prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti manje ili jednako iznosu gubitka u koloni prethodna godina u obrascu Bilans stanja. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1062 kol. 6 > 0, onda je AOP 0422 kol. 6 bilansa stanja ≥ AOP-a 1062 kol. 6 Smanjenje neto imovine od poslovanja fonda prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti manje ili jednako iznosu gubitka u koloni prethodna godina u obrascu Bilans stanja. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        ######################################
        #### KRAJ KONTROLNIH PRAVILA    ######
        ######################################

        return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}

    except Exception as e:
        #trace = traceback.format_exc() #traceback.print_tb(sys.exc_info()[2])
        trace=''
        errorMsg = e.message

        exceptionList.append({'errorMessage':errorMsg, 'trace':trace})
        
        return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}

 
       
