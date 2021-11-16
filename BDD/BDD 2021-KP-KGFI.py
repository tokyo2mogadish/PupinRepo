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

        ######################################
        #### POCETAK KONTROLNIH PRAVILA ######
        ######################################



        #00000-1
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-2
        if not( suma(bs,1,30,5)+suma(bs,1,30,6)+suma(bs,1,30,7)+suma(bs,401,448,5)+suma(bs,401,448,6)+suma(bs,401,448,7)+suma(bu,1001,1038,5)+suma(bu,1001,1038,6)+suma(ioor,2001,2026,5)+suma(ioor,2001,2026,6)+suma(iotg,3001,3049,3)+suma(iotg,3001,3049,4)+suma(iopk,4001,4264,1) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0030) kol.5 + (0001 do 0030) kol.6 + (0001 do 0030) kol.7  bilansa stanja+ (0401 do 0448) kol. 5 + (0401 do 0448) kol. 6 + (0401 do 0448) kol. 7 bilansa stanja + (1001 do 1038) kol. 5 + (1001 do 1038) kol. 6 bilansa uspeha + (2001 do 2026) kol. 5 + (2001 do 2026) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3049) kol. 3 + (3001 do 3049) kol. 4 izveštaja o tokovima gotovine + (4001 do 4264)kol.1 izveštaja o promenama na kapitalu > 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0030) kol.5 + (0001 do 0030) kol.6 + (0001 do 0030) kol.7  bilansa stanja+ (0401 do 0448) kol. 5 + (0401 do 0448) kol. 6 + (0401 do 0448) kol. 7 bilansa stanja + (1001 do 1038) kol. 5 + (1001 do 1038) kol. 6 bilansa uspeha + (2001 do 2026) kol. 5 + (2001 do 2026) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3049) kol. 3 + (3001 do 3049) kol. 4 izveštaja o tokovima gotovine + (4001 do 4264)kol.1 izveštaja o promenama na kapitalu > 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0030) kol.5 + (0001 do 0030) kol.6 + (0001 do 0030) kol.7  bilansa stanja+ (0401 do 0448) kol. 5 + (0401 do 0448) kol. 6 + (0401 do 0448) kol. 7 bilansa stanja + (1001 do 1038) kol. 5 + (1001 do 1038) kol. 6 bilansa uspeha + (2001 do 2026) kol. 5 + (2001 do 2026) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3049) kol. 3 + (3001 do 3049) kol. 4 izveštaja o tokovima gotovine + (4001 do 4264)kol.1 izveštaja o promenama na kapitalu > 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0030) kol.5 + (0001 do 0030) kol.6 + (0001 do 0030) kol.7  bilansa stanja+ (0401 do 0448) kol. 5 + (0401 do 0448) kol. 6 + (0401 do 0448) kol. 7 bilansa stanja + (1001 do 1038) kol. 5 + (1001 do 1038) kol. 6 bilansa uspeha + (2001 do 2026) kol. 5 + (2001 do 2026) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3049) kol. 3 + (3001 do 3049) kol. 4 izveštaja o tokovima gotovine + (4001 do 4264)kol.1 izveštaja o promenama na kapitalu > 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0030) kol.5 + (0001 do 0030) kol.6 + (0001 do 0030) kol.7  bilansa stanja+ (0401 do 0448) kol. 5 + (0401 do 0448) kol. 6 + (0401 do 0448) kol. 7 bilansa stanja + (1001 do 1038) kol. 5 + (1001 do 1038) kol. 6 bilansa uspeha + (2001 do 2026) kol. 5 + (2001 do 2026) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3049) kol. 3 + (3001 do 3049) kol. 4 izveštaja o tokovima gotovine + (4001 do 4264)kol.1 izveštaja o promenama na kapitalu > 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}
        #00000-3
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-4
        # U bar jednoj od tri navedene forme kolona napomena mora da ima bar jedan karakter
        bsNapomene = Zahtev.Forme['Bilans stanja'].TekstualnaPoljaForme;
        buNapomene = Zahtev.Forme['Bilans uspeha'].TekstualnaPoljaForme;
        ioorNapomene = Zahtev.Forme['Izveštaj o ostalom rezultatu'].TekstualnaPoljaForme;

        if not(proveriNapomene(bsNapomene, 1, 30, 4) or proveriNapomene(bsNapomene, 401, 448, 4) or proveriNapomene(buNapomene, 1001, 1038, 4) or proveriNapomene(ioorNapomene, 2001, 2026, 4)): 
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Na AOP-u (0001 do 0030) + (0401 do 0448) bilansa stanja + (1001 do 1038) bilansa uspeha + (2001 do 2026) izveštaja o ostalom rezultatu u koloni 4 (Napomena broj) mora biti unet bar jedan karakter Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ='Na AOP-u (0001 do 0030) + (0401 do 0448) bilansa stanja + (1001 do 1038) bilansa uspeha + (2001 do 2026) izveštaja o ostalom rezultatu u koloni 4 (Napomena broj) mora biti unet bar jedan karakter Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='Na AOP-u (0001 do 0030) + (0401 do 0448) bilansa stanja + (1001 do 1038) bilansa uspeha + (2001 do 2026) izveštaja o ostalom rezultatu u koloni 4 (Napomena broj) mora biti unet bar jedan karakter Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        #Provera da li je fizahtev placen
        if not(Zahtev.Placen):
            ostalo_errors.append('Naknada za obradu i javno objavljivanje izveštaja i propisane dokumentacije nije uplaćena u propisanom iznosu. Instrukcije za uplatu propisane naknade date su u okviru PIS FI sistema za konkretan zahtev, na linku „Status naplate zahteva / Instrukcija za plaćanje". Ukoliko ste izvršili uplatu, a naknada nije uparena, priložite Dokaz o uplati naknade u delu Dokumentacija (na mestu predviđenom za dokaz o uplati naknade), kako biste mogli da podnesete izveštaj.');

        #Provera negativnih AOP-a
        lista=""
        lista_bs = find_negativni(bs, 1, 448, 5, 7)
        lista_bu = find_negativni(bu, 1001, 1038, 5, 6)
        lista_ioor = find_negativni(ioor, 2001, 2026, 5, 6)
        lista_iotg = find_negativni(iotg, 3001, 3049, 3, 4)
        lista_iopk = find_negativni(iopk, 4001, 4264, 1, 1)
       
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
        if not( suma(bs,1,30,5)+suma(bs,401,448,5) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0030) kol. 5 + (0401 do 0448) kol. 5 > 0 Bilans stanja, po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #00002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,30,6)+suma(bs,401,448,6) == 0 ):
                lzbir =  suma(bs,1,30,6)+suma(bs,401,448,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0030) kol. 6 + (0401 do 0448) kol. 6 = 0 Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00003
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,30,7)+suma(bs,401,448,7) == 0 ):
                lzbir =  suma(bs,1,30,7)+suma(bs,401,448,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0030) kol. 7 + (0401 do 0448) kol. 7 = 0 Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00004
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,30,6)+suma(bs,401,448,6) > 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0030) kol. 6 + (0401 do 0448) kol. 6 > 0 Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #00005
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,30,7)+suma(bs,401,448,7) > 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0030) kol. 7 + (0401 do 0448) kol. 7 > 0 Bilans stanja, po pravilu,  mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #00006
        if not( aop(bs,1,5) == suma_liste(bs,[2,3,6,9,10,11,12],5) ):
            lzbir =  aop(bs,1,5) 
            dzbir =  suma_liste(bs,[2,3,6,9,10,11,12],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0001 kol. 5 = AOP-u (0002 + 0003 + 0006 + 0009 + 0010 + 0011 + 0012) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00007
        if not( aop(bs,1,6) == suma_liste(bs,[2,3,6,9,10,11,12],6) ):
            lzbir =  aop(bs,1,6) 
            dzbir =  suma_liste(bs,[2,3,6,9,10,11,12],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0001 kol. 6 = AOP-u (0002 + 0003 + 0006 + 0009 + 0010 + 0011 + 0012) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00008
        if not( aop(bs,1,7) == suma_liste(bs,[2,3,6,9,10,11,12],7) ):
            lzbir =  aop(bs,1,7) 
            dzbir =  suma_liste(bs,[2,3,6,9,10,11,12],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0001 kol. 7 = AOP-u (0002 + 0003 + 0006 + 0009 + 0010 + 0011 + 0012) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00009
        if not( aop(bs,3,5) == suma(bs,4,5,5) ):
            lzbir =  aop(bs,3,5) 
            dzbir =  suma(bs,4,5,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0003 kol. 5 = AOP-u (0004 + 0005) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00010
        if not( aop(bs,3,6) == suma(bs,4,5,6) ):
            lzbir =  aop(bs,3,6) 
            dzbir =  suma(bs,4,5,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0003 kol. 6 = AOP-u (0004 + 0005) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00011
        if not( aop(bs,3,7) == suma(bs,4,5,7) ):
            lzbir =  aop(bs,3,7) 
            dzbir =  suma(bs,4,5,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0003 kol. 7 = AOP-u (0004 + 0005) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00012
        if not( aop(bs,6,5) == suma(bs,7,8,5) ):
            lzbir =  aop(bs,6,5) 
            dzbir =  suma(bs,7,8,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0006 kol. 5 = AOP-u (0007 + 0008) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00013
        if not( aop(bs,6,6) == suma(bs,7,8,6) ):
            lzbir =  aop(bs,6,6) 
            dzbir =  suma(bs,7,8,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0006 kol. 6 = AOP-u (0007 + 0008) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00014
        if not( aop(bs,6,7) == suma(bs,7,8,7) ):
            lzbir =  aop(bs,6,7) 
            dzbir =  suma(bs,7,8,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0006 kol. 7 = AOP-u (0007 + 0008) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00015
        if not( aop(bs,13,5) == suma_liste(bs,[14,15,16,24],5) ):
            lzbir =  aop(bs,13,5) 
            dzbir =  suma_liste(bs,[14,15,16,24],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0013 kol. 5 = AOP-u (0014 + 0015 + 0016 + 0024) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00016
        if not( aop(bs,13,6) == suma_liste(bs,[14,15,16,24],6) ):
            lzbir =  aop(bs,13,6) 
            dzbir =  suma_liste(bs,[14,15,16,24],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0013 kol. 6 = AOP-u (0014 + 0015 + 0016 + 0024) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00017
        if not( aop(bs,13,7) == suma_liste(bs,[14,15,16,24],7) ):
            lzbir =  aop(bs,13,7) 
            dzbir =  suma_liste(bs,[14,15,16,24],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0013 kol. 7 = AOP-u (0014 + 0015 + 0016 + 0024) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00018
        if not( aop(bs,16,5) == suma(bs,17,23,5) ):
            lzbir =  aop(bs,16,5) 
            dzbir =  suma(bs,17,23,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0016 kol. 5 = AOP-u (0017 + 0018 + 0019 + 0020 + 0021 + 0022 + 0023) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00019
        if not( aop(bs,16,6) == suma(bs,17,23,6) ):
            lzbir =  aop(bs,16,6) 
            dzbir =  suma(bs,17,23,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0016 kol. 6 = AOP-u (0017 + 0018 + 0019 + 0020 + 0021 + 0022 + 0023) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00020
        if not( aop(bs,16,7) == suma(bs,17,23,7) ):
            lzbir =  aop(bs,16,7) 
            dzbir =  suma(bs,17,23,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0016 kol. 7 = AOP-u (0017 + 0018 + 0019 + 0020 + 0021 + 0022 + 0023) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00021
        if not( aop(bs,24,5) == suma(bs,25,26,5) ):
            lzbir =  aop(bs,24,5) 
            dzbir =  suma(bs,25,26,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0024 kol. 5 = AOP-u (0025 + 0026) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00022
        if not( aop(bs,24,6) == suma(bs,25,26,6) ):
            lzbir =  aop(bs,24,6) 
            dzbir =  suma(bs,25,26,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0024 kol. 6 = AOP-u (0025 + 0026) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00023
        if not( aop(bs,24,7) == suma(bs,25,26,7) ):
            lzbir =  aop(bs,24,7) 
            dzbir =  suma(bs,25,26,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0024 kol. 7 = AOP-u (0025 + 0026) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00024
        if not( aop(bs,29,5) == suma_liste(bs,[1,13,27,28],5) ):
            lzbir =  aop(bs,29,5) 
            dzbir =  suma_liste(bs,[1,13,27,28],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0029 kol. 5 = AOP-u (0001 + 0013 + 0027 + 0028) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00025
        if not( aop(bs,29,6) == suma_liste(bs,[1,13,27,28],6) ):
            lzbir =  aop(bs,29,6) 
            dzbir =  suma_liste(bs,[1,13,27,28],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0029 kol. 6 = AOP-u (0001 + 0013 + 0027 + 0028) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00026
        if not( aop(bs,29,7) == suma_liste(bs,[1,13,27,28],7) ):
            lzbir =  aop(bs,29,7) 
            dzbir =  suma_liste(bs,[1,13,27,28],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0029 kol. 7 = AOP-u (0001 + 0013 + 0027 + 0028) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00027
        if( suma_liste(bs,[402,404,407,408,409,411,414],5) > suma_liste(bs,[403,410,415,418],5) ):
            if not( aop(bs,401,5) == suma_liste(bs,[402,404,407,408,409,411,414],5)-suma_liste(bs,[403,410,415,418],5) ):
                lzbir =  aop(bs,401,5) 
                dzbir =  suma_liste(bs,[402,404,407,408,409,411,414],5)-suma_liste(bs,[403,410,415,418],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0401 kol. 5 = AOP-u (0402 - 0403 + 0404 + 0407 + 0408 + 0409 - 0410 + 0411 + 0414 - 0415 - 0418) kol. 5, ako je AOP (0402 + 0404 + 0407 + 0408 + 0409 + 0411 + 0414)  kol. 5 > AOP-a (0403 + 0410 + 0415 + 0418) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00028
        if( suma_liste(bs,[402,404,407,408,409,411,414],6) > suma_liste(bs,[403,410,415,418],6) ):
            if not( aop(bs,401,6) == suma_liste(bs,[402,404,407,408,409,411,414],6)-suma_liste(bs,[403,410,415,418],6) ):
                lzbir =  aop(bs,401,6) 
                dzbir =  suma_liste(bs,[402,404,407,408,409,411,414],6)-suma_liste(bs,[403,410,415,418],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0401 kol. 6 = AOP-u (0402 - 0403 + 0404 + 0407 + 0408 + 0409 - 0410 + 0411 + 0414 - 0415 - 0418) kol. 6, ako je AOP (0402 + 0404 + 0407 + 0408 + 0409 + 0411 + 0414)  kol. 6 > AOP-a (0403 + 0410 + 0415 + 0418) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00029
        if( suma_liste(bs,[402,404,407,408,409,411,414],7) > suma_liste(bs,[403,410,415,418],7) ):
            if not( aop(bs,401,7) == suma_liste(bs,[402,404,407,408,409,411,414],7)-suma_liste(bs,[403,410,415,418],7) ):
                lzbir =  aop(bs,401,7) 
                dzbir =  suma_liste(bs,[402,404,407,408,409,411,414],7)-suma_liste(bs,[403,410,415,418],7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0401 kol. 7 = AOP-u (0402 - 0403 + 0404 + 0407 + 0408 + 0409 - 0410 + 0411 + 0414 - 0415 - 0418) kol. 7, ako je AOP (0402 + 0404 + 0407 + 0408 + 0409 + 0411 + 0414)  kol. 7 > AOP-a (0403 + 0410 + 0415 + 0418) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00030
        if( aop(bs,29,5) > suma_liste(bs,[419,444,445],5) ):
            if not( aop(bs,401,5) == aop(bs,29,5)-suma_liste(bs,[419,444,445],5) ):
                lzbir =  aop(bs,401,5) 
                dzbir =  aop(bs,29,5)-suma_liste(bs,[419,444,445],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP  0401 kol. 5 = AOP-u (0029 - 0419 - 0444 - 0445) kol. 5, ako je AOP 0029 kol. 5  >  AOP-a (0419 + 0444 + 0445) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00031
        if( aop(bs,29,6) > suma_liste(bs,[419,444,445],6) ):
            if not( aop(bs,401,6) == aop(bs,29,6)-suma_liste(bs,[419,444,445],6) ):
                lzbir =  aop(bs,401,6) 
                dzbir =  aop(bs,29,6)-suma_liste(bs,[419,444,445],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP  0401 kol. 6 = AOP-u (0029 - 0419 - 0444 - 0445) kol. 6, ako je AOP 0029 kol. 6 > AOP-a (0419 + 0444 + 0445) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00032
        if( aop(bs,29,7) > suma_liste(bs,[419,444,445],7) ):
            if not( aop(bs,401,7) == aop(bs,29,7)-suma_liste(bs,[419,444,445],7) ):
                lzbir =  aop(bs,401,7) 
                dzbir =  aop(bs,29,7)-suma_liste(bs,[419,444,445],7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP  0401 kol. 7 = AOP-u (0029 - 0419 - 0444 - 0445) kol. 7, ako je AOP 0029 kol. 7 > AOP-a (0419 + 0444 + 0445) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00033
        if not( aop(bs,404,5) == suma(bs,405,406,5) ):
            lzbir =  aop(bs,404,5) 
            dzbir =  suma(bs,405,406,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0404 kol. 5 = AOP-u (0405 + 0406) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00034
        if not( aop(bs,404,6) == suma(bs,405,406,6) ):
            lzbir =  aop(bs,404,6) 
            dzbir =  suma(bs,405,406,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0404 kol. 6 = AOP-u (0405 + 0406) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00035
        if not( aop(bs,404,7) == suma(bs,405,406,7) ):
            lzbir =  aop(bs,404,7) 
            dzbir =  suma(bs,405,406,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0404 kol. 7 = AOP-u (0405 + 0406) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00036
        if not( aop(bs,411,5) == suma(bs,412,413,5) ):
            lzbir =  aop(bs,411,5) 
            dzbir =  suma(bs,412,413,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0411 kol. 5 = AOP-u (0412 + 0413) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00037
        if not( aop(bs,411,6) == suma(bs,412,413,6) ):
            lzbir =  aop(bs,411,6) 
            dzbir =  suma(bs,412,413,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0411 kol. 6 = AOP-u (0412 + 0413) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00038
        if not( aop(bs,411,7) == suma(bs,412,413,7) ):
            lzbir =  aop(bs,411,7) 
            dzbir =  suma(bs,412,413,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0411 kol. 7 = AOP-u (0412 + 0413) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00039
        #Za ovaj set se ne primenjuje pravilo 
        
        #00040
        #Za ovaj set se ne primenjuje pravilo 
        
        #00041
        #Za ovaj set se ne primenjuje pravilo 
        
        #00042
        if not( aop(bs,415,5) == suma(bs,416,417,5) ):
            lzbir =  aop(bs,415,5) 
            dzbir =  suma(bs,416,417,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0415 kol. 5 = AOP-u (0416 + 0417) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00043
        if not( aop(bs,415,6) == suma(bs,416,417,6) ):
            lzbir =  aop(bs,415,6) 
            dzbir =  suma(bs,416,417,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0415 kol. 6 = AOP-u (0416 + 0417) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00044
        if not( aop(bs,415,7) == suma(bs,416,417,7) ):
            lzbir =  aop(bs,415,7) 
            dzbir =  suma(bs,416,417,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0415 kol. 7 = AOP-u (0416 + 0417) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00045
        if not( aop(bs,419,5) == suma_liste(bs,[420,421,422,428,434,440],5) ):
            lzbir =  aop(bs,419,5) 
            dzbir =  suma_liste(bs,[420,421,422,428,434,440],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0419 kol. 5 = AOP-u (0420 + 0421 + 0422 + 0428 + 0434 + 0440) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00046
        if not( aop(bs,419,6) == suma_liste(bs,[420,421,422,428,434,440],6) ):
            lzbir =  aop(bs,419,6) 
            dzbir =  suma_liste(bs,[420,421,422,428,434,440],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0419 kol. 6 = AOP-u (0420 + 0421 + 0422 + 0428 + 0434 + 0440) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00047
        if not( aop(bs,419,7) == suma_liste(bs,[420,421,422,428,434,440],7) ):
            lzbir =  aop(bs,419,7) 
            dzbir =  suma_liste(bs,[420,421,422,428,434,440],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0419 kol. 7 = AOP-u (0420 + 0421 + 0422 + 0428 + 0434 + 0440) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00048
        if not( aop(bs,422,5) == suma(bs,423,427,5) ):
            lzbir =  aop(bs,422,5) 
            dzbir =  suma(bs,423,427,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0422 kol. 5 = AOP-u (0423 + 0424 + 0425 + 0426 + 0427) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00049
        if not( aop(bs,422,6) == suma(bs,423,427,6) ):
            lzbir =  aop(bs,422,6) 
            dzbir =  suma(bs,423,427,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0422 kol. 6 = AOP-u (0423 + 0424 + 0425 + 0426 + 0427) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00050
        if not( aop(bs,422,7) == suma(bs,423,427,7) ):
            lzbir =  aop(bs,422,7) 
            dzbir =  suma(bs,423,427,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0422 kol. 7 = AOP-u (0423 + 0424 + 0425 + 0426 + 0427) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00051
        if not( aop(bs,428,5) == suma(bs,429,433,5) ):
            lzbir =  aop(bs,428,5) 
            dzbir =  suma(bs,429,433,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0428 kol. 5 = AOP-u (0429 + 0430 + 0431 + 0432 + 0433) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00052
        if not( aop(bs,428,6) == suma(bs,429,433,6) ):
            lzbir =  aop(bs,428,6) 
            dzbir =  suma(bs,429,433,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0428 kol. 6 = AOP-u (0429 + 0430 + 0431 + 0432 + 0433) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00053
        if not( aop(bs,428,7) == suma(bs,429,433,7) ):
            lzbir =  aop(bs,428,7) 
            dzbir =  suma(bs,429,433,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0428 kol. 7 = AOP-u (0429 + 0430 + 0431 + 0432 + 0433) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00054
        if not( aop(bs,434,5) == suma(bs,435,439,5) ):
            lzbir =  aop(bs,434,5) 
            dzbir =  suma(bs,435,439,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0434 kol. 5 = AOP-u (0435 + 0436 + 0437 + 0438 + 0439) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00055
        if not( aop(bs,434,6) == suma(bs,435,439,6) ):
            lzbir =  aop(bs,434,6) 
            dzbir =  suma(bs,435,439,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0434 kol. 6 = AOP-u (0435 + 0436 + 0437 + 0438 + 0439) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00056
        if not( aop(bs,434,7) == suma(bs,435,439,7) ):
            lzbir =  aop(bs,434,7) 
            dzbir =  suma(bs,435,439,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0434 kol. 7 = AOP-u (0435 + 0436 + 0437 + 0438 + 0439) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00057
        if not( aop(bs,440,5) == suma(bs,441,443,5) ):
            lzbir =  aop(bs,440,5) 
            dzbir =  suma(bs,441,443,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0440 kol. 5 = AOP-u (0441 + 0442 + 0443) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00058
        if not( aop(bs,440,6) == suma(bs,441,443,6) ):
            lzbir =  aop(bs,440,6) 
            dzbir =  suma(bs,441,443,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0440 kol. 6 = AOP-u (0441 + 0442 + 0443) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00059
        if not( aop(bs,440,7) == suma(bs,441,443,7) ):
            lzbir =  aop(bs,440,7) 
            dzbir =  suma(bs,441,443,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0440 kol. 7 = AOP-u (0441 + 0442 + 0443) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00060
        if( suma_liste(bs,[402,404,407,408,409,411,414],5) < suma_liste(bs,[403,410,415,418],5) ):
            if not( aop(bs,446,5) == suma_liste(bs,[403,410,415,418],5)-suma_liste(bs,[402,404,407,408,409,411,414],5) ):
                lzbir =  aop(bs,446,5) 
                dzbir =  suma_liste(bs,[403,410,415,418],5)-suma_liste(bs,[402,404,407,408,409,411,414],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0446 kol. 5 = AOP-u (0403 + 0410 + 0415 + 0418 - 0402 - 0404 - 0407 - 0408 - 0409 - 0411 - 0414) kol. 5, ako je AOP (0402 + 0404 + 0407 + 0408 + 0409 + 0411 + 0414) kol. 5 < AOP-a (0403 + 0410 + 0415 + 0418) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00061
        if( suma_liste(bs,[402,404,407,408,409,411,414],6) < suma_liste(bs,[403,410,415,418],6) ):
            if not( aop(bs,446,6) == suma_liste(bs,[403,410,415,418],6)-suma_liste(bs,[402,404,407,408,409,411,414],6) ):
                lzbir =  aop(bs,446,6) 
                dzbir =  suma_liste(bs,[403,410,415,418],6)-suma_liste(bs,[402,404,407,408,409,411,414],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0446 kol. 6 = AOP-u (0403 + 0410 + 0415 + 0418 - 0402 - 0404 - 0407 - 0408 - 0409 - 0411 - 0414) kol. 6, ako je AOP (0402 + 0404 + 0407 + 0408 + 0409 + 0411 + 0414) kol. 6 < AOP-a (0403 + 0410 + 0415 + 0418) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00062
        if( suma_liste(bs,[402,404,407,408,409,411,414],7) < suma_liste(bs,[403,410,415,418],7) ):
            if not( aop(bs,446,7) == suma_liste(bs,[403,410,415,418],7)-suma_liste(bs,[402,404,407,408,409,411,414],7) ):
                lzbir =  aop(bs,446,7) 
                dzbir =  suma_liste(bs,[403,410,415,418],7)-suma_liste(bs,[402,404,407,408,409,411,414],7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0446 kol. 7 = AOP-u (0403 + 0410 + 0415 + 0418 - 0402 - 0404 - 0407 - 0408 - 0409 - 0411 - 0414) kol. 7, ako je AOP (0402 + 0404 + 0407 + 0408 + 0409 + 0411 + 0414) kol. 7 < AOP-a (0403 + 0410 + 0415 + 0418) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00063
        if( aop(bs,29,5) < suma_liste(bs,[419,444,445],5) ):
            if not( aop(bs,446,5) == suma_liste(bs,[419,444,445],5)-aop(bs,29,5) ):
                lzbir =  aop(bs,446,5) 
                dzbir =  suma_liste(bs,[419,444,445],5)-aop(bs,29,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0446 kol. 5 = AOP-u (0419 + 0444 + 0445 - 0029) kol. 5, ako je AOP 0029 kol. 5 < AOP-a (0419 + 0444 + 0445) kol. 5   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00064
        if( aop(bs,29,6) < suma_liste(bs,[419,444,445],6) ):
            if not( aop(bs,446,6) == suma_liste(bs,[419,444,445],6)-aop(bs,29,6) ):
                lzbir =  aop(bs,446,6) 
                dzbir =  suma_liste(bs,[419,444,445],6)-aop(bs,29,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0446 kol. 6 = AOP-u (0419 + 0444 + 0445 - 0029) kol. 6, ako je AOP 0029 kol. 6 < AOP-a (0419 + 0444 + 0445) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00065
        if( aop(bs,29,7) < suma_liste(bs,[419,444,445],7) ):
            if not( aop(bs,446,7) == suma_liste(bs,[419,444,445],7)-aop(bs,29,7) ):
                lzbir =  aop(bs,446,7) 
                dzbir =  suma_liste(bs,[419,444,445],7)-aop(bs,29,7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0446 kol. 7 = AOP-u (0419 + 0444 + 0445 - 0029) kol. 7, ako je AOP 0029 kol. 7 < AOP-a (0419 + 0444 + 0445) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00066
        if( suma_liste(bs,[402,404,407,408,409,411,414],5) == suma_liste(bs,[403,410,415,418],5) ):
            if not( suma_liste(bs,[401,446],5) == 0 ):
                lzbir =  suma_liste(bs,[401,446],5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0446) kol. 5 = 0, ako je AOP (0402 + 0404 + 0407 + 0408 + 0409 + 0411 + 0414) kol. 5 = AOP-u (0403 + 0410 + 0415 + 0418) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00067
        if( suma_liste(bs,[402,404,407,408,409,411,414],6) == suma_liste(bs,[403,410,415,418],6) ):
            if not( suma_liste(bs,[401,446],6) == 0 ):
                lzbir =  suma_liste(bs,[401,446],6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0446) kol. 6 = 0, ako je AOP (0402 + 0404 + 0407 + 0408 + 0409 + 0411 + 0414) kol. 6 = AOP-u (0403 + 0410 + 0415 + 0418) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00068
        if( suma_liste(bs,[402,404,407,408,409,411,414],7) == suma_liste(bs,[403,410,415,418],7) ):
            if not( suma_liste(bs,[401,446],7) == 0 ):
                lzbir =  suma_liste(bs,[401,446],7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0446) kol. 7 = 0, ako je AOP (0402 + 0404 + 0407 + 0408 + 0409 + 0411 + 0414) kol. 7 = AOP-u (0403 + 0410 + 0415 + 0418) kol. 7 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00069
        if( aop(bs,29,5) == suma_liste(bs,[419,444,445],5) ):
            if not( suma_liste(bs,[401,446],5) == 0 ):
                lzbir =  suma_liste(bs,[401,446],5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0446) kol. 5 = 0, ako je AOP 0029 kol. 5 = AOP-u (0419 + 0444 + 0445) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00070
        if( aop(bs,29,6) == suma_liste(bs,[419,444,445],6) ):
            if not( suma_liste(bs,[401,446],6) == 0 ):
                lzbir =  suma_liste(bs,[401,446],6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0446) kol. 6 = 0, ako je AOP 0029 kol. 6 = AOP-u (0419 + 0444 + 0445) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00071
        if( aop(bs,29,7) == suma_liste(bs,[419,444,445],7) ):
            if not( suma_liste(bs,[401,446],7) == 0 ):
                lzbir =  suma_liste(bs,[401,446],7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0446) kol. 7 = 0, ako je AOP 0029 kol. 7 = AOP-u (0419 + 0444 + 0445) kol. 7 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00072
        if( aop(bs,401,5) > 0 ):
            if not( aop(bs,446,5) == 0 ):
                lzbir =  aop(bs,446,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0401 kol. 5 > 0 onda je AOP 0446 kol. 5 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00073
        if( aop(bs,446,5) > 0 ):
            if not( aop(bs,401,5) == 0 ):
                lzbir =  aop(bs,401,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0446 kol. 5 > 0 onda je AOP 0401 kol. 5 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00074
        if( aop(bs,401,6) > 0 ):
            if not( aop(bs,446,6) == 0 ):
                lzbir =  aop(bs,446,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0401 kol. 6 > 0 onda je AOP 0446 kol. 6 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00075
        if( aop(bs,446,6) > 0 ):
            if not( aop(bs,401,6) == 0 ):
                lzbir =  aop(bs,401,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0446 kol. 6 > 0 onda je AOP 0401 kol. 6 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00076
        if( aop(bs,401,7) > 0 ):
            if not( aop(bs,446,7) == 0 ):
                lzbir =  aop(bs,446,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0401 kol. 7 > 0 onda je AOP 0446 kol. 7 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00077
        if( aop(bs,446,7) > 0 ):
            if not( aop(bs,401,7) == 0 ):
                lzbir =  aop(bs,401,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0446 kol. 7 > 0 onda je AOP 0401 kol. 7 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00078
        if not( aop(bs,447,5) == suma_liste(bs,[401,419,444,445],5)-aop(bs,446,5) ):
            lzbir =  aop(bs,447,5) 
            dzbir =  suma_liste(bs,[401,419,444,445],5)-aop(bs,446,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0447 kol. 5 = AOP-u (0401 + 0419 + 0444 + 0445 - 0446) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00079
        if not( aop(bs,447,6) == suma_liste(bs,[401,419,444,445],6)-aop(bs,446,6) ):
            lzbir =  aop(bs,447,6) 
            dzbir =  suma_liste(bs,[401,419,444,445],6)-aop(bs,446,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0447 kol. 6 = AOP-u (0401 + 0419 + 0444 + 0445 - 0446) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00080
        if not( aop(bs,447,7) == suma_liste(bs,[401,419,444,445],7)-aop(bs,446,7) ):
            lzbir =  aop(bs,447,7) 
            dzbir =  suma_liste(bs,[401,419,444,445],7)-aop(bs,446,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0447 kol. 7 = AOP-u (0401 + 0419 + 0444 + 0445 - 0446) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00081
        if not( aop(bs,29,5) == aop(bs,447,5) ):
            lzbir =  aop(bs,29,5) 
            dzbir =  aop(bs,447,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0029 kol. 5 = AOP-u 0447 kol. 5 Kontrolni pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00082
        if not( aop(bs,29,6) == aop(bs,447,6) ):
            lzbir =  aop(bs,29,6) 
            dzbir =  aop(bs,447,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0029 kol. 6 = AOP-u 0447 kol. 6 Kontrolni pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00083
        if not( aop(bs,29,7) == aop(bs,447,7) ):
            lzbir =  aop(bs,29,7) 
            dzbir =  aop(bs,447,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0029 kol. 7 = AOP-u 0447 kol. 7 Kontrolni pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00084
        if not( aop(bs,30,5) == aop(bs,448,5) ):
            lzbir =  aop(bs,30,5) 
            dzbir =  aop(bs,448,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0030 kol. 5 = AOP-u 0448 kol. 5 Kontrolni pravilo zahteva slaganje vanbilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00085
        if not( aop(bs,30,6) == aop(bs,448,6) ):
            lzbir =  aop(bs,30,6) 
            dzbir =  aop(bs,448,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0030 kol. 6 = AOP-u 0448 kol. 6 Kontrolni pravilo zahteva slaganje vanbilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00086
        if not( aop(bs,30,7) == aop(bs,448,7) ):
            lzbir =  aop(bs,30,7) 
            dzbir =  aop(bs,448,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0030 kol. 7 = AOP-u 0448 kol. 7 Kontrolni pravilo zahteva slaganje vanbilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00087
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if( suma(bu,1001,1038,5) > 0 ):
                if not( suma(bs,1,30,5)+suma(bs,401,448,5) != suma(bs,1,30,6)+suma(bs,401,448,6) ):
                    
                    naziv_obrasca='Bilans uspeha'
                    poruka  ='***Ako je zbir podataka na oznakama za AOP (1001 do 1038) kol. 5 bilansa uspeha > 0 onda zbir podataka na oznakama za AOP (0001 do 0030) kol. 5 + (0401 do 0448) kol. 5 ≠ zbiru podataka na oznakama za AOP (0001 do 0030) kol. 6 + (0401 do 0448) kol. 6 Zbirovi podataka u kolonama 5 i 6 bilansa stanja su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama;  '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ='***Ako je zbir podataka na oznakama za AOP (1001 do 1038) kol. 5 bilansa uspeha > 0 onda zbir podataka na oznakama za AOP (0001 do 0030) kol. 5 + (0401 do 0448) kol. 5 ≠ zbiru podataka na oznakama za AOP (0001 do 0030) kol. 6 + (0401 do 0448) kol. 6 Zbirovi podataka u kolonama 5 i 6 bilansa stanja su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama;  '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
        
        #BILANS USPEHA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #10001
        if not( suma(bu,1001,1038,5) > 0 ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP (1001 do 1038) kol. 5 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #10002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bu,1001,1038,6) == 0 ):
                lzbir =  suma(bu,1001,1038,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Zbir podataka na oznakama za AOP (1001 do 1038) kol. 6 = 0 Bilans uspeha za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bu,1001,1038,6) > 0 ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Zbir podataka na oznakama za AOP (1001 do 1038) kol. 6 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10004
        if not( aop(bu,1002,5) == suma(bu,1003,1005,5) ):
            lzbir =  aop(bu,1002,5) 
            dzbir =  suma(bu,1003,1005,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1002 kol. 5 = AOP-u (1003 + 1004 + 1005) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10005
        if not( aop(bu,1002,6) == suma(bu,1003,1005,6) ):
            lzbir =  aop(bu,1002,6) 
            dzbir =  suma(bu,1003,1005,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1002 kol. 6 = AOP-u (1003 + 1004 + 1005) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10006
        if( aop(bu,1001,5) > aop(bu,1002,5) ):
            if not( aop(bu,1006,5) == aop(bu,1001,5)-aop(bu,1002,5) ):
                lzbir =  aop(bu,1006,5) 
                dzbir =  aop(bu,1001,5)-aop(bu,1002,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1006 kol. 5 = AOP-u (1001 - 1002) kol. 5, ako je AOP 1001 kol. 5 > AOP-a 1002 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10007
        if( aop(bu,1001,6) > aop(bu,1002,6) ):
            if not( aop(bu,1006,6) == aop(bu,1001,6)-aop(bu,1002,6) ):
                lzbir =  aop(bu,1006,6) 
                dzbir =  aop(bu,1001,6)-aop(bu,1002,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1006 kol. 6 = AOP-u (1001 - 1002) kol. 6, ako je AOP 1001 kol. 6 > AOP-a 1002 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10008
        if( aop(bu,1001,5) < aop(bu,1002,5) ):
            if not( aop(bu,1007,5) == aop(bu,1002,5)-aop(bu,1001,5) ):
                lzbir =  aop(bu,1007,5) 
                dzbir =  aop(bu,1002,5)-aop(bu,1001,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1007 kol. 5 = AOP-u (1002 - 1001) kol. 5, ako je AOP 1001 kol. 5 < AOP-a 1002 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10009
        if( aop(bu,1001,6) < aop(bu,1002,6) ):
            if not( aop(bu,1007,6) == aop(bu,1002,6)-aop(bu,1001,6) ):
                lzbir =  aop(bu,1007,6) 
                dzbir =  aop(bu,1002,6)-aop(bu,1001,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1007 kol. 6 = AOP-u (1002 - 1001) kol. 6, ako je AOP 1001 kol. 6 < AOP-a 1002 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10010
        if( aop(bu,1001,5) == aop(bu,1002,5) ):
            if not( suma(bu,1006,1007,5) == 0 ):
                lzbir =  suma(bu,1006,1007,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  =' AOP (1006 + 1007) kol. 5 = 0, ako je AOP 1001 kol. 5 = AOP-u 1002 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10011
        if( aop(bu,1001,6) == aop(bu,1002,6) ):
            if not( suma(bu,1006,1007,6) == 0 ):
                lzbir =  suma(bu,1006,1007,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  =' AOP (1006 + 1007) kol. 6 = 0, ako je AOP 1001 kol. 6 = AOP-u 1002 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10012
        if( aop(bu,1006,5) > 0 ):
            if not( aop(bu,1007,5) == 0 ):
                lzbir =  aop(bu,1007,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1006 kol. 5 > 0 onda je AOP 1007 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10013
        if( aop(bu,1007,5) > 0 ):
            if not( aop(bu,1006,5) == 0 ):
                lzbir =  aop(bu,1006,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1007 kol. 5 > 0 onda je AOP 1006 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10014
        if( aop(bu,1006,6) > 0 ):
            if not( aop(bu,1007,6) == 0 ):
                lzbir =  aop(bu,1007,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1006 kol. 6 > 0 onda je AOP 1007 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10015
        if( aop(bu,1007,6) > 0 ):
            if not( aop(bu,1006,6) == 0 ):
                lzbir =  aop(bu,1006,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1007 kol. 6 > 0 onda je AOP 1006 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10016
        if not( suma_liste(bu,[1001,1007],5) == suma_liste(bu,[1002,1006],5) ):
            lzbir =  suma_liste(bu,[1001,1007],5) 
            dzbir =  suma_liste(bu,[1002,1006],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1007) kol. 5 = AOP-u (1002 + 1006) kol.5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10017
        if not( suma_liste(bu,[1001,1007],6) == suma_liste(bu,[1002,1006],6) ):
            lzbir =  suma_liste(bu,[1001,1007],6) 
            dzbir =  suma_liste(bu,[1002,1006],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1007) kol. 6 = AOP-u (1002 + 1006) kol.6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10018
        if( aop(bu,1008,5) > aop(bu,1009,5) ):
            if not( aop(bu,1010,5) == aop(bu,1008,5)-aop(bu,1009,5) ):
                lzbir =  aop(bu,1010,5) 
                dzbir =  aop(bu,1008,5)-aop(bu,1009,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1010 kol. 5 = AOP-u (1008 - 1009) kol. 5, ako je AOP 1008 kol. 5 > AOP-a 1009 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10019
        if( aop(bu,1008,6) > aop(bu,1009,6) ):
            if not( aop(bu,1010,6) == aop(bu,1008,6)-aop(bu,1009,6) ):
                lzbir =  aop(bu,1010,6) 
                dzbir =  aop(bu,1008,6)-aop(bu,1009,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1010 kol. 6 = AOP-u (1008 - 1009) kol. 6, ako je AOP 1008 kol. 6 > AOP-a 1009 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10020
        if( aop(bu,1008,5) < aop(bu,1009,5) ):
            if not( aop(bu,1011,5) == aop(bu,1009,5)-aop(bu,1008,5) ):
                lzbir =  aop(bu,1011,5) 
                dzbir =  aop(bu,1009,5)-aop(bu,1008,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1011 kol. 5 = AOP-u (1009 - 1008) kol. 5, ako je AOP 1008 kol. 5 < AOP-a 1009 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10021
        if( aop(bu,1008,6) < aop(bu,1009,6) ):
            if not( aop(bu,1011,6) == aop(bu,1009,6)-aop(bu,1008,6) ):
                lzbir =  aop(bu,1011,6) 
                dzbir =  aop(bu,1009,6)-aop(bu,1008,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1011 kol. 6 = AOP-u (1009 - 1008) kol. 6, ako je AOP 1008 kol. 6 < AOP-a 1009 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10022
        if( aop(bu,1008,5) == aop(bu,1009,5) ):
            if not( suma(bu,1010,1011,5) == 0 ):
                lzbir =  suma(bu,1010,1011,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  =' AOP (1010 + 1011) kol. 5 = 0, ako je AOP 1008 kol. 5 = AOP-u 1009 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10023
        if( aop(bu,1008,6) == aop(bu,1009,6) ):
            if not( suma(bu,1010,1011,6) == 0 ):
                lzbir =  suma(bu,1010,1011,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  =' AOP (1010 + 1011) kol. 6 = 0, ako je AOP 1008 kol. 6 = AOP-u 1009 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10024
        if( aop(bu,1010,5) > 0 ):
            if not( aop(bu,1011,5) == 0 ):
                lzbir =  aop(bu,1011,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1010 kol. 5 > 0 onda je AOP 1011 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10025
        if( aop(bu,1011,5) > 0 ):
            if not( aop(bu,1010,5) == 0 ):
                lzbir =  aop(bu,1010,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1011 kol. 5 > 0 onda je AOP 1010 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10026
        if( aop(bu,1010,6) > 0 ):
            if not( aop(bu,1011,6) == 0 ):
                lzbir =  aop(bu,1011,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1010 kol. 6 > 0 onda je AOP 1011 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10027
        if( aop(bu,1011,6) > 0 ):
            if not( aop(bu,1010,6) == 0 ):
                lzbir =  aop(bu,1010,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1011 kol. 6 > 0 onda je AOP 1010 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10028
        if not( suma_liste(bu,[1008,1011],5) == suma(bu,1009,1010,5) ):
            lzbir =  suma_liste(bu,[1008,1011],5) 
            dzbir =  suma(bu,1009,1010,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1008 + 1011) kol. 5 = AOP-u (1009 + 1010) kol.5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10029
        if not( suma_liste(bu,[1008,1011],6) == suma(bu,1009,1010,6) ):
            lzbir =  suma_liste(bu,[1008,1011],6) 
            dzbir =  suma(bu,1009,1010,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1008 + 1011) kol. 6 = AOP-u (1009 + 1010) kol.6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10030
        if( aop(bu,1012,5) > aop(bu,1013,5) ):
            if not( aop(bu,1014,5) == aop(bu,1012,5)-aop(bu,1013,5) ):
                lzbir =  aop(bu,1014,5) 
                dzbir =  aop(bu,1012,5)-aop(bu,1013,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1014 kol. 5 = AOP-u (1012 - 1013) kol. 5, ako je AOP 1012 kol. 5 > AOP-a 1013 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10031
        if( aop(bu,1012,6) > aop(bu,1013,6) ):
            if not( aop(bu,1014,6) == aop(bu,1012,6)-aop(bu,1013,6) ):
                lzbir =  aop(bu,1014,6) 
                dzbir =  aop(bu,1012,6)-aop(bu,1013,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1014 kol. 6 = AOP-u (1012 - 1013) kol. 6, ako je AOP 1012 kol. 6 > AOP-a 1013 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10032
        if( aop(bu,1012,5) < aop(bu,1013,5) ):
            if not( aop(bu,1015,5) == aop(bu,1013,5)-aop(bu,1012,5) ):
                lzbir =  aop(bu,1015,5) 
                dzbir =  aop(bu,1013,5)-aop(bu,1012,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1015 kol. 5 = AOP-u (1013 - 1012) kol. 5, ako je AOP 1012 kol. 5 < AOP-a 1013 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10033
        if( aop(bu,1012,6) < aop(bu,1013,6) ):
            if not( aop(bu,1015,6) == aop(bu,1013,6)-aop(bu,1012,6) ):
                lzbir =  aop(bu,1015,6) 
                dzbir =  aop(bu,1013,6)-aop(bu,1012,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1015 kol. 6 = AOP-u (1013 - 1012) kol. 6, ako je AOP 1012 kol. 6 < AOP-a 1013 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10034
        if( aop(bu,1012,5) == aop(bu,1013,5) ):
            if not( suma(bu,1014,1015,5) == 0 ):
                lzbir =  suma(bu,1014,1015,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  =' AOP (1014 + 1015) kol. 5 = 0, ako je AOP 1012 kol. 5 = AOP-u 1013 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10035
        if( aop(bu,1012,6) == aop(bu,1013,6) ):
            if not( suma(bu,1014,1015,6) == 0 ):
                lzbir =  suma(bu,1014,1015,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  =' AOP (1014 + 1015) kol. 6 = 0, ako je AOP 1012 kol. 6 = AOP-u 1013 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10036
        if( aop(bu,1014,5) > 0 ):
            if not( aop(bu,1015,5) == 0 ):
                lzbir =  aop(bu,1015,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1014 kol. 5 > 0 onda je AOP 1015 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10037
        if( aop(bu,1015,5) > 0 ):
            if not( aop(bu,1014,5) == 0 ):
                lzbir =  aop(bu,1014,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1015 kol. 5 > 0 onda je AOP 1014 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10038
        if( aop(bu,1014,6) > 0 ):
            if not( aop(bu,1015,6) == 0 ):
                lzbir =  aop(bu,1015,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1014 kol. 6 > 0 onda je AOP 1015 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10039
        if( aop(bu,1015,6) > 0 ):
            if not( aop(bu,1014,6) == 0 ):
                lzbir =  aop(bu,1014,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1015 kol. 6 > 0 onda je AOP 1014 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10040
        if not( suma_liste(bu,[1012,1015],5) == suma(bu,1013,1014,5) ):
            lzbir =  suma_liste(bu,[1012,1015],5) 
            dzbir =  suma(bu,1013,1014,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1012 + 1015) kol. 5 = AOP-u (1013 + 1014) kol.5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10041
        if not( suma_liste(bu,[1012,1015],6) == suma(bu,1013,1014,6) ):
            lzbir =  suma_liste(bu,[1012,1015],6) 
            dzbir =  suma(bu,1013,1014,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1012 + 1015) kol. 6 = AOP-u (1013 + 1014) kol.6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10042
        if not( aop(bu,1016,5) == suma_liste(bu,[1006,1010,1014],5) ):
            lzbir =  aop(bu,1016,5) 
            dzbir =  suma_liste(bu,[1006,1010,1014],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1016 kol. 5 = AOP-u (1006 + 1010 + 1014) kol.5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10043
        if not( aop(bu,1016,6) == suma_liste(bu,[1006,1010,1014],6) ):
            lzbir =  aop(bu,1016,6) 
            dzbir =  suma_liste(bu,[1006,1010,1014],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1016 kol. 6 = AOP-u (1006 + 1010 + 1014) kol.6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10044
        if not( aop(bu,1017,5) == suma_liste(bu,[1007,1011,1015],5) ):
            lzbir =  aop(bu,1017,5) 
            dzbir =  suma_liste(bu,[1007,1011,1015],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1017 kol. 5 = AOP-u (1007 + 1011 + 1015) kol.5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10045
        if not( aop(bu,1017,6) == suma_liste(bu,[1007,1011,1015],6) ):
            lzbir =  aop(bu,1017,6) 
            dzbir =  suma_liste(bu,[1007,1011,1015],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1017 kol. 6 = AOP-u (1007 + 1011 + 1015) kol.6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10046
        if( suma_liste(bu,[1016,1018,1020,1022,1024],5) > suma_liste(bu,[1017,1019,1021,1023,1025],5) ):
            if not( aop(bu,1026,5) == suma_liste(bu,[1016,1018,1020,1022,1024],5)-suma_liste(bu,[1017,1019,1021,1023,1025],5) ):
                lzbir =  aop(bu,1026,5) 
                dzbir =  suma_liste(bu,[1016,1018,1020,1022,1024],5)-suma_liste(bu,[1017,1019,1021,1023,1025],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1026 kol. 5 = AOP-u (1016 - 1017 + 1018 - 1019 + 1020 - 1021 + 1022 - 1023 + 1024 - 1025) kol. 5, ako je AOP (1016 + 1018 + 1020 + 1022 + 1024) kol. 5 > AOP-a (1017 + 1019 + 1021 + 1023 + 1025) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10047
        if( suma_liste(bu,[1016,1018,1020,1022,1024],6) > suma_liste(bu,[1017,1019,1021,1023,1025],6) ):
            if not( aop(bu,1026,6) == suma_liste(bu,[1016,1018,1020,1022,1024],6)-suma_liste(bu,[1017,1019,1021,1023,1025],6) ):
                lzbir =  aop(bu,1026,6) 
                dzbir =  suma_liste(bu,[1016,1018,1020,1022,1024],6)-suma_liste(bu,[1017,1019,1021,1023,1025],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1026 kol. 6 = AOP-u (1016 - 1017 + 1018 - 1019 + 1020 - 1021 + 1022 - 1023 + 1024 - 1025) kol. 6, ako je AOP (1016 + 1018 + 1020 + 1022 + 1024) kol. 6 > AOP-a (1017 + 1019 + 1021 + 1023 + 1025) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10048
        if( suma_liste(bu,[1016,1018,1020,1022,1024],5) < suma_liste(bu,[1017,1019,1021,1023,1025],5) ):
            if not( aop(bu,1027,5) == suma_liste(bu,[1017,1019,1021,1023,1025],5)-suma_liste(bu,[1016,1018,1020,1022,1024],5) ):
                lzbir =  aop(bu,1027,5) 
                dzbir =  suma_liste(bu,[1017,1019,1021,1023,1025],5)-suma_liste(bu,[1016,1018,1020,1022,1024],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1027 kol. 5 = AOP-u (1017 - 1016 + 1019 - 1018 + 1021 - 1020 + 1023 - 1022 + 1025 - 1024) kol. 5, ako je AOP (1016 + 1018 + 1020 + 1022 + 1024) kol. 5 < AOP-a (1017 + 1019 + 1021 + 1023 + 1025) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10049
        if( suma_liste(bu,[1016,1018,1020,1022,1024],6) < suma_liste(bu,[1017,1019,1021,1023,1025],6) ):
            if not( aop(bu,1027,6) == suma_liste(bu,[1017,1019,1021,1023,1025],6)-suma_liste(bu,[1016,1018,1020,1022,1024],6) ):
                lzbir =  aop(bu,1027,6) 
                dzbir =  suma_liste(bu,[1017,1019,1021,1023,1025],6)-suma_liste(bu,[1016,1018,1020,1022,1024],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1027 kol. 6 = AOP-u (1017 - 1016 + 1019 - 1018 + 1021 - 1020 + 1023 - 1022 + 1025 - 1024) kol. 6, ako je AOP (1016 + 1018 + 1020 + 1022 + 1024) kol. 6 < AOP-a (1017 + 1019 + 1021 + 1023 + 1025) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10050
        if( suma_liste(bu,[1016,1018,1020,1022,1024],5) == suma_liste(bu,[1017,1019,1021,1023,1025],5) ):
            if not( suma(bu,1026,1027,5) == 0 ):
                lzbir =  suma(bu,1026,1027,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1026 + 1027) kol. 5 = 0, ako je AOP (1016 + 1018 + 1020 + 1022 + 1024) kol. 5 = AOP-u (1017 + 1019 + 1021 + 1023 + 1025) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10051
        if( suma_liste(bu,[1016,1018,1020,1022,1024],6) == suma_liste(bu,[1017,1019,1021,1023,1025],6) ):
            if not( suma(bu,1026,1027,6) == 0 ):
                lzbir =  suma(bu,1026,1027,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1026 + 1027) kol. 6 = 0, ako je AOP (1016 + 1018 + 1020 + 1022 + 1024) kol. 6 = AOP-u (1017 + 1019 + 1021 + 1023 + 1025) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10052
        if( aop(bu,1026,5) > 0 ):
            if not( aop(bu,1027,5) == 0 ):
                lzbir =  aop(bu,1027,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1026 kol. 5 > 0 onda je AOP 1027 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10053
        if( aop(bu,1027,5) > 0 ):
            if not( aop(bu,1026,5) == 0 ):
                lzbir =  aop(bu,1026,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1027 kol. 5 > 0 onda je AOP 1026 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10054
        if( aop(bu,1026,6) > 0 ):
            if not( aop(bu,1027,6) == 0 ):
                lzbir =  aop(bu,1027,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1026 kol. 6 > 0 onda je AOP 1027 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10055
        if( aop(bu,1027,6) > 0 ):
            if not( aop(bu,1026,6) == 0 ):
                lzbir =  aop(bu,1026,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1027 kol. 6 > 0 onda je AOP 1026 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10056
        if not( suma_liste(bu,[1016,1018,1020,1022,1024,1027],5) == suma_liste(bu,[1017,1019,1021,1023,1025,1026],5) ):
            lzbir =  suma_liste(bu,[1016,1018,1020,1022,1024,1027],5) 
            dzbir =  suma_liste(bu,[1017,1019,1021,1023,1025,1026],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1016 + 1018 + 1020 + 1022 + 1024 + 1027) kol. 5 = AOP-u (1017 + 1019 + 1021 + 1023 + 1025 + 1026) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10057
        if not( suma_liste(bu,[1016,1018,1020,1022,1024,1027],6) == suma_liste(bu,[1017,1019,1021,1023,1025,1026],6) ):
            lzbir =  suma_liste(bu,[1016,1018,1020,1022,1024,1027],6) 
            dzbir =  suma_liste(bu,[1017,1019,1021,1023,1025,1026],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1016 + 1018 + 1020 + 1022 + 1024 + 1027) kol. 6 = AOP-u (1017 + 1019 + 1021 + 1023 + 1025 + 1026) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10058
        if not( suma_liste(bu,[1001,1008,1012,1018,1020,1022,1024,1027],5) == suma_liste(bu,[1002,1009,1013,1019,1021,1023,1025,1026],5) ):
            lzbir =  suma_liste(bu,[1001,1008,1012,1018,1020,1022,1024,1027],5) 
            dzbir =  suma_liste(bu,[1002,1009,1013,1019,1021,1023,1025,1026],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1008 + 1012 + 1018 + 1020 + 1022 + 1024 + 1027) kol. 5 = AOP-u (1002 + 1009 + 1013+ 1019 + 1021 + 1023 + 1025 + 1026) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10059
        if not( suma_liste(bu,[1001,1008,1012,1018,1020,1022,1024,1027],6) == suma_liste(bu,[1002,1009,1013,1019,1021,1023,1025,1026],6) ):
            lzbir =  suma_liste(bu,[1001,1008,1012,1018,1020,1022,1024,1027],6) 
            dzbir =  suma_liste(bu,[1002,1009,1013,1019,1021,1023,1025,1026],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1008 + 1012 + 1018 + 1020 + 1022 + 1024 + 1027) kol. 6 = AOP-u (1002 + 1009 + 1013+ 1019 + 1021 + 1023 + 1025 + 1026) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10060
        #Za ovaj set se ne primenjuje pravilo 
        
        #10061
        if( suma_liste(bu,[1026,1030],5) > suma(bu,1027,1029,5) ):
            if not( aop(bu,1031,5) == suma_liste(bu,[1026,1030],5)-suma(bu,1027,1029,5) ):
                lzbir =  aop(bu,1031,5) 
                dzbir =  suma_liste(bu,[1026,1030],5)-suma(bu,1027,1029,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1031 kol. 5 = AOP-u (1026 - 1027 - 1028 - 1029 + 1030) kol. 5, ako je AOP (1026 + 1030) kol. 5 > AOP-a (1027 + 1028 + 1029) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10062
        if( suma_liste(bu,[1026,1030],6) > suma(bu,1027,1029,6) ):
            if not( aop(bu,1031,6) == suma_liste(bu,[1026,1030],6)-suma(bu,1027,1029,6) ):
                lzbir =  aop(bu,1031,6) 
                dzbir =  suma_liste(bu,[1026,1030],6)-suma(bu,1027,1029,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1031 kol. 6 = AOP-u (1026 - 1027 - 1028 - 1029 + 1030) kol. 6, ako je AOP (1026 + 1030) kol. 6 > AOP-a (1027 + 1028 + 1029) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10063
        if( suma_liste(bu,[1026,1030],5) < suma(bu,1027,1029,5) ):
            if not( aop(bu,1032,5) == suma(bu,1027,1029,5)-suma_liste(bu,[1026,1030],5) ):
                lzbir =  aop(bu,1032,5) 
                dzbir =  suma(bu,1027,1029,5)-suma_liste(bu,[1026,1030],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1032 kol. 5 = AOP-u (1027 - 1026 + 1028 + 1029 - 1030) kol. 5, ako je AOP (1026 + 1030) kol. 5 < AOP-a (1027 + 1028 + 1029) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10064
        if( suma_liste(bu,[1026,1030],6) < suma(bu,1027,1029,6) ):
            if not( aop(bu,1032,6) == suma(bu,1027,1029,6)-suma_liste(bu,[1026,1030],6) ):
                lzbir =  aop(bu,1032,6) 
                dzbir =  suma(bu,1027,1029,6)-suma_liste(bu,[1026,1030],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1032 kol. 6 = AOP-u (1027 - 1026 + 1028 + 1029 - 1030) kol. 6, ako je AOP (1026 + 1030) kol. 6 < AOP-a (1027 + 1028 + 1029) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10065
        if( suma_liste(bu,[1026,1030],5) == suma(bu,1027,1029,5) ):
            if not( suma(bu,1031,1032,5) == 0 ):
                lzbir =  suma(bu,1031,1032,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1031 + 1032) kol. 5 = 0, ako je AOP (1026 + 1030) kol. 5 = AOP-u (1027 + 1028 + 1029) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10066
        if( suma_liste(bu,[1026,1030],6) == suma(bu,1027,1029,6) ):
            if not( suma(bu,1031,1032,6) == 0 ):
                lzbir =  suma(bu,1031,1032,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1031 + 1032) kol. 6 = 0, ako je AOP (1026 + 1030) kol. 6 = AOP-u (1027 + 1028 + 1029) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10067
        if( aop(bu,1031,5) > 0 ):
            if not( aop(bu,1032,5) == 0 ):
                lzbir =  aop(bu,1032,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1031 kol. 5 > 0 onda je AOP 1032 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10068
        if( aop(bu,1032,5) > 0 ):
            if not( aop(bu,1031,5) == 0 ):
                lzbir =  aop(bu,1031,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1032 kol. 5 > 0 onda je AOP 1031 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10069
        if( aop(bu,1031,6) > 0 ):
            if not( aop(bu,1032,6) == 0 ):
                lzbir =  aop(bu,1032,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1031 kol. 6 > 0 onda je AOP 1032 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10070
        if( aop(bu,1032,6) > 0 ):
            if not( aop(bu,1031,6) == 0 ):
                lzbir =  aop(bu,1031,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1032 kol. 6 > 0 onda je AOP 1031 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10071
        if not( suma_liste(bu,[1026,1030,1032],5) == suma_liste(bu,[1027,1028,1029,1031],5) ):
            lzbir =  suma_liste(bu,[1026,1030,1032],5) 
            dzbir =  suma_liste(bu,[1027,1028,1029,1031],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1026 + 1030 + 1032) kol. 5 = AOP-u (1027 + 1028 + 1029 + 1031) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10072
        if not( suma_liste(bu,[1026,1030,1032],6) == suma_liste(bu,[1027,1028,1029,1031],6) ):
            lzbir =  suma_liste(bu,[1026,1030,1032],6) 
            dzbir =  suma_liste(bu,[1027,1028,1029,1031],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1026 + 1030 + 1032) kol. 6 = AOP-u (1027 + 1028 + 1029 + 1031) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10073
        if( aop(bu,1031,5) >= 0 ):
            if not( aop(bu,1031,5) == suma(bu,1033,1034,5)-suma(bu,1035,1036,5) ):
                lzbir =  aop(bu,1031,5) 
                dzbir =  suma(bu,1033,1034,5)-suma(bu,1035,1036,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1031 kol. 5 ≥ 0, onda je AOP 1031 kol. 5 = AOP-u (1033  + 1034 - 1035 - 1036) kol. 5   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10074
        if( aop(bu,1031,6) >= 0 ):
            if not( aop(bu,1031,6) == suma(bu,1033,1034,6)-suma(bu,1035,1036,6) ):
                lzbir =  aop(bu,1031,6) 
                dzbir =  suma(bu,1033,1034,6)-suma(bu,1035,1036,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1031 kol. 6 ≥ 0, onda je AOP 1031 kol. 6 = AOP-u (1033  + 1034 - 1035 - 1036) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10075
        if( aop(bu,1032,5) > 0 ):
            if not( aop(bu,1032,5) == suma(bu,1035,1036,5)-suma(bu,1033,1034,5) ):
                lzbir =  aop(bu,1032,5) 
                dzbir =  suma(bu,1035,1036,5)-suma(bu,1033,1034,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1032 kol. 5 > 0, onda je AOP 1032 kol. 5 = AOP-u (1035  + 1036 - 1033 - 1034) kol. 5   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10076
        if( aop(bu,1032,6) > 0 ):
            if not( aop(bu,1032,6) == suma(bu,1035,1036,6)-suma(bu,1033,1034,6) ):
                lzbir =  aop(bu,1032,6) 
                dzbir =  suma(bu,1035,1036,6)-suma(bu,1033,1034,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1032 kol. 6 > 0, onda je AOP 1032 kol. 6 = AOP-u (1035  + 1036 - 1033 - 1034) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10077
        #Za ovaj set se ne primenjuje pravilo 
        
        #10078
        #Za ovaj set se ne primenjuje pravilo 
        
        #10079
        #Za ovaj set se ne primenjuje pravilo 
        
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
        #Za ovaj set se ne primenjuje pravilo 
        
        #10089
        #Za ovaj set se ne primenjuje pravilo 
        
        #10090
        #Za ovaj set se ne primenjuje pravilo 
        
        #10091
        #Za ovaj set se ne primenjuje pravilo 
        
        #10092
        #Za ovaj set se ne primenjuje pravilo 
        
        #10093
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if( suma(bu,1001,1038,5) > 0 ):
                if not( suma(bu,1001,1038,5) != suma(bu,1001,1038,6) ):
                    
                    naziv_obrasca='Bilans uspeha'
                    poruka  ='***Ako je zbir podataka na oznakama za AOP (1001 do 1038) kol. 5 > 0 onda zbir podataka na oznakama za AOP (1001 do 1038) kol. 5 ≠ zbiru podataka na oznakama za AOP  (1001 do 1038) kol. 6 Zbirovi podataka u kolonama 5 i 6 bilansa uspeha su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama;  '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
        
        
        #IZVEŠTAJ O OSTALOM REZULTATU - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #20001
        if not( suma(ioor,2001,2026,5) > 0 ):
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='Zbir podataka na oznakama za AOP (2001 do 2026) kol. 5 > 0 Izveštaj o ostalom rezultatu, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #20002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(ioor,2001,2026,6) == 0 ):
                lzbir =  suma(ioor,2001,2026,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Zbir podataka na oznakama za AOP (2001 do 2026) kol. 6 = 0 Izveštaj o ostalom rezultatu za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(ioor,2001,2026,6) > 0 ):
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Zbir podataka na oznakama za AOP (2001 do 2026) kol. 6 > 0 Izveštaj o ostalom rezultatu, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #20004
        if not( aop(ioor,2001,5) == aop(bu,1031,5) ):
            lzbir =  aop(ioor,2001,5) 
            dzbir =  aop(bu,1031,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 2001 kol. 5 = AOP-u 1031 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2001 kol. 5 = AOP-u 1031 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20005
        if not( aop(ioor,2001,6) == aop(bu,1031,6) ):
            lzbir =  aop(ioor,2001,6) 
            dzbir =  aop(bu,1031,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 2001 kol. 6 = AOP-u 1031 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2001 kol. 6 = AOP-u 1031 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20006
        if not( aop(ioor,2002,5) == aop(bu,1032,5) ):
            lzbir =  aop(ioor,2002,5) 
            dzbir =  aop(bu,1032,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 2002 kol. 5 = AOP-u 1032 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2002 kol. 5 = AOP-u 1032 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20007
        if not( aop(ioor,2002,6) == aop(bu,1032,6) ):
            lzbir =  aop(ioor,2002,6) 
            dzbir =  aop(bu,1032,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 2002 kol. 6 = AOP-u 1032 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2002 kol. 6 = AOP-u 1032 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20008
        if( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],5) > suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],5) ):
            if not( aop(ioor,2019,5) == suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],5)-suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],5) ):
                lzbir =  aop(ioor,2019,5) 
                dzbir =  suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],5)-suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2019 kol. 5 = AOP-u (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017 - 2004 - 2006 - 2008 - 2010 - 2012 - 2014 - 2016 - 2018) kol. 5, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017) kol. 5 > AOP-a (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20009
        if( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],6) > suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],6) ):
            if not( aop(ioor,2019,6) == suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],6)-suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],6) ):
                lzbir =  aop(ioor,2019,6) 
                dzbir =  suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],6)-suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2019 kol. 6 = AOP-u (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017 - 2004 - 2006 - 2008 - 2010 - 2012 - 2014 - 2016 - 2018) kol. 6, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017) kol. 6 > AOP-a (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20010
        if( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],5) < suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],5) ):
            if not( aop(ioor,2020,5) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],5)-suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],5) ):
                lzbir =  aop(ioor,2020,5) 
                dzbir =  suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],5)-suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2020 kol. 5 = AOP-u (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018 - 2003 - 2005 - 2007 - 2009 - 2011 - 2013 - 2015 - 2017) kol. 5, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017) kol. 5 < AOP-a (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20011
        if( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],6) < suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],6) ):
            if not( aop(ioor,2020,6) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],6)-suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],6) ):
                lzbir =  aop(ioor,2020,6) 
                dzbir =  suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],6)-suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2020 kol. 6 = AOP-u (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018 - 2003 - 2005 - 2007 - 2009 - 2011 - 2013 - 2015 - 2017) kol. 6, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017) kol. 6 < AOP-a (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20012
        if( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],5) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],5) ):
            if not( suma(ioor,2019,2020,5) == 0 ):
                lzbir =  suma(ioor,2019,2020,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP (2019 + 2020) kol. 5 = 0, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017)  kol. 5 = AOP-u (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20013
        if( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017],6) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018],6) ):
            if not( suma(ioor,2019,2020,6) == 0 ):
                lzbir =  suma(ioor,2019,2020,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP (2019 + 2020) kol. 6 = 0, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017)  kol. 6 = AOP-u (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20014
        if( aop(ioor,2019,5) > 0 ):
            if not( aop(ioor,2020,5) == 0 ):
                lzbir =  aop(ioor,2020,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2019 kol. 5 > 0, onda je AOP 2020 kol. 5 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20015
        if( aop(ioor,2020,5) > 0 ):
            if not( aop(ioor,2019,5) == 0 ):
                lzbir =  aop(ioor,2019,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je  AOP 2020 kol. 5 > 0, onda je AOP 2019 kol. 5 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20016
        if( aop(ioor,2019,6) > 0 ):
            if not( aop(ioor,2020,6) == 0 ):
                lzbir =  aop(ioor,2020,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2019 kol. 6 > 0, onda je AOP 2020 kol. 6 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20017
        if( aop(ioor,2020,6) > 0 ):
            if not( aop(ioor,2019,6) == 0 ):
                lzbir =  aop(ioor,2019,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je  AOP 2020 kol. 6 > 0, onda je AOP 2019 kol. 6 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20018
        if not( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2020],5) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2019],5) ):
            lzbir =  suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2020],5) 
            dzbir =  suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2019],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017 + 2020) kol. 5 = AOP-u (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018 + 2019) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20019
        if not( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2020],6) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2019],6) ):
            lzbir =  suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2017,2020],6) 
            dzbir =  suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2018,2019],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017 + 2020) kol. 6 = AOP-u (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018 + 2019) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20020
        if( suma_liste(ioor,[2001,2019],5) > suma_liste(ioor,[2002,2020],5) ):
            if not( aop(ioor,2021,5) == suma_liste(ioor,[2001,2019],5)-suma_liste(ioor,[2002,2020],5) ):
                lzbir =  aop(ioor,2021,5) 
                dzbir =  suma_liste(ioor,[2001,2019],5)-suma_liste(ioor,[2002,2020],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2021 kol. 5 = AOP-u (2001 - 2002 + 2019 - 2020) kol. 5, ako je AOP (2001 + 2019) kol. 5 > AOP-a (2002 + 2020) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20021
        if( suma_liste(ioor,[2001,2019],6) > suma_liste(ioor,[2002,2020],6) ):
            if not( aop(ioor,2021,6) == suma_liste(ioor,[2001,2019],6)-suma_liste(ioor,[2002,2020],6) ):
                lzbir =  aop(ioor,2021,6) 
                dzbir =  suma_liste(ioor,[2001,2019],6)-suma_liste(ioor,[2002,2020],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2021 kol. 6 = AOP-u (2001 - 2002 + 2019 - 2020) kol. 6, ako je AOP (2001 + 2019) kol. 6 > AOP-a (2002 + 2020) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20022
        if not( aop(ioor,2021,5) == suma(ioor,2022,2023,5) ):
            lzbir =  aop(ioor,2021,5) 
            dzbir =  suma(ioor,2022,2023,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2021 kol. 5 = AOP-u (2022+ 2023) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20023
        if not( aop(ioor,2021,6) == suma(ioor,2022,2023,6) ):
            lzbir =  aop(ioor,2021,6) 
            dzbir =  suma(ioor,2022,2023,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2021 kol. 6 = AOP-u (2022+ 2023) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20024
        if( suma_liste(ioor,[2001,2019],5) < suma_liste(ioor,[2002,2020],5) ):
            if not( aop(ioor,2024,5) == suma_liste(ioor,[2002,2020],5)-suma_liste(ioor,[2001,2019],5) ):
                lzbir =  aop(ioor,2024,5) 
                dzbir =  suma_liste(ioor,[2002,2020],5)-suma_liste(ioor,[2001,2019],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2024 kol. 5 = AOP-u (2002 - 2001 + 2020 - 2019) kol. 5, ako je AOP (2001 + 2019) kol. 5 < AOP-a (2002 + 2020) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20025
        if( suma_liste(ioor,[2001,2019],6) < suma_liste(ioor,[2002,2020],6) ):
            if not( aop(ioor,2024,6) == suma_liste(ioor,[2002,2020],6)-suma_liste(ioor,[2001,2019],6) ):
                lzbir =  aop(ioor,2024,6) 
                dzbir =  suma_liste(ioor,[2002,2020],6)-suma_liste(ioor,[2001,2019],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2024 kol. 6 = AOP-u (2002 - 2001 + 2020 - 2019) kol. 6, ako je AOP (2001 + 2019) kol. 6 < AOP-a (2002 + 2020) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20026
        if not( aop(ioor,2024,5) == suma(ioor,2025,2026,5) ):
            lzbir =  aop(ioor,2024,5) 
            dzbir =  suma(ioor,2025,2026,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2024 kol. 5 = AOP-u (2025+ 2026) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20027
        if not( aop(ioor,2024,6) == suma(ioor,2025,2026,6) ):
            lzbir =  aop(ioor,2024,6) 
            dzbir =  suma(ioor,2025,2026,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2024 kol. 6 = AOP-u (2025+ 2026) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20028
        if( suma_liste(ioor,[2001,2019],5) == suma_liste(ioor,[2002,2020],5) ):
            if not( suma_liste(ioor,[2021,2024],5) == 0 ):
                lzbir =  suma_liste(ioor,[2021,2024],5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP (2021 + 2024) kol. 5 = 0, ako je AOP (2001 + 2019) kol. 5 = AOP-u (2002 + 2020) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20029
        if( suma_liste(ioor,[2001,2019],6) == suma_liste(ioor,[2002,2020],6) ):
            if not( suma_liste(ioor,[2021,2024],6) == 0 ):
                lzbir =  suma_liste(ioor,[2021,2024],6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP (2021 + 2024) kol. 6 = 0, ako je AOP (2001 + 2019) kol. 6 = AOP-u (2002 + 2020) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20030
        if( aop(ioor,2021,5) > 0 ):
            if not( aop(ioor,2024,5) == 0 ):
                lzbir =  aop(ioor,2024,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2021 kol. 5 > 0, onda je AOP 2024 kol. 5 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20031
        if( aop(ioor,2024,5) > 0 ):
            if not( aop(ioor,2021,5) == 0 ):
                lzbir =  aop(ioor,2021,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2024 kol. 5 > 0, onda je AOP 2021 kol. 5 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20032
        if( aop(ioor,2021,6) > 0 ):
            if not( aop(ioor,2024,6) == 0 ):
                lzbir =  aop(ioor,2024,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2021 kol. 6 > 0, onda je AOP 2024 kol. 6 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20033
        if( aop(ioor,2024,6) > 0 ):
            if not( aop(ioor,2021,6) == 0 ):
                lzbir =  aop(ioor,2021,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2024 kol. 6 > 0, onda je AOP 2021 kol. 6 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20034
        if not( suma_liste(ioor,[2001,2019,2024],5) == suma_liste(ioor,[2002,2020,2021],5) ):
            lzbir =  suma_liste(ioor,[2001,2019,2024],5) 
            dzbir =  suma_liste(ioor,[2002,2020,2021],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP (2001 + 2019 + 2024) kol. 5 = AOP-u (2002 + 2020 + 2021) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20035
        if not( suma_liste(ioor,[2001,2019,2024],6) == suma_liste(ioor,[2002,2020,2021],6) ):
            lzbir =  suma_liste(ioor,[2001,2019,2024],6) 
            dzbir =  suma_liste(ioor,[2002,2020,2021],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP (2001 + 2019 + 2024) kol. 6 = AOP-u (2002 + 2020 + 2021) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20036
        #Za ovaj set se ne primenjuje pravilo 
        
        #20037
        #Za ovaj set se ne primenjuje pravilo 
        
        #IZVEŠTAJ O TOKOVIMA GOTOVINE - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #30001
        if not( suma(iotg,3001,3049,3) > 0 ):
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='Zbir podataka na oznakama za AOP (3001 do 3049) kol. 3 > 0 Izveštaj o tokovima gotovine, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #30002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(iotg,3001,3049,4) == 0 ):
                lzbir =  suma(iotg,3001,3049,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Zbir podataka na oznakama za AOP (3001 do 3049) kol. 4 = 0 Izveštaj o tokovima gotovine za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(iotg,3001,3049,4) > 0 ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Zbir podataka na oznakama za AOP (3001 do 3049) kol. 4 > 0 Izveštaj o tokovima gotovine, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #30004
        if not( aop(iotg,3001,3) == suma(iotg,3002,3010,3) ):
            lzbir =  aop(iotg,3001,3) 
            dzbir =  suma(iotg,3002,3010,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3001 kol. 3 = AOP-u (3002 + 3003 + 3004 + 3005 + 3006 + 3007 + 3008 + 3009 + 3010) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30005
        if not( aop(iotg,3001,4) == suma(iotg,3002,3010,4) ):
            lzbir =  aop(iotg,3001,4) 
            dzbir =  suma(iotg,3002,3010,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3001 kol. 4 = AOP-u (3002 + 3003 + 3004 + 3005 + 3006 + 3007 + 3008 + 3009 + 3010) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30006
        if not( aop(iotg,3011,3) == suma(iotg,3012,3015,3) ):
            lzbir =  aop(iotg,3011,3) 
            dzbir =  suma(iotg,3012,3015,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3011 kol. 3 = AOP-u (3012 + 3013 + 3014 + 3015) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30007
        if not( aop(iotg,3011,4) == suma(iotg,3012,3015,4) ):
            lzbir =  aop(iotg,3011,4) 
            dzbir =  suma(iotg,3012,3015,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3011 kol. 4 = AOP-u (3012 + 3013 + 3014 + 3015) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30008
        if( aop(iotg,3001,3) > aop(iotg,3011,3) ):
            if not( aop(iotg,3016,3) == aop(iotg,3001,3)-aop(iotg,3011,3) ):
                lzbir =  aop(iotg,3016,3) 
                dzbir =  aop(iotg,3001,3)-aop(iotg,3011,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3016 kol. 3 = AOP-u (3001 - 3011) kol. 3, ako je AOP 3001 kol. 3 > AOP-a 3011 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30009
        if( aop(iotg,3001,4) > aop(iotg,3011,4) ):
            if not( aop(iotg,3016,4) == aop(iotg,3001,4)-aop(iotg,3011,4) ):
                lzbir =  aop(iotg,3016,4) 
                dzbir =  aop(iotg,3001,4)-aop(iotg,3011,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3016 kol. 4 = AOP-u (3001 - 3011) kol. 4, ako je AOP 3001 kol. 4 > AOP-a 3011 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30010
        if( aop(iotg,3001,3) < aop(iotg,3011,3) ):
            if not( aop(iotg,3017,3) == aop(iotg,3011,3)-aop(iotg,3001,3) ):
                lzbir =  aop(iotg,3017,3) 
                dzbir =  aop(iotg,3011,3)-aop(iotg,3001,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3017 kol. 3 = AOP-u (3011 - 3001) kol. 3, ako je AOP 3001 kol. 3 < AOP-a 3011 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30011
        if( aop(iotg,3001,4) < aop(iotg,3011,4) ):
            if not( aop(iotg,3017,4) == aop(iotg,3011,4)-aop(iotg,3001,4) ):
                lzbir =  aop(iotg,3017,4) 
                dzbir =  aop(iotg,3011,4)-aop(iotg,3001,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3017 kol. 4 = AOP-u (3011 - 3001) kol. 4, ako je AOP 3001 kol. 4 < AOP-a 3011 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30012
        if( aop(iotg,3001,3) == aop(iotg,3011,3) ):
            if not( suma(iotg,3016,3017,3) == 0 ):
                lzbir =  suma(iotg,3016,3017,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3016 + 3017) kol. 3 = 0, ako je AOP 3001 kol. 3 = AOP-u 3011 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30013
        if( aop(iotg,3001,4) == aop(iotg,3011,4) ):
            if not( suma(iotg,3016,3017,4) == 0 ):
                lzbir =  suma(iotg,3016,3017,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3016 + 3017) kol. 4 = 0, ako je AOP 3001 kol. 4 = AOP-u 3011 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30014
        if( aop(iotg,3016,3) > 0 ):
            if not( aop(iotg,3017,3) == 0 ):
                lzbir =  aop(iotg,3017,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3016 kol. 3 > 0 onda je AOP 3017 kol. 3 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30015
        if( aop(iotg,3017,3) > 0 ):
            if not( aop(iotg,3016,3) == 0 ):
                lzbir =  aop(iotg,3016,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3017 kol. 3 > 0 onda je AOP 3016 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30016
        if( aop(iotg,3016,4) > 0 ):
            if not( aop(iotg,3017,4) == 0 ):
                lzbir =  aop(iotg,3017,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3016 kol. 4 > 0 onda je AOP 3017 kol. 4 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30017
        if( aop(iotg,3017,4) > 0 ):
            if not( aop(iotg,3016,4) == 0 ):
                lzbir =  aop(iotg,3016,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3017 kol. 4 > 0 onda je AOP 3016 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30018
        if not( suma_liste(iotg,[3001,3017],3) == suma_liste(iotg,[3011,3016],3) ):
            lzbir =  suma_liste(iotg,[3001,3017],3) 
            dzbir =  suma_liste(iotg,[3011,3016],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3001 + 3017) kol. 3 = AOP-u (3011 + 3016) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30019
        if not( suma_liste(iotg,[3001,3017],4) == suma_liste(iotg,[3011,3016],4) ):
            lzbir =  suma_liste(iotg,[3001,3017],4) 
            dzbir =  suma_liste(iotg,[3011,3016],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3001 + 3017) kol. 4 = AOP-u (3011 + 3016) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30020
        if not( aop(iotg,3018,3) == suma(iotg,3019,3022,3) ):
            lzbir =  aop(iotg,3018,3) 
            dzbir =  suma(iotg,3019,3022,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3018 kol. 3 = AOP-u (3019 + 3020 + 3021 + 3022) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30021
        if not( aop(iotg,3018,4) == suma(iotg,3019,3022,4) ):
            lzbir =  aop(iotg,3018,4) 
            dzbir =  suma(iotg,3019,3022,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3018 kol. 4 = AOP-u (3019 + 3020 + 3021 + 3022) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30022
        if not( aop(iotg,3023,3) == suma(iotg,3024,3026,3) ):
            lzbir =  aop(iotg,3023,3) 
            dzbir =  suma(iotg,3024,3026,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3023 kol. 3 = AOP-u (3024 + 3025 + 3026) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30023
        if not( aop(iotg,3023,4) == suma(iotg,3024,3026,4) ):
            lzbir =  aop(iotg,3023,4) 
            dzbir =  suma(iotg,3024,3026,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3023 kol. 4 = AOP-u (3024 + 3025 + 3026) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30024
        if( aop(iotg,3018,3) > aop(iotg,3023,3) ):
            if not( aop(iotg,3027,3) == aop(iotg,3018,3)-aop(iotg,3023,3) ):
                lzbir =  aop(iotg,3027,3) 
                dzbir =  aop(iotg,3018,3)-aop(iotg,3023,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3027 kol. 3 = AOP-u (3018 - 3023) kol. 3, ako je AOP 3018 kol. 3 > AOP-a 3023 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30025
        if( aop(iotg,3018,4) > aop(iotg,3023,4) ):
            if not( aop(iotg,3027,4) == aop(iotg,3018,4)-aop(iotg,3023,4) ):
                lzbir =  aop(iotg,3027,4) 
                dzbir =  aop(iotg,3018,4)-aop(iotg,3023,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3027 kol. 4 = AOP-u (3018 - 3023) kol. 4, ako je AOP 3018 kol. 4 > AOP-a 3023 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30026
        if( aop(iotg,3018,3) < aop(iotg,3023,3) ):
            if not( aop(iotg,3028,3) == aop(iotg,3023,3)-aop(iotg,3018,3) ):
                lzbir =  aop(iotg,3028,3) 
                dzbir =  aop(iotg,3023,3)-aop(iotg,3018,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3028 kol. 3 = AOP-u (3023 - 3018) kol. 3, ako je AOP 3018 kol. 3 < AOP-a 3023 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30027
        if( aop(iotg,3018,4) < aop(iotg,3023,4) ):
            if not( aop(iotg,3028,4) == aop(iotg,3023,4)-aop(iotg,3018,4) ):
                lzbir =  aop(iotg,3028,4) 
                dzbir =  aop(iotg,3023,4)-aop(iotg,3018,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3028 kol. 4 = AOP-u (3023 - 3018) kol. 4, ako je AOP 3018 kol. 4 < AOP-a 3023 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30028
        if( aop(iotg,3018,3) == aop(iotg,3023,3) ):
            if not( suma(iotg,3027,3028,3) == 0 ):
                lzbir =  suma(iotg,3027,3028,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3027 + 3028) kol. 3 = 0, ako je AOP 3018 kol. 3 = AOP-u 3023 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30029
        if( aop(iotg,3018,4) == aop(iotg,3023,4) ):
            if not( suma(iotg,3027,3028,4) == 0 ):
                lzbir =  suma(iotg,3027,3028,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3027 + 3028) kol. 4 = 0, ako je AOP 3018 kol. 4 = AOP-u 3023 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30030
        if( aop(iotg,3027,3) > 0 ):
            if not( aop(iotg,3028,3) == 0 ):
                lzbir =  aop(iotg,3028,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3027 kol. 3 > 0 onda je AOP 3028 kol. 3 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30031
        if( aop(iotg,3028,3) > 0 ):
            if not( aop(iotg,3027,3) == 0 ):
                lzbir =  aop(iotg,3027,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3028 kol. 3 > 0 onda je AOP 3027 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30032
        if( aop(iotg,3027,4) > 0 ):
            if not( aop(iotg,3028,4) == 0 ):
                lzbir =  aop(iotg,3028,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3027 kol. 4 > 0 onda je AOP 3028 kol. 4 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30033
        if( aop(iotg,3028,4) > 0 ):
            if not( aop(iotg,3027,4) == 0 ):
                lzbir =  aop(iotg,3027,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3028 kol. 4 > 0 onda je AOP 3027 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30034
        if not( suma_liste(iotg,[3018,3028],3) == suma_liste(iotg,[3023,3027],3) ):
            lzbir =  suma_liste(iotg,[3018,3028],3) 
            dzbir =  suma_liste(iotg,[3023,3027],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3018 + 3028) kol. 3 = AOP-u (3023 + 3027) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30035
        if not( suma_liste(iotg,[3018,3028],4) == suma_liste(iotg,[3023,3027],4) ):
            lzbir =  suma_liste(iotg,[3018,3028],4) 
            dzbir =  suma_liste(iotg,[3023,3027],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3018 + 3028) kol. 4 = AOP-u (3023 + 3027) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30036
        if not( aop(iotg,3029,3) == suma(iotg,3030,3034,3) ):
            lzbir =  aop(iotg,3029,3) 
            dzbir =  suma(iotg,3030,3034,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3029 kol. 3 = AOP-u (3030 + 3031 + 3032 + 3033 + 3034) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30037
        if not( aop(iotg,3029,4) == suma(iotg,3030,3034,4) ):
            lzbir =  aop(iotg,3029,4) 
            dzbir =  suma(iotg,3030,3034,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3029 kol. 4 = AOP-u (3030 + 3031 + 3032 + 3033 + 3034) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30038
        if not( aop(iotg,3035,3) == suma(iotg,3036,3041,3) ):
            lzbir =  aop(iotg,3035,3) 
            dzbir =  suma(iotg,3036,3041,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3035 kol. 3 = AOP-u (3036 + 3037 + 3038 + 3039 + 3040 + 3041) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30039
        if not( aop(iotg,3035,4) == suma(iotg,3036,3041,4) ):
            lzbir =  aop(iotg,3035,4) 
            dzbir =  suma(iotg,3036,3041,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3035 kol. 4 = AOP-u (3036 + 3037 + 3038 + 3039 + 3040 + 3041) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30040
        if( aop(iotg,3029,3) > aop(iotg,3035,3) ):
            if not( aop(iotg,3042,3) == aop(iotg,3029,3)-aop(iotg,3035,3) ):
                lzbir =  aop(iotg,3042,3) 
                dzbir =  aop(iotg,3029,3)-aop(iotg,3035,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3042 kol. 3 = AOP-u (3029 - 3035) kol. 3, ako je AOP 3029 kol. 3 > AOP-a 3035 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30041
        if( aop(iotg,3029,4) > aop(iotg,3035,4) ):
            if not( aop(iotg,3042,4) == aop(iotg,3029,4)-aop(iotg,3035,4) ):
                lzbir =  aop(iotg,3042,4) 
                dzbir =  aop(iotg,3029,4)-aop(iotg,3035,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3042 kol. 4 = AOP-u (3029 - 3035) kol. 4, ako je AOP 3029 kol. 4 > AOP-a 3035 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30042
        if( aop(iotg,3029,3) < aop(iotg,3035,3) ):
            if not( aop(iotg,3043,3) == aop(iotg,3035,3)-aop(iotg,3029,3) ):
                lzbir =  aop(iotg,3043,3) 
                dzbir =  aop(iotg,3035,3)-aop(iotg,3029,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3043 kol. 3 = AOP-u (3035 - 3029) kol. 3, ako je AOP 3029 kol. 3 < AOP-a 3035 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30043
        if( aop(iotg,3029,4) < aop(iotg,3035,4) ):
            if not( aop(iotg,3043,4) == aop(iotg,3035,4)-aop(iotg,3029,4) ):
                lzbir =  aop(iotg,3043,4) 
                dzbir =  aop(iotg,3035,4)-aop(iotg,3029,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3043 kol. 4 = AOP-u (3035 - 3029) kol. 4, ako je AOP 3029 kol. 4 < AOP-a 3035 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30044
        if( aop(iotg,3029,3) == aop(iotg,3035,3) ):
            if not( suma(iotg,3042,3043,3) == 0 ):
                lzbir =  suma(iotg,3042,3043,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3042 + 3043) kol. 3 = 0, ako je AOP 3029 kol. 3 = AOP-u 3035 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30045
        if( aop(iotg,3029,4) == aop(iotg,3035,4) ):
            if not( suma(iotg,3042,3043,4) == 0 ):
                lzbir =  suma(iotg,3042,3043,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3042 + 3043) kol. 4 = 0, ako je AOP 3029 kol. 4 = AOP-u 3035 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30046
        if( aop(iotg,3042,3) > 0 ):
            if not( aop(iotg,3043,3) == 0 ):
                lzbir =  aop(iotg,3043,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3042 kol. 3 > 0 onda je AOP 3043 kol. 3 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30047
        if( aop(iotg,3043,3) > 0 ):
            if not( aop(iotg,3042,3) == 0 ):
                lzbir =  aop(iotg,3042,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3043 kol. 3 > 0 onda je AOP 3042 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30048
        if( aop(iotg,3042,4) > 0 ):
            if not( aop(iotg,3043,4) == 0 ):
                lzbir =  aop(iotg,3043,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3042 kol. 4 > 0 onda je AOP 3043 kol. 4 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30049
        if( aop(iotg,3043,4) > 0 ):
            if not( aop(iotg,3042,4) == 0 ):
                lzbir =  aop(iotg,3042,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3043 kol. 4 > 0 onda je AOP 3042 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30050
        if not( suma_liste(iotg,[3029,3043],3) == suma_liste(iotg,[3035,3042],3) ):
            lzbir =  suma_liste(iotg,[3029,3043],3) 
            dzbir =  suma_liste(iotg,[3035,3042],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3029 + 3043) kol. 3 = AOP-u (3035 + 3042) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30051
        if not( suma_liste(iotg,[3029,3043],4) == suma_liste(iotg,[3035,3042],4) ):
            lzbir =  suma_liste(iotg,[3029,3043],4) 
            dzbir =  suma_liste(iotg,[3035,3042],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3029 + 3043) kol. 4 = AOP-u (3035 + 3042) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30052
        if( suma_liste(iotg,[3016,3027,3042],3) > suma_liste(iotg,[3017,3028,3043],3) ):
            if not( aop(iotg,3044,3) == suma_liste(iotg,[3016,3027,3042],3)-suma_liste(iotg,[3017,3028,3043],3) ):
                lzbir =  aop(iotg,3044,3) 
                dzbir =  suma_liste(iotg,[3016,3027,3042],3)-suma_liste(iotg,[3017,3028,3043],3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3044 kol. 3 = AOP-u (3016 + 3027 + 3042 - 3017 - 3028 - 3043) kol. 3, ako je AOP (3016 + 3027 + 3042) kol. 3 > AOP-a (3017 + 3028 + 3043) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30053
        if( suma_liste(iotg,[3016,3027,3042],4) > suma_liste(iotg,[3017,3028,3043],4) ):
            if not( aop(iotg,3044,4) == suma_liste(iotg,[3016,3027,3042],4)-suma_liste(iotg,[3017,3028,3043],4) ):
                lzbir =  aop(iotg,3044,4) 
                dzbir =  suma_liste(iotg,[3016,3027,3042],4)-suma_liste(iotg,[3017,3028,3043],4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3044 kol. 4 = AOP-u (3016 + 3027 + 3042 - 3017 - 3028 - 3043) kol. 4, ako je AOP (3016 + 3027 + 3042) kol. 4 > AOP-a (3017 + 3028 + 3043) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30054
        if( suma_liste(iotg,[3016,3027,3042],3) < suma_liste(iotg,[3017,3028,3043],3) ):
            if not( aop(iotg,3045,3) == suma_liste(iotg,[3017,3028,3043],3)-suma_liste(iotg,[3016,3027,3042],3) ):
                lzbir =  aop(iotg,3045,3) 
                dzbir =  suma_liste(iotg,[3017,3028,3043],3)-suma_liste(iotg,[3016,3027,3042],3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3045 kol. 3 = AOP-u (3017 + 3028 + 3043 - 3016 - 3027 - 3042) kol. 3, ako je AOP (3016 + 3027 + 3042) kol. 3 < AOP-a (3017 + 3028 + 3043) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30055
        if( suma_liste(iotg,[3016,3027,3042],4) < suma_liste(iotg,[3017,3028,3043],4) ):
            if not( aop(iotg,3045,4) == suma_liste(iotg,[3017,3028,3043],4)-suma_liste(iotg,[3016,3027,3042],4) ):
                lzbir =  aop(iotg,3045,4) 
                dzbir =  suma_liste(iotg,[3017,3028,3043],4)-suma_liste(iotg,[3016,3027,3042],4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3045 kol. 4 = AOP-u (3017 + 3028 + 3043 - 3016 - 3027 - 3042) kol. 4, ako je AOP (3016 + 3027 + 3042) kol. 4 < AOP-a (3017 + 3028 + 3043) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30056
        if( suma_liste(iotg,[3016,3027,3042],3) == suma_liste(iotg,[3017,3028,3043],3) ):
            if not( suma(iotg,3044,3045,3) == 0 ):
                lzbir =  suma(iotg,3044,3045,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3044 + 3045) kol. 3 = 0,  ako je AOP (3016 + 3027 + 3042) kol. 3 = AOP-u (3017 + 3028 + 3043) kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30057
        if( suma_liste(iotg,[3016,3027,3042],4) == suma_liste(iotg,[3017,3028,3043],4) ):
            if not( suma(iotg,3044,3045,4) == 0 ):
                lzbir =  suma(iotg,3044,3045,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3044 + 3045) kol. 4 = 0,  ako je AOP (3016 + 3027 + 3042) kol. 4 = AOP-u (3017 + 3028 + 3043) kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30058
        if( aop(iotg,3044,3) > 0 ):
            if not( aop(iotg,3045,3) == 0 ):
                lzbir =  aop(iotg,3045,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3044 kol. 3 > 0 onda je AOP 3045 kol. 3 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30059
        if( aop(iotg,3045,3) > 0 ):
            if not( aop(iotg,3044,3) == 0 ):
                lzbir =  aop(iotg,3044,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3045 kol. 3 > 0 onda je AOP 3044 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30060
        if( aop(iotg,3044,4) > 0 ):
            if not( aop(iotg,3045,4) == 0 ):
                lzbir =  aop(iotg,3045,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3044 kol. 4 > 0 onda je AOP 3045 kol. 4 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30061
        if( aop(iotg,3045,4) > 0 ):
            if not( aop(iotg,3044,4) == 0 ):
                lzbir =  aop(iotg,3044,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3045 kol. 4 > 0 onda je AOP 3044 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30062
        if not( suma_liste(iotg,[3016,3027,3042,3045],3) == suma_liste(iotg,[3017,3028,3043,3044],3) ):
            lzbir =  suma_liste(iotg,[3016,3027,3042,3045],3) 
            dzbir =  suma_liste(iotg,[3017,3028,3043,3044],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3016 + 3027 + 3042 + 3045) kol. 3 = AOP-u (3017 + 3028 + 3043 + 3044) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30063
        if not( suma_liste(iotg,[3016,3027,3042,3045],4) == suma_liste(iotg,[3017,3028,3043,3044],4) ):
            lzbir =  suma_liste(iotg,[3016,3027,3042,3045],4) 
            dzbir =  suma_liste(iotg,[3017,3028,3043,3044],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3016 + 3027 + 3042 + 3045) kol. 4 = AOP-u (3017 + 3028 + 3043 + 3044) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30064
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( aop(iotg,3046,3) == 0 ):
                lzbir =  aop(iotg,3046,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3046 kol. 3 = 0 Novoosnovana pravna lica ne smeju imati prikazan podatak za prethodnu godinu '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30065
        if( suma_liste(iotg,[3044,3046,3047],3) > suma_liste(iotg,[3045,3048],3) ):
            if not( aop(iotg,3049,3) == suma_liste(iotg,[3044,3046,3047],3)-suma_liste(iotg,[3045,3048],3) ):
                lzbir =  aop(iotg,3049,3) 
                dzbir =  suma_liste(iotg,[3044,3046,3047],3)-suma_liste(iotg,[3045,3048],3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3049 kol. 3 = AOP-u (3044 - 3045 + 3046 + 3047 - 3048) kol. 3, ako je AOP (3044 + 3046 + 3047) kol. 3 > AOP-a (3045 + 3048) kol. 3   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30066
        if( suma_liste(iotg,[3044,3046,3047],4) > suma_liste(iotg,[3045,3048],4) ):
            if not( aop(iotg,3049,4) == suma_liste(iotg,[3044,3046,3047],4)-suma_liste(iotg,[3045,3048],4) ):
                lzbir =  aop(iotg,3049,4) 
                dzbir =  suma_liste(iotg,[3044,3046,3047],4)-suma_liste(iotg,[3045,3048],4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3049 kol. 4 = AOP-u (3044 - 3045 + 3046 + 3047 - 3048) kol. 4, ako je AOP (3044 + 3046 + 3047) kol. 4 > AOP-a (3045 + 3048) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30067
        if( suma_liste(iotg,[3044,3046,3047],3) <= suma_liste(iotg,[3045,3048],3) ):
            if not( aop(iotg,3049,3) == 0 ):
                lzbir =  aop(iotg,3049,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3049 kol. 3 = 0, ako je AOP (3044 + 3046 + 3047) kol. 3 ≤ AOP-a (3045 + 3048) kol. 3   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30068
        if( suma_liste(iotg,[3044,3046,3047],4) <= suma_liste(iotg,[3045,3048],4) ):
            if not( aop(iotg,3049,4) == 0 ):
                lzbir =  aop(iotg,3049,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3049 kol. 4 = 0, ako je AOP (3044 + 3046 + 3047) kol. 4 ≤ AOP-a (3045 + 3048) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30069
        if not( aop(iotg,3049,4) == aop(iotg,3046,3) ):
            lzbir =  aop(iotg,3049,4) 
            dzbir =  aop(iotg,3046,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3049 kol. 4 = AOP-u 3046 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30070
        if not( aop(iotg,3049,3) == aop(bs,22,5) ):
            lzbir =  aop(iotg,3049,3) 
            dzbir =  aop(bs,22,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 3049 kol. 3 = AOP-u 0022 kol. 5 bilansa stanja Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3049 kol. 3 = AOP-u 0022 kol. 5 bilansa stanja Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #30071
        if not( aop(iotg,3049,4) == aop(bs,22,6) ):
            lzbir =  aop(iotg,3049,4) 
            dzbir =  aop(bs,22,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 3049 kol. 4 = AOP-u 0022 kol. 6 bilansa stanja Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3049 kol. 4 = AOP-u 0022 kol. 6 bilansa stanja Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #IZVEŠTAJ O PROMENAMA NA KAPITALU - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #40001
        if not( suma(iopk,4019, 4022, 1) +suma(iopk,4041, 4044, 1) +suma(iopk,4063, 4066, 1) +suma(iopk,4085, 4088, 1) +suma(iopk,4107, 4110, 1) +suma(iopk,4129, 4132, 1) +suma(iopk,4151, 4154, 1) +suma(iopk,4173, 4176, 1) +suma(iopk,4195, 4198, 1) +suma(iopk,4217, 4220, 1) +suma(iopk,4239, 4242, 1) +suma(iopk,4261, 4264, 1)  > 0 ):
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='Zbir podataka na oznakama za AOP (4019 do 4022) + (4041 do 4044) + (4063 do 4066) + (4085 do 4088) + (4107 do 4110) + (4129 do 4132) + (4151 do 4154) + (4173 do 4176) + (4195 do 4198) + (4217 do 4220) + (4239 do 4242) + (4261 do 4264) > 0 Izveštaj o promenama na kapitalu, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(iopk,4001, 4018, 1) +suma(iopk,4023, 4040, 1) +suma(iopk,4045, 4062, 1) +suma(iopk,4067, 4084, 1) +suma(iopk,4089, 4106, 1) +suma(iopk,4111, 4128, 1) +suma(iopk,4133, 4150, 1) +suma(iopk,4155, 4172, 1) +suma(iopk,4177, 4194, 1) +suma(iopk,4199, 4216, 1) +suma(iopk,4221, 4238, 1) +suma(iopk,4243, 4260, 1)  == 0 ):
                lzbir =  suma(iopk,4001, 4018, 1) +suma(iopk,4023, 4040, 1) +suma(iopk,4045, 4062, 1) +suma(iopk,4067, 4084, 1) +suma(iopk,4089, 4106, 1) +suma(iopk,4111, 4128, 1) +suma(iopk,4133, 4150, 1) +suma(iopk,4155, 4172, 1) +suma(iopk,4177, 4194, 1) +suma(iopk,4199, 4216, 1) +suma(iopk,4221, 4238, 1) +suma(iopk,4243, 4260, 1)  
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Zbir podataka na oznakama za AOP (4001 do 4018) + (4023 do 4040) + (4045 do 4062) + (4067 do 4084) + (4089 do 4106) + (4111 do 4128) + (4133 do 4150) + (4155 do 4172) + (4177 do 4194) + (4199 do 4216) + (4221 do 4238) + (4243 do 4260) = 0 Izveštaj o promenama na kapitalu za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(iopk,4001, 4018, 1) +suma(iopk,4023, 4040, 1) +suma(iopk,4045, 4062, 1) +suma(iopk,4067, 4084, 1) +suma(iopk,4089, 4106, 1) +suma(iopk,4111, 4128, 1) +suma(iopk,4133, 4150, 1) +suma(iopk,4155, 4172, 1) +suma(iopk,4177, 4194, 1) +suma(iopk,4199, 4216, 1) +suma(iopk,4221, 4238, 1) +suma(iopk,4243, 4260, 1)  > 0 ):
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Zbir podataka na oznakama za AOP (4001 do 4018) + (4023 do 4040) + (4045 do 4062) + (4067 do 4084) + (4089 do 4106) + (4111 do 4128) + (4133 do 4150) + (4155 do 4172) + (4177 do 4194) + (4199 do 4216) + (4221 do 4238) + (4243 do 4260) > 0 Izveštaj o promenama na kapitalu, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #40004
        if not( aop(iopk,4001,1) == 0 ):
            lzbir =  aop(iopk,4001,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4001 = 0 Osnovni kapital ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40005
        if not( aop(iopk,4007,1) == 0 ):
            lzbir =  aop(iopk,4007,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4007 = 0 Osnovni kapital ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40006
        if not( aop(iopk,4008,1) == suma_liste(iopk,[4002,4004,4006],1)-suma_liste(iopk,[4003,4005],1) ):
            lzbir =  aop(iopk,4008,1) 
            dzbir =  suma_liste(iopk,[4002,4004,4006],1)-suma_liste(iopk,[4003,4005],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4008 = AOP-u (4002 - 4003 + 4004 - 4005 + 4006)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40007
        if not( aop(iopk,4011,1) == 0 ):
            lzbir =  aop(iopk,4011,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4011 = 0 Osnovni kapital ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40008
        if not( aop(iopk,4012,1) == suma_liste(iopk,[4008,4010],1)-aop(iopk,4009,1) ):
            lzbir =  aop(iopk,4012,1) 
            dzbir =  suma_liste(iopk,[4008,4010],1)-aop(iopk,4009,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4012 = AOP-u (4008 - 4009 + 4010)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40009
        if not( aop(iopk,4017,1) == 0 ):
            lzbir =  aop(iopk,4017,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4017 = 0 Osnovni kapital ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40010
        if not( aop(iopk,4018,1) == suma_liste(iopk,[4012,4014,4016],1)-suma_liste(iopk,[4013,4015],1) ):
            lzbir =  aop(iopk,4018,1) 
            dzbir =  suma_liste(iopk,[4012,4014,4016],1)-suma_liste(iopk,[4013,4015],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4018 = AOP-u (4012 - 4013 + 4014 - 4015 + 4016)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40011
        if not( aop(iopk,4021,1) == 0 ):
            lzbir =  aop(iopk,4021,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4021 = 0 Osnovni kapital ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40012
        if not( aop(iopk,4022,1) == suma_liste(iopk,[4018,4020],1)-aop(iopk,4019,1) ):
            lzbir =  aop(iopk,4022,1) 
            dzbir =  suma_liste(iopk,[4018,4020],1)-aop(iopk,4019,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4022 = AOP-u (4018 - 4019 + 4020)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40013
        if not( aop(iopk,4024,1) == 0 ):
            lzbir =  aop(iopk,4024,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4024 = 0 Upisani a neuplaćeni kapital ne može imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40014
        if not( aop(iopk,4029,1) == suma_liste(iopk,[4023,4025,4027],1)-suma_liste(iopk,[4026,4028],1) ):
            lzbir =  aop(iopk,4029,1) 
            dzbir =  suma_liste(iopk,[4023,4025,4027],1)-suma_liste(iopk,[4026,4028],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4029 = AOP-u (4023 + 4025 - 4026 + 4027 - 4028)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40015
        if not( aop(iopk,4030,1) == 0 ):
            lzbir =  aop(iopk,4030,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4030 = 0 Upisani a neuplaćeni kapital ne može imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40016
        if not( aop(iopk,4033,1) == suma_liste(iopk,[4029,4031],1)-aop(iopk,4032,1) ):
            lzbir =  aop(iopk,4033,1) 
            dzbir =  suma_liste(iopk,[4029,4031],1)-aop(iopk,4032,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4033 = AOP-u (4029 + 4031 - 4032)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40017
        if not( aop(iopk,4034,1) == 0 ):
            lzbir =  aop(iopk,4034,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4034 = 0 Upisani a neuplaćeni kapital ne može imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40018
        if not( aop(iopk,4039,1) == suma_liste(iopk,[4033,4035,4037],1)-suma_liste(iopk,[4036,4038],1) ):
            lzbir =  aop(iopk,4039,1) 
            dzbir =  suma_liste(iopk,[4033,4035,4037],1)-suma_liste(iopk,[4036,4038],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4039 = AOP-u (4033 + 4035 - 4036 + 4037 - 4038)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40019
        if not( aop(iopk,4040,1) == 0 ):
            lzbir =  aop(iopk,4040,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4040 = 0 Upisani a neuplaćeni kapital ne može imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40020
        if not( aop(iopk,4043,1) == suma_liste(iopk,[4039,4041],1)-aop(iopk,4042,1) ):
            lzbir =  aop(iopk,4043,1) 
            dzbir =  suma_liste(iopk,[4039,4041],1)-aop(iopk,4042,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4043 = AOP-u (4039 + 4041 - 4042)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40021
        if not( aop(iopk,4044,1) == 0 ):
            lzbir =  aop(iopk,4044,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4044 = 0 Upisani a neuplaćeni kapital ne može imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40022
        if not( aop(iopk,4045,1) == 0 ):
            lzbir =  aop(iopk,4045,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4045 = 0 Rezerve ne mogu imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40023
        if not( aop(iopk,4051,1) == 0 ):
            lzbir =  aop(iopk,4051,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4051 = 0 Rezerve ne mogu imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40024
        if not( aop(iopk,4052,1) == suma_liste(iopk,[4046,4048,4050],1)-suma_liste(iopk,[4047,4049],1) ):
            lzbir =  aop(iopk,4052,1) 
            dzbir =  suma_liste(iopk,[4046,4048,4050],1)-suma_liste(iopk,[4047,4049],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4052 = AOP-u (4046 - 4047 + 4048 - 4049 + 4050)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40025
        if not( aop(iopk,4055,1) == 0 ):
            lzbir =  aop(iopk,4055,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4055 = 0 Rezerve ne mogu imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40026
        if not( aop(iopk,4056,1) == suma_liste(iopk,[4052,4054],1)-aop(iopk,4053,1) ):
            lzbir =  aop(iopk,4056,1) 
            dzbir =  suma_liste(iopk,[4052,4054],1)-aop(iopk,4053,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4056 = AOP-u (4052 - 4053 + 4054)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40027
        if not( aop(iopk,4061,1) == 0 ):
            lzbir =  aop(iopk,4061,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4061 = 0 Rezerve ne mogu imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40028
        if not( aop(iopk,4062,1) == suma_liste(iopk,[4056,4058,4060],1)-suma_liste(iopk,[4057,4059],1) ):
            lzbir =  aop(iopk,4062,1) 
            dzbir =  suma_liste(iopk,[4056,4058,4060],1)-suma_liste(iopk,[4057,4059],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4062 = AOP-u (4056 - 4057 + 4058 - 4059 + 4060)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40029
        if not( aop(iopk,4065,1) == 0 ):
            lzbir =  aop(iopk,4065,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4065 = 0 Rezerve ne mogu imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40030
        if not( aop(iopk,4066,1) == suma_liste(iopk,[4062,4064],1)-aop(iopk,4063,1) ):
            lzbir =  aop(iopk,4066,1) 
            dzbir =  suma_liste(iopk,[4062,4064],1)-aop(iopk,4063,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4066 = AOP-u (4062 - 4063 + 4064)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40031
        if not( aop(iopk,4068,1) == 0 ):
            lzbir =  aop(iopk,4068,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4068 = 0 Gubitak ne može imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40032
        if not( aop(iopk,4073,1) == suma_liste(iopk,[4067,4069,4071],1)-suma_liste(iopk,[4070,4072],1) ):
            lzbir =  aop(iopk,4073,1) 
            dzbir =  suma_liste(iopk,[4067,4069,4071],1)-suma_liste(iopk,[4070,4072],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4073 = AOP-u (4067 + 4069 - 4070 + 4071 - 4072)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40033
        if not( aop(iopk,4074,1) == 0 ):
            lzbir =  aop(iopk,4074,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4074 = 0 Gubitak ne može imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40034
        if not( aop(iopk,4077,1) == suma_liste(iopk,[4073,4075],1)-aop(iopk,4076,1) ):
            lzbir =  aop(iopk,4077,1) 
            dzbir =  suma_liste(iopk,[4073,4075],1)-aop(iopk,4076,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4077 = AOP-u (4073 + 4075 - 4076)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40035
        if not( aop(iopk,4078,1) == 0 ):
            lzbir =  aop(iopk,4078,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4078 = 0 Gubitak ne može imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40036
        if not( aop(iopk,4083,1) == suma_liste(iopk,[4077,4079,4081],1)-suma_liste(iopk,[4080,4082],1) ):
            lzbir =  aop(iopk,4083,1) 
            dzbir =  suma_liste(iopk,[4077,4079,4081],1)-suma_liste(iopk,[4080,4082],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4083 = AOP-u (4077 + 4079 - 4080 + 4081 - 4082)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40037
        if not( aop(iopk,4084,1) == 0 ):
            lzbir =  aop(iopk,4084,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4084 = 0 Gubitak ne može imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40038
        if not( aop(iopk,4087,1) == suma_liste(iopk,[4083,4085],1)-aop(iopk,4086,1) ):
            lzbir =  aop(iopk,4087,1) 
            dzbir =  suma_liste(iopk,[4083,4085],1)-aop(iopk,4086,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4087 = AOP-u (4083 + 4085 - 4086)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40039
        if not( aop(iopk,4088,1) == 0 ):
            lzbir =  aop(iopk,4088,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4088 = 0 Gubitak ne može imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40040
        if not( aop(iopk,4090,1) == 0 ):
            lzbir =  aop(iopk,4090,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4090 = 0 Otkupljene sopstvene akcije ne mogu imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40041
        if not( aop(iopk,4095,1) == suma_liste(iopk,[4089,4091,4093],1)-suma_liste(iopk,[4092,4094],1) ):
            lzbir =  aop(iopk,4095,1) 
            dzbir =  suma_liste(iopk,[4089,4091,4093],1)-suma_liste(iopk,[4092,4094],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4095 = AOP-u (4089 + 4091 - 4092 + 4093 - 4094)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40042
        if not( aop(iopk,4096,1) == 0 ):
            lzbir =  aop(iopk,4096,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4096 = 0 Otkupljene sopstvene akcije ne mogu imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40043
        if not( aop(iopk,4099,1) == suma_liste(iopk,[4095,4097],1)-aop(iopk,4098,1) ):
            lzbir =  aop(iopk,4099,1) 
            dzbir =  suma_liste(iopk,[4095,4097],1)-aop(iopk,4098,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4099 = AOP-u (4095 + 4097 - 4098)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40044
        if not( aop(iopk,4100,1) == 0 ):
            lzbir =  aop(iopk,4100,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4100 = 0 Otkupljene sopstvene akcije ne mogu imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40045
        if not( aop(iopk,4105,1) == suma_liste(iopk,[4099,4101,4103],1)-suma_liste(iopk,[4102,4104],1) ):
            lzbir =  aop(iopk,4105,1) 
            dzbir =  suma_liste(iopk,[4099,4101,4103],1)-suma_liste(iopk,[4102,4104],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4105 = AOP-u (4099 + 4101 - 4102 + 4103 - 4104)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40046
        if not( aop(iopk,4106,1) == 0 ):
            lzbir =  aop(iopk,4106,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4106 = 0 Otkupljene sopstvene akcije ne mogu imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40047
        if not( aop(iopk,4109,1) == suma_liste(iopk,[4105,4107],1)-aop(iopk,4108,1) ):
            lzbir =  aop(iopk,4109,1) 
            dzbir =  suma_liste(iopk,[4105,4107],1)-aop(iopk,4108,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4109 = AOP-u (4105 + 4107 - 4108)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40048
        if not( aop(iopk,4110,1) == 0 ):
            lzbir =  aop(iopk,4110,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4110 = 0 Otkupljene sopstvene akcije ne mogu imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40049
        if not( aop(iopk,4111,1) == 0 ):
            lzbir =  aop(iopk,4111,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4111 = 0 Neraspoređeni dobitak ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40050
        if not( aop(iopk,4117,1) == 0 ):
            lzbir =  aop(iopk,4117,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4117 = 0 Neraspoređeni dobitak ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40051
        if not( aop(iopk,4118,1) == suma_liste(iopk,[4112,4114,4116],1)-suma_liste(iopk,[4113,4115],1) ):
            lzbir =  aop(iopk,4118,1) 
            dzbir =  suma_liste(iopk,[4112,4114,4116],1)-suma_liste(iopk,[4113,4115],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4118 = AOP-u (4112 - 4113 + 4114 - 4115 + 4116)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40052
        if not( aop(iopk,4121,1) == 0 ):
            lzbir =  aop(iopk,4121,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4121 = 0 Neraspoređeni dobitak ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40053
        if not( aop(iopk,4122,1) == suma_liste(iopk,[4118,4120],1)-aop(iopk,4119,1) ):
            lzbir =  aop(iopk,4122,1) 
            dzbir =  suma_liste(iopk,[4118,4120],1)-aop(iopk,4119,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4122 = AOP-u (4118 - 4119 + 4120)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40054
        if not( aop(iopk,4127,1) == 0 ):
            lzbir =  aop(iopk,4127,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4127 = 0 Neraspoređeni dobitak ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40055
        if not( aop(iopk,4128,1) == suma_liste(iopk,[4122,4124,4126],1)-suma_liste(iopk,[4123,4125],1) ):
            lzbir =  aop(iopk,4128,1) 
            dzbir =  suma_liste(iopk,[4122,4124,4126],1)-suma_liste(iopk,[4123,4125],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4128 = AOP-u (4122 - 4123 + 4124 - 4125 + 4126)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40056
        if not( aop(iopk,4131,1) == 0 ):
            lzbir =  aop(iopk,4131,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4131 = 0 Neraspoređeni dobitak ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40057
        if not( aop(iopk,4132,1) == suma_liste(iopk,[4128,4130],1)-aop(iopk,4129,1) ):
            lzbir =  aop(iopk,4132,1) 
            dzbir =  suma_liste(iopk,[4128,4130],1)-aop(iopk,4129,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4132 = AOP-u (4128 - 4129 + 4130)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40058
        if not( aop(iopk,4133,1) == 0 ):
            lzbir =  aop(iopk,4133,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4133 = 0 Revalorizacione rezerve ne mogu imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40059
        if not( aop(iopk,4139,1) == 0 ):
            lzbir =  aop(iopk,4139,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4139 = 0 Revalorizacione rezerve ne mogu imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40060
        if not( aop(iopk,4140,1) == suma_liste(iopk,[4134,4136,4138],1)-suma_liste(iopk,[4135,4137],1) ):
            lzbir =  aop(iopk,4140,1) 
            dzbir =  suma_liste(iopk,[4134,4136,4138],1)-suma_liste(iopk,[4135,4137],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4140 = AOP-u (4134 - 4135 + 4136 - 4137 + 4138)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40061
        if not( aop(iopk,4143,1) == 0 ):
            lzbir =  aop(iopk,4143,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4143 = 0 Revalorizacione rezerve ne mogu imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40062
        if not( aop(iopk,4144,1) == suma_liste(iopk,[4140,4142],1)-aop(iopk,4141,1) ):
            lzbir =  aop(iopk,4144,1) 
            dzbir =  suma_liste(iopk,[4140,4142],1)-aop(iopk,4141,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4144 = AOP-u (4140 - 4141 + 4142)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40063
        if not( aop(iopk,4149,1) == 0 ):
            lzbir =  aop(iopk,4149,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4149 = 0 Revalorizacione rezerve ne mogu imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40064
        if not( aop(iopk,4150,1) == suma_liste(iopk,[4144,4146,4148],1)-suma_liste(iopk,[4145,4147],1) ):
            lzbir =  aop(iopk,4150,1) 
            dzbir =  suma_liste(iopk,[4144,4146,4148],1)-suma_liste(iopk,[4145,4147],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4150 = AOP-u (4144 - 4145 + 4146 - 4147 + 4148)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40065
        if not( aop(iopk,4153,1) == 0 ):
            lzbir =  aop(iopk,4153,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4153 = 0 Revalorizacione rezerve ne mogu imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40066
        if not( aop(iopk,4154,1) == suma_liste(iopk,[4150,4152],1)-aop(iopk,4151,1) ):
            lzbir =  aop(iopk,4154,1) 
            dzbir =  suma_liste(iopk,[4150,4152],1)-aop(iopk,4151,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4154 = AOP-u (4150 - 4151 + 4152)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40067
        if not( aop(iopk,4155,1) == 0 ):
            lzbir =  aop(iopk,4155,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4155 = 0 Nerealizovani dobici po osnovu HOV ne mogu imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40068
        if not( aop(iopk,4161,1) == 0 ):
            lzbir =  aop(iopk,4161,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4161 = 0 Nerealizovani dobici po osnovu HOV ne mogu imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40069
        if not( aop(iopk,4162,1) == suma_liste(iopk,[4156,4158,4160],1)-suma_liste(iopk,[4157,4159],1) ):
            lzbir =  aop(iopk,4162,1) 
            dzbir =  suma_liste(iopk,[4156,4158,4160],1)-suma_liste(iopk,[4157,4159],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4162 = AOP-u (4156 - 4157 + 4158 - 4159 + 4160)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40070
        if not( aop(iopk,4165,1) == 0 ):
            lzbir =  aop(iopk,4165,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4165 = 0 Nerealizovani dobici po osnovu HOV ne mogu imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40071
        if not( aop(iopk,4166,1) == suma_liste(iopk,[4162,4164],1)-aop(iopk,4163,1) ):
            lzbir =  aop(iopk,4166,1) 
            dzbir =  suma_liste(iopk,[4162,4164],1)-aop(iopk,4163,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4166 = AOP-u (4162 - 4163 + 4164)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40072
        if not( aop(iopk,4171,1) == 0 ):
            lzbir =  aop(iopk,4171,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4171 = 0 Nerealizovani dobici po osnovu HOV ne mogu imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40073
        if not( aop(iopk,4172,1) == suma_liste(iopk,[4166,4168,4170],1)-suma_liste(iopk,[4167,4169],1) ):
            lzbir =  aop(iopk,4172,1) 
            dzbir =  suma_liste(iopk,[4166,4168,4170],1)-suma_liste(iopk,[4167,4169],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4172 = AOP-u (4166 - 4167 + 4168 - 4169 + 4170)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40074
        if not( aop(iopk,4175,1) == 0 ):
            lzbir =  aop(iopk,4175,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4175 = 0 Nerealizovani dobici po osnovu HOV ne mogu imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40075
        if not( aop(iopk,4176,1) == suma_liste(iopk,[4172,4174],1)-aop(iopk,4173,1) ):
            lzbir =  aop(iopk,4176,1) 
            dzbir =  suma_liste(iopk,[4172,4174],1)-aop(iopk,4173,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4176 = AOP-u (4172 - 4173 + 4174)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40076
        if not( aop(iopk,4178,1) == 0 ):
            lzbir =  aop(iopk,4178,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4178 = 0 Nerealizovani gubici po osnovu HOV ne mogu imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40077
        if not( aop(iopk,4183,1) == suma_liste(iopk,[4177,4179,4181],1)-suma_liste(iopk,[4180,4182],1) ):
            lzbir =  aop(iopk,4183,1) 
            dzbir =  suma_liste(iopk,[4177,4179,4181],1)-suma_liste(iopk,[4180,4182],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4183 = AOP-u (4177 + 4179 - 4180 + 4181 - 4182)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40078
        if not( aop(iopk,4184,1) == 0 ):
            lzbir =  aop(iopk,4184,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4184 = 0 Nerealizovani gubici po osnovu HOV ne mogu imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40079
        if not( aop(iopk,4187,1) == suma_liste(iopk,[4183,4185],1)-aop(iopk,4186,1) ):
            lzbir =  aop(iopk,4187,1) 
            dzbir =  suma_liste(iopk,[4183,4185],1)-aop(iopk,4186,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4187 = AOP-u (4183 + 4185 - 4186)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40080
        if not( aop(iopk,4188,1) == 0 ):
            lzbir =  aop(iopk,4188,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4188 = 0 Nerealizovani gubici po osnovu HOV ne mogu imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40081
        if not( aop(iopk,4193,1) == suma_liste(iopk,[4187,4189,4191],1)-suma_liste(iopk,[4190,4192],1) ):
            lzbir =  aop(iopk,4193,1) 
            dzbir =  suma_liste(iopk,[4187,4189,4191],1)-suma_liste(iopk,[4190,4192],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4193 = AOP-u (4187 + 4189 - 4190 + 4191 - 4192)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40082
        if not( aop(iopk,4194,1) == 0 ):
            lzbir =  aop(iopk,4194,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4194 = 0 Nerealizovani gubici po osnovu HOV ne mogu imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40083
        if not( aop(iopk,4197,1) == suma_liste(iopk,[4193,4195],1)-aop(iopk,4196,1) ):
            lzbir =  aop(iopk,4197,1) 
            dzbir =  suma_liste(iopk,[4193,4195],1)-aop(iopk,4196,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4197 = AOP-u (4193 + 4195 - 4196)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40084
        if not( aop(iopk,4198,1) == 0 ):
            lzbir =  aop(iopk,4198,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4198 = 0 Nerealizovani gubici po osnovu HOV ne mogu imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40085
        #Za ovaj set se ne primenjuje pravilo 
        
        #40086
        if not( aop(iopk,4199,1) == 0 ):
            lzbir =  aop(iopk,4199,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4199 = 0 Učešće bez prava kontrole ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40087
        if not( aop(iopk,4205,1) == 0 ):
            lzbir =  aop(iopk,4205,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4205 = 0 Učešće bez prava kontrole ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40088
        if not( aop(iopk,4206,1) == suma_liste(iopk,[4200,4202,4204],1)-suma_liste(iopk,[4201,4203],1) ):
            lzbir =  aop(iopk,4206,1) 
            dzbir =  suma_liste(iopk,[4200,4202,4204],1)-suma_liste(iopk,[4201,4203],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4206 = AOP-u (4200 - 4201 + 4202 - 4203 + 4204)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40089
        if not( aop(iopk,4209,1) == 0 ):
            lzbir =  aop(iopk,4209,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4209 = 0 Učešće bez prava kontrole ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40090
        if not( aop(iopk,4210,1) == suma_liste(iopk,[4206,4208],1)-aop(iopk,4207,1) ):
            lzbir =  aop(iopk,4210,1) 
            dzbir =  suma_liste(iopk,[4206,4208],1)-aop(iopk,4207,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4210 = AOP-u (4206 - 4207 + 4208)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40091
        if not( aop(iopk,4215,1) == 0 ):
            lzbir =  aop(iopk,4215,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4215 = 0 Učešće bez prava kontrole ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40092
        if not( aop(iopk,4216,1) == suma_liste(iopk,[4210,4212,4214],1)-suma_liste(iopk,[4211,4213],1) ):
            lzbir =  aop(iopk,4216,1) 
            dzbir =  suma_liste(iopk,[4210,4212,4214],1)-suma_liste(iopk,[4211,4213],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4216 = AOP-u (4210 - 4211 + 4212 - 4213 + 4214)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40093
        if not( aop(iopk,4219,1) == 0 ):
            lzbir =  aop(iopk,4219,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4219 = 0 Učešće bez prava kontrole ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40094
        if not( aop(iopk,4220,1) == suma_liste(iopk,[4216,4218],1)-aop(iopk,4217,1) ):
            lzbir =  aop(iopk,4220,1) 
            dzbir =  suma_liste(iopk,[4216,4218],1)-aop(iopk,4217,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4220 = AOP-u (4216 - 4217 + 4218)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40095
        if not( aop(iopk,4221,1) == 0 ):
            lzbir =  aop(iopk,4221,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4221 = 0 Ukupan kapital ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40096
        if( suma_liste(iopk,[4002,4024,4046,4068,4090,4112,4134,4156,4178,4200],1) > suma_liste(iopk,[4001,4023,4045,4067,4089,4111,4133,4155,4177,4199],1) ):
            if not( aop(iopk,4222,1) == suma_liste(iopk,[4002,4024,4046,4068,4090,4112,4134,4156,4178,4200],1)-suma_liste(iopk,[4001,4023,4045,4067,4089,4111,4133,4155,4177,4199],1) ):
                lzbir =  aop(iopk,4222,1) 
                dzbir =  suma_liste(iopk,[4002,4024,4046,4068,4090,4112,4134,4156,4178,4200],1)-suma_liste(iopk,[4001,4023,4045,4067,4089,4111,4133,4155,4177,4199],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4222 = AOP-u (4002 + 4024 + 4046 + 4068 + 4090 + 4112 + 4134 + 4156 + 4178 + 4200 - 4001 - 4023 - 4045 - 4067 - 4089 - 4111 - 4133 - 4155 - 4177 - 4199), ako je AOP (4002 + 4024 + 4046 + 4068 + 4090 + 4112 + 4134 + 4156 + 4178 + 4200 ) > AOP-a (4001 + 4023 + 4045 + 4067 + 4089 + 4111 + 4133 + 4155 + 4177 + 4199)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40097
        if( suma_liste(iopk,[4002,4024,4046,4068,4090,4112,4134,4156,4178,4200],1) < suma_liste(iopk,[4001,4023,4045,4067,4089,4111,4133,4155,4177,4199],1) ):
            if not( aop(iopk,4243,1) == suma_liste(iopk,[4001,4023,4045,4067,4089,4111,4133,4155,4177,4199],1)-suma_liste(iopk,[4002,4024,4046,4068,4090,4112,4134,4156,4178,4200],1) ):
                lzbir =  aop(iopk,4243,1) 
                dzbir =  suma_liste(iopk,[4001,4023,4045,4067,4089,4111,4133,4155,4177,4199],1)-suma_liste(iopk,[4002,4024,4046,4068,4090,4112,4134,4156,4178,4200],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4243 = AOP-u (4001 + 4023 + 4045 + 4067 + 4089 + 4111 + 4133 + 4155 + 4177 + 4199 - 4002 - 4024 - 4046 - 4068 - 4090 - 4112 - 4134 - 4156 - 4178 - 4200 ), ako je AOP (4002 + 4024 + 4046 + 4068 + 4090 + 4112 + 4134 + 4156 + 4178 + 4200 ) < AOP-a (4001 + 4023 + 4045 + 4067 + 4089 + 4111 + 4133 + 4155 + 4177 + 4199)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40098
        if not( aop(iopk,4244,1) == 0 ):
            lzbir =  aop(iopk,4244,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4244 = 0 Gubitak iznad visine  kapitala ne može imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40099
        if( suma_liste(iopk,[4002,4024,4046,4068,4090,4112,4134,4156,4178,4200],1) == suma_liste(iopk,[4001,4023,4045,4067,4089,4111,4133,4155,4177,4199],1) ):
            if not( aop(iopk,4222,1) + aop(iopk,4243,1) == 0 ):
                lzbir =  aop(iopk,4222,1) + aop(iopk,4243,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP (4222 + 4243) = 0, ako je AOP (4002 + 4024 + 4046 + 4068 + 4090 + 4112 + 4134 + 4156 + 4178 + 4200 ) = AOP-u (4001 + 4023 + 4045 + 4067 + 4089 + 4111 + 4133 + 4155 + 4177 + 4199) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40100
        if( aop(iopk,4222,1) > 0 ):
            if not( aop(iopk,4243,1) == 0 ):
                lzbir =  aop(iopk,4243,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4222 > 0 onda je AOP 4243 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40101
        if( aop(iopk,4243,1) > 0 ):
            if not( aop(iopk,4222,1) == 0 ):
                lzbir =  aop(iopk,4222,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4243 > 0 onda je AOP 4222 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40102
        if not( aop(iopk,4223,1) == 0 ):
            lzbir =  aop(iopk,4223,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4223 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40103
        if not( aop(iopk,4224,1) == 0 ):
            lzbir =  aop(iopk,4224,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4224 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40104
        if not( aop(iopk,4245,1) == 0 ):
            lzbir =  aop(iopk,4245,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4245 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40105
        if not( aop(iopk,4246,1) == 0 ):
            lzbir =  aop(iopk,4246,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4246 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40106
        if not( aop(iopk,4225,1) == 0 ):
            lzbir =  aop(iopk,4225,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4225 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40107
        if not( aop(iopk,4226,1) == 0 ):
            lzbir =  aop(iopk,4226,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4226 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40108
        if not( aop(iopk,4247,1) == 0 ):
            lzbir =  aop(iopk,4247,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4247 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40109
        if not( aop(iopk,4248,1) == 0 ):
            lzbir =  aop(iopk,4248,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4248 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40110
        if not( aop(iopk,4227,1) == 0 ):
            lzbir =  aop(iopk,4227,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4227 = 0 Ukupan kapital ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40111
        if( suma_liste(iopk,[4008,4030,4052,4074,4096,4118,4140,4162,4184,4206],1) > suma_liste(iopk,[4007,4029,4051,4073,4095,4117,4139,4161,4183,4205],1) ):
            if not( aop(iopk,4228,1) == suma_liste(iopk,[4008,4030,4052,4074,4096,4118,4140,4162,4184,4206],1)-suma_liste(iopk,[4007,4029,4051,4073,4095,4117,4139,4161,4183,4205],1) ):
                lzbir =  aop(iopk,4228,1) 
                dzbir =  suma_liste(iopk,[4008,4030,4052,4074,4096,4118,4140,4162,4184,4206],1)-suma_liste(iopk,[4007,4029,4051,4073,4095,4117,4139,4161,4183,4205],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4228 = AOP-u (4008 + 4030 + 4052 + 4074 + 4096 + 4118 + 4140 + 4162 + 4184 + 4206 - 4007 - 4029 - 4051 - 4073 - 4095 - 4117 - 4139 - 4161 - 4183 - 4205), ako je AOP (4008 + 4030 + 4052 + 4074 + 4096 + 4118 + 4140 + 4162 + 4184 + 4206) > AOP-a (4007 + 4029 + 4051 + 4073 + 4095 + 4117 + 4139 + 4161 + 4183 + 4205)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40112
        if( suma_liste(iopk,[4008,4030,4052,4074,4096,4118,4140,4162,4184,4206],1) < suma_liste(iopk,[4007,4029,4051,4073,4095,4117,4139,4161,4183,4205],1) ):
            if not( aop(iopk,4249,1) == suma_liste(iopk,[4007,4029,4051,4073,4095,4117,4139,4161,4183,4205],1)-suma_liste(iopk,[4008,4030,4052,4074,4096,4118,4140,4162,4184,4206],1) ):
                lzbir =  aop(iopk,4249,1) 
                dzbir =  suma_liste(iopk,[4007,4029,4051,4073,4095,4117,4139,4161,4183,4205],1)-suma_liste(iopk,[4008,4030,4052,4074,4096,4118,4140,4162,4184,4206],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4249 = AOP-u (4007 + 4029 + 4051 + 4073 + 4095 + 4117 + 4139 + 4161 + 4183 + 4205 - 4008 - 4030 - 4052 - 4074 - 4096 - 4118 - 4140 - 4162 - 4184 - 4206), ako je AOP (4008 + 4030 + 4052 + 4074 + 4096 + 4118 + 4140 + 4162 + 4184 + 4206) < AOP-a (4007 + 4029 + 4051 + 4073 + 4095 + 4117 + 4139 + 4161 + 4183 + 4205)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40113
        if not( aop(iopk,4250,1) == 0 ):
            lzbir =  aop(iopk,4250,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4250 = 0 Gubitak iznad visine  kapitala ne može imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40114
        if( suma_liste(iopk,[4008,4030,4052,4074,4096,4118,4140,4162,4184,4206],1) == suma_liste(iopk,[4007,4029,4051,4073,4095,4117,4139,4161,4183,4205],1) ):
            if not( aop(iopk,4228,1) + aop(iopk,4249,1) == 0 ):
                lzbir =  aop(iopk,4228,1) + aop(iopk,4249,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP (4228 + 4249) = 0, ako je AOP (4008 + 4030 + 4052 + 4074 + 4096 + 4118 + 4140 + 4162 + 4184 + 4206) = AOP-u (4007 + 4029 + 4051 + 4073 + 4095 + 4117 + 4139 + 4161 + 4183 + 4205) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40115
        if( aop(iopk,4228,1) > 0 ):
            if not( aop(iopk,4249,1) == 0 ):
                lzbir =  aop(iopk,4249,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4228 > 0 onda je AOP 4249 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40116
        if( aop(iopk,4249,1) > 0 ):
            if not( aop(iopk,4228,1) == 0 ):
                lzbir =  aop(iopk,4228,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4249 > 0 onda je AOP 4228 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40117
        if not( aop(iopk,4229,1) == 0 ):
            lzbir =  aop(iopk,4229,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4229 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40118
        if not( aop(iopk,4230,1) == 0 ):
            lzbir =  aop(iopk,4230,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4230 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40119
        if not( aop(iopk,4251,1) == 0 ):
            lzbir =  aop(iopk,4251,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4251 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40120
        if not( aop(iopk,4252,1) == 0 ):
            lzbir =  aop(iopk,4252,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4252 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40121
        if not( aop(iopk,4231,1) == 0 ):
            lzbir =  aop(iopk,4231,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4231 = 0 Ukupan kapital ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40122
        if( suma_liste(iopk,[4012,4034,4056,4078,4100,4122,4144,4166,4188,4210],1) > suma_liste(iopk,[4011,4033,4055,4077,4099,4121,4143,4165,4187,4209],1) ):
            if not( aop(iopk,4232,1) == suma_liste(iopk,[4012,4034,4056,4078,4100,4122,4144,4166,4188,4210],1)-suma_liste(iopk,[4011,4033,4055,4077,4099,4121,4143,4165,4187,4209],1) ):
                lzbir =  aop(iopk,4232,1) 
                dzbir =  suma_liste(iopk,[4012,4034,4056,4078,4100,4122,4144,4166,4188,4210],1)-suma_liste(iopk,[4011,4033,4055,4077,4099,4121,4143,4165,4187,4209],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4232 = AOP-u (4012 + 4034 + 4056 + 4078 + 4100 + 4122 + 4144 + 4166 + 4188 + 4210 - 4011 - 4033 - 4055 - 4077 - 4099 - 4121 - 4143 - 4165 - 4187 - 4209), ako je AOP (4012 + 4034 + 4056 + 4078 + 4100 + 4122 + 4144 + 4166 + 4188 + 4210 ) > AOP-a (4011 + 4033 + 4055 + 4077 + 4099 + 4121 + 4143 + 4165 + 4187 + 4209)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40123
        if( suma_liste(iopk,[4012,4034,4056,4078,4100,4122,4144,4166,4188,4210],1) < suma_liste(iopk,[4011,4033,4055,4077,4099,4121,4143,4165,4187,4209],1) ):
            if not( aop(iopk,4253,1) == suma_liste(iopk,[4011,4033,4055,4077,4099,4121,4143,4165,4187,4209],1)-suma_liste(iopk,[4012,4034,4056,4078,4100,4122,4144,4166,4188,4210],1) ):
                lzbir =  aop(iopk,4253,1) 
                dzbir =  suma_liste(iopk,[4011,4033,4055,4077,4099,4121,4143,4165,4187,4209],1)-suma_liste(iopk,[4012,4034,4056,4078,4100,4122,4144,4166,4188,4210],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4253 = AOP-u (4011 + 4033 + 4055 + 4077 + 4099 + 4121 + 4143 + 4165 + 4187 + 4209 - 4012 - 4034 - 4056 - 4078 - 4100 - 4122 - 4144 - 4166 - 4188 - 4210), ako je AOP (4012 + 4034 + 4056 + 4078 + 4100 + 4122 + 4144 + 4166 + 4188 + 4210) < AOP-a (4011 + 4033 + 4055 + 4077 + 4099 + 4121 + 4143 + 4165 + 4187 + 4209)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40124
        if not( aop(iopk,4254,1) == 0 ):
            lzbir =  aop(iopk,4254,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4254 = 0 Gubitak iznad visine  kapitala ne može imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40125
        if( suma_liste(iopk,[4012,4034,4056,4078,4100,4122,4144,4166,4188,4210],1) == suma_liste(iopk,[4011,4033,4055,4077,4099,4121,4143,4165,4187,4209],1) ):
            if not( aop(iopk,4232,1) + aop(iopk,4253,1) == 0 ):
                lzbir =  aop(iopk,4232,1) + aop(iopk,4253,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP (4232 + 4253) = 0, ako je AOP (4012 + 4034 + 4056 + 4078 + 4100 + 4122 + 4144 + 4166 + 4188 + 4210) = AOP-u (4011 + 4033 + 4055 + 4077 + 4099 + 4121 + 4143 + 4165 + 4187 + 4209) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40126
        if( aop(iopk,4232,1) > 0 ):
            if not( aop(iopk,4253,1) == 0 ):
                lzbir =  aop(iopk,4253,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4232 > 0 onda je AOP 4253 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40127
        if( aop(iopk,4253,1) > 0 ):
            if not( aop(iopk,4232,1) == 0 ):
                lzbir =  aop(iopk,4232,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je  AOP 4253 > 0 onda je AOP 4232 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40128
        if not( aop(iopk,4233,1) == 0 ):
            lzbir =  aop(iopk,4233,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4233 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40129
        if not( aop(iopk,4234,1) == 0 ):
            lzbir =  aop(iopk,4234,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4234 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40130
        if not( aop(iopk,4255,1) == 0 ):
            lzbir =  aop(iopk,4255,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4255 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40131
        if not( aop(iopk,4256,1) == 0 ):
            lzbir =  aop(iopk,4256,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4256 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40132
        if not( aop(iopk,4235,1) == 0 ):
            lzbir =  aop(iopk,4235,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4235 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40133
        if not( aop(iopk,4236,1) == 0 ):
            lzbir =  aop(iopk,4236,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4236 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40134
        if not( aop(iopk,4257,1) == 0 ):
            lzbir =  aop(iopk,4257,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4257 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40135
        if not( aop(iopk,4258,1) == 0 ):
            lzbir =  aop(iopk,4258,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4258 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40136
        if not( aop(iopk,4237,1) == 0 ):
            lzbir =  aop(iopk,4237,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4237 = 0 Ukupan kapital ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40137
        if( suma_liste(iopk,[4018,4040,4062,4084,4106,4128,4150,4172,4194,4216],1) > suma_liste(iopk,[4017,4039,4061,4083,4105,4127,4149,4171,4193,4215],1) ):
            if not( aop(iopk,4238,1) == suma_liste(iopk,[4018,4040,4062,4084,4106,4128,4150,4172,4194,4216],1)-suma_liste(iopk,[4017,4039,4061,4083,4105,4127,4149,4171,4193,4215],1) ):
                lzbir =  aop(iopk,4238,1) 
                dzbir =  suma_liste(iopk,[4018,4040,4062,4084,4106,4128,4150,4172,4194,4216],1)-suma_liste(iopk,[4017,4039,4061,4083,4105,4127,4149,4171,4193,4215],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4238 = AOP-u (4018 + 4040 + 4062 + 4084 + 4106 + 4128 + 4150 + 4172 + 4194 + 4216 - 4017 - 4039 - 4061 - 4083 - 4105 - 4127 - 4149 - 4171 - 4193 - 4215), ako je AOP (4018 + 4040 + 4062 + 4084 + 4106 + 4128 + 4150 + 4172 + 4194 + 4216) > AOP-a (4017 + 4039 + 4061 + 4083 + 4105 + 4127 + 4149 + 4171 + 4193 + 4215)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40138
        if( suma_liste(iopk,[4018,4040,4062,4084,4106,4128,4150,4172,4194,4216],1) < suma_liste(iopk,[4017,4039,4061,4083,4105,4127,4149,4171,4193,4215],1) ):
            if not( aop(iopk,4259,1) == suma_liste(iopk,[4017,4039,4061,4083,4105,4127,4149,4171,4193,4215],1)-suma_liste(iopk,[4018,4040,4062,4084,4106,4128,4150,4172,4194,4216],1) ):
                lzbir =  aop(iopk,4259,1) 
                dzbir =  suma_liste(iopk,[4017,4039,4061,4083,4105,4127,4149,4171,4193,4215],1)-suma_liste(iopk,[4018,4040,4062,4084,4106,4128,4150,4172,4194,4216],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4259 = AOP-u (4017 + 4039 + 4061 + 4083 + 4105 + 4127 + 4149 + 4171 + 4193 + 4215 - 4018 - 4040 - 4062 - 4084 - 4106 - 4128 - 4150 - 4172 - 4194 - 4216), ako je AOP (4018 + 4040 + 4062 + 4084 + 4106 + 4128 + 4150 + 4172 + 4194 + 4216) < AOP-a (4017 + 4039 + 4061 + 4083 + 4105 + 4127 + 4149 + 4171 + 4193 + 4215)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40139
        if not( aop(iopk,4260,1) == 0 ):
            lzbir =  aop(iopk,4260,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4260 = 0 Gubitak iznad visine  kapitala ne može imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40140
        if( suma_liste(iopk,[4018,4040,4062,4084,4106,4128,4150,4172,4194,4216],1) == suma_liste(iopk,[4017,4039,4061,4083,4105,4127,4149,4171,4193,4215],1) ):
            if not( aop(iopk,4238,1) + aop(iopk,4259,1) == 0 ):
                lzbir =  aop(iopk,4238,1) + aop(iopk,4259,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP (4238 + 4259) = 0, ako je AOP (4018 + 4040 + 4062 + 4084 + 4106 + 4128 + 4150 + 4172 + 4194 + 4216) = AOP-u (4017 + 4039 + 4061 + 4083 + 4105 + 4127 + 4149 + 4171 + 4193 + 4215) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40141
        if( aop(iopk,4238,1) > 0 ):
            if not( aop(iopk,4259,1) == 0 ):
                lzbir =  aop(iopk,4259,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4238 > 0 onda je AOP 4259 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40142
        if( aop(iopk,4259,1) > 0 ):
            if not( aop(iopk,4238,1) == 0 ):
                lzbir =  aop(iopk,4238,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4259 > 0 onda je AOP 4238 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40143
        if not( aop(iopk,4239,1) == 0 ):
            lzbir =  aop(iopk,4239,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4239 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40144
        if not( aop(iopk,4240,1) == 0 ):
            lzbir =  aop(iopk,4240,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4240 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40145
        if not( aop(iopk,4261,1) == 0 ):
            lzbir =  aop(iopk,4261,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4261 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40146
        if not( aop(iopk,4262,1) == 0 ):
            lzbir =  aop(iopk,4262,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4262 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40147
        if not( aop(iopk,4241,1) == 0 ):
            lzbir =  aop(iopk,4241,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4241 = 0 Ukupan kapital ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40148
        if( suma_liste(iopk,[4022,4044,4066,4088,4110,4132,4154,4176,4198,4220],1) > suma_liste(iopk,[4021,4043,4065,4087,4109,4131,4153,4175,4197,4219],1) ):
            if not( aop(iopk,4242,1) == suma_liste(iopk,[4022,4044,4066,4088,4110,4132,4154,4176,4198,4220],1)-suma_liste(iopk,[4021,4043,4065,4087,4109,4131,4153,4175,4197,4219],1) ):
                lzbir =  aop(iopk,4242,1) 
                dzbir =  suma_liste(iopk,[4022,4044,4066,4088,4110,4132,4154,4176,4198,4220],1)-suma_liste(iopk,[4021,4043,4065,4087,4109,4131,4153,4175,4197,4219],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4242 = AOP-u (4022 + 4044 + 4066 + 4088 + 4110 + 4132 + 4154 + 4176 + 4198 + 4220 - 4021 - 4043 - 4065 - 4087 - 4109 - 4131 - 4153 - 4175 - 4197 - 4219), ako je AOP (4022 + 4044 + 4066 + 4088 + 4110 + 4132 + 4154 + 4176 + 4198 + 4220) > AOP-a (4021 + 4043 + 4065 + 4087 + 4109 + 4131 + 4153 + 4175 + 4197 + 4219)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40149
        if( suma_liste(iopk,[4022,4044,4066,4088,4110,4132,4154,4176,4198,4220],1) < suma_liste(iopk,[4021,4043,4065,4087,4109,4131,4153,4175,4197,4219],1) ):
            if not( aop(iopk,4263,1) == suma_liste(iopk,[4021,4043,4065,4087,4109,4131,4153,4175,4197,4219],1)-suma_liste(iopk,[4022,4044,4066,4088,4110,4132,4154,4176,4198,4220],1) ):
                lzbir =  aop(iopk,4263,1) 
                dzbir =  suma_liste(iopk,[4021,4043,4065,4087,4109,4131,4153,4175,4197,4219],1)-suma_liste(iopk,[4022,4044,4066,4088,4110,4132,4154,4176,4198,4220],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4263 = AOP-u (4021 + 4043 + 4065 + 4087 + 4109 + 4131 + 4153 + 4175 + 4197 + 4219 - 4022 - 4044 - 4066 - 4088 - 4110 - 4132 - 4154 - 4176 - 4198 - 4220), ako je AOP (4022 + 4044 + 4066 + 4088 + 4110 + 4132 + 4154 + 4176 + 4198 + 4220) < AOP-a (4021 + 4043 + 4065 + 4087 + 4109 + 4131 + 4153 + 4175 + 4197 + 4219)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40150
        if not( aop(iopk,4264,1) == 0 ):
            lzbir =  aop(iopk,4264,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4264 = 0 Gubitak iznad visine  kapitala ne može imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40151
        if( suma_liste(iopk,[4022,4044,4066,4088,4110,4132,4154,4176,4198,4220],1) == suma_liste(iopk,[4021,4043,4065,4087,4109,4131,4153,4175,4197,4219],1) ):
            if not( aop(iopk,4242,1) + aop(iopk,4263,1) == 0 ):
                lzbir =  aop(iopk,4242,1) + aop(iopk,4263,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP (4242 + 4263) = 0, ako je AOP (4022 + 4044 + 4066 + 4088 + 4110 + 4132 + 4154 + 4176 + 4198 + 4220) = AOP-u (4021 + 4043 + 4065 + 4087 + 4109 + 4131 + 4153 + 4175 + 4197 + 4219) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40152
        if( aop(iopk,4242,1) > 0 ):
            if not( aop(iopk,4263,1) == 0 ):
                lzbir =  aop(iopk,4263,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4242 > 0 onda je AOP 4263 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40153
        if( aop(iopk,4263,1) > 0 ):
            if not( aop(iopk,4242,1) == 0 ):
                lzbir =  aop(iopk,4242,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4263 > 0 onda je AOP 4242 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40154
        if not( aop(iopk,4008,1) == aop(bs,402,7) ):
            lzbir =  aop(iopk,4008,1) 
            dzbir =  aop(bs,402,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4008 = AOP-u 0402 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4008 = AOP-u 0402 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40155
        if not( aop(iopk,4012,1) == aop(bs,402,6) ):
            lzbir =  aop(iopk,4012,1) 
            dzbir =  aop(bs,402,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4012 = AOP-u 0402 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4012 = AOP-u 0402 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40156
        if not( aop(iopk,4022,1) == aop(bs,402,5) ):
            lzbir =  aop(iopk,4022,1) 
            dzbir =  aop(bs,402,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4022 = AOP-u 0402 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4022 = AOP-u 0402 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40157
        if not( aop(iopk,4029,1) == aop(bs,403,7) ):
            lzbir =  aop(iopk,4029,1) 
            dzbir =  aop(bs,403,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4029 = AOP-u 0403 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4029 = AOP-u 0403 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40158
        if not( aop(iopk,4033,1) == aop(bs,403,6) ):
            lzbir =  aop(iopk,4033,1) 
            dzbir =  aop(bs,403,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4033 = AOP-u 0403 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4033 = AOP-u 0403 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40159
        if not( aop(iopk,4043,1) == aop(bs,403,5) ):
            lzbir =  aop(iopk,4043,1) 
            dzbir =  aop(bs,403,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4043 = AOP-u 0403 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4043 = AOP-u 0403 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40160
        if not( aop(iopk,4052,1) == suma_liste(bs,[404,407],7) ):
            lzbir =  aop(iopk,4052,1) 
            dzbir =  suma_liste(bs,[404,407],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4052 = AOP-u (0404 + 0407) kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4052 = AOP-u (0404 + 0407) kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40161
        if not( aop(iopk,4056,1) == suma_liste(bs,[404,407],6) ):
            lzbir =  aop(iopk,4056,1) 
            dzbir =  suma_liste(bs,[404,407],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4056 = AOP-u (0404 + 0407) kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4056 = AOP-u (0404 + 0407) kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40162
        if not( aop(iopk,4066,1) == suma_liste(bs,[404,407],5) ):
            lzbir =  aop(iopk,4066,1) 
            dzbir =  suma_liste(bs,[404,407],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4066 = AOP-u (0404 + 0407) kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4066 = AOP-u (0404 + 0407) kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40163
        if not( aop(iopk,4073,1) == aop(bs,415,7) ):
            lzbir =  aop(iopk,4073,1) 
            dzbir =  aop(bs,415,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4073 = AOP-u 0415 kol. 7  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4073 = AOP-u 0415 kol. 7  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40164
        if not( aop(iopk,4077,1) == aop(bs,415,6) ):
            lzbir =  aop(iopk,4077,1) 
            dzbir =  aop(bs,415,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4077 = AOP-u 0415 kol. 6  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4077 = AOP-u 0415 kol. 6  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40165
        if not( aop(iopk,4087,1) == aop(bs,415,5) ):
            lzbir =  aop(iopk,4087,1) 
            dzbir =  aop(bs,415,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4087 = AOP-u 0415 kol. 5  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4087 = AOP-u 0415 kol. 5  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40166
        if not( aop(iopk,4095,1) == aop(bs,418,7) ):
            lzbir =  aop(iopk,4095,1) 
            dzbir =  aop(bs,418,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4095 = AOP-u 0418 kol. 7  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4095 = AOP-u 0418 kol. 7  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40167
        if not( aop(iopk,4099,1) == aop(bs,418,6) ):
            lzbir =  aop(iopk,4099,1) 
            dzbir =  aop(bs,418,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4099 = AOP-u 0418 kol. 6  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4099 = AOP-u 0418 kol. 6  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40168
        if not( aop(iopk,4109,1) == aop(bs,418,5) ):
            lzbir =  aop(iopk,4109,1) 
            dzbir =  aop(bs,418,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4109 = AOP-u 0418 kol. 5  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4109 = AOP-u 0418 kol. 5  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40169
        if not( aop(iopk,4118,1) == aop(bs,411,7) ):
            lzbir =  aop(iopk,4118,1) 
            dzbir =  aop(bs,411,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4118 = AOP-u 0411 kol. 7  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4118 = AOP-u 0411 kol. 7  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40170
        if not( aop(iopk,4122,1) == aop(bs,411,6) ):
            lzbir =  aop(iopk,4122,1) 
            dzbir =  aop(bs,411,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4122 = AOP-u 0411 kol. 6  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4122 = AOP-u 0411 kol. 6  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40171
        if not( aop(iopk,4132,1) == aop(bs,411,5) ):
            lzbir =  aop(iopk,4132,1) 
            dzbir =  aop(bs,411,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4132 = AOP-u 0411 kol. 5  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4132 = AOP-u 0411 kol. 5  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40172
        if not( aop(iopk,4140,1) == aop(bs,408,7) ):
            lzbir =  aop(iopk,4140,1) 
            dzbir =  aop(bs,408,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4140 = AOP-u 0408 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4140 = AOP-u 0408 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40173
        if not( aop(iopk,4144,1) == aop(bs,408,6) ):
            lzbir =  aop(iopk,4144,1) 
            dzbir =  aop(bs,408,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4144 = AOP-u 0408 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4144 = AOP-u 0408 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40174
        if not( aop(iopk,4154,1) == aop(bs,408,5) ):
            lzbir =  aop(iopk,4154,1) 
            dzbir =  aop(bs,408,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP4154 = AOP-u 0408 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP4154 = AOP-u 0408 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40175
        if not( aop(iopk,4162,1) == aop(bs,409,7) ):
            lzbir =  aop(iopk,4162,1) 
            dzbir =  aop(bs,409,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4162 = AOP-u 0409 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4162 = AOP-u 0409 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40176
        if not( aop(iopk,4166,1) == aop(bs,409,6) ):
            lzbir =  aop(iopk,4166,1) 
            dzbir =  aop(bs,409,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4166 = AOP-u 0409 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4166 = AOP-u 0409 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40177
        if not( aop(iopk,4176,1) == aop(bs,409,5) ):
            lzbir =  aop(iopk,4176,1) 
            dzbir =  aop(bs,409,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4176 = AOP-u 0409 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4176 = AOP-u 0409 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40178
        if not( aop(iopk,4183,1) == aop(bs,410,7) ):
            lzbir =  aop(iopk,4183,1) 
            dzbir =  aop(bs,410,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4183 = AOP-u 0410 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4183 = AOP-u 0410 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40179
        if not( aop(iopk,4187,1) == aop(bs,410,6) ):
            lzbir =  aop(iopk,4187,1) 
            dzbir =  aop(bs,410,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4187 = AOP-u 0410 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4187 = AOP-u 0410 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40180
        if not( aop(iopk,4197,1) == aop(bs,410,5) ):
            lzbir =  aop(iopk,4197,1) 
            dzbir =  aop(bs,410,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4197 = AOP-u 0410 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4197 = AOP-u 0410 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40181
        if not( aop(iopk,4206,1) == aop(bs,414,7) ):
            lzbir =  aop(iopk,4206,1) 
            dzbir =  aop(bs,414,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4206 = AOP-u 0414 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4206 = AOP-u 0414 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40182
        if not( aop(iopk,4210,1) == aop(bs,414,6) ):
            lzbir =  aop(iopk,4210,1) 
            dzbir =  aop(bs,414,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4210 = AOP-u 0414 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4210 = AOP-u 0414 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40183
        if not( aop(iopk,4220,1) == aop(bs,414,5) ):
            lzbir =  aop(iopk,4220,1) 
            dzbir =  aop(bs,414,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4220 = AOP-u 0414 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4220 = AOP-u 0414 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40184
        if not( aop(iopk,4228,1) == aop(bs,401,7) ):
            lzbir =  aop(iopk,4228,1) 
            dzbir =  aop(bs,401,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4228 = AOP-u 0401 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4228 = AOP-u 0401 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40185
        if not( aop(iopk,4232,1) == aop(bs,401,6) ):
            lzbir =  aop(iopk,4232,1) 
            dzbir =  aop(bs,401,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4232 = AOP-u 0401 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4232 = AOP-u 0401 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40186
        if not( aop(iopk,4242,1) == aop(bs,401,5) ):
            lzbir =  aop(iopk,4242,1) 
            dzbir =  aop(bs,401,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4242 = AOP-u 0401 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4242 = AOP-u 0401 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40187
        if not( aop(iopk,4249,1) == aop(bs,446,7) ):
            lzbir =  aop(iopk,4249,1) 
            dzbir =  aop(bs,446,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4249 = AOP-u 0446 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4249 = AOP-u 0446 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40188
        if not( aop(iopk,4253,1) == aop(bs,446,6) ):
            lzbir =  aop(iopk,4253,1) 
            dzbir =  aop(bs,446,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4253 = AOP-u 0446 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4253 = AOP-u 0446 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40189
        if not( aop(iopk,4263,1) == aop(bs,446,5) ):
            lzbir =  aop(iopk,4263,1) 
            dzbir =  aop(bs,446,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4263 = AOP-u 0446 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4263 = AOP-u 0446 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        
        #POSEBNI PODACI:
        #●PRAVILO NE TREBA DA BUDE VIDLJIVO ZA KORISNIKA, ODNOSNO ZA OBVEZNIKA TREBA DA VIDI SAMO KOMENTAR KOJI JE DAT UZ PRAVILO. 
        #●U OBRASCU NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #100001
        if not( aop(pp,10002,1) >= 0 ):
            
            naziv_obrasca='Posebni podaci'
            poruka  =' Podatak o prosečnom broju zaposlenih mora biti upisan; ako nema zaposlenih upisuje se broj 0 '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #100002
        if not( aop(pp,10002,1) <= 250 ):
            
            naziv_obrasca='Posebni podaci'
            poruka  =' Granične vrednosti date su da bi se izbegle slučajne greške prilikom iskazivanja broja zaposlenih; Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        pps=Zahtev.Forme['Posebni podaci'].TekstualnaPoljaForme
        ppsnum=Zahtev.Forme['Posebni podaci'].NumerickaPoljaForme
        
        #100003
        for x in range (10100, 10300):
            if validiraj_spisak_pravnih_lica_obuhvacenih_konsolidacijom( x, aop(pps,x,2), aop(pps,x,3), aop(pps,x,4), aop(pps,x,5)) == False: 
                
                naziv_obrasca='Posebni podaci'
                poruka  ='Na spisak pravnih lica koja su obuhvaćena konsolidacijom mora biti unet bar jedno pravno lice Na spisak pravnih lica koja su obuhvaćena konsolidacijom niste uneli nijedan podatak '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #100004
        for x in range (10100, 10300):
            if aop(pps,x,5) == Zahtev.ObveznikInfo.MaticniBroj: 
                
                naziv_obrasca='Posebni podaci'
                poruka  ='Matično pravno lice ne može biti na spisku pravnih lica koja su obuhvaćena konsolidacijom Matično pravno lice ne može biti na spisku pravnih lica koja su obuhvaćena konsolidacijom '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #100005
        for x in range (10100, 10300):
            if validiraj_spisak_pravnih_lica_obuhvacenih_konsolidacijom( x, aop(pps,x,2), aop(pps,x,3), aop(pps,x,4), aop(pps,x,5)) == False: 
                
                naziv_obrasca='Posebni podaci'
                poruka  ='Za domaće pravno lice obveznik mora da unese matični broj, poslovno ime i sedište, a za strano pravno lice poslovno ime, državu i sedište Za domaće pravno lice unesite  matični broj, poslovno ime i sedište. Za strano pravno lice unesite poslovno ime, državu i sedište '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #100006
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
        
        #100007 Pravilo za kontrolu da li je unešen pravilno redni broj
        for x in range (10100, 10300):
            if (aop(ppsnum, x, 1)!=0):
                if not (aop(ppsnum, x, 1)==(x-10099)):
                    rednibroj=aop(ppsnum, x, 1) 
                    
                    naziv_obrasca='Posebni podaci'
                    poruka  ='Redni broj na spisku mora biti unet po rastućem redosledu Na spisku pravnih lica koja su obuhvaćena konsolidacijom u koloni "Redni broj" podatak nije unet po rastućem redosledu '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
        
        #100008 kontrolno pravilo da korisnik ne sme da ostavi prazan red između validno unesenih redova
        for x in range(10100, 10300):
            if(aop(ppsnum, x, 1)==0):
                if( x != 10299 and aop(ppsnum, x+1,1)!=0 ): 
                    
                    naziv_obrasca='Posebni podaci'
                    poruka  ='Obveznik ne sme da ostavi prazan red između pravilno unetih rednih brojeva Na spisku pravnih lica koja su obuhvaćena konsolidacijom  potrebno je popuniti kolonu "redni broj" po rastućem redosledu brojeva bez preskakanja redova '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
        
        #100009 Obveznik mora uneti redni broj ukoliko je popunio podatke o zavisnom pravnom lici
        for x in range (10100, 10300):
            if (aop(ppsnum, x, 1) == 0):
                if (validiraj_spisak_pravnih_lica( x, aop(pps,x,2), aop(pps,x,3), aop(pps,x,4), aop(pps,x,5))):
                    rednibroj=aop(ppsnum, x, 1)
                    #form_errors.append("#100009 GRESKA: NEMA BROJA LEPO POPUNJENE KOLONE. Greska u redu: " +str(x-10099)+ " ,redni broj: "+str(rednibroj)) 
                    
                    naziv_obrasca='Posebni podaci'
                    poruka  ='Na spisku pravnih lica koja su obuhvaćena konsolidacijom obveznik mora uneti redni broj ukoliko je popunio podatke o zavisnom pravnom licu Na spisku pravnih lica koja su obuhvaćena konsolidacijom obveznik mora uneti redni broj ukoliko je popunio podatke o zavisnom pravnom licu '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
        
        #100010 Ukoliko je obveznik dodao redni broj da mora popuniti podatke o zavisnom pravnom licu.
        for x in range (10100, 10300):
            if (aop(ppsnum, x, 1) != 0 ):
                if (validiraj_spisak_pravnih_lica( x, aop(pps,x,2), aop(pps,x,3), aop(pps,x,4), aop(pps,x,5))==False):
                    rednibroj=aop(ppsnum, x, 1)
                    #form_errors.append("#100009 GRESKA: IMA BROJA LOSE POPUNJENE KOLONE. Greska u redu: " + str(x-10099)+ " ,redni broj: "+ str(rednibroj)) 
                    
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
