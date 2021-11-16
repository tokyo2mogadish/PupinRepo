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

#Ako forma ima bar jednu napomenu u zadatom opsegu vraca True u suprotnom False   
#def proveriNapomene(aop_dict, prvi_aop, poslednji_aop, kolona):
#    imaBarJednuNapomenu = False
#    for aop_broj in range (prvi_aop, poslednji_aop+1):
#        aop_key = broj_u_aop(aop_broj, kolona)
#        if aop_dict[aop_key].strip():
#            imaBarJednuNapomenu = True
#            break
#    return imaBarJednuNapomenu 

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
        if not( suma(bs,1,3,5)+suma(bs,1,3,6)+suma(bs,1,3,7)+suma(bs,9,14,5)+suma(bs,9,14,6)+suma(bs,9,14,7)+suma(bs,19,25,5)+suma(bs,19,25,6)+suma(bs,19,25,7)+suma(bs,401,405,5)+suma(bs,401,405,6)+suma(bs,401,405,7)+aop(bs,408,5)+aop(bs,408,6)+aop(bs,408,7)+suma(bs,411,413,5)+suma(bs,411,413,6)+suma(bs,411,413,7)+suma(bs,416,428,5)+suma(bs,416,428,6)+suma(bs,416,428,7)+suma(bu,1001,1048,5)+suma(bu,1001,1048,6) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0003) kol. 5 + (0001 do 0003) kol. 6 + (0001 do 0003) kol. 7 + (0009 do 0014) kol. 5 + (0009 do 0014) kol. 6 + (0009 do 0014) kol. 7  + (0019 do 0025) kol. 5 + (0019 do 0025) kol. 6 +  (0019 do 0025) kol. 7 bilansa stanja + (0401 do 0405) kol. 5 + (0401 do 0405) kol. 6 +  (0401 do 0405) kol. 7  + 0408 kol.5 + 0408 kol. 6 + 0408 kol. 7  + (0411 do 0413) kol. 5 + (0411 do 0413) kol. 6 +  (0411 do 0413) kol. 7 + (0416 do 0428) kol. 5 + (0416 do 0428) kol. 6 + (0416 do 0428) kol. 7  bilansa stanja + (1001 do 1048) kol. 5 + (1001 do 1048) kol. 6 bilansa uspeha > 0 Vanredni finansijski izveštaj, po pravilu ne sme biti bez podataka; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0003) kol. 5 + (0001 do 0003) kol. 6 + (0001 do 0003) kol. 7 + (0009 do 0014) kol. 5 + (0009 do 0014) kol. 6 + (0009 do 0014) kol. 7  + (0019 do 0025) kol. 5 + (0019 do 0025) kol. 6 +  (0019 do 0025) kol. 7 bilansa stanja + (0401 do 0405) kol. 5 + (0401 do 0405) kol. 6 +  (0401 do 0405) kol. 7  + 0408 kol.5 + 0408 kol. 6 + 0408 kol. 7  + (0411 do 0413) kol. 5 + (0411 do 0413) kol. 6 +  (0411 do 0413) kol. 7 + (0416 do 0428) kol. 5 + (0416 do 0428) kol. 6 + (0416 do 0428) kol. 7  bilansa stanja + (1001 do 1048) kol. 5 + (1001 do 1048) kol. 6 bilansa uspeha > 0 Vanredni finansijski izveštaj, po pravilu ne sme biti bez podataka; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #00000-5
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-6
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-7
        bsNapomene = Zahtev.Forme['Bilans stanja'].TekstualnaPoljaForme;
        buNapomene = Zahtev.Forme['Bilans uspeha'].TekstualnaPoljaForme;
        if not(proveriNapomene(bsNapomene,1,3,4) and proveriNapomene(bsNapomene,9,14,4) and proveriNapomene(bsNapomene,19,25,4) and proveriNapomene(bsNapomene,401,405,4) and proveriNapomene(bsNapomene,408,408,4) and proveriNapomene(bsNapomene,411,413,4) and proveriNapomene(bsNapomene,416,428,4) and proveriNapomene(buNapomene,1001,1048,4) ): 
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Na AOP-u (0001 do 0003) + (0009 do 0014)+ (0019 do 0025) bilansa stanja + (0401 do 0405) + 0408  + (0411 do 0413) + (0416 do 0428) bilansa stanja + (1001 do 1048) bilansa uspeha, u koloni 4 (Napomena broj) ne sme biti iskazan podatak kod obveznika koji nemaju obavezu dostavljanja napomena uz finansijski izveštaj. '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ='Na AOP-u (0001 do 0003) + (0009 do 0014)+ (0019 do 0025) bilansa stanja + (0401 do 0405) + 0408  + (0411 do 0413) + (0416 do 0428) bilansa stanja + (1001 do 1048) bilansa uspeha, u koloni 4 (Napomena broj) ne sme biti iskazan podatak kod obveznika koji nemaju obavezu dostavljanja napomena uz finansijski izveštaj. '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #Provera da li je fizahtev placen
        if not(Zahtev.Placen):
            ostalo_errors.append('Naknada za obradu i javno objavljivanje izveštaja i propisane dokumentacije nije uplaćena u propisanom iznosu. Instrukcije za uplatu propisane naknade date su u okviru PIS FI sistema za konkretan zahtev, na linku „Status naplate zahteva / Instrukcija za plaćanje". Ukoliko ste izvršili uplatu, a naknada nije uparena, priložite Dokaz o uplati naknade u delu Dokumentacija (na mestu predviđenom za dokaz o uplati naknade), kako biste mogli da podnesete izveštaj.');

        #Provera negativnih AOP-a
        lista=""
        lista_bs = find_negativni(bs, 1, 428, 5, 7)
        lista_bu = find_negativni(bu, 1001, 1048, 5, 6)
       
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
        #Za ovaj set se ne primenjuje pravilo 
        
        #00002
        if not( suma(bs,1,3,5)+suma(bs,9,14,5)+suma(bs,19,25,5)+suma(bs,401,405,5)+aop(bs,408,5)+suma(bs,411,413,5)+suma(bs,416,428,5) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0003) kol. 5 + (0009 do 0014) kol. 5 + (0019 do 0025) kol. 5 + (0401 do 0405) kol. 5  + 0408 kol. 5 + (0411 do 0413) kol. 5 + (0416 do 0428) kol. 5 > 0 Bilans stanja, po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #00003
        #Za ovaj set se ne primenjuje pravilo 
        
        #00004
        #Za ovaj set se ne primenjuje pravilo 
        
        #00005
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,3,6)+suma(bs,9,14,6)+suma(bs,19,25,6)+suma(bs,401,405,6)+aop(bs,408,6)+suma(bs,411,413,6)+suma(bs,416,428,6) == 0 ):
                lzbir =  suma(bs,1,3,6)+suma(bs,9,14,6)+suma(bs,19,25,6)+suma(bs,401,405,6)+aop(bs,408,6)+suma(bs,411,413,6)+suma(bs,416,428,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0003) kol. 6 + (0009 do 0014) kol. 6 + (0019 do 0025) kol. 6 + (0401 do 0405) kol. 6  + 0408 kol. 6 + (0411 do 0413) kol. 6 + (0416 do 0428) kol. 6 = 0 Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00006
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,3,7)+suma(bs,9,14,7)+suma(bs,19,25,7)+suma(bs,401,405,7)+aop(bs,408,7)+suma(bs,411,413,7)+suma(bs,416,428,7) == 0 ):
                lzbir =  suma(bs,1,3,7)+suma(bs,9,14,7)+suma(bs,19,25,7)+suma(bs,401,405,7)+aop(bs,408,7)+suma(bs,411,413,7)+suma(bs,416,428,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0003) kol. 7 + (0009 do 0014) kol. 7+ (0019 do 0025) kol. 7 + (0401 do 0405) kol. 7  + 0408 kol. 7 + (0411 do 0413) kol. 7 + (0416 do 0428) kol. 7 = 0 Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00007
        #Za ovaj set se ne primenjuje pravilo 
        
        #00008
        #Za ovaj set se ne primenjuje pravilo 
        
        #00009
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,3,6)+suma(bs,9,14,6)+suma(bs,19,25,6)+suma(bs,401,405,6)+aop(bs,408,6)+suma(bs,411,413,6)+suma(bs,416,428,6) > 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0003) kol. 6 + (0009 do 0014) kol. 6 + (0019 do 0025) kol. 6 + (0401 do 0405) kol. 6  + 0408 kol. 6 + (0411 do 0413) kol. 6 + (0416 do 0428) kol. 6  > 0 Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #00010
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,3,7)+suma(bs,9,14,7)+suma(bs,19,25,7)+suma(bs,401,405,7)+aop(bs,408,7)+suma(bs,411,413,7)+suma(bs,416,428,7) > 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0003) kol. 7 + (0009 do 0014) kol. 7 + (0019 do 0025) kol. 7 + (0401 do 0405) kol. 7  + 0408 kol. 7 + (0411 do 0413) kol. 7 + (0416 do 0428) kol. 7  > 0 Bilans stanja, po pravilu,  mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #00011
        if not( aop(bs,1,5) == suma_liste(bs,[2,3,9,10,11,12],5) ):
            lzbir =  aop(bs,1,5) 
            dzbir =  suma_liste(bs,[2,3,9,10,11,12],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0001 kol. 5 = AOP-u (0002 + 0003 + 0009 + 0010 + 0011 + 0012) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00012
        if not( aop(bs,1,6) == suma_liste(bs,[2,3,9,10,11,12],6) ):
            lzbir =  aop(bs,1,6) 
            dzbir =  suma_liste(bs,[2,3,9,10,11,12],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0001 kol. 6 = AOP-u (0002 + 0003 + 0009 + 0010 + 0011 + 0012) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00013
        if not( aop(bs,1,7) == suma_liste(bs,[2,3,9,10,11,12],7) ):
            lzbir =  aop(bs,1,7) 
            dzbir =  suma_liste(bs,[2,3,9,10,11,12],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0001 kol. 7 = AOP-u (0002 + 0003 + 0009 + 0010 + 0011 + 0012) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00014
        #Za ovaj set se ne primenjuje pravilo 
        
        #00015
        #Za ovaj set se ne primenjuje pravilo 
        
        #00016
        #Za ovaj set se ne primenjuje pravilo 
        
        #00017
        if not( aop(bs,13,5) == suma_liste(bs,[14,19,20,21,22,23],5) ):
            lzbir =  aop(bs,13,5) 
            dzbir =  suma_liste(bs,[14,19,20,21,22,23],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0013 kol. 5 = AOP-u (0014 + 0019 + 0020 + 0021 + 0022 + 0023) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00018
        if not( aop(bs,13,6) == suma_liste(bs,[14,19,20,21,22,23],6) ):
            lzbir =  aop(bs,13,6) 
            dzbir =  suma_liste(bs,[14,19,20,21,22,23],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0013 kol. 6 = AOP-u (0014 + 0019 + 0020 + 0021 + 0022 + 0023) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00019
        if not( aop(bs,13,7) == suma_liste(bs,[14,19,20,21,22,23],7) ):
            lzbir =  aop(bs,13,7) 
            dzbir =  suma_liste(bs,[14,19,20,21,22,23],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0013 kol. 7 = AOP-u (0014 + 0019 + 0020 + 0021 + 0022 + 0023) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00020
        #Za ovaj set se ne primenjuje pravilo 
        
        #00021
        #Za ovaj set se ne primenjuje pravilo 
        
        #00022
        #Za ovaj set se ne primenjuje pravilo 
        
        #00023
        if not( aop(bs,24,5) == suma_liste(bs,[1,13],5) ):
            lzbir =  aop(bs,24,5) 
            dzbir =  suma_liste(bs,[1,13],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0024 kol. 5 = AOP-u (0001 + 0013) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00024
        if not( aop(bs,24,6) == suma_liste(bs,[1,13],6) ):
            lzbir =  aop(bs,24,6) 
            dzbir =  suma_liste(bs,[1,13],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0024 kol. 6 = AOP-u (0001 + 0013) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00025
        if not( aop(bs,24,7) == suma_liste(bs,[1,13],7) ):
            lzbir =  aop(bs,24,7) 
            dzbir =  suma_liste(bs,[1,13],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0024 kol. 7 = AOP-u (0001 + 0013) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00026
        if( suma_liste(bs,[402,403,405],5) > suma_liste(bs,[404,408],5) ):
            if not( aop(bs,401,5) == suma_liste(bs,[402,403,405],5)-suma_liste(bs,[404,408],5) ):
                lzbir =  aop(bs,401,5) 
                dzbir =  suma_liste(bs,[402,403,405],5)-suma_liste(bs,[404,408],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0401 kol. 5 = AOP-u (0402 + 0403 - 0404 + 0405 - 0408) kol. 5, ako je AOP (0402 + 0403 + 0405) kol. 5 > AOP-a (0404 + 0408) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00027
        if( suma_liste(bs,[402,403,405],6) > suma_liste(bs,[404,408],6) ):
            if not( aop(bs,401,6) == suma_liste(bs,[402,403,405],6)-suma_liste(bs,[404,408],6) ):
                lzbir =  aop(bs,401,6) 
                dzbir =  suma_liste(bs,[402,403,405],6)-suma_liste(bs,[404,408],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0401 kol. 6 = AOP-u (0402 + 0403 - 0404 + 0405 - 0408) kol. 6, ako je AOP (0402 + 0403 + 0405) kol. 6 > AOP-a (0404 + 0408) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00028
        if( suma_liste(bs,[402,403,405],7) > suma_liste(bs,[404,408],7) ):
            if not( aop(bs,401,7) == suma_liste(bs,[402,403,405],7)-suma_liste(bs,[404,408],7) ):
                lzbir =  aop(bs,401,7) 
                dzbir =  suma_liste(bs,[402,403,405],7)-suma_liste(bs,[404,408],7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0401 kol. 7 = AOP-u (0402 + 0403 - 0404 + 0405 - 0408) kol. 7, ako je AOP (0402 + 0403 + 0405) kol. 7 > AOP-a (0404 + 0408) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00029
        if( aop(bs,24,5) > suma_liste(bs,[411,416,417,418],5) ):
            if not( aop(bs,401,5) == aop(bs,24,5)-suma_liste(bs,[411,416,417,418],5) ):
                lzbir =  aop(bs,401,5) 
                dzbir =  aop(bs,24,5)-suma_liste(bs,[411,416,417,418],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0401 kol. 5 = AOP-u (0024 - 0411 - 0416 - 0417 - 0418) kol. 5, ako je AOP 0024 kol. 5 > AOP-a (0411 + 0416 + 0417 + 0418) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00030
        if( aop(bs,24,6) > suma_liste(bs,[411,416,417,418],6) ):
            if not( aop(bs,401,6) == aop(bs,24,6)-suma_liste(bs,[411,416,417,418],6) ):
                lzbir =  aop(bs,401,6) 
                dzbir =  aop(bs,24,6)-suma_liste(bs,[411,416,417,418],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0401 kol. 6 = AOP-u (0024 - 0411 - 0416 - 0417 - 0418) kol. 6, ako je AOP 0024 kol. 6 > AOP-a (0411 + 0416 + 0417 + 0418) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00031
        if( aop(bs,24,7) > suma_liste(bs,[411,416,417,418],7) ):
            if not( aop(bs,401,7) == aop(bs,24,7)-suma_liste(bs,[411,416,417,418],7) ):
                lzbir =  aop(bs,401,7) 
                dzbir =  aop(bs,24,7)-suma_liste(bs,[411,416,417,418],7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0401 kol. 7 = AOP-u (0024 - 0411 - 0416 - 0417 - 0418) kol. 7, ako je AOP 0024 kol. 7 > AOP-a (0411 + 0416 + 0417 + 0418) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00032
        #Za ovaj set se ne primenjuje pravilo 
        
        #00033
        #Za ovaj set se ne primenjuje pravilo 
        
        #00034
        #Za ovaj set se ne primenjuje pravilo 
        
        #00035
        #Za ovaj set se ne primenjuje pravilo 
        
        #00036
        #Za ovaj set se ne primenjuje pravilo 
        
        #00037
        #Za ovaj set se ne primenjuje pravilo 
        
        #00038
        if not( aop(bs,411,5) == suma(bs,412,413,5) ):
            lzbir =  aop(bs,411,5) 
            dzbir =  suma(bs,412,413,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0411 kol. 5 = AOP-u (0412 + 0413) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00039
        if not( aop(bs,411,6) == suma(bs,412,413,6) ):
            lzbir =  aop(bs,411,6) 
            dzbir =  suma(bs,412,413,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0411 kol. 6 = AOP-u (0412 + 0413) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00040
        if not( aop(bs,411,7) == suma(bs,412,413,7) ):
            lzbir =  aop(bs,411,7) 
            dzbir =  suma(bs,412,413,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0411 kol. 7 = AOP-u (0412 + 0413) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00041
        #Za ovaj set se ne primenjuje pravilo 
        
        #00042
        #Za ovaj set se ne primenjuje pravilo 
        
        #00043
        #Za ovaj set se ne primenjuje pravilo 
        
        #00044
        if not( aop(bs,418,5) == suma(bs,419,425,5) ):
            lzbir =  aop(bs,418,5) 
            dzbir =  suma(bs,419,425,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0418 kol. 5 = AOP-u (0419 + 0420 + 0421 + 0422 + 0423 + 0424 + 0425) kol. 5   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00045
        if not( aop(bs,418,6) == suma(bs,419,425,6) ):
            lzbir =  aop(bs,418,6) 
            dzbir =  suma(bs,419,425,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0418 kol. 6 = AOP-u (0419 + 0420 + 0421 + 0422 + 0423 + 0424 + 0425) kol. 6   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00046
        if not( aop(bs,418,7) == suma(bs,419,425,7) ):
            lzbir =  aop(bs,418,7) 
            dzbir =  suma(bs,419,425,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0418 kol. 7 = AOP-u (0419 + 0420 + 0421 + 0422 + 0423 + 0424 + 0425) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00047
        if( suma_liste(bs,[411,416,417,418],5) > aop(bs,24,5) ):
            if not( aop(bs,426,5) == suma_liste(bs,[411,416,417,418],5)-aop(bs,24,5) ):
                lzbir =  aop(bs,426,5) 
                dzbir =  suma_liste(bs,[411,416,417,418],5)-aop(bs,24,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0426 kol. 5 = AOP-u (0411 + 0416 + 0417 + 0418 - 0024) kol. 5, ako je AOP (0411 + 0416 + 0417 + 0418) kol. 5  > AOP-a 0024 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00048
        if( suma_liste(bs,[411,416,417,418],6) > aop(bs,24,6) ):
            if not( aop(bs,426,6) == suma_liste(bs,[411,416,417,418],6)-aop(bs,24,6) ):
                lzbir =  aop(bs,426,6) 
                dzbir =  suma_liste(bs,[411,416,417,418],6)-aop(bs,24,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0426 kol. 6 = AOP-u (0411 + 0416 + 0417 + 0418 - 0024) kol. 6, ako je AOP (0411 + 0416 + 0417 + 0418) kol. 6  > AOP-a 0024 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00049
        if( suma_liste(bs,[411,416,417,418],7) > aop(bs,24,7) ):
            if not( aop(bs,426,7) == suma_liste(bs,[411,416,417,418],7)-aop(bs,24,7) ):
                lzbir =  aop(bs,426,7) 
                dzbir =  suma_liste(bs,[411,416,417,418],7)-aop(bs,24,7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0426 kol. 7 = AOP-u (0411 + 0416 + 0417 + 0418 - 0024) kol. 7, ako je AOP (0411 + 0416 + 0417 + 0418) kol. 7 > AOP-a 0024 kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00050
        if( suma_liste(bs,[404,408],5) > suma_liste(bs,[402,403,405],5) ):
            if not( aop(bs,426,5) == suma_liste(bs,[404,408],5)-suma_liste(bs,[402,403,405],5) ):
                lzbir =  aop(bs,426,5) 
                dzbir =  suma_liste(bs,[404,408],5)-suma_liste(bs,[402,403,405],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0426 kol. 5 = AOP-u (0404 + 0408 - 0402 - 0403 - 0405) kol. 5, ako je AOP (0404 + 0408) kol. 5  > AOP-u (0402 + 0403 + 0405) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00051
        if( suma_liste(bs,[404,408],6) > suma_liste(bs,[402,403,405],6) ):
            if not( aop(bs,426,6) == suma_liste(bs,[404,408],6)-suma_liste(bs,[402,403,405],6) ):
                lzbir =  aop(bs,426,6) 
                dzbir =  suma_liste(bs,[404,408],6)-suma_liste(bs,[402,403,405],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0426 kol. 6 = AOP-u (0404 + 0408 - 0402 - 0403 - 0405) kol. 6, ako je AOP (0404 + 0408) kol. 6  > AOP-u (0402 + 0403 + 0405) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00052
        if( suma_liste(bs,[404,408],7) > suma_liste(bs,[402,403,405],7) ):
            if not( aop(bs,426,7) == suma_liste(bs,[404,408],7)-suma_liste(bs,[402,403,405],7) ):
                lzbir =  aop(bs,426,7) 
                dzbir =  suma_liste(bs,[404,408],7)-suma_liste(bs,[402,403,405],7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0426 kol. 7 = AOP-u (0404 + 0408 - 0402 - 0403 - 0405) kol. 7, ako je AOP (0404 + 0408) kol. 7  > AOP-u (0402 + 0403 + 0405) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00053
        if( suma_liste(bs,[402,403,405],5) == suma_liste(bs,[404,408],5) ):
            if not( suma_liste(bs,[401,426],5) == 0 ):
                lzbir =  suma_liste(bs,[401,426],5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0426) kol. 5 = 0, ako je AOP (0402 + 0403 + 0405) kol. 5 = AOP-u (0404 + 0408) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00054
        if( suma_liste(bs,[402,403,405],6) == suma_liste(bs,[404,408],6) ):
            if not( suma_liste(bs,[401,426],6) == 0 ):
                lzbir =  suma_liste(bs,[401,426],6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0426) kol. 6 = 0, ako je AOP (0402 + 0403 + 0405) kol. 6 = AOP-u (0404 + 0408) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00055
        if( suma_liste(bs,[402,403,405],7) == suma_liste(bs,[404,408],7) ):
            if not( suma_liste(bs,[401,426],7) == 0 ):
                lzbir =  suma_liste(bs,[401,426],7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0426) kol. 7 = 0, ako je AOP (0402 + 0403 + 0405) kol. 7 = AOP-u (0404 + 0408) kol. 7 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00056
        if( aop(bs,24,5) == suma_liste(bs,[411,416,417,418],5) ):
            if not( suma_liste(bs,[401,426],5) == 0 ):
                lzbir =  suma_liste(bs,[401,426],5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0426) kol. 5 = 0, ako je AOP 0024 kol. 5 = AOP-u (0411 + 0416 + 0417 + 0418 ) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00057
        if( aop(bs,24,6) == suma_liste(bs,[411,416,417,418],6) ):
            if not( suma_liste(bs,[401,426],6) == 0 ):
                lzbir =  suma_liste(bs,[401,426],6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0426) kol. 6 = 0, ako je AOP 0024 kol. 6 = AOP-u (0411 + 0416 + 0417 + 0418 ) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00058
        if( aop(bs,24,7) == suma_liste(bs,[411,416,417,418],7) ):
            if not( suma_liste(bs,[401,426],7) == 0 ):
                lzbir =  suma_liste(bs,[401,426],7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0426) kol. 7 = 0, ako je AOP 0024 kol. 7 = AOP-u (0411 + 0416 + 0417 + 0418 ) kol. 7 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00059
        if( aop(bs,401,5) > 0 ):
            if not( aop(bs,426,5) == 0 ):
                lzbir =  aop(bs,426,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0401 kol. 5 > 0 onda je AOP 0426 kol. 5 = 0 Ne mogu biti istovremeno prikazani ulozi i višak rashoda nad prihodima iznad visine uloga '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00060
        if( aop(bs,426,5) > 0 ):
            if not( aop(bs,401,5) == 0 ):
                lzbir =  aop(bs,401,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0426 kol. 5 > 0, onda je AOP 0401 kol. 5 = 0 Ne mogu biti istovremeno prikazani ulozi i višak rashoda nad prihodima iznad visine uloga '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00061
        if( aop(bs,401,6) > 0 ):
            if not( aop(bs,426,6) == 0 ):
                lzbir =  aop(bs,426,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0401 kol. 6 > 0 onda je AOP 0426 kol. 6 = 0 Ne mogu biti istovremeno prikazani ulozi i višak rashoda nad prihodima iznad visine uloga '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00062
        if( aop(bs,426,6) > 0 ):
            if not( aop(bs,401,6) == 0 ):
                lzbir =  aop(bs,401,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0426 kol. 6 > 0, onda je AOP 0401 kol. 6 = 0 Ne mogu biti istovremeno prikazani ulozi i višak rashoda nad prihodima iznad visine uloga '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00063
        if( aop(bs,401,7) > 0 ):
            if not( aop(bs,426,7) == 0 ):
                lzbir =  aop(bs,426,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0401 kol. 7 > 0 onda je AOP 0426 kol. 7 = 0 Ne mogu biti istovremeno prikazani ulozi i višak rashoda nad prihodima iznad visine uloga '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00064
        if( aop(bs,426,7) > 0 ):
            if not( aop(bs,401,7) == 0 ):
                lzbir =  aop(bs,401,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0426 kol. 7 > 0, onda je AOP 0401 kol. 7 = 0 Ne mogu biti istovremeno prikazani ulozi i višak rashoda nad prihodima iznad visine uloga '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00065
        if not( aop(bs,427,5) == suma_liste(bs,[401,411,416,417,418],5)-aop(bs,426,5) ):
            lzbir =  aop(bs,427,5) 
            dzbir =  suma_liste(bs,[401,411,416,417,418],5)-aop(bs,426,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0427 kol. 5 = AOP-u (0401 + 0411 + 0416+ 0417 + 0418 - 0426) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00066
        if not( aop(bs,427,6) == suma_liste(bs,[401,411,416,417,418],6)-aop(bs,426,6) ):
            lzbir =  aop(bs,427,6) 
            dzbir =  suma_liste(bs,[401,411,416,417,418],6)-aop(bs,426,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0427 kol. 6 = AOP-u (0401 + 0411 + 0416+ 0417 + 0418 - 0426) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00067
        if not( aop(bs,427,7) == suma_liste(bs,[401,411,416,417,418],7)-aop(bs,426,7) ):
            lzbir =  aop(bs,427,7) 
            dzbir =  suma_liste(bs,[401,411,416,417,418],7)-aop(bs,426,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0427 kol. 7 = AOP-u (0401 + 0411 + 0416+ 0417 + 0418 - 0426) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00068
        if not( aop(bs,24,5) == aop(bs,427,5) ):
            lzbir =  aop(bs,24,5) 
            dzbir =  aop(bs,427,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0024 kol. 5 = AOP-u 0427 kol. 5 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00069
        if not( aop(bs,24,6) == aop(bs,427,6) ):
            lzbir =  aop(bs,24,6) 
            dzbir =  aop(bs,427,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0024 kol. 6 = AOP-u 0427 kol. 6 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00070
        if not( aop(bs,24,7) == aop(bs,427,7) ):
            lzbir =  aop(bs,24,7) 
            dzbir =  aop(bs,427,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0024 kol. 7 = AOP-u 0427 kol. 7 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00071
        if not( aop(bs,25,5) == aop(bs,428,5) ):
            lzbir =  aop(bs,25,5) 
            dzbir =  aop(bs,428,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0025 kol. 5 = AOP-u 0428 kol. 5 Kontrolno pravilo zahteva slaganje vanbilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00072
        if not( aop(bs,25,6) == aop(bs,428,6) ):
            lzbir =  aop(bs,25,6) 
            dzbir =  aop(bs,428,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0025 kol. 6 = AOP-u 0428 kol. 6 Kontrolno pravilo zahteva slaganje vanbilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00073
        if not( aop(bs,25,7) == aop(bs,428,7) ):
            lzbir =  aop(bs,25,7) 
            dzbir =  aop(bs,428,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0025 kol. 7 = AOP-u 0428 kol. 7 Kontrolno pravilo zahteva slaganje vanbilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00074
        #Za ovaj set se ne primenjuje pravilo 
        
        #00075
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if( suma(bu,1001,1048,5) > 0 ):
                if not( suma(bs,1,3,5)+suma(bs,9,14,5)+suma(bs,19,25,5)+suma(bs,401,405,5)+aop(bs,408,5)+suma(bs,411,413,5)+suma(bs,416,428,5) != suma(bs,1,3,6)+suma(bs,9,14,6)+suma(bs,19,25,6)+suma(bs,401,405,6)+aop(bs,408,6)+suma(bs,411,413,6)+suma(bs,416,428,6) ):
                    
                    naziv_obrasca='Bilans uspeha'
                    poruka  ='***Ako je zbir podataka na oznakama za AOP (1001 do 1048) kol. 5 > 0 onda zbir podataka na oznakama za AOP (0001 do 0003) kol. 5 + (0009 do 0014) kol. 5 + (0019 do 0025) kol. 5 + (0401 do 0405) kol. 5 + 0408 kol. 5 + (0411 do 0413) kol. 5 + (0416 do 0428) kol. 5  ≠ zbiru podataka na oznakama za AOP (0001 do 0003) kol. 6 + (0009 do 0014) kol. 6 + (0019 do 0025) kol. 6 + (0401 do 0405) kol. 6 + 0408 kol. 6 + (0411 do 0413) kol. 6 + (0416 do 0428) kol. 6  Zbirovi podataka u kolonama 5 i 6 bilansa stanja su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama;  '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ='***Ako je zbir podataka na oznakama za AOP (1001 do 1048) kol. 5 > 0 onda zbir podataka na oznakama za AOP (0001 do 0003) kol. 5 + (0009 do 0014) kol. 5 + (0019 do 0025) kol. 5 + (0401 do 0405) kol. 5 + 0408 kol. 5 + (0411 do 0413) kol. 5 + (0416 do 0428) kol. 5  ≠ zbiru podataka na oznakama za AOP (0001 do 0003) kol. 6 + (0009 do 0014) kol. 6 + (0019 do 0025) kol. 6 + (0401 do 0405) kol. 6 + 0408 kol. 6 + (0411 do 0413) kol. 6 + (0416 do 0428) kol. 6  Zbirovi podataka u kolonama 5 i 6 bilansa stanja su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama;  '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
        
        #BILANS USPEHA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #10001
        if not( suma(bu,1001,1048,5) > 0 ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP (1001 do 1048) kol. 5 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #10002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bu,1001,1048,6) == 0 ):
                lzbir =  suma(bu,1001,1048,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Zbir podataka na oznakama za AOP (1001 do 1048) kol. 6 = 0 Bilans uspeha za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bu,1001,1048,6) > 0 ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Zbir podataka na oznakama za AOP (1001 do 1048) kol. 6 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10004
        if not( aop(bu,1001,5) == suma_liste(bu,[1002,1003,1004,1005,1006,1007,1009],5)-aop(bu,1008,5) ):
            lzbir =  aop(bu,1001,5) 
            dzbir =  suma_liste(bu,[1002,1003,1004,1005,1006,1007,1009],5)-aop(bu,1008,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1001 kol. 5 = AOP-u (1002 + 1003 + 1004 + 1005 + 1006 + 1007 - 1008 + 1009) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10005
        if not( aop(bu,1001,6) == suma_liste(bu,[1002,1003,1004,1005,1006,1007,1009],6)-aop(bu,1008,6) ):
            lzbir =  aop(bu,1001,6) 
            dzbir =  suma_liste(bu,[1002,1003,1004,1005,1006,1007,1009],6)-aop(bu,1008,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1001 kol. 6 = AOP-u (1002 + 1003 + 1004 + 1005 + 1006 + 1007 - 1008 + 1009) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10006
        if not( aop(bu,1010,5) == suma(bu,1011,1018,5) ):
            lzbir =  aop(bu,1010,5) 
            dzbir =  suma(bu,1011,1018,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1010 kol. 5 = AOP-u (1011 + 1012 + 1013 + 1014 + 1015 + 1016 + 1017 + 1018) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10007
        if not( aop(bu,1010,6) == suma(bu,1011,1018,6) ):
            lzbir =  aop(bu,1010,6) 
            dzbir =  suma(bu,1011,1018,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1010 kol. 6 = AOP-u (1011 + 1012 + 1013 + 1014 + 1015 + 1016 + 1017 + 1018) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10008
        if( aop(bu,1019,5) == aop(bu,1001,5)-aop(bu,1010,5) ):
            if not( aop(bu,1001,5) > aop(bu,1010,5) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1019 kol. 5 = AOP-u (1001 - 1010) kol. 5, ako je AOP 1001 kol. 5 > AOP-a 1010 kol. 5  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10009
        if( aop(bu,1001,6) > aop(bu,1010,6) ):
            if not( aop(bu,1019,6) == aop(bu,1001,6)-aop(bu,1010,6) ):
                lzbir =  aop(bu,1019,6) 
                dzbir =  aop(bu,1001,6)-aop(bu,1010,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1019 kol. 6 = AOP-u (1001 - 1010) kol. 6, ako je AOP 1001 kol. 6  > AOP-a 1010 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10010
        if( aop(bu,1001,5) < aop(bu,1010,5) ):
            if not( aop(bu,1020,5) == aop(bu,1010,5)-aop(bu,1001,5) ):
                lzbir =  aop(bu,1020,5) 
                dzbir =  aop(bu,1010,5)-aop(bu,1001,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1020 kol. 5 = AOP-u (1010 - 1001) kol. 5, ako je AOP 1001 kol. 5 < AOP-a 1010 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10011
        if( aop(bu,1001,6) < aop(bu,1010,6) ):
            if not( aop(bu,1020,6) == aop(bu,1010,6)-aop(bu,1001,6) ):
                lzbir =  aop(bu,1020,6) 
                dzbir =  aop(bu,1010,6)-aop(bu,1001,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1020 kol. 6 = AOP-u (1010 - 1001) kol. 6, ako je AOP 1001 kol. 6 < AOP-a 1010 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10012
        if( aop(bu,1001,5) == aop(bu,1010,5) ):
            if not( suma(bu,1019,1020,5) == 0 ):
                lzbir =  suma(bu,1019,1020,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1019 + 1020) kol. 5 = 0, ako je AOP 1001 kol. 5 = AOP-u 1010 kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10013
        if( aop(bu,1001,6) == aop(bu,1010,6) ):
            if not( suma(bu,1019,1020,6) == 0 ):
                lzbir =  suma(bu,1019,1020,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1019 + 1020) kol. 6 = 0, ako je AOP 1001 kol. 6 = AOP-u 1010 kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10014
        if( aop(bu,1019,5) > 0 ):
            if not( aop(bu,1020,5) == 0 ):
                lzbir =  aop(bu,1020,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1019 kol. 5 > 0 onda je AOP 1020 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10015
        if( aop(bu,1020,5) > 0 ):
            if not( aop(bu,1019,5) == 0 ):
                lzbir =  aop(bu,1019,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1020 kol. 5 > 0 onda je AOP 1019 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10016
        if( aop(bu,1019,6) > 0 ):
            if not( aop(bu,1020,6) == 0 ):
                lzbir =  aop(bu,1020,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1019 kol. 6 > 0 onda je AOP 1020 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10017
        if( aop(bu,1020,6) > 0 ):
            if not( aop(bu,1019,6) == 0 ):
                lzbir =  aop(bu,1019,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1020 kol. 6 > 0 onda je AOP 1019 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10018
        if not( suma_liste(bu,[1002,1003,1004,1005,1006,1007,1009,1020],5) == suma_liste(bu,[1008,1011,1012,1013,1014,1015,1016,1017,1018,1019],5) ):
            lzbir =  suma_liste(bu,[1002,1003,1004,1005,1006,1007,1009,1020],5) 
            dzbir =  suma_liste(bu,[1008,1011,1012,1013,1014,1015,1016,1017,1018,1019],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1002 + 1003 + 1004 + 1005 + 1006 + 1007 + 1009 + 1020) kol. 5 = AOP-u (1008 + 1011 + 1012 + 1013 + 1014 + 1015 + 1016 + 1017 + 1018 + 1019) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10019
        if not( suma_liste(bu,[1002,1003,1004,1005,1006,1007,1009,1020],6) == suma_liste(bu,[1008,1011,1012,1013,1014,1015,1016,1017,1018,1019],6) ):
            lzbir =  suma_liste(bu,[1002,1003,1004,1005,1006,1007,1009,1020],6) 
            dzbir =  suma_liste(bu,[1008,1011,1012,1013,1014,1015,1016,1017,1018,1019],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1002 + 1003 + 1004 + 1005 + 1006 + 1007 + 1009 + 1020) kol. 6 = AOP-u (1008 + 1011 + 1012 + 1013 + 1014 + 1015 + 1016 + 1017 + 1018 + 1019) kol. 6  Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10020
        if not( aop(bu,1021,5) == suma(bu,1022,1026,5) ):
            lzbir =  aop(bu,1021,5) 
            dzbir =  suma(bu,1022,1026,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1021 kol. 5 = AOP-u (1022 + 1023 + 1024 + 1025 + 1026) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10021
        if not( aop(bu,1021,6) == suma(bu,1022,1026,6) ):
            lzbir =  aop(bu,1021,6) 
            dzbir =  suma(bu,1022,1026,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1021 kol. 6 = AOP-u (1022 + 1023 + 1024 + 1025 + 1026) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10022
        if not( aop(bu,1027,5) == suma(bu,1028,1031,5) ):
            lzbir =  aop(bu,1027,5) 
            dzbir =  suma(bu,1028,1031,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1027 kol. 5 = AOP-u (1028 + 1029 + 1030 + 1031) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10023
        if not( aop(bu,1027,6) == suma(bu,1028,1031,6) ):
            lzbir =  aop(bu,1027,6) 
            dzbir =  suma(bu,1028,1031,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1027 kol. 6 = AOP-u (1028 + 1029 + 1030 + 1031) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10024
        if( aop(bu,1021,5) > aop(bu,1027,5) ):
            if not( aop(bu,1032,5) == aop(bu,1021,5)-aop(bu,1027,5) ):
                lzbir =  aop(bu,1032,5) 
                dzbir =  aop(bu,1021,5)-aop(bu,1027,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1032 kol. 5 = AOP-u (1021 - 1027) kol. 5, ako je AOP 1021 kol. 5 > AOP-a 1027 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10025
        if( aop(bu,1021,6) > aop(bu,1027,6) ):
            if not( aop(bu,1032,6) == aop(bu,1021,6)-aop(bu,1027,6) ):
                lzbir =  aop(bu,1032,6) 
                dzbir =  aop(bu,1021,6)-aop(bu,1027,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1032 kol. 6 = AOP-u (1021 - 1027) kol. 6, ako je AOP 1021 kol. 6 > AOP-a 1027 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10026
        if( aop(bu,1021,5) < aop(bu,1027,5) ):
            if not( aop(bu,1033,5) == aop(bu,1027,5)-aop(bu,1021,5) ):
                lzbir =  aop(bu,1033,5) 
                dzbir =  aop(bu,1027,5)-aop(bu,1021,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1033 kol. 5 = AOP-u (1027 - 1021) kol. 5, ako je AOP 1021 kol. 5 < AOP-a 1027 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10027
        if( aop(bu,1021,6) < aop(bu,1027,6) ):
            if not( aop(bu,1033,6) == aop(bu,1027,6)-aop(bu,1021,6) ):
                lzbir =  aop(bu,1033,6) 
                dzbir =  aop(bu,1027,6)-aop(bu,1021,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1033 kol. 6 = AOP-u (1027 - 1021) kol. 6, ako je AOP 1021 kol. 6 < AOP-a 1027 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10028
        if( aop(bu,1021,5) == aop(bu,1027,5) ):
            if not( suma(bu,1032,1033,5) == 0 ):
                lzbir =  suma(bu,1032,1033,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1032 + 1033) kol. 5 = 0, ako je AOP 1021 kol. 5 = AOP-u 1027 kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10029
        if( aop(bu,1021,6) == aop(bu,1027,6) ):
            if not( suma(bu,1032,1033,6) == 0 ):
                lzbir =  suma(bu,1032,1033,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1032 + 1033) kol. 6 = 0, ako je AOP 1021 kol. 6 = AOP-u 1027 kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10030
        if( aop(bu,1032,5) > 0 ):
            if not( aop(bu,1033,5) == 0 ):
                lzbir =  aop(bu,1033,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1032 kol. 5 > 0 onda je AOP 1033 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10031
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
        
        #10032
        if( aop(bu,1032,6) > 0 ):
            if not( aop(bu,1033,6) == 0 ):
                lzbir =  aop(bu,1033,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1032 kol. 6 > 0 onda je AOP 1033 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10033
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
        
        #10034
        if not( suma_liste(bu,[1021,1033],5) == suma_liste(bu,[1027,1032],5) ):
            lzbir =  suma_liste(bu,[1021,1033],5) 
            dzbir =  suma_liste(bu,[1027,1032],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1021 + 1033) kol. 5 = AOP-u (1027 + 1032) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10035
        if not( suma_liste(bu,[1021,1033],6) == suma_liste(bu,[1027,1032],6) ):
            lzbir =  suma_liste(bu,[1021,1033],6) 
            dzbir =  suma_liste(bu,[1027,1032],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1021 + 1033) kol. 6 = AOP-u (1027 + 1032) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10036
        if not( aop(bu,1038,5) == suma_liste(bu,[1001,1021,1034,1036],5) ):
            lzbir =  aop(bu,1038,5) 
            dzbir =  suma_liste(bu,[1001,1021,1034,1036],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1038 kol. 5 = AOP-u (1001 + 1021 + 1034 + 1036) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10037
        if not( aop(bu,1038,6) == suma_liste(bu,[1001,1021,1034,1036],6) ):
            lzbir =  aop(bu,1038,6) 
            dzbir =  suma_liste(bu,[1001,1021,1034,1036],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1038 kol. 6 = AOP-u (1001 + 1021 + 1034 + 1036) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10038
        if not( aop(bu,1039,5) == suma_liste(bu,[1010,1027,1035,1037],5) ):
            lzbir =  aop(bu,1039,5) 
            dzbir =  suma_liste(bu,[1010,1027,1035,1037],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1039 kol. 5 = AOP-u (1010 + 1027 + 1035 + 1037) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10039
        if not( aop(bu,1039,6) == suma_liste(bu,[1010,1027,1035,1037],6) ):
            lzbir =  aop(bu,1039,6) 
            dzbir =  suma_liste(bu,[1010,1027,1035,1037],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1039 kol. 6 = AOP-u (1010 + 1027 + 1035 + 1037) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10040
        if( aop(bu,1038,5) > aop(bu,1039,5) ):
            if not( aop(bu,1040,5) == aop(bu,1038,5)-aop(bu,1039,5) ):
                lzbir =  aop(bu,1040,5) 
                dzbir =  aop(bu,1038,5)-aop(bu,1039,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1040 kol. 5 = AOP-u (1038 - 1039) kol. 5, ako je AOP 1038 kol. 5 >  AOP-a 1039 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10041
        if( aop(bu,1038,6) > aop(bu,1039,6) ):
            if not( aop(bu,1040,6) == aop(bu,1038,6)-aop(bu,1039,6) ):
                lzbir =  aop(bu,1040,6) 
                dzbir =  aop(bu,1038,6)-aop(bu,1039,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1040 kol. 6 = AOP-u (1038 - 1039) kol. 6, ako je AOP 1038 kol. 6 > AOP-a 1039 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10042
        if( aop(bu,1039,5) > aop(bu,1038,5) ):
            if not( aop(bu,1041,5) == aop(bu,1039,5)-aop(bu,1038,5) ):
                lzbir =  aop(bu,1041,5) 
                dzbir =  aop(bu,1039,5)-aop(bu,1038,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1041 kol. 5 = AOP-u (1039 - 1038) kol. 5, ako je AOP 1039 kol. 5 > AOP-a 1038 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10043
        if( aop(bu,1039,6) > aop(bu,1038,6) ):
            if not( aop(bu,1041,6) == aop(bu,1039,6)-aop(bu,1038,6) ):
                lzbir =  aop(bu,1041,6) 
                dzbir =  aop(bu,1039,6)-aop(bu,1038,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1041 kol. 6 = AOP-u (1039 - 1038) kol. 6, ako je AOP 1039 kol. 6 > AOP-a 1038 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10044
        if( aop(bu,1038,5) == aop(bu,1039,5) ):
            if not( suma(bu,1040,1041,5) == 0 ):
                lzbir =  suma(bu,1040,1041,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1040 + 1041) kol. 5 = 0, ako je AOP 1038 kol. 5 = AOP-u 1039 kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10045
        if( aop(bu,1038,6) == aop(bu,1039,6) ):
            if not( suma(bu,1040,1041,6) == 0 ):
                lzbir =  suma(bu,1040,1041,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1040 + 1041) kol. 6 = 0, ako je AOP 1038 kol. 6 = AOP-u 1039 kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10046
        if( aop(bu,1040,5) > 0 ):
            if not( aop(bu,1041,5) == 0 ):
                lzbir =  aop(bu,1041,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1040 kol. 5 > 0 onda je AOP 1041 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani višak prihoda nad rashodima i višak rashoda nad prihodima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10047
        if( aop(bu,1041,5) > 0 ):
            if not( aop(bu,1040,5) == 0 ):
                lzbir =  aop(bu,1040,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1041 kol. 5 > 0 onda je AOP 1040 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani višak prihoda nad rashodima i višak rashoda nad prihodima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10048
        if( aop(bu,1040,6) > 0 ):
            if not( aop(bu,1041,6) == 0 ):
                lzbir =  aop(bu,1041,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1040 kol. 6 > 0 onda je AOP 1041 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani višak prihoda nad rashodima i višak rashoda nad prihodima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10049
        if( aop(bu,1041,6) > 0 ):
            if not( aop(bu,1040,6) == 0 ):
                lzbir =  aop(bu,1040,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1041 kol. 6 > 0 onda je AOP 1040 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani višak prihoda nad rashodima i višak rashoda nad prihodima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10050
        if not( suma_liste(bu,[1038,1041],5) == suma(bu,1039,1040,5) ):
            lzbir =  suma_liste(bu,[1038,1041],5) 
            dzbir =  suma(bu,1039,1040,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1038 + 1041) kol. 5 = AOP-u (1039 + 1040) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10051
        if not( suma_liste(bu,[1038,1041],6) == suma(bu,1039,1040,6) ):
            lzbir =  suma_liste(bu,[1038,1041],6) 
            dzbir =  suma(bu,1039,1040,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1038 + 1041) kol. 6 = AOP-u (1039 + 1040) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10052
        if( aop(bu,1042,5) > 0 ):
            if not( aop(bu,1043,5) == 0 ):
                lzbir =  aop(bu,1043,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1042 kol. 5 > 0 onda je AOP 1043 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani višak prihoda nad rashodima i višak rashoda nad prihodima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10053
        if( aop(bu,1043,5) > 0 ):
            if not( aop(bu,1042,5) == 0 ):
                lzbir =  aop(bu,1042,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1043 kol. 5 > 0 onda je AOP 1042 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani višak prihoda nad rashodima i višak rashoda nad prihodima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10054
        if( aop(bu,1042,6) > 0 ):
            if not( aop(bu,1043,6) == 0 ):
                lzbir =  aop(bu,1043,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1042 kol. 6 > 0 onda je AOP 1043 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani višak prihoda nad rashodima i višak rashoda nad prihodima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10055
        if( aop(bu,1043,6) > 0 ):
            if not( aop(bu,1042,6) == 0 ):
                lzbir =  aop(bu,1042,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1043 kol. 6 > 0 onda je AOP 1042 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani višak prihoda nad rashodima i višak rashoda nad prihodima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10056
        if( suma_liste(bu,[1040,1042],5) > suma_liste(bu,[1041,1043],5) ):
            if not( aop(bu,1044,5) == suma_liste(bu,[1040,1042],5)-suma_liste(bu,[1041,1043],5) ):
                lzbir =  aop(bu,1044,5) 
                dzbir =  suma_liste(bu,[1040,1042],5)-suma_liste(bu,[1041,1043],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1044 kol. 5 = AOP-u (1040 - 1041 + 1042 - 1043) kol. 5, ako je AOP (1040 + 1042) kol. 5 > AOP-a (1041 + 1043) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10057
        if( suma_liste(bu,[1040,1042],6) > suma_liste(bu,[1041,1043],6) ):
            if not( aop(bu,1044,6) == suma_liste(bu,[1040,1042],6)-suma_liste(bu,[1041,1043],6) ):
                lzbir =  aop(bu,1044,6) 
                dzbir =  suma_liste(bu,[1040,1042],6)-suma_liste(bu,[1041,1043],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1044 kol. 6 = AOP-u (1040 - 1041 + 1042 - 1043) kol. 6, ako je AOP (1040 + 1042) kol. 6 > AOP-a (1041 + 1043) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10058
        if( suma_liste(bu,[1040,1042],5) < suma_liste(bu,[1041,1043],5) ):
            if not( aop(bu,1045,5) == suma_liste(bu,[1041,1043],5)-suma_liste(bu,[1040,1042],5) ):
                lzbir =  aop(bu,1045,5) 
                dzbir =  suma_liste(bu,[1041,1043],5)-suma_liste(bu,[1040,1042],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1045 kol. 5 = AOP-u (1041 - 1040 + 1043 - 1042) kol. 5, ako je AOP (1040 + 1042) kol. 5 < AOP-a (1041 + 1043) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10059
        if( suma_liste(bu,[1040,1042],6) < suma_liste(bu,[1041,1043],6) ):
            if not( aop(bu,1045,6) == suma_liste(bu,[1041,1043],6)-suma_liste(bu,[1040,1042],6) ):
                lzbir =  aop(bu,1045,6) 
                dzbir =  suma_liste(bu,[1041,1043],6)-suma_liste(bu,[1040,1042],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1045 kol. 6 = AOP-u (1041 - 1040 + 1043 - 1042) kol. 6, ako je AOP (1040 + 1042) kol. 6 < AOP-a (1041 + 1043) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10060
        if( suma_liste(bu,[1040,1042],5) == suma_liste(bu,[1041,1043],5) ):
            if not( suma(bu,1044,1045,5) == 0 ):
                lzbir =  suma(bu,1044,1045,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1044 + 1045) kol. 5 = 0, ako je AOP (1040 + 1042) kol. 5 = AOP-u (1041 + 1043) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10061
        if( suma_liste(bu,[1040,1042],6) == suma_liste(bu,[1041,1043],6) ):
            if not( suma(bu,1044,1045,6) == 0 ):
                lzbir =  suma(bu,1044,1045,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1044 + 1045) kol. 6 = 0, ako je AOP (1040 + 1042) kol. 6 = AOP-u (1041 + 1043) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10062
        if( aop(bu,1044,5) > 0 ):
            if not( aop(bu,1045,5) == 0 ):
                lzbir =  aop(bu,1045,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1044 kol. 5 > 0 onda je AOP 1045 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani višak prihoda nad rashodima i višak rashoda nad prihodima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10063
        if( aop(bu,1045,5) > 0 ):
            if not( aop(bu,1044,5) == 0 ):
                lzbir =  aop(bu,1044,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1045 kol. 5 > 0 onda je AOP 1044 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani višak prihoda nad rashodima i višak rashoda nad prihodima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10064
        if( aop(bu,1044,6) > 0 ):
            if not( aop(bu,1045,6) == 0 ):
                lzbir =  aop(bu,1045,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1044 kol. 6 > 0 onda je AOP 1045 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani višak prihoda nad rashodima i višak rashoda nad prihodima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10065
        if( aop(bu,1045,6) > 0 ):
            if not( aop(bu,1044,6) == 0 ):
                lzbir =  aop(bu,1044,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1045 kol. 6 > 0 onda je AOP 1044 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani višak prihoda nad rashodima i višak rashoda nad prihodima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10066
        if not( suma_liste(bu,[1001,1021,1034,1036,1042,1045],5) == suma_liste(bu,[1010,1027,1035,1037,1043,1044],5) ):
            lzbir =  suma_liste(bu,[1001,1021,1034,1036,1042,1045],5) 
            dzbir =  suma_liste(bu,[1010,1027,1035,1037,1043,1044],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1021 + 1034 + 1036 + 1042 + 1045) kol. 5 = AOP-u (1010 + 1027 + 1035 + 1037 + 1043 + 1044) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10067
        if not( suma_liste(bu,[1001,1021,1034,1036,1042,1045],6) == suma_liste(bu,[1010,1027,1035,1037,1043,1044],6) ):
            lzbir =  suma_liste(bu,[1001,1021,1034,1036,1042,1045],6) 
            dzbir =  suma_liste(bu,[1010,1027,1035,1037,1043,1044],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1021 + 1034 + 1036 + 1042 + 1045) kol. 6 = AOP-u (1010 + 1027 + 1035 + 1037 + 1043 + 1044) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10068
        if( aop(bu,1044,5) > suma(bu,1045,1046,5) ):
            if not( aop(bu,1047,5) == aop(bu,1044,5)-suma(bu,1045,1046,5) ):
                lzbir =  aop(bu,1047,5) 
                dzbir =  aop(bu,1044,5)-suma(bu,1045,1046,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1047 kol. 5 = AOP-u (1044 - 1045 - 1046) kol. 5, ako je AOP 1044 kol. 5 > AOP-a (1045 + 1046) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10069
        if( aop(bu,1044,6) > suma(bu,1045,1046,6) ):
            if not( aop(bu,1047,6) == aop(bu,1044,6)-suma(bu,1045,1046,6) ):
                lzbir =  aop(bu,1047,6) 
                dzbir =  aop(bu,1044,6)-suma(bu,1045,1046,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1047 kol. 6 = AOP-u (1044 - 1045 - 1046) kol. 6, ako je AOP 1044 kol. 6 > AOP-a (1045 + 1046) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10070
        if( aop(bu,1044,5) < suma(bu,1045,1046,5) ):
            if not( aop(bu,1048,5) == suma(bu,1045,1046,5)-aop(bu,1044,5) ):
                lzbir =  aop(bu,1048,5) 
                dzbir =  suma(bu,1045,1046,5)-aop(bu,1044,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1048 kol. 5 = AOP-u (1045 - 1044 + 1046) kol. 5, ako je AOP 1044 kol. 5 < AOP-a (1045 + 1046) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10071
        if( aop(bu,1044,6) < suma(bu,1045,1046,6) ):
            if not( aop(bu,1048,6) == suma(bu,1045,1046,6)-aop(bu,1044,6) ):
                lzbir =  aop(bu,1048,6) 
                dzbir =  suma(bu,1045,1046,6)-aop(bu,1044,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1048 kol. 6 = AOP-u (1045 - 1044 + 1046) kol. 6, ako je AOP 1044 kol. 6 < AOP-a (1045 + 1046) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10072
        if( aop(bu,1044,5) == suma(bu,1045,1046,5) ):
            if not( suma(bu,1047,1048,5) == 0 ):
                lzbir =  suma(bu,1047,1048,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1047 + 1048) kol. 5 = 0, ako je AOP 1044 kol. 5 = AOP-u (1045 + 1046) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10073
        if( aop(bu,1044,6) == suma(bu,1045,1046,6) ):
            if not( suma(bu,1047,1048,6) == 0 ):
                lzbir =  suma(bu,1047,1048,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1047 + 1048) kol. 6 = 0, ako je AOP 1044 kol. 6 = AOP-u (1045 + 1046) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10074
        if( aop(bu,1047,5) > 0 ):
            if not( aop(bu,1048,5) == 0 ):
                lzbir =  aop(bu,1048,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1047 kol. 5 > 0 onda je AOP 1048 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani višak prihoda nad rashodima i višak rashoda nad prihodima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10075
        if( aop(bu,1048,5) > 0 ):
            if not( aop(bu,1047,5) == 0 ):
                lzbir =  aop(bu,1047,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1048 kol. 5 > 0 onda je AOP 1047 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani višak prihoda nad rashodima i višak rashoda nad prihodima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10076
        if( aop(bu,1047,6) > 0 ):
            if not( aop(bu,1048,6) == 0 ):
                lzbir =  aop(bu,1048,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1047 kol. 6 > 0 onda je AOP 1048 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani višak prihoda nad rashodima i višak rashoda nad prihodima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10077
        if( aop(bu,1048,6) > 0 ):
            if not( aop(bu,1047,6) == 0 ):
                lzbir =  aop(bu,1047,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1048 kol. 6 > 0 onda je AOP 1047 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani višak prihoda nad rashodima i višak rashoda nad prihodima '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10078
        if not( suma_liste(bu,[1044,1048],5) == suma(bu,1045,1047,5) ):
            lzbir =  suma_liste(bu,[1044,1048],5) 
            dzbir =  suma(bu,1045,1047,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1044 + 1048) kol. 5 = AOP-u (1045 + 1046 + 1047) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10079
        if not( suma_liste(bu,[1044,1048],6) == suma(bu,1045,1047,6) ):
            lzbir =  suma_liste(bu,[1044,1048],6) 
            dzbir =  suma(bu,1045,1047,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1044 + 1048) kol. 6 = AOP-u (1045 + 1046 + 1047) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10080
        #Za ovaj set se ne primenjuje pravilo 
        
        #10081
        #Za ovaj set se ne primenjuje pravilo 
        
        #10082
        #Za ovaj set se ne primenjuje pravilo 
        
        #10083
        #Za ovaj set se ne primenjuje pravilo 
        
        #10084
        #Za ovaj set se ne primenjuje pravilo 
        
        #10085
        #Za ovaj set se ne primenjuje pravilo 
        
        #10086
        #Za ovaj set se ne primenjuje pravilo 
        
        #10087
        #Za ovaj set se ne primenjuje pravilo 
        
        #10088
        if( aop(bu,1047,5) > 0 ):
            if not( aop(bs,405,5) >= aop(bu,1047,5) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1047 kol. 5 > 0, onda je AOP 0405 kol. 5 bilansa stanja ≥ AOP-a 1047 kol. 5  Neto višak prihoda nad rashodima tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu viška prihoda nad rashodima u koloni tekuća godina u obrascu Bilans stanja; Ukoliko ti podaci nisu usaglašeni, zakonski zastupnik potpisivanjem izveštaja potvrđuje da je tako iskazan rezultat u Bilansu stanja ispravan i tačan, odnosno da je iskazan u skladu sa propisima '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1047 kol. 5 > 0, onda je AOP 0405 kol. 5 bilansa stanja ≥ AOP-a 1047 kol. 5  Neto višak prihoda nad rashodima tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu viška prihoda nad rashodima u koloni tekuća godina u obrascu Bilans stanja; Ukoliko ti podaci nisu usaglašeni, zakonski zastupnik potpisivanjem izveštaja potvrđuje da je tako iskazan rezultat u Bilansu stanja ispravan i tačan, odnosno da je iskazan u skladu sa propisima '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10089
        if( aop(bu,1047,6) > 0 ):
            if not( aop(bs,405,6) >= aop(bu,1047,6) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1047 kol. 6 > 0, onda je AOP 0405 kol. 6 bilansa stanja ≥ AOP-a 1047 kol. 6  Neto višak prihoda nad rashodima prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu viška prihoda nad rashodima u koloni prethodna godina u obrascu Bilans stanja.  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1047 kol. 6 > 0, onda je AOP 0405 kol. 6 bilansa stanja ≥ AOP-a 1047 kol. 6  Neto višak prihoda nad rashodima prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu viška prihoda nad rashodima u koloni prethodna godina u obrascu Bilans stanja.  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10090
        if( aop(bu,1048,5) > 0 ):
            if not( aop(bs,408,5) >= aop(bu,1048,5) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1048 kol. 5 > 0, onda je AOP 0408 kol. 5 bilansa stanja ≥ AOP-a 1048 kol. 5  Neto višak rashoda nad prihodima tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu viška rashoda nad prihodima tekuće godine u obrascu Bilans stanja; Ukoliko ti podaci nisu usaglašeni, zakonski zastupnik potpisivanjem izveštaja potvrđuje da je tako iskazan rezultat u Bilansu stanja ispravan i tačan, odnosno da je iskazan u skladu sa propisima '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1048 kol. 5 > 0, onda je AOP 0408 kol. 5 bilansa stanja ≥ AOP-a 1048 kol. 5  Neto višak rashoda nad prihodima tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu viška rashoda nad prihodima tekuće godine u obrascu Bilans stanja; Ukoliko ti podaci nisu usaglašeni, zakonski zastupnik potpisivanjem izveštaja potvrđuje da je tako iskazan rezultat u Bilansu stanja ispravan i tačan, odnosno da je iskazan u skladu sa propisima '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10091
        if( aop(bu,1048,6) > 0 ):
            if not( aop(bs,408,6) >= aop(bu,1048,6) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1048 kol. 6 > 0, onda je AOP 0408 kol. 6 bilansa stanja ≥ AOP-a 1048 kol. 6  Neto višak rashoda nad prihodima prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu viška rashoda nad prihodima u koloni prethodna godina u obrascu Bilans stanja. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1048 kol. 6 > 0, onda je AOP 0408 kol. 6 bilansa stanja ≥ AOP-a 1048 kol. 6  Neto višak rashoda nad prihodima prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu viška rashoda nad prihodima u koloni prethodna godina u obrascu Bilans stanja. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10092
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if( suma(bu,1001,1048,5) > 0 ):
                if not( suma(bu,1001,1048,5) != suma(bu,1001,1048,6) ):
                    
                    naziv_obrasca='Bilans uspeha'
                    poruka  ='***Ako je zbir podataka na oznakama za AOP (1001 do 1048) kol. 5 > 0 onda zbir podataka na oznakama za AOP (1001 do 1048) kol. 5 ≠ zbiru podataka na oznakama za AOP  (1001 do 1048) kol. 6 Zbirovi podataka u kolonama 5 i 6 bilansa uspeha su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama;  '
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

 
        
