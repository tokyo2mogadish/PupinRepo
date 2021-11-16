import sys
import re
#sys.path.append(r"C:\IronPython2.7\Lib")
#import traceback
import datetime
from System import DateTime

exceptionList = []

#Vraca numericka polja forme
def getForme(Zahtev,nazivForme):
    if nazivForme in Zahtev.Forme:
        return Zahtev.Forme[nazivForme].NumerickaPoljaForme
    else:
        raise Exception('Obrazac pod nazivom: '+nazivForme+' ne postoji')

#BROJ KONVERTUJE U AOP KEY FORMATA aop-0000-0
def broj_u_aop(aop_broj, broj_kolone):
    seq = ("aop", str(aop_broj).zfill(4), str(broj_kolone))
    aop_key = "_".join(seq)
    return aop_key

#VRACA VREDNOST AOP POLJA. AKO POLJE DICTIONARY-ja NEMA VREDNOST, VRACA NULU
def aop(aop_dict, aop_broj, kolona):   
    aop_key = broj_u_aop(aop_broj, kolona)

    if aop_key in aop_dict:
        a=aop_dict[aop_key]
       
        if a is None:
            return 0
        return a

    raise Exception('Validacion skripta očekuje ' + aop_key + ' koji nije pronadjen')

#VRACA VREDNOST AOP POLJA. AKO POLJE DICTIONARY-ja NEMA VREDNOST, VRACA -1
def aop_1(aop_dict, aop_broj, kolona):   
    aop_key = broj_u_aop(aop_broj, kolona)

    if aop_key in aop_dict:
        a=aop_dict[aop_key]
       
        if a is None:
            return -1
        return a

    raise Exception('Validacion skripta očekuje ' + aop_key + ' koji nije pronadjen')

#SUMA AOPA SA LISTE
def suma_liste(aop_dict, lista, kolona):
    sum = 0
    for x in lista:
        sum += aop(aop_dict, x, kolona)
    return sum

#VRACA TRUE AKO JE JE OBVEZNIK JAVNO PREDUZECE ILI FALSE AKO NIJE
def jeste_javno_preduzece(Zahtev):
    if Zahtev.ObveznikInfo.PodgrupaObveznika.value__ == 78:
        return True
    return False

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

        pz = getForme(Zahtev,'Predmet zamene') 

        #Provera da li su upisani podaci o prijemu
        
        #Provera da li lice odgovorno za sastavljanje je upisano
        if (Zahtev.LiceOdgovornoZaSastavljanje is None):
            ostalo_errors.append('Podaci za lice odgovorno za sastavljanje finansijskog izveštaja nisu upisani.')


       #Provera da li lice odgovorno za potpisivanje
        if (len(Zahtev.Potpisnici) == 0):
            ostalo_errors.append('Podaci o potpisniku finansijskog izveštaja nisu upisani.')

        #Provera da li su prosledjeni obavezni ulazni dokumenti
        if (Zahtev.ValidacijaUlaznihDokumenataOmoguceno==True):
            if (Zahtev.NacinPodnosenja.value__ == 1):
                if Zahtev.UlazniDokumenti.Count>0:
                    for k in Zahtev.UlazniDokumenti.Keys:
                        if Zahtev.UlazniDokumenti[k].Obavezan==True and Zahtev.UlazniDokumenti[k].Barkod == None:
                            doc_errors.append('Dokument sa nazivom "'+Zahtev.UlazniDokumenti[k].Naziv+'" niste priložili.') 
                
        
          
                             
        #Provera da li zahtev sadrži formu sa nazivom predmet zamene
        # if (Zahtev.NacinPodnosenja.value__ == 1 or (Zahtev.NacinPodnosenja.value__ == 3 and  Zahtev.FiStanje.value__ > 0)):          
        #     if len(pz)==0:
        #         form_errors.append('Obrazac predmet zamene nije popunjen') 

        # Provera da li zahtev do sada ima form_errors, ako ima odmah vraca greske, bey obyira na nacin podnosenja i stanje#############################################################
        if (len(form_errors)>0):            
            return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors, 'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings,'exceptions': exceptionList}
        

        ######################################
        ######################################
        #### POCETAK KONTROLNIH PRAVILA ######
        ######################################
        ######################################


        ### Provera da li je fizahtev placen ###########################################################################################################################################
        if not(Zahtev.Placen):
            ostalo_warnings.append('Naknada za obradu i javno objavljivanje zahteva za zamenu dokumentacije nije uplaćena u propisanom iznosu. Instrukcije za uplatu propisane naknade date su u okviru PIS FI sistema za konkretan zahtev, na linku „Status naplate zahteva / Instrukcija za plaćanje". Ukoliko ste izvršili uplatu, a naknada nije uparena, priložite Dokaz o uplati naknade u delu Dokumentacija (na mestu predviđenom za dokaz o uplati naknade), kako biste mogli da podnesete izveštaj.');
        ################################################################################################################################################################################

        ### Polje može biti prazno ili u njega mogu biti uneti vrednosti 0 ili 1. U drugom slučaju vraća grešku. Metoda aop() vraca 0 ako je polje prazno ##################################################################
        neispravanUnosBrojac = 0
        if (aop(pz,21001,1) != 0 and aop(pz,21001,1) != 1):
            neispravanUnosBrojac += 1
        if (aop(pz,21002,1) != 0 and aop(pz,21002,1) != 1):
            neispravanUnosBrojac += 1        
        if (aop(pz,21003,1) != 0 and aop(pz,21003,1) != 1):
            neispravanUnosBrojac += 1
        if (aop(pz,21004,1) != 0 and aop(pz,21004,1) != 1):
            neispravanUnosBrojac += 1
        if (aop(pz,21005,1) != 0 and aop(pz,21005,1) != 1):
            neispravanUnosBrojac += 1
        if (aop(pz,21006,1) != 0 and aop(pz,21006,1) != 1):
            neispravanUnosBrojac += 1
        if (aop(pz,21007,1) != 0 and aop(pz,21007,1) != 1):
            neispravanUnosBrojac += 1
        if neispravanUnosBrojac > 0:
            naziv_obrasca='Predmet zamene'
            poruka  ='Vrednosti u poljima forme mogu biti samo brojevi 0 ili 1'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        ################################################################################################################################################################################           

        ### Proverava da li je uzabran bar jedan predmet zamene #######################################################################################################################
        if suma_liste(pz, [21001, 21002, 21003, 21004, 21005, 21006, 21007], 1) == 0:
            naziv_obrasca='Predmet zamene'
            poruka  ='Izaberite predmet zamene!'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        ################################################################################################################################################################################

        ################################################################################################################################################################################
        ### POCETAK PROVERA ZA SVAKI AOP ##############################################################################################################################################
        ################################################################################################################################################################################


        ##### Ako je označen aop-21001-1 aop-21001-1 aop-21001-1 aop-21001-1 aop-21001-1 aop-21001-1 aop-21001-1 aop-21001-1 aop-21001-1 aop-21001-1 aop-21001-1 aop-21001-1 aop-21001-1:
        if aop(pz,21001,1) == 1:

            # Ograničenja vezana za vrstu i grupu obvznika - e=ne mo\e istovremeno da oynači ---------------------------------------------------------------------------------------------------------------------

            # Ogranicenja vezana za kombinovanje sa drugim predmetima zamene - ne moze istovremeno da oznaci AOP-e aop-21007-1
            if aop(pz,21002,1) == 1:
                if 'Izabrana je nedozvoljena kombinacija predmeta zamene!' not in form_errors:
                    
                    naziv_obrasca='Predmet zamene'
                    poruka  ='Izabrana je nedozvoljena kombinacija predmeta zamene!'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            # Ogranicenja vezana za kombinovanje sa drugim predmetima zamene - NEMA ---------------------------------------------------------------------------------------------------

            # Provera dokumentacije za izabrani predmet zamene ------------------------------------------------------------------------------------------------------------------------
            # Ako je označio aop-21001-1 MORA DA POSTOJI ULAZNI DOKUMENT 1. 'Одлука о усвајању финансијског извештаја'
            # Prolazi kroz niz key-eva dictionary-ja i ako ispuni uslov inkrementira brojac
            brojacIspravnihPrilozenihDokumenata = 0
            for k in Zahtev.UlazniDokumenti.Keys:
                if Zahtev.UlazniDokumenti[k].Barkod != None:
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Odluka o usvajanju finansijskog izveštaja':    
                        brojacIspravnihPrilozenihDokumenata += 1
            # Ako je brojac nula znaci da nije dodat odgovarajuci dokument i vraca se greska
            if brojacIspravnihPrilozenihDokumenata == 0:
                if 'Niste priložili dokument "Odluka o usvajanju finansijskog izveštaja"' not in doc_errors:  
                    doc_errors.append('Niste priložili dokument "Odluka o usvajanju finansijskog izveštaja"')
                 
            #Ostali dokumenti ne smeju biti priloženi osim ako nisu izabrani odgovarajuci predmeti zamene
            for k in Zahtev.UlazniDokumenti.Keys:
                if Zahtev.UlazniDokumenti[k].Barkod != None:
                    # Dokument 1. 'Odluka o usvajanju finansijskog izveštaja' se ne proverava u ovoj petlji
                    # Dokument 3. 'Godišnji izveštaj o poslovanju izmenjene sadržine' ne može biti priložen ako nije označen aop-21003-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Godišnji izveštaj o poslovanju izmenjene sadržine':
                        if aop(pz,21005,1) == 0:
                            if 'Označeni dokument "Godišnji izveštaj o poslovanju izmenjene sadržine" nije dozvoljen za izabrani predmet zamene' not in doc_errors:   
                                doc_errors.append('Označeni dokument "Godišnji izveštaj o poslovanju izmenjene sadržine" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 4.'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije' ne može biti priložen ako nije označen aop-21004-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije':
                        if aop(pz,21003,1) == 0 and aop(pz,21004,1) == 0:
                            if 'Označeni dokument "Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije" nije dozvoljen za izabrani predmet zamene' not in doc_errors:   
                                doc_errors.append('Označeni dokument "Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 5.'Izjašnjenje odgovornog lica o razlozima zamene' ne može biti priložen nisje označen bilo koji drugi aop
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Izjašnjenje odgovornog lica o razlozima zamene':
                        if aop(pz,21002,1) == 0 and aop(pz,21003,1) == 0 and aop(pz,21004,1) == 0 and aop(pz,21005,1) == 0 and aop(pz,21006,1) == 0 and aop(pz,21007,1) == 0:
                            if 'Označeni dokument "Izjašnjenje odgovornog lica o razlozima zamene" nije dozvoljen za izabrani predmet zamene' not in doc_errors:   
                                doc_errors.append('Označeni dokument "Izjašnjenje odgovornog lica o razlozima zamene" nije dozvoljen za izabrani predmet zamene') 

        ################################################################################################################################################################################


        ##### Ako je označen aop-21003-1 aop-21003-1 aop-21003-1 aop-21003-1 aop-21003-1 aop-21003-1 aop-21003-1 aop-21003-1 aop-21003-1 aop-21003-1 aop-21003-1 aop-21003-1 aop-21003-1:
        if aop(pz,21005,1) == 1:

            # Ograničenja vezana za vrstu i grupu obvznika - primenjuju samo velika pravna lica i/ili javna drustva
            # if (Zahtev.ObveznikInfo.PodgrupaObveznika.value__ != 79 and Zahtev.ObveznikInfo.VelicinaObveznika.value__ != 4):
            #     if 'Godišnji izveštaj o poslovanju izmenjene sadržine je dozvoljen samo za velika pravna lica i javna društva' not in form_errors:  
                    
            #         naziv_obrasca='Predmet zamene'
            #         poruka  ='Godišnji izveštaj o poslovanju izmenjene sadržine je dozvoljen samo za velika pravna lica i javna društva'
            #         aop_pozicije=[]
            #         poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            #         form_errors.append(poruka_obrasca)

            # Ogranicenja vezana za kombinovanje sa drugim predmetima zamene - NEMA

            # Provera dokumentacije za izabrani predmet zamene ------------------------------------------------------------------------------------------------------------------------
            # Ako je označio aop-21003-1 MORA DA POSTOJI ULAZNI DOKUMENTI 3. 'Godišnji izveštaj o poslovanju izmenjene sadržine' i 5. 'Izjašnjenje odgovornog lica o razlozima zamene'   
            # Prolazi kroz niz key-eva dictionary-ja i ako ispuni uslov inkrementira brojac
            brojacIspravnihPrilozenihDokumenata = 0
            for k in Zahtev.UlazniDokumenti.Keys:
                if Zahtev.UlazniDokumenti[k].Barkod != None:
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Godišnji izveštaj o poslovanju izmenjene sadržine':    
                        brojacIspravnihPrilozenihDokumenata += 1
            #Ako je brojac nula znaci da nije dodat odgovarajuci dokument i vraca se greska
            if brojacIspravnihPrilozenihDokumenata == 0:
                if 'Niste priložili dokument "Godišnji izveštaj o poslovanju izmenjene sadržine"' not in doc_errors:  
                    doc_errors.append('Niste priložili dokument "Godišnji izveštaj o poslovanju izmenjene sadržine"')

            brojacIspravnihPrilozenihDokumenata = 0
            for k in Zahtev.UlazniDokumenti.Keys:
                if Zahtev.UlazniDokumenti[k].Barkod != None:
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Izjašnjenje odgovornog lica o razlozima zamene':    
                        brojacIspravnihPrilozenihDokumenata += 1
            #Ako je brojac nula znaci da nije dodat odgovarajuci dokument i vraca se greska
            if brojacIspravnihPrilozenihDokumenata == 0:
                if 'Niste priložili dokument "Izjašnjenje odgovornog lica o razlozima zamene"' not in doc_errors:  
                    doc_errors.append('Niste priložili dokument "Izjašnjenje odgovornog lica o razlozima zamene"')

            #Ostali dokumenti ne smeju biti priloženi osim ako nisu izabrani odgovarajuci predmeti zamene
            for k in Zahtev.UlazniDokumenti.Keys:
                if Zahtev.UlazniDokumenti[k].Barkod != None:
                    # Dokument 1. 'Odluka o usvajanju finansijskog izveštaja' ne može biti priložen ako nije označen aop-21001-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Odluka o usvajanju finansijskog izveštaja':
                        if aop(pz,21001,1) == 0 and aop(pz,21002,1) == 0:
                            if 'Označeni dokument "Odluka o usvajanju finansijskog izveštaja" nije dozvoljen za izabrani predmet zamene' not in doc_errors:   
                                doc_errors.append('Označeni dokument "Odluka o usvajanju finansijskog izveštaja" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 3. 'Godišnji izveštaj o poslovanju izmenjene sadržine' se ne proverava u ovoj petlji
                    # Dokument 4.'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije' ne može biti priložen ako nije označen aop-21004-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije':
                        if aop(pz,21003,1) == 0 and aop(pz,21004,1) == 0:
                            if 'Označeni dokument "Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije" nije dozvoljen za izabrani predmet zamene' not in doc_errors:   
                                doc_errors.append('Označeni dokument "Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 5.'Izjašnjenje odgovornog lica o razlozima zamene' se ne proverava u ovoj petlji

        ################################################################################################################################################################################


        ##### Ako je označen aop-21004-1 aop-21004-1 aop-21004-1 aop-21004-1 aop-21004-1 aop-21004-1 aop-21004-1 aop-21004-1 aop-21004-1 aop-21004-1 aop-21004-1 aop-21004-1 aop-21004-1:
        if aop(pz,21003,1) == 1:

            # Ograničenja vezana za vrstu i grupu obveznika - NEMA

            # Ogranicenja vezana za kombinovanje sa drugim predmetima zamene - NEMA
            if aop(pz,21004,1) == 1:
                if 'Izabrana je nedozvoljena kombinacija predmeta zamene!' not in form_errors:
                    
                    naziv_obrasca='Predmet zamene'
                    poruka  ='Izabrana je nedozvoljena kombinacija predmeta zamene!'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            # Provera dokumentacije za izabrani predmet zamene
            # Ako je označio aop-21004-1 MORA DA POSTOJI ULAZNI DOKUMENTI 4. 'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije' i 5. 'Izjašnjenje odgovornog lica o razlozima zamene' 
            #Prolazi kroz niz key-eva dictionary-ja i ako ispuni uslov inkrementira brojac
            brojacIspravnihPrilozenihDokumenata = 0
            for k in Zahtev.UlazniDokumenti.Keys:
                if Zahtev.UlazniDokumenti[k].Barkod != None:
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije':    
                        brojacIspravnihPrilozenihDokumenata += 1
            #Ako je brojac nula znaci da nije dodat odgovarajuci dokument i vraca se greska
            if brojacIspravnihPrilozenihDokumenata == 0:
                if 'Niste priložili dokument "Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije"' not in doc_errors:  
                    doc_errors.append('Niste priložili dokument "Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije"')

            brojacIspravnihPrilozenihDokumenata = 0
            for k in Zahtev.UlazniDokumenti.Keys:
                if Zahtev.UlazniDokumenti[k].Barkod != None:
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Izjašnjenje odgovornog lica o razlozima zamene':    
                        brojacIspravnihPrilozenihDokumenata += 1
            #Ako je brojac nula znaci da nije dodat odgovarajuci dokument i vraca se greska
            if brojacIspravnihPrilozenihDokumenata == 0:
                if 'Niste priložili dokument "Izjašnjenje odgovornog lica o razlozima zamene"' not in doc_errors:  
                    doc_errors.append('Niste priložili dokument "Izjašnjenje odgovornog lica o razlozima zamene"')

            #Ostali dokumenti ne smeju biti priloženi osim ako nisu izabrani odgovarajuci predmeti zamene
            for k in Zahtev.UlazniDokumenti.Keys:
                if Zahtev.UlazniDokumenti[k].Barkod != None:
                    # Dokument 1. 'Odluka o usvajanju finansijskog izveštaja' ne može biti priložen ako nije označen aop-21001-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Odluka o usvajanju finansijskog izveštaja':
                        if aop(pz,21001,1) == 0 and aop(pz,21002,1) == 0:
                            if 'Označeni dokument "Odluka o usvajanju finansijskog izveštaja" nije dozvoljen za izabrani predmet zamene' not in doc_errors:   
                                doc_errors.append('Označeni dokument "Odluka o usvajanju finansijskog izveštaja" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 3. 'Godišnji izveštaj o poslovanju izmenjene sadržine' ne može biti priložen ako nije označen aop-21003-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Godišnji izveštaj o poslovanju izmenjene sadržine':
                        if aop(pz,21005,1) == 0:
                            if 'Označeni dokument "Godišnji izveštaj o poslovanju izmenjene sadržine" nije dozvoljen za izabrani predmet zamene' not in doc_errors:   
                                doc_errors.append('Označeni dokument "Godišnji izveštaj o poslovanju izmenjene sadržine" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 4.'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije' se ne proverava u ovoj petlji
                    # Dokument 5.'Izjašnjenje odgovornog lica o razlozima zamene' se ne proverava u ovoj petlji

        ################################################################################################################################################################################
        ################################################################################################################################################################################


        ##### Ako je označen aop-21004-1 aop-21004-1 aop-21004-1 aop-21004-1 aop-21004-1 aop-21004-1 aop-21004-1 aop-21004-1 aop-21004-1 aop-21004-1 aop-21004-1 aop-21004-1 aop-21004-1:
        if aop(pz,21004,1) == 1:

            # Ograničenja vezana za vrstu i grupu obveznika - NEMA

            # Ogranicenja vezana za kombinovanje sa drugim predmetima zamene - NEMA
            if aop(pz,21003,1) == 1:
                if 'Izabrana je nedozvoljena kombinacija predmeta zamene!' not in form_errors:
                    
                    naziv_obrasca='Predmet zamene'
                    poruka  ='Izabrana je nedozvoljena kombinacija predmeta zamene!'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            # Provera dokumentacije za izabrani predmet zamene
            # Ako je označio aop-21004-1 MORA DA POSTOJI ULAZNI DOKUMENTI 4. 'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije' i 5. 'Izjašnjenje odgovornog lica o razlozima zamene' 
            #Prolazi kroz niz key-eva dictionary-ja i ako ispuni uslov inkrementira brojac
            brojacIspravnihPrilozenihDokumenata = 0
            for k in Zahtev.UlazniDokumenti.Keys:
                if Zahtev.UlazniDokumenti[k].Barkod != None:
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije':    
                        brojacIspravnihPrilozenihDokumenata += 1
            #Ako je brojac nula znaci da nije dodat odgovarajuci dokument i vraca se greska
            if brojacIspravnihPrilozenihDokumenata == 0:
                if 'Niste priložili dokument "Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije"' not in doc_errors:  
                    doc_errors.append('Niste priložili dokument "Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije"')

            brojacIspravnihPrilozenihDokumenata = 0
            for k in Zahtev.UlazniDokumenti.Keys:
                if Zahtev.UlazniDokumenti[k].Barkod != None:
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Izjašnjenje odgovornog lica o razlozima zamene':    
                        brojacIspravnihPrilozenihDokumenata += 1
            #Ako je brojac nula znaci da nije dodat odgovarajuci dokument i vraca se greska
            if brojacIspravnihPrilozenihDokumenata == 0:
                if 'Niste priložili dokument "Izjašnjenje odgovornog lica o razlozima zamene"' not in doc_errors:  
                    doc_errors.append('Niste priložili dokument "Izjašnjenje odgovornog lica o razlozima zamene"')

            #Ostali dokumenti ne smeju biti priloženi osim ako nisu izabrani odgovarajuci predmeti zamene
            for k in Zahtev.UlazniDokumenti.Keys:
                if Zahtev.UlazniDokumenti[k].Barkod != None:
                    # Dokument 1. 'Odluka o usvajanju finansijskog izveštaja' ne može biti priložen ako nije označen aop-21001-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Odluka o usvajanju finansijskog izveštaja':
                        if aop(pz,21001,1) == 0 and aop(pz,21002,1) == 0:
                            if 'Označeni dokument "Odluka o usvajanju finansijskog izveštaja" nije dozvoljen za izabrani predmet zamene' not in doc_errors:   
                                doc_errors.append('Označeni dokument "Odluka o usvajanju finansijskog izveštaja" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 3. 'Godišnji izveštaj o poslovanju izmenjene sadržine' ne može biti priložen ako nije označen aop-21003-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Godišnji izveštaj o poslovanju izmenjene sadržine':
                        if aop(pz,21005,1) == 0:
                            if 'Označeni dokument "Godišnji izveštaj o poslovanju izmenjene sadržine" nije dozvoljen za izabrani predmet zamene' not in doc_errors:   
                                doc_errors.append('Označeni dokument "Godišnji izveštaj o poslovanju izmenjene sadržine" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 4.'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije' se ne proverava u ovoj petlji
                    # Dokument 5.'Izjašnjenje odgovornog lica o razlozima zamene' se ne proverava u ovoj petlji

        ################################################################################################################################################################################


        ##### Ako je označen aop-21005-1 aop-21005-1 aop-21005-1 aop-21005-1 aop-21005-1 aop-21005-1 aop-21005-1 aop-21005-1 aop-21005-1 aop-21005-1 aop-21005-1 aop-21005-1 aop-21005-1:
        if aop(pz,21006,1) == 1:
            # Ograničenja vezana za vrstu i grupu obvznika  - NEMA

            # Ogranicenja vezana za kombinovanje sa drugim predmetima zamene  - NEMA

            # U aop-10001-1 MORA da unese bilo koji pozitivan ceo broj
            if not(aop_1(pz,10001,1) >= 0):
                
                naziv_obrasca='Predmet zamene'
                poruka  ="Podatak o prosečnom broju zaposlenih, u delu Posebni podaci, mora biti upisan; ako nema zaposlenih upisuje se broj 0"
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                naziv_obrasca='Posebni podaci'
                poruka  ="Podatak o prosečnom broju zaposlenih, u delu Posebni podaci, mora biti upisan; ako nema zaposlenih upisuje se broj 0"
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            #novo-2020-POCETAK
            # Funkcija aop_1() vraća -1 ako je polje prazno - dakle nije uneta vrednost
            if (aop_1(pz,10005,1)== -1):
                if 'Nije uneta veličina obveznika!' not in form_errors:  
                    
                    naziv_obrasca='Predmet zamene'
                    poruka  ='Nije uneta veličina obveznika!'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            # U aop-10005-1 može da unese SAMO 2, 3 ili 4
            if ( aop_1(pz,10005,1) != 2 and aop_1(pz,10005,1) != 3 and aop_1(pz,10005,1) != 4 and aop_1(pz,10005,1) != -1):
                if 'Uneta je neispravna vrednost za veličinu obveznika!' not in form_errors:  
                    
                    naziv_obrasca='Predmet zamene'
                    poruka  ='Uneta je neispravna vrednost za veličinu obveznika!'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            # Ako je preuzetnik ne može da unese 2, 3 ili 4
            if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
                if (aop_1(pz,10005,1) == 2 or aop_1(pz,10005,1) == 3 or aop_1(pz,10005,1) == 4):
                    if 'Uneta je neispravna vrednost za veličinu obveznika!' not in form_errors:  
                        
                        naziv_obrasca='Predmet zamene'
                        poruka  ='Uneta je neispravna vrednost za veličinu obveznika!'
                        aop_pozicije=[]
                        poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                        form_errors.append(poruka_obrasca)

            # Ako je grupa obveznika za liste mora da unese 4
            if (Zahtev.ObveznikInfo.GrupaObveznika.value__ in [2, 3, 4, 6, 10, 11, 12, 14, 15, 17, 18, 19, 20]):  #platne institucije - listu poslala Zorka
                if (aop_1(pz,10005,1) == 1 or aop_1(pz,10005,1) == 2 or aop_1(pz,10005,1) == 3):
                    if 'Uneta je neispravna vrednost za veličinu obveznika!' not in form_errors:  
                        
                        naziv_obrasca='Predmet zamene'
                        poruka  ='Uneta je neispravna vrednost za veličinu obveznika!'
                        aop_pozicije=[]
                        poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                        form_errors.append(poruka_obrasca)
 
            # # Ako veličina nije jedan i ako nije prazno polje (!= -1) a uneo je broj veći od 1000 prikazuje se upozorenje                  
            # if not (Zahtev.ObveznikInfo.VelicinaObveznika.value__ == 1):
            #     if aop_1(pz,10005,1) != -1:
            #         if not(aop_1(pz,10001,1) <= 1000):
                        
            #             naziv_obrasca='Predmet zamene'
            #             poruka  ="Prosečan broj zaposlenih je veći od 1.000; Granična vrednost data je da bi se izbegla slučajna greška prilikom iskazivanja broja zaposlenih;Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih;"
            #             aop_pozicije=[]
            #             poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            #             form_warnings.append(poruka_obrasca)
   
            # # Ako je veličina jedan i ako nije prazno polje (!= -1) a uneo je broj veći od 50 prikazuje se upozorenje                                  
            # if (Zahtev.ObveznikInfo.VelicinaObveznika.value__== 1):
            #     if aop_1(pz,10005,1) != -1:
            #         if not(aop_1(pz,10001,1) <= 50):
                        
            #             naziv_obrasca='Predmet zamene'
            #             poruka  ="Prosečan broj zaposlenih je veći od 50; Granična vrednost data je da bi se izbegla slučajna greška prilikom iskazivanja broja zaposlenih;Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih;"
            #             aop_pozicije=[]
            #             poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            #             form_warnings.append(poruka_obrasca)
            #novo-KRAJ
            
            # Provera dokumentacije za izabrani predmet zamene
            brojacIspravnihPrilozenihDokumenata = 0
            for k in Zahtev.UlazniDokumenti.Keys:
                if Zahtev.UlazniDokumenti[k].Barkod != None:
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Izjašnjenje odgovornog lica o razlozima zamene':    
                        brojacIspravnihPrilozenihDokumenata += 1
            #Ako je brojac nula znaci da nije dodat odgovarajuci dokument i vraca se greska
            if brojacIspravnihPrilozenihDokumenata == 0:
                if 'Niste priložili dokument "Izjašnjenje odgovornog lica o razlozima zamene"' not in doc_errors:  
                    doc_errors.append('Niste priložili dokument "Izjašnjenje odgovornog lica o razlozima zamene"')

            #Ostali dokumenti ne smeju biti priloženi osim ako nisu izabrani odgovarajuci predmeti zamene
            for k in Zahtev.UlazniDokumenti.Keys:
                if Zahtev.UlazniDokumenti[k].Barkod != None:
                    # Dokument 1. 'Odluka o usvajanju finansijskog izveštaja' ne može biti priložen ako nije označen aop-21001-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Odluka o usvajanju finansijskog izveštaja':
                        if aop(pz,21001,1) == 0 and aop(pz,21002,1) == 0:
                            if 'Označeni dokument "Odluka o usvajanju finansijskog izveštaja" nije dozvoljen za izabrani predmet zamene' not in doc_errors:   
                                doc_errors.append('Označeni dokument "Odluka o usvajanju finansijskog izveštaja" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 3. 'Godišnji izveštaj o poslovanju izmenjene sadržine' ne može biti priložen ako nije označen aop-21003-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Godišnji izveštaj o poslovanju izmenjene sadržine':
                        if aop(pz,21005,1) == 0:
                            if 'Označeni dokument "Godišnji izveštaj o poslovanju izmenjene sadržine" nije dozvoljen za izabrani predmet zamene' not in doc_errors:   
                                doc_errors.append('Označeni dokument "Godišnji izveštaj o poslovanju izmenjene sadržine" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 4.'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije' ne može biti priložen ako nije označen aop-21004-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije':
                        if aop(pz,21003,1) == 0 and aop(pz,21004,1) == 0:
                            if 'Označeni dokument "Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije" nije dozvoljen za izabrani predmet zamene' not in doc_errors:   
                                doc_errors.append('Označeni dokument "Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 5.'Izjašnjenje odgovornog lica o razlozima zamene' se ne proverava u ovoj petlji

        #### Ako NIJE označen aop-21006-1 obrazac ne može biti popunjen u delu posebni podaci - broj zaposlenih na nivou ekonomske celine
        else:
            if (aop_1(pz,10001,1) != -1):
                if 'Niste označili odgovarajući predmet zamene da biste mogli da popunite podatke o broju zaposlenih na nivou ekonomske celine u delu "Posebni podaci"' not in form_errors :
                    
                    naziv_obrasca='Predmet zamene'
                    poruka  ='Niste označili odgovarajući predmet zamene da biste mogli da popunite podatke o broju zaposlenih na nivou ekonomske celine u delu "Posebni podaci"'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    naziv_obrasca='Posebni podaci'
                    poruka  ='Niste označili odgovarajući predmet zamene da biste mogli da popunite podatke o broju zaposlenih na nivou ekonomske celine u delu "Posebni podaci"'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #NOVO 2019 pocetak
            if (aop_1(pz,10005,1) != -1):
                if 'Niste označili odgovarajući predmet zamene da biste mogli da popunite podatke u delu "Posebni podaci"' not in form_errors :
                    
                    naziv_obrasca='Predmet zamene'
                    poruka  ='Niste označili odgovarajući predmet zamene da biste mogli da popunite podatke u delu "Posebni podaci"'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    naziv_obrasca='Posebni podaci'
                    poruka  ='Niste označili odgovarajući predmet zamene da biste mogli da popunite podatke u delu "Posebni podaci"'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #kraj 

        ################################################################################################################################################################################

        pps=Zahtev.Forme['Predmet zamene'].TekstualnaPoljaForme

        #dodata ova dva reda (ppsnum otkomentarisan) 2019
        #pps=Zahtev.Forme['Posebni podaci'].TekstualnaPoljaForme
        ppsnum=Zahtev.Forme['Predmet zamene'].NumerickaPoljaForme
  
        ##### Ako je označen aop-21006-1 aop-21006-1 aop-21006-1 aop-21006-1 aop-21006-1 aop-21006-1 aop-21006-1 aop-21006-1 aop-21006-1 aop-21006-1 aop-21006-1 aop-21006-1 aop-21006-1:
        if aop(pz,21007,1) == 1:
            # Ograničenja vezana za vrstu i grupu obvznika  - NEMA

            # Ogranicenja vezana za kombinovanje sa drugim predmetima zamene  - NEMA
              
            # validiraj spisak zavisnih pravnih lica  
            for x in range (10100, 10300):
                if validiraj_spisak_pravnih_lica_obuhvacenih_konsolidacijom( x, aop(pps,x,2), aop(pps,x,3), aop(pps,x,4), aop(pps,x,5)) == False:
                    
                    naziv_obrasca='Posebni podaci'
                    poruka  ="Greška u obrascu Posebni podaci! Za domaće pravno lice unesite matični broj sa 8 cifara, poslovno ime  i sedište. Za strano pravno lice unesite poslovno ime, državu i sedište. (greška u redu: " + str(x-10099) + ")"
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    naziv_obrasca='Predmet zamene'
                    poruka  ="Greška u obrascu Posebni podaci! Za domaće pravno lice unesite matični broj sa 8 cifara, poslovno ime  i sedište. Za strano pravno lice unesite poslovno ime, državu i sedište. (greška u redu: " + str(x-10099) + ")"
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    
                
            #100003                               
            for x in range (10100, 10300):
                if aop(pps,x,5) == Zahtev.ObveznikInfo.MaticniBroj:
                    
                    naziv_obrasca='Posebni podaci'
                    poruka  ="Matično pravno lice ne može biti u spisku pravnih lica koja su obuhvaćena konsolidacijom! (Greška u redu: " + str(x-10099) + ")" 
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    
            #100004
            imaDuplikate = False                               
            for x in range (10100, 10300):
                for y in range (x, 10300):
                    if len(aop(pps,x,5)) != 0 and x != y and aop(pps,x,5) == aop(pps,y,5):
                        imaDuplikate = True
            if imaDuplikate:
                
                naziv_obrasca='Posebni podaci'
                poruka  ="Greška u obrascu Posebni podaci! Na spisak pravnih lica koja su obuhvaćena konsolidacijom ste uneli duplikate matičnih brojeva!"
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                

            #100008 Pravilo za kontrolu da li je unešen pravilno redni broj 
            for x in range (10100, 10300):
                if (aop(ppsnum, x, 1)!=0):
                    if not (aop(ppsnum, x, 1)==(x-10099)):
                        
                        naziv_obrasca='Posebni podaci'
                        poruka  ="Greška u obrascu Posebni podaci, u koloni Redni broj podatak nije unešen po rastućem redosledu. (Greška u redu: "+str(x-10099)+")"
                        aop_pozicije=[]
                        poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                        form_errors.append(poruka_obrasca)

            #100009 Obveznik mora uneti redni broj ukoliko je popunio podatke o zavisnom pravnom lici i obrnuto ukoliko je dodao redni broj da mora popuniti podatke o zavisnom pravnom licu.
            for x in range (10100, 10300):
                if (aop(ppsnum, x, 1) == 0):
                    if (validiraj_spisak_pravnih_lica( x, aop(pps,x,2), aop(pps,x,3), aop(pps,x,4), aop(pps,x,5))):
                        
                        naziv_obrasca='Posebni podaci'
                        poruka  ="U obrascu Posebni podaci, u Spisku pravnih lica obuhvaćenih konsolidacijom obveznik mora uneti redni broj ukoliko je popunio podatake o zavisnom pravnom licu i obrnuto ukoliko je dodao redni broj mora da popuni podatke o zavisnom pravnom licu. (Greška u redu: "+str(x-10099)+")"
                        aop_pozicije=[]
                        poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                        form_errors.append(poruka_obrasca)
                        
                    
            for x in range (10100, 10300):
                if (aop(ppsnum, x, 1) != 0 ):
                    if (validiraj_spisak_pravnih_lica( x, aop(pps,x,2), aop(pps,x,3), aop(pps,x,4), aop(pps,x,5))==False):
                        
                        naziv_obrasca='Posebni podaci'
                        poruka  ="U obrascu Posebni podaci, u Spisku pravnih lica obuhvaćenih konsolidacijom obveznik mora uneti redni broj ukoliko je popunio podatake o zavisnom pravnom licu i obrnuto ukoliko je dodao redni broj mora da popuni podatke o zavisnom pravnom licu. (Greška u redu: "+str(x-10099)+")"
                        aop_pozicije=[]
                        poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                        form_errors.append(poruka_obrasca)
                        

            #100011 kontrolno pravilo da korisnik ne sme da ostavi prazan red između validno unesenih redova
            for x in range(10100, 10300):
                if(aop(ppsnum, x, 1)==0):
                    if( x != 10299 and aop(ppsnum, x+1,1)!=0 ):
                        
                        naziv_obrasca='Posebni podaci'
                        poruka  ="GREŠKA U obrascu Posebni podaci, u Spisku pravnih lica obuhvaćenih konsolidacijom potrebno je popuniti kolonu “redni broj” po rastućem redosledu brojeva i bez preskakanja redova"
                        aop_pozicije=[]
                        poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                        form_errors.append(poruka_obrasca)
                        
            ##100012 prethodno pravilo bolje
            #lista=[]
            #for x in range(10100, 10300):
            #    if (aop(ppsnum, x, 1)!=0):
            #        lista.append(x)
            #if(max(lista)-10099 != len(lista)):
            #    form_errors.append("GREŠKA2 U obrascu Posebni podaci, u Spisku pravnih lica obuhvaćenih konsolidacijom potrebno je popuniti kolonu “redni broj” po rastućem redosledu brojeva i bez preskakanja redova MAX:"+str(max(lista)-10099)+" LEN:"+str(len(lista)))


                    
                   

            # Provera dokumentacije za izabrani predmet zamene
            brojacIspravnihPrilozenihDokumenata = 0
            for k in Zahtev.UlazniDokumenti.Keys:
                if Zahtev.UlazniDokumenti[k].Barkod != None:
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Izjašnjenje odgovornog lica o razlozima zamene':    
                        brojacIspravnihPrilozenihDokumenata += 1
            #Ako je brojac nula znaci da nije dodat odgovarajuci dokument i vraca se greska
            if brojacIspravnihPrilozenihDokumenata == 0:
                if 'Niste priložili dokument "Izjašnjenje odgovornog lica o razlozima zamene"' not in doc_errors:  
                    doc_errors.append('Niste priložili dokument "Izjašnjenje odgovornog lica o razlozima zamene"')

            #Ostali dokumenti ne smeju biti priloženi osim ako nisu izabrani odgovarajuci predmeti zamene
            for k in Zahtev.UlazniDokumenti.Keys:
                if Zahtev.UlazniDokumenti[k].Barkod != None:
                    # Dokument 1. 'Odluka o usvajanju finansijskog izveštaja' ne može biti priložen ako nije označen aop-21001-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Odluka o usvajanju finansijskog izveštaja':
                        if aop(pz,21001,1) == 0 and aop(pz,21002,1) == 0:
                            if 'Označeni dokument "Odluka o usvajanju finansijskog izveštaja" nije dozvoljen za izabrani predmet zamene' not in doc_errors:   
                                doc_errors.append('Označeni dokument "Odluka o usvajanju finansijskog izveštaja" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 3. 'Godišnji izveštaj o poslovanju izmenjene sadržine' ne može biti priložen ako nije označen aop-21003-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Godišnji izveštaj o poslovanju izmenjene sadržine':
                        if aop(pz,21005,1) == 0:
                            if 'Označeni dokument "Godišnji izveštaj o poslovanju izmenjene sadržine" nije dozvoljen za izabrani predmet zamene' not in doc_errors:   
                                doc_errors.append('Označeni dokument "Godišnji izveštaj o poslovanju izmenjene sadržine" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 4.'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije' ne može biti priložen ako nije označen aop-21004-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije':
                        if aop(pz,21003,1) == 0 and aop(pz,21003,1) == 0:
                            if 'Označeni dokument "Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije" nije dozvoljen za izabrani predmet zamene' not in doc_errors:   
                                doc_errors.append('Označeni dokument "Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 5.'Izjašnjenje odgovornog lica o razlozima zamene' se ne proverava u ovoj petlji

        #### Ako NIJE označen aop-21007-1 obrazac ne može biti popunjen u delu posebni podaci - spisak pravnih lica koja su obuhvaćena konsolidacijom
        else:
            u_spisku_pravnih_lica_postoji_unos = False

            for x in range (10100, 10300):
                if len(aop(pps,x,2)) > 0 or len(aop(pps,x,3)) > 0 or len(aop(pps,x,4)) > 0 or len(aop(pps,x,5)) > 0: 
                    u_spisku_pravnih_lica_postoji_unos = True
            
            if u_spisku_pravnih_lica_postoji_unos == True:
                if 'Niste označili odgovarajući predmet zamene da biste mogli da popunite spisak pravnih lica koja su obuhvaćena konsolidacijom u delu "Posebni podaci"' not in form_errors :
                    
                    naziv_obrasca='Posebni podaci'
                    poruka  ='Niste označili odgovarajući predmet zamene da biste mogli da popunite spisak pravnih lica koja su obuhvaćena konsolidacijom u delu "Posebni podaci"'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    
                    
                    
                    naziv_obrasca='Predmet zamene'
                    poruka  ='Niste označili odgovarajući predmet zamene da biste mogli da popunite spisak pravnih lica koja su obuhvaćena konsolidacijom u delu "Posebni podaci"'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

        ################################################################################################################################################################################

        ##### Ako je označen aop-21007-1 aop-21007-1 aop-21007-1 aop-21007-1 aop-21007-1 aop-21007-1 aop-21007-1 aop-21007-1 aop-21007-1 aop-21007-1 aop-21007-1 aop-21007-1 aop-21007-1:
        if aop(pz,21002,1) == 1:

            # Ograničenja vezana za vrstu i grupu obvznika - NEMA ---------------------------------------------------------------------------------------------------------------------

            # Ogranicenja vezana za kombinovanje sa drugim predmetima zamene - ne moze istovremeno da oznaci AOP-e aop-21007-1
            if aop(pz,21001,1) == 1:
                if 'Izabrana je nedozvoljena kombinacija predmeta zamene!' not in form_errors:
                    
                    naziv_obrasca='Predmet zamene'
                    poruka  ='Izabrana je nedozvoljena kombinacija predmeta zamene!'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            # Provera dokumentacije za izabrani predmet zamene ------------------------------------------------------------------------------------------------------------------------
            # Ako je označio aop-21001-1 MORA DA POSTOJI ULAZNI DOKUMENT 1. 'Одлука о усвајању финансијског извештаја'
            # Prolazi kroz niz key-eva dictionary-ja i ako ispuni uslov inkrementira brojac
            brojacIspravnihPrilozenihDokumenata = 0
            for k in Zahtev.UlazniDokumenti.Keys:
                if Zahtev.UlazniDokumenti[k].Barkod != None:
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Odluka o usvajanju finansijskog izveštaja':    
                        brojacIspravnihPrilozenihDokumenata += 1
            # Ako je brojac nula znaci da nije dodat odgovarajuci dokument i vraca se greska
            if brojacIspravnihPrilozenihDokumenata == 0:
                if 'Niste priložili dokument "Odluka o usvajanju finansijskog izveštaja"' not in doc_errors:  
                    doc_errors.append('Niste priložili dokument "Odluka o usvajanju finansijskog izveštaja"')

            brojacIspravnihPrilozenihDokumenata = 0
            for k in Zahtev.UlazniDokumenti.Keys:
                if Zahtev.UlazniDokumenti[k].Barkod != None:
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Izjašnjenje odgovornog lica o razlozima zamene':    
                        brojacIspravnihPrilozenihDokumenata += 1
            #Ako je brojac nula znaci da nije dodat odgovarajuci dokument i vraca se greska
            if brojacIspravnihPrilozenihDokumenata == 0:
                if 'Niste priložili dokument "Izjašnjenje odgovornog lica o razlozima zamene"' not in doc_errors:  
                    doc_errors.append('Niste priložili dokument "Izjašnjenje odgovornog lica o razlozima zamene"')
                                     
            #Ostali dokumenti ne smeju biti priloženi osim ako nisu izabrani odgovarajuci predmeti zamene
            for k in Zahtev.UlazniDokumenti.Keys:
                if Zahtev.UlazniDokumenti[k].Barkod != None:
                    # Dokument 1. 'Odluka o usvajanju finansijskog izveštaja' se ne proverava u ovoj petlji
                    # Dokument 3. 'Godišnji izveštaj o poslovanju izmenjene sadržine' ne može biti priložen ako nije označen aop-21003-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Godišnji izveštaj o poslovanju izmenjene sadržine':
                        if aop(pz,21005,1) == 0:
                            if 'Označeni dokument "Godišnji izveštaj o poslovanju izmenjene sadržine" nije dozvoljen za izabrani predmet zamene' not in doc_errors:   
                                doc_errors.append('Označeni dokument "Godišnji izveštaj o poslovanju izmenjene sadržine" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 4.'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije' ne može biti priložen ako nije označen aop-21004-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije':
                        if aop(pz,21003,1) == 0 and aop(pz,21004,1) == 0:
                            if 'Označeni dokument "Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije" nije dozvoljen za izabrani predmet zamene' not in doc_errors:   
                                doc_errors.append('Označeni dokument "Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije" nije dozvoljen za izabrani predmet zamene')


        ################################################################################################################################################################################

        ################################################################################################################################################################################               
        ### KRAJ PROVERA ZA SVAKI AOP ##################################################################################################################################################
        ################################################################################################################################################################################


        ###########################################################
        ###########################################################
        #### KRAJ KONTROLNIH PRAVILA  - VRACA SVE KOLEKCIJE  ######
        ###########################################################
        ###########################################################

        return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors, 'exceptions' : exceptionList}

    except Exception as e:
        #trace = traceback.format_exc()
        trace=''
        errorMsg = e.message

        exceptionList.append({'errorMessage':errorMsg, 'trace':trace})
        
        return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors, 'exceptions' : exceptionList}