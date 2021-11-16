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
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-3
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-4
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-5
        if not( suma(bs,1,60,5)+suma(bs,1,60,6)+suma(bs,1,60,7)+suma(bs,401,457,5)+suma(bs,401,457,6)+suma(bs,401,457,7)+suma(bu,1001,1062,5)+suma(bu,1001,1062,6) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0060) kol. 5 + (0001 do 0060) kol. 6 + (0001 do 0060) kol. 7 bilansa stanja + (0401 do 0457) kol. 5 + (0401 do 0457) kol. 6 + (0401 do 0457) kol. 7 bilansa stanja + (1001 do 1062) kol. 5 + (1001 do 1062) kol. 6 bilansa uspeha > 0 Vanredni finansijski izveštaj, po pravilu, ne sme biti bez podataka; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0060) kol. 5 + (0001 do 0060) kol. 6 + (0001 do 0060) kol. 7 bilansa stanja + (0401 do 0457) kol. 5 + (0401 do 0457) kol. 6 + (0401 do 0457) kol. 7 bilansa stanja + (1001 do 1062) kol. 5 + (1001 do 1062) kol. 6 bilansa uspeha > 0 Vanredni finansijski izveštaj, po pravilu, ne sme biti bez podataka; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            #return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}
        #00000-6
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-7
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-8
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-9
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-10
        #U nijednoj od dve navedene forme kolona Napomena ne sme da bude popunjena
        bsNapomene = Zahtev.Forme['Bilans stanja'].TekstualnaPoljaForme;
        buNapomene = Zahtev.Forme['Bilans uspeha'].TekstualnaPoljaForme;
        if not(proveriNapomene(bsNapomene,1,60,4) and proveriNapomene(bsNapomene,401,457,4) and proveriNapomene(buNapomene,1001,1062,4)):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Na AOP-u (0001 do 0060) bilansa stanja + (0401 do 0457) bilansa stanja + (1001 do 1062) bilansa uspeha u koloni 4 (Napomena broj) ne sme biti iskazan podatak kod obveznika koji nemaju obavezu dostavljanja napomena uz finansijski izveštaj. '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ='Na AOP-u (0001 do 0060) bilansa stanja + (0401 do 0457) bilansa stanja + (1001 do 1062) bilansa uspeha u koloni 4 (Napomena broj) ne sme biti iskazan podatak kod obveznika koji nemaju obavezu dostavljanja napomena uz finansijski izveštaj. '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #Provera da li je fizahtev placen
        if not(Zahtev.Placen):
            ostalo_errors.append('Naknada za obradu i javno objavljivanje izveštaja i propisane dokumentacije nije uplaćena u propisanom iznosu. Instrukcije za uplatu propisane naknade date su u okviru PIS FI sistema za konkretan zahtev, na linku „Status naplate zahteva / Instrukcija za plaćanje". Ukoliko ste izvršili uplatu, a naknada nije uparena, priložite Dokaz o uplati naknade u delu Dokumentacija (na mestu predviđenom za dokaz o uplati naknade), kako biste mogli da podnesete izveštaj.');       
        #Provera negativnih AOP-a
        lista=""
        lista_bs = find_negativni(bs, 1, 457, 5, 7)
        lista_bu = find_negativni(bu, 1001, 1062, 5, 6)
       
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

        #00000-11
        #Za ovaj set se ne primenjuje pravilo 
        
        #BILANS STANJA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        #00001
        if not( suma(bs,1,60,5)+suma(bs,401,457,5) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0060) kol. 5 + (0401 do 0457) kol. 5 > 0 Bilans stanja, po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #00002
        #Za ovaj set se ne primenjuje pravilo 
        
        #00003
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,60,6)+suma(bs,401,457,6) == 0 ):
                lzbir =  suma(bs,1,60,6)+suma(bs,401,457,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0060) kol. 6 + (0401 do 0457) kol. 6 = 0 Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00004
        #Za ovaj set se ne primenjuje pravilo 
        
        #00005
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,60,7)+suma(bs,401,457,7) == 0 ):
                lzbir =  suma(bs,1,60,7)+suma(bs,401,457,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0060) kol. 7 + (0401 do 0457) kol. 7 = 0 Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00006
        #Za ovaj set se ne primenjuje pravilo 
        
        #00007
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,60,6)+suma(bs,401,457,6) > 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0060) kol. 6 + (0401 do 0457) kol. 6 > 0 Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #00008
        #Za ovaj set se ne primenjuje pravilo 
        
        #00009
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,60,7)+suma(bs,401,457,7) > 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0060) kol. 7 + (0401 do 0457) kol. 7 > 0 Bilans stanja, po pravilu,  mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #00010
        #Za ovaj set se ne primenjuje pravilo 
        
        #00011
        if not( aop(bs,2,5) == suma_liste(bs,[3,9,17,18,28],5) ):
            lzbir =  aop(bs,2,5) 
            dzbir =  suma_liste(bs,[3,9,17,18,28],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0002 kol. 5 = AOP-u (0003 + 0009 + 0017 + 0018 + 0028) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00012
        if not( aop(bs,2,6) == suma_liste(bs,[3,9,17,18,28],6) ):
            lzbir =  aop(bs,2,6) 
            dzbir =  suma_liste(bs,[3,9,17,18,28],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0002 kol. 6 = AOP-u (0003 + 0009 + 0017 + 0018 + 0028) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00013
        if not( aop(bs,2,7) == suma_liste(bs,[3,9,17,18,28],7) ):
            lzbir =  aop(bs,2,7) 
            dzbir =  suma_liste(bs,[3,9,17,18,28],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0002 kol. 7 = AOP-u (0003 + 0009 + 0017 + 0018 + 0028) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00014
        if not( aop(bs,3,5) == suma(bs,4,8,5) ):
            lzbir =  aop(bs,3,5) 
            dzbir =  suma(bs,4,8,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0003 kol. 5 = AOP-u (0004 + 0005 + 0006 + 0007 + 0008) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00015
        if not( aop(bs,3,6) == suma(bs,4,8,6) ):
            lzbir =  aop(bs,3,6) 
            dzbir =  suma(bs,4,8,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0003 kol. 6 = AOP-u (0004 + 0005 + 0006 + 0007 + 0008) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00016
        if not( aop(bs,3,7) == suma(bs,4,8,7) ):
            lzbir =  aop(bs,3,7) 
            dzbir =  suma(bs,4,8,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0003 kol. 7 = AOP-u (0004 + 0005 + 0006 + 0007 + 0008) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00017
        if not( aop(bs,9,5) == suma(bs,10,16,5) ):
            lzbir =  aop(bs,9,5) 
            dzbir =  suma(bs,10,16,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0009 kol. 5 = AOP-u (0010 + 0011 + 0012 + 0013 + 0014 + 0015 + 0016) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00018
        if not( aop(bs,9,6) == suma(bs,10,16,6) ):
            lzbir =  aop(bs,9,6) 
            dzbir =  suma(bs,10,16,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0009 kol. 6 = AOP-u (0010 + 0011 + 0012 + 0013 + 0014 + 0015 + 0016) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00019
        if not( aop(bs,9,7) == suma(bs,10,16,7) ):
            lzbir =  aop(bs,9,7) 
            dzbir =  suma(bs,10,16,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0009 kol. 7 = AOP-u (0010 + 0011 + 0012 + 0013 + 0014 + 0015 + 0016) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00020
        if not( aop(bs,18,5) == suma(bs,19,27,5) ):
            lzbir =  aop(bs,18,5) 
            dzbir =  suma(bs,19,27,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0018 kol. 5 = AOP-u (0019 + 0020 + 0021 + 0022 + 0023 + 0024 + 0025 + 0026 + 0027) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00021
        if not( aop(bs,18,6) == suma(bs,19,27,6) ):
            lzbir =  aop(bs,18,6) 
            dzbir =  suma(bs,19,27,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0018 kol. 6 = AOP-u (0019 + 0020 + 0021 + 0022 + 0023 + 0024 + 0025 + 0026 + 0027) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00022
        if not( aop(bs,18,7) == suma(bs,19,27,7) ):
            lzbir =  aop(bs,18,7) 
            dzbir =  suma(bs,19,27,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0018 kol. 7 = AOP-u (0019 + 0020 + 0021 + 0022 + 0023 + 0024 + 0025 + 0026 + 0027) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00023
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8 ):
            if not( aop(bs, 26, 5) + aop(bs, 55, 5) == 0 ):
                lzbir =  aop(bs, 26, 5) + aop(bs, 55, 5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  =' AOP (0026 + 0055) kol. 5 = 0 Preduzetnici ne mogu imati otkupljene sopstvene akcije odnosno udele   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
        #00024
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8 ):
            if not( aop(bs, 26, 6) + aop(bs, 55, 6) == 0 ):
                lzbir =  aop(bs, 26, 6) + aop(bs, 55, 6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  =' AOP (0026 + 0055) kol. 6 = 0 Preduzetnici ne mogu imati otkupljene sopstvene akcije odnosno udele  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
        #00025
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8 ):
            if not( aop(bs, 26, 7) + aop(bs, 55, 7) == 0 ):
                lzbir =  aop(bs, 26, 7) + aop(bs, 55, 7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  =' AOP (0026 + 0055) kol. 7 = 0 Preduzetnici ne mogu imati otkupljene sopstvene akcije odnosno udele  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                 
        #00026
        if not( aop(bs,30,5) == suma_liste(bs,[31,37,38,44,48,57,58],5) ):
            lzbir =  aop(bs,30,5) 
            dzbir =  suma_liste(bs,[31,37,38,44,48,57,58],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0030 kol. 5 = AOP-u (0031 + 0037 + 0038 + 0044 + 0048 + 0057 + 0058) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00027
        if not( aop(bs,30,6) == suma_liste(bs,[31,37,38,44,48,57,58],6) ):
            lzbir =  aop(bs,30,6) 
            dzbir =  suma_liste(bs,[31,37,38,44,48,57,58],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0030 kol. 6 = AOP-u (0031 + 0037 + 0038 + 0044 + 0048 + 0057 + 0058) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00028
        if not( aop(bs,30,7) == suma_liste(bs,[31,37,38,44,48,57,58],7) ):
            lzbir =  aop(bs,30,7) 
            dzbir =  suma_liste(bs,[31,37,38,44,48,57,58],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0030 kol. 7 = AOP-u (0031 + 0037 + 0038 + 0044 + 0048 + 0057 + 0058) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00029
        if not( aop(bs,31,5) == suma(bs,32,36,5) ):
            lzbir =  aop(bs,31,5) 
            dzbir =  suma(bs,32,36,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0031 kol. 5 = AOP-u (0032 + 0033 + 0034 + 0035 + 0036) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00030
        if not( aop(bs,31,6) == suma(bs,32,36,6) ):
            lzbir =  aop(bs,31,6) 
            dzbir =  suma(bs,32,36,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0031 kol. 6 = AOP-u (0032 + 0033 + 0034 + 0035 + 0036) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00031
        if not( aop(bs,31,7) == suma(bs,32,36,7) ):
            lzbir =  aop(bs,31,7) 
            dzbir =  suma(bs,32,36,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0031 kol. 7 = AOP-u (0032 + 0033 + 0034 + 0035 + 0036) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00032
        if not( aop(bs,38,5) == suma(bs,39,43,5) ):
            lzbir =  aop(bs,38,5) 
            dzbir =  suma(bs,39,43,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0038 kol. 5 = AOP-u (0039 + 0040 + 0041 + 0042 + 0043) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00033
        if not( aop(bs,38,6) == suma(bs,39,43,6) ):
            lzbir =  aop(bs,38,6) 
            dzbir =  suma(bs,39,43,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0038 kol. 6 = AOP-u (0039 + 0040 + 0041 + 0042 + 0043) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00034
        if not( aop(bs,38,7) == suma(bs,39,43,7) ):
            lzbir =  aop(bs,38,7) 
            dzbir =  suma(bs,39,43,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0038 kol. 7 = AOP-u (0039 + 0040 + 0041 + 0042 + 0043) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00035
        if not( aop(bs,44,5) == suma(bs,45,47,5) ):
            lzbir =  aop(bs,44,5) 
            dzbir =  suma(bs,45,47,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0044 kol. 5 = AOP-u (0045 + 0046 + 0047) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00036
        if not( aop(bs,44,6) == suma(bs,45,47,6) ):
            lzbir =  aop(bs,44,6) 
            dzbir =  suma(bs,45,47,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0044 kol. 6 = AOP-u (0045 + 0046 + 0047) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00037
        if not( aop(bs,44,7) == suma(bs,45,47,7) ):
            lzbir =  aop(bs,44,7) 
            dzbir =  suma(bs,45,47,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0044 kol. 7 = AOP-u (0045 + 0046 + 0047) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00038
        if not( aop(bs,48,5) == suma(bs,49,56,5) ):
            lzbir =  aop(bs,48,5) 
            dzbir =  suma(bs,49,56,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0048 kol. 5 = AOP-u (0049 + 0050 + 0051 + 0052 + 0053 + 0054 + 0055 + 0056) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00039
        if not( aop(bs,48,6) == suma(bs,49,56,6) ):
            lzbir =  aop(bs,48,6) 
            dzbir =  suma(bs,49,56,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0048 kol. 6 = AOP-u (0049 + 0050 + 0051 + 0052 + 0053 + 0054 + 0055 + 0056) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00040
        if not( aop(bs,48,7) == suma(bs,49,56,7) ):
            lzbir =  aop(bs,48,7) 
            dzbir =  suma(bs,49,56,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0048 kol. 7 = AOP-u (0049 + 0050 + 0051 + 0052 + 0053 + 0054 + 0055 + 0056) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00041
        if not( aop(bs,59,5) == suma_liste(bs,[1,2,29,30],5) ):
            lzbir =  aop(bs,59,5) 
            dzbir =  suma_liste(bs,[1,2,29,30],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0059 kol. 5 = AOP-u (0001 + 0002 + 0029 + 0030) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00042
        if not( aop(bs,59,6) == suma_liste(bs,[1,2,29,30],6) ):
            lzbir =  aop(bs,59,6) 
            dzbir =  suma_liste(bs,[1,2,29,30],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0059 kol. 6 = AOP-u (0001 + 0002 + 0029 + 0030) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00043
        if not( aop(bs,59,7) == suma_liste(bs,[1,2,29,30],7) ):
            lzbir =  aop(bs,59,7) 
            dzbir =  suma_liste(bs,[1,2,29,30],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0059 kol. 7 = AOP-u (0001 + 0002 + 0029 + 0030) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00044
        if( suma_liste(bs,[402,403,404,405,406,408,411],5) > suma_liste(bs,[407,412],5) ):
            if not( aop(bs,401,5) == suma_liste(bs,[402,403,404,405,406,408,411],5)-suma_liste(bs,[407,412],5) ):
                lzbir =  aop(bs,401,5) 
                dzbir =  suma_liste(bs,[402,403,404,405,406,408,411],5)-suma_liste(bs,[407,412],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0401 kol. 5 = AOP-u (0402 + 0403 + 0404 + 0405 + 0406 - 0407 + 0408 + 0411 - 0412) kol. 5, ako je AOP (0402 + 0403 + 0404 + 0405 + 0406 + 0408 + 0411) kol. 5 > AOP-a (0407 + 0412) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00045
        if( suma_liste(bs,[402,403,404,405,406,408,411],6) > suma_liste(bs,[407,412],6) ):
            if not( aop(bs,401,6) == suma_liste(bs,[402,403,404,405,406,408,411],6)-suma_liste(bs,[407,412],6) ):
                lzbir =  aop(bs,401,6) 
                dzbir =  suma_liste(bs,[402,403,404,405,406,408,411],6)-suma_liste(bs,[407,412],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0401 kol. 6 = AOP-u (0402 + 0403 + 0404 + 0405 + 0406 - 0407 + 0408 + 0411 - 0412) kol. 6, ako je AOP (0402 + 0403 + 0404 + 0405 + 0406 + 0408 + 0411) kol. 6 > AOP-a (0407 + 0412) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00046
        if( suma_liste(bs,[402,403,404,405,406,408,411],7) > suma_liste(bs,[407,412],7) ):
            if not( aop(bs,401,7) == suma_liste(bs,[402,403,404,405,406,408,411],7)-suma_liste(bs,[407,412],7) ):
                lzbir =  aop(bs,401,7) 
                dzbir =  suma_liste(bs,[402,403,404,405,406,408,411],7)-suma_liste(bs,[407,412],7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0401 kol. 7 = AOP-u (0402 + 0403 + 0404 + 0405 + 0406 - 0407 + 0408 + 0411 - 0412) kol. 7, ako je AOP (0402 + 0403 + 0404 + 0405 + 0406 + 0408 + 0411) kol. 7 > AOP-a (0407 + 0412) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00047
        if( aop(bs,59,5) > suma_liste(bs,[415,429,430,431],5) ):
            if not( aop(bs,401,5) == aop(bs,59,5)-suma_liste(bs,[415,429,430,431],5) ):
                lzbir =  aop(bs,401,5) 
                dzbir =  aop(bs,59,5)-suma_liste(bs,[415,429,430,431],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0401 kol. 5 = AOP-u (0059 - 0415 - 0429 - 0430 - 0431) kol. 5, ako je AOP 0059 kol. 5 > AOP-a (0415 + 0429 + 0430 + 0431) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00048
        if( aop(bs,59,6) > suma_liste(bs,[415,429,430,431],6) ):
            if not( aop(bs,401,6) == aop(bs,59,6)-suma_liste(bs,[415,429,430,431],6) ):
                lzbir =  aop(bs,401,6) 
                dzbir =  aop(bs,59,6)-suma_liste(bs,[415,429,430,431],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0401 kol. 6 = AOP-u (0059 - 0415 - 0429 - 0430 - 0431) kol. 6, ako je AOP 0059 kol. 6 > AOP-a (0415 + 0429 + 0430 + 0431) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00049
        if( aop(bs,59,7) > suma_liste(bs,[415,429,430,431],7) ):
            if not( aop(bs,401,7) == aop(bs,59,7)-suma_liste(bs,[415,429,430,431],7) ):
                lzbir =  aop(bs,401,7) 
                dzbir =  aop(bs,59,7)-suma_liste(bs,[415,429,430,431],7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0401 kol. 7 = AOP-u (0059 - 0415 - 0429 - 0430 - 0431) kol. 7, ako je AOP 0059 kol. 7 > AOP-a (0415 + 0429 + 0430 + 0431) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00050
        if not( aop(bs,408,5) == suma(bs,409,410,5) ):
            lzbir =  aop(bs,408,5) 
            dzbir =  suma(bs,409,410,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0408 kol. 5 = AOP-u (0409 + 0410) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00051
        if not( aop(bs,408,6) == suma(bs,409,410,6) ):
            lzbir =  aop(bs,408,6) 
            dzbir =  suma(bs,409,410,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0408 kol. 6 = AOP-u (0409 + 0410) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00052
        if not( aop(bs,408,7) == suma(bs,409,410,7) ):
            lzbir =  aop(bs,408,7) 
            dzbir =  suma(bs,409,410,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0408 kol. 7 = AOP-u (0409 + 0410) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00053
        if not( aop(bs,411,5) == 0 ):
            lzbir =  aop(bs,411,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0411 kol. 5 = 0 Učešće bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00054
        if not( aop(bs,411,6) == 0 ):
            lzbir =  aop(bs,411,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0411 kol. 6 = 0 Učešće bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00055
        if not( aop(bs,411,7) == 0 ):
            lzbir =  aop(bs,411,7) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0411 kol. 7 = 0 Učešće bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00056
        if not( aop(bs,412,5) == suma(bs,413,414,5) ):
            lzbir =  aop(bs,412,5) 
            dzbir =  suma(bs,413,414,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0412 kol. 5 = AOP-u (0413 + 0414) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00057
        if not( aop(bs,412,6) == suma(bs,413,414,6) ):
            lzbir =  aop(bs,412,6) 
            dzbir =  suma(bs,413,414,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0412 kol. 6 = AOP-u (0413 + 0414) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00058
        if not( aop(bs,412,7) == suma(bs,413,414,7) ):
            lzbir =  aop(bs,412,7) 
            dzbir =  suma(bs,413,414,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0412 kol. 7 = AOP-u (0413 + 0414) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00059
        if not( aop(bs,415,5) == suma_liste(bs,[416,420,428],5) ):
            lzbir =  aop(bs,415,5) 
            dzbir =  suma_liste(bs,[416,420,428],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0415 kol. 5 = AOP-u (0416 + 0420 + 0428) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00060
        if not( aop(bs,415,6) == suma_liste(bs,[416,420,428],6) ):
            lzbir =  aop(bs,415,6) 
            dzbir =  suma_liste(bs,[416,420,428],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0415 kol. 6 = AOP-u (0416 + 0420 + 0428) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00061
        if not( aop(bs,415,7) == suma_liste(bs,[416,420,428],7) ):
            lzbir =  aop(bs,415,7) 
            dzbir =  suma_liste(bs,[416,420,428],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0415 kol. 7 = AOP-u (0416 + 0420 + 0428) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00062
        if not( aop(bs,416,5) == suma(bs,417,419,5) ):
            lzbir =  aop(bs,416,5) 
            dzbir =  suma(bs,417,419,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0416 kol. 5 = AOP-u (0417 + 0418 + 0419) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00063
        if not( aop(bs,416,6) == suma(bs,417,419,6) ):
            lzbir =  aop(bs,416,6) 
            dzbir =  suma(bs,417,419,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0416 kol. 6 = AOP-u (0417 + 0418 + 0419) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00064
        if not( aop(bs,416,7) == suma(bs,417,419,7) ):
            lzbir =  aop(bs,416,7) 
            dzbir =  suma(bs,417,419,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0416 kol. 7 = AOP-u (0417 + 0418 + 0419) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00065
        if not( aop(bs,420,5) == suma(bs,421,427,5) ):
            lzbir =  aop(bs,420,5) 
            dzbir =  suma(bs,421,427,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0420 kol. 5 = AOP-u (0421 + 0422 + 0423 + 0424 + 0425 + 0426 + 0427) kol. 5   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00066
        if not( aop(bs,420,6) == suma(bs,421,427,6) ):
            lzbir =  aop(bs,420,6) 
            dzbir =  suma(bs,421,427,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0420 kol. 6 = AOP-u (0421 + 0422 + 0423 + 0424 + 0425 + 0426 + 0427) kol. 6   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00067
        if not( aop(bs,420,7) == suma(bs,421,427,7) ):
            lzbir =  aop(bs,420,7) 
            dzbir =  suma(bs,421,427,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0420 kol. 7 = AOP-u (0421 + 0422 + 0423 + 0424 + 0425 + 0426 + 0427) kol. 7   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00068
        if not( aop(bs,431,5) == suma_liste(bs,[432,433,441,442,449,453,454],5) ):
            lzbir =  aop(bs,431,5) 
            dzbir =  suma_liste(bs,[432,433,441,442,449,453,454],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0431 kol. 5 = AOP-u (0432 + 0433 + 0441 + 0442 + 0449 + 0453 + 0454) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00069
        if not( aop(bs,431,6) == suma_liste(bs,[432,433,441,442,449,453,454],6) ):
            lzbir =  aop(bs,431,6) 
            dzbir =  suma_liste(bs,[432,433,441,442,449,453,454],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0431 kol. 6 = AOP-u (0432 + 0433 + 0441 + 0442 + 0449 + 0453 + 0454) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00070
        if not( aop(bs,431,7) == suma_liste(bs,[432,433,441,442,449,453,454],7) ):
            lzbir =  aop(bs,431,7) 
            dzbir =  suma_liste(bs,[432,433,441,442,449,453,454],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0431 kol. 7 = AOP-u (0432 + 0433 + 0441 + 0442 + 0449 + 0453 + 0454) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00071
        if not( aop(bs,433,5) == suma(bs,434,440,5) ):
            lzbir =  aop(bs,433,5) 
            dzbir =  suma(bs,434,440,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0433 kol. 5 = AOP-u (0434 + 0435 + 0436 + 0437 + 0438 + 0439 + 0440) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00072
        if not( aop(bs,433,6) == suma(bs,434,440,6) ):
            lzbir =  aop(bs,433,6) 
            dzbir =  suma(bs,434,440,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0433 kol. 6 = AOP-u (0434 + 0435 + 0436 + 0437 + 0438 + 0439 + 0440) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00073
        if not( aop(bs,433,7) == suma(bs,434,440,7) ):
            lzbir =  aop(bs,433,7) 
            dzbir =  suma(bs,434,440,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0433 kol. 7 = AOP-u (0434 + 0435 + 0436 + 0437 + 0438 + 0439 + 0440) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00074
        if not( aop(bs,442,5) == suma(bs,443,448,5) ):
            lzbir =  aop(bs,442,5) 
            dzbir =  suma(bs,443,448,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0442 kol. 5 = AOP-u (0443 + 0444 + 0445 + 0446 + 0447 + 0448) kol. 5   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00075
        if not( aop(bs,442,6) == suma(bs,443,448,6) ):
            lzbir =  aop(bs,442,6) 
            dzbir =  suma(bs,443,448,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0442 kol. 6 = AOP-u (0443 + 0444 + 0445 + 0446 + 0447 + 0448) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00076
        if not( aop(bs,442,7) == suma(bs,443,448,7) ):
            lzbir =  aop(bs,442,7) 
            dzbir =  suma(bs,443,448,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0442 kol. 7 = AOP-u (0443 + 0444 + 0445 + 0446 + 0447 + 0448) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00077
        if not( aop(bs,449,5) == suma(bs,450,452,5) ):
            lzbir =  aop(bs,449,5) 
            dzbir =  suma(bs,450,452,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0449 kol. 5 = AOP-u (0450 + 0451 + 0452) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00078
        if not( aop(bs,449,6) == suma(bs,450,452,6) ):
            lzbir =  aop(bs,449,6) 
            dzbir =  suma(bs,450,452,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0449 kol. 6 = AOP-u (0450 + 0451 + 0452) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00079
        if not( aop(bs,449,7) == suma(bs,450,452,7) ):
            lzbir =  aop(bs,449,7) 
            dzbir =  suma(bs,450,452,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0449 kol. 7 = AOP-u (0450 + 0451 + 0452) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00080
        if( suma_liste(bs,[402,403,404,405,406,408,411],5) < suma_liste(bs,[407,412],5) ):
            if not( aop(bs,455,5) == suma_liste(bs,[407,412],5)-suma_liste(bs,[402,403,404,405,406,408,411],5) ):
                lzbir =  aop(bs,455,5) 
                dzbir =  suma_liste(bs,[407,412],5)-suma_liste(bs,[402,403,404,405,406,408,411],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0455 kol. 5 = AOP-u (0407 + 0412 - 0402 - 0403 - 0404 - 0405 - 0406 - 0408 - 0411) kol. 5, ako je AOP (0402 + 0403 + 0404 + 0405 + 0406 + 0408 + 0411) kol. 5 < AOP-a (0407 + 0412) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00081
        if( suma_liste(bs,[402,403,404,405,406,408,411],6) < suma_liste(bs,[407,412],6) ):
            if not( aop(bs,455,6) == suma_liste(bs,[407,412],6)-suma_liste(bs,[402,403,404,405,406,408,411],6) ):
                lzbir =  aop(bs,455,6) 
                dzbir =  suma_liste(bs,[407,412],6)-suma_liste(bs,[402,403,404,405,406,408,411],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0455 kol. 6 = AOP-u (0407 + 0412 - 0402 - 0403 - 0404 - 0405 - 0406 - 0408 - 0411) kol. 6, ako je AOP (0402 + 0403 + 0404 + 0405 + 0406 + 0408 + 0411) kol. 6 < AOP-a (0407 + 0412) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00082
        if( suma_liste(bs,[402,403,404,405,406,408,411],7) < suma_liste(bs,[407,412],7) ):
            if not( aop(bs,455,7) == suma_liste(bs,[407,412],7)-suma_liste(bs,[402,403,404,405,406,408,411],7) ):
                lzbir =  aop(bs,455,7) 
                dzbir =  suma_liste(bs,[407,412],7)-suma_liste(bs,[402,403,404,405,406,408,411],7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0455 kol. 7 = AOP-u (0407 + 0412 - 0402 - 0403 - 0404 - 0405 - 0406 - 0408 - 0411) kol. 7, ako je AOP (0402 + 0403 + 0404 + 0405 + 0406 + 0408 + 0411) kol. 7 < AOP-a (0407 + 0412) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00083
        if( aop(bs,59,5) < suma_liste(bs,[415,429,430,431],5) ):
            if not( aop(bs,455,5) == suma_liste(bs,[415,429,430,431],5)-aop(bs,59,5) ):
                lzbir =  aop(bs,455,5) 
                dzbir =  suma_liste(bs,[415,429,430,431],5)-aop(bs,59,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0455 kol. 5 = AOP-u (0415 + 0429 + 0430 + 0431 - 0059) kol. 5, ako je AOP 0059 kol. 5 < AOP-a (0415 + 0429 + 0430 + 0431) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00084
        if( aop(bs,59,6) < suma_liste(bs,[415,429,430,431],6) ):
            if not( aop(bs,455,6) == suma_liste(bs,[415,429,430,431],6)-aop(bs,59,6) ):
                lzbir =  aop(bs,455,6) 
                dzbir =  suma_liste(bs,[415,429,430,431],6)-aop(bs,59,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0455 kol. 6 = AOP-u (0415 + 0429 + 0430 + 0431 - 0059) kol. 6, ako je AOP 0059 kol. 6 < AOP-a (0415 + 0429 + 0430 + 0431) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00085
        if( aop(bs,59,7) < suma_liste(bs,[415,429,430,431],7) ):
            if not( aop(bs,455,7) == suma_liste(bs,[415,429,430,431],7)-aop(bs,59,7) ):
                lzbir =  aop(bs,455,7) 
                dzbir =  suma_liste(bs,[415,429,430,431],7)-aop(bs,59,7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0455 kol. 7 = AOP-u (0415 + 0429 + 0430 + 0431 - 0059) kol. 7, ako je AOP 0059 kol. 7 < AOP-a (0415 + 0429 + 0430 + 0431) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00086
        if( suma_liste(bs,[402,403,404,405,406,408,411],5) == suma_liste(bs,[407,412],5) ):
            if not( suma_liste(bs,[401,455],5) == 0 ):
                lzbir =  suma_liste(bs,[401,455],5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0455) kol. 5 = 0, ako je AOP (0402 + 0403 + 0404 + 0405 + 0406 + 0408 + 0411) kol. 5 = AOP-u (0407 + 0412) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00087
        if( suma_liste(bs,[402,403,404,405,406,408,411],6) == suma_liste(bs,[407,412],6) ):
            if not( suma_liste(bs,[401,455],6) == 0 ):
                lzbir =  suma_liste(bs,[401,455],6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0455) kol. 6 = 0, ako je AOP (0402 + 0403 + 0404 + 0405 + 0406 + 0408 + 0411) kol. 6 = AOP-u (0407 + 0412) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00088
        if( suma_liste(bs,[402,403,404,405,406,408,411],7) == suma_liste(bs,[407,412],7) ):
            if not( suma_liste(bs,[401,455],7) == 0 ):
                lzbir =  suma_liste(bs,[401,455],7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0455) kol. 7 = 0, ako je AOP (0402 + 0403 + 0404 + 0405 + 0406 + 0408 + 0411) kol. 7 = AOP-u (0407 + 0412) kol. 7 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00089
        if( aop(bs,59,5) == suma_liste(bs,[415,429,430,431],5) ):
            if not( suma_liste(bs,[401,455],5) == 0 ):
                lzbir =  suma_liste(bs,[401,455],5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0455) kol. 5 = 0, ako je AOP 0059 kol. 5 = AOP-a (0415 + 0429 + 0430 + 0431) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00090
        if( aop(bs,59,6) == suma_liste(bs,[415,429,430,431],6) ):
            if not( suma_liste(bs,[401,455],6) == 0 ):
                lzbir =  suma_liste(bs,[401,455],6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0455) kol. 6 = 0, ako je AOP 0059 kol. 6 = AOP-a (0415 + 0429 + 0430 + 0431) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00091
        if( aop(bs,59,7) == suma_liste(bs,[415,429,430,431],7) ):
            if not( suma_liste(bs,[401,455],7) == 0 ):
                lzbir =  suma_liste(bs,[401,455],7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0455) kol. 7 = 0, ako je AOP 0059 kol. 7 = AOP-a (0415 + 0429 + 0430 + 0431) kol. 7 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00092
        if( aop(bs,401,5) > 0 ):
            if not( aop(bs,455,5) == 0 ):
                lzbir =  aop(bs,455,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0401 kol. 5 > 0 onda je AOP 0455 kol. 5 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00093
        if( aop(bs,455,5) > 0 ):
            if not( aop(bs,401,5) == 0 ):
                lzbir =  aop(bs,401,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0455 kol. 5 > 0 onda je AOP 0401 kol. 5 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00094
        if( aop(bs,401,6) > 0 ):
            if not( aop(bs,455,6) == 0 ):
                lzbir =  aop(bs,455,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0401 kol. 6 > 0 onda je AOP 0455 kol. 6 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00095
        if( aop(bs,455,6) > 0 ):
            if not( aop(bs,401,6) == 0 ):
                lzbir =  aop(bs,401,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0455 kol. 6 > 0 onda je AOP 0401 kol. 6 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00096
        if( aop(bs,401,7) > 0 ):
            if not( aop(bs,455,7) == 0 ):
                lzbir =  aop(bs,455,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0401 kol. 7 > 0 onda je AOP 0455 kol. 7 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00097
        if( aop(bs,455,7) > 0 ):
            if not( aop(bs,401,7) == 0 ):
                lzbir =  aop(bs,401,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0455 kol. 7 > 0 onda je AOP 0401 kol. 7 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00098
        if not( aop(bs,456,5) == suma_liste(bs,[401,415,429,430,431],5)-aop(bs,455,5) ):
            lzbir =  aop(bs,456,5) 
            dzbir =  suma_liste(bs,[401,415,429,430,431],5)-aop(bs,455,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0456 kol. 5 = AOP-u (0401 + 0415 + 0429 + 0430 + 0431 - 0455) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00099
        if not( aop(bs,456,6) == suma_liste(bs,[401,415,429,430,431],6)-aop(bs,455,6) ):
            lzbir =  aop(bs,456,6) 
            dzbir =  suma_liste(bs,[401,415,429,430,431],6)-aop(bs,455,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0456 kol. 6 = AOP-u (0401 + 0415 + 0429 + 0430 + 0431 - 0455) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00100
        if not( aop(bs,456,7) == suma_liste(bs,[401,415,429,430,431],7)-aop(bs,455,7) ):
            lzbir =  aop(bs,456,7) 
            dzbir =  suma_liste(bs,[401,415,429,430,431],7)-aop(bs,455,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0456 kol. 7 = AOP-u (0401 + 0415 + 0429 + 0430 + 0431 - 0455) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00101
        if not( aop(bs,59,5) == aop(bs,456,5) ):
            lzbir =  aop(bs,59,5) 
            dzbir =  aop(bs,456,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0059 kol. 5 = AOP-u 0456 kol. 5 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00102
        if not( aop(bs,59,6) == aop(bs,456,6) ):
            lzbir =  aop(bs,59,6) 
            dzbir =  aop(bs,456,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0059 kol. 6 = AOP-u 0456 kol. 6 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00103
        if not( aop(bs,59,7) == aop(bs,456,7) ):
            lzbir =  aop(bs,59,7) 
            dzbir =  aop(bs,456,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0059 kol. 7 = AOP-u 0456 kol. 7 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00104
        if not( aop(bs,60,5) == aop(bs,457,5) ):
            lzbir =  aop(bs,60,5) 
            dzbir =  aop(bs,457,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0060 kol. 5 = AOP-u 0457 kol. 5 Kontrolno pravilo zahteva slaganje vanbilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00105
        if not( aop(bs,60,6) == aop(bs,457,6) ):
            lzbir =  aop(bs,60,6) 
            dzbir =  aop(bs,457,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0060 kol. 6 = AOP-u 0457 kol. 6 Kontrolno pravilo zahteva slaganje vanbilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00106
        if not( aop(bs,60,7) == aop(bs,457,7) ):
            lzbir =  aop(bs,60,7) 
            dzbir =  aop(bs,457,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0060 kol. 7 = AOP-u 0457 kol. 7 Kontrolno pravilo zahteva slaganje vanbilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00107
        if not( aop(bs,1,5) == aop(bs,403,5) ):
            lzbir =  aop(bs,1,5) 
            dzbir =  aop(bs,403,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0001 kol. 5 = AOP-u 0403 kol. 5 Upisani a neuplaćeni kapital u aktivi mora biti jednak upisanom a neuplaćenom kapitalu u pasivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00108
        if not( aop(bs,1,6) == aop(bs,403,6) ):
            lzbir =  aop(bs,1,6) 
            dzbir =  aop(bs,403,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0001 kol. 6 = AOP-u 0403 kol. 6 Upisani a neuplaćeni kapital u aktivi mora biti jednak upisanom a neuplaćenom kapitalu u pasivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00109
        if not( aop(bs,1,7) == aop(bs,403,7) ):
            lzbir =  aop(bs,1,7) 
            dzbir =  aop(bs,403,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0001 kol. 7 = AOP-u 0403 kol. 7 Upisani a neuplaćeni kapital u aktivi mora biti jednak upisanom a neuplaćenom kapitalu u pasivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00110
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8 ):
            if not( aop(bs, 1, 5)  == 0 ):
                lzbir =  aop(bs, 1, 5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  =' AOP 0001 kol. 5 = 0  Preduzetnici ne mogu imati upisani a neuplaćeni kapital '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                 
        #00111
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8 ):
            if not( aop(bs, 1, 6)  == 0 ):
                lzbir =  aop(bs, 1, 6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  =' AOP 0001 kol. 6 = 0  Preduzetnici ne mogu imati upisani a neuplaćeni kapital '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                  
        #00112
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8 ):
            if not( aop(bs, 1, 7)  == 0 ):
                lzbir =  aop(bs, 1, 7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  =' AOP 0001 kol. 7 = 0  Preduzetnici ne mogu imati upisani a neuplaćeni kapital '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                   
        #00113
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8 ):
            if not( aop(bs, 404, 5)  == 0 ):
                lzbir =  aop(bs, 404, 5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  =' AOP 0404 kol. 5 = 0  Preduzetnici ne mogu imati emisionu premiju '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00114
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8 ):
            if not( aop(bs, 404, 6)  == 0 ):
                lzbir =  aop(bs, 404, 6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  =' AOP 0404 kol. 6 = 0  Preduzetnici ne mogu imati emisionu premiju '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00115
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8 ):
            if not( aop(bs, 404, 7)  == 0 ):
                lzbir =  aop(bs, 404, 7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  =' AOP 0404 kol. 7 = 0  Preduzetnici ne mogu imati emisionu premiju '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00116
        if( suma(bu,1001,1062,5) > 0 ):
            if not( suma(bs,1,60,5)+suma(bs,401,457,5) != suma(bs,1,60,6)+suma(bs,401,457,6) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='***Ako je zbir podataka na oznakama za AOP (1001 do 1062) kol. 5 bilansa uspeha  > 0 onda zbir podataka na oznakama za AOP (0001 do 0060) kol. 5 bilansa stanja + (0401 do 0457) kol. 5 bilansa stanja ≠ zbiru podataka na oznakama za AOP (0001 do 0060) kol. 6 bilansa stanja + (0401 do 0457) kol. 6 bilansa stanja Zbirovi podataka u kolonama 5 i 6 bilansa stanja su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama;  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='***Ako je zbir podataka na oznakama za AOP (1001 do 1062) kol. 5 bilansa uspeha  > 0 onda zbir podataka na oznakama za AOP (0001 do 0060) kol. 5 bilansa stanja + (0401 do 0457) kol. 5 bilansa stanja ≠ zbiru podataka na oznakama za AOP (0001 do 0060) kol. 6 bilansa stanja + (0401 do 0457) kol. 6 bilansa stanja Zbirovi podataka u kolonama 5 i 6 bilansa stanja su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama;  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #00117
        #Za ovaj set se ne primenjuje pravilo 
        
        #BILANS USPEHA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        #10001
        if not( suma(bu,1001,1062,5) > 0 ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP (1001 do 1062) kol. 5 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #10002
        #Za ovaj set se ne primenjuje pravilo 
        #10003
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bu,1001,1062,6) == 0 ):
                lzbir =  suma(bu,1001,1062,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Zbir podataka na oznakama za AOP (1001 do 1062) kol. 6 = 0 Bilans uspeha za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10004
        #Za ovaj set se ne primenjuje pravilo 
        
        #10005
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bu,1001,1062,6) > 0 ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Zbir podataka na oznakama za AOP (1001 do 1062) kol. 6 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10006        
        #Za ovaj set se ne primenjuje pravilo 
        
        #10007
        if not( aop(bu,1001,5) == suma_liste(bu,[1002,1005,1008,1009,1011,1012],5)-aop(bu,1010,5) ):
            lzbir =  aop(bu,1001,5) 
            dzbir =  suma_liste(bu,[1002,1005,1008,1009,1011,1012],5)-aop(bu,1010,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1001 kol. 5 = AOP-u (1002 + 1005 + 1008 + 1009 - 1010 + 1011 + 1012) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10008
        if not( aop(bu,1001,6) == suma_liste(bu,[1002,1005,1008,1009,1011,1012],6)-aop(bu,1010,6) ):
            lzbir =  aop(bu,1001,6) 
            dzbir =  suma_liste(bu,[1002,1005,1008,1009,1011,1012],6)-aop(bu,1010,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1001 kol. 6 = AOP-u (1002 + 1005 + 1008 + 1009 - 1010 + 1011 + 1012) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10009
        if not( aop(bu,1002,5) == suma(bu,1003,1004,5) ):
            lzbir =  aop(bu,1002,5) 
            dzbir =  suma(bu,1003,1004,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1002 kol. 5 = AOP-u (1003 + 1004) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10010
        if not( aop(bu,1002,6) == suma(bu,1003,1004,6) ):
            lzbir =  aop(bu,1002,6) 
            dzbir =  suma(bu,1003,1004,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1002 kol. 6 = AOP-u (1003 + 1004) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10011
        if not( aop(bu,1005,5) == suma(bu,1006,1007,5) ):
            lzbir =  aop(bu,1005,5) 
            dzbir =  suma(bu,1006,1007,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1005 kol. 5 = AOP-u (1006 + 1007) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10012
        if not( aop(bu,1005,6) == suma(bu,1006,1007,6) ):
            lzbir =  aop(bu,1005,6) 
            dzbir =  suma(bu,1006,1007,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1005 kol. 6 = AOP-u (1006 + 1007) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10013
        if not( aop(bu,1013,5) == suma_liste(bu,[1014,1015,1016,1020,1021,1022,1023,1024],5) ):
            lzbir =  aop(bu,1013,5) 
            dzbir =  suma_liste(bu,[1014,1015,1016,1020,1021,1022,1023,1024],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1013 kol. 5 = AOP-u (1014 + 1015 + 1016 + 1020 + 1021 + 1022 + 1023 + 1024) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10014
        if not( aop(bu,1013,6) == suma_liste(bu,[1014,1015,1016,1020,1021,1022,1023,1024],6) ):
            lzbir =  aop(bu,1013,6) 
            dzbir =  suma_liste(bu,[1014,1015,1016,1020,1021,1022,1023,1024],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1013 kol. 6 = AOP-u (1014 + 1015 + 1016 + 1020 + 1021 + 1022 + 1023 + 1024) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10015
        if not( aop(bu,1016,5) == suma(bu,1017,1019,5) ):
            lzbir =  aop(bu,1016,5) 
            dzbir =  suma(bu,1017,1019,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1016 kol. 5 = AOP-u (1017 + 1018 + 1019) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10016
        if not( aop(bu,1016,6) == suma(bu,1017,1019,6) ):
            lzbir =  aop(bu,1016,6) 
            dzbir =  suma(bu,1017,1019,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1016 kol. 6 = AOP-u (1017 + 1018 + 1019) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10017
        if( aop(bu,1001,5) > aop(bu,1013,5) ):
            if not( aop(bu,1025,5) == aop(bu,1001,5)-aop(bu,1013,5) ):
                lzbir =  aop(bu,1025,5) 
                dzbir =  aop(bu,1001,5)-aop(bu,1013,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1025 kol. 5 = AOP-u (1001 - 1013) kol. 5, ako je AOP 1001 kol. 5 > AOP-a 1013 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10018
        if( aop(bu,1001,6) > aop(bu,1013,6) ):
            if not( aop(bu,1025,6) == aop(bu,1001,6)-aop(bu,1013,6) ):
                lzbir =  aop(bu,1025,6) 
                dzbir =  aop(bu,1001,6)-aop(bu,1013,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1025 kol. 6 = AOP-u (1001 - 1013) kol. 6, ako je AOP 1001 kol. 6 > AOP-a 1013 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10019
        if( aop(bu,1001,5) < aop(bu,1013,5) ):
            if not( aop(bu,1026,5) == aop(bu,1013,5)-aop(bu,1001,5) ):
                lzbir =  aop(bu,1026,5) 
                dzbir =  aop(bu,1013,5)-aop(bu,1001,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1026 kol. 5 = AOP-u (1013 - 1001) kol. 5, ako je AOP 1001 kol. 5 < AOP-a 1013 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10020
        if( aop(bu,1001,6) < aop(bu,1013,6) ):
            if not( aop(bu,1026,6) == aop(bu,1013,6)-aop(bu,1001,6) ):
                lzbir =  aop(bu,1026,6) 
                dzbir =  aop(bu,1013,6)-aop(bu,1001,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1026 kol. 6 = AOP-u (1013 - 1001) kol. 6, ako je AOP 1001 kol. 6 < AOP-a 1013 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10021
        if( aop(bu,1001,5) == aop(bu,1013,5) ):
            if not( suma(bu,1025,1026,5) == 0 ):
                lzbir =  suma(bu,1025,1026,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1025 + 1026) kol. 5 = 0, ako je AOP 1001 kol. 5 = AOP-u 1013 kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10022
        if( aop(bu,1001,6) == aop(bu,1013,6) ):
            if not( suma(bu,1025,1026,6) == 0 ):
                lzbir =  suma(bu,1025,1026,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1025 + 1026) kol. 6 = 0, ako je AOP 1001 kol. 6 = AOP-u 1013 kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10023
        if( aop(bu,1025,5) > 0 ):
            if not( aop(bu,1026,5) == 0 ):
                lzbir =  aop(bu,1026,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1025 kol. 5 > 0 onda je AOP 1026 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10024
        if( aop(bu,1026,5) > 0 ):
            if not( aop(bu,1025,5) == 0 ):
                lzbir =  aop(bu,1025,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1026 kol. 5 > 0 onda je AOP 1025 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10025
        if( aop(bu,1025,6) > 0 ):
            if not( aop(bu,1026,6) == 0 ):
                lzbir =  aop(bu,1026,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1025 kol. 6 > 0 onda je AOP 1026 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10026
        if( aop(bu,1026,6) > 0 ):
            if not( aop(bu,1025,6) == 0 ):
                lzbir =  aop(bu,1025,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1026 kol. 6 > 0 onda je AOP 1025 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10027
        if not( suma_liste(bu,[1002,1005,1008,1009,1011,1012,1026],5) == suma_liste(bu,[1010,1014,1015,1016,1020,1021,1022,1023,1024,1025],5) ):
            lzbir =  suma_liste(bu,[1002,1005,1008,1009,1011,1012,1026],5) 
            dzbir =  suma_liste(bu,[1010,1014,1015,1016,1020,1021,1022,1023,1024,1025],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1002 + 1005 + 1008 + 1009 + 1011 + 1012 + 1026) kol. 5 = AOP-u (1010 + 1014 + 1015 + 1016 + 1020 + 1021 + 1022 + 1023 + 1024 + 1025) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10028
        if not( suma_liste(bu,[1002,1005,1008,1009,1011,1012,1026],6) == suma_liste(bu,[1010,1014,1015,1016,1020,1021,1022,1023,1024,1025],6) ):
            lzbir =  suma_liste(bu,[1002,1005,1008,1009,1011,1012,1026],6) 
            dzbir =  suma_liste(bu,[1010,1014,1015,1016,1020,1021,1022,1023,1024,1025],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1002 + 1005 + 1008 + 1009 + 1011 + 1012 + 1026) kol. 6 = AOP-u (1010 + 1014 + 1015 + 1016 + 1020 + 1021 + 1022 + 1023 + 1024 + 1025) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10029
        if not( aop(bu,1027,5) == suma(bu,1028,1031,5) ):
            lzbir =  aop(bu,1027,5) 
            dzbir =  suma(bu,1028,1031,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1027 kol. 5 = AOP-u (1028 + 1029 + 1030 + 1031) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10030
        if not( aop(bu,1027,6) == suma(bu,1028,1031,6) ):
            lzbir =  aop(bu,1027,6) 
            dzbir =  suma(bu,1028,1031,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1027 kol. 6 = AOP-u (1028 + 1029 + 1030 + 1031) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10031
        if not( aop(bu,1032,5) == suma(bu,1033,1036,5) ):
            lzbir =  aop(bu,1032,5) 
            dzbir =  suma(bu,1033,1036,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1032 kol. 5 = AOP-u (1033 + 1034 + 1035 + 1036) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10032
        if not( aop(bu,1032,6) == suma(bu,1033,1036,6) ):
            lzbir =  aop(bu,1032,6) 
            dzbir =  suma(bu,1033,1036,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1032 kol. 6 = AOP-u (1033 + 1034 + 1035 + 1036) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10033
        if( aop(bu,1027,5) > aop(bu,1032,5) ):
            if not( aop(bu,1037,5) == aop(bu,1027,5)-aop(bu,1032,5) ):
                lzbir =  aop(bu,1037,5) 
                dzbir =  aop(bu,1027,5)-aop(bu,1032,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1037 kol. 5 = AOP-u (1027 - 1032) kol. 5, ako je AOP 1027 kol. 5 > AOP-a 1032 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10034
        if( aop(bu,1027,6) > aop(bu,1032,6) ):
            if not( aop(bu,1037,6) == aop(bu,1027,6)-aop(bu,1032,6) ):
                lzbir =  aop(bu,1037,6) 
                dzbir =  aop(bu,1027,6)-aop(bu,1032,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1037 kol. 6 = AOP-u (1027 - 1032) kol. 6, ako je AOP 1027 kol. 6 > AOP-a 1032 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10035
        if( aop(bu,1027,5) < aop(bu,1032,5) ):
            if not( aop(bu,1038,5) == aop(bu,1032,5)-aop(bu,1027,5) ):
                lzbir =  aop(bu,1038,5) 
                dzbir =  aop(bu,1032,5)-aop(bu,1027,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1038 kol. 5 = AOP-u (1032 - 1027) kol. 5, ako je AOP 1027 kol. 5 < AOP-a 1032 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10036
        if( aop(bu,1027,6) < aop(bu,1032,6) ):
            if not( aop(bu,1038,6) == aop(bu,1032,6)-aop(bu,1027,6) ):
                lzbir =  aop(bu,1038,6) 
                dzbir =  aop(bu,1032,6)-aop(bu,1027,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1038 kol. 6 = AOP-u (1032 - 1027) kol. 6, ako je AOP 1027 kol. 6 < AOP-a 1032 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10037
        if( aop(bu,1027,5) == aop(bu,1032,5) ):
            if not( suma(bu,1037,1038,5) == 0 ):
                lzbir =  suma(bu,1037,1038,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1037 + 1038) kol. 5 = 0, ako je AOP 1027 kol. 5 = AOP-u 1032 kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10038
        if( aop(bu,1027,6) == aop(bu,1032,6) ):
            if not( suma(bu,1037,1038,6) == 0 ):
                lzbir =  suma(bu,1037,1038,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1037 + 1038) kol. 6 = 0, ako je AOP 1027 kol. 6 = AOP-u 1032 kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10039
        if( aop(bu,1037,5) > 0 ):
            if not( aop(bu,1038,5) == 0 ):
                lzbir =  aop(bu,1038,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1037 kol. 5 > 0 onda je AOP 1038 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10040
        if( aop(bu,1038,5) > 0 ):
            if not( aop(bu,1037,5) == 0 ):
                lzbir =  aop(bu,1037,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1038 kol. 5 > 0 onda je AOP 1037 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10041
        if( aop(bu,1037,6) > 0 ):
            if not( aop(bu,1038,6) == 0 ):
                lzbir =  aop(bu,1038,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1037 kol. 6 > 0 onda je AOP 1038 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10042
        if( aop(bu,1038,6) > 0 ):
            if not( aop(bu,1037,6) == 0 ):
                lzbir =  aop(bu,1037,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1038 kol. 6 > 0 onda je AOP 1037 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10043
        if not( suma_liste(bu,[1028,1029,1030,1031,1038],5) == suma(bu,1033,1037,5) ):
            lzbir =  suma_liste(bu,[1028,1029,1030,1031,1038],5) 
            dzbir =  suma(bu,1033,1037,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1028 + 1029 + 1030 + 1031 + 1038) kol. 5 = AOP-u (1033 + 1034 + 1035 + 1036 + 1037) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10044
        if not( suma_liste(bu,[1028,1029,1030,1031,1038],6) == suma(bu,1033,1037,6) ):
            lzbir =  suma_liste(bu,[1028,1029,1030,1031,1038],6) 
            dzbir =  suma(bu,1033,1037,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1028 + 1029 + 1030 + 1031 + 1038) kol. 6 = AOP-u (1033 + 1034 + 1035 + 1036 + 1037) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10045
        if not( aop(bu,1043,5) == suma_liste(bu,[1001,1027,1039,1041],5) ):
            lzbir =  aop(bu,1043,5) 
            dzbir =  suma_liste(bu,[1001,1027,1039,1041],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1043 kol. 5 = AOP-u (1001 + 1027 + 1039 + 1041) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10046
        if not( aop(bu,1043,6) == suma_liste(bu,[1001,1027,1039,1041],6) ):
            lzbir =  aop(bu,1043,6) 
            dzbir =  suma_liste(bu,[1001,1027,1039,1041],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1043 kol. 6 = AOP-u (1001 + 1027 + 1039 + 1041) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10047
        if not( aop(bu,1044,5) == suma_liste(bu,[1013,1032,1040,1042],5) ):
            lzbir =  aop(bu,1044,5) 
            dzbir =  suma_liste(bu,[1013,1032,1040,1042],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1044 kol. 5 = AOP-u (1013 + 1032 + 1040 + 1042) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10048
        if not( aop(bu,1044,6) == suma_liste(bu,[1013,1032,1040,1042],6) ):
            lzbir =  aop(bu,1044,6) 
            dzbir =  suma_liste(bu,[1013,1032,1040,1042],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1044 kol. 6 = AOP-u (1013 + 1032 + 1040 + 1042) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10049
        if( aop(bu,1043,5) > aop(bu,1044,5) ):
            if not( aop(bu,1045,5) == aop(bu,1043,5)-aop(bu,1044,5) ):
                lzbir =  aop(bu,1045,5) 
                dzbir =  aop(bu,1043,5)-aop(bu,1044,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1045 kol. 5 = AOP-u (1043 - 1044) kol. 5, ako je AOP 1043 kol. 5 > AOP-a 1044 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10050
        if( aop(bu,1043,6) > aop(bu,1044,6) ):
            if not( aop(bu,1045,6) == aop(bu,1043,6)-aop(bu,1044,6) ):
                lzbir =  aop(bu,1045,6) 
                dzbir =  aop(bu,1043,6)-aop(bu,1044,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1045 kol. 6 = AOP-u (1043 - 1044) kol. 6, ako je AOP 1043 kol. 6 > AOP-a 1044 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10051
        if( aop(bu,1043,5) < aop(bu,1044,5) ):
            if not( aop(bu,1046,5) == aop(bu,1044,5)-aop(bu,1043,5) ):
                lzbir =  aop(bu,1046,5) 
                dzbir =  aop(bu,1044,5)-aop(bu,1043,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1046 kol. 5 = AOP-u (1044 - 1043) kol. 5, ako je AOP 1043 kol. 5 < AOP-a 1044 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10052
        if( aop(bu,1043,6) < aop(bu,1044,6) ):
            if not( aop(bu,1046,6) == aop(bu,1044,6)-aop(bu,1043,6) ):
                lzbir =  aop(bu,1046,6) 
                dzbir =  aop(bu,1044,6)-aop(bu,1043,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1046 kol. 6 = AOP-u (1044 - 1043) kol. 6, ako je AOP 1043 kol. 6 < AOP-a 1044 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10053
        if( aop(bu,1043,5) == aop(bu,1044,5) ):
            if not( suma(bu,1045,1046,5) == 0 ):
                lzbir =  suma(bu,1045,1046,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1045 + 1046) kol. 5 = 0, ako je AOP 1043 kol. 5 = AOP-u 1044 kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10054
        if( aop(bu,1043,6) == aop(bu,1044,6) ):
            if not( suma(bu,1045,1046,6) == 0 ):
                lzbir =  suma(bu,1045,1046,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1045 + 1046) kol. 6 = 0, ako je AOP 1043 kol. 6 = AOP-u 1044 kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10055
        if( aop(bu,1045,5) > 0 ):
            if not( aop(bu,1046,5) == 0 ):
                lzbir =  aop(bu,1046,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1045 kol. 5 > 0 onda je AOP 1046 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10056
        if( aop(bu,1046,5) > 0 ):
            if not( aop(bu,1045,5) == 0 ):
                lzbir =  aop(bu,1045,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1046 kol. 5 > 0 onda je AOP 1045 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10057
        if( aop(bu,1045,6) > 0 ):
            if not( aop(bu,1046,6) == 0 ):
                lzbir =  aop(bu,1046,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1045 kol. 6 > 0 onda je AOP 1046 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10058
        if( aop(bu,1046,6) > 0 ):
            if not( aop(bu,1045,6) == 0 ):
                lzbir =  aop(bu,1045,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1046 kol. 6 > 0 onda je AOP 1045 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10059
        if not( suma_liste(bu,[1043,1046],5) == suma(bu,1044,1045,5) ):
            lzbir =  suma_liste(bu,[1043,1046],5) 
            dzbir =  suma(bu,1044,1045,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1043 + 1046) kol. 5 = AOP-u (1044 + 1045) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10060
        if not( suma_liste(bu,[1043,1046],6) == suma(bu,1044,1045,6) ):
            lzbir =  suma_liste(bu,[1043,1046],6) 
            dzbir =  suma(bu,1044,1045,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1043 + 1046) kol. 6 = AOP-u (1044 + 1045) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10061
        if not( suma_liste(bu,[1001,1027,1039,1041,1046],5) == suma_liste(bu,[1013,1032,1040,1042,1045],5) ):
            lzbir =  suma_liste(bu,[1001,1027,1039,1041,1046],5) 
            dzbir =  suma_liste(bu,[1013,1032,1040,1042,1045],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1027 + 1039 + 1041 + 1046) kol. 5 = AOP-u (1013 + 1032 + 1040 + 1042 + 1045) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10062
        if not( suma_liste(bu,[1001,1027,1039,1041,1046],6) == suma_liste(bu,[1013,1032,1040,1042,1045],6) ):
            lzbir =  suma_liste(bu,[1001,1027,1039,1041,1046],6) 
            dzbir =  suma_liste(bu,[1013,1032,1040,1042,1045],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1027 + 1039 + 1041 + 1046) kol. 6 = AOP-u (1013 + 1032 + 1040 + 1042 + 1045) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10063
        if( aop(bu,1047,5) > 0 ):
            if not( aop(bu,1048,5) == 0 ):
                lzbir =  aop(bu,1048,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1047 kol. 5 > 0 onda je AOP 1048 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10064
        if( aop(bu,1048,5) > 0 ):
            if not( aop(bu,1047,5) == 0 ):
                lzbir =  aop(bu,1047,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1048 kol. 5 > 0 onda je AOP 1047 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10065
        if( aop(bu,1047,6) > 0 ):
            if not( aop(bu,1048,6) == 0 ):
                lzbir =  aop(bu,1048,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1047 kol. 6 > 0 onda je AOP 1048 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10066
        if( aop(bu,1048,6) > 0 ):
            if not( aop(bu,1047,6) == 0 ):
                lzbir =  aop(bu,1047,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1048 kol. 6 > 0 onda je AOP 1047 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10067
        if( suma_liste(bu,[1045,1047],5) > suma_liste(bu,[1046,1048],5) ):
            if not( aop(bu,1049,5) == suma_liste(bu,[1045,1047],5)-suma_liste(bu,[1046,1048],5) ):
                lzbir =  aop(bu,1049,5) 
                dzbir =  suma_liste(bu,[1045,1047],5)-suma_liste(bu,[1046,1048],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1049 kol. 5 = AOP-u (1045 - 1046 + 1047 - 1048) kol. 5, ako je AOP (1045 + 1047) kol. 5 > AOP-a (1046 + 1048) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10068
        if( suma_liste(bu,[1045,1047],6) > suma_liste(bu,[1046,1048],6) ):
            if not( aop(bu,1049,6) == suma_liste(bu,[1045,1047],6)-suma_liste(bu,[1046,1048],6) ):
                lzbir =  aop(bu,1049,6) 
                dzbir =  suma_liste(bu,[1045,1047],6)-suma_liste(bu,[1046,1048],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1049 kol. 6 = AOP-u (1045 - 1046 + 1047 - 1048) kol. 6, ako je AOP (1045 + 1047) kol. 6 > AOP-a (1046 + 1048) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10069
        if( suma_liste(bu,[1045,1047],5) < suma_liste(bu,[1046,1048],5) ):
            if not( aop(bu,1050,5) == suma_liste(bu,[1046,1048],5)-suma_liste(bu,[1045,1047],5) ):
                lzbir =  aop(bu,1050,5) 
                dzbir =  suma_liste(bu,[1046,1048],5)-suma_liste(bu,[1045,1047],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1050 kol. 5 = AOP-u (1046 - 1045 + 1048 - 1047) kol. 5, ako je AOP (1045 + 1047) kol. 5 < AOP-a (1046 + 1048) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10070
        if( suma_liste(bu,[1045,1047],6) < suma_liste(bu,[1046,1048],6) ):
            if not( aop(bu,1050,6) == suma_liste(bu,[1046,1048],6)-suma_liste(bu,[1045,1047],6) ):
                lzbir =  aop(bu,1050,6) 
                dzbir =  suma_liste(bu,[1046,1048],6)-suma_liste(bu,[1045,1047],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1050 kol. 6 = AOP-u (1046 - 1045 + 1048 - 1047) kol. 6, ako je AOP (1045 + 1047) kol. 6 < AOP-a (1046 + 1048) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10071
        if( suma_liste(bu,[1045,1047],5) == suma_liste(bu,[1046,1048],5) ):
            if not( suma(bu,1049,1050,5) == 0 ):
                lzbir =  suma(bu,1049,1050,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1049 + 1050) kol. 5 = 0, ako je AOP (1045 + 1047) kol. 5 = AOP-u (1046 + 1048) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10072
        if( suma_liste(bu,[1045,1047],6) == suma_liste(bu,[1046,1048],6) ):
            if not( suma(bu,1049,1050,6) == 0 ):
                lzbir =  suma(bu,1049,1050,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1049 + 1050) kol. 6 = 0, ako je AOP (1045 + 1047) kol. 6 = AOP-u (1046 + 1048) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10073
        if( aop(bu,1049,5) > 0 ):
            if not( aop(bu,1050,5) == 0 ):
                lzbir =  aop(bu,1050,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1049 kol. 5 > 0 onda je AOP 1050 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10074
        if( aop(bu,1050,5) > 0 ):
            if not( aop(bu,1049,5) == 0 ):
                lzbir =  aop(bu,1049,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1050 kol. 5 > 0 onda je AOP 1049 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10075
        if( aop(bu,1049,6) > 0 ):
            if not( aop(bu,1050,6) == 0 ):
                lzbir =  aop(bu,1050,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1049 kol. 6 > 0 onda je AOP 1050 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10076
        if( aop(bu,1050,6) > 0 ):
            if not( aop(bu,1049,6) == 0 ):
                lzbir =  aop(bu,1049,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1050 kol. 6 > 0 onda je AOP 1049 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10077
        if not( suma_liste(bu,[1045,1047,1050],5) == suma_liste(bu,[1046,1048,1049],5) ):
            lzbir =  suma_liste(bu,[1045,1047,1050],5) 
            dzbir =  suma_liste(bu,[1046,1048,1049],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1045 + 1047 + 1050) kol. 5 = AOP-u (1046 + 1048 + 1049) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10078
        if not( suma_liste(bu,[1045,1047,1050],6) == suma_liste(bu,[1046,1048,1049],6) ):
            lzbir =  suma_liste(bu,[1045,1047,1050],6) 
            dzbir =  suma_liste(bu,[1046,1048,1049],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1045 + 1047 + 1050) kol. 6 = AOP-u (1046 + 1048 + 1049) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10079
        if( suma_liste(bu,[1049,1053],5) > suma_liste(bu,[1050,1051,1052,1054],5) ):
            if not( aop(bu,1055,5) == suma_liste(bu,[1049,1053],5)-suma_liste(bu,[1050,1051,1052,1054],5) ):
                lzbir =  aop(bu,1055,5) 
                dzbir =  suma_liste(bu,[1049,1053],5)-suma_liste(bu,[1050,1051,1052,1054],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1055 kol. 5 = AOP-u (1049 - 1050 - 1051 - 1052 + 1053 - 1054) kol. 5, ako je AOP (1049 + 1053) kol. 5 > AOP-a (1050 + 1051 + 1052 + 1054) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10080
        if( suma_liste(bu,[1049,1053],6) > suma_liste(bu,[1050,1051,1052,1054],6) ):
            if not( aop(bu,1055,6) == suma_liste(bu,[1049,1053],6)-suma_liste(bu,[1050,1051,1052,1054],6) ):
                lzbir =  aop(bu,1055,6) 
                dzbir =  suma_liste(bu,[1049,1053],6)-suma_liste(bu,[1050,1051,1052,1054],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1055 kol. 6 = AOP-u (1049 - 1050 - 1051 - 1052 + 1053 - 1054) kol. 6, ako je AOP (1049 + 1053) kol. 6 > AOP-a (1050 + 1051 + 1052 + 1054) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10081
        if( suma_liste(bu,[1049,1053],5) < suma_liste(bu,[1050,1051,1052,1054],5) ):
            if not( aop(bu,1056,5) == suma_liste(bu,[1050,1051,1052,1054],5)-suma_liste(bu,[1049,1053],5) ):
                lzbir =  aop(bu,1056,5) 
                dzbir =  suma_liste(bu,[1050,1051,1052,1054],5)-suma_liste(bu,[1049,1053],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1056 kol. 5 = AOP-u (1050 - 1049 + 1051 + 1052 - 1053 + 1054) kol. 5,  ako je AOP (1049 + 1053) kol. 5 < AOP-a (1050 + 1051 + 1052 + 1054) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10082
        if( suma_liste(bu,[1049,1053],6) < suma_liste(bu,[1050,1051,1052,1054],6) ):
            if not( aop(bu,1056,6) == suma_liste(bu,[1050,1051,1052,1054],6)-suma_liste(bu,[1049,1053],6) ):
                lzbir =  aop(bu,1056,6) 
                dzbir =  suma_liste(bu,[1050,1051,1052,1054],6)-suma_liste(bu,[1049,1053],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1056 kol. 6 = AOP-u (1050 - 1049 + 1051 + 1052 - 1053 + 1054) kol. 6,  ako je AOP (1049 + 1053) kol. 6 < AOP-a (1050 + 1051 + 1052 + 1054) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10083
        if( suma_liste(bu,[1049,1053],5) == suma_liste(bu,[1050,1051,1052,1054],5) ):
            if not( suma(bu,1055,1056,5) == 0 ):
                lzbir =  suma(bu,1055,1056,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1055 + 1056) kol. 5 = 0, ako je AOP (1049 + 1053) kol. 5 = AOP-u (1050 + 1051 + 1052 + 1054) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10084
        if( suma_liste(bu,[1049,1053],6) == suma_liste(bu,[1050,1051,1052,1054],6) ):
            if not( suma(bu,1055,1056,6) == 0 ):
                lzbir =  suma(bu,1055,1056,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1055 + 1056) kol. 6 = 0, ako je AOP (1049 + 1053) kol. 6 = AOP-u (1050 + 1051 + 1052 + 1054) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10085
        if( aop(bu,1055,5) > 0 ):
            if not( aop(bu,1056,5) == 0 ):
                lzbir =  aop(bu,1056,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1055 kol. 5 > 0 onda je AOP 1056 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10086
        if( aop(bu,1056,5) > 0 ):
            if not( aop(bu,1055,5) == 0 ):
                lzbir =  aop(bu,1055,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1056 kol. 5 > 0 onda je AOP 1055 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10087
        if( aop(bu,1055,6) > 0 ):
            if not( aop(bu,1056,6) == 0 ):
                lzbir =  aop(bu,1056,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1055 kol. 6 > 0 onda je AOP 1056 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10088
        if( aop(bu,1056,6) > 0 ):
            if not( aop(bu,1055,6) == 0 ):
                lzbir =  aop(bu,1055,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1056 kol. 6 > 0 onda je AOP 1055 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10089
        if not( suma_liste(bu,[1049,1053,1056],5) == suma_liste(bu,[1050,1051,1052,1054,1055],5) ):
            lzbir =  suma_liste(bu,[1049,1053,1056],5) 
            dzbir =  suma_liste(bu,[1050,1051,1052,1054,1055],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1049 + 1053 + 1056) kol. 5 = AOP-u (1050 + 1051 + 1052 + 1054 + 1055) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10090
        if not( suma_liste(bu,[1049,1053,1056],6) == suma_liste(bu,[1050,1051,1052,1054,1055],6) ):
            lzbir =  suma_liste(bu,[1049,1053,1056],6) 
            dzbir =  suma_liste(bu,[1050,1051,1052,1054,1055],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1049 + 1053 + 1056) kol. 6 = AOP-u (1050 + 1051 + 1052 + 1054 + 1055) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10091
        if not( suma_liste(bu,[1001,1027,1039,1041,1047,1053,1056],5) == suma_liste(bu,[1013,1032,1040,1042,1048,1051,1052,1054,1055],5) ):
            lzbir =  suma_liste(bu,[1001,1027,1039,1041,1047,1053,1056],5) 
            dzbir =  suma_liste(bu,[1013,1032,1040,1042,1048,1051,1052,1054,1055],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1027 + 1039 + 1041 + 1047 + 1053 + 1056) kol. 5 = AOP-u (1013 + 1032 + 1040 + 1042 + 1048 + 1051 + 1052 + 1054 + 1055) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10092
        if not( suma_liste(bu,[1001,1027,1039,1041,1047,1053,1056],6) == suma_liste(bu,[1013,1032,1040,1042,1048,1051,1052,1054,1055],6) ):
            lzbir =  suma_liste(bu,[1001,1027,1039,1041,1047,1053,1056],6) 
            dzbir =  suma_liste(bu,[1013,1032,1040,1042,1048,1051,1052,1054,1055],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1027 + 1039 + 1041 + 1047 + 1053 + 1056) kol. 6 = AOP-u (1013 + 1032 + 1040 + 1042 + 1048 + 1051 + 1052 + 1054 + 1055) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10093
        #Za ovaj set se ne primenjuje pravilo 
        #10094
        #Za ovaj set se ne primenjuje pravilo 
        #10095
        #Za ovaj set se ne primenjuje pravilo 
        #10096
        #Za ovaj set se ne primenjuje pravilo 
        #10097
        if not( aop(bu,1057,5) == 0 ):
            lzbir =  aop(bu,1057,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1057 kol. 5 = 0 Neto dobitak koji pripada učešćima bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10098
        if not( aop(bu,1057,6) == 0 ):
            lzbir =  aop(bu,1057,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1057 kol. 6 = 0 Neto dobitak koji pripada učešćima bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10099
        if not( aop(bu,1058,5) == 0 ):
            lzbir =  aop(bu,1058,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1058 kol. 5 = 0 Neto dobitak koji pripada matičnom pravnom licu  prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10100
        if not( aop(bu,1058,6) == 0 ):
            lzbir =  aop(bu,1058,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1058 kol. 6 = 0 Neto dobitak koji pripada matičnom pravnom licu  prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10101
        if not( aop(bu,1059,5) == 0 ):
            lzbir =  aop(bu,1059,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1059 kol. 5 = 0 Neto gubitak koji pripada učešćima bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10102
        if not( aop(bu,1059,6) == 0 ):
            lzbir =  aop(bu,1059,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1059 kol. 6 = 0 Neto gubitak koji pripada učešćima bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10103
        if not( aop(bu,1060,5) == 0 ):
            lzbir =  aop(bu,1060,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1060 kol. 5 = 0 Neto gubitak koji pripada matičnom pravnom licu prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10104
        if not( aop(bu,1060,6) == 0 ):
            lzbir =  aop(bu,1060,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1060 kol. 6 = 0 Neto gubitak koji pripada matičnom pravnom licu prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10105
        if( aop(bu,1055,5) > 0 ):
            if not( aop(bs,410,5) == aop(bu,1055,5) ):
                lzbir =  aop(bs,410,5) 
                dzbir =  aop(bu,1055,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1055 kol. 5  > 0, onda je AOP 0410 kol. 5 bilansa stanja = AOP-u 1055 kol. 5   Neto dobitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu neraspoređenog dobitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1055 kol. 5  > 0, onda je AOP 0410 kol. 5 bilansa stanja = AOP-u 1055 kol. 5   Neto dobitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu neraspoređenog dobitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10106
        if( aop(bs,410,5) > 0 ):
            if not( aop(bs,410,5) == aop(bu,1055,5) ):
                lzbir =  aop(bs,410,5) 
                dzbir =  aop(bu,1055,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0410 kol. 5 bilansa stanja > 0, onda je AOP 0410 kol. 5 bilansa stanja = AOP-u 1055 kol. 5   Neto dobitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu neraspoređenog dobitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 0410 kol. 5 bilansa stanja > 0, onda je AOP 0410 kol. 5 bilansa stanja = AOP-u 1055 kol. 5   Neto dobitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu neraspoređenog dobitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10107
        if( aop(bu,1055,6) > 0 ):
            if not( aop(bs,410,6) == aop(bu,1055,6) ):
                lzbir =  aop(bs,410,6) 
                dzbir =  aop(bu,1055,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1055 kol. 6  > 0, onda je AOP 0410 kol. 6 bilansa stanja = AOP-u 1055 kol. 6  Neto dobitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak   neraspoređenom dobitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja.  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1055 kol. 6  > 0, onda je AOP 0410 kol. 6 bilansa stanja = AOP-u 1055 kol. 6  Neto dobitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak   neraspoređenom dobitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja.  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10108
        if( aop(bs,410,6) > 0 ):
            if not( aop(bs,410,6) == aop(bu,1055,6) ):
                lzbir =  aop(bs,410,6) 
                dzbir =  aop(bu,1055,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0410 kol. 6 bilansa stanja > 0, onda je AOP 0410 kol. 6 bilansa stanja = AOP-u 1055 kol. 6  Neto dobitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak   neraspoređenom dobitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja.  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 0410 kol. 6 bilansa stanja > 0, onda je AOP 0410 kol. 6 bilansa stanja = AOP-u 1055 kol. 6  Neto dobitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak   neraspoređenom dobitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja.  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10109
        if( aop(bu,1056,5) > 0 ):
            if not( aop(bs,414,5) == aop(bu,1056,5) ):
                lzbir =  aop(bs,414,5) 
                dzbir =  aop(bu,1056,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1056 kol. 5 > 0, onda  je AOP 0414 kol. 5 bilansa stanja = AOP-u 1056 kol. 5   Neto gubitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu gubitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1056 kol. 5 > 0, onda  je AOP 0414 kol. 5 bilansa stanja = AOP-u 1056 kol. 5   Neto gubitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu gubitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10110
        if( aop(bs,414,5) > 0 ):
            if not( aop(bs,414,5) == aop(bu,1056,5) ):
                lzbir =  aop(bs,414,5) 
                dzbir =  aop(bu,1056,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0414 kol. 5 bilansa stanja > 0, onda  je AOP 0414 kol. 5 bilansa stanja = AOP-u 1056 kol. 5   Neto gubitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu gubitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 0414 kol. 5 bilansa stanja > 0, onda  je AOP 0414 kol. 5 bilansa stanja = AOP-u 1056 kol. 5   Neto gubitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu gubitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10111
        if( aop(bu,1056,6) > 0 ):
            if not( aop(bs,414,6) == aop(bu,1056,6) ):
                lzbir =  aop(bs,414,6) 
                dzbir =  aop(bu,1056,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1056 kol. 6 > 0, onda  je AOP 0414 kol. 6 bilansa stanja = AOP-u 1056 kol. 6  Neto gubitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak  gubitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja.  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1056 kol. 6 > 0, onda  je AOP 0414 kol. 6 bilansa stanja = AOP-u 1056 kol. 6  Neto gubitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak  gubitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja.  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10112
        if( aop(bs,414,6) > 0 ):
            if not( aop(bs,414,6) == aop(bu,1056,6) ):
                lzbir =  aop(bs,414,6) 
                dzbir =  aop(bu,1056,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0414 kol. 6 bilansa stanja > 0, onda  je AOP 0414 kol. 6 bilansa stanja = AOP-u 1056 kol. 6  Neto gubitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak  gubitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja.  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 0414 kol. 6 bilansa stanja > 0, onda  je AOP 0414 kol. 6 bilansa stanja = AOP-u 1056 kol. 6  Neto gubitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak  gubitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja.  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10113
        #Za ovaj set se ne primenjuje pravilo 
        #10114
        #Za ovaj set se ne primenjuje pravilo 
        #10115
        #Za ovaj set se ne primenjuje pravilo 
        #10116
        #Za ovaj set se ne primenjuje pravilo 
        #10117
        if not( aop(bu,1051,5) > 0 ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1051 kol. 5 > 0 Na poziciji Poreski rashod perioda nije iskazan podatak; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #10118
        if not( aop(bu,1054,5) == 0 ):
            lzbir =  aop(bu,1054,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1054 kol. 5 = 0 Proveriti tačnost unetog podatka na poziciji Isplaćena lična primanja poslodavca, kako bi se izbegle slučajne greške prilikom iskazivanja ovog podatka; Zakonski zastupnik svojim potpisom potvrđuje da pravno lice ima isplaćena lična primanja poslodavca '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #10119
        if( suma(bu,1001,1062,5) > 0 ):
            if not( suma(bu,1001,1062,5) != suma(bu,1001,1062,6) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='***Ako je zbir podataka na oznakama za AOP (1001 do 1062) kol. 5 bilansa uspeha > 0 onda zbir podataka na oznakama za AOP (1001 do 1062) kol. 5 bilansa uspeha ≠ zbiru podataka na oznakama za AOP  (1001 do 1062) kol. 6 bilansa uspeha Zbirovi podataka u kolonama 5 i 6 bilansa uspeha su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10120
        #Za ovaj set se ne primenjuje pravilo
        
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

 