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
   
#VALIDIRAJ SPISAK PRAVNIH LICA KOA SU OBUHVAĆENA KONSOLIDACIJOM (POSEBNI PODACI ZA KONSOLIDOVANE)
def validiraj_spisak_pravnih_lica_obuhvacenih_konsolidacijom(brojReda, kol_2, kol_3, kol_4, kol_5):
    
    # ako nije popunio nijedno polje vraca true - ovo je dozvoljeno
    if len(kol_2) == 0 and len(kol_3) == 0 and len(kol_4) == 0 and len(kol_5) == 0:
        if(brojReda == 10100):
            return False
        else:
            return True

    # ako je u bilo koje polje nesto upisao radi validaciju 
    kol_2_isvalid = False;
    kol_3_isvalid = False;
    kol_4_isvalid = False;
    kol_5_isvalid = False;

    if len(kol_2)>2: 
        kol_2_isvalid = True
    if len(kol_3)>2: 
        kol_3_isvalid = True
    if len(kol_4)>2:
        kol_4_isvalid = True
    if len(kol_5)==8 and kol_5.isdigit():
        kol_5_isvalid = True
    
    brojacIspravnih = 0
    if kol_2_isvalid: brojacIspravnih += 1
    if kol_3_isvalid: brojacIspravnih += 1
    if kol_4_isvalid: brojacIspravnih += 1
    if kol_5_isvalid: brojacIspravnih += 1

    #ako je ispravno popunio samo jedno ili dva polja vraca gresku
    if brojacIspravnih == 0 or brojacIspravnih == 1 or brojacIspravnih == 2:
        return False

    #ako je ispravno popunio tri polja
    if brojacIspravnih == 3:
        #ako je nesto upiao u kol_5 - maticni broj proverava kolone 2, 4 i 5 (ako je upisao maticni broj mora da bude ispravam)
        if(len(kol_5)>0):
            if kol_2_isvalid == False or kol_4_isvalid == False or kol_5_isvalid == False:
                return False
        #ako nije nista upiao u kol_5 - maticni broj proverava kolone 2 i 4
        else:
             if kol_2_isvalid == False or kol_4_isvalid == False:
                 return False
    return True

#Validiraj spisak pravnih lica
def validiraj_spisak_pravnih_lica(brojReda, kol_2, kol_3, kol_4, kol_5):
    if (len(kol_2) == 0 and len(kol_3) == 0 and len(kol_4) == 0 and len(kol_5) == 0):
        return False

    # ako je u bilo koje polje nesto upisao radi validaciju 
    kol_2_isvalid = False;
    kol_3_isvalid = False;
    kol_4_isvalid = False;
    kol_5_isvalid = False;

    if len(kol_2)>2: 
        kol_2_isvalid = True
    if len(kol_3)>2: 
        kol_3_isvalid = True
    if len(kol_4)>2:
        kol_4_isvalid = True
    if len(kol_5)==8 and kol_5.isdigit():
        kol_5_isvalid = True
    
    brojacIspravnih = 0
    if kol_2_isvalid: brojacIspravnih += 1
    if kol_3_isvalid: brojacIspravnih += 1
    if kol_4_isvalid: brojacIspravnih += 1
    if kol_5_isvalid: brojacIspravnih += 1

    #ako je ispravno popunio samo jedno ili dva polja vraca gresku
    if brojacIspravnih == 0 or brojacIspravnih == 1 or brojacIspravnih == 2:
        return False

    #ako je ispravno popunio tri polja
    if brojacIspravnih == 3:
        #ako je nesto upiao u kol_5 - maticni broj proverava kolone 2, 4 i 5 (ako je upisao maticni broj mora da bude ispravam)
        if(len(kol_5)>0):
            if kol_2_isvalid == False or kol_4_isvalid == False or kol_5_isvalid == False:
                return False
        #ako nije nista upiao u kol_5 - maticni broj proverava kolone 2 i 4
        else:
             if kol_2_isvalid == False or kol_4_isvalid == False:
                 return False
    return True


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

        ioor = getForme(Zahtev,'Izveštaj o ostalom rezultatu')
        if len(ioor)==0:
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='Izveštaj o ostalom rezultatu nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        iotg = getForme(Zahtev,'Izveštaj o tokovima gotovine')
        if len(iotg)==0:
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='Izveštaj o tokovima gotovine nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            
        iopk = getForme(Zahtev,'Izveštaj o promenama na kapitalu')
        if len(iopk)==0:
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='Izveštaj o promenama na kapitalu nije popunjen'
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

        if len(form_errors)>0:
            return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}

        lzbir = 0
        dzbir = 0
        razlika = 0

        hasError = False

        ######################################
        #### POCETAK KONTROLNIH PRAVILA ######
        ######################################


        #00000-1
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-2
        if not( suma(bs,1,54,5)+suma(bs,1,54,6)+suma(bs,1,54,7)+suma(bs,401,460,5)+suma(bs,401,460,6)+suma(bs,401,460,7)+suma(bu,1001,1110,5)+suma(bu,1001,1110,6)+suma(ioor,2001,2031,5)+suma(ioor,2001,2031,6)+suma(iotg,3001,3054,3)+suma(iotg,3001,3054,4)+suma(iopk,4001,4344,1) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0054) kol. 5 + (0001 do 0054) kol. 6 + (0001 do 0054) kol. 7 bilansa stanja + (0401 do 0460) kol. 5 + (0401 do 0460) kol. 6 + (0401 do 0460) kol. 7 bilansa stanja + (1001 do 1110) kol. 5 + (1001 do 1110) kol. 6 bilansa uspeha + (2001 do 2031) kol. 5 + (2001 do 2031) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3054) kol. 3 + (3001 do 3054) kol. 4 izveštaja o tokovima gotovine + (4001 do 4344) izveštaja o promenama na kapitalu  > 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0054) kol. 5 + (0001 do 0054) kol. 6 + (0001 do 0054) kol. 7 bilansa stanja + (0401 do 0460) kol. 5 + (0401 do 0460) kol. 6 + (0401 do 0460) kol. 7 bilansa stanja + (1001 do 1110) kol. 5 + (1001 do 1110) kol. 6 bilansa uspeha + (2001 do 2031) kol. 5 + (2001 do 2031) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3054) kol. 3 + (3001 do 3054) kol. 4 izveštaja o tokovima gotovine + (4001 do 4344)  izveštaja o promenama na kapitalu  > 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0054) kol. 5 + (0001 do 0054) kol. 6 + (0001 do 0054) kol. 7 bilansa stanja + (0401 do 0460) kol. 5 + (0401 do 0460) kol. 6 + (0401 do 0460) kol. 7 bilansa stanja + (1001 do 1110) kol. 5 + (1001 do 1110) kol. 6 bilansa uspeha + (2001 do 2031) kol. 5 + (2001 do 2031) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3054) kol. 3 + (3001 do 3054) kol. 4 izveštaja o tokovima gotovine + (4001 do 4344)  izveštaja o promenama na kapitalu  > 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0054) kol. 5 + (0001 do 0054) kol. 6 + (0001 do 0054) kol. 7 bilansa stanja + (0401 do 0460) kol. 5 + (0401 do 0460) kol. 6 + (0401 do 0460) kol. 7 bilansa stanja + (1001 do 1110) kol. 5 + (1001 do 1110) kol. 6 bilansa uspeha + (2001 do 2031) kol. 5 + (2001 do 2031) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3054) kol. 3 + (3001 do 3054) kol. 4 izveštaja o tokovima gotovine + (4001 do 4344) izveštaja o promenama na kapitalu  > 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0054) kol. 5 + (0001 do 0054) kol. 6 + (0001 do 0054) kol. 7 bilansa stanja + (0401 do 0460) kol. 5 + (0401 do 0460) kol. 6 + (0401 do 0460) kol. 7 bilansa stanja + (1001 do 1110) kol. 5 + (1001 do 1110) kol. 6 bilansa uspeha + (2001 do 2031) kol. 5 + (2001 do 2031) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3054) kol. 3 + (3001 do 3054) kol. 4 izveštaja o tokovima gotovine + (4001 do 4344)  izveštaja o promenama na kapitalu  > 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}

        #00000-3
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-4
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-5
        # U bar jednoj od tri navedene forme kolona napomena mora da ima bar jedan karakter
        #00000-5 - Novo pravilo 2016.
        # U bar jednoj od tri navedene forme kolona napomena mora da ima bar jedan karakter
        bsNapomene = Zahtev.Forme['Bilans stanja'].TekstualnaPoljaForme;
        buNapomene = Zahtev.Forme['Bilans uspeha'].TekstualnaPoljaForme;
        ioorNapomene = Zahtev.Forme['Izveštaj o ostalom rezultatu'].TekstualnaPoljaForme;

        if not(proveriNapomene(bsNapomene, 1, 54, 4) or proveriNapomene(bsNapomene, 401, 460, 4) or proveriNapomene(buNapomene, 1001, 1110, 4) or proveriNapomene(ioorNapomene, 2001, 2031, 4)): 
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Na AOP-u (0001 do 0054) bilansa stanja + (0401 do 0460) bilansa stanja + (1001 do 1110) bilansa uspeha + (2001 do 2031) izveštaja o ostalom rezultatu u koloni 4 (Napomena broj) mora biti unet bar jedan karakter Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ='Na AOP-u (0001 do 0054) bilansa stanja + (0401 do 0460) bilansa stanja + (1001 do 1110) bilansa uspeha + (2001 do 2031) izveštaja o ostalom rezultatu u koloni 4 (Napomena broj) mora biti unet bar jedan karakter Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='Na AOP-u (0001 do 0054) bilansa stanja + (0401 do 0460) bilansa stanja + (1001 do 1110) bilansa uspeha + (2001 do 2031) izveštaja o ostalom rezultatu u koloni 4 (Napomena broj) mora biti unet bar jedan karakter Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #Provera da li je fizahtev placen
        if not(Zahtev.Placen):
            ostalo_errors.append('Naknada za obradu i javno objavljivanje izveštaja i propisane dokumentacije nije uplaćena u propisanom iznosu. Instrukcije za uplatu propisane naknade date su u okviru PIS FI sistema za konkretan zahtev, na linku „Status naplate zahteva / Instrukcija za plaćanje". Ukoliko ste izvršili uplatu, a naknada nije uparena, priložite Dokaz o uplati naknade u delu Dokumentacija (na mestu predviđenom za dokaz o uplati naknade), kako biste mogli da podnesete izveštaj.');

        #Provera negativnih AOP-a
        lista=""
        lista_bs = find_negativni(bs, 1, 460, 5, 7)
        lista_bu = find_negativni(bu, 1001, 1110, 5, 6)
        lista_ioor = find_negativni(ioor, 2001, 2031, 5, 6)
        lista_iotg = find_negativni(iotg, 3001, 3054, 3, 4)
        lista_iopk = find_negativni(iopk, 4001, 4344, 1, 1)
        

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
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ="Unete vrednosti ne mogu biti negativne ! (" + lista + ")"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ="Unete vrednosti ne mogu biti negativne ! (" + lista + ")"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ="Unete vrednosti ne mogu biti negativne ! (" + lista + ")"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)


        #BILANS STANJA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        #00001
        if not( suma(bs,1,54,5)+suma(bs,401,460,5) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0054) kol. 5 + (0401 do 0460) kol. 5 > 0 Bilans stanja, po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #00002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,54,6)+suma(bs,401,460,6) == 0 ):
                lzbir =  suma(bs,1,54,6)+suma(bs,401,460,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0054) kol. 6 + (0401 do 0460) kol. 6 = 0 Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00003
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,54,7)+suma(bs,401,460,7) == 0 ):
                lzbir =  suma(bs,1,54,7)+suma(bs,401,460,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0054) kol. 7 + (0401 do 0460) kol. 7 = 0 Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00004
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,54,6)+suma(bs,401,460,6) > 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0054) kol. 6 + (0401 do 0460) kol. 6 > 0 Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #00005
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,54,7)+suma(bs,401,460,7) > 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0054) kol. 7 + (0401 do 0460) kol. 7 > 0 Bilans stanja, po pravilu,  mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #00006
        if not( aop(bs,2,5) == suma_liste(bs,[3,4,5,6,9,10,21,22],5) ):
            lzbir =  aop(bs,2,5) 
            dzbir =  suma_liste(bs,[3,4,5,6,9,10,21,22],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0002 kol. 5 = AOP-u (0003 + 0004 + 0005 + 0006 + 0009 + 0010 + 0021 + 0022) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00007
        if not( aop(bs,2,6) == suma_liste(bs,[3,4,5,6,9,10,21,22],6) ):
            lzbir =  aop(bs,2,6) 
            dzbir =  suma_liste(bs,[3,4,5,6,9,10,21,22],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0002 kol. 6 = AOP-u (0003 + 0004 + 0005 + 0006 + 0009 + 0010 + 0021 + 0022) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00008
        if not( aop(bs,2,7) == suma_liste(bs,[3,4,5,6,9,10,21,22],7) ):
            lzbir =  aop(bs,2,7) 
            dzbir =  suma_liste(bs,[3,4,5,6,9,10,21,22],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0002 kol. 7 = AOP-u (0003 + 0004 + 0005 + 0006 + 0009 + 0010 + 0021 + 0022) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00009
        if not( aop(bs,6,5) == suma(bs,7,8,5) ):
            lzbir =  aop(bs,6,5) 
            dzbir =  suma(bs,7,8,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0006 kol. 5 = AOP-u (0007 + 0008) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00010
        if not( aop(bs,6,6) == suma(bs,7,8,6) ):
            lzbir =  aop(bs,6,6) 
            dzbir =  suma(bs,7,8,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0006 kol. 6 = AOP-u (0007 + 0008) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00011
        if not( aop(bs,6,7) == suma(bs,7,8,7) ):
            lzbir =  aop(bs,6,7) 
            dzbir =  suma(bs,7,8,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0006 kol. 7 = AOP-u (0007 + 0008) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00012
        if not( aop(bs,10,5) == suma_liste(bs,[11,15],5) ):
            lzbir =  aop(bs,10,5) 
            dzbir =  suma_liste(bs,[11,15],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0010 kol. 5 = AOP-u (0011 + 0015) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00013
        if not( aop(bs,10,6) == suma_liste(bs,[11,15],6) ):
            lzbir =  aop(bs,10,6) 
            dzbir =  suma_liste(bs,[11,15],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0010 kol. 6 = AOP-u (0011 + 0015) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00014
        if not( aop(bs,10,7) == suma_liste(bs,[11,15],7) ):
            lzbir =  aop(bs,10,7) 
            dzbir =  suma_liste(bs,[11,15],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0010 kol. 7 = AOP-u (0011 + 0015) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00015
        if not( aop(bs,11,5) == suma(bs,12,14,5) ):
            lzbir =  aop(bs,11,5) 
            dzbir =  suma(bs,12,14,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0011 kol. 5 = AOP-u (0012 + 0013 + 0014) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00016
        if not( aop(bs,11,6) == suma(bs,12,14,6) ):
            lzbir =  aop(bs,11,6) 
            dzbir =  suma(bs,12,14,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0011 kol. 6 = AOP-u (0012 + 0013 + 0014) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00017
        if not( aop(bs,11,7) == suma(bs,12,14,7) ):
            lzbir =  aop(bs,11,7) 
            dzbir =  suma(bs,12,14,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0011 kol. 7 = AOP-u (0012 + 0013 + 0014) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00018
        if not( aop(bs,15,5) == suma_liste(bs,[16,19,20],5) ):
            lzbir =  aop(bs,15,5) 
            dzbir =  suma_liste(bs,[16,19,20],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0015 kol. 5 = AOP-u (0016 + 0019 + 0020) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00019
        if not( aop(bs,15,6) == suma_liste(bs,[16,19,20],6) ):
            lzbir =  aop(bs,15,6) 
            dzbir =  suma_liste(bs,[16,19,20],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0015 kol. 6 = AOP-u (0016 + 0019 + 0020) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00020
        if not( aop(bs,15,7) == suma_liste(bs,[16,19,20],7) ):
            lzbir =  aop(bs,15,7) 
            dzbir =  suma_liste(bs,[16,19,20],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0015 kol. 7 = AOP-u (0016 + 0019 + 0020) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00021
        if not( aop(bs,16,5) == suma(bs,17,18,5) ):
            lzbir =  aop(bs,16,5) 
            dzbir =  suma(bs,17,18,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0016 kol. 5 = AOP-u (0017 + 0018) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00022
        if not( aop(bs,16,6) == suma(bs,17,18,6) ):
            lzbir =  aop(bs,16,6) 
            dzbir =  suma(bs,17,18,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0016 kol. 6 = AOP-u (0017 + 0018) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00023
        if not( aop(bs,16,7) == suma(bs,17,18,7) ):
            lzbir =  aop(bs,16,7) 
            dzbir =  suma(bs,17,18,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0016 kol. 7 = AOP-u (0017 + 0018) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00024
        if not( aop(bs,23,5) == suma_liste(bs,[24,25,26,45,46,49],5) ):
            lzbir =  aop(bs,23,5) 
            dzbir =  suma_liste(bs,[24,25,26,45,46,49],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0023 kol. 5 = AOP-u (0024 + 0025 + 0026 + 0045 + 0046 + 0049) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00025
        if not( aop(bs,23,6) == suma_liste(bs,[24,25,26,45,46,49],6) ):
            lzbir =  aop(bs,23,6) 
            dzbir =  suma_liste(bs,[24,25,26,45,46,49],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0023 kol. 6 = AOP-u (0024 + 0025 + 0026 + 0045 + 0046 + 0049) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00026
        if not( aop(bs,23,7) == suma_liste(bs,[24,25,26,45,46,49],7) ):
            lzbir =  aop(bs,23,7) 
            dzbir =  suma_liste(bs,[24,25,26,45,46,49],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0023 kol. 7 = AOP-u (0024 + 0025 + 0026 + 0045 + 0046 + 0049) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00027
        if not( aop(bs,26,5) == suma_liste(bs,[27,32,33,44],5) ):
            lzbir =  aop(bs,26,5) 
            dzbir =  suma_liste(bs,[27,32,33,44],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0026 kol. 5 = AOP-u (0027 + 0032 + 0033 + 0044) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00028
        if not( aop(bs,26,6) == suma_liste(bs,[27,32,33,44],6) ):
            lzbir =  aop(bs,26,6) 
            dzbir =  suma_liste(bs,[27,32,33,44],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0026 kol. 6 = AOP-u (0027 + 0032 + 0033 + 0044) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00029
        if not( aop(bs,26,7) == suma_liste(bs,[27,32,33,44],7) ):
            lzbir =  aop(bs,26,7) 
            dzbir =  suma_liste(bs,[27,32,33,44],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0026 kol. 7 = AOP-u (0027 + 0032 + 0033 + 0044) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00030
        if not( aop(bs,27,5) == suma(bs,28,31,5) ):
            lzbir =  aop(bs,27,5) 
            dzbir =  suma(bs,28,31,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0027 kol. 5 = AOP-u (0028 + 0029 + 0030 + 0031) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00031
        if not( aop(bs,27,6) == suma(bs,28,31,6) ):
            lzbir =  aop(bs,27,6) 
            dzbir =  suma(bs,28,31,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0027 kol. 6 = AOP-u (0028 + 0029 + 0030 + 0031) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00032
        if not( aop(bs,27,7) == suma(bs,28,31,7) ):
            lzbir =  aop(bs,27,7) 
            dzbir =  suma(bs,28,31,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0027 kol. 7 = AOP-u (0028 + 0029 + 0030 + 0031) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00033
        if not( aop(bs,33,5) == suma_liste(bs,[34,38,42,43],5) ):
            lzbir =  aop(bs,33,5) 
            dzbir =  suma_liste(bs,[34,38,42,43],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0033 kol. 5 = AOP-u (0034 + 0038 + 0042 + 0043) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00034
        if not( aop(bs,33,6) == suma_liste(bs,[34,38,42,43],6) ):
            lzbir =  aop(bs,33,6) 
            dzbir =  suma_liste(bs,[34,38,42,43],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0033 kol. 6 = AOP-u (0034 + 0038 + 0042 + 0043) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00035
        if not( aop(bs,33,7) == suma_liste(bs,[34,38,42,43],7) ):
            lzbir =  aop(bs,33,7) 
            dzbir =  suma_liste(bs,[34,38,42,43],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0033 kol. 7 = AOP-u (0034 + 0038 + 0042 + 0043) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00036
        if not( aop(bs,34,5) == suma(bs,35,37,5) ):
            lzbir =  aop(bs,34,5) 
            dzbir =  suma(bs,35,37,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0034 kol. 5 = AOP-u (0035 + 0036 + 0037) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00037
        if not( aop(bs,34,6) == suma(bs,35,37,6) ):
            lzbir =  aop(bs,34,6) 
            dzbir =  suma(bs,35,37,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0034 kol. 6 = AOP-u (0035 + 0036 + 0037) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00038
        if not( aop(bs,34,7) == suma(bs,35,37,7) ):
            lzbir =  aop(bs,34,7) 
            dzbir =  suma(bs,35,37,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0034 kol. 7 = AOP-u (0035 + 0036 + 0037) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00039
        if not( aop(bs,38,5) == suma(bs,39,41,5) ):
            lzbir =  aop(bs,38,5) 
            dzbir =  suma(bs,39,41,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0038 kol. 5 = AOP-u (0039 + 0040 + 0041) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00040
        if not( aop(bs,38,6) == suma(bs,39,41,6) ):
            lzbir =  aop(bs,38,6) 
            dzbir =  suma(bs,39,41,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0038 kol. 6 = AOP-u (0039 + 0040 + 0041) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00041
        if not( aop(bs,38,7) == suma(bs,39,41,7) ):
            lzbir =  aop(bs,38,7) 
            dzbir =  suma(bs,39,41,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0038 kol. 7 = AOP-u (0039 + 0040 + 0041) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00042
        if not( aop(bs,46,5) == suma(bs,47,48,5) ):
            lzbir =  aop(bs,46,5) 
            dzbir =  suma(bs,47,48,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0046 kol. 5 = AOP-u (0047 + 0048) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00043
        if not( aop(bs,46,6) == suma(bs,47,48,6) ):
            lzbir =  aop(bs,46,6) 
            dzbir =  suma(bs,47,48,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0046 kol. 6 = AOP-u (0047 + 0048) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00044
        if not( aop(bs,46,7) == suma(bs,47,48,7) ):
            lzbir =  aop(bs,46,7) 
            dzbir =  suma(bs,47,48,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0046 kol. 7 = AOP-u (0047 + 0048) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00045
        if not( aop(bs,49,5) == suma(bs,50,52,5) ):
            lzbir =  aop(bs,49,5) 
            dzbir =  suma(bs,50,52,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0049 kol. 5 = AOP-u (0050 + 0051 + 0052) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00046
        if not( aop(bs,49,6) == suma(bs,50,52,6) ):
            lzbir =  aop(bs,49,6) 
            dzbir =  suma(bs,50,52,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0049 kol. 6 = AOP-u (0050 + 0051 + 0052) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00047
        if not( aop(bs,49,7) == suma(bs,50,52,7) ):
            lzbir =  aop(bs,49,7) 
            dzbir =  suma(bs,50,52,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0049 kol. 7 = AOP-u (0050 + 0051 + 0052) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00048
        if not( aop(bs,53,5) == suma_liste(bs,[1,2,23],5) ):
            lzbir =  aop(bs,53,5) 
            dzbir =  suma_liste(bs,[1,2,23],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0053 kol. 5 = AOP-u (0001 + 0002 + 0023) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00049
        if not( aop(bs,53,6) == suma_liste(bs,[1,2,23],6) ):
            lzbir =  aop(bs,53,6) 
            dzbir =  suma_liste(bs,[1,2,23],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0053 kol. 6 = AOP-u (0001 + 0002 + 0023) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00050
        if not( aop(bs,53,7) == suma_liste(bs,[1,2,23],7) ):
            lzbir =  aop(bs,53,7) 
            dzbir =  suma_liste(bs,[1,2,23],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0053 kol. 7 = AOP-u (0001 + 0002 + 0023) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00051
        if not( aop(bs,401,5) == suma_liste(bs,[402,407,408,411,412,414,421],5)-suma_liste(bs,[413,417,420],5) ):
            lzbir =  aop(bs,401,5) 
            dzbir =  suma_liste(bs,[402,407,408,411,412,414,421],5)-suma_liste(bs,[413,417,420],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0401 kol. 5 = AOP-u (0402 + 0407+ 0408 + 0411 + 0412 - 0413 + 0414 - 0417 - 0420 + 0421) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00052
        if not( aop(bs,401,6) == suma_liste(bs,[402,407,408,411,412,414,421],6)-suma_liste(bs,[413,417,420],6) ):
            lzbir =  aop(bs,401,6) 
            dzbir =  suma_liste(bs,[402,407,408,411,412,414,421],6)-suma_liste(bs,[413,417,420],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0401 kol. 6 = AOP-u (0402 + 0407+ 0408 + 0411 + 0412 - 0413 + 0414 - 0417 - 0420 + 0421) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00053
        if not( aop(bs,401,7) == suma_liste(bs,[402,407,408,411,412,414,421],7)-suma_liste(bs,[413,417,420],7) ):
            lzbir =  aop(bs,401,7) 
            dzbir =  suma_liste(bs,[402,407,408,411,412,414,421],7)-suma_liste(bs,[413,417,420],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0401 kol. 7 = AOP-u (0402 + 0407+ 0408 + 0411 + 0412 - 0413 + 0414 - 0417 - 0420 + 0421) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00054
        if not( aop(bs,402,5) == suma(bs,403,406,5) ):
            lzbir =  aop(bs,402,5) 
            dzbir =  suma(bs,403,406,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0402 kol. 5 = AOP-u (0403 + 0404 + 0405 + 0406) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00055
        if not( aop(bs,402,6) == suma(bs,403,406,6) ):
            lzbir =  aop(bs,402,6) 
            dzbir =  suma(bs,403,406,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0402 kol. 6 = AOP-u (0403 + 0404 + 0405 + 0406) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00056
        if not( aop(bs,402,7) == suma(bs,403,406,7) ):
            lzbir =  aop(bs,402,7) 
            dzbir =  suma(bs,403,406,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0402 kol. 7 = AOP-u (0403 + 0404 + 0405 + 0406) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00057
        if not( aop(bs,408,5) == suma(bs,409,410,5) ):
            lzbir =  aop(bs,408,5) 
            dzbir =  suma(bs,409,410,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0408 kol. 5 = AOP-u (0409 + 0410) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00058
        if not( aop(bs,408,6) == suma(bs,409,410,6) ):
            lzbir =  aop(bs,408,6) 
            dzbir =  suma(bs,409,410,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0408 kol. 6 = AOP-u (0409 + 0410) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00059
        if not( aop(bs,408,7) == suma(bs,409,410,7) ):
            lzbir =  aop(bs,408,7) 
            dzbir =  suma(bs,409,410,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0408 kol. 7 = AOP-u (0409 + 0410) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00060
        if not( aop(bs,414,5) == suma(bs,415,416,5) ):
            lzbir =  aop(bs,414,5) 
            dzbir =  suma(bs,415,416,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0414 kol. 5 = AOP-u (0415 + 0416) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00061
        if not( aop(bs,414,6) == suma(bs,415,416,6) ):
            lzbir =  aop(bs,414,6) 
            dzbir =  suma(bs,415,416,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0414 kol. 6 = AOP-u (0415 + 0416) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00062
        if not( aop(bs,414,7) == suma(bs,415,416,7) ):
            lzbir =  aop(bs,414,7) 
            dzbir =  suma(bs,415,416,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0414 kol. 7 = AOP-u (0415 + 0416) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00063
        if not( aop(bs,417,5) == suma(bs,418,419,5) ):
            lzbir =  aop(bs,417,5) 
            dzbir =  suma(bs,418,419,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0417 kol. 5 = AOP-u (0418 + 0419) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00064
        if not( aop(bs,417,6) == suma(bs,418,419,6) ):
            lzbir =  aop(bs,417,6) 
            dzbir =  suma(bs,418,419,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0417 kol. 6 = AOP-u (0418 + 0419) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00065
        if not( aop(bs,417,7) == suma(bs,418,419,7) ):
            lzbir =  aop(bs,417,7) 
            dzbir =  suma(bs,418,419,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0417 kol. 7 = AOP-u (0418 + 0419) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00066
        #Za ovaj set se ne primenjuje pravilo 
        
        #00067
        #Za ovaj set se ne primenjuje pravilo 
        
        #00068
        #Za ovaj set se ne primenjuje pravilo 
        
        #00069
        if not( aop(bs,422,5) == suma_liste(bs,[423,430,434,435,444,453,457],5) ):
            lzbir =  aop(bs,422,5) 
            dzbir =  suma_liste(bs,[423,430,434,435,444,453,457],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0422 kol. 5 = AOP-u (0423 + 0430 + 0434 + 0435 + 0444 + 0453 + 0457) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00070
        if not( aop(bs,422,6) == suma_liste(bs,[423,430,434,435,444,453,457],6) ):
            lzbir =  aop(bs,422,6) 
            dzbir =  suma_liste(bs,[423,430,434,435,444,453,457],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0422 kol. 6 = AOP-u (0423 + 0430 + 0434 + 0435 + 0444 + 0453 + 0457) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00071
        if not( aop(bs,422,7) == suma_liste(bs,[423,430,434,435,444,453,457],7) ):
            lzbir =  aop(bs,422,7) 
            dzbir =  suma_liste(bs,[423,430,434,435,444,453,457],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0422 kol. 7 = AOP-u (0423 + 0430 + 0434 + 0435 + 0444 + 0453 + 0457) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00072
        if not( aop(bs,423,5) == suma(bs,424,429,5) ):
            lzbir =  aop(bs,423,5) 
            dzbir =  suma(bs,424,429,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0423 kol. 5 = AOP-u (0424 + 0425 + 0426 + 0427 + 0428 + 0429) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00073
        if not( aop(bs,423,6) == suma(bs,424,429,6) ):
            lzbir =  aop(bs,423,6) 
            dzbir =  suma(bs,424,429,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0423 kol. 6 = AOP-u (0424 + 0425 + 0426 + 0427 + 0428 + 0429) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00074
        if not( aop(bs,423,7) == suma(bs,424,429,7) ):
            lzbir =  aop(bs,423,7) 
            dzbir =  suma(bs,424,429,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0423 kol. 7 = AOP-u (0424 + 0425 + 0426 + 0427 + 0428 + 0429) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00075
        if not( aop(bs,430,5) == suma(bs,431,433,5) ):
            lzbir =  aop(bs,430,5) 
            dzbir =  suma(bs,431,433,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0430 kol. 5 = AOP-u (0431 + 0432 + 0433) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00076
        if not( aop(bs,430,6) == suma(bs,431,433,6) ):
            lzbir =  aop(bs,430,6) 
            dzbir =  suma(bs,431,433,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0430 kol. 6 = AOP-u (0431 + 0432 + 0433) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00077
        if not( aop(bs,430,7) == suma(bs,431,433,7) ):
            lzbir =  aop(bs,430,7) 
            dzbir =  suma(bs,431,433,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0430 kol. 7 = AOP-u (0431 + 0432 + 0433) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00078
        if not( aop(bs,435,5) == suma_liste(bs,[436,440,441,442,443],5) ):
            lzbir =  aop(bs,435,5) 
            dzbir =  suma_liste(bs,[436,440,441,442,443],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0435 kol. 5 = AOP-u (0436 + 0440 + 0441 + 0442 + 0443) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00079
        if not( aop(bs,435,6) == suma_liste(bs,[436,440,441,442,443],6) ):
            lzbir =  aop(bs,435,6) 
            dzbir =  suma_liste(bs,[436,440,441,442,443],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0435 kol. 6 = AOP-u (0436 + 0440 + 0441 + 0442 + 0443) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00080
        if not( aop(bs,435,7) == suma_liste(bs,[436,440,441,442,443],7) ):
            lzbir =  aop(bs,435,7) 
            dzbir =  suma_liste(bs,[436,440,441,442,443],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0435 kol. 7 = AOP-u (0436 + 0440 + 0441 + 0442 + 0443) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00081
        if not( aop(bs,436,5) == suma(bs,437,439,5) ):
            lzbir =  aop(bs,436,5) 
            dzbir =  suma(bs,437,439,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0436 kol. 5 = AOP-u (0437 + 0438 + 0439) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00082
        if not( aop(bs,436,6) == suma(bs,437,439,6) ):
            lzbir =  aop(bs,436,6) 
            dzbir =  suma(bs,437,439,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0436 kol. 6 = AOP-u (0437 + 0438 + 0439) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00083
        if not( aop(bs,436,7) == suma(bs,437,439,7) ):
            lzbir =  aop(bs,436,7) 
            dzbir =  suma(bs,437,439,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0436 kol. 7 = AOP-u (0437 + 0438 + 0439) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00084
        if not( aop(bs,444,5) == suma_liste(bs,[445,449,450],5) ):
            lzbir =  aop(bs,444,5) 
            dzbir =  suma_liste(bs,[445,449,450],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0444 kol. 5 = AOP-u (0445 + 0449 + 0450) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00085
        if not( aop(bs,444,6) == suma_liste(bs,[445,449,450],6) ):
            lzbir =  aop(bs,444,6) 
            dzbir =  suma_liste(bs,[445,449,450],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0444 kol. 6 = AOP-u (0445 + 0449 + 0450) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00086
        if not( aop(bs,444,7) == suma_liste(bs,[445,449,450],7) ):
            lzbir =  aop(bs,444,7) 
            dzbir =  suma_liste(bs,[445,449,450],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0444 kol. 7 = AOP-u (0445 + 0449 + 0450) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00087
        if not( aop(bs,445,5) == suma(bs,446,448,5) ):
            lzbir =  aop(bs,445,5) 
            dzbir =  suma(bs,446,448,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0445 kol. 5 = AOP-u (0446 + 0447 + 0448) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00088
        if not( aop(bs,445,6) == suma(bs,446,448,6) ):
            lzbir =  aop(bs,445,6) 
            dzbir =  suma(bs,446,448,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0445 kol. 6 = AOP-u (0446 + 0447 + 0448) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00089
        if not( aop(bs,445,7) == suma(bs,446,448,7) ):
            lzbir =  aop(bs,445,7) 
            dzbir =  suma(bs,446,448,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0445 kol. 7 = AOP-u (0446 + 0447 + 0448) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00090
        if not( aop(bs,450,5) == suma(bs,451,452,5) ):
            lzbir =  aop(bs,450,5) 
            dzbir =  suma(bs,451,452,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0450 kol. 5 = AOP-u (0451 + 0452) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00091
        if not( aop(bs,450,6) == suma(bs,451,452,6) ):
            lzbir =  aop(bs,450,6) 
            dzbir =  suma(bs,451,452,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0450 kol. 6 = AOP-u (0451 + 0452) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00092
        if not( aop(bs,450,7) == suma(bs,451,452,7) ):
            lzbir =  aop(bs,450,7) 
            dzbir =  suma(bs,451,452,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0450 kol. 7 = AOP-u (0451 + 0452) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00093
        if not( aop(bs,453,5) == suma(bs,454,456,5) ):
            lzbir =  aop(bs,453,5) 
            dzbir =  suma(bs,454,456,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0453 kol. 5 = AOP-u (0454 + 0455 + 0456) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00094
        if not( aop(bs,453,6) == suma(bs,454,456,6) ):
            lzbir =  aop(bs,453,6) 
            dzbir =  suma(bs,454,456,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0453 kol. 6 = AOP-u (0454 + 0455 + 0456) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00095
        if not( aop(bs,453,7) == suma(bs,454,456,7) ):
            lzbir =  aop(bs,453,7) 
            dzbir =  suma(bs,454,456,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0453 kol. 7 = AOP-u (0454 + 0455 + 0456) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00096
        if( aop(bs,401,5) > 0 ):
            if not( aop(bs,458,5) == 0 ):
                lzbir =  aop(bs,458,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0401 kol. 5 > 0, onda je AOP 0458 kol. 5 = 0 Ne mogu biti istovremeno prikazani kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00097
        if( aop(bs,458,5) > 0 ):
            if not( aop(bs,401,5) == 0 ):
                lzbir =  aop(bs,401,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0458 kol. 5 > 0, onda je AOP 0401 kol. 5 = 0 Ne mogu biti istovremeno prikazani kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00098
        if( aop(bs,401,6) > 0 ):
            if not( aop(bs,458,6) == 0 ):
                lzbir =  aop(bs,458,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0401 kol. 6 > 0, onda je AOP 0458 kol. 6 = 0 Ne mogu biti istovremeno prikazani kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00099
        if( aop(bs,458,6) > 0 ):
            if not( aop(bs,401,6) == 0 ):
                lzbir =  aop(bs,401,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0458 kol. 6 > 0, onda je AOP 0401 kol. 6 = 0 Ne mogu biti istovremeno prikazani kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00100
        if( aop(bs,401,7) > 0 ):
            if not( aop(bs,458,7) == 0 ):
                lzbir =  aop(bs,458,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0401 kol. 7 > 0, onda je AOP 0458 kol. 7 = 0 Ne mogu biti istovremeno prikazani kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00101
        if( aop(bs,458,7) > 0 ):
            if not( aop(bs,401,7) == 0 ):
                lzbir =  aop(bs,401,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako jeAOP 0458 kol. 7 > 0, onda je AOP 0401 kol. 7 = 0 Ne mogu biti istovremeno prikazani kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00102
        if not( aop(bs,459,5) == suma_liste(bs,[401,422],5)-aop(bs,458,5) ):
            lzbir =  aop(bs,459,5) 
            dzbir =  suma_liste(bs,[401,422],5)-aop(bs,458,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0459 kol. 5 = AOP-u (0401 + 0422 - 0458) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00103
        if not( aop(bs,459,6) == suma_liste(bs,[401,422],6)-aop(bs,458,6) ):
            lzbir =  aop(bs,459,6) 
            dzbir =  suma_liste(bs,[401,422],6)-aop(bs,458,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0459 kol. 6 = AOP-u (0401 + 0422 - 0458) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00104
        if not( aop(bs,459,7) == suma_liste(bs,[401,422],7)-aop(bs,458,7) ):
            lzbir =  aop(bs,459,7) 
            dzbir =  suma_liste(bs,[401,422],7)-aop(bs,458,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0459 kol. 7 = AOP-u (0401 + 0422 - 0458) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00105
        if not( aop(bs,53,5) == aop(bs,459,5) ):
            lzbir =  aop(bs,53,5) 
            dzbir =  aop(bs,459,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0053 kol. 5 = AOP-u 0459 kol. 5  Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00106
        if not( aop(bs,53,6) == aop(bs,459,6) ):
            lzbir =  aop(bs,53,6) 
            dzbir =  aop(bs,459,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0053 kol. 6 = AOP-u 0459 kol. 6 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00107
        if not( aop(bs,53,7) == aop(bs,459,7) ):
            lzbir =  aop(bs,53,7) 
            dzbir =  aop(bs,459,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0053 kol. 7 = AOP-u 0459 kol. 7 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00108
        if not( aop(bs,54,5) == aop(bs,460,5) ):
            lzbir =  aop(bs,54,5) 
            dzbir =  aop(bs,460,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0054 kol. 5 = AOP-u 0460 kol. 5  Kontrolno pravilo zahteva slaganje vanbilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00109
        if not( aop(bs,54,6) == aop(bs,460,6) ):
            lzbir =  aop(bs,54,6) 
            dzbir =  aop(bs,460,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0054 kol. 6 = AOP-u 0460 kol. 6 Kontrolno pravilo zahteva slaganje vanbilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00110
        if not( aop(bs,54,7) == aop(bs,460,7) ):
            lzbir =  aop(bs,54,7) 
            dzbir =  aop(bs,460,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0054 kol. 7 = AOP-u 0460 kol. 7 Kontrolno pravilo zahteva slaganje vanbilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00111
        if not( aop(bs,1,5) == aop(bs,407,5) ):
            lzbir =  aop(bs,1,5) 
            dzbir =  aop(bs,407,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0001 kol. 5 = AOP-u 0407 kol. 5 Neuplaćeni upisani kapital u aktivi mora biti jednak upisanom a neuplaćenom kapitalu u pasivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00112
        if not( aop(bs,1,6) == aop(bs,407,6) ):
            lzbir =  aop(bs,1,6) 
            dzbir =  aop(bs,407,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0001 kol. 6 = AOP-u 0407 kol. 6 Neuplaćeni upisani kapital u aktivi mora biti jednak upisanom a neuplaćenom kapitalu u pasivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00113
        if not( aop(bs,1,7) == aop(bs,407,7) ):
            lzbir =  aop(bs,1,7) 
            dzbir =  aop(bs,407,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0001 kol. 7 = AOP-u 0407 kol. 7 Neuplaćeni upisani kapital u aktivi mora biti jednak upisanom a neuplaćenom kapitalu u pasivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00114
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if( suma(bu,1001,1110,5) > 0 ):
                if not( suma(bs,1,54,5)+suma(bs,401,460,5) != suma(bs,1,54,6)+suma(bs,401,460,6) ):
                    
                    naziv_obrasca='Bilans uspeha'
                    poruka  ='***Ako je zbir podataka na oznakama za AOP (1001 do 1110) kol. 5 > 0 onda zbir podataka na oznakama za AOP (0001 do 0054) kol. 5 + (0401 do 0460) kol. 5 ≠ zbiru podataka na oznakama za AOP (0001 do 0054) kol. 6 + (0401 do 0460) kol. 6 Zbirovi podataka u kolonama 5 i 6 bilansa stanja su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama;  '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ='***Ako je zbir podataka na oznakama za AOP (1001 do 1110) kol. 5 > 0 onda zbir podataka na oznakama za AOP (0001 do 0054) kol. 5 + (0401 do 0460) kol. 5 ≠ zbiru podataka na oznakama za AOP (0001 do 0054) kol. 6 + (0401 do 0460) kol. 6 Zbirovi podataka u kolonama 5 i 6 bilansa stanja su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama;  '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
        
        #BILANS USPEHA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #10001
        if not( suma(bu,1001,1110,5) > 0 ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP (1001 do 1110) kol. 5 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #10002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bu,1001,1110,6) == 0 ):
                lzbir =  suma(bu,1001,1110,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Zbir podataka na oznakama za AOP (1001 do 1110) kol. 6 = 0 Bilans uspeha za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bu,1001,1110,6) > 0 ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Zbir podataka na oznakama za AOP (1001 do 1110) kol. 6 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period;Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10004
        if not( aop(bu,1001,5) == suma_liste(bu,[1002,1009,1014,1015],5) ):
            lzbir =  aop(bu,1001,5) 
            dzbir =  suma_liste(bu,[1002,1009,1014,1015],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1001 kol. 5 = AOP-u (1002 + 1009 + 1014 + 1015) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10005
        if not( aop(bu,1001,6) == suma_liste(bu,[1002,1009,1014,1015],6) ):
            lzbir =  aop(bu,1001,6) 
            dzbir =  suma_liste(bu,[1002,1009,1014,1015],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1001 kol. 6 = AOP-u (1002 + 1009 + 1014 + 1015) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10006
        if not( aop(bu,1002,5) == suma_liste(bu,[1003,1004,1008],5)-suma(bu,1005,1007,5) ):
            lzbir =  aop(bu,1002,5) 
            dzbir =  suma_liste(bu,[1003,1004,1008],5)-suma(bu,1005,1007,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1002 kol. 5 = AOP-u (1003 + 1004 - 1005 - 1006 - 1007 + 1008) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10007
        if not( aop(bu,1002,6) == suma_liste(bu,[1003,1004,1008],6)-suma(bu,1005,1007,6) ):
            lzbir =  aop(bu,1002,6) 
            dzbir =  suma_liste(bu,[1003,1004,1008],6)-suma(bu,1005,1007,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1002 kol. 6 = AOP-u (1003 + 1004 - 1005 - 1006 - 1007 + 1008) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10008
        if not( aop(bu,1009,5) == suma_liste(bu,[1010,1013],5)-suma(bu,1011,1012,5) ):
            lzbir =  aop(bu,1009,5) 
            dzbir =  suma_liste(bu,[1010,1013],5)-suma(bu,1011,1012,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1009 kol. 5 = AOP-u (1010 - 1011 - 1012 + 1013) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10009
        if not( aop(bu,1009,6) == suma_liste(bu,[1010,1013],6)-suma(bu,1011,1012,6) ):
            lzbir =  aop(bu,1009,6) 
            dzbir =  suma_liste(bu,[1010,1013],6)-suma(bu,1011,1012,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1009 kol. 6 = AOP-u (1010 - 1011 - 1012 + 1013) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10010
        if not( aop(bu,1016,5) == suma_liste(bu,[1017,1026,1034,1045,1047,1048],5)-suma_liste(bu,[1035,1044,1046],5) ):
            lzbir =  aop(bu,1016,5) 
            dzbir =  suma_liste(bu,[1017,1026,1034,1045,1047,1048],5)-suma_liste(bu,[1035,1044,1046],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1016 kol. 5 = AOP-u (1017 + 1026 + 1034 - 1035 - 1044 + 1045 - 1046 + 1047 + 1048) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10011
        if not( aop(bu,1016,6) == suma_liste(bu,[1017,1026,1034,1045,1047,1048],6)-suma_liste(bu,[1035,1044,1046],6) ):
            lzbir =  aop(bu,1016,6) 
            dzbir =  suma_liste(bu,[1017,1026,1034,1045,1047,1048],6)-suma_liste(bu,[1035,1044,1046],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1016 kol. 6 = AOP-u (1017 + 1026 + 1034 - 1035 - 1044 + 1045 - 1046 + 1047 + 1048) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10012
        if not( aop(bu,1017,5) == suma(bu,1018,1025,5) ):
            lzbir =  aop(bu,1017,5) 
            dzbir =  suma(bu,1018,1025,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1017 kol. 5 = AOP-u (1018 + 1019 + 1020 + 1021 + 1022 + 1023 + 1024 + 1025) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10013
        if not( aop(bu,1017,6) == suma(bu,1018,1025,6) ):
            lzbir =  aop(bu,1017,6) 
            dzbir =  suma(bu,1018,1025,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1017 kol. 6 = AOP-u (1018 + 1019 + 1020 + 1021 + 1022 + 1023 + 1024 + 1025) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10014
        if not( aop(bu,1026,5) == suma(bu,1027,1031,5)-suma(bu,1032,1033,5) ):
            lzbir =  aop(bu,1026,5) 
            dzbir =  suma(bu,1027,1031,5)-suma(bu,1032,1033,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1026 kol. 5 = AOP-u (1027 + 1028 + 1029 + 1030 + 1031 - 1032 - 1033) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10015
        if not( aop(bu,1026,6) == suma(bu,1027,1031,6)-suma(bu,1032,1033,6) ):
            lzbir =  aop(bu,1026,6) 
            dzbir =  suma(bu,1027,1031,6)-suma(bu,1032,1033,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1026 kol. 6 = AOP-u (1027 + 1028 + 1029 + 1030 + 1031 - 1032 - 1033) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10016
        if( suma_liste(bu,[1036,1038,1040,1042],5) > suma_liste(bu,[1037,1039,1041,1043],5) ):
            if not( aop(bu,1034,5) == suma_liste(bu,[1036,1038,1040,1042],5)-suma_liste(bu,[1037,1039,1041,1043],5) ):
                lzbir =  aop(bu,1034,5) 
                dzbir =  suma_liste(bu,[1036,1038,1040,1042],5)-suma_liste(bu,[1037,1039,1041,1043],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1034 kol. 5 = AOP-u (1036 - 1037 + 1038 - 1039 + 1040 - 1041 + 1042 - 1043) kol. 5, ako je AOP (1036 + 1038 + 1040 + 1042) kol. 5 > AOP-a (1037 + 1039 + 1041 + 1043) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10017
        if( suma_liste(bu,[1036,1038,1040,1042],6) > suma_liste(bu,[1037,1039,1041,1043],6) ):
            if not( aop(bu,1034,6) == suma_liste(bu,[1036,1038,1040,1042],6)-suma_liste(bu,[1037,1039,1041,1043],6) ):
                lzbir =  aop(bu,1034,6) 
                dzbir =  suma_liste(bu,[1036,1038,1040,1042],6)-suma_liste(bu,[1037,1039,1041,1043],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1034 kol. 6 = AOP-u (1036 - 1037 + 1038 - 1039 + 1040 - 1041 + 1042 - 1043) kol. 6, ako je AOP (1036 + 1038 + 1040 + 1042) kol. 6 > AOP-a (1037 + 1039 + 1041 + 1043) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10018
        if( suma_liste(bu,[1036,1038,1040,1042],5) < suma_liste(bu,[1037,1039,1041,1043],5) ):
            if not( aop(bu,1035,5) == suma_liste(bu,[1037,1039,1041,1043],5)-suma_liste(bu,[1036,1038,1040,1042],5) ):
                lzbir =  aop(bu,1035,5) 
                dzbir =  suma_liste(bu,[1037,1039,1041,1043],5)-suma_liste(bu,[1036,1038,1040,1042],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1035 kol. 5 = AOP-u (1037 - 1036 - 1038 + 1039 - 1040 + 1041 - 1042 + 1043) kol. 5, ako je AOP (1036 + 1038 + 1040 + 1042) kol. 5 < AOP-a (1037 + 1039 + 1041 + 1043) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10019
        if( suma_liste(bu,[1036,1038,1040,1042],6) < suma_liste(bu,[1037,1039,1041,1043],6) ):
            if not( aop(bu,1035,6) == suma_liste(bu,[1037,1039,1041,1043],6)-suma_liste(bu,[1036,1038,1040,1042],6) ):
                lzbir =  aop(bu,1035,6) 
                dzbir =  suma_liste(bu,[1037,1039,1041,1043],6)-suma_liste(bu,[1036,1038,1040,1042],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1035 kol. 6 = AOP-u (1037 - 1036 - 1038 + 1039 - 1040 + 1041 - 1042 + 1043) kol. 6, ako je AOP (1036 + 1038 + 1040 + 1042) kol. 6 < AOP-a (1037 + 1039 + 1041 + 1043) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10020
        if( suma_liste(bu,[1036,1038,1040,1042],5) == suma_liste(bu,[1037,1039,1041,1043],5) ):
            if not( suma(bu,1034,1035,5) == 0 ):
                lzbir =  suma(bu,1034,1035,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1034 + 1035) kol. 5 = 0, ako je AOP (1036 + 1038 + 1040 + 1042) kol. 5 = AOP-u (1037 + 1039 + 1041 + 1043) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10021
        if( suma_liste(bu,[1036,1038,1040,1042],6) == suma_liste(bu,[1037,1039,1041,1043],6) ):
            if not( suma(bu,1034,1035,6) == 0 ):
                lzbir =  suma(bu,1034,1035,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1034 + 1035) kol. 6 = 0, ako je AOP (1036 + 1038 + 1040 + 1042) kol. 6 = AOP-u (1037 + 1039 + 1041 + 1043) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10022
        if( aop(bu,1034,5) > 0 ):
            if not( aop(bu,1035,5) == 0 ):
                lzbir =  aop(bu,1035,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1034 kol. 5 > 0, onda je AOP 1035 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazana povećanje i smanjenje '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10023
        if( aop(bu,1035,5) > 0 ):
            if not( aop(bu,1034,5) == 0 ):
                lzbir =  aop(bu,1034,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1035 kol. 5 > 0, onda je AOP 1034 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazana povećanje i smanjenje '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10024
        if( aop(bu,1034,6) > 0 ):
            if not( aop(bu,1035,6) == 0 ):
                lzbir =  aop(bu,1035,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1034 kol. 6 > 0, onda je AOP 1035 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazana povećanje i smanjenje '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10025
        if( aop(bu,1035,6) > 0 ):
            if not( aop(bu,1034,6) == 0 ):
                lzbir =  aop(bu,1034,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1035 kol. 6 > 0, onda je AOP 1034 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazana povećanje i smanjenje '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10026
        if not( suma_liste(bu,[1035,1036,1038,1040,1042],5) == suma_liste(bu,[1034,1037,1039,1041,1043],5) ):
            lzbir =  suma_liste(bu,[1035,1036,1038,1040,1042],5) 
            dzbir =  suma_liste(bu,[1034,1037,1039,1041,1043],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1035 + 1036 + 1038 + 1040 + 1042) kol. 5 = AOP-u (1034 + 1037 + 1039 + 1041 + 1043) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10027
        if not( suma_liste(bu,[1035,1036,1038,1040,1042],6) == suma_liste(bu,[1034,1037,1039,1041,1043],6) ):
            lzbir =  suma_liste(bu,[1035,1036,1038,1040,1042],6) 
            dzbir =  suma_liste(bu,[1034,1037,1039,1041,1043],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1035 + 1036 + 1038 + 1040 + 1042) kol. 6 = AOP-u (1034 + 1037 + 1039 + 1041 + 1043) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10028
        if( aop(bu,1001,5) > aop(bu,1016,5) ):
            if not( aop(bu,1049,5) == aop(bu,1001,5)-aop(bu,1016,5) ):
                lzbir =  aop(bu,1049,5) 
                dzbir =  aop(bu,1001,5)-aop(bu,1016,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1049 kol. 5 = AOP-u (1001 - 1016) kol. 5, ako je AOP 1001 kol. 5 > AOP-a 1016 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10029
        if( aop(bu,1001,6) > aop(bu,1016,6) ):
            if not( aop(bu,1049,6) == aop(bu,1001,6)-aop(bu,1016,6) ):
                lzbir =  aop(bu,1049,6) 
                dzbir =  aop(bu,1001,6)-aop(bu,1016,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1049 kol. 6 = AOP-u (1001 - 1016) kol. 6, ako je AOP 1001 kol. 6 > AOP-a 1016 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10030
        if( aop(bu,1001,5) < aop(bu,1016,5) ):
            if not( aop(bu,1050,5) == aop(bu,1016,5)-aop(bu,1001,5) ):
                lzbir =  aop(bu,1050,5) 
                dzbir =  aop(bu,1016,5)-aop(bu,1001,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1050 kol. 5 = AOP-u (1016 - 1001) kol. 5, ako je AOP 1001 kol. 5 < AOP-a 1016 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10031
        if( aop(bu,1001,6) < aop(bu,1016,6) ):
            if not( aop(bu,1050,6) == aop(bu,1016,6)-aop(bu,1001,6) ):
                lzbir =  aop(bu,1050,6) 
                dzbir =  aop(bu,1016,6)-aop(bu,1001,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1050 kol. 6 = AOP-u (1016 - 1001) kol. 6, ako je AOP 1001 kol. 6 < AOP-a 1016 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10032
        if( aop(bu,1001,5) == aop(bu,1016,5) ):
            if not( suma(bu,1049,1050,5) == 0 ):
                lzbir =  suma(bu,1049,1050,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1049 + 1050) kol. 5 = 0, ako je AOP 1001 kol. 5 = AOP-u 1016 kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10033
        if( aop(bu,1001,6) == aop(bu,1016,6) ):
            if not( suma(bu,1049,1050,6) == 0 ):
                lzbir =  suma(bu,1049,1050,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1049 + 1050) kol. 6 = 0, ako je AOP 1001 kol. 6 = AOP-u 1016 kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10034
        if( aop(bu,1049,5) > 0 ):
            if not( aop(bu,1050,5) == 0 ):
                lzbir =  aop(bu,1050,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1049 kol. 5 > 0, onda je AOP 1050 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10035
        if( aop(bu,1050,5) > 0 ):
            if not( aop(bu,1049,5) == 0 ):
                lzbir =  aop(bu,1049,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1050 kol. 5 > 0, onda je AOP 1049 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10036
        if( aop(bu,1049,6) > 0 ):
            if not( aop(bu,1050,6) == 0 ):
                lzbir =  aop(bu,1050,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1049 kol. 6 > 0, onda je AOP 1050 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10037
        if( aop(bu,1050,6) > 0 ):
            if not( aop(bu,1049,6) == 0 ):
                lzbir =  aop(bu,1049,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1050 kol. 6 > 0, onda je AOP 1049 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10038
        if not( suma_liste(bu,[1001,1050],5) == suma_liste(bu,[1016,1049],5) ):
            lzbir =  suma_liste(bu,[1001,1050],5) 
            dzbir =  suma_liste(bu,[1016,1049],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1050) kol. 5 = AOP-u (1016 + 1049) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10039
        if not( suma_liste(bu,[1001,1050],6) == suma_liste(bu,[1016,1049],6) ):
            lzbir =  suma_liste(bu,[1001,1050],6) 
            dzbir =  suma_liste(bu,[1016,1049],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1050) kol. 6 = AOP-u (1016 + 1049) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10040
        if not( aop(bu,1051,5) == suma_liste(bu,[1052,1053,1057,1058,1059,1060,1061],5) ):
            lzbir =  aop(bu,1051,5) 
            dzbir =  suma_liste(bu,[1052,1053,1057,1058,1059,1060,1061],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1051 kol. 5 = AOP-u (1052 + 1053 + 1057 + 1058 + 1059 + 1060 + 1061) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10041
        if not( aop(bu,1051,6) == suma_liste(bu,[1052,1053,1057,1058,1059,1060,1061],6) ):
            lzbir =  aop(bu,1051,6) 
            dzbir =  suma_liste(bu,[1052,1053,1057,1058,1059,1060,1061],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1051 kol. 6 = AOP-u (1052 + 1053 + 1057 + 1058 + 1059 + 1060 + 1061) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10042
        if not( aop(bu,1053,5) == suma(bu,1054,1056,5) ):
            lzbir =  aop(bu,1053,5) 
            dzbir =  suma(bu,1054,1056,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1053 kol. 5 = AOP-u (1054 + 1055 + 1056) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10043
        if not( aop(bu,1053,6) == suma(bu,1054,1056,6) ):
            lzbir =  aop(bu,1053,6) 
            dzbir =  suma(bu,1054,1056,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1053 kol. 6 = AOP-u (1054 + 1055 + 1056) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10044
        if not( aop(bu,1062,5) == suma_liste(bu,[1063,1064,1067,1068,1069,1070],5) ):
            lzbir =  aop(bu,1062,5) 
            dzbir =  suma_liste(bu,[1063,1064,1067,1068,1069,1070],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1062 kol. 5 = AOP-u (1063 + 1064 + 1067 + 1068 + 1069 + 1070) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10045
        if not( aop(bu,1062,6) == suma_liste(bu,[1063,1064,1067,1068,1069,1070],6) ):
            lzbir =  aop(bu,1062,6) 
            dzbir =  suma_liste(bu,[1063,1064,1067,1068,1069,1070],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1062 kol. 6 = AOP-u (1063 + 1064 + 1067 + 1068 + 1069 + 1070) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10046
        if not( aop(bu,1064,5) == suma(bu,1065,1066,5) ):
            lzbir =  aop(bu,1064,5) 
            dzbir =  suma(bu,1065,1066,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1064 kol. 5 = AOP-u (1065 + 1066) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10047
        if not( aop(bu,1064,6) == suma(bu,1065,1066,6) ):
            lzbir =  aop(bu,1064,6) 
            dzbir =  suma(bu,1065,1066,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1064 kol. 6 = AOP-u (1065 + 1066) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10048
        if( aop(bu,1051,5) > aop(bu,1062,5) ):
            if not( aop(bu,1071,5) == aop(bu,1051,5)-aop(bu,1062,5) ):
                lzbir =  aop(bu,1071,5) 
                dzbir =  aop(bu,1051,5)-aop(bu,1062,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1071 kol. 5 = AOP-u (1051 - 1062) kol. 5, ako je AOP 1051 kol. 5 > AOP-a 1062 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10049
        if( aop(bu,1051,6) > aop(bu,1062,6) ):
            if not( aop(bu,1071,6) == aop(bu,1051,6)-aop(bu,1062,6) ):
                lzbir =  aop(bu,1071,6) 
                dzbir =  aop(bu,1051,6)-aop(bu,1062,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1071 kol. 6 = AOP-u (1051 - 1062) kol. 6, ako je AOP 1051 kol. 6 > AOP-a 1062 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10050
        if( aop(bu,1051,5) < aop(bu,1062,5) ):
            if not( aop(bu,1072,5) == aop(bu,1062,5)-aop(bu,1051,5) ):
                lzbir =  aop(bu,1072,5) 
                dzbir =  aop(bu,1062,5)-aop(bu,1051,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1072 kol. 5 = AOP-u (1062 - 1051) kol. 5, ako je AOP 1051 kol. 5 < AOP-a 1062 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10051
        if( aop(bu,1051,6) < aop(bu,1062,6) ):
            if not( aop(bu,1072,6) == aop(bu,1062,6)-aop(bu,1051,6) ):
                lzbir =  aop(bu,1072,6) 
                dzbir =  aop(bu,1062,6)-aop(bu,1051,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1072 kol. 6 = AOP-u (1062 - 1051) kol. 6, ako je AOP 1051 kol. 6 < AOP-a 1062 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10052
        if( aop(bu,1051,5) == aop(bu,1062,5) ):
            if not( suma(bu,1071,1072,5) == 0 ):
                lzbir =  suma(bu,1071,1072,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1071 + 1072) kol. 5 = 0,  ako je AOP 1051 kol. 5 = AOP-u 1062 kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10053
        if( aop(bu,1051,6) == aop(bu,1062,6) ):
            if not( suma(bu,1071,1072,6) == 0 ):
                lzbir =  suma(bu,1071,1072,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1071 + 1072) kol. 6 = 0,  ako je AOP 1051 kol. 6 = AOP-u 1062 kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10054
        if( aop(bu,1071,5) > 0 ):
            if not( aop(bu,1072,5) == 0 ):
                lzbir =  aop(bu,1072,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1071 kol. 5 > 0, onda je AOP 1072 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10055
        if( aop(bu,1072,5) > 0 ):
            if not( aop(bu,1071,5) == 0 ):
                lzbir =  aop(bu,1071,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je  AOP 1072 kol. 5 > 0, onda je AOP 1071 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10056
        if( aop(bu,1071,6) > 0 ):
            if not( aop(bu,1072,6) == 0 ):
                lzbir =  aop(bu,1072,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1071 kol. 6 > 0, onda je AOP 1072 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10057
        if( aop(bu,1072,6) > 0 ):
            if not( aop(bu,1071,6) == 0 ):
                lzbir =  aop(bu,1071,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1072 kol. 6 > 0, onda je AOP 1071 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10058
        if not( suma_liste(bu,[1051,1072],5) == suma_liste(bu,[1062,1071],5) ):
            lzbir =  suma_liste(bu,[1051,1072],5) 
            dzbir =  suma_liste(bu,[1062,1071],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1051 + 1072) kol. 5 = AOP-u (1062 + 1071) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10059
        if not( suma_liste(bu,[1051,1072],6) == suma_liste(bu,[1062,1071],6) ):
            lzbir =  suma_liste(bu,[1051,1072],6) 
            dzbir =  suma_liste(bu,[1062,1071],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1051 + 1072) kol. 6 = AOP-u (1062 + 1071) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10060
        if not( aop(bu,1073,5) == suma_liste(bu,[1074,1079,1084],5)-aop(bu,1085,5) ):
            lzbir =  aop(bu,1073,5) 
            dzbir =  suma_liste(bu,[1074,1079,1084],5)-aop(bu,1085,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1073 kol. 5 = AOP-u (1074 + 1079 + 1084 - 1085) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10061
        if not( aop(bu,1073,6) == suma_liste(bu,[1074,1079,1084],6)-aop(bu,1085,6) ):
            lzbir =  aop(bu,1073,6) 
            dzbir =  suma_liste(bu,[1074,1079,1084],6)-aop(bu,1085,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1073 kol. 6 = AOP-u (1074 + 1079 + 1084 - 1085) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10062
        if not( aop(bu,1074,5) == suma_liste(bu,[1075,1076,1078],5)-aop(bu,1077,5) ):
            lzbir =  aop(bu,1074,5) 
            dzbir =  suma_liste(bu,[1075,1076,1078],5)-aop(bu,1077,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1074 kol. 5 = AOP-u (1075 + 1076 - 1077 + 1078) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10063
        if not( aop(bu,1074,6) == suma_liste(bu,[1075,1076,1078],6)-aop(bu,1077,6) ):
            lzbir =  aop(bu,1074,6) 
            dzbir =  suma_liste(bu,[1075,1076,1078],6)-aop(bu,1077,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1074 kol. 6 = AOP-u (1075 + 1076 - 1077 + 1078) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10064
        if not( aop(bu,1079,5) == suma(bu,1080,1083,5) ):
            lzbir =  aop(bu,1079,5) 
            dzbir =  suma(bu,1080,1083,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1079 kol. 5 = AOP-u (1080 + 1081 + 1082 + 1083) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10065
        if not( aop(bu,1079,6) == suma(bu,1080,1083,6) ):
            lzbir =  aop(bu,1079,6) 
            dzbir =  suma(bu,1080,1083,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1079 kol. 6 = AOP-u (1080 + 1081 + 1082 + 1083) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10066
        if( suma_liste(bu,[1049,1071],5) > suma_liste(bu,[1050,1072,1073],5) ):
            if not( aop(bu,1086,5) == suma_liste(bu,[1049,1071],5)-suma_liste(bu,[1050,1072,1073],5) ):
                lzbir =  aop(bu,1086,5) 
                dzbir =  suma_liste(bu,[1049,1071],5)-suma_liste(bu,[1050,1072,1073],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1086 kol. 5 = AOP-u (1049 + 1071 - 1050 - 1072 - 1073) kol. 5, ako je AOP (1049 + 1071) kol. 5 > AOP-a (1050 + 1072 + 1073) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10067
        if( suma_liste(bu,[1049,1071],6) > suma_liste(bu,[1050,1072,1073],6) ):
            if not( aop(bu,1086,6) == suma_liste(bu,[1049,1071],6)-suma_liste(bu,[1050,1072,1073],6) ):
                lzbir =  aop(bu,1086,6) 
                dzbir =  suma_liste(bu,[1049,1071],6)-suma_liste(bu,[1050,1072,1073],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1086 kol. 6 = AOP-u (1049 + 1071 - 1050 - 1072 - 1073) kol. 6, ako je AOP (1049 + 1071) kol. 6 > AOP-a (1050 + 1072 + 1073) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10068
        if( suma_liste(bu,[1049,1071],5) < suma_liste(bu,[1050,1072,1073],5) ):
            if not( aop(bu,1087,5) == suma_liste(bu,[1050,1072,1073],5)-suma_liste(bu,[1049,1071],5) ):
                lzbir =  aop(bu,1087,5) 
                dzbir =  suma_liste(bu,[1050,1072,1073],5)-suma_liste(bu,[1049,1071],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1087 kol. 5 = AOP-u (1050 - 1049 - 1071 + 1072 + 1073) kol. 5, ako je AOP (1049 + 1071) kol. 5 < AOP-a (1050 + 1072 + 1073) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10069
        if( suma_liste(bu,[1049,1071],6) < suma_liste(bu,[1050,1072,1073],6) ):
            if not( aop(bu,1087,6) == suma_liste(bu,[1050,1072,1073],6)-suma_liste(bu,[1049,1071],6) ):
                lzbir =  aop(bu,1087,6) 
                dzbir =  suma_liste(bu,[1050,1072,1073],6)-suma_liste(bu,[1049,1071],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1087 kol. 6 = AOP-u (1050 - 1049 - 1071 + 1072 + 1073) kol. 6, ako je AOP (1049 + 1071) kol. 6 < AOP-a (1050 + 1072 + 1073) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10070
        if( suma_liste(bu,[1049,1071],5) == suma_liste(bu,[1050,1072,1073],5) ):
            if not( suma(bu,1086,1087,5) == 0 ):
                lzbir =  suma(bu,1086,1087,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1086 + 1087) kol. 5 = 0,  ako je AOP (1049 + 1071) kol. 5 = AOP-u (1050 + 1072 + 1073) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10071
        if( suma_liste(bu,[1049,1071],6) == suma_liste(bu,[1050,1072,1073],6) ):
            if not( suma(bu,1086,1087,6) == 0 ):
                lzbir =  suma(bu,1086,1087,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1086 + 1087) kol. 6 = 0,  ako je AOP (1049 + 1071) kol. 6 = AOP-u (1050 + 1072 + 1073) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10072
        if( aop(bu,1086,5) > 0 ):
            if not( aop(bu,1087,5) == 0 ):
                lzbir =  aop(bu,1087,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1086 kol. 5 > 0, onda je AOP 1087 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10073
        if( aop(bu,1087,5) > 0 ):
            if not( aop(bu,1086,5) == 0 ):
                lzbir =  aop(bu,1086,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1087 kol. 5 > 0, onda je AOP 1086 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10074
        if( aop(bu,1086,6) > 0 ):
            if not( aop(bu,1087,6) == 0 ):
                lzbir =  aop(bu,1087,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1086 kol. 6 > 0, onda je AOP 1087 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10075
        if( aop(bu,1087,6) > 0 ):
            if not( aop(bu,1086,6) == 0 ):
                lzbir =  aop(bu,1086,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1087 kol. 6 > 0, onda je AOP 1086 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10076
        if not( suma_liste(bu,[1049,1071,1087],5) == suma_liste(bu,[1050,1072,1073,1086],5) ):
            lzbir =  suma_liste(bu,[1049,1071,1087],5) 
            dzbir =  suma_liste(bu,[1050,1072,1073,1086],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1049 + 1071 + 1087) kol. 5 = AOP-u (1050 + 1072 + 1073 + 1086) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10077
        if not( suma_liste(bu,[1049,1071,1087],6) == suma_liste(bu,[1050,1072,1073,1086],6) ):
            lzbir =  suma_liste(bu,[1049,1071,1087],6) 
            dzbir =  suma_liste(bu,[1050,1072,1073,1086],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1049 + 1071 + 1087) kol. 6 = AOP-u (1050 + 1072 + 1073 + 1086) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10078
        if( suma_liste(bu,[1086,1088,1090,1092],5) > suma_liste(bu,[1087,1089,1091,1093],5) ):
            if not( aop(bu,1094,5) == suma_liste(bu,[1086,1088,1090,1092],5)-suma_liste(bu,[1087,1089,1091,1093],5) ):
                lzbir =  aop(bu,1094,5) 
                dzbir =  suma_liste(bu,[1086,1088,1090,1092],5)-suma_liste(bu,[1087,1089,1091,1093],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1094 kol. 5 = AOP-u (1086 + 1088 + 1090 + 1092 - 1087 - 1089 - 1091 - 1093) kol. 5, ako je AOP (1086 + 1088 + 1090 + 1092) kol. 5 > AOP-a (1087 + 1089 + 1091 + 1093) kol. 5   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10079
        if( suma_liste(bu,[1086,1088,1090,1092],6) > suma_liste(bu,[1087,1089,1091,1093],6) ):
            if not( aop(bu,1094,6) == suma_liste(bu,[1086,1088,1090,1092],6)-suma_liste(bu,[1087,1089,1091,1093],6) ):
                lzbir =  aop(bu,1094,6) 
                dzbir =  suma_liste(bu,[1086,1088,1090,1092],6)-suma_liste(bu,[1087,1089,1091,1093],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1094 kol. 6 = AOP-u (1086 + 1088 + 1090 + 1092 - 1087 - 1089 - 1091 - 1093) kol. 6, ako je AOP (1086 + 1088 + 1090 + 1092) kol. 6 > AOP-a (1087 + 1089 + 1091 + 1093) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10080
        if( suma_liste(bu,[1086,1088,1090,1092],5) < suma_liste(bu,[1087,1089,1091,1093],5) ):
            if not( aop(bu,1095,5) == suma_liste(bu,[1087,1089,1091,1093],5)-suma_liste(bu,[1086,1088,1090,1092],5) ):
                lzbir =  aop(bu,1095,5) 
                dzbir =  suma_liste(bu,[1087,1089,1091,1093],5)-suma_liste(bu,[1086,1088,1090,1092],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1095 kol. 5 = AOP-u (1087 + 1089 + 1091 + 1093 - 1086 - 1088 - 1090 - 1092) kol. 5, ako je AOP (1086 + 1088 + 1090 + 1092) kol. 5 < AOP-a (1087 + 1089 + 1091 + 1093) kol. 5   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10081
        if( suma_liste(bu,[1086,1088,1090,1092],6) < suma_liste(bu,[1087,1089,1091,1093],6) ):
            if not( aop(bu,1095,6) == suma_liste(bu,[1087,1089,1091,1093],6)-suma_liste(bu,[1086,1088,1090,1092],6) ):
                lzbir =  aop(bu,1095,6) 
                dzbir =  suma_liste(bu,[1087,1089,1091,1093],6)-suma_liste(bu,[1086,1088,1090,1092],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1095 kol. 6 = AOP-u (1087 + 1089 + 1091 + 1093 - 1086 - 1088 - 1090 - 1092 ) kol. 6, ako je AOP (1086 + 1088 + 1090 + 1092) kol. 6 < AOP-a (1087 + 1089 + 1091 + 1093) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10082
        if( suma_liste(bu,[1086,1088,1090,1092],5) == suma_liste(bu,[1087,1089,1091,1093],5) ):
            if not( suma(bu,1094,1095,5) == 0 ):
                lzbir =  suma(bu,1094,1095,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1094 + 1095) kol. 5 = 0, ako je AOP (1086 + 1088 + 1090 + 1092) kol. 5 = AOP-u (1087 + 1089 + 1091 + 1093) kol. 5  Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10083
        if( suma_liste(bu,[1086,1088,1090,1092],6) == suma_liste(bu,[1087,1089,1091,1093],6) ):
            if not( suma(bu,1094,1095,6) == 0 ):
                lzbir =  suma(bu,1094,1095,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1094 + 1095) kol. 6 = 0, ako je AOP (1086 + 1088 + 1090 + 1092) kol. 6 = AOP-u (1087 + 1089 + 1091 + 1093) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10084
        if( aop(bu,1094,5) > 0 ):
            if not( aop(bu,1095,5) == 0 ):
                lzbir =  aop(bu,1095,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1094 kol. 5 > 0, onda je AOP 1095 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10085
        if( aop(bu,1095,5) > 0 ):
            if not( aop(bu,1094,5) == 0 ):
                lzbir =  aop(bu,1094,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1095 kol. 5 > 0, onda je AOP 1094 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10086
        if( aop(bu,1094,6) > 0 ):
            if not( aop(bu,1095,6) == 0 ):
                lzbir =  aop(bu,1095,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1094 kol. 6 > 0, onda je AOP 1095 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10087
        if( aop(bu,1095,6) > 0 ):
            if not( aop(bu,1094,6) == 0 ):
                lzbir =  aop(bu,1094,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1095 kol. 6 > 0, onda je AOP 1094 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10088
        if not( suma_liste(bu,[1086,1088,1090,1092,1095],5) == suma_liste(bu,[1087,1089,1091,1093,1094],5) ):
            lzbir =  suma_liste(bu,[1086,1088,1090,1092,1095],5) 
            dzbir =  suma_liste(bu,[1087,1089,1091,1093,1094],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1086 + 1088 + 1090 + 1092 + 1095) kol. 5 = AOP-u (1087 + 1089 + 1091 + 1093 + 1094) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10089
        if not( suma_liste(bu,[1086,1088,1090,1092,1095],6) == suma_liste(bu,[1087,1089,1091,1093,1094],6) ):
            lzbir =  suma_liste(bu,[1086,1088,1090,1092,1095],6) 
            dzbir =  suma_liste(bu,[1087,1089,1091,1093,1094],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1086 + 1088 + 1090 + 1092 + 1095) kol. 6 = AOP-u (1087 + 1089 + 1091 + 1093 + 1094) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10090
        if( aop(bu,1096,5) > 0 ):
            if not( aop(bu,1097,5) == 0 ):
                lzbir =  aop(bu,1097,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1096 kol. 5 > 0, onda je AOP 1097 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10091
        if( aop(bu,1097,5) > 0 ):
            if not( aop(bu,1096,5) == 0 ):
                lzbir =  aop(bu,1096,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1097 kol. 5 > 0, onda je AOP 1096 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10092
        if( aop(bu,1096,6) > 0 ):
            if not( aop(bu,1097,6) == 0 ):
                lzbir =  aop(bu,1097,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1096 kol. 6 > 0, onda je AOP 1097 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10093
        if( aop(bu,1097,6) > 0 ):
            if not( aop(bu,1096,6) == 0 ):
                lzbir =  aop(bu,1096,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1097 kol. 6 > 0, onda je AOP 1096 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10094
        if( suma_liste(bu,[1094,1096],5) > suma_liste(bu,[1095,1097],5) ):
            if not( aop(bu,1098,5) == suma_liste(bu,[1094,1096],5)-suma_liste(bu,[1095,1097],5) ):
                lzbir =  aop(bu,1098,5) 
                dzbir =  suma_liste(bu,[1094,1096],5)-suma_liste(bu,[1095,1097],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1098 kol. 5 = AOP-u (1094 + 1096 - 1095 - 1097) kol. 5, ako je AOP (1094 + 1096) kol. 5 > AOP-a (1095 + 1097) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10095
        if( suma_liste(bu,[1094,1096],6) > suma_liste(bu,[1095,1097],6) ):
            if not( aop(bu,1098,6) == suma_liste(bu,[1094,1096],6)-suma_liste(bu,[1095,1097],6) ):
                lzbir =  aop(bu,1098,6) 
                dzbir =  suma_liste(bu,[1094,1096],6)-suma_liste(bu,[1095,1097],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1098 kol. 6 = AOP-u (1094 + 1096 - 1095 - 1097) kol. 6, ako je AOP (1094 + 1096) kol. 6 > AOP-a (1095 + 1097) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10096
        if( suma_liste(bu,[1094,1096],5) < suma_liste(bu,[1095,1097],5) ):
            if not( aop(bu,1099,5) == suma_liste(bu,[1095,1097],5)-suma_liste(bu,[1094,1096],5) ):
                lzbir =  aop(bu,1099,5) 
                dzbir =  suma_liste(bu,[1095,1097],5)-suma_liste(bu,[1094,1096],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1099 kol. 5 = AOP-u (1095 + 1097 - 1094 - 1096) kol. 5, ako je AOP (1094 + 1096) kol. 5 < AOP-a (1095 + 1097) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10097
        if( suma_liste(bu,[1094,1096],6) < suma_liste(bu,[1095,1097],6) ):
            if not( aop(bu,1099,6) == suma_liste(bu,[1095,1097],6)-suma_liste(bu,[1094,1096],6) ):
                lzbir =  aop(bu,1099,6) 
                dzbir =  suma_liste(bu,[1095,1097],6)-suma_liste(bu,[1094,1096],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1099 kol. 6 = AOP-u (1095 + 1097 - 1094 - 1096) kol. 6, ako je AOP (1094 + 1096) kol. 6 < AOP-a (1095 + 1097) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10098
        if( suma_liste(bu,[1094,1096],5) == suma_liste(bu,[1095,1097],5) ):
            if not( suma(bu,1098,1099,5) == 0 ):
                lzbir =  suma(bu,1098,1099,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1098 + 1099) kol. 5 = 0, ako je AOP (1094 + 1096) kol. 5 = AOP-u (1095 + 1097) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10099
        if( suma_liste(bu,[1094,1096],6) == suma_liste(bu,[1095,1097],6) ):
            if not( suma(bu,1098,1099,6) == 0 ):
                lzbir =  suma(bu,1098,1099,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1098 + 1099) kol. 6 = 0, ako je AOP (1094 + 1096) kol. 6 = AOP-u (1095 + 1097) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10100
        if( aop(bu,1098,5) > 0 ):
            if not( aop(bu,1099,5) == 0 ):
                lzbir =  aop(bu,1099,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1098 kol. 5 > 0, onda je AOP 1099 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10101
        if( aop(bu,1099,5) > 0 ):
            if not( aop(bu,1098,5) == 0 ):
                lzbir =  aop(bu,1098,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1099 kol. 5 > 0, onda je AOP 1098 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10102
        if( aop(bu,1098,6) > 0 ):
            if not( aop(bu,1099,6) == 0 ):
                lzbir =  aop(bu,1099,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1098 kol. 6 > 0, onda je AOP 1099 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10103
        if( aop(bu,1099,6) > 0 ):
            if not( aop(bu,1098,6) == 0 ):
                lzbir =  aop(bu,1098,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1099 kol. 6 > 0, onda je AOP 1098 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10104
        if not( suma_liste(bu,[1094,1096,1099],5) == suma_liste(bu,[1095,1097,1098],5) ):
            lzbir =  suma_liste(bu,[1094,1096,1099],5) 
            dzbir =  suma_liste(bu,[1095,1097,1098],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1094 + 1096 + 1099) kol. 5 = AOP-u (1095 + 1097 + 1098) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10105
        if not( suma_liste(bu,[1094,1096,1099],6) == suma_liste(bu,[1095,1097,1098],6) ):
            lzbir =  suma_liste(bu,[1094,1096,1099],6) 
            dzbir =  suma_liste(bu,[1095,1097,1098],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1094 + 1096 + 1099) kol. 6 = AOP-u (1095 + 1097 + 1098) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10106
        if( suma_liste(bu,[1098,1101],5) > suma_liste(bu,[1099,1100,1102],5) ):
            if not( aop(bu,1103,5) == suma_liste(bu,[1098,1101],5)-suma_liste(bu,[1099,1100,1102],5) ):
                lzbir =  aop(bu,1103,5) 
                dzbir =  suma_liste(bu,[1098,1101],5)-suma_liste(bu,[1099,1100,1102],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1103 kol. 5 = AOP-u (1098 - 1099 - 1100 + 1101 - 1102) kol. 5, ako je AOP (1098 + 1101) kol. 5 > AOP-a (1099 + 1100 + 1102) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10107
        if( suma_liste(bu,[1098,1101],6) > suma_liste(bu,[1099,1100,1102],6) ):
            if not( aop(bu,1103,6) == suma_liste(bu,[1098,1101],6)-suma_liste(bu,[1099,1100,1102],6) ):
                lzbir =  aop(bu,1103,6) 
                dzbir =  suma_liste(bu,[1098,1101],6)-suma_liste(bu,[1099,1100,1102],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1103 kol. 6 = AOP-u (1098 - 1099 - 1100 + 1101 - 1102) kol. 6, ako je AOP (1098 + 1101) kol. 6 > AOP-a (1099 + 1100 + 1102) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10108
        if( suma_liste(bu,[1098,1101],5) < suma_liste(bu,[1099,1100,1102],5) ):
            if not( aop(bu,1106,5) == suma_liste(bu,[1099,1100,1102],5)-suma_liste(bu,[1098,1101],5) ):
                lzbir =  aop(bu,1106,5) 
                dzbir =  suma_liste(bu,[1099,1100,1102],5)-suma_liste(bu,[1098,1101],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1106 kol. 5 = AOP-u (1099 - 1098 + 1100 - 1101 + 1102) kol. 5, ako je AOP (1098 + 1101) kol. 5 < AOP-a (1099 + 1100 + 1102) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10109
        if( suma_liste(bu,[1098,1101],6) < suma_liste(bu,[1099,1100,1102],6) ):
            if not( aop(bu,1106,6) == suma_liste(bu,[1099,1100,1102],6)-suma_liste(bu,[1098,1101],6) ):
                lzbir =  aop(bu,1106,6) 
                dzbir =  suma_liste(bu,[1099,1100,1102],6)-suma_liste(bu,[1098,1101],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1106 kol. 6 = AOP-u (1099 - 1098 + 1100 - 1101 + 1102) kol. 6, ako je AOP (1098 + 1101) kol. 6 < AOP-a (1099 + 1100 + 1102) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10110
        if( suma_liste(bu,[1098,1101],5) == suma_liste(bu,[1099,1100,1102],5) ):
            if not( suma_liste(bu,[1103,1106],5) == 0 ):
                lzbir =  suma_liste(bu,[1103,1106],5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1103 + 1106) kol. 5 = 0,  ako je AOP (1098 + 1101) kol. 5 = AOP-u (1099 + 1100 + 1102) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10111
        if( suma_liste(bu,[1098,1101],6) == suma_liste(bu,[1099,1100,1102],6) ):
            if not( suma_liste(bu,[1103,1106],6) == 0 ):
                lzbir =  suma_liste(bu,[1103,1106],6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1103 + 1106) kol. 6 = 0,  ako je AOP (1098 + 1101) kol. 6 = AOP-u (1099 + 1100 + 1102) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10112
        if( aop(bu,1103,5) > 0 ):
            if not( aop(bu,1106,5) == 0 ):
                lzbir =  aop(bu,1106,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1103 kol. 5 > 0, onda je AOP 1106 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10113
        if( aop(bu,1106,5) > 0 ):
            if not( aop(bu,1103,5) == 0 ):
                lzbir =  aop(bu,1103,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1106 kol. 5 > 0, onda je AOP 1103 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10114
        if( aop(bu,1103,6) > 0 ):
            if not( aop(bu,1106,6) == 0 ):
                lzbir =  aop(bu,1106,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1103 kol. 6 > 0, onda je AOP 1106 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10115
        if( aop(bu,1106,6) > 0 ):
            if not( aop(bu,1103,6) == 0 ):
                lzbir =  aop(bu,1103,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1106 kol. 6 > 0, onda je AOP 1103 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10116
        if not( suma_liste(bu,[1098,1101,1106],5) == suma_liste(bu,[1099,1100,1102,1103],5) ):
            lzbir =  suma_liste(bu,[1098,1101,1106],5) 
            dzbir =  suma_liste(bu,[1099,1100,1102,1103],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1098 + 1101 + 1106) kol. 5 = AOP-u (1099 + 1100 + 1102 + 1103) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10117
        if not( suma_liste(bu,[1098,1101,1106],6) == suma_liste(bu,[1099,1100,1102,1103],6) ):
            lzbir =  suma_liste(bu,[1098,1101,1106],6) 
            dzbir =  suma_liste(bu,[1099,1100,1102,1103],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1098 + 1101 + 1106) kol. 6 = AOP-u (1099 + 1100 + 1102 + 1103) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10118
        if( aop(bu,1103,5) > 0 ):
            if not( aop(bu,1103,5) == suma(bu,1104,1105,5)-suma(bu,1107,1108,5) ):
                lzbir =  aop(bu,1103,5) 
                dzbir =  suma(bu,1104,1105,5)-suma(bu,1107,1108,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1103 kol. 5 > 0, onda je AOP 1103 kol. 5 = AOP-u (1104 + 1105 - 1107 - 1108) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10119
        if( aop(bu,1103,6) > 0 ):
            if not( aop(bu,1103,6) == suma(bu,1104,1105,6)-suma(bu,1107,1108,6) ):
                lzbir =  aop(bu,1103,6) 
                dzbir =  suma(bu,1104,1105,6)-suma(bu,1107,1108,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1103 kol. 6 > 0, onda je AOP 1103 kol. 6 = AOP-u (1104 + 1105 - 1107 - 1108) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10120
        if( aop(bu,1106,5) > 0 ):
            if not( aop(bu,1106,5) == suma(bu,1107,1108,5)-suma(bu,1104,1105,5) ):
                lzbir =  aop(bu,1106,5) 
                dzbir =  suma(bu,1107,1108,5)-suma(bu,1104,1105,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1106 kol. 5 > 0, onda je AOP 1106 kol. 5 = AOP-u (1107 + 1108 - 1104 -1105) kol. 5   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10121
        if( aop(bu,1106,6) > 0 ):
            if not( aop(bu,1106,6) == suma(bu,1107,1108,6)-suma(bu,1104,1105,6) ):
                lzbir =  aop(bu,1106,6) 
                dzbir =  suma(bu,1107,1108,6)-suma(bu,1104,1105,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1106 kol. 6 > 0, onda je AOP 1106 kol. 6 = AOP-u (1107 + 1108 - 1104 -1105) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10122
        #Za ovaj set se ne primenjuje pravilo 
        
        #10123
        #Za ovaj set se ne primenjuje pravilo 
        
        #10124
        #Za ovaj set se ne primenjuje pravilo 
        
        #10125
        #Za ovaj set se ne primenjuje pravilo 
        
        #10126
        #Za ovaj set se ne primenjuje pravilo 
        
        #10127
        #Za ovaj set se ne primenjuje pravilo 
        
        #10128
        #Za ovaj set se ne primenjuje pravilo 
        
        #10129
        #Za ovaj set se ne primenjuje pravilo 
        
        #10130
        #Za ovaj set se ne primenjuje pravilo 
        
        #10131
        #Za ovaj set se ne primenjuje pravilo 
        
        #10132
        #Za ovaj set se ne primenjuje pravilo 
        
        #10133
        #Za ovaj set se ne primenjuje pravilo 
        
        #10134
        #Za ovaj set se ne primenjuje pravilo 
        
        #10135
        #Za ovaj set se ne primenjuje pravilo 
        
        #10136
        #Za ovaj set se ne primenjuje pravilo 
        
        #10137
        #Za ovaj set se ne primenjuje pravilo 
        
        #10138
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if( suma(bu,1001,1110,5) > 0 ):
                if not( suma(bu,1001,1110,5) != suma(bu,1001,1110,6) ):
                    
                    naziv_obrasca='Bilans uspeha'
                    poruka  ='***Ako je zbir podataka na oznakama za AOP (1001 do 1110) kol. 5 > 0 onda zbir podataka na oznakama za AOP (1001 do 1110) kol. 5 ≠ zbiru podataka na oznakama za AOP  (1001 do 1110) kol. 6 Zbirovi podataka u kolonama 5 i 6 bilansa uspeha su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama;  '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
        
        #IZVEŠTAJ O OSTALOM REZULTATU - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #20001
        if not( suma(ioor,2001,2031,5) > 0 ):
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='Zbir podataka na oznakama za AOP (2001 do 2031) kol. 5 > 0 Izveštaj o ostalom rezultatu, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #20002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(ioor,2001,2031,6) == 0 ):
                lzbir =  suma(ioor,2001,2031,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Zbir podataka na oznakama za AOP (2001 do 2031) kol. 6 = 0 Izveštaj o ostalom rezultatu za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(ioor,2001,2031,6) > 0 ):
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Zbir podataka na oznakama za AOP (2001 do 2031) kol. 6 > 0 Izveštaj o ostalom rezultatu, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #20004
        if not( aop(ioor,2001,5) == aop(bu,1103,5) ):
            lzbir =  aop(ioor,2001,5) 
            dzbir =  aop(bu,1103,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 2001 kol. 5 = AOP-u 1103 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2001 kol. 5 = AOP-u 1103 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20005
        if not( aop(ioor,2001,6) == aop(bu,1103,6) ):
            lzbir =  aop(ioor,2001,6) 
            dzbir =  aop(bu,1103,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 2001 kol. 6 = AOP-u 1103 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2001 kol. 6 = AOP-u 1103 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20006
        if not( aop(ioor,2002,5) == aop(bu,1106,5) ):
            lzbir =  aop(ioor,2002,5) 
            dzbir =  aop(bu,1106,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 2002 kol. 5 = AOP-u 1106 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2002 kol. 5 = AOP-u 1106 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20007
        if not( aop(ioor,2002,6) == aop(bu,1106,6) ):
            lzbir =  aop(ioor,2002,6) 
            dzbir =  aop(bu,1106,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 2002 kol. 6 = AOP-u 1106 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2002 kol. 6 = AOP-u 1106 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20008
        if not( aop(ioor,2021,5) == suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2019],5) ):
            lzbir =  aop(ioor,2021,5) 
            dzbir =  suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2019],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2021 kol. 5 = AOP-u (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017 + 2019) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20009
        if not( aop(ioor,2021,6) == suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2019],6) ):
            lzbir =  aop(ioor,2021,6) 
            dzbir =  suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2019],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2021 kol. 6 = AOP-u (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017 + 2019) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20010
        if not( aop(ioor,2022,5) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2020],5) ):
            lzbir =  aop(ioor,2022,5) 
            dzbir =  suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2020],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2022 kol. 5 = AOP-u (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018 + 2020) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20011
        if not( aop(ioor,2022,6) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2020],6) ):
            lzbir =  aop(ioor,2022,6) 
            dzbir =  suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2020],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2022 kol. 6 = AOP-u (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018 + 2020) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20012
        if( aop(ioor,2021,5) > suma(ioor,2022,2023,5) ):
            if not( aop(ioor,2024,5) == aop(ioor,2021,5)-suma(ioor,2022,2023,5) ):
                lzbir =  aop(ioor,2024,5) 
                dzbir =  aop(ioor,2021,5)-suma(ioor,2022,2023,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2024 kol. 5 = AOP-u (2021 - 2022 - 2023) kol. 5, ako je AOP 2021 kol. 5 > AOP-a (2022 + 2023) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20013
        if( aop(ioor,2021,6) > suma(ioor,2022,2023,6) ):
            if not( aop(ioor,2024,6) == aop(ioor,2021,6)-suma(ioor,2022,2023,6) ):
                lzbir =  aop(ioor,2024,6) 
                dzbir =  aop(ioor,2021,6)-suma(ioor,2022,2023,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2024 kol. 6 = AOP-u (2021 - 2022 - 2023) kol. 6, ako je AOP 2021 kol. 6 > AOP-a (2022 + 2023) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20014
        if( aop(ioor,2021,5) < suma(ioor,2022,2023,5) ):
            if not( aop(ioor,2025,5) == suma(ioor,2022,2023,5)-aop(ioor,2021,5) ):
                lzbir =  aop(ioor,2025,5) 
                dzbir =  suma(ioor,2022,2023,5)-aop(ioor,2021,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2025 kol. 5 = AOP-u (2022 - 2021 + 2023) kol. 5, ako je AOP 2021 kol. 5 < AOP-a (2022 + 2023) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20015
        if( aop(ioor,2021,6) < suma(ioor,2022,2023,6) ):
            if not( aop(ioor,2025,6) == suma(ioor,2022,2023,6)-aop(ioor,2021,6) ):
                lzbir =  aop(ioor,2025,6) 
                dzbir =  suma(ioor,2022,2023,6)-aop(ioor,2021,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2025 kol. 6 = AOP-u (2022 - 2021 + 2023) kol. 6, ako je AOP 2021 kol. 6 < AOP-a (2022 + 2023) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20016
        if( aop(ioor,2021,5) == suma(ioor,2022,2023,5) ):
            if not( suma(ioor,2024,2025,5) == 0 ):
                lzbir =  suma(ioor,2024,2025,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP (2024 + 2025) kol. 5 = 0, ako je AOP 2021 kol. 5 = AOP-u (2022 + 2023) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20017
        if( aop(ioor,2021,6) == suma(ioor,2022,2023,6) ):
            if not( suma(ioor,2024,2025,6) == 0 ):
                lzbir =  suma(ioor,2024,2025,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP (2024 + 2025) kol. 6 = 0, ako je AOP 2021 kol. 6 = AOP-u (2022 + 2023) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20018
        if( aop(ioor,2024,5) > 0 ):
            if not( aop(ioor,2025,5) == 0 ):
                lzbir =  aop(ioor,2025,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2024 kol. 5 > 0, onda je AOP 2025 kol. 5 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20019
        if( aop(ioor,2025,5) > 0 ):
            if not( aop(ioor,2024,5) == 0 ):
                lzbir =  aop(ioor,2024,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2025 kol. 5 > 0, onda je AOP 2024 kol. 5 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20020
        if( aop(ioor,2024,6) > 0 ):
            if not( aop(ioor,2025,6) == 0 ):
                lzbir =  aop(ioor,2025,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2024 kol. 6 > 0, onda je AOP 2025 kol. 6 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20021
        if( aop(ioor,2025,6) > 0 ):
            if not( aop(ioor,2024,6) == 0 ):
                lzbir =  aop(ioor,2024,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2025 kol. 6 > 0, onda je AOP 2024 kol. 6 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20022
        if not( suma_liste(ioor,[2021,2025],5) == suma(ioor,2022,2024,5) ):
            lzbir =  suma_liste(ioor,[2021,2025],5) 
            dzbir =  suma(ioor,2022,2024,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP (2021 + 2025) kol. 5 = AOP-u (2022 + 2023 + 2024) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20023
        if not( suma_liste(ioor,[2021,2025],6) == suma(ioor,2022,2024,6) ):
            lzbir =  suma_liste(ioor,[2021,2025],6) 
            dzbir =  suma(ioor,2022,2024,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP (2021 + 2025) kol. 6 = AOP-u (2022 + 2023 + 2024) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20024
        if( suma_liste(ioor,[2001,2024],5) > suma_liste(ioor,[2002,2025],5) ):
            if not( aop(ioor,2026,5) == suma_liste(ioor,[2001,2024],5)-suma_liste(ioor,[2002,2025],5) ):
                lzbir =  aop(ioor,2026,5) 
                dzbir =  suma_liste(ioor,[2001,2024],5)-suma_liste(ioor,[2002,2025],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2026 kol. 5 = AOP-u (2001 + 2024 - 2002 - 2025) kol. 5, ako je AOP (2001 + 2024) kol. 5 > AOP-a (2002 + 2025) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20025
        if( suma_liste(ioor,[2001,2024],6) > suma_liste(ioor,[2002,2025],6) ):
            if not( aop(ioor,2026,6) == suma_liste(ioor,[2001,2024],6)-suma_liste(ioor,[2002,2025],6) ):
                lzbir =  aop(ioor,2026,6) 
                dzbir =  suma_liste(ioor,[2001,2024],6)-suma_liste(ioor,[2002,2025],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2026 kol. 6 = AOP-u (2001 + 2024 - 2002 - 2025) kol. 6, ako je AOP (2001 + 2024) kol. 6 > AOP-a (2002 + 2025) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20026
        if( suma_liste(ioor,[2001,2024],5) < suma_liste(ioor,[2002,2025],5) ):
            if not( aop(ioor,2029,5) == suma_liste(ioor,[2002,2025],5)-suma_liste(ioor,[2001,2024],5) ):
                lzbir =  aop(ioor,2029,5) 
                dzbir =  suma_liste(ioor,[2002,2025],5)-suma_liste(ioor,[2001,2024],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2029 kol. 5 = AOP-u (2002 - 2001 - 2024 + 2025) kol. 5, ako je AOP (2001 + 2024) kol. 5 < AOP-a (2002 + 2025) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20027
        if( suma_liste(ioor,[2001,2024],6) < suma_liste(ioor,[2002,2025],6) ):
            if not( aop(ioor,2029,6) == suma_liste(ioor,[2002,2025],6)-suma_liste(ioor,[2001,2024],6) ):
                lzbir =  aop(ioor,2029,6) 
                dzbir =  suma_liste(ioor,[2002,2025],6)-suma_liste(ioor,[2001,2024],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2029 kol. 6 = AOP-u (2002 - 2001 - 2024 + 2025) kol. 6, ako je AOP (2001 + 2024) kol. 6 < AOP-a (2002 + 2025) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20028
        if( suma_liste(ioor,[2001,2024],5) == suma_liste(ioor,[2002,2025],5) ):
            if not( suma_liste(ioor,[2026,2029],5) == 0 ):
                lzbir =  suma_liste(ioor,[2026,2029],5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP (2026 + 2029) kol. 5 = 0, ako je AOP (2001 + 2024) kol. 5 = AOP-u (2002 + 2025) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20029
        if( suma_liste(ioor,[2001,2024],6) == suma_liste(ioor,[2002,2025],6) ):
            if not( suma_liste(ioor,[2026,2029],6) == 0 ):
                lzbir =  suma_liste(ioor,[2026,2029],6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP (2026 + 2029) kol. 6 = 0, ako je AOP (2001 + 2024) kol. 6 = AOP-u (2002 + 2025) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20030
        if( aop(ioor,2026,5) > 0 ):
            if not( aop(ioor,2029,5) == 0 ):
                lzbir =  aop(ioor,2029,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2026 kol. 5 > 0, onda je AOP 2029 kol. 5 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20031
        if( aop(ioor,2029,5) > 0 ):
            if not( aop(ioor,2026,5) == 0 ):
                lzbir =  aop(ioor,2026,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2029 kol. 5 > 0, onda je AOP 2026 kol. 5 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20032
        if( aop(ioor,2026,6) > 0 ):
            if not( aop(ioor,2029,6) == 0 ):
                lzbir =  aop(ioor,2029,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2026 kol. 6 > 0, onda je AOP 2029 kol. 6 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20033
        if( aop(ioor,2029,6) > 0 ):
            if not( aop(ioor,2026,6) == 0 ):
                lzbir =  aop(ioor,2026,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2029 kol. 6 > 0, onda je AOP 2026 kol. 6 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20034
        if not( suma_liste(ioor,[2001,2024,2029],5) == suma_liste(ioor,[2002,2025,2026],5) ):
            lzbir =  suma_liste(ioor,[2001,2024,2029],5) 
            dzbir =  suma_liste(ioor,[2002,2025,2026],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP (2001 + 2024 + 2029) kol. 5 = AOP-u (2002 + 2025 + 2026) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20035
        if not( suma_liste(ioor,[2001,2024,2029],6) == suma_liste(ioor,[2002,2025,2026],6) ):
            lzbir =  suma_liste(ioor,[2001,2024,2029],6) 
            dzbir =  suma_liste(ioor,[2002,2025,2026],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP (2001 + 2024 + 2029) kol. 6 = AOP-u (2002 + 2025 + 2026) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20036
        if( aop(ioor,2026,5) > 0 ):
            if not( aop(ioor,2026,5) == suma(ioor,2027,2028,5)-suma(ioor,2030,2031,5) ):
                lzbir =  aop(ioor,2026,5) 
                dzbir =  suma(ioor,2027,2028,5)-suma(ioor,2030,2031,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2026 kol. 5 > 0, onda je AOP 2026 kol. 5 = AOP-u (2027 + 2028 - 2030 - 2031) kol. 5   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20037
        if( aop(ioor,2026,6) > 0 ):
            if not( aop(ioor,2026,6) == suma(ioor,2027,2028,6)-suma(ioor,2030,2031,6) ):
                lzbir =  aop(ioor,2026,6) 
                dzbir =  suma(ioor,2027,2028,6)-suma(ioor,2030,2031,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2026 kol. 6 > 0, onda je AOP 2026 kol. 6 = AOP-u (2027 + 2028 - 2030 - 2031) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20038
        if( aop(ioor,2029,5) > 0 ):
            if not( aop(ioor,2029,5) == suma(ioor,2030,2031,5)-suma(ioor,2027,2028,5) ):
                lzbir =  aop(ioor,2029,5) 
                dzbir =  suma(ioor,2030,2031,5)-suma(ioor,2027,2028,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2029 kol. 5 > 0, onda je AOP 2029 kol. 5 = AOP-u (2030 + 2031 - 2027 - 2028) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20039
        if( aop(ioor,2029,6) > 0 ):
            if not( aop(ioor,2029,6) == suma(ioor,2030,2031,6)-suma(ioor,2027,2028,6) ):
                lzbir =  aop(ioor,2029,6) 
                dzbir =  suma(ioor,2030,2031,6)-suma(ioor,2027,2028,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2029 kol. 6 > 0, onda je AOP 2029 kol. 6 = AOP-u (2030 + 2031 - 2027 - 2028) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        
        #IZVEŠTAJ O TOKOVIMA GOTOVINE - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #30001
        if not( suma(iotg,3001,3054,3) > 0 ):
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='Zbir podataka na oznakama za AOP (3001 do 3054) kol. 3 > 0 Izveštaj o tokovima gotovine, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #30002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(iotg,3001,3054,4) == 0 ):
                lzbir =  suma(iotg,3001,3054,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Zbir podataka na oznakama za AOP (3001 do 3054) kol. 4 = 0 Izveštaj o tokovima gotovine za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(iotg,3001,3054,4) > 0 ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Zbir podataka na oznakama za AOP (3001 do 3054) kol. 4 > 0 Izveštaj o tokovima gotovine, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #30004
        if not( aop(iotg,3001,3) == suma(iotg,3002,3006,3) ):
            lzbir =  aop(iotg,3001,3) 
            dzbir =  suma(iotg,3002,3006,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3001 kol. 3 = AOP-u (3002 + 3003 + 3004 + 3005 + 3006) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30005
        if not( aop(iotg,3001,4) == suma(iotg,3002,3006,4) ):
            lzbir =  aop(iotg,3001,4) 
            dzbir =  suma(iotg,3002,3006,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3001 kol. 4 = AOP-u (3002 + 3003 + 3004 + 3005 + 3006) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30006
        if not( aop(iotg,3007,3) == suma(iotg,3008,3016,3) ):
            lzbir =  aop(iotg,3007,3) 
            dzbir =  suma(iotg,3008,3016,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3007 kol. 3 = AOP-u (3008 + 3009 + 3010 + 3011 + 3012 + 3013 + 3014 + 3015 + 3016) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30007
        if not( aop(iotg,3007,4) == suma(iotg,3008,3016,4) ):
            lzbir =  aop(iotg,3007,4) 
            dzbir =  suma(iotg,3008,3016,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3007 kol. 4 = AOP-u (3008 + 3009 + 3010 + 3011 + 3012 + 3013 + 3014 + 3015 + 3016) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30008
        if( aop(iotg,3001,3) > aop(iotg,3007,3) ):
            if not( aop(iotg,3017,3) == aop(iotg,3001,3)-aop(iotg,3007,3) ):
                lzbir =  aop(iotg,3017,3) 
                dzbir =  aop(iotg,3001,3)-aop(iotg,3007,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  =' AOP 3017 kol. 3 = AOP-u (3001 - 3007) kol. 3, ako je AOP 3001 kol. 3 > AOP-a 3007 kol. 3   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30009
        if( aop(iotg,3001,4) > aop(iotg,3007,4) ):
            if not( aop(iotg,3017,4) == aop(iotg,3001,4)-aop(iotg,3007,4) ):
                lzbir =  aop(iotg,3017,4) 
                dzbir =  aop(iotg,3001,4)-aop(iotg,3007,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  =' AOP 3017 kol. 4 = AOP-u (3001 - 3007) kol. 4, ako je AOP 3001 kol. 4 > AOP-a 3007 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30010
        if( aop(iotg,3001,3) < aop(iotg,3007,3) ):
            if not( aop(iotg,3018,3) == aop(iotg,3007,3)-aop(iotg,3001,3) ):
                lzbir =  aop(iotg,3018,3) 
                dzbir =  aop(iotg,3007,3)-aop(iotg,3001,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3018 kol. 3 = AOP-u (3007 - 3001) kol. 3, ako je AOP 3001 kol. 3 < AOP-a 3007 kol. 3    '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30011
        if( aop(iotg,3001,4) < aop(iotg,3007,4) ):
            if not( aop(iotg,3018,4) == aop(iotg,3007,4)-aop(iotg,3001,4) ):
                lzbir =  aop(iotg,3018,4) 
                dzbir =  aop(iotg,3007,4)-aop(iotg,3001,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3018 kol. 4 = AOP-u (3007 - 3001) kol. 4, ako je AOP 3001 kol. 4 < AOP-a 3007 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30012
        if( aop(iotg,3001,3) == aop(iotg,3007,3) ):
            if not( suma(iotg,3017,3018,3) == 0 ):
                lzbir =  suma(iotg,3017,3018,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3017 + 3018) kol. 3 = 0, ako je AOP 3001 kol. 3 = AOP-u 3007 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30013
        if( aop(iotg,3001,4) == aop(iotg,3007,4) ):
            if not( suma(iotg,3017,3018,4) == 0 ):
                lzbir =  suma(iotg,3017,3018,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3017 + 3018) kol. 4 = 0, ako je AOP 3001 kol. 4 = AOP-u 3007 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30014
        if( aop(iotg,3017,3) > 0 ):
            if not( aop(iotg,3018,3) == 0 ):
                lzbir =  aop(iotg,3018,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3017 kol. 3 > 0 onda je AOP 3018 kol. 3 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30015
        if( aop(iotg,3018,3) > 0 ):
            if not( aop(iotg,3017,3) == 0 ):
                lzbir =  aop(iotg,3017,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3018 kol. 3 > 0 onda je AOP 3017 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30016
        if( aop(iotg,3017,4) > 0 ):
            if not( aop(iotg,3018,4) == 0 ):
                lzbir =  aop(iotg,3018,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3017 kol. 4 > 0 onda je AOP 3018 kol. 4 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30017
        if( aop(iotg,3018,4) > 0 ):
            if not( aop(iotg,3017,4) == 0 ):
                lzbir =  aop(iotg,3017,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3018 kol. 4 > 0 onda je AOP 3017 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30018
        if not( suma_liste(iotg,[3001,3018],3) == suma_liste(iotg,[3007,3017],3) ):
            lzbir =  suma_liste(iotg,[3001,3018],3) 
            dzbir =  suma_liste(iotg,[3007,3017],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3001 + 3018) kol. 3 = AOP-u (3007 + 3017) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30019
        if not( suma_liste(iotg,[3001,3018],4) == suma_liste(iotg,[3007,3017],4) ):
            lzbir =  suma_liste(iotg,[3001,3018],4) 
            dzbir =  suma_liste(iotg,[3007,3017],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3001 + 3018) kol. 4 = AOP-u (3007 + 3017) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30020
        if not( aop(iotg,3019,3) == suma(iotg,3020,3024,3) ):
            lzbir =  aop(iotg,3019,3) 
            dzbir =  suma(iotg,3020,3024,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3019 kol. 3 = AOP-u (3020 + 3021 + 3022 + 3023 + 3024) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30021
        if not( aop(iotg,3019,4) == suma(iotg,3020,3024,4) ):
            lzbir =  aop(iotg,3019,4) 
            dzbir =  suma(iotg,3020,3024,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3019 kol. 4 = AOP-u (3020 + 3021 + 3022 + 3023 + 3024) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30022
        if not( aop(iotg,3025,3) == suma(iotg,3026,3028,3) ):
            lzbir =  aop(iotg,3025,3) 
            dzbir =  suma(iotg,3026,3028,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3025 kol. 3 = AOP-u (3026 + 3027 + 3028) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30023
        if not( aop(iotg,3025,4) == suma(iotg,3026,3028,4) ):
            lzbir =  aop(iotg,3025,4) 
            dzbir =  suma(iotg,3026,3028,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3025 kol. 4 = AOP-u (3026 + 3027 + 3028) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30024
        if( aop(iotg,3019,3) > aop(iotg,3025,3) ):
            if not( aop(iotg,3029,3) == aop(iotg,3019,3)-aop(iotg,3025,3) ):
                lzbir =  aop(iotg,3029,3) 
                dzbir =  aop(iotg,3019,3)-aop(iotg,3025,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3029 kol. 3 = AOP-u (3019 - 3025) kol. 3, ako je AOP 3019 kol. 3 > AOP-a 3025 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30025
        if( aop(iotg,3019,4) > aop(iotg,3025,4) ):
            if not( aop(iotg,3029,4) == aop(iotg,3019,4)-aop(iotg,3025,4) ):
                lzbir =  aop(iotg,3029,4) 
                dzbir =  aop(iotg,3019,4)-aop(iotg,3025,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3029 kol. 4 = AOP-u (3019 - 3025) kol. 4, ako je AOP 3019 kol. 4 > AOP-a 3025 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30026
        if( aop(iotg,3019,3) < aop(iotg,3025,3) ):
            if not( aop(iotg,3030,3) == aop(iotg,3025,3)-aop(iotg,3019,3) ):
                lzbir =  aop(iotg,3030,3) 
                dzbir =  aop(iotg,3025,3)-aop(iotg,3019,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3030 kol. 3 = AOP-u (3025 - 3019) kol. 3,ako je AOP 3019 kol. 3 < AOP-a 3025 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30027
        if( aop(iotg,3019,4) < aop(iotg,3025,4) ):
            if not( aop(iotg,3030,4) == aop(iotg,3025,4)-aop(iotg,3019,4) ):
                lzbir =  aop(iotg,3030,4) 
                dzbir =  aop(iotg,3025,4)-aop(iotg,3019,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3030 kol. 4 = AOP-u (3025 - 3019) kol. 4,ako je AOP 3019 kol. 4 < AOP-a 3025 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30028
        if( aop(iotg,3019,3) == aop(iotg,3025,3) ):
            if not( suma(iotg,3029,3030,3) == 0 ):
                lzbir =  suma(iotg,3029,3030,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3029 + 3030) kol. 3 = 0, ako je AOP 3019 kol. 3 = AOP-u 3025 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30029
        if( aop(iotg,3019,4) == aop(iotg,3025,4) ):
            if not( suma(iotg,3029,3030,4) == 0 ):
                lzbir =  suma(iotg,3029,3030,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3029 + 3030) kol. 4 = 0, ako je AOP 3019 kol. 4 = AOP-u 3025 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30030
        if( aop(iotg,3029,3) > 0 ):
            if not( aop(iotg,3030,3) == 0 ):
                lzbir =  aop(iotg,3030,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3029 kol. 3 > 0 onda je AOP 3030 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30031
        if( aop(iotg,3030,3) > 0 ):
            if not( aop(iotg,3029,3) == 0 ):
                lzbir =  aop(iotg,3029,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3030 kol. 3 > 0 onda je AOP 3029 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30032
        if( aop(iotg,3029,4) > 0 ):
            if not( aop(iotg,3030,4) == 0 ):
                lzbir =  aop(iotg,3030,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3029 kol. 4 > 0 onda je AOP 3030 kol. 4 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30033
        if( aop(iotg,3030,4) > 0 ):
            if not( aop(iotg,3029,4) == 0 ):
                lzbir =  aop(iotg,3029,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3030 kol. 4 > 0 onda je AOP 3029 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30034
        if not( suma_liste(iotg,[3019,3030],3) == suma_liste(iotg,[3025,3029],3) ):
            lzbir =  suma_liste(iotg,[3019,3030],3) 
            dzbir =  suma_liste(iotg,[3025,3029],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3019 + 3030) kol. 3 = AOP-u (3025 + 3029) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30035
        if not( suma_liste(iotg,[3019,3030],4) == suma_liste(iotg,[3025,3029],4) ):
            lzbir =  suma_liste(iotg,[3019,3030],4) 
            dzbir =  suma_liste(iotg,[3025,3029],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3019 + 3030) kol. 4 = AOP-u (3025 + 3029) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30036
        if not( aop(iotg,3031,3) == suma(iotg,3032,3036,3) ):
            lzbir =  aop(iotg,3031,3) 
            dzbir =  suma(iotg,3032,3036,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3031 kol. 3 = AOP-u (3032 + 3033 + 3034 + 3035 + 3036) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30037
        if not( aop(iotg,3031,4) == suma(iotg,3032,3036,4) ):
            lzbir =  aop(iotg,3031,4) 
            dzbir =  suma(iotg,3032,3036,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3031 kol. 4 = AOP-u (3032 + 3033 + 3034 + 3035 + 3036) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30038
        if not( aop(iotg,3037,3) == suma(iotg,3038,3044,3) ):
            lzbir =  aop(iotg,3037,3) 
            dzbir =  suma(iotg,3038,3044,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3037 kol. 3 = AOP-u (3038 + 3039 + 3040 + 3041 + 3042 + 3043 + 3044) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30039
        if not( aop(iotg,3037,4) == suma(iotg,3038,3044,4) ):
            lzbir =  aop(iotg,3037,4) 
            dzbir =  suma(iotg,3038,3044,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3037 kol. 4 = AOP-u (3038 + 3039 + 3040 + 3041 + 3042 + 3043 + 3044) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30040
        if( aop(iotg,3031,3) > aop(iotg,3037,3) ):
            if not( aop(iotg,3045,3) == aop(iotg,3031,3)-aop(iotg,3037,3) ):
                lzbir =  aop(iotg,3045,3) 
                dzbir =  aop(iotg,3031,3)-aop(iotg,3037,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3045 kol. 3 = AOP-u (3031 - 3037) kol. 3, ako je AOP 3031 kol. 3 > AOP-a 3037 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30041
        if( aop(iotg,3031,4) > aop(iotg,3037,4) ):
            if not( aop(iotg,3045,4) == aop(iotg,3031,4)-aop(iotg,3037,4) ):
                lzbir =  aop(iotg,3045,4) 
                dzbir =  aop(iotg,3031,4)-aop(iotg,3037,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3045 kol. 4 = AOP-u (3031 - 3037) kol. 4, ako je AOP 3031 kol. 4 > AOP-a 3037 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30042
        if( aop(iotg,3031,3) < aop(iotg,3037,3) ):
            if not( aop(iotg,3046,3) == aop(iotg,3037,3)-aop(iotg,3031,3) ):
                lzbir =  aop(iotg,3046,3) 
                dzbir =  aop(iotg,3037,3)-aop(iotg,3031,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3046 kol. 3 = AOP-u (3037 - 3031) kol. 3, ako je AOP 3031 kol. 3 < AOP-a 3037 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30043
        if( aop(iotg,3031,4) < aop(iotg,3037,4) ):
            if not( aop(iotg,3046,4) == aop(iotg,3037,4)-aop(iotg,3031,4) ):
                lzbir =  aop(iotg,3046,4) 
                dzbir =  aop(iotg,3037,4)-aop(iotg,3031,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3046 kol. 4 = AOP-u (3037 - 3031) kol. 4, ako je AOP 3031 kol. 4 < AOP-a 3037 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30044
        if( aop(iotg,3031,3) == aop(iotg,3037,3) ):
            if not( suma(iotg,3045,3046,3) == 0 ):
                lzbir =  suma(iotg,3045,3046,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3045 + 3046) kol. 3 = 0, ako je AOP 3031 kol. 3 = AOP-u 3037 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30045
        if( aop(iotg,3031,4) == aop(iotg,3037,4) ):
            if not( suma(iotg,3045,3046,4) == 0 ):
                lzbir =  suma(iotg,3045,3046,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3045 + 3046) kol. 4 = 0, ako je AOP 3031 kol. 4 = AOP-u 3037 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30046
        if( aop(iotg,3045,3) > 0 ):
            if not( aop(iotg,3046,3) == 0 ):
                lzbir =  aop(iotg,3046,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3045 kol. 3 > 0 onda je AOP 3046 kol. 3 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30047
        if( aop(iotg,3046,3) > 0 ):
            if not( aop(iotg,3045,3) == 0 ):
                lzbir =  aop(iotg,3045,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3046 kol. 3 > 0 onda je AOP 3045 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30048
        if( aop(iotg,3045,4) > 0 ):
            if not( aop(iotg,3046,4) == 0 ):
                lzbir =  aop(iotg,3046,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3045 kol. 4 > 0 onda je AOP 3046 kol. 4 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30049
        if( aop(iotg,3046,4) > 0 ):
            if not( aop(iotg,3045,4) == 0 ):
                lzbir =  aop(iotg,3045,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3046 kol. 4 > 0 onda je AOP 3045 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30050
        if not( suma_liste(iotg,[3031,3046],3) == suma_liste(iotg,[3037,3045],3) ):
            lzbir =  suma_liste(iotg,[3031,3046],3) 
            dzbir =  suma_liste(iotg,[3037,3045],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3031 + 3046) kol. 3 = AOP-u (3037 + 3045) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30051
        if not( suma_liste(iotg,[3031,3046],4) == suma_liste(iotg,[3037,3045],4) ):
            lzbir =  suma_liste(iotg,[3031,3046],4) 
            dzbir =  suma_liste(iotg,[3037,3045],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3031 + 3046) kol. 4 = AOP-u (3037 + 3045) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30052
        if not( aop(iotg,3047,3) == suma_liste(iotg,[3001,3019,3031],3) ):
            lzbir =  aop(iotg,3047,3) 
            dzbir =  suma_liste(iotg,[3001,3019,3031],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3047 kol. 3 = AOP-u (3001 + 3019 + 3031) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30053
        if not( aop(iotg,3047,4) == suma_liste(iotg,[3001,3019,3031],4) ):
            lzbir =  aop(iotg,3047,4) 
            dzbir =  suma_liste(iotg,[3001,3019,3031],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3047 kol. 4 = AOP-u (3001 + 3019 + 3031) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30054
        if not( aop(iotg,3048,3) == suma_liste(iotg,[3007,3025,3037],3) ):
            lzbir =  aop(iotg,3048,3) 
            dzbir =  suma_liste(iotg,[3007,3025,3037],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3048 kol. 3 = AOP-u (3007 + 3025 + 3037) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30055
        if not( aop(iotg,3048,4) == suma_liste(iotg,[3007,3025,3037],4) ):
            lzbir =  aop(iotg,3048,4) 
            dzbir =  suma_liste(iotg,[3007,3025,3037],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3048 kol. 4 = AOP-u (3007 + 3025 + 3037) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30056
        if( aop(iotg,3047,3) > aop(iotg,3048,3) ):
            if not( aop(iotg,3049,3) == aop(iotg,3047,3)-aop(iotg,3048,3) ):
                lzbir =  aop(iotg,3049,3) 
                dzbir =  aop(iotg,3047,3)-aop(iotg,3048,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3049 kol. 3 = AOP-u (3047 - 3048) kol. 3, ako je AOP 3047 kol. 3 > AOP-a 3048 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30057
        if( aop(iotg,3047,4) > aop(iotg,3048,4) ):
            if not( aop(iotg,3049,4) == aop(iotg,3047,4)-aop(iotg,3048,4) ):
                lzbir =  aop(iotg,3049,4) 
                dzbir =  aop(iotg,3047,4)-aop(iotg,3048,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3049 kol. 4 = AOP-u (3047 - 3048) kol. 4, ako je AOP 3047 kol. 4 > AOP-a 3048 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30058
        if( aop(iotg,3047,3) < aop(iotg,3048,3) ):
            if not( aop(iotg,3050,3) == aop(iotg,3048,3)-aop(iotg,3047,3) ):
                lzbir =  aop(iotg,3050,3) 
                dzbir =  aop(iotg,3048,3)-aop(iotg,3047,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3050 kol. 3 = AOP-u (3048 - 3047) kol. 3,  ako je AOP 3047 kol. 3 < AOP-a 3048 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30059
        if( aop(iotg,3047,4) < aop(iotg,3048,4) ):
            if not( aop(iotg,3050,4) == aop(iotg,3048,4)-aop(iotg,3047,4) ):
                lzbir =  aop(iotg,3050,4) 
                dzbir =  aop(iotg,3048,4)-aop(iotg,3047,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3050 kol. 4 = AOP-u (3048 - 3047) kol. 4,  ako je AOP 3047 kol. 4 < AOP-a 3048 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30060
        if( aop(iotg,3047,3) == aop(iotg,3048,3) ):
            if not( suma(iotg,3049,3050,3) == 0 ):
                lzbir =  suma(iotg,3049,3050,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3049 + 3050) kol. 3 = 0, ako je AOP 3047 kol. 3 = AOP-u 3048 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30061
        if( aop(iotg,3047,4) == aop(iotg,3048,4) ):
            if not( suma(iotg,3049,3050,4) == 0 ):
                lzbir =  suma(iotg,3049,3050,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3049 + 3050) kol. 4 = 0, ako je AOP 3047 kol. 4 = AOP-u 3048 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30062
        if( aop(iotg,3049,3) > 0 ):
            if not( aop(iotg,3050,3) == 0 ):
                lzbir =  aop(iotg,3050,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3049 kol. 3 > 0 onda je AOP 3050 kol. 3 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30063
        if( aop(iotg,3050,3) > 0 ):
            if not( aop(iotg,3049,3) == 0 ):
                lzbir =  aop(iotg,3049,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3050 kol. 3 > 0 onda je AOP 3049 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30064
        if( aop(iotg,3049,4) > 0 ):
            if not( aop(iotg,3050,4) == 0 ):
                lzbir =  aop(iotg,3050,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3049 kol. 4 > 0 onda je AOP 3050 kol. 4 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30065
        if( aop(iotg,3050,4) > 0 ):
            if not( aop(iotg,3049,4) == 0 ):
                lzbir =  aop(iotg,3049,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3050 kol. 4 > 0 onda je AOP 3049 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30066
        if not( suma_liste(iotg,[3047,3050],3) == suma(iotg,3048,3049,3) ):
            lzbir =  suma_liste(iotg,[3047,3050],3) 
            dzbir =  suma(iotg,3048,3049,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3047 + 3050) kol. 3 = AOP-u (3048 + 3049) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30067
        if not( suma_liste(iotg,[3047,3050],4) == suma(iotg,3048,3049,4) ):
            lzbir =  suma_liste(iotg,[3047,3050],4) 
            dzbir =  suma(iotg,3048,3049,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3047 + 3050) kol. 4 = AOP-u (3048 + 3049) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30068
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( aop(iotg,3051,3) == 0 ):
                lzbir =  aop(iotg,3051,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3051 kol. 3 = 0 Novoosnovana pravna lica ne smeju imati prikazan podatak za prethodnu godinu '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30069
        if( suma_liste(iotg,[3049,3051,3052],3) > suma_liste(iotg,[3050,3053],3) ):
            if not( aop(iotg,3054,3) == suma_liste(iotg,[3049,3051,3052],3)-suma_liste(iotg,[3050,3053],3) ):
                lzbir =  aop(iotg,3054,3) 
                dzbir =  suma_liste(iotg,[3049,3051,3052],3)-suma_liste(iotg,[3050,3053],3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3054 kol. 3 = AOP-u (3049 - 3050 + 3051 + 3052 - 3053) kol. 3, ako je AOP (3049 + 3051 + 3052) kol. 3 > AOP-a (3050 + 3053) kol. 3   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30070
        if( suma_liste(iotg,[3049,3051,3052],4) > suma_liste(iotg,[3050,3053],4) ):
            if not( aop(iotg,3054,4) == suma_liste(iotg,[3049,3051,3052],4)-suma_liste(iotg,[3050,3053],4) ):
                lzbir =  aop(iotg,3054,4) 
                dzbir =  suma_liste(iotg,[3049,3051,3052],4)-suma_liste(iotg,[3050,3053],4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3054 kol. 4 = AOP-u (3049 - 3050 + 3051 + 3052 - 3053) kol. 4, ako je AOP (3049 + 3051 + 3052) kol. 4 > AOP-a (3050 + 3053) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30071
        if( suma_liste(iotg,[3049,3051,3052],3) <= suma_liste(iotg,[3050,3053],3) ):
            if not( aop(iotg,3054,3) == 0 ):
                lzbir =  aop(iotg,3054,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3054 kol. 3 = 0, ako je AOP (3049 + 3051 + 3052) kol. 3 ≤ AOP-a (3050 + 3053) kol. 3   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30072
        if( suma_liste(iotg,[3049,3051,3052],4) <= suma_liste(iotg,[3050,3053],4) ):
            if not( aop(iotg,3054,4) == 0 ):
                lzbir =  aop(iotg,3054,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3054 kol. 4 = 0, ako je AOP (3049 + 3051 + 3052) kol. 4 ≤ AOP-a (3050 + 3053) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30073
        if not( aop(iotg,3054,4) == aop(iotg,3051,3) ):
            lzbir =  aop(iotg,3054,4) 
            dzbir =  aop(iotg,3051,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3054 kol. 4 = AOP-u 3051 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30074
        if not( aop(iotg,3054,3) == aop(bs,44,5) ):
            lzbir =  aop(iotg,3054,3) 
            dzbir =  aop(bs,44,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 3054 kol. 3 = AOP-u 0044 kol. 5 bilansa stanja Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3054 kol. 3 = AOP-u 0044 kol. 5 bilansa stanja Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #30075
        if not( aop(iotg,3054,4) == aop(bs,44,6) ):
            lzbir =  aop(iotg,3054,4) 
            dzbir =  aop(bs,44,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 3054 kol. 4 = AOP-u 0044 kol. 6 bilansa stanja Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3054 kol. 4 = AOP-u 0044 kol. 6 bilansa stanja Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #IZVEŠTAJ O PROMENAMA NA KAPITALU - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #40001
        if not( suma(iopk,4018, 4026, 1) +suma(iopk,4043, 4050, 1) +suma(iopk,4067, 4074, 1) +suma(iopk,4091, 4098, 1) +suma(iopk,4115, 4122, 1) +suma(iopk,4140, 4148, 1) +suma(iopk,4167, 4176, 1) +suma(iopk,4198, 4210, 1) +suma(iopk,4227, 4234, 1) +suma(iopk,4252, 4260, 1) +suma(iopk,4277, 4284, 1) +suma(iopk,4304, 4314, 1)+ aop(iopk, 4320, 1) +suma(iopk,4337, 4344, 1)  > 0 ):
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='Zbir podataka na oznakama za AOP (4018 do 4026) + (4043 do 4050) + (4067 do 4074) + (4091 do 4098) + (4115 do 4122) + (4140 do 4148) + (4167 do 4176) + (4198 do 4210) + (4227 do 4234) + (4252 do 4260) + (4277 do 4284) + (4304 do 4314) + 4320 + (4337 do 4344) > 0 Izveštaj o promenama na kapitalu, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40002
        if(Zahtev.ObveznikInfo.Novoosnovan == True):
            if not( suma(iopk,4001, 4017, 1) +suma(iopk,4027, 4042, 1) +suma(iopk,4051, 4066, 1) +suma(iopk,4075, 4090, 1) +suma(iopk,4099, 4114, 1) +suma(iopk,4123, 4139, 1) +suma(iopk,4149, 4166, 1) +suma(iopk,4177, 4197, 1) +suma(iopk,4211, 4226, 1) +suma(iopk,4235, 4251, 1) +suma(iopk,4261, 4276, 1) +suma(iopk,4285, 4303, 1) +suma(iopk,4315, 4319, 1) +suma(iopk,4321, 4336, 1)  == 0 ):
                lzbir =  suma(iopk,4001, 4017, 1) +suma(iopk,4027, 4042, 1) +suma(iopk,4051, 4066, 1) +suma(iopk,4075, 4090, 1) +suma(iopk,4099, 4114, 1) +suma(iopk,4123, 4139, 1) +suma(iopk,4149, 4166, 1) +suma(iopk,4177, 4197, 1) +suma(iopk,4211, 4226, 1) +suma(iopk,4235, 4251, 1) +suma(iopk,4261, 4276, 1) +suma(iopk,4285, 4303, 1) +suma(iopk,4315, 4319, 1) +suma(iopk,4321, 4336, 1)  
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Zbir podataka na oznakama za AOP (4001 do 4017) + (4027 do 4042) + (4051 do 4066) + (4075 do 4090) + (4099 do 4114) + (4123 do 4139) + (4149 do 4166) + (4177 do 4197) + (4211 do 4226) + (4235 do 4251) + (4261 do 4276) + (4285 do 4303) + (4315 do 4319) + (4321 do 4336) = 0 Izveštaj o promenama na kapitalu za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40003
        if(Zahtev.ObveznikInfo.Novoosnovan == False):
            if not( suma(iopk,4001, 4017, 1) +suma(iopk,4027, 4042, 1) +suma(iopk,4051, 4066, 1) +suma(iopk,4075, 4090, 1) +suma(iopk,4099, 4114, 1) +suma(iopk,4123, 4139, 1) +suma(iopk,4149, 4166, 1) +suma(iopk,4177, 4197, 1) +suma(iopk,4211, 4226, 1) +suma(iopk,4235, 4251, 1) +suma(iopk,4261, 4276, 1) +suma(iopk,4285, 4303, 1) +suma(iopk,4315, 4319, 1) +suma(iopk,4321, 4336, 1)  > 0 ):
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Zbir podataka na oznakama za AOP (4001 do 4017) + (4027 do 4042) + (4051 do 4066) + (4075 do 4090) + (4099 do 4114) + (4123 do 4139) + (4149 do 4166) + (4177 do 4197) + (4211 do 4226) + (4235 do 4251) + (4261 do 4276) + (4285 do 4303) + (4315 do 4319) + (4321 do 4336) > 0 Izveštaj o promenama na kapitalu, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #40004
        if not( aop(iopk,4004,1) == suma(iopk,4001,4002,1)-aop(iopk,4003,1) ):
            lzbir =  aop(iopk,4004,1) 
            dzbir =  suma(iopk,4001,4002,1)-aop(iopk,4003,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4004 = AOP-u (4001 + 4002 - 4003)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40005
        if not( aop(iopk,4030,1) == suma(iopk,4027,4028,1)-aop(iopk,4029,1) ):
            lzbir =  aop(iopk,4030,1) 
            dzbir =  suma(iopk,4027,4028,1)-aop(iopk,4029,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4030 = AOP-u (4027 + 4028 - 4029)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40006
        if not( aop(iopk,4054,1) == suma(iopk,4051,4052,1)-aop(iopk,4053,1) ):
            lzbir =  aop(iopk,4054,1) 
            dzbir =  suma(iopk,4051,4052,1)-aop(iopk,4053,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4054 = AOP-u (4051 + 4052 - 4053)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40007
        if not( aop(iopk,4078,1) == suma(iopk,4075,4076,1)-aop(iopk,4077,1) ):
            lzbir =  aop(iopk,4078,1) 
            dzbir =  suma(iopk,4075,4076,1)-aop(iopk,4077,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4078 = AOP-u (4075 + 4076 - 4077)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40008
        if not( aop(iopk,4102,1) == suma(iopk,4099,4100,1)-aop(iopk,4101,1) ):
            lzbir =  aop(iopk,4102,1) 
            dzbir =  suma(iopk,4099,4100,1)-aop(iopk,4101,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4102 = AOP-u (4099 + 4100 - 4101)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40009
        if not( aop(iopk,4126,1) == suma(iopk,4123,4124,1)-aop(iopk,4125,1) ):
            lzbir =  aop(iopk,4126,1) 
            dzbir =  suma(iopk,4123,4124,1)-aop(iopk,4125,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4126 = AOP-u (4123 + 4124 - 4125)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40010
        if not( aop(iopk,4152,1) == suma(iopk,4149,4150,1)-aop(iopk,4151,1) ):
            lzbir =  aop(iopk,4152,1) 
            dzbir =  suma(iopk,4149,4150,1)-aop(iopk,4151,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4152 = AOP-u (4149 + 4150 - 4151)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40011
        if not( aop(iopk,4180,1) == suma(iopk,4177,4178,1)-aop(iopk,4179,1) ):
            lzbir =  aop(iopk,4180,1) 
            dzbir =  suma(iopk,4177,4178,1)-aop(iopk,4179,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4180 = AOP-u (4177 + 4178 - 4179)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40012
        if not( aop(iopk,4214,1) == suma(iopk,4211,4212,1)-aop(iopk,4213,1) ):
            lzbir =  aop(iopk,4214,1) 
            dzbir =  suma(iopk,4211,4212,1)-aop(iopk,4213,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4214 = AOP-u (4211 + 4212 - 4213)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40013
        if not( aop(iopk,4238,1) == suma(iopk,4235,4236,1)-aop(iopk,4237,1) ):
            lzbir =  aop(iopk,4238,1) 
            dzbir =  suma(iopk,4235,4236,1)-aop(iopk,4237,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4238 = AOP-u (4235 + 4236 - 4237)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40014
        if not( aop(iopk,4264,1) == suma(iopk,4261,4262,1)-aop(iopk,4263,1) ):
            lzbir =  aop(iopk,4264,1) 
            dzbir =  suma(iopk,4261,4262,1)-aop(iopk,4263,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4264 = AOP-u (4261 + 4262 - 4263)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40015
        if not( aop(iopk,4288,1) == suma(iopk,4285,4286,1)-aop(iopk,4287,1) ):
            lzbir =  aop(iopk,4288,1) 
            dzbir =  suma(iopk,4285,4286,1)-aop(iopk,4287,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4288 = AOP-u (4285 + 4286 - 4287)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40016
        if not( aop(iopk,4324,1) == suma(iopk,4321,4322,1)-aop(iopk,4323,1) ):
            lzbir =  aop(iopk,4324,1) 
            dzbir =  suma(iopk,4321,4322,1)-aop(iopk,4323,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4324 = AOP-u (4321 + 4322 - 4323)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40017
        if not( aop(iopk,4177,1) == suma_liste(iopk,[4001,4027,4051,4075,4099,4123,4149],1) ):
            lzbir =  aop(iopk,4177,1) 
            dzbir =  suma_liste(iopk,[4001,4027,4051,4075,4099,4123,4149],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4177 = AOP-u (4001 + 4027 + 4051 + 4075 + 4099 + 4123 + 4149)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40018
        if not( aop(iopk,4178,1) == suma_liste(iopk,[4002,4028,4052,4076,4100,4124,4150],1) ):
            lzbir =  aop(iopk,4178,1) 
            dzbir =  suma_liste(iopk,[4002,4028,4052,4076,4100,4124,4150],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4178 = AOP-u (4002 + 4028 + 4052 + 4076 + 4100 + 4124 + 4150)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40019
        if not( aop(iopk,4179,1) == suma_liste(iopk,[4003,4029,4053,4077,4101,4125,4151],1) ):
            lzbir =  aop(iopk,4179,1) 
            dzbir =  suma_liste(iopk,[4003,4029,4053,4077,4101,4125,4151],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4179 = AOP-u (4003 + 4029 + 4053 + 4077 + 4101 + 4125 + 4151)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40020
        if not( aop(iopk,4180,1) == suma_liste(iopk,[4004,4030,4054,4078,4102,4126,4152],1) ):
            lzbir =  aop(iopk,4180,1) 
            dzbir =  suma_liste(iopk,[4004,4030,4054,4078,4102,4126,4152],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4180 = AOP-u (4004 + 4030 + 4054 + 4078 + 4102 + 4126 + 4152)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40021
        if not( aop(iopk,4285,1) == suma_liste(iopk,[4211,4235,4261],1) ):
            lzbir =  aop(iopk,4285,1) 
            dzbir =  suma_liste(iopk,[4211,4235,4261],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4285 = AOP-u (4211 + 4235 + 4261)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40022
        if not( aop(iopk,4286,1) == suma_liste(iopk,[4212,4236,4262],1) ):
            lzbir =  aop(iopk,4286,1) 
            dzbir =  suma_liste(iopk,[4212,4236,4262],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4286 = AOP-u (4212 + 4236 + 4262)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40023
        if not( aop(iopk,4287,1) == suma_liste(iopk,[4213,4237,4263],1) ):
            lzbir =  aop(iopk,4287,1) 
            dzbir =  suma_liste(iopk,[4213,4237,4263],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4287 = AOP-u (4213 + 4237 + 4263)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40024
        if not( aop(iopk,4288,1) == suma_liste(iopk,[4214,4238,4264],1) ):
            lzbir =  aop(iopk,4288,1) 
            dzbir =  suma_liste(iopk,[4214,4238,4264],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4288 = AOP-u (4214 + 4238 + 4264)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40025
        if not( aop(iopk,4315,1) == aop(iopk,4177,1) - aop(iopk,4285,1) ):
            lzbir =  aop(iopk,4315,1) 
            dzbir =  aop(iopk,4177,1) - aop(iopk,4285,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4315 = AOP-u (4177 - 4285)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40026
        if( aop(iopk,4315,1) > 0 ):
            if not( aop(iopk,4321,1) == 0 ):
                lzbir =  aop(iopk,4321,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4315 > 0, onda je AOP 4321 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40027
        if( aop(iopk,4321,1) > 0 ):
            if not( aop(iopk,4315,1) == 0 ):
                lzbir =  aop(iopk,4315,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4321 > 0, onda je AOP 4315 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40028
        if not( aop(iopk,4316,1) == aop(iopk,4180,1) - aop(iopk,4288,1) ):
            lzbir =  aop(iopk,4316,1) 
            dzbir =  aop(iopk,4180,1) - aop(iopk,4288,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4316 = AOP-u (4180 - 4288)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40029
        if( aop(iopk,4316,1) > 0 ):
            if not( aop(iopk,4324,1) == 0 ):
                lzbir =  aop(iopk,4324,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4316 > 0, onda je AOP 4324 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40030
        if( aop(iopk,4324,1) > 0 ):
            if not( aop(iopk,4316,1) == 0 ):
                lzbir =  aop(iopk,4316,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4324 > 0, onda je AOP 4316 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40031
        if not( aop(iopk,4181,1) == suma_liste(iopk,[4005,4055,4079],1) ):
            lzbir =  aop(iopk,4181,1) 
            dzbir =  suma_liste(iopk,[4005,4055,4079],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4181 = AOP-u (4005 + 4055 + 4079)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40032
        if not( aop(iopk,4182,1) == aop(iopk,4127,1) ):
            lzbir =  aop(iopk,4182,1) 
            dzbir =  aop(iopk,4127,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4182 = AOP-u 4127  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40033
        if not( aop(iopk,4183,1) == aop(iopk,4128,1) ):
            lzbir =  aop(iopk,4183,1) 
            dzbir =  aop(iopk,4128,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4183 = AOP-u 4128  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40034
        if not( aop(iopk,4289,1) == aop(iopk,4265,1) ):
            lzbir =  aop(iopk,4289,1) 
            dzbir =  aop(iopk,4265,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4289 = AOP-u 4265  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40035
        if not( aop(iopk,4184,1) == suma_liste(iopk,[4006,4031,4103,4153],1) ):
            lzbir =  aop(iopk,4184,1) 
            dzbir =  suma_liste(iopk,[4006,4031,4103,4153],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4184 = AOP-u (4006 + 4031 + 4103 + 4153)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40036
        if not( aop(iopk,4290,1) == aop(iopk,4215,1) ):
            lzbir =  aop(iopk,4290,1) 
            dzbir =  aop(iopk,4215,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4290 = AOP-u 4215  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40037
        if not( aop(iopk,4291,1) == aop(iopk,4239,1) ):
            lzbir =  aop(iopk,4291,1) 
            dzbir =  aop(iopk,4239,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4291 = AOP-u 4239  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40038
        if not( aop(iopk,4292,1) == aop(iopk,4240,1) ):
            lzbir =  aop(iopk,4292,1) 
            dzbir =  aop(iopk,4240,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4292 = AOP-u 4240  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40039
        if not( aop(iopk,4185,1) == suma_liste(iopk,[4007,4032,4056,4080,4104,4129,4154],1) ):
            lzbir =  aop(iopk,4185,1) 
            dzbir =  suma_liste(iopk,[4007,4032,4056,4080,4104,4129,4154],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4185 = AOP-u (4007 + 4032 + 4056 + 4080 + 4104 + 4129 + 4154)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40040
        if not( aop(iopk,4293,1) == suma_liste(iopk,[4216,4241,4266],1) ):
            lzbir =  aop(iopk,4293,1) 
            dzbir =  suma_liste(iopk,[4216,4241,4266],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4293 = AOP-u (4216 + 4241 + 4266)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40041
        if not( aop(iopk,4186,1) == suma_liste(iopk,[4008,4033,4057,4081,4105,4130,4155],1) ):
            lzbir =  aop(iopk,4186,1) 
            dzbir =  suma_liste(iopk,[4008,4033,4057,4081,4105,4130,4155],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4186 = AOP-u (4008 + 4033 + 4057 + 4081 + 4105 + 4130 + 4155)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40042
        if not( aop(iopk,4294,1) == suma_liste(iopk,[4217,4242,4267],1) ):
            lzbir =  aop(iopk,4294,1) 
            dzbir =  suma_liste(iopk,[4217,4242,4267],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4294 = AOP-u (4217 + 4242 + 4267)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40043
        if not( aop(iopk,4187,1) == aop(iopk,4156,1) ):
            lzbir =  aop(iopk,4187,1) 
            dzbir =  aop(iopk,4156,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4187 = AOP-u 4156  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40044
        if not( aop(iopk,4188,1) == aop(iopk,4157,1) ):
            lzbir =  aop(iopk,4188,1) 
            dzbir =  aop(iopk,4157,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4188 = AOP-u 4157  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40045
        if not( aop(iopk,4189,1) == suma_liste(iopk,[4009,4034,4058,4082,4106,4131,4158],1) ):
            lzbir =  aop(iopk,4189,1) 
            dzbir =  suma_liste(iopk,[4009,4034,4058,4082,4106,4131,4158],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4189 = AOP-u (4009 + 4034 + 4058 + 4082 + 4106 + 4131 + 4158)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40046
        if not( aop(iopk,4295,1) == suma_liste(iopk,[4218,4243,4268],1) ):
            lzbir =  aop(iopk,4295,1) 
            dzbir =  suma_liste(iopk,[4218,4243,4268],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4295 = AOP-u (4218 + 4243 + 4268)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40047
        if not( aop(iopk,4190,1) == suma_liste(iopk,[4010,4035,4059,4083,4107,4132,4159],1) ):
            lzbir =  aop(iopk,4190,1) 
            dzbir =  suma_liste(iopk,[4010,4035,4059,4083,4107,4132,4159],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4190 = AOP-u (4010 + 4035 + 4059 + 4083 + 4107 + 4132 + 4159)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40048
        if not( aop(iopk,4296,1) == suma_liste(iopk,[4219,4244,4269],1) ):
            lzbir =  aop(iopk,4296,1) 
            dzbir =  suma_liste(iopk,[4219,4244,4269],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4296 = AOP-u (4219 + 4244 + 4269)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40049
        if not( aop(iopk,4011,1) == suma_liste(iopk,[4005,4006,4007,4009],1) ):
            lzbir =  aop(iopk,4011,1) 
            dzbir =  suma_liste(iopk,[4005,4006,4007,4009],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4011 = AOP-u (4005 + 4006 + 4007 + 4009)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40050
        if not( aop(iopk,4012,1) == aop(iopk,4008,1) + aop(iopk,4010,1) ):
            lzbir =  aop(iopk,4012,1) 
            dzbir =  aop(iopk,4008,1) + aop(iopk,4010,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4012 = AOP-u (4008 + 4010)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40051
        if not( aop(iopk,4036,1) == suma_liste(iopk,[4031,4032,4034],1) ):
            lzbir =  aop(iopk,4036,1) 
            dzbir =  suma_liste(iopk,[4031,4032,4034],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4036 = AOP-u (4031 + 4032 + 4034)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40052
        if not( aop(iopk,4037,1) == aop(iopk,4033,1) + aop(iopk,4035,1) ):
            lzbir =  aop(iopk,4037,1) 
            dzbir =  aop(iopk,4033,1) + aop(iopk,4035,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4037 = AOP-u (4033 + 4035)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40053
        if not( aop(iopk,4060,1) == suma_liste(iopk,[4055,4056,4058],1) ):
            lzbir =  aop(iopk,4060,1) 
            dzbir =  suma_liste(iopk,[4055,4056,4058],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4060 = AOP-u (4055 + 4056 + 4058)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40054
        if not( aop(iopk,4061,1) == aop(iopk,4057,1) + aop(iopk,4059,1) ):
            lzbir =  aop(iopk,4061,1) 
            dzbir =  aop(iopk,4057,1) + aop(iopk,4059,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4061 = AOP-u (4057 + 4059)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40055
        if not( aop(iopk,4084,1) == suma_liste(iopk,[4079,4080,4082],1) ):
            lzbir =  aop(iopk,4084,1) 
            dzbir =  suma_liste(iopk,[4079,4080,4082],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4084 = AOP-u (4079 + 4080 + 4082)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40056
        if not( aop(iopk,4085,1) == aop(iopk,4081,1) + aop(iopk,4083,1) ):
            lzbir =  aop(iopk,4085,1) 
            dzbir =  aop(iopk,4081,1) + aop(iopk,4083,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4085 = AOP-u (4081 + 4083)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40057
        if not( aop(iopk,4108,1) == suma_liste(iopk,[4103,4104,4106],1) ):
            lzbir =  aop(iopk,4108,1) 
            dzbir =  suma_liste(iopk,[4103,4104,4106],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4108 = AOP-u (4103 + 4104 + 4106)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40058
        if not( aop(iopk,4109,1) == aop(iopk,4105,1) + aop(iopk,4107,1) ):
            lzbir =  aop(iopk,4109,1) 
            dzbir =  aop(iopk,4105,1) + aop(iopk,4107,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4109 = AOP-u (4105 + 4107)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40059
        if not( aop(iopk,4133,1) == suma_liste(iopk,[4127,4129,4131],1) ):
            lzbir =  aop(iopk,4133,1) 
            dzbir =  suma_liste(iopk,[4127,4129,4131],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4133 = AOP-u (4127 + 4129 + 4131)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40060
        if not( aop(iopk,4134,1) == suma_liste(iopk,[4128,4130,4132],1) ):
            lzbir =  aop(iopk,4134,1) 
            dzbir =  suma_liste(iopk,[4128,4130,4132],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4134 = AOP-u (4128 + 4130 + 4132)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40061
        if not( aop(iopk,4160,1) == suma_liste(iopk,[4153,4154,4158],1) ):
            lzbir =  aop(iopk,4160,1) 
            dzbir =  suma_liste(iopk,[4153,4154,4158],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4160 = AOP-u (4153 + 4154 + 4158)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40062
        if not( aop(iopk,4161,1) == suma_liste(iopk,[4155,4156,4157,4159],1) ):
            lzbir =  aop(iopk,4161,1) 
            dzbir =  suma_liste(iopk,[4155,4156,4157,4159],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4161 = AOP-u (4155 + 4156 + 4157 + 4159)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40063
        if not( aop(iopk,4191,1) == suma_liste(iopk,[4181,4182,4184,4185,4189],1) ):
            lzbir =  aop(iopk,4191,1) 
            dzbir =  suma_liste(iopk,[4181,4182,4184,4185,4189],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4191 = AOP-u (4181 + 4182 + 4184 + 4185 + 4189)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40064
        if not( aop(iopk,4192,1) == suma_liste(iopk,[4183,4186,4187,4188,4190],1) ):
            lzbir =  aop(iopk,4192,1) 
            dzbir =  suma_liste(iopk,[4183,4186,4187,4188,4190],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4192 = AOP-u (4183 + 4186 + 4187 + 4188 + 4190)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40065
        if not( aop(iopk,4191,1) == suma_liste(iopk,[4011,4036,4060,4084,4108,4133,4160],1) ):
            lzbir =  aop(iopk,4191,1) 
            dzbir =  suma_liste(iopk,[4011,4036,4060,4084,4108,4133,4160],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4191 = AOP-u (4011 + 4036 + 4060 + 4084 + 4108 + 4133 + 4160)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40066
        if not( aop(iopk,4192,1) == suma_liste(iopk,[4012,4037,4061,4085,4109,4134,4161],1) ):
            lzbir =  aop(iopk,4192,1) 
            dzbir =  suma_liste(iopk,[4012,4037,4061,4085,4109,4134,4161],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4192 = AOP-u (4012 + 4037 + 4061 + 4085 + 4109 + 4134 + 4161)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40067
        if not( aop(iopk,4220,1) == suma_liste(iopk,[4215,4216,4218],1) ):
            lzbir =  aop(iopk,4220,1) 
            dzbir =  suma_liste(iopk,[4215,4216,4218],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4220 = AOP-u (4215 + 4216 + 4218)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40068
        if not( aop(iopk,4221,1) == aop(iopk,4217,1) + aop(iopk,4219,1) ):
            lzbir =  aop(iopk,4221,1) 
            dzbir =  aop(iopk,4217,1) + aop(iopk,4219,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4221 = AOP-u (4217 + 4219)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40069
        if not( aop(iopk,4245,1) == suma_liste(iopk,[4239,4241,4243],1) ):
            lzbir =  aop(iopk,4245,1) 
            dzbir =  suma_liste(iopk,[4239,4241,4243],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4245 = AOP-u (4239 + 4241 + 4243)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40070
        if not( aop(iopk,4246,1) == suma_liste(iopk,[4240,4242,4244],1) ):
            lzbir =  aop(iopk,4246,1) 
            dzbir =  suma_liste(iopk,[4240,4242,4244],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4246 = AOP-u (4240 + 4242 + 4244)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40071
        if not( aop(iopk,4270,1) == suma_liste(iopk,[4265,4266,4268],1) ):
            lzbir =  aop(iopk,4270,1) 
            dzbir =  suma_liste(iopk,[4265,4266,4268],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4270 = AOP-u (4265 + 4266 + 4268)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40072
        if not( aop(iopk,4271,1) == aop(iopk,4267,1) + aop(iopk,4269,1) ):
            lzbir =  aop(iopk,4271,1) 
            dzbir =  aop(iopk,4267,1) + aop(iopk,4269,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4271 = AOP-u (4267 + 4269)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40073
        if not( aop(iopk,4297,1) == suma_liste(iopk,[4289,4290,4291,4293,4295],1) ):
            lzbir =  aop(iopk,4297,1) 
            dzbir =  suma_liste(iopk,[4289,4290,4291,4293,4295],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4297 = AOP-u (4289 + 4290 + 4291 + 4293 + 4295)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40074
        if not( aop(iopk,4298,1) == suma_liste(iopk,[4292,4294,4296],1) ):
            lzbir =  aop(iopk,4298,1) 
            dzbir =  suma_liste(iopk,[4292,4294,4296],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4298 = AOP-u (4292 + 4294 + 4296)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40075
        if not( aop(iopk,4297,1) == suma_liste(iopk,[4220,4245,4270],1) ):
            lzbir =  aop(iopk,4297,1) 
            dzbir =  suma_liste(iopk,[4220,4245,4270],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4297 = AOP-u (4220 + 4245 + 4270)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40076
        if not( aop(iopk,4298,1) == suma_liste(iopk,[4221,4246,4271],1) ):
            lzbir =  aop(iopk,4298,1) 
            dzbir =  suma_liste(iopk,[4221,4246,4271],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4298 = AOP-u (4221 + 4246 + 4271)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40077
        if not( aop(iopk,4330,1) == suma_liste(iopk,[4325,4326,4328],1) ):
            lzbir =  aop(iopk,4330,1) 
            dzbir =  suma_liste(iopk,[4325,4326,4328],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4330 = AOP-u (4325 + 4326 + 4328)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40078
        if not( aop(iopk,4331,1) == aop(iopk,4327,1) + aop(iopk,4329,1) ):
            lzbir =  aop(iopk,4331,1) 
            dzbir =  aop(iopk,4327,1) + aop(iopk,4329,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4331 = AOP-u (4327 + 4329)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40079
        if not( aop(iopk,4013,1) == suma_liste(iopk,[4004,4011],1)-aop(iopk,4012,1) ):
            lzbir =  aop(iopk,4013,1) 
            dzbir =  suma_liste(iopk,[4004,4011],1)-aop(iopk,4012,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4013 = AOP-u (4004 + 4011 - 4012)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40080
        if not( aop(iopk,4038,1) == suma_liste(iopk,[4030,4036],1)-aop(iopk,4037,1) ):
            lzbir =  aop(iopk,4038,1) 
            dzbir =  suma_liste(iopk,[4030,4036],1)-aop(iopk,4037,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4038 = AOP-u (4030 + 4036 - 4037)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40081
        if not( aop(iopk,4062,1) == suma_liste(iopk,[4054,4060],1)-aop(iopk,4061,1) ):
            lzbir =  aop(iopk,4062,1) 
            dzbir =  suma_liste(iopk,[4054,4060],1)-aop(iopk,4061,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4062 = AOP-u (4054 + 4060 - 4061)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40082
        if not( aop(iopk,4086,1) == suma_liste(iopk,[4078,4084],1)-aop(iopk,4085,1) ):
            lzbir =  aop(iopk,4086,1) 
            dzbir =  suma_liste(iopk,[4078,4084],1)-aop(iopk,4085,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4086 = AOP-u (4078 + 4084 - 4085)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40083
        if not( aop(iopk,4110,1) == suma_liste(iopk,[4102,4108],1)-aop(iopk,4109,1) ):
            lzbir =  aop(iopk,4110,1) 
            dzbir =  suma_liste(iopk,[4102,4108],1)-aop(iopk,4109,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4110 = AOP-u (4102 + 4108 - 4109)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40084
        if not( aop(iopk,4135,1) == suma_liste(iopk,[4126,4133],1)-aop(iopk,4134,1) ):
            lzbir =  aop(iopk,4135,1) 
            dzbir =  suma_liste(iopk,[4126,4133],1)-aop(iopk,4134,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4135 = AOP-u (4126 + 4133 - 4134)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40085
        if not( aop(iopk,4162,1) == suma_liste(iopk,[4152,4160],1)-aop(iopk,4161,1) ):
            lzbir =  aop(iopk,4162,1) 
            dzbir =  suma_liste(iopk,[4152,4160],1)-aop(iopk,4161,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4162 = AOP-u (4152 + 4160 - 4161)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40086
        if not( aop(iopk,4193,1) == suma_liste(iopk,[4180,4191],1)-aop(iopk,4192,1) ):
            lzbir =  aop(iopk,4193,1) 
            dzbir =  suma_liste(iopk,[4180,4191],1)-aop(iopk,4192,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4193 = AOP-u (4180 + 4191 - 4192)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40087
        if not( aop(iopk,4222,1) == suma_liste(iopk,[4214,4220],1)-aop(iopk,4221,1) ):
            lzbir =  aop(iopk,4222,1) 
            dzbir =  suma_liste(iopk,[4214,4220],1)-aop(iopk,4221,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4222 = AOP-u (4214 + 4220 - 4221)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40088
        if not( aop(iopk,4247,1) == suma_liste(iopk,[4238,4245],1)-aop(iopk,4246,1) ):
            lzbir =  aop(iopk,4247,1) 
            dzbir =  suma_liste(iopk,[4238,4245],1)-aop(iopk,4246,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4247 = AOP-u (4238 + 4245 - 4246)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40089
        if not( aop(iopk,4272,1) == suma_liste(iopk,[4264,4270],1)-aop(iopk,4271,1) ):
            lzbir =  aop(iopk,4272,1) 
            dzbir =  suma_liste(iopk,[4264,4270],1)-aop(iopk,4271,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4272 = AOP-u (4264 + 4270 - 4271)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40090
        if not( aop(iopk,4299,1) == suma_liste(iopk,[4288,4297],1)-aop(iopk,4298,1) ):
            lzbir =  aop(iopk,4299,1) 
            dzbir =  suma_liste(iopk,[4288,4297],1)-aop(iopk,4298,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4299 = AOP-u (4288 + 4297 - 4298)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40091
        if not( aop(iopk,4332,1) == suma_liste(iopk,[4324,4330],1)-aop(iopk,4331,1) ):
            lzbir =  aop(iopk,4332,1) 
            dzbir =  suma_liste(iopk,[4324,4330],1)-aop(iopk,4331,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4332 = AOP-u (4324 + 4330 - 4331)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40092
        if not( aop(iopk,4193,1) == suma_liste(iopk,[4013,4038,4062,4086,4110,4135,4162],1) ):
            lzbir =  aop(iopk,4193,1) 
            dzbir =  suma_liste(iopk,[4013,4038,4062,4086,4110,4135,4162],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4193 = AOP-u (4013 + 4038 + 4062 + 4086 + 4110 + 4135 + 4162)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40093
        if not( aop(iopk,4299,1) == suma_liste(iopk,[4222,4247,4272],1) ):
            lzbir =  aop(iopk,4299,1) 
            dzbir =  suma_liste(iopk,[4222,4247,4272],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4299 = AOP-u (4222 + 4247 + 4272)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40094
        if not( aop(iopk,4317,1) == aop(iopk,4193,1) - aop(iopk,4299,1) ):
            lzbir =  aop(iopk,4317,1) 
            dzbir =  aop(iopk,4193,1) - aop(iopk,4299,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4317 = AOP-u (4193 - 4299)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40095
        if( aop(iopk,4317,1) > 0 ):
            if not( aop(iopk,4332,1) == 0 ):
                lzbir =  aop(iopk,4332,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4317 > 0, onda je AOP 4332 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40096
        if( aop(iopk,4332,1) > 0 ):
            if not( aop(iopk,4317,1) == 0 ):
                lzbir =  aop(iopk,4317,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4332 > 0, onda je AOP 4317 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40097
        if not( aop(iopk,4014,1) == aop(iopk,4013,1) ):
            lzbir =  aop(iopk,4014,1) 
            dzbir =  aop(iopk,4013,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4014 = AOP-u 4013  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40098
        if not( aop(iopk,4039,1) == aop(iopk,4038,1) ):
            lzbir =  aop(iopk,4039,1) 
            dzbir =  aop(iopk,4038,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4039 = AOP-u 4038  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40099
        if not( aop(iopk,4063,1) == aop(iopk,4062,1) ):
            lzbir =  aop(iopk,4063,1) 
            dzbir =  aop(iopk,4062,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4063 = AOP-u 4062  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40100
        if not( aop(iopk,4087,1) == aop(iopk,4086,1) ):
            lzbir =  aop(iopk,4087,1) 
            dzbir =  aop(iopk,4086,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4087 = AOP-u 4086  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40101
        if not( aop(iopk,4111,1) == aop(iopk,4110,1) ):
            lzbir =  aop(iopk,4111,1) 
            dzbir =  aop(iopk,4110,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4111 = AOP-u 4110  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40102
        if not( aop(iopk,4136,1) == aop(iopk,4135,1) ):
            lzbir =  aop(iopk,4136,1) 
            dzbir =  aop(iopk,4135,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4136 = AOP-u 4135  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40103
        if not( aop(iopk,4163,1) == aop(iopk,4162,1) ):
            lzbir =  aop(iopk,4163,1) 
            dzbir =  aop(iopk,4162,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4163 = AOP-u 4162  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40104
        if not( aop(iopk,4194,1) == aop(iopk,4193,1) ):
            lzbir =  aop(iopk,4194,1) 
            dzbir =  aop(iopk,4193,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4194 = AOP-u 4193  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40105
        if not( aop(iopk,4223,1) == aop(iopk,4222,1) ):
            lzbir =  aop(iopk,4223,1) 
            dzbir =  aop(iopk,4222,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4223 = AOP-u 4222  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40106
        if not( aop(iopk,4248,1) == aop(iopk,4247,1) ):
            lzbir =  aop(iopk,4248,1) 
            dzbir =  aop(iopk,4247,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4248 = AOP-u 4247  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40107
        if not( aop(iopk,4273,1) == aop(iopk,4272,1) ):
            lzbir =  aop(iopk,4273,1) 
            dzbir =  aop(iopk,4272,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4273 = AOP-u 4272  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40108
        if not( aop(iopk,4300,1) == aop(iopk,4299,1) ):
            lzbir =  aop(iopk,4300,1) 
            dzbir =  aop(iopk,4299,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4300 = AOP-u 4299  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40109
        if not( aop(iopk,4318,1) == aop(iopk,4317,1) ):
            lzbir =  aop(iopk,4318,1) 
            dzbir =  aop(iopk,4317,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4318 = AOP-u 4317  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40110
        if not( aop(iopk,4333,1) == aop(iopk,4332,1) ):
            lzbir =  aop(iopk,4333,1) 
            dzbir =  aop(iopk,4332,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4333 = AOP-u 4332  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40111
        if not( aop(iopk,4017,1) == suma(iopk,4014,4015,1)-aop(iopk,4016,1) ):
            lzbir =  aop(iopk,4017,1) 
            dzbir =  suma(iopk,4014,4015,1)-aop(iopk,4016,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4017 = AOP-u (4014 + 4015 - 4016)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40112
        if not( aop(iopk,4042,1) == suma(iopk,4039,4040,1)-aop(iopk,4041,1) ):
            lzbir =  aop(iopk,4042,1) 
            dzbir =  suma(iopk,4039,4040,1)-aop(iopk,4041,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4042 = AOP-u (4039 + 4040 - 4041)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40113
        if not( aop(iopk,4066,1) == suma(iopk,4063,4064,1)-aop(iopk,4065,1) ):
            lzbir =  aop(iopk,4066,1) 
            dzbir =  suma(iopk,4063,4064,1)-aop(iopk,4065,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4066 = AOP-u (4063 + 4064 - 4065)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40114
        if not( aop(iopk,4090,1) == suma(iopk,4087,4088,1)-aop(iopk,4089,1) ):
            lzbir =  aop(iopk,4090,1) 
            dzbir =  suma(iopk,4087,4088,1)-aop(iopk,4089,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4090 = AOP-u (4087 + 4088 - 4089)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40115
        if not( aop(iopk,4114,1) == suma(iopk,4111,4112,1)-aop(iopk,4113,1) ):
            lzbir =  aop(iopk,4114,1) 
            dzbir =  suma(iopk,4111,4112,1)-aop(iopk,4113,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4114 = AOP-u (4111 + 4112 - 4113)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40116
        if not( aop(iopk,4139,1) == suma(iopk,4136,4137,1)-aop(iopk,4138,1) ):
            lzbir =  aop(iopk,4139,1) 
            dzbir =  suma(iopk,4136,4137,1)-aop(iopk,4138,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4139 = AOP-u (4136 + 4137 - 4138)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40117
        if not( aop(iopk,4166,1) == suma(iopk,4163,4164,1)-aop(iopk,4165,1) ):
            lzbir =  aop(iopk,4166,1) 
            dzbir =  suma(iopk,4163,4164,1)-aop(iopk,4165,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4166 = AOP-u (4163 + 4164 - 4165)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40118
        if not( aop(iopk,4197,1) == suma(iopk,4194,4195,1)-aop(iopk,4196,1) ):
            lzbir =  aop(iopk,4197,1) 
            dzbir =  suma(iopk,4194,4195,1)-aop(iopk,4196,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4197 = AOP-u (4194 + 4195 - 4196)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40119
        if not( aop(iopk,4226,1) == suma(iopk,4223,4224,1)-aop(iopk,4225,1) ):
            lzbir =  aop(iopk,4226,1) 
            dzbir =  suma(iopk,4223,4224,1)-aop(iopk,4225,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4226 = AOP-u (4223 + 4224 - 4225)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40120
        if not( aop(iopk,4251,1) == suma(iopk,4248,4249,1)-aop(iopk,4250,1) ):
            lzbir =  aop(iopk,4251,1) 
            dzbir =  suma(iopk,4248,4249,1)-aop(iopk,4250,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4251 = AOP-u (4248 + 4249 - 4250)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40121
        if not( aop(iopk,4276,1) == suma(iopk,4273,4274,1)-aop(iopk,4275,1) ):
            lzbir =  aop(iopk,4276,1) 
            dzbir =  suma(iopk,4273,4274,1)-aop(iopk,4275,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4276 = AOP-u (4273 + 4274 - 4275)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40122
        if not( aop(iopk,4303,1) == suma(iopk,4300,4301,1)-aop(iopk,4302,1) ):
            lzbir =  aop(iopk,4303,1) 
            dzbir =  suma(iopk,4300,4301,1)-aop(iopk,4302,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4303 = AOP-u (4300 + 4301 - 4302)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40123
        if not( aop(iopk,4336,1) == suma(iopk,4333,4334,1)-aop(iopk,4335,1) ):
            lzbir =  aop(iopk,4336,1) 
            dzbir =  suma(iopk,4333,4334,1)-aop(iopk,4335,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4336 = AOP-u (4333 + 4334 - 4335)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40124
        if not( aop(iopk,4195,1) == suma_liste(iopk,[4015,4040,4064,4088,4112,4137,4164],1) ):
            lzbir =  aop(iopk,4195,1) 
            dzbir =  suma_liste(iopk,[4015,4040,4064,4088,4112,4137,4164],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4195 = AOP-u (4015 + 4040 + 4064 + 4088 + 4112 + 4137 + 4164)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40125
        if not( aop(iopk,4196,1) == suma_liste(iopk,[4016,4041,4065,4089,4113,4138,4165],1) ):
            lzbir =  aop(iopk,4196,1) 
            dzbir =  suma_liste(iopk,[4016,4041,4065,4089,4113,4138,4165],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4196 = AOP-u (4016 + 4041 + 4065 + 4089 + 4113 + 4138 + 4165)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40126
        if not( aop(iopk,4197,1) == suma_liste(iopk,[4017,4042,4066,4090,4114,4139,4166],1) ):
            lzbir =  aop(iopk,4197,1) 
            dzbir =  suma_liste(iopk,[4017,4042,4066,4090,4114,4139,4166],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4197 = AOP-u (4017 + 4042 + 4066 + 4090 + 4114 + 4139 + 4166)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40127
        if not( aop(iopk,4301,1) == suma_liste(iopk,[4224,4249,4274],1) ):
            lzbir =  aop(iopk,4301,1) 
            dzbir =  suma_liste(iopk,[4224,4249,4274],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4301 = AOP-u (4224 + 4249 + 4274)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40128
        if not( aop(iopk,4302,1) == suma_liste(iopk,[4225,4250,4275],1) ):
            lzbir =  aop(iopk,4302,1) 
            dzbir =  suma_liste(iopk,[4225,4250,4275],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4302 = AOP-u (4225 + 4250 + 4275)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40129
        if not( aop(iopk,4303,1) == suma_liste(iopk,[4226,4251,4276],1) ):
            lzbir =  aop(iopk,4303,1) 
            dzbir =  suma_liste(iopk,[4226,4251,4276],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4303 = AOP-u (4226 + 4251 + 4276)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40130
        if not( aop(iopk,4319,1) == aop(iopk,4197,1) - aop(iopk,4303,1) ):
            lzbir =  aop(iopk,4319,1) 
            dzbir =  aop(iopk,4197,1) - aop(iopk,4303,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4319 = AOP-u (4197 - 4303)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40131
        if( aop(iopk,4319,1) > 0 ):
            if not( aop(iopk,4336,1) == 0 ):
                lzbir =  aop(iopk,4336,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4319 > 0, onda je AOP 4336 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40132
        if( aop(iopk,4336,1) > 0 ):
            if not( aop(iopk,4319,1) == 0 ):
                lzbir =  aop(iopk,4319,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4336 > 0, onda je AOP 4319 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40133
        if not( aop(iopk,4198,1) == suma_liste(iopk,[4018,4067,4091],1) ):
            lzbir =  aop(iopk,4198,1) 
            dzbir =  suma_liste(iopk,[4018,4067,4091],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4198 = AOP-u (4018 + 4067 + 4091)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40134
        if not( aop(iopk,4199,1) == aop(iopk,4140,1) ):
            lzbir =  aop(iopk,4199,1) 
            dzbir =  aop(iopk,4140,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4199 = AOP-u 4140  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40135
        if not( aop(iopk,4200,1) == aop(iopk,4141,1) ):
            lzbir =  aop(iopk,4200,1) 
            dzbir =  aop(iopk,4141,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4200 = AOP-u 4141  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40136
        if not( aop(iopk,4304,1) == aop(iopk,4277,1) ):
            lzbir =  aop(iopk,4304,1) 
            dzbir =  aop(iopk,4277,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4304 = AOP-u 4277  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40137
        if not( aop(iopk,4201,1) == suma_liste(iopk,[4019,4043,4115,4167],1) ):
            lzbir =  aop(iopk,4201,1) 
            dzbir =  suma_liste(iopk,[4019,4043,4115,4167],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4201 = AOP-u (4019 + 4043 + 4115 + 4167)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40138
        if not( aop(iopk,4305,1) == aop(iopk,4227,1) ):
            lzbir =  aop(iopk,4305,1) 
            dzbir =  aop(iopk,4227,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4305 = AOP-u 4227  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40139
        if not( aop(iopk,4306,1) == aop(iopk,4252,1) ):
            lzbir =  aop(iopk,4306,1) 
            dzbir =  aop(iopk,4252,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4306 = AOP-u 4252  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40140
        if not( aop(iopk,4307,1) == aop(iopk,4253,1) ):
            lzbir =  aop(iopk,4307,1) 
            dzbir =  aop(iopk,4253,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4307 = AOP-u 4253  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40141
        if not( aop(iopk,4202,1) == suma_liste(iopk,[4020,4044,4068,4092,4116,4142,4168],1) ):
            lzbir =  aop(iopk,4202,1) 
            dzbir =  suma_liste(iopk,[4020,4044,4068,4092,4116,4142,4168],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4202 = AOP-u (4020 + 4044 + 4068 + 4092 + 4116 + 4142 + 4168)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40142
        if not( aop(iopk,4308,1) == suma_liste(iopk,[4228,4254,4278],1) ):
            lzbir =  aop(iopk,4308,1) 
            dzbir =  suma_liste(iopk,[4228,4254,4278],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4308 = AOP-u (4228 + 4254 + 4278)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40143
        if not( aop(iopk,4203,1) == suma_liste(iopk,[4021,4045,4069,4093,4117,4143,4169],1) ):
            lzbir =  aop(iopk,4203,1) 
            dzbir =  suma_liste(iopk,[4021,4045,4069,4093,4117,4143,4169],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4203 = AOP-u (4021 + 4045 + 4069 + 4093 + 4117 + 4143 + 4169)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40144
        if not( aop(iopk,4309,1) == suma_liste(iopk,[4229,4255,4279],1) ):
            lzbir =  aop(iopk,4309,1) 
            dzbir =  suma_liste(iopk,[4229,4255,4279],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4309 = AOP-u (4229 + 4255 + 4279)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40145
        if not( aop(iopk,4204,1) == aop(iopk,4170,1) ):
            lzbir =  aop(iopk,4204,1) 
            dzbir =  aop(iopk,4170,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4204 = AOP-u 4170  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40146
        if not( aop(iopk,4205,1) == aop(iopk,4171,1) ):
            lzbir =  aop(iopk,4205,1) 
            dzbir =  aop(iopk,4171,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4205 = AOP-u 4171  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40147
        if not( aop(iopk,4206,1) == suma_liste(iopk,[4022,4046,4070,4094,4118,4144,4172],1) ):
            lzbir =  aop(iopk,4206,1) 
            dzbir =  suma_liste(iopk,[4022,4046,4070,4094,4118,4144,4172],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4206 = AOP-u (4022 + 4046 + 4070 + 4094 + 4118 + 4144 + 4172)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40148
        if not( aop(iopk,4310,1) == suma_liste(iopk,[4230,4256,4280],1) ):
            lzbir =  aop(iopk,4310,1) 
            dzbir =  suma_liste(iopk,[4230,4256,4280],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4310 = AOP-u (4230 + 4256 + 4280)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40149
        if not( aop(iopk,4207,1) == suma_liste(iopk,[4023,4047,4071,4095,4119,4145,4173],1) ):
            lzbir =  aop(iopk,4207,1) 
            dzbir =  suma_liste(iopk,[4023,4047,4071,4095,4119,4145,4173],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4207 = AOP-u (4023 + 4047 + 4071 + 4095 + 4119 + 4145 + 4173)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40150
        if not( aop(iopk,4311,1) == suma_liste(iopk,[4231,4257,4281],1) ):
            lzbir =  aop(iopk,4311,1) 
            dzbir =  suma_liste(iopk,[4231,4257,4281],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4311 = AOP-u (4231 + 4257 + 4281)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40151
        if not( aop(iopk,4024,1) == suma_liste(iopk,[4018,4019,4020,4022],1) ):
            lzbir =  aop(iopk,4024,1) 
            dzbir =  suma_liste(iopk,[4018,4019,4020,4022],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4024 = AOP-u (4018 + 4019 + 4020 + 4022)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40152
        if not( aop(iopk,4025,1) == aop(iopk,4021,1) + aop(iopk,4023,1) ):
            lzbir =  aop(iopk,4025,1) 
            dzbir =  aop(iopk,4021,1) + aop(iopk,4023,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4025 = AOP-u (4021 + 4023)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40153
        if not( aop(iopk,4048,1) == suma_liste(iopk,[4043,4044,4046],1) ):
            lzbir =  aop(iopk,4048,1) 
            dzbir =  suma_liste(iopk,[4043,4044,4046],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4048 = AOP-u (4043 + 4044 + 4046)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40154
        if not( aop(iopk,4049,1) == aop(iopk,4045,1) + aop(iopk,4047,1) ):
            lzbir =  aop(iopk,4049,1) 
            dzbir =  aop(iopk,4045,1) + aop(iopk,4047,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4049 = AOP-u (4045 + 4047)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40155
        if not( aop(iopk,4072,1) == suma_liste(iopk,[4067,4068,4070],1) ):
            lzbir =  aop(iopk,4072,1) 
            dzbir =  suma_liste(iopk,[4067,4068,4070],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4072 = AOP-u (4067 + 4068 + 4070)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40156
        if not( aop(iopk,4073,1) == aop(iopk,4069,1) + aop(iopk,4071,1) ):
            lzbir =  aop(iopk,4073,1) 
            dzbir =  aop(iopk,4069,1) + aop(iopk,4071,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4073 = AOP-u (4069 + 4071)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40157
        if not( aop(iopk,4096,1) == suma_liste(iopk,[4091,4092,4094],1) ):
            lzbir =  aop(iopk,4096,1) 
            dzbir =  suma_liste(iopk,[4091,4092,4094],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4096 = AOP-u (4091 + 4092 + 4094)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40158
        if not( aop(iopk,4097,1) == aop(iopk,4093,1) + aop(iopk,4095,1) ):
            lzbir =  aop(iopk,4097,1) 
            dzbir =  aop(iopk,4093,1) + aop(iopk,4095,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4097 = AOP-u (4093 + 4095)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40159
        if not( aop(iopk,4120,1) == suma_liste(iopk,[4115,4116,4118],1) ):
            lzbir =  aop(iopk,4120,1) 
            dzbir =  suma_liste(iopk,[4115,4116,4118],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4120 = AOP-u (4115 + 4116 + 4118)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40160
        if not( aop(iopk,4121,1) == aop(iopk,4117,1) + aop(iopk,4119,1) ):
            lzbir =  aop(iopk,4121,1) 
            dzbir =  aop(iopk,4117,1) + aop(iopk,4119,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4121 = AOP-u (4117 + 4119)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40161
        if not( aop(iopk,4146,1) == suma_liste(iopk,[4140,4142,4144],1) ):
            lzbir =  aop(iopk,4146,1) 
            dzbir =  suma_liste(iopk,[4140,4142,4144],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4146 = AOP-u (4140 + 4142 + 4144)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40162
        if not( aop(iopk,4147,1) == suma_liste(iopk,[4141,4143,4145],1) ):
            lzbir =  aop(iopk,4147,1) 
            dzbir =  suma_liste(iopk,[4141,4143,4145],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4147 = AOP-u (4141 + 4143 + 4145)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40163
        if not( aop(iopk,4174,1) == suma_liste(iopk,[4167,4168,4172],1) ):
            lzbir =  aop(iopk,4174,1) 
            dzbir =  suma_liste(iopk,[4167,4168,4172],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4174 = AOP-u (4167 + 4168 + 4172)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40164
        if not( aop(iopk,4175,1) == suma_liste(iopk,[4169,4170,4171,4173],1) ):
            lzbir =  aop(iopk,4175,1) 
            dzbir =  suma_liste(iopk,[4169,4170,4171,4173],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4175 = AOP-u (4169 + 4170 + 4171 + 4173)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40165
        if not( aop(iopk,4208,1) == suma_liste(iopk,[4198,4199,4201,4202,4206],1) ):
            lzbir =  aop(iopk,4208,1) 
            dzbir =  suma_liste(iopk,[4198,4199,4201,4202,4206],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4208 = AOP-u (4198 + 4199 + 4201 + 4202 + 4206)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40166
        if not( aop(iopk,4209,1) == suma_liste(iopk,[4200,4203,4204,4205,4207],1) ):
            lzbir =  aop(iopk,4209,1) 
            dzbir =  suma_liste(iopk,[4200,4203,4204,4205,4207],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4209 = AOP-u (4200 + 4203 + 4204 + 4205 + 4207)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40167
        if not( aop(iopk,4208,1) == suma_liste(iopk,[4024,4048,4072,4096,4120,4146,4174],1) ):
            lzbir =  aop(iopk,4208,1) 
            dzbir =  suma_liste(iopk,[4024,4048,4072,4096,4120,4146,4174],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4208 = AOP-u (4024 + 4048 + 4072 + 4096 + 4120 + 4146 + 4174)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40168
        if not( aop(iopk,4209,1) == suma_liste(iopk,[4025,4049,4073,4097,4121,4147,4175],1) ):
            lzbir =  aop(iopk,4209,1) 
            dzbir =  suma_liste(iopk,[4025,4049,4073,4097,4121,4147,4175],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4209 = AOP-u (4025 + 4049 + 4073 + 4097 + 4121 + 4147 + 4175)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40169
        if not( aop(iopk,4232,1) == suma_liste(iopk,[4227,4228,4230],1) ):
            lzbir =  aop(iopk,4232,1) 
            dzbir =  suma_liste(iopk,[4227,4228,4230],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4232 = AOP-u (4227 + 4228 + 4230)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40170
        if not( aop(iopk,4233,1) == aop(iopk,4229,1) + aop(iopk,4231,1) ):
            lzbir =  aop(iopk,4233,1) 
            dzbir =  aop(iopk,4229,1) + aop(iopk,4231,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4233 = AOP-u (4229 + 4231)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40171
        if not( aop(iopk,4258,1) == suma_liste(iopk,[4252,4254,4256],1) ):
            lzbir =  aop(iopk,4258,1) 
            dzbir =  suma_liste(iopk,[4252,4254,4256],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4258 = AOP-u (4252 + 4254 + 4256)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40172
        if not( aop(iopk,4259,1) == suma_liste(iopk,[4253,4255,4257],1) ):
            lzbir =  aop(iopk,4259,1) 
            dzbir =  suma_liste(iopk,[4253,4255,4257],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4259 = AOP-u (4253 + 4255 + 4257)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40173
        if not( aop(iopk,4282,1) == suma_liste(iopk,[4277,4278,4280],1) ):
            lzbir =  aop(iopk,4282,1) 
            dzbir =  suma_liste(iopk,[4277,4278,4280],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4282 = AOP-u (4277 + 4278 + 4280)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40174
        if not( aop(iopk,4283,1) == aop(iopk,4279,1) + aop(iopk,4281,1) ):
            lzbir =  aop(iopk,4283,1) 
            dzbir =  aop(iopk,4279,1) + aop(iopk,4281,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4283 = AOP-u (4279 + 4281)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40175
        if not( aop(iopk,4312,1) == suma_liste(iopk,[4304,4305,4306,4308,4310],1) ):
            lzbir =  aop(iopk,4312,1) 
            dzbir =  suma_liste(iopk,[4304,4305,4306,4308,4310],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4312 = AOP-u (4304 + 4305 + 4306 + 4308 + 4310)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40176
        if not( aop(iopk,4313,1) == suma_liste(iopk,[4307,4309,4311],1) ):
            lzbir =  aop(iopk,4313,1) 
            dzbir =  suma_liste(iopk,[4307,4309,4311],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4313 = AOP-u (4307 + 4309 + 4311)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40177
        if not( aop(iopk,4312,1) == suma_liste(iopk,[4232,4258,4282],1) ):
            lzbir =  aop(iopk,4312,1) 
            dzbir =  suma_liste(iopk,[4232,4258,4282],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4312 = AOP-u (4232 + 4258 + 4282)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40178
        if not( aop(iopk,4313,1) == suma_liste(iopk,[4233,4259,4283],1) ):
            lzbir =  aop(iopk,4313,1) 
            dzbir =  suma_liste(iopk,[4233,4259,4283],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4313 = AOP-u (4233 + 4259 + 4283)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40179
        if not( aop(iopk,4342,1) == suma_liste(iopk,[4337,4338,4340],1) ):
            lzbir =  aop(iopk,4342,1) 
            dzbir =  suma_liste(iopk,[4337,4338,4340],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4342 = AOP-u (4337 + 4338 + 4340)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40180
        if not( aop(iopk,4343,1) == aop(iopk,4339,1) + aop(iopk,4341,1) ):
            lzbir =  aop(iopk,4343,1) 
            dzbir =  aop(iopk,4339,1) + aop(iopk,4341,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4343 = AOP-u (4339 + 4341)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40181
        if not( aop(iopk,4026,1) == suma_liste(iopk,[4017,4024],1)-aop(iopk,4025,1) ):
            lzbir =  aop(iopk,4026,1) 
            dzbir =  suma_liste(iopk,[4017,4024],1)-aop(iopk,4025,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4026 = AOP-u (4017 + 4024 - 4025)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40182
        if not( aop(iopk,4050,1) == suma_liste(iopk,[4042,4048],1)-aop(iopk,4049,1) ):
            lzbir =  aop(iopk,4050,1) 
            dzbir =  suma_liste(iopk,[4042,4048],1)-aop(iopk,4049,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4050 = AOP-u (4042 + 4048 - 4049)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40183
        if not( aop(iopk,4074,1) == suma_liste(iopk,[4066,4072],1)-aop(iopk,4073,1) ):
            lzbir =  aop(iopk,4074,1) 
            dzbir =  suma_liste(iopk,[4066,4072],1)-aop(iopk,4073,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4074 = AOP-u (4066 + 4072 - 4073)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40184
        if not( aop(iopk,4098,1) == suma_liste(iopk,[4090,4096],1)-aop(iopk,4097,1) ):
            lzbir =  aop(iopk,4098,1) 
            dzbir =  suma_liste(iopk,[4090,4096],1)-aop(iopk,4097,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4098 = AOP-u (4090 + 4096 - 4097)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40185
        if not( aop(iopk,4122,1) == suma_liste(iopk,[4114,4120],1)-aop(iopk,4121,1) ):
            lzbir =  aop(iopk,4122,1) 
            dzbir =  suma_liste(iopk,[4114,4120],1)-aop(iopk,4121,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4122 = AOP-u (4114 + 4120 - 4121)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40186
        if not( aop(iopk,4148,1) == suma_liste(iopk,[4139,4146],1)-aop(iopk,4147,1) ):
            lzbir =  aop(iopk,4148,1) 
            dzbir =  suma_liste(iopk,[4139,4146],1)-aop(iopk,4147,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4148 = AOP-u (4139 + 4146 - 4147)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40187
        if not( aop(iopk,4176,1) == suma_liste(iopk,[4166,4174],1)-aop(iopk,4175,1) ):
            lzbir =  aop(iopk,4176,1) 
            dzbir =  suma_liste(iopk,[4166,4174],1)-aop(iopk,4175,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4176 = AOP-u (4166 + 4174 - 4175)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40188
        if not( aop(iopk,4210,1) == suma_liste(iopk,[4197,4208],1)-aop(iopk,4209,1) ):
            lzbir =  aop(iopk,4210,1) 
            dzbir =  suma_liste(iopk,[4197,4208],1)-aop(iopk,4209,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4210 = AOP-u (4197 + 4208 - 4209)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40189
        if not( aop(iopk,4234,1) == suma_liste(iopk,[4226,4232],1)-aop(iopk,4233,1) ):
            lzbir =  aop(iopk,4234,1) 
            dzbir =  suma_liste(iopk,[4226,4232],1)-aop(iopk,4233,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4234 = AOP-u (4226 + 4232 - 4233)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40190
        if not( aop(iopk,4260,1) == suma_liste(iopk,[4251,4258],1)-aop(iopk,4259,1) ):
            lzbir =  aop(iopk,4260,1) 
            dzbir =  suma_liste(iopk,[4251,4258],1)-aop(iopk,4259,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4260 = AOP-u (4251 + 4258 - 4259)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40191
        if not( aop(iopk,4284,1) == suma_liste(iopk,[4276,4282],1)-aop(iopk,4283,1) ):
            lzbir =  aop(iopk,4284,1) 
            dzbir =  suma_liste(iopk,[4276,4282],1)-aop(iopk,4283,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4284 = AOP-u (4276 + 4282 - 4283)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40192
        if not( aop(iopk,4314,1) == suma_liste(iopk,[4303,4312],1)-aop(iopk,4313,1) ):
            lzbir =  aop(iopk,4314,1) 
            dzbir =  suma_liste(iopk,[4303,4312],1)-aop(iopk,4313,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4314 = AOP-u (4303 + 4312 - 4313)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40193
        if not( aop(iopk,4344,1) == suma_liste(iopk,[4336,4342],1)-aop(iopk,4343,1) ):
            lzbir =  aop(iopk,4344,1) 
            dzbir =  suma_liste(iopk,[4336,4342],1)-aop(iopk,4343,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4344 = AOP-u (4336 + 4342 - 4343)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40194
        if not( aop(iopk,4210,1) == suma_liste(iopk,[4026,4050,4074,4098,4122,4148,4176],1) ):
            lzbir =  aop(iopk,4210,1) 
            dzbir =  suma_liste(iopk,[4026,4050,4074,4098,4122,4148,4176],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4210 = AOP-u (4026 + 4050 + 4074 + 4098 + 4122 + 4148 + 4176)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40195
        if not( aop(iopk,4314,1) == suma_liste(iopk,[4234,4260,4284],1) ):
            lzbir =  aop(iopk,4314,1) 
            dzbir =  suma_liste(iopk,[4234,4260,4284],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4314 = AOP-u (4234 + 4260 + 4284)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40196
        if not( aop(iopk,4320,1) == aop(iopk,4210,1) - aop(iopk,4314,1) ):
            lzbir =  aop(iopk,4320,1) 
            dzbir =  aop(iopk,4210,1) - aop(iopk,4314,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4320 = AOP-u (4210 - 4314)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40197
        if( aop(iopk,4320,1) > 0 ):
            if not( aop(iopk,4344,1) == 0 ):
                lzbir =  aop(iopk,4344,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4320 > 0, onda je AOP 4344 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40198
        if( aop(iopk,4344,1) > 0 ):
            if not( aop(iopk,4320,1) == 0 ):
                lzbir =  aop(iopk,4320,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4344 > 0, onda je AOP 4320 = 0 Ne mogu biti istovremeno prikazani ukupan kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40199
        if not( aop(iopk,4004,1) + aop(iopk,4030,1) == suma_liste(bs,[402,421],7) ):
            lzbir =  aop(iopk,4004,1) + aop(iopk,4030,1) 
            dzbir =  suma_liste(bs,[402,421],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP (4004 + 4030) = AOP-u (0402 + 0421) kol. 7 bilans stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP (4004 + 4030) = AOP-u (0402 + 0421) kol. 7 bilans stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40200
        if not( aop(iopk,4054,1) == aop(bs,407,7) ):
            lzbir =  aop(iopk,4054,1) 
            dzbir =  aop(bs,407,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4054 = AOP-u 0407 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4054 = AOP-u 0407 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40201
        if not( aop(iopk,4078,1) == aop(bs,409,7) ):
            lzbir =  aop(iopk,4078,1) 
            dzbir =  aop(bs,409,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4078 = AOP-u 0409 kol. 7 bilans stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4078 = AOP-u 0409 kol. 7 bilans stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40202
        if not( aop(iopk,4102,1) == aop(bs,410,7) ):
            lzbir =  aop(iopk,4102,1) 
            dzbir =  aop(bs,410,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4102 = AOP-u 0410 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4102 = AOP-u 0410 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40203
        if not( aop(iopk,4126,1) == suma(bs,411,412,7) ):
            lzbir =  aop(iopk,4126,1) 
            dzbir =  suma(bs,411,412,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4126 = AOP-u (0411 + 0412) kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4126 = AOP-u (0411 + 0412) kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40204
        if not( aop(iopk,4152,1) == aop(bs,414,7) ):
            lzbir =  aop(iopk,4152,1) 
            dzbir =  aop(bs,414,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4152 = AOP-u 0414 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4152 = AOP-u 0414 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40205
        if not( aop(iopk,4214,1) == aop(bs,417,7) ):
            lzbir =  aop(iopk,4214,1) 
            dzbir =  aop(bs,417,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4214 = AOP-u 0417 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4214 = AOP-u 0417 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40206
        if not( aop(iopk,4238,1) == aop(bs,420,7) ):
            lzbir =  aop(iopk,4238,1) 
            dzbir =  aop(bs,420,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4238 = AOP-u 0420 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4238 = AOP-u 0420 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40207
        if not( aop(iopk,4264,1) == aop(bs,413,7) ):
            lzbir =  aop(iopk,4264,1) 
            dzbir =  aop(bs,413,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4264 = AOP-u 0413 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4264 = AOP-u 0413 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40208
        if not( aop(iopk,4316,1) == aop(bs,401,7) ):
            lzbir =  aop(iopk,4316,1) 
            dzbir =  aop(bs,401,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4316 = AOP-u 0401 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4316 = AOP-u 0401 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40209
        if not( aop(iopk,4324,1) == aop(bs,458,7) ):
            lzbir =  aop(iopk,4324,1) 
            dzbir =  aop(bs,458,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4324 = AOP-u 0458 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4324 = AOP-u 0458 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40210
        if not( aop(iopk,4013,1) + aop(iopk,4038,1) == suma_liste(bs,[402,421],6) ):
            lzbir =  aop(iopk,4013,1) + aop(iopk,4038,1) 
            dzbir =  suma_liste(bs,[402,421],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP (4013 + 4038) = AOP-u (0402 + 0421) kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP (4013 + 4038) = AOP-u (0402 + 0421) kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40211
        if not( aop(iopk,4062,1) == aop(bs,407,6) ):
            lzbir =  aop(iopk,4062,1) 
            dzbir =  aop(bs,407,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4062 = AOP-u 0407 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4062 = AOP-u 0407 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40212
        if not( aop(iopk,4086,1) == aop(bs,409,6) ):
            lzbir =  aop(iopk,4086,1) 
            dzbir =  aop(bs,409,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4086 = AOP-u 0409 kol. 6 bilans stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4086 = AOP-u 0409 kol. 6 bilans stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40213
        if not( aop(iopk,4110,1) == aop(bs,410,6) ):
            lzbir =  aop(iopk,4110,1) 
            dzbir =  aop(bs,410,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4110 = AOP-u 0410 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4110 = AOP-u 0410 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40214
        if not( aop(iopk,4135,1) == suma(bs,411,412,6) ):
            lzbir =  aop(iopk,4135,1) 
            dzbir =  suma(bs,411,412,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4135 = AOP-u (0411 + 0412) kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4135 = AOP-u (0411 + 0412) kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40215
        if not( aop(iopk,4162,1) == aop(bs,414,6) ):
            lzbir =  aop(iopk,4162,1) 
            dzbir =  aop(bs,414,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4162 = AOP-u 0414 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4162 = AOP-u 0414 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40216
        if not( aop(iopk,4222,1) == aop(bs,417,6) ):
            lzbir =  aop(iopk,4222,1) 
            dzbir =  aop(bs,417,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4222 = AOP-u 0417 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4222 = AOP-u 0417 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40217
        if not( aop(iopk,4247,1) == aop(bs,420,6) ):
            lzbir =  aop(iopk,4247,1) 
            dzbir =  aop(bs,420,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4247 = AOP-u 0420 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4247 = AOP-u 0420 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40218
        if not( aop(iopk,4272,1) == aop(bs,413,6) ):
            lzbir =  aop(iopk,4272,1) 
            dzbir =  aop(bs,413,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4272 = AOP-u 0413 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4272 = AOP-u 0413 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40219
        if not( aop(iopk,4317,1) == aop(bs,401,6) ):
            lzbir =  aop(iopk,4317,1) 
            dzbir =  aop(bs,401,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4317 = AOP-u 0401 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4317 = AOP-u 0401 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40220
        if not( aop(iopk,4332,1) == aop(bs,458,6) ):
            lzbir =  aop(iopk,4332,1) 
            dzbir =  aop(bs,458,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4332 = AOP-u 0458 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4332 = AOP-u 0458 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40221
        if not( aop(iopk,4026,1) + aop(iopk,4050,1) == suma_liste(bs,[402,421],5) ):
            lzbir =  aop(iopk,4026,1) + aop(iopk,4050,1) 
            dzbir =  suma_liste(bs,[402,421],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP (4026 + 4050) = AOP-u (0402 + 0421) kol. 5 bilans stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP (4026 + 4050) = AOP-u (0402 + 0421) kol. 5 bilans stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40222
        if not( aop(iopk,4074,1) == aop(bs,407,5) ):
            lzbir =  aop(iopk,4074,1) 
            dzbir =  aop(bs,407,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4074 = AOP-u 0407 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4074 = AOP-u 0407 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40223
        if not( aop(iopk,4098,1) == aop(bs,409,5) ):
            lzbir =  aop(iopk,4098,1) 
            dzbir =  aop(bs,409,5)
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4098 = AOP-u 0409 kol. 5 bilans stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4098 = AOP-u 0409 kol. 5 bilans stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40224
        if not( aop(iopk,4122,1) == aop(bs,410,5) ):
            lzbir =  aop(iopk,4122,1) 
            dzbir =  aop(bs,410,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4122 = AOP-u 0410 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4122 = AOP-u 0410 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40225
        if not( aop(iopk,4148,1) == suma(bs,411,412,5) ):
            lzbir =  aop(iopk,4148,1) 
            dzbir =  suma(bs,411,412,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4148 = AOP-u (0411 + 0412) kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4148 = AOP-u (0411 + 0412) kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40226
        if not( aop(iopk,4176,1) == aop(bs,414,5) ):
            lzbir =  aop(iopk,4176,1) 
            dzbir =  aop(bs,414,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4176 = AOP-u 0414 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4176 = AOP-u 0414 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40227
        if not( aop(iopk,4234,1) == aop(bs,417,5) ):
            lzbir =  aop(iopk,4234,1) 
            dzbir =  aop(bs,417,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4234 = AOP-u 0417 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4234 = AOP-u 0417 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40228
        if not( aop(iopk,4260,1) == aop(bs,420,5) ):
            lzbir =  aop(iopk,4260,1) 
            dzbir =  aop(bs,420,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4260 = AOP-u 0420 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4260 = AOP-u 0420 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40229
        if not( aop(iopk,4284,1) == aop(bs,413,5) ):
            lzbir =  aop(iopk,4284,1) 
            dzbir =  aop(bs,413,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4284 = AOP-u 0413 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4284 = AOP-u 0413 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40230
        if not( aop(iopk,4320,1) == aop(bs,401,5) ):
            lzbir =  aop(iopk,4320,1) 
            dzbir =  aop(bs,401,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4320 = AOP-u 0401 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4320 = AOP-u 0401 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40231
        if not( aop(iopk,4344,1) == aop(bs,458,5) ):
            lzbir =  aop(iopk,4344,1) 
            dzbir =  aop(bs,458,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4344 = AOP-u 0458 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4344 = AOP-u 0458 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        
        #POSEBNI PODACI:
        #●PRAVILO NE TREBA DA BUDE VIDLJIVO ZA KORISNIKA, ODNOSNO ZA OBVEZNIKA TREBA DA VIDI SAMO KOMENTAR KOJI JE DAT UZ PRAVILO. 
        #●U OBRASCU NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #100001
        #Za ovaj set se ne primenjuje pravilo 
        
        #100002
        if not( 2 <= aop(pp,10001,1) and 4 >= aop(pp, 10001, 1)  ):
            
            naziv_obrasca='Posebni podaci'
            poruka  =' Oznaka za veličinu mora biti  2, 3  ili 4 '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #100003
        if not( aop(pp,10002,1) >= 0 ):
            
            naziv_obrasca='Posebni podaci'
            poruka  =' Podatak o prosečnom broju zaposlenih u tekućoj godini mora biti upisan; ako nema zaposlenih upisuje se broj 0 '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        pps=Zahtev.Forme['Posebni podaci'].TekstualnaPoljaForme
        ppsnum=Zahtev.Forme['Posebni podaci'].NumerickaPoljaForme
        
        #100012
        for x in range (10100, 10300):
            if validiraj_spisak_pravnih_lica_obuhvacenih_konsolidacijom( x, aop(pps,x,2), aop(pps,x,3), aop(pps,x,4), aop(pps,x,5)) == False:
                #(Greška u redu: "+str(x-10099)+")")     
                
                naziv_obrasca='Posebni podaci'
                poruka  ='Na spisak pravnih lica koja su obuhvaćena konsolidacijom mora biti uneto bar jedno pravno lice Na spisak pravnih lica koja su obuhvaćena konsolidacijom niste uneli nijedan podatak '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #100013
        for x in range (10100, 10300):
            if aop(pps,x,5) == Zahtev.ObveznikInfo.MaticniBroj: 
                
                naziv_obrasca='Posebni podaci'
                poruka  ='Matično pravno lice ne može biti na spisku pravnih lica koja su obuhvaćena konsolidacijom Matično pravno lice ne može biti na spisku pravnih lica koja su obuhvaćena konsolidacijom '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #100014
        for x in range (10100, 10300):
            if validiraj_spisak_pravnih_lica_obuhvacenih_konsolidacijom( x, aop(pps,x,2), aop(pps,x,3), aop(pps,x,4), aop(pps,x,5)) == False: 
                
                naziv_obrasca='Posebni podaci'
                poruka  ='Za domaće pravno lice obveznik mora da unese matični broj, poslovno ime i sedište, a za strano pravno lice poslovno ime, državu i sedište Za domaće pravno lice unesite  matični broj, poslovno ime i sedište. Za strano pravno lice unesite poslovno ime, državu i sedište '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #100015
        imaDuplikate = False                               
        for x in range (10100, 10300):
            for y in range (x, 10300):
                if len(aop(pps,x,5)) != 0 and x != y and aop(pps,x,5) == aop(pps,y,5):
                    imaDuplikate = True
        if imaDuplikate:
            
            naziv_obrasca='Posebni podaci'
            poruka  ='Na spisku ne sme da se pojavi dva puta isto pravno lice Na spisak pravnih lica koja su obuhvaćena konsolidacijom uneli ste duplikate matičnih brojeva '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #100016
        for x in range (10100, 10300):
            if (aop(ppsnum, x, 1)!=0):
                if not (aop(ppsnum, x, 1)==(x-10099)): 
                    
                    naziv_obrasca='Posebni podaci'
                    poruka  ='Redni broj na spisku mora biti unet po rastućem redosledu Na spisku pravnih lica koja su obuhvaćena konsolidacijom u koloni "Redni broj" podatak nije unet po rastućem redosledu '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
        
        #100017
        for x in range(10100, 10300):
            if(aop(ppsnum, x, 1)==0):
                if( x != 10299 and aop(ppsnum, x+1,1)!=0 ):
                    
                    naziv_obrasca='Posebni podaci'
                    poruka  ='Obveznik ne sme da ostavi prazan red između pravilno unetih rednih brojeva Na spisku pravnih lica koja su obuhvaćena konsolidacijom  potrebno je popuniti kolonu "redni broj" po rastućem redosledu brojeva bez preskakanja redova '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
        
        #100018
        for x in range (10100, 10300):
            if (aop(ppsnum, x, 1) == 0):
                if (validiraj_spisak_pravnih_lica( x, aop(pps,x,2), aop(pps,x,3), aop(pps,x,4), aop(pps,x,5))): 
                    
                    naziv_obrasca='Posebni podaci'
                    poruka  ='Na spisku pravnih lica koja su obuhvaćena konsolidacijom obveznik mora uneti redni broj ukoliko je popunio podatke o zavisnom pravnom licu Na spisku pravnih lica koja su obuhvaćena konsolidacijom obveznik mora uneti redni broj ukoliko je popunio podatke o zavisnom pravnom licu '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
        
        #100019
        for x in range (10100, 10300):
            if (aop(ppsnum, x, 1) != 0 ):
                if (validiraj_spisak_pravnih_lica( x, aop(pps,x,2), aop(pps,x,3), aop(pps,x,4), aop(pps,x,5))==False): 
                    
                    naziv_obrasca='Posebni podaci'
                    poruka  ='Na spisku pravnih lica koja su obuhvaćena konsolidacijom obveznik mora uneti podatke o zavisnom pravnom licu  ukoliko je dodao redni broj  Na spisku pravnih lica koja su obuhvaćena konsolidacijom obveznik mora uneti podatke o zavisnom pravnom licu  ukoliko je dodao redni broj  '
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
        
        
