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

#LISTA NEGATIVNIH PO IOPK OBRASCU - Nova funkcija koja proverava da li u iopk obrascu ima negativnih izuzev onih iz dozvoljene liste
def find_negativni_iopk(aop_dict, prvi_aop, poslednji_aop,lista_dozvoljenih, prva_kolona, poslednja_kolona): 
    aopi = ""
    for aop_broj in range (prvi_aop,poslednji_aop+1):
        for kolona in range (prva_kolona,poslednja_kolona+1):
                aop_key = broj_u_aop(aop_broj, kolona)
                if aop_key in aop_dict:
                    a=aop_dict[aop_key]       
                    if not (a is None):                        
                        if (a < 0 and aop_broj not in lista_dozvoljenih) :
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

        pp= getForme(Zahtev,'Posebni podaci')
        if len(pp)==0:
            
            naziv_obrasca='Posebni podaci'
            poruka  ='Obrazac Posebni podaci nije popunjen'
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
        if not( suma(bs,1,60,5)+suma(bs,1,60,6)+suma(bs,1,60,7)+suma(bs,401,457,5)+suma(bs,401,457,6)+suma(bs,401,457,7)+suma(bu,1001,1062,5)+suma(bu,1001,1062,6)+suma(ioor,2001,2029,5)+suma(ioor,2001,2029,6)+suma(iotg,3001,3055,3)+suma(iotg,3001,3055,4)+suma(iopk,4001,4090,1)+suma_liste(si,[9008,9015,9016,9022,9023,9030,9031,9037],6)+suma(si,9038,9062,4)+suma(si,9038,9062,5)+suma(si,9063,9071,3)+suma(si,9063,9071,4)+suma(si,9072,9118,4)+suma(si,9072,9118,5)+suma(si,9119,9126,3)+suma(si,9119,9126,4)+suma(si,9127,9136,6) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0060) kol. 5 + (0001 do 0060) kol. 6 + (0001 do 0060) kol. 7 bilansa stanja + (0401 do 0457) kol. 5 + (0401 do 0457) kol. 6 + (0401 do 0457) kol. 7 bilansa stanja + (1001 do 1062) kol. 5 + (1001 do 1062) kol. 6 bilansa uspeha + (2001 do 2029) kol. 5 + (2001 do 2029) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3055) kol. 3 + (3001 do 3055) kol. 4 izveštaja o tokovima gotovine + (4001 do 4090) izveštaja o promenama na kapitalu  + (9008 + 9015 + 9016 + 9022 + 9023 + 9030 + 9031 + 9037) kol. 6 + (9038 do 9062) kol.4  + (9038 do 9062) kol.5 + (9063 do 9071) kol.3  + (9063 do 9071) kol.4 + (9072 do 9118) kol.4 + (9072 do 9118) kol.5 + (9119 do 9126) kol.3 + (9119 do 9126) kol.4 + (9127 до 9136) kol. 6 statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0060) kol. 5 + (0001 do 0060) kol. 6 + (0001 do 0060) kol. 7 bilansa stanja + (0401 do 0457) kol. 5 + (0401 do 0457) kol. 6 + (0401 do 0457) kol. 7 bilansa stanja + (1001 do 1062) kol. 5 + (1001 do 1062) kol. 6 bilansa uspeha + (2001 do 2029) kol. 5 + (2001 do 2029) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3055) kol. 3 + (3001 do 3055) kol. 4 izveštaja o tokovima gotovine + (4001 do 4090) izveštaja o promenama na kapitalu  + (9008 + 9015 + 9016 + 9022 + 9023 + 9030 + 9031 + 9037) kol. 6 + (9038 do 9062) kol.4  + (9038 do 9062) kol.5 + (9063 do 9071) kol.3  + (9063 do 9071) kol.4 + (9072 do 9118) kol.4 + (9072 do 9118) kol.5 + (9119 do 9126) kol.3 + (9119 do 9126) kol.4 + (9127 до 9136) kol. 6 statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0060) kol. 5 + (0001 do 0060) kol. 6 + (0001 do 0060) kol. 7 bilansa stanja + (0401 do 0457) kol. 5 + (0401 do 0457) kol. 6 + (0401 do 0457) kol. 7 bilansa stanja + (1001 do 1062) kol. 5 + (1001 do 1062) kol. 6 bilansa uspeha + (2001 do 2029) kol. 5 + (2001 do 2029) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3055) kol. 3 + (3001 do 3055) kol. 4 izveštaja o tokovima gotovine + (4001 do 4090) izveštaja o promenama na kapitalu  + (9008 + 9015 + 9016 + 9022 + 9023 + 9030 + 9031 + 9037) kol. 6 + (9038 do 9062) kol.4  + (9038 do 9062) kol.5 + (9063 do 9071) kol.3  + (9063 do 9071) kol.4 + (9072 do 9118) kol.4 + (9072 do 9118) kol.5 + (9119 do 9126) kol.3 + (9119 do 9126) kol.4 + (9127 до 9136) kol. 6 statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0060) kol. 5 + (0001 do 0060) kol. 6 + (0001 do 0060) kol. 7 bilansa stanja + (0401 do 0457) kol. 5 + (0401 do 0457) kol. 6 + (0401 do 0457) kol. 7 bilansa stanja + (1001 do 1062) kol. 5 + (1001 do 1062) kol. 6 bilansa uspeha + (2001 do 2029) kol. 5 + (2001 do 2029) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3055) kol. 3 + (3001 do 3055) kol. 4 izveštaja o tokovima gotovine + (4001 do 4090) izveštaja o promenama na kapitalu  + (9008 + 9015 + 9016 + 9022 + 9023 + 9030 + 9031 + 9037) kol. 6 + (9038 do 9062) kol.4  + (9038 do 9062) kol.5 + (9063 do 9071) kol.3  + (9063 do 9071) kol.4 + (9072 do 9118) kol.4 + (9072 do 9118) kol.5 + (9119 do 9126) kol.3 + (9119 do 9126) kol.4 + (9127 до 9136) kol. 6 statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0060) kol. 5 + (0001 do 0060) kol. 6 + (0001 do 0060) kol. 7 bilansa stanja + (0401 do 0457) kol. 5 + (0401 do 0457) kol. 6 + (0401 do 0457) kol. 7 bilansa stanja + (1001 do 1062) kol. 5 + (1001 do 1062) kol. 6 bilansa uspeha + (2001 do 2029) kol. 5 + (2001 do 2029) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3055) kol. 3 + (3001 do 3055) kol. 4 izveštaja o tokovima gotovine + (4001 do 4090) izveštaja o promenama na kapitalu  + (9008 + 9015 + 9016 + 9022 + 9023 + 9030 + 9031 + 9037) kol. 6 + (9038 do 9062) kol.4  + (9038 do 9062) kol.5 + (9063 do 9071) kol.3  + (9063 do 9071) kol.4 + (9072 do 9118) kol.4 + (9072 do 9118) kol.5 + (9119 do 9126) kol.3 + (9119 do 9126) kol.4 + (9127 до 9136) kol. 6 statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0060) kol. 5 + (0001 do 0060) kol. 6 + (0001 do 0060) kol. 7 bilansa stanja + (0401 do 0457) kol. 5 + (0401 do 0457) kol. 6 + (0401 do 0457) kol. 7 bilansa stanja + (1001 do 1062) kol. 5 + (1001 do 1062) kol. 6 bilansa uspeha + (2001 do 2029) kol. 5 + (2001 do 2029) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3055) kol. 3 + (3001 do 3055) kol. 4 izveštaja o tokovima gotovine + (4001 do 4090) izveštaja o promenama na kapitalu  + (9008 + 9015 + 9016 + 9022 + 9023 + 9030 + 9031 + 9037) kol. 6 + (9038 do 9062) kol.4  + (9038 do 9062) kol.5 + (9063 do 9071) kol.3  + (9063 do 9071) kol.4 + (9072 do 9118) kol.4 + (9072 do 9118) kol.5 + (9119 do 9126) kol.3 + (9119 do 9126) kol.4 + (9127 до 9136) kol. 6 statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka; '
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
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-6
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-7
        # U bar jednoj od tri navedene forme kolona napomena mora da ima bar jedan karakter
        bsNapomene = Zahtev.Forme['Bilans stanja'].TekstualnaPoljaForme;
        buNapomene = Zahtev.Forme['Bilans uspeha'].TekstualnaPoljaForme;
        ioorNapomene = Zahtev.Forme['Izveštaj o ostalom rezultatu'].TekstualnaPoljaForme;

        if not (proveriNapomene(bsNapomene, 1, 60, 4) or proveriNapomene(bsNapomene, 401, 457, 4) or proveriNapomene(buNapomene, 1001, 1062, 4) or proveriNapomene(ioorNapomene, 2001, 2029, 4) ):  
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Na AOP-u (0001 do 0060) bilansa stanja + (0401 do 0457) bilansa stanja + (1001 do 1062) bilansa uspeha + (2001 do 2029) izveštaja o ostalom rezultatu u koloni 4 (Napomena broj) mora biti unet bar jedan karakter; Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ='Na AOP-u (0001 do 0060) bilansa stanja + (0401 do 0457) bilansa stanja + (1001 do 1062) bilansa uspeha + (2001 do 2029) izveštaja o ostalom rezultatu u koloni 4 (Napomena broj) mora biti unet bar jedan karakter; Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='Na AOP-u (0001 do 0060) bilansa stanja + (0401 do 0457) bilansa stanja + (1001 do 1062) bilansa uspeha + (2001 do 2029) izveštaja o ostalom rezultatu u koloni 4 (Napomena broj) mora biti unet bar jedan karakter; Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #Provera da li je fizahtev placen
        if not(Zahtev.Placen):
            ostalo_errors.append('Naknada za obradu i javno objavljivanje izveštaja i propisane dokumentacije nije uplaćena u propisanom iznosu. Instrukcije za uplatu propisane naknade date su u okviru PIS FI sistema za konkretan zahtev, na linku „Status naplate zahteva / Instrukcija za plaćanje". Ukoliko ste izvršili uplatu, a naknada nije uparena, priložite Dokaz o uplati naknade u delu Dokumentacija (na mestu predviđenom za dokaz o uplati naknade), kako biste mogli da podnesete izveštaj.');

        
        #Provera negativnih AOP-a
        #lista dozvoljenih negativnih aopa u iopk obrascu
        lista_dozvoljenih = [4002, 4004, 4006, 4008, 4011, 4013, 4015, 4017, 4020, 4022, 4024, 4026, 4029, 4031, 4033, 4035, 4037, 4038, 4039, 4040, 4041, 4042, 4043, 4044, 4045, 4047, 4049, 4051,4053, 4056, 4058, 4060, 4062, 4065, 4067, 4069, 4071, 4074, 4076, 4078, 4080, 4083, 4085, 4087, 4089]
        lista=""
        lista_bs = find_negativni(bs, 1, 457, 5, 7)
        lista_bu = find_negativni(bu, 1001, 1062, 5, 6)
        lista_ioor = find_negativni(ioor, 2001, 2029, 5, 6)
        lista_iotg = find_negativni(iotg, 3001, 3055, 3, 4)
        lista_iopk = find_negativni_iopk(aop_dict= iopk, prvi_aop=4001, poslednji_aop=4090, lista_dozvoljenih= lista_dozvoljenih, prva_kolona=1, poslednja_kolona=1 )
        lista_si = find_negativni(si, 9001, 9136, 3, 6)

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

        #00000-8
        #Za ovaj set se ne primenjuje pravilo 

        #00000-9
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-10
        #Za ovaj set se ne primenjuje pravilo 
        
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
                poruka  =' AOP (0026 + 0055) kol. 5 = 0 Preduzetnici ne mogu imati otkupljene sopstvene akcije odnosno udele  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
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
                poruka  =' AOP (0026 + 0055) kol. 6 = 0 Preduzetnici ne mogu imati otkupljene sopstvene akcije odnosno udele   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
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
        #IZVEŠTAJ O OSTALOM REZULTATU - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        #20001
        if not( suma(ioor,2001,2029,5) > 0 ):
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='Zbir podataka na oznakama za AOP (2001 do 2029) kol. 5 > 0 Izveštaj o ostalom rezultatu, po pravilu,  mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #20002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(ioor,2001,2029,6) == 0 ):
                lzbir =  suma(ioor,2001,2029,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Zbir podataka na oznakama za AOP (2001 do 2029) kol. 6 = 0 Izveštaj o ostalom rezultatu za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(ioor,2001,2029,6) > 0 ):
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Zbir podataka na oznakama za AOP (2001 do 2029) kol. 6 > 0 Izveštaj o ostalom rezultatu, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #20004
        if not( aop(ioor,2001,5) == aop(bu,1055,5) ):
            lzbir =  aop(ioor,2001,5) 
            dzbir =  aop(bu,1055,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 2001 kol. 5 = AOP-u 1055 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2001 kol. 5 = AOP-u 1055 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20005
        if not( aop(ioor,2001,6) == aop(bu,1055,6) ):
            lzbir =  aop(ioor,2001,6) 
            dzbir =  aop(bu,1055,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 2001 kol. 6 = AOP-u 1055 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2001 kol. 6 = AOP-u 1055 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20006
        if not( aop(ioor,2002,5) == aop(bu,1056,5) ):
            lzbir =  aop(ioor,2002,5) 
            dzbir =  aop(bu,1056,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 2002 kol. 5 = AOP-u 1056 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2002 kol. 5 = AOP-u 1056 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20007
        if not( aop(ioor,2002,6) == aop(bu,1056,6) ):
            lzbir =  aop(ioor,2002,6) 
            dzbir =  aop(bu,1056,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 2002 kol. 6 = AOP-u 1056 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2002 kol. 6 = AOP-u 1056 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
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
                poruka  ='AOP 2020 kol. 5 = AOP-u (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018 - 2003 - 2005 - 2007 - 2009 - 2011 - 2013 - 2015 - 2017) kol. 5,  ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017) kol. 5 < AOP-a (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
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
                poruka  ='AOP (2019 + 2020) kol. 5 = 0, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017) kol. 5 = AOP-u (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
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
                poruka  ='AOP (2019 + 2020) kol. 6 = 0, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2017) kol. 6 = AOP-u (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2018) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
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
                poruka  ='Ako je AOP 2019 kol. 5 > 0 onda je AOP 2020 kol. 5 = 0  U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
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
                poruka  ='Ako je AOP 2020 kol. 5 > 0 onda je AOP 2019 kol. 5 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
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
                poruka  ='Ako je AOP 2019 kol. 6 > 0 onda je AOP 2020 kol. 6 = 0  U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
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
                poruka  ='Ako je AOP 2020 kol. 6 > 0 onda je AOP 2019 kol. 6 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
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
        if( suma_liste(ioor,[2019,2022],5) > suma(ioor,2020,2021,5) ):
            if not( aop(ioor,2023,5) == suma_liste(ioor,[2019,2022],5)-suma(ioor,2020,2021,5) ):
                lzbir =  aop(ioor,2023,5) 
                dzbir =  suma_liste(ioor,[2019,2022],5)-suma(ioor,2020,2021,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2023 kol. 5 = AOP-u (2019 - 2020 - 2021 + 2022) kol. 5, ako je AOP (2019 + 2022) kol. 5 > AOP-a (2020 + 2021) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20021
        if( suma_liste(ioor,[2019,2022],6) > suma(ioor,2020,2021,6) ):
            if not( aop(ioor,2023,6) == suma_liste(ioor,[2019,2022],6)-suma(ioor,2020,2021,6) ):
                lzbir =  aop(ioor,2023,6) 
                dzbir =  suma_liste(ioor,[2019,2022],6)-suma(ioor,2020,2021,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2023 kol. 6 = AOP-u (2019 - 2020 - 2021 + 2022) kol. 6, ako je AOP (2019 + 2022) kol. 6 > AOP-a (2020 + 2021) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20022
        if( suma_liste(ioor,[2019,2022],5) < suma(ioor,2020,2021,5) ):
            if not( aop(ioor,2024,5) == suma(ioor,2020,2021,5)-suma_liste(ioor,[2019,2022],5) ):
                lzbir =  aop(ioor,2024,5) 
                dzbir =  suma(ioor,2020,2021,5)-suma_liste(ioor,[2019,2022],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2024 kol. 5 = AOP-u (2020 - 2019 + 2021 - 2022) kol. 5, ako je AOP (2019 + 2022) kol. 5 < AOP-a (2020 + 2021) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20023
        if( suma_liste(ioor,[2019,2022],6) < suma(ioor,2020,2021,6) ):
            if not( aop(ioor,2024,6) == suma(ioor,2020,2021,6)-suma_liste(ioor,[2019,2022],6) ):
                lzbir =  aop(ioor,2024,6) 
                dzbir =  suma(ioor,2020,2021,6)-suma_liste(ioor,[2019,2022],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2024 kol. 6 = AOP-u (2020 - 2019 + 2021 - 2022) kol. 6, ako je AOP (2019 + 2022) kol. 6 < AOP-a (2020 + 2021) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20024
        if( suma_liste(ioor,[2019,2022],5) == suma(ioor,2020,2021,5) ):
            if not( suma(ioor,2023,2024,5) == 0 ):
                lzbir =  suma(ioor,2023,2024,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP (2023 + 2024) kol. 5 = 0, ako je AOP (2019 + 2022) kol. 5 = AOP-u (2020 + 2021) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20025
        if( suma_liste(ioor,[2019,2022],6) == suma(ioor,2020,2021,6) ):
            if not( suma(ioor,2023,2024,6) == 0 ):
                lzbir =  suma(ioor,2023,2024,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP (2023 + 2024) kol. 6 = 0, ako je AOP (2019 + 2022) kol. 6 = AOP-u (2020 + 2021) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20026
        if( aop(ioor,2023,5) > 0 ):
            if not( aop(ioor,2024,5) == 0 ):
                lzbir =  aop(ioor,2024,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2023 kol. 5 > 0 onda je AOP 2024 kol. 5 = 0  U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20027
        if( aop(ioor,2024,5) > 0 ):
            if not( aop(ioor,2023,5) == 0 ):
                lzbir =  aop(ioor,2023,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2024 kol. 5 > 0 onda je AOP 2023 kol. 5 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20028
        if( aop(ioor,2023,6) > 0 ):
            if not( aop(ioor,2024,6) == 0 ):
                lzbir =  aop(ioor,2024,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2023 kol. 6 > 0 onda je AOP 2024 kol. 6 = 0  U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20029
        if( aop(ioor,2024,6) > 0 ):
            if not( aop(ioor,2023,6) == 0 ):
                lzbir =  aop(ioor,2023,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2024 kol. 6 > 0 onda je AOP 2023 kol. 6 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20030
        if not( suma_liste(ioor,[2019,2022,2024],5) == suma_liste(ioor,[2020,2021,2023],5) ):
            lzbir =  suma_liste(ioor,[2019,2022,2024],5) 
            dzbir =  suma_liste(ioor,[2020,2021,2023],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP (2019 + 2022 + 2024) kol. 5 = AOP-u (2020 + 2021 + 2023) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20031
        if not( suma_liste(ioor,[2019,2022,2024],6) == suma_liste(ioor,[2020,2021,2023],6) ):
            lzbir =  suma_liste(ioor,[2019,2022,2024],6) 
            dzbir =  suma_liste(ioor,[2020,2021,2023],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP (2019 + 2022 + 2024) kol. 6 = AOP-u (2020 + 2021 + 2023) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20032
        if( suma_liste(ioor,[2001,2023],5) > suma_liste(ioor,[2002,2024],5) ):
            if not( aop(ioor,2025,5) == suma_liste(ioor,[2001,2023],5)-suma_liste(ioor,[2002,2024],5) ):
                lzbir =  aop(ioor,2025,5) 
                dzbir =  suma_liste(ioor,[2001,2023],5)-suma_liste(ioor,[2002,2024],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2025 kol. 5 = AOP-u (2001 - 2002 + 2023 - 2024) kol. 5, ako je AOP (2001 + 2023) kol. 5 > AOP-a (2002 + 2024) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20033
        if( suma_liste(ioor,[2001,2023],6) > suma_liste(ioor,[2002,2024],6) ):
            if not( aop(ioor,2025,6) == suma_liste(ioor,[2001,2023],6)-suma_liste(ioor,[2002,2024],6) ):
                lzbir =  aop(ioor,2025,6) 
                dzbir =  suma_liste(ioor,[2001,2023],6)-suma_liste(ioor,[2002,2024],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2025 kol. 6 = AOP-u (2001 - 2002 + 2023 - 2024) kol. 6, ako je AOP (2001 + 2023) kol. 6 > AOP-a (2002 + 2024) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20034
        if( suma_liste(ioor,[2001,2023],5) < suma_liste(ioor,[2002,2024],5) ):
            if not( aop(ioor,2026,5) == suma_liste(ioor,[2002,2024],5)-suma_liste(ioor,[2001,2023],5) ):
                lzbir =  aop(ioor,2026,5) 
                dzbir =  suma_liste(ioor,[2002,2024],5)-suma_liste(ioor,[2001,2023],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2026 kol. 5 = AOP-u (2002 - 2001 + 2024 - 2023) kol. 5, ako je AOP (2001 + 2023) kol. 5 < AOP-a (2002 + 2024) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20035
        if( suma_liste(ioor,[2001,2023],6) < suma_liste(ioor,[2002,2024],6) ):
            if not( aop(ioor,2026,6) == suma_liste(ioor,[2002,2024],6)-suma_liste(ioor,[2001,2023],6) ):
                lzbir =  aop(ioor,2026,6) 
                dzbir =  suma_liste(ioor,[2002,2024],6)-suma_liste(ioor,[2001,2023],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2026 kol. 6 = AOP-u (2002 - 2001 + 2024 - 2023) kol. 6, ako je AOP (2001 + 2023) kol. 6 < AOP-a (2002 + 2024) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20036
        if( suma_liste(ioor,[2001,2023],5) == suma_liste(ioor,[2002,2024],5) ):
            if not( suma(ioor,2025,2026,5) == 0 ):
                lzbir =  suma(ioor,2025,2026,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP (2025 + 2026) kol. 5 = 0, ako je AOP (2001 + 2023) kol. 5 = AOP-u (2002 + 2024) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20037
        if( suma_liste(ioor,[2001,2023],6) == suma_liste(ioor,[2002,2024],6) ):
            if not( suma(ioor,2025,2026,6) == 0 ):
                lzbir =  suma(ioor,2025,2026,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP (2025 + 2026) kol. 6 = 0, ako je AOP (2001 + 2023) kol. 6 = AOP-u (2002 + 2024) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20038
        if( aop(ioor,2025,5) > 0 ):
            if not( aop(ioor,2026,5) == 0 ):
                lzbir =  aop(ioor,2026,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2025 kol. 5 > 0 onda je AOP 2026 kol. 5 = 0  U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20039
        if( aop(ioor,2026,5) > 0 ):
            if not( aop(ioor,2025,5) == 0 ):
                lzbir =  aop(ioor,2025,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2026 kol. 5 > 0 onda je AOP 2025 kol. 5 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20040
        if( aop(ioor,2025,6) > 0 ):
            if not( aop(ioor,2026,6) == 0 ):
                lzbir =  aop(ioor,2026,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2025 kol. 6 > 0 onda je AOP 2026 kol. 6 = 0  U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20041
        if( aop(ioor,2026,6) > 0 ):
            if not( aop(ioor,2025,6) == 0 ):
                lzbir =  aop(ioor,2025,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2026 kol. 6 > 0 onda je AOP 2025 kol. 6 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20042
        if not( suma_liste(ioor,[2001,2023,2026],5) == suma_liste(ioor,[2002,2024,2025],5) ):
            lzbir =  suma_liste(ioor,[2001,2023,2026],5) 
            dzbir =  suma_liste(ioor,[2002,2024,2025],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP (2001 + 2023 + 2026) kol. 5 = AOP-u (2002 + 2024 + 2025) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20043
        if not( suma_liste(ioor,[2001,2023,2026],6) == suma_liste(ioor,[2002,2024,2025],6) ):
            lzbir =  suma_liste(ioor,[2001,2023,2026],6) 
            dzbir =  suma_liste(ioor,[2002,2024,2025],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP (2001 + 2023 + 2026) kol. 6 = AOP-u (2002 + 2024 + 2025) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20044
        #Za ovaj set se ne primenjuje pravilo 
        #20045
        #Za ovaj set se ne primenjuje pravilo 
        #20046
        #Za ovaj set se ne primenjuje pravilo 
        #20047
        #Za ovaj set se ne primenjuje pravilo
         
        #20048
        if not( aop(ioor,2027,5) == 0 ):
            lzbir =  aop(ioor,2027,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2027 kol. 5 = 0  Ukupan neto sveobuhvatni rezultat koji je pripisan matičnom pravnom licu i učešćima bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20049
        if not( aop(ioor,2027,6) == 0 ):
            lzbir =  aop(ioor,2027,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2027 kol. 6 = 0  Ukupan neto sveobuhvatni rezultat koji je pripisan matičnom pravnom licu i učešćima bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20050
        if not( aop(ioor,2028,5) == 0 ):
            lzbir =  aop(ioor,2028,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2028 kol. 5 = 0  Ukupan neto sveobuhvatni rezultat koji je pripisan matičnom pravnom licu i učešćima bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20051
        if not( aop(ioor,2028,6) == 0 ):
            lzbir =  aop(ioor,2028,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2028 kol. 6 = 0  Ukupan neto sveobuhvatni rezultat koji je pripisan matičnom pravnom licu i učešćima bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20052
        if not( aop(ioor,2029,5) == 0 ):
            lzbir =  aop(ioor,2029,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2029 kol. 5 = 0  Ukupan neto sveobuhvatni rezultat koji je pripisan matičnom pravnom licu i učešćima bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20053
        if not( aop(ioor,2029,6) == 0 ):
            lzbir =  aop(ioor,2029,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2029 kol. 6 = 0  Ukupan neto sveobuhvatni rezultat koji je pripisan matičnom pravnom licu i učešćima bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #IZVEŠTAJ O TOKOVIMA GOTOVINE - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #30001
        if not( suma(iotg,3001,3055,3) > 0 ):
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='Zbir podataka na oznakama za AOP (3001 do 3055) kol. 3 > 0 Izveštaj o tokovima gotovine, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #30002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(iotg,3001,3055,4) == 0 ):
                lzbir =  suma(iotg,3001,3055,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Zbir podataka na oznakama za AOP (3001 do 3055) kol. 4 = 0 Izveštaj o tokovima gotovine za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(iotg,3001,3055,4) > 0 ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Zbir podataka na oznakama za AOP (3001 do 3055) kol. 4 > 0 Izveštaj o tokovima gotovine, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
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
        if not( aop(iotg,3006,3) == suma(iotg,3007,3014,3) ):
            lzbir =  aop(iotg,3006,3) 
            dzbir =  suma(iotg,3007,3014,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3006 kol. 3 = AOP-u (3007 + 3008 + 3009 + 3010 + 3011 + 3012 + 3013 + 3014) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30007
        if not( aop(iotg,3006,4) == suma(iotg,3007,3014,4) ):
            lzbir =  aop(iotg,3006,4) 
            dzbir =  suma(iotg,3007,3014,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3006 kol. 4 = AOP-u (3007 + 3008 + 3009 + 3010 + 3011 + 3012 + 3013 + 3014) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30008
        if( aop(iotg,3001,3) > aop(iotg,3006,3) ):
            if not( aop(iotg,3015,3) == aop(iotg,3001,3)-aop(iotg,3006,3) ):
                lzbir =  aop(iotg,3015,3) 
                dzbir =  aop(iotg,3001,3)-aop(iotg,3006,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3015 kol. 3 = AOP-u (3001 - 3006) kol. 3, ako je AOP 3001 kol. 3 > AOP-a 3006 kol. 3   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30009
        if( aop(iotg,3001,4) > aop(iotg,3006,4) ):
            if not( aop(iotg,3015,4) == aop(iotg,3001,4)-aop(iotg,3006,4) ):
                lzbir =  aop(iotg,3015,4) 
                dzbir =  aop(iotg,3001,4)-aop(iotg,3006,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3015 kol. 4 = AOP-u (3001 - 3006) kol. 4, ako je AOP 3001 kol. 4 > AOP-a 3006 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30010
        if( aop(iotg,3001,3) < aop(iotg,3006,3) ):
            if not( aop(iotg,3016,3) == aop(iotg,3006,3)-aop(iotg,3001,3) ):
                lzbir =  aop(iotg,3016,3) 
                dzbir =  aop(iotg,3006,3)-aop(iotg,3001,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3016 kol. 3 = AOP-u (3006 - 3001) kol. 3, ako je AOP 3001 kol. 3 < AOP-a 3006 kol. 3    '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30011
        if( aop(iotg,3001,4) < aop(iotg,3006,4) ):
            if not( aop(iotg,3016,4) == aop(iotg,3006,4)-aop(iotg,3001,4) ):
                lzbir =  aop(iotg,3016,4) 
                dzbir =  aop(iotg,3006,4)-aop(iotg,3001,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3016 kol. 4 = AOP-u (3006 - 3001) kol. 4, ako je AOP 3001 kol. 4 < AOP-a 3006 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30012
        if( aop(iotg,3001,3) == aop(iotg,3006,3) ):
            if not( suma(iotg,3015,3016,3) == 0 ):
                lzbir =  suma(iotg,3015,3016,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3015 + 3016) kol. 3 = 0, ako je AOP 3001 kol. 3 = AOP-a 3006 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30013
        if( aop(iotg,3001,4) == aop(iotg,3006,4) ):
            if not( suma(iotg,3015,3016,4) == 0 ):
                lzbir =  suma(iotg,3015,3016,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3015 + 3016) kol. 4 = 0, ako je AOP 3001 kol. 4 = AOP-a 3006 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30014
        if( aop(iotg,3015,3) > 0 ):
            if not( aop(iotg,3016,3) == 0 ):
                lzbir =  aop(iotg,3016,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3015 kol. 3 > 0 onda je AOP 3016 kol. 3 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30015
        if( aop(iotg,3016,3) > 0 ):
            if not( aop(iotg,3015,3) == 0 ):
                lzbir =  aop(iotg,3015,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3016 kol. 3 > 0 onda je AOP 3015 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30016
        if( aop(iotg,3015,4) > 0 ):
            if not( aop(iotg,3016,4) == 0 ):
                lzbir =  aop(iotg,3016,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3015 kol. 4 > 0 onda je AOP 3016 kol. 4 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30017
        if( aop(iotg,3016,4) > 0 ):
            if not( aop(iotg,3015,4) == 0 ):
                lzbir =  aop(iotg,3015,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3016 kol. 4 > 0 onda je AOP 3015 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30018
        if not( suma_liste(iotg,[3001,3016],3) == suma_liste(iotg,[3006,3015],3) ):
            lzbir =  suma_liste(iotg,[3001,3016],3) 
            dzbir =  suma_liste(iotg,[3006,3015],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3001 + 3016) kol. 3 = AOP-u (3006 + 3015) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30019
        if not( suma_liste(iotg,[3001,3016],4) == suma_liste(iotg,[3006,3015],4) ):
            lzbir =  suma_liste(iotg,[3001,3016],4) 
            dzbir =  suma_liste(iotg,[3006,3015],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3001 + 3016) kol. 4 = AOP-u (3006 + 3015) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30020
        if not( aop(iotg,3017,3) == suma(iotg,3018,3022,3) ):
            lzbir =  aop(iotg,3017,3) 
            dzbir =  suma(iotg,3018,3022,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3017 kol. 3 = AOP-u (3018 + 3019 + 3020 + 3021 + 3022) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30021
        if not( aop(iotg,3017,4) == suma(iotg,3018,3022,4) ):
            lzbir =  aop(iotg,3017,4) 
            dzbir =  suma(iotg,3018,3022,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3017 kol. 4 = AOP-u (3018 + 3019 + 3020 + 3021 + 3022) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
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
        if( aop(iotg,3017,3) > aop(iotg,3023,3) ):
            if not( aop(iotg,3027,3) == aop(iotg,3017,3)-aop(iotg,3023,3) ):
                lzbir =  aop(iotg,3027,3) 
                dzbir =  aop(iotg,3017,3)-aop(iotg,3023,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3027 kol. 3 = AOP-u (3017 - 3023) kol. 3, ako je AOP 3017 kol. 3 > AOP-a 3023 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30025
        if( aop(iotg,3017,4) > aop(iotg,3023,4) ):
            if not( aop(iotg,3027,4) == aop(iotg,3017,4)-aop(iotg,3023,4) ):
                lzbir =  aop(iotg,3027,4) 
                dzbir =  aop(iotg,3017,4)-aop(iotg,3023,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3027 kol. 4 = AOP-u (3017 - 3023) kol. 4, ako je AOP 3017 kol. 4 > AOP-a 3023 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30026
        if( aop(iotg,3017,3) < aop(iotg,3023,3) ):
            if not( aop(iotg,3028,3) == aop(iotg,3023,3)-aop(iotg,3017,3) ):
                lzbir =  aop(iotg,3028,3) 
                dzbir =  aop(iotg,3023,3)-aop(iotg,3017,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3028 kol. 3 = AOP-u (3023 - 3017) kol. 3, ako je AOP 3017 kol. 3 < AOP-a 3023 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30027
        if( aop(iotg,3017,4) < aop(iotg,3023,4) ):
            if not( aop(iotg,3028,4) == aop(iotg,3023,4)-aop(iotg,3017,4) ):
                lzbir =  aop(iotg,3028,4) 
                dzbir =  aop(iotg,3023,4)-aop(iotg,3017,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3028 kol. 4 = AOP-u (3023 - 3017) kol. 4, ako je AOP 3017 kol. 4 < AOP-a 3023 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30028
        if( aop(iotg,3017,3) == aop(iotg,3023,3) ):
            if not( suma(iotg,3027,3028,3) == 0 ):
                lzbir =  suma(iotg,3027,3028,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3027 + 3028) kol. 3 = 0, ako je AOP 3017 kol. 3 = AOP-u 3023 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30029
        if( aop(iotg,3017,4) == aop(iotg,3023,4) ):
            if not( suma(iotg,3027,3028,4) == 0 ):
                lzbir =  suma(iotg,3027,3028,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3027 + 3028) kol. 4 = 0, ako je AOP 3017 kol. 4 = AOP-u 3023 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
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
        if not( suma_liste(iotg,[3017,3028],3) == suma_liste(iotg,[3023,3027],3) ):
            lzbir =  suma_liste(iotg,[3017,3028],3) 
            dzbir =  suma_liste(iotg,[3023,3027],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3017 + 3028) kol. 3 = AOP-u (3023 + 3027) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30035
        if not( suma_liste(iotg,[3017,3028],4) == suma_liste(iotg,[3023,3027],4) ):
            lzbir =  suma_liste(iotg,[3017,3028],4) 
            dzbir =  suma_liste(iotg,[3023,3027],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3017 + 3028) kol. 4 = AOP-u (3023 + 3027) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30036
        if not( aop(iotg,3029,3) == suma(iotg,3030,3036,3) ):
            lzbir =  aop(iotg,3029,3) 
            dzbir =  suma(iotg,3030,3036,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3029 kol. 3 = AOP-u (3030 + 3031 + 3032 + 3033 + 3034 + 3035 + 3036) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30037
        if not( aop(iotg,3029,4) == suma(iotg,3030,3036,4) ):
            lzbir =  aop(iotg,3029,4) 
            dzbir =  suma(iotg,3030,3036,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3029 kol. 4 = AOP-u (3030 + 3031 + 3032 + 3033 + 3034 + 3035 + 3036) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30038
        if not( aop(iotg,3037,3) == suma(iotg,3038,3045,3) ):
            lzbir =  aop(iotg,3037,3) 
            dzbir =  suma(iotg,3038,3045,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3037 kol. 3 = AOP-u (3038 + 3039 + 3040 + 3041 + 3042 + 3043 + 3044 + 3045) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30039
        if not( aop(iotg,3037,4) == suma(iotg,3038,3045,4) ):
            lzbir =  aop(iotg,3037,4) 
            dzbir =  suma(iotg,3038,3045,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3037 kol. 4 = AOP-u (3038 + 3039 + 3040 + 3041 + 3042 + 3043 + 3044 + 3045) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30040
        if( aop(iotg,3029,3) > aop(iotg,3037,3) ):
            if not( aop(iotg,3046,3) == aop(iotg,3029,3)-aop(iotg,3037,3) ):
                lzbir =  aop(iotg,3046,3) 
                dzbir =  aop(iotg,3029,3)-aop(iotg,3037,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3046 kol. 3 = AOP-u (3029 - 3037) kol. 3, ako je AOP 3029 kol. 3 > AOP-a 3037 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30041
        if( aop(iotg,3029,4) > aop(iotg,3037,4) ):
            if not( aop(iotg,3046,4) == aop(iotg,3029,4)-aop(iotg,3037,4) ):
                lzbir =  aop(iotg,3046,4) 
                dzbir =  aop(iotg,3029,4)-aop(iotg,3037,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3046 kol. 4 = AOP-u (3029 - 3037) kol. 4, ako je AOP 3029 kol. 4 > AOP-a 3037 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30042
        if( aop(iotg,3029,3) < aop(iotg,3037,3) ):
            if not( aop(iotg,3047,3) == aop(iotg,3037,3)-aop(iotg,3029,3) ):
                lzbir =  aop(iotg,3047,3) 
                dzbir =  aop(iotg,3037,3)-aop(iotg,3029,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3047 kol. 3 = AOP-u (3037 - 3029) kol. 3, ako je AOP 3029 kol. 3 < AOP-a 3037 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30043
        if( aop(iotg,3029,4) < aop(iotg,3037,4) ):
            if not( aop(iotg,3047,4) == aop(iotg,3037,4)-aop(iotg,3029,4) ):
                lzbir =  aop(iotg,3047,4) 
                dzbir =  aop(iotg,3037,4)-aop(iotg,3029,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3047 kol. 4 = AOP-u (3037 - 3029) kol. 4, ako je AOP 3029 kol. 4 < AOP-a 3037 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30044
        if( aop(iotg,3029,3) == aop(iotg,3037,3) ):
            if not( suma(iotg,3046,3047,3) == 0 ):
                lzbir =  suma(iotg,3046,3047,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3046 + 3047) kol. 3 = 0, ako je AOP 3029 kol. 3 = AOP-u 3037 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30045
        if( aop(iotg,3029,4) == aop(iotg,3037,4) ):
            if not( suma(iotg,3046,3047,4) == 0 ):
                lzbir =  suma(iotg,3046,3047,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3046 + 3047) kol. 4 = 0, ako je AOP 3029 kol. 4 = AOP-u 3037 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30046
        if( aop(iotg,3046,3) > 0 ):
            if not( aop(iotg,3047,3) == 0 ):
                lzbir =  aop(iotg,3047,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3046 kol. 3 > 0 onda je AOP 3047 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30047
        if( aop(iotg,3047,3) > 0 ):
            if not( aop(iotg,3046,3) == 0 ):
                lzbir =  aop(iotg,3046,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3047 kol. 3 > 0 onda je AOP 3046 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30048
        if( aop(iotg,3046,4) > 0 ):
            if not( aop(iotg,3047,4) == 0 ):
                lzbir =  aop(iotg,3047,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3046 kol. 4 > 0 onda je AOP 3047 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30049
        if( aop(iotg,3047,4) > 0 ):
            if not( aop(iotg,3046,4) == 0 ):
                lzbir =  aop(iotg,3046,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3047 kol. 4 > 0 onda je AOP 3046 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30050
        if not( suma_liste(iotg,[3029,3047],3) == suma_liste(iotg,[3037,3046],3) ):
            lzbir =  suma_liste(iotg,[3029,3047],3) 
            dzbir =  suma_liste(iotg,[3037,3046],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3029 + 3047) kol. 3 = AOP-u (3037 + 3046) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30051
        if not( suma_liste(iotg,[3029,3047],4) == suma_liste(iotg,[3037,3046],4) ):
            lzbir =  suma_liste(iotg,[3029,3047],4) 
            dzbir =  suma_liste(iotg,[3037,3046],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3029 + 3047) kol. 4 = AOP-u (3037 + 3046) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30052
        if not( aop(iotg,3048,3) == suma_liste(iotg,[3001,3017,3029],3) ):
            lzbir =  aop(iotg,3048,3) 
            dzbir =  suma_liste(iotg,[3001,3017,3029],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3048 kol. 3 = AOP-u (3001 + 3017 + 3029) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30053
        if not( aop(iotg,3048,4) == suma_liste(iotg,[3001,3017,3029],4) ):
            lzbir =  aop(iotg,3048,4) 
            dzbir =  suma_liste(iotg,[3001,3017,3029],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3048 kol. 4 = AOP-u (3001 + 3017 + 3029) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30054
        if not( aop(iotg,3049,3) == suma_liste(iotg,[3006,3023,3037],3) ):
            lzbir =  aop(iotg,3049,3) 
            dzbir =  suma_liste(iotg,[3006,3023,3037],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3049 kol. 3 = AOP-u (3006 + 3023 + 3037) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30055
        if not( aop(iotg,3049,4) == suma_liste(iotg,[3006,3023,3037],4) ):
            lzbir =  aop(iotg,3049,4) 
            dzbir =  suma_liste(iotg,[3006,3023,3037],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3049 kol. 4 = AOP-u (3006 + 3023 + 3037) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30056
        if( aop(iotg,3048,3) > aop(iotg,3049,3) ):
            if not( aop(iotg,3050,3) == aop(iotg,3048,3)-aop(iotg,3049,3) ):
                lzbir =  aop(iotg,3050,3) 
                dzbir =  aop(iotg,3048,3)-aop(iotg,3049,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3050 kol. 3 = AOP-u (3048 - 3049) kol. 3, ako je AOP 3048 kol. 3 > AOP-a 3049 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30057
        if( aop(iotg,3048,4) > aop(iotg,3049,4) ):
            if not( aop(iotg,3050,4) == aop(iotg,3048,4)-aop(iotg,3049,4) ):
                lzbir =  aop(iotg,3050,4) 
                dzbir =  aop(iotg,3048,4)-aop(iotg,3049,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3050 kol. 4 = AOP-u (3048 - 3049) kol. 4, ako je AOP 3048 kol. 4 > AOP-a 3049 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30058
        if( aop(iotg,3048,3) < aop(iotg,3049,3) ):
            if not( aop(iotg,3051,3) == aop(iotg,3049,3)-aop(iotg,3048,3) ):
                lzbir =  aop(iotg,3051,3) 
                dzbir =  aop(iotg,3049,3)-aop(iotg,3048,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3051 kol. 3 = AOP-u (3049 - 3048) kol. 3, ako je AOP 3048 kol. 3 < AOP-a 3049 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30059
        if( aop(iotg,3048,4) < aop(iotg,3049,4) ):
            if not( aop(iotg,3051,4) == aop(iotg,3049,4)-aop(iotg,3048,4) ):
                lzbir =  aop(iotg,3051,4) 
                dzbir =  aop(iotg,3049,4)-aop(iotg,3048,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3051 kol. 4 = AOP-u (3049 - 3048) kol. 4, ako je AOP 3048 kol. 4 < AOP-a 3049 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30060
        if( aop(iotg,3048,3) == aop(iotg,3049,3) ):
            if not( suma(iotg,3050,3051,3) == 0 ):
                lzbir =  suma(iotg,3050,3051,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3050 + 3051) kol. 3 = 0, ako je AOP 3048 kol. 3 = AOP-u 3049 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30061
        if( aop(iotg,3048,4) == aop(iotg,3049,4) ):
            if not( suma(iotg,3050,3051,4) == 0 ):
                lzbir =  suma(iotg,3050,3051,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3050 + 3051) kol. 4 = 0, ako je AOP 3048 kol. 4 = AOP-u 3049 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30062
        if( aop(iotg,3050,3) > 0 ):
            if not( aop(iotg,3051,3) == 0 ):
                lzbir =  aop(iotg,3051,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3050 kol. 3 > 0 onda je AOP 3051 kol. 3 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30063
        if( aop(iotg,3051,3) > 0 ):
            if not( aop(iotg,3050,3) == 0 ):
                lzbir =  aop(iotg,3050,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3051 kol. 3 > 0 onda je AOP 3050 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30064
        if( aop(iotg,3050,4) > 0 ):
            if not( aop(iotg,3051,4) == 0 ):
                lzbir =  aop(iotg,3051,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3050 kol. 4 > 0 onda je AOP 3051 kol. 4 = 0  U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30065
        if( aop(iotg,3051,4) > 0 ):
            if not( aop(iotg,3050,4) == 0 ):
                lzbir =  aop(iotg,3050,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3051 kol. 4 > 0 onda je AOP 3050 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30066
        if not( suma_liste(iotg,[3048,3051],3) == suma(iotg,3049,3050,3) ):
            lzbir =  suma_liste(iotg,[3048,3051],3) 
            dzbir =  suma(iotg,3049,3050,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3048 + 3051) kol. 3 = AOP-u (3049 + 3050) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30067
        if not( suma_liste(iotg,[3048,3051],4) == suma(iotg,3049,3050,4) ):
            lzbir =  suma_liste(iotg,[3048,3051],4) 
            dzbir =  suma(iotg,3049,3050,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3048 + 3051) kol. 4 = AOP-u (3049 + 3050) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30068
        if not( suma_liste(iotg,[3015,3027,3046,3051],3) == suma_liste(iotg,[3016,3028,3047,3050],3) ):
            lzbir =  suma_liste(iotg,[3015,3027,3046,3051],3) 
            dzbir =  suma_liste(iotg,[3016,3028,3047,3050],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3015 + 3027 + 3046 + 3051) kol. 3 = AOP-u (3016 + 3028 + 3047 + 3050) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30069
        if not( suma_liste(iotg,[3015,3027,3046,3051],4) == suma_liste(iotg,[3016,3028,3047,3050],4) ):
            lzbir =  suma_liste(iotg,[3015,3027,3046,3051],4) 
            dzbir =  suma_liste(iotg,[3016,3028,3047,3050],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3015 + 3027 + 3046 + 3051) kol. 4 = AOP-u (3016 + 3028 + 3047 + 3050) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30070
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( aop(iotg,3052,3) == 0 ):
                lzbir =  aop(iotg,3052,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3052 kol. 3 = 0 Novoosnovana pravna lica ne smeju imati prikazan podatak za prethodnu godinu '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30071
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( aop(iotg,3052,4) == aop(bs,57,7) ):
                lzbir =  aop(iotg,3052,4) 
                dzbir =  aop(bs,57,7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 3052 kol. 4 = AOP-u 0057 kol. 7 bilansa stanja Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3052 kol. 4 = AOP-u 0057 kol. 7 bilansa stanja Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #30072
        if( suma_liste(iotg,[3050,3052,3053],3) > suma_liste(iotg,[3051,3054],3) ):
            if not( aop(iotg,3055,3) == suma_liste(iotg,[3050,3052,3053],3)-suma_liste(iotg,[3051,3054],3) ):
                lzbir =  aop(iotg,3055,3) 
                dzbir =  suma_liste(iotg,[3050,3052,3053],3)-suma_liste(iotg,[3051,3054],3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3055 kol. 3 = AOP-u (3050 - 3051 + 3052 + 3053 - 3054) kol. 3, ako je AOP (3050 + 3052 + 3053) kol. 3 > AOP-a (3051 + 3054) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30073
        if( suma_liste(iotg,[3050,3052,3053],4) > suma_liste(iotg,[3051,3054],4) ):
            if not( aop(iotg,3055,4) == suma_liste(iotg,[3050,3052,3053],4)-suma_liste(iotg,[3051,3054],4) ):
                lzbir =  aop(iotg,3055,4) 
                dzbir =  suma_liste(iotg,[3050,3052,3053],4)-suma_liste(iotg,[3051,3054],4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3055 kol. 4 = AOP-u (3050 - 3051 + 3052 + 3053 - 3054) kol. 4, ako je AOP (3050 + 3052 + 3053) kol. 4 > AOP-a (3051 + 3054) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30074
        if( suma_liste(iotg,[3050,3052,3053],3) <= suma_liste(iotg,[3051,3054],3) ):
            if not( aop(iotg,3055,3) == 0 ):
                lzbir =  aop(iotg,3055,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3055 kol. 3 = 0, ako je AOP (3050 + 3052 + 3053) kol. 3 ≤ AOP-a (3051 + 3054) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30075
        if( suma_liste(iotg,[3050,3052,3053],4) <= suma_liste(iotg,[3051,3054],4) ):
            if not( aop(iotg,3055,4) == 0 ):
                lzbir =  aop(iotg,3055,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3055 kol. 4 = 0, ako je AOP (3050 + 3052 + 3053) kol. 4 ≤ AOP-a (3051 + 3054) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30076
        if not( aop(iotg,3052,3) == aop(iotg,3055,4) ):
            lzbir =  aop(iotg,3052,3) 
            dzbir =  aop(iotg,3055,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3052 kol. 3 = AOP- u 3055 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30077
        if not( aop(iotg,3055,3) == aop(bs,57,5) ):
            lzbir =  aop(iotg,3055,3) 
            dzbir =  aop(bs,57,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 3055 kol. 3 = AOP-u 0057 kol. 5 bilansa stanja Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3055 kol. 3 = AOP-u 0057 kol. 5 bilansa stanja Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #30078
        if not( aop(iotg,3055,4) == aop(bs,57,6) ):
            lzbir =  aop(iotg,3055,4) 
            dzbir =  aop(bs,57,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 3055 kol. 4 = AOP-u 0057 kol. 6 bilansa stanja Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3055 kol. 4 = AOP-u 0057 kol. 6 bilansa stanja Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #IZVEŠTAJ O PROMENAMA NA KAPITALU - POTREBNO JE OBEZBEDITI UNOS IZNOSA SA PREDZNAKOM - (MINUS) NA SLEDEĆIM AOP POZICIJAMA: 4002, 4004, 4006, 4008, 4011, 4013, 4015, 4017, 4020, 4022, 4024, 4026, 4029, 4031, 4033, 4035, 4037, 4038, 4039, 4040, 4041, 4042, 4043, 4044, 4045, 4047, 4049, 4051,4053, 4056, 4058, 4060, 4062, 4065, 4067, 4069, 4071, 4074, 4076, 4078, 4080, 4083, 4085, 4087, 4089. NA OSTALIM AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        #40001
        if not ( suma(iopk, 4008, 4009, 1) + suma(iopk, 4017, 4018, 1) + suma(iopk, 4026, 4027, 1) + suma(iopk, 4035, 4036, 1) + suma(iopk, 4044, 4045, 1) + suma(iopk, 4053, 4054, 1) + suma(iopk, 4062, 4063, 1) + suma(iopk, 4071, 4072, 1) + suma(iopk, 4080, 4081, 1) + suma(iopk, 4089, 4090, 1) > 0 ):
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='Zbir podataka na oznakama za AOP (4008 do 4009) + (4017 do 4018) + (4026 do 4027) + (4035 do 4036) + (4044 do 4045) + (4053 do 4054) + (4062 do 4063) + (4071 do 4072) + (4080 do 4081) + (4089 do 4090)  > 0  Izveštaj o promenama na kapitalu, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40002
        if(Zahtev.ObveznikInfo.Novoosnovan == True):
            if not ( suma(iopk, 4001, 4007, 1) + suma(iopk, 4010, 4016, 1) + suma(iopk, 4019, 4025, 1) + suma(iopk, 4028, 4034, 1) + suma(iopk, 4037, 4043, 1) + suma(iopk, 4046, 4052, 1) + suma(iopk, 4055, 4061, 1) + suma(iopk, 4064, 4070, 1) + suma(iopk, 4073, 4079, 1) + suma(iopk, 4082, 4088, 1) == 0 ):
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Zbir podataka na oznakama za AOP (4001 do 4007) + (4010 do 4016) + (4019 do 4025) + (4028 do 4034) + (4037 do 4043) + (4046 do 4052) + (4055 do 4061) + (4064 do 4070) + (4073 do 4079) + (4082 do 4088) = 0  Izveštaj o promenama na kapitalu za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period;'
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

        #40003
        if(Zahtev.ObveznikInfo.Novoosnovan == False):
            if not ( suma(iopk, 4001, 4007, 1) + suma(iopk, 4010, 4016, 1) + suma(iopk, 4019, 4025, 1) + suma(iopk, 4028, 4034, 1) + suma(iopk, 4037, 4043, 1) + suma(iopk, 4046, 4052, 1) + suma(iopk, 4055, 4061, 1) + suma(iopk, 4064, 4070, 1) + suma(iopk, 4073, 4079, 1) + suma(iopk, 4082, 4088, 1) > 0 ):
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Zbir podataka na oznakama za AOP (4001 do 4007) + (4010 do 4016) + (4019 do 4025) + (4028 do 4034) + (4037 do 4043) + (4046 do 4052) + (4055 do 4061) + (4064 do 4070) + (4073 do 4079) + (4082 do 4088) > 0  Izveštaj o promenama na kapitalu, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga'
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

        #40004
        if not( aop(iopk,4003,1) == aop(iopk,4001,1) + aop(iopk,4002,1) ):
            lzbir =  aop(iopk,4003,1) 
            dzbir =  aop(iopk,4001,1) + aop(iopk,4002,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4003 = AOP-u (4001 + 4002)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40005
        if not( aop(iopk,4012,1) == aop(iopk,4010,1) + aop(iopk,4011,1) ):
            lzbir =  aop(iopk,4012,1) 
            dzbir =  aop(iopk,4010,1) + aop(iopk,4011,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4012 = AOP-u (4010 + 4011)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40006
        if not( aop(iopk,4021,1) == aop(iopk,4019,1) + aop(iopk,4020,1) ):
            lzbir =  aop(iopk,4021,1) 
            dzbir =  aop(iopk,4019,1) + aop(iopk,4020,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4021 = AOP-u (4019 + 4020)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40007
        if not( aop(iopk,4030,1) == aop(iopk,4028,1) + aop(iopk,4029,1) ):
            lzbir =  aop(iopk,4030,1) 
            dzbir =  aop(iopk,4028,1) + aop(iopk,4029,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4030 = AOP-u (4028 + 4029)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40008
        if not( aop(iopk,4039,1) == aop(iopk,4037,1) + aop(iopk,4038,1) ):
            lzbir =  aop(iopk,4039,1) 
            dzbir =  aop(iopk,4037,1) + aop(iopk,4038,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4039 = AOP-u (4037 + 4038)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40009
        if not( aop(iopk,4048,1) == aop(iopk,4046,1) + aop(iopk,4047,1) ):
            lzbir =  aop(iopk,4048,1) 
            dzbir =  aop(iopk,4046,1) + aop(iopk,4047,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4048 = AOP-u (4046 + 4047)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40010
        if not( aop(iopk,4057,1) == aop(iopk,4055,1) + aop(iopk,4056,1) ):
            lzbir =  aop(iopk,4057,1) 
            dzbir =  aop(iopk,4055,1) + aop(iopk,4056,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4057 = AOP-u (4055 + 4056)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40011
        if not( aop(iopk,4066,1) == aop(iopk,4064,1) + aop(iopk,4065,1) ):
            lzbir =  aop(iopk,4066,1) 
            dzbir =  aop(iopk,4064,1) + aop(iopk,4065,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4066 = AOP-u (4064 + 4065)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40012
        if not( aop(iopk,4005,1) == aop(iopk,4003,1) + aop(iopk,4004,1) ):
            lzbir =  aop(iopk,4005,1) 
            dzbir =  aop(iopk,4003,1) + aop(iopk,4004,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4005 = AOP-u (4003 + 4004)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40013
        if not( aop(iopk,4014,1) == aop(iopk,4012,1) + aop(iopk,4013,1) ):
            lzbir =  aop(iopk,4014,1) 
            dzbir =  aop(iopk,4012,1) + aop(iopk,4013,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4014 = AOP-u (4012 + 4013)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40014
        if not( aop(iopk,4023,1) == aop(iopk,4021,1) + aop(iopk,4022,1) ):
            lzbir =  aop(iopk,4023,1) 
            dzbir =  aop(iopk,4021,1) + aop(iopk,4022,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4023 = AOP-u (4021 + 4022)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40015
        if not( aop(iopk,4032,1) == aop(iopk,4030,1) + aop(iopk,4031,1) ):
            lzbir =  aop(iopk,4032,1) 
            dzbir =  aop(iopk,4030,1) + aop(iopk,4031,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4032 = AOP-u (4030 + 4031)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40016
        if not( aop(iopk,4041,1) == aop(iopk,4039,1) + aop(iopk,4040,1) ):
            lzbir =  aop(iopk,4041,1) 
            dzbir =  aop(iopk,4039,1) + aop(iopk,4040,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4041 = AOP-u (4039 + 4040)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40017
        if not( aop(iopk,4050,1) == aop(iopk,4048,1) + aop(iopk,4049,1) ):
            lzbir =  aop(iopk,4050,1) 
            dzbir =  aop(iopk,4048,1) + aop(iopk,4049,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4050 = AOP-u (4048 + 4049)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40018
        if not( aop(iopk,4059,1) == aop(iopk,4057,1) + aop(iopk,4058,1) ):
            lzbir =  aop(iopk,4059,1) 
            dzbir =  aop(iopk,4057,1) + aop(iopk,4058,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4059 = AOP-u (4057 + 4058)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40019
        if not( aop(iopk,4068,1) == aop(iopk,4066,1) + aop(iopk,4067,1) ):
            lzbir =  aop(iopk,4068,1) 
            dzbir =  aop(iopk,4066,1) + aop(iopk,4067,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4068 = AOP-u (4066 + 4067)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40020
        if not( aop(iopk,4007,1) == aop(iopk,4005,1) + aop(iopk,4006,1) ):
            lzbir =  aop(iopk,4007,1) 
            dzbir =  aop(iopk,4005,1) + aop(iopk,4006,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4007 = AOP-u (4005 + 4006)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40021
        if not( aop(iopk,4016,1) == aop(iopk,4014,1) + aop(iopk,4015,1) ):
            lzbir =  aop(iopk,4016,1) 
            dzbir =  aop(iopk,4014,1) + aop(iopk,4015,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4016 = AOP-u (4014 + 4015)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40022
        if not( aop(iopk,4025,1) == aop(iopk,4023,1) + aop(iopk,4024,1) ):
            lzbir =  aop(iopk,4025,1) 
            dzbir =  aop(iopk,4023,1) + aop(iopk,4024,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4025 = AOP-u (4023 + 4024)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40023
        if not( aop(iopk,4034,1) == aop(iopk,4032,1) + aop(iopk,4033,1) ):
            lzbir =  aop(iopk,4034,1) 
            dzbir =  aop(iopk,4032,1) + aop(iopk,4033,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4034 = AOP-u (4032 + 4033)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40024
        if not( aop(iopk,4043,1) == aop(iopk,4041,1) + aop(iopk,4042,1) ):
            lzbir =  aop(iopk,4043,1) 
            dzbir =  aop(iopk,4041,1) + aop(iopk,4042,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4043 = AOP-u (4041 + 4042)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40025
        if not( aop(iopk,4052,1) == aop(iopk,4050,1) + aop(iopk,4051,1) ):
            lzbir =  aop(iopk,4052,1) 
            dzbir =  aop(iopk,4050,1) + aop(iopk,4051,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4052 = AOP-u (4050 + 4051)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40026
        if not( aop(iopk,4061,1) == aop(iopk,4059,1) + aop(iopk,4060,1) ):
            lzbir =  aop(iopk,4061,1) 
            dzbir =  aop(iopk,4059,1) + aop(iopk,4060,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4061 = AOP-u (4059 + 4060)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40027
        if not( aop(iopk,4070,1) == aop(iopk,4068,1) + aop(iopk,4069,1) ):
            lzbir =  aop(iopk,4070,1) 
            dzbir =  aop(iopk,4068,1) + aop(iopk,4069,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4070 = AOP-u (4068 + 4069)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40028
        if not( aop(iopk,4009,1) == aop(iopk,4007,1) + aop(iopk,4008,1) ):
            lzbir =  aop(iopk,4009,1) 
            dzbir =  aop(iopk,4007,1) + aop(iopk,4008,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4009 = AOP-u (4007 + 4008)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40029
        if not( aop(iopk,4018,1) == aop(iopk,4016,1) + aop(iopk,4017,1) ):
            lzbir =  aop(iopk,4018,1) 
            dzbir =  aop(iopk,4016,1) + aop(iopk,4017,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4018 = AOP-u (4016 + 4017)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40030
        if not( aop(iopk,4027,1) == aop(iopk,4025,1) + aop(iopk,4026,1) ):
            lzbir =  aop(iopk,4027,1) 
            dzbir =  aop(iopk,4025,1) + aop(iopk,4026,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4027 = AOP-u (4025 + 4026)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40031
        if not( aop(iopk,4036,1) == aop(iopk,4034,1) + aop(iopk,4035,1) ):
            lzbir =  aop(iopk,4036,1) 
            dzbir =  aop(iopk,4034,1) + aop(iopk,4035,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4036 = AOP-u (4034 + 4035)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40032
        if not( aop(iopk,4045,1) == aop(iopk,4043,1) + aop(iopk,4044,1) ):
            lzbir =  aop(iopk,4045,1) 
            dzbir =  aop(iopk,4043,1) + aop(iopk,4044,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4045 = AOP-u (4043 + 4044)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40033
        if not( aop(iopk,4054,1) == aop(iopk,4052,1) + aop(iopk,4053,1) ):
            lzbir =  aop(iopk,4054,1) 
            dzbir =  aop(iopk,4052,1) + aop(iopk,4053,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4054 = AOP-u (4052 + 4053)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40034
        if not( aop(iopk,4063,1) == aop(iopk,4061,1) + aop(iopk,4062,1) ):
            lzbir =  aop(iopk,4063,1) 
            dzbir =  aop(iopk,4061,1) + aop(iopk,4062,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4063 = AOP-u (4061 + 4062)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40035
        if not( aop(iopk,4072,1) == aop(iopk,4070,1) + aop(iopk,4071,1) ):
            lzbir =  aop(iopk,4072,1) 
            dzbir =  aop(iopk,4070,1) + aop(iopk,4071,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4072 = AOP-u (4070 + 4071)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40036
        if not( suma(iopk, 4064, 4072, 1) == 0 ):
            lzbir =  suma(iopk, 4064, 4072, 1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='Zbir AOP-a (4064 do 4072) = 0 Učešće bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        #40037
        if( suma_liste(iopk,[4001,4010,4019,4028,4037,4046,4064],1)-aop(iopk,4055,1) > 0 ):
            if not( aop(iopk,4073,1) == suma_liste(iopk,[4001,4010,4019,4028,4037,4046,4064],1)-aop(iopk,4055,1) ):
                lzbir =  aop(iopk,4073,1) 
                dzbir =  suma_liste(iopk,[4001,4010,4019,4028,4037,4046,4064],1)-aop(iopk,4055,1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4073 = AOP-u (4001 + 4010 + 4019 + 4028 + 4037 + 4046 - 4055 + 4064), ako je AOP (4001 + 4010 + 4019 + 4028 + 4037 + 4046 -4055 + 4064) > 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40038
        if( suma_liste(iopk,[4001,4010,4019,4028,4037,4046,4064],1)-aop(iopk,4055,1) < 0 ):
            if not( aop(iopk,4082,1) == aop(iopk,4055,1)-suma_liste(iopk,[4001,4010,4019,4028,4037,4046,4064],1) ):
                lzbir =  aop(iopk,4082,1) 
                dzbir =  aop(iopk,4055,1)-suma_liste(iopk,[4001,4010,4019,4028,4037,4046,4064],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4082 = AOP-u (4055 - 4001 - 4010 - 4019 - 4028 - 4037 - 4046 - 4064), ako je AOP (4001 + 4010 + 4019 + 4028 + 4037 + 4046 - 4055 + 4064) < 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40039
        if( suma_liste(iopk,[4001,4010,4019,4028,4037,4046,4064],1)-aop(iopk,4055,1) == 0 ):
            if not( aop(iopk,4073,1) + aop(iopk,4082,1) == 0 ):
                lzbir =  aop(iopk,4073,1) + aop(iopk,4082,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP (4073 + 4082) = 0, ako je AOP (4001 + 4010 + 4019 + 4028 + 4037 + 4046 - 4055 + 4064) = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40040
        if( aop(iopk,4073,1) > 0 ):
            if not( aop(iopk,4082,1) == 0 ):
                lzbir =  aop(iopk,4082,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4073 > 0 onda je AOP 4082 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40041
        if( aop(iopk,4082,1) > 0 ):
            if not( aop(iopk,4073,1) == 0 ):
                lzbir =  aop(iopk,4073,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4082 > 0 onda je AOP 4073 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40042
        if not( aop(iopk,4074,1) == 0 ):
            lzbir =  aop(iopk,4074,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4074 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40043
        if not( aop(iopk,4083,1) == 0 ):
            lzbir =  aop(iopk,4083,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4083 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40044
        if( suma_liste(iopk,[4003,4012,4021,4030,4039,4048,4066],1)-aop(iopk,4057,1) > 0 ):
            if not( aop(iopk,4075,1) == suma_liste(iopk,[4003,4012,4021,4030,4039,4048,4066],1)-aop(iopk,4057,1) ):
                lzbir =  aop(iopk,4075,1) 
                dzbir =  suma_liste(iopk,[4003,4012,4021,4030,4039,4048,4066],1)-aop(iopk,4057,1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4075 = AOP-u (4003 + 4012 + 4021 + 4030 + 4039 + 4048 - 4057 + 4066), ako je AOP (4003 + 4012 + 4021 + 4030 + 4039 + 4048 - 4057 + 4066) > 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40045
        if( suma_liste(iopk,[4003,4012,4021,4030,4039,4048,4066],1)-aop(iopk,4057,1) < 0 ):
            if not( aop(iopk,4084,1) == aop(iopk,4057,1)-suma_liste(iopk,[4003,4012,4021,4030,4039,4048,4066],1) ):
                lzbir =  aop(iopk,4084,1) 
                dzbir =  aop(iopk,4057,1)-suma_liste(iopk,[4003,4012,4021,4030,4039,4048,4066],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4084 = AOP-u (4057 - 4003 - 4012 - 4021 - 4030 - 4039 - 4048 - 4066), ako je AOP (4003 + 4012 + 4021 + 4030 + 4039 + 4048 - 4057 + 4066) < 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40046
        if( suma_liste(iopk,[4003,4012,4021,4030,4039,4048,4066],1)-aop(iopk,4057,1) == 0 ):
            if not( aop(iopk,4075,1) + aop(iopk,4084,1) == 0 ):
                lzbir =  aop(iopk,4075,1) + aop(iopk,4084,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP (4075 + 4084) = 0, ako je AOP (4003 + 4012 + 4021 + 4030 + 4039 + 4048 - 4057 + 4066) = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40047
        if( aop(iopk,4075,1) > 0 ):
            if not( aop(iopk,4084,1) == 0 ):
                lzbir =  aop(iopk,4084,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4075 > 0 onda je AOP 4084 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40048
        if( aop(iopk,4084,1) > 0 ):
            if not( aop(iopk,4075,1) == 0 ):
                lzbir =  aop(iopk,4075,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4084 > 0 onda je AOP 4075 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40049
        if not( aop(iopk,4076,1) == 0 ):
            lzbir =  aop(iopk,4076,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4076 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40050
        if not( aop(iopk,4085,1) == 0 ):
            lzbir =  aop(iopk,4085,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4085 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40051
        if( suma_liste(iopk,[4005,4014,4023,4032,4041,4050,4068],1)-aop(iopk,4059,1) > 0 ):
            if not( aop(iopk,4077,1) == suma_liste(iopk,[4005,4014,4023,4032,4041,4050,4068],1)-aop(iopk,4059,1) ):
                lzbir =  aop(iopk,4077,1) 
                dzbir =  suma_liste(iopk,[4005,4014,4023,4032,4041,4050,4068],1)-aop(iopk,4059,1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4077 = AOP-u (4005 + 4014 + 4023 + 4032 + 4041 + 4050 - 4059 + 4068), ako je AOP (4005 + 4014 + 4023 + 4032 + 4041 + 4050 - 4059 + 4068) > 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40052
        if( suma_liste(iopk,[4005,4014,4023,4032,4041,4050,4068],1)-aop(iopk,4059,1) < 0 ):
            if not( aop(iopk,4086,1) == aop(iopk,4059,1)-suma_liste(iopk,[4005,4014,4023,4032,4041,4050,4068],1) ):
                lzbir =  aop(iopk,4086,1) 
                dzbir =  aop(iopk,4059,1)-suma_liste(iopk,[4005,4014,4023,4032,4041,4050,4068],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4086 = AOP-u (4059 - 4005 - 4014 - 4023 - 4032 - 4041 - 4050 - 4068), ako je AOP (4005 + 4014 + 4023 + 4032 + 4041 + 4050 - 4059 + 4068) < 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40053
        if( suma_liste(iopk,[4005,4014,4023,4032,4041,4050,4068],1)-aop(iopk,4059,1) == 0 ):
            if not( aop(iopk,4077,1) + aop(iopk,4086,1) == 0 ):
                lzbir =  aop(iopk,4077,1) + aop(iopk,4086,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP (4077 + 4086) = 0, ako je AOP (4005 + 4014 + 4023 + 4032 + 4041 + 4050 - 4059 + 4068) = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40054
        if( aop(iopk,4077,1) > 0 ):
            if not( aop(iopk,4086,1) == 0 ):
                lzbir =  aop(iopk,4086,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4077 > 0 onda je AOP 4086 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40055
        if( aop(iopk,4086,1) > 0 ):
            if not( aop(iopk,4077,1) == 0 ):
                lzbir =  aop(iopk,4077,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4086 > 0 onda je AOP 4077 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40056
        if not( aop(iopk,4078,1) == 0 ):
            lzbir =  aop(iopk,4078,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4078 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40057
        if not( aop(iopk,4087,1) == 0 ):
            lzbir =  aop(iopk,4087,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4087 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40058
        if( suma_liste(iopk,[4007,4016,4025,4034,4043,4052,4070],1)-aop(iopk,4061,1) > 0 ):
            if not( aop(iopk,4079,1) == suma_liste(iopk,[4007,4016,4025,4034,4043,4052,4070],1)-aop(iopk,4061,1) ):
                lzbir =  aop(iopk,4079,1) 
                dzbir =  suma_liste(iopk,[4007,4016,4025,4034,4043,4052,4070],1)-aop(iopk,4061,1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4079 = AOP-u (4007 + 4016 + 4025 + 4034 + 4043 + 4052 - 4061 + 4070), ako je AOP (4007 + 4016 + 4025 + 4034 + 4043 + 4052 - 4061 + 4070) > 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40059
        if( suma_liste(iopk,[4007,4016,4025,4034,4043,4052,4070],1)-aop(iopk,4061,1) < 0 ):
            if not( aop(iopk,4088,1) == aop(iopk,4061,1)-suma_liste(iopk,[4007,4016,4025,4034,4043,4052,4070],1) ):
                lzbir =  aop(iopk,4088,1) 
                dzbir =  aop(iopk,4061,1)-suma_liste(iopk,[4007,4016,4025,4034,4043,4052,4070],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4088 = AOP-u (4061 - 4007 - 4016 - 4025 - 4034 - 4043 - 4052 - 4070), ako je AOP (4007 + 4016 + 4025 + 4034 + 4043 + 4052 - 4061 + 4070) < 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40060
        if( suma_liste(iopk,[4007,4016,4025,4034,4043,4052,4070],1)-aop(iopk,4061,1) == 0 ):
            if not( aop(iopk,4079,1) + aop(iopk,4088,1) == 0 ):
                lzbir =  aop(iopk,4079,1) + aop(iopk,4088,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP (4079 + 4088) = 0, ako je AOP (4007 + 4016 + 4025 + 4034 + 4043 + 4052 - 4061 + 4070) = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40061
        if( aop(iopk,4079,1) > 0 ):
            if not( aop(iopk,4088,1) == 0 ):
                lzbir =  aop(iopk,4088,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4079 > 0 onda je AOP 4088 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40062
        if( aop(iopk,4088,1) > 0 ):
            if not( aop(iopk,4079,1) == 0 ):
                lzbir =  aop(iopk,4079,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4088 > 0 onda je AOP 4079 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40063
        if not( aop(iopk,4080,1) == 0 ):
            lzbir =  aop(iopk,4080,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4080 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40064
        if not( aop(iopk,4089,1) == 0 ):
            lzbir =  aop(iopk,4089,1) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4089 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40065
        if( suma_liste(iopk,[4009,4018,4027,4036,4045,4054,4072],1)-aop(iopk,4063,1) > 0 ):
            if not( aop(iopk,4081,1) == suma_liste(iopk,[4009,4018,4027,4036,4045,4054,4072],1)-aop(iopk,4063,1) ):
                lzbir =  aop(iopk,4081,1) 
                dzbir =  suma_liste(iopk,[4009,4018,4027,4036,4045,4054,4072],1)-aop(iopk,4063,1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4081 = AOP-u (4009 + 4018 + 4027 + 4036 + 4045 + 4054 - 4063 + 4072), ako je AOP (4009 + 4018 + 4027 + 4036 + 4045 + 4054 - 4063 + 4072) > 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40066
        if( suma_liste(iopk,[4009,4018,4027,4036,4045,4054,4072],1)-aop(iopk,4063,1) < 0 ):
            if not( aop(iopk,4090,1) == aop(iopk,4063,1)-suma_liste(iopk,[4009,4018,4027,4036,4045,4054,4072],1) ):
                lzbir =  aop(iopk,4090,1) 
                dzbir =  aop(iopk,4063,1)-suma_liste(iopk,[4009,4018,4027,4036,4045,4054,4072],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4090 = AOP-u (4063 - 4009 - 4018 - 4027 - 4036 - 4045 - 4054 - 4072), ako je AOP (4009 + 4018 + 4027 + 4036 + 4045 + 4054 - 4063 + 4072) < 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40067
        if( suma_liste(iopk,[4009,4018,4027,4036,4045,4054,4072],1)-aop(iopk,4063,1) == 0 ):
            if not( aop(iopk,4081,1) + aop(iopk,4090,1) == 0 ):
                lzbir =  aop(iopk,4081,1) + aop(iopk,4090,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP (4081 + 4090) = 0, ako je AOP (4009 + 4018 + 4027 + 4036 + 4045 + 4054 - 4063 + 4072) = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40068
        if( aop(iopk,4081,1) > 0 ):
            if not( aop(iopk,4090,1) == 0 ):
                lzbir =  aop(iopk,4090,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4081 > 0 onda je AOP 4090 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40069
        if( aop(iopk,4090,1) > 0 ):
            if not( aop(iopk,4081,1) == 0 ):
                lzbir =  aop(iopk,4081,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4090 > 0 onda je AOP 4081 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40070
        if not( aop(iopk,4003,1) + aop(iopk,4012,1) == aop(bs,402,7) ):
            lzbir =  aop(iopk,4003,1) + aop(iopk,4012,1) 
            dzbir =  aop(bs,402,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP (4003 + 4012)  = AOP-u 0402 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP (4003 + 4012)  = AOP-u 0402 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40071
        if not( aop(iopk,4005,1) + aop(iopk,4014,1) == aop(bs,402,6) ):
            lzbir =  aop(iopk,4005,1) + aop(iopk,4014,1) 
            dzbir =  aop(bs,402,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP (4005 + 4014)  = AOP-u 0402 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP (4005 + 4014)  = AOP-u 0402 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40072
        if not( aop(iopk,4009,1) + aop(iopk,4018,1) == aop(bs,402,5) ):
            lzbir =  aop(iopk,4009,1) + aop(iopk,4018,1) 
            dzbir =  aop(bs,402,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP (4009 + 4018)  = AOP-u 0402 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP (4009 + 4018)  = AOP-u 0402 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40073
        if not( aop(iopk,4021,1) == aop(bs,403,7) ):
            lzbir =  aop(iopk,4021,1) 
            dzbir =  aop(bs,403,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4021 = AOP-u 0403 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4021 = AOP-u 0403 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40074
        if not( aop(iopk,4023,1) == aop(bs,403,6) ):
            lzbir =  aop(iopk,4023,1) 
            dzbir =  aop(bs,403,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4023 = AOP-u 0403 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4023 = AOP-u 0403 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40075
        if not( aop(iopk,4027,1) == aop(bs,403,5) ):
            lzbir =  aop(iopk,4027,1) 
            dzbir =  aop(bs,403,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4027 = AOP-u 0403 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4027 = AOP-u 0403 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40076
        if not( aop(iopk,4030,1) == suma(bs,404,405,7) ):
            lzbir =  aop(iopk,4030,1) 
            dzbir =  suma(bs,404,405,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4030 = AOP-u (0404 + 0405) kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4030 = AOP-u (0404 + 0405) kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40077
        if not( aop(iopk,4032,1) == suma(bs,404,405,6) ):
            lzbir =  aop(iopk,4032,1) 
            dzbir =  suma(bs,404,405,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4032 = AOP-u (0404 + 0405) kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4032 = AOP-u (0404 + 0405) kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40078
        if not( aop(iopk,4036,1) == suma(bs,404,405,5) ):
            lzbir =  aop(iopk,4036,1) 
            dzbir =  suma(bs,404,405,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4036 = AOP-u (0404 + 0405) kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4036 = AOP-u (0404 + 0405) kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40079
        if not( aop(iopk,4039,1) == aop(bs,406,7)-aop(bs,407,7) ):
            lzbir =  aop(iopk,4039,1) 
            dzbir =  aop(bs,406,7)-aop(bs,407,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4039 = AOP-u (0406 - 0407) kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4039 = AOP-u (0406 - 0407) kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40080
        if not( aop(iopk,4041,1) == aop(bs,406,6)-aop(bs,407,6) ):
            lzbir =  aop(iopk,4041,1) 
            dzbir =  aop(bs,406,6)-aop(bs,407,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4041 = AOP-u (0406 - 0407) kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4041 = AOP-u (0406 - 0407) kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40081
        if not( aop(iopk,4045,1) == aop(bs,406,5)-aop(bs,407,5) ):
            lzbir =  aop(iopk,4045,1) 
            dzbir =  aop(bs,406,5)-aop(bs,407,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4045 = AOP-u (0406 - 0407) kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4045 = AOP-u (0406 - 0407) kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40082
        if not( aop(iopk,4048,1) == aop(bs,408,7) ):
            lzbir =  aop(iopk,4048,1) 
            dzbir =  aop(bs,408,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4048 = AOP-u 0408 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4048 = AOP-u 0408 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40083
        if not( aop(iopk,4050,1) == aop(bs,408,6) ):
            lzbir =  aop(iopk,4050,1) 
            dzbir =  aop(bs,408,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4050 = AOP-u 0408 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4050 = AOP-u 0408 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40084
        if not( aop(iopk,4054,1) == aop(bs,408,5) ):
            lzbir =  aop(iopk,4054,1) 
            dzbir =  aop(bs,408,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4054 = AOP-u 0408 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4054 = AOP-u 0408 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40085
        if not( aop(iopk,4057,1) == aop(bs,412,7) ):
            lzbir =  aop(iopk,4057,1) 
            dzbir =  aop(bs,412,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4057 = AOP-u 0412 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4057 = AOP-u 0412 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40086
        if not( aop(iopk,4059,1) == aop(bs,412,6) ):
            lzbir =  aop(iopk,4059,1) 
            dzbir =  aop(bs,412,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4059 = AOP-u 0412 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4059 = AOP-u 0412 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40087
        if not( aop(iopk,4063,1) == aop(bs,412,5) ):
            lzbir =  aop(iopk,4063,1) 
            dzbir =  aop(bs,412,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4063 = AOP-u 0412 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4063 = AOP-u 0412 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40088
        #Za ovaj set se ne primenjuje pravilo 
        #40089
        #Za ovaj set se ne primenjuje pravilo 
        #40090
        #Za ovaj set se ne primenjuje pravilo 
        #40091
        if not( aop(iopk,4075,1) == aop(bs,401,7) ):
            lzbir =  aop(iopk,4075,1) 
            dzbir =  aop(bs,401,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4075 = AOP-u 0401 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4075 = AOP-u 0401 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40092
        if not( aop(iopk,4077,1) == aop(bs,401,6) ):
            lzbir =  aop(iopk,4077,1) 
            dzbir =  aop(bs,401,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4077 = AOP-u 0401 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4077 = AOP-u 0401 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40093
        if not( aop(iopk,4081,1) == aop(bs,401,5) ):
            lzbir =  aop(iopk,4081,1) 
            dzbir =  aop(bs,401,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4081 = AOP-u 0401 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4081 = AOP-u 0401 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40094
        if not( aop(iopk,4084,1) == aop(bs,455,7) ):
            lzbir =  aop(iopk,4084,1) 
            dzbir =  aop(bs,455,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4084 = AOP-u 0455 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4084 = AOP-u 0455 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40095
        if not( aop(iopk,4086,1) == aop(bs,455,6) ):
            lzbir =  aop(iopk,4086,1) 
            dzbir =  aop(bs,455,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4086 = AOP-u 0455 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4086 = AOP-u 0455 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40096
        if not( aop(iopk,4090,1) == aop(bs,455,5) ):
            lzbir =  aop(iopk,4090,1) 
            dzbir =  aop(bs,455,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4090 = AOP-u 0455 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4090 = AOP-u 0455 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #STATISTIČKI IZVEŠTAJ - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #90001
        if not( suma(si,9009,9015,4)+suma(si,9009,9015,5)+suma(si,9009,9015,6)+suma(si,9017,9022,4)+suma(si,9017,9022,5)+suma(si,9017,9022,6)+suma(si,9024,9030,4)+suma(si,9024,9030,5)+suma(si,9024,9030,6)+suma(si,9032,9037,4)+suma(si,9032,9037,5)+suma(si,9032,9037,6)+suma(si,9038,9062,4)+suma(si,9063,9071,3)+suma(si,9072,9118,4)+suma(si,9119,9126,3)+suma(si,9127,9136,4)+suma(si,9127,9136,5)+suma(si,9127,9136,6) > 0 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir podataka na oznakama za AOP (9009 do 9015) kol. 4 + (9009 do 9015) kol. 5 + (9009 do 9015) kol. 6 + (9017 do 9022) kol. 4 + (9017 do 9022) kol. 5 + (9017 do 9022) kol. 6 + (9024 do 9030) kol. 4 + (9024 do 9030) kol. 5 + (9024 do 9030) kol. 6 + (9032 do 9037) kol. 4 + (9032 do 9037) kol. 5 + (9032 do 9037) kol. 6 + (9038 do 9062) kol. 4 + (9063 do 9071) kol. 3 + (9072 do 9118) kol. 4 + (9119 do 9126) kol. 3 + (9127 do 9136) kol. 4 +  (9127 do 9136) kol. 5 + (9127 do 9136) kol. 6 > 0 Statistički izveštaj, po pravilu,  mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(si,9001,9007,4)+aop(si,9008,4)+aop(si,9008,5)+aop(si,9008,6)+aop(si,9016,4)+aop(si,9016,5)+aop(si,9016,6)+aop(si,9023,4)+aop(si,9023,5)+aop(si,9023,6)+aop(si,9031,4)+aop(si,9031,5)+aop(si,9031,6)+suma(si,9038,9062,5)+suma(si,9063,9071,4)+suma(si,9072,9118,5)+suma(si,9119,9126,4) == 0 ):
                lzbir =  suma(si,9001,9007,4)+aop(si,9008,4)+aop(si,9008,5)+aop(si,9008,6)+aop(si,9016,4)+aop(si,9016,5)+aop(si,9016,6)+aop(si,9023,4)+aop(si,9023,5)+aop(si,9023,6)+aop(si,9031,4)+aop(si,9031,5)+aop(si,9031,6)+suma(si,9038,9062,5)+suma(si,9063,9071,4)+suma(si,9072,9118,5)+suma(si,9119,9126,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Zbir podataka na oznakama za AOP (9001 do 9007) kol.4 + 9008 kol. 4 + 9008 kol. 5 + 9008 kol. 6 + 9016 kol. 4 + 9016 kol. 5 + 9016 kol. 6 + 9023 kol. 4 + 9023 kol. 5 + 9023 kol. 6 + 9031 kol. 4 + 9031 kol. 5 + 9031 kol. 6 + (9038 do 9062) kol. 5 + (9063 do 9071) kol. 4 + (9072 do 9118) kol. 5 + (9119 do 9126) kol. 4 = 0 Statistički izveštaj za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #90003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( aop(si,9008,4)+aop(si,9008,5)+aop(si,9008,6)+aop(si,9016,4)+aop(si,9016,5)+aop(si,9016,6)+aop(si,9023,4)+aop(si,9023,5)+aop(si,9023,6)+aop(si,9031,4)+aop(si,9031,5)+aop(si,9031,6)+suma(si,9038,9062,5)+suma(si,9063,9071,4)+suma(si,9072,9118,5)+suma(si,9119,9126,4) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Zbir podataka na oznakama za AOP 9008 kol. 4 + 9008 kol. 5 + 9008 kol. 6 + 9016 kol. 4 + 9016 kol. 5 + 9016 kol. 6 + 9023 kol. 4 + 9023 kol. 5 + 9023 kol. 6 + 9031 kol. 4 + 9031 kol. 5 + 9031 kol. 6 + (9038 do 9062) kol. 5 + (9063 do 9071) kol. 4 + (9072 do 9118) kol. 5 + (9119 do 9126) kol. 4 > 0 Statistički izveštaj, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period;Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90004 dva uslova
        if not( aop(si, 9001, 3) >= 1 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='1 ≤ AOP-a 9001 kol. 3 ≤ 12  Broj meseci poslovanja obveznika mora biti iskazan u intervalu između 1 i 12; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        if not( aop(si, 9001, 3) <= 12 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='1 ≤ AOP-a 9001 kol. 3 ≤ 12  Broj meseci poslovanja obveznika mora biti iskazan u intervalu između 1 i 12; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        #90005
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( aop(si, 9001, 4) >= 1 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='1 ≤ AOP-a 9001 kol. 4 ≤ 12  Broj meseci poslovanja obveznika osnovanih u ranijim godinama, po pravilu, mora biti iskazan u intervalu između 1 i 12; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( aop(si, 9001, 4) <= 12 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='1 ≤ AOP-a 9001 kol. 4 ≤ 12  Broj meseci poslovanja obveznika osnovanih u ranijim godinama, po pravilu, mora biti iskazan u intervalu između 1 i 12; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
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
                poruka  ='AOP 9001 kol. 3 = 12 Broj meseci poslovanja obveznika osnovanih ranijih godina mora biti 12, osim za obveznike koji su kupljeni iz stečaja '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #90007 duplo pravilo
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if not( aop(si, 9002, 3) >= 1 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='1 ≤ AOP-a 9002 kol. 3 ≤ 5  Oznaka za vlasništvo mora biti iskazana u intervalu između 1 i 5; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if not( aop(si, 9002, 3) <=5 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='1 ≤ AOP-a 9002 kol. 3 ≤ 5  Oznaka za vlasništvo mora biti iskazana u intervalu između 1 i 5; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

        #90008 duplo pravilo
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if(Zahtev.ObveznikInfo.Novoosnovan == False): 
                if not( aop(si, 9002, 4) >= 1  ):
                    
                    naziv_obrasca='Statistički izveštaj'
                    poruka  ='1 ≤ AOP-a 9002 kol. 4 ≤ 5  Oznaka za vlasništvo, po pravilu, mora biti iskazana u intervalu između 1 i 5; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
        
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if(Zahtev.ObveznikInfo.Novoosnovan == False): 
                if not( aop(si, 9002, 4) <= 5  ):
                    
                    naziv_obrasca='Statistički izveštaj'
                    poruka  ='1 ≤ AOP-a 9002 kol. 4 ≤ 5  Oznaka za vlasništvo, po pravilu, mora biti iskazana u intervalu između 1 i 5; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

        #90009
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if not(aop(si, 9002, 3) == 2):
                lzbir =  aop(si,9002,3) 
                dzbir =  2 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='AOP 9002 kol. 3 = 2 Oznaka za vlasništvo kod preduzetnika mora biti obavezno 2 (privatno ) '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

        #90010
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if(Zahtev.ObveznikInfo.Novoosnovan == False):
                if not(aop(si, 9002, 4) == 2):
                    lzbir =  aop(si,9002,4) 
                    dzbir =  2 
                    razlika = lzbir - dzbir
                    
                    naziv_obrasca='Statistički izveštaj'
                    poruka  ='AOP 9002 kol. 4 = 2 Oznaka za vlasništvo kod preduzetnika mora biti obavezno 2 (privatno );  Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga'+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
            
        #90011
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if( aop(si,9003,3) > 0 ):
                if not( suma_liste(si,[9046,9048,9050],4) > 0 ):
                    
                    naziv_obrasca='Statistički izveštaj'
                    poruka  ='Ako je AOP 9003 kol. 3 > 0, onda je zbir AOP-a (9046 + 9048 + 9050) kol. 4 > 0 Ukoliko u kapitalu učestvuju strana lica, mora biti iskazana vrednost stranog kapitala, ako je veća od 500,00 RSD; Ukoliko podaci o vrednosti kapitala nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje da je vrednost tog kapitala manja od 500,00 RSD '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
            
        #90012
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if( suma_liste(si,[9046,9048,9050],4) > 0 ):
                if not( aop(si,9003,3) > 0 ):
                    
                    naziv_obrasca='Statistički izveštaj'
                    poruka  ='Ako je zbir AOP-a (9046 + 9048 + 9050) kol. 4 > 0 onda je AOP 9003 kol. 3 > 0 Ukoliko je iskazana vrednost stranog kapitala, obveznik mora iskazati broj stranih lica koja učestvuju u kapitalu; '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
        
        #90013
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if( aop(si,9003,4) > 0 ):
                if not( suma_liste(si,[9046,9048,9050],5) > 0 ):
                    
                    naziv_obrasca='Statistički izveštaj'
                    poruka  ='Ako je AOP 9003 kol. 4 > 0, onda je zbir AOP-a (9046 + 9048 + 9050) kol. 5 > 0  Ukoliko u kapitalu učestvuju strana lica, mora biti iskazana vrednost stranog kapitala, ako je veća od 500,00 RSD; Ukoliko podaci o vrednosti kapitala nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje da je vrednost tog kapitala manja od 500,00 RSD '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
            
        #90014
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if( suma_liste(si,[9046,9048,9050],5) > 0 ):
                if not( aop(si,9003,4) > 0 ):
                    
                    naziv_obrasca='Statistički izveštaj'
                    poruka  ='Ako je zbir AOP-a (9046 + 9048 + 9050) kol. 5 > 0 onda je AOP 9003 kol. 4 > 0 Ukoliko je iskazana vrednost stranog kapitala, obveznik mora iskazati broj stranih lica koja učestvuju u kapitalu; '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
        #90015
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if not( aop(si,9004,3) <= aop(si,9003,3) ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='AOP 9004 kol. 3 ≤ AOP-a 9003 kol. 3  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
        #90016
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if not( aop(si,9004,4) <= aop(si,9003,4) ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='AOP 9004 kol. 4 ≤ AOP-a 9003 kol. 4  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
        #90017
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if not(aop(si, 9004, 3) == 0):
                lzbir =  aop(si,9004,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='AOP 9004 kol. 3 = 0 Učešće stranog kapitala u preduzetničkoj radnji ne može biti manje od 100% '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

        #90018
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if not(aop(si, 9004, 4) == 0):
                lzbir =  aop(si,9004,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='AOP 9004 kol. 4 = 0 Učešće stranog kapitala u preduzetničkoj radnji ne može biti manje od 100% '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

        #90019
        if not( aop(si,9005,3) > 0 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9005 kol. 3 > 0 Na poziciji Prosečan broj zaposlenih nije iskazan podatak; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90020
        if( aop(si,9005,3) > 0 ):
            if not( suma(si,9074,9076,4) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP 9005 kol. 3 > 0, onda je AOP (9074 + 9075 + 9076) kol. 4 > 0 Ukoliko je iskazan prosečan broj zaposlenih, obveznik, po pravilu, mora imati iskazane obaveze po osnovu bruto zarada; Ukoliko jedan od navedenih podataka nije prikazan, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90021
        if( suma(si,9074,9076,4) > 0 ):
            if not( aop(si,9005,3) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP (9074 + 9075 + 9076) kol. 4 > 0, onda je AOP 9005 kol. 3 > 0 Ukoliko su iskazane obaveze po osnovu bruto zarada, obveznik, po pravilu, mora imati iskazan prosečan broj zaposlenih; Ukoliko jedan od navedenih podataka nije prikazan, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90022
        if( aop(si,9005,4) > 0 ):
            if not( suma(si,9074,9076,5) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP 9005 kol. 4 > 0, onda je AOP (9074 + 9075 + 9076) kol. 5 > 0 Ukoliko je iskazan prosečan broj zaposlenih, obveznik, po pravilu, mora imati iskazane obaveze po osnovu bruto zarada; Ukoliko jedan od navedenih podataka nije prikazan, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90023
        if( suma(si,9074,9076,5) > 0 ):
            if not( aop(si,9005,4) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je  AOP (9074 + 9075 + 9076) kol. 5 > 0, onda je AOP 9005 kol. 4 > 0 Ukoliko su iskazane obaveze po osnovu bruto zarada, obveznik, po pravilu, mora imati iskazan prosečan broj zaposlenih; Ukoliko jedan od navedenih podataka nije prikazan, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90024
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if not( aop(si,9005,3) <= 1000 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='AOP 9005 kol. 3 ≤ 1000 Granične vrednosti date su da bi se izbegle slučajne greške prilikom iskazivanja broja zaposlenih; Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

        #90025
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if not( aop(si,9005,4) <= 1000 ) :
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='AOP 9005 kol. 4 ≤ 1000 Granične vrednosti date su da bi se izbegle slučajne greške prilikom iskazivanja broja zaposlenih; Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

        #90026
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if not(aop(si, 9005, 3) <= 50):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='AOP 9005 kol. 3 ≤ 50 Granične vrednosti date su da bi se izbegle slučajne greške prilikom iskazivanja broja zaposlenih; Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
 
        #90027
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if not(aop(si, 9005, 4) <= 50):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='AOP 9005 kol. 4 ≤ 50 Granične vrednosti date su da bi se izbegle slučajne greške prilikom iskazivanja broja zaposlenih; Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
 
        #90028
        if not( aop(si,9006,3) > 0 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9006 kol. 3 > 0 Na poziciji Broj zaposlenih preko agencija i organizacija za zapošljavanje nije iskazan podatak; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90029
        if not( aop(si,9006,3) <= 50 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9006 kol. 3 ≤ 50 Granične vrednosti date su da bi se izbegle slučajne greške prilikom iskazivanja broja zaposlenih preko agencija i organizacija za zapošljavanje;Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90030
        if not( aop(si,9006,4) <= 50 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9006 kol. 4 ≤ 50 Granične vrednosti date su da bi se izbegle slučajne greške prilikom iskazivanja broja zaposlenih preko agencija i organizacija za zapošljavanje;Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90031
        if not( aop(si,9007,3) > 0 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9007 kol. 3 > 0 Na poziciji Prosečan broj volontera  nije iskazan podatak; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90032
        if not( aop(si,9007,3) <= 50 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9007 kol. 3 ≤ 50 Granične vrednosti date su da bi se izbegle slučajne greške prilikom iskazivanja broja volontera; Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90033
        if not( aop(si,9007,4) <= 50 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9007 kol. 4 ≤ 50 Granične vrednosti date su da bi se izbegle slučajne greške prilikom iskazivanja broja volontera; Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90034
        if not( aop(si,9008,6) == aop(si,9008,4)-aop(si,9008,5) ):
            lzbir =  aop(si,9008,6) 
            dzbir =  aop(si,9008,4)-aop(si,9008,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9008 kol. 6 = AOP-u 9008 kol. 4 - AOP 9008 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90035
        if not( aop(si,9015,6) == aop(si,9015,4)-aop(si,9015,5) ):
            lzbir =  aop(si,9015,6) 
            dzbir =  aop(si,9015,4)-aop(si,9015,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9015 kol. 6 = AOP-u 9015 kol. 4 - AOP 9015 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90036
        if not( aop(si,9016,6) == aop(si,9016,4)-aop(si,9016,5) ):
            lzbir =  aop(si,9016,6) 
            dzbir =  aop(si,9016,4)-aop(si,9016,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9016 kol. 6 = AOP-u 9016 kol. 4 - AOP 9016 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90037
        if not( aop(si,9022,6) == aop(si,9022,4)-aop(si,9022,5) ):
            lzbir =  aop(si,9022,6) 
            dzbir =  aop(si,9022,4)-aop(si,9022,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9022 kol. 6 = AOP-u 9022 kol. 4 - AOP 9022 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90038
        if not( aop(si,9023,6) == aop(si,9023,4)-aop(si,9023,5) ):
            lzbir =  aop(si,9023,6) 
            dzbir =  aop(si,9023,4)-aop(si,9023,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9023 kol. 6 = AOP-u 9023 kol. 4 - AOP 9023 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90039
        if not( aop(si,9030,6) == aop(si,9030,4)-aop(si,9030,5) ):
            lzbir =  aop(si,9030,6) 
            dzbir =  aop(si,9030,4)-aop(si,9030,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9030 kol. 6 = AOP-u 9030 kol. 4 - AOP 9030 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90040
        if not( aop(si,9031,6) == aop(si,9031,4)-aop(si,9031,5) ):
            lzbir =  aop(si,9031,6) 
            dzbir =  aop(si,9031,4)-aop(si,9031,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9031 kol. 6 = AOP-u 9031 kol. 4 - AOP 9031 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90041
        if not( aop(si,9037,6) == aop(si,9037,4)-aop(si,9037,5) ):
            lzbir =  aop(si,9037,6) 
            dzbir =  aop(si,9037,4)-aop(si,9037,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9037 kol. 6 = AOP-u 9037 kol. 4 - AOP 9037 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90042
        if not( aop(si,9015,4) == suma_liste(si,[9008,9009,9010,9011,9013,9014],4)-aop(si,9012,4) ):
            lzbir =  aop(si,9015,4) 
            dzbir =  suma_liste(si,[9008,9009,9010,9011,9013,9014],4)-aop(si,9012,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9015 kol. 4 = AOP-u (9008 + 9009 + 9010 + 9011 - 9012 + 9013 + 9014) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90043
        if not( aop(si,9015,5) == suma_liste(si,[9008,9009,9010,9011,9013,9014],5)-aop(si,9012,5) ):
            lzbir =  aop(si,9015,5) 
            dzbir =  suma_liste(si,[9008,9009,9010,9011,9013,9014],5)-aop(si,9012,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9015 kol. 5 = AOP-u (9008 + 9009 + 9010 + 9011 - 9012 + 9013 + 9014) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90044
        if not( aop(si,9013,4) == 0 ):
            lzbir =  aop(si,9013,4) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9013 kol. 4 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90045
        if not( aop(si,9013,6) == 0 ):
            lzbir =  aop(si,9013,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9013 kol. 6 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90046
        if not( aop(si,9022,4) == suma_liste(si,[9016,9017,9018,9020,9021],4)-aop(si,9019,4) ):
            lzbir =  aop(si,9022,4) 
            dzbir =  suma_liste(si,[9016,9017,9018,9020,9021],4)-aop(si,9019,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9022 kol. 4 = AOP-u (9016 + 9017 + 9018 - 9019 + 9020 + 9021) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90047
        if not( aop(si,9022,5) == suma_liste(si,[9016,9017,9018,9020,9021],5)-aop(si,9019,5) ):
            lzbir =  aop(si,9022,5) 
            dzbir =  suma_liste(si,[9016,9017,9018,9020,9021],5)-aop(si,9019,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9022 kol. 5 = AOP-u (9016 + 9017 + 9018 - 9019 + 9020 + 9021) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90048
        if not( aop(si,9020,4) == 0 ):
            lzbir =  aop(si,9020,4) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9020 kol. 4 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90049
        if not( aop(si,9020,6) == 0 ):
            lzbir =  aop(si,9020,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9020 kol. 6 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90050
        if not( aop(si,9030,4) == suma_liste(si,[9023,9024,9025,9026,9028,9029],4)-aop(si,9027,4) ):
            lzbir =  aop(si,9030,4) 
            dzbir =  suma_liste(si,[9023,9024,9025,9026,9028,9029],4)-aop(si,9027,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9030 kol. 4 = AOP-u (9023 + 9024 + 9025 + 9026 - 9027 + 9028 + 9029) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90051
        if not( aop(si,9030,5) == suma_liste(si,[9023,9024,9025,9026,9028,9029],5)-aop(si,9027,5) ):
            lzbir =  aop(si,9030,5) 
            dzbir =  suma_liste(si,[9023,9024,9025,9026,9028,9029],5)-aop(si,9027,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9030 kol. 5 = AOP-u (9023 + 9024 + 9025 + 9026 - 9027 + 9028 + 9029) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90052
        if not( aop(si,9028,4) == 0 ):
            lzbir =  aop(si,9028,4) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9028 kol. 4 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90053
        if not( aop(si,9028,6) == 0 ):
            lzbir =  aop(si,9028,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9028 kol. 6 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90054
        if not( aop(si,9037,4) == suma_liste(si,[9031,9032,9033,9035,9036],4)-aop(si,9034,4) ):
            lzbir =  aop(si,9037,4) 
            dzbir =  suma_liste(si,[9031,9032,9033,9035,9036],4)-aop(si,9034,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9037 kol. 4 = AOP-u (9031 + 9032 + 9033 - 9034 + 9035 + 9036) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90055
        if not( aop(si,9037,5) == suma_liste(si,[9031,9032,9033,9035,9036],5)-aop(si,9034,5) ):
            lzbir =  aop(si,9037,5) 
            dzbir =  suma_liste(si,[9031,9032,9033,9035,9036],5)-aop(si,9034,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9037 kol. 5 = AOP-u (9031 + 9032 + 9033 - 9034 + 9035 + 9036) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90056
        if not( aop(si,9035,4) == 0 ):
            lzbir =  aop(si,9035,4) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9035 kol. 4 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90057
        if not( aop(si,9035,6) == 0 ):
            lzbir =  aop(si,9035,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9035 kol. 6 = 0  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90058
        if not( aop(si,9008,6) == aop(bs,3,6) ):
            lzbir =  aop(si,9008,6) 
            dzbir =  aop(bs,3,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9008 kol. 6 = AOP-u 0003 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9008 kol. 6 = AOP-u 0003 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90059
        if not( aop(si,9015,6) == aop(bs,3,5) ):
            lzbir =  aop(si,9015,6) 
            dzbir =  aop(bs,3,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9015 kol. 6 = AOP-u 0003 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9015 kol. 6 = AOP-u 0003 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90060
        if not( suma_liste(si,[9016,9023],6) == aop(bs,9,6) ):
            lzbir =  suma_liste(si,[9016,9023],6) 
            dzbir =  aop(bs,9,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir AOP-a (9016 + 9023) kol. 6 = AOP-u 0009 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir AOP-a (9016 + 9023) kol. 6 = AOP-u 0009 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90061
        if not( suma_liste(si,[9022,9030],6) == aop(bs,9,5) ):
            lzbir =  suma_liste(si,[9022,9030],6) 
            dzbir =  aop(bs,9,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Znir AOP-a (9022 + 9030) kol. 6 = AOP-u 0009 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Znir AOP-a (9022 + 9030) kol. 6 = AOP-u 0009 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90062
        if not( aop(si,9031,6) == aop(bs,17,6) ):
            lzbir =  aop(si,9031,6) 
            dzbir =  aop(bs,17,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9031 kol. 6 = AOP-u 0017 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9031 kol. 6 = AOP-u 0017 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90063
        if not( aop(si,9037,6) == aop(bs,17,5) ):
            lzbir =  aop(si,9037,6) 
            dzbir =  aop(bs,17,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9037 kol. 6 = AOP-u 0017 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9037 kol. 6 = AOP-u 0017 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90064
        if not( aop(si,9044,4) == suma(si,9038,9043,4) ):
            lzbir =  aop(si,9044,4) 
            dzbir =  suma(si,9038,9043,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9044 kol. 4 = AOP-u (9038 + 9039 + 9040 + 9041+ 9042 + 9043) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90065
        if not( aop(si,9044,5) == suma(si,9038,9043,5) ):
            lzbir =  aop(si,9044,5) 
            dzbir =  suma(si,9038,9043,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9044 kol. 5 = AOP-u (9038 + 9039 + 9040 + 9041+ 9042 + 9043) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90066
        if not( aop(si,9044,4) == suma_liste(bs,[31,37],5) ):
            lzbir =  aop(si,9044,4) 
            dzbir =  suma_liste(bs,[31,37],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9044 kol. 4 = zbiru AOP-a (0031 + 0037) kol. 5 bilansa stanja  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9044 kol. 4 = zbiru AOP-a (0031 + 0037) kol. 5 bilansa stanja  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90067
        if not( aop(si,9044,5) == suma_liste(bs,[31,37],6) ):
            lzbir =  aop(si,9044,5) 
            dzbir =  suma_liste(bs,[31,37],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9044 kol. 5 = zbiru AOP-a (0031 + 0037) kol. 6 bilansa stanja  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9044 kol. 5 = zbiru AOP-a (0031 + 0037) kol. 6 bilansa stanja  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90068
        if not( aop(si,9057,4) == suma_liste(si,[9045,9047,9049,9051,9052,9053,9054,9055,9056],4) ):
            lzbir =  aop(si,9057,4) 
            dzbir =  suma_liste(si,[9045,9047,9049,9051,9052,9053,9054,9055,9056],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9057 kol. 4 = AOP-u (9045 + 9047 + 9049 + 9051 + 9052 + 9053 + 9054 + 9055 + 9056) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90069
        if not( aop(si,9057,5) == suma_liste(si,[9045,9047,9049,9051,9052,9053,9054,9055,9056],5) ):
            lzbir =  aop(si,9057,5) 
            dzbir =  suma_liste(si,[9045,9047,9049,9051,9052,9053,9054,9055,9056],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9057 kol. 5 = AOP-u (9045 + 9047 + 9049 + 9051 + 9052 + 9053 + 9054 + 9055 + 9056) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90070
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if not( suma(si,9045,9055,4) == 0 ):
                lzbir =  suma(si,9045,9055,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Zbir AOP-a (9045 do 9055) kol. 4 = 0 Preduzetnici mogu imati samo ostali osnovni kapital '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
        #90071
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if not( suma(si,9045,9055,5) == 0 ):
                lzbir =  suma(si,9045,9055,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Zbir AOP-a (9045 do 9055) kol. 5 = 0 Preduzetnici mogu imati samo ostali osnovni kapital '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
        #90072
        if not( aop(si,9046,4) <= aop(si,9045,4) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9046 kol. 4 ≤ AOP-a 9045 kol. 4  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90073
        if not( aop(si,9046,5) <= aop(si,9045,5) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9046 kol. 5 ≤ AOP-a 9045 kol. 5  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90074
        if not( aop(si,9048,4) <= aop(si,9047,4) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9048 kol. 4 ≤ AOP-a 9047 kol. 4  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90075
        if not( aop(si,9048,5) <= aop(si,9047,5) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9048 kol. 5 ≤ AOP-a 9047 kol. 5  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90076
        if not( aop(si,9050,4) <= aop(si,9049,4) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9050 kol. 4 ≤ AOP-a 9049 kol. 4  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90077
        if not( aop(si,9050,5) <= aop(si,9049,5) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9050 kol. 5 ≤ AOP-a 9049 kol. 5  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90078
        if not( aop(si,9057,4) == suma_liste(bs,[402,404],5) ):
            lzbir =  aop(si,9057,4) 
            dzbir =  suma_liste(bs,[402,404],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9057 kol. 4 = Zbiru AOP-a (0402 + 0404) kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9057 kol. 4 = Zbiru AOP-a (0402 + 0404) kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90079
        if not( aop(si,9057,5) == suma_liste(bs,[402,404],6) ):
            lzbir =  aop(si,9057,5) 
            dzbir =  suma_liste(bs,[402,404],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9057 kol. 5= Zbiru AOP-a (0402 + 0404) kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9057 kol. 5= Zbiru AOP-a (0402 + 0404) kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90080
        if not( aop(si,9054,4) == aop(bs,404,5) ):
            lzbir =  aop(si,9054,4) 
            dzbir =  aop(bs,404,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9054 kol. 4 = AOP-u 0404 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9054 kol. 4 = AOP-u 0404 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90081
        if not( aop(si,9054,5) == aop(bs,404,6) ):
            lzbir =  aop(si,9054,5) 
            dzbir =  aop(bs,404,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9054 kol. 5 = AOP-u 0404 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9054 kol. 5 = AOP-u 0404 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90082
        if not( suma_liste(si,[9045,9047,9049,9051,9052,9053,9055,9056],4) == aop(bs,402,5) ):
            lzbir =  suma_liste(si,[9045,9047,9049,9051,9052,9053,9055,9056],4) 
            dzbir =  aop(bs,402,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir AOP-a (9045 + 9047 + 9049 + 9051 + 9052 + 9053 + 9055 + 9056) kol. 4 = AOP-u 0402 kol.5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir AOP-a (9045 + 9047 + 9049 + 9051 + 9052 + 9053 + 9055 + 9056) kol. 4 = AOP-u 0402 kol.5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90083
        if not( suma_liste(si,[9045,9047,9049,9051,9052,9053,9055,9056],5) == aop(bs,402,6) ):
            lzbir =  suma_liste(si,[9045,9047,9049,9051,9052,9053,9055,9056],5) 
            dzbir =  aop(bs,402,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir AOP-a (9045 + 9047 + 9049 + 9051 + 9052 + 9053 + 9055 + 9056) kol. 5 = AOP-u 0402 kol.6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir AOP-a (9045 + 9047 + 9049 + 9051 + 9052 + 9053 + 9055 + 9056) kol. 5 = AOP-u 0402 kol.6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90084
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if not( suma(si,9058,9062,4) == 0 ):
                lzbir =  suma(si,9058,9062,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Zbir AOP-a (9058 do 9062 ) kol. 4 = 0 Preduzetnici ne mogu imati akcijski kapital '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
             
        #90085
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if not( suma(si,9058,9062,5) == 0 ):
                lzbir =  suma(si,9058,9062,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Zbir AOP-a (9058 do 9062 ) kol. 5 = 0 Preduzetnici ne mogu imati akcijski kapital '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
             
        #90086
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if( aop(si,9058,4) > 0 ):
                if not( aop(si,9059,4) > 0 ):
                    
                    naziv_obrasca='Statistički izveštaj'
                    poruka  ='Ako je AOP 9058 kol. 4 > 0, onda je AOP 9059 kol. 4 > 0  Ako je prikazan broj akcija, mora biti prikazana i vrednost akcija '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
        #90087
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if( aop(si,9059,4) > 0 ):
                if not( aop(si,9058,4) > 0 ):
                    
                    naziv_obrasca='Statistički izveštaj'
                    poruka  ='Ako je AOP 9059 kol. 4 > 0 onda je AOP 9058 kol. 4 > 0 Ako je prikazana vrednost akcija, mora biti prikazan broj akcija '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
        #90088
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if( aop(si,9058,5) > 0 ):
                if not( aop(si,9059,5) > 0 ):
                    
                    naziv_obrasca='Statistički izveštaj'
                    poruka  ='Ako je AOP 9058 kol. 5 > 0, onda je AOP 9059 kol. 5 > 0  Ako je prikazan broj akcija, mora biti prikazana i vrednost akcija '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
        #90089
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if( aop(si,9059,5) > 0 ):
                if not( aop(si,9058,5) > 0 ):
                    
                    naziv_obrasca='Statistički izveštaj'
                    poruka  ='Ako je AOP 9059 kol. 5 > 0 onda je AOP 9058 kol. 5 > 0 Ako je prikazana vrednost akcija, mora biti prikazan broj akcija '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
        #90090
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if( aop(si,9060,4) > 0 ):
                if not( aop(si,9061,4) > 0 ):
                    
                    naziv_obrasca='Statistički izveštaj'
                    poruka  ='Ako je AOP 9060 kol. 4 > 0, onda je AOP 9061 kol. 4 > 0  Ako je prikazan broj akcija, mora biti prikazana i vrednost akcija '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
        #90091
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if( aop(si,9061,4) > 0 ):
                if not( aop(si,9060,4) > 0 ):
                    
                    naziv_obrasca='Statistički izveštaj'
                    poruka  ='Ako je AOP 9061 kol. 4 > 0 onda je AOP 9060 kol. 4 > 0 Ako je prikazana vrednost akcija, mora biti prikazan broj akcija '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
        #90092
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if( aop(si,9060,5) > 0 ):
                if not( aop(si,9061,5) > 0 ):
                    
                    naziv_obrasca='Statistički izveštaj'
                    poruka  ='Ako je AOP 9060 kol. 5 > 0, onda je AOP 9061 kol. 5 > 0  Ako je prikazan broj akcija, mora biti prikazana i vrednost akcija '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
        #90093
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if( aop(si,9061,5) > 0 ):
                if not( aop(si,9060,5) > 0 ):
                    
                    naziv_obrasca='Statistički izveštaj'
                    poruka  ='Ako je AOP 9061 kol. 5 > 0 onda je AOP 9060 kol. 5 > 0 Ako je prikazana vrednost akcija, mora biti prikazan broj akcija '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
        #90094
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if not( aop(si,9062,4) == suma_liste(si,[9059,9061],4) ):
                lzbir =  aop(si,9062,4) 
                dzbir =  suma_liste(si,[9059,9061],4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='AOP 9062 kol. 4 = AOP-u (9059 + 9061) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
        #90095
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if not( aop(si,9062,5) == suma_liste(si,[9059,9061],5) ):
                lzbir =  aop(si,9062,5) 
                dzbir =  suma_liste(si,[9059,9061],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='AOP 9062 kol. 5 = AOP-u (9059 + 9061) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
        #90096
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if not( aop(si,9062,4) == aop(si,9045,4) ):
                lzbir =  aop(si,9062,4) 
                dzbir =  aop(si,9045,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='AOP 9062 kol. 4 = AOP-u 9045 kol. 4 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
        #90097
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if not( aop(si,9062,5) == aop(si,9045,5) ):
                lzbir =  aop(si,9062,5) 
                dzbir =  aop(si,9045,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='AOP 9062 kol. 5 = AOP-u 9045 kol. 5 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
        #90098
        if not( aop(si,9071,3) == suma(si,9063,9070,3) ):
            lzbir =  aop(si,9071,3) 
            dzbir =  suma(si,9063,9070,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9071 kol. 3 = AOP-u (9063 + 9064 + 9065 + 9066 + 9067 + 9068 + 9069 + 9070) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90099
        if not( aop(si,9071,4) == suma(si,9063,9070,4) ):
            lzbir =  aop(si,9071,4) 
            dzbir =  suma(si,9063,9070,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9071 kol. 4 = AOP-u (9063 + 9064 + 9065 + 9066 + 9067 + 9068 + 9069 + 9070) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90100
        if not( aop(si,9071,3) == aop(iotg,3045,3) ):
            lzbir =  aop(si,9071,3) 
            dzbir =  aop(iotg,3045,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 9071 kol. 3 = AOP-u 3045 kol. 3 izveštaja o tokovima gotovine Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9071 kol. 3 = AOP-u 3045 kol. 3 izveštaja o tokovima gotovine Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90101
        if not( aop(si,9071,4) == aop(iotg,3045,4) ):
            lzbir =  aop(si,9071,4) 
            dzbir =  aop(iotg,3045,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 9071 kol. 4 = AOP-u 3045 kol. 4 izveštaja o tokovima gotovine Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9071 kol. 4 = AOP-u 3045 kol. 4 izveštaja o tokovima gotovine Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90102
        if not( aop(si,9078,4) == suma(si,9072,9077,4) ):
            lzbir =  aop(si,9078,4) 
            dzbir =  suma(si,9072,9077,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9078 kol. 4 = AOP-u (9072 + 9073 + 9074 + 9075 + 9076 + 9077) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90103
        if not( aop(si,9078,5) == suma(si,9072,9077,5) ):
            lzbir =  aop(si,9078,5) 
            dzbir =  suma(si,9072,9077,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9078 kol. 5 = AOP-u (9072 + 9073 + 9074 + 9075 + 9076 + 9077) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90104
        if not( aop(si,9080,4) <= suma(si,9074,9076,4) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9080 kol. 4 ≤ AOP-a (9074 + 9075 + 9076) kol. 4 Troškovi zarada, po pravilu, su manji ili jednaki obavezama za bruto zarade '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90105
        if not( aop(si,9080,5) <= suma(si,9074,9076,5) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9080 kol. 5 ≤ AOP-a (9074 + 9075 + 9076) kol. 5 Troškovi zarada, po pravilu, su manji ili jednaki obavezama za bruto zarade '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90106
        if not( aop(si,9098,4) == suma(si,9079,9097,4) ):
            lzbir =  aop(si,9098,4) 
            dzbir =  suma(si,9079,9097,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9098 kol. 4 = Zbiru AOP-a (od 9079 do 9097) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90107
        if not( aop(si,9098,5) == suma(si,9079,9097,5) ):
            lzbir =  aop(si,9098,5) 
            dzbir =  suma(si,9079,9097,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9098 kol. 5 = Zbiru AOP-a (od 9079 do 9097) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90108
        if not( suma(si,9080,9088,4) == aop(bu,1016,5) ):
            lzbir =  suma(si,9080,9088,4) 
            dzbir =  aop(bu,1016,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (9080 + 9081 + 9082 + 9083 + 9084 + 9085 + 9086 + 9087 + 9088) kol. 4 = AOP-u 1016 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP (9080 + 9081 + 9082 + 9083 + 9084 + 9085 + 9086 + 9087 + 9088) kol. 4 = AOP-u 1016 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90109
        if not( suma(si,9080,9088,5) == aop(bu,1016,6) ):
            lzbir =  suma(si,9080,9088,5) 
            dzbir =  aop(bu,1016,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (9080 + 9081 + 9082 + 9083 + 9084 + 9085 + 9086 + 9087 + 9088) kol. 5 = AOP-u 1016 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP (9080 + 9081 + 9082 + 9083 + 9084 + 9085 + 9086 + 9087 + 9088) kol. 5 = AOP-u 1016 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90110
        if not( aop(si,9080,4) == aop(bu,1017,5) ):
            lzbir =  aop(si,9080,4) 
            dzbir =  aop(bu,1017,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9080  kol. 4 = AOP-u 1017 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9080  kol. 4 = AOP-u 1017 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90111
        if not( aop(si,9080,5) == aop(bu,1017,6) ):
            lzbir =  aop(si,9080,5) 
            dzbir =  aop(bu,1017,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9080  kol. 5 = AOP-u 1017 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9080  kol. 5 = AOP-u 1017 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90112
        if not( aop(si,9081,4) == aop(bu,1018,5) ):
            lzbir =  aop(si,9081,4) 
            dzbir =  aop(bu,1018,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9081  kol. 4 = AOP-u 1018 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9081  kol. 4 = AOP-u 1018 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90113
        if not( aop(si,9081,5) == aop(bu,1018,6) ):
            lzbir =  aop(si,9081,5) 
            dzbir =  aop(bu,1018,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9081  kol. 5 = AOP-u 1018 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9081  kol. 5 = AOP-u 1018 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90114
        if not( suma(si,9082,9088,4) == aop(bu,1019,5) ):
            lzbir =  suma(si,9082,9088,4) 
            dzbir =  aop(bu,1019,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir AOP-a (9082 + 9083 + 9084 + 9085 + 9086 + 9087 + 9088) kol. 4 = AOP-u 1019 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir AOP-a (9082 + 9083 + 9084 + 9085 + 9086 + 9087 + 9088) kol. 4 = AOP-u 1019 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90115
        if not( suma(si,9082,9088,5) == aop(bu,1019,6) ):
            lzbir =  suma(si,9082,9088,5) 
            dzbir =  aop(bu,1019,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir AOP-a (9082 + 9083 + 9084 + 9085 + 9086 + 9087 + 9088) kol. 5 = AOP-u 1019 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir AOP-a (9082 + 9083 + 9084 + 9085 + 9086 + 9087 + 9088) kol. 5 = AOP-u 1019 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90116
        if not( aop(si,9090,4) <= aop(si,9089,4) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9090 kol. 4 ≤ AOP-a 9089 kol. 4  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90117
        if not( aop(si,9090,5) <= aop(si,9089,5) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9090 kol. 5 ≤ AOP-a 9089 kol. 5  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90118
        if not( aop(si,9091,4) <= aop(bu,1022,5) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9091 kol. 4 ≤ 1022 kol. 5 bilansa uspeha Troškovi istraživanja i razvoja su izdvojeni deo troškova proizvodnih usluga. '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9091 kol. 4 ≤ 1022 kol. 5 bilansa uspeha Troškovi istraživanja i razvoja su izdvojeni deo troškova proizvodnih usluga. '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90119
        if not( aop(si,9091,5) <= aop(bu,1022,6) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9091 kol. 5 ≤ 1022 kol. 6 bilansa uspeha Troškovi istraživanja i razvoja su izdvojeni deo troškova proizvodnih usluga. '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9091 kol. 5 ≤ 1022 kol. 6 bilansa uspeha Troškovi istraživanja i razvoja su izdvojeni deo troškova proizvodnih usluga. '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90120
        if not( suma(si,9092,9096,4) <= aop(bu,1024,5) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir AOP-a (9092 + 9093 + 9094 + 9095 + 9096) kol. 4 ≤ AOP-a 1024 kol. 5 bilansa uspeha Troškovi osiguranja, platnog prometa, članarina, poreza i doprinosa su izdvojeni deo nematerijalnih troškova '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir AOP-a (9092 + 9093 + 9094 + 9095 + 9096) kol. 4 ≤ AOP-a 1024 kol. 5 bilansa uspeha Troškovi osiguranja, platnog prometa, članarina, poreza i doprinosa su izdvojeni deo nematerijalnih troškova '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90121
        if not( suma(si,9092,9096,5) <= aop(bu,1024,6) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir AOP-a (9092 + 9093 + 9094 + 9095 + 9096) kol. 5 ≤ AOP-a 1024 kol. 6 bilansa uspeha Troškovi osiguranja, platnog prometa, članarina, poreza i doprinosa su izdvojeni deo nematerijalnih troškova '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir AOP-a (9092 + 9093 + 9094 + 9095 + 9096) kol. 5 ≤ AOP-a 1024 kol. 6 bilansa uspeha Troškovi osiguranja, platnog prometa, članarina, poreza i doprinosa su izdvojeni deo nematerijalnih troškova '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90122
        if not( aop(si,9105,4) == suma(si,9099,9104,4) ):
            lzbir =  aop(si,9105,4) 
            dzbir =  suma(si,9099,9104,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9105 kol. 4 = AOP-u (9099 + 9100 + 9101 + 9102 + 9103 + 9104) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90123
        if not( aop(si,9105,5) == suma(si,9099,9104,5) ):
            lzbir =  aop(si,9105,5) 
            dzbir =  suma(si,9099,9104,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9105 kol. 5 = AOP-u (9099 + 9100 + 9101 + 9102 + 9103 + 9104) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90124
        if not( aop(si,9105,4) <= aop(bu,1032,5) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9105 kol. 4 ≤ AOP-a 1032 kol. 5 bilansa uspeha Rashodi kamata su deo finansijskih rashoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9105 kol. 4 ≤ AOP-a 1032 kol. 5 bilansa uspeha Rashodi kamata su deo finansijskih rashoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90125
        if not( aop(si,9105,5) <= aop(bu,1032,6) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9105 kol. 5 ≤ AOP-a 1032 kol. 6 bilansa uspeha Rashodi kamata su deo finansijskih rashoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9105 kol. 5 ≤ AOP-a 1032 kol. 6 bilansa uspeha Rashodi kamata su deo finansijskih rashoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90126
        if not( aop(si,9112,4) == suma(si,9106,9111,4) ):
            lzbir =  aop(si,9112,4) 
            dzbir =  suma(si,9106,9111,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9112 kol. 4 = Zbiru AOP-a (od 9106 do 9111) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90127
        if not( aop(si,9112,5) == suma(si,9106,9111,5) ):
            lzbir =  aop(si,9112,5) 
            dzbir =  suma(si,9106,9111,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9112 kol. 5 = Zbiru AOP-a (od 9106 do 9111) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90128
        if not( suma(si,9106,9108,4) <= aop(bu,1011,5) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir AOP-a (9106 + 9107 + 9108) kol. 4 ≤ AOP-a 1011 kol. 5 bilansa uspeha Prihodi od premija subvencija, dotacija, donacija i sl. kao i drugi poslovni prihodi  su deo ostalih poslovnih prihoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir AOP-a (9106 + 9107 + 9108) kol. 4 ≤ AOP-a 1011 kol. 5 bilansa uspeha Prihodi od premija subvencija, dotacija, donacija i sl. kao i drugi poslovni prihodi  su deo ostalih poslovnih prihoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90129
        if not( suma(si,9106,9108,5) <= aop(bu,1011,6) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir AOP-a (9106 + 9107 + 9108) kol. 5 ≤ AOP-a 1011 kol. 6 bilansa uspeha Prihodi od premija subvencija, dotacija, donacija i sl. kao i drugi poslovni prihodi  su deo ostalih poslovnih prihoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir AOP-a (9106 + 9107 + 9108) kol. 5 ≤ AOP-a 1011 kol. 6 bilansa uspeha Prihodi od premija subvencija, dotacija, donacija i sl. kao i drugi poslovni prihodi  su deo ostalih poslovnih prihoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90130
        if not( suma(si,9109,9110,4) <= aop(si,9108,4) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir AOP-a (9109 + 9110) kol. 4 ≤ AOP-a 9108 kol. 4 Prihodi od zakupnina za zemljište i prihodi od članarina su deo Drugih poslovnih prihoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90131
        if not( suma(si,9109,9110,5) <= aop(si,9108,5) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir AOP-a (9109 + 9110) kol. 5 ≤ AOP-a 9108 kol. 5 Prihodi od zakupnina za zemljište i prihodi od članarina su deo Drugih poslovnih prihoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90132
        if not( aop(si,9111,4) <= suma_liste(bu,[1028,1031],5) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9111 kol. 4 ≤ zbiru AOP-a (1028 + 1031) kol. 5 bilansa uspeha Prihodi po osnovu dividendi i učešća u dobitku su  deo finansijskih prihoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9111 kol. 4 ≤ zbiru AOP-a (1028 + 1031) kol. 5 bilansa uspeha Prihodi po osnovu dividendi i učešća u dobitku su  deo finansijskih prihoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90133
        if not( aop(si,9111,5) <= suma_liste(bu,[1028,1031],6) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9111 kol. 5 ≤ zbiru AOP-a (1028 + 1031) kol. 6 bilansa uspeha Prihodi po osnovu dividendi i učešća u dobitku su  deo finansijskih prihoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9111 kol. 5 ≤ zbiru AOP-a (1028 + 1031) kol. 6 bilansa uspeha Prihodi po osnovu dividendi i učešća u dobitku su  deo finansijskih prihoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90134
        if not( aop(si,9118,4) == suma(si,9113,9117,4) ):
            lzbir =  aop(si,9118,4) 
            dzbir =  suma(si,9113,9117,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9118 kol. 4 = AOP-u (9113 + 9114 + 9115 + 9116 + 9117) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90135
        if not( aop(si,9118,5) == suma(si,9113,9117,5) ):
            lzbir =  aop(si,9118,5) 
            dzbir =  suma(si,9113,9117,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9118 kol. 5 = AOP-u (9113 + 9114 + 9115 + 9116 + 9117) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90136
        if not( aop(si,9118,4) <= aop(bu,1027,5) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9118 kol. 4 ≤ AOP-a 1027 kol. 5 bilansa uspeha Rashodi kamata su deo finansijskih rashoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9118 kol. 4 ≤ AOP-a 1027 kol. 5 bilansa uspeha Rashodi kamata su deo finansijskih rashoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90137
        if not( aop(si,9118,5) <= aop(bu,1027,6) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9118 kol. 5 ≤ AOP-a 1027 kol. 6 bilansa uspeha Rashodi kamata su deo finansijskih rashoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9118 kol. 5 ≤ AOP-a 1027 kol. 6 bilansa uspeha Rashodi kamata su deo finansijskih rashoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90138
        if not( aop(si,9126,3) == suma(si,9119,9125,3) ):
            lzbir =  aop(si,9126,3) 
            dzbir =  suma(si,9119,9125,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9126 kol. 3 = Zbiru AOP-a (od 9119 do 9125) kol. 3   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90139
        if not( aop(si,9126,4) == suma(si,9119,9125,4) ):
            lzbir =  aop(si,9126,4) 
            dzbir =  suma(si,9119,9125,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9126 kol. 4 = Zbiru AOP-a (od 9119 do 9125) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90140
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if not( aop(si,9125,3) == 0 ):
                lzbir =  aop(si,9125,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='AOP 9125 kol. 3 = 0 Navedeni podatak iskazuju samo preduzetnici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
        #90141
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if not( aop(si,9125,4) == 0 ):
                lzbir =  aop(si,9125,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='AOP 9125 kol. 4 = 0 Navedeni podatak iskazuju samo preduzetnici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
        #90142
        if not( aop(si,9127,6) == aop(si,9127,4)-aop(si,9127,5) ):
            lzbir =  aop(si,9127,6) 
            dzbir =  aop(si,9127,4)-aop(si,9127,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9127 kol. 6 = AOP-u 9127 kol. 4 - AOP 9127 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90143
        if not( aop(si,9127,6) <= aop(bs,48,5) ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9127 kol. 6 ≤  AOP-u 0048 kol. 5 bilansa stanja Dati kratkoročni krediti i zajmovi fizičkim licima i preduzetnicima su deo kratkoročnih finansijskih plasmana '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9127 kol. 6 ≤  AOP-u 0048 kol. 5 bilansa stanja Dati kratkoročni krediti i zajmovi fizičkim licima i preduzetnicima su deo kratkoročnih finansijskih plasmana '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90144
        if not( aop(si,9128,6) == aop(si,9128,4)-aop(si,9128,5) ):
            lzbir =  aop(si,9128,6) 
            dzbir =  aop(si,9128,4)-aop(si,9128,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9128 kol. 6 = AOP-u 9128 kol. 4 - AOP 9128 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90145
        if not( aop(si,9128,6) <= aop(bs,18,5) ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9128 kol. 6 ≤  AOP-u 0018 kol. 5 bilansa stanja Dati dugoročni krediti i zajmovi fizičkim licima i preduzetnicima su deo dugoročnih finansijskih plasmana i potraživanja '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9128 kol. 6 ≤  AOP-u 0018 kol. 5 bilansa stanja Dati dugoročni krediti i zajmovi fizičkim licima i preduzetnicima su deo dugoročnih finansijskih plasmana i potraživanja '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90146
        if not( aop(si,9129,4) == suma(si,9130,9132,4) ):
            lzbir =  aop(si,9129,4) 
            dzbir =  suma(si,9130,9132,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9129 kol. 4 = AOP-u (9130 + 9131 + 9132) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90147
        if not( aop(si,9129,5) == suma(si,9130,9132,5) ):
            lzbir =  aop(si,9129,5) 
            dzbir =  suma(si,9130,9132,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9129 kol. 5 = AOP-u (9130 + 9131 + 9132) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90148
        if not( aop(si,9129,6) == suma(si,9130,9132,6) ):
            lzbir =  aop(si,9129,6) 
            dzbir =  suma(si,9130,9132,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9129 kol. 6 = AOP-u (9130 + 9131 + 9132) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90149
        if not( aop(si,9129,6) == aop(si,9129,4)-aop(si,9129,5) ):
            lzbir =  aop(si,9129,6) 
            dzbir =  aop(si,9129,4)-aop(si,9129,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9129 kol. 6 = AOP-u 9129 kol. 4 - AOP 9129 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90150
        if not( aop(si,9130,6) == aop(si,9130,4)-aop(si,9130,5) ):
            lzbir =  aop(si,9130,6) 
            dzbir =  aop(si,9130,4)-aop(si,9130,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9130 kol. 6 = AOP-u 9130 kol. 4 - AOP 9130 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90151
        if not( aop(si,9131,6) == aop(si,9131,4)-aop(si,9131,5) ):
            lzbir =  aop(si,9131,6) 
            dzbir =  aop(si,9131,4)-aop(si,9131,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9131 kol. 6 = AOP-u 9131 kol. 4 - AOP 9131 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90152
        if not( aop(si,9132,6) == aop(si,9132,4)-aop(si,9132,5) ):
            lzbir =  aop(si,9132,6) 
            dzbir =  aop(si,9132,4)-aop(si,9132,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9132 kol. 6 = AOP-u 9132 kol. 4 - AOP 9132 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90153
        if not( aop(si,9129,6) <= suma_liste(bs,[3,9,17,18,31,38],5) ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9129 kol. 6 ≤ AOP-a (0003 + 0009 + 0017 + 0018 + 0031 + 0038) kol. 5 bilansa stanja Vrednost prodatih proizvoda, robe i usluga ne može biti veća od zbira stalne imovine, zaliha i potraživanja od prodaje '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9129 kol. 6 ≤ AOP-a (0003 + 0009 + 0017 + 0018 + 0031 + 0038) kol. 5 bilansa stanja Vrednost prodatih proizvoda, robe i usluga ne može biti veća od zbira stalne imovine, zaliha i potraživanja od prodaje '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90154
        if not( aop(si,9133,4) == suma(si,9134,9136,4) ):
            lzbir =  aop(si,9133,4) 
            dzbir =  suma(si,9134,9136,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9133 kol. 4 = AOP-u (9134 + 9135 + 9136) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90155
        if not( aop(si,9133,5) == suma(si,9134,9136,5) ):
            lzbir =  aop(si,9133,5) 
            dzbir =  suma(si,9134,9136,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9133 kol. 5 = AOP-u (9134 + 9135 + 9136) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90156
        if not( aop(si,9133,6) == suma(si,9134,9136,6) ):
            lzbir =  aop(si,9133,6) 
            dzbir =  suma(si,9134,9136,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9133 kol. 6 = AOP-u (9134 + 9135 + 9136) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90157
        if not( aop(si,9133,6) == aop(si,9133,4)-aop(si,9133,5) ):
            lzbir =  aop(si,9133,6) 
            dzbir =  aop(si,9133,4)-aop(si,9133,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9133 kol. 6 = AOP-u 9133 kol. 4 - AOP 9133 kol. 5   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90158
        if not( aop(si,9134,6) == aop(si,9134,4)-aop(si,9134,5) ):
            lzbir =  aop(si,9134,6) 
            dzbir =  aop(si,9134,4)-aop(si,9134,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9134 kol. 6 = AOP-u 9134 kol. 4 - AOP 9134 kol. 5   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90159
        if not( aop(si,9135,6) == aop(si,9135,4)-aop(si,9135,5) ):
            lzbir =  aop(si,9135,6) 
            dzbir =  aop(si,9135,4)-aop(si,9135,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9135 kol. 6 = AOP-u 9135 kol. 4 - AOP 9135 kol. 5   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90160
        if not( aop(si,9136,6) == aop(si,9136,4)-aop(si,9136,5) ):
            lzbir =  aop(si,9136,6) 
            dzbir =  aop(si,9136,4)-aop(si,9136,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9136 kol. 6 = AOP-u 9136 kol. 4 - AOP 9136 kol. 5   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90161
        if not( aop(si,9133,6) <= suma_liste(bs,[43,45,47],5) ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9133 kol. 6 ≤ AOP-a (0043 + 0045 + 0047) kol. 5 bilansa stanja Potraživanja od fizičkih lica i  preduzetnika, državnih organa i institucija, kao i od organa i institucija lokalne samouprave su deo ostalih potraživanja '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9133 kol. 6 ≤ AOP-a (0043 + 0045 + 0047) kol. 5 bilansa stanja Potraživanja od fizičkih lica i  preduzetnika, državnih organa i institucija, kao i od organa i institucija lokalne samouprave su deo ostalih potraživanja '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #POSEBNI PODACI:
        #PRAVILO NE TREBA DA BUDE VIDLJIVO ZA KORISNIKA, ODNOSNO ZA OBVEZNIKA TREBA DA VIDI SAMO KOMENTAR KOJI JE DAT UZ PRAVILO. 
        #U OBRASCU NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        #PLATNE INSTITUCIJE I FAKTORING DRUŠTVA POPUNJAVAJU SAMO POLJE "VELIČINA ZA NAREDNU POSLOVNU GODINU"
        
        #100001
        if not( aop(pp,10001, 1) >= 1 and aop(pp, 10001, 1) <= 4 ):
            
            naziv_obrasca='Posebni podaci'
            poruka  =' Oznaka za veličinu mora biti 1, 2, 3  ili 4 '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #100002
        #Za ovaj set se ne primenjuje pravilo 
        
        #100003
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 15 or Zahtev.ObveznikInfo.GrupaObveznika.value__ == 17):
            if not( aop(pp,10001,1) == 4 ):
                
                naziv_obrasca='Posebni podaci'
                poruka  =' Platne institucije i institucije elektronskog novca, kao i faktoring društva unose oznaku za velika pravna lica (oznaka 4) '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #100004
        if not (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 15):
            if not (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 17):
                if not( aop(pp,10002,1) >= 0 ):
                    
                    naziv_obrasca='Posebni podaci'
                    poruka  ='Podatak o prosečnom broju zaposlenih u tekućoj godini u obrascu Posebni podaci mora biti upisan; ako nema zaposlenih upisuje se broj 0'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
        
        #100005
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 15 or Zahtev.ObveznikInfo.GrupaObveznika.value__ == 17):
            if not( aop(pp,10002,1) == 0 ):
                
                naziv_obrasca='Posebni podaci'
                poruka  =' Platne institucije i institucije elektronskog novca, kao i faktoring društva u skladu sa članom 6. Zakona smatraju se velikim pravnim licima. Podatak o prosečnom broju zaposlenih, u obrascu posebni podaci, ne treba popunjavati. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
        #100006
        if not (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 15):
            if not (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 17):
                if not( aop(pp,10002,1) == aop(si, 9005, 3) ):
                    
                    naziv_obrasca='Statistički izveštaj'
                    poruka  ='Podatak o prosečnom broju zaposlenih u tekućoj godini, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Statistički izveštaj na poziciji AOP 9005 u koloni 3'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    naziv_obrasca='Posebni podaci'
                    poruka  ='Podatak o prosečnom broju zaposlenih u tekućoj godini, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Statistički izveštaj na poziciji AOP 9005 u koloni 3'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
        
        #100007
        #Za ovaj set se ne primenjuje pravilo 
        
        #100008
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 15 or Zahtev.ObveznikInfo.GrupaObveznika.value__ == 17):
            if not( aop(pp,10003,1) == 0 ):
                
                naziv_obrasca='Posebni podaci'
                poruka  =' Platne institucije i institucije elektronskog novca, kao i faktoring društva u skladu sa članom 6. Zakona smatraju se velikim pravnim licima Podatak o poslovnom prihodu, u obrascu posebni podaci, ne treba popunjavati.  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
        #100009
        if not (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 15):
            if not (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 17):
                if not( aop(pp,10003,1) == aop(bu, 1001, 5) ):
                    
                    naziv_obrasca='Bilans uspeha'
                    poruka  ='Podatak o poslovnom prihodu u tekućoj godini, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Bilans uspeha na poziciji AOP 1001 u koloni 5'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    naziv_obrasca='Posebni podaci'
                    poruka  ='Podatak o poslovnom prihodu u tekućoj godini, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Bilans uspeha na poziciji AOP 1001 u koloni 5'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
             
        
        #100010
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 15 or Zahtev.ObveznikInfo.GrupaObveznika.value__ == 17):
            if not( aop(pp,10004,1) == 0 ):
                
                naziv_obrasca='Posebni podaci'
                poruka  =' Platne institucije i institucije elektronskog novca, kao i faktoring društva u skladu sa članom 6. Zakona smatraju se velikim pravnim licima Podatak o vrednosti ukupne aktive na bilansni dan, u obrascu posebni podaci, ne treba popunjavati. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
        #100011
        if not (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 15):
            if not (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 17):
                if not( aop(pp,10004,1) == aop(bs, 59, 5) ):
                    
                    naziv_obrasca='Bilans stanja'
                    poruka  ='Podatak o vrednosti ukupne aktive u tekućoj godini, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Bilans stanja na poziciji AOP 0059 u koloni 5'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    naziv_obrasca='Posebni podaci'
                    poruka  ='Podatak o vrednosti ukupne aktive u tekućoj godini, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Bilans stanja na poziciji AOP 0059 u koloni 5'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
        
        
        #100012
        if not (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 15):
            if not (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 17):
                if not( aop(pp,10102,1) >= 0 ):
                    
                    naziv_obrasca='Posebni podaci'
                    poruka  ='Podatak o prosečnom broju zaposlenih u prethodnoj godini,  mora biti upisan; ako nema zaposlenih upisuje se broj 0'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
         
        
        #100013
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 15 or Zahtev.ObveznikInfo.GrupaObveznika.value__ == 17):
            if not( aop(pp,10102,1) == 0 ):
                
                naziv_obrasca='Posebni podaci'
                poruka  =' Platne institucije i institucije elektronskog novca, kao i faktoring društva u skladu sa članom 6. Zakona smatraju se velikim pravnim licima '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
        #100014
        if not (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 15):
            if not (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 17):
                if not( aop(pp,10102,1) == aop(si, 9005, 4) ):
                    
                    naziv_obrasca='Statistički izveštaj'
                    poruka  ='Podatak o prosečnom broju zaposlenih u prethodnoj godini, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Statistički izveštaj na poziciji AOP 9005 u koloni 4'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    naziv_obrasca='Posebni podaci'
                    poruka  ='Podatak o prosečnom broju zaposlenih u prethodnoj godini, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Statistički izveštaj na poziciji AOP 9005 u koloni 4'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
        
        #100015
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 15 or Zahtev.ObveznikInfo.GrupaObveznika.value__ == 17):
            if not( aop(pp,10103,1) == 0 ):
                
                naziv_obrasca='Posebni podaci'
                poruka  =' Platne institucije i institucije elektronskog novca, kao i faktoring društva u skladu sa članom 6. Zakona smatraju se velikim pravnim licima. Podatak o prosečnom broju zaposlenih u prethodnoj izveštajnoj godini, u obrascu posebni podaci, ne treba popunjavati.  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
        #100016
        if not (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 15):
            if not (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 17):
                if not( aop(pp,10103,1) == aop(bu, 1001, 6) ):
                    
                    naziv_obrasca='Bilans uspeha'
                    poruka  ='Podatak o poslovnom prihodu prethodne godine, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Bilans uspeha na poziciji AOP 1001 u koloni 6'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    naziv_obrasca='Posebni podaci'
                    poruka  ='Podatak o poslovnom prihodu prethodne godine, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Bilans uspeha na poziciji AOP 1001 u koloni 6'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
        
        #100017
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 15 or Zahtev.ObveznikInfo.GrupaObveznika.value__ == 17):
            if not( aop(pp,10104,1) == 0 ):
                
                naziv_obrasca='Posebni podaci'
                poruka  =' Platne institucije i institucije elektronskog novca, kao i faktoring društva u skladu sa članom 6. Zakona smatraju se velikim pravnim licima Podatak o poslovnom prihodu u prethodnoj izveštajnoj godini, u obrascu posebni podaci, ne treba popunjavati.'
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
    
        #100018
        if not (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 15):
            if not (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 17):
                if not( aop(pp,10104,1) == aop(bs, 59, 6) ):
                    
                    naziv_obrasca='Bilans stanja'
                    poruka  ='Podatak o vrednosti ukupne aktive prethodne godine, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Bilans stanja na poziciji AOP 0059 u koloni 6'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    naziv_obrasca='Posebni podaci'
                    poruka  ='Podatak o vrednosti ukupne aktive prethodne godine, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Bilans stanja na poziciji AOP 0059 u koloni 6'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
        
        #100019
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 15 or Zahtev.ObveznikInfo.GrupaObveznika.value__ == 17):
            if not( aop(pp,10110,1) == 0 ):
                
                naziv_obrasca='Posebni podaci'
                poruka  =' Platne institucije i institucije elektronskog novca, kao i faktoring društva u skladu sa članom 6. Zakona smatraju se velikim pravnim licima Podatak o vrednosti ukupne aktive na kraju perioda prethodne izveštajne godine, u obrascu posebni podaci, ne treba popunjavati. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #100020
        #Za ovaj set se ne primenjuje pravilo 
        
        #100021
        #Za ovaj set se ne primenjuje pravilo 
        
        #100022
        #Za ovaj set se ne primenjuje pravilo 
        
        #100023
        #Za ovaj set se ne primenjuje pravilo 
        
        #100024
        #Za ovaj set se ne primenjuje pravilo 
        
        #100025
        #Za ovaj set se ne primenjuje pravilo 
        
        #100026
        #Za ovaj set se ne primenjuje pravilo 
        
        #100027
        #Za ovaj set se ne primenjuje pravilo 
        
        #100028
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
