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
            if ((Zahtev.NacinPodnosenja.value__ == 1 or (Zahtev.NacinPodnosenja.value__ == 2 and Zahtev.FiStanje.value__ > 1) or (Zahtev.NacinPodnosenja.value__ == 3 and Zahtev.FiStanje.value__ > 0))):
                if Zahtev.UlazniDokumenti.Count>0:
                    for k in Zahtev.UlazniDokumenti.Keys:
                        if Zahtev.UlazniDokumenti[k].Obavezan==True and Zahtev.UlazniDokumenti[k].Barkod == None:
                            doc_errors.append('Dokument sa nazivom "'+Zahtev.UlazniDokumenti[k].Naziv+'" niste priložili.')


        
        #Prilagoditi proveru postojanja forme u zavisnosti od tipa FI

        if (Zahtev.NacinPodnosenja.value__ == 1 or Zahtev.NacinPodnosenja.value__ == 2 or (Zahtev.NacinPodnosenja.value__ == 3 and  Zahtev.FiStanje.value__ > 0)):
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

            si = getForme(Zahtev,'Statistički izveštaj')
            if len(si)==0:
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Statistički izveštaj nije popunjen'
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
        if not( suma(bs,1,33,5)+suma(bs,1,33,6)+suma(bs,1,33,7)+suma(bs,401,427,5)+suma(bs,401,427,6)+suma(bs,401,427,7)+suma(bu,1001,1064,5)+suma(bu,1001,1064,6)+suma(ioor,2001,2014,5)+suma(ioor,2001,2014,6)+suma(iotg,3001,3032,3)+suma(iotg,3001,3032,4)+suma(iopk,4001,4242,1)+suma(si,9005,9032,4)+suma(si,9005,9032,5) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP od (0001 do 0033) kol. 5 + (0001 do 0033) kol. 6 + (0001 do 0033) kol. 7 bilansa stanja + (0401 do 0427) kol. 5 + (0401 do 0427) kol. 6 + (0401 do 0427) kol. 7 bilansa stanja  + (1001 do 1064) kol. 5 + (1001 do 1064) kol. 6 bilansa uspeha + (2001 do 2014) kol. 5 + (2001 do 2014) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3032) kol. 3 + (3001 do 3032) kol. 4 izveštaja o tokovima gotovine + (4001 do 4242)kol.1  izveštaja o promenama na kapitalu + (9005 do 9032) kol. 4 + (9005 do 9032) kol. 5 statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP od (0001 do 0033) kol. 5 + (0001 do 0033) kol. 6 + (0001 do 0033) kol. 7 bilansa stanja + (0401 do 0427) kol. 5 + (0401 do 0427) kol. 6 + (0401 do 0427) kol. 7 bilansa stanja  + (1001 do 1064) kol. 5 + (1001 do 1064) kol. 6 bilansa uspeha + (2001 do 2014) kol. 5 + (2001 do 2014) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3032) kol. 3 + (3001 do 3032) kol. 4 izveštaja o tokovima gotovine + (4001 do 4242)kol.1  izveštaja o promenama na kapitalu + (9005 do 9032) kol. 4 + (9005 do 9032) kol. 5 statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='Zbir podataka na oznakama za AOP od (0001 do 0033) kol. 5 + (0001 do 0033) kol. 6 + (0001 do 0033) kol. 7 bilansa stanja + (0401 do 0427) kol. 5 + (0401 do 0427) kol. 6 + (0401 do 0427) kol. 7 bilansa stanja  + (1001 do 1064) kol. 5 + (1001 do 1064) kol. 6 bilansa uspeha + (2001 do 2014) kol. 5 + (2001 do 2014) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3032) kol. 3 + (3001 do 3032) kol. 4 izveštaja o tokovima gotovine + (4001 do 4242)kol.1  izveštaja o promenama na kapitalu + (9005 do 9032) kol. 4 + (9005 do 9032) kol. 5 statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='Zbir podataka na oznakama za AOP od (0001 do 0033) kol. 5 + (0001 do 0033) kol. 6 + (0001 do 0033) kol. 7 bilansa stanja + (0401 do 0427) kol. 5 + (0401 do 0427) kol. 6 + (0401 do 0427) kol. 7 bilansa stanja  + (1001 do 1064) kol. 5 + (1001 do 1064) kol. 6 bilansa uspeha + (2001 do 2014) kol. 5 + (2001 do 2014) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3032) kol. 3 + (3001 do 3032) kol. 4 izveštaja o tokovima gotovine + (4001 do 4242)kol.1  izveštaja o promenama na kapitalu + (9005 do 9032) kol. 4 + (9005 do 9032) kol. 5 statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='Zbir podataka na oznakama za AOP od (0001 do 0033) kol. 5 + (0001 do 0033) kol. 6 + (0001 do 0033) kol. 7 bilansa stanja + (0401 do 0427) kol. 5 + (0401 do 0427) kol. 6 + (0401 do 0427) kol. 7 bilansa stanja  + (1001 do 1064) kol. 5 + (1001 do 1064) kol. 6 bilansa uspeha + (2001 do 2014) kol. 5 + (2001 do 2014) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3032) kol. 3 + (3001 do 3032) kol. 4 izveštaja o tokovima gotovine + (4001 do 4242)kol.1  izveštaja o promenama na kapitalu + (9005 do 9032) kol. 4 + (9005 do 9032) kol. 5 statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir podataka na oznakama za AOP od (0001 do 0033) kol. 5 + (0001 do 0033) kol. 6 + (0001 do 0033) kol. 7 bilansa stanja + (0401 do 0427) kol. 5 + (0401 do 0427) kol. 6 + (0401 do 0427) kol. 7 bilansa stanja  + (1001 do 1064) kol. 5 + (1001 do 1064) kol. 6 bilansa uspeha + (2001 do 2014) kol. 5 + (2001 do 2014) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3032) kol. 3 + (3001 do 3032) kol. 4 izveštaja o tokovima gotovine + (4001 do 4242)kol.1  izveštaja o promenama na kapitalu + (9005 do 9032) kol. 4 + (9005 do 9032) kol. 5 statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}
        
        #00000-2
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-3
        # U bar jednoj od tri navedene forme kolona napomena mora da ima bar jedan karakter
        bsNapomene = Zahtev.Forme['Bilans stanja'].TekstualnaPoljaForme;
        buNapomene = Zahtev.Forme['Bilans uspeha'].TekstualnaPoljaForme;
        ioorNapomene = Zahtev.Forme['Izveštaj o ostalom rezultatu'].TekstualnaPoljaForme;

        if not (proveriNapomene(bsNapomene, 1, 33, 4) or proveriNapomene(bsNapomene, 401, 427, 4) or proveriNapomene(buNapomene, 1001, 1064, 4) or proveriNapomene(ioorNapomene, 2001, 2014, 4) ): 
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP od (0001 do 0033) bilansa stanja + (0401 do 0427) bilansa stanja + (1001 do 1064) bilansa uspeha + (2001 do 2014) izveštaja o ostalom rezultatu u koloni 4 (Napomena broj) mora biti unet bar jedan karakter Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP od (0001 do 0033) bilansa stanja + (0401 do 0427) bilansa stanja + (1001 do 1064) bilansa uspeha + (2001 do 2014) izveštaja o ostalom rezultatu u koloni 4 (Napomena broj) mora biti unet bar jedan karakter Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='Zbir podataka na oznakama za AOP od (0001 do 0033) bilansa stanja + (0401 do 0427) bilansa stanja + (1001 do 1064) bilansa uspeha + (2001 do 2014) izveštaja o ostalom rezultatu u koloni 4 (Napomena broj) mora biti unet bar jedan karakter Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        if not(Zahtev.Placen):
            ostalo_errors.append('Naknada za obradu i javno objavljivanje izveštaja i propisane dokumentacije nije uplaćena u propisanom iznosu. Instrukcije za uplatu propisane naknade date su u okviru PIS FI sistema za konkretan zahtev, na linku „Status naplate zahteva / Instrukcija za plaćanje". Ukoliko ste izvršili uplatu, a naknada nije uparena, priložite Dokaz o uplati naknade u delu Dokumentacija (na mestu predviđenom za dokaz o uplati naknade), kako biste mogli da podnesete izveštaj.');

        
        #Provera negativnih AOP-a
        lista=""
        lista_bs = find_negativni(bs, 1, 427, 5, 7)
        lista_bu = find_negativni(bu, 1001, 1064, 5, 6)
        lista_ioor = find_negativni(ioor, 2001, 2014, 5, 6)
        lista_iotg = find_negativni(iotg, 3001, 3032, 3, 4)
        lista_iopk = find_negativni(iopk, 4001, 4242, 1, 1)
        lista_si = find_negativni(si, 9001, 9032, 3, 5)

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
            naziv_obrasca='Statistički izveštaj'
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
        
        #IZVEŠTAJ O OSTALOM REZULTATU - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #20001
        if not( suma(ioor,2001,2014,5) > 0 ):
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='Zbir podataka na oznakama za AOP (2001 do 2014) kol. 5 > 0 Izveštaj o ostalom rezultatu, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #20002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(ioor,2001,2014,6) == 0 ):
                lzbir =  suma(ioor,2001,2014,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Zbir podataka na oznakama za AOP (2001 do 2014) kol. 6 = 0 Izveštaj o ostalom rezultatu za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(ioor,2001,2014,6) > 0 ):
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Zbir podataka na oznakama za AOP (2001 do 2014) kol. 6 > 0 Izveštaj o ostalom rezultatu, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #20004
        if not( aop(ioor,2001,5) == aop(bu,1061,5) ):
            lzbir =  aop(ioor,2001,5) 
            dzbir =  aop(bu,1061,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 2001 kol. 5 = AOP-u 1061 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2001 kol. 5 = AOP-u 1061 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20005
        if not( aop(ioor,2001,6) == aop(bu,1061,6) ):
            lzbir =  aop(ioor,2001,6) 
            dzbir =  aop(bu,1061,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 2001 kol. 6 = AOP-u 1061 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2001 kol. 6 = AOP-u 1061 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20006
        if not( aop(ioor,2002,5) == aop(bu,1062,5) ):
            lzbir =  aop(ioor,2002,5) 
            dzbir =  aop(bu,1062,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 2002 kol. 5 = AOP-u 1062 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2002 kol. 5 = AOP-u 1062 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20007
        if not( aop(ioor,2002,6) == aop(bu,1062,6) ):
            lzbir =  aop(ioor,2002,6) 
            dzbir =  aop(bu,1062,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 2002 kol. 6 = AOP-u 1062 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2002 kol. 6 = AOP-u 1062 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20008
        if( suma_liste(ioor,[2003,2005,2007,2009],5) > suma_liste(ioor,[2004,2006,2008,2010],5) ):
            if not( aop(ioor,2011,5) == suma_liste(ioor,[2003,2005,2007,2009],5)-suma_liste(ioor,[2004,2006,2008,2010],5) ):
                lzbir =  aop(ioor,2011,5) 
                dzbir =  suma_liste(ioor,[2003,2005,2007,2009],5)-suma_liste(ioor,[2004,2006,2008,2010],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2011 kol. 5 = AOP-u (2003 + 2005 + 2007 + 2009 - 2004 - 2006 - 2008 - 2010) kol. 5, ako je AOP (2003 + 2005 + 2007 + 2009) kol. 5 > AOP-a (2004 + 2006 + 2008 + 2010) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20009
        if( suma_liste(ioor,[2003,2005,2007,2009],6) > suma_liste(ioor,[2004,2006,2008,2010],6) ):
            if not( aop(ioor,2011,6) == suma_liste(ioor,[2003,2005,2007,2009],6)-suma_liste(ioor,[2004,2006,2008,2010],6) ):
                lzbir =  aop(ioor,2011,6) 
                dzbir =  suma_liste(ioor,[2003,2005,2007,2009],6)-suma_liste(ioor,[2004,2006,2008,2010],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2011 kol. 6 = AOP-u (2003 + 2005 + 2007 + 2009 - 2004 - 2006 - 2008 - 2010) kol. 6, ako je AOP (2003 + 2005 + 2007 + 2009) kol. 6 > AOP-a (2004 + 2006 + 2008 + 2010) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20010
        if( suma_liste(ioor,[2003,2005,2007,2009],5) < suma_liste(ioor,[2004,2006,2008,2010],5) ):
            if not( aop(ioor,2012,5) == suma_liste(ioor,[2004,2006,2008,2010],5)-suma_liste(ioor,[2003,2005,2007,2009],5) ):
                lzbir =  aop(ioor,2012,5) 
                dzbir =  suma_liste(ioor,[2004,2006,2008,2010],5)-suma_liste(ioor,[2003,2005,2007,2009],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2012 kol. 5 = AOP-u (2004 + 2006 + 2008 + 2010 - 2003 - 2005 - 2007 - 2009) kol. 5,  ako je AOP (2003 + 2005 + 2007 + 2009) kol. 5 < AOP-a (2004 + 2006 + 2008 + 2010) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20011
        if( suma_liste(ioor,[2003,2005,2007,2009],6) < suma_liste(ioor,[2004,2006,2008,2010],6) ):
            if not( aop(ioor,2012,6) == suma_liste(ioor,[2004,2006,2008,2010],6)-suma_liste(ioor,[2003,2005,2007,2009],6) ):
                lzbir =  aop(ioor,2012,6) 
                dzbir =  suma_liste(ioor,[2004,2006,2008,2010],6)-suma_liste(ioor,[2003,2005,2007,2009],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2012 kol. 6 = AOP-u (2004 + 2006 + 2008 + 2010 - 2003 - 2005 - 2007 - 2009) kol. 6,  ako je AOP (2003 + 2005 + 2007 + 2009) kol. 6 < AOP-a (2004 + 2006 + 2008 + 2010) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20012
        if( suma_liste(ioor,[2003,2005,2007,2009],5) == suma_liste(ioor,[2004,2006,2008,2010],5) ):
            if not( suma(ioor,2011,2012,5) == 0 ):
                lzbir =  suma(ioor,2011,2012,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP (2011 + 2012) kol. 5 = 0, ako je AOP (2003 + 2005 + 2007 + 2009) kol. 5 = AOP-u (2004 + 2006 + 2008 + 2010) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20013
        if( suma_liste(ioor,[2003,2005,2007,2009],6) == suma_liste(ioor,[2004,2006,2008,2010],6) ):
            if not( suma(ioor,2011,2012,6) == 0 ):
                lzbir =  suma(ioor,2011,2012,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP (2011 + 2012) kol. 6 = 0, ako je AOP (2003 + 2005 + 2007 + 2009) kol. 6 = AOP-u (2004 + 2006 + 2008 + 2010) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20014
        if( aop(ioor,2011,5) > 0 ):
            if not( aop(ioor,2012,5) == 0 ):
                lzbir =  aop(ioor,2012,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2011 kol. 5 > 0 onda je AOP 2012 kol. 5 = 0  U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan ostali sveobuhvatni dobitak i ukupan ostali sveobuhvatni gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20015
        if( aop(ioor,2012,5) > 0 ):
            if not( aop(ioor,2011,5) == 0 ):
                lzbir =  aop(ioor,2011,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2012 kol. 5 > 0 onda je AOP 2011 kol. 5 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan ostali sveobuhvatni dobitak i ukupan ostali sveobuhvatni gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20016
        if( aop(ioor,2011,6) > 0 ):
            if not( aop(ioor,2012,6) == 0 ):
                lzbir =  aop(ioor,2012,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2011 kol. 6 > 0 onda je AOP 2012 kol. 6 = 0  U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan ostali sveobuhvatni dobitak i ukupan ostali sveobuhvatni gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20017
        if( aop(ioor,2012,6) > 0 ):
            if not( aop(ioor,2011,6) == 0 ):
                lzbir =  aop(ioor,2011,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2012 kol. 6 > 0 onda je AOP 2011 kol. 6 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan ostali sveobuhvatni dobitak i ukupan ostali sveobuhvatni gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20018
        if not( suma_liste(ioor,[2003,2005,2007,2009,2012],5) == suma_liste(ioor,[2004,2006,2008,2010,2011],5) ):
            lzbir =  suma_liste(ioor,[2003,2005,2007,2009,2012],5) 
            dzbir =  suma_liste(ioor,[2004,2006,2008,2010,2011],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP (2003 + 2005 + 2007 + 2009 + 2012) kol. 5 = AOP-u (2004 + 2006 + 2008 + 2010 + 2011) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20019
        if not( suma_liste(ioor,[2003,2005,2007,2009,2012],6) == suma_liste(ioor,[2004,2006,2008,2010,2011],6) ):
            lzbir =  suma_liste(ioor,[2003,2005,2007,2009,2012],6) 
            dzbir =  suma_liste(ioor,[2004,2006,2008,2010,2011],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP (2003 + 2005 + 2007 + 2009 + 2012) kol. 6 = AOP-u (2004 + 2006 + 2008 + 2010 + 2011) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20020
        if( suma_liste(ioor,[2001,2011],5) > suma_liste(ioor,[2002,2012],5) ):
            if not( aop(ioor,2013,5) == suma_liste(ioor,[2001,2011],5)-suma_liste(ioor,[2002,2012],5) ):
                lzbir =  aop(ioor,2013,5) 
                dzbir =  suma_liste(ioor,[2001,2011],5)-suma_liste(ioor,[2002,2012],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2013 kol. 5 = AOP-u (2001 - 2002 + 2011 - 2012) kol. 5, ako je AOP (2001 + 2011) kol. 5 > AOP-a (2002 + 2012) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20021
        if( suma_liste(ioor,[2001,2011],6) > suma_liste(ioor,[2002,2012],6) ):
            if not( aop(ioor,2013,6) == suma_liste(ioor,[2001,2011],6)-suma_liste(ioor,[2002,2012],6) ):
                lzbir =  aop(ioor,2013,6) 
                dzbir =  suma_liste(ioor,[2001,2011],6)-suma_liste(ioor,[2002,2012],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2013 kol. 6 = AOP-u (2001 - 2002 + 2011 - 2012) kol. 6, ako je AOP (2001 + 2011) kol. 6 > AOP-a (2002 + 2012) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20022
        if( suma_liste(ioor,[2001,2011],5) < suma_liste(ioor,[2002,2012],5) ):
            if not( aop(ioor,2014,5) == suma_liste(ioor,[2002,2012],5)-suma_liste(ioor,[2001,2011],5) ):
                lzbir =  aop(ioor,2014,5) 
                dzbir =  suma_liste(ioor,[2002,2012],5)-suma_liste(ioor,[2001,2011],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2014 kol. 5 = AOP-u (2002 - 2001 + 2012 - 2011) kol. 5, ako je AOP (2001 + 2011) kol. 5 < AOP-a (2002 + 2012) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20023
        if( suma_liste(ioor,[2001,2011],6) < suma_liste(ioor,[2002,2012],6) ):
            if not( aop(ioor,2014,6) == suma_liste(ioor,[2002,2012],6)-suma_liste(ioor,[2001,2011],6) ):
                lzbir =  aop(ioor,2014,6) 
                dzbir =  suma_liste(ioor,[2002,2012],6)-suma_liste(ioor,[2001,2011],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2014 kol. 6 = AOP-u (2002 - 2001 + 2012 - 2011) kol. 6, ako je AOP (2001 + 2011) kol. 6 < AOP-a (2002 + 2012) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20024
        if( suma_liste(ioor,[2001,2011],5) == suma_liste(ioor,[2002,2012],5) ):
            if not( suma(ioor,2013,2014,5) == 0 ):
                lzbir =  suma(ioor,2013,2014,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP (2013 + 2014) kol. 5 = 0, ako je AOP (2001 + 2011) kol. 5 = AOP-u (2002 + 2012) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20025
        if( suma_liste(ioor,[2001,2011],6) == suma_liste(ioor,[2002,2012],6) ):
            if not( suma(ioor,2013,2014,6) == 0 ):
                lzbir =  suma(ioor,2013,2014,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP (2013 + 2014) kol. 6 = 0, ako je AOP (2001 + 2011) kol. 6 = AOP-u (2002 + 2012) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20026
        if( aop(ioor,2013,5) > 0 ):
            if not( aop(ioor,2014,5) == 0 ):
                lzbir =  aop(ioor,2014,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2013 kol. 5 > 0 onda je AOP 2014 kol. 5 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan neto sveobuhvatni dobitak i ukupan neto sveobuhvatni gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20027
        if( aop(ioor,2014,5) > 0 ):
            if not( aop(ioor,2013,5) == 0 ):
                lzbir =  aop(ioor,2013,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2014 kol. 5 > 0 onda je AOP 2013 kol. 5 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan neto sveobuhvatni dobitak i ukupan neto sveobuhvatni gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20028
        if( aop(ioor,2013,6) > 0 ):
            if not( aop(ioor,2014,6) == 0 ):
                lzbir =  aop(ioor,2014,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2013 kol. 6 > 0 onda je AOP 2014 kol. 6 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan neto sveobuhvatni dobitak i ukupan neto sveobuhvatni gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20029
        if( aop(ioor,2014,6) > 0 ):
            if not( aop(ioor,2013,6) == 0 ):
                lzbir =  aop(ioor,2013,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2014 kol. 6 > 0 onda je AOP 2013 kol. 6 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan neto sveobuhvatni dobitak i ukupan neto sveobuhvatni gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20030
        if not( suma_liste(ioor,[2001,2011,2014],5) == suma_liste(ioor,[2002,2012,2013],5) ):
            lzbir =  suma_liste(ioor,[2001,2011,2014],5) 
            dzbir =  suma_liste(ioor,[2002,2012,2013],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP (2001 + 2011 + 2014) kol. 5 = AOP-u (2002 + 2012 + 2013) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20031
        if not( suma_liste(ioor,[2001,2011,2014],6) == suma_liste(ioor,[2002,2012,2013],6) ):
            lzbir =  suma_liste(ioor,[2001,2011,2014],6) 
            dzbir =  suma_liste(ioor,[2002,2012,2013],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP (2001 + 2011 + 2014) kol. 6 = AOP-u (2002 + 2012 + 2013) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        
        #IZVEŠTAJ O TOKOVIMA GOTOVINE - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #30001
        if not( suma(iotg,3001,3032,3) > 0 ):
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='Zbir podataka na oznakama za AOP (3001 do 3032) kol. 3 > 0 Izveštaj o tokovima gotovine, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #30002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(iotg,3001,3032,4) == 0 ):
                lzbir =  suma(iotg,3001,3032,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Zbir podataka na oznakama za AOP (3001 do 3032) kol. 4 = 0 Izveštaj o tokovima gotovine za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(iotg,3001,3032,4) > 0 ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Zbir podataka na oznakama za AOP (3001 do 3032) kol. 4 > 0 Izveštaj o tokovima gotovine, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #30004
        if not( aop(iotg,3001,3) == suma(iotg,3002,3005,3) ):
            lzbir =  aop(iotg,3001,3) 
            dzbir =  suma(iotg,3002,3005,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3001 kol. 3 = AOP-u (3002 + 3003 + 3004 + 3005) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30005
        if not( aop(iotg,3001,4) == suma(iotg,3002,3005,4) ):
            lzbir =  aop(iotg,3001,4) 
            dzbir =  suma(iotg,3002,3005,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3001 kol. 4 = AOP-u (3002 + 3003 + 3004 + 3005) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30006
        if not( aop(iotg,3006,3) == suma(iotg,3007,3013,3) ):
            lzbir =  aop(iotg,3006,3) 
            dzbir =  suma(iotg,3007,3013,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3006 kol. 3 = AOP-u (3007 + 3008 + 3009 + 3010 + 3011 + 3012 + 3013) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30007
        if not( aop(iotg,3006,4) == suma(iotg,3007,3013,4) ):
            lzbir =  aop(iotg,3006,4) 
            dzbir =  suma(iotg,3007,3013,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3006 kol. 4 = AOP-u (3007 + 3008 + 3009 + 3010 + 3011 + 3012 + 3013) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30008
        if( aop(iotg,3001,3) > aop(iotg,3006,3) ):
            if not( aop(iotg,3014,3) == aop(iotg,3001,3)-aop(iotg,3006,3) ):
                lzbir =  aop(iotg,3014,3) 
                dzbir =  aop(iotg,3001,3)-aop(iotg,3006,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3014 kol. 3 = AOP-u (3001 - 3006) kol. 3, ako je AOP 3001 kol. 3 > AOP-a 3006 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30009
        if( aop(iotg,3001,4) > aop(iotg,3006,4) ):
            if not( aop(iotg,3014,4) == aop(iotg,3001,4)-aop(iotg,3006,4) ):
                lzbir =  aop(iotg,3014,4) 
                dzbir =  aop(iotg,3001,4)-aop(iotg,3006,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3014 kol. 4 = AOP-u (3001 - 3006) kol. 4, ako je AOP 3001 kol. 4 > AOP-a 3006 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30010
        if( aop(iotg,3001,3) < aop(iotg,3006,3) ):
            if not( aop(iotg,3015,3) == aop(iotg,3006,3)-aop(iotg,3001,3) ):
                lzbir =  aop(iotg,3015,3) 
                dzbir =  aop(iotg,3006,3)-aop(iotg,3001,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3015 kol. 3 = AOP-u (3006 - 3001) kol. 3, ako je AOP 3001 kol. 3 < AOP-a 3006 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30011
        if( aop(iotg,3001,4) < aop(iotg,3006,4) ):
            if not( aop(iotg,3015,4) == aop(iotg,3006,4)-aop(iotg,3001,4) ):
                lzbir =  aop(iotg,3015,4) 
                dzbir =  aop(iotg,3006,4)-aop(iotg,3001,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3015 kol. 4 = AOP-u (3006 - 3001) kol. 4, ako je AOP 3001 kol. 4 < AOP-a 3006 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30012
        if( aop(iotg,3001,3) == aop(iotg,3006,3) ):
            if not( suma(iotg,3014,3015,3) == 0 ):
                lzbir =  suma(iotg,3014,3015,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3014 + 3015) kol. 3 = 0, ako je AOP 3001 kol. 3 = AOP-u 3006 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30013
        if( aop(iotg,3001,4) == aop(iotg,3006,4) ):
            if not( suma(iotg,3014,3015,4) == 0 ):
                lzbir =  suma(iotg,3014,3015,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3014 + 3015) kol. 4 = 0, ako je AOP 3001 kol. 4 = AOP-u 3006 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30014
        if( aop(iotg,3014,3) > 0 ):
            if not( aop(iotg,3015,3) == 0 ):
                lzbir =  aop(iotg,3015,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3014 kol. 3 > 0, onda je AOP 3015 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30015
        if( aop(iotg,3015,3) > 0 ):
            if not( aop(iotg,3014,3) == 0 ):
                lzbir =  aop(iotg,3014,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3015 kol. 3 > 0, onda je AOP 3014 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30016
        if( aop(iotg,3014,4) > 0 ):
            if not( aop(iotg,3015,4) == 0 ):
                lzbir =  aop(iotg,3015,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3014 kol. 4 > 0, onda je AOP 3015 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30017
        if( aop(iotg,3015,4) > 0 ):
            if not( aop(iotg,3014,4) == 0 ):
                lzbir =  aop(iotg,3014,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3015 kol. 4 > 0, onda je AOP 3014 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30018
        if not( suma_liste(iotg,[3001,3015],3) == suma_liste(iotg,[3006,3014],3) ):
            lzbir =  suma_liste(iotg,[3001,3015],3) 
            dzbir =  suma_liste(iotg,[3006,3014],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3001 + 3015) kol. 3 = AOP-u (3006 + 3014) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30019
        if not( suma_liste(iotg,[3001,3015],4) == suma_liste(iotg,[3006,3014],4) ):
            lzbir =  suma_liste(iotg,[3001,3015],4) 
            dzbir =  suma_liste(iotg,[3006,3014],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3001 + 3015) kol. 4 = AOP-u (3006 + 3014) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30020
        if not( aop(iotg,3016,3) == suma(iotg,3017,3019,3) ):
            lzbir =  aop(iotg,3016,3) 
            dzbir =  suma(iotg,3017,3019,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3016 kol. 3 = AOP-u (3017 + 3018 + 3019) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30021
        if not( aop(iotg,3016,4) == suma(iotg,3017,3019,4) ):
            lzbir =  aop(iotg,3016,4) 
            dzbir =  suma(iotg,3017,3019,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3016 kol. 4 = AOP-u (3017 + 3018 + 3019) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30022
        if not( aop(iotg,3020,3) == suma(iotg,3021,3024,3) ):
            lzbir =  aop(iotg,3020,3) 
            dzbir =  suma(iotg,3021,3024,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3020 kol. 3 = AOP-u (3021 + 3022 + 3023 + 3024) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30023
        if not( aop(iotg,3020,4) == suma(iotg,3021,3024,4) ):
            lzbir =  aop(iotg,3020,4) 
            dzbir =  suma(iotg,3021,3024,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3020 kol. 4 = AOP-u (3021 + 3022 + 3023 + 3024) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30024
        if( aop(iotg,3016,3) > aop(iotg,3020,3) ):
            if not( aop(iotg,3025,3) == aop(iotg,3016,3)-aop(iotg,3020,3) ):
                lzbir =  aop(iotg,3025,3) 
                dzbir =  aop(iotg,3016,3)-aop(iotg,3020,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3025 kol. 3 = AOP-u (3016 - 3020) kol. 3, ako je AOP 3016 kol. 3 > AOP-a 3020 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30025
        if( aop(iotg,3016,4) > aop(iotg,3020,4) ):
            if not( aop(iotg,3025,4) == aop(iotg,3016,4)-aop(iotg,3020,4) ):
                lzbir =  aop(iotg,3025,4) 
                dzbir =  aop(iotg,3016,4)-aop(iotg,3020,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3025 kol. 4 = AOP-u (3016 - 3020) kol. 4, ako je AOP 3016 kol. 4 > AOP-a 3020 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30026
        if( aop(iotg,3016,3) < aop(iotg,3020,3) ):
            if not( aop(iotg,3026,3) == aop(iotg,3020,3)-aop(iotg,3016,3) ):
                lzbir =  aop(iotg,3026,3) 
                dzbir =  aop(iotg,3020,3)-aop(iotg,3016,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3026 kol. 3 = AOP-u (3020 - 3016) kol. 3, ako je AOP 3016 kol. 3 < AOP-a 3020 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30027
        if( aop(iotg,3016,4) < aop(iotg,3020,4) ):
            if not( aop(iotg,3026,4) == aop(iotg,3020,4)-aop(iotg,3016,4) ):
                lzbir =  aop(iotg,3026,4) 
                dzbir =  aop(iotg,3020,4)-aop(iotg,3016,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3026 kol. 4 = AOP-u (3020 - 3016) kol. 4, ako je AOP 3016 kol. 4 < AOP-a 3020 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30028
        if( aop(iotg,3016,3) == aop(iotg,3020,3) ):
            if not( suma(iotg,3025,3026,3) == 0 ):
                lzbir =  suma(iotg,3025,3026,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3025 + 3026) kol. 3 = 0, ako je AOP 3016 kol. 3 = AOP-u 3020 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30029
        if( aop(iotg,3016,4) == aop(iotg,3020,4) ):
            if not( suma(iotg,3025,3026,4) == 0 ):
                lzbir =  suma(iotg,3025,3026,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3025 + 3026) kol. 4 = 0, ako je AOP 3016 kol. 4 = AOP-u 3020 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30030
        if( aop(iotg,3025,3) > 0 ):
            if not( aop(iotg,3026,3) == 0 ):
                lzbir =  aop(iotg,3026,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3025 kol. 3 > 0, onda je AOP 3026 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30031
        if( aop(iotg,3026,3) > 0 ):
            if not( aop(iotg,3025,3) == 0 ):
                lzbir =  aop(iotg,3025,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3026 kol. 3 > 0, onda je AOP 3025 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30032
        if( aop(iotg,3025,4) > 0 ):
            if not( aop(iotg,3026,4) == 0 ):
                lzbir =  aop(iotg,3026,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3025 kol. 4 > 0, onda je AOP 3026 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30033
        if( aop(iotg,3026,4) > 0 ):
            if not( aop(iotg,3025,4) == 0 ):
                lzbir =  aop(iotg,3025,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3026 kol. 4 > 0, onda je AOP 3025 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30034
        if not( suma_liste(iotg,[3016,3026],3) == suma_liste(iotg,[3020,3025],3) ):
            lzbir =  suma_liste(iotg,[3016,3026],3) 
            dzbir =  suma_liste(iotg,[3020,3025],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3016 + 3026) kol. 3 = AOP-u (3020 + 3025) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30035
        if not( suma_liste(iotg,[3016,3026],4) == suma_liste(iotg,[3020,3025],4) ):
            lzbir =  suma_liste(iotg,[3016,3026],4) 
            dzbir =  suma_liste(iotg,[3020,3025],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3016 + 3026) kol. 4 = AOP-u (3020 + 3025) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30036
        if( suma_liste(iotg,[3014,3025],3) > suma_liste(iotg,[3015,3026],3) ):
            if not( aop(iotg,3027,3) == suma_liste(iotg,[3014,3025],3)-suma_liste(iotg,[3015,3026],3) ):
                lzbir =  aop(iotg,3027,3) 
                dzbir =  suma_liste(iotg,[3014,3025],3)-suma_liste(iotg,[3015,3026],3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3027 kol. 3 = AOP-u (3014 + 3025 - 3015 - 3026) kol. 3, ako je AOP (3014 + 3025) kol. 3 > AOP-a (3015 + 3026) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30037
        if( suma_liste(iotg,[3014,3025],4) > suma_liste(iotg,[3015,3026],4) ):
            if not( aop(iotg,3027,4) == suma_liste(iotg,[3014,3025],4)-suma_liste(iotg,[3015,3026],4) ):
                lzbir =  aop(iotg,3027,4) 
                dzbir =  suma_liste(iotg,[3014,3025],4)-suma_liste(iotg,[3015,3026],4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3027 kol. 4 = AOP-u (3014 + 3025 - 3015 - 3026) kol. 4, ako je AOP (3014 + 3025) kol. 4 > AOP-a (3015 + 3026) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30038
        if( suma_liste(iotg,[3014,3025],3) < suma_liste(iotg,[3015,3026],3) ):
            if not( aop(iotg,3028,3) == suma_liste(iotg,[3015,3026],3)-suma_liste(iotg,[3014,3025],3) ):
                lzbir =  aop(iotg,3028,3) 
                dzbir =  suma_liste(iotg,[3015,3026],3)-suma_liste(iotg,[3014,3025],3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3028 kol. 3 = AOP-u (3015 + 3026 - 3014 - 3025) kol. 3, ako je AOP (3014 + 3025) kol. 3 < AOP-a (3015 + 3026) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30039
        if( suma_liste(iotg,[3014,3025],4) < suma_liste(iotg,[3015,3026],4) ):
            if not( aop(iotg,3028,4) == suma_liste(iotg,[3015,3026],4)-suma_liste(iotg,[3014,3025],4) ):
                lzbir =  aop(iotg,3028,4) 
                dzbir =  suma_liste(iotg,[3015,3026],4)-suma_liste(iotg,[3014,3025],4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3028 kol. 4 = AOP-u (3015 + 3026 - 3014 - 3025) kol. 4, ako je AOP (3014 + 3025) kol. 4 < AOP-a (3015 + 3026) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30040
        if( suma_liste(iotg,[3014,3025],3) == suma_liste(iotg,[3015,3026],3) ):
            if not( suma(iotg,3027,3028,3) == 0 ):
                lzbir =  suma(iotg,3027,3028,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3027 + 3028) kol. 3 = 0, ako je AOP (3014 + 3025) kol. 3 = AOP-u (3015 + 3026) kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30041
        if( suma_liste(iotg,[3014,3025],4) == suma_liste(iotg,[3015,3026],4) ):
            if not( suma(iotg,3027,3028,4) == 0 ):
                lzbir =  suma(iotg,3027,3028,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3027 + 3028) kol. 4 = 0, ako je AOP (3014 + 3025) kol. 4 = AOP-u (3015 + 3026) kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30042
        if( aop(iotg,3027,3) > 0 ):
            if not( aop(iotg,3028,3) == 0 ):
                lzbir =  aop(iotg,3028,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3027 kol. 3 > 0, onda je AOP 3028 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30043
        if( aop(iotg,3028,3) > 0 ):
            if not( aop(iotg,3027,3) == 0 ):
                lzbir =  aop(iotg,3027,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3028 kol. 3 > 0, onda je AOP 3027 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30044
        if( aop(iotg,3027,4) > 0 ):
            if not( aop(iotg,3028,4) == 0 ):
                lzbir =  aop(iotg,3028,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3027 kol. 4 > 0, onda je AOP 3028 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30045
        if( aop(iotg,3028,4) > 0 ):
            if not( aop(iotg,3027,4) == 0 ):
                lzbir =  aop(iotg,3027,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3028 kol. 4 > 0, onda je AOP 3027 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30046
        if not( suma_liste(iotg,[3014,3025,3028],3) == suma_liste(iotg,[3015,3026,3027],3) ):
            lzbir =  suma_liste(iotg,[3014,3025,3028],3) 
            dzbir =  suma_liste(iotg,[3015,3026,3027],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3014 + 3025 + 3028) kol. 3 = AOP-u (3015 + 3026 + 3027) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30047
        if not( suma_liste(iotg,[3014,3025,3028],4) == suma_liste(iotg,[3015,3026,3027],4) ):
            lzbir =  suma_liste(iotg,[3014,3025,3028],4) 
            dzbir =  suma_liste(iotg,[3015,3026,3027],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3014 + 3025 + 3028) kol. 4 = AOP-u (3015 + 3026 + 3027) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30048
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( aop(iotg,3029,3) == 0 ):
                lzbir =  aop(iotg,3029,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3029 kol. 3 = 0 Novoosnovana pravna lica ne smeju imati prikazan podatak za prethodnu godinu '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30049
        if( suma_liste(iotg,[3027,3029,3030],3) > suma_liste(iotg,[3028,3031],3) ):
            if not( aop(iotg,3032,3) == suma_liste(iotg,[3027,3029,3030],3)-suma_liste(iotg,[3028,3031],3) ):
                lzbir =  aop(iotg,3032,3) 
                dzbir =  suma_liste(iotg,[3027,3029,3030],3)-suma_liste(iotg,[3028,3031],3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3032 kol. 3 = AOP-u (3027 - 3028 + 3029 + 3030 - 3031) kol. 3, ako je AOP (3027 + 3029 + 3030) kol. 3 > AOP-a (3028 + 3031) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30050
        if( suma_liste(iotg,[3027,3029,3030],4) > suma_liste(iotg,[3028,3031],4) ):
            if not( aop(iotg,3032,4) == suma_liste(iotg,[3027,3029,3030],4)-suma_liste(iotg,[3028,3031],4) ):
                lzbir =  aop(iotg,3032,4) 
                dzbir =  suma_liste(iotg,[3027,3029,3030],4)-suma_liste(iotg,[3028,3031],4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3032 kol. 4 = AOP-u (3027 - 3028 + 3029 + 3030 - 3031) kol. 4, ako je AOP (3027 + 3029 + 3030) kol. 4 > AOP-a (3028 + 3031) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30051
        if( suma_liste(iotg,[3027,3029,3030],3) <= suma_liste(iotg,[3028,3031],3) ):
            if not( aop(iotg,3032,3) == 0 ):
                lzbir =  aop(iotg,3032,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3032 kol. 3 = 0, ako je AOP (3027 + 3029 + 3030) kol. 3 ≤ AOP-a (3028 + 3031) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30052
        if( suma_liste(iotg,[3027,3029,3030],4) <= suma_liste(iotg,[3028,3031],4) ):
            if not( aop(iotg,3032,4) == 0 ):
                lzbir =  aop(iotg,3032,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3032 kol. 4 = 0, ako je AOP (3027 + 3029 + 3030) kol. 4 ≤ AOP-a (3028 + 3031) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30053
        if not( aop(iotg,3032,4) == aop(iotg,3029,3) ):
            lzbir =  aop(iotg,3032,4) 
            dzbir =  aop(iotg,3029,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3032 kol. 4 = AOP-u 3029 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30054
        if not( aop(iotg,3032,3) == aop(bs,2,5) ):
            lzbir =  aop(iotg,3032,3) 
            dzbir =  aop(bs,2,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 3032 kol. 3 = AOP-u 0002 kol. 5 bilansa stanja Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3032 kol. 3 = AOP-u 0002 kol. 5 bilansa stanja Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #30055
        if not( aop(iotg,3032,4) == aop(bs,2,6) ):
            lzbir =  aop(iotg,3032,4) 
            dzbir =  aop(bs,2,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 3032 kol. 4 = AOP-u 0002 kol. 6 bilansa stanja Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3032 kol. 4 = AOP-u 0002 kol. 6 bilansa stanja Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #IZVEŠTAJ O PROMENAMA NA KAPITALU - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #40001
        if not( suma(iopk,4019, 4022, 1) +suma(iopk,4041, 4044, 1) +suma(iopk,4063, 4066, 1) +suma(iopk,4085, 4088, 1) +suma(iopk,4107, 4110, 1) +suma(iopk,4129, 4132, 1) +suma(iopk,4151, 4154, 1) +suma(iopk,4173, 4176, 1) +suma(iopk,4195, 4198, 1) +suma(iopk,4217, 4220, 1) +suma(iopk,4239, 4242, 1)  > 0 ):
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='Zbir podataka na oznakama za AOP (4019 do 4022) + (4041 do 4044) + (4063 do 4066) + (4085 do 4088) + (4107 do 4110) + (4129 do 4132) + (4151 do 4154) + (4173 do 4176) + (4195 do 4198) + (4217 do 4220) + (4239 do 4242) > 0 Izveštaj o promenama na kapitalu, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(iopk,4001, 4018, 1) +suma(iopk,4023, 4040, 1) +suma(iopk,4045, 4062, 1) +suma(iopk,4067, 4084, 1) +suma(iopk,4089, 4106, 1) +suma(iopk,4111, 4128, 1) +suma(iopk,4133, 4150, 1) +suma(iopk,4155, 4172, 1) +suma(iopk,4177, 4194, 1) +suma(iopk,4199, 4216, 1) +suma(iopk,4221, 4238, 1)  == 0 ):
                lzbir =  suma(iopk,4001, 4018, 1) +suma(iopk,4023, 4040, 1) +suma(iopk,4045, 4062, 1) +suma(iopk,4067, 4084, 1) +suma(iopk,4089, 4106, 1) +suma(iopk,4111, 4128, 1) +suma(iopk,4133, 4150, 1) +suma(iopk,4155, 4172, 1) +suma(iopk,4177, 4194, 1) +suma(iopk,4199, 4216, 1) +suma(iopk,4221, 4238, 1)  
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Zbir podataka na oznakama za AOP (4001 do 4018) + (4023 do 4040) + (4045 do 4062) + (4067 do 4084) + (4089 do 4106) + (4111 do 4128) + (4133 do 4150) + (4155 do 4172) + (4177 do 4194) + (4199 do 4216) + (4221 do 4238) = 0 Izveštaj o promenama na kapitalu za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(iopk,4001, 4018, 1) +suma(iopk,4023, 4040, 1) +suma(iopk,4045, 4062, 1) +suma(iopk,4067, 4084, 1) +suma(iopk,4089, 4106, 1) +suma(iopk,4111, 4128, 1) +suma(iopk,4133, 4150, 1) +suma(iopk,4155, 4172, 1) +suma(iopk,4177, 4194, 1) +suma(iopk,4199, 4216, 1) +suma(iopk,4221, 4238, 1)  > 0 ):
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Zbir podataka na oznakama za AOP (4001 do 4018) + (4023 do 4040) + (4045 do 4062) + (4067 do 4084) + (4089 do 4106) + (4111 do 4128) + (4133 do 4150) + (4155 do 4172) + (4177 do 4194) + (4199 do 4216) + (4221 do 4238) > 0 Izveštaj o promenama na kapitalu, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
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
            poruka  ='AOP 4155 = 0 Nerealizovani dobici ne mogu imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40068
        if not( aop(iopk,4161,1) == 0 ):
            lzbir =  aop(iopk,4161,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4161 = 0 Nerealizovani dobici ne mogu imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
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
            poruka  ='AOP 4165 = 0 Nerealizovani dobici ne mogu imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
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
            poruka  ='AOP 4171 = 0 Nerealizovani dobici ne mogu imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
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
            poruka  ='AOP 4175 = 0 Nerealizovani dobici ne mogu imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
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
            poruka  ='AOP 4178 = 0 Nerealizovani gubici ne mogu imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
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
            poruka  ='AOP 4184 = 0 Nerealizovani gubici ne mogu imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
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
            poruka  ='AOP 4188 = 0 Nerealizovani gubici ne mogu imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
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
            poruka  ='AOP 4194 = 0 Nerealizovani gubici ne mogu imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
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
            poruka  ='AOP 4198 = 0 Nerealizovani gubici ne mogu imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40085
        if not( aop(iopk,4199,1) == 0 ):
            lzbir =  aop(iopk,4199,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4199 = 0 Ukupni kapital ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40086
        if( suma_liste(iopk,[4002,4024,4046,4068,4090,4112,4134,4156,4178],1) > suma_liste(iopk,[4001,4023,4045,4067,4089,4111,4133,4155,4177],1) ):
            if not( aop(iopk,4200,1) == suma_liste(iopk,[4002,4024,4046,4068,4090,4112,4134,4156,4178],1)-suma_liste(iopk,[4001,4023,4045,4067,4089,4111,4133,4155,4177],1) ):
                lzbir =  aop(iopk,4200,1) 
                dzbir =  suma_liste(iopk,[4002,4024,4046,4068,4090,4112,4134,4156,4178],1)-suma_liste(iopk,[4001,4023,4045,4067,4089,4111,4133,4155,4177],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4200 = AOP-u (4002 + 4024 + 4046 + 4068 + 4090 + 4112 + 4134 + 4156 + 4178 - 4001 - 4023 - 4045 - 4067 - 4089 - 4111 - 4133 - 4155 - 4177), ako je AOP (4002 + 4024 + 4046 + 4068 + 4090 + 4112 + 4134 + 4156 + 4178) > AOP-a (4001 + 4023 + 4045 + 4067 + 4089 + 4111 + 4133 + 4155 + 4177)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40087
        if( suma_liste(iopk,[4002,4024,4046,4068,4090,4112,4134,4156,4178],1) < suma_liste(iopk,[4001,4023,4045,4067,4089,4111,4133,4155,4177],1) ):
            if not( aop(iopk,4221,1) == suma_liste(iopk,[4001,4023,4045,4067,4089,4111,4133,4155,4177],1)-suma_liste(iopk,[4002,4024,4046,4068,4090,4112,4134,4156,4178],1) ):
                lzbir =  aop(iopk,4221,1) 
                dzbir =  suma_liste(iopk,[4001,4023,4045,4067,4089,4111,4133,4155,4177],1)-suma_liste(iopk,[4002,4024,4046,4068,4090,4112,4134,4156,4178],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4221 = AOP-u (4001 + 4023 + 4045 + 4067 + 4089 + 4111 + 4133 + 4155 + 4177 - 4002 - 4024 - 4046 - 4068 - 4090 - 4112 - 4134 - 4156 - 4178), ako je AOP (4002 + 4024 + 4046 + 4068 + 4090 + 4112 + 4134 + 4156 + 4178) < AOP-a (4001 + 4023 + 4045 + 4067 + 4089 + 4111 + 4133 + 4155 + 4177)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40088
        if not( aop(iopk,4222,1) == 0 ):
            lzbir =  aop(iopk,4222,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4222 = 0 Gubitak iznad visine kapitala ne može imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40089
        if( suma_liste(iopk,[4002,4024,4046,4068,4090,4112,4134,4156,4178],1) == suma_liste(iopk,[4001,4023,4045,4067,4089,4111,4133,4155,4177],1) ):
            if not( aop(iopk,4200,1) + aop(iopk,4221,1) == 0 ):
                lzbir =  aop(iopk,4200,1) + aop(iopk,4221,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP (4200 + 4221) = 0, ako je AOP (4002 + 4024 + 4046 + 4068 + 4090 + 4112 + 4134 + 4156 + 4178) = AOP-u (4001 + 4023 + 4045 + 4067 + 4089 + 4111 + 4133 + 4155 + 4177) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40090
        if( aop(iopk,4200,1) > 0 ):
            if not( aop(iopk,4221,1) == 0 ):
                lzbir =  aop(iopk,4221,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4200 > 0 onda je AOP 4221 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40091
        if( aop(iopk,4221,1) > 0 ):
            if not( aop(iopk,4200,1) == 0 ):
                lzbir =  aop(iopk,4200,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4221 > 0 onda je AOP 4200 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40092
        if not( aop(iopk,4201,1) == 0 ):
            lzbir =  aop(iopk,4201,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4201 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40093
        if not( aop(iopk,4202,1) == 0 ):
            lzbir =  aop(iopk,4202,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4202 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40094
        if not( aop(iopk,4203,1) == 0 ):
            lzbir =  aop(iopk,4203,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4203 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40095
        if not( aop(iopk,4204,1) == 0 ):
            lzbir =  aop(iopk,4204,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4204 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40096
        if not( aop(iopk,4223,1) == 0 ):
            lzbir =  aop(iopk,4223,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4223 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40097
        if not( aop(iopk,4224,1) == 0 ):
            lzbir =  aop(iopk,4224,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4224 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40098
        if not( aop(iopk,4225,1) == 0 ):
            lzbir =  aop(iopk,4225,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4225 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40099
        if not( aop(iopk,4226,1) == 0 ):
            lzbir =  aop(iopk,4226,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4226 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40100
        if not( aop(iopk,4205,1) == 0 ):
            lzbir =  aop(iopk,4205,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4205 = 0 Ukupni kapital ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40101
        if( suma_liste(iopk,[4008,4030,4052,4074,4096,4118,4140,4162,4184],1) > suma_liste(iopk,[4007,4029,4051,4073,4095,4117,4139,4161,4183],1) ):
            if not( aop(iopk,4206,1) == suma_liste(iopk,[4008,4030,4052,4074,4096,4118,4140,4162,4184],1)-suma_liste(iopk,[4007,4029,4051,4073,4095,4117,4139,4161,4183],1) ):
                lzbir =  aop(iopk,4206,1) 
                dzbir =  suma_liste(iopk,[4008,4030,4052,4074,4096,4118,4140,4162,4184],1)-suma_liste(iopk,[4007,4029,4051,4073,4095,4117,4139,4161,4183],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4206 = AOP-u (4008 + 4030 + 4052 + 4074 + 4096 + 4118 + 4140 + 4162 + 4184 - 4007 - 4029 - 4051 - 4073 - 4095 - 4117 - 4139 - 4161 - 4183), ako je AOP (4008 + 4030 + 4052 + 4074 + 4096 + 4118 + 4140 + 4162 + 4184) > AOP-a (4007 + 4029 + 4051 + 4073 + 4095 + 4117 + 4139 + 4161 + 4183)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40102
        if( suma_liste(iopk,[4008,4030,4052,4074,4096,4118,4140,4162,4184],1) < suma_liste(iopk,[4007,4029,4051,4073,4095,4117,4139,4161,4183],1) ):
            if not( aop(iopk,4227,1) == suma_liste(iopk,[4007,4029,4051,4073,4095,4117,4139,4161,4183],1)-suma_liste(iopk,[4008,4030,4052,4074,4096,4118,4140,4162,4184],1) ):
                lzbir =  aop(iopk,4227,1) 
                dzbir =  suma_liste(iopk,[4007,4029,4051,4073,4095,4117,4139,4161,4183],1)-suma_liste(iopk,[4008,4030,4052,4074,4096,4118,4140,4162,4184],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4227 = AOP-u (4007 + 4029 + 4051 + 4073 + 4095 + 4117 + 4139 + 4161 + 4183 - 4008 - 4030 - 4052 - 4074 - 4096 - 4118 - 4140 - 4162 - 4184), ako je AOP (4008 + 4030 + 4052 + 4074 + 4096 + 4118 + 4140 + 4162 + 4184) < AOP-a (4007 + 4029 + 4051 + 4073 + 4095 + 4117 + 4139 + 4161 + 4183)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40103
        if not( aop(iopk,4228,1) == 0 ):
            lzbir =  aop(iopk,4228,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4228 = 0 Gubitak iznad visine kapitala ne može imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40104
        if( suma_liste(iopk,[4008,4030,4052,4074,4096,4118,4140,4162,4184],1) == suma_liste(iopk,[4007,4029,4051,4073,4095,4117,4139,4161,4183],1) ):
            if not( aop(iopk,4206,1) + aop(iopk,4227,1) == 0 ):
                lzbir =  aop(iopk,4206,1) + aop(iopk,4227,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP (4206 + 4227) = 0, ako je AOP (4008 + 4030 + 4052 + 4074 + 4096 + 4118 + 4140 + 4162 + 4184) = AOP-u (4007 + 4029 + 4051 + 4073 + 4095 + 4117 + 4139 + 4161 + 4183) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40105
        if( aop(iopk,4206,1) > 0 ):
            if not( aop(iopk,4227,1) == 0 ):
                lzbir =  aop(iopk,4227,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4206 > 0 onda je AOP 4227 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40106
        if( aop(iopk,4227,1) > 0 ):
            if not( aop(iopk,4206,1) == 0 ):
                lzbir =  aop(iopk,4206,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4227 > 0 onda je AOP 4206 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40107
        if not( aop(iopk,4207,1) == 0 ):
            lzbir =  aop(iopk,4207,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4207 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40108
        if not( aop(iopk,4208,1) == 0 ):
            lzbir =  aop(iopk,4208,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4208 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40109
        if not( aop(iopk,4229,1) == 0 ):
            lzbir =  aop(iopk,4229,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4229 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40110
        if not( aop(iopk,4230,1) == 0 ):
            lzbir =  aop(iopk,4230,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4230 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40111
        if not( aop(iopk,4209,1) == 0 ):
            lzbir =  aop(iopk,4209,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4209 = 0 Ukupni kapital ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40112
        if( suma_liste(iopk,[4012,4034,4056,4078,4100,4122,4144,4166,4188],1) > suma_liste(iopk,[4011,4033,4055,4077,4099,4121,4143,4165,4187],1) ):
            if not( aop(iopk,4210,1) == suma_liste(iopk,[4012,4034,4056,4078,4100,4122,4144,4166,4188],1)-suma_liste(iopk,[4011,4033,4055,4077,4099,4121,4143,4165,4187],1) ):
                lzbir =  aop(iopk,4210,1) 
                dzbir =  suma_liste(iopk,[4012,4034,4056,4078,4100,4122,4144,4166,4188],1)-suma_liste(iopk,[4011,4033,4055,4077,4099,4121,4143,4165,4187],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4210 = AOP-u (4012 + 4034 + 4056 + 4078 + 4100 + 4122 + 4144 + 4166 + 4188 - 4011 - 4033 - 4055 - 4077 - 4099 - 4121 - 4143 - 4165 - 4187), ako je AOP (4012 + 4034 + 4056 + 4078 + 4100 + 4122 + 4144 + 4166 + 4188) > AOP-a (4011 + 4033 + 4055 + 4077 + 4099 + 4121 + 4143 + 4165 + 4187)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40113
        if( suma_liste(iopk,[4012,4034,4056,4078,4100,4122,4144,4166,4188],1) < suma_liste(iopk,[4011,4033,4055,4077,4099,4121,4143,4165,4187],1) ):
            if not( aop(iopk,4231,1) == suma_liste(iopk,[4011,4033,4055,4077,4099,4121,4143,4165,4187],1)-suma_liste(iopk,[4012,4034,4056,4078,4100,4122,4144,4166,4188],1) ):
                lzbir =  aop(iopk,4231,1) 
                dzbir =  suma_liste(iopk,[4011,4033,4055,4077,4099,4121,4143,4165,4187],1)-suma_liste(iopk,[4012,4034,4056,4078,4100,4122,4144,4166,4188],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4231 = AOP-u (4011 + 4033 + 4055 + 4077 + 4099 + 4121 + 4143 + 4165 + 4187 - 4012 - 4034 - 4056 - 4078 - 4100 - 4122 - 4144 - 4166 - 4188), ako je AOP (4012 + 4034 + 4056 + 4078 + 4100 + 4122 + 4144 + 4166 + 4188) < AOP-a (4011 + 4033 + 4055 + 4077 + 4099 + 4121 + 4143 + 4165 + 4187)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40114
        if not( aop(iopk,4232,1) == 0 ):
            lzbir =  aop(iopk,4232,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4232 = 0 Gubitak iznad visine kapitala ne može imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40115
        if( suma_liste(iopk,[4012,4034,4056,4078,4100,4122,4144,4166,4188],1) == suma_liste(iopk,[4011,4033,4055,4077,4099,4121,4143,4165,4187],1) ):
            if not( aop(iopk,4210,1) + aop(iopk,4231,1) == 0 ):
                lzbir =  aop(iopk,4210,1) + aop(iopk,4231,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP (4210 + 4231) = 0, ako je AOP (4012 + 4034 + 4056 + 4078 + 4100 + 4122 + 4144 + 4166 + 4188) = AOP-u (4011 + 4033 + 4055 + 4077 + 4099 + 4121 + 4143 + 4165 + 4187) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40116
        if( aop(iopk,4210,1) > 0 ):
            if not( aop(iopk,4231,1) == 0 ):
                lzbir =  aop(iopk,4231,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4210 > 0 onda je AOP 4231 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40117
        if( aop(iopk,4231,1) > 0 ):
            if not( aop(iopk,4210,1) == 0 ):
                lzbir =  aop(iopk,4210,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4231 > 0 onda je AOP 4210 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40118
        if not( aop(iopk,4211,1) == 0 ):
            lzbir =  aop(iopk,4211,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4211 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40119
        if not( aop(iopk,4212,1) == 0 ):
            lzbir =  aop(iopk,4212,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4212 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40120
        if not( aop(iopk,4213,1) == 0 ):
            lzbir =  aop(iopk,4213,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4213 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40121
        if not( aop(iopk,4214,1) == 0 ):
            lzbir =  aop(iopk,4214,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4214 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40122
        if not( aop(iopk,4233,1) == 0 ):
            lzbir =  aop(iopk,4233,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4233 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40123
        if not( aop(iopk,4234,1) == 0 ):
            lzbir =  aop(iopk,4234,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4234 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40124
        if not( aop(iopk,4235,1) == 0 ):
            lzbir =  aop(iopk,4235,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4235 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40125
        if not( aop(iopk,4236,1) == 0 ):
            lzbir =  aop(iopk,4236,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4236 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40126
        if not( aop(iopk,4215,1) == 0 ):
            lzbir =  aop(iopk,4215,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4215 = 0 Ukupni kapital ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40127
        if( suma_liste(iopk,[4018,4040,4062,4084,4106,4128,4150,4172,4194],1) > suma_liste(iopk,[4017,4039,4061,4083,4105,4127,4149,4171,4193],1) ):
            if not( aop(iopk,4216,1) == suma_liste(iopk,[4018,4040,4062,4084,4106,4128,4150,4172,4194],1)-suma_liste(iopk,[4017,4039,4061,4083,4105,4127,4149,4171,4193],1) ):
                lzbir =  aop(iopk,4216,1) 
                dzbir =  suma_liste(iopk,[4018,4040,4062,4084,4106,4128,4150,4172,4194],1)-suma_liste(iopk,[4017,4039,4061,4083,4105,4127,4149,4171,4193],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4216 = AOP-u (4018 + 4040 + 4062 + 4084 + 4106 + 4128 + 4150 + 4172 + 4194 - 4017 - 4039 - 4061 - 4083 - 4105 - 4127 - 4149 - 4171 - 4193), ako je AOP (4018 + 4040 + 4062 + 4084 + 4106 + 4128 + 4150 + 4172 + 4194) > AOP-a (4017 + 4039 + 4061 + 4083 + 4105 + 4127 + 4149 + 4171 + 4193)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40128
        if( suma_liste(iopk,[4018,4040,4062,4084,4106,4128,4150,4172,4194],1) < suma_liste(iopk,[4017,4039,4061,4083,4105,4127,4149,4171,4193],1) ):
            if not( aop(iopk,4237,1) == suma_liste(iopk,[4017,4039,4061,4083,4105,4127,4149,4171,4193,4194],1)-suma_liste(iopk,[4018,4040,4062,4084,4106,4128,4150,4172],1) ):
                lzbir =  aop(iopk,4237,1) 
                dzbir =  suma_liste(iopk,[4017,4039,4061,4083,4105,4127,4149,4171,4193,4194],1)-suma_liste(iopk,[4018,4040,4062,4084,4106,4128,4150,4172],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4237 = AOP-u (4017 + 4039 + 4061 + 4083 + 4105 + 4127 + 4149 + 4171 + 4193 - 4018 - 4040 - 4062 - 4084 - 4106 - 4128 - 4150 - 4172 + 4194), ako je AOP (4018 + 4040 + 4062 + 4084 + 4106 + 4128 + 4150 + 4172 + 4194) < AOP-a (4017 + 4039 + 4061 + 4083 + 4105 + 4127 + 4149 + 4171 + 4193)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40129
        if not( aop(iopk,4238,1) == 0 ):
            lzbir =  aop(iopk,4238,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4238 = 0 Gubitak iznad visine kapitala ne može imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40130
        if( suma_liste(iopk,[4018,4040,4062,4084,4106,4128,4150,4172,4194],1) == suma_liste(iopk,[4017,4039,4061,4083,4105,4127,4149,4171,4193],1) ):
            if not( aop(iopk,4216,1) + aop(iopk,4237,1) == 0 ):
                lzbir =  aop(iopk,4216,1) + aop(iopk,4237,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP (4216 + 4237) = 0, ako je AOP (4018 + 4040 + 4062 + 4084 + 4106 + 4128 + 4150 + 4172 + 4194) = AOP-u (4017 + 4039 + 4061 + 4083 + 4105 + 4127 + 4149 + 4171 + 4193) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40131
        if( aop(iopk,4216,1) > 0 ):
            if not( aop(iopk,4237,1) == 0 ):
                lzbir =  aop(iopk,4237,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4216 > 0 onda je AOP 4237 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40132
        if( aop(iopk,4237,1) > 0 ):
            if not( aop(iopk,4216,1) == 0 ):
                lzbir =  aop(iopk,4216,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4237 > 0 onda je AOP 4216 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40133
        if not( aop(iopk,4217,1) == 0 ):
            lzbir =  aop(iopk,4217,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4217 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40134
        if not( aop(iopk,4218,1) == 0 ):
            lzbir =  aop(iopk,4218,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4218 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40135
        if not( aop(iopk,4239,1) == 0 ):
            lzbir =  aop(iopk,4239,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4239 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40136
        if not( aop(iopk,4240,1) == 0 ):
            lzbir =  aop(iopk,4240,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4240 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40137
        if not( aop(iopk,4219,1) == 0 ):
            lzbir =  aop(iopk,4219,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4219 = 0 Ukupni kapital ne može imati dugovni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40138
        if( suma_liste(iopk,[4022,4044,4066,4088,4110,4132,4154,4176,4198],1) > suma_liste(iopk,[4021,4043,4065,4087,4109,4131,4153,4175,4197],1) ):
            if not( aop(iopk,4220,1) == suma_liste(iopk,[4022,4044,4066,4088,4110,4132,4154,4176,4198],1)-suma_liste(iopk,[4021,4043,4065,4087,4109,4131,4153,4175,4197],1) ):
                lzbir =  aop(iopk,4220,1) 
                dzbir =  suma_liste(iopk,[4022,4044,4066,4088,4110,4132,4154,4176,4198],1)-suma_liste(iopk,[4021,4043,4065,4087,4109,4131,4153,4175,4197],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4220 = AOP-u (4022 + 4044 + 4066 + 4088 + 4110 + 4132 + 4154 + 4176 + 4198 - 4021 - 4043 - 4065 - 4087 - 4109 - 4131 - 4153 - 4175 - 4197), ako je AOP (4022 + 4044 + 4066 + 4088 + 4110 + 4132 + 4154 + 4176 + 4198) > AOP-a (4021 + 4043 + 4065 + 4087 + 4109 + 4131 + 4153 + 4175 + 4197)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40139
        if( suma_liste(iopk,[4022,4044,4066,4088,4110,4132,4154,4176,4198],1) < suma_liste(iopk,[4021,4043,4065,4087,4109,4131,4153,4175,4197],1) ):
            if not( aop(iopk,4241,1) == suma_liste(iopk,[4021,4043,4065,4087,4109,4131,4153,4175,4197],1)-suma_liste(iopk,[4022,4044,4066,4088,4110,4132,4154,4176,4198],1) ):
                lzbir =  aop(iopk,4241,1) 
                dzbir =  suma_liste(iopk,[4021,4043,4065,4087,4109,4131,4153,4175,4197],1)-suma_liste(iopk,[4022,4044,4066,4088,4110,4132,4154,4176,4198],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4241 = AOP-u (4021 + 4043 + 4065 + 4087 + 4109 + 4131 + 4153 + 4175 + 4197 - 4022 - 4044 - 4066 - 4088 - 4110 - 4132 - 4154 - 4176 - 4198), ako je AOP (4022 + 4044 + 4066 + 4088 + 4110 + 4132 + 4154 + 4176 + 4198) < AOP-a (4021 + 4043 + 4065 + 4087 + 4109 + 4131 + 4153 + 4175 + 4197)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40140
        if not( aop(iopk,4242,1) == 0 ):
            lzbir =  aop(iopk,4242,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4242 = 0 Gubitak iznad visine kapitala ne može imati potražni saldo '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40141
        if( suma_liste(iopk,[4022,4044,4066,4088,4110,4132,4154,4176,4198],1) == suma_liste(iopk,[4021,4043,4065,4087,4109,4131,4153,4175,4197],1) ):
            if not( aop(iopk,4220,1) + aop(iopk,4241,1) == 0 ):
                lzbir =  aop(iopk,4220,1) + aop(iopk,4241,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP (4220 + 4241) = 0, ako je AOP (4022 + 4044 + 4066 + 4088 + 4110 + 4132 + 4154 + 4176 + 4198) = AOP-u (4021 + 4043 + 4065 + 4087 + 4109 + 4131 + 4153 + 4175 + 4197) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40142
        if( aop(iopk,4220,1) > 0 ):
            if not( aop(iopk,4241,1) == 0 ):
                lzbir =  aop(iopk,4241,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4220 > 0 onda je AOP 4241 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40143
        if( aop(iopk,4241,1) > 0 ):
            if not( aop(iopk,4220,1) == 0 ):
                lzbir =  aop(iopk,4220,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4241 > 0 onda je AOP 4220 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40144
        if not( aop(iopk,4008,1) == aop(bs,412,7) ):
            lzbir =  aop(iopk,4008,1) 
            dzbir =  aop(bs,412,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4008 = AOP-u 0412 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4008 = AOP-u 0412 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40145
        if not( aop(iopk,4012,1) == aop(bs,412,6) ):
            lzbir =  aop(iopk,4012,1) 
            dzbir =  aop(bs,412,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4012 = AOP-u 0412 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4012 = AOP-u 0412 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40146
        if not( aop(iopk,4022,1) == aop(bs,412,5) ):
            lzbir =  aop(iopk,4022,1) 
            dzbir =  aop(bs,412,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4022 = AOP-u 0412 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4022 = AOP-u 0412 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40147
        if not( aop(iopk,4029,1) == aop(bs,415,7) ):
            lzbir =  aop(iopk,4029,1) 
            dzbir =  aop(bs,415,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4029 = AOP-u 0415 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4029 = AOP-u 0415 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40148
        if not( aop(iopk,4033,1) == aop(bs,415,6) ):
            lzbir =  aop(iopk,4033,1) 
            dzbir =  aop(bs,415,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4033 = AOP-u 0415 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4033 = AOP-u 0415 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40149
        if not( aop(iopk,4043,1) == aop(bs,415,5) ):
            lzbir =  aop(iopk,4043,1) 
            dzbir =  aop(bs,415,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4043 = AOP-u 0415 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4043 = AOP-u 0415 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40150
        if not( aop(iopk,4052,1) == suma(bs,416,417,7) ):
            lzbir =  aop(iopk,4052,1) 
            dzbir =  suma(bs,416,417,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4052 = AOP-u (0416 + 0417) kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4052 = AOP-u (0416 + 0417) kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40151
        if not( aop(iopk,4056,1) == suma(bs,416,417,6) ):
            lzbir =  aop(iopk,4056,1) 
            dzbir =  suma(bs,416,417,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4056 = AOP-u (0416 + 0417) kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4056 = AOP-u (0416 + 0417) kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40152
        if not( aop(iopk,4066,1) == suma(bs,416,417,5) ):
            lzbir =  aop(iopk,4066,1) 
            dzbir =  suma(bs,416,417,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4066 = AOP-u (0416 + 0417) kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4066 = AOP-u (0416 + 0417) kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40153
        if not( aop(iopk,4073,1) == aop(bs,422,7) ):
            lzbir =  aop(iopk,4073,1) 
            dzbir =  aop(bs,422,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4073 = AOP-u 0422 kol. 7  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4073 = AOP-u 0422 kol. 7  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40154
        if not( aop(iopk,4077,1) == aop(bs,422,6) ):
            lzbir =  aop(iopk,4077,1) 
            dzbir =  aop(bs,422,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4077 = AOP-u 0422 kol. 6  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4077 = AOP-u 0422 kol. 6  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40155
        if not( aop(iopk,4087,1) == aop(bs,422,5) ):
            lzbir =  aop(iopk,4087,1) 
            dzbir =  aop(bs,422,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4087 = AOP-u 0422 kol. 5  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4087 = AOP-u 0422 kol. 5  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40156
        if not( aop(iopk,4095,1) == aop(bs,423,7) ):
            lzbir =  aop(iopk,4095,1) 
            dzbir =  aop(bs,423,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4095 = AOP-u 0423 kol. 7  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4095 = AOP-u 0423 kol. 7  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40157
        if not( aop(iopk,4099,1) == aop(bs,423,6) ):
            lzbir =  aop(iopk,4099,1) 
            dzbir =  aop(bs,423,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4099 = AOP-u 0423 kol. 6  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4099 = AOP-u 0423 kol. 6  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40158
        if not( aop(iopk,4109,1) == aop(bs,423,5) ):
            lzbir =  aop(iopk,4109,1) 
            dzbir =  aop(bs,423,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4109 = AOP-u 0423 kol. 5  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4109 = AOP-u 0423 kol. 5  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40159
        if not( aop(iopk,4118,1) == aop(bs,421,7) ):
            lzbir =  aop(iopk,4118,1) 
            dzbir =  aop(bs,421,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4118 = AOP-u 0421 kol. 7  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4118 = AOP-u 0421 kol. 7  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40160
        if not( aop(iopk,4122,1) == aop(bs,421,6) ):
            lzbir =  aop(iopk,4122,1) 
            dzbir =  aop(bs,421,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4122 = AOP-u 0421 kol. 6  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4122 = AOP-u 0421 kol. 6  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40161
        if not( aop(iopk,4132,1) == aop(bs,421,5) ):
            lzbir =  aop(iopk,4132,1) 
            dzbir =  aop(bs,421,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4132 = AOP-u 0421 kol. 5  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4132 = AOP-u 0421 kol. 5  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40162
        if not( aop(iopk,4140,1) == aop(bs,418,7) ):
            lzbir =  aop(iopk,4140,1) 
            dzbir =  aop(bs,418,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4140 = AOP-u 0418 kol. 7  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4140 = AOP-u 0418 kol. 7  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40163
        if not( aop(iopk,4144,1) == aop(bs,418,6) ):
            lzbir =  aop(iopk,4144,1) 
            dzbir =  aop(bs,418,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4144 = AOP-u 0418 kol. 6  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4144 = AOP-u 0418 kol. 6  bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40164
        if not( aop(iopk,4154,1) == aop(bs,418,5) ):
            lzbir =  aop(iopk,4154,1) 
            dzbir =  aop(bs,418,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4154 = AOP-u 0418 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4154 = AOP-u 0418 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40165
        if not( aop(iopk,4162,1) == aop(bs,419,7) ):
            lzbir =  aop(iopk,4162,1) 
            dzbir =  aop(bs,419,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4162 = AOP-u 0419 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4162 = AOP-u 0419 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40166
        if not( aop(iopk,4166,1) == aop(bs,419,6) ):
            lzbir =  aop(iopk,4166,1) 
            dzbir =  aop(bs,419,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4166 = AOP-u 0419 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4166 = AOP-u 0419 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40167
        if not( aop(iopk,4176,1) == aop(bs,419,5) ):
            lzbir =  aop(iopk,4176,1) 
            dzbir =  aop(bs,419,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4176 = AOP-u 0419 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4176 = AOP-u 0419 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40168
        if not( aop(iopk,4183,1) == aop(bs,420,7) ):
            lzbir =  aop(iopk,4183,1) 
            dzbir =  aop(bs,420,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4183 = AOP-u 0420 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4183 = AOP-u 0420 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40169
        if not( aop(iopk,4187,1) == aop(bs,420,6) ):
            lzbir =  aop(iopk,4187,1) 
            dzbir =  aop(bs,420,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4187 = AOP-u 0420 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4187 = AOP-u 0420 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40170
        if not( aop(iopk,4197,1) == aop(bs,420,5) ):
            lzbir =  aop(iopk,4197,1) 
            dzbir =  aop(bs,420,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4197 = AOP-u 0420 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4197 = AOP-u 0420 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40171
        if not( aop(iopk,4206,1) == aop(bs,411,7) ):
            lzbir =  aop(iopk,4206,1) 
            dzbir =  aop(bs,411,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4206 = AOP-u 0411 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4206 = AOP-u 0411 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40172
        if not( aop(iopk,4210,1) == aop(bs,411,6) ):
            lzbir =  aop(iopk,4210,1) 
            dzbir =  aop(bs,411,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4210 = AOP-u 0411 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4210 = AOP-u 0411 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40173
        if not( aop(iopk,4220,1) == aop(bs,411,5) ):
            lzbir =  aop(iopk,4220,1) 
            dzbir =  aop(bs,411,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4220 = AOP-u 0411 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4220 = AOP-u 0411 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40174
        if not( aop(iopk,4227,1) == aop(bs,424,7) ):
            lzbir =  aop(iopk,4227,1) 
            dzbir =  aop(bs,424,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4227 = AOP-u 0424 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4227 = AOP-u 0424 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40175
        if not( aop(iopk,4231,1) == aop(bs,424,6) ):
            lzbir =  aop(iopk,4231,1) 
            dzbir =  aop(bs,424,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4231 = AOP-u 0424 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4231 = AOP-u 0424 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40176
        if not( aop(iopk,4241,1) == aop(bs,424,5) ):
            lzbir =  aop(iopk,4241,1) 
            dzbir =  aop(bs,424,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4241 = AOP-u 0424 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4241 = AOP-u 0424 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #STATISTIČKI IZVEŠTAJ - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #90001
        if not( suma(si,9005,9032,4) > 0 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir podataka na oznakama za AOP (9005 do 9032) kol. 4 > 0 Statistički izveštaj, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90002
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(si,9005,9032,5) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Zbir podataka na oznakama za AOP (9005 do 9032) kol. 5 > 0 Statistički izveštaj, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90003
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(si,9001,9004,4)+suma(si,9005,9032,5) == 0 ):
                lzbir =  suma(si,9001,9004,4)+suma(si,9005,9032,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Zbir podataka na oznakama za AOP (9001 do 9004) kol. 4 + (9005 do 9032) kol. 5 = 0 Statistički izveštaj za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #90004
        if not( 1 <= aop(si,9001,3) and aop(si,9001,3) <= 12 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='1 ≤ AOP-a 9001 kol. 3 ≤ 12  Broj meseci poslovanja obveznika mora biti iskazan u intervalu između 1 i 12; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90005
        if not( 1 <= aop(si,9001,4) and aop(si,9001,4) <= 12 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='1 ≤ AOP-a 9001 kol. 4 ≤ 12  Broj meseci poslovanja obveznika osnovanih u ranijim godinama po pravilu mora biti iskazan u intervalu između 1 i 12; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90006
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( aop(si,9001,3) == 12 ):
                lzbir =  aop(si,9001,3) 
                dzbir =  12 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='AOP 9001 kol. 3 = 12 Broj meseci poslovanja obveznika osnovanih ranijih godina, po pravilu, mora biti 12 '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90007
        if not( aop(si,9003,3) <= aop(si,9002,3) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9003 kol. 3 ≤ AOP-a 9002 kol. 3  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90008
        if not( aop(si,9003,4) <= aop(si,9002,4) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9003 kol. 4 ≤ AOP-a 9002 kol. 4  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90009
        if( aop(si,9002,3) > 0 ):
            if not( suma_liste(si,[9006,9013],4) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP 9002 kol. 3 > 0, onda je AOP (9006 + 9013) kol. 4 > 0 Ukoliko u kapitalu učestvuju strana lica, mora biti iskazana vrednost stranog kapitala, ako je veća od 500,00 RSD; Ukoliko podaci o vrednosti kapitala nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje da je vrednost tog kapitala manja od 500,00 RSD '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90010
        if( suma_liste(si,[9006,9013],4) > 0 ):
            if not( aop(si,9002,3) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP (9006 + 9013) kol. 4 > 0, onda je AOP 9002 kol. 3 > 0 Ukoliko je iskazana vrednost stranog kapitala, obveznik mora iskazati broj stranih lica koja učestvuju u kapitalu; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #90011
        if( aop(si,9002,4) > 0 ):
            if not( suma_liste(si,[9006,9013],5) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP 9002 kol. 4 > 0, onda je AOP (9006 + 9013) kol. 5 > 0 Ukoliko u kapitalu učestvuju strana lica, mora biti iskazana vrednost stranog kapitala, ako je veća od 500,00 RSD; Ukoliko podaci o vrednosti kapitala nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje da je vrednost tog kapitala manja od 500,00 RSD '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90012
        if( suma_liste(si,[9006,9013],5) > 0 ):
            if not( aop(si,9002,4) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP (9006 + 9013) kol. 5 > 0, onda je AOP 9002 kol. 4 > 0 Ukoliko je iskazana vrednost stranog kapitala, obveznik mora iskazati broj stranih lica koja učestvuju u kapitalu; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #90013
        if( aop(si,9004,3) > 0 ):
            if not( aop(si,9017,4) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP 9004 kol. 3 > 0, onda je AOP 9017 kol. 4 > 0 Ukoliko je iskazan prosečan broj zaposlenih, obveznik, po pravilu, mora imati iskazane obaveze po osnovu neto zarada; Ukoliko jedan od navedenih podataka nije prikazan, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90014
        if( aop(si,9017,4) > 0 ):
            if not( aop(si,9004,3) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP 9017 kol. 4 > 0, onda je AOP 9004 kol. 3 > 0 Ukoliko su iskazane obaveze po osnovu bruto zarada, obveznik, po pravilu, mora imati iskazan prosečan broj zaposlenih; Ukoliko jedan od navedenih podataka nije prikazan, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90015
        if( aop(si,9004,4) > 0 ):
            if not( aop(si,9017,5) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP 9004 kol. 4 > 0, onda je AOP 9017 kol. 5 > 0 Ukoliko je iskazan prosečan broj zaposlenih, obveznik, po pravilu, mora imati iskazane obaveze po osnovu neto zarada; Ukoliko jedan od navedenih podataka nije prikazan, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90016
        if( aop(si,9017,5) > 0 ):
            if not( aop(si,9004,4) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP 9017 kol. 5 > 0, onda je AOP 9004 kol. 4 > 0 Ukoliko su iskazane obaveze po osnovu bruto zarada, obveznik, po pravilu, mora imati iskazan prosečan broj zaposlenih; Ukoliko jedan od navedenih podataka nije prikazan, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90017
        if not( aop(si,9004,3) > 0 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9004 kol. 3 > 0 Na poziciji Prosečan broj zaposlenih nije iskazan podatak; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90018
        if not( aop(si,9004,3) <= 50 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9004 kol. 3 ≤ 50 Granične vrednosti date su da bi se izbegle slučajne greške prilikom iskazivanja broja zaposlenih;Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90019
        if not( aop(si,9004,4) <= 50 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9004 kol. 4 ≤ 50 Granične vrednosti date su da bi se izbegle slučajne greške prilikom iskazivanja broja zaposlenih;Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90020
        if not( aop(si,9006,4) <= aop(si,9005,4) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9006 kol. 4 ≤ AOP-a 9005 kol. 4  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90021
        if not( aop(si,9006,5) <= aop(si,9005,5) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9006 kol. 5 ≤ AOP-a 9005 kol. 5  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90022
        if( aop(si,9007,4) > 0 ):
            if not( aop(si,9008,4) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP 9007 kol. 4 > 0, onda je AOP 9008 kol. 4 > 0 Ako je prikazan broj akcija , mora biti prikazana i vrednost akcija '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #90023
        if( aop(si,9008,4) > 0 ):
            if not( aop(si,9007,4) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP 9008 kol. 4 > 0, onda je AOP 9007 kol. 4 > 0 Ako je prikazana vrednost akcija, mora biti prikazan broj akcija '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #90024
        if( aop(si,9007,5) > 0 ):
            if not( aop(si,9008,5) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP 9007 kol. 5 > 0, onda je AOP 9008 kol. 5 > 0 Ako je prikazan broj akcija , mora biti prikazana i vrednost akcija '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #90025
        if( aop(si,9008,5) > 0 ):
            if not( aop(si,9007,5) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP 9008 kol. 5 > 0, onda je AOP 9007 kol. 5 > 0 Ako je prikazana vrednost akcija, mora biti prikazan broj akcija '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #90026
        if( aop(si,9009,4) > 0 ):
            if not( aop(si,9010,4) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP 9009 kol. 4 > 0, onda je AOP 9010 kol. 4 > 0 Ako je prikazan broj akcija , mora biti prikazana i vrednost akcija '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #90027
        if( aop(si,9010,4) > 0 ):
            if not( aop(si,9009,4) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP 9010 kol. 4 > 0, onda je AOP 9009 kol. 4 > 0 Ako je prikazana vrednost akcija, mora biti prikazan broj akcija '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #90028
        if( aop(si,9009,5) > 0 ):
            if not( aop(si,9010,5) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP 9009 kol. 5 > 0, onda je AOP 9010 kol. 5 > 0 Ako je prikazan broj akcija , mora biti prikazana i vrednost akcija '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #90029
        if( aop(si,9010,5) > 0 ):
            if not( aop(si,9009,5) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP 9010 kol. 5 > 0, onda je AOP 9009 kol. 5 > 0 Ako je prikazana vrednost akcija, mora biti prikazan broj akcija '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #90030
        if not( aop(si,9011,4) == suma_liste(si,[9008,9010],4) ):
            lzbir =  aop(si,9011,4) 
            dzbir =  suma_liste(si,[9008,9010],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9011 kol. 4 = AOP-u (9008 + 9010) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90031
        if not( aop(si,9011,5) == suma_liste(si,[9008,9010],5) ):
            lzbir =  aop(si,9011,5) 
            dzbir =  suma_liste(si,[9008,9010],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9011 kol. 5 = AOP-u (9008 + 9010) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90032
        if not( aop(si,9011,4) == aop(si,9005,4) ):
            lzbir =  aop(si,9011,4) 
            dzbir =  aop(si,9005,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9011 kol. 4 = AOP-u 9005 kol. 4 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90033
        if not( aop(si,9011,5) == aop(si,9005,5) ):
            lzbir =  aop(si,9011,5) 
            dzbir =  aop(si,9005,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9011 kol. 5 = AOP-u 9005 kol. 5 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90034
        if not( aop(si,9013,4) <= aop(si,9012,4) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9013 kol. 4 ≤ AOP-a 9012 kol. 4  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90035
        if not( aop(si,9013,5) <= aop(si,9012,5) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9013 kol. 5 ≤ AOP-a 9012 kol. 5  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90036
        if not( aop(si,9005,4) == aop(bs,413,5) ):
            lzbir =  aop(si,9005,4) 
            dzbir =  aop(bs,413,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9005 kol. 4 = AOP-u 0413 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9005 kol. 4 = AOP-u 0413 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90037
        if not( aop(si,9005,5) == aop(bs,413,6) ):
            lzbir =  aop(si,9005,5) 
            dzbir =  aop(bs,413,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9005 kol. 5 = AOP-u 0413 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9005 kol. 5 = AOP-u 0413 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90038
        if not( aop(si,9012,4) == aop(bs,414,5) ):
            lzbir =  aop(si,9012,4) 
            dzbir =  aop(bs,414,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9012 kol. 4 = AOP-u 0414 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9012 kol. 4 = AOP-u 0414 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90039
        if not( aop(si,9012,5) == aop(bs,414,6) ):
            lzbir =  aop(si,9012,5) 
            dzbir =  aop(bs,414,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9012 kol. 5 = AOP-u 0414 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9012 kol. 5 = AOP-u 0414 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90040
        if not( suma_liste(si,[9005,9012],4) == aop(bs,412,5) ):
            lzbir =  suma_liste(si,[9005,9012],4) 
            dzbir =  aop(bs,412,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP (9005 + 9012) kol. 4 = AOP-u 0412 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP (9005 + 9012) kol. 4 = AOP-u 0412 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90041
        if not( suma_liste(si,[9005,9012],5) == aop(bs,412,6) ):
            lzbir =  suma_liste(si,[9005,9012],5) 
            dzbir =  aop(bs,412,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP (9005 + 9012) kol. 5 = AOP-u 0412 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP (9005 + 9012) kol. 5 = AOP-u 0412 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90042
        if not( aop(si,9018,4) == suma(si,9014,9017,4) ):
            lzbir =  aop(si,9018,4) 
            dzbir =  suma(si,9014,9017,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9018 kol. 4 = AOP-u (9014 + 9015 + 9016 + 9017) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90043
        if not( aop(si,9018,5) == suma(si,9014,9017,5) ):
            lzbir =  aop(si,9018,5) 
            dzbir =  suma(si,9014,9017,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9018 kol. 5 = AOP-u (9014 + 9015 + 9016 + 9017) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90044
        if not( aop(si,9026,4) == suma(si,9019,9025,4) ):
            lzbir =  aop(si,9026,4) 
            dzbir =  suma(si,9019,9025,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9026 kol. 4 = AOP-u (9019 + 9020 + 9021 + 9022 + 9023 + 9024 + 9025) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90045
        if not( aop(si,9026,5) == suma(si,9019,9025,5) ):
            lzbir =  aop(si,9026,5) 
            dzbir =  suma(si,9019,9025,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9026 kol. 5 = AOP-u (9019 + 9020 + 9021 + 9022 + 9023 + 9024 + 9025) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90046
        if not( suma_liste(si,[9019,9020,9021,9022,9024,9025],4) <= aop(bu,1025,5) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (9019 + 9020 + 9021 + 9022 + 9024 + 9025) kol. 4 ≤ AOP-a 1025 kol. 5 bilansa uspeha  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP (9019 + 9020 + 9021 + 9022 + 9024 + 9025) kol. 4 ≤ AOP-a 1025 kol. 5 bilansa uspeha  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90047
        if not( suma_liste(si,[9019,9020,9021,9022,9024,9025],5) <= aop(bu,1025,6) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (9019 + 9020 + 9021 + 9022 + 9024 + 9025) kol. 5 ≤ AOP-a 1025 kol. 6 bilansa uspeha  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP (9019 + 9020 + 9021 + 9022 + 9024 + 9025) kol. 5 ≤ AOP-a 1025 kol. 6 bilansa uspeha  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90048
        if not( aop(si,9023,4) == aop(bu,1020,5) ):
            lzbir =  aop(si,9023,4) 
            dzbir =  aop(bu,1020,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9023 kol. 4 = AOP-a 1020 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9023 kol. 4 = AOP-a 1020 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90049
        if not( aop(si,9023,5) == aop(bu,1020,6) ):
            lzbir =  aop(si,9023,5) 
            dzbir =  aop(bu,1020,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9023 kol. 5 = AOP-a 1020 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9023 kol. 5 = AOP-a 1020 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90050
        if not( aop(si,9032,4) == suma(si,9027,9031,4) ):
            lzbir =  aop(si,9032,4) 
            dzbir =  suma(si,9027,9031,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9032 kol. 4 = AOP-u (9027 + 9028 + 9029 + 9030 + 9031) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90051
        if not( aop(si,9032,5) == suma(si,9027,9031,5) ):
            lzbir =  aop(si,9032,5) 
            dzbir =  suma(si,9027,9031,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9032 kol. 5 = AOP-u (9027 + 9028 + 9029 + 9030 + 9031) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90052
        if not( suma(si,9027,9028,4) <= aop(bu,1002,5) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (9027 + 9028) kol. 4 ≤ AOP-a 1002 kol. 5 bilansa uspeha Prihodi od kamata na depozite i od kamata na hartije od vrednosti su izdvojeni deo prihoda od kamata '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP (9027 + 9028) kol. 4 ≤ AOP-a 1002 kol. 5 bilansa uspeha Prihodi od kamata na depozite i od kamata na hartije od vrednosti su izdvojeni deo prihoda od kamata '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90053
        if not( suma(si,9027,9028,5) <= aop(bu,1002,6) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (9027 + 9028) kol. 5 ≤ AOP-a 1002 kol. 6 bilansa uspeha Prihodi od kamata na depozite i od kamata na hartije od vrednosti su izdvojeni deo prihoda od kamata '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP (9027 + 9028) kol. 5 ≤ AOP-a 1002 kol. 6 bilansa uspeha Prihodi od kamata na depozite i od kamata na hartije od vrednosti su izdvojeni deo prihoda od kamata '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90054
        if not( suma(si,9029,9031,4) <= aop(bu,1008,5) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (9029 + 9030 + 9031) kol. 4 ≤ AOP-a 1008 kol. 5 bilansa uspeha Prihodi od naknada šteta od društava za osiguranje, povraćaja poreskih dažbina i po osnovu donacija su izdvojeni deo ostalih poslovnih prihoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP (9029 + 9030 + 9031) kol. 4 ≤ AOP-a 1008 kol. 5 bilansa uspeha Prihodi od naknada šteta od društava za osiguranje, povraćaja poreskih dažbina i po osnovu donacija su izdvojeni deo ostalih poslovnih prihoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90055
        if not( suma(si,9029,9031,5) <= aop(bu,1008,6) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (9029 + 9030 + 9031) kol. 5 ≤ AOP-a 1008 kol. 6 bilansa uspeha Prihodi od naknada šteta od društava za osiguranje, povraćaja poreskih dažbina i po osnovu donacija su izdvojeni deo ostalih poslovnih prihoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP (9029 + 9030 + 9031) kol. 5 ≤ AOP-a 1008 kol. 6 bilansa uspeha Prihodi od naknada šteta od društava za osiguranje, povraćaja poreskih dažbina i po osnovu donacija su izdvojeni deo ostalih poslovnih prihoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #POSEBNI PODACI - NEMA
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

