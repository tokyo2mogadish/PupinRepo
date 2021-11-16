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
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-2
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-3
        if not( suma(bs,1,3,5)+suma(bs,1,3,6)+suma(bs,1,3,7)+aop(bs,9,5)+aop(bs,9,6)+aop(bs,9,7)+suma(bs,17,18,5)+suma(bs,17,18,6)+suma(bs,17,18,7)+suma(bs,28,31,5)+suma(bs,28,31,6)+suma(bs,28,31,7)+suma(bs,37,38,5)+suma(bs,37,38,6)+suma(bs,37,38,7)+aop(bs,44,5)+aop(bs,44,6)+aop(bs,44,7)+aop(bs,48,5)+aop(bs,48,6)+aop(bs,48,7)+suma(bs,57,60,5)+suma(bs,57,60,6)+suma(bs,57,60,7)+suma(bs,401,408,5)+suma(bs,401,408,6)+suma(bs,401,408,7)+suma(bs,411,412,5)+suma(bs,411,412,6)+suma(bs,411,412,7)+suma(bs,415,416,5)+suma(bs,415,416,6)+suma(bs,415,416,7)+aop(bs,420,5)+aop(bs,420,6)+aop(bs,420,7)+suma(bs,428,433,5)+suma(bs,428,433,6)+suma(bs,428,433,7)+suma(bs,441,442,5)+suma(bs,441,442,6)+suma(bs,441,442,7)+aop(bs,449,5)+aop(bs,449,6)+aop(bs,449,7)+suma(bs,453,457,5)+suma(bs,453,457,6)+suma(bs,453,457,7)+suma(bu,1001,1002,5)+suma(bu,1001,1002,6)+aop(bu,1005,5)+aop(bu,1005,6)+suma(bu,1008,1016,5)+suma(bu,1008,1016,6)+suma(bu,1020,1056,5)+suma(bu,1020,1056,6)+suma_liste(si,[9008,9015,9016,9022,9023,9030,9031,9037],6)+suma(si,9038,9062,4)+suma(si,9038,9062,5)+suma(si,9063,9071,3)+suma(si,9063,9071,4)+suma(si,9072,9118,4)+suma(si,9072,9118,5)+suma(si,9119,9126,3)+suma(si,9119,9126,4)+suma(si,9127,9136,6) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0003) kol. 5 + (0001 do 0003) kol. 6 + (0001 do 0003) kol. 7 + 0009 kol.5 + 0009 kol.6 + 0009 kol.7 + (0017 do 0018) kol.5 + (0017 do 0018) kol.6 + (0017 do 0018) kol.7 + (0028 do 0031) kol.5 + (0028 do 0031) kol.6 + (0028 do 0031) kol.7 + (0037 do 0038) kol.5 + (0037 do 0038) kol.6 + (0037 do 0038) kol.7 + 0044 kol. 5 + 0044 kol. 6 + 0044 kol. 7 + 0048 kol.5 + 0048 kol.6 + 0048 kol.7 + (0057 do 0060) kol. 5 + (0057 do 0060) kol. 6 + (0057 do 0060) kol. 7 bilansa stanja + (0401 do 0408) kol. 5 + (0401 do 0408) kol. 6 + (0401 do 0408) kol. 7 + (0411 do 0412) kol. 5 + (0411 do 0412) kol. 6 + (0411 do 0412) kol. 7 + (0415 do 0416) kol. 5 + (0415 do 0416) kol. 6 + (0415 do 0416) kol. 7 + 0420 kol. 5 + 0420 kol. 6 + 0420 kol. 7 + (0428 do 0433) kol. 5 + (0428 do 0433) kol. 6 + (0428 do 0433) kol. 7 + (0441 do 0442) kol.5 + (0441 do 0442) kol.6 + (0441 do 0442) kol.7 + 0449 kol. 5 + 0449 kol. 6 + 0449 kol. 7 + (0453 do 0457) kol. 5 + (0453 do 0457) kol. 6 + (0453 do 0457) kol. 7 bilansa stanja + (1001 do 1002) kol. 5 + (1001 do 1002) kol. 6  + 1005 kol.5 + 1005 kol.6  + (1008 do 1016) kol. 5 + (1008 do 1016) kol. 6 + (1020 do 1056) kol. 5 + (1020 do 1056) kol. 6 bilansa uspeha + (9008 + 9015 + 9016 + 9022 + 9023 + 9030 + 9031 + 9037) kol. 6 + (9038 do 9062) kol.4  + (9038 do 9062) kol.5 + (9063 do 9071) kol.3  + (9063 do 9071) kol.4 + (9072 do 9118) kol.4 + (9072 do 9118) kol.5 + (9119 do 9126) kol.3 + (9119 do 9126) kol.4 + (9127 до 9136) kol. 6 statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka; Ukoliko pravno lice nije imalo poslovnih događaja, niti u poslovnim knjigama ima podatke o imovini i obavezama dužno je da dostavi Izjavu o neaktivnosti;'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0003) kol. 5 + (0001 do 0003) kol. 6 + (0001 do 0003) kol. 7 + 0009 kol.5 + 0009 kol.6 + 0009 kol.7 + (0017 do 0018) kol.5 + (0017 do 0018) kol.6 + (0017 do 0018) kol.7 + (0028 do 0031) kol.5 + (0028 do 0031) kol.6 + (0028 do 0031) kol.7 + (0037 do 0038) kol.5 + (0037 do 0038) kol.6 + (0037 do 0038) kol.7 + 0044 kol. 5 + 0044 kol. 6 + 0044 kol. 7 + 0048 kol.5 + 0048 kol.6 + 0048 kol.7 + (0057 do 0060) kol. 5 + (0057 do 0060) kol. 6 + (0057 do 0060) kol. 7 bilansa stanja + (0401 do 0408) kol. 5 + (0401 do 0408) kol. 6 + (0401 do 0408) kol. 7 + (0411 do 0412) kol. 5 + (0411 do 0412) kol. 6 + (0411 do 0412) kol. 7 + (0415 do 0416) kol. 5 + (0415 do 0416) kol. 6 + (0415 do 0416) kol. 7 + 0420 kol. 5 + 0420 kol. 6 + 0420 kol. 7 + (0428 do 0433) kol. 5 + (0428 do 0433) kol. 6 + (0428 do 0433) kol. 7 + (0441 do 0442) kol.5 + (0441 do 0442) kol.6 + (0441 do 0442) kol.7 + 0449 kol. 5 + 0449 kol. 6 + 0449 kol. 7 + (0453 do 0457) kol. 5 + (0453 do 0457) kol. 6 + (0453 do 0457) kol. 7 bilansa stanja + (1001 do 1002) kol. 5 + (1001 do 1002) kol. 6  + 1005 kol.5 + 1005 kol.6  + (1008 do 1016) kol. 5 + (1008 do 1016) kol. 6 + (1020 do 1056) kol. 5 + (1020 do 1056) kol. 6 bilansa uspeha + (9008 + 9015 + 9016 + 9022 + 9023 + 9030 + 9031 + 9037) kol. 6 + (9038 do 9062) kol.4  + (9038 do 9062) kol.5 + (9063 do 9071) kol.3  + (9063 do 9071) kol.4 + (9072 do 9118) kol.4 + (9072 do 9118) kol.5 + (9119 do 9126) kol.3 + (9119 do 9126) kol.4 + (9127 до 9136) kol. 6 statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka; Ukoliko pravno lice nije imalo poslovnih događaja, niti u poslovnim knjigama ima podatke o imovini i obavezama dužno je da dostavi Izjavu o neaktivnosti;'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0003) kol. 5 + (0001 do 0003) kol. 6 + (0001 do 0003) kol. 7 + 0009 kol.5 + 0009 kol.6 + 0009 kol.7 + (0017 do 0018) kol.5 + (0017 do 0018) kol.6 + (0017 do 0018) kol.7 + (0028 do 0031) kol.5 + (0028 do 0031) kol.6 + (0028 do 0031) kol.7 + (0037 do 0038) kol.5 + (0037 do 0038) kol.6 + (0037 do 0038) kol.7 + 0044 kol. 5 + 0044 kol. 6 + 0044 kol. 7 + 0048 kol.5 + 0048 kol.6 + 0048 kol.7 + (0057 do 0060) kol. 5 + (0057 do 0060) kol. 6 + (0057 do 0060) kol. 7 bilansa stanja + (0401 do 0408) kol. 5 + (0401 do 0408) kol. 6 + (0401 do 0408) kol. 7 + (0411 do 0412) kol. 5 + (0411 do 0412) kol. 6 + (0411 do 0412) kol. 7 + (0415 do 0416) kol. 5 + (0415 do 0416) kol. 6 + (0415 do 0416) kol. 7 + 0420 kol. 5 + 0420 kol. 6 + 0420 kol. 7 + (0428 do 0433) kol. 5 + (0428 do 0433) kol. 6 + (0428 do 0433) kol. 7 + (0441 do 0442) kol.5 + (0441 do 0442) kol.6 + (0441 do 0442) kol.7 + 0449 kol. 5 + 0449 kol. 6 + 0449 kol. 7 + (0453 do 0457) kol. 5 + (0453 do 0457) kol. 6 + (0453 do 0457) kol. 7 bilansa stanja + (1001 do 1002) kol. 5 + (1001 do 1002) kol. 6  + 1005 kol.5 + 1005 kol.6  + (1008 do 1016) kol. 5 + (1008 do 1016) kol. 6 + (1020 do 1056) kol. 5 + (1020 do 1056) kol. 6 bilansa uspeha + (9008 + 9015 + 9016 + 9022 + 9023 + 9030 + 9031 + 9037) kol. 6 + (9038 do 9062) kol.4  + (9038 do 9062) kol.5 + (9063 do 9071) kol.3  + (9063 do 9071) kol.4 + (9072 do 9118) kol.4 + (9072 do 9118) kol.5 + (9119 do 9126) kol.3 + (9119 do 9126) kol.4 + (9127 до 9136) kol. 6 statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka; Ukoliko pravno lice nije imalo poslovnih događaja, niti u poslovnim knjigama ima podatke o imovini i obavezama dužno je da dostavi Izjavu o neaktivnosti;'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}
        #00000-4
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-5
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-6
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-7
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-8
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-9
        if not (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8): 
            bsNapomene = Zahtev.Forme['Bilans stanja'].TekstualnaPoljaForme;
            buNapomene = Zahtev.Forme['Bilans uspeha'].TekstualnaPoljaForme;        

            if not (proveriNapomene(bsNapomene, 1, 3, 4) or proveriNapomene(bsNapomene, 9, 9, 4) or proveriNapomene(bsNapomene, 17, 18, 4) or proveriNapomene(bsNapomene, 28, 31, 4) or proveriNapomene(bsNapomene, 37, 38, 4) or proveriNapomene(bsNapomene, 44, 44, 4) or proveriNapomene(bsNapomene, 48, 48, 4) or proveriNapomene(bsNapomene, 57, 60, 4) or proveriNapomene(bsNapomene, 401, 408, 4) or proveriNapomene(bsNapomene, 411, 412, 4) or proveriNapomene(bsNapomene, 415, 416, 4) or proveriNapomene(bsNapomene, 420, 420, 4) or proveriNapomene(bsNapomene, 428, 433, 4) or proveriNapomene(bsNapomene, 441, 442, 4) or proveriNapomene(bsNapomene, 449, 449, 4)or proveriNapomene(bsNapomene, 453, 457, 4) or proveriNapomene(buNapomene, 1001, 1002, 4) or proveriNapomene(buNapomene, 1005, 1005, 4) or proveriNapomene(buNapomene, 1008, 1016, 4)or proveriNapomene(buNapomene, 1020, 1056, 4) ):   
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Na AOP-u (0001 do 0003)  + 0009 + (0017 do 0018) + (0028 do 0031) + (0037 do 0038) + 0044 + 0048 + (0057 do 0060) bilansa stanja + (0401 do 0408) + (0411 do 0412) + (0415 do 0416) + 0420 + (0428 do 0433) + (0441 do 0442) + 0449 + (0453 do 0457) bilansa stanja + (1001 do 1002) + 1005 + (1008 do 1016) + (1020 do 1056) bilansa uspeha u koloni 4 (Napomena broj) mora biti unet bar jedan karakter Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje'
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ='Na AOP-u (0001 do 0003)  + 0009 + (0017 do 0018) + (0028 do 0031) + (0037 do 0038) + 0044 + 0048 + (0057 do 0060) bilansa stanja + (0401 do 0408) + (0411 do 0412) + (0415 do 0416) + 0420 + (0428 do 0433) + (0441 do 0442) + 0449 + (0453 do 0457) bilansa stanja + (1001 do 1002) + 1005 + (1008 do 1016) + (1020 do 1056) bilansa uspeha u koloni 4 (Napomena broj) mora biti unet bar jedan karakter Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje'
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #Provera da li je fizahtev placen
        if not(Zahtev.Placen):
            ostalo_errors.append('Naknada za obradu i javno objavljivanje izveštaja i propisane dokumentacije nije uplaćena u propisanom iznosu. Instrukcije za uplatu propisane naknade date su u okviru PIS FI sistema za konkretan zahtev, na linku „Status naplate zahteva / Instrukcija za plaćanje". Ukoliko ste izvršili uplatu, a naknada nije uparena, priložite Dokaz o uplati naknade u delu Dokumentacija (na mestu predviđenom za dokaz o uplati naknade), kako biste mogli da podnesete izveštaj.');

        
        #Provera negativnih AOP-a
        lista=""
        lista_bs = find_negativni(bs, 1, 457, 5, 7)
        lista_bu = find_negativni(bu, 1001, 1056, 5, 6)
        lista_si = find_negativni(si, 9001, 9136, 3, 6)

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

        #00000-10
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-11
        if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8): 
            #U nijednoj od dve navedene forme kolona Napomena ne sme da bude popunjena
            bsNapomene = Zahtev.Forme['Bilans stanja'].TekstualnaPoljaForme;
            buNapomene = Zahtev.Forme['Bilans uspeha'].TekstualnaPoljaForme;
            if ( proveriNapomene(bsNapomene, 1, 3, 4) or proveriNapomene(bsNapomene, 9, 9, 4) or proveriNapomene(bsNapomene, 17, 18, 4) or proveriNapomene(bsNapomene, 28, 31, 4) or proveriNapomene(bsNapomene, 37, 38, 4) or proveriNapomene(bsNapomene, 44, 44, 4) or proveriNapomene(bsNapomene, 48, 48, 4) or proveriNapomene(bsNapomene, 57, 60, 4) or proveriNapomene(bsNapomene, 401, 408, 4) or proveriNapomene(bsNapomene, 411, 412, 4) or proveriNapomene(bsNapomene, 415, 416, 4) or proveriNapomene(bsNapomene, 420, 420, 4) or proveriNapomene(bsNapomene, 428, 433, 4) or proveriNapomene(bsNapomene, 441, 442, 4) or proveriNapomene(bsNapomene, 449, 449, 4) or proveriNapomene(bsNapomene, 453, 457, 4) or proveriNapomene(buNapomene, 1001, 1002, 4) or proveriNapomene(buNapomene, 1005, 1005, 4) or proveriNapomene(buNapomene, 1008, 1016, 4) or proveriNapomene(buNapomene, 1020, 1056, 4) ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Na AOP-u (0001 do 0003)  + 0009 + (0017 do 0018) + (0028 do 0031) + (0037 do 0038) + 0044 + 0048 + (0057 do 0060) bilansa stanja + (0401 do 0408) + (0411 do 0412) + (0415 do 0416) + 0420 + (0428 do 0433) + (0441 do 0442) + 0449 + (0453 do 0457) bilansa stanja + (1001 do 1002) + 1005 + (1008 do 1016) + (1020 do 1056) bilansa uspeha  u koloni 4 (Napomena broj) ne sme biti iskazan podatak kod obveznika koji nemaju obavezu dostavljanja napomena uz finansijski izveštaj.'
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ='Na AOP-u (0001 do 0003)  + 0009 + (0017 do 0018) + (0028 do 0031) + (0037 do 0038) + 0044 + 0048 + (0057 do 0060) bilansa stanja + (0401 do 0408) + (0411 do 0412) + (0415 do 0416) + 0420 + (0428 do 0433) + (0441 do 0442) + 0449 + (0453 do 0457) bilansa stanja + (1001 do 1002) + 1005 + (1008 do 1016) + (1020 do 1056) bilansa uspeha  u koloni 4 (Napomena broj) ne sme biti iskazan podatak kod obveznika koji nemaju obavezu dostavljanja napomena uz finansijski izveštaj.'
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        
        #BILANS STANJA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        #00001
        #Za ovaj set se ne primenjuje pravilo 
        
        #00002
        if not( suma(bs,1,3,5)+aop(bs,9,5)+suma(bs,17,18,5)+suma(bs,28,31,5)+suma(bs,37,38,5)+aop(bs,44,5)+aop(bs,48,5)+suma(bs,57,60,5)+suma(bs,401,408,5)+suma(bs,411,412,5)+suma(bs,415,416,5)+aop(bs,420,5)+suma(bs,428,433,5)+suma(bs,441,442,5)+aop(bs,449,5)+suma(bs,453,457,5) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0003) kol. 5 + 0009 kol.5 + (0017 do 0018) kol.5 + (0028 do 0031) kol.5 + (0037 do 0038) kol.5 + 0044 kol. 5 + 0048 kol.5 + (0057 do 0060) kol. 5 + (0401 do 0408) kol. 5 + (0411 do 0412) kol. 5 + (0415 do 0416) kol. 5 + 0420 kol. 5 + (0428 do 0433) kol. 5 + (0441 do 0442) kol.5 + 0449 kol. 5 + (0453 do 0457) kol. 5  > 0 Bilans stanja, po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #00003
        #Za ovaj set se ne primenjuje pravilo 
        
        #00004
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,3,6)+aop(bs,9,6)+suma(bs,17,18,6)+suma(bs,28,31,6)+suma(bs,37,38,6)+aop(bs,44,6)+aop(bs,48,6)+suma(bs,57,60,6)+suma(bs,401,408,6)+suma(bs,411,412,6)+suma(bs,415,416,6)+aop(bs,420,6)+suma(bs,428,433,6)+suma(bs,441,442,6)+aop(bs,449,6)+suma(bs,453,457,6) == 0 ):
                lzbir =  suma(bs,1,3,6)+aop(bs,9,6)+suma(bs,17,18,6)+suma(bs,28,31,6)+suma(bs,37,38,6)+aop(bs,44,6)+aop(bs,48,6)+suma(bs,57,60,6)+suma(bs,401,408,6)+suma(bs,411,412,6)+suma(bs,415,416,6)+aop(bs,420,6)+suma(bs,428,433,6)+suma(bs,441,442,6)+aop(bs,449,6)+suma(bs,453,457,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0003) kol. 6 + 0009 kol. 6 + (0017 do 0018) kol. 6 + (0028 do 0031) kol. 6 + (0037 do 0038) kol. 6 + 0044 kol. 6 + 0048 kol. 6 + (0057 do 0060) kol. 6 + (0401 do 0408) kol. 6 + (0411 do 0412) kol. 6 + (0415 do 0416) kol. 6 + 0420 kol. 6 + (0428 do 0433) kol. 6 + (0441 do 0442) kol. 6 + 0449 kol. 6 + (0453 do 0457) kol. 6  =  0 Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00005
        #Za ovaj set se ne primenjuje pravilo 
        
        #00006
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,3,7)+aop(bs,9,7)+suma(bs,17,18,7)+suma(bs,28,31,7)+suma(bs,37,38,7)+aop(bs,44,7)+aop(bs,48,7)+suma(bs,57,60,7)+suma(bs,401,408,7)+suma(bs,411,412,7)+suma(bs,415,416,7)+aop(bs,420,7)+suma(bs,428,433,7)+suma(bs,441,442,7)+aop(bs,449,7)+suma(bs,453,457,7) == 0 ):
                lzbir =  suma(bs,1,3,7)+aop(bs,9,7)+suma(bs,17,18,7)+suma(bs,28,31,7)+suma(bs,37,38,7)+aop(bs,44,7)+aop(bs,48,7)+suma(bs,57,60,7)+suma(bs,401,408,7)+suma(bs,411,412,7)+suma(bs,415,416,7)+aop(bs,420,7)+suma(bs,428,433,7)+suma(bs,441,442,7)+aop(bs,449,7)+suma(bs,453,457,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0003) kol. 7 + 0009 kol. 7 + (0017 do 0018) kol. 7 + (0028 do 0031) kol. 7 + (0037 do 0038) kol. 7 + 0044 kol. 7 + 0048 kol. 7 + (0057 do 0060) kol. 7 + (0401 do 0408) kol. 7 + (0411 do 0412) kol. 7 + (0415 do 0416) kol. 7 + 0420 kol. 7 + (0428 do 0433) kol. 7 + (0441 do 0442) kol. 7 + 0449 kol. 7 + (0453 do 0457) kol. 7  =  0 Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00007
        #Za ovaj set se ne primenjuje pravilo 
        
        #00008
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,3,6)+aop(bs,9,6)+suma(bs,17,18,6)+suma(bs,28,31,6)+suma(bs,37,38,6)+aop(bs,44,6)+aop(bs,48,6)+suma(bs,57,60,6)+suma(bs,401,408,6)+suma(bs,411,412,6)+suma(bs,415,416,6)+aop(bs,420,6)+suma(bs,428,433,6)+suma(bs,441,442,6)+aop(bs,449,6)+suma(bs,453,457,6) > 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0003) kol. 6 + 0009 kol. 6 + (0017 do 0018) kol. 6 + (0028 do 0031) kol. 6 + (0037 do 0038) kol. 6 + 0044 kol. 6 + 0048 kol. 6 + (0057 do 0060) kol. 6 + (0401 do 0408) kol. 6 + (0411 do 0412) kol. 6 + (0415 do 0416) kol. 6 + 0420 kol. 6 + (0428 do 0433) kol. 6 + (0441 do 0442) kol. 6 + 0449 kol. 6 + (0453 do 0457) kol. 6 > 0 Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #00009
        #Za ovaj set se ne primenjuje pravilo 
        
        #00010
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,3,7)+aop(bs,9,7)+suma(bs,17,18,7)+suma(bs,28,31,7)+suma(bs,37,38,7)+aop(bs,44,7)+aop(bs,48,7)+suma(bs,57,60,7)+suma(bs,401,408,7)+suma(bs,411,412,7)+suma(bs,415,416,7)+aop(bs,420,7)+suma(bs,428,433,7)+suma(bs,441,442,7)+aop(bs,449,7)+suma(bs,453,457,7) > 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0003) kol. 7 + 0009 kol. 7 + (0017 do 0018) kol. 7 + (0028 do 0031) kol. 7 + (0037 do 0038) kol. 7 + 0044 kol. 7 + 0048 kol. 7 + (0057 do 0060) kol. 7 + (0401 do 0408) kol. 7 + (0411 do 0412) kol. 7 + (0415 do 0416) kol. 7 + 0420 kol. 7 + (0428 do 0433) kol. 7 + (0441 do 0442) kol. 7 + 0449 kol. 7 + (0453 do 0457) kol. 7  > 0 Bilans stanja, po pravilu,  mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
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
        #Za ovaj set se ne primenjuje pravilo 
        
        #00015
        #Za ovaj set se ne primenjuje pravilo 
        
        #00016
        #Za ovaj set se ne primenjuje pravilo 
        
        #00017
        #Za ovaj set se ne primenjuje pravilo 
        
        #00018
        #Za ovaj set se ne primenjuje pravilo 
        
        #00019
        #Za ovaj set se ne primenjuje pravilo 
        
        #00020
        #Za ovaj set se ne primenjuje pravilo 
        
        #00021
        #Za ovaj set se ne primenjuje pravilo 
        
        #00022
        #Za ovaj set se ne primenjuje pravilo 
        
        #00023
        #Za ovaj set se ne primenjuje pravilo 
        
        #00024
        #Za ovaj set se ne primenjuje pravilo 
        
        #00025
        #Za ovaj set se ne primenjuje pravilo 
        
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
        #Za ovaj set se ne primenjuje pravilo 
        
        #00030
        #Za ovaj set se ne primenjuje pravilo 
        
        #00031
        #Za ovaj set se ne primenjuje pravilo 
        
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
        #Za ovaj set se ne primenjuje pravilo 
        
        #00039
        #Za ovaj set se ne primenjuje pravilo 
        
        #00040
        #Za ovaj set se ne primenjuje pravilo 
        
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
        #Za ovaj set se ne primenjuje pravilo 
        
        #00051
        #Za ovaj set se ne primenjuje pravilo 
        
        #00052
        #Za ovaj set se ne primenjuje pravilo 
        
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
        #Za ovaj set se ne primenjuje pravilo 
        
        #00057
        #Za ovaj set se ne primenjuje pravilo 
        
        #00058
        #Za ovaj set se ne primenjuje pravilo 
        
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
        #Za ovaj set se ne primenjuje pravilo 
        
        #00063
        #Za ovaj set se ne primenjuje pravilo 
        
        #00064
        #Za ovaj set se ne primenjuje pravilo 
        
        #00065
        #Za ovaj set se ne primenjuje pravilo 
        
        #00066
        #Za ovaj set se ne primenjuje pravilo 
        
        #00067
        #Za ovaj set se ne primenjuje pravilo 
        
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
        #Za ovaj set se ne primenjuje pravilo 
        
        #00072
        #Za ovaj set se ne primenjuje pravilo 
        
        #00073
        #Za ovaj set se ne primenjuje pravilo 
        
        #00074
        #Za ovaj set se ne primenjuje pravilo 
        
        #00075
        #Za ovaj set se ne primenjuje pravilo 
        
        #00076
        #Za ovaj set se ne primenjuje pravilo 
        
        #00077
        #Za ovaj set se ne primenjuje pravilo 
        
        #00078
        #Za ovaj set se ne primenjuje pravilo 
        
        #00079
        #Za ovaj set se ne primenjuje pravilo 
        
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
        #Za ovaj set se ne primenjuje pravilo 
        
        #00117
        if( suma(bu,1001,1002,5)+aop(bu,1005,5)+suma(bu,1008,1016,5)+suma(bu,1020,1056,5) > 0 ):
            if not( suma(bs,1,3,5)+aop(bs,9,5)+suma(bs,17,18,5)+suma(bs,28,31,5)+suma(bs,37,38,5)+aop(bs,44,5)+aop(bs,48,5)+suma(bs,57,60,5)+suma(bs,401,408,5)+suma(bs,411,412,5)+suma(bs,415,416,5)+aop(bs,420,5)+suma(bs,428,433,5)+suma(bs,441,442,5)+aop(bs,449,5)+suma(bs,453,457,5) != suma(bs,1,3,6)+aop(bs,9,6)+suma(bs,17,18,6)+suma(bs,28,31,6)+suma(bs,37,38,6)+aop(bs,44,6)+aop(bs,48,6)+suma(bs,57,60,6)+suma(bs,401,408,6)+suma(bs,411,412,6)+suma(bs,415,416,6)+aop(bs,420,6)+suma(bs,428,433,6)+suma(bs,441,442,6)+aop(bs,449,6)+suma(bs,453,457,6) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='***Ako je zbir podataka na oznakama za AOP (1001 do 1002) kol. 5 + 1005 kol. 5 + (1008 do 1016) kol. 5 + (1020 do 1056) kol. 5 bilansa uspeha > 0 onda zbir podataka na oznakama za AOP (0001 do 0003) kol. 5 + 0009 kol. 5 + (0017 do 0018) kol. 5 + (0028 do 0031) kol. 5 + (0037 do 0038) kol. 5 + 0044 kol. 5 + 0048 kol. 5 + (0057 do 0060) kol. 5 bilansa stanja + (0401 do 0408) kol. 5 + (0411 do 0412) kol. 5 + (0415 do 0416) kol. 5 + 0420 kol. 5 + (0428 do 0433) kol. 5 + (0441 do 0442) kol. 5 + 0449 kol. 5 + (0453 do 0457) kol. 5 bilansa stanja ≠ zbiru podataka na oznakama za AOP (0001 do 0003) kol. 6 + 0009 kol. 6 + (0017 do 0018) kol. 6 + (0028 do 0031) kol. 6 + (0037 do 0038) kol. 6 + 0044 kol. 6 + 0048 kol. 6 + (0057 do 0060) kol. 6 bilansa stanja + (0401 do 0408) kol. 6 + (0411 do 0412) kol. 6 + (0415 do 0416) kol. 6 + 0420 kol. 6 + (0428 do 0433) kol. 6 + (0441 do 0442) kol. 6 + 0449 kol. 6 + (0453 do 0457) kol. 6 bilansa stanja Zbirovi podataka u kolonama 5 i 6 bilansa stanja su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama;  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='***Ako je zbir podataka na oznakama za AOP (1001 do 1002) kol. 5 + 1005 kol. 5 + (1008 do 1016) kol. 5 + (1020 do 1056) kol. 5 bilansa uspeha > 0 onda zbir podataka na oznakama za AOP (0001 do 0003) kol. 5 + 0009 kol. 5 + (0017 do 0018) kol. 5 + (0028 do 0031) kol. 5 + (0037 do 0038) kol. 5 + 0044 kol. 5 + 0048 kol. 5 + (0057 do 0060) kol. 5 bilansa stanja + (0401 do 0408) kol. 5 + (0411 do 0412) kol. 5 + (0415 do 0416) kol. 5 + 0420 kol. 5 + (0428 do 0433) kol. 5 + (0441 do 0442) kol. 5 + 0449 kol. 5 + (0453 do 0457) kol. 5 bilansa stanja ≠ zbiru podataka na oznakama za AOP (0001 do 0003) kol. 6 + 0009 kol. 6 + (0017 do 0018) kol. 6 + (0028 do 0031) kol. 6 + (0037 do 0038) kol. 6 + 0044 kol. 6 + 0048 kol. 6 + (0057 do 0060) kol. 6 bilansa stanja + (0401 do 0408) kol. 6 + (0411 do 0412) kol. 6 + (0415 do 0416) kol. 6 + 0420 kol. 6 + (0428 do 0433) kol. 6 + (0441 do 0442) kol. 6 + 0449 kol. 6 + (0453 do 0457) kol. 6 bilansa stanja Zbirovi podataka u kolonama 5 i 6 bilansa stanja su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama;  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #BILANS USPEHA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #10001
        #Za ovaj set se ne primenjuje pravilo 
        
        #10002
        if not( suma(bu,1001,1002,5)+aop(bu,1005,5)+suma(bu,1008,1016,5)+suma(bu,1020,1056,5) > 0 ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP (1001 do 1002)  kol. 5 + 1005  kol. 5 + (1008 do 1016) kol. 5 + (1020 do 1056)  kol. 5 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #10003
        #Za ovaj set se ne primenjuje pravilo 
        
        #10004
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bu,1001,1002,6)+aop(bu,1005,6)+suma(bu,1008,1016,6)+suma(bu,1020,1056,6) == 0 ):
                lzbir =  suma(bu,1001,1002,6)+aop(bu,1005,6)+suma(bu,1008,1016,6)+suma(bu,1020,1056,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Zbir podataka na oznakama za AOP (1001 do 1002)  kol. 6 + 1005  kol. 6 + (1008 do 1016) kol. 6 + (1020 do 1056)  kol. 6 = 0 Bilans uspeha za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10005
        #Za ovaj set se ne primenjuje pravilo 
        
        #10006
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bu,1001,1002,6)+aop(bu,1005,6)+suma(bu,1008,1016,6)+suma(bu,1020,1056,6) > 0 ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Zbir podataka na oznakama za AOP (1001 do 1002)  kol. 6 + 1005  kol. 6 + (1008 do 1016) kol. 6 + (1020 do 1056)  kol. 6  > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
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
        #Za ovaj set se ne primenjuje pravilo 
        
        #10010
        #Za ovaj set se ne primenjuje pravilo 
        
        #10011
        #Za ovaj set se ne primenjuje pravilo 
        
        #10012
        #Za ovaj set se ne primenjuje pravilo 
        
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
        #Za ovaj set se ne primenjuje pravilo 
        
        #10016
        #Za ovaj set se ne primenjuje pravilo 
        
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
        #Za ovaj set se ne primenjuje pravilo 
        
        #10106
        #Za ovaj set se ne primenjuje pravilo 
        
        #10107
        #Za ovaj set se ne primenjuje pravilo 
        
        #10108
        #Za ovaj set se ne primenjuje pravilo 
        
        #10109
        #Za ovaj set se ne primenjuje pravilo 
        
        #10110
        #Za ovaj set se ne primenjuje pravilo 
        
        #10111
        #Za ovaj set se ne primenjuje pravilo 
        
        #10112
        #Za ovaj set se ne primenjuje pravilo 
        
        #10113
        if( aop(bu,1055,5) > 0 ):
            if not( aop(bs,408,5) >= aop(bu,1055,5) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1055 kol. 5 > 0, onda je AOP  0408 kol. 5 bilansa stanja ≥ AOP-a 1055 kol. 5  Neto dobitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu neraspoređenog dobitka u koloni tekuća godina u obrascu Bilans stanja; Ukoliko ti podaci nisu usaglašeni, zakonski zastupnik potpisivanjem izveštaja potvrđuje da je tako iskazan rezultat u Bilansu stanja ispravan i tačan, odnosno da je iskazan u skladu sa propisima. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1055 kol. 5 > 0, onda je AOP  0408 kol. 5 bilansa stanja ≥ AOP-a 1055 kol. 5  Neto dobitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu neraspoređenog dobitka u koloni tekuća godina u obrascu Bilans stanja; Ukoliko ti podaci nisu usaglašeni, zakonski zastupnik potpisivanjem izveštaja potvrđuje da je tako iskazan rezultat u Bilansu stanja ispravan i tačan, odnosno da je iskazan u skladu sa propisima. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10114
        if( aop(bu,1055,6) > 0 ):
            if not( aop(bs,408,6) >= aop(bu,1055,6) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1055 kol. 6 > 0, onda je AOP  0408 kol. 6 bilansa stanja ≥ AOP-a 1055 kol. 6  Neto dobitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu neraspoređenog dobitka u koloni prethodna godina u obrascu Bilans stanja.  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1055 kol. 6 > 0, onda je AOP  0408 kol. 6 bilansa stanja ≥ AOP-a 1055 kol. 6  Neto dobitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu neraspoređenog dobitka u koloni prethodna godina u obrascu Bilans stanja.  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10115
        if( aop(bu,1056,5) > 0 ):
            if not( aop(bs,412,5) >= aop(bu,1056,5) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1056 kol. 5 > 0, onda je AOP 0412 kol. 5 bilansa stanja ≥ AOP-a 1056 kol. 5  Neto gubitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu gubitka u koloni tekuća godina u obrascu Bilans stanja;  Ukoliko ti podaci nisu usaglašeni, zakonski zastupnik potpisivanjem izveštaja potvrđuje da je tako iskazan rezultat u bilansu stanja ispravan i tačan, odnosno da je iskazan u skladu sa propisima. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1056 kol. 5 > 0, onda je AOP 0412 kol. 5 bilansa stanja ≥ AOP-a 1056 kol. 5  Neto gubitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu gubitka u koloni tekuća godina u obrascu Bilans stanja;  Ukoliko ti podaci nisu usaglašeni, zakonski zastupnik potpisivanjem izveštaja potvrđuje da je tako iskazan rezultat u bilansu stanja ispravan i tačan, odnosno da je iskazan u skladu sa propisima. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10116
        if( aop(bu,1056,6) > 0 ):
            if not( aop(bs,412,6) >= aop(bu,1056,6) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1056 kol. 6 bilansa uspeha > 0, onda je AOP 0412 kol. 6 bilansa stanja ≥ AOP-a 1056 kol. 6 bilansa uspeha Neto gubitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu gubitka u koloni prethodna godina u obrascu Bilans stanja.   '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1056 kol. 6 bilansa uspeha > 0, onda je AOP 0412 kol. 6 bilansa stanja ≥ AOP-a 1056 kol. 6 bilansa uspeha Neto gubitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu gubitka u koloni prethodna godina u obrascu Bilans stanja.   '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
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
        #Za ovaj set se ne primenjuje pravilo 
        
        #10120
        if( suma(bu,1001,1002,5)+aop(bu,1005,5)+suma(bu,1008,1016,5)+suma(bu,1020,1056,5) > 0 ):
            if not( suma(bu,1001,1002,5)+aop(bu,1005,5)+suma(bu,1008,1016,5)+suma(bu,1020,1056,5) != suma(bu,1001,1002,6)+aop(bu,1005,6)+suma(bu,1008,1016,6)+suma(bu,1020,1056,6) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='***Ako je zbir podataka na oznakama za AOP (1001 do 1002) kol. 5 + 1005 kol. 5 + (1008 do 1016) kol. 5 + (1020 do 1056)  kol. 5 bilansa uspeha > 0 onda zbir podataka na oznakama za AOP (1001 do 1002) kol. 5 + 1005 kol. 5 + (1008 do 1016) kol. 5 + (1020 do 1056)  kol. 5 bilansa uspeha≠ zbiru podataka na oznakama za AOP (1001 do 1002) kol. 6 + 1005 kol. 6 + (1008 do 1016) kol. 6 + (1020 do 1056)  kol. 6 bilansa uspeha Zbirovi podataka u kolonama 5 i 6 bilansa uspeha su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama;  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        
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
            if not( 1 <= aop(si,9001,4) and aop(si, 9001, 4) <= 12 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='1 ≤ AOP-a 9001 kol. 4 ≤ 12  Broj meseci poslovanja obveznika osnovanih u ranijim godinama, po pravilu, mora biti iskazan u intervalu između 1 i 12; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #90006
        if not(Zahtev.ObveznikInfo.Novoosnovan == True ):
            if not( aop(si,9001,3) == 12 ):
                lzbir =  aop(si,9001,3) 
                dzbir =  12 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='AOP 9001 kol. 3 = 12 Broj meseci poslovanja obveznika osnovanih ranijih godina mora biti 12, osim za obveznike koji su kupljeni iz stečaja '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
        #90007
        if not(Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if not( 1 <= aop(si,9002,3) and aop(si,9002,3) <= 5 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='1 ≤ AOP-a 9002 kol. 3 ≤ 5  Oznaka za vlasništvo mora biti iskazana u intervalu između 1 i 5; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
        #90008
        if(Zahtev.ObveznikInfo.Novoosnovan == False and Zahtev.ObveznikInfo.GrupaObveznika.value__ != 8 ): 
            if not( 1 <= aop(si,9002,4) and aop(si,9002,4) <= 5 ):
                
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
                    poruka  ='AOP 9002 kol. 4 = 2 Oznaka za vlasništvo kod preduzetnika mora biti obavezno 2 (privatno ); Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
        
        #90011
        if not (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if( aop(si,9003,3) > 0 ):
                if not( suma_liste(si,[9046,9048,9050],4) > 0 ):
                    
                    naziv_obrasca='Statistički izveštaj'
                    poruka  ='Ako je AOP 9003 kol. 3 > 0, onda je zbir AOP-a (9046 + 9048 + 9050) kol. 4 > 0 Ukoliko u kapitalu učestvuju strana lica, mora biti iskazana vrednost stranog kapitala, ako je veća od 500,00 RSD; Ukoliko podaci o vrednosti kapitala nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje da je vrednost tog kapitala manja od 500,00 RSD '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
            
        #90012
        if not (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if( suma_liste(si,[9046,9048,9050],4) > 0 ):
                if not( aop(si,9003,3) > 0 ):
                    
                    naziv_obrasca='Statistički izveštaj'
                    poruka  ='Ako je zbir AOP-a (9046 + 9048 + 9050) kol. 4 > 0 onda je AOP 9003 kol. 3 > 0 Ukoliko je iskazana vrednost stranog kapitala, obveznik mora iskazati broj stranih lica koja učestvuju u kapitalu; '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
        #90013
        if not (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if( aop(si,9003,4) > 0 ):
                if not( suma_liste(si,[9046,9048,9050],5) > 0 ):
                    
                    naziv_obrasca='Statistički izveštaj'
                    poruka  ='Ako je AOP 9003 kol. 4 > 0, onda je zbir AOP-a (9046 + 9048 + 9050) kol. 5 > 0  Ukoliko u kapitalu učestvuju strana lica, mora biti iskazana vrednost stranog kapitala, ako je veća od 500,00 RSD; Ukoliko podaci o vrednosti kapitala nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje da je vrednost tog kapitala manja od 500,00 RSD '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
            
        #90014
        if not (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if( suma_liste(si,[9046,9048,9050],5) > 0 ):
                if not( aop(si,9003,4) > 0 ):
                    
                    naziv_obrasca='Statistički izveštaj'
                    poruka  ='Ako je zbir AOP-a (9046 + 9048 + 9050) kol. 5 > 0 onda je AOP 9003 kol. 4 > 0 Ukoliko je iskazana vrednost stranog kapitala, obveznik mora iskazati broj stranih lica koja učestvuju u kapitalu; '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
        #90015
        if not (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            if not( aop(si,9004,3) <= aop(si,9003,3) ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='AOP 9004 kol. 3 ≤ AOP-a 9003 kol. 3  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
        #90016
        if not (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
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
        #Za ovaj set se ne primenjuje pravilo 
        
        #90025
        #Za ovaj set se ne primenjuje pravilo 
        
        #90026
        if not( aop(si,9005,3) <= 50 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9005 kol. 3 ≤ 50 Granične vrednosti date su da bi se izbegle slučajne greške prilikom iskazivanja broja zaposlenih; Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90027
        if not( aop(si,9005,4) <= 50 ):
            
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
        if not( aop(si,9008,6) == aop(si,9008,4)+aop(si,9008,5) ):
            lzbir =  aop(si,9008,6) 
            dzbir =  aop(si,9008,4)+aop(si,9008,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9008 kol. 6 = AOP-u 9008 kol. 4 - AOP 9008 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90035
        if not( aop(si,9015,6) == aop(si,9015,4)+aop(si,9015,5) ):
            lzbir =  aop(si,9015,6) 
            dzbir =  aop(si,9015,4)+aop(si,9015,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9015 kol. 6 = AOP-u 9015 kol. 4 - AOP 9015 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90036
        if not( aop(si,9016,6) == aop(si,9016,4)+aop(si,9016,5) ):
            lzbir =  aop(si,9016,6) 
            dzbir =  aop(si,9016,4)+aop(si,9016,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9016 kol. 6 = AOP-u 9016 kol. 4 - AOP 9016 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90037
        if not( aop(si,9022,6) == aop(si,9022,4)+aop(si,9022,5) ):
            lzbir =  aop(si,9022,6) 
            dzbir =  aop(si,9022,4)+aop(si,9022,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9022 kol. 6 = AOP-u 9022 kol. 4 - AOP 9022 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90038
        if not( aop(si,9023,6) == aop(si,9023,4)+aop(si,9023,5) ):
            lzbir =  aop(si,9023,6) 
            dzbir =  aop(si,9023,4)+aop(si,9023,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9023 kol. 6 = AOP-u 9023 kol. 4 - AOP 9023 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90039
        if not( aop(si,9030,6) == aop(si,9030,4)+aop(si,9030,5) ):
            lzbir =  aop(si,9030,6) 
            dzbir =  aop(si,9030,4)+aop(si,9030,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9030 kol. 6 = AOP-u 9030 kol. 4 - AOP 9030 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90040
        if not( aop(si,9031,6) == aop(si,9031,4)+aop(si,9031,5) ):
            lzbir =  aop(si,9031,6) 
            dzbir =  aop(si,9031,4)+aop(si,9031,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9031 kol. 6 = AOP-u 9031 kol. 4 - AOP 9031 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90041
        if not( aop(si,9037,6) == aop(si,9037,4)+aop(si,9037,5) ):
            lzbir =  aop(si,9037,6) 
            dzbir =  aop(si,9037,4)+aop(si,9037,5) 
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
        #Za ovaj set se ne primenjuje pravilo 
        
        #90101
        #Za ovaj set se ne primenjuje pravilo 
        
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
        if not( aop(si,9127,6) == aop(si,9127,4)+aop(si,9127,5) ):
            lzbir =  aop(si,9127,6) 
            dzbir =  aop(si,9127,4)+aop(si,9127,5) 
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
        if not( aop(si,9128,6) == aop(si,9128,4)+aop(si,9128,5) ):
            lzbir =  aop(si,9128,6) 
            dzbir =  aop(si,9128,4)+aop(si,9128,5) 
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
        if not( aop(si,9129,6) == aop(si,9129,4)+aop(si,9129,5) ):
            lzbir =  aop(si,9129,6) 
            dzbir =  aop(si,9129,4)+aop(si,9129,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9129 kol. 6 = AOP-u 9129 kol. 4 - AOP 9129 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90150
        if not( aop(si,9130,6) == aop(si,9130,4)+aop(si,9130,5) ):
            lzbir =  aop(si,9130,6) 
            dzbir =  aop(si,9130,4)+aop(si,9130,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9130 kol. 6 = AOP-u 9130 kol. 4 - AOP 9130 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90151
        if not( aop(si,9131,6) == aop(si,9131,4)+aop(si,9131,5) ):
            lzbir =  aop(si,9131,6) 
            dzbir =  aop(si,9131,4)+aop(si,9131,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9131 kol. 6 = AOP-u 9131 kol. 4 - AOP 9131 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90152
        if not( aop(si,9132,6) == aop(si,9132,4)+aop(si,9132,5) ):
            lzbir =  aop(si,9132,6) 
            dzbir =  aop(si,9132,4)+aop(si,9132,5) 
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
        #Za ovaj set se ne primenjuje pravilo 
        
        #POSEBNI PODACI:
        #●PRAVILO NE TREBA DA BUDE VIDLJIVO ZA KORISNIKA, ODNOSNO ZA OBVEZNIKA TREBA DA VIDI SAMO KOMENTAR KOJI JE DAT UZ PRAVILO. 
        #●U OBRASCU NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        #●PLATNE INSTITUCIJE I FAKTORING DRUŠTVA POPUNJAVAJU SAMO POLJE "VELIČINA ZA NAREDNU POSLOVNU GODINU"
        
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
        #Za ovaj set se ne primenjuje pravilo 
        
        #100004
        if not( aop(pp,10002,1) >= 0 ):
            
            naziv_obrasca='Posebni podaci'
            poruka  ='Podatak o prosečnom broju zaposlenih u tekućoj godini u obrascu Posebni podaci mora biti upisan; ako nema zaposlenih upisuje se broj 0'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            
        #100005
        #Za ovaj set se ne primenjuje pravilo 
        
        #100006
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
        #Za ovaj set se ne primenjuje pravilo 
        
        #100009
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
        #Za ovaj set se ne primenjuje pravilo 
        
        #100011
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
        if not( aop(pp,10102,1) >= 0 ):
            
            naziv_obrasca='Posebni podaci'
            poruka  ='Podatak o prosečnom broju zaposlenih u prethodnoj godini,  mora biti upisan; ako nema zaposlenih upisuje se broj 0'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
         
        #100013
        #Za ovaj set se ne primenjuje pravilo 
        
        #100014
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
        #Za ovaj set se ne primenjuje pravilo 
        
        #100016
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
        #Za ovaj set se ne primenjuje pravilo 
        
        #100018
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
        #Za ovaj set se ne primenjuje pravilo 
        
        #100020
        if not( aop(pp,10110,1) == aop(bu, 1043, 6) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='  Podatak o ukupnom prihodu prethodne godine, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Bilans uspeha na AOP poziciji 1043 u koloni 6.'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Posebni podaci'
            poruka  ='  Podatak o ukupnom prihodu prethodne godine, u delu posebni podaci, mora biti jednak iskazanom podatku u obrascu Bilans uspeha na AOP poziciji 1043 u koloni 6.'
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

        
