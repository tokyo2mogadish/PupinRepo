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
        ostalo_warnings = []
        ostalo_errors = []
        exceptions=[]
        
        lzbir = 0
        dzbir = 0
        razlika = 0
                                                       
        #Provera da li su upisani podaci o prijemu
        #if ((Zahtev.NacinPodnosenja.value__ == 3 or (Zahtev.NacinPodnosenja.value__ == 2 and Zahtev.FiStanje.value__ > 0)) and (Zahtev.BrojRMarkice is None or len(Zahtev.BrojRMarkice) == 0)):           
        #    form_errors.append('U formi Podaci o prijemu, broj poštanske pošiljke nije upisan.') 

        #if ((Zahtev.NacinPodnosenja.value__ == 3 or (Zahtev.NacinPodnosenja.value__ == 2 and Zahtev.FiStanje.value__ > 0)) and (Zahtev.DatumPodnosenja < DateTime(2015,1,1,) or Zahtev.DatumPodnosenja >  DateTime.Now)):                       
        #    form_errors.append('U formi Podaci o prijemu, datum podnošenja ne sme biti manji od 01.01.2015. niti veći od tekućeg datuma.')

        
        #Provera da li lice odgovorno za sastavljanje je upisano
        if (Zahtev.LiceOdgovornoZaSastavljanje is None):
            ostalo_errors.append('Podaci za lice odgovorno za sastavljanje finansijskog izveštaja nisu upisani.')


       #Provera da li lice odgovorno za potpisivanje
        if (len(Zahtev.Potpisnici) == 0):
            ostalo_errors.append('Podaci o potpisniku finansijskog izveštaja nisu upisani.')
        

        #Provera da li je za papirne i hibridne bar jedan dokument barkodiran
        '''
        if (Zahtev.ValidacijaUlaznihDokumenataOmoguceno==True):
            if ((Zahtev.NacinPodnosenja.value__ == 3 or (Zahtev.NacinPodnosenja.value__ == 2 and Zahtev.FiStanje.value__ > 0))):
                if Zahtev.UlazniDokumenti.Count>0:
                    nDocWithBarCode = 0
                    for k in Zahtev.UlazniDokumenti.Keys:
                        if Zahtev.UlazniDokumenti[k].Barkod != None:
                            nDocWithBarCode += 1
                    if nDocWithBarCode == 0:
                        doc_errors.append('Morate dodati bar jedan ulazni dokument.')
        '''        
        
        #Provera da li su prosledjeni svi ulazni dokumenti
        if (Zahtev.ValidacijaUlaznihDokumenataOmoguceno==True):
            # if ((Zahtev.NacinPodnosenja.value__ == 1 or (Zahtev.NacinPodnosenja.value__ == 2 and Zahtev.FiStanje.value__ > 1) or (Zahtev.NacinPodnosenja.value__ == 3 and Zahtev.FiStanje.value__ > 0))):
            if Zahtev.UlazniDokumenti.Count>0:
                for k in Zahtev.UlazniDokumenti.Keys:
                    if Zahtev.UlazniDokumenti[k].Obavezan==True and Zahtev.UlazniDokumenti[k].Barkod == None:
                        doc_errors.append('Dokument sa nazivom "'+Zahtev.UlazniDokumenti[k].Naziv+'" niste priložili.')


        
        #Prilagoditi proveru postojanja forme u zavisnosti od tipa FI

        # if (Zahtev.NacinPodnosenja.value__ == 1 or Zahtev.NacinPodnosenja.value__ == 2 or (Zahtev.NacinPodnosenja.value__ == 3 and  Zahtev.FiStanje.value__ > 0)):
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

        si = getForme(Zahtev,'Statistički izveštaj')
        if len(si)==0:
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Statistički izveštaj nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        pp = getForme(Zahtev,'Posebni podaci')
        if len(pp)==0:
            
            naziv_obrasca='Posebni podaci'
            poruka  ='Obrazac "Posebni podaci" nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        if (len(form_errors)>0):
            return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}

        # if (Zahtev.NacinPodnosenja.value__ == 3 and  Zahtev.FiStanje.value__ == 0 ):
        #     return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}

        # if (Zahtev.NacinPodnosenja.value__ == 2 and  Zahtev.FiStanje.value__ > 0 and (len(doc_errors)>0 or len(form_errors)>0) ):
        #     return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}

        ######################################
        #### POCETAK KONTROLNIH PRAVILA ######
        ######################################
        
        #00000-1
        if not( suma(bs,1,25,5)+suma(bs,1,25,6)+suma(bs,1,25,7)+suma(bs,401,428,5)+suma(bs,401,428,6)+suma(bs,401,428,7)+suma(bu,1001,1048,5)+suma(bu,1001,1048,6)+suma_liste(si,[9007,9014,9015,9021,9022,9029,9030,9036],6)+suma(si,9037,9094,4)+suma(si,9037,9094,5)+suma(si,9095,9104,3)+suma(si,9095,9104,4) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0025) kol. 5 + (0001 do 0025) kol. 6 + (0001 do 0025) kol. 7 bilansa stanja + (0401 do 0428) kol. 5 + (0401 do 0428) kol. 6+ (0401 do 0428) kol. 7 bilansa stanja + (1001 do 1048) kol. 5 + (1001 do 1048) kol. 6 bilansa uspeha + (9007 + 9014 + 9015 + 9021 + 9022 + 9029 + 9030 + 9036) kol. 6 + (9037 do 9094) kol. 4 + (9037 do 9094) kol. 5 + (9095 do 9104) kol. 3 + (9095 do 9104) kol. 4  statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0025) kol. 5 + (0001 do 0025) kol. 6 + (0001 do 0025) kol. 7 bilansa stanja + (0401 do 0428) kol. 5 + (0401 do 0428) kol. 6+ (0401 do 0428) kol. 7 bilansa stanja + (1001 do 1048) kol. 5 + (1001 do 1048) kol. 6 bilansa uspeha + (9007 + 9014 + 9015 + 9021 + 9022 + 9029 + 9030 + 9036) kol. 6 + (9037 do 9094) kol. 4 + (9037 do 9094) kol. 5 + (9095 do 9104) kol. 3 + (9095 do 9104) kol. 4  statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0025) kol. 5 + (0001 do 0025) kol. 6 + (0001 do 0025) kol. 7 bilansa stanja + (0401 do 0428) kol. 5 + (0401 do 0428) kol. 6+ (0401 do 0428) kol. 7 bilansa stanja + (1001 do 1048) kol. 5 + (1001 do 1048) kol. 6 bilansa uspeha + (9007 + 9014 + 9015 + 9021 + 9022 + 9029 + 9030 + 9036) kol. 6 + (9037 do 9094) kol. 4 + (9037 do 9094) kol. 5 + (9095 do 9104) kol. 3 + (9095 do 9104) kol. 4  statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}

        #00000-2
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-3
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-4
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-5
        # U bar jednoj od dve navedene forme kolona napomena mora da ima bar jedan karakter
        bsNapomene = Zahtev.Forme['Bilans stanja'].TekstualnaPoljaForme;
        buNapomene = Zahtev.Forme['Bilans uspeha'].TekstualnaPoljaForme;

        if not(proveriNapomene(bsNapomene, 1, 25, 4) or proveriNapomene(bsNapomene, 401, 428, 4) or proveriNapomene(buNapomene, 1001, 1048, 4)): 
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Na AOP-u (0001 do 0025) bilansa stanja + (0401 do 0428) bilansa stanja + (1001 do 1048) bilansa uspeha u koloni 4 (Napomena broj) mora biti unet bar jedan karakter Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ='Na AOP-u (0001 do 0025) bilansa stanja + (0401 do 0428) bilansa stanja + (1001 do 1048) bilansa uspeha u koloni 4 (Napomena broj) mora biti unet bar jedan karakter Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #Provera da li je fizahtev placen
        if not(Zahtev.Placen):
            ostalo_errors.append('Naknada za obradu i javno objavljivanje izveštaja i propisane dokumentacije nije uplaćena u propisanom iznosu. Instrukcije za uplatu propisane naknade date su u okviru PIS FI sistema za konkretan zahtev, na linku „Status naplate zahteva / Instrukcija za plaćanje". Ukoliko ste izvršili uplatu, a naknada nije uparena, priložite Dokaz o uplati naknade u delu Dokumentacija (na mestu predviđenom za dokaz o uplati naknade), kako biste mogli da podnesete izveštaj.');

        # UPOZORENJE ZA SVE KOJI DOSTAVLJAJU SAMOSTALNI RGFI
        
        # naziv_obrasca='Posebni podaci'
        # poruka  ='VAŽNA NAPOMENA: Proverite da li ste podatak o broju zaposlenih koji ste iskazali u obrascu Posebni podaci usaglasili sa podatkom o broju zaposlenih koji ste iskazali u Izveštaju za statističke potrebe. Ukoliko se podaci razlikuju potrebno je dostaviti obrazloženje zbog čega je nastala razlika, u suprotnom biće poslato obaveštenje o nedostacima.'
        # aop_pozicije=[]
        # poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
        # form_warnings.append(poruka_obrasca)

        #Provera negativnih AOP-a
        lista=""
        lista_bs = find_negativni(bs, 1, 428, 5, 7)
        lista_bu = find_negativni(bu, 1001, 1048, 5, 6)
        lista_si = find_negativni(si, 9001, 9104, 3, 6)
       
        if (len(lista_bs) > 0):
            lista = lista_bs
        if len(lista_bu) > 0:
            if len(lista) > 0:
                lista = lista + ", " + lista_bu
            else:
                lista = lista_bu                           
        if len(lista_si) > 0:
            if len(lista) > 0:
                lista = lista + ", " + lista_si
            else:
                lista = lista_si
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
            naziv_obrasca='Statistički izveštaj'
            poruka  ="Unete vrednosti ne mogu biti negativne ! (" + lista + ")"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00000-6
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-7
        #Za ovaj set se ne primenjuje pravilo 
        
        #BILANS STANJA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #00001
        if not( suma(bs,1,25,5)+suma(bs,401,428,5) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0025) kol. 5 + (0401 do 0428) kol. 5 > 0 Bilans stanja, po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #00002
        #Za ovaj set se ne primenjuje pravilo 
        
        #00003
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,25,6)+suma(bs,401,428,6) == 0 ):
                lzbir =  suma(bs,1,25,6)+suma(bs,401,428,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0025) kol. 6 + (0401 do 0428) kol. 6 = 0 Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00004
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,25,7)+suma(bs,401,428,7) == 0 ):
                lzbir =  suma(bs,1,25,7)+suma(bs,401,428,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0025) kol. 7 + (0401 do 0428) kol. 7 = 0 Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00005
        #Za ovaj set se ne primenjuje pravilo 
        
        #00006
        #Za ovaj set se ne primenjuje pravilo 
        
        #00007
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,25,6)+suma(bs,401,428,6) > 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0025) kol. 6  + (0401 do 0428) kol. 6 > 0 Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #00008
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,25,7)+suma(bs,401,428,7) > 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0025) kol. 7 + (0401 do 0428) kol. 7  >   0 Bilans stanja, po pravilu,  mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #00009
        #Za ovaj set se ne primenjuje pravilo 
        
        #00010
        #Za ovaj set se ne primenjuje pravilo 
        
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
        if not( aop(bs,14,5) == suma(bs,15,18,5) ):
            lzbir =  aop(bs,14,5) 
            dzbir =  suma(bs,15,18,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0014 kol. 5 = AOP-u (0015 + 0016 + 0017 + 0018) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00021
        if not( aop(bs,14,6) == suma(bs,15,18,6) ):
            lzbir =  aop(bs,14,6) 
            dzbir =  suma(bs,15,18,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0014 kol. 6 = AOP-u (0015 + 0016 + 0017 + 0018) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00022
        if not( aop(bs,14,7) == suma(bs,15,18,7) ):
            lzbir =  aop(bs,14,7) 
            dzbir =  suma(bs,15,18,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0014 kol. 7 = AOP-u (0015 + 0016 + 0017 + 0018) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
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
        if not( aop(bs,405,5) == suma(bs,406,407,5) ):
            lzbir =  aop(bs,405,5) 
            dzbir =  suma(bs,406,407,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0405 kol. 5 = AOP-u (0406 + 0407) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00033
        if not( aop(bs,405,6) == suma(bs,406,407,6) ):
            lzbir =  aop(bs,405,6) 
            dzbir =  suma(bs,406,407,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0405 kol. 6 = AOP-u (0406 + 0407) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00034
        if not( aop(bs,405,7) == suma(bs,406,407,7) ):
            lzbir =  aop(bs,405,7) 
            dzbir =  suma(bs,406,407,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0405 kol. 7 = AOP-u (0406 + 0407) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00035
        if not( aop(bs,408,5) == suma(bs,409,410,5) ):
            lzbir =  aop(bs,408,5) 
            dzbir =  suma(bs,409,410,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0408 kol. 5 = AOP-u (0409 + 0410) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00036
        if not( aop(bs,408,6) == suma(bs,409,410,6) ):
            lzbir =  aop(bs,408,6) 
            dzbir =  suma(bs,409,410,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0408 kol. 6 = AOP-u (0409 + 0410) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00037
        if not( aop(bs,408,7) == suma(bs,409,410,7) ):
            lzbir =  aop(bs,408,7) 
            dzbir =  suma(bs,409,410,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0408 kol. 7 = AOP-u (0409 + 0410) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
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
        if not( aop(bs,413,5) == suma(bs,414,415,5) ):
            lzbir =  aop(bs,413,5) 
            dzbir =  suma(bs,414,415,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0413 kol. 5 = AOP-u (0414 + 0415) kol. 5   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00042
        if not( aop(bs,413,6) == suma(bs,414,415,6) ):
            lzbir =  aop(bs,413,6) 
            dzbir =  suma(bs,414,415,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0413 kol. 6 = AOP-u (0414 + 0415) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00043
        if not( aop(bs,413,7) == suma(bs,414,415,7) ):
            lzbir =  aop(bs,413,7) 
            dzbir =  suma(bs,414,415,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0413 kol. 7 = AOP-u (0414 + 0415) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
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
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if( suma(bu,1001,1048,5) > 0 ):
                if not( suma(bs,1,25,5)+suma(bs,401,428,5) != suma(bs,1,25,6)+suma(bs,401,428,6) ):
                    
                    naziv_obrasca='Bilans uspeha'
                    poruka  ='***Ako je zbir podataka na oznakama za AOP (1001 do 1048) kol. 5 > 0 onda zbir podataka na oznakama za AOP (0001 do 0025) kol. 5 + (0401 do 0428) kol. 5 ≠ zbiru podataka na oznakama za AOP (0001 do 0025) kol. 6 + (0401 do 0428) kol. 6 Zbirovi podataka u kolonama 5 i 6 bilansa stanja su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama;  '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ='***Ako je zbir podataka na oznakama za AOP (1001 do 1048) kol. 5 > 0 onda zbir podataka na oznakama za AOP (0001 do 0025) kol. 5 + (0401 do 0428) kol. 5 ≠ zbiru podataka na oznakama za AOP (0001 do 0025) kol. 6 + (0401 do 0428) kol. 6 Zbirovi podataka u kolonama 5 i 6 bilansa stanja su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama;  '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
        
        #00075
        #Za ovaj set se ne primenjuje pravilo 
        
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
        if( aop(bu,1001,5) > aop(bu,1010,5) ):
            if not( aop(bu,1019,5) == aop(bu,1001,5)-aop(bu,1010,5) ):
                lzbir =  aop(bu,1019,5) 
                dzbir =  aop(bu,1001,5)-aop(bu,1010,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1019 kol. 5 = AOP-u (1001 - 1010) kol. 5, ako je AOP 1001 kol. 5 > AOP-a 1010 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
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
        if( aop(bu,1047,5) > 0 ):
            if not( aop(bs,407,5) == aop(bu,1047,5) ):
                lzbir =  aop(bs,407,5) 
                dzbir =  aop(bu,1047,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1047 kol. 5 > 0, onda je AOP 0407 kol. 5 bilansa stanja = AOP-u 1047 kol. 5 Neto višak prihoda nad rashodima tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu viška prihoda nad rashodima tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1047 kol. 5 > 0, onda je AOP 0407 kol. 5 bilansa stanja = AOP-u 1047 kol. 5 Neto višak prihoda nad rashodima tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu viška prihoda nad rashodima tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10081
        if( aop(bu,1047,6) > 0 ):
            if not( aop(bs,407,6) == aop(bu,1047,6) ):
                lzbir =  aop(bs,407,6) 
                dzbir =  aop(bu,1047,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1047 kol. 6 > 0, onda je AOP 0407 kol. 6 bilansa stanja = AOP-u 1047 kol. 6 Neto višak prihoda nad rashodima prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu viška prihoda nad rashodima tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1047 kol. 6 > 0, onda je AOP 0407 kol. 6 bilansa stanja = AOP-u 1047 kol. 6 Neto višak prihoda nad rashodima prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu viška prihoda nad rashodima tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10082
        if( aop(bs,407,5) > 0 ):
            if not( aop(bu,1047,5) == aop(bs,407,5) ):
                lzbir =  aop(bu,1047,5) 
                dzbir =  aop(bs,407,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0407 kol. 5 bilansa stanja > 0 , onda je AOP 1047 kol. 5 = AOP 0407-u kol. 5 bilansa stanja  Neto višak prihoda nad rashodima tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu viška prihoda nad rashodima tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 0407 kol. 5 bilansa stanja > 0 , onda je AOP 1047 kol. 5 = AOP 0407-u kol. 5 bilansa stanja  Neto višak prihoda nad rashodima tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu viška prihoda nad rashodima tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10083
        if( aop(bs,407,6) > 0 ):
            if not( aop(bu,1047,6) == aop(bs,407,6) ):
                lzbir =  aop(bu,1047,6) 
                dzbir =  aop(bs,407,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0407 kol. 6 bilansa stanja > 0 , onda je AOP 1047 kol. 6 = AOP 0407-u kol. 6 bilansa stanja  Neto višak prihoda nad rashodima prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu viška prihoda nad rashodima tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 0407 kol. 6 bilansa stanja > 0 , onda je AOP 1047 kol. 6 = AOP 0407-u kol. 6 bilansa stanja  Neto višak prihoda nad rashodima prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu viška prihoda nad rashodima tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10084
        if( aop(bu,1048,5) > 0 ):
            if not( aop(bs,410,5) == aop(bu,1048,5) ):
                lzbir =  aop(bs,410,5) 
                dzbir =  aop(bu,1048,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1048 kol. 5 > 0, onda je AOP 0410 kol. 5 bilansa stanja = AOP-u 1048 kol. 5 Neto višak rashoda nad prihodima tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu viška rashoda nad prihodima tekuće godine u obrascu Bilans stanja;  Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1048 kol. 5 > 0, onda je AOP 0410 kol. 5 bilansa stanja = AOP-u 1048 kol. 5 Neto višak rashoda nad prihodima tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu viška rashoda nad prihodima tekuće godine u obrascu Bilans stanja;  Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10085
        if( aop(bu,1048,6) > 0 ):
            if not( aop(bs,410,6) == aop(bu,1048,6) ):
                lzbir =  aop(bs,410,6) 
                dzbir =  aop(bu,1048,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1048 kol. 6 > 0, onda je AOP 0410 kol. 6 bilansa stanja = AOP-u 1048 kol. 6 Neto višak rashoda nad prihodima prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu viška rashoda nad prihodima tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1048 kol. 6 > 0, onda je AOP 0410 kol. 6 bilansa stanja = AOP-u 1048 kol. 6 Neto višak rashoda nad prihodima prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu viška rashoda nad prihodima tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10086
        if( aop(bs,410,5) > 0 ):
            if not( aop(bu,1048,5) == aop(bs,410,5) ):
                lzbir =  aop(bu,1048,5) 
                dzbir =  aop(bs,410,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0410 kol. 5 bilansa stanja > 0, onda je AOP 1048 kol. 5 = AOP-u 0410 kol. 5 bilansa stanja Neto višak rashoda nad prihodima tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu viška rashoda nad prihodima tekuće godine u obrascu Bilans stanja;  Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 0410 kol. 5 bilansa stanja > 0, onda je AOP 1048 kol. 5 = AOP-u 0410 kol. 5 bilansa stanja Neto višak rashoda nad prihodima tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu viška rashoda nad prihodima tekuće godine u obrascu Bilans stanja;  Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10087
        if( aop(bs,410,6) > 0 ):
            if not( aop(bu,1048,6) == aop(bs,410,6) ):
                lzbir =  aop(bu,1048,6) 
                dzbir =  aop(bs,410,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0410 kol. 6 bilansa stanja > 0, onda je AOP 1048 kol. 6 = AOP-u 0410 kol. 6 bilansa stanja Neto višak rashoda nad prihodima prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu viška rashoda nad prihodima tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 0410 kol. 6 bilansa stanja > 0, onda je AOP 1048 kol. 6 = AOP-u 0410 kol. 6 bilansa stanja Neto višak rashoda nad prihodima prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu viška rashoda nad prihodima tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10088
        #Za ovaj set se ne primenjuje pravilo 
        
        #10089
        #Za ovaj set se ne primenjuje pravilo 
        
        #10090
        #Za ovaj set se ne primenjuje pravilo 
        
        #10091
        #Za ovaj set se ne primenjuje pravilo 
        
        #10092
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if( suma(bu,1001,1048,5) > 0 ):
                if not( suma(bu,1001,1048,5) != suma(bu,1001,1048,6) ):
                    
                    naziv_obrasca='Bilans uspeha'
                    poruka  ='***Ako je zbir podataka na oznakama za AOP (1001 do 1048) kol. 5 > 0 onda zbir podataka na oznakama za AOP (1001 do 1048) kol. 5 ≠ zbiru podataka na oznakama za AOP  (1001 do 1048) kol. 6 Zbirovi podataka u kolonama 5 i 6 bilansa uspeha su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama;  '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
        
        #STATISTIČKI IZVEŠTAJ - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #90001
        if not( suma(si,9008,9014,4)+suma(si,9008,9014,5)+suma(si,9008,9014,6)+suma(si,9016,9021,4)+suma(si,9016,9021,5)+suma(si,9016,9021,6)+suma(si,9023,9029,4)+suma(si,9023,9029,5)+suma(si,9023,9029,6)+suma(si,9031,9036,4)+suma(si,9031,9036,5)+suma(si,9031,9036,6)+suma(si,9037,9094,4)+suma(si,9095,9104,3) > 0 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir podataka na oznakama za AOP (9008 do 9014) kol. 4 + (9008 do 9014) kol. 5 + (9008 do 9014) kol. 6 + (9016 do 9021) kol. 4 + (9016 do 9021) kol. 5 + (9016 do 9021) kol. 6 + (9023 do 9029) kol. 4 + (9023 do 9029) kol. 5 + (9023 do 9029) kol. 6 + (9031 do 9036) kol. 4 + (9031 do 9036) kol. 5 + (9031 do 9036) kol. 6 + (9037 do 9094) kol. 4 + (9095 do 9104) kol. 3  > 0 Statistički izveštaj, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90002
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( aop(si,9007,4)+aop(si,9007,5)+aop(si,9007,6)+aop(si,9015,4)+aop(si,9015,5)+aop(si,9015,6)+aop(si,9022,4)+aop(si,9022,5)+aop(si,9022,6)+aop(si,9030,4)+aop(si,9030,5)+aop(si,9030,6)+suma(si,9037,9094,5)+suma(si,9095,9104,4) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Zbir podataka na oznakama za AOP 9007 kol. 4 + 9007 kol. 5 + 9007 kol. 6 + 9015 kol. 4 + 9015 kol. 5 + 9015 kol. 6 + 9022 kol. 4 + 9022 kol. 5 + 9022 kol. 6  + 9030 kol. 4 + 9030 kol. 5 + 9030 kol. 6 + (9037 do 9094) kol. 5 + (9095 do 9104) kol. 4 > 0 Statistički izveštaj, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90003
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(si,9001,9006,4)+aop(si,9007,4)+aop(si,9007,5)+aop(si,9007,6)+aop(si,9015,4)+aop(si,9015,5)+aop(si,9015,6)+aop(si,9022,4)+aop(si,9022,5)+aop(si,9022,6)+aop(si,9030,4)+aop(si,9030,5)+aop(si,9030,6)+suma(si,9037,9094,5)+suma(si,9095,9104,4) == 0 ):
                lzbir =  suma(si,9001,9006,4)+aop(si,9007,4)+aop(si,9007,5)+aop(si,9007,6)+aop(si,9015,4)+aop(si,9015,5)+aop(si,9015,6)+aop(si,9022,4)+aop(si,9022,5)+aop(si,9022,6)+aop(si,9030,4)+aop(si,9030,5)+aop(si,9030,6)+suma(si,9037,9094,5)+suma(si,9095,9104,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Zbir podataka na oznakama za AOP (9001 do 9006) kol. 4 + 9007 kol. 4 + 9007 kol. 5 + 9007 kol. 6 + 9015 kol. 4 + 9015 kol. 5 + 9015 kol. 6 + 9022 kol. 4 + 9022 kol. 5 + 9022 kol. 6  + 9030 kol. 4 + 9030 kol. 5 + 9030 kol. 6 + (9037 do 9094) kol. 5 + (9095 do 9104) kol. 4 = 0 Statistički izveštaj za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #90004
        if( 1 <= aop(si,9001,3) and 12 >= aop(si, 9001, 3) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='1 ≤ AOP-a 9001 kol. 3 ≤ 12 Broj meseci poslovanja obveznika mora biti iskazan u intervalu između 1 i 12; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90005
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( 1 <= aop(si,9001,4) and 12 >= aop(si, 9001, 4) ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='1 ≤ AOP-a 9001 kol. 4 ≤ 12 Broj meseci poslovanja obveznika osnovanih u ranijim godinama, po pravilu, mora biti iskazan u intervalu između 1 i 12; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90006
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( aop(si,9001,3) == 12 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='AOP 9001 kol. 3 = 12 Broj meseci poslovanja obveznika osnovanih ranijih godina mora biti 12  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #90007
        if not( 1 <= aop(si,9002,3) and 5 >= aop(si,9002,3) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='1 ≤ AOP 9002 kol. 3 ≤ 5 Oznaka za vlasništvo, po pravilu, mora biti iskazana u intervalu između 1 i 5; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90008
        if not( 1 <= aop(si,9002,4) and 5 >= aop(si, 9002, 4) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='1 ≤ AOP 9002 kol. 4 ≤ 5 Oznaka za vlasništvo, po pravilu, mora biti iskazana u intervalu između 1 i 5; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90009
        if not( aop(si, 9003, 3)>0 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9003 kol. 3 > 0    Na poziciji Broj stranih (pravnih ili fizičkih) lica koja imaju uloge nije iskazan podatak; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90010
        if not( aop(si, 9004, 3)>0 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9004 kol. 3 > 0    Na poziciji Prosečan broj zaposlenih nije iskazan podatak; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        
        #90011
        if not( aop(si,9004,3) <= 50 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='***AOP 9004 kol. 3 ≤ 50 Granične vrednosti date su da bi se izbegle slučajne greške prilikom iskazivanja broja zaposlenih; Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90012
        if not( aop(si,9004,4) <= 50 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9004 kol. 4 ≤ 50 Granične vrednosti date su da bi se izbegle slučajne greške prilikom iskazivanja broja zaposlenih; Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90013
        if( aop(si,9004,3) > 0 ):
            if not( suma(si,9044,9046,4) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP 9004 kol. 3 > 0, onda je AOP (9044 + 9045 + 9046) kol. 4 > 0 Ukoliko je iskazan prosečan broj zaposlenih, obveznik, po pravilu, mora imati iskazane obaveze po osnovu bruto zarada; Ukoliko jedan od navedenih podataka nije prikazan, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90014
        if( suma(si,9044,9046,4) > 0 ):
            if not( aop(si,9004,3) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP (9044 + 9045 + 9046) kol. 4 > 0, onda je AOP 9004 kol. 3 > 0  Ukoliko su iskazane obaveze po osnovu bruto zarada, obveznik, po pravilu, mora imati iskazan prosečan broj zaposlenih; Ukoliko jedan od navedenih podataka nije prikazan, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90015
        if( aop(si,9004,4) > 0 ):
            if not( suma(si,9044,9046,5) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP 9004 kol. 4 > 0, onda je AOP (9044 + 9045 + 9046) kol. 5 > 0 Ukoliko je iskazan prosečan broj zaposlenih, obveznik, po pravilu, mora imati iskazane obaveze po osnovu bruto zarada; Ukoliko jedan od navedenih podataka nije prikazan, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90016
        if( suma(si,9044,9046,5) > 0 ):
            if not( aop(si,9004,4) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP (9044 + 9045 + 9046) kol. 5 > 0, onda je AOP 9004 kol. 4 > 0  Ukoliko su iskazane obaveze po osnovu bruto zarada, obveznik, po pravilu, mora imati iskazan prosečan broj zaposlenih;Ukoliko jedan od navedenih podataka nije prikazan, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90017
        if not( aop(si,9005,3) > 0 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9005 kol. 3 > 0 Na poziciji Broj zaposlenih preko agencija i organizacija za zapošljavanje nije iskazan podatak; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90018
        if not( aop(si,9005,3) <= 50 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9005 kol. 3 ≤ 50 Granične vrednosti date su da bi se izbegle slučajne greške prilikom iskazivanja broja zaposlenih preko agencija i organizacija za zapošljavanje; Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90019
        if not( aop(si,9005,4) <= 50 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9005 kol. 4 ≤ 50 Granične vrednosti date su da bi se izbegle slučajne greške prilikom iskazivanja broja zaposlenih preko agencija i organizacija za zapošljavanje; Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90020
        if not( aop(si,9006,3) > 0 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9006 kol. 3 > 0 Na poziciji Prosečan broj volontera  nije iskazan podatak; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90021
        if not( aop(si,9006,3) <= 50 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9006 kol. 3 ≤ 50 Granične vrednosti date su da bi se izbegle slučajne greške prilikom iskazivanja broja volontera; Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90022
        if not( aop(si,9006,4) <= 50 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9006 kol. 4 ≤ 50 Granične vrednosti date su da bi se izbegle slučajne greške prilikom iskazivanja broja volontera; Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90023
        if not( aop(si,9007,6) == aop(si,9007,4)-aop(si,9007,5) ):
            lzbir =  aop(si,9007,6) 
            dzbir =  aop(si,9007,4)-aop(si,9007,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9007 kol. 6 = AOP-u 9007 kol. 4 - AOP 9007 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90024
        if not( aop(si,9014,6) == aop(si,9014,4)-aop(si,9014,5) ):
            lzbir =  aop(si,9014,6) 
            dzbir =  aop(si,9014,4)-aop(si,9014,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9014 kol. 6 = AOP-u 9014 kol. 4 - AOP 9014 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90025
        if not( aop(si,9015,6) == aop(si,9015,4)-aop(si,9015,5) ):
            lzbir =  aop(si,9015,6) 
            dzbir =  aop(si,9015,4)-aop(si,9015,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9015 kol. 6 = AOP-u 9015 kol. 4 - AOP 9015 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90026
        if not( aop(si,9021,6) == aop(si,9021,4)-aop(si,9021,5) ):
            lzbir =  aop(si,9021,6) 
            dzbir =  aop(si,9021,4)-aop(si,9021,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9021 kol. 6 = AOP-u 9021 kol. 4 - AOP 9021 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90027
        if not( aop(si,9022,6) == aop(si,9022,4)-aop(si,9022,5) ):
            lzbir =  aop(si,9022,6) 
            dzbir =  aop(si,9022,4)-aop(si,9022,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9022 kol. 6 = AOP-u 9022 kol. 4 - AOP 9022 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90028
        if not( aop(si,9029,6) == aop(si,9029,4)-aop(si,9029,5) ):
            lzbir =  aop(si,9029,6) 
            dzbir =  aop(si,9029,4)-aop(si,9029,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9029 kol. 6 = AOP-u 9029 kol. 4 - AOP 9029 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90029
        if not( aop(si,9030,6) == aop(si,9030,4)-aop(si,9030,5) ):
            lzbir =  aop(si,9030,6) 
            dzbir =  aop(si,9030,4)-aop(si,9030,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9030 kol. 6 = AOP-u 9030 kol. 4 - AOP 9030 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90030
        if not( aop(si,9036,6) == aop(si,9036,4)-aop(si,9036,5) ):
            lzbir =  aop(si,9036,6) 
            dzbir =  aop(si,9036,4)-aop(si,9036,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9036 kol. 6 = AOP-u 9036 kol. 4 - AOP 9036 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90031
        if not( aop(si,9014,4) == suma_liste(si,[9007,9008,9009,9010,9012,9013],4)-aop(si,9011,4) ):
            lzbir =  aop(si,9014,4) 
            dzbir =  suma_liste(si,[9007,9008,9009,9010,9012,9013],4)-aop(si,9011,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9014 kol. 4 = AOP-u (9007 + 9008 + 9009 + 9010 - 9011 + 9012 + 9013) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90032
        if not( aop(si,9014,5) == suma_liste(si,[9007,9008,9009,9010,9012,9013],5)-aop(si,9011,5) ):
            lzbir =  aop(si,9014,5) 
            dzbir =  suma_liste(si,[9007,9008,9009,9010,9012,9013],5)-aop(si,9011,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9014 kol. 5 = AOP-u (9007 + 9008 + 9009 + 9010 - 9011 + 9012 + 9013) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90033
        if not( aop(si,9012,4) == 0 ):
            lzbir =  aop(si,9012,4) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9012 kol. 4 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90034
        if not( aop(si,9012,6) == 0 ):
            lzbir =  aop(si,9012,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9012 kol. 6 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90035
        if not( aop(si,9021,4) == suma_liste(si,[9015,9016,9017,9019,9020],4)-aop(si,9018,4) ):
            lzbir =  aop(si,9021,4) 
            dzbir =  suma_liste(si,[9015,9016,9017,9019,9020],4)-aop(si,9018,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9021 kol. 4 = AOP-u (9015 + 9016 + 9017 - 9018 + 9019 + 9020) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90036
        if not( aop(si,9021,5) == suma_liste(si,[9015,9016,9017,9019,9020],5)-aop(si,9018,5) ):
            lzbir =  aop(si,9021,5) 
            dzbir =  suma_liste(si,[9015,9016,9017,9019,9020],5)-aop(si,9018,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9021 kol. 5 = AOP-u (9015 + 9016 + 9017 - 9018 + 9019 + 9020) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90037
        if not( aop(si,9019,4) == 0 ):
            lzbir =  aop(si,9019,4) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9019 kol. 4 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90038
        if not( aop(si,9019,6) == 0 ):
            lzbir =  aop(si,9019,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9019 kol. 6 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90039
        if not( aop(si,9029,4) == suma_liste(si,[9022,9023,9024,9025,9027,9028],4)-aop(si,9026,4) ):
            lzbir =  aop(si,9029,4) 
            dzbir =  suma_liste(si,[9022,9023,9024,9025,9027,9028],4)-aop(si,9026,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9029 kol. 4 = AOP-u (9022 + 9023 + 9024 + 9025 - 9026 + 9027 + 9028) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90040
        if not( aop(si,9029,5) == suma_liste(si,[9022,9023,9024,9025,9027,9028],5)-aop(si,9026,5) ):
            lzbir =  aop(si,9029,5) 
            dzbir =  suma_liste(si,[9022,9023,9024,9025,9027,9028],5)-aop(si,9026,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9029 kol. 5 = AOP-u (9022 + 9023 + 9024 + 9025 - 9026 + 9027 + 9028) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90041
        if not( aop(si,9027,4) == 0 ):
            lzbir =  aop(si,9027,4) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9027 kol. 4 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90042
        if not( aop(si,9027,6) == 0 ):
            lzbir =  aop(si,9027,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9027 kol. 6 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90043
        if not( aop(si,9036,4) == suma_liste(si,[9030,9031,9032,9034,9035],4)-aop(si,9033,4) ):
            lzbir =  aop(si,9036,4) 
            dzbir =  suma_liste(si,[9030,9031,9032,9034,9035],4)-aop(si,9033,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9036 kol. 4 = AOP-u (9030 + 9031 + 9032 - 9033 + 9034 + 9035) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90044
        if not( aop(si,9036,5) == suma_liste(si,[9030,9031,9032,9034,9035],5)-aop(si,9033,5) ):
            lzbir =  aop(si,9036,5) 
            dzbir =  suma_liste(si,[9030,9031,9032,9034,9035],5)-aop(si,9033,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9036 kol. 5 = AOP-u (9030 + 9031 + 9032 - 9033 + 9034 + 9035) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90045
        if not( aop(si,9034,4) == 0 ):
            lzbir =  aop(si,9034,4) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9034 kol. 4 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90046
        if not( aop(si,9034,6) == 0 ):
            lzbir =  aop(si,9034,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9034 kol. 6 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90047
        if not( aop(si,9007,6) == aop(bs,2,6) ):
            lzbir =  aop(si,9007,6) 
            dzbir =  aop(bs,2,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9007 kol. 6 = AOP-u 0002 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9007 kol. 6 = AOP-u 0002 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90048
        if not( aop(si,9014,6) == aop(bs,2,5) ):
            lzbir =  aop(si,9014,6) 
            dzbir =  aop(bs,2,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9014 kol. 6 = AOP-u 0002 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9014 kol. 6 = AOP-u 0002 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90049
        if not( suma_liste(si,[9015,9022],6) == aop(bs,3,6) ):
            lzbir =  suma_liste(si,[9015,9022],6) 
            dzbir =  aop(bs,3,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP (9015 + 9022) kol. 6 = AOP-u 0003 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP (9015 + 9022) kol. 6 = AOP-u 0003 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90050
        if not( suma_liste(si,[9021,9029],6) == aop(bs,3,5) ):
            lzbir =  suma_liste(si,[9021,9029],6) 
            dzbir =  aop(bs,3,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP (9021 + 9029) kol. 6 = AOP-u 0003 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP (9021 + 9029) kol. 6 = AOP-u 0003 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90051
        if not( aop(si,9030,6) == aop(bs,9,6) ):
            lzbir =  aop(si,9030,6) 
            dzbir =  aop(bs,9,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9030 kol. 6 = AOP-u 0009 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9030 kol. 6 = AOP-u 0009 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90052
        if not( aop(si,9036,6) == aop(bs,9,5) ):
            lzbir =  aop(si,9036,6) 
            dzbir =  aop(bs,9,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9036 kol. 6 = AOP-u 0009 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9036 kol. 6 = AOP-u 0009 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90053
        if not( aop(si,9037,4) == aop(bs,15,5) ):
            lzbir =  aop(si,9037,4) 
            dzbir =  aop(bs,15,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9037 kol. 4 = AOP-u 0015 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9037 kol. 4 = AOP-u 0015 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90054
        if not( aop(si,9037,5) == aop(bs,15,6) ):
            lzbir =  aop(si,9037,5) 
            dzbir =  aop(bs,15,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9037 kol. 5 = AOP-u 0015 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9037 kol. 5 = AOP-u 0015 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90055
        if not( suma(si,9038,9039,4) == aop(bs,16,5) ):
            lzbir =  suma(si,9038,9039,4) 
            dzbir =  aop(bs,16,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP (9038 + 9039) kol. 4 = AOP-u 0016 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP (9038 + 9039) kol. 4 = AOP-u 0016 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90056
        if not( suma(si,9038,9039,5) == aop(bs,16,6) ):
            lzbir =  suma(si,9038,9039,5) 
            dzbir =  aop(bs,16,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP (9038 + 9039) kol. 5 = AOP-u 0016 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP (9038 + 9039) kol. 5 = AOP-u 0016 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90057
        if not( aop(si,9040,4) == aop(bs,17,5) ):
            lzbir =  aop(si,9040,4) 
            dzbir =  aop(bs,17,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9040 kol. 4 = AOP-u 0017 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9040 kol. 4 = AOP-u 0017 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90058
        if not( aop(si,9040,5) == aop(bs,17,6) ):
            lzbir =  aop(si,9040,5) 
            dzbir =  aop(bs,17,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9040 kol. 5 = AOP-u 0017 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9040 kol. 5 = AOP-u 0017 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90059
        if not( aop(si,9041,4) == aop(bs,18,5) ):
            lzbir =  aop(si,9041,4) 
            dzbir =  aop(bs,18,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9041 kol. 4 = AOP-u 0018 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9041 kol. 4 = AOP-u 0018 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90060
        if not( aop(si,9041,5) == aop(bs,18,6) ):
            lzbir =  aop(si,9041,5) 
            dzbir =  aop(bs,18,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9041 kol. 5 = AOP-u 0018 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9041 kol. 5 = AOP-u 0018 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90061
        if not( aop(si,9042,4) == suma(si,9037,9041,4) ):
            lzbir =  aop(si,9042,4) 
            dzbir =  suma(si,9037,9041,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9042 kol. 4 = AOP-u (9037 + 9038 + 9039 + 9040 + 9041) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90062
        if not( aop(si,9042,5) == suma(si,9037,9041,5) ):
            lzbir =  aop(si,9042,5) 
            dzbir =  suma(si,9037,9041,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9042 kol. 5 = AOP-u (9037 + 9038 + 9039 + 9040 + 9041) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90063
        if not( aop(si,9042,4) == aop(bs,14,5) ):
            lzbir =  aop(si,9042,4) 
            dzbir =  aop(bs,14,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9042 kol. 4 = AOP-u 0014 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9042 kol. 4 = AOP-u 0014 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90064
        if not( aop(si,9042,5) == aop(bs,14,6) ):
            lzbir =  aop(si,9042,5) 
            dzbir =  aop(bs,14,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9042 kol. 5 = AOP-u 0014 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9042 kol. 5 = AOP-u 0014 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90065
        if not( aop(si,9048,4) == suma(si,9043,9047,4) ):
            lzbir =  aop(si,9048,4) 
            dzbir =  suma(si,9043,9047,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9048 kol. 4 = AOP-u (9043 + 9044 + 9045 + 9046 + 9047) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90066
        if not( aop(si,9048,5) == suma(si,9043,9047,5) ):
            lzbir =  aop(si,9048,5) 
            dzbir =  suma(si,9043,9047,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9048 kol. 5 = AOP-u (9043 + 9044 + 9045 + 9046 + 9047) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90067
        if not( aop(si,9049,4) <= aop(bu,1012,5) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9049 kol. 4 ≤ AOP-a 1012 kol. 5 bilansa uspeha Troškovi goriva i energije su izdvojeni deo troškova materijala i energije '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9049 kol. 4 ≤ AOP-a 1012 kol. 5 bilansa uspeha Troškovi goriva i energije su izdvojeni deo troškova materijala i energije '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90068
        if not( aop(si,9049,5) <= aop(bu,1012,6) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9049 kol. 5 ≤ AOP-a 1012 kol. 6 bilansa uspeha Troškovi goriva i energije su izdvojeni deo troškova materijala i energije '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9049 kol. 5 ≤ AOP-a 1012 kol. 6 bilansa uspeha Troškovi goriva i energije su izdvojeni deo troškova materijala i energije '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90069
        if not( aop(si,9050,4) <= suma(si,9044,9046,4) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP-a 9050 kol. 4 ≤ AOP-a (9044 + 9045 + 9046) kol. 4 Troškovi zarada su, po pravilu, manji ili jednaki obavezama za bruto zarade '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90070
        if not( aop(si,9050,5) <= suma(si,9044,9046,5) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP-a 9050 kol. 5 ≤ AOP-a (9044 + 9045 + 9046) kol. 5 Troškovi zarada su, po pravilu, manji ili jednaki obavezama za bruto zarade '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90071
        if not( suma_liste(si,[9050,9051,9052,9053,9054,9055,9056,9057,9058,9059,9061],4) <= suma(bu,1013,1016,5) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir AOP-a (9050 + 9051 + 9052 + 9053 + 9054 + 9055 + 9056 + 9057 + 9058 + 9059 + 9061) kol. 4 ≤  zbiru AOP-a (1013 do 1016) kol. 5 bilansa uspeha Izdvojeni delovi  troškova zarada, naknada zarada i ostalih ličnih rashoda, troškova proizvodnih usluga i troškova rezervisanja su manji ili jednaki od ukupnih troškova po tim osnovama iskazanim u Bilansu uspeha'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir AOP-a (9050 + 9051 + 9052 + 9053 + 9054 + 9055 + 9056 + 9057 + 9058 + 9059 + 9061) kol. 4 ≤  zbiru AOP-a (1013 do 1016) kol. 5 bilansa uspeha Izdvojeni delovi  troškova zarada, naknada zarada i ostalih ličnih rashoda, troškova proizvodnih usluga i troškova rezervisanja su manji ili jednaki od ukupnih troškova po tim osnovama iskazanim u Bilansu uspeha'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90072
        if not( suma_liste(si,[9050,9051,9052,9053,9054,9055,9056,9057,9058,9059,9061],5) <= suma(bu,1013,1016,6) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir AOP-a (9050 + 9051 + 9052 + 9053 + 9054 + 9055 + 9056 + 9057 + 9058 + 9059 + 9061) kol. 5 ≤  zbiru AOP-a (1013 do 1016) kol. 6 bilansa uspeha Izdvojeni delovi  troškova zarada, naknada zarada i ostalih ličnih rashoda, troškova proizvodnih usluga i troškova rezervisanja su manji ili jednaki od ukupnih troškova po tim osnovama iskazanim u Bilansu uspeha '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir AOP-a (9050 + 9051 + 9052 + 9053 + 9054 + 9055 + 9056 + 9057 + 9058 + 9059 + 9061) kol. 5 ≤  zbiru AOP-a (1013 do 1016) kol. 6 bilansa uspeha Izdvojeni delovi  troškova zarada, naknada zarada i ostalih ličnih rashoda, troškova proizvodnih usluga i troškova rezervisanja su manji ili jednaki od ukupnih troškova po tim osnovama iskazanim u Bilansu uspeha'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90073
        if not( aop(si,9060,4) <= aop(si,9059,4) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9060 kol. 4 ≤ AOP-a 9059 kol. 4 Troškovi zakupnina zemljišta su deo troškova zakupnina '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90074
        if not( aop(si,9060,5) <= aop(si,9059,5) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9060 kol. 5 ≤ AOP-a 9059 kol. 5 Troškovi zakupnina zemljišta su deo troškova zakupnina '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90075
        if not( suma(si,9062,9066,4) <= aop(bu,1018,5) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir AOP-a (9062 do 9066) kol. 4 ≤  AOP-u 1018 kol. 5 bilansa uspeha Troškovi osiguranja, platnog prometa, članarina, poreza i naknada i doprinosa su izdvojeni deo nematerijalnih troškova  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir AOP-a (9062 do 9066) kol. 4 ≤  AOP-u 1018 kol. 5 bilansa uspeha Troškovi osiguranja, platnog prometa, članarina, poreza i naknada i doprinosa su izdvojeni deo nematerijalnih troškova  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90076
        if not( suma(si,9062,9066,5) <= aop(bu,1018,6) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir AOP-a (9062 do 9066) kol. 5 ≤  AOP-u 1018 kol. 6 bilansa uspeha Troškovi osiguranja, platnog prometa, članarina, poreza i naknada i doprinosa su izdvojeni deo nematerijalnih troškova  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir AOP-a (9062 do 9066) kol. 5 ≤  AOP-u 1018 kol. 6 bilansa uspeha Troškovi osiguranja, platnog prometa, članarina, poreza i naknada i doprinosa su izdvojeni deo nematerijalnih troškova  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90077
        if not( aop(si,9067,4) == aop(bu,1017,5) ):
            lzbir =  aop(si,9067,4) 
            dzbir =  aop(bu,1017,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9067 kol. 4 =  AOP-u 1017 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9067 kol. 4 =  AOP-u 1017 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90078
        if not( aop(si,9067,5) == aop(bu,1017,6) ):
            lzbir =  aop(si,9067,5) 
            dzbir =  aop(bu,1017,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9067 kol. 5 =  AOP-u 1017 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9067 kol. 5 =  AOP-u 1017 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90079
        if not( aop(si,9068,4) == suma(si,9049,9067,4) ):
            lzbir =  aop(si,9068,4) 
            dzbir =  suma(si,9049,9067,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9068 kol. 4 = Zbiru AOP-a (9049 do 9067) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90080
        if not( aop(si,9068,5) == suma(si,9049,9067,5) ):
            lzbir =  aop(si,9068,5) 
            dzbir =  suma(si,9049,9067,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9068 kol. 5 = Zbiru AOP-a (9049 do 9067) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90081
        if not( suma(si,9069,9074,4) <= aop(bu,1027,5) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir AOP-a (9069 do 9074) kol. 4 ≤  AOP-u 1027 kol. 5 bilansa uspeha Rashodi kamata su izdvojeni deo finansijskih rashoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir AOP-a (9069 do 9074) kol. 4 ≤  AOP-u 1027 kol. 5 bilansa uspeha Rashodi kamata su izdvojeni deo finansijskih rashoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90082
        if not( suma(si,9069,9074,5) <= aop(bu,1027,6) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir AOP-a (9069 do 9074) kol. 5 ≤  AOP-u 1027 kol. 6 bilansa uspeha Rashodi kamata su izdvojeni deo finansijskih rashoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir AOP-a (9069 do 9074) kol. 5 ≤  AOP-u 1027 kol. 6 bilansa uspeha Rashodi kamata su izdvojeni deo finansijskih rashoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90083
        if not( aop(si,9075,4) == suma(si,9069,9074,4) ):
            lzbir =  aop(si,9075,4) 
            dzbir =  suma(si,9069,9074,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9075 kol. 4 = Zbiru AOP-a (9069 do 9074) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90084
        if not( aop(si,9075,5) == suma(si,9069,9074,5) ):
            lzbir =  aop(si,9075,5) 
            dzbir =  suma(si,9069,9074,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9075 kol. 5 = Zbiru AOP-a (9069 do 9074) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90085
        if not( aop(si,9081,4) <= aop(si,9080,4) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9081 kol. 4 ≤ AOP-a 9080 kol. 4 Prihodi od donacija, dotacija i sl. od domaćih javnih preduzeća su izdvojeni deo prihoda od donacija, dotacija i sl. od domaćih privrednih društava, preduzetnika i drugih pravnih lica  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90086
        if not( aop(si,9081,5) <= aop(si,9080,5) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9081 kol. 5 ≤ AOP-a 9080 kol. 5 Prihodi od donacija, dotacija i sl. od domaćih javnih preduzeća su izdvojeni deo prihoda od donacija, dotacija i sl. od domaćih privrednih društava, preduzetnika i drugih pravnih lica  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90087
        if not( suma_liste(si,[9076,9077,9078,9079,9080,9082,9083,9084,9085],4) <= aop(bu,1005,5) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir AOP-a (9076 + 9077 + 9078 + 9079 + 9080 + 9082+ 9083 + 9084+ 9085) kol. 4 ≤  AOP-u 1005 kol. 5 bilansa uspeha Izdvojeni delovi prihoda od donacija, dotacija, subvencija i sl. su manji ili jednaki od ukupnog prihoda po tom osnovu iskazanog u Bilansu uspeha '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir AOP-a (9076 + 9077 + 9078 + 9079 + 9080 + 9082+ 9083 + 9084+ 9085) kol. 4 ≤  AOP-u 1005 kol. 5 bilansa uspeha Izdvojeni delovi prihoda od donacija, dotacija, subvencija i sl. su manji ili jednaki od ukupnog prihoda po tom osnovu iskazanog u Bilansu uspeha'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90088
        if not( suma_liste(si,[9076,9077,9078,9079,9080,9082,9083,9084,9085],5) <= aop(bu,1005,6) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir AOP-a (9076 + 9077 + 9078 + 9079 + 9080 + 9082+ 9083 + 9084+ 9085) kol. 5 ≤  AOP-u 1005 kol. 6 bilansa uspeha Izdvojeni delovi prihoda od donacija, dotacija, subvencija i sl. su manji ili jednaki od ukupnog prihoda po tom osnovu iskazanog u Bilansu uspeha '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir AOP-a (9076 + 9077 + 9078 + 9079 + 9080 + 9082+ 9083 + 9084+ 9085) kol. 5 ≤  AOP-u 1005 kol. 6 bilansa uspeha Izdvojeni delovi prihoda od donacija, dotacija, subvencija i sl. su manji ili jednaki od ukupnog prihoda po tom osnovu iskazanog u Bilansu uspeha'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90089
        if not( aop(si,9086,4) <= aop(bu,1006,5) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9086 kol. 4 ≤  AOP-u 1006 kol. 5 bilansa uspeha Prihodi od zakupa za zemljište su izdvojeni deo prihoda od nefinansijske imovine '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9086 kol. 4 ≤  AOP-u 1006 kol. 5 bilansa uspeha Prihodi od zakupa za zemljište su izdvojeni deo prihoda od nefinansijske imovine '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90090
        if not( aop(si,9086,5) <= aop(bu,1006,6) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9086 kol. 5 ≤  AOP-u 1006 kol. 6 bilansa uspeha Prihodi od zakupa za zemljište su izdvojeni deo prihoda od nefinansijske imovine '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9086 kol. 5 ≤  AOP-u 1006 kol. 6 bilansa uspeha Prihodi od zakupa za zemljište su izdvojeni deo prihoda od nefinansijske imovine '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90091
        if not( suma_liste(si,[9087,9089,9090,9091,9092,9093],4) <= aop(bu,1021,5) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (9087 + 9089 + 9090 + 9091 + 9092 + 9093) kol. 4 ≤  AOP-u 1021 kol. 5 bilansa uspeha Prihodi od dividendi i prihodi od kamata su deo finansijskih prihoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP (9087 + 9089 + 9090 + 9091 + 9092 + 9093) kol. 4 ≤  AOP-u 1021 kol. 5 bilansa uspeha Prihodi od dividendi i prihodi od kamata su deo finansijskih prihoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90092
        if not( suma_liste(si,[9087,9089,9090,9091,9092,9093],5) <= aop(bu,1021,6) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (9087 + 9089 + 9090 + 9091 + 9092 + 9093) kol. 5 ≤  AOP-u 1021 kol. 6 bilansa uspeha Prihodi od dividendi i prihodi od kamata su deo finansijskih prihoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP (9087 + 9089 + 9090 + 9091 + 9092 + 9093) kol. 5 ≤  AOP-u 1021 kol. 6 bilansa uspeha Prihodi od dividendi i prihodi od kamata su deo finansijskih prihoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90093
        if not( aop(si,9088,4) == suma(si,9076,9087,4) ):
            lzbir =  aop(si,9088,4) 
            dzbir =  suma(si,9076,9087,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9088 kol. 4 = zbiru AOP-a (9076 do 9087) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90094
        if not( aop(si,9088,5) == suma(si,9076,9087,5) ):
            lzbir =  aop(si,9088,5) 
            dzbir =  suma(si,9076,9087,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9088 kol. 5 = zbiru AOP-a (9076 do 9087) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90095
        if not( aop(si,9094,4) == suma(si,9089,9093,4) ):
            lzbir =  aop(si,9094,4) 
            dzbir =  suma(si,9089,9093,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9094 kol. 4 = zbiru AOP-a (9089 do 9093) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90096
        if not( aop(si,9094,5) == suma(si,9089,9093,5) ):
            lzbir =  aop(si,9094,5) 
            dzbir =  suma(si,9089,9093,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9094 kol. 5 = zbiru AOP-a (9089 do 9093) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90097
        if not( aop(si,9104,3) == suma(si,9095,9103,3) ):
            lzbir =  aop(si,9104,3) 
            dzbir =  suma(si,9095,9103,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9104 kol. 3 = zbiru AOP-a (9095 do 9103) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90098
        if not( aop(si,9104,4) == suma(si,9095,9103,4) ):
            lzbir =  aop(si,9104,4) 
            dzbir =  suma(si,9095,9103,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9104 kol. 4 = zbiru AOP-a (9095 do 9103) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #POSEBNI PODACI:
        #●PRAVILO NE TREBA DA BUDE VIDLJIVO ZA KORISNIKA, ODNOSNO ZA OBVEZNIKA TREBA DA VIDI SAMO KOMENTAR KOJI JE DAT UZ PRAVILO. 
        #●NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #100001
        if not( 1 <= aop(pp,10001,1) and 4 >= aop(pp, 10001, 1) ):
            
            naziv_obrasca='Posebni podaci'
            poruka  =' Oznaka za veličinu mora biti 1, 2, 3  ili 4 '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #100002
        if not( aop(pp,10002,1) >= 0 ):
            
            naziv_obrasca='Posebni podaci'
            poruka  =' Podatak o prosečnom broju zaposlenih u tekućoj godini mora biti upisan; ako nema zaposlenih upisuje se broj 0 '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #100003
        if not( aop(pp,10002,1) == aop(si,9004,3) ):
            lzbir =  aop(pp,10002,1) 
            dzbir =  aop(si,9004,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  =' Podatak o prosečnom broju zaposlenih u tekućoj godini, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Statistički izveštaj na poziciji AOP 9004 u koloni 3 '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Posebni podaci'
            poruka  =' Podatak o prosečnom broju zaposlenih u tekućoj godini, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Statistički izveštaj na poziciji AOP 9004 u koloni 3 '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #100004
        if not( aop(pp,10003,1) == aop(bu,1001,5) ):
            lzbir =  aop(pp,10003,1) 
            dzbir =  aop(bu,1001,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  =' Podatak o poslovnom prihodu u tekućoj godini, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Bilans uspeha na poziciji AOP 1001 u koloni 5 '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Posebni podaci'
            poruka  =' Podatak o poslovnom prihodu u tekućoj godini, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Bilans uspeha na poziciji AOP 1001 u koloni 5 '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #100005
        if not( aop(pp,10004,1) == aop(bs,24,5) ):
            lzbir =  aop(pp,10004,1) 
            dzbir =  aop(bs,24,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  =' Podatak o vrednosti ukupne aktive u tekućoj godini, u delu posebni podaci, mora biti jednak iskazanom podatku  u obrascu Bilans stanja  na poziciji AOP 0024 u koloni 5 '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Posebni podaci'
            poruka  =' Podatak o vrednosti ukupne aktive u tekućoj godini, u delu posebni podaci, mora biti jednak iskazanom podatku  u obrascu Bilans stanja  na poziciji AOP 0024 u koloni 5 '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #100006
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( aop(pp,10102,1) >= 0 ):
                
                naziv_obrasca='Posebni podaci'
                poruka  =' Podatak o prosečnom broju zaposlenih u prethodnoj godini mora biti upisan; ako nema zaposlenih upisuje se broj 0 '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #100007
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( aop(pp,10102,1) == aop(si,9004,4) ):
                lzbir =  aop(pp,10102,1) 
                dzbir =  aop(si,9004,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Statistički izveštaj'
                poruka  =' Podatak o prosečnom broju zaposlenih u prethodnoj godini, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Statistički izveštaj na poziciji AOP 9004 u koloni 4 '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                naziv_obrasca='Posebni podaci'
                poruka  =' Podatak o prosečnom broju zaposlenih u prethodnoj godini, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Statistički izveštaj na poziciji AOP 9004 u koloni 4 '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #100008
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( aop(pp,10103,1) == aop(bu,1001,6) ):
                lzbir =  aop(pp,10103,1) 
                dzbir =  aop(bu,1001,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  =' Podatak o poslovnom prihodu, u prethodnoj godini, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Bilans uspeha na poziciji AOP 1001 u koloni 6 '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                naziv_obrasca='Posebni podaci'
                poruka  =' Podatak o poslovnom prihodu, u prethodnoj godini, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Bilans uspeha na poziciji AOP 1001 u koloni 6 '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #100009
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( aop(pp,10104,1) == aop(bs,24,6) ):
                lzbir =  aop(pp,10104,1) 
                dzbir =  aop(bs,24,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  =' Podatak o vrednosti ukupne aktive prethodne godine, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Bilans stanja  na poziciji AOP 0024 u koloni 6 '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                naziv_obrasca='Posebni podaci'
                poruka  =' Podatak o vrednosti ukupne aktive prethodne godine, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Bilans stanja  na poziciji AOP 0024 u koloni 6 '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #100010
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( aop(pp,10110,1) == aop(bu,1038,6) ):
                lzbir =  aop(pp,10110,1) 
                dzbir =  aop(bu,1038,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  =' Podatak o ukupnom prihodu prethodne godine, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Bilans uspeha na poziciji AOP 1038 u koloni 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                naziv_obrasca='Posebni podaci'
                poruka  =' Podatak o ukupnom prihodu prethodne godine, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Bilans uspeha na poziciji AOP 1038 u koloni 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

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

 
        
