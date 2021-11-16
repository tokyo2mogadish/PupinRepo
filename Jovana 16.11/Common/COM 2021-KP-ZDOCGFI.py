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
        raise Exception('Obrazac pod nazivom '+nazivForme+' ne postoji')

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

        
        # Provera da li lice odgovorno za sastavljanje je upisano
        if (Zahtev.LiceOdgovornoZaSastavljanje is None):
            ostalo_errors.append('Podaci za lice odgovorno za sastavljanje finansijskog izveštaja nisu upisani.')

        # Provera da li lice odgovorno za potpisivanje #################################################################################################################################
        if (len(Zahtev.Potpisnici) == 0):
            ostalo_errors.append('Podaci o potpisniku finansijskog izveštaja nisu upisani.')                   

        # Provera da li su prosledjeni obavezni ulazni dokumenti #######################################################################################################################
        if (Zahtev.ValidacijaUlaznihDokumenataOmoguceno==True):
            if (Zahtev.NacinPodnosenja.value__ == 1):
                if Zahtev.UlazniDokumenti.Count>0:
                    for k in Zahtev.UlazniDokumenti.Keys:
                        if Zahtev.UlazniDokumenti[k].Obavezan==True and Zahtev.UlazniDokumenti[k].Barkod == None:
                            doc_errors.append('Dokument sa nazivom "'+Zahtev.UlazniDokumenti[k].Naziv+'" niste priložili.') 

        # # Provera da li je za papirne bar jedan dokument barkodiran ####################################################################################################################      
        # if (Zahtev.ValidacijaUlaznihDokumenataOmoguceno==True):
        #     if Zahtev.NacinPodnosenja.value__ == 3:
        #         if Zahtev.UlazniDokumenti.Count>0:
        #             nDocWithBarCode = 0
        #             for k in Zahtev.UlazniDokumenti.Keys:
        #                 if Zahtev.UlazniDokumenti[k].Barkod != None and Zahtev.UlazniDokumenti[k].Obavezan==False:
        #                     nDocWithBarCode += 1
        #             if nDocWithBarCode == 0:
        #                 doc_errors.append('Morate dodati bar jedan ulazni dokument.')                       
                         
        
     
        # Provera da li zahtev do sada ima form_errors, ako ima odmah vraca greske, bey obyira na nacin podnosenja i stanje#############################################################
        if (len(form_errors)>0):            
            return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors, 'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings,'exceptions': exceptionList}
        
        
        
        ################################################################################################################################################################################ 
        ################################################################################################################################################################################
        ### POCETAK KONTROLNIH PRAVILA #################################################################################################################################################
        ################################################################################################################################################################################
        ################################################################################################################################################################################

        ### Provera da li je fizahtev placen ###########################################################################################################################################
        if not(Zahtev.Placen):
            ostalo_errors.append('Naknada za obradu i javno objavljivanje zahteva za zamenu dokumentacije nije uplaćena u propisanom iznosu. Instrukcije za uplatu propisane naknade date su u okviru PIS FI sistema za konkretan zahtev, na linku „Status naplate zahteva / Instrukcija za plaćanje". Ukoliko ste izvršili uplatu, a naknada nije uparena, priložite Dokaz o uplati naknade u delu Dokumentacija (na mestu predviđenom za dokaz o uplati naknade), kako biste mogli da podnesete izveštaj.');
        ################################################################################################################################################################################

        ############## Polje može biti prazno ili u njega mogu biti uneti vrednosti 0 ili 1. U drugom slučaju vraća grešku. Metoda aop() vraca 0 ako je polje prazno ###################      
        neispravanUnosBrojac = 0
        if (aop(pz,20001,1) != 0 and aop(pz,20001,1) != 1):
            neispravanUnosBrojac += 1
        if (aop(pz,20002,1) != 0 and aop(pz,20002,1) != 1):
            neispravanUnosBrojac += 1
        if (aop(pz,20003,1) != 0 and aop(pz,20003,1) != 1):
            neispravanUnosBrojac += 1
        if (aop(pz,20004,1) != 0 and aop(pz,20004,1) != 1):
           neispravanUnosBrojac += 1
        if (aop(pz,20005,1) != 0 and aop(pz,20005,1) != 1):
           neispravanUnosBrojac += 1
        # if (aop(pz,20006,1) != 0 and aop(pz,20006,1) != 1):
        #     neispravanUnosBrojac += 1
        # if (aop(pz,20007,1) != 0 and aop(pz,20007,1) != 1):
        #     neispravanUnosBrojac += 1
        # if (aop(pz,20008,1) != 0 and aop(pz,20008,1) != 1):
        #     neispravanUnosBrojac += 1
        # if (aop(pz,20009,1) != 0 and aop(pz,20009,1) != 1):
        #     neispravanUnosBrojac += 1
        if neispravanUnosBrojac > 0:
            naziv_obrasca='Predmet zamene'
            poruka  ='Vrednosti u poljima forme mogu biti samo brojevi 0 ili 1'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        ################################################################################################################################################################################

        ### Proverava da li je uzabran bar jedan predmet zamene #######################################################################################################################
        if suma_liste(pz, [20001, 20002, 20003, 20004, 20005], 1) == 0:
            naziv_obrasca='Predmet zamene'
            poruka  ='Izaberite predmet zamene!'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        ################################################################################################################################################################################


        ### POCETAK PROVERA ZA SVAKI AOP ##############################################################################################################################################
        ################################################################################################################################################################################

        ### Ako je označen aop-20001-1 aop-20001-1 aop-20001-1 aop-20001-1 aop-20001-1 aop-20001-1 aop-20001-1 aop-20001-1 aop-20001-1 aop-20001-1 aop-20001-1 aop-20001-1 aop-20001-1:
        if aop(pz,20001,1) == 1:

            # Ogranicenja vezana za vrstu i grupu obveznika - ne primenjuju PREDZETNICI -------------------------------------------------------------
            # if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            # if 'Izabrani predmet zamene nije dozvoljen za preduzetnike!' not in form_errors:
            #     naziv_obrasca='Predmet zamene'
            #     poruka  ='Izabrani predmet zamene nije dozvoljen za preduzetnike!'
            #     aop_pozicije=[]
            #     poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}  
            #     form_errors.append(poruka_obrasca) 

            # Ogranicenja vezana za kombinovanje sa drugim predmetima zamene - ne moze istovremeno da oznaci AOP-e aop-20009-1
            if aop(pz,20002,1) == 1:
                if 'Izabrana je nedozvoljena kombinacija predmeta zamene!' not in form_errors:
                    naziv_obrasca='Predmet zamene'
                    poruka  ='Izabrana je nedozvoljena kombinacija predmeta zamene!'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}  
                    form_errors.append(poruka_obrasca) 

            # Provera dokumentacije za izabrani predmet zamene --------------------------------------------------------------------------------------
            # Ako je označio aop-20001-1 MORA DA POSTOJI ULAZNI DOKUMENT 1. 'Одлука о усвајању финансијског извештаја'                                 
            #Prolazi kroz niz key-eva dictionary-ja i ako ispuni uslov inkrementira brojac
            brojacIspravnihPrilozenihDokumenata = 0
            for k in Zahtev.UlazniDokumenti.Keys:
                if Zahtev.UlazniDokumenti[k].Barkod != None:
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Odluka o usvajanju finansijskog izveštaja':    
                        brojacIspravnihPrilozenihDokumenata += 1
            #Ako je brojac nula znaci da nije dodat odgovarajuci dokument i vraca se greska
            if brojacIspravnihPrilozenihDokumenata == 0:
                if 'Niste priložili dokument "Odluka o usvajanju finansijskog izveštaja"' not in doc_errors:  
                    
                    doc_errors.append('Niste priložili dokument "Odluka o usvajanju finansijskog izveštaja"')

            #Ostali dokumenti ne smeju biti priloženi osim ako nisu izabrani odgovarajuci predmeti zamene
            for k in Zahtev.UlazniDokumenti.Keys:
                if Zahtev.UlazniDokumenti[k].Barkod != None:
                    # Dokument 1. 'Odluka o usvajanju finansijskog izveštaja' se ne proverava u ovoj petlji
                    # Dokument 2. 'Odluka o raspodeli dobiti odnosno pokriću gubitka' ne može biti priložen ako nije označen aop-20002-1 ili aop-20003-1
                    # if Zahtev.UlazniDokumenti[k].Naziv == 'Odluka o raspodeli dobiti odnosno pokriću gubitka':
                    if aop(pz,20002,1) == 0 and aop(pz,20003,1) == 0:
                        if 'Označeni dokument "Odluka o raspodeli dobiti odnosno pokriću gubitka" nije dozvoljen za izabrani predmet zamene' not in doc_errors:  
                            
                            doc_errors.append('Označeni dokument "Odluka o raspodeli dobiti odnosno pokriću gubitka" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 5.'Godišnji izveštaj o poslovanju izmenjene sadržine' ne može biti priložen ako nije označen aop-20006-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Godišnji izveštaj o poslovanju izmenjene sadržine':
                        if aop(pz,20005,1) == 0:
                            if 'Označeni dokument "Godišnji izveštaj o poslovanju izmenjene sadržine" nije dozvoljen za izabrani predmet zamene' not in doc_errors:
                                 
                                doc_errors.append('Označeni dokument "Godišnji izveštaj o poslovanju izmenjene sadržine" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 6.'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije' ne može biti priložen ako nije označen aop-20007-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije':
                        if aop(pz,20003,1) == 0 and aop(pz,20004,1) == 0:
                            if 'Označeni dokument "Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije" nije dozvoljen za izabrani predmet zamene' not in doc_errors:   
                                
                                doc_errors.append('Označeni dokument "Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije" nije dozvoljen za izabrani predmet zamene') 
                    # Dokument 7.'Izjašnjenje odgovornog lica o razlozima zamene' ne može biti priložen ako nije označen aop-20003-1, aop-20006-1, aop-20007-1, aop-20008-1 ili aop-20009-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Izjašnjenje odgovornog lica o razlozima zamene':
                        if aop(pz,20002,1) == 0 and aop(pz,20003,1) == 0 and aop(pz,20004,1) == 0 and aop(pz,20005,1) == 0 :
                            if 'Označeni dokument "Izjašnjenje odgovornog lica o razlozima zamene" nije dozvoljen za izabrani predmet zamene' not in doc_errors:
                                
                                doc_errors.append('Označeni dokument "Izjašnjenje odgovornog lica o razlozima zamene" nije dozvoljen za izabrani predmet zamene') 

        ################################################################################################################################################################################
 
                                                      
        # ### Ako je označen aop-20002-1 aop-20002-1 aop-20002-1 aop-20002-1 aop-20002-1 aop-20002-1 aop-20002-1 aop-20002-1 aop-20002-1 aop-20002-1 aop-20002-1 aop-20002-1 aop-20002-1:
        # if aop(pz,20002,1) == 1:

        #     # Ogranicenja vezana za vrstu i grupu obveznika - ne primenjuju PREDZETNICI
        #     # if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
        #     if 'Izabrani predmet zamene nije dozvoljen za preduzetnike!' not in form_errors:
        #         naziv_obrasca='Predmet zamene'
        #         poruka  ='Izabrani predmet zamene nije dozvoljen za preduzetnike!'
        #         aop_pozicije=[]
        #         poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}   
        #         form_errors.append(poruka_obrasca)  

        #     # Ogranicenja vezana za kombinovanje sa drugim predmetima zamene - ne moze istovremeno da oznaci AOP-e aop-20002-1
        #     if aop(pz,20001,1) == 1:
        #         if 'Izabrana je nedozvoljena kombinacija predmeta zamene!' not in form_errors:
        #             naziv_obrasca='Predmet zamene'
        #             poruka  ='Izabrana je nedozvoljena kombinacija predmeta zamene!'
        #             aop_pozicije=[]
        #             poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}   
        #             form_errors.append(poruka_obrasca) 
                    
        #     # Provera dokumentacije za izabrani predmet zamene --------------------------------------------------------------------------------------------------------------aop-20002-1
        #     # Ako je označio aop-20003-1 MORA DA POSTOJI ULAZNI DOKUMENT 2. 'Odluka o raspodeli dobiti odnosno pokriću gubitka'                                  
        #     #Prolazi kroz niz key-eva dictionary-ja i ako ispuni uslov inkrementira brojac
        #     brojacIspravnihPrilozenihDokumenata = 0
        #     for k in Zahtev.UlazniDokumenti.Keys:
        #         if Zahtev.UlazniDokumenti[k].Barkod != None:
        #             if Zahtev.UlazniDokumenti[k].Naziv == 'Odluka o usvajanju finansijskog izveštaja':    
        #                 brojacIspravnihPrilozenihDokumenata += 1
        #     #Ako je brojac nula znaci da nije dodat odgovarajuci dokument i vraca se greska
        #     if brojacIspravnihPrilozenihDokumenata == 0:
        #         if 'Niste priložili dokument "Odluka o usvajanju finansijskog izveštaja"' not in doc_errors:  
                     
        #             doc_errors.append('Niste priložili dokument "Odluka o usvajanju finansijskog izveštaja"')

        #     #Ostali dokumenti ne smeju biti priloženi osim ako nisu izabrani odgovarajuci predmeti zamene
        #     for k in Zahtev.UlazniDokumenti.Keys:
        #         if Zahtev.UlazniDokumenti[k].Barkod != None:
        #             # Dokument 1. 'Одлука о усвајању финансијског извештаја' ne može biti priložen ako nije označen aop-20001-1
        #             # if Zahtev.UlazniDokumenti[k].Naziv == 'Odluka o usvajanju finansijskog izveštaja':
        #             #     if aop(pz,20001,1) == 0 and aop(pz,20009,1) == 0:
        #             #         if 'Označeni dokument "Odluka o usvajanju finansijskog izveštaja" nije dozvoljen za izabrani predmet zamene' not in doc_errors:
                                
        #             #             doc_errors.append('Označeni dokument "Odluka o usvajanju finansijskog izveštaja" nije dozvoljen za izabrani predmet zamene')
        #             # Dokument 2. 'Odluka o raspodeli dobiti odnosno pokriću gubitka' se ne proverava u ovoj petlji
        #             # Dokument 5.'Godišnji izveštaj o poslovanju izmenjene sadržine' ne može biti priložen ako nije označen aop-20006-1
        #             if Zahtev.UlazniDokumenti[k].Naziv == 'Godišnji izveštaj o poslovanju izmenjene sadržine':
        #                 if aop(pz,20005,1) == 0:
        #                     if 'Označeni dokument "Godišnji izveštaj o poslovanju izmenjene sadržine" nije dozvoljen za izabrani predmet zamene' not in doc_errors: 
                                  
        #                         doc_errors.append('Označeni dokument "Godišnji izveštaj o poslovanju izmenjene sadržine" nije dozvoljen za izabrani predmet zamene')
        #             # Dokument 6.'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije' ne može biti priložen ako nije označen aop-20007-1
        #             if Zahtev.UlazniDokumenti[k].Naziv == 'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije':
        #                 if aop(pz,20003,1) == 0 and aop(pz,20004,1) == 0:
        #                     if 'Označeni dokument "Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije" nije dozvoljen za izabrani predmet zamene' not in doc_errors:  
                                
        #                         doc_errors.append('Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije" nije dozvoljen za izabrani predmet zamene') 
        #             # Dokument 7.'Izjašnjenje odgovornog lica o razlozima zamene' ne može biti priložen ako nije označen aop-20003-1, aop-20006-1, aop-20007-1, aop-20008-1 ili aop-20009-1
        #             if Zahtev.UlazniDokumenti[k].Naziv == 'Izjašnjenje odgovornog lica o razlozima zamene':
        #                 if aop(pz,20002,1) == 0 and aop(pz,20003,1) == 0 and aop(pz,20004,1) == 0 and aop(pz,20005,1) == 0:
        #                     if 'Označeni dokument "Izjašnjenje odgovornog lica o razlozima zamene" nije dozvoljen za izabrani predmet zamene' not in doc_errors: 
                                  
        #                         doc_errors.append('Označeni dokument "Izjašnjenje odgovornog lica o razlozima zamene" nije dozvoljen za izabrani predmet zamene') 
                                                                  
        ################################################################################################################################################################################

                                                        
        ### Ako je označen aop-20003-1 aop-20003-1 aop-20003-1 aop-20003-1 aop-20003-1 aop-20003-1 aop-20003-1 aop-20003-1 aop-20003-1 aop-20003-1 aop-20003-1 aop-20003-1 aop-20003-1:
        if aop(pz,20002,1) == 1:

            # Ogranicenja vezana za vrstu i grupu  obveznika - ne primenjuju PREDZETNICI
            # if (Zahtev.ObveznikInfo.GrupaObveznika.value__ == 8):
            #     if 'Izabrani predmet zamene nije dozvoljen za preduzetnike!' not in form_errors: 
            #         naziv_obrasca='Predmet zamene'
            #         poruka  ='Izabrani predmet zamene nije dozvoljen za preduzetnike!'
            #         aop_pozicije=[]
            #         poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}  
            #         form_errors.append(poruka_obrasca) 

            # Ogranicenja vezana za kombinovanje sa drugim predmetima zamene - ne moze istovremeno da oznaci AOP-e aop-20002-1
            if aop(pz,20001,1) == 1:
                if 'Izabrana je nedozvoljena kombinacija predmeta zamene!' not in form_errors:
                    naziv_obrasca='Predmet zamene'
                    poruka  ='Izabrana je nedozvoljena kombinacija predmeta zamene!'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije} 
                    form_errors.append(poruka_obrasca)  

            # Provera dokumentacije za izabrani predmet zamene --------------------------------------------------------------------------------------
            # Ako je označio aop-20003-1 MORA DA POSTOJI ULAZNI DOKUMENTI 2. 'Odluka o raspodeli dobiti odnosno pokriću gubitka' i 8. 'Izjašnjenje odgovornog lica o razlozima zamene'                               
            #Prolazi kroz niz key-eva dictionary-ja i ako ispuni uslov inkrementira brojac
            brojacIspravnihPrilozenihDokumenata = 0
            for k in Zahtev.UlazniDokumenti.Keys:
                if Zahtev.UlazniDokumenti[k].Barkod != None:
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Odluka o usvajanju finansijskog izveštaja':    
                        brojacIspravnihPrilozenihDokumenata += 1
            #Ako je brojac nula znaci da nije dodat odgovarajuci dokument i vraca se greska
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
                    # # Dokument 1. 'Одлука о усвајању финансијског извештаја' ne može biti priložen ako nije označen aop-20001-1
                    # if Zahtev.UlazniDokumenti[k].Naziv == 'Odluka o usvajanju finansijskog izveštaja':
                    #     if aop(pz,20001,1) == 0 and aop(pz,20009,1) == 0:
                    #         if 'Označeni dokument "Odluka o usvajanju finansijskog izveštaja" nije dozvoljen za izabrani predmet zamene' not in doc_errors:  
                                
                    #             doc_errors.append('Označeni dokument "Odluka o usvajanju finansijskog izveštaja" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 2. 'Odluka o raspodeli dobiti odnosno pokriću gubitka' se ne proverava u ovoj petlji
                    # Dokument 5.'Godišnji izveštaj o poslovanju izmenjene sadržine' ne može biti priložen ako nije označen aop-20006-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Godišnji izveštaj o poslovanju izmenjene sadržine':
                        if aop(pz,20005,1) == 0:
                            if 'Označeni dokument "Godišnji izveštaj o poslovanju izmenjene sadržine" nije dozvoljen za izabrani predmet zamene' not in doc_errors: 
                                 
                                doc_errors.append('Označeni dokument "Godišnji izveštaj o poslovanju izmenjene sadržine" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 6.'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije' ne može biti priložen ako nije označen aop-20007-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije':
                        if aop(pz,20003,1) == 0 and aop(pz,20004,1) == 0:
                            if 'Označeni dokument "Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije" nije dozvoljen za izabrani predmet zamene' not in doc_errors:
                                
                                doc_errors.append('Označeni dokument "Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije" nije dozvoljen za izabrani predmet zamene') 

        ################################################################################################################################################################################

                                                           
        ### Ako je označen aop-20006-1 aop-20006-1 aop-20006-1 aop-20006-1 aop-20006-1 aop-20006-1 aop-20006-1 aop-20006-1 aop-20006-1 aop-20006-1 aop-20006-1 aop-20006-1 aop-20006-1:
        if aop(pz,20005,1) == 1:

            # Ogranicenja vezana za vrstu i grupu obveznika - primenjuju samo velika pravna lica i/ili javna drustva
            if (Zahtev.ObveznikInfo.PodgrupaObveznika.value__ != 79 and Zahtev.ObveznikInfo.VelicinaObveznika.value__ != 4 and Zahtev.ObveznikInfo.VelicinaObveznika.value__ != 3):
                if 'Godišnji izveštaj o poslovanju je dozvoljen samo za velika pravna lica i javna društva' not in form_errors: 
                    naziv_obrasca='Predmet zamene'
                    poruka  ='Godišnji izveštaj o poslovanju je dozvoljen samo za velika i srednja pravna lica i sva javna društva'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}    
                    form_errors.append(poruka_obrasca) 

            # Ogranicenja vezana za kombinovanje sa drugim predmetima zamene - NEMA 
 
            # Provera dokumentacije za izabrani predmet zamene ------------------------------------------------------------------------------------------------------------------------
            # Ako je označio aop-20006-1 MORA DA POSTOJI ULAZNI DOKUMENTI 5. 'Godišnji izveštaj o poslovanju izmenjene sadržine' i 8. 'Izjašnjenje odgovornog lica o razlozima zamene'                               
            #Prolazi kroz niz key-eva dictionary-ja i ako ispuni uslov inkrementira brojac
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
                    # Dokument 1. 'Одлука о усвајању финансијског извештаја' ne može biti priložen ako nije označen aop-20001-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Odluka o usvajanju finansijskog izveštaja':
                        if aop(pz,20001,1) == 0 and aop(pz,20002,1) == 0:
                            if 'Označeni dokument "Odluka o usvajanju finansijskog izveštaja" nije dozvoljen za izabrani predmet zamene' not in doc_errors:  
                                
                                doc_errors.append('Označeni dokument "Odluka o usvajanju finansijskog izveštaja" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 2. 'Odluka o raspodeli dobiti odnosno pokriću gubitka' ne može biti priložen ako nije označen aop-20002-1 ili aop-20003-1
                    # if Zahtev.UlazniDokumenti[k].Naziv == 'Odluka o raspodeli dobiti odnosno pokriću gubitka':
                    #     if aop(pz,20002,1) == 0 and aop(pz,20003,1) == 0:
                    #         if 'Označeni dokument "Odluka o raspodeli dobiti odnosno pokriću gubitka" nije dozvoljen za izabrani predmet zamene' not in doc_errors:
                                 
                    #             doc_errors.append('Označeni dokument "Odluka o raspodeli dobiti odnosno pokriću gubitka" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 5. 'Godišnji izveštaj o poslovanju izmenjene sadržine' se ne proverava u ovoj petlji
                    # Dokument 6.'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije' ne može biti priložen ako nije označen aop-20007-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije':
                        if aop(pz,20003,1) == 0 and aop(pz,20004,1) == 0:
                            if 'Označeni dokument "Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije" nije dozvoljen za izabrani predmet zamene' not in doc_errors:    
                                doc_errors.append('Označeni dokument "Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije" nije dozvoljen za izabrani predmet zamene') 

        ################################################################################################################################################################################
                                          
        ### Ako je označen aop-20007-1 aop-20007-1 aop-20007-1 aop-20007-1 aop-20007-1 aop-20007-1 aop-20007-1 aop-20007-1 aop-20007-1 aop-20007-1 aop-20007-1 aop-20007-1 aop-20007-1:
        if aop(pz,20003,1) == 1:
        
            # Ogranicenja vezana za vrstu i grupu obveznika - primenjuju samo obveznici revizije
            if (Zahtev.ObveznikInfo.ObveznikRevizije != True):
                if 'Zamena finansijskog izveštaja koji je bio predmet revizije dozvoljena je samo za obveznike revizije' not in form_errors: 
                    naziv_obrasca='Predmet zamene'
                    poruka  ='Zamena finansijskog izveštaja koji je bio predmet revizije dozvoljena je samo za obveznike revizije'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}  
                    form_errors.append(poruka_obrasca) 

            if aop(pz,20004,1) == 1:
                if 'Izabrana je nedozvoljena kombinacija predmeta zamene!' not in form_errors:
                    naziv_obrasca='Predmet zamene'
                    poruka  ='Izabrana je nedozvoljena kombinacija predmeta zamene!'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}  
                    form_errors.append(poruka_obrasca) 
 

            # Provera dokumentacije za izabrani predmet zamene -------------------------------------------------------------------------------------------------------------------------
            # Ako je označio aop-20007-1 MORA DA POSTOJE ULAZNI DOKUMENTI 6. 'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije' i 8. 'Izjašnjenje odgovornog lica o razlozima zamene'                               
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
                    # Dokument 1. 'Одлука о усвајању финансијског извештаја' ne može biti priložen ako nije označen aop-20001-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Odluka o usvajanju finansijskog izveštaja':
                        if aop(pz,20001,1) == 0 and aop(pz,20002,1) == 0:
                            if 'Označeni dokument "Odluka o usvajanju finansijskog izveštaja" nije dozvoljen za izabrani predmet zamene' not in doc_errors:
                                  
                                doc_errors.append('Označeni dokument "Odluka o usvajanju finansijskog izveštaja" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 2. 'Odluka o raspodeli dobiti odnosno pokriću gubitka' ne može biti priložen ako nije označen aop-20002-1 ili aop-20003-1
                    # if Zahtev.UlazniDokumenti[k].Naziv == 'Odluka o raspodeli dobiti odnosno pokriću gubitka':
                    #     if aop(pz,20002,1) == 0 and aop(pz,20003,1) == 0:
                    #         if 'Označeni dokument "Odluka o raspodeli dobiti odnosno pokriću gubitka" nije dozvoljen za izabrani predmet zamene' not in doc_errors:  
                                
                    #             doc_errors.append('Označeni dokument "Odluka o raspodeli dobiti odnosno pokriću gubitka" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 5.'Godišnji izveštaj o poslovanju izmenjene sadržine' ne može biti priložen ako nije označen aop-20006-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Godišnji izveštaj o poslovanju izmenjene sadržine':
                        if aop(pz,20005,1) == 0:
                            if 'Označeni dokument "Godišnji izveštaj o poslovanju izmenjene sadržine" nije dozvoljen za izabrani predmet zamene' not in doc_errors:
                                
                                doc_errors.append('Označeni dokument "Godišnji izveštaj o poslovanju izmenjene sadržine" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 6. 'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije' se ne proverava u ovoj petlji

        ################################################################################################################################################################################
             
                                                           
        ### Ako je označen aop-20007-1 aop-20007-1 aop-20007-1 aop-20007-1 aop-20007-1 aop-20007-1 aop-20007-1 aop-20007-1 aop-20007-1 aop-20007-1 aop-20007-1 aop-20007-1 aop-20007-1:
        if aop(pz,20004,1) == 1:
        
            # Ogranicenja vezana za vrstu i grupu obveznika - primenjuju samo obveznici revizije
            if (Zahtev.ObveznikInfo.ObveznikRevizije != True):
                if 'Zamena finansijskog izveštaja koji je bio predmet revizije dozvoljena je samo za obveznike revizije' not in form_errors: 
                    naziv_obrasca='Predmet zamene'
                    poruka  ='Zamena finansijskog izveštaja koji je bio predmet revizije dozvoljena je samo za obveznike revizije'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}  
                    form_errors.append(poruka_obrasca) 

            if aop(pz,20003,1) == 1:
                if 'Izabrana je nedozvoljena kombinacija predmeta zamene!' not in form_errors:
                    naziv_obrasca='Predmet zamene'
                    poruka  ='Izabrana je nedozvoljena kombinacija predmeta zamene!'
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}  
                    form_errors.append(poruka_obrasca) 
 

            # Provera dokumentacije za izabrani predmet zamene -------------------------------------------------------------------------------------------------------------------------
            # Ako je označio aop-20007-1 MORA DA POSTOJE ULAZNI DOKUMENTI 6. 'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije' i 8. 'Izjašnjenje odgovornog lica o razlozima zamene'                               
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
                    # Dokument 1. 'Одлука о усвајању финансијског извештаја' ne može biti priložen ako nije označen aop-20001-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Odluka o usvajanju finansijskog izveštaja':
                        if aop(pz,20001,1) == 0 and aop(pz,20002,1) == 0:
                            if 'Označeni dokument "Odluka o usvajanju finansijskog izveštaja" nije dozvoljen za izabrani predmet zamene' not in doc_errors:
                                  
                                doc_errors.append('Označeni dokument "Odluka o usvajanju finansijskog izveštaja" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 2. 'Odluka o raspodeli dobiti odnosno pokriću gubitka' ne može biti priložen ako nije označen aop-20002-1 ili aop-20003-1
                    # if Zahtev.UlazniDokumenti[k].Naziv == 'Odluka o raspodeli dobiti odnosno pokriću gubitka':
                    #     if aop(pz,20002,1) == 0 and aop(pz,20003,1) == 0:
                    #         if 'Označeni dokument "Odluka o raspodeli dobiti odnosno pokriću gubitka" nije dozvoljen za izabrani predmet zamene' not in doc_errors:  
                                
                    #             doc_errors.append('Označeni dokument "Odluka o raspodeli dobiti odnosno pokriću gubitka" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 5.'Godišnji izveštaj o poslovanju izmenjene sadržine' ne može biti priložen ako nije označen aop-20006-1
                    if Zahtev.UlazniDokumenti[k].Naziv == 'Godišnji izveštaj o poslovanju izmenjene sadržine':
                        if aop(pz,20005,1) == 0:
                            if 'Označeni dokument "Godišnji izveštaj o poslovanju izmenjene sadržine" nije dozvoljen za izabrani predmet zamene' not in doc_errors:
                                
                                doc_errors.append('Označeni dokument "Godišnji izveštaj o poslovanju izmenjene sadržine" nije dozvoljen za izabrani predmet zamene')
                    # Dokument 6. 'Revizorski izveštaj sa odgovarajućim finansijskim izveštajem koji je bio predmet revizije' se ne proverava u ovoj petlji

        ################################################################################################################################################################################
 
        ################################################################################################################################################################################               
        ### KRAJ PROVERA ZA SVAKI AOP ##################################################################################################################################################
        ################################################################################################################################################################################
                                                                                                                         
        ################################################################################################################################################################################
        ################################################################################################################################################################################
        # KRAJ KONTROLNIH PRAVILA  - VRACA SVE KOLEKCIJE  ##############################################################################################################################
        ################################################################################################################################################################################
        ################################################################################################################################################################################

        return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}

    except Exception as e:
        #trace = traceback.format_exc() #traceback.print_tb(sys.exc_info()[2])
        trace=''
        errorMsg = e.message

        exceptionList.append({'errorMessage':errorMsg, 'trace':trace})
        
        return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}

 
        